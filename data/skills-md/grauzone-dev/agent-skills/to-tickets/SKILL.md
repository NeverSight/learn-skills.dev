---
name: to-tickets
description: Turn an approved plan, spec, or conversation into dependency-aware implementation tickets and publish them through the repository's configured tracker. Use when approved work needs to become trackable tickets.
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# To tickets

Turn an approved plan, spec, or conversation into **tracer-bullet** implementation tickets: narrow, complete slices with explicit **blocking edges**.

## Process

### 1. Establish the contracts

Read `docs/agents/issue-tracker.md` before drafting or publishing. When it exists, also read `docs/agents/triage-labels.md` before applying a triage state, and read `docs/agents/domain.md` before using domain vocabulary or locating ADRs.

If `docs/agents/issue-tracker.md` is absent or does not describe how to create tickets, run the `setup-software-engineering-skills` skill before continuing.

Work from the conversation context. When the user supplies a spec path, issue reference, or URL, fetch its full body and comments. Treat an existing issue as a **source** unless the user explicitly asks to make it a parent; preserve the source and every parent unchanged.

**Complete when:** the tracker rules, applicable metadata rules, relevant domain references, and complete source material are available.

### 2. Ground the breakdown

Explore the affected code when the available source does not already establish its current behavior, boundaries, and terminology. Use the domain vocabulary and applicable ADRs named by the domain contract.

Identify preparatory refactoring only when it makes a later vertical slice independently buildable and verifiable.

**Complete when:** every proposed ticket can name a user-visible outcome in the project’s vocabulary, and any necessary preparatory work is explicit.

### 3. Draft tracer bullets

Break the work into tracer-bullet tickets.

- Each ticket delivers one narrow, complete path through every **affected** layer—not a horizontal layer-only task.
- Each ticket is demonstrable or independently verifiable and fits one fresh context window.
- Assign every in-scope outcome to exactly one ticket; acceptance criteria make the outcome checkable.
- Give each ticket its **blocking edges**: only tickets that must complete before this ticket can start. A ticket without blockers can start immediately.
- Keep the dependency graph acyclic.

When a mechanical change has a codebase-wide **blast radius** and cannot remain green as tracer bullets, load [wide-refactors.md](references/wide-refactors.md) and use its expand–migrate–contract sequence.

**Complete when:** the tickets cover the approved scope exactly once, each has checkable acceptance criteria, and every blocking edge is necessary and acyclic.

### 4. Get approval

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title:** a short descriptive name
- **Blocked by:** the ticket titles or numbers that genuinely gate it
- **What it delivers:** the end-to-end behavior it makes work
- **Acceptance criteria:** the observable conditions that prove it works

Ask whether the granularity is right, the blocking edges are correct, and any tickets should merge or split. Iterate until the user approves the exact breakdown to publish.

**Complete when:** the user has approved every ticket, acceptance criterion, and blocking edge.

### 5. Publish and verify

Follow `docs/agents/issue-tracker.md` as the source of truth for creation, metadata, hierarchy, and dependency operations.

1. Create one ticket per approved item in dependency order, so every blocker has an identifier before a blocked ticket refers to it.
2. Use the tracker’s configured native blocking mechanism when documented. Otherwise, add a `## Blocked by` section to each ticket body with the blocking ticket identifiers; write `None — can start immediately` for an unblocked ticket.
3. Apply the configured ready-for-agent state only when `docs/agents/triage-labels.md` exists and the tracker requires that metadata. Use its mapped value and all tracker-required fields; do not substitute a literal label.
4. Do not create a parent/sub-issue relationship or modify a source issue unless the user explicitly requested it. When relevant, include a source reference in the new ticket body.
5. Read back every created ticket. Confirm that its title, body, metadata, source reference, and blocking edges match the approved breakdown.

For local Markdown, create one file per ticket under the configured feature directory and use the exact configured fields and naming convention. For other trackers, use the configured creation and relationship operations rather than inferring platform behavior.

**Complete when:** every approved ticket exists in the configured tracker, every required blocking edge resolves to the correct ticket, required metadata is valid, and the published set matches the approved breakdown.

## Ticket body

Use the configured tracker’s required body and metadata format. Where it does not supply a template, use:

```markdown
## What to build

The end-to-end behavior this ticket makes work from the user’s perspective.

## Acceptance criteria

- [ ] Observable condition 1
- [ ] Observable condition 2

## Blocked by

- Blocking ticket reference, or `None — can start immediately`.

## Source

Reference to the source spec or issue, when applicable.
```

Keep ticket prose decision-rich and durable: describe behavior, contracts, and acceptance conditions rather than current file paths or layer-by-layer implementation. When a prototype produced a decision-rich artifact, include the decision-rich excerpt marked as prototype-derived and link the executable prototype as its primary source.
