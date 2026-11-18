---
name: jira-writer
description: >-
  Prepares concise Jira-ready Russian issue drafts (title, structured description,
  acceptance criteria). Use when the user asks for a Jira task, backlog item, bug,
  spike, technical task, acceptance criteria, or a paste-ready issue before implementation.
---

# Jira Writer

Produces text for manual paste into Jira (no API). Convention mirrors a typical `jira-writer` agent role: short issue, verifiable acceptance criteria.

## When to apply

- User says «напиши задачу», «написать задачу», «сделай задачу» — always Jira, no clarifying questions.
- Formulate or refine a Jira task, bug, spike, or tech debt item.
- Need a ready-to-paste title + description + acceptance criteria.
- Summarize planned or completed work as an issue (scope framing only).

## Output language

- **Issue text (Название, Описание, Критерии приемки, Дополнительно): Russian only.**

## Output format

Always output the issue in **Jira Wiki Markup** so the user can paste it directly into Jira:

- Headings: `h2.`, `h3.`
- Bullet lists: `*` (not `-`)
- Bold: `*text*`
- Code: `{{text}}` inline for **simple identifiers only** (letters, digits, underscores, parentheses — e.g. `{{getAddresses()}}`, `{{bpm_id}}`), `{code}...{code}` blocks
- **Never use `{{...}}` when the content contains dots (`.`), colons (`:`), angle brackets (`<>`), or spaces** — Jira treats `{{a.b}}` and `{{id: type}}` as unknown macros. Write such expressions as plain text or restructure the sentence. Examples: `{{care.repository.ts}}` → write as plain text `care.repository.ts`; `{{created_at ASC}}` → write as plain text `created_at ASC`; `{{addresses.name}}` → write as plain text `addresses.name`.
- **Never end a bullet point with `{{text}}`** — Jira fails to render the last `{{...}}` on a line. Always add a word or punctuation after it. This applies to ALL identifiers at end of line, including TypeScript type names, field names, method names. BAD: `* Секция: {{details}}` — GOOD: `* Секция: поле {{details}} (текст запроса)`; BAD: `* Метод {{findById(id)}}` — GOOD: `* Метод {{findById(id)}} в репозитории`.

Split the output into **two separate fenced code blocks** so the user can copy each part independently in Plannotator:

1. First block — the title only, plain text without any heading markup (no `h2.` prefix).
2. Second block — everything else, starting directly with `h3. Контекст` (omit the `h2. Описание` heading entirely).

Never wrap the entire issue in a single fenced code block.

## Approval: plannotator annotate loop (no Plan Mode)

Native Plan Mode is not used. Approve the draft through `rules/skills/document-approval.md`: stable path, `plannotator annotate --gate --json`, reopen the same file after edits.

When writing to a temp file for use with `plannotator annotate`, write the file in **Jira Wiki Markup only** — no Markdown, no fenced code block wrapper. Use `.md` extension (plannotator does not support `.txt`). This allows the user to copy the content directly from Plannotator into Jira without any conversion.

**Why a file, not `plannotator last`:** `plannotator last` reads the previous completed turn. Since the issue and the Bash call happen in the same turn, `plannotator last` always captures the wrong message. Writing to a file and using `plannotator annotate` bypasses this entirely.

## Output structure (use these headings)

### Название

- Pattern: **optional `[context]` prefix(es) + action + object + goal/result**.
- Short, specific, implementation-oriented.
- Avoid vague titles ("Доработать логику", "Исправить баг").
- **Context prefixes — up to 2, in square brackets, before the title text.** A context prefix names the kind of work or the affected scope, e.g. `[тех-долг]`, `[web]`, `[api-gateway]`. Add one when it isn't obvious from the description alone (bug/feature work in a known app doesn't need it; tech debt, security hardening, or work spanning a specific app/component benefits from it). Never stack more than 2 — if a third context seems needed, drop the least essential one or fold it into the description instead. Example: `[тех-долг] Закрыть open redirect на странице /api/error`, `[api-gateway] Добавить повторную синхронизацию при частичном сбое смены статуса`.

