# Contributing to Image Text Extractor

Thank you for considering contributing! This project follows the **Pipeline Protocol** defined in `agent/AGENT.md`.

## Development Setup

```bash
python -m venv my
source my/bin/activate
pip install -r requirements.txt
# System deps
sudo apt install tesseract-ocr tesseract-ocr-eng
```

## Code Style

- **Python:** snake_case for functions/variables, PascalCase for classes, UPPER_SNAKE_CASE for constants.
- **Imports:** stdlib → third-party → local, separated by a blank line.
- **No cloud dependencies** (`requests`, `openai`) — everything must run offline.

## Pipeline Architecture

| Module | Responsibility | Output |
|---|---|---|
| `ingestion.py` | OCR via Tesseract | `/tmp/input.txt` (or `"FAILED"`) |
| `transformation.py` | LLM post-processing | `/tmp/output.json` (validated JSON) |
| `storage.py` | SQLite persistence | `/tmp/ocr_extractions.sqlite3` |

Each module runs as a *separate subprocess* communicating via files in `/tmp/`.

## Testing

```bash
python test1.py                    # Full smoke test (requires Tesseract)
python scripts/ci/compile_python.py          # Syntax check
python scripts/ci/test_storage_contract.py   # Storage contract
python scripts/ci/forbid_cloud_clients.py    # Cloud check
```

## Pre-commit Hooks

Install with `pre-commit install && pre-commit install -t pre-push`.  
Hooks run: syntax check, cloud-ban, storage contract, and OCR smoke test (push only).

## Pull Request Process

1. Ensure all CI checks pass (`.gitlab-ci.yml`).
2. Update `CHANGELOG.md` with your changes under the appropriate version heading.
3. Maintain backward compatibility with the `/tmp/` file-based contract.
4. Get at least one maintainer review before merging.
