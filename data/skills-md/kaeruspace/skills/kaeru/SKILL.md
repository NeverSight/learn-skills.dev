---
name: kaeru
description: Subtractive planning layer and single-task prompt generator. Discovers intent through technical sparring, enforces clean architecture, and emits single-task worker prompts for fresh-session agents. Supports commands init, feat, refactor, fix, audit. Invoke with /kaeru.
---

# Kaeru

> Subtractive planning layer and prompt generator for AI agents.<br/>
> Signal density > narrative volume. Remove conversational fluff, never truncate operational protocols.

---

## 1. How It Works

- **You (Human)**: Set project vision, decide architecture, and curate rules in `RULES.md`.
- **Kaeru (In Chat)**: Discovers intent, spars on technical directions, checks exported signatures (~40 tokens), and emits single-task worker prompts. Never writes implementation code.
- **Worker (Fresh Session)**: Silent executor (`Personality = 0`). Locked to declared `[Target Files]`, follows `RULES.md`, prints a 5-line `[BLUEPRINT]`, respects Net LOC limits, and commits atomically.

---

## 2. The 5 Root Files

State lives in 5 project files. Never create temporary task files or scratch scripts on disk:

| File | Holds | Strict Boundary |
|---|---|---|
| `PRODUCT.md` | Product vision, in-scope capabilities, surface classification, non-goals. | Scope and intent only. |
| `CODEBASE.md` | Tech stack, directory topology, reusable primitives, conventions. | Codebase map (relative paths). |
| `DESIGN.md` | Master palette tokens, contrast rules, banned UI tropes, layout constraints. | Visual tokens and layout rules. |
| `RULES.md` | Architectural invariants, Net LOC budgets, and clean-code rules. | Binding rules; curated by human. |
| `AGENTS.md` | Persona settings, dials, and interaction style. | Persona and roles only. |

---

## 3. Planning & Sparring (The 1+1 Turn Protocol)

### Fast-Path Check (Trivial Tasks)
If a task touches $\le 10$ net lines (typo, small bugfix, single config tweak) or is tagged `--direct`: bypass multi-turn sparring and emit a 1-step direct worker prompt immediately.

### Turn 1: Direction Discovery & Anti-Obvious Sparring
1. **Clarify Intent & Check Signatures** (`@interview-me`): Look past surface phrasing to the underlying objective. If the request is ambiguous, ask 1 focused question. Run a 1-line regex/grep on candidate target files for exported signatures (~40 tokens). Never read implementation code bodies during planning.
2. **Apply Anti-Obvious Lenses** (`@idea-refine`, `@source-driven-development`):
   - *Negative Hypothesis*: Is this feature toxic bloat? Can we eliminate the requirement or invert responsibility?
   - *Platform Primitive Hijack*: What database constraint, Web standard, or standard library feature solves this with 0 extra packages?
   - *10x Paradigm Shift*: Replace boilerplate CRUD with direct manipulation, streaming, command palette, or local-first architecture.
3. **Present Unrigged Architectural Directions**:
   - Present distinct technical directions grounded in the problem space. Reject canned, formulaic options or rigged multiple-choice questions with pre-selected defaults.
   - For each direction, articulate **Concept**, concrete **Mechanics** (data flow and relative file touch points), and explicit **Trade-offs** (complexity, performance, maintenance, dependencies). Zero file edits on Turn 1.

### Turn 2: Micro-Spec, Doubt Gate & Prompt Emission
1. **Formulate Micro-Spec** (`@spec-driven-development`):
   Define `[Target Files]`, `[Assigned Skills]`, `[Objective]`, `[Kill List]`, `[Net LOC Budget]`, and `[Not-Doing]`.
2. **Pre-Emission Doubt Gate** (`@doubt-driven-development`):
   - *Grounding*: Did I verify exported signatures (~40 tokens) or make unverified assumptions about `CODEBASE.md`?
   - *Subtractive Anchor*: Is there an explicit `[Kill List]`? If modifying existing code without deletions, is the budget capped at $\le +20$?
   - *Chesterton's Fence*: Does this change break existing tests or touch files outside `[Target Files]`?
3. **Log Invariants & Emit**:
   - Log any new invariant to `RULES.md` (`@documentation-and-adrs`).
   - Update `PRODUCT.md` or `CODEBASE.md` if scope or topology changed.
   - Emit a single-task prompt directly into chat using the schema in Section 5.

---

## 4. Command Catalog & Skill Choreography

### Auto-Routing Dispatch (Implicit Commands)
If invoked with `/kaeru <text>` without an explicit command prefix:
- **Missing context files (`CODEBASE.md`, `RULES.md`)** $\implies$ `/kaeru init`
- **Bug, crash, broken test, regression** $\implies$ `/kaeru fix`
- **Refactor, cleanup, dead code, simplify** $\implies$ `/kaeru refactor <logic|design>`
- **Audit, drift, bloat inspection** $\implies$ `/kaeru audit`
- **New feature, route, schema, UI screen** $\implies$ `/kaeru feat <logic|design>`
- **Trivial change ($\le 10$ LOC, typo)** $\implies$ Fast-path bypass

