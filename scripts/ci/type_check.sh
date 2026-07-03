#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running mypy..."
python -m mypy . --no-error-summary
echo "Type check passed."
