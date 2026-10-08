---
name: uxaudit
description: Run UX regression testing for a running app — combining static catalog checks (AI-slop, accessibility, Nielsen heuristics) with dynamic project-aware journey checks operated in pixel-only mode. Produces a unified editorial dashboard grouped into UX issues and UI risk signals, with cited sources, on-demand evidence, and improvement suggestions. Use this whenever you want to evaluate whether an app is understandable, polished, free of AI slop patterns, follows usability heuristics, AND completes its real user journeys end to end. Especially valuable after building a new app or iterating on UI changes.
argument-hint: "[<target>] [--url URL] [--lang ja|en] [--viewport mobile-sm|mobile|tablet|tablet-pro|desktop|desktop-lg|WxH] [--electron-app PATH] [--scenario-mode locked|refresh|hybrid] [--only categories] [--skip categories] [--yes|-y]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# UX Regression Testing For Apps

A skill for running UX regression testing on a running app through two reader-facing buckets — `UX issues` and `UI risk signals`. The dashboard is meant to be read through those two top-level buckets first; each check inside the `ux` band is also tagged with a `subtype` (`understand` / `decide` / `act` / `recover`) so reviewers can drill into where in the user's flow the failure happens. Every judgment-call check is anchored in published, publicly-verifiable research (NN/g, WCAG 2.2, ISO 9241-11/110, Krug, Norman, Cooper, Christensen, peer-reviewed studies). Self-evident anti-patterns (lorem ipsum, "Coming soon" stubs) ship without an academic anchor because they aren't judgment calls. The full allow-list and the "don't invent" rule live in `references/knowledge/sources.md`. Architecture, subagent isolation, and the L1→L4 evaluation model live in `references/concepts/architecture.md`.

## What this is

Most testing tells you whether code **works**. uxaudit tells you whether the result is **usable** and **wants-to-be-used**.

Two layers run side by side:

- **Catalog** — universal craft floor: AI slop fingerprints, WCAG, Nielsen heuristics, generic taglines. Project-agnostic, mostly stable.
- **Scenario** — whether THIS app's actual user journeys complete with continuity. Discovered from the project's own files; differs per project.

The catalog covers the floor of craft. The scenario layer covers journey continuity. Neither pretends to predict whether the product is the right product to build — that's a human question.

The dashboard presents findings in two reader-facing buckets:

- **UX issues** — problems that make the user struggle to understand, decide, or complete the task
- **UI risk signals** — templated, sloppy, or risky interface patterns that are likely to degrade the experience

Each check is also tagged with a `category` (derived from its directory layout — `accessibility`, `ai-slop`, `core-experience`, `desirability`, `usability`) and, when its band is `ux`, a `subtype` (`understand` / `decide` / `act` / `recover`). Reviewers should read the output through the two top-level buckets first; category and subtype are secondary axes the dashboard exposes for drill-down.

## How the dashboard reads (band first, then UX subtype)

The reader-facing hierarchy is:

1. **Band** (top level): `ux` vs `ui-risk`
2. **UX subtype** (only inside the `ux` band): `understand` → `decide` → `act` → `recover`
3. **Severity** (only inside the `ui-risk` band): `critical` → `major` → `minor`

The four UX subtypes are the canonical questions a reviewer cares about:

| Subtype | Question |
|---|---|
| **Understand** | Can the user tell what this is and what they are looking at? |
| **Decide** | Can the user choose the next action without excess judgment? |
| **Act** | Can the user move through the task and reach value? |
| **Recover** | Can the user read system state and recover when needed? |

An older rationale doc, `references/concepts/ux-layers.md`, frames the same territory using the Usability / Desirability / Retention vocabulary. That naming is kept only as conceptual prose — the check catalog itself has no `layer` field, only `band` + `subtype`. A "Retention" layer is explicitly out of scope: a single session cannot measure whether users come back.

## Argument semantics

Frontmatter `argument-hint` lists the surface flags. Their meanings:

