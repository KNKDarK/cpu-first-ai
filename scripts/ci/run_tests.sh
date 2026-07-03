#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running tests with coverage..."
python -m pytest specs/ -v --cov-report=xml:coverage.xml
echo "Tests passed."
