---
name: a11y-workflow
description: "Orchestrate the a11y accessibility lifecycle: scout → plan → critique → [perspective audit] → test → critique. Dual-mode: full lifecycle automation or step-by-step dispatch. Spawns specialist agents at depth-1 from the main session."
license: Apache-2.0
compatibility: Claude Code only — orchestrates Claude Code subagent spawning
metadata:
  author: zivtech
  version: "1.1.0"
---

# A11y Workflow Orchestrator

This skill sequences the accessibility lifecycle by spawning specialist agents from the main session. All agents run at depth-1 — no nested delegation.

## When to Use

- `/a11y-workflow full <target>` — run the complete plan-critique-test-critique lifecycle
- `/a11y-workflow step <step-name> <target>` — run a single step, user drives the sequence
- When reviewing or planning accessibility for a component, page, or feature

## Team Roles

| Role | Agent | Model | Job |
|------|-------|-------|-----|
| Scout | `a11y-scout` | haiku | File discovery, ARIA inventory, component type ID |
| Reader | `a11y-evidence-reader` | haiku → sonnet | Evidence digest + coverage note when artifacts exceed the inject budget (never opus) |
| Planner | `a11y-planner` | opus | Design accessibility before coding (9-phase) |
| Critic | `a11y-critic` | opus | Review ARIA patterns, focus management, state communication (8-phase) |
| Tester | `a11y-test` skill | n/a | Playwright keyboard tests, axe-core scans, baseline-url-scan sweeps (`--census` DOM heuristics, `--alt-snapshot`), keyboard-a11y-tester journey audits, virtual-screen-reader component SR assertions |
| Auditor | `perspective-audit` | opus | Deep 7-perspective review on escalated perspectives |

## Context Passing Between Agents

Each agent starts with a fresh context window. The main session bridges context between them:

- **Scout → Planner/Critic**: Scout returns a structured recon summary (~500-1500 chars). Inject verbatim into the next agent's prompt.
- **Planner → Critic**: Planner writes plan to `docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md`. Critic is spawned with file paths to the plan and source code — it reads both using its Read tool.
- **Critic → Perspective Audit**: Extract only the alarm levels and findings for escalated perspectives (~500-1500 chars). Inject into the perspective-audit prompt.
- **Test → Critic**: Inject structured test results summary (~500-1000 chars) into the critic prompt alongside source file paths. keyboard-a11y-tester artifacts (`trace.json`, `deterministic-findings.json`, `screen-reader-census.json`) typically exceed the inject budget — check against the threshold below; when they do, the orchestrator routes them through `a11y-evidence-reader` (below) rather than reading them wholesale — never the critic itself. The critic's Phase 0 covers any targeted re-read via the passed paths.
- **Evidence-reader delegation (the inject budget)**: when a step's evidence artifacts exceed **8K measured tokens (≈32KB on disk, chars/4)**, the orchestrator spawns `a11y-evidence-reader` (haiku extraction, sonnet if interpretation is needed, never opus) instead of reading the corpus itself, then hands the digest **plus the original artifact paths** to the critic/planner — which never spawns the reader itself (depth-1 holds). Findings cite digest handles; a targeted re-read routes back through the orchestrator, not a wholesale re-read. Rationale: 8K ≈ 2× the reader's own ≤4K-token digest ceiling (`a11y-evidence-reader.md`) — past that ratio delegation nets real compression. Tunable pending Phase 3 rows (`docs/plans/2026-08-24-context-utilization-plan.md`).
- **Size budget rule**: Output > 2K chars → write to file, next agent reads. Output ≤ 2K chars → inject into prompt. **Exception: the evidence-reader's digest.** The reader's `Write`/`Edit` tools are blocked by design, so its digest is exempt from this rule and injected whole regardless of size. If the digest opens with `BUDGET EXCEEDED`, the orchestrator — not the reader — writes it to a file verbatim and passes the path to the next agent; it never re-summarizes the digest to force it under budget.

## Skill-Improvement Capture (gate-exit discipline)

A passive collection surface (a side file nobody is required to populate) is not a mechanism — engagements that set one up have produced nothing from it. Capture works only when it is a required field of a step that already has to run, not an optional extra step of its own. Every "Return to User" gate exit in Mode 1 (Steps 5 and 9 below) and every single-step dispatch in Mode 2 carries this requirement: **before presenting findings, state one line** — either "No skill-improvement candidate observed this run" or a one-line candidate naming the source step and the recurring gap it points at (a pattern a scout/planner/critic/tester kept re-deriving, a routing table that under- or over-fired, a false positive or false negative worth a fixture). This is not a document to maintain between runs; it is output the gate exit cannot skip.

