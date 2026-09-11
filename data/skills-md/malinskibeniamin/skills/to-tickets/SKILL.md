---
name: to-tickets
description: Split a plan into tracer-bullet tickets with explicit blocking edges.
disable-model-invocation: true
---

# To Tickets

Turn an approved plan, spec, or conversation into independently verifiable vertical slices.
If `CLAUDE.md` exists, read `CLAUDE.md` first; otherwise read `AGENTS.md`. Follow its Issue
tracker pointer. If absent, use `/work-automation-kit` or its local fallback.

## 1. Gather

Use existing conversation context. Fetch a supplied spec, issue, or URL with its complete
body and comments. Explore only when current code and domain vocabulary are still unclear;
respect the project glossary and ADRs. Prefer making the change easy before the easy change.

## 2. Draft slices

Each ticket:

- Cuts a narrow end-to-end path through needed layers, rather than one horizontal layer.
- Is demoable or verifiable alone and fits one fresh context window.
- Declares only genuine blockers; no blockers means ready now.
- Describes user-visible behavior and acceptance, not volatile file paths or snippets.

**Wide refactors are the exception.** Use expand, migrate, contract: add the new form beside
the old; move callers in independently green batches; then delete the old form. Each migrate batch is blocked by expand.
The contract is blocked by every migrate batch. If batches cannot
stay green alone, use an integration branch and final integrate-and-verify ticket.

Use `/plan-arbiter` when multiple graphs survive. Use `/visual-plan` for a large graph whose
frontier or blockers need inspection.

## 3. Confirm

Present a numbered list with **Title**, **Blocked by**, and **What it delivers**. Ask whether
granularity and edges are right and whether to merge or split tickets. Iterate until approved.

## 4. Publish

Publish one item per ticket, blockers first. Never modify or close the parent.

- **Local:** write `.scratch/<feature-slug>/tickets/<NN>-<slug>.md`, numbered from `01`.
  Each file lists blocker numbers and titles.
- **Tracker:** create one issue per ticket. Attach it with the native sub-issue relationship
  and native blockers when available; otherwise write explicit blocker links. Apply the
  configured `ready-for-agent` role.

The frontier is every ticket whose blockers are complete.

```markdown
# <NN> -- <Ticket title>
**What to build:** <end-to-end behavior from the user's perspective>
**Blocked by:** <ticket numbers and titles, or None -- can start immediately>
**Status:** ready-for-agent
## Acceptance criteria
- [ ] <observable criterion>
```

For tracker issues, add `## Parent` when a parent exists, followed by `## What to build`,
`## Acceptance criteria`, and `## Blocked by`.

Do not inline implementation detail. For `/prototype` code, add a context pointer to its durable location.
