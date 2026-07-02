import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable

import pytesseract  # type: ignore
from PIL import Image, ImageEnhance, ImageOps


OUTPUT_FILE: str = "/tmp/input.txt"
RAW_OUTPUT_FILE: str = "/tmp/input_raw.txt"
CONFIDENCE_THRESHOLD: int = 40


@dataclass(frozen=True)
class OcrCandidate:
    text: str
    confidence: float
    score: float


def _check_tesseract() -> None:
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        print(
            "Tesseract-OCR is not installed or not in PATH.\n"
            "Install it via your package manager:\n"
            "  Ubuntu/Debian: sudo apt install tesseract-ocr\n"
            "  macOS: brew install tesseract\n"
            "  Windows: https://github.com/UB-Mannheim/tesseract/wiki",
            file=sys.stderr,
        )
        sys.exit(1)


def _prepare_image(image: Image.Image) -> Image.Image:
    gray = ImageOps.autocontrast(image.convert("L"))
    gray = ImageEnhance.Contrast(gray).enhance(2)
    enlarged = gray.resize((gray.width * 3, gray.height * 3))
    return enlarged.point(lambda pixel: 255 if pixel > 180 else 0)


def _get_mean_confidence(image: Image.Image, psm: int = 6) -> float:
    data: Dict[str, Any] = pytesseract.image_to_data(
        image, output_type=pytesseract.Output.DICT, config=f"--oem 3 --psm {psm}"
    )
    confidences: list[float] = [float(c) for c in data["conf"] if str(c) != "-1"]
    return sum(confidences) / len(confidences) if confidences else 0.0


def _image_variants(image: Image.Image) -> Iterable[tuple[str, Image.Image, int]]:
    gray = ImageOps.autocontrast(image.convert("L"))
    contrast = ImageEnhance.Contrast(gray).enhance(2)

    yield "default", _prepare_image(image), 6
    yield "receipt_lines", contrast.resize((gray.width * 2, gray.height * 2)).point(
        lambda pixel: 255 if pixel > 165 else 0
    ), 4
    yield "soft_scaled", contrast.resize((gray.width * 3, gray.height * 3)), 6
    yield "dense_receipt", contrast.resize((gray.width * 4, gray.height * 4)).point(
        lambda pixel: 255 if pixel > 165 else 0
    ), 6
    yield "auto_segment", contrast.resize((gray.width * 3, gray.height * 3)), 3
    yield "sparse_text", contrast.resize((gray.width * 3, gray.height * 3)), 11


def _text_score(text: str, confidence: float) -> float:
    words = re.findall(r"[A-Za-z0-9$€£₹]+", text)
    lines = [line for line in text.splitlines() if line.strip()]
    known_receipt_words = {
        "receipt",
        "invoice",
        "item",
        "total",
        "cash",
        "change",
        "price",
        "store",
        "shopping",
        "thanks",
    }
    known_hits = sum(1 for word in words if word.lower() in known_receipt_words)
    noisy_words = sum(
        1
        for word in words
        if len(word) > 12 and not re.search(r"[AEIOUaeiou$€£₹]", word)
    )
    too_short_penalty = 60 if len(words) < 8 else 0
    return (
        confidence
        + min(len(words), 90) * 0.7
        + min(len(lines), 20) * 2.5
        + known_hits * 3
        - noisy_words * 4
        - too_short_penalty
    )


def _extract_best_text(image: Image.Image) -> tuple[str, float]:
    candidates: list[OcrCandidate] = []
    for _, variant, psm in _image_variants(image):
        raw_text = pytesseract.image_to_string(variant, config=f"--oem 3 --psm {psm}")
        confidence = _get_mean_confidence(variant, psm)
        candidates.append(
            OcrCandidate(
                text=raw_text,
                confidence=confidence,
                score=_text_score(raw_text, confidence),
            )
        )

    best = max(candidates, key=lambda candidate: candidate.score)
    return best.text, best.confidence


def _fix_common_ocr_words(text: str) -> str:
    replacements = {
        "ftem": "Item",
        "ttem": "Item",
        "trem": "Item",
        "tlem": "Item",
        "ltem": "Item",
        "ltiem": "Item",
        "tem": "Item",
        "widin": "Width",
        "widht": "Width",
        "widl": "Width",
        "widlh": "Width",
        "heignt": "Height",
        "reciept": "Receipt",
        "recipt": "Receipt",
        "invoce": "Invoice",
        "shopprng": "Shopping",
        "shopplng": "Shopping",
    }

    def replace_word(match: re.Match[str]) -> str:
        value = match.group(0)
        replacement = replacements.get(value.lower())
        return replacement if replacement else value

    return re.sub(r"\b[A-Za-z]+\b", replace_word, text)


def _normalize_money(text: str) -> str:
    text = re.sub(r"(?i)\b(cash|change|total)\s+s\s+(?=\d)", r"\1 $ ", text)
    text = re.sub(r"\bS\s+(?=\d{2,5}(?:[,.]\d{2})?\b)", "$ ", text)
    text = re.sub(r"\$\s*(\d+)[,.](\d{2})\b", r"$ \1.\2", text)

    def add_decimal(match: re.Match[str]) -> str:
        digits = match.group(1)
        if len(digits) < 4 or len(digits) > 5:
            return match.group(0)
        return f"$ {digits[:-2]}.{digits[-2:]}"

    return re.sub(r"\$\s*(\d{4,5})\b", add_decimal, text)


def _drop_noise_lines(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue

        alnum_count = sum(char.isalnum() for char in stripped)
        useful_symbols = any(symbol in stripped for symbol in "$€£₹")
        mostly_noise = (
            len(stripped) > 30
            and alnum_count / len(stripped) < 0.2
            and not useful_symbols
        )
        if mostly_noise:
            continue
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)


def _clean_text(raw: str) -> str:
    text = raw.replace("“", '"').replace("”", '"').replace("’", "'")
    text = _fix_common_ocr_words(text)
    text = _normalize_money(text)
    text = _drop_noise_lines(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[^\w\s\n.,!?;:()'\"$€£₹%+=*/<>#@\[\]{}&|_\\^~-]", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def process_image(image_path: str) -> str:
    _check_tesseract()
    source_image = Image.open(image_path)

    raw_text, confidence = _extract_best_text(source_image)
    if confidence < CONFIDENCE_THRESHOLD:
        msg: str = "FAILED"
        Path(OUTPUT_FILE).write_text(msg, encoding="utf-8")
        Path(RAW_OUTPUT_FILE).write_text(msg, encoding="utf-8")
        return msg

    Path(RAW_OUTPUT_FILE).write_text(raw_text.strip(), encoding="utf-8")
    clean: str = _clean_text(raw_text)
    if not clean:
        msg = "FAILED"
        Path(OUTPUT_FILE).write_text(msg, encoding="utf-8")
        Path(RAW_OUTPUT_FILE).write_text(msg, encoding="utf-8")
        return msg

    Path(OUTPUT_FILE).write_text(clean, encoding="utf-8")
    return clean


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <image_path>", file=sys.stderr)
        sys.exit(1)

    result: str = process_image(sys.argv[1])
    print(result)


if __name__ == "__main__":
    main()