### Описание

Use up to three subsections (Решение may be omitted, see below):

1. **Контекст** — why the task exists now. **1 sentence, hard cap.** State where this came from (an audit, a roadmap, an incident) and why it matters right now — nothing else. Background, scope notes, and "заодно..." asides belong in Проблема/Решение if they're load-bearing, or nowhere if they aren't. If the sentence isn't answering "why now", cut it.
2. **Проблема** — what is broken, missing, or inefficient. **Max 3 bullets** (`*`), one distinct problem per bullet, each **one line**. Merge related facts; drop minor ones instead of listing everything. One problem — one short sentence, no list. State the fact, let its severity speak for itself.
3. **Решение** — the direction of the change: what must move, be added, or be replaced, and roughly where. **Max 3 bullets**, each one line. **State direction, not a design doc.** Name the affected module/domain/layer (e.g. "модуль orders в api-gateway", "общие компоненты карточки заказа") so both a human and an AI implementer know unambiguously where to go — but do not name specific classes, method signatures, exact input()/output() shapes, or file paths unless a name is genuinely load-bearing (e.g. an existing thing being reused or removed, where ambiguity would send the implementer to the wrong file). The detailed design belongs to the later implementation plan (`writing-plans`), not the issue.
   **Omit Решение for a bug whose fix is just "make it behave as expected"** — Проблема plus Критерии приемки already say everything. Keep it only when the direction isn't obvious from the problem.

**Style — short and direct.** One sentence ≤ ~15 words, no introductory phrases, no formal connectors ("в связи с тем что", "необходимо отметить", "подтверждённый"), no stacked qualifiers. Plain words, but keep the technical specifics: cut words, not facts.

### Критерии приемки

- Flat checklist of **3–5** **observable, testable** outcomes, each one line.
- **Do not restate Решение.** Include only what can be verified from outside and is not obvious from Решение. If a criterion is just the Решение bullet in past tense — drop it.
- For bugs: include **expected behavior**, not only the symptom.
- For features: describe **user or system outcome**, not only implementation steps.

### Дополнительно

Include **only** when necessary to remove ambiguity: assumptions, dependencies, technical notes, or blocking questions.

By default **do not** add sections: `Объем`, `Технические заметки`, `Открытые вопросы` (unless the user asked or the task would stay ambiguous without them).

## Writing rules

- Brevity over completeness: if a sentence or bullet can be cut without losing a fact the implementer needs, cut it.
- Prefer precise product/technical nouns over generic wording.
- If details are missing: state **minimal explicit assumptions**; do not invent hidden requirements or external business context not given by the user or repo.
- Do not merge implementation status / changelog into the draft unless the user asked.
- Do not turn the issue into a full design document unless the user asked for that depth.
- Do not overload with scope boundaries and meta-notes by default.

## Optional inputs (ask only if blocking)

- Issue type (Story/Bug/Task/Spike), epic/link, priority, component, affected product or service.

## Template (copy and fill)

```
<Название задачи>
```

```
h3. Контекст
…

h3. Проблема
…

h3. Решение
…

h3. Критерии приемки
* …
* …
```

For a simple bug, drop the `h3. Решение` block entirely.

## After output

Approval flow (no native Plan Mode; see `rules/skills/document-approval.md`):

1. Write the issue draft into `tmp/drafts/<issue-slug>.md`, using the same two-block structure as the chat output: first block — title only; second block — body in Jira Wiki Markup, starting at `h3. Контекст`.
2. Open it with `plannotator annotate --gate --json` (version history on) and wait for the final decision.
3. If annotation feedback comes back — revise the same file and reopen it.
4. `dismissed` — stop, nothing is approved.
5. Once approved as-is (no annotation feedback) — do NOT reprint the issue text in chat. The user already saw and approved the exact draft via Plannotator/the approval flow; repeating it in chat is a pure duplicate. Just move on to the next step (e.g. writing-plans).
