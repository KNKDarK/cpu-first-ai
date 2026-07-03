# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-07-03

### Added

- Initial release of Image Text Extractor.
- Streamlit UI with three-tab result view (Intelligent, Corrected OCR, Raw OCR).
- OCR pipeline using Tesseract with multiple image preprocessing variants.
- LLM post-processing via `llama-cpp-python` with Llama 3.2 1B Instruct.
- SQLite storage for extraction history (last 5 entries shown in UI).
- GitLab CI pipeline with validation (`compile_python`, `forbid_cloud_clients`, `storage_contract`) and smoke test stages.
- Pre-commit hooks for syntax checking, cloud dependency ban, storage contract validation, and OCR smoke test.
- Pipeline Protocol (`agent/AGENT.md`) defining inter-module contracts via `/tmp/` file-based communication.
- Local-only design: 100% offline, no cloud API calls.
