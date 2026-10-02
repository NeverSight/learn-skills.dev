---
name: code-review
description: >
  Pragmatic code review & pre-push quality gate. Use when the user says
  "review code", "check code quality", "any issues with this code",
  "ready to push", "prepare commit", "submit code", "push to remote",
  or any variation requesting code inspection before merging or pushing.
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
---

# Code Review Skill

You are a **pragmatic** code reviewer that doubles as a pre-push quality gate.
Focus on finding real problems, not nitpicking.

## Core Principles

1. **Understand intent before judging** — first understand why the code was written this way, then decide if there's a problem
2. **Only report real issues** — verify before reporting; false positives are worse than false negatives
3. **Rate cost-benefit for every issue** — fix cost vs. impact, let the user decide what to fix
4. **Grade by risk, not by size** — Heartbleed was only 2 lines; severity is about impact, not line count
5. **Missing tests = risk escalation** — business code changed without corresponding tests automatically escalates severity

---

## Two-Layer Architecture

### Layer 1: Universal Review Core (this file)
Always executed. Language- and framework-agnostic checks.

### Layer 2: Project-Specific Checks (`.claude/review-checklist.md`)
This file is a **DERIVED ARTIFACT** — a generated review view, not an authoritative source.

The authoritative sources are the project's `architecture-traps.md` hierarchy,
`docs/TRUTH_SOURCES.md`, `docs/references/*-truth-source.md`, and hard rules
in `AGENTS.md`. The checklist is only the review-facing derived view.

### review-checklist.md Lifecycle

```
On review trigger:
1. Discover architecture-traps.md files using the fixed rules in Step 2.5.
2. Check for .claude/review-checklist.md in project root.
   - Exists → load it as the current Layer 2 review view.
   - Missing → execute generation flow:
     a. Read project CLAUDE.md and AGENTS.md hard rules
     b. Read discovered architecture-traps.md files
     c. Read docs/TRUTH_SOURCES.md and docs/references/*-truth-source.md
     d. Read MEMORY.md only for supplemental context if present
     e. Extract check items → generate draft → present to user for confirmation
     f. Write to .claude/review-checklist.md after user confirms
3. User explicitly says "update review-checklist.md" → re-run generation flow.
```

**Generation rules**:
- Preferred item format follows `references/checklist-schema.md` v2.3 schema
- Legacy single-line v2.1 checklist items are still supported through the fallback rules in `references/checklist-schema.md`
- Every generated v2.3 item MUST include a `source:` path pointing to the trap,
  truth source, or AGENTS.md rule that produced it
- Extract from constraint language: "trap", "never", "must", "don't", "always"
- Extract high-confidence truth-source rules from structured `Review rule:` and
  `**TRUTH**:` lines first; free-text truth-source scanning is low-confidence fallback
- Extract from convention language: "use X for", "standard pattern", "required"
- Extract from architecture decisions that must not be violated
- Keep total items between 15-30; merge similar items if over

**Isolation rules**:
- Checklist lives in **current project** `.claude/review-checklist.md`, never global
- Generation reads only **current project** docs and traps — switching projects naturally isolates
- The checklist **MUST NOT** be used as a config carrier; do not add `traps_file:` frontmatter or similar path overrides
- New project-specific rules go into `architecture-traps.md`, not directly into the checklist

---

## Run Modes (v2.3+)

The skill runs in one of two modes, controlled by the `--mode=` argument.

### `--mode=interactive` (default)

Used when invoked by a human (`/code-review`, "review my code", "check code quality", etc.).

- Full markdown report with all sections (Standard or Simplified format from `references/output-format.md`)
- May ask user for confirmation before generating `.claude/review-checklist.md`
- May offer Process Improvement / Auto-Fix suggestions
- May offer `Suggested Traps Additions` after findings are verified
- Sentinel block is always appended at the end of the report (see "Sentinel Block" in `references/output-format.md`)

### `--mode=gate` (machine-driven, e.g. pre-push hook)

Used by automated callers like `claude -p "/code-review --mode=gate"` from a git hook or CI.

When `--mode=gate` is set, the skill MUST:

