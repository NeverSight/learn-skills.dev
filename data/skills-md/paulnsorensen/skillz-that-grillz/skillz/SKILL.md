---
name: skillz
description: >
  Add, improve, audit, self-update, wedge, or experiment on a skill or sub-agent definition so it
  runs predictably on Claude Code, Codex, OMP, and other Agent Skills hosts.
  Use for /skillz <add|improve|audit|self-update|wedge|experiment>, "improve this skill",
  "optimize this skill", "tighten this skill",
  "audit this agent", "new skill for X", "skill not triggering", "fix
  trigger rate", or "what in this skill should be a CLI". Do NOT use for
  CLAUDE.md or system-prompt edits, or for code changes that a cheese
  pipeline skill owns.
disable-model-invocation: true
argument-hint: "<add|improve|audit|self-update|wedge|experiment> [<path>|<name>]"
license: MIT
metadata:
  author: paulnsorensen
  dispatches-agents: audit and self-update only, when the host offers sub-agents
---

# skillz

Add, improve, audit, wedge, and self-update skill and agent definitions.
The product is a **predictable** definition: the same process on every run and on every harness.
Every lens asks one question of each line: *does this make the run more predictable, or is it sediment?*

The mode is the first word after the skill name.
`optimize` and `tighten` are aliases for `improve`.
Require a target only for `add`, `improve`, `audit`, and `wedge`.
`self-update` has no target.
Ask for the mode when it is missing.
Ask for a target when the mode requires one.

## Modes

| Mode | Target | Analytics | Writes | Product |
|---|---|---|---|---|
| `add <name>` | a new skill name | no | creates `skills/<name>/` | a registered skill that passes the rubric |
| `improve <path>` | a `SKILL.md` or agent file | no | edits the target | applied fixes + residual findings |
| `audit <path>` | a `SKILL.md` or agent file | yes | none | calibrated report |
| `self-update` | this skill | yes | `references/harness-layout.md` + this skill | research delta + applied fixes |
| `wedge <path>` | a `SKILL.md` | no | none | a `/wedge` handoff brief per offload candidate |
| `experiment` | an inspection or audit manifest, or public self-test | approved normalized cases only | isolated run directory | paired measurements and a private candidate patch |

For `experiment`, read `references/experiments.md`. Follow its workflow, not the shared audit protocol.
Ask which harness command and model the user wants before setup.
Use the installed `scripts/skillz-experiment.pyz`. Do not require a source checkout.

## Shared protocol

### 1. Read and classify

Read the target. Read a linked reference only when its stated trigger matches the run.
A full-package audit may explicitly read every file in the target package.
For `audit`, run `python3 <this-skill-directory>/scripts/inspect_skill.py <target>` before applying the rubric.
Use its JSON as objective package facts, not a fitness score.
Report a helper error without treating it as a successful audit.
Classify it as **agent** (`tools:` / `disallowedTools:` or an `agents/registry.yaml` entry) or **skill** (`name:` + `description:`).
Measure the body: bytes/4 after the frontmatter block; report `~N tok` against the 5k budget.
List the deploy targets the definition reaches (`references/harness-layout.md § Layout`).

### 2. Rubric

Score each lens.
Each row names the principle, the failure mode it catches, and a checkable test.
Read `references/anti-patterns.md` when a finding needs the expanded form.

