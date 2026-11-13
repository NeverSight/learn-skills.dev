---
name: project-bootstrap
description: >
  Use when пользователь начинает новый проект, хочет расширить существующий, говорит "создай структуру",
  "разверни агента", "настрой проект", описывает новую задачу и хочет получить готовую агентскую среду.
  Создаёт агентскую инфраструктуру (AGENTS.md, SESSION_HANDOFF.md, .gitignore, .agents/memory, rules, skills, scripts; plan.md — опционально)
  с адаптацией под тип проекта (ops/код/агентский/контент) и модель (DeepSeek/GLM/Qwen/универсал).
  ROUTER: новый проект → project-bootstrap · план спринта → wave-spec · 2+ модели → multi-model-orchestration.
  Do NOT use для мелких правок, аудита, или задач внутри уже настроенного проекта.
disable-model-invocation: true
---

# project-bootstrap v2.2.0

Создаёт агентскую инфраструктуру с адаптацией под тип проекта, модель и сложность.
**Variant E + GRACE-якоря** — правила неизбежны: в преамбуле (primacy) и closing anchors (recency).

**Быстрый старт:** `bash scripts/classify_project.sh` → классификация → выбор шаблона → генерация → contradiction check → двойной аудит.

## TL;DR (minimum path)

**project-bootstrap = ДОМ для агента.** Создаёт AGENTS.md (Variant E: правила в преамбуле + closing anchors), SESSION_HANDOFF.md, .gitignore, `.agents/memory/MEMORY.md`, rules. Адаптация под тип (ops/code/agent/content) и модель (DeepSeek/GLM/Qwen/universal).

**Это точка входа.** После bootstrap: план спринта → `wave-spec`; нужно ≥2 моделей → `multi-model-orchestration`.

**Не использовать** для мелких правок/аудита/уже настроенного проекта (там режим расширения).

**Next step (вставить в сгенерированный AGENTS.md в Фазе 6)** — роутер-таблица, чтобы владелец видел навигацию в файле проекта:

| Хочу… | Скилл |
|---|---|
| Новый проект / настроить среду | project-bootstrap |
| Спланировать и сделать спринт (волну) | wave-spec |
| Обсудить / отревьюить 2+ моделями | multi-model-orchestration |

---

## Workflow

### Фаза 0: Классификация проекта

1. **Запусти классификатор:**
   ```bash
   bash scripts/classify_project.sh <project_dir>
   ```
2. **Прочитай вывод** — JSON с полями: `type`, `complexity`, `variant`, `model_profile`.
3. **Проверь существующий AGENTS.md:** `ls AGENTS.md 2>/dev/null` — если найден → **режим расширения** (не перезаписывать, дополнять).

**Типы проектов и приоритет гибридов** (ops > code > agent > content):

| Тип | Сигналы | Шаблон |
|-----|---------|--------|
| `ops` / `ops-code` | Docker, SSH, .env, nginx, продакшен-риски | Variant E полный (преамбула + чеклист + IF-THEN) |
| `code` / `code-content` | Исходники (py/ts/js), тесты, CI/CD | Variant E + GRACE-якоря |
| `agent` | Скиллы, агенты, промпты, модели | Variant E + модельно-специфичные CLOSING ANCHORS |
| `content` | Статьи, briefs, Excel, интеграции | Облегчённый: преамбула без тех. правил |
| `undetermined` | <3 файлов, нет AGENTS.md | Базовый шаблон с предложением доработать |

**Шкала сложности:**
- `TRIVIAL` — <3 файлов, нет AGENTS.md → простой шаблон, без VS-architect.
- `MODERATE` — 3-20 файлов или есть AGENTS.md → стандартный workflow.
- `UNCERTAIN` — >20 файлов, нестандартная структура → полный анализ + VS-architect.

