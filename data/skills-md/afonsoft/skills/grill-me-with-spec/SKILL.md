---
name: grill-me-with-spec
license: MIT
description: Use when the user needs to create or refine a feature SPEC SDD before implementation. Interviews the user in Portuguese, builds a design tree, and writes `.specs/SPEC-{YYYYMMDD}-{feature}.md` following the SDD template. Do NOT use for writing implementation code or after the SPEC is approved. Part of the afonsoft/skills collection.
metadata:
  version: "1.1.0"
  visibility: public
  author: afonsoft
  url: https://github.com/afonsoft/skills
---

# Grill me with SPEC

## Overview

Interview the user relentlessly in **Portuguese (pt-BR)** until a shared understanding is reached, then write a complete SPEC SDD (Spec-Driven Development document) in `.specs/SPEC-{YYYYMMDD}-{feature}.md`. The SPEC becomes the single source of truth before any implementation.

All questions directed at the user must be in Portuguese. This skill itself and internal reasoning are written in English.

## When to Use

- The user asks for a new feature, change, bugfix, or refactor.
- A request is ambiguous, underspecified, or needs clarification.
- Before any implementation begins.
- The existing SPEC is outdated and needs refinement.

- User asks or mentions this skill in English (e.g., "use /grill-me-with-spec", "run grill-me-with-spec").
- O usuário pede ou menciona esta skill em português (ex.: "use /grill-me-with-spec", "execute grill-me-with-spec").

## When NOT to Use

- Do not use for implementation — that is the job of the implementation skill (`/execute-tdd-spec`, etc.).
- Do not use when a SPEC already exists and is approved and the user only wants execution.
- Do not use when the user explicitly refuses to provide requirements.

## Core Principles

1. **No guessing.** If a fact is missing, ask the user. If the user declines, mark it `[A DEFINIR]` in the SPEC.
2. **No implementation.** Never write implementation code. The output is the SPEC only.
3. **Shared understanding first.** The session ends only when the design-tree frontier is empty.
4. **Evidence-based.** Look up repository, docs, and code facts with sub-agents. Do not ask the user for things you can find yourself.

## The Design Tree

Map the request as a **design tree**: every decision branches into the decisions that depend on it.

- **Root**: the original user request.
- **Nodes**: decisions to be made.
- **Edges**: dependencies between decisions.
- **Frontier**: decisions whose prerequisites are settled and can be asked now.

Work the tree in **rounds**. Ask the whole frontier in one round, then wait for the user's answers before the next round. A question whose answer depends on another still-open question belongs to a later round. The session is done when the frontier is empty.

## Round Format

Every round is addressed to the user and must be in Portuguese:

```text
❓ **Q1** - **<titulo da pergunta em pt-BR>**: <corpo da pergunta em pt-BR>

➡️ <sua resposta recomendada em pt-BR>

---

❓ **Q2** - **<titulo da pergunta em pt-BR>**: <corpo da pergunta em pt-BR>

➡️ <sua resposta recomendada em pt-BR>
```

Always include a **recommended answer**. This accelerates convergence and tests whether the user agrees.

## Question Categories

Ask at least one round covering each category. You do not need to ask every question — only the ones relevant to the frontier.

### Identity

- What is the short name (kebab-case) for this feature?
- What type is it: `Feature | Bugfix | Refactor | API | Infra | Frontend | Docs`?
- Which repository and branch will hold it?
- Is there an existing ticket or parent Issue?

### Domain

- What is the business problem being solved?
- Who is the primary user or persona?
- What is the desired outcome or benefit?
- What does success look like?

### Scope

- What is in scope?
- What is explicitly out of scope?
- What would a user assume is included but is not?

### Stack and Architecture

- Which stack or framework is affected?
- Which layers, modules, or services change?
- Which files must be read before implementing?
- Which files will be created or modified?

### Data and State

- What data is consumed or produced?
- What are the entities, fields, and types?
- Is there a migration, schema change, or new persistence?

### API and Contracts

- Does the feature expose or consume an API?
- What are the endpoints, methods, headers, auth, request/response shapes?
- What are the expected errors?