## Mode 1 — Full Lifecycle

Invocation: `/a11y-workflow full <target>`

The main session follows these steps sequentially. Do NOT spawn all agents at once — each step's output informs the next.

### Step 1: Scout
```
Agent(subagent_type="a11y-scout", model="haiku", prompt="
  Discover and inventory the accessibility state of: <target>
  Return: file paths, component type, existing ARIA attributes, estimated complexity.
  Keep output under 1500 chars — structured summary only.
")
```

### Step 2: Plan
```
Agent(subagent_type="a11y-planner", model="opus", prompt="
  Design accessibility for the following component.
  Scout recon: <inject scout output>
  Source files: <file paths from scout>
  Write the plan to docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md
")
```

### Step 3: Critique the Plan
```
Agent(subagent_type="a11y-critic", model="opus", prompt="
  Review this accessibility plan for gaps before implementation.
  Plan file: <path written by planner>
  Source files: <file paths from scout>
  Flag perspective alarm levels (LOW/MEDIUM/HIGH) for each of the 7 perspectives.
")
```

### Step 4: Perspective Audit (conditional)
Only if the critic flags any perspective at MEDIUM or HIGH alarm:
```
Agent(subagent_type="perspective-audit", model="opus", prompt="
  Deep review from escalated perspectives.
  Escalated perspectives and findings: <extract from critic output>
  Source files: <file paths>
")
```

### Step 4b: Role Audit — Design Mode (optional)
If user requests role-specific review, or the plan affects multiple team roles:
```
Agent(subagent_type="a11y-role-auditor", model="opus", prompt="
  Review this accessibility plan from team responsibility perspectives.
  Mode: design
  Roles: visual-design, ux-design (or all if requested)
  Plan file: <path>
  Source files: <file paths>
")
```

### Step 5: Return to User
State the skill-improvement-capture line (see above), then present the plan + critique + perspective audit + role audit findings. User revises and implements.

### Step 6: Test (after implementation)
Invoke the `/a11y-test` skill, routing by target kind:

