# Project Constitution

## Identity

This project is **Image Text Extractor** — a fully offline OCR-to-LLM pipeline for extracting text from images using Tesseract and local Llama inference.

## Core Principles

1. **100% Local**: No cloud APIs, no network calls after setup.
2. **Pipeline Protocol**: Each module (Ingestion → Transformation → Storage) runs as an independent subprocess communicating via file-based contracts in `/tmp/`.
3. **Validation First**: All inter-module data must be validated (JSON schema, sentinel values).
4. **Offline-First**: Model weights and all dependencies must be cacheable locally.

## Spec-Driven Development

- All feature specs live in `specs/`.
- Each spec defines inputs, expected outputs, and boundary conditions.
- Changes to the pipeline contract must be reflected in both specs and the constitution.
- New modules must be specified before implementation.

## Team Roles

| Role | Module | Output Contract |
|---|---|---|
| Ingestion (M1) | `ingestion.py` | `/tmp/input.txt` or `"FAILED"` |
| Transformation (M2) | `transformation.py` | `/tmp/output.json` with lock file |
| Storage (M3) | `storage.py` + `streamlit_app.py` | SQLite persistence + UI |

## Boundaries

- No `import requests`
- No `import openai`
- No hardcoded secrets or credentials
- All temporary files in `/tmp/` only
