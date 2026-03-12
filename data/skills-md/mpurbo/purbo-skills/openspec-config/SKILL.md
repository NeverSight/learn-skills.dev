---
name: openspec-config
description: >
  Use when setting up or updating OpenSpec's config.yaml for a project, or when
  OpenSpec workflow isn't picking up development disciplines (TDD, progressive
  phases, FP conventions). Triggers: "configure openspec", "setup openspec",
  "openspec config", "why didn't openspec use TDD", "openspec not invoking
  skills", "grounding config". Generates config.yaml with project context and
  skill invocation rules across sessions. Do NOT use for non-OpenSpec projects
  or for general CLAUDE.md configuration.
---

# OpenSpec Config

Configures OpenSpec's `config.yaml` so that every artifact inherits project
context and invokes the right skills at each workflow step. Run once per project
for initial setup, then update the **phase context** each time you start a new
phase.

**Two problems it solves:**
1. **Lost discipline:** Skills are session-scoped. TDD invoked in one session is
   forgotten in the next. `config.yaml` is the cross-session memory.
2. **Wasted tokens:** Loading the full subsystem design spec (~1000 lines) into
   every OpenSpec session when only one phase's section (~30 lines) + consumed
   contracts are needed.

## When to Use

- **New project setup:** After `openspec init` or when `config.yaml` is empty/default
- **Starting a new phase:** Update the phase context block before each OpenSpec
  change (see Step 5: Phase Context Switch)
- **Missing discipline:** Agent didn't invoke TDD during apply, skipped
  progressive phases, ignored project conventions
- **New skills added:** Installed new superpowers or tech-specific skills that
  should be woven into the OpenSpec workflow
- **New subsystem spec ready:** Subsystem Design Spec created via
  `subsystem-design-spec` skill, now need OpenSpec configured for its phases

## Process

### Step 1: Discover Project Context

Scan for project documentation:

```
Search order:
1. docs/**/*.md, docs/**/*.txt         — specs, design specs, architecture docs
2. CLAUDE.md, .claude/CLAUDE.md        — developer context
3. openspec/config.yaml                — current config (may be empty)
4. Cargo.toml, package.json, go.mod    — tech stack signals
5. openspec/specs/**/*.md              — existing capability specs
```

Extract:
- **Project identity:** Name, purpose, domain (1-2 sentences)
- **Tech stack:** Language, framework, key libraries, build system
- **Architecture principles:** From system spec or CLAUDE.md
- **Conventions:** Load from `docs/conventions.md` if it exists (produced by
  `subsystem-design-spec` after the first subsystem). This replaces scanning
  individual specs for naming patterns and structural conventions.
- **Subsystem specs:** Paths to any Subsystem Design Specs — referenced by path
  only, NOT loaded in full (see Phase Context Switch)

### Step 2: Discover Available Skills

Scan the installed skills to build a mapping:

**Superpowers skills** (check system prompt):
- `superpowers:test-driven-development` — TDD discipline
- `superpowers:systematic-debugging` — debugging methodology
- `superpowers:brainstorming` — creative exploration
- `superpowers:writing-plans` — plan creation from specs
- `superpowers:executing-plans` — plan execution with review checkpoints
- `superpowers:verification-before-completion` — evidence-based verification
- `superpowers:requesting-code-review` — review after implementation
- `superpowers:finishing-a-development-branch` — branch completion workflow

**Tech-specific skills** (check installed plugins):
- `fp-rust` — FP-first Rust conventions
- `fp-kstream-design` / `fp-kstream-implement` — Kafka Streams
- Any other domain-specific skills

Only reference skills that are actually installed. Do NOT reference skills that
don't exist in the environment.

### Step 3: Map Skills to OpenSpec Workflow Steps