- **Component/widget with (or needing) codified tests** → `npx playwright test` `.spec.js` + axe-core scans (the skill's primary path).
- **Baseline sweep across a list of URLs** (spot-check set, sampled route list, no `.spec.js` per page) → `references/baseline-url-scan.mjs`, with `--census` for DOM-census heuristics (empty paragraphs, autocomplete-absence, duplicate ids — reported under their own `census` key, never mixed into axe violations) and `--alt-snapshot` for a diffable per-page alt-text map. Detector output only, same as the axe-core lanes. The scanner's own detection coverage is regression-tested in `evals/suites/baseline-scan/` (fixture pair + `expected-rules.json` + `run_rig.sh`) — that rig verifies the scanner still catches its known defect classes, it does not substitute for running the scanner against the target under test.
- **Component announcement/name/reading-order behavior (pre-deploy, no URL)** → virtual-screen-reader assertions in the project's own unit suite or Storybook play functions, alongside the `.spec.js` lane — light-DOM components only (shadow roots are invisible to it), persistent-container pattern for live regions, never fake timers, never as keyboard evidence. See the a11y-test skill's component section.
- **Live URL + user journey** ("can a keyboard-only or screen-reader user complete X on this page?") → keyboard-a11y-tester: batch crawl for recon, then a driven `serve`/`step` session for interaction evidence. The main session drives the serve/step loop directly — it is a CLI, not an agent, so depth-1 is preserved. Calibration: batch-mode 4.1.3 findings are prompts to drive, never failures.

All lanes produce evidence for Step 7 — match each finding's evidence type against the a11y-test Verification evidence contract before treating a fix as verified.

### Step 6b: Role Audit — Code Mode (optional)
If user requests role-attributed findings, or findings need to be routed to specific team members:
```
Agent(subagent_type="a11y-role-auditor", model="opus", prompt="
  Review this implementation from team responsibility perspectives.
  Mode: code
  Roles: all (or specific roles if requested)
  Source files: <file paths>
  Test results summary: <inject test output summary>
")
```

### Step 6c: Digest Evidence (conditional)
If Step 6's test artifacts exceed the inject budget (see "Context Passing Between Agents" above):
```
Agent(subagent_type="a11y-evidence-reader", model="haiku", prompt="
  Question: <what the critic must adjudicate>
  Artifacts: <paths>
  question_source: orchestrator, /a11y-workflow Step 6c
")
```
Escalate to `model="sonnet"` when interpretation is genuinely needed (schema not covered by a recipe, conflicting artifacts, an evidence class that isn't obvious from the question, vision-mode verdicts). Never opus — a question needing opus-tier judgment is not an extraction question; hand the reader's handles to the opus-tier critic instead. Pass the returned digest **plus the original artifact paths** into Step 7 — the coverage note travels with it, and a targeted re-read routes back through the orchestrator, never a wholesale re-read of the corpus.

### Step 7: Critique the Implementation
```
Agent(subagent_type="a11y-critic", model="opus", prompt="
  Review this implementation for accessibility design issues.
  Source files: <file paths>
  Test results summary: <inject test output summary>
  keyboard-a11y-tester artifacts (if produced): <if Step 6c ran: the digest + coverage note from Step 6c, plus the original artifact paths. Otherwise: raw paths to trace.json / deterministic-findings.json / screen-reader-census.json>
  virtual-screen-reader results (if produced): <inject spoken-phrase log slices + tool version + test file paths — logs are small enough to inject directly>
")
```

### Step 8: Perspective Audit (conditional)
Same as Step 4 — only if critic flags MEDIUM/HIGH alarms.

### Step 9: Return to User
State the skill-improvement-capture line (see above), then present implementation critique + perspective audit findings. User fixes and re-tests.

## Mode 2 — Step Dispatcher

Invocation: `/a11y-workflow step <step-name> <target>`

User drives each step manually. The skill spawns the appropriate agent for the requested step. Each dispatched step's own return to the user carries the skill-improvement-capture line before its findings — the requirement is per gate exit, not per mode.

| Step Name | Agent | Model | What It Does |
|-----------|-------|-------|-------------|
| `scout` | a11y-scout | haiku | Discover files, inventory ARIA state |
| `plan` | a11y-planner | opus | Design accessibility (pass prior recon if available) |
| `critique` | a11y-critic | opus | Review plan or implementation |
| `test` | a11y-test skill | n/a | Run Playwright + axe-core; baseline-url-scan.mjs (`--census`/`--alt-snapshot`) for a URL-list sweep; virtual-screen-reader assertions for component announcement targets; keyboard-a11y-tester journey audit for live-URL targets |
| `read` | a11y-evidence-reader | haiku → sonnet | Digest evidence artifacts that exceed the inject budget into a contract-shaped digest + coverage note; never opus |
| `audit` | perspective-audit | opus | Deep perspective review (specify `--perspectives` to limit) |
| `roles` | a11y-role-auditor | opus | ARRM role-based review (specify `--roles` to limit) |

### Examples
```
/a11y-workflow step scout src/components/Modal.tsx
/a11y-workflow step plan src/components/Modal.tsx
/a11y-workflow step critique src/components/Modal.tsx
/a11y-workflow step audit src/components/Modal.tsx --perspectives keyboard,cognitive
/a11y-workflow step roles src/components/Modal.tsx --roles visual-design,ux-design
```

## Triage Mode (Cost-Sensitive)

For cost-sensitive runs, add `--triage` to critique steps:
```
/a11y-workflow step critique --triage src/components/Modal.tsx
```

This spawns the critic at Sonnet first, reads the structured output, and checks escalation signals:
- **CLEAN verdict** (no bugs found) → re-run at Opus (false positive risk)
- **ADVERSARIAL pattern** / ambiguous tradeoff → re-run at Opus (verdict calibration)
- **Low-confidence CRITICAL finding** → re-run at Opus (severity calibration)
- **No verdict emitted** → re-run at Opus (model budget exhausted)

Perspective audit escalation (MEDIUM/HIGH alarm) always runs at Opus regardless of triage mode.

## Benchmark Validation

Phase 1 benchmark (8 hard fixtures via Claude Code subagents, 2026-05-19):

| Tier | FLAWED (5) | ADVERSARIAL (3) | Total |
|------|-----------|----------------|-------|
| Opus | 5/5 PASS | 3/3 PASS (best-tier verdicts) | **8/8** |
| Sonnet-think | inherited from Haiku (pass) | resolved Haiku failures (acceptable verdicts) | 8/8 |
| Haiku | 5/5 PASS | 0/3 (wrong verdicts) | 5/8 |

Opus achieves best-tier verdict quality on every ADVERSARIAL fixture on the first pass. This is the measured basis for Opus-default routing.
