# AGENTS.md: Pipeline Protocol

> [!IMPORTANT]
> **Instructions for AI Agents (Antigravity/u, Codex, and OpenCode):**
> Whenever you start reading/working in this directory, you **must** read this file to understand the project boundaries, team responsibilities, and rules of engagement. For overall project context, tech stack, and setup, refer to the [README.md](file:///home/knkdark/hack1/README.md).
>
> **Core Rule Access:** Ensure this file and [README.md](file:///home/knkdark/hack1/README.md) are always loaded and followed.

## 1. Team Responsibilities
- **Member 1 (Ingestion):** Responsible for raw data path. 
    - *Contract:* Must return cleaned text to `/tmp/input.txt`.
- **Member 2 (Transformation):** Responsible for LLM inference. 
    - *Contract:* Must read from `/tmp/input.txt`, output validated JSON to `/tmp/output.json`.
- **Member 3 (Storage/Orchestrator):** Responsible for DB and UI.
    - *Contract:* Watch `/tmp/output.json` and persist to SQLite.

## 2. Boundaries (Rules of Engagement)
- **Always do:** Validate JSON schema using Pydantic.
- **Ask first:** Before changing the data schema (fields in JSON).
- **Never do:** Use `requests` or `openai` libraries; never trigger an API call to a cloud endpoint.

## 3. Communication Patterns
- If M1's OCR fails, it must write "FAILED" to `/tmp/input.txt` so M2 knows to skip inference.
- M3 handles the UI "loading" state based on the presence of a ".lock" file created by M2.
