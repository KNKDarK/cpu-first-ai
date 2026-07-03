---
type: plan
feature: ocr-pipeline
status: active
---

# Plan: OCR Pipeline

## Objective

Build a reliable OCR ingestion module that runs Tesseract with multiple image preprocessing variants and selects the best result using a scoring heuristic.

## Implementation Steps

- [x] Implement `ingestion.py` with Tesseract subprocess call
- [x] Add image preprocessing variants (grayscale, OTSU, contrast, inverted)
- [x] Implement scoring heuristic (confidence × word count)
- [x] Write cleaned output to `/tmp/input.txt` and raw to `/tmp/input_raw.txt`
- [x] Handle failure with `"FAILED"` sentinel
- [x] Add image format validation (JPG, JPEG, PNG only)
- [x] Write spec-driven tests in `specs/test_ingestion.py`

## Dependencies

- Tesseract OCR system package
- pytesseract Python binding
- Pillow for image processing

## Acceptance Criteria

- [ ] Uploaded image produces cleaned text in `/tmp/input.txt`
- [ ] Blank/corrupted images produce `"FAILED"`
- [ ] Multiple preprocessing variants are attempted
- [ ] Best result selected by scoring heuristic