| Lens | Principle → catches | Check |
|---|---|---|
| **Predictability** | Fixed protocol with checkable completion → «premature completion» | Every step ends on a done-condition an agent can verify. |
| **Invocation** | `description` = trigger conditions, front-loaded, third person → «workflow summary», «summary description» | Trigger phrases + "Do NOT use for"; no internal workflow; ≤1024 chars; first sentence carries the trigger. `references/description-optimization.md`. |
| **Portability** | Spec-core frontmatter plus additive Claude fields; user-only policy on every host → «Claude-only assumption», «sidecar missing», «`$ARGUMENTS` dependence» | `disable-model-invocation: true` pairs with `agents/openai.yaml`; args are parsed from the text after the skill name; no `${CLAUDE_SKILL_DIR}`; skills cross-referenced by `/name`; dispatch and GitHub ops name the contract before host syntax. Full matrix: `references/harness-layout.md`. |
| **Information hierarchy** | Disclose only what some runs skip; body ≤5k tok; references one level deep, each with a read trigger → «sprawl», «untriggered split», «`@file` force-load» | Relocation counts only when runs branch on the block and the `## References` entry names the trigger. `references/progressive-disclosure.md`. |
| **Leading words** | One pretrained word beats a restated triad → «duplication», «no-op weak word» | Collapse restatements; strengthen weak words (`be thorough` → `relentless`). |
| **Pruning** | Single source of truth; delete no-ops → «sediment» | No meaning in two places; no line the model obeys by default. Delete whole sentences. |
| **Deterministic offload** | Fixed computation runs as a bundled command, not regenerated prose → «inline script» | No step makes the model write or re-derive the same parse, count, filter, sort, or projection on every run; each bundled script has an invocation line and an output contract. Fix through `wedge`. |
| **Tool scoping** | Read-only / write-scoped / focused; use host enforcement when available → «prose-only constraint» | Claude skills use `disallowed-tools` to remove tools for the current turn. Their `allowed-tools` grants permission without prompts; it is not a deny list. Claude agents use `disallowedTools`. Report actual enforcement per mode and mark prose-only limits as degraded. Do not disable writes for `improve`. |
| **Context & fork** | Fork when output > ~500 lines or only a digest is needed → «monolithic output» | Fork matches size; a wrap-up signal exists; `model:` + `effort:` set on model-invoked skills, absent on user-only skills. |
| **Prompt quality** | Positive framing, why-over-what, one strong example, "What this never does" → «negation-heavy», «rules without reasons» | Judgment tasks use a scaffold, not always/never. `references/decision-frameworks.md`. |
| **Calibration** | Judgment agents tag confidence × severity → «judgment without calibration» | `<certain>` / `<speculative>` / `<don't know>`; don't-know never surfaces. |
| **Output format** | Summary first, tables for findings, clean-vs-issues signal → «no output format» | Format defined; summary and detail split. |
| **Usage** *(audit, self-update)* | Declared matches actual → «declared-vs-actual», «decay» | Declared tools are the used tools; error rate near baseline; usage not declining. |

### 3. Calibrate

Tag each finding with severity × confidence.
The kernel is `references/calibration.md`; the defaults:

- **Severity by lens** — Predictability, Invocation, Portability, Tool scoping, Calibration → `high`; Information hierarchy, Context & fork, Pruning → `high`/`medium`; Leading words, Deterministic offload, Output format, Usage → `medium`.
- **Confidence** — a cited line plus a concrete failure, a reference that does it right, or analytics data → `<certain>`; a checkable but unverified observation → `<speculative>`; a misread → `<don't know>`, dropped.
- **Re-derive** — re-read the target and re-derive each `<speculative>` finding once without the first pass. Drop it when it does not reproduce.
- Order by severity, then `<certain>` first.

## Mode: add

1. Confirm the name: kebab-case, ≤64 chars, directory name equals `name:`, and no collision in `skills/`, `~/.claude/skills`, `~/.agents/skills`.
2. Collect from the argument or ask: purpose in one sentence, ≥5 trigger phrases, anti-triggers, invocation policy (model-invoked or user-only), and the harness set.
3. Write the skill from `references/harness-layout.md § Template`.
   Keep the body ≤2k tok at birth.
   Create a reference only for a block that some runs skip.
   Add `agents/openai.yaml` when the skill is user-only.
   Set `model` + `effort` only when the skill is model-invoked.
4. Register the skill in its repo's index (`references/harness-layout.md § Registration`).
   A repo-local skill stays out of every global list; place it per `references/harness-layout.md § Repo-local skills`.
5. Run `improve` on the new file once, then the repo's deploy step when one exists (a dotfiles sync, `npx skills add`, or a copy into the harness skills directory).

Done means: the file exists, the repo index names it (or every repo-local host path resolves), the deploy step exits 0 when one exists, and the Invocation lens passes.

## Mode: improve

1. Run the shared protocol without analytics.
2. Apply every `<certain>` finding of severity medium or higher that does not change protocol semantics.
   Record each Deterministic offload finding as a residual for `/skillz wedge`; a new CLI is a redesign.
3. Put every `<speculative>` finding and every protocol-semantic change to the user as one approval question, with your recommendation for each.
   Apply the approved ones and record the declined ones.
   A delegated run returns these findings to its parent, and the parent asks.
   A PR body or a report is not approval.
4. Keep the target's voice and protocol semantics. Tighten; do not redesign.
5. Re-measure the body. Report before/after tokens and the residual findings.
6. Run the repo's deploy step when the target lives under a `skills/` or `agents/` tree that a sync distributes.
   Confirm the deployed copy matches the source; a vendored skill with the same name overwrites a local one (`harness-layout.md § Layout`).

Done means: every `<certain>` finding above `low` is fixed or recorded as an explicitly accepted residual, the user has approved or declined every item submitted for approval, the body is ≤5k tok, and the repo's quality gate exits 0.

## Mode: audit

1. Run `references/analytics-ceremony.md`. If DuckDB is absent, offer its opt-in raw-log fallback; never run it automatically.
2. Run the shared protocol with the Usage lens.
3. Emit the report below. Write nothing else.
4. Close with `Run /skillz improve <path> to apply.`

Done means: the report lists every surfaced finding with a cited line, and the below-bar count is stated.

## Mode: wedge

