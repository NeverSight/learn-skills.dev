---
name: to-spec
description: Turn the current conversation into a spec published to the project tracker — no interview, just synthesis of what was already discussed.
metadata.derived-from: https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f7533f8eea9a859c87/skills/engineering/to-spec/SKILL.md
metadata.derivation-note: Adds reproducibility invariant + self-containedness litmus test (see derived to-tickets) + grilling gate. Tracker deferred to consumer AGENTS.md; vocabulary pinned to docs/glossary (`uvx disambiguate`), decisions to writing-adrs. Upstream `/setup-matt-pocock-skills` dropped. Caveman-condensed.
disable-model-invocation: true
---

# To Spec

Produce spec (aka PRD) from current conversation + codebase understanding. Do NOT interview user — synthesize what you already know.

## Reproducibility invariant

Spec — and tickets later derived from it — must be **self-contained**: replayed by any implementer, human or agent, builds roughly same application. Every outcome-shaping decision lives in spec itself, or durable docs it references — ADRs (`writing-adrs`), glossary terms (`docs/glossary/`). Never conversation context, tribal knowledge, implementer discretion.

**Litmus test:** two independent implementers could build meaningfully different things → spec underspecified. Add decision to spec, or record as ADR/glossary term + reference.

## Grilling gate

Spec is load-bearing. No grilling session (`docs/glossary/grilling-session.md`) in context → stop, ask user: "No grilling session found — really skip?" Proceed only on explicit confirmation; note skip in Further Notes.

## Process

1. Explore repo if not already done. Use glossary vocabulary (`uvx disambiguate <term>`) throughout; respect ADRs in touched area.

2. Sketch seams for testing the feature. Prefer existing seams; new seams at highest point possible. Fewer seams better — ideal is one.

   Check seams with user.

3. Write spec per template — as short as possible, caveman mode preferred (`caveman` skill), precision and understandability must not suffer. Apply litmus test to every section, publish per consumer repo's tracker conventions (AGENTS.md). Apply `ready-for-agent` label — no further triage.

Spec template:

```markdown
## Problem Statement

Problem, from user's perspective.

## Solution

Solution, from user's perspective.

## User Stories

LONG numbered list: "As an <actor>, I want <feature>, so that <benefit>".
Example: "As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending."
Extremely extensive — cover all aspects.

## Implementation Decisions

Decisions made: modules built/modified, interfaces, technical clarifications, architecture, schema changes, API contracts, specific interactions.

Hard-to-reverse or surprising decisions → also record as ADR (`writing-adrs`) + reference. Decision only in conversation, not listed here → fails litmus test — write it down.

No file paths/code snippets — stale fast. Exception: prototype snippet encoding a decision more precisely than prose (state machine, reducer, schema, type shape) → inline within relevant decision, note prototype origin, trim to decision-rich parts.

## Testing Decisions

What makes a good test (external behavior only, not implementation details), which modules tested, prior art in codebase.

## Out of Scope

What this spec excludes.

## Further Notes

Anything else.
```