**Режим расширения** (AGENTS.md существует):
1. Прочитай существующий AGENTS.md и MEMORY.md.
2. Определи текущую структуру — какие модули уже есть.
3. Примени Фазу 1 только к новым требованиям.
4. В Фазе 2 определи, что добавить (не дублировать).
5. При генерации сохрани существующие файлы, дополни AGENTS.md, создай только новое.
6. В сводке: что было, что добавлено.

---

### Фаза 1: Анализ «тёмных пятен»

Определи, что нужно уточнить ИЗВНЕ (не из памяти модели):

**1a. Внешние инструменты, API и технологии**
- webfetch/websearch: `"<name> best practices 2025 2026"`, `"<name> common pitfalls"`.
- **Не ищи CLI-синтаксис** для не-CLI-инструментов.
- Собери данные с источником: `<!-- source: https://..., YYYY-MM-DD -->`.
- Занеси в MEMORY.md → «Инструменты и ресурсы».

**1b. Существующие проекты**
- `glob ../**/.agents/memory/MEMORY.md` — известные грабли, процедуры.
- Если есть `.opencode/` — просканируй `.opencode/agents/` (не дублируй).

**1c. API и протоколы**
- webfetch документации: эндпоинты, аутентификация, лимиты.
- Занеси в MEMORY.md с источником.

**Decision Framework** — выбери архитектурные решения:

| Ситуация | Решение |
|----------|---------|
| Частая/защищённая операция | MCP (упомянуть в AGENTS.md) |
| Редкая/сложная операция | CLI-команда (commands/) |
| Цепочка действий | Скрипт в skills/*/scripts/ |
| Повторяемый workflow | Skill с SKILL.md |
| Разнотемпературные агенты | `.opencode/agents/` с model+temp |
| Аналитический проект | Multi-model cross-validation |
| Adversarial-проверка | review-агент + цикл review→fix |
| NDA/PII | rules/nda-anonymization.md |
| Бинарные форматы (DOCX, PDF) | scripts/ для экстракции |
| Методология >50 строк | `.agents/memory/<topic>-research.md` |

---

### Фаза 2: Определение структуры

На основе classified-типа и задачи определи модули `.agents/`:

| Модуль | Когда нужен |
|--------|-----------|
| `memory/MEMORY.md` | **Всегда** |
| `rules/general.md` | **Всегда** |
| `rules/*.md` | Повторяемые операции, безопасность |
| `.opencode/agents/` | Сабагенты с model/temperature |
| `agents/` | Role-play персоны |
| `commands/` | Повторяемые /-команды |
| `skills/` | Workflow из нескольких шагов |
| `skills/*/scripts/` | Детерминированные операции |
| `.agents/scripts/` | Утилиты для >1 скилла |
| `docs/` | Формальная спецификация (SPEC/PRD) |

**Выбор варианта AGENTS.md** — см. `references/variant-e-structure.md`:
- `variant-e-full` → полная преамбула + чеклист + closing anchors (DeepSeek).
- `variant-e-grace` → Variant E + GRACE-якоря в кодовых файлах.
- `variant-e-model` → модельно-специфичные closing anchors.
  - **Multi-model project type (3 operational rules):** если classify_project.sh детектит multi-model signals (orca orchestration, dispatch --inject, worker_done в контексте) → обязательно включить operational rules из `references/operational-rules.md` через `${OPERATIONAL_RULES_MULTI_MODEL}` placeholder в преамбуле + `${OPERATIONAL_RULES_RECENCY}` в closing anchors.
- `lightweight` → облегчённая преамбула без технических правил.
- `base` → базовый шаблон.

**Для UNCERTAIN-проектов:** запусти VS-architect для генерации альтернатив структуры.

---

### Фаза 3: Генерация файлов

#### 3a. Корневые файлы

**`plan.md` (ОПЦИОНАЛЬНЫЙ)** — шаблон `assets/templates/plan.md.tmpl`. Стратегический план: фазы, решения, блокеры. **БЕЗ статусов** (статусы → SESSION_HANDOFF.md).

**Когда создавать:** только если проект НЕ использует wave-spec для планирования. Если пользователь упоминает wave-spec или проект уже содержит `waves/` → пропустить plan.md, добавить примечание: «Для операционного планирования используй wave-spec (SPEC.xml + PLAN.xml)».

**Проверка перед созданием:** `ls waves/ 2>/dev/null` — если существует → plan.md НЕ создавать.

**`AGENTS.md`** — шаблон `assets/templates/AGENTS.md.tmpl`. Структура Variant E:
```
┌─ ЗАГОЛОВОК + описание проекта
├─ 🔴 ПРЕАМБУЛА: N ЖЕЛЕЗНЫХ ПРАВИЛ (IF-THEN)
├─ 📋 ЧЕКЛИСТ ПЕРЕД ДЕЙСТВИЕМ
├─ 📐 ПРОТОКОЛ (command-first)
├─ §1 Известные проблемы / Gotcha's
├─ §2 Failure Packet
├─ §3 Иерархия инструкций
├─ §4 Архитектура + Loaded Context (Progressive Disclosure)
├─ §5 Handoff между сессиями (полный протокол: override §21, append-only, crash-safe, чеклист)
└─ CLOSING ANCHORS (recency-зона, модельно-специфичные)
```

**Критические правила размещаются дважды:** в преамбуле (primacy) и в closing anchors (recency). Правила неизбежны.

**GRACE-якоря** — во всех генерируемых файлах (спецификация: `references/grace-anchors.md`):
```markdown
<!-- @rule id="F-01" priority="critical" -->
➡ Правило
<!-- @rule-end -->
```

**`SESSION_HANDOFF.md`** — шаблон `assets/templates/SESSION_HANDOFF.md.tmpl`. Append-only журнал сессий (каждая сессия дописывает блок). CONFIRMED_FACTS, UNRESOLVED_ISSUES, FAILED_APPROACHES, LEARNED_RULES → MEMORY.md (не дублировать).

**`.gitignore`** — создай обязательно:
```
# Secrets
*.env
# но НЕ .example

