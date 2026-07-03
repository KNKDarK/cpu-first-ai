#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running pip-audit..."
python -m pip_audit --strict --requirement requirements.txt
echo "Dependency audit passed."
