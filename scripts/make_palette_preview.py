from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from brand_config import find_font, hex_to_rgb, load_tokens

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    tokens = load_tokens()
    pal = tokens["palette"]
    width, row_h = 1400, 120
    height = row_h * len(pal)
    img = Image.new("RGB", (width, height), hex_to_rgb("#070A0D"))
    draw = ImageDraw.Draw(img)
    font_path = find_font("heading")
    body_font_path = find_font("body")
    font = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
    body = ImageFont.truetype(body_font_path, 24) if body_font_path else ImageFont.load_default()

    y = 0
    for name, data in pal.items():
        color = data["hex"]
        draw.rectangle([0, y, 260, y + row_h], fill=hex_to_rgb(color))
        text_color = hex_to_rgb("#F3F1EA") if name not in ["warm_white", "paper"] else hex_to_rgb("#070A0D")
        draw.text((32, y + 32), color, fill=text_color, font=font)
        draw.text((300, y + 24), name, fill=hex_to_rgb("#F3F1EA"), font=font)
        draw.text((300, y + 68), data["role"], fill=hex_to_rgb("#C9A96A"), font=body)
        y += row_h

    out = ROOT / "outputs" / "assets" / "palette_preview.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(out)


if __name__ == "__main__":
    main()
