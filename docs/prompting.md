# Prompting Rules

## Как писать промпт

Промпт должен быть коротким и управляемым.

Структура:

1. Формат и тип ассета.
2. Заголовок и подзаголовок.
3. Композиция.
4. Палитра.
5. Визуальный объект.
6. Референсы.
7. Запреты.
8. Требования к читаемости.

## Пример

```text
Create 16:9 course cover for Pro Options beginner course.
Style: premium trading terminal + calm learning system, expensive but not flashy.
Title: ОПЦИОНЫ С НУЛЯ
Subtitle: От Call и Put до первых стратегий и управления риском
Main visual object: payoff curve + option chain card
Palette: base black #070A0D, deep green #06251C, terminal green #16C784, warm white #F3F1EA, champagne gold #C9A96A.
Composition: large readable title left, mentor/photo or payoff graph right, subtle terminal grid, lots of negative space.
Avoid: rockets, cash, casino, crypto neon, aggressive red, office glam, profit guarantees.
```

## Когда использовать фото Сэма

Если в задаче нужен человек, использовать `references/sam_photos/`.

Не описывать лицо с нуля, если есть референс. Задача модели: сохранить узнаваемость.

## Когда использовать код

- Payoff-графики всегда лучше генерировать кодом.
- Палитры и черновые layout лучше генерировать скриптами.
- Image model использовать для финального визуального объединения, атмосферы и сложной композиции.