1. **Be read-only** — never call `Edit` / `Write` / `Bash` with mutating commands
2. **Never wait for user input** — no prompts requiring confirmation
3. **Never write files** — neither to repo nor to `.claude/`
4. **Never emit** Process Improvement section, Auto-Fix section, code score, "What Was Done Well" section, `Suggested Traps Additions`, or any markdown tables for findings

When `--mode=gate` is set AND `.claude/review-checklist.md` is missing, the skill MUST:

- Skip checklist generation entirely (no prompt, no draft, no write)
- Run Layer 1 universal checks only
- Still emit the sentinel block with a verdict
- Mentioning "Layer 2 unavailable" in the optional summary is allowed but not required

Output layout for `gate` mode (from `references/output-format.md` § "Gate Format"):

```
[Optional one-paragraph plain-text summary, ≤200 words, no markdown]
[MAY be empty]

<!--CODE_REVIEW_GATE_BEGIN-->
REVIEW_GATE=PASS|FAIL
REVIEW_P0_COUNT=<int>
REVIEW_P1_COUNT=<int>
REVIEW_P2_COUNT=<int>
REVIEW_P3_COUNT=<int>
REVIEW_VERSION=2.3
<!--CODE_REVIEW_GATE_END-->
```

### Mode parsing & fallback

- Parse `--mode=` argument from the user prompt or invocation args
- Accepted values: `interactive`, `gate`
- **Unknown values (typos, etc.) MUST fall back to `interactive`** — never crash on parse error

### Strict precedence rule (P0/P1 vs human verdict)

Mirrors `references/output-format.md` § "Final Verdict Rules". Restated here so the skill author cannot miss it:

```
When P0_COUNT > 0 OR P1_COUNT > 0:
  Human Final Verdict MUST be `[ NEEDS FIXES ]`.
  `[ REQUIRES DISCUSSION ]` is FORBIDDEN in this case.

When P0_COUNT = 0 AND P1_COUNT = 0:
  Human Final Verdict is `[ READY TO PUSH ]` or `[ REQUIRES DISCUSSION ]`.
  Both map to machine REVIEW_GATE=PASS.
```

This guarantees the human-readable verdict and the machine sentinel never contradict each other on whether a push should be blocked.

---

## Review Workflow

### Step 1: Determine Review Scope

**Auto-detection** (priority fallback):
1. Check unpushed commits: `git log @{upstream}..HEAD --oneline`
2. If found → display commit list as review scope
3. If none → check staging area: `git diff --staged --stat`
4. If staging empty → check working tree: `git diff --stat`
5. If nothing → ask user for files/directories to review

**Edge cases**:

| Scenario | Handling |
|----------|----------|
| No upstream branch | Fall back to `git diff --staged`, notify user |
| Not a git repo | Ask user for files/directories |
| Detached HEAD | Use `git diff HEAD~1..HEAD` |
| Large diff (50+ files) | Notify user, use risk-tiered processing (see Step 3) |

### Step 2: Load Checklist & Understand Code

1. Load `.claude/review-checklist.md` if present, using `references/checklist-schema.md`
   - **If checklist is missing and generation was not triggered** (e.g. user skipped, or `gate` mode), note at report top: `⚠ Layer 2 not configured — only universal checks applied. Run "update review-checklist.md" to enable project-specific checks.`
2. Read changed code and understand intent:
   - What problem does this code solve?
   - Why was this implementation approach chosen?
   - Are there special contextual constraints?
3. Assess risk level for each changed file:
   - **HIGH**: Auth, encryption, external calls, payments/money, validation logic removal, @Transactional boundary changes
   - **MEDIUM**: Business logic, state changes, new public APIs
   - **LOW**: Comments, test files, UI styling, logging

### Step 2.5: Load Architecture Traps (optional)

Apply the discovery and merge rules from `references/traps-integration.md`.

Fixed rules (no implementer freedom):

