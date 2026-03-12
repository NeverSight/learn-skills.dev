---
name: feature-radar
description: |
  Full-cycle feature discovery, evaluation, and prioritization. Builds a persistent knowledge
  base at .feature-radar/ and runs a 6-phase workflow to recommend what to build next.
  Modes: full (all phases), quick (scan only), evaluate (prioritize), #N (deep-dive one).
  MUST use this skill whenever the user asks about feature priorities, roadmaps, what to build,
  or wants to evaluate/compare feature ideas — even if they don't say "feature radar" explicitly.
  Use when the user:
  - Asks "what should we build next?", "what's most impactful?", or similar
  - Wants to prioritize, rank, or compare features or backlog items
  - Needs roadmap planning, project direction, or strategic feature decisions
  - Says "help me prioritize", "review our backlog", "what are we missing"
  - Mentions .feature-radar/ directory or feature tracking
  - Wants periodic reassessment of deferred or open opportunities
---

# Feature Discovery & Prioritization

## Mode Routing

<HARD-GATE>
Parse the user argument BEFORE any other logic. Determine the mode:

| Argument | Mode | Phases |
|----------|------|--------|
| (none) or `full` | full | 1-6 (all) |
| `quick` | quick | 1-3 only |
| `evaluate` | evaluate | reconciliation → 5-6 (skip 1-3) |
| `#N` (e.g. `#2`) | focus | Read opportunity N → Phase 5 (single item) → Phase 6 |

