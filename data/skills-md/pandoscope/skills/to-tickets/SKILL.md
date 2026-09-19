---
name: to-tickets
description: Break a plan, spec, or the current conversation into tracer-bullet tickets with blocking edges, published to the project tracker. Use when splitting approved work into issues.
metadata.derived-from: https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f7533f8eea9a859c87/skills/engineering/to-tickets/SKILL.md
metadata.derivation-note: Adds reproducible-build-spec invariant (self-containedness litmus test, bugfix-as-spec-correction) + grilling gate + reconciliation on completion. Tracker deferred to consumer AGENTS.md; vocabulary pinned to docs/glossary (`uvx disambiguate`), decisions to writing-adrs/documenting-decisions; new vocabulary declared under an Introduces list (link-as-if-exists). Upstream `/setup-matt-pocock-skills` + local-files tracker mode dropped. Caveman-condensed; vertical slices, blocking edges, expand–contract, user quiz kept.
disable-model-invocation: true
---

# To Tickets

Break plan/spec/conversation into **tickets** — tracer-bullet vertical slices, each declaring tickets that **block** it. Publish per consumer repo's tracker conventions (AGENTS.md).

## Reproducibility invariant

> Full issue set, replayed in dependency order — features and bugfixes alike — must build roughly same application, regardless of who or what implements.

Issue stream = buildable spec. Every rule below serves this.

### Self-containedness

Every outcome-shaping decision lives **in issue itself**, or durable docs it references — ADRs (`writing-adrs`), glossary terms (`docs/glossary/`). Never conversation context, tribal knowledge, implementer discretion.

**Litmus test:** two independent implementers could build meaningfully different things → ticket underspecified. Add decision to ticket, or record as ADR/glossary term + reference.

### New vocabulary

Ticket introducing a domain concept declares it under `## Introduces` — one slug per line, each linked **as if the term file already existed** (`docs/glossary/<slug>.md`, link-as-if-exists convention). Implementation creates the file; until then `--lint` reports broken cross-reference — that IS the enforcement, not a bug. The list = durable record of vocabulary the ticket adds.

### Bugfixes = spec corrections

Never patch instruction ("change Y to X in file Z"). State correction to spec stream:

- *Issue N implied X; implementation did Y; X correct.* — or
- *Issue N specified Y; Y wrong; X′ now correct.*

Replay then builds X directly, not bug + patch. Bugfix reveals spec-level decision → ADR + reference from issue.

### Reconciliation on completion

Ticket not finished until it reflects what was built. Before close: fold deviations, mid-session scope, decisions back into issue (or its ADR/glossary refs). Else replay builds first draft, not final state. `documenting-decisions` after-task step performs this.

## Grilling gate

Tickets are load-bearing. No grilling session (`docs/glossary/grilling-session.md`) in context → stop, ask user: "No grilling session found — really skip?" Proceed only on explicit confirmation; note skip in parent issue/PR.

## Process

### 1. Gather context

Work from conversation context. User passes reference (spec path, issue number/URL) → fetch, read full body + comments.

### 2. Explore codebase (optional)

Understand current code state. Titles/descriptions use glossary vocabulary (`uvx disambiguate <term>`); respect ADRs in touched area.

Look for prefactoring opportunities. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break work into **tracer bullet** tickets:

- Each slice: narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT horizontal slice of one layer
- Completed slice demoable/verifiable alone
- Sized to one fresh context window
- Prefactoring first

Each ticket declares **blocking edges** — tickets that must complete first. No blockers → start immediately.

Apply litmus test to every draft: drafting decisions (interfaces, naming, sequencing trade-offs) go into ticket body, ADR, or glossary term — mark per `documenting-decisions`.

**Wide refactors: exception to vertical slicing.** One mechanical change (rename column, retype shared symbol), **blast radius** spans codebase — single edit breaks thousands of call sites, no slice lands green. Sequence as **expand–contract**. Expand: new form beside old, nothing breaks. Migrate: call sites in batches sized by blast radius (per package/directory), each batch own ticket blocked by expand — CI stays green, old form still exists. Contract: delete old form once no caller remains, blocked by every batch. Batches can't stay green alone → keep sequence, share integration branch, all block final integrate-and-verify ticket — green promised only there.

### 4. Quiz user

Numbered list. Per ticket:

- **Title**: short name
- **Blocked by**: gating tickets, if any
- **What it delivers**: end-to-end behaviour made to work

Ask:

- Granularity right? (too coarse/fine)
- Blocking edges correct — only genuine gates?
- Merge or split any?
- Any ticket failing litmus test — decision still only in conversation?

Iterate until approved.

### 5. Publish

One issue per ticket, dependency order (blockers first) → edges reference real issue numbers. Native blocking relation where tracker has one, else "Blocked by" section. Apply `ready-for-agent` label unless told otherwise — tickets agent-grabbable by construction.

Work the **frontier**: any ticket with all blockers done. Linear chain → top to bottom.

Do NOT close/modify parent issue.

Issue template:

```markdown
## Parent

Reference to parent issue (omit if source wasn't an issue).

## What to build

End-to-end behaviour, user's perspective — not layer-by-layer implementation.

## Decisions

Every outcome-shaping decision, stated or referenced (ADR/glossary). Bugfix: spec-correction statement. Omit only if genuinely none.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Introduces

- [slug](docs/glossary/slug.md) — one-line meaning. Omit if no new term.

## Blocked by

- Reference per blocking ticket, or "None — can start immediately".
```

Ticket prose: as short as possible, caveman mode preferred (`caveman` skill) — precision and understandability must not suffer.

No file paths/code snippets — stale fast. Exception: prototype snippet encoding a decision more precisely than prose (state machine, reducer, schema, type shape) → inline, note prototype origin, trim to decision-rich parts.

Work frontier one ticket at a time, clearing context between tickets.
