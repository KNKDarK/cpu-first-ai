import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel


OUTPUT_FILE = Path("/tmp/output.json")
LOCK_FILE = Path("/tmp/output.json.lock")
DB_FILE = Path("/tmp/ocr_extractions.sqlite3")


class CleanedText(BaseModel):
    cleaned_text: str


class ExtractionRecord(BaseModel):
    id: int
    created_at: str
    source_image: str | None
    raw_text: str | None
    corrected_text: str | None
    cleaned_text: str


def init_db(db_path: Path = DB_FILE) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS extractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                source_image TEXT,
                raw_text TEXT,
                corrected_text TEXT,
                cleaned_text TEXT NOT NULL
            )
            """
        )


def load_validated_output(output_path: Path = OUTPUT_FILE) -> CleanedText | None:
    if not output_path.exists():
        return None

    data: dict[str, Any] = json.loads(output_path.read_text(encoding="utf-8"))
    if data.get("status") == "error":
        return None
    return CleanedText.model_validate(data)


def persist_output(
    *,
    source_image: str | None = None,
    raw_text: str | None = None,
    corrected_text: str | None = None,
    output_path: Path = OUTPUT_FILE,
    db_path: Path = DB_FILE,
) -> int | None:
    validated = load_validated_output(output_path)
    if validated is None:
        return None

    init_db(db_path)
    created_at = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO extractions (
                created_at,
                source_image,
                raw_text,
                corrected_text,
                cleaned_text
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                created_at,
                source_image,
                raw_text,
                corrected_text,
                validated.cleaned_text,
            ),
        )
        return int(cursor.lastrowid)


def fetch_recent(limit: int = 10, db_path: Path = DB_FILE) -> list[ExtractionRecord]:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, created_at, source_image, raw_text, corrected_text, cleaned_text
            FROM extractions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [ExtractionRecord.model_validate(dict(row)) for row in rows]


def watch_and_persist(
    *,
    source_image: str | None = None,
    raw_text: str | None = None,
    corrected_text: str | None = None,
    timeout_seconds: float = 60,
    poll_seconds: float = 0.25,
) -> int | None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if OUTPUT_FILE.exists() and not LOCK_FILE.exists():
            return persist_output(
                source_image=source_image,
                raw_text=raw_text,
                corrected_text=corrected_text,
            )
        time.sleep(poll_seconds)
    return None


def main() -> None:
    record_id = watch_and_persist()
    if record_id is None:
        print("No validated output persisted.")
        return
    print(f"Persisted extraction #{record_id}.")


if __name__ == "__main__":
    main()