| Argument | Default when omitted | Notes |
|---|---|---|
| `<target>` | cwd directory basename | Workspace label only — used for directory naming and the dashboard header. |
| `--url URL` | Auto-detected by the Project Locator (Step 2 of the playbook) reading `package.json` scripts, `vite/next/astro/nuxt` configs, `.env PORT`, `Procfile`, and Rails/Django/Phoenix defaults. If the declared dev server isn't running, the orchestrator offers to launch it in a background shell with user consent and stops it on exit. | Mutually exclusive with `--electron-app`. |
| `--electron-app PATH` | (none) | Path to an Electron entry point or package dir. L4 may evaluate it if the Judge can operate the app in pixel-only mode from the same session; otherwise it must escalate or skip honestly. |
| `--viewport <preset\|WxH>` | Scout's `primary_viewport` from `project-context.json`, falling back to `desktop`. | See viewport preset table below. Named presets set `isMobile: true` in Playwright; custom `WxH` does not. |
| `--viewports <list>` | (single iteration with `--viewport`) | Comma-separated. Produces one iteration per viewport with suffixed directory names (`iteration-N-mobile`, …). Mutually exclusive with `--viewport`. |
| `--lang ja\|en` | `en` | When `ja`, the orchestrator includes `Language: ja` in every Scout / Journey-Compiler / Judge / Reconciler / Proposer dispatch prompt body and passes `--language ja` to `aggregate.py`. Every `uxaudit-*` agent handles the language directive inline — translation contract is embedded in the agent system prompt. **Machine fields stay verbatim** (`check_id`, `source`, `pass_criteria`, `rationale`, file basenames, route paths) — only narrative fields are translated. L1/L2 catalog detector strings are English-only. |
| `--scenario-mode locked\|refresh\|hybrid` | `hybrid` | Controls whether the project's **scenario contract** (the Scout's `project-context.json`, treated as an evidence-based hypothesis the human has ratified) is reused or re-synthesized between iterations. `locked` = pure **regression run**: reuse the previous iteration's contract verbatim, do not re-run the Scout, give iter-to-iter comparison maximum stability. `refresh` = throw the contract away and re-synthesize from scratch (use after major IA/product changes when the old contract no longer represents the product). `hybrid` = keep the existing contract entries stable but let the Scout add new candidate journeys on top (the default — preserves comparability while letting coverage grow). See `references/concepts/discovery-and-scope.md` Part 0 for the framing rationale. |
| `--only <categories>` | (all categories) | Comma-separated category filter. Valid categories: `ai-slop`, `accessibility`, `usability`, `core-experience`, `desirability`. |
| `--skip <categories>` | (none) | Comma-separated category exclusion (same valid set as `--only`). |
| `--yes` / `-y` | (off — orchestrator pauses on disambiguation) | **Unattended mode.** Skip every confirmation prompt and pick safe defaults so the run completes end-to-end without human intervention. The only place the orchestrator currently pauses is **Phase 01 Step 3** (dev-server disambiguation / launch consent). Defaults applied with `--yes`: case C (multiple running) → first auditable+running candidate, sorted by `confidence` then `app_id`; case D (one declared, none running) → auto-launch via the existing background launch procedure; case E (multiple declared, none running) → first declared, then auto-launch. Cases F (zero declared) and "native platform without `--url`" still abort — there is nothing safe to assume. The orchestrator must log the auto-pick (`[uxaudit] --yes: auto-picked '<app_id>' (...)`) so the chosen target is visible in the run log. |

The iteration metadata records the actual scenario contract mode used:

- `scenario_mode`
- `scenario_source_iteration`
- `comparable_to_previous`

This is what lets History mode distinguish "same measuring stick, new fix attempt" from "the measuring stick itself changed."

Native macOS/iOS/Android apps and CLIs are out of scope: uxaudit is screenshot- and DOM-driven, so a target without a rendered DOM cannot be audited.

Alternate entry points the orchestrator may be asked to run directly (not slash invocations — these are post-audit views over an existing workspace):

```bash
python $UXAUDIT_DIR/scripts/generate_dashboard.py <workspace> --timeline
python $UXAUDIT_DIR/scripts/generate_dashboard.py <ws-a> <ws-b> --compare
python $UXAUDIT_DIR/scripts/generate_dashboard.py --library
```

`$UXAUDIT_DIR` is exported by orchestrator playbook Step 0 in plugin / `--plugin-dir` / standalone-symlink / dev-checkout modes — the resolution chain in [`references/playbook/00-env-setup.md`](./references/playbook/00-env-setup.md) walks `$CLAUDE_SKILL_DIR` → `$CLAUDE_PLUGIN_ROOT/skills/uxaudit` → `$HOME/.claude/skills/uxaudit` → common dev paths and verifies each candidate by looking for `SKILL.md`. The dashboard auto-detects mode (audit / history / compare / library) from inputs. See `references/modes/library.md` for the central registry, archiving, and `.uxauditignore`.

## Viewport presets