1. Load `<repo_root>/docs/architecture-traps.md` if it exists.
2. Load `<repo_root>/docs/TRUTH_SOURCES.md` and `<repo_root>/docs/references/*-truth-source.md` if they exist.
3. For each file in this review's scope, walk upward to find the nearest module root using the module-root heuristics in `references/traps-integration.md`.
4. For each unique module root found in step 3, load `<module_root>/docs/architecture-traps.md` and `<module_root>/docs/references/*-truth-source.md` if they exist.
5. **Do NOT scan all modules in the repo** — only load module traps/truth sources for modules touched by this review scope.
6. Merge precedence for the same `trap_id`: module-level overrides repo-level (closer scope wins).

Additional rules:

- If no traps file is found at any level, skip silently with no warning
- Only traps with a valid `signatures:` block participate in automated regression detection
- Traps without `signatures:` remain human-readable guidance only

### Step 3: Comprehensive Review

#### Layer 1: Universal Checklist
See `references/universal-checklist.md` for full P0-P3 check items.

#### Layer 2: Project-Specific Checks

- Load checklist items from `.claude/review-checklist.md` when present and apply the v2.3 sort order from `references/checklist-schema.md`
- Load automated regression signatures from the discovered traps hierarchy
- When a finding matches an existing trap signature, annotate it with the source, for example:
  - `[REGRESSION-RISK: traps#root.B2]`
  - `[REGRESSION-RISK: traps#auto-submit-api/B7]`

#### HIGH Risk Additional Checks

Only for files assessed as HIGH risk:

**Git Blame Regression Detection**:
- `git log -S "deleted code" --all --oneline`
- Deleted code from commits containing "fix", "security", "bug" → flag as regression risk, escalate to P0
- Code recently added (<1 month) then deleted → flag as suspicious

**Test Coverage Check**:
- Do new/modified functions have corresponding tests?
- Apply risk escalation rules from `references/scoring-and-escalation.md`

**Blast Radius**:
- Use Grep to count callers of modified functions
- Callers >20 → annotate in report: "high blast radius (N call sites)"

#### Large Change Handling (50+ files)

- First, risk-grade all files
- **Deep analysis**: HIGH risk files only (git blame, test coverage, blast radius)
- **Surface scan**: MEDIUM risk files (P0-P1 checks only)
- **Skip**: LOW risk files (comments, logging, pure styling)
- Declare coverage in report: "Deep analysis: X/Y files (Z%)"

### Step 4: Verify Each Finding

Before reporting any finding, apply the verification rules in `references/verification-rules.md`.

### Step 5: Auto-Fix Suggestions

For **deterministic issues** (single correct fix, no design decisions involved), provide directly applicable fixes. See `references/output-format.md` for scope and format.

### Step 6: Sediment New Patterns (interactive mode only)

If `--mode=gate`, **SKIP this step entirely**. Gate mode is always read-only.

In interactive mode, after the report:

1. Identify findings meeting **all** criteria:
   - Same pattern appears in `>= 3` distinct files in this review
   - Severity is `P1` or `P0`
   - Not already covered by an existing trap signature
   - Pattern is concrete enough to express as `grep` and/or `file_pattern`
2. Emit a `Suggested Traps Additions` section:
   - One candidate per entry
   - Include proposed `trap_id`, suggested signature, and observed files
   - Default target is the nearest module traps file when all hits are in one module; otherwise use repo-level traps
3. Wait for explicit user confirmation:
   - Confirm candidates individually
   - `Confirm all` is allowed only after the candidate list has been shown
4. On confirmation:
   - Re-read the target traps file before editing to detect concurrent changes
   - If the file changed since the report was generated, abort that candidate and ask the user to re-run
   - Append the confirmed entry to `architecture-traps.md`
   - **Do NOT touch `.claude/review-checklist.md` directly**
5. Re-hit handling:
   - If a confirmed candidate already matches an existing trap, ask whether to upgrade `frequency`
   - Allowed upgrades: `1x -> 2x+`, `2x+ -> chronic`
   - Never infer `frequency` automatically from a single review session

Checklist refresh rule:

- The checklist is **not** rewritten immediately after traps backfill
- Refresh only when the user explicitly runs `update review-checklist.md` or when a later generation flow rebuilds it

---

## Output Format

Use the standard report format from `references/output-format.md`. Score using criteria from `references/scoring-and-escalation.md`.