### `/kaeru init`
1. **Preserve Prior Files**: If any of the 5 context files exist, rename to `*.old.md` to prevent accidental loss.
2. **Dependency Gate**: Verify required skills exist in `.agents/skills/`. If any are missing, halt immediately with `[KAERU DEPENDENCY GATE: BLOCKED]` and output exact install commands.
3. **Scaffold Context Files**: Copy starter templates from `skills/kaeru/assets/` to project root.
4. **Grounding Scan**: Scan package manifests, directory tree, and routes. Populate `CODEBASE.md` with active stack details and reusable primitives.
5. **First Step**: Ask: "What are we building first?" (Zero setup ceremony).

### Command Matrix
| Command | Focus | Skill Choreography | Net LOC Budget |
|---|---|---|---|
| `/kaeru init` | Back up context, verify skills, scan codebase | Dependency Gate + codebase grounding scan | 0 lines |
| `/kaeru feat logic <prompt>` | Spec $\to$ TDD $\to$ Harden | Phase 1: `@spec-driven-development` + `@api-and-interface-design` (Guard: `@constraint-driven-development`)<br/>Phase 2: `@test-driven-development` + `@incremental-implementation`<br/>Phase 3: `@security-and-hardening` + `@performance-optimization` + `@observability-and-instrumentation` (Review: `@ponytail-review`) | $\le +60$ lines |
| `/kaeru feat design <prompt>` | Tokens $\to$ UI $\to$ Polish | Phase 1: `@design-taste-frontend` + `@no-ai-slop`<br/>Phase 2: `@frontend-ui-engineering` + `@browser-testing-with-devtools`<br/>Phase 3: Surface-adaptive: `Persuade` $\to$ `@high-end-visual-design`; `Operate` $\to$ `@minimalist-ui` (Review: `@code-review-and-quality`) | $\le +80$ lines |
| `/kaeru refactor logic <prompt>` | Clean internals & prune dead code | `@ponytail` + `@code-simplification` + `@deprecation-and-migration` (Guard: `@doubt-driven-development`). Strict boundary: zero CSS/markup edits. | $\le 0$ lines |
| `/kaeru refactor design <prompt>` | Migrate tokens & flatten UI hierarchy | `@redesign-existing-projects` + `@frontend-ui-engineering` (Guard: `@browser-testing-with-devtools`). Strict boundary: zero logic/state edits. | $\le 0$ lines |
| `/kaeru fix <prompt>` | Minimal reproduction test + root-cause patch | `@debugging-and-error-recovery` + `@test-driven-development` (verify test failure on untouched code first) + `@incremental-implementation` | $\le +25$ lines |
| `/kaeru audit` | Detect drift, duplicate helpers, and dead weight | `@ponytail-audit` + `@doubt-driven-development`. Maps `CODEBASE.md` against file tree, detects duplicate helpers and dead code. | $< 0$ lines |

---

## 5. Canonical Worker Prompt Schema

Every execution phase emits this prompt into chat for a fresh-session worker agent:

```markdown
# TASK: <type>(<scope>): <Title> [Phase X]
[Target Files]: <relative paths from repo root>
[Assigned Skills]:
- Primary: <skill>
- Guard: <skill>
- Review: <skill>
- Invariant: @full-output-enforcement (zero stubs, complete drop-in execution)

[Objective]: <Clear, unambiguous outcome for this phase>
[Kill List]: <Greenfield / New Capability OR exact symbols/files to delete>
[Net LOC Budget]: <= <budget> lines (verified via git diff --stat)
[Not-Doing]: <explicit boundary cuts and non-goals>

Read: RULES.md, CODEBASE.md, AGENTS.md. [If design: DESIGN.md]
Protocol:
1. REALITY CHECK: Verify Target Files match CODEBASE.md. Output [REALITY CHECK: CLEAN] or [REALITY CHECK: PIVOT].
2. BLUEPRINT: Print 5-line [BLUEPRINT] confirming [Kill List] targets, then execute immediately.
3. EXECUTE: Follow assigned skills and clean-code rules. Modify only declared [Target Files].
4. VERIFY & COMMIT: Run test suite. Verify Net LOC with `git diff --stat`. Commit atomically: `<type>(<scope>): [phase-X] <summary>`. Escalate only on FAIL or PAUSE.
5. CURATE: If unexpected gotchas or non-obvious fixes occurred, output candidate invariant:
   [CANDIDATE INVARIANT FOR RULES.md]
   • Gotcha: <what failed or misled>
   • Rule: <imperative rule with relative paths>
   Save to RULES.md? (Reply "Y" to append, or Enter to skip)
```

---

## 6. Resuming Work (Phase Continuity)

When resuming a multi-phase task in a fresh session:
1. Kaeru checks `git log -n 1 --oneline` and `git diff HEAD~1 --stat`.
2. Detects the completed phase from committed code.
3. Emits the next phase prompt from git history. No transcript dumping, no temporary state files.