# Session state
SESSION_HANDOFF.md

# NDA / обезличенные данные
*_clean.txt
*.anon.*
mapping*.json

# OS files
.DS_Store
Thumbs.db
*.swp
*~
```

**Обнаружение данных:** `ls` корня → найди существующие папки (interview/, profile/). Включи в архитектуру AGENTS.md.

#### 3b. `.agents/memory/MEMORY.md`

Шаблон `assets/templates/MEMORY.md.tmpl`. Append-only. Секции:
- CONFIRMED_FACTS (с источниками)
- UNRESOLVED_ISSUES (severity: low/medium/high/critical)
- FAILED_APPROACHES
- Решения + отклонённые альтернативы
- Инструменты и ресурсы
- Известные ограничения
- Анти-паттерны

**GRACE-якоря:** `<!-- @anchor id="..." triggers="..." -->` на ключевых фактах.

#### 3c. `.agents/rules/general.md`

Шаблон `assets/templates/general-rule.md.tmpl`. GRACE-якоря на правилах и анти-паттернах.

#### 3d. Дополнительные модули

Создавай по необходимости (rules, agents, commands, skills, scripts, docs). Шаблоны — в `assets/templates/`.

**Обязательный скрипт:** скопируй `scripts/verify-handoff-gate.sh` (из скилла) в `.agents/scripts/verify-handoff-gate.sh` проекта. Используется в Фазе 4c.

---

### Фаза 4: Contradiction Check + Position Analysis

**4a. Cross-document contradiction check** (ВСЕГДА):

1. Прочитай все Level 1 файлы (AGENTS.md, MEMORY.md, general.md, SESSION_HANDOFF.md).
2. Ищи противоречия:
   - Правило в одном файле противоречит правилу в другом.
   - Команда в одном файле запрещена в другом.
   - Разные значения для одного параметра.
3. Классифицируй: MAJOR (нарушение = отказ) / MINOR (стилистика) / FALSE (разрешённое различие).
4. Исправь MAJOR-противоречия. Запиши в MEMORY.md.

**4b. Position analysis** (AGENTS.md > 200 строк):

1. Измерь позиции критических правил: строки относительно общей длины.
2. Если правила в зоне 30-80% (Lost in the Middle) → перемести в преамбулу или closing anchors.
3. Проверь, что @rule-якоря есть в начале И в конце.

**4c. Handoff-Destination Verification Gate** (ВСЕГДА, после 4b):

Запусти `bash .agents/scripts/verify-handoff-gate.sh`. Скрипт проверяет 4 правила:
1. В AGENTS.md нет handoff-данных (блоков `## Session Handoff — [DATE]`)
2. В AGENTS.md нет секции `## CONFIRMED_FACTS` (факты → MEMORY.md)
3. SESSION_HANDOFF.md содержит `append-only` в заголовке
4. MEMORY.md ссылается на SESSION_HANDOFF.md с `append-only`

