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

Offline OCR text extraction from images using Tesseract, local Llama post-processing, and SQLite history. 100% local, no cloud APIs.

## Tech Stack

- **OCR:** Tesseract via pytesseract
- **Post-processing:** llama-cpp-python with a local GGUF model
- **Storage:** SQLite
- **UI:** Streamlit
- **Image processing:** Pillow

## Usage

Upload an image (JPG, JPEG, PNG) and click **Extract Text**.

The pipeline writes OCR text to `/tmp/input.txt`, validates transformed JSON at `/tmp/output.json`, and stores successful extractions in `/tmp/ocr_extractions.sqlite3`.
