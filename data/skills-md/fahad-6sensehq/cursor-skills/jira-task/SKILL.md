---
name: jira-task
description: Breaks Jira stories into subtasks with standardized naming and fixed 1, 2, or 3 story points. Use when the user asks to break down a Jira story, create subtasks, estimate story points, split a ticket, generate a Jira task breakdown, or create implementation tickets from a story.
---

# Jira Story Breakdown

Team/shared, project-agnostic playbook. Same naming and fixed 1–2–3 point scale for every repo.

Read these when needed:

- Point guide: [references/points.md](references/points.md)
- Frontend catalog: [references/catalog-frontend.md](references/catalog-frontend.md)
- Backend catalog: [references/catalog-backend.md](references/catalog-backend.md)
- Integrations catalog: [references/catalog-integrations.md](references/catalog-integrations.md)
- Vendor catalogs: [references/catalog-vendors.md](references/catalog-vendors.md)
- Naming and description templates: [references/templates.md](references/templates.md)
- Worked examples: [references/examples.md](references/examples.md)

## Hard rules

1. Every subtask is **1, 2, or 3 story points**. Never more than 3.
2. If work needs more than 3 points, split it by responsibility.
3. When a subtask matches a named catalog row, use that **fixed** point value. Do not re-judge 1 vs 2 vs 3.
4. One responsibility per subtask. Never mix UI, logic, and API in one ticket.
5. Skip layers the story does not need. Do not invent dummy tickets.
6. Do not create unnecessary subtasks just to increase story points.
7. Do not split work that already matches a single catalog row at ≤3 points.
8. Same type of work gets the same points in every project.
9. Do not estimate from seniority, deadlines, client importance, or developer speed.
10. Include third-party dashboard/configuration work when the story requires it.
11. Present the breakdown table **before** creating Jira issues. Wait for confirmation.
12. Every subtask includes Summary, Type (`Subtask`), Story Points, and Description with acceptance criteria.
13. Use generic names (`payment provider`, `notification service`, `maps SDK`). Name a real vendor only if the story names it.
14. Parent story points = **sum of subtask points**, or leave the parent unestimated. Do not give the parent an independent Fibonacci number.

## When not to split

Keep a single catalog-matched subtask when the change is one responsibility:

- Copy, color, spacing, or label tweaks
- A single environment variable
- A one-line config or dependency bump
- A trivial bug with a known fix

Do not create UI + functionality + API tickets for work that is only one of those.

If actual work is materially larger than the matching catalog row, split into separate responsibilities instead of raising the fixed point value.

## Layer order (skip unused)

**Frontend / mobile UI stories**

1. UI
2. Functionality
3. API connection (`Connect [X] API`)
4. Tests

**Backend stories**

1. Database / DTO / validation (when schema or contracts change)
2. Functionality (service, business logic)
3. API implementation (`Implement [X] API`)
4. Tests

**Third-party / integration stories**

1. Integration setup (only if the service is new)
2. Dashboard / configuration (when required outside the codebase)
3. Backend functionality
4. API implementation
5. Frontend connection
6. Webhook / event handling (only if inbound events exist)
7. Tests

**Bug**

1. Investigate only if the cause is unknown (`Investigate [topic]` — 1)
2. `Fix [issue]` — use catalog maintenance rows when they match (e.g. Fix UI bug = 1, Fix functional bug = 2, Fix backend bug = 2)
3. Tests if the bug is non-trivial

**Spike**

- Timeboxed `Investigate [topic]` — 1
- Never mix research with implementation

## Workflow

1. Read the story. If requirements are missing, list them and stop guessing large implementation work.
2. Identify only the layers that apply.
3. Name each subtask using [references/templates.md](references/templates.md).
4. Assign fixed points from the catalogs via [references/points.md](references/points.md).
5. Show this table and wait:

```markdown
**Story:** [story summary]
**Parent points:** [sum] (sum of subtasks)

| # | Summary | Type | Points |
| --- | --- | --- | ---: |
| 1 | [summary] | Subtask | 1 |

Shall I create these subtasks in Jira?
```

6. After confirmation, create subtasks. Do not auto-create.

## Subtask description

```markdown
## Scope
- What to build
- Where (module/screen/endpoint)

## Out of scope
- What this subtask must not include

## Acceptance criteria
- [ ] Testable criterion 1
- [ ] Testable criterion 2

## Notes
- Design / API / dependency if applicable
```

## Naming cheat sheet

Look up the exact fixed points in the catalogs. Defaults below are the common catalog values.

| Kind | Pattern | Typical pts |
| --- | --- | ---: |
| UI | `Add [Component/Screen] UI` | 1–3 (see FE catalog) |
| Client/server logic | `Add [feature] functionality` | 1–3 |
| Frontend API | `Connect [resource] API` | 1–3 |
| Backend API | `Implement [resource] API` | 2–3 |
| New external service | `Add [service] integration` | 1–2 |
| Configure external | `Configure [service] dashboard/settings` | 1–2 |
| External workflow | `Add [service] [workflow] functionality` | 2–3 |
| Webhook | `Implement [service] [event] webhook` | 2–3 |
| Event handling | `Add [service] [event] handling functionality` | 2 |
| Frontend third-party | `Connect [service] [feature]` | 2–3 |
| Mobile native | `Add [feature] native functionality` | 1–2 (non-catalog) |
| Bug | `Fix [issue]` | 1–2 |
| Spike | `Investigate [topic]` | 1 |
| Tests | `Add [feature] tests` | 2–3 |
| Migration | `Add [entity] migration` / `Add database migration` | 2 |
| Backfill | `Add [entity] backfill` | 1–2 (non-catalog) |
| Worker | `Add [job] worker functionality` / background job | 3 |
| CI | `Update [pipeline] CI` | 1–2 (non-catalog) |
| Config | `Add [env] configuration` / `Configure …` | 1–2 |
| Docs | `Add [feature] documentation` | 1–2 |
| Analytics | `Add analytics tracking` / `Connect [event] analytics` | 1 |
| Accessibility | `Add [screen] accessibility` | 1 (non-catalog) |
| i18n | `Add [feature] translations` | 1 (non-catalog) |

Never use `Connect [X] API` for backend implementation. Use `Implement [X] API`.
