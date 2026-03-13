---
name: assumption-killer
description: "Kills the untested assumptions in your codebase. Surfaces beliefs about how the system works that have never been verified against actual code, from critical gaps in business logic to subtle intent drift. Use when you're not sure if what Claude built matches what you meant, before launch, before a major integration, or after inheriting a codebase."
disable-model-invocation: true
argument-hint: "[generate|verify|fix]"
---

# The Assumption Killer

Verify that your code does what you think it does.

AI-generated code runs. It passes linters. It might even have tests. But does it match your business intent? Does the checkout flow actually enforce the rules you described? Does the auth system link accounts the way you expect?

This skill makes those beliefs explicit, then tests each one against the actual code. It applies to customer flows, business logic, cross-system dependencies — anywhere the gap between "what I asked for" and "what got built" can hide bugs.

> **Token warning:** This skill is intentionally thorough. The `generate` step uses parallel subagents to investigate flows concurrently. The `verify` step uses a 3-phase pipeline (extract→verify→compile) with file-based handoffs between agents to scale to large codebases without context overflow. Expect significant token usage. This is the tradeoff — shallow analysis misses bugs, deep analysis costs tokens.

## Step routing

- If `$0` is `generate` → run [Step 1: Generate](#step-1-generate)
- If `$0` is `verify` → run [Step 2: Verify](#step-2-verify)
- If `$0` is `fix` → run [Step 3: Fix](#step-3-fix)
- If `$0` is empty or unrecognized → explain the three steps and ask which to run

---

## Step 1: Generate

### Phase 1A: Repo Health Assessment

Before generating assumptions, assess the codebase to calibrate how much to trust what you read. A well-maintained repo gets benefit of the doubt. A neglected one gets deeper scrutiny on every assumption.

Investigate:

1. **Git history** — Run `git log --oneline -30` and `git shortlog -sn`. Evaluate:
   - Commit message quality (descriptive vs "fix" / "update" / "wip")
   - Commit frequency and recency
   - Number of contributors
   - Evidence of code review (merge commits, PR references)

2. **Code organization** — Use Glob and Read to assess:
   - Directory structure (logical grouping vs flat)
   - Naming conventions (consistent vs mixed)
   - Dead code, commented-out blocks, TODO density
   - Separation of concerns

3. **Documentation** — Tiered discovery and trust calibration:

   **Count first:** `find . -name "*.md" -not -path "*/node_modules/*" | wc -l`

   **Read depth scaled to count:**
   - < 10 files: read all tiers fully
   - 10–30 files: read tier 1–2 fully, scan headings for tier 3–4
   - 30+ files: read tier 1 fully, scan headings for tier 2–3, deep-read only if headings suggest business rules or architecture decisions

   **Tiers:**
   - **Tier 1 (always read fully):** `CLAUDE.md`, `AGENTS.md`, `agents.md`, `.cursorrules`, `copilot-instructions.md`
   - **Tier 2:** Root `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `CHANGELOG.md`
   - **Tier 3:** `docs/**/*.md`, `doc/**/*.md`
   - **Tier 4:** `*.md` inside source directories — scan headings only
   - **Skip:** `node_modules/**`

   **Trust calibration for Tier 1:** Extract 3–5 concrete verifiable claims (specific files, constants, values, described behaviors). Spot-check each against actual code. Check how much has changed since last update: `git log --oneline <last-tier1-commit>..HEAD | wc -l`. Claims that hold → High. Mixed → Medium. Contradicted → Low, treat as context only, rely on executable specs instead.

   **Executable specs (harvest regardless of doc quality):**
   - TypeScript interfaces and types used as specifications
   - Zod / Yup / Joi / Valibot schemas with constraints
   - Database / ORM schemas (Prisma, Drizzle, etc.)
   - Named constants and enums encoding business rules
   - Test `describe` / `it` names as stated behavior specs

   **Produce `/tmp/ak-doc-context.md`** — a tight synthesis, aim for < 100 lines:
   - Source trust levels with one-line reason each
   - Key business rules from highest-trust sources
   - Executable invariants from types, schemas, constants, and test descriptions
   - Contradictions found (sources disagreeing with code or each other — flag these as priority assumptions)
   - Calibration note: which sources to weight, which to treat as context only

4. **Test coverage** — Look for:
   - Test files and organization
   - Test runner config
   - Test-to-source ratio

5. **Dependency health** — Check package manifests for:
   - Lock file presence
   - Obviously outdated or deprecated packages

Write a brief **Repo Health Assessment** (5-10 lines) summarizing what you found. This calibrates the skepticism level for everything that follows.

### Phase 1B: Assumption Generation

Walk through **every user-facing flow** in the codebase, end to end. Be exhaustive — cover happy paths, error paths, edge cases, and boundary conditions.

**Use parallel subagents** (Task tool with `subagent_type: Explore`) to investigate multiple flows concurrently. Each flow is an independent investigation. Assign one subagent per flow or logical group of flows. This is where the depth comes from — each subagent can trace a full execution path without competing for context.

**Each subagent reads `/tmp/ak-doc-context.md` first.** This tells it what the documentation claims so it checks code against stated rules — not just observes behavior in isolation.

For each flow:

1. **Describe what happens step by step** — which files, which functions, in what order
2. **Flag anything you're uncertain about** — mark it explicitly with one of:
   - `[UNCERTAIN]` — you can't tell from the code alone
   - `[ASSUMPTION]` — you're making a reasonable guess based on patterns
   - `[UNCLEAR]` — the code is ambiguous or contradictory
3. **Call out cross-flow dependencies** — where one flow's failure could break another
4. **Rate your confidence** — calibrated against the repo health assessment. Lower confidence for areas with poor test coverage, cryptic naming, or missing docs.
5. **Cross-reference the Documentation Context** — does the code match what the docs and executable specs claim? Flag any divergence as `[UNCERTAIN]` and note which source contradicts the code.

**Also assign one dedicated subagent to invariants** — separate from user flow investigation:
- Check that schemas, types, and constants encoding business rules are actually enforced at runtime
- Look for constants that are defined but not used, types that are declared but bypassed, schemas that are imported but not applied
- Flag anywhere the machine-enforced spec and the actual code path diverge

### Output

Use the doc structure identified in Phase 1A. If no docs directory was found, create `docs/`.

Save to `{docs_dir}/assumptions.md` with this structure:

```markdown
# System Assumptions

> **Generated:** {date}
> **Repo health:** {one-line summary}

## Repo Health Assessment
{5-10 line calibration of codebase quality and what it means for trust levels}

## Flow 1: {Flow Name}

### What happens
{step-by-step walkthrough with file:line references}

### Assumptions
- [ASSUMPTION] {what you believe is true}
- [UNCERTAIN] {what you can't determine from code alone}
- [UNCLEAR] {where the code is ambiguous}

### Cross-flow risks
{where this flow depends on or affects other flows}

## Flow 2: ...

## Invariants

### What was checked
{schemas, types, constants, and test descriptions harvested in Phase 1A}

### Findings
- [ASSUMPTION] {invariant appears enforced — cite file:line}
- [UNCERTAIN] {invariant defined but enforcement path is unclear}
- [UNCLEAR] {machine-enforced spec and actual code path diverge}
```

After saving, tell the user:

**"Review this file. Correct anything I got wrong. Add context I'm missing — business rules, customer behavior, historical decisions. The more you correct now, the more bugs verification will find. Run `/assumption-killer verify` when ready."**

**Critical:** Do NOT proceed to verification. Do NOT fix anything. The human correction step between generate and verify is what makes this work. Without it, you're just auditing code — with it, you're testing beliefs.

---

## Step 2: Verify

### Prerequisites

1. Find the assumptions file — look for `assumptions.md` in the docs directory. If not found, ask the user for the path.
2. Read it completely.
3. Auto-detect high-risk assumptions — scan for `[UNCERTAIN]`, `[ASSUMPTION]`, `[UNCLEAR]` markers. These get the deepest investigation.

### Verification Process — 3-Phase Pipeline

Verification uses an extract→verify→compile pipeline. Agents write findings to files, not back into the main context. This prevents context overflow on large codebases.

**Architecture:**

```
Phase 0:  2-3 extractors (parallel)  →  N context files
Phase 1:  N verifiers    (parallel)  →  N finding files
Phase 2:  1 compiler     (serial)    →  1 final document
```

**Critical rules:**
- All agents use `subagent_type: general-purpose` (they need Write tool access)
- All agents run with `run_in_background: true`
- Each agent writes to its OWN files only — no shared writes
- Main context monitors progress via 1-line return summaries, never reads raw findings directly
- Temp file convention: `/tmp/ak-doc-context.md` (from Step 1, persists through Step 2), `/tmp/ak-context-flow-{N}.md`, and `/tmp/ak-verify-flow-{N}.md`

---

#### Phase 0: Extract Context

Pre-extract focused code sections so verification agents don't search the full codebase.

1. Count the flows in the assumptions file
2. Group flows into 2-3 batches for extraction (e.g., for 7 flows: A = flows 1-3, B = flows 4-5, C = flows 6-7)
3. Launch 2-3 **general-purpose** agents in parallel, one per batch

Each extraction agent receives:
- The full "What happens", "Assumptions", and "Cross-flow risks" sections for its assigned flows
- Instructions to extract ONLY the code sections referenced by those assumptions

Each extraction agent does:
1. For each assigned flow, identify the specific files and functions referenced in the assumptions
2. Read those files and extract the relevant code sections (function bodies, specific line ranges — not entire files)
3. Write one focused context file per flow: `/tmp/ak-context-flow-{N}.md`
4. Each context file should be self-contained: include the flow's assumptions at the top, followed by the extracted code sections with file:line annotations
5. Return a 1-line confirmation: `"Wrote context for flows X, Y, Z"`

**Wait for all extraction agents to complete before starting Phase 1.**

---

#### Phase 1: Verify

Launch N **general-purpose** agents in parallel — one per flow.

Each verification agent receives:
- The path to its pre-extracted context file: `/tmp/ak-context-flow-{N}.md`
- The path to the Documentation Context: `/tmp/ak-doc-context.md`
- The classification rubric (below)
- The confidence calibration from the repo health assessment

Each verification agent does:
1. Read its context file (focused, ~200-400 lines instead of searching the full codebase) and the Documentation Context
2. For **every** assumption in the flow, classify the result:
   - **Confirmed** — code does what the assumption says. Cite file:line.
   - **Incorrect (code bug)** — the code doesn't do what it should. Describe the bug, impact, and fix options.
   - **Incorrect (wrong assumption)** — the code is fine but the assumption was wrong. Explain actual behavior.
   - **Partially correct** — some aspects confirmed, others not. Be specific.
   - **When choosing between "code bug" and "wrong assumption":** cross-reference the Documentation Context. If a High or Medium trust source explicitly states the expected behavior and the code contradicts it → code bug. If the doc context is silent or Low trust → classify based on code patterns alone.
   - **For intent drift:** if the Documentation Context captures stated intent (from CLAUDE.md or equivalent) and the code diverges from it → flag as intent drift with the specific source cited.
3. For **high-risk items** (tagged `[UNCERTAIN]`, `[ASSUMPTION]`, `[UNCLEAR]`):
   - Trace the FULL execution path, including error handling
   - Check edge cases and boundary conditions
   - Look for related code that might contradict the assumption
   - Cross-reference with tests if they exist
4. Write findings to `/tmp/ak-verify-flow-{N}.md` as a markdown table (one row per assumption) with brief evidence
5. Return a 1-line summary: `"Flow N: X confirmed, Y incorrect, Z flags"`

**Wait for all verification agents to complete before starting Phase 2.**

---

#### Phase 2: Compile

Launch 1 **general-purpose** compiler agent.

The compiler agent receives:
- The paths to all finding files: `/tmp/ak-verify-flow-*.md`
- The path to the original assumptions file (for the header: date, repo health)
- The docs directory path for the output file
- The output format template (below)

The compiler agent does:
1. Read all `/tmp/ak-verify-flow-*.md` files
2. Read the assumptions file header (date, repo health summary)
3. Compile into `{docs_dir}/assumption-verification.md` using the output format below
4. Build the Verdict Summary table, count bugs/corrections, assemble all Flow-by-Flow sections
5. Return a summary: `"Written to {path}. X bugs found, Y assumptions corrected, Z high-risk items."`

Main context presents the compiler's summary to the user.

---

### Output

The compiler writes to `{docs_dir}/assumption-verification.md` with this structure:

```markdown
# Assumption Verification

> **Verified:** {date}
> **Input:** {path to assumptions file}
> **Repo health:** {summary from assumptions file}

## Verdict Summary

| Flow | Assumption | Status | Action Needed |
|------|-----------|--------|---------------|
| ... | ... | Confirmed / Incorrect (bug) / Incorrect (wrong assumption) / Partially correct | ... |

**Bugs found:** {count}
**Assumptions corrected:** {count}
**High-risk items investigated:** {count}

## Flow-by-Flow Verification

### Flow 1: {Flow Name} — {STATUS}

**Assumption:** {what was claimed}

**Verification:** {what you found, with file:line references}

**Impact:** {if incorrect — real-world consequence}

**Action:** {what to do about it}

---

## New Bugs Found

### Bug A: {Title}
**Severity:** Critical / High / Medium / Low
**Impact:** {user-facing consequence}
**Fix:** {concrete fix description}
**Priority:** P0-P3

## Corrections to Assumptions Doc
{list each assumption that needs updating with the corrected text}

## Prerequisites Discovered
{blocking issues found that must be addressed before planned work}
```

Intermediate files (`/tmp/ak-context-flow-*.md`, `/tmp/ak-verify-flow-*.md`) are working artifacts. They persist in `/tmp` for debugging but are not part of the final output.

**Critical:** Do NOT fix anything. Output the verification document only. The user decides what to act on and in what order.

---

## Step 3: Fix

### Prerequisites

1. Find the verification file — look for `assumption-verification.md` in the docs directory.
2. Read it completely.
3. Present the list of actionable items to the user and **ask which to fix**. Do not assume all items should be fixed. The user may want to defer some, skip others, or reorder priorities.

### Fix Process

Work through approved items in the user's chosen priority order:

1. **Bugs found** (Incorrect — code bug):
   - Fix the code
   - Update or add tests if test infrastructure exists for the area
   - Note what was changed

2. **Assumption corrections** (Incorrect — wrong assumption):
   - Update the original `assumptions.md` with corrected information
   - These are documentation fixes, not code fixes

3. **Action items** (Confirmed with action needed):
   - Address action items noted in the verification
   - May be code fixes, documentation updates, or new issues to track

After fixing, update the verification doc to mark each addressed item as `[RESOLVED]`.

### Output

Provide a summary:
- Code changes made (files and brief description)
- Documentation updates
- Items deferred or skipped (and why)
- Remaining open items

---

## Additional resources

- For the methodology and principles behind this workflow, see [methodology.md](methodology.md)
- For an example of what verification output looks like, see [examples/sample-verification.md](examples/sample-verification.md)
