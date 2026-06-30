from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from brand_config import load_tokens

BANNED_WORDS = [
    "гарант", "без риска", "секрет", "иксы", "ракета", "ламбо", "lamborghini",
    "казино", "пассивный доход", "быстрый заработок", "сигнал", "инсайд"
]


def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def word_count(text: str) -> int:
    return len(re.findall(r"[\wА-Яа-яЁё]+", text or ""))


def audit(brief: dict) -> list[str]:
    tokens = load_tokens()
    limits = tokens["copy_limits"]
    warnings = []

    title = brief.get("title", "")
    subtitle = brief.get("subtitle", "")
    body = brief.get("body", "")
    joined = " ".join([title, subtitle, body]).lower()

    if not brief.get("format"):
        warnings.append("No format specified.")
    if not brief.get("audience") and brief.get("asset_type") != "lesson_slide":
        warnings.append("No audience specified.")
    if not brief.get("visual_object"):
        warnings.append("No option-related visual object specified.")
    if word_count(title) > limits["cover_title_words_max"] and brief.get("asset_type") != "lesson_slide":
        warnings.append(f"Title is too long: {word_count(title)} words. Max {limits['cover_title_words_max']}.")
    if word_count(subtitle) > limits["cover_subtitle_words_max"] and brief.get("asset_type") != "lesson_slide":
        warnings.append(f"Subtitle is too long: {word_count(subtitle)} words. Max {limits['cover_subtitle_words_max']}.")
    if brief.get("asset_type") == "lesson_slide" and word_count(" ".join([title, body])) > limits["slide_words_max"]:
        warnings.append(f"Slide has too many words: {word_count(' '.join([title, body]))}. Max {limits['slide_words_max']}.")

    for banned in BANNED_WORDS:
        if banned in joined:
            warnings.append(f"Banned/hype wording found: {banned}")

    avoid = [x.lower() for x in brief.get("avoid", [])]
    if "aggressive red" not in avoid and "red" not in " ".join(avoid):
        warnings.append("Add avoidance rule for aggressive red / signal-style visuals.")

    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit design brief against brand rules.")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    brief = load_json(args.input)
    warnings = audit(brief)
    if warnings:
        print("Design audit warnings:")
        for warning in warnings:
            print(f"- {warning}")
        raise SystemExit(1)
    print("Design audit passed.")


if __name__ == "__main__":
    main()
