---
name: audit-and-migrate
description: |
  Slice-based, evidence-driven framework for auditing and migrating debt-heavy codebases. Use for large refactors, codebase consolidation, tech debt paydown, dependency standardization, architecture cleanup, or any multi-session migration. Also use when asked to audit the codebase, migrate from X to Y, standardize on one approach, consolidate duplicated code, or run a systematic refactor with built-in cleanup, residue sweeps, and a final ship-readiness gate. Make sure to use this skill whenever the user wants a controlled migration with slices, guardrails, handoffs, cleanup, or release closeout, even if they do not explicitly say "migration". Mentions of ratchets, slices, migration playbooks, anti-vestigial discipline, convergence, or release cleanup should strongly trigger it.
---

# Systematic Codebase Audit & Migration

A structured methodology for tackling codebases with accumulated technical debt. Works in three phases — **audit** (understand and freeze the problem), **migrate** (pay it down slice by slice with proof), then **closeout** (remove residue and prove the repo is actually ready to ship).

## Why This Methodology Exists

Agents without structure fail at four things during large refactors:

1. **Drift** — forgetting what's been done, redoing completed work, or leaving things half-finished across sessions. This wastes time and introduces conflicts.
2. **Vestigial code** — adding new implementations without deleting what they replace. The codebase grows when it should be shrinking.
3. **Intuition-driven confidence** — saying "this should work" instead of proving it. When an agent can't point to a deterministic check that passed, its confidence is unfounded.
4. **False finish** — stopping when the new path works even though temporary adapters, stale docs, orphaned dependencies, or release blockers remain.

Every rule in this methodology prevents one of these four failures. When a rule feels heavy, that's the justification.

---

## Session Protocol

**Do this at the start of every session.** This is what makes the methodology survive context compaction and session switches.

### Starting a Session

1. Check if control plane artifacts exist (look in `.claude/migration/` or wherever the project stores them):
   - `CHARTER.md`, `DECISIONS.md`, `SLICES.yaml`, `MAP.csv`, `RATCHETS.yaml`, `SHIP_CHECKLIST.md`
   - Latest `HANDOFF.md` if prior sessions have touched the migration
2. If they **don't exist** → you're starting fresh. Begin with Phase 1 (Audit).
3. If they **do exist** → read them in this order:
   a. `CHARTER.md` — re-absorb the mission and invariants
   b. `SHIP_CHECKLIST.md` — re-load the project-specific definition of "ready to ship"
   c. `DECISIONS.md` — understand what's been decided and why
   d. Latest `HANDOFF.md` — recover current status and blockers quickly
   e. All `in_progress` slices in `SLICES.yaml` — this is your current work
   f. Run the guard script to see current status

### Ending a Session

Write or update `HANDOFF.md` (or append to the most recent commit message if the handoff is small). Five parts, no exceptions:

1. **What changed** — files modified, slices advanced, decisions made
2. **What is now true** — new invariants, completed slices, updated budgets
3. **What remains** — incomplete slices, known risks, blocking issues
4. **What blocks shipping right now** — explicit blockers, or `None`
5. **Exact next steps** — the specific command or test sequence to run next

Example:
```markdown
## Handoff — 2026-03-01
### Changed
- Completed slice-003 (user routes auth migration)
- Ratchet budget for jwt.verify decreased from 8 → 5

### Now True
- All user route auth goes through withAuth() middleware
- Behavioral tests cover user routes at 100%

### Remains
- slice-004 (data routes) ready to start
- slice-005 (admin routes) blocked on Decision 4 re: webhook auth

### Shipping Blockers
- None

### Next Steps
1. Run `./guard.sh --status` to confirm baseline
2. Start slice-004: mark in_progress in SLICES.yaml
3. Write behavioral tests for src/api/posts.ts and src/api/comments.ts
```

This format survives context compaction. The next session (or a different agent) can pick up without information loss or having to guess whether the repo is actually releasable.

---

## Phase 1: Audit

The audit phase is about understanding the problem space before changing production code. Measuring first creates the foundation that makes migration safe, and defining the ship gate early prevents the common failure mode where the implementation lands but cleanup keeps spilling into follow-up runs.

### Step 1: Create the Charter

Create `CHARTER.md` using the template in [references/templates/CHARTER.md](references/templates/CHARTER.md). This defines:

- **Mission** — one sentence: what are you migrating and why
- **Critical workflows** — user-visible paths that must not regress
- **External surfaces** — public APIs, env vars, dashboards, webhooks, CLI entrypoints, data contracts, or automation hooks the migration might break outside the immediate repo
- **Invariants** — things that must remain true throughout (e.g., "all existing tests pass", "no user-facing behavior changes")
- **Non-goals** — things you're explicitly NOT doing (prevents scope creep)
- **Guardrails** — process rules
- **Ship gate** — the exact automated and manual evidence required before calling the migration done

The charter is the constitution. When in doubt about scope, check the charter.

### Step 2: Inventory the Problem Space

Catalog everything in the target domain — code, tests, scripts, docs, configuration, tooling, and dependencies. For each item, classify by leverage:

- **High** — keep and expand. Good code the migration builds on.
- **Medium** — keep but refactor. Structurally sound but needs updating.
- **Low** — replace. This is the debt you're paying down.

Be exhaustive. Anything missed here risks becoming vestigial code later. If an item is low leverage, record what will replace it or which slice will delete it.

### Step 2b: Capture Critical Workflows and Hotspots

Before designing slices, sweep for the parts of the system most likely to burn you later:

- **Critical workflows** — the user-facing paths that absolutely cannot regress
- **Known hotspots** — recent bug-fix churn, TODO/FIXME/HACK clusters, flaky tests, or fragile subsystems
- **Manual-only surfaces** — visual checks, hardware, or third-party UI flows automation cannot fully prove

These become your slice smoke tests, manual checks, and ship-gate inputs.

### Step 3: Measure Anti-Patterns

Use grep/ripgrep to count specific weak patterns. The goal is concrete numbers, not vibes.

For each pattern, record:
- The grep pattern used to find it
- The search scope used to find it
- The current count
- Why it's problematic

**Examples** (adapt to your codebase):
```
Pattern: source\.contains\(        Scope: test/          Count: 43    Problem: Tests code shape, not behavior
Pattern: Task\.sleep\(             Scope: test/          Count: 17    Problem: Non-deterministic timing
Pattern: struct Scenario           Scope: test/          Count: 22    Problem: Duplicated test scaffolding
Pattern: require\(.*/utils/old-    Scope: src/ docs/     Count: 8     Problem: Imports from deprecated module
```

### Step 4: Freeze with CI Ratchets

