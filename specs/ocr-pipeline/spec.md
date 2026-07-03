---
type: spec
module: ingestion
status: active
feature: ocr-pipeline
---

# Spec: OCR Pipeline

## Summary

The OCR pipeline (`ingestion.py`) processes an uploaded image through Tesseract with multiple preprocessing variants and selects the best result.

## Input Contract

- File: user-uploaded image (JPG, JPEG, PNG)
- Location: Streamlit `file_uploader` → saved to temp path

## Output Contract

- `/tmp/input.txt` — cleaned OCR text (highest-confidence result)
- `/tmp/input_raw.txt` — raw Tesseract output before cleanup
- On failure: `/tmp/input.txt` contains `"FAILED"`

## Preprocessing Variants

1. Grayscale
2. Grayscale + OTSU thresholding
3. Grayscale + contrast enhancement
4. Inverted (dark mode)

Scoring: combined confidence + word-count heuristic.

## Edge Cases

- Blank image → `"FAILED"`
- Image with no text → `"FAILED"`
- Corrupted image file → `"FAILED"`
- Very large image (>10MB) → should still process

## Validation Rules

- [ ] Output always written to `/tmp/input.txt`
- [ ] Raw output always written to `/tmp/input_raw.txt`
- [ ] Single word of text is valid output (not FAILED)
