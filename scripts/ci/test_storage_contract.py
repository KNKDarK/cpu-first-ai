#!/usr/bin/env python3
"""Fast local contract checks for the storage/orchestrator boundary."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from storage import fetch_recent, load_validated_output, persist_output


def test_validated_output_and_persistence() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        output_path = root / "output.json"
        db_path = root / "ocr.sqlite3"

        output_path.write_text(json.dumps({"cleaned_text": "Receipt total $ 12.34"}), encoding="utf-8")

        validated = load_validated_output(output_path)
        assert validated is not None
        assert validated.cleaned_text == "Receipt total $ 12.34"

        record_id = persist_output(
            source_image="receipt.jpg",
            raw_text="raw text",
            corrected_text="corrected text",
            output_path=output_path,
            db_path=db_path,
        )
        assert record_id == 1

        records = fetch_recent(limit=5, db_path=db_path)
        assert len(records) == 1
        assert records[0].source_image == "receipt.jpg"
        assert records[0].cleaned_text == "Receipt total $ 12.34"


def test_error_output_is_not_persisted() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        output_path = root / "output.json"
        db_path = root / "ocr.sqlite3"

        output_path.write_text(json.dumps({"status": "error"}), encoding="utf-8")

        assert load_validated_output(output_path) is None
        assert persist_output(output_path=output_path, db_path=db_path) is None


def main() -> int:
    test_validated_output_and_persistence()
    test_error_output_is_not_persisted()
    print("Storage contract checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
