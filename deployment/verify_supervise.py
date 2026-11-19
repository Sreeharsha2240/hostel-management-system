"""Database-free supervisor checks: python -m unittest deployment.verify_supervise."""

import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from deployment import supervise


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.root = self.folder / "private"
        self.root.mkdir()
        release = self.folder / "source"
        (release / "deployment").mkdir(parents=True)
        (release / "deployment" / "windows.py").write_text("", encoding="utf-8")
        self.config = {
            "schema_version": 1,
            "root": str(self.root),
            "release": str(release),
            "tunnel_id": "12345678-1234-5678-1234-567812345678",
        }
        for name in supervise.PATH_KEYS - {"root", "release"}:
            path = self.root / name
            path.write_text("", encoding="utf-8")
            self.config[name] = str(path)
        self.runtime = {
            "DJANGO_SECRET_KEY": "supervisor-unit-test-secret-with-many-different-characters-12345",
            "DB_NAME": "hms_public",
            "DB_USER": "app_user",
            "DB_PASSWORD": "private-value",
            "DB_HOST": "127.0.0.1",
            "DB_PORT": "33081",
            "HMS_PORT": 8110,
        }
        Path(self.config["runtime_config"]).write_text(
            json.dumps(self.runtime), encoding="utf-8"
        )
        self.server_text = (
            "[mysqld]\nbind-address=127.0.0.1\nport=33081\nmysqlx=0\n"
            f"datadir={(self.root / 'mysql-data').as_posix()}\n"
        )
        Path(self.config["mysql_config"]).write_text(self.server_text, encoding="utf-8")
        Path(self.config["mysql_client_config"]).write_text(
            "[client]\nhost=127.0.0.1\nport=33081\nuser=root\npassword=private-root-value\n",
            encoding="utf-8",
        )
        self.operations = self.root / "operations.json"
        self.write_operations()

    def write_operations(self):
        self.operations.write_text(json.dumps(self.config), encoding="utf-8")

    def loaded(self):
        return supervise.load_operations(self.operations)

    def supervisor(self):
        supervisor = supervise.Supervisor(self.loaded())
        self.addCleanup(supervisor.events.close)
        return supervisor

    def test_config_accepts_dedicated_loopback_and_no_preflight_mutation(self):
        with (
            patch.object(supervise.subprocess, "Popen") as popen,
            patch.object(supervise.subprocess, "run") as run,
        ):
            self.assertEqual(
                supervise.main(["--config", str(self.operations), "--check"]), 0
            )
        popen.assert_not_called()
        run.assert_not_called()
        self.assertFalse((self.root / "logs").exists())
        self.assertEqual(self.loaded()["database_port"], 33081)

    def test_unsafe_paths_and_runtime_hosts_are_rejected(self):
        for key in supervise.PRIVATE_KEYS:
            with self.subTest(key=key):
                original = self.config[key]
                self.config[key] = str(self.folder / "outside")
                self.write_operations()
                with self.assertRaises(supervise.ConfigurationError):
                    self.loaded()
                self.config[key] = original
        self.write_operations()
        self.runtime["DB_HOST"] = "0.0.0.0"
        Path(self.config["runtime_config"]).write_text(
            json.dumps(self.runtime), encoding="utf-8"
        )
        with self.assertRaises(supervise.ConfigurationError):
            self.loaded()

    def test_mysql_networking_and_private_datadir_are_required(self):
        for original, replacement in (
            ("bind-address=127.0.0.1", "bind-address=0.0.0.0"),
            ("mysqlx=0", "mysqlx=1"),
            ("port=33081", "port=3306"),
            ((self.root / "mysql-data").as_posix(), self.folder.as_posix()),
        ):
            with self.subTest(replacement=replacement):
                Path(self.config["mysql_config"]).write_text(
                    self.server_text.replace(original, replacement), encoding="utf-8"
                )
                with self.assertRaises(supervise.ConfigurationError):
                    self.loaded()

    def test_option_file_includes_are_rejected(self):
        Path(self.config["mysql_config"]).write_text(
            self.server_text + "!include elsewhere.ini\n", encoding="utf-8"
        )
        with self.assertRaises(supervise.ConfigurationError):
            self.loaded()

    def test_defaults_and_other_mysql_groups_cannot_override_networking(self):
        inherited = "[DEFAULT]\nbind-address=127.0.0.1\n" + self.server_text.replace(
            "bind-address=127.0.0.1\n", ""
        )
        for text in (
            inherited,
            "[DEFAULT]\n" + self.server_text,
            self.server_text + "[server]\nbind-address=0.0.0.0\n",
            self.server_text + "[mysqld-8.4]\nbind-address=0.0.0.0\n",
        ):
            with self.subTest(text=text):
                Path(self.config["mysql_config"]).write_text(text, encoding="utf-8")
                with self.assertRaises(supervise.ConfigurationError):
                    self.loaded()

    def test_unknown_mysql_aliases_and_canonical_duplicates_are_rejected(self):
        for option in (
            "loose-bind-address=0.0.0.0",
            "enable-named-pipe",
            "skip-networking=off",
            "bind_address=127.0.0.1",
            "MYSQLX=1",
        ):
            with self.subTest(option=option):
                Path(self.config["mysql_config"]).write_text(
                    self.server_text + option + "\n", encoding="utf-8"
                )
                with self.assertRaises(supervise.ConfigurationError):
                    self.loaded()

    def test_client_extra_groups_and_non_tcp_protocol_are_rejected(self):
        path = Path(self.config["mysql_client_config"])
        original = path.read_text(encoding="utf-8")
        for extra in ("protocol=PIPE\n", "[mysqladmin]\nhost=other-machine\n"):
            with self.subTest(extra=extra):
                path.write_text(original + extra, encoding="utf-8")
                with self.assertRaises(supervise.ConfigurationError):
                    self.loaded()

    def test_exclusive_lock_rejects_a_second_supervisor_and_releases(self):
        path = self.root / "supervisor.lock"
        with supervise.exclusive_lock(path):
            with self.assertRaises(OSError), supervise.exclusive_lock(path):
                self.fail("Duplicate supervisor acquired the lock")
        with supervise.exclusive_lock(path):
            pass

    def test_backup_is_atomic_and_retention_happens_only_after_success(self):
        supervisor = self.supervisor()
        folder = self.root / "backups"
        for index in range(15):
            (folder / f"hms-old-{index:02}.sql").write_text(
                "old backup", encoding="utf-8"
            )

        def dump(command, **kwargs):
            self.assertTrue(command[1].startswith("--defaults-file="))
            self.assertEqual(
                command[2:6],
                [
                    "--no-login-paths",
                    "--protocol=TCP",
                    "--host=127.0.0.1",
                    "--port=33081",
                ],
            )
            self.assertIn("--single-transaction", command)
            self.assertIn("--no-tablespaces", command)
            self.assertEqual(command[-1], "hms_public")
            self.assertFalse(any("private-root-value" in value for value in command))
            self.assertEqual(len(list(folder.glob("hms-*.sql"))), 15)
            kwargs["stdout"].write(b"-- complete deterministic test dump\n")
            return SimpleNamespace(returncode=0)

        with patch.object(supervise.subprocess, "run", side_effect=dump):
            supervisor.backup()
        self.assertEqual(len(list(folder.glob("hms-*.sql"))), 14)
        self.assertEqual(list(folder.glob("*.partial")), [])
        before = set(folder.iterdir())
        with patch.object(
            supervise.subprocess, "run", return_value=SimpleNamespace(returncode=1)
        ):
            with self.assertRaises(RuntimeError):
                supervisor.backup()
        self.assertEqual(set(folder.iterdir()), before)

    def test_admin_readiness_requires_status_and_hides_credentials(self):
        supervisor = self.supervisor()
        with patch.object(
            supervise.subprocess, "run", return_value=SimpleNamespace(returncode=1)
        ) as run:
            self.assertFalse(supervisor.admin("status"))
        command = run.call_args.args[0]
        self.assertEqual(command[-1], "status")
        self.assertTrue(command[1].startswith("--defaults-file="))
        self.assertEqual(
            command[2:6],
            ["--no-login-paths", "--protocol=TCP", "--host=127.0.0.1", "--port=33081"],
        )
        self.assertNotIn("private-root-value", " ".join(command))

    def test_shutdown_uses_only_owned_handles_and_database_admin_first(self):
        supervisor = self.supervisor()
        order = []
        for name in ("database", "application", "tunnel"):
            child = Mock()
            child.poll.return_value = None
            child.terminate.side_effect = lambda name=name: order.append(name)
            child.wait.return_value = 0
            supervisor.children[name] = child
        with patch.object(
            supervisor,
            "admin",
            side_effect=lambda operation: order.append(operation) or True,
        ):
            supervisor.stop_children()
        self.assertEqual(order, ["tunnel", "application", "shutdown"])
        self.assertEqual(supervisor.children, {})

    def test_dead_owned_database_is_never_shutdown_via_an_unowned_port(self):
        supervisor = self.supervisor()
        child = Mock()
        child.poll.return_value = 1
        supervisor.children["database"] = child
        with patch.object(supervisor, "admin") as admin:
            supervisor.stop_children()
        admin.assert_not_called()
        child.kill.assert_not_called()

    def test_stop_request_is_latched_and_starts_no_processes(self):
        supervisor = self.supervisor()
        (self.root / "stop.request").touch()
        with patch.object(supervise.subprocess, "Popen") as popen:
            self.assertEqual(supervisor.run(), 0)
        popen.assert_not_called()
        self.assertTrue((self.root / "stop.request").exists())

    def test_launch_failure_closes_log_and_does_not_create_owned_handle(self):
        supervisor = self.supervisor()
        with patch.object(
            supervise.subprocess, "Popen", side_effect=OSError("private-value")
        ):
            with self.assertRaises(OSError):
                supervisor.start("application", ["unused"])
        self.assertEqual(supervisor.children, {})
        self.assertEqual(supervisor.streams, {})

    def test_hung_child_is_killed_only_after_owned_shutdown_timeout(self):
        supervisor = self.supervisor()
        child = Mock()
        child.poll.return_value = None
        child.wait.side_effect = [subprocess.TimeoutExpired("owned", 30), 0]
        supervisor.children["application"] = child
        supervisor.stop_children()
        child.terminate.assert_called_once_with()
        child.kill.assert_called_once_with()

    def test_failed_cleanup_keeps_handle_so_restart_cannot_duplicate_it(self):
        supervisor = self.supervisor()
        child = Mock()
        child.poll.return_value = None
        child.wait.side_effect = subprocess.TimeoutExpired("owned", 30)
        supervisor.children["application"] = child
        supervisor.stop_children()
        self.assertIs(supervisor.children["application"], child)

    def test_startup_orders_readiness_backup_app_and_named_tunnel(self):
        supervisor = self.supervisor()
        actions = []

        def start(name, command):
            actions.append((name, command))
            child = Mock()
            child.poll.return_value = None
            supervisor.children[name] = child

        with (
            patch.object(supervisor, "start", side_effect=start),
            patch.object(supervisor, "admin", return_value=True),
            patch.object(supervisor, "require_free_port"),
            patch.object(
                supervisor,
                "wait_ready",
                side_effect=lambda name, probe: actions.append(("ready", name)),
            ),
            patch.object(
                supervisor, "backup", side_effect=lambda: actions.append(("backup",))
            ),
            patch.object(
                supervisor,
                "pause",
                side_effect=lambda seconds: supervisor.stopping.set(),
            ),
        ):
            self.assertEqual(supervisor.run(), 0)
        self.assertEqual(
            [entry[0] for entry in actions],
            ["database", "ready", "backup", "application", "ready", "tunnel"],
        )
        database_command = actions[0][1]
        self.assertTrue(database_command[1].startswith("--defaults-file="))
        app_command = actions[3][1]
        self.assertEqual(app_command[1:4], ["-m", "deployment.windows", "--config"])
        tunnel_command = actions[-1][1]
        self.assertEqual(tunnel_command[1:3], ["tunnel", "--config"])
        self.assertEqual(tunnel_command[-2:], ["run", self.config["tunnel_id"]])
        self.assertNotIn("--token", tunnel_command)

    def test_startup_retries_with_backoff_without_printing_exception_secrets(self):
        supervisor = self.supervisor()
        delays = []

        def pause(seconds):
            delays.append(seconds)
            if len(delays) == 2:
                supervisor.stopping.set()

        with (
            patch.object(
                supervisor,
                "require_free_port",
                side_effect=RuntimeError("private-value"),
            ),
            patch.object(supervisor, "pause", side_effect=pause),
        ):
            self.assertEqual(supervisor.run(), 0)
        self.assertEqual(delays, [1, 2])
        log = (self.root / "logs" / "supervisor.log").read_text(encoding="utf-8")
        self.assertNotIn("private-value", log)
        self.assertIn("RuntimeError", log)

    def test_running_child_logs_rotate_without_newlines_or_process_restarts(self):
        payload = b"long-output-without-any-newline-" * 300
        child = Mock()
        child.stdout = io.BytesIO(payload)
        child.poll.return_value = 0
        with (
            patch.object(supervise, "MAX_LOG_BYTES", 128),
            patch.object(supervise, "LOG_CHUNK_BYTES", 32),
            patch.object(supervise.subprocess, "Popen", return_value=child) as popen,
        ):
            supervisor = self.supervisor()
            supervisor.start("tunnel", ["unused-test-executable"])
            supervisor.stop_children()
        popen.assert_called_once()
        self.assertEqual(popen.call_args.kwargs["stdout"], subprocess.PIPE)
        child.terminate.assert_not_called()
        self.assertEqual(supervisor.readers, {})
        self.assertEqual(supervisor.streams, {})
        self.assertTrue(child.stdout.closed)
        logs = list((self.root / "logs").glob("tunnel.log*"))
        self.assertEqual(len(logs), 5)
        self.assertTrue(all(path.stat().st_size <= 160 for path in logs))
        retained = b"".join(
            (self.root / "logs" / name).read_bytes()
            for name in (
                "tunnel.log.4",
                "tunnel.log.3",
                "tunnel.log.2",
                "tunnel.log.1",
                "tunnel.log",
            )
        )
        self.assertTrue(payload.endswith(retained))

    def test_supervisor_event_log_rotates_during_one_running_session(self):
        with patch.object(supervise, "MAX_LOG_BYTES", 180):
            supervisor = self.supervisor()
            for number in range(100):
                supervisor.event(f"event number {number}")
        logs = list((self.root / "logs").glob("supervisor.log*"))
        self.assertEqual(len(logs), 5)
        self.assertTrue(all(path.stat().st_size <= 180 for path in logs))
        self.assertIn(
            "event number 99",
            (self.root / "logs" / "supervisor.log").read_text(encoding="utf-8"),
        )

    def test_logging_io_failure_does_not_echo_child_output_or_stop_draining(self):
        self.supervisor()
        handler = supervise.rotating_log(
            self.root / "logs" / "io-failure.log", raw=True
        )
        self.addCleanup(handler.close)
        pipe = io.BytesIO(b"private-value" * 5000)
        with (
            patch.object(handler.stream, "write", side_effect=OSError("disk full")),
            patch.object(supervise.sys, "stderr", new_callable=io.StringIO) as stderr,
        ):
            supervise.drain_output(pipe, handler)
        self.assertTrue(pipe.closed)
        self.assertEqual(stderr.getvalue(), "")

    def test_output_decoder_preserves_utf8_across_chunk_boundaries(self):
        self.supervisor()
        handler = supervise.rotating_log(self.root / "logs" / "utf8.log", raw=True)
        self.addCleanup(handler.close)
        payload = "hello \u20b9 \u2603 \U0001f600" * 50
        with patch.object(supervise, "LOG_CHUNK_BYTES", 7):
            supervise.drain_output(io.BytesIO(payload.encode("utf-8")), handler)
        self.assertEqual(
            (self.root / "logs" / "utf8.log").read_text(encoding="utf-8"), payload
        )


if __name__ == "__main__":
    unittest.main()
