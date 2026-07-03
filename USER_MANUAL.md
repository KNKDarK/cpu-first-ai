# Image Text Extractor — User Manual

## Overview

Image Text Extractor is a fully offline web application that extracts text from images using OCR (Tesseract) and refines it with a local Llama 3.2 AI model. No internet connection or cloud API is required after initial setup.

## System Requirements

- **OS:** Linux (tested on Fedora, Ubuntu/Debian)
- **Python:** 3.10+
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk:** ~1 GB for the LLM model

## Installation

### 1. Install System Dependencies

```bash
sudo apt install tesseract-ocr tesseract-ocr-eng   # Debian/Ubuntu
sudo dnf install tesseract tesseract-langpack-eng  # Fedora
```

### 2. Set Up Python Environment

```bash
python -m venv my
source my/bin/activate
pip install -r requirements.txt
```

### 3. Download the LLM Model

```bash
bash scripts/download_model.sh
```

Or manually place a GGUF model at `models/Llama-3.2-1B-Instruct-Q4_K_M.gguf`.

### 4. Launch the App

```bash
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (typically `http://localhost:8501`).

## Usage

### Extracting Text

1. Click **Browse files** and select an image (JPG, JPEG, or PNG).
2. Click **Extract Text**.
3. View results in three tabs:
   - **Intelligent Extraction** — LLM-refined, cleaned text.
   - **Corrected OCR** — Best Tesseract output after preprocessing.
   - **Raw OCR** — Unprocessed Tesseract output.

### Viewing History

Expand **Extraction History** at the bottom of the page to see the last 5 extractions stored in SQLite.

## File Locations

| Item | Path |
|---|---|
| OCR output (cleaned) | `/tmp/input.txt` |
| OCR output (raw) | `/tmp/input_raw.txt` |
| LLM output (JSON) | `/tmp/output.json` |
| SQLite database | `/tmp/ocr_extractions.sqlite3` |

## Troubleshooting

| Problem | Solution |
|---|---|
| `TesseractNotFoundError` | Install tesseract-ocr system package |
| Model not found | Run `scripts/download_model.sh` |
| Subprocess fails | Check `/tmp/output.json` for error details |
| Slow inference | Close other applications to free RAM |
