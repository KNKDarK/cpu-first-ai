---
type: tasks
feature: llm-transformation
status: active
---

# Tasks: LLM Transformation

## Breakdown

- [x] Set up llama-cpp-python inference pipeline
- [x] Download and cache GGUF model via huggingface-hub
- [x] Implement input reading from `/tmp/input.txt`
- [x] Build prompt template for OCR correction
- [x] Parse LLM output into `{"cleaned_text": "..."}` JSON
- [x] Implement lock file creation/removal
- [x] Handle `"FAILED"` sentinel passthrough
- [x] Handle empty input
- [x] Handle long input truncation
- [x] Write spec tests

## Effort Estimate

2 days

## Notes

Model loading is slow on first run. Consider adding a loading progress indicator.
