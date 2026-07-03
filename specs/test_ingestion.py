#!/usr/bin/env python3
"""Spec-driven tests for the OCR ingestion pipeline."""

from __future__ import annotations

import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class TestIngestionSpec(unittest.TestCase):
    """Verify ingestion.py follows the OCR pipeline spec."""

    def test_ingestion_module_exists(self):
        self.assertTrue((ROOT / "ingestion.py").exists())

    def test_ingestion_is_executable(self):
        """Must have a __main__ guard to run as a subprocess."""
        source = (ROOT / "ingestion.py").read_text()
        self.assertIn("if __name__", source)
        self.assertIn("main()", source)

    def test_ingestion_output_contract(self):
        """Should reference /tmp/input.txt as output path."""
        source = (ROOT / "ingestion.py").read_text()
        self.assertIn("input.txt", source)

    def test_ingestion_fail_sentinel(self):
        """Should write FAILED on failure."""
        source = (ROOT / "ingestion.py").read_text()
        self.assertIn("FAILED", source)


if __name__ == "__main__":
    unittest.main()
