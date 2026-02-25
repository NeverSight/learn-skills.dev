---
name: implement
description: Use this skill when writing code — building features, fixing bugs, refactoring, or any multi-step implementation work. Activates on mentions of implement, build this, code this, start coding, fix this bug, refactor, make changes, develop this feature, implementation plan, coding task, write the code, or start building.
---

# Implementation

Verification-driven coding with tight feedback loops. Distilled from 21,321 tracked operations across 64+ projects, 612 debugging sessions, and 2,476 conversation histories. These are the patterns that consistently ship working code.

**Core insight:** 2-3 edits then verify. 73% of fixes go unverified — that's the #1 quality gap. The difference between a clean session and a debugging spiral is verification cadence.

## The Sequence

Every implementation follows the same macro-sequence, regardless of scale:

```dot
digraph implement {
    rankdir=LR;
    node [shape=box];

    "ORIENT" [style=filled, fillcolor="#e8e8ff"];
    "PLAN" [style=filled, fillcolor="#fff8e0"];
    "IMPLEMENT" [style=filled, fillcolor="#ffe8e8"];
    "VERIFY" [style=filled, fillcolor="#e8ffe8"];
    "COMMIT" [style=filled, fillcolor="#e8e8ff"];

    "ORIENT" -> "PLAN";
    "PLAN" -> "IMPLEMENT";
    "IMPLEMENT" -> "VERIFY";
    "VERIFY" -> "IMPLEMENT" [label="fix", style=dashed];
    "VERIFY" -> "COMMIT" [label="pass"];
}
```

**ORIENT** — Read existing code before touching anything. `Grep -> Read -> Read` is the dominant opening. Sessions that read 10+ files before the first edit require fewer fix iterations. Never start with blind changes.

**PLAN** — Scale-dependent (see below). Skip for trivial fixes, write a task list for features, run a research swarm for epics.

**IMPLEMENT** — Work in batches of 2-3 edits, then verify. Follow the dependency chain. Edit existing files 9:1 over creating new ones. Fix errors immediately — don't accumulate them.

**VERIFY** — Typecheck is the primary gate. Run it after every 2-3 edits. Run tests after feature-complete. Run the full suite before commit.

**COMMIT** — Tests are the final gate. Stage specific files only, never `git add -A`. HEREDOC commit messages with conventional commit format.

---

## Scale Selection

Strategy changes dramatically based on scope. Pick the right weight class:

| Scale | Edits | Strategy |
|-------|-------|----------|
| **Trivial** (config, typo) | 1-5 | Read -> Edit -> Verify -> Commit |
| **Small fix** | 5-20 | Grep error -> Read -> Fix -> Test -> Commit |
| **Feature** | 50-200 | Plan -> Layer-by-layer impl -> Verify per layer |
| **Subsystem** | 300-500 | Task planning -> Wave dispatch -> Layer-by-layer |
| **Epic** | 1000+ | Research swarm -> Spec -> Parallel agents -> Integration |

**Skip planning when:** Scope is clear, single-file change, fix describable in one sentence.

**Plan when:** Multiple files, unfamiliar code, uncertain approach.

---

## Dependency Chain

Build things in this order. Validated across fullstack, Rust, and monorepo projects:

```
Types/Models -> Backend Logic -> API Routes -> Frontend Types -> Hooks/Client -> UI Components -> Tests
```

**Fullstack (Python + TypeScript):**
1. Database model + migration
2. Service/business logic layer
3. API routes (FastAPI or tRPC)
4. Frontend API client
5. React hooks wrapping API calls
6. UI components consuming hooks
7. Lint -> typecheck -> test -> commit

**Rust:**
1. Error types (`thiserror` enum with `#[from]`)
2. Type definitions (structs, enums)
3. Core logic (`impl` blocks)
4. Module wiring (`mod.rs` re-exports)
5. `cargo check` -> `cargo clippy` -> `cargo test`

**Key finding:** Database migrations are written AFTER the code that needs them. Frontend drives backend changes as often as the reverse.

---

## Verification Cadence

The single most impactful practice. Get this right and everything else follows.

| Gate | When | Speed |
|------|------|-------|
| **Typecheck** | After every 2-3 edits | Fast (primary gate) |
| **Lint (autofix)** | After implementation batch | Fast |
| **Tests (specific)** | After feature complete | Medium |
| **Tests (full suite)** | Before commit | Slow |
| **Build** | Before PR/deploy only | Slowest |