Если FAIL → contradiction: handoff-данные или факты попали в AGENTS.md, либо нарушен append-only контракт. Исправь перед Фазой 5.

Если скрипта нет (legacy bootstrap) → выполни grep-проверки вручную.

---

### Фаза 5: Верификация + Двойной аудит

**5a. Базовая верификация:**
1. `read` каждого созданного файла — проверь, что читается.
2. AGENTS.md содержит Loaded Context для всех модулей.
3. Валидность YAML frontmatter.
4. `.gitignore` включает SESSION_HANDOFF.md и секреты.
5. `grep -c '@rule' AGENTS.md` > 0 и `grep -c '@anchor' MEMORY.md` > 0.
6. Handoff-целостность проверена в Фазе 4c (`verify-handoff-gate.sh`).

**5b. Двойной аудит** (ВСЕГДА):

Запусти двух аудиторов параллельно:
```
task(auditor) + task(auditor-glm)
```

Каждый проверяет:
- 0 MAJOR-противоречий между Level 1 файлами.
- AGENTS.md начинается с преамбулы (не архитектуры).
- Все шаблоны содержат GRACE-якоря.
- Handoff'ы не в AGENTS.md.
- CLOSING ANCHORS присутствуют (если модель DeepSeek).
- Правила неизбежны (primacy + recency).

Если любой аудитор нашёл MAJOR-блокер → назад в Фазу 3 (исправить и перегенерировать).

---

### Фаза 6: Capture + Сводка

**6a. Запись решений в MEMORY.md:**
- Принятые решения — что выбрано и почему.
- Отклонённые альтернативы — что рассматривалось и КОНКРЕТНЫЙ критерий отказа.
- Отложенное — что решено не делать сейчас и почему.

**6b. Сводка:** что создано, какие решения приняты, что добавить позже, какие альтернативы отклонены.

---

## Progressive Disclosure

Основной workflow — в этом файле. Детали — в references/:

| Файл | Когда читать |
|------|-------------|
| `references/variant-e-structure.md` | При генерации AGENTS.md — выбор структуры Variant E |
| `references/grace-anchors.md` | При вставке @rule/@anchor — схема и grep-команды |
| `references/model-profiles.md` | При выборе модельного профиля — DeepSeek vs GLM vs Qwen vs универсал |
| `references/playbook.md` | При создании модулей — condensed Agent Playbook |
| `references/workflow-patterns.md` | При выборе архитектуры skills — каталог паттернов |

---

## Переменные шаблонов

