---
name: openspec-proposal
description: "Создать новое OpenSpec предложение изменения. Scaffold proposal.md, tasks.md, design.md и spec deltas."
argument-hint: <описание изменения>
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# /openspec-proposal — Создание предложения изменения

**Guardrails**
- Минимальные реализации — добавляй сложность только когда запрошено
- Строго в рамках запрошенного результата
- Читай `openspec/AGENTS.md` для соглашений OpenSpec
- Выявляй неясности и задавай уточняющие вопросы ДО редактирования файлов
- НЕ пиши код на этапе proposal. Только документы (proposal.md, tasks.md, design.md, spec deltas)

**Steps**
1. Прочитай `openspec/project.md`, проверь `openspec/changes/` и `openspec/specs/`, изучи связанный код через Grep/Glob
2. Выбери уникальный `change-id` (глагол-существительное) и создай scaffold в `openspec/changes/<id>/`:
   - `proposal.md` — что, зачем, влияние
   - `tasks.md` — упорядоченный чеклист задач
   - `design.md` — архитектурные решения (если нужно)
3. Маппинг изменения в конкретные capabilities, разбей на spec deltas
4. Draft spec deltas в `changes/<id>/specs/<capability>/spec.md`:
   - Используй `## ADDED|MODIFIED|REMOVED Requirements`
   - Минимум один `#### Scenario:` на каждый requirement
5. Draft `tasks.md` — упорядоченный список верифицируемых задач
6. Валидируй через `openspec validate <id> --strict` (если CLI доступен) или ручная проверка

**Reference**
- Поиск существующих requirements: `Grep "Requirement:|Scenario:" openspec/specs/`
- Изучай кодовую базу через Grep/Glob для alignment с текущей реализацией
