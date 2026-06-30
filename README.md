# Pro Options Course Design Skill

Скилл для оформления базового курса по биржевым опционам Сэма Шарипова / Pro Опционы.

Цель: быстро собирать обложки курса, обложки модулей, слайды, визуальные схемы, payoff-графики и промпты для генерации изображений в единой стилистике: дорогой трейдерский терминал, спокойная учебная система, без офисной вычурности и без инфобиз-неона.

## Что внутри

```text
brand/                  дизайн-токены, брендбук, палитра, правила
brand/logos/            сюда добавить официальные лого проекта и партнёров
references/approved/    утверждённые визуалы и лучшие референсы
references/rejected/    анти-референсы, что нельзя повторять
references/sam_photos/  фото Сэма для сохранения узнаваемости
references/course_screens/ скриншоты терминала, графики, таблицы, lesson frames
inputs/                 JSON-брифы для генерации
outputs/                результаты скриптов
scripts/                генераторы, аудиторы, компоновщики промптов
docs/                   подробная документация
templates/              текстовые шаблоны для уроков, модулей, обложек
SKILL.md                основная инструкция для агента
AGENTS.md               короткий runbook для Codex/Claude/Hermes
```

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/make_palette_preview.py
python scripts/payoff_chart.py --strategy long_call --out outputs/assets/long_call.png
python scripts/render_cover.py --input inputs/course_cover.example.json --out outputs/examples/course_cover.png
python scripts/build_prompt.py --input inputs/course_cover.example.json --compact
python scripts/audit_design.py --input inputs/course_cover.example.json
```

## Основная идея стиля

**Премиальный торговый терминал + спокойная учебная система.**

Не “трейдинг-сигналы”, не крипто-неон, не офисная презентация. Визуал должен выглядеть как продукт практика, который системно объясняет сложный инструмент новичкам.

## Базовая палитра

| Роль | HEX |
|---|---:|
| Base Black | `#070A0D` |
| Deep Green | `#06251C` |
| Terminal Green | `#16C784` |
| Warm White | `#F3F1EA` |
| Graphite Gray | `#20262D` |
| Champagne Gold | `#C9A96A` |
| Risk Red | `#D94A4A` |
| Data Blue | `#4A90E2` |

## Где экономятся токены агента

1. Агент читает сначала `brand/tokens.json`, а не весь брендбук.
2. Скрипт `build_prompt.py` собирает короткий промпт из брифа, палитры и правил.
3. `payoff_chart.py` генерирует графики опциона кодом, без описания графиков в промпте.
4. `render_cover.py` делает быстрый черновой макет без генеративной модели.
5. `audit_design.py` проверяет словесный перегруз, banned-элементы и соответствие палитре.

## Что нужно добавить вручную

- официальное лого Pro Опционы или курса в `brand/logos/`;
- утверждённые обложки и визуалы в `references/approved/`;
- фото Сэма в `references/sam_photos/`;
- анти-референсы в `references/rejected/`, чтобы агент понимал, чего избегать.

## Рекомендуемое имя репозитория

`pro-options-course-design-skill`