| Переменная | Шаблон | Что подставить | Откуда взять |
|-----------|--------|---------------|-------------|
| `${PROJECT_NAME}` | AGENTS.md, MEMORY.md, SESSION_HANDOFF, plan.md | Название проекта (1-3 слова) | Извлеки из задачи |
| `${PROJECT_DESCRIPTION}` | AGENTS.md | Краткое описание (1 строка) | Извлеки из задачи |
| `${DATE}` | AGENTS.md, MEMORY.md, plan.md | Текущая дата ISO | Системная дата |
| `${MODEL_PROFILE}` | AGENTS.md | Модельный профиль (deepseek/glm/qwen/universal) | Из classify_project.sh |
| `${PROJECT_FULL_DESCRIPTION}` | AGENTS.md | Полное описание (1 абзац) | Извлеки из задачи |
| `${PROJECT_DIR}` | AGENTS.md | Имя директории проекта | Текущая директория |
| `${ARCHITECTURE_TREE}` | AGENTS.md | Древовидная схема | Сгенерируй из структуры + `ls` |
| `${ARCHITECTURE_NOTES}` | AGENTS.md | Пояснения к архитектуре | Опиши неочевидные решения |
| `${LOADED_CONTEXT_L1}` | AGENTS.md | Level 1: всегда | MEMORY.md + general.md + SESSION_HANDOFF.md (append-only) |
| `${LOADED_CONTEXT_L2}` | AGENTS.md | Level 2: по триггеру | Rules с триггер-словами |
| `${LOADED_CONTEXT_L3}` | AGENTS.md | Level 3: on-demand | Skills, commands, agents |
| `${PREAMBLE_RULES}` | AGENTS.md | N железных правил IF-THEN (преамбула) | Извлеки из задачи |
| `${OPERATIONAL_RULES_MULTI_MODEL}` | AGENTS.md | 3 operational rules IF-THEN (multi-model projects only) | Include если project type = agent/multi-model; иначе empty |
| `${CLOSING_ANCHORS}` | AGENTS.md | Правила в recency-зоне | Дубликат PREAMBLE_RULES + модельные якоря |
| `${OPERATIONAL_RULES_RECENCY}` | AGENTS.md | 3 compressed operational rule one-liners (multi-model projects only) | Include если project type = agent/multi-model; иначе empty |
| `${WORK_PROTOCOL}` | AGENTS.md | Command-first протокол | Конкретные команды |
| `${SETUP_COMMANDS}` | AGENTS.md | Команды настройки | Если нужны |
| `${INIT_NOTE}` | AGENTS.md | Заметка о создании | «Агентская инфраструктура v2, модули: ...» |
| `${CHECKLIST_ITEMS}` | AGENTS.md | Чеклист перед действием | Извлеки из задачи |
| `${GOTCHAS}` | AGENTS.md | Известные проблемы | Из фазы 1 |
| `${FAILURE_PACKET}` | AGENTS.md | Формат failure packet | Стандартный |
| `${INSTRUCTION_HIERARCHY}` | AGENTS.md | Иерархия инструкций | AGENTS.md > HANDBOOK > правила |
| `${FACTS}` | MEMORY.md | Подтверждённые факты | Из фазы 1 (webfetch) |
| `${INIT_CONTEXT}` | MEMORY.md | Контекст создания | Из задачи |
| `${INIT_DECISIONS}` | MEMORY.md | Принятые решения | Ключевые выборы |
| `${TOOLS_AND_RESOURCES}` | MEMORY.md | Инструменты | Из фазы 1a с источниками |
| `${LIMITATIONS}` | MEMORY.md | Ограничения | Из webfetch |
| `${ANTIPATTERNS}` | MEMORY.md | Чего не делать | Из webfetch + общие |
| `${INIT_EVENT}` | MEMORY.md | Событие создания | Описание структуры |
| `${RULE_FRONTMATTER_EXTRA}` | rule.md | Доп. поля frontmatter | Опционально |
| `${RULE_NAME}` | rule.md | Имя (kebab-case) | Из задачи |
| `${RULE_DESCRIPTION}` | rule.md | **Когда** применять | Триггер-контекст |
| `${RULE_APPLIES_TO}` | rule.md | Glob-маски | `["**/*"]` или специфичные |
| `${RULE_PRIORITY}` | rule.md | low/medium/high/critical | critical для безопасности |
| `${RULE_TITLE}` | rule.md | Заголовок | Человекочитаемое |
| `${RULE_CONTENT}` | rule.md | Тело правила | Из задачи + webfetch |
| `${COMMAND_NAME}` | command.md | Имя команды | kebab-case |
| `${COMMAND_DESCRIPTION}` | command.md | **Когда** применять | Триггер-контекст |
| `${AGENT_NAME}` | agent-persona.md | Имя сабагента | Из задачи |
| `${AGENT_INVOKE}` | agent-persona.md | Триггер (`@role`) | Из задачи |
| `${AGENT_DESCRIPTION}` | agent-persona.md | **Когда** вызывать | Триггер-контекст |
| `${SKILL_NAME}` | SKILL.md | Имя (kebab-case) | Из задачи |
| `${SKILL_DESCRIPTION}` | SKILL.md | **Когда** использовать | Триггер-контекст |
| `${AGENT_MODEL}` | opencode-agent.md | Модель | Из задачи |
| `${AGENT_TEMPERATURE}` | opencode-agent.md | Temperature | Из задачи |
| `${NDA_WHITELIST}` | nda-anonymization.md | Белый список | Из задачи |