### The Edit-Verify-Fix Cycle

The sweet spot: **3 changes -> verify -> 1 fix**. This is the most common successful pattern.

The expensive pattern: **2 changes -> typecheck -> 15 fixes** (type cascade). Prevent by grepping all consumers before modifying shared types.

**Combined gates save time:** `turbo lint:fix typecheck --filter=pkg` runs both in one shot. Scope verification to affected packages, never the full monorepo.

**Practical tips:**
- Run `lint:fix` BEFORE `lint` check to reduce iterations
- `cargo check` over `cargo build` (2-3x faster, same error detection)
- Truncate verbose output: `2>&1 | tail -20`
- Wrap tests with timeout: `timeout 120 uv run pytest`

---

## Decision Trees

### Read vs Edit

```
Familiar file you edited this session?
  Yes -> Edit directly (verify after)
  No  -> Read it this session?
    Yes -> Edit
    No  -> Read first (79% of quick fixes start with reading)
```

### Subagents vs Direct Work

```
Self-contained with a clear deliverable?
  Yes -> Produces verbose output (tests, logs, research)?
    Yes -> Subagent (keeps context clean)
    No  -> Need frequent back-and-forth?
      Yes -> Direct
      No  -> Subagent
  No -> Direct (iterative refinement needs shared context)
```

### Refactoring Approach

```
Can changes be made incrementally?
  Yes -> Move first, THEN consolidate (separate commits)
        New code alongside old, remove old only after tests pass
  No  -> Analysis phase first (parallel review agents)
        Gap analysis: old vs new function-by-function
        Implement gaps as focused tasks
```

### Bug Fix vs Feature vs Refactor

| Type | Cadence | Typical Cycles |
|------|---------|---------------|
| **Bug fix** | Grep error -> Read 2-5 files -> Edit 1-3 files -> Test -> Commit | 1-2 |
| **Feature** | Plan -> Models -> API -> Frontend -> Test -> Commit | 5-15 |
| **Refactor** | Audit -> Gap analysis -> Incremental migration -> Verify parity | 10-30+ |
| **Upgrade** | Research changelog -> Identify breaking changes -> Bump -> Fix consumers | Variable |

---

## Error Recovery

**65% of debugging sessions resolve in 1-2 iterations.** The remaining 35% risk spiraling into 6+ iterations.

### Quick Resolution (Do This)

1. Read relevant code first (79% success correlation)
2. Form explicit hypothesis: "The issue is X because Y"
3. Make ONE targeted fix
4. Verify the fix worked

### Spiral Prevention (Avoid This)

1. **Separate error domains** — fix ALL type errors first, THEN test failures. Never interleave.
2. **3-strike rule** — after 3 failed attempts on same error: change approach entirely, or escalate.
3. **Cascade depth > 3** — pause, enumerate ALL remaining issues, fix in dependency order.
4. **Context rot** — after ~15-20 iterations, `/clear` and start fresh. A clean session with a better prompt beats accumulated corrections every time.

### The Two-Correction Rule

If you've corrected the same issue twice, `/clear` and restart. Accumulated context noise defeats accuracy.

---

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| 20+ edits without verification | Verify every 2-3 edits |
| Fix without verifying the fix (73% of fixes!) | One fix, one verify, repeat |
| `fix -> fix -> fix` chains without checking | Always verify between fixes |
| Editing without reading first | Read the file immediately before editing |
| Writing tests from memory | Read actual function signatures first |
| Changing shared types without grepping consumers | `Grep` all usages before modifying shared types |
| Mixing move and change in one commit | Move first commit, change second commit |
| Debugging spiral past 3 attempts | Change approach or escalate |
| Premature optimization | Correctness first, optimize after tests pass |

---

## Cross-Model Review

For high-stakes changes, use `/hyperskills:codex-review` after implementation. A fresh model context eliminates implementation bias and catches real bugs: migration idempotency, PII in debug logging, empty array edge cases, missing batch limits.

---

## References

For quantitative benchmarks and implementation archetype templates, consult `references/benchmarks.md`.

---

## What This Skill is NOT

- **Not a gate.** Don't follow all five phases for a typo fix. Scale selection exists for a reason.
- **Not a replacement for reading code.** This skill tells you HOW to implement, not WHAT to implement.
- **Not a planning tool.** Use `/hyperskills:plan` for task decomposition.
- **Not an excuse to skip tests.** "Verify" means running actual checks, not eyeballing the diff.