| Preset | CSS size | DSF | UA | Typical device |
|---|---|---|---|---|
| `mobile-sm` | 375 × 667 | 2 | iPhone | iPhone SE (catches designs that break at small widths) |
| `mobile` | 390 × 844 | 3 | iPhone | iPhone 13 / 14 / 15 / 16 (default mobile) |
| `tablet` | 820 × 1180 | 2 | iPad | iPad (10th gen), iPad Air |
| `tablet-pro` | 1024 × 1366 | 2 | iPad | iPad Pro 12.9" (catches designs that treat tablets as desktop) |
| `desktop` | 1440 × 900 | 1 | Mac | MacBook Air / Pro 13" (default) |
| `desktop-lg` | 1920 × 1080 | 1 | Mac | 1080p external monitor (catches `max-width: 1440` bugs) |

Named presets that claim to be "mobile" (`mobile-sm`, `mobile`, `tablet`, `tablet-pro`) set `isMobile: true` in Playwright — **without this the browser ignores `<meta viewport>` and lays out at 980 CSS px even inside a 390-wide context**, so media queries like `@media (max-width: 640px)` silently never fire. Both presets and custom `WxH` go through this logic.

For any device that isn't in the preset list, use `--viewport WIDTHxHEIGHT` directly (e.g. `--viewport 430x932` for iPhone Pro Max, `--viewport 744x1133` for iPad Mini). Custom sizes use DSF=1 and a desktop UA — they're a Responsive-Mode equivalent, not a device simulator.

4K monitors are intentionally NOT a preset: modern OS scaling (macOS Retina, Windows 150 %+) renders 4K displays at ≤ 1920 × 1080 CSS px, so a physical-4K preset would duplicate `desktop-lg`.

## Workflow (orchestrating agent)

**The orchestrator follows the literal step-by-step in `references/playbook/index.md` (which routes to the per-phase files `00-env-setup.md` … `06-aggregate-report.md`).** Read the index before running. The high-level shape:

