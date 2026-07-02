# GitLab CI Pipeline & Runner Setup

## Pipeline

The `.gitlab-ci.yml` defines two stages:

| Stage | Job | Runs | Requires |
|-------|-----|------|----------|
| `validate` | `validate` | Python syntax, forbidden imports, storage contract | Python + pydantic |
| `smoke` | `ocr_smoke` | Full OCR on test receipt | Tesseract, Python deps |

The `ocr_smoke` job is tagged `local-ocr` — it runs only on runners with that tag.

## Runner Registration

The OCR smoke job needs a runner that can install system packages (Tesseract). Register one:

```bash
gitlab-runner register \
  --url https://code.swecha.org \
  --registration-token <PROJECT_OR_GROUP_TOKEN> \
  --executor docker \
  --docker-image python:3.12-slim \
  --description ocr-runner \
  --tag-list local-ocr \
  --run-untagged=false
```

Get the registration token from: **Settings → CI/CD → Runners → New project runner**.

## Local Pre-commit / Pre-push Hooks

After cloning, install the hooks:

```bash
pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type pre-push
```

| Hook | Runs on | What it does |
|------|---------|-------------|
| `python-compile` | commit + push | `py_compile` all `.py` files |
| `forbid-cloud-clients` | commit + push | Blocks `openai`, `requests` imports |
| `storage-contract` | commit + push | Tests `storage.py` JSON/Pydantic contract |
| `ocr-smoke` | push only | Runs OCR on `test_receipt.jpg` (needs Tesseract on `PATH`) |

Run manually:

```bash
pre-commit run --all-files           # pre-commit checks
pre-commit run --hook-stage pre-push --all-files  # pre-push checks
```
