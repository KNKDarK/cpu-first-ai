# Spec: SQLite Storage

## Summary

`storage.py` persists validated extraction results to a local SQLite database and provides query functions for the UI.

## Input Contract

- `/tmp/output.json` — validated JSON with `cleaned_text` key
- Database: `/tmp/ocr_extractions.sqlite3`

## Output Contract

- SQLite table `extractions` with columns: `id`, `text`, `word_count`, `char_count`, `line_count`, `created_at`
- Streamlit UI shows last 5 extractions

## Edge Cases

- Database file doesn't exist → auto-created
- Corrupt JSON input → skip, return empty result
- Multiple rapid writes → sequential, no race conditions

## Validation Rules

- [ ] `persist_output()` validates JSON before writing
- [ ] `get_recent_extractions(limit=5)` returns ordered results
- [ ] Word/char/line counts computed before storage
