"""Console-free scheduled-task entry point, copied into the private root."""

import argparse
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv)
    path = args.config.resolve()
    root = path.parent
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    output = logs / "launcher.log"
    if output.exists() and output.stat().st_size > 1024 * 1024:
        output.replace(output.with_suffix(".previous"))
    with output.open("a", encoding="utf-8") as stream:
        with redirect_stdout(stream), redirect_stderr(stream):
            try:
                if path.stat().st_size > 65536:
                    raise ValueError("Oversized operations configuration")
                operations = json.loads(path.read_text(encoding="utf-8-sig"))
                if Path(operations["root"]).resolve() != root:
                    raise ValueError("Operations root mismatch")
                release = Path(operations["release"])
                if not release.is_absolute():
                    raise ValueError("Absolute release path required")
                sys.path.insert(0, str(release))
                from deployment.supervise import main as supervise

                return supervise(["--config", str(path)])
            except Exception as error:
                print(
                    f"Laptop startup failed ({type(error).__name__}); inspect configuration."
                )
                return 1


if __name__ == "__main__":
    raise SystemExit(main())
