from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = [
    "brand/logos/pro-options",
    "brand/logos/partners",
    "references/approved",
    "references/rejected",
    "references/sam_photos",
    "references/course_screens",
    "outputs/assets",
    "outputs/examples",
]


def main() -> None:
    for folder in FOLDERS:
        path = ROOT / folder
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
