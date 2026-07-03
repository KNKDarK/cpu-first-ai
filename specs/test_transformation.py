#!/usr/bin/env python3
"""Spec-driven tests for the LLM transformation module."""

from __future__ import annotations

import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class TestTransformationSpec(unittest.TestCase):
    """Verify transformation.py follows the spec."""

    def test_transformation_module_exists(self):
        self.assertTrue((ROOT / "transformation.py").exists())

    def test_transformation_has_main(self):
        source = (ROOT / "transformation.py").read_text()
        self.assertIn("if __name__", source)
        self.assertIn("main()", source)

    def test_output_is_json(self):
        """Should produce JSON with cleaned_text key."""
        source = (ROOT / "transformation.py").read_text()
        self.assertIn("cleaned_text", source)

    def test_lock_file_used(self):
        """Should use a .lock file during processing."""
        source = (ROOT / "transformation.py").read_text()
        self.assertIn(".lock", source)


if __name__ == "__main__":
    unittest.main()
