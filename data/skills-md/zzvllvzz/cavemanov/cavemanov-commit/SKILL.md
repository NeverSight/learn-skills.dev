---
name: cavemanov-commit
description: >
  Генерация кратких сообщений коммита в формате Conventional Commits.
  Используй когда пользователь просит сгенерировать коммит, описание изменений
  для git, или вызывает /cavemanov-commit.
---

Генерируй краткое сообщение коммита для текущих staged изменений.

## Формат

Conventional Commits. Структура: `<тип>(<область>): <описание>`

Типы: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`

## Правила

- Subject: ≤50 символов, императив, нижний регистр после типа
- Без точки в конце subject
- Body: только когда "почему" неочевидно из subject
- Объяснять **почему**, а не **что** — `git diff` уже показывает что
- Пустая строка между subject и body
- Body: обёртка на 72 символа

## Примеры

Хорошо:
```
fix(auth): check token expiry with strict inequality

Previous check used `<=` which accepted tokens at exact expiry time.
Clock skew between services caused intermittent 401s.
```

Хорошо (самодостаточный subject):
```
docs: fix typo in README install instructions
```

Плохо:
```
Updated some files.
```

Плохо (повтор того что показывает diff):
```
feat: add new function called validateInput to utils.js
```

## Процесс

1. Прочитать `git diff --cached`
2. Определить тип и область изменения
3. Написать subject (≤50 символов, императив)
4. Решить нужен ли body — нужен только если "почему" неочевидно
5. Вывести готовое сообщение одним блоком без пояснений
