---
name: skill-architect
description: "Architect and audit portable agent skills for retrieval, predictability, progressive disclosure, evals, and repository gates. Use when the user asks to \"create a skill\", \"author a skill\", \"improve a skill\", \"review a skill\", \"refactor a skill\", \"compare skill rubrics\", \"distill a skill from sessions\", \"reconcile skill plans\", or \"teach skill authoring\"; when paths include `skills/<name>/SKILL.md`, `references/*.md`, helper scripts, evals, lockfiles, security manifests, or vendor adapters; or when mentions include skill-creator, Skill Development, skills.sh, trigger descriptions, completion criteria, leading words, or model/user invocation."
license: MIT
compatibility: macOS, Linux, or Windows; optional helper scripts require Python >=3.10
metadata:
  author: t4sh
  version: "0.1.3"
  tags: skill-authoring, skill-creator, skill-review, skill-rubric, agent-skills, multi-agent, claude, codex, openai, anthropic, antigravity, azure
---

# Skill Architect

Architect portable, high-quality agent skills from a vendor-neutral perspective. Use this skill as an independent planning, creation, review, refactoring, comparison, distillation, reconciliation, and teaching layer for any agent skill repository or runtime.

## Why this skill exists

Several high-signal upstream skills overlap while emphasizing different strengths:

