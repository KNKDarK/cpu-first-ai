import json
from pathlib import Path

from llama_cpp import Llama
from dataclasses import dataclass, asdict
from huggingface_hub import hf_hub_download


INPUT_FILE = Path("/tmp/input.txt")
OUTPUT_FILE = Path("/tmp/output.json")
LOCK_FILE = Path("/tmp/output.json.lock")
MODEL_PATH = Path(__file__).resolve().parent / "models" / "Llama-3.2-1B-Instruct-Q4_K_M.gguf"
HF_REPO_ID = "bartowski/Llama-3.2-1B-Instruct-GGUF"
HF_FILENAME = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"


def ensure_model() -> None:
    if MODEL_PATH.exists():
        return
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading model from Hugging Face Hub ({HF_REPO_ID})...")
    hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_FILENAME,
        local_dir=MODEL_PATH.parent,
        local_dir_use_symlinks=False,
        resume_download=True,
    )
    print("Model download complete.")

SYSTEM_PROMPT = """
You are an OCR text post-processor. Clean up the raw OCR text below:
- Fix obvious spelling errors and typos
- Fix incorrect spacing (words merged or split incorrectly)
- Remove garbage or stray special characters
- Preserve numbers, dates, prices, and meaningful formatting
- Output clean, readable plain text
- Do NOT add explanations, markdown, or extra text

You must return a JSON object with the key "cleaned_text" containing the cleaned plain text. Do not add any explanations or markdown formatting outside of the JSON object.
""".strip()


@dataclass
class CleanedText:
    cleaned_text: str


def write_error() -> None:
    OUTPUT_FILE.write_text(json.dumps({"status": "error"}), encoding="utf-8")


def main() -> None:
    ensure_model()
    if not INPUT_FILE.exists() or not MODEL_PATH.exists():
        write_error()
        return

    raw_text = INPUT_FILE.read_text(encoding="utf-8").strip()
    if not raw_text or raw_text == "FAILED":
        write_error()
        return

    LOCK_FILE.write_text("running", encoding="utf-8")
    try:
        llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=2048,
            verbose=False,
        )
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_text},
            ],
            temperature=0,
            max_tokens=512,
            response_format={"type": "json_object"},
        )
        content = response["choices"][0]["message"]["content"].strip()
        data = json.loads(content)
        validated = CleanedText(**data)
    except Exception:
        write_error()
        return
    finally:
        LOCK_FILE.unlink(missing_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(asdict(validated)),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