### UI / UX

- Are there user-facing screens, components, or flows?
- What are the happy and unhappy paths?
- What accessibility or responsiveness constraints apply?

### Security and Compliance

- What authentication or authorization is required?
- Is any PII or sensitive data involved?
- Are there rate limits, audit, or privacy requirements?

### Observability

- How is the feature monitored, logged, or traced?
- What metrics or alerts should exist?

### Validation

- What is the minimum verification evidence (tests, lint, build)?
- What coverage or quality gate is required?
- What is the deployment or release path?

## Example Round in Portuguese

```text
Vamos consolidar o escopo antes de seguir. Aqui estao as perguntas que preciso que voce confirme:

❓ **Q1** - **Nome da funcionalidade**: Qual nome curto voce quer usar para essa feature? (ex: `notificacao-push`, `relatorio-mensal`)

➡️ Meu palpite: `notificacao-push`

---

❓ **Q2** - **Tipo de entrega**: Isso e uma Feature nova, Refactor, Bugfix, API ou Infra?

➡️ Meu palpite: `Feature`

---

❓ **Q3** - **Stack afetada**: Qual linguagem/framework principal sera alterado? (ex: .NET 8, Next.js 14, Python 3.12)

➡️ Meu palpite: `Next.js 14`

---

❓ **Q4** - **Fora de escopo**: O que NAO devemos incluir nessa entrega? Liste 2-3 itens explicitamente.

➡️ Meu palpite: painel administrativo, configuracao de templates, mobile nativo
```

## Fact Gathering

Finding facts is the agent's job, never the user's. When a frontier question needs a fact from the environment (file system, tools, docs, code), dispatch a sub-agent to find it. Do not ask the user for anything you could look up yourself. Do not block: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now.

## Writing the SPEC SDD

Once the design tree is settled, create `.specs/SPEC-{YYYYMMDD}-{feature}.md` by filling the template in `references/spec-sdd-template.md`. The parent agent must read the SPEC and wait for user approval before implementation.

The SPEC must include all sections 0-9:

0. **Metadata** — feature, type, stack, repository, branch, ticket, status.
1. **User Story** — As a / I want / So that, plus problem context.
2. **Scope** — in scope and out of scope.
3. **Technical Context** — where the change happens, files to read, files to create/modify.
4. **Requirements** — numbered, verifiable requirements with input/output.
5. **API Contract** — only if the feature exposes/consumes an API.
6. **Acceptance Criteria** — BDD scenarios and edge cases.
7. **Task Plan** — ordered, small tasks with validation strategy.
8. **Organization Guardrails** — branch policy, security, scope, architecture.
9. **Definition of Done** — checklist to complete during implementation.

Use `[A DEFINIR]` only when the user explicitly declines to answer. The goal is no more than three `[A DEFINIR]` items; if there are more, the design tree is not done.

## Approval Flow

1. Write the SPEC with `Status: Draft`.
2. Read it back to the user as a concise summary.
3. Ask for approval or revision.
4. If the user approves, update `Status: Approved`.
5. Only after `Status = Approved` may implementation begin. Do not write implementation code.

## Verification Checklist

- [ ] The design tree is complete (empty frontier).
- [ ] The SPEC file is written in `.specs/SPEC-{YYYYMMDD}-{feature}.md`.
- [ ] All sections 0-9 are filled.
- [ ] Requirements are numbered and verifiable.
- [ ] Acceptance criteria use BDD "Given...when...then" format.
- [ ] User explicitly approved the SPEC.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Asking questions in English | Always address the user in Portuguese. |
| Implementing before approval | Stop at the SPEC. Implementation is a separate step. |
| Filling gaps with guesses | Use `[A DEFINIR]` or ask the user. |
| Skipping the design tree | Build the tree in rounds to avoid hidden assumptions. |
| Writing a SPEC without user confirmation | The user must explicitly approve. |

## References

- `references/spec-sdd-template.md` — full SDD template
- `create-issues` — for turning the approved SPEC into GitHub Issues
- `orchestrator` — for the full agentic workflow
