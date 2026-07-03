---
type: spec
module: transformation
status: active
---

# Spec: LLM Transformation

## Summary

`transformation.py` reads cleaned OCR text from `/tmp/input.txt` and sends it to a local Llama 3.2 1B model for post-processing.

## Input Contract

- `/tmp/input.txt` — cleaned OCR text (or `"FAILED"`)
- Lock file: `/tmp/output.json.lock` (creates during processing)

## Output Contract

- `/tmp/output.json` — JSON with shape `{"cleaned_text": "<refined text>"}`
- Lock file removed after write
- On failure: JSON with `{"cleaned_text": "FAILED"}`

## Edge Cases

- Empty input → `{"cleaned_text": "FAILED"}`
- `"FAILED"` sentinel → pass through as `{"cleaned_text": "FAILED"}`
- Very long input → truncated to model context window (2048 tokens)

## Validation Rules

- [ ] Output is valid JSON with `cleaned_text` key
- [ ] Lock file exists during processing, removed after
- [ ] No cloud API calls made