| Workflow Step | Skills to Invoke | Why |
|---------------|-----------------|-----|
| `proposal` | Reference subsystem design spec phases | Proposal scope matches one phase from the design spec |
| `specs` | *(general practice)* | WHEN/THEN scenarios must be translatable to test cases |
| `design` | `superpowers:brainstorming` (if exploratory) | Explore alternatives before committing |
| `tasks` | Reference subsystem design spec phase | Task grouping follows phase structure, TDD ordering |
| `apply` | `superpowers:test-driven-development`, tech-specific skills | TDD within each task, language conventions during coding |
| Post-apply | `superpowers:verification-before-completion` | Evidence before claiming done |

### Step 4: Generate config.yaml

Write `openspec/config.yaml` with two sections:

#### `context:` section

Two parts: **project-wide** (stable, set once) and **current phase** (updated
per phase). Both are injected into every `openspec instructions` call, so keep
them concise to minimize token consumption.

```yaml
context: |
  ## Artifact Compliance
  After writing any artifact, re-read each rule from the instructions and verify
  the written content satisfies every rule. Fix violations before reporting
  completion. Rules are constraints, not suggestions.

  ## Project: <name>
  <1-2 sentence description from project docs>

  ## Tech Stack
  <language, framework, key libraries, build system>

  ## Architecture Principles
  <from system spec or CLAUDE.md — keep to 3-5 bullets>

  ## Development Discipline
  - TDD (red-green-refactor): Use superpowers:test-driven-development during apply.
  - <tech-specific>: Use <skill-name> when writing <language> code.
  - Conventions: see docs/conventions.md

  ## Current Phase: S{n}.{m} — {Phase Name}
  <paste the phase section from the subsystem design spec — scope, contracts
  consumed/exposed, gate, verification, review tier, dependencies>

  ## Contracts from Prior Phases
  <for each phase listed in "Contracts consumed", paste ONLY its
  "Contracts exposed" block — type/trait signatures, not full phase section>
```

**Why this structure matters:** The project-wide section is ~15-20 lines and
rarely changes. The current phase section is ~10-30 lines and changes per phase.
Together they give the AI exactly what it needs without loading the full design
spec (~1000 lines).

#### `rules:` section

Per-artifact constraints. Only valid OpenSpec artifact IDs: **proposal**,
**design**, **specs**, **tasks**.

**IMPORTANT:** Do NOT add `prd` or any other ID not in this list. OpenSpec will
reject unknown artifact IDs with: `Unknown artifact ID in rules`.

**Use these rules verbatim.** Do not rephrase, simplify, or "improve" the
wording — the exact text matters because it's what gets injected into artifact
instructions across sessions. You MAY append project-specific rules after the
standard ones.

**YAML safety:** Always quote rule strings that contain `: ` (colon-space) —
YAML interprets unquoted `key: value` as a mapping, not a string. When in doubt,
quote all rule strings.

```yaml
rules:
  proposal:
    - "Scope this proposal to a single phase from the Subsystem Design Spec."
    - "Reference the phase's scope, contracts exposed/consumed, and gate criteria."
    - "Each phase must be reviewable, testable, and contract-bounded."
    - "Include the review tier (gate-only, spot-check, full-review) from the design spec."
  specs:
    - "Every requirement MUST have at least one WHEN/THEN scenario."
    - "Scenarios must be directly translatable to TDD test cases."
    - "Reference acceptance criteria (AC-{n}.{y}) from the design spec user stories."
  design:
    - "Follow FP-first architecture: types → pure functions → effects → composition."
    - "Justify decisions with rationale and alternatives considered."
    - "Flag risks with mitigations."
    - "Reference design decisions (D{n}) from the Subsystem Design Spec where applicable."
  tasks:
    - "Order tasks for TDD — test first, then implementation."
    - "Each task must be completable in one TDD cycle (red-green-refactor)."
    - "Include a gate task that runs the phase's gate command and verification steps."
    - "After the gate task, include a separate documentation task that: (1) updates docs/conventions.md with newly established contracts, and (2) writes a manual verification guide documenting how to manually verify the phase's output (commands to run, expected output, what to inspect)."
```

