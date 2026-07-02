#!/bin/bash

cd "$(dirname "$0")"

echo "===================================================================="
echo "  🔍 Image Text Extractor"
echo "  Offline OCR via Tesseract"
echo "===================================================================="

if [ -x "my/bin/streamlit" ]; then
    my/bin/streamlit run streamlit_app.py --server.port=8501 --server.address=localhost
else
    streamlit run streamlit_app.py --server.port=8501 --server.address=localhost
fi
