#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
default_exe = root / "build-ninja" / "modules" / "cli" / ("cgride.exe" if os.name == "nt" else "cgride")
cgride = Path(os.environ.get("CGRIDE", str(default_exe)))
example = Path(os.environ.get("EXAMPLE", str(root / "examples" / "hello")))

if not cgride.exists():
    print(f"cgride executable not found: {cgride}", file=sys.stderr)
    print("Set CGRIDE=/path/to/cgride or build the default Ninja tree first.", file=sys.stderr)
    raise SystemExit(1)

commands = [
    ("first build", [str(cgride), "build", "--rebuild"]),
    ("noop build 1", [str(cgride), "build"]),
    ("noop build 2", [str(cgride), "build"]),
    ("run 1", [str(cgride), "run"]),
    ("run 2", [str(cgride), "run"]),
]

for label, command in commands:
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=example, check=False)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    print(f"{label}: {elapsed_ms:.1f}ms")

    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
