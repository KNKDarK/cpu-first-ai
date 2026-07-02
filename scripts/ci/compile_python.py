#!/usr/bin/env python3
"""Compile project Python files while skipping local environments and caches."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path


SKIP_DIRS = {".git", ".mypy_cache", "__pycache__", "my"}
ROOT = Path(__file__).resolve().parents[2]


def iter_python_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    failed = False
    for path in iter_python_files():
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failed = True
            print(exc.msg, file=sys.stderr)

    if failed:
        return 1

    print("Python syntax checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
