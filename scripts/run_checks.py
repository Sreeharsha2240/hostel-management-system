"""Run the same MySQL checks locally and in CI, preserving logs and exit codes."""

import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / 'test-results'
LINT_PATHS = ['accounts', 'audit', 'hostels', 'students', 'hms', 'tests', 'scripts']


def run_step(label, arguments, steps):
    command = [sys.executable, *arguments]
    log_path = RESULTS / f'{label}.log'
    started = perf_counter()
    print(f'\nRunning {label}', flush=True)
    child_env = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    with log_path.open('w', encoding='utf-8') as log:
        with subprocess.Popen(
            command,
            cwd=ROOT,
            env=child_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
        ) as process:
            for line in process.stdout:
                print(line, end='', flush=True)
                log.write(line)
            return_code = process.wait()
    steps.append(
        {
            'name': label,
            'command': command,
            'exit_code': return_code,
            'elapsed_seconds': round(perf_counter() - started, 3),
            'log': str(log_path.relative_to(ROOT)),
        }
    )
    return return_code


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    RESULTS.mkdir(exist_ok=True)
    metadata = {
        'started_at': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'platform': platform.platform(),
        'git_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=ROOT,
            text=True,
        ).strip(),
        'working_tree_dirty': bool(
            subprocess.check_output(
                ['git', 'status', '--porcelain'],
                cwd=ROOT,
                text=True,
            ).strip()
        ),
        'steps': [],
    }
    checks = [
        ('lint', ['-m', 'ruff', 'check', *LINT_PATHS]),
        ('format', ['-m', 'ruff', 'format', '--check', *LINT_PATHS]),
        ('database-check', ['manage.py', 'check', '--database', 'default']),
        ('migration-check', ['manage.py', 'makemigrations', '--check', '--dry-run']),
    ]
    failed = False
    for label, arguments in checks:
        if run_step(label, arguments, metadata['steps']):
            failed = True
            break
    if not failed:
        sys.path.insert(0, str(ROOT))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
        import django

        django.setup()
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute('SELECT VERSION()')
            database_version = cursor.fetchone()[0]
        metadata.update(
            django=django.get_version(),
            database_vendor=connection.vendor,
            database_version=database_version,
        )
        connection.close()
        failed = bool(
            run_step('coverage-erase', ['-m', 'coverage', 'erase'], metadata['steps'])
        )
        failed = (
            bool(
                run_step(
                    'django-tests',
                    [
                        '-m',
                        'coverage',
                        'run',
                        'manage.py',
                        'test',
                        '--noinput',
                        '--verbosity',
                        '2',
                    ],
                    metadata['steps'],
                )
            )
            or failed
        )
        failed = (
            bool(
                run_step(
                    'coverage-report', ['-m', 'coverage', 'report'], metadata['steps']
                )
            )
            or failed
        )
        failed = (
            bool(run_step('coverage-xml', ['-m', 'coverage', 'xml'], metadata['steps']))
            or failed
        )
    metadata['status'] = 'failed' if failed else 'passed'
    metadata['completed_at'] = datetime.now(timezone.utc).isoformat()
    (RESULTS / 'run.json').write_text(
        json.dumps(metadata, indent=2) + '\n', encoding='utf-8'
    )
    print(f'\nChecks {metadata["status"]}. Evidence: {RESULTS}', flush=True)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
