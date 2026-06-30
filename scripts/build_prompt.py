from __future__ import annotations

import argparse
import json
from pathlib import Path

from brand_config import load_tokens

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def compact_prompt(brief: dict, tokens: dict) -> str:
    pal = tokens["palette"]
    logo = tokens.get("canonical_logo", {})
    palette_line = ", ".join([
        f"{name} {data['hex']}" for name, data in pal.items()
        if name in [
            "base_black", "deep_green", "terminal_green", "warm_white", "graphite_gray",
            "champagne_gold", "course_logo_gold", "course_logo_white", "risk_red", "data_blue"
        ]
    ])
    avoid = brief.get("avoid") or tokens.get("banned_motifs", [])
    must_have = brief.get("must_have", [])
    refs = []
    if brief.get("person_reference"):
        refs.append(f"person refs: {brief['person_reference']}")
    logo_ref = brief.get("logo_reference") or logo.get("reference_file")
    if logo_ref:
        refs.append(f"canonical course logo: {logo_ref}")

    lines = [
        f"Create {brief.get('format', '16:9')} {brief.get('asset_type', 'visual')} for Pro Options beginner course.",
        "Style: premium trading terminal + calm learning system, expensive but not flashy.",
        f"Title: {brief.get('title', '')}",
    ]
    if brief.get("subtitle"):
        lines.append(f"Subtitle: {brief['subtitle']}")
    if brief.get("product_label"):
        lines.append(f"Small label: {brief['product_label']}")
    if brief.get("module_number"):
        lines.append(f"Module mark: МОДУЛЬ {brief['module_number']}")
    if brief.get("visual_object"):
        lines.append(f"Main visual object: {brief['visual_object']}")
    if brief.get("mentor"):
        lines.append(f"Mentor: {brief['mentor']}; preserve identity if photo reference is provided.")

    if logo:
        lines.append(
            "Logo lockup: use the canonical provided logo exactly: "
            f"{logo.get('main_text', 'ПРО ОПЦИОНЫ')} with ПРО white and ОПЦИОНЫ gold, "
            f"subtitle {logo.get('subtitle', 'для начинающих')} in white, thin geometric sans, wide tracking, centered."
        )

    lines.extend([
        f"Palette: {palette_line}.",
        "Composition: large readable title, one main visual object, subtle terminal grid, lots of negative space.",
        "Use payoff curves, option chain cards, strike lines, risk/profit zones where relevant.",
    ])
    if must_have:
        lines.append("Must have: " + "; ".join(must_have) + ".")
    if refs:
        lines.append("Use external references/assets, do not redraw logos from memory: " + "; ".join(refs) + ".")
    lines.append("Avoid: " + "; ".join(avoid) + ".")
    lines.append("No small text clutter. No profit guarantees. Red only for risk markers. Never alter the canonical logo text, colors or proportions.")
    return "\n".join(lines)


def full_prompt(brief: dict, tokens: dict) -> str:
    return compact_prompt(brief, tokens) + "\n\nDesign rationale:\n" + "\n".join([
        "The visual should reduce beginner anxiety and make options feel structured.",
        "The course should look like a professional trading desk, not like trading signals.",
        "Use dark graphite as the base, green for market logic, gold for premium micro-accents, red only for risk.",
        "The logo is a fixed asset and should not be reinterpreted.",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build compact image-generation prompt from course brief.")
    parser.add_argument("--input", required=True, help="Path to JSON brief")
    parser.add_argument("--compact", action="store_true", help="Print compact prompt")
    parser.add_argument("--out", help="Optional output .txt path")
    args = parser.parse_args()

    brief = load_json(args.input)
    tokens = load_tokens()
    prompt = compact_prompt(brief, tokens) if args.compact else full_prompt(brief, tokens)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(prompt, encoding="utf-8")
    print(prompt)


if __name__ == "__main__":
    main()
