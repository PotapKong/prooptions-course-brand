from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS_PATH = ROOT / "brand" / "tokens.json"


def load_tokens() -> dict:
    with TOKENS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def palette() -> dict[str, str]:
    tokens = load_tokens()
    return {name: data["hex"] for name, data in tokens["palette"].items()}


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.strip().lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def get_font_candidates(kind: str = "heading") -> list[str]:
    """Return system font candidates. Font files are not bundled."""
    if kind == "mono":
        return [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
            "C:/Windows/Fonts/consola.ttf",
        ]
    if kind == "body":
        return [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    return [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]


def find_font(kind: str = "heading") -> str | None:
    for candidate in get_font_candidates(kind):
        if Path(candidate).exists():
            return candidate
    return None
