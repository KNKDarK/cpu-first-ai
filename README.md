---
title: Image Text Extractor
emoji: 🔍
colorFrom: purple
colorTo: blue
sdk: streamlit
app_file: streamlit_app.py
pinned: false
---

# Image Text Extractor

**Fully offline OCR text extraction from images** — powered by Tesseract for optical character recognition and a local Llama 3.2 1B model for intelligent post-processing. 100% local, no cloud APIs, no data leaves your machine.

## Features

- **Multi-variant OCR** — Tesseract runs across multiple image preprocessings (grayscale, OTSU thresholding, contrast enhancement, dark-mode inversion) and selects the best result.
- **AI-Powered Refinement** — A local Llama 3.2 1B Instruct GGUF model fixes OCR errors, spacing, stray characters, and formatting.
- **Three-Tab Output** — View Intelligent Extraction (LLM-refined), Corrected OCR (best Tesseract pass), and Raw OCR side by side.
- **Persistent History** — Last 5 extractions saved to SQLite and expandable in the UI.
- **Pipeline Protocol** — Modular architecture with file-based inter-process contracts (see `agent/AGENT.md`).

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| OCR | Tesseract via `pytesseract` |
| LLM | `llama-cpp-python` + Llama 3.2 1B Instruct Q4_K_M |
| Storage | SQLite |
| Image Processing | Pillow, NumPy |

## Quick Start

### Prerequisites

- Python 3.10+
- Tesseract OCR (`tesseract-ocr` + `tesseract-ocr-eng`)
- 4 GB RAM (8 GB recommended)
- ~1 GB disk for the LLM model

### Installation

```bash
# 1. System dependencies
sudo apt install tesseract-ocr tesseract-ocr-eng

# 2. Python environment
python -m venv my
source my/bin/activate
pip install -r requirements.txt

# 3. Download the LLM model
bash scripts/download_model.sh

# 4. Launch
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser.

## Usage

1. Click **Browse files** and select an image (JPG, JPEG, PNG).
2. Click **Extract Text**.
3. View results in the three tabs.
4. Expand **Extraction History** to see previous results.

## Project Structure

```
├── streamlit_app.py          # Main UI (entry point)
├── ingestion.py              # OCR pipeline
├── transformation.py         # LLM post-processing
├── storage.py                # SQLite persistence
├── agent/
│   └── AGENT.md              # Pipeline Protocol
├── scripts/
│   ├── download_model.sh     # Model downloader
│   └── ci/                   # CI validation scripts
├── specs/                    # Feature specs (Spec-Driven Development)
├── .specify/                 # Spec-Kit constitution & templates
├── Dockerfile                # Container build
└── dockerignore
```

## CI/CD

GitLab CI pipeline with validation stages (syntax check, cloud-ban, storage contract) and an OCR smoke test. Pre-commit hooks enforce quality gates. See `.gitlab-ci.yml` and `.pre-commit-config.yaml`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions must follow the Pipeline Protocol and maintain 100% local operation.

## License

[GNU Affero General Public License v3.0](LICENSE) — ensures that modifications made to network-server deployments must be shared with users.