For each measured anti-pattern, create a ratchet that enforces a maximum budget equal to the current count. See [The CI Ratchet Pattern](#the-ci-ratchet-pattern) for the technique.

This is the most important step. Once ratchets are in place, debt can only decrease. No one — human or agent — can accidentally reintroduce eliminated patterns. Ratchets are only trustworthy if the query and search scope are explicit and the count measures matches, not just matching files.

Write these ratchets into `RATCHETS.yaml` using the template in [references/templates/RATCHETS.yaml](references/templates/RATCHETS.yaml). Do not let the guard script become the only place the budgets live.

### Step 5: Write the Audit Document

Create a comprehensive audit doc. Include:
- Method used (how you inventoried and measured)
- Current metrics (all anti-pattern counts)
- Leverage assessment (what's high/medium/low)
- Critical workflows and known hotspots
- Hard conclusions (what needs to change — be direct)
- Guardrails added (what CI checks are now in place)
- Ship criteria and manual-only verification surfaces
- Proposed slices (your initial plan for Phase 2)

### Step 5b: Produce Practical Reference Material

Alongside the control plane artifacts, produce domain-specific reference material that will accelerate the actual migration work:

- **Translation guide** — a lookup table mapping old patterns to their new equivalents (e.g., raw SQL queries → ORM calls, Redux patterns → Zustand patterns). This saves every slice from reinventing translations.
- **Edge cases and gotchas** — document known pitfalls when converting between the old and new approaches. Things that look like straightforward translations but have subtle behavioral differences.
- **Code pattern examples** — concrete before/after code samples for the most common migration scenarios.

This material pays for itself many times over — without it, every slice (and every agent session) independently rediscovers the same conversion patterns. With it, the knowledge is captured once and reused throughout.

### Step 6: Create Remaining Artifacts

Using templates in [references/templates/](references/templates/):
- `DECISIONS.md` — seed with any architecture decisions from the audit
- `SLICES.yaml` — populate with proposed slices from the audit doc
- `MAP.csv` — populate with all files from the inventory
- `RATCHETS.yaml` — machine-readable anti-pattern budgets and scopes
- `SHIP_CHECKLIST.md` — define the exact release gate once, then execute it during closeout

---

## Phase 2: Migration

Migration is slice-by-slice debt paydown. Each slice is a vertical, outcome-based unit of work that can be independently verified.

### Calibrate Before Starting

If the audit was done without full codebase access (e.g., based on a description or partial exploration), the first action in Phase 2 is calibrating the ratchet budgets against reality. Run every grep pattern from the audit document and update the guard script budgets with actual counts. This is a quick, high-value step — incorrect budgets produce either false failures (budget too low) or silent regression (budget too high).

Also run the guard script with a `--status` flag (if you added one) to confirm a clean green baseline before starting any slice work.

Also confirm `SHIP_CHECKLIST.md` contains exact commands and scenarios rather than placeholders. A closeout phase is only as good as the checklist it runs.

### Reserve the Closeout Slice

Before starting implementation, reserve a final **convergence** slice in `SLICES.yaml`. It should depend on every implementation slice and own whole-codebase cleanup: residue sweep, dependency pruning, docs/config reconciliation, and execution of `SHIP_CHECKLIST.md`.

If you don't reserve this slice up front, cleanup becomes "later work," and later work quietly becomes another migration.

### Picking the Next Slice

Review `SLICES.yaml` for the highest-leverage unblocked slice:
1. Check dependencies — don't start a slice whose dependencies aren't `done`
2. Prefer high-leverage slices (ones that eliminate the most anti-pattern instances or unblock other slices)
3. Prefer smaller blast radius when leverage is equal

### The Slice Lifecycle

Every implementation slice follows five stages.

#### A. Start
1. Mark the slice `in_progress` in `SLICES.yaml`
2. Ensure all files this slice will touch are listed in `MAP.csv`
3. Define `deletion_targets`, `temp_artifacts`, `dependency_changes`, `residue_queries`, `verification_commands`, `docs_to_update`, and any touched `external_surfaces` in `SLICES.yaml` before writing any code
4. Run the guard script to get a clean baseline

#### B. Build (TDD-first)

1. **Write tests that fail without the new behavior.** These tests define "done" for this slice. Test behavior through public interfaces, not implementation details.
2. **Implement the canonical path.** The new, correct way of doing the thing.
3. **Migrate call sites.** Update everything that uses the old path to use the new one.
4. **Update supporting artifacts in this same slice.** Docs, config, env examples, scripts, fixtures, and CI references are part of the migration, not follow-up chores.
5. **Delete the replaced code in this same slice.** This is a hard rule. The reasoning: agents that defer deletion forget. Old code becomes vestigial. By the time anyone notices, call sites have drifted back to using it. Deleting in the same change makes the migration atomic.
6. **Remove or explicitly track temporary scaffolding.** Adapters, debug helpers, one-off scripts, and temporary flags either die in this slice or get recorded as `temp_artifacts` with an owning slice.

#### C. Cleanup Sweep

Before calling the slice "verified," do a focused residue sweep across touched paths and their adjacent modules:

1. Search for orphaned files, unused exports, dead tests, stale adapters, dead branches, outdated docs/config, and unused dependencies exposed by this slice
2. Remove confirmed dead items immediately
3. If something might be dead but isn't provable yet, turn it into an explicit blocking follow-up slice or note it in `DECISIONS.md` with an owner and exit condition

Cleanup is not just "delete what you already planned to delete." It is "prove this slice didn't leave residue nearby."

Residue queries must be **specific and scoped**. Avoid broad patterns like `legacy` across the whole repo when legitimate retained names still exist. Prefer queries like `import.*legacy-auth`, `LEGACY_COOKIE_NAME`, or `TODO\\(migration\\)` with explicit search roots.

#### D. Verify

Run all applicable checks:
1. Guard script passes — no unmapped files, no denylist or residue violations
2. `verification_commands` pass — run the exact automated commands recorded in `SLICES.yaml`
3. Replay/smoke scenarios pass — if defined in `SLICES.yaml`, run them
4. `residue_queries` return zero matches — old names, flags, TODO markers, and temp markers are actually gone
5. Charter invariants and relevant ship-checklist requirements still hold
6. Manual checks are only used for surfaces automation cannot cover, and their results are recorded in slice notes
7. External surfaces still work — dashboards, public exports, env contracts, webhooks, or CLI entrypoints affected by the slice are explicitly re-checked

#### E. Close

1. Confirm all `deletion_targets` are physically removed (not commented out, not behind a flag — gone)
2. Confirm all `temp_artifacts` are removed or explicitly handed to a later owning slice
3. Reconcile `docs_to_update` and `dependency_changes`
4. Remove empty directories and migration-only scaffolding if the slice made them vestigial
5. Update `MAP.csv` — mark migrated files, remove deleted files, keep docs/config/tooling entries in sync
6. Update `SLICES.yaml` — mark slice `done`, record what was accomplished and what evidence passed
7. Update `RATCHETS.yaml` — decrement budgets, add notes for ratchets driven to zero
8. Add denylist patterns for removed names/paths
9. Record any new decisions in `DECISIONS.md`

If the cleanup sweep uncovers extra dead code beyond the original `deletion_targets`, either delete it now or create an explicit follow-up slice before calling the current slice done. Do not leave newly discovered residue as ambient debt.

---

## Phase 3: Closeout & Ship Gate

Migration is not complete when the last implementation slice lands. It is complete when the repo is globally clean and the project-specific ship gate passes.

Treat closeout as a real convergence slice, not an afterthought.

1. **Re-run the inventory.** Reconcile `MAP.csv` against reality. No unmapped files, orphaned replacements, or forgotten side artifacts.
2. **Run a whole-migration residue sweep.** Search code, tests, docs, config, tooling, and dependencies for leftovers: old symbols, dead files, stale adapters, unused packages, temporary flags, scratch scripts, debug logging, and TODO/FIXME/HACK markers introduced by the migration.
3. **Prune and verify dependencies.** Remove unused packages, scripts, feature flags, lockfile noise, and migration-only helpers.
4. **Reconcile operational surfaces.** README, ADRs, env examples, CI workflows, dashboards, public APIs, webhooks, CLI entrypoints, and developer docs must describe the new architecture, not the old one.
5. **Execute `SHIP_CHECKLIST.md`.** Run the exact lint/typecheck/build/test/replay/smoke/manual checks defined during the audit. Automate everything possible; manual checks are only for visual, experiential, hardware, or third-party surfaces automation cannot prove.
6. **Review the diff like a release candidate.** Look for accidental churn, empty directories, backup files, commented-out code, stray logs, or `old`/`new`/`final` artifacts.
7. **Write the final handoff.** State either `Ready to ship` or list the exact blockers that remain. If debt is intentionally retained, record it in `DECISIONS.md` with an owner and exit condition.

---

## The CI Ratchet Pattern

The methodology's signature technique. Instead of eliminating all instances of a bad pattern at once:

1. **Count** the pattern (e.g., 43 `source.contains` assertions)
2. **Set the budget** — CI maximum equals current count (43)
3. **Decrement** — each slice that eliminates instances reduces the budget
4. **Enforce** — CI fails if the count exceeds the budget
5. **Reach zero** — budget eventually hits 0, pattern fully eliminated
6. **Keep the guard** — maintain the check at 0 as a permanent regression guard

**Why this works so well for agents:** It provides a clear, mechanical pass/fail signal. No judgment about whether a few instances are "OK." The ratchet answers definitively. Progress is visible: 43 → 38 → 29 → 15 → 7 → 0 is a concrete trajectory.

**Implementation:** Typically a shell script that greps for the pattern, counts matches, compares against the budget, and exits non-zero if count exceeds budget. Count exact matches, not just matching files, and keep the search scope explicit. Budgets should live in `RATCHETS.yaml`, not only in the script. See [references/guard-script-pattern.md](references/guard-script-pattern.md) for the pattern. Wire it into CI or pre-commit hooks.

---

## Anti-Vestigial Discipline

Vestigial code — old code replaced but never deleted — is the biggest source of codebase bloat in agent-assisted development. Agents optimize for "does the new thing work?" without asking "did I remove the old thing?"

For every slice:

1. **Define `deletion_targets` before implementation.** Write them into `SLICES.yaml` before building. This creates accountability — you can't "forget" to delete something when it's pre-defined.

2. **Add denylist patterns for removed names/paths.** After deleting code, add a grep pattern to the guard script that fails if the name reappears. Stronger than test coverage because it catches reintroduction anywhere in the codebase.

3. **Delete docs describing removed architecture.** Stale docs about removed systems actively mislead future agents and developers.

4. **Remove obsolete scripts, config, and env fallbacks.** Configuration for removed features is invisible debt.

5. **No "temporary" adapters without:** an owning slice ID, an expiry condition, and an explicit deletion target. Adapters without a planned death live forever.

6. **Kill migration markers.** `TODO(migration)`, temporary debug logging, scratch files, and `old`/`new`/`final` copies are residue, not harmless notes.

---

## Slice Design Rules

Each slice must be:

- **Vertical and outcome-based** — a complete capability, not a horizontal sweep like "rename all files" or "update all imports." Vertical slices are independently meaningful.
- **Decision-complete** — ownership of logic is explicit. No shared ownership with unclear boundaries.
- **Independently verifiable** — has deterministic checks. If you can't write a guard or test that confirms correctness, the slice is too vague.
- **Cleanup-complete** — owns the neighboring dead code, docs, config, and temporary scaffolding it exposes. Not "feature works, cleanup later."
- **Bounded in blast radius** — small enough to review and revert cleanly. If reverting means untangling 40 files, split it.

---

## Confidence Model

When verifying slice correctness, use layered evidence in priority order:

1. **Deterministic replay** (highest confidence) — re-run inputs and diff outputs against known-good baselines
2. **Automated smoke tests** — exercise critical user-facing workflows end-to-end
3. **Full test suites** — run all tests across the codebase
4. **Manual checks** (lowest confidence) — only for high-risk UX changes

If evidence sources conflict, deterministic replay wins. "Tests pass but the replay diff differs" means something is wrong — investigate, don't dismiss.

If a check can be automated, it belongs in `verification_commands`, not in human memory or a future TODO.

---

## The Control Plane

Seven artifacts govern the migration. Templates are in [references/templates/](references/templates/).

| Artifact | Purpose | Update Frequency |
|---|---|---|
| `CHARTER.md` | Mission, invariants, non-goals, guardrails | Rarely (scope changes only) |
| `DECISIONS.md` | Append-only architecture decisions | Each decision-making slice |
| `SLICES.yaml` | Machine-readable slice ledger | Start and close of each slice |
| `MAP.csv` | Source-of-truth path mapping | Start and close of each slice |
| `RATCHETS.yaml` | Machine-readable anti-pattern budgets, scopes, and rationale | Seed in audit, update when budgets fall |
| `SHIP_CHECKLIST.md` | Project-specific release gate and closeout checklist | Seed in audit, execute during closeout |
| Guard script | CI-enforced invariant checks | When adding/removing ratchets |

### DECISIONS.md Protocol
- **Append-only.** Never edit past entries.
- **Reversals are new entries.** Changing your mind about decision #3? Add decision #7 that says "Supersedes #3" and explains why.
- **No silent rewrites.** Decision history matters for understanding the codebase's evolution.
- **Waivers expire.** If you ship with retained debt or a temporary exception, record the owner and exit condition.

### SLICES.yaml Fields
Each slice tracks: `id`, `type` (`implementation` or `convergence`), `name`, `status` (proposed → in_progress → done), `dependencies`, `touched_paths`, `external_surfaces`, `contracts` (added/changed/removed), `denylist_patterns`, `deletion_targets`, `temp_artifacts`, `docs_to_update`, `dependency_changes`, `residue_queries`, `verification_commands`, `replay_scenarios`, `smoke_scenarios`, `manual_checks`, `risks`, `notes`.

### MAP.csv Columns
`slice_id, kind, capability, current_path, target_path, status, delete_in_pr, verification, notes`

Every file touched by the migration must appear. This prevents files from falling through the cracks. Use `kind` to keep docs/config/tooling first-class, not invisible side work, and `verification` to record the command or scenario that proves the artifact is still valid.

---

## Agent Coordination

When using multiple agents or parallel sessions:

1. **Keep parallel work on truly independent file sets.** Two agents committing to the same branch can silently displace each other's work. Slice boundaries should map to non-overlapping files.

2. **CI ratchets are the most agent-friendly guardrail.** Mechanical pass/fail beats requiring judgment about whether a change is "safe."

3. **Denylist patterns prevent regression more reliably than tests.** A regex CI check saying "this function name must not appear in this directory" is stronger than hoping test coverage catches reintroduction.

4. **The handoff contract is non-negotiable.** Without it, context compaction causes agents to redo completed work or skip remaining work.

5. **Keep closeout owned by one slice.** Parallelize implementation slices when file sets are disjoint, but reserve one convergence slice that owns the final residue sweep and ship gate.

---

## Beyond Code

This methodology works for non-code domains too — scripts, docs, tooling, configuration. The cycle is the same: inventory → measure → freeze → pay down. The "delete in the same change" discipline and anti-vestigial sweeps are just as valuable when consolidating documentation or eliminating redundant scripts.
