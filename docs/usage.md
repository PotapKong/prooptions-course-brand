# Использование

## 1. Создать бриф

Скопировать один из файлов в `inputs/` и заменить заголовок, подзаголовок, формат, аудиторию и визуальный объект.

```bash
cp inputs/course_cover.example.json inputs/my_cover.json
```

## 2. Сгенерировать payoff-график

```bash
python scripts/payoff_chart.py --strategy long_call --out outputs/assets/long_call.png
```

Доступные стратегии:

- `long_call`
- `long_put`
- `short_call`
- `short_put`
- `bull_call_spread`
- `bull_put_spread`

## 3. Собрать черновой макет

```bash
python scripts/render_cover.py --input inputs/my_cover.json --out outputs/examples/my_cover.png
```

Этот рендер нужен не как финальная картинка, а как быстрый layout-черновик.

## 4. Собрать промпт для image model

```bash
python scripts/build_prompt.py --input inputs/my_cover.json --compact
```

## 5. Проверить бриф

```bash
python scripts/audit_design.py --input inputs/my_cover.json
```

Если аудит ругается на длину заголовка, перегруз или hype-слова, сначала исправить бриф.
