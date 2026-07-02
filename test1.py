import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
IMAGE_PATH = ROOT_DIR / "test_receipt.jpg"
INPUT_FILE = Path("/tmp/input.txt")


def main() -> int:
    print(f"Looking for test image: {IMAGE_PATH}")
    if not IMAGE_PATH.exists():
        print(f"FAILURE: Missing test image: {IMAGE_PATH}")
        return 1

    INPUT_FILE.unlink(missing_ok=True)

    print("Running OCR on test image...")
    result = subprocess.run(
        [sys.executable, "ingestion.py", str(IMAGE_PATH)],
        cwd=ROOT_DIR, text=True, capture_output=True,
    )

    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    if result.returncode != 0:
        print(f"FAILURE: ingestion.py exited with code {result.returncode}")
        return 1

    if not INPUT_FILE.exists():
        print(f"FAILURE: Ingestion did not produce {INPUT_FILE}")
        return 1

    text = INPUT_FILE.read_text(encoding="utf-8").strip()
    if text == "FAILED":
        print(f"FAILURE: Could not extract text from image (low confidence)")
        return 1
    if not text:
        print(f"FAILURE: Extracted text is empty")
        return 1

    print(f"SUCCESS: Extracted {len(text)} characters ({len(text.split())} words)")
    print("---")
    print(text)
    print("---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
