#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "Running bandit security scan..."
python -m bandit -r . -c .bandit
echo "Secret scan passed."
