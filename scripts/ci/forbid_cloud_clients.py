#!/usr/bin/env python3
"""Fail if project Python files import forbidden cloud client libraries."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


FORBIDDEN_MODULES = {"openai", "requests"}
SKIP_DIRS = {".git", ".mypy_cache", "__pycache__", "my"}
ROOT = Path(__file__).resolve().parents[2]


def iter_python_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def imported_root(alias_name: str) -> str:
    return alias_name.split(".", 1)[0]


def check_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = imported_root(alias.name)
                if root in FORBIDDEN_MODULES:
                    errors.append(f"{path.relative_to(ROOT)}:{node.lineno}: forbidden import {alias.name!r}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = imported_root(node.module)
            if root in FORBIDDEN_MODULES:
                errors.append(f"{path.relative_to(ROOT)}:{node.lineno}: forbidden import from {node.module!r}")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in iter_python_files():
        errors.extend(check_file(path))

    if errors:
        print("Forbidden cloud client imports found:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print("No forbidden cloud client imports found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