Route rules:
- **full**: Follow normal workflow (Phase 1-6).
- **quick**: Execute Phase 1-3, then skip to Completion Summary.
- **evaluate**: Run "Subsequent Runs" reconciliation (steps 1-2), then jump directly to Phase 5-6.
- **focus (#N)**: Read `.feature-radar/opportunities/{N}-*.md`. If not found, list available opportunities and ask user to pick. Then run Phase 5 for that single opportunity, followed by Phase 6.

State the detected mode before proceeding: "Mode: {mode}"
</HARD-GATE>

## Bootstrap (First Run)

If `.feature-radar/` does not exist at the project root, create it:

```
.feature-radar/
├── base.md
├── archive/
├── opportunities/
├── specs/
└── references/
```

Then generate `base.md` by completing the following:

<HARD-GATE>
Complete ALL steps before presenting base.md to the user:

1. **Detect stack** — read `go.mod`, `package.json`, `Cargo.toml`, `pyproject.toml`. Follow imports to understand the dependency graph. Don't just read the config — understand the architecture.
2. **Map structure** — list top-level directories. For each, read at least one file to understand its purpose. Identify: entry points, core logic, tests, docs, configuration.
3. **Extract features** — scan exports, commands, API routes, or public functions. Read the implementations, not just the names. Understand what each feature actually does.
4. **Find inspiration sources** — read README, CONTRIBUTING, docs/ for related projects and communities
5. **Verify with user** — present the generated base.md and ask: "Does this accurately describe your project?"
</HARD-GATE>

After presenting base.md, support iterative refinement per `references/WORKFLOW-PATTERNS.md`.

<HARD-GATE>
Do NOT proceed to the Workflow until the user approves base.md.
</HARD-GATE>

### base.md Template

Generate `base.md` following the structure defined in `references/SPEC.md` (sections 2-5).
Read `references/SPEC.md` first, then fill `{placeholders}` with project-specific analysis.

Key sections to generate:
- **Project Context** — detected language, architecture, key feature areas, core philosophy, inspiration sources
- **Feature Inventory** — implemented features table + value & innovation landscape table
- **Tracking Summary** — counts per category (start at 0)
- **Directory Layout** — tree view
- **Classification Rules** — per references/SPEC.md §3.2-3.5
- **Maintenance Workflow** — feature flow between directories
- **Archive Extraction Checklist** — per references/SPEC.md §4.3

After creating the directory, ask the user:
**"Should I add `.feature-radar/` to `.gitignore`?"**
(Recommended if the tracking data is internal and shouldn't be committed.)

## Subsequent Runs

On subsequent runs (`.feature-radar/` already exists):
1. Read existing `base.md` — do NOT overwrite
2. Run reconciliation per `references/DEEP-READ.md` steps 2-6
3. Proceed to Mode Routing

## Behavioral Directives

<HARD-GATE>
Read and follow `references/DIRECTIVES.md`.

Additional directives for this skill:
- **Do not skip phases outside mode rules** — follow the Mode Routing and Phase execution HARD-GATEs. For conditional phases, state the skip condition check result before deciding to skip.
- **Reconcile on subsequent runs** — see "Subsequent Runs" section above.
</HARD-GATE>

## Workflow

Execute phases in order.

<HARD-GATE>
Phase execution rules (mode-dependent):

**full mode** (default):
- Phase 1-3: ALWAYS execute.
- Phase 4: Skip ONLY if no documentation directory exists.
- Phase 5-6: Skip ONLY if no open opportunities exist.

**quick mode**:
- Phase 1-3: Execute. Stop after Phase 3 → Completion Summary.

**evaluate mode**:
- Phase 1-4: Skip (reconciliation already done in Subsequent Runs).
- Phase 5-6: Execute. Skip ONLY if no open opportunities exist.

**focus mode (#N)**:
- Phase 1-4: Skip.
- Phase 5: Evaluate the single targeted opportunity only.
- Phase 6: Propose for that opportunity only.

For each phase completed, state what was produced before moving to the next phase.
</HARD-GATE>

### Phase 1: Scan & Classify

1. Read source files (feature ideas, user feedback, ecosystem observations, creative proposals, issue trackers)
2. Cross-reference each entry against the codebase
3. Classify:
   - **Done / Covered / Rejected / N/A** → archive
   - **Open / Partially Done** → opportunity
   - **Cross-cutting pattern** → specs
   - **External observation** → references

**Checkpoint**: Present classification results using this format, then ask "Continue to Phase 2?"

```
Phase 1 complete:
| Classification | Count | Items |
|---------------|-------|-------|
| Archive       | {n}   | {list} |
| Opportunity   | {n}   | {list} |
| Spec          | {n}   | {list} |
| Reference     | {n}   | {list} |
```

### Phase 2: Archive Completed Features

For each archive candidate:

1. Create `archive/{nn}-{slug}.md`
2. Run the **Archive Extraction Checklist** (mandatory):
   - Extract learnings → `specs/`
   - Derive new opportunities → `opportunities/`
   - Update references → `references/`
   - Update ecosystem trends → `specs/ecosystem-trends.md`
3. Mark the entry as processed in the source (strikethrough + status)

### Phase 3: Organize Open Opportunities

1. Create `opportunities/{nn}-{slug}.md`
2. Assess **Impact** and **Effort** realistically
3. Write an honest "Our Position" — do we actually want this?

**Checkpoint**: Present opportunities using this format, then ask "Continue to Phase 4?"

```
Phase 3 complete: {n} opportunities organized
| # | Opportunity | Impact | Effort | Our Position |
|---|------------|--------|--------|-------------|
| {nn} | {title} | High/Med/Low | High/Med/Low | {1-line stance} |
```

### Phase 4: Gap Analysis

Find implemented features that docs don't mention:

1. Scan documentation for coverage of implemented features
2. For each gap: which feature, which page should cover it, standalone guide or section

### Phase 5: Evaluate & Prioritize

| Criterion | Question |
|-----------|----------|
| **Real user demand** | Are users actually asking for this? |
| **Value uplift** | Does this meaningfully improve the user experience or unlock new possibilities? |
| **Innovation potential** | Does this introduce a creative breakthrough or unique approach? |
| **Effort / impact ratio** | Is the cost justified by the benefit? |
| **Architectural fit** | Does it align with our core philosophy? |
| **Ecosystem timing** | Is the ecosystem ready? |

Rank into tiers:
- **Build next**: High value + strong demand or innovation potential + reasonable effort
- **Build soon**: Good value + moderate demand
- **Monitor**: Low demand or premature
- **Skip**: Conflicts with philosophy or negligible value

**Checkpoint**: Present tier ranking using this format, then ask "Continue to Phase 6 (Propose)?"

```
Phase 5 complete:
| Tier | # | Opportunity | Demand | Value | Innovation | Effort/Impact | Fit | Timing |
|------|---|------------|--------|-------|------------|--------------|-----|--------|
| Build next | {nn} | {title} | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} |
| Build soon | ... | | | | | | |
| Monitor    | ... | | | | | | |
| Skip       | ... | | | | | | |
```

### Phase 6: Propose & Decide

For each "Build next" feature (top 1-3), present a proposal card:

```
### {nn}. {Title}
**Pitch**: {One paragraph — what value does this create?}
**Effort**: {N days} — {brief justification}
**Key decisions**:
- {decision 1}
- {decision 2}
```

After all cards, ask: **"Should we enter plan mode for [feature]?"**

## Completion Summary

Follow the template in `references/DIRECTIVES.md`, with skill name "Complete" and an additional line:
`Top recommendation: {feature name} — {one-line pitch}`

## Guardrails

- **Don't copy blindly.** Evaluate fit with YOUR architecture and users, not someone else's.
- **Don't overcount.** 1 issue with no comments = weak signal.
- **Don't undercount.** Multiple independent asks = strong signal.
- **Chase value, not features.** Ask "what problem does this solve?" before "what does this do?"
- **Be honest about effort.** Low < 1 day. Medium 1-3 days. High 1+ week.
- **Challenge deferred items.** "Deferred" ≠ "forever" — re-evaluate each session.
- **Think creatively.** The best features aren't always the obvious ones — look for novel angles.
