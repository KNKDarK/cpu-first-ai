#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="models"
MODEL_URL="https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
MODEL_FILE="${MODEL_DIR}/Llama-3.2-1B-Instruct-Q4_K_M.gguf"

if [ -f "$MODEL_FILE" ]; then
  echo "Model already exists at $MODEL_FILE"
  exit 0
fi

mkdir -p "$MODEL_DIR"
echo "Downloading model from Hugging Face..."
curl -L -o "$MODEL_FILE" "$MODEL_URL"
echo "Model downloaded to $MODEL_FILE"
