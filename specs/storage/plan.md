---
type: plan
feature: storage
status: active
---

# Plan: SQLite Storage

## Objective

Build a storage module that persists validated extraction results to SQLite and provides retrieval for the Streamlit UI.

## Implementation Steps

- [x] Implement `storage.py` with SQLite database initialization
- [x] Create `extractions` table with schema (id, text, word_count, char_count, line_count, created_at)
- [x] Implement `persist_output()` with JSON validation
- [x] Implement `get_recent_extractions(limit=5)` for UI
- [x] Compute word/char/line counts before storage
- [x] Handle missing database file (auto-create)
- [x] Handle corrupt JSON gracefully
- [x] Integrate with Streamlit UI history panel
- [x] Write spec-driven tests in `specs/test_storage.py`

## Dependencies

- Python stdlib sqlite3
- Pydantic/dataclasses for validation

## Acceptance Criteria

- [ ] Extraction records are persisted to SQLite
- [ ] UI shows last 5 extractions in history
- [ ] Corrupt input is handled without crashing
- [ ] Database is auto-created if missing