| Source | Strength to preserve | Boundary to avoid |
|---|---|---|
| [Agent Skills **open specification**](https://agentskills.io/specification) | Canonical portable folder/frontmatter contract, progressive-disclosure directories, compatibility metadata, and validation baseline | Experimental fields such as `allowed-tools` are runtime-dependent and do not override a repository's accepted schema |
| [Anthropic **Skill Development**](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development) | Strong structure, trigger descriptions, progressive disclosure, validation checklist | Claude Code plugin-specific assumptions are not portable as-is |
| [Anthropic **skill-creator**](https://www.skills.sh/anthropics/skills/skill-creator) | Skill evals, baseline-vs-with-skill testing, trigger optimization, blind comparison, benchmark loops | Too heavy and Claude-specific to be the whole portable rubric |
| [OpenAI **skill-creator**](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | Codex/OpenAI compatibility, concise scaffold guidance, `agents/openai.yaml` metadata | Too OpenAI-specific to be the central standard |

Treat the Agent Skills specification as the portable syntax baseline, then use this skill as a quality and governance synthesis: it directs, plans, and reviews skill work at the architecture level, then routes into source-specific, project-specific, or repository-specific details only when needed. Concrete examples of this rubric in practice can be inspected across the `skills4sh` skills.

## Operating mode

Start with the current working context, not an upstream rubric. Check the CWD, project files, installed skill location, or repository convention first. Use the Agent Skills specification for portable baseline syntax; external rubrics inform content quality, while local rules win on accepted frontmatter fields, manifests, lockfiles, CI, and release gates. Do not add experimental `allowed-tools` unless the target runtime and repository schema both accept and enforce it.

Use this order:

1. **Classify the request** — choose `plan`, `create`, `audit`, `fix`, `refactor`, `compare`, `distill`, `reconcile`, or `teach` before deciding files or checks.
2. **Read the local standard** — find the CWD/project/repository authoring standard, agent instructions, check commands, and target skill before editing.
3. **Select the lens** — structure, quality/evals, vendor compatibility, distribution governance, or predictability.
4. **Run the predictability pass** — check invocation fit, branch uniqueness, information hierarchy, completion criteria, leading words, duplication, sediment, sprawl, no-op lines, and premature-completion risk before proposing edits.
5. **Plan the artifact** — decide the portable core, references, optional assets/scripts, vendor metadata, and validation path.
6. **Patch narrowly** — avoid churn-only rewrites; improve only the requested surface and directly related standard violations.
7. **Verify mechanically** — run repo checks or the closest local equivalent before handing back.

## Command modes

Use command-like modes when the user names one explicitly. If no mode is named, infer the closest mode from the request and state the assumption.

| Mode | Use when | Primary reference | Output |
|---|---|---|---|
| `skill-architect: plan` | Designing a skill, repo standard, gate, release, or migration before editing | [Portable rubric](references/house-rubric.md), [Naming and packaging](references/naming-and-packaging.md) | Scope, affected files, standards, verification path, rollback notes |
| `skill-architect: create` | Creating a new portable skill or scaffolding a skill folder | [Portable rubric](references/house-rubric.md) | `SKILL.md` plus linked references/assets/scripts and repo metadata plan |
| `skill-architect: audit` | Reviewing an existing skill or skill repo against the rubric | [Portable rubric](references/house-rubric.md) | Source-cited findings table, mechanical gate status, patch recommendations |
| `skill-architect: fix` | Applying narrow deterministic fixes that `validate_skill.py` can prove | [Portable rubric](references/house-rubric.md) | Dry-run patch list or applied safe fixes, then validation output |
| `skill-architect: refactor` | Improving an existing skill without changing its purpose | [Portable rubric](references/house-rubric.md), [Eval methodology](references/eval-methodology.md) | Trigger rewrite, reference split, routing cleanup, verification updates |
| `skill-architect: compare` | Comparing upstream skill-development, authoring, or creator rubrics | [Comparative study](references/comparative-study.md) | Evidence matrix, reusable rules, adoption/rejection decisions |
| `skill-architect: distill` | Reviewing one session, a session ID/path, or a group of sessions to extract a reusable skill | [Eval methodology](references/eval-methodology.md), [Portable rubric](references/house-rubric.md) | Session evidence map, reusable workflow, skill proposal or draft, eval plan |
| `skill-architect: reconcile` | Refreshing stale skill plans, audits, session-distilled proposals, or blocked skill backlogs | [Eval methodology](references/eval-methodology.md), [Portable rubric](references/house-rubric.md) | Updated status, drift decisions, retired/reopened items, next executable plan |
| `skill-architect: teach` | Explaining skill authoring standards or coaching a user/agent | [Portable rubric](references/house-rubric.md), [Vendor adapters](references/vendor-adapters.md) | Concise lesson, examples, and next-step exercise or checklist |

### Mode rules

- **Plan** before non-trivial multi-file changes, new gates, release work, or cross-vendor adapter changes.
- **Create** should start from concrete use cases, then draft the portable core before vendor metadata.
- **Audit** is read-only by default; present findings and wait unless the user also asks to patch.
- **Fix** is deterministic and dry-run-first; only apply `fix_skill.py --write` for safe mechanical edits, then run `validate_skill.py`.
- **Refactor** preserves intent; do not rename, split, or change behavior beyond the requested scope without calling it out.
- **Compare** must cite inspected sources and separate source facts from adoption decisions.
- **Distill** must separate session-specific events from reusable patterns, cite the session source, and propose a skill only from repeated or high-value behavior.
- **Reconcile** must verify whether prior plans, findings, and proposals still match the current context; retire fixed or rejected items instead of re-reporting them.
- **Teach** should explain the smallest useful rule, then give one concrete example rather than dumping the whole rubric.

## Skill architecture workflow

### 1. Gather concrete use cases

Capture only the details that determine structure:

- exact user phrases that should trigger the skill
- file paths, tools, APIs, or error messages that imply the skill
- repeated task shape: quick reference, workflow, router, review rubric, or deterministic helper
- target runtimes: Claude, Codex/OpenAI, Craft, Cursor, Antigravity, Azure/Copilot-style agents, or generic file-reading agents
- whether the skill needs references, assets, examples, or helper scripts

Ask one focused question if a structural choice is ambiguous. Otherwise infer from the CWD/project/repository pattern and state the assumption.

### 2. Separate portable core from adapters

The portable core lives in `SKILL.md` and linked references. Vendor details live in adapter sections or metadata files.

Use this split:

| Layer | Contains | Avoid |
|---|---|---|
| Portable core | trigger intent, workflow, checks, references, scripts/assets | one vendor's CLI assumptions as universal truth |
| Local convention | required frontmatter, versions, hashes, security files, README/plugin registry updates, or platform conventions | upstream defaults that fail local checks |
| Vendor adapter | OpenAI YAML, Claude plugin notes, Antigravity/Azure conventions, installation constraints | changing the portable workflow to fit one agent |
| Quality harness | eval prompts, baseline comparisons, review packets, pressure tests | claiming quality from prose review alone |

### 3. Draft with progressive disclosure

Keep `SKILL.md` focused on routing and immediate behavior. Move long comparisons, advanced examples, vendor matrices, and eval details to `references/`.

Minimum portable skill shape:

```text
skills/<skill-name>/
├── SKILL.md
├── LICENSE
└── references/          # only when detail would bloat SKILL.md
```

Add `assets/` or helper scripts only when they materially improve repeatability. Treat scripts as inert skill assets unless the local project or runtime explicitly allows executable helpers; document, link, hash, and security-scan them according to local conventions when available.

### 4. Review before patching

Prepare a compact audit packet before making non-trivial edits:

| Check | Evidence | Decision |
|---|---|---|
| Trigger description is concrete | `SKILL.md` frontmatter line | keep / patch |
| Invocation fit is justified | description, expected caller, context/cognitive load tradeoff | keep model-invoked / make user-invoked / add router |
| Branches are unique | description, command table, mode rules | keep / collapse synonym-only trigger branches |
| Information hierarchy is clean | section inventory | keep in `SKILL.md` / move to reference / split sequence |
| Completion criteria are checkable | every ordered step or command workflow | keep / sharpen / add done criteria |
| Leading words carry repeated concepts | repeated behavior terms and trigger language | keep prose / collapse to leading word |
| Pruning pass finds no sediment | duplicated, stale, no-op, or sprawling lines | keep / delete / disclose |
| `SKILL.md` is lean enough | word count | keep / split |
| References are linked | link check | keep / patch |
| Vendor assumptions are isolated | relevant section/file | keep / patch |
| Mechanical gates are available | repository scripts, CI, evals, or fixtures | run / note skipped |

Run a **predictability and pruning pass** before judging style or patching content:

1. **Invocation fit:** decide whether the skill should be model-invoked or user-invoked. Pay context load only when autonomous agent reach or cross-skill reach is necessary; recommend a router skill when many user-invoked skills create cognitive load.
2. **Description branches:** keep one trigger per real branch, remove synonym-only trigger duplication, and front-load strong leading words that also appear in prompts, docs, or code.
3. **Information hierarchy:** classify each major block as step, in-skill reference, or disclosed reference. Inline what every branch needs; move branch-only detail behind a context pointer.
4. **Completion criteria:** every ordered step should end with a checkable done condition. Sharpen vague criteria before splitting a sequence.
5. **Premature-completion risk:** if visible post-completion steps pull attention forward and the current criterion cannot be sharpened further, recommend a real context-boundary split.
6. **Leading words:** replace repeated explanatory prose with a compact pretrained concept only when it improves predictable execution or invocation.
7. **Pruning:** apply sentence-level relevance and no-op tests; remove duplication, sediment, and sprawl instead of polishing dead prose.

For behavior-shaping skills, add at least one forward test or prompt scenario. For any shipped CI, shell, or code — helper scripts, snippets, or workflow examples — review it for functional correctness and execute it against a fixture rather than vouching for it by reading. Reading alone routinely misses logic defects (wrong regex, broken cascade handling, crash-after-success) that a fixture run surfaces immediately; security-scanning and shape-checking do not cover correctness. An audit is incomplete until each embedded-code finding or pass includes a fixture command plus observed output, or an explicit skipped-risk note.

Use a bounded executable-surface triage before invoking a full code-review lens. Check whether the artifact has: fixture coverage for shipped scripts/snippets, fail-closed error handling, shell/runtime portability, pinned or cached external tools, path and quoting safety, network/credential boundaries, parser edge-case tests, and CI visibility. Report these as skill-architecture risks with evidence and a verification path; route algorithmic correctness, exploitability analysis, performance tuning, or large refactors to a dedicated code-review skill instead of expanding this skill's scope.

For eval and adapter claims, calibrate the finding to local policy and evidence quality: prompt-only eval catalogs are useful retrieval vectors but incomplete evidence for high-risk behavior claims, and missing vendor adapters are packaging defects only when the local repo requires them. Weak descriptions are deterministic failures only when the rule is portable and low-false-positive; in `skills4sh`, generic trigger-only wording such as `Use when creating skills.` fails mechanically.

For test vectors, harness setup, enumeration consistency, and severity calibration, use [Eval methodology](references/eval-methodology.md) and [Portable rubric](references/house-rubric.md) rather than expanding `SKILL.md`.

### 5. Make handoffs executable

When producing a plan, proposal, audit packet, or distilled skill spec for another agent or a future session, write for the weakest plausible executor. Include exact paths, relevant excerpts, local conventions, scope boundaries, verification commands with expected results, drift checks when source state matters, and STOP conditions for mismatches.

Record rejected findings or non-adopted patterns with one-line rationales so they do not return in the next audit or reconciliation pass.

### 6. Verify and hand off

Run the narrowest meaningful checks for the current working context. Prefer documented validation commands, CI gates, evals, fixture tests, hash checks, and security scans when present.

For `skills4sh` examples, the usual checks are:

```bash
npm run check:skill-standard
npm run check:drift
node bin/hash-check.mjs
npm test
```

Run a focused or full security scan when new files contain scripts, shell examples, credentials guidance, network examples, or other security-sensitive patterns.

Report exactly what passed, failed, or was skipped. Do not claim an eval, scan, or fixture test that was not run.

## Helper scripts

Optional helper scripts live under `assets/scripts/` so they ship as inert skill assets:

| Script | Use |
|---|---|
| [`assets/scripts/inspect_skill.py`](assets/scripts/inspect_skill.py) | Summarize a skill folder: files, frontmatter, body word count, linked references, and obvious missing pieces |
| [`assets/scripts/validate_skill.py`](assets/scripts/validate_skill.py) | Run a local portable-skill validation pass against one skill folder, with warning-only progressive-disclosure hints |
| [`assets/scripts/fix_skill.py`](assets/scripts/fix_skill.py) | Dry-run or apply conservative deterministic fixes to `SKILL.md`, then rerun validation |
| [`assets/scripts/scaffold_skill.py`](assets/scripts/scaffold_skill.py) | Create a starter skill folder using the portable rubric |

Read or run scripts only when the task needs deterministic inspection or scaffolding. Local validation commands and CI, when present, remain the source of truth.

### Deterministic checks vs judgment

Skill work splits across three layers — keep them separate and route each check to the layer that can decide it:

| Layer | Owns | Examples |
|---|---|---|
| Portable validator (`validate_skill.py`) | Minimal deterministic checks that hold inside one skill folder, no repo metadata or network | frontmatter present + `name`/directory match + kebab-case, description has concrete trigger detail, body within the hard size cap, `references/*.md` linked from `SKILL.md`, in-skill relative Markdown link targets, and same/cross-file Markdown heading anchors |
| Portable fixer (`fix_skill.py`) | Safe mechanical edits that require no taste or domain judgment; dry-run unless `--write` is explicit | frontmatter `name` normalization and insertion of missing `references/*.md` links in `SKILL.md` |
| Local binding gate (project CI) | Deterministic checks that depend on repo conventions; **binding and a superset** | file hashes, `skills-lock.json`, security manifests, doc-sync, semver — in `skills4sh`: `check:drift`, `check:guardskills`, `hash-check`, `npm test` |
| This skill's rubric (judgment) | What no script can decide | trigger *quality*, executable-surface triage, embedded-code *correctness* (review + fixture run), body altitude beyond the cap, vendor-isolation, narrative bloat |

The litmus test: **if a script can decide it, automate it; if it needs reasoning or taste, it stays in the rubric.** When a local binding gate exists, it wins over the portable validator on any overlap. The portable validator is deliberately narrow: it checks only facts visible inside one skill folder. Codifying a rule (for example a numeric size band) moves it from judgment toward the validator; treat that as the goal, not a loss.

## Reference files

| File | Load when |
|---|---|
| [references/comparative-study.md](references/comparative-study.md) | Comparing Anthropic, OpenAI, Matt Pocock, Obra, Azure, Antigravity, or other skill-development/authoring/creator patterns |
| [references/house-rubric.md](references/house-rubric.md) | Creating or reviewing a portable rubric; checking predictability, invocation fit, completion criteria, pruning, enumeration consistency, executable-surface triage, and severity calibration |
| [references/vendor-adapters.md](references/vendor-adapters.md) | Separating portable core instructions from Claude, OpenAI/Codex, Craft, Cursor, Antigravity, Azure, or future agent metadata |
| [references/eval-methodology.md](references/eval-methodology.md) | Testing triggers, building test-vector catalogs, setting up lightweight harnesses, comparing baseline behavior, or planning pressure tests |
| [references/naming-and-packaging.md](references/naming-and-packaging.md) | Avoiding slug collisions, deciding names, updating lockfiles/security manifests, and packaging repo updates |

## Non-negotiables

- Do not make a vendor-specific skill the portable rubric verbatim.
- Do not reinstall upstream `skill-creator` over an existing skill without checking provenance and collision risk.
- Do not ship loose summary-only descriptions; the description must include a concise capability clause and concrete trigger/use conditions.
- Do not add unlinked reference files.
- Do not add helper scripts without a concrete repeatability benefit and a validation path.
- Do not treat `skills.sh` popularity as quality proof; inspect source, tests, security posture, and portability.