Find the work in the target that belongs in a bundled CLI, then write the brief that `/wedge` builds from.
The user runs `/wedge`; this mode writes no code and starts no build, because packaging is `/wedge`'s contract.

1. Read the target and its `scripts/`. Score the Deterministic offload lens only.
   For an agent file, report that `/wedge` packages only skills, then stop.
2. List each candidate with its line.
   A candidate is a fixed parse, validation, count, filter, sort, or projection that every run repeats.
   A bundled script without an output contract is also a candidate.
   Classification, recommendations, and user decisions stay in prose; they are never candidates.
3. Write each candidate's behavior contract: command name, inputs, output shape, ordering with tie-breaks, empty result, errors, and side effects.
   Name the prose that stays and the target line that will call the command.
4. Rank candidates by how often a run repeats the work, then by target line, ascending. With zero candidates, report `No offload candidates` and stop.
5. Emit the brief below. Close with `Run /wedge with candidate <n> of this brief.`
   When `/wedge` is not installed, add its install command: `npx skills add paulnsorensen/skillz-that-grillz --skill wedge`.

Done means: every candidate cites a line and has all seven contract fields.

```markdown
## skillz wedge: <name>

| # | Step (line) | Transformation | Command | Stays in prose |
|---|---|---|---|---|

### Candidate <n>: <command>
**Inputs** · **Output** · **Ordering** · **Empty** · **Errors** · **Side effects** · **Caller line**
```

## Mode: self-update

1. Check every source in `## Sources` of `references/harness-layout.md` for changes since its `Checked:` date; delegate to a fresh-context research agent when the host offers one.
   Cover frontmatter fields, discovery paths, invocation policy, argument handling, and body budgets for Claude Code, the Agent Skills spec, Codex, OMP, Pi, Zed, and the `skills` CLI.
2. Diff the digest against the reference.
   Update the matrix, the rules, the template, and the `Checked:` date.
   Record each rejected claim with its reason under `## Rejected`.
3. Run `audit` on this `SKILL.md`, then `improve` on it.
4. Run the repo's deploy step when one exists, then its quality gate.

Done means: `Checked:` is today, every source in the list was queried, and this skill passes its own rubric.

## Report

```markdown
## skillz <mode>: <name>

- Type: agent | skill · Invocation: model | user-only · Tools: <N allowed, N disallowed> · Body: ~N tok (before → after for improve)
- Harnesses reached: <list> · Findings: N surfaced, N below the bar

| # | Severity | Confidence | Lens | Issue (line) | Fix | Applied (yes / approved / declined) |
|---|---|---|---|---|---|---|

### Detail (per surfaced finding)
**What** · **Why** (the principle) · **How** (exact section) · **Reference** (a definition that does it right)

### Recommended hooks
Only for a rule that must hold every time; pick from `references/hooks-catalog.md`. Omit when none.

### Below the bar
N findings were `<don't know>` or trivial (not shown).
```

## What this skill never does

- `audit` and `wedge` never write; `improve` never redesigns; `add` never registers a skill whose description fails the Invocation lens.
- It never surfaces `<don't know>`.
- It never exempts itself; a finding against `skillz` is filed like any other.

## Gotchas

- Generic findings on simple skills: every finding cites a line or a named pattern.
- Over-indexing on missing `disallowedTools` when the host default already constrains the tool list.
- The `<speculative>` re-derivation is the first step skipped under time pressure and the one that catches the most false positives.
- `disable-model-invocation` alone leaves Codex free to auto-invoke; the sidecar is the fix, not more prose.
- A hook is for a rule that must hold every time, not for every finding.

## References

Read on demand:

- `references/harness-layout.md` — Portability lens fires, `add` (global or repo-local), or `self-update`; the frontmatter matrix, rules, template, sidecar, and sources.
- `references/analytics-ceremony.md` — `audit` and `self-update`; use the bundled engine for best-effort per-pack analytics.
- `references/raw-log-fallback.md` — DuckDB is absent and the user opts into a sampled, read-only Usage scan.
- `references/anti-patterns.md` — a finding needs the expanded failure mode.
- `references/progressive-disclosure.md` — Information hierarchy fires.
- `references/description-optimization.md` — Invocation fires.
- `references/decision-frameworks.md` — Prompt quality flags rigid rules on a judgment task.
- `references/hooks-catalog.md` — a finding needs 100%-of-the-time enforcement.
- `references/skill-usage.md`, `references/agent-orchestration.md`, `references/drift-regression.md` — the analytics packs.
- `engine/scripts/` and `engine/references/` — internal analytics ingestion, query, schema, conventions, and coverage; not a separate skill.
- `references/calibration.md` — the confidence × severity kernel.
- `references/experiments.md` — `experiment`; bounded GEPA search, case schema, isolation, and the frozen inspection contract.
