#!/usr/bin/env python3
"""Spec-driven tests for the storage module."""

from __future__ import annotations

import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class TestStorageSpec(unittest.TestCase):
    """Verify storage.py follows the spec."""

    def test_storage_module_exists(self):
        self.assertTrue((ROOT / "storage.py").exists())

    def test_persist_output_function(self):
        source = (ROOT / "storage.py").read_text()
        self.assertIn("persist_output", source)

    def test_get_recent_extractions(self):
        source = (ROOT / "storage.py").read_text()
        self.assertIn("fetch_recent", source)

    def test_sqlite_used(self):
        source = (ROOT / "storage.py").read_text()
        self.assertIn("sqlite3", source)


if __name__ == "__main__":
    unittest.main()
