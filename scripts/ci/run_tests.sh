#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running tests with coverage..."
python -m pytest specs/ --cov=. --cov-report=term --cov-report=xml -v
echo "Tests passed."