| Step | What | Run by |
|---|---|---|
| 0 | Environment setup (plugin vs standalone, `NODE_PATH`, `UXAUDIT_LANG`) | Bash |
| 1 | Workspace setup + stale dev-server cleanup | Bash |
| 2 | **Project locator** — detect monorepo, enumerate dev server candidates (per sub-app), probe running state | Subagent (`agents/uxaudit-locator.md`, sonnet) |
| 3 | **URL resolution** — use `--url` if given, else pick a running candidate, else offer to launch in background with user consent. With `--yes` / `-y` (unattended mode): all consent / disambiguation prompts are skipped and the orchestrator picks safe defaults instead — see `references/playbook/01-discovery.md` for the per-case decision tree. | Bash + background shell |
| 4 | **Scout** — discover purpose, design system, journeys, viewport → `project-context.json` | Subagent (`agents/uxaudit-scout.md`, opus) |
| 5 | Resolve viewport (Scout's `primary_viewport`, abort on native warning) | Bash |
| 6 | Capture target | `capture.mjs` |
| 7 | Catalog L1/L2 | `run_all_checks.py` |
| 8 | Build compressed evaluation briefs from `project-context.json` | `generate_evaluation_briefs.py` |
| 9 | **Journey Compiler** — translate Scout's natural-language journeys into executable journey scripts (`<iter-dir>/journey-scripts/*.json`). One subagent dispatch covers all journeys. | Subagent (`agents/uxaudit-journey-compiler.md`, sonnet) |
| 10 | **L4 capture** — fan `capture_journey.mjs` out across `journey-scripts/*.json` at 4-way parallelism. Per-journey `evidence/{01..99}-*.png` + `steps.json` are written. Verdicts are NOT decided here. | `run_all_checks.py` (integrated) |
| 11 | **L3 + L4 Judge dispatch** (NO project context allowed) — L3 reads the static screenshot, L4 reads ONLY the per-journey `evidence/` (no browser, no curl, no `journey-scripts/`). All Judges batched in a single parallel `Agent` message. | Subagents (`agents/uxaudit-l3-judge.md`, `agents/uxaudit-l4-judge.md`, opus) |
| 12 | **Completeness gate** — `verify_completeness.py` blocks until every L3/L4 has a real verdict (recognizes the new `awaiting evidence-only judge dispatch` sentinel) | `verify_completeness.py` |
| 13 | **Result schema gate** — `validate_results.py` blocks on any malformed `result.json` | `validate_results.py` |
| 14 | Reconciler (optional) — narrow override of catalog fails when design system justifies | Subagent (`agents/uxaudit-reconciler.md`, sonnet) |
| 15 | **Proposer** — cross-check synthesis: cluster fails by root cause, produce ranked fix plan (`improvement-proposal.json`). First role allowed to see BOTH verdicts and project context. | Subagent (`agents/uxaudit-proposer.md`, sonnet) |
| 16 | Aggregate → `benchmark.json` (embeds proposal) | `aggregate.py` |
| 17 | Dashboard (renders Top fixes section from proposal) | `generate_dashboard.py` |
| 18 | Report verdict + top 3 fixes + **stop any dev server we started** | Orchestrator |

**Critical isolation rule:** L3/L4 Judge dispatches in Step 11 are physically sandboxed via their agent frontmatter tool allowlists — `uxaudit-l3-judge` has `Read, Write` only, `uxaudit-l4-judge` has `Read, Write, Glob` only. They physically cannot read `project-context.json`, the spec, the compiled `journey-scripts/`, or any project file because they have no Bash, no WebFetch, no Grep. The L4 split (Step 9 Compiler + Step 10 capture + Step 11 evidence-only Judge) is what makes "pixel-only at judgment time" mechanically enforceable. The Reconciler in Step 14 is the only place where intent and observation meet. See `references/concepts/architecture.md` for the rationale and `references/subagents/judge-output-format.md` for the canonical Judge output contract (kept as a reference document for check authors — the new `uxaudit-l3-judge` / `uxaudit-l4-judge` agents embed the contract inline in their system prompts).

`/uxaudit` is **autonomous from L1 through L4**. Step 12 blocks the pipeline until every Judge has actually run; Step 13 blocks if any verdict is malformed.

L4's pixel-only guarantee at judgment time is enforced by the capture/judge split:

- Step 9 (Compiler) is the only role with selector context — it reads HTML and writes JSON action scripts. It commits no judgment.
- Step 10 (`capture_journey.mjs`) executes those scripts and writes screenshots + `steps.json`. It commits no judgment.
- Step 11 (L4 Judge) reads only the screenshots, the action trace, and the compressed evaluation brief. It must NOT open a browser, run curl, or read `journey-scripts/`. Verdicts come from what is visible in the PNGs, with `steps.json` used only to disambiguate ordering and to know whether a screenshot represents a successful step or a captured failure state.

## Adding or modifying checks

Reading order when authoring a new check:

1. **`references/authoring/check-authoring.md`** — contract: when to add a check, the 10 manifest fields, classification (band/subtype) and method (L1–L4) choice, evidence-file policy, common mistakes, end-to-end checklist
2. **`schemas/check-manifest.schema.json`** — formal JSON Schema enforced by the pre-flight validator
3. **`references/authoring/adding-checks.md`** — L1 / L2 / L3 / L4 worked walkthroughs with the actual `check_lib` / `_target.mjs` API
4. **`scripts/validate_checks.py`** + **`scripts/test_checks.py`** — run after every edit

```bash
python scripts/validate_checks.py            # pre-flight: validate all check.json
python scripts/test_checks.py                # regression: L1 fixtures
python scripts/validate_results.py <iter>    # post-flight: every result.json
```

**Three safeguards work together** to prevent silent quality drift as the catalog grows:

| Safeguard | Catches | When it runs |
|---|---|---|
| **`validate_checks.py`** | Manifest drift (typo, wrong enum, missing implementation file, id↔path mismatch) | Pre-flight gate inside `run_all_checks.py` |
| **`test_checks.py`** | Logic drift in `detect.py` (threshold change silently breaks detection) | After every implementation edit; per-check fixtures under `checks/<cat>/<name>/fixtures/{pass,fail}/` |
| **`validate_results.py`** | Result drift after Judge dispatch (malformed `result.json`, missing `suggestion` on a fail) | Post-flight gate at Step 13 |

For L3/L4 specifically, every Judge subagent must produce result.json conforming to **`references/subagents/judge-output-format.md`** (the canonical contract for check authors). The `uxaudit-l3-judge` and `uxaudit-l4-judge` agent definitions embed the contract inline in their system prompts — authors of new L3/L4 checks read the reference document to understand the contract, then write a check-specific `prompt.md` that only enumerates the finding-type tags and the per-axis rubric. Keep evidence assets minimal: L3 usually attaches zero or one supporting screenshot/crop when it materially helps the reviewer; L4 attaches ordered journey waypoints.

## What this skill DOES NOT do

- **Predict retention** — only real users over time can show this
- **Replace human judgment** — checks surface signals; humans decide what matters
- **Test correctness** — that's the Evaluator's job (Playwright + assertions). This skill assumes the app works.
- **Test market fit** — the spec being built may be the wrong spec entirely. Human question.

## See also

**Runtime references** — the orchestrator loads these on-demand during a run:

| Reading | When to load |
|---|---|
| `references/playbook/index.md` | Read first when running an audit — phase map + isolation rule + failure modes. Then load only the phase file for your current phase. |
| `references/playbook/00-env-setup.md` … `06-aggregate-report.md` | One per phase. Load only the file for the phase you are executing. |
| `references/knowledge/category-baselines.md` | Scout on-demand when discovery sources D1–D4 are thin (category-baseline fallback) |
| `references/modes/feature-scope.md` | Only when `--scope feature` is set |
| `references/modes/library.md` | Only for `--library` / `--archive` / `--unarchive` post-audit views |

**Subagent definitions** — Claude Code loads these automatically when the orchestrator dispatches `subagent_type="uxaudit-<role>"`. The orchestrator does NOT re-inject them into prompt bodies:

| Agent file | Role | Model | Tools | Invoked at |
|---|---|---|---|---|
| `agents/uxaudit-locator.md` | Project locator (monorepo / dev-server enumeration) | sonnet | Read, Glob, Grep, Bash, Write | Phase 01 Step 2 |
| `agents/uxaudit-scout.md` | Project-context discovery | opus | Read, Glob, Grep, Write, WebSearch, WebFetch | Phase 01 Step 4 |
| `agents/uxaudit-journey-compiler.md` | NL journey → executable JSON | sonnet | Read, Write, Bash, WebFetch | Phase 03 Step 9 + 9.6 heal |
| `agents/uxaudit-l3-judge.md` | L3-vision Judge | opus | Read, Write | Phase 04 Step 11 |
| `agents/uxaudit-l4-judge.md` | L4-journey Judge (evidence-only) | opus | Read, Write, Glob | Phase 04 Step 11 |
| `agents/uxaudit-reconciler.md` | Catalog-vs-intent override | sonnet | Read, Edit, Write, Glob | Phase 05 Step 14 |
| `agents/uxaudit-proposer.md` | Root-cause synthesis + ranked fix plan | sonnet | Read, Write, Glob | Phase 05 Step 15 |

**Subagent reference documents** — read by check authors or for understanding contracts; NOT injected at dispatch time:

| Reading | Purpose |
|---|---|
| `references/subagents/judge-output-format.md` | Canonical L3/L4 `result.json` contract (embedded inline in `uxaudit-l3-judge` / `uxaudit-l4-judge`). Read this when authoring a new L3/L4 check's `prompt.md`. |
| `references/subagents/language-preamble.md` | Translation contract for `--lang ja` (embedded inline in every `uxaudit-*` agent). Kept as a reference for the aggregate scripts that still key off its enumeration of translated vs verbatim fields. |
| `references/subagents/heal-preamble.md` | Heal-request contract for validator-triggered re-dispatch (embedded inline in every `uxaudit-*` agent's "If re-dispatched" section). |

**Contributor references** — human-only documentation, NOT loaded at runtime. Do not cite from subagent briefs or playbook phase files:

| Reading | Purpose |
|---|---|
| `references/concepts/architecture.md` | Pipeline diagram, Scout/Judge/Reconciler isolation rationale, L1–L4 model, failure modes |
| `references/concepts/discovery-and-scope.md` | Journey discovery, whole-app vs feature-scope, first-time vs returning context |
| `references/concepts/experience-model.md` | Project-shaped UX contract: jobs, first value, key decisions, recovery expectations |
| `references/concepts/ux-layers.md` | Philosophy: what uxaudit measures (Usability + Desirability) and what it does not (Retention) |
| `references/knowledge/sources.md` | The "don't invent" rule + the allow-list of citation sources every judgment-call check is anchored in |
| `references/authoring/check-authoring.md` | Contract + checklist for adding new checks |
| `references/authoring/adding-checks.md` | L1 / L2 / L3 / L4 walkthroughs with the real API |

**Schemas + scripts** — machine artifacts, not prose:

| Artifact | Purpose |
|---|---|
| `schemas/project-context.schema.json` | Scout output schema (journeys, jobs, experience_model) |
| `schemas/check-manifest.schema.json` | check.json manifest schema, enforced by `validate_checks.py` |
| `schemas/check-result.schema.json` | result.json schema, enforced by `validate_results.py` |
| `schemas/improvement-proposal.schema.json` | Proposer output schema |
| `scripts/validate_project_context.py` | Validate Scout output (schema + linkage + coverage warnings) |
| `scripts/generate_evaluation_briefs.py` | Derive compressed Judge inputs from `project-context.json` |
