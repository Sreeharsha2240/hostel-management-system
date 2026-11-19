"""Supervise the private Windows laptop deployment as the signed-in user.

Run ``python -m deployment.supervise --config <private-root>/operations.json``.
Schema version 1 requires absolute paths named root, release, python,
runtime_config, mysqld, mysqladmin, mysqldump, mysql_config,
mysql_client_config, cloudflared, tunnel_config, and a UUID tunnel_id.
The config itself and all state, logs, data, and backups stay under root.
Provision root with user/SYSTEM-only ACLs before running this module.
Creating root/stop.request requests shutdown and stays latched until the
operator explicitly removes it. --check only reads configuration.
"""

from __future__ import annotations

import argparse
import codecs
import configparser
import ctypes
import json
import logging
import os
import re
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from uuid import UUID, uuid4

from deployment.windows import ConfigurationError, load_config

PATH_KEYS = frozenset(
    {
        "root",
        "release",
        "python",
        "runtime_config",
        "mysqld",
        "mysqladmin",
        "mysqldump",
        "mysql_config",
        "mysql_client_config",
        "cloudflared",
        "tunnel_config",
    }
)
PRIVATE_KEYS = {
    "runtime_config",
    "mysql_config",
    "mysql_client_config",
    "tunnel_config",
}
MAX_LOG_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 4
LOG_CHUNK_BYTES = 16 * 1024
MYSQL_OPTIONS = {
    "mysqld": {
        "datadir",
        "bind-address",
        "port",
        "mysqlx",
        "character-set-server",
        "collation-server",
        "max-connections",
        "local-infile",
        "skip-name-resolve",
        "log-error",
    },
    "client": {"host", "port", "protocol", "user", "password"},
}


class BasicJobLimits(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", ctypes.c_uint32),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", ctypes.c_uint32),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", ctypes.c_uint32),
        ("SchedulingClass", ctypes.c_uint32),
    ]


class JobIoCounters(ctypes.Structure):
    _fields_ = [
        (name, ctypes.c_uint64)
        for name in (
            "ReadOperationCount",
            "WriteOperationCount",
            "OtherOperationCount",
            "ReadTransferCount",
            "WriteTransferCount",
            "OtherTransferCount",
        )
    ]


