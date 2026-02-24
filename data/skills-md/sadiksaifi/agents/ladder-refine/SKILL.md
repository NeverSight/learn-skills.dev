---
name: ladder-refine
description: >-
  Rewrites a phase spec into canonical Ladder format without altering intent.
  Use when a spec is malformed, incomplete, or fails validation.
compatibility: Requires git, Claude Code with plan mode and Task tool support
---

# Ladder Refine

Rewrite a spec file in-place to match the canonical Ladder format without altering intent or scope.

## When to Use

- User says "refine spec," "fix spec," "reformat phase," "ladder refine," or "/ladder-refine"
- `/ladder-execute` reports spec validation failures
- Spec exists but is not in canonical format
- Invoke with a file path argument

## When NOT to Use

- `.ladder/OVERVIEW.md` doesn't exist → "Run `/ladder-init` first"
- No spec exists yet → use `/ladder-create`
- Spec is already canonical and ready → use `/ladder-execute`
- User wants to add new features to a spec → use `/ladder-create` for a new phase

## Quick Reference

| Field | Value |
|-------|-------|
| **Input** | Spec file path (`.ladder/specs/L-<N>-<slug>.md`) |
| **Output** | Rewritten spec file (same path, canonical format) |
| **Commits** | `chore(ladder): refine L-<N> spec to canonical format` |
| **Prerequisites** | `.ladder/OVERVIEW.md`, existing spec file |

## Iron Laws

1. **Specs are immutable** after creation — refinement is the ONE exception, and it only restructures, never changes intent.
2. **No content added or removed** — restructure only. Refinement preserves meaning.
3. **`progress.md` is the single source of truth** for execution state.
4. **User approval before persistent actions** — present the rewritten spec before overwriting.

## Hard Gates

<HARD-GATE>
SOURCE SPEC EXISTS: The provided spec file must exist on disk. If not → print "Spec file not found at <path>" and STOP.
</HARD-GATE>

<HARD-GATE>
GAP ANALYSIS FIRST: Present the gap analysis to the user BEFORE rewriting. The user must see what's missing/wrong before you change anything.
</HARD-GATE>

<HARD-GATE>
VALIDATION PASS: The refined spec MUST pass ALL 5 validation rules from `references/spec-format.md` before writing to disk. If it doesn't pass, fix it until it does.
</HARD-GATE>

<HARD-GATE>
NO SCOPE CHANGES: Do NOT add features, requirements, or steps that weren't in the original spec. Do NOT remove content. Restructure only.
</HARD-GATE>

## Workflow

### Phase A: Analysis

#### 1. Load Context

1. Read `.ladder/OVERVIEW.md` for product context.
2. Read `references/spec-format.md` for the canonical format and validation rules.
3. Read the provided spec file.

#### 2. Analyze Gaps

Check the spec against the canonical format:
- Which of the 11 required sections are present/missing?
- Does the Step Sequence use enriched `S<N>` format?
- Do steps have Acceptance criteria?
- Do Entry/Exit Criteria follow the rules?

Present findings to the user as a gap summary.

### Phase B: Clarification

#### 3. Clarify Ambiguities

Ask the user to resolve ALL ambiguities in a single message. Typical questions:
- Missing UX or accessibility requirements
- Unclear scope boundaries
- Steps that need splitting or merging
- Missing acceptance criteria for steps

If there are no ambiguities, skip this step.

### Phase C: Rewrite

#### 4. Rewrite Spec

Rewrite the file in-place to the canonical format:
- **Do NOT** alter intent or scope
- **Do NOT** add features or new requirements
- **Do NOT** remove content — restructure only
- **Do NOT** create separate files
- Assign `S<N>` IDs to all steps sequentially
- Add Complexity, Deliverable, Files, Depends on, Details, and Acceptance to every step
- Ensure all 11 required sections are present

Present the rewritten spec to the user for approval before writing.

### Phase D: Finalize

#### 5. Write & Commit

Write the approved spec to disk (overwrite in place).

```
chore(ladder): refine L-<N> spec to canonical format
```

#### 6. Confirm

Print:
> "Spec refined to canonical format. Ready for `/ladder-execute`."

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Adding features during refinement | Scope creep — refinement only restructures | If new features needed, use `/ladder-create` for a new phase |
| Rewriting from scratch | Loses original author's intent | Transform existing content into canonical sections |
| Skipping gap analysis | User doesn't know what changed | Present gaps BEFORE rewriting (Hard Gate) |
| Not validating after rewrite | Spec might still fail validation | Run all 5 validation rules before writing |
| Expanding scope of steps | Steps grow beyond original intent | Match original scope — restructure, don't expand |

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "This spec is so bad I should start over" | Transform existing content — never rewrite from scratch |
| "I'll add a few extra requirements while I'm here" | NO scope changes is a HARD GATE |
| "The user probably meant X" | If ambiguous, ask during clarification phase |
| "I'll just write the new spec without showing the gap analysis" | Gap analysis presentation is a HARD GATE |
| "This step is too big but I'll leave it" | Split it — refinement includes structural improvements |

## Integration

| Direction | Skill | Signal |
|-----------|-------|--------|
| **Requires** | `/ladder-init` | `.ladder/OVERVIEW.md` exists |
| **Requires** | Existing spec | File at provided path |
| **Triggered by** | `/ladder-execute` | Spec validation failure |
| **Enables** | `/ladder-execute` | Canonical spec ready for implementation |
