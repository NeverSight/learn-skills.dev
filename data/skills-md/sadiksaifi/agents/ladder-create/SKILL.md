---
name: ladder-create
description: >-
  Creates new phase specs in canonical Ladder format with step sequences and
  acceptance criteria. Use when adding an implementation phase or when the user
  describes a feature to spec out.
compatibility: Requires git, Claude Code with plan mode and Task tool support
---

# Ladder Create

Generate a new phase spec in canonical Ladder format.

## When to Use

- User says "create phase," "new phase," "add phase," "ladder create," or "/ladder-create"
- User provides a feature description to turn into a phase spec
- Direct mode: `/ladder-create "Add SFTP support"`
- Q&A mode: `/ladder-create` (no argument — will ask questions)

## When NOT to Use

- `.ladder/OVERVIEW.md` doesn't exist → "Run `/ladder-init` first"
- Spec already exists and needs restructuring → use `/ladder-refine`
- Spec exists and is ready to implement → use `/ladder-execute`

## Quick Reference

| Field | Value |
|-------|-------|
| **Input** | Feature description (direct) or Q&A answers |
| **Output** | `.ladder/specs/L-<N>-<slug>.md` |
| **Commits** | `chore(ladder): add L-<N> spec — <slug>` |
| **Prerequisites** | `.ladder/OVERVIEW.md` must exist |

## Iron Laws

1. **Specs are immutable** after creation — only `progress.md` is a living document.
2. **Evidence before completion** — never claim a step is done without proof.
3. **`progress.md` is the single source of truth** for execution state.
4. **User approval before persistent actions** — always confirm before writing files or committing.

## Hard Gates

<HARD-GATE>
OVERVIEW REQUIRED: `.ladder/OVERVIEW.md` must exist before proceeding. If not → print "Run `/ladder-init` first" and STOP.
</HARD-GATE>

<HARD-GATE>
COMPLETE SPEC: The generated spec must contain ALL 11 required sections per `references/spec-format.md` before presenting to user. Do not present a partial spec.
</HARD-GATE>

<HARD-GATE>
ACCEPTANCE CRITERIA: Every step in the Step Sequence MUST have at least one acceptance criterion. No exceptions.
</HARD-GATE>

<HARD-GATE>
USER REVIEW: Present the full spec to the user and receive explicit approval BEFORE writing to disk. Never write first and show after.
</HARD-GATE>

## Workflow

### Phase A: Context Loading

#### 1. Load Context

1. Read `.ladder/OVERVIEW.md` for product context and Phase Registry.
2. Read `references/spec-format.md` for the canonical format.

#### 2. Gather Input

**Direct mode** (argument provided): Parse the description for objective and scope.

**Q&A mode** (no argument): Ask the user:
1. Objective — what does this phase deliver?
2. Prerequisites — what must exist before this phase?
3. Scope — what's included?
4. Exclusions — what's explicitly out?
5. References — any `.ladder/refs/` docs relevant?

### Phase B: Generation

#### 3. Determine Phase Number

- **Standard:** Next integer after the highest phase in the Phase Registry.
- **Fractional insertion** (e.g., L-01.1): When the user requests a phase between existing phases.
  - Update surrounding phases' Entry/Exit Criteria in-place to reference the new phase.
  - Commit surrounding changes: `chore(ladder): update entry/exit criteria for L-<N.1> insertion`
  - Update OVERVIEW.md Phase Registry.

#### 4. Generate Spec

Generate all 11 required sections (+ section 12 if references exist) per `references/spec-format.md`:
- Aim for 6–12 steps per phase
- Assign `S<N>` IDs to each step
- Set Complexity for each step
- Write Acceptance criteria for every step
- Reference predecessor phase in Entry Criteria
- Include "UAT checklist items pass" in Exit Criteria

### Phase C: Review

#### 5. User Review

Present the full spec to the user for review before writing to disk. Incorporate any requested changes. Repeat until approved.

### Phase D: Persist

#### 6. Write Spec

Write to `.ladder/specs/L-<N>-<slug>.md` where `<slug>` is a kebab-case summary.

#### 7. Update OVERVIEW.md

Add the new phase to the Phase Registry table.

#### 8. Commit

```
chore(ladder): add L-<N> spec — <slug>
```

#### 9. Summary

Print the file path and suggest:
> "Run `/ladder-execute <path>` to begin implementation."

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Writing spec before user review | User can't influence final output | Present full spec, wait for approval (Hard Gate) |
| Fewer than 6 steps | Phase is too coarse-grained for progress tracking | Split large steps until each is implementable in one commit |
| Steps without acceptance criteria | `/ladder-execute` will reject the spec | Every step needs ≥1 testable criterion |
| Adding scope the user didn't request | Scope creep undermines trust | Only spec what was asked for |
| Skipping Q&A in interactive mode | Spec lacks user context | Always ask all 5 questions |
| Vague acceptance criteria | "Works correctly" is untestable | Use observable outcomes: "returns 200," "renders in <2s" |

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "I'll write the spec and the user can edit it later" | User review is a HARD GATE — present before writing |
| "This step is simple, it doesn't need acceptance criteria" | Every step needs criteria — no exceptions |
| "I'll add some extra features while I'm at it" | Only spec what was requested — no scope creep |
| "5 steps is enough" | Aim for 6–12. Fewer means steps are too coarse |
| "I can figure out the scope without asking" | Q&A exists for a reason — gather user context |

## Integration

| Direction | Skill | Signal |
|-----------|-------|--------|
| **Requires** | `/ladder-init` | `.ladder/OVERVIEW.md` exists |
| **Enables** | `/ladder-execute` | Canonical spec in `.ladder/specs/` |
| **Related** | `/ladder-refine` | If created spec needs restructuring |
