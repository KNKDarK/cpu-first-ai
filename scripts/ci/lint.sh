#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running ruff..."
python -m ruff check . --quiet
python -m ruff format . --check --quiet
echo "Lint passed."
