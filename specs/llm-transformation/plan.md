---
type: plan
feature: llm-transformation
status: active
---

# Plan: LLM Transformation

## Objective

Build an LLM post-processing module that reads OCR output and refines it using a local Llama model, producing validated JSON output.

## Implementation Steps

- [x] Implement `transformation.py` with llama-cpp-python inference
- [x] Load GGUF model from `models/` directory
- [x] Read input from `/tmp/input.txt`
- [x] Write validated JSON output to `/tmp/output.json`
- [x] Implement lock file protocol (`/tmp/output.json.lock`)
- [x] Handle `"FAILED"` sentinel passthrough
- [x] Handle empty input gracefully
- [x] Truncate input to model context window
- [x] Write spec-driven tests in `specs/test_transformation.py`

## Dependencies

- llama-cpp-python
- GGUF model file (Llama 3.2 1B Instruct Q4_K_M)
- huggingface-hub for model download

## Acceptance Criteria

- [ ] OCR text is refined by LLM and written as JSON
- [ ] Lock file signals processing state
- [ ] `"FAILED"` input passes through as `"FAILED"` output
- [ ] No cloud API calls made
