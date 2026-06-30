from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from brand_config import find_font, hex_to_rgb, palette

FORMATS = {
    "16:9": (1920, 1080),
    "1080x1350": (1080, 1350),
    "1:1": (1080, 1080),
    "9:16": (1080, 1920),
}


def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def font(kind: str, size: int):
    path = find_font(kind)
    return ImageFont.truetype(path, size) if path else ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj, max_width: int) -> list[str]:
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_grid(draw: ImageDraw.ImageDraw, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    w, h = size
    step = max(48, w // 28)
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=color, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=color, width=1)


def draw_payoff_like(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], pal: dict[str, str]) -> None:
    x1, y1, x2, y2 = box
    w, h = x2 - x1, y2 - y1
    base_y = y1 + int(h * 0.62)
    strike_x = x1 + int(w * 0.46)
    draw.rounded_rectangle(box, radius=28, outline=hex_to_rgb(pal["graphite_gray"]), width=2, fill=hex_to_rgb("#0D1318"))
    draw.line([(x1 + 40, base_y), (x2 - 40, base_y)], fill=hex_to_rgb(pal["graphite_gray"]), width=3)
    draw.line([(strike_x, y1 + 40), (strike_x, y2 - 40)], fill=hex_to_rgb(pal["champagne_gold"]), width=2)
    pts = []
    for i in range(80):
        t = i / 79
        x = x1 + 50 + t * (w - 100)
        y = base_y + 80 if x < strike_x else base_y + 80 - ((x - strike_x) / (x2 - strike_x - 50)) * (h * 0.58)
        pts.append((x, y))
    draw.line(pts, fill=hex_to_rgb(pal["terminal_green"]), width=7, joint="curve")
    draw.text((x1 + 42, y1 + 34), "PAYOFF", fill=hex_to_rgb(pal["warm_white"]), font=font("mono", 28))
    draw.text((strike_x + 12, y2 - 78), "STRIKE", fill=hex_to_rgb(pal["champagne_gold"]), font=font("mono", 22))


def render(brief: dict, out: str | Path) -> Path:
    pal = palette()
    width, height = FORMATS.get(brief.get("format", "16:9"), FORMATS["16:9"])
    img = Image.new("RGB", (width, height), hex_to_rgb(pal["base_black"]))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, height], fill=hex_to_rgb(pal["base_black"]))
    draw_grid(draw, (width, height), tuple(int(c * 0.18) for c in hex_to_rgb(pal["warm_white"])))
    draw.ellipse([int(width * 0.58), -int(height * 0.28), int(width * 1.18), int(height * 0.55)], fill=hex_to_rgb(pal["deep_green"]))
    draw.ellipse([-int(width * 0.18), int(height * 0.65), int(width * 0.45), int(height * 1.22)], fill=hex_to_rgb("#0B1515"))

    margin = int(width * 0.07)
    top = int(height * 0.12)
    title = brief.get("title", "ОПЦИОНЫ С НУЛЯ")
    subtitle = brief.get("subtitle", "")
    product = brief.get("product_label", "Базовый курс · Pro Опционы")
    module = brief.get("module_number")

    title_size = int(width * (0.062 if width > height else 0.085))
    sub_size = int(width * (0.023 if width > height else 0.040))
    label_size = int(width * (0.018 if width > height else 0.030))
    title_font = font("heading", title_size)
    sub_font = font("body", sub_size)
    mono_font = font("mono", label_size)
    max_text_width = int(width * (0.52 if width > height else 0.82))

    if module:
        draw.rounded_rectangle([margin, int(height * 0.055), margin + int(width * 0.18), int(height * 0.105)], radius=18, fill=hex_to_rgb(pal["champagne_gold"]))
        draw.text((margin + 22, int(height * 0.066)), f"МОДУЛЬ {module}", fill=hex_to_rgb(pal["base_black"]), font=mono_font)

    y = top
    for line in wrap_text(draw, title, title_font, max_text_width):
        draw.text((margin, y), line, fill=hex_to_rgb(pal["warm_white"]), font=title_font)
        y += int(title_size * 1.04)

    y += int(height * 0.03)
    if subtitle:
        for line in wrap_text(draw, subtitle, sub_font, max_text_width):
            draw.text((margin, y), line, fill=hex_to_rgb(pal["champagne_gold"]), font=sub_font)
            y += int(sub_size * 1.35)

    box = (int(width * 0.57), int(height * 0.23), int(width * 0.94), int(height * 0.78)) if width > height else (int(width * 0.12), int(height * 0.55), int(width * 0.88), int(height * 0.85))
    draw_payoff_like(draw, box, pal)

    draw.line([(margin, height - int(height * 0.11)), (width - margin, height - int(height * 0.11))], fill=hex_to_rgb(pal["graphite_gray"]), width=2)
    draw.text((margin, height - int(height * 0.08)), product, fill=hex_to_rgb(pal["terminal_green"]), font=mono_font)

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render draft course/module cover from JSON brief.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="outputs/examples/cover.png")
    args = parser.parse_args()
    print(render(load_json(args.input), args.out))


if __name__ == "__main__":
    main()
