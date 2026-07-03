---
type: tasks
feature: storage
status: active
---

# Tasks: SQLite Storage

## Breakdown

- [x] Initialize SQLite database with schema
- [x] Implement `persist_output()` with JSON loading
- [x] Implement word/char/line count computation
- [x] Implement `get_recent_extractions()` query
- [x] Handle missing database (auto-create)
- [x] Handle corrupt JSON (skip gracefully)
- [x] Integrate with Streamlit UI history panel
- [x] Write spec tests

## Effort Estimate

1 day

## Notes

Database lives at `/tmp/ocr_extractions.sqlite3` — ephemeral storage. Consider making configurable via environment variable.