---

## Что НЕ делать

- **НЕ** задавать больше 2 уточняющих вопросов.
- **НЕ** спрашивать «нужны ли тебе agents/?» — определи по задаче.
- **НЕ** галлюцинировать факты. Не знаешь → `<!-- TODO -->` в MEMORY.md.
- **НЕ** создавать избыточные модули.
- **НЕ** полагаться на память модели для синтаксиса — проверяй через webfetch.
- **НЕ** хранить пароли/токены в `.agents/`.
- **НЕ** требовать формальной спецификации.
- **НЕ** коммитить SESSION_HANDOFF.md.
- **НЕ** размещать handoff-данные в AGENTS.md — только ссылки.
- **НЕ** пропускать contradiction check — он обязателен.
- **НЕ** пропускать двойной аудит — он обязателен.
- **НЕ** вписывать доменные паттерны в скилл — модель сама определит структуру.

---

## Примеры

### Технический проект: бекапы серверов

**Пользователь:** «Надо бекапить 3 сервера на Backblaze B2. SSH-ключи в ~/.ssh/config.»

**Скилл:** classify → ops → Variant E полный → webfetch b2/restic CLI → создаёт AGENTS.md (преамбула: backup перед каждым действием), SESSION_HANDOFF.md, .gitignore, b2.env.example, MEMORY.md, rules/backup-procedures.md, rules/restore-procedures.md, commands/backup-status.md → contradiction check → двойной аудит.

### Контент-проект: поиск работы

**Пользователь:** «Хочу проект для поиска работы: обработка вакансий, резюме под разные роли. Есть данные в interview/ и profile/.»

**Скилл:** classify → content → lightweight → `ls` → видит данные → webfetch hh.ru API → создаёт AGENTS.md (облегчённая преамбула), SESSION_HANDOFF.md, .gitignore, MEMORY.md, skills/match-vacancy/, skills/compile-resume/ → contradiction check → двойной аудит.

---

## Cross-skill compatibility

project-bootstrap creates the agent infrastructure that other skills build upon.

### After bootstrap (recommended)
1. **wave-spec** — creates SPEC.xml + PLAN.xml for wave-based planning with lifecycle gates
2. **multi-model-orchestration** — executes dispatch/review via Orca for multi-model workflows

### plan.md policy
- **По умолчанию НЕ создаётся.** Wave-spec PLAN.xml покрывает операционное планирование.
- Создаётся только если: (a) проект НЕ использует wave-spec, (b) пользователь явно запросил.
- Проверка: `ls waves/ 2>/dev/null` — если существует → plan.md пропускается.

---
## Ссылки

- `references/variant-e-structure.md` — структура Variant E
- `references/grace-anchors.md` — спецификация GRACE-якорей
- `references/model-profiles.md` — DeepSeek vs GLM vs Qwen vs универсал
- `references/playbook.md` — Agent Playbook condensed
- `references/workflow-patterns.md` — каталог паттернов
- `scripts/classify_project.sh` — авто-классификация проекта
