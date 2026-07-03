#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running detect-secrets..."
python -m detect_secrets scan --all-files --exclude-files 'my/|__pycache__/|.mypy_cache/|builds/|.git/' > /tmp/secrets_output.json
python -c "
import json
with open('/tmp/secrets_output.json') as f:
    data = json.load(f)
results = data.get('results', {})
total = sum(len(v) for v in results.values())
if total:
    print(f'Found {total} potential secret(s)')
    exit(1)
else:
    print('No secrets found.')
"
echo "Secret scan passed."
