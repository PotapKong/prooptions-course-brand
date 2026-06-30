# Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_project.py
python scripts/make_palette_preview.py
python scripts/payoff_chart.py --strategy long_call --out outputs/assets/long_call.png
python scripts/render_cover.py --input inputs/course_cover.example.json --out outputs/examples/course_cover.png
python scripts/build_prompt.py --input inputs/course_cover.example.json --compact
python scripts/audit_design.py --input inputs/course_cover.example.json
```
