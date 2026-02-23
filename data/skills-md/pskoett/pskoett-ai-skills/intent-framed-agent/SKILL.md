---
name: intent-framed-agent
description: "Frames coding-agent work sessions with explicit intent capture and drift monitoring. Use when a session transitions from planning/Q&A to implementation for coding tasks, refactors, feature builds, bug fixes, or other multi-step execution where scope drift is a risk."
---

# Intent Framed Agent

## Install

```bash
npx skills add pskoett/pskoett-ai-skills
```

```bash
npx skills add pskoett/pskoett-ai-skills/intent-framed-agent
```

## Purpose

This skill turns implicit intent into an explicit, trackable artifact at the
moment execution starts. It creates a lightweight intent contract, watches for
scope drift while work is in progress, and closes each intent with a short
resolution record.

## Scope (Important)

Use this skill for coding tasks only. It is designed for implementation work
that changes executable code.

Do not use it for general-agent activities such as:
- broad research
- planning-only conversations
- documentation-only work
- operational/admin tasks with no coding implementation

For trivial edits (for example, simple renames or typo fixes), skip the full
intent frame.

## Trigger

Activate at the planning-to-execution transition for non-trivial coding work.

Common cues:
- User says: "go ahead", "implement this", "let's start building"
- Agent is about to move from discussion into code changes

## Workflow

### Phase 1: Intent Capture

At execution start, emit:

```markdown
## Intent Frame #N

**Outcome:** [One sentence. What does done look like?]
**Approach:** [How we will implement it. Key decisions.]
**Constraints:** [Out-of-scope boundaries.]
**Success criteria:** [How we verify completion.]
**Estimated complexity:** [Small / Medium / Large]
```

Rules:
- Keep each field to 1-2 sentences.
- Ask for confirmation before coding:
  - `Does this capture what we are doing? Anything to adjust before I start?`
- Do not proceed until the user confirms or adjusts.

### Phase 2: Intent Monitor

During execution, monitor for drift at natural boundaries:
- before touching a new area/file
- before starting a new logical work unit
- when current action feels tangential

Drift examples:
- work outside stated scope
- approach changes with no explicit pivot
- new features/refactors outside constraints
- solving a different problem than the stated outcome

When detected, emit:

```markdown
## Intent Check #N

This looks like it may be moving outside the stated intent.

**Stated outcome:** [From active frame]
**Current action:** [What is happening]
**Question:** Is this a deliberate pivot or accidental scope creep?
```

If pivot is intentional, update the active intent frame and continue. If not,
return to the original scope.

### Phase 3: Intent Resolution

When work under the active intent ends, emit:

```markdown
## Intent Resolution #N

**Outcome:** [Fulfilled / Partially fulfilled / Pivoted / Abandoned]
**What was delivered:** [Brief actual output]
**Pivots:** [Any acknowledged changes, or None]
**Open items:** [Remaining in-scope items, or None]
```

Resolution is preferred but optional if the session ends abruptly.

## Multi-Intent Sessions

One session can contain multiple intent frames.

Rules:
1. Resolve current intent before opening the next.
2. If user changes direction mid-task, resolve current intent as
   `Abandoned` or `Pivoted`, then open a new frame.
3. Drift checks always target the currently active frame.
4. Number frames sequentially within the session (`#1`, `#2`, ...).
5. Constraints do not carry forward unless explicitly restated.

## Entire CLI Integration

Entire CLI: https://github.com/entireio/cli

When tool access is available, detect Entire at activation:

```bash
entire status 2>/dev/null
```

- If it succeeds, mention that intent records will be captured in the session
  transcript on the checkpoint branch.
- If unavailable/failing, continue silently. Do not block execution and do not
  nag about installation.

Copilot/chat fallback:
- If command execution is unavailable, skip detection and continue with the
  same intent workflow in chat output.

## Guardrails

- Keep it lightweight; avoid long prose.
- Do not over-trigger on trivial tasks.
- Do not interrupt on every small step.
- Treat acknowledged pivots as valid.
- Preserve exact structured block headers/fields for parseability.

## Interoperability with Other Skills

Use this skill as the front-door alignment layer for non-trivial coding work:
1. `plan-interview` (optional, for requirement shaping)
2. `intent-framed-agent` (execution contract + drift monitoring)
3. Implementation
4. `simplify-and-harden` (post-completion quality/security pass)
5. `self-improvement` (capture recurring patterns and promote durable rules)

This ordering helps reduce scope drift early and improve repeatability across
tasks.