### Step 5: Present for Review

Show the generated config.yaml to the user. Highlight:
- Which project docs were used for context
- Which skills were discovered and mapped
- Which phase is set as the current phase
- Any gaps (e.g., "no tech-specific skill found for your language")

### Step 6: Phase Context Switch

**Run this step each time you start a new phase — BEFORE creating a new
change with `opsx:new` or `openspec-new-change`.** This is a prerequisite,
not optional. If config.yaml still references the previous phase, every
artifact in the new change will inherit stale context (wrong contracts,
wrong gate, wrong verification steps).

**Workflow integration:** The first action when beginning a new phase is:
1. Run `openspec-config` (this skill) to switch the phase context
2. Then run `opsx:new` to create the change

**What to update** (phase-specific blocks only — do NOT touch project-wide
parts or rules):

1. Open the Subsystem Design Spec, locate the next phase's section (e.g., S1.3)
2. Replace the `## Current Phase` block in config.yaml with the new phase's
   scope, contracts consumed/exposed, gate, verification, review tier, and
   dependencies
3. Replace the `## Contracts from Prior Phases` block with ONLY the "Contracts
   exposed" entries from each phase listed in "Contracts consumed"
4. Do NOT include full prior phase sections, implementation details, or
   unrelated phases

**Example:** When switching to S1.7 (YFinance DataSource), which consumes
S1.1 contracts and S1.5 rate limiting:

```yaml
  ## Current Phase: S1.7 — YFinance Data Source
  Scope: Implement DataSource trait for Yahoo Finance. HTTP client, response
    parsing, symbol mapping (IDX:BBCA -> BBCA.JK), timezone conversion, date
    range chunking.
  Size estimate: ~5 files, ~450 lines
  Contracts consumed: S1.1 (DataSource trait, OhlcvBar, DataSourceError),
    S1.5 (RateLimiter, RetryPolicy)
  Contracts exposed: YFinanceDataSource::new(config) -> Self, implements
    DataSource trait, SymbolMapper::to_yahoo(market, ticker) -> String
  Gate: cargo test — mock HTTP response tests
  Verification: Verify symbol mapping for IDX, timezone conversion, HTTP error
    classification, date range chunking
  Review tier: full-review
  Dependencies: S1.1 contracts, S1.5 rate limiting

  ## Contracts from Prior Phases
  S1.1: OhlcvBar { timestamp, open, high, low, close, volume, adjusted_close },
    DataSource trait (fetch_ohlcv), DataSourceError enum, Resolution enum
  S1.5: RateLimiter::new(rps), acquire() -> impl Future;
    RetryPolicy::new(max_attempts, initial_backoff_ms),
    retry_with_backoff(policy, action) -> Result<T, RetryExhausted<E>>
```

This gives the AI ~20 lines of phase context instead of ~1000 lines of full
spec. Over 80 phases, the token savings are substantial.

## Anti-Rationalization Table

| Thought | Reality |
|---------|---------|
| "The project is simple, config.yaml is overkill" | Simple projects grow. Config.yaml costs nothing and prevents discipline gaps. |
| "CLAUDE.md already has my conventions" | CLAUDE.md isn't injected into OpenSpec instructions. config.yaml is. |
| "I'll remember to invoke TDD manually" | You won't. Sessions don't share memory. Config.yaml does. |
| "The skills will be picked up from the system prompt" | Skills are invoked on trigger words. Artifact creation doesn't trigger them without config.yaml. |
| "I'll add context later when I need it" | Later = after the gap causes a problem. Set it up now. |
| "I'll update config.yaml after creating the change" | Too late — artifacts already generated with stale phase context. Update BEFORE `opsx:new`. |

## Maintenance

Re-run this skill when:
- New Subsystem Design Spec is created
- Tech stack changes (new language, framework)
- New skills are installed
- After a retrospective reveals a discipline gap
