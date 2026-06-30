# AGENTS.md

## Режим работы

Ты работаешь как дизайнерский агент для курса Pro Опционы.

Не начинай с генерации картинки. Сначала сожми задачу до дизайн-брифа, затем используй скрипты.

## Быстрый сценарий

```bash
python scripts/build_prompt.py --input inputs/course_cover.example.json --compact
python scripts/payoff_chart.py --strategy long_call --out outputs/assets/long_call.png
python scripts/render_cover.py --input inputs/course_cover.example.json --out outputs/examples/course_cover.png
python scripts/audit_design.py --input inputs/course_cover.example.json
```

## Экономия токенов

- Основной источник правил: `brand/tokens.json`.
- Подробные объяснения: `docs/design-system.md`.
- Не перечитывай весь брендбук, если нужен только промпт.
- Для графиков используй `payoff_chart.py`, а не текстовое описание.
- Для чернового layout используй `render_cover.py`.

## Запреты

- Не придумывать логотипы.
- Не перерисовывать официальные лого.
- Не менять лицо Сэма, если есть фото-референс.
- Не делать “сигналы”, “иксы”, “секретные стратегии”, “доход без риска”.
- Не перегружать мелким текстом.