class ExtendedJobLimits(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", BasicJobLimits),
        ("IoInfo", JobIoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class WindowsProcessJob:
    """Own the supervisor and all descendants, including launcher wrappers.

    Assigning ourselves before spawning avoids a child/grandchild assignment
    race. The unnamed, noninheritable job handle dies with the supervisor even
    on forced termination; Windows then terminates the entire associated tree.
    """

    def __init__(self, kernel=None):
        self.kernel = kernel or ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([ctypes.c_void_p, ctypes.c_wchar_p], ctypes.c_void_p),
            "SetInformationJobObject": (
                [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32],
                ctypes.c_int,
            ),
            "AssignProcessToJobObject": (
                [ctypes.c_void_p, ctypes.c_void_p],
                ctypes.c_int,
            ),
            "GetCurrentProcess": ([], ctypes.c_void_p),
            "CloseHandle": ([ctypes.c_void_p], ctypes.c_int),
        }
        for name, (arguments, result) in signatures.items():
            method = getattr(self.kernel, name)
            method.argtypes = arguments
            method.restype = result
        self.handle = self.kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise OSError("Cannot create the supervisor process job.")
        try:
            self._limits(kill_on_close=True)
            if not self.kernel.AssignProcessToJobObject(
                self.handle, self.kernel.GetCurrentProcess()
            ):
                raise OSError("Cannot isolate the supervisor process tree.")
        except BaseException:
            self.kernel.CloseHandle(self.handle)
            self.handle = None
            raise

    def _limits(self, *, kill_on_close: bool):
        limits = ExtendedJobLimits()
        limits.BasicLimitInformation.LimitFlags = 0x2000 if kill_on_close else 0
        if not self.kernel.SetInformationJobObject(
            self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            raise OSError("Cannot configure supervisor process-tree cleanup.")

    def close(self, *, disarm: bool):
        if self.handle and disarm:
            self._limits(kill_on_close=False)
            handle, self.handle = self.handle, None
            self.kernel.CloseHandle(handle)
        # On an unclean exit retain the raw Win32 handle until ExitProcess.
        # Closing the armed self-job here could terminate us before our nonzero
        # exit status reaches Task Scheduler. There is deliberately no __del__.


def within(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ConfigurationError("A private deployment path leaves its root.")
    return resolved


def mysql_options(path: Path, section: str) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    if any(line.lstrip().startswith("!") for line in text.splitlines()):
        raise ConfigurationError("MySQL option-file includes are not supported.")
    parser = configparser.ConfigParser(interpolation=None, allow_no_value=True)
    parser.optionxform = str
    parser.read_string(text)
    if (
        parser.defaults()
        or re.search(r"^\s*\[DEFAULT\]\s*(?:[#;].*)?$", text, re.MULTILINE)
        or set(parser.sections()) != {section}
    ):
        raise ConfigurationError(
            "MySQL options must use exactly their owned section without defaults."
        )
    options = {}
    for key, value in parser[section].items():
        canonical = key.lower().replace("_", "-")
        if canonical not in MYSQL_OPTIONS[section] or canonical in options:
            raise ConfigurationError(
                "MySQL options contain an unsupported or duplicate setting."
            )
        options[canonical] = (value or "").strip().strip("\"'")
    return options


def load_operations(path: Path) -> dict:
    path = path.resolve()
    if path.stat().st_size > 65536:
        raise ConfigurationError("The operations config is too large.")
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    if (
        not isinstance(config, dict)
        or type(config.get("schema_version")) is not int
        or config.get("schema_version") != 1
    ):
        raise ConfigurationError("Expected operations schema_version 1.")
    if set(config) != PATH_KEYS | {"schema_version", "tunnel_id"}:
        raise ConfigurationError("The operations config has missing or unknown keys.")
    for key in PATH_KEYS:
        value = config[key]
        if not isinstance(value, str) or not Path(value).is_absolute():
            raise ConfigurationError("Every deployment path must be absolute.")
        config[key] = Path(value).resolve()
    root = config["root"]
    if root != path.parent or not root.is_dir():
        raise ConfigurationError(
            "The operations config must reside directly in its root."
        )
    for key in PRIVATE_KEYS:
        within(root, config[key])
    for name in ("logs", "backups", "supervisor.lock", "stop.request"):
        within(root, root / name)
    for key in PATH_KEYS - {"root", "release"}:
        if not config[key].is_file():
            raise ConfigurationError("A required deployment file is missing.")
    if not (config["release"] / "deployment" / "windows.py").is_file():
        raise ConfigurationError(
            "The source release does not contain the Windows launcher."
        )
    try:
        config["tunnel_id"] = str(UUID(config["tunnel_id"]))
    except (TypeError, ValueError, AttributeError) as error:
        raise ConfigurationError("tunnel_id must be a named tunnel UUID.") from error
    environment, port = load_config(config["runtime_config"])
    if environment["DB_HOST"] != "127.0.0.1":
        raise ConfigurationError("The dedicated database must bind to IPv4 loopback.")
    if not re.fullmatch(r"[A-Za-z0-9_]+", environment["DB_NAME"]):
        raise ConfigurationError(
            "DB_NAME must contain only letters, digits, or underscores."
        )
    database_port = int(environment["DB_PORT"])
    if database_port == port:
        raise ConfigurationError("The database and application ports must differ.")
    server = mysql_options(config["mysql_config"], "mysqld")
    client = mysql_options(config["mysql_client_config"], "client")
    if (
        server.get("bind-address") != "127.0.0.1"
        or server.get("port") != str(database_port)
        or server.get("mysqlx", "").lower() not in {"0", "off", "false"}
        or client.get("host") != "127.0.0.1"
        or client.get("port") != str(database_port)
        or client.get("protocol", "tcp").lower() != "tcp"
        or not client.get("user")
        or not client.get("password")
    ):
        raise ConfigurationError(
            "MySQL configs must select the dedicated loopback port and disable mysqlx."
        )
    data = Path(server.get("datadir", ""))
    if not data.is_absolute() or within(root, data) == root:
        raise ConfigurationError("MySQL datadir must be a private subdirectory.")
    for name in ("log-error", "pid-file"):
        if name in server:
            within(root, Path(server[name]))
    config.update(
        database_name=environment["DB_NAME"], database_port=database_port, port=port
    )
    return config


@contextmanager
def exclusive_lock(path: Path):
    """Hold an OS lock for the supervisor lifetime; stale files are harmless."""
    stream = path.open("a+b")
    locked = False
    try:
        if path.stat().st_size == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:  # Allows the same safety tests on Linux without opening listeners.
            import fcntl

            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        locked = True
        yield
    finally:
        if locked and os.name == "nt":
            import msvcrt

            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        stream.close()


class PrivateRotatingHandler(RotatingFileHandler):
    def handleError(self, record):
        # Logging failures must not echo child output or credentials to stderr.
        # The pipe reader keeps draining so a full disk cannot deadlock a child.
        pass


def rotating_log(path: Path, *, raw: bool = False) -> RotatingFileHandler:
    handler = PrivateRotatingHandler(
        path,
        maxBytes=MAX_LOG_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
        errors="replace",
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    if raw:
        handler.terminator = ""
    return handler


def drain_output(pipe, handler: RotatingFileHandler):
    """Read bounded chunks, including arbitrarily long lines, until child EOF."""
    decoder = codecs.getincrementaldecoder("utf-8")("replace")
    try:
        while data := pipe.read(LOG_CHUNK_BYTES):
            message = decoder.decode(data)
            if message:
                handler.handle(logging.makeLogRecord({"msg": message}))
        remaining = decoder.decode(b"", final=True)
        if remaining:
            handler.handle(logging.makeLogRecord({"msg": remaining}))
    except (OSError, ValueError):
        pass
    finally:
        pipe.close()


class Supervisor:
    def __init__(self, config: dict):
        self.config = config
        self.root = config["root"]
        self.stopping = threading.Event()
        self.children: dict[str, subprocess.Popen] = {}
        self.streams: dict[str, RotatingFileHandler] = {}
        self.readers: dict[str, threading.Thread] = {}
        self.force_tree_cleanup = False
        for name in ("logs", "backups"):
            within(self.root, self.root / name).mkdir(exist_ok=True)
        self.events = rotating_log(
            within(self.root, self.root / "logs" / "supervisor.log")
        )

    def event(self, message: str):
        self.events.handle(
            logging.makeLogRecord({"msg": f"{datetime.now(UTC).isoformat()} {message}"})
        )

    def stopped(self) -> bool:
        return self.stopping.is_set() or (self.root / "stop.request").exists()

    def pause(self, seconds: float):
        deadline = time.monotonic() + seconds
        while not self.stopped() and time.monotonic() < deadline:
            self.stopping.wait(min(0.5, max(0, deadline - time.monotonic())))

    def start(self, name: str, command: list[str]):
        log = within(self.root, self.root / "logs" / f"{name}.log")
        stream = rotating_log(log, raw=True)
        try:
            child = subprocess.Popen(
                command,
                cwd=self.config["release"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        except BaseException:
            stream.close()
            raise
        self.children[name] = child
        self.streams[name] = stream
        reader = threading.Thread(
            target=drain_output, args=(child.stdout, stream), daemon=True
        )
        reader.start()
        self.readers[name] = reader
        self.event(f"started {name}")

    def admin(self, operation: str) -> bool:
        try:
            result = subprocess.run(
                [
                    str(self.config["mysqladmin"]),
                    f"--defaults-file={self.config['mysql_client_config']}",
                    "--no-login-paths",
                    "--protocol=TCP",
                    "--host=127.0.0.1",
                    f"--port={self.config['database_port']}",
                    "--connect-timeout=3",
                    operation,
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                check=False,
            )
            return result.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False

    def wait_ready(self, name: str, probe, seconds: float = 60):
        deadline = time.monotonic() + seconds
        while not self.stopped() and time.monotonic() < deadline:
            if self.children[name].poll() is not None:
                self.force_tree_cleanup = True
                raise RuntimeError("A managed child exited before readiness.")
            if probe() and self.children[name].poll() is None:
                return
            self.pause(0.5)
        raise RuntimeError("Readiness timed out or shutdown was requested.")

    def application_ready(self) -> bool:
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.config['port']}/login/",
            headers={"Host": "se.d3va.dev", "X-Forwarded-Proto": "https"},
        )
        try:
            # Never follow redirects to the public host during an origin probe.
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({}), NoRedirect()
            )
            with opener.open(request, timeout=3) as response:
                return response.status == 200
        except (OSError, urllib.error.URLError):
            return False

    def require_free_port(self, port: int):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                raise RuntimeError(
                    "A required local port already has an unmanaged listener."
                )
        except (ConnectionRefusedError, TimeoutError):
            pass

    def backup(self):
        folder = within(self.root, self.root / "backups")
        filename = (
            datetime.now(UTC).strftime("hms-%Y%m%dT%H%M%S") + f"-{uuid4().hex[:8]}.sql"
        )
        final = within(self.root, folder / filename)
        temporary = final.with_suffix(".partial")
        try:
            with temporary.open("xb") as stream:
                result = subprocess.run(
                    [
                        str(self.config["mysqldump"]),
                        f"--defaults-file={self.config['mysql_client_config']}",
                        "--no-login-paths",
                        "--protocol=TCP",
                        "--host=127.0.0.1",
                        f"--port={self.config['database_port']}",
                        "--single-transaction",
                        "--quick",
                        "--no-tablespaces",
                        "--set-gtid-purged=OFF",
                        self.config["database_name"],
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=stream,
                    stderr=subprocess.DEVNULL,
                    timeout=300,
                    check=False,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
                stream.flush()
                os.fsync(stream.fileno())
            if result.returncode or temporary.stat().st_size == 0:
                raise RuntimeError("Database backup did not complete.")
            temporary.replace(final)
        finally:
            temporary.unlink(missing_ok=True)
        completed = sorted(
            folder.glob("hms-*.sql"),
            key=lambda item: item.stat().st_mtime_ns,
            reverse=True,
        )
        for obsolete in completed[14:]:
            within(self.root, obsolete).unlink()
        self.event("database backup completed")

    def terminate_tree(self, child):
        """Terminate only a live process retained by our own Popen handle."""
        if child.poll() is not None:
            self.force_tree_cleanup = True
            return
        if os.name != "nt":
            child.terminate()
            return
        executable = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"), "System32", "taskkill.exe"
        )
        result = subprocess.run(
            [str(executable), "/PID", str(child.pid), "/T", "/F"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if result.returncode and child.poll() is None:
            raise RuntimeError("An owned process tree did not stop.")

    def stop_children(self):
        for name in ("tunnel", "application", "database"):
            child = self.children.get(name)
            finished = child is None or child.poll() is not None
            if child is not None and finished:
                self.force_tree_cleanup = True
            try:
                if not finished:
                    if name == "database":
                        self.admin("shutdown")
                    else:
                        self.terminate_tree(child)
                    try:
                        child.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        self.event(f"forced stop {name}")
                        self.terminate_tree(child)
                        child.wait(timeout=10)
                    finished = True
            except (OSError, RuntimeError, subprocess.TimeoutExpired):
                self.force_tree_cleanup = True
                self.event(f"stop incomplete {name}")
            finally:
                if finished:
                    reader = self.readers.get(name)
                    if reader:
                        reader.join(timeout=5)
                    if reader and reader.is_alive():
                        self.force_tree_cleanup = True
                        self.event(f"output drain incomplete {name}")
                    else:
                        self.children.pop(name, None)
                        self.readers.pop(name, None)
                        if (
                            not reader
                            and child is not None
                            and child.stdout is not None
                        ):
                            child.stdout.close()
                        stream = self.streams.pop(name, None)
                        if stream:
                            stream.close()

    def run(self) -> int:
        delay = 1
        next_backup = 0.0
        try:
            while not self.stopped():
                try:
                    if self.children:
                        raise RuntimeError("An owned process has not stopped yet.")
                    self.require_free_port(self.config["database_port"])
                    self.require_free_port(self.config["port"])
                    self.start(
                        "database",
                        [
                            str(self.config["mysqld"]),
                            f"--defaults-file={self.config['mysql_config']}",
                            "--no-monitor",
                        ],
                    )
                    self.wait_ready("database", lambda: self.admin("status"))
                    if not next_backup:
                        self.backup()
                        next_backup = time.monotonic() + 86400
                    self.start(
                        "application",
                        [
                            str(self.config["python"]),
                            "-m",
                            "deployment.windows",
                            "--config",
                            str(self.config["runtime_config"]),
                        ],
                    )
                    self.wait_ready("application", self.application_ready)
                    self.start(
                        "tunnel",
                        [
                            str(self.config["cloudflared"]),
                            "tunnel",
                            "--config",
                            str(self.config["tunnel_config"]),
                            "run",
                            self.config["tunnel_id"],
                        ],
                    )
                    healthy_since = time.monotonic()
                    while not self.stopped():
                        if any(
                            child.poll() is not None for child in self.children.values()
                        ):
                            self.force_tree_cleanup = True
                            self.event(
                                "managed child exited; returning to the task restarter"
                            )
                            return 1
                        now = time.monotonic()
                        if now - healthy_since >= 60:
                            delay = 1
                        if now >= next_backup:
                            try:
                                self.backup()
                                next_backup = time.monotonic() + 86400
                            except (OSError, RuntimeError, subprocess.SubprocessError):
                                self.event(
                                    "database backup failed; retry in five minutes"
                                )
                                next_backup = time.monotonic() + 300
                        self.pause(1)
                except (OSError, RuntimeError, subprocess.SubprocessError) as error:
                    self.event(f"stack retry ({type(error).__name__}); delay {delay}s")
                    if self.force_tree_cleanup:
                        return 1
                finally:
                    self.stop_children()
                self.pause(delay)
                delay = min(delay * 2, 60)
        finally:
            self.stop_children()
            self.event("supervisor stopped")
            self.events.close()
        return 1 if self.children else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        config = load_operations(args.config)
        if args.check:
            print("Supervisor configuration validated; no processes started.")
            return 0
        with exclusive_lock(config["root"] / "supervisor.lock"):
            job = WindowsProcessJob() if os.name == "nt" else None
            supervisor = None
            try:
                supervisor = Supervisor(config)
                for name in (signal.SIGINT, signal.SIGTERM):
                    signal.signal(name, lambda signum, frame: supervisor.stopping.set())
                return supervisor.run()
            finally:
                if job:
                    job.close(
                        disarm=supervisor is None
                        or (
                            not supervisor.children
                            and not supervisor.force_tree_cleanup
                        )
                    )
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print(
            f"Supervisor unavailable ({type(error).__name__}); check private configuration or duplicate startup.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
