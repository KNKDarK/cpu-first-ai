# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 1.x | ✅ |
| < 1.0 | ❌ |

## Reporting a Vulnerability

This project operates fully offline with no network calls. However, if you discover a security issue:

1. **Do not** open a public GitHub issue.
2. Email the maintainers (see commit history) with details.
3. You should receive a response within 7 days.

## Security Design

- **No cloud APIs** — all processing is local; no data leaves your machine.
- **No `requests` or `openai` imports** — enforced by CI (`forbid_cloud_clients.py`).
- **No sensitive data logged** — temporary files live in `/tmp/` and use generic names.
- **SQLite database** is local only; no network exposure.

## Best Practices

- Run the application on a trusted network or locally only.
- Do not expose the Streamlit app (`streamlit run`) to the public internet.
- Regularly update dependencies via `pip install --upgrade -r requirements.txt`.
- Review any GGUF models loaded into `models/` for provenance.
