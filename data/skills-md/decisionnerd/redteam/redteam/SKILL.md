---
name: redteam
description: >-
  Applied critical thinking and red teaming for decisions, plans, and strategies,
  plus RedTeam extensions (outside-view, invert, incentives, steelman, calibrate,
  ai-check, launch, rfc, misuse, reversibility, record, sequence, culture, ladder).
  Use when the user wants to challenge assumptions, stress-test plans, decisions,
  strategies, policies, designs, or arguments; run premortems, ACH, assumptions checks,
  frame audits, groupthink mitigation, base-rate forecasting, incentive gaming analysis,
  or AI output quality review. Works in chat or with a `.redteam/` directory.
  Not penetration testing. Implements The Red Team Handbook v10 — see lineage.md.
version: 0.2.0
argument-hint: "[command] [target]"
user-invocable: true
allowed-tools:
  - Bash(node scripts/*)
  - Bash(node */scripts/context.mjs*)
  - Bash(node */scripts/pin.mjs*)
  - Bash(node */scripts/init.mjs*)
license: Apache-2.0
---

Red teaming as applied critical thinking: challenge assumptions, surface hidden risks, and improve decisions before commitment.

**RedTeam** is the skill. It implements ***The Red Team Handbook*, Version 10** — successor to the defunct UFMCS v9.0 work, extended with decision science, product red teaming, and AI-quality checks. See [reference/lineage.md](reference/lineage.md). Not cybersecurity penetration testing.

Superset catalog: [reference/extensions-catalog.md](reference/extensions-catalog.md)

## Setup

You MUST do these steps before proceeding. `<skill-dir>` below is the directory containing this SKILL.md (the runtime usually shows it as the skill's base directory); run scripts from there, never from the user's project.

1. Run `node <skill-dir>/scripts/context.mjs` once per session. Keep cwd at the user's project. If the request names a specific decision, document, or file, append `--target <path>` to the command. If you've already seen its output in this conversation, do not re-run it. The script prints the project's decision context (`CONTEXT.md` when present) or reports `NO_CONTEXT_MD`. **If it reports `NO_CONTEXT_MD`:** divert into `reference/init.md` only when the user invoked `init`, or when they are starting a new decision review with no prior context and need structured capture. For scoped commands against material the user already provided in chat (a plan, memo, strategy, PRD, email draft), **do not block on init** — the user's input is the context. Offer `/redteam init` once as an optional follow-up to persist context. A missing CONTEXT.md must never block a scoped review.
2. If the user invoked a sub-command (`premortem`, `ach`, `challenge`, ...), you MUST read `reference/<command>.md` next. Non-optional. The reference defines the command's flow.
3. For any review targeting a document, plan, or codebase artifact, read the actual source material before analyzing. Do not critique from memory or summary alone.
4. Read `reference/principles.md` when performing any adversarial or evaluative command. It encodes the four core principles and ACT/GTM fundamentals. Skipping it produces shallow pushback instead of structured red teaming.

## Core principles (always apply)

- **Make the implicit explicit.** Surface assumptions, frames, and biases that are driving the conclusion but not stated.
- **Separate perception from interpretation.** What is observed vs. what is inferred?
- **Generate and evaluate alternatives.** A decision without rejected alternatives is incomplete.
- **Match tool to time.** Use quick reflex checks when time is short; use full technique sequences when the stakes warrant it.
- **Be the loyal opposition.** Challenge the thinking, not the person's worth. The goal is a better decision, not winning an argument.
- **Do not confuse red teaming with negativity.** Identify strengths and viable paths, not only flaws.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `init` | Setup | Capture decision context in CONTEXT.md and configure `.redteam/` | [reference/init.md](reference/init.md) |
| `challenge [target]` | Evaluate | Adversarial review: assumptions, logic, risks, alternatives | [reference/challenge.md](reference/challenge.md) |
| `critique [target]` | Evaluate | Structured critique of a document, plan, or proposal | [reference/critique.md](reference/critique.md) |
| `review [target]` | Evaluate | Pre-commitment decision gate before approval or launch | [reference/review.md](reference/review.md) |
| `premortem [target]` | Technique | Imagine failure, then work backward to prevent it | [reference/premortem.md](reference/premortem.md) |
| `ach [target]` | Technique | Analysis of Competing Hypotheses | [reference/ach.md](reference/ach.md) |
| `assumptions [target]` | Technique | Key assumptions check and sensitivity analysis | [reference/assumptions.md](reference/assumptions.md) |
| `devils-advocate [target]` | Technique | Structured devil's advocacy | [reference/devils-advocate.md](reference/devils-advocate.md) |
| `5-whys [target]` | Technique | Drill to root causes and hidden assumptions | [reference/5-whys.md](reference/5-whys.md) |
| `futures [target]` | Technique | Alternative futures analysis | [reference/futures.md](reference/futures.md) |
| `frame [target]` | Technique | Frame audit — what lens is shaping this view? | [reference/frame.md](reference/frame.md) |
| `groupthink [target]` | Facilitate | Design a groupthink-mitigation session | [reference/groupthink.md](reference/groupthink.md) |
| `ideate [target]` | Facilitate | Divergent thinking: generate alternatives | [reference/ideate.md](reference/ideate.md) |
| `converge [target]` | Facilitate | Convergent decision support: narrow options | [reference/converge.md](reference/converge.md) |
| `tools` | Reference | Browse Handbook v10 technique catalog + extensions | [reference/tools.md](reference/tools.md) |
| **Extensions** | | | |
| `outside-view [target]` | Extension | Base rates and reference class forecasting | [reference/outside-view.md](reference/outside-view.md) |
| `invert [target]` | Extension | Inversion — what would guarantee failure? | [reference/invert.md](reference/invert.md) |
| `incentives [target]` | Extension | Goodhart, perverse incentives, metric gaming | [reference/incentives.md](reference/incentives.md) |
| `ladder [target]` | Extension | Ladder of inference (Argyris) | [reference/ladder.md](reference/ladder.md) |
| `steelman [target]` | Extension | Steel-man before devil's advocacy | [reference/steelman.md](reference/steelman.md) |
| `calibrate [target]` | Extension | Confidence and evidence grading | [reference/calibrate.md](reference/calibrate.md) |
| `sequence [target]` | Extension | Tool-chain playbooks for decision types | [reference/sequence.md](reference/sequence.md) |
| `culture [target]` | Extension | Stakeholder worldview mapping | [reference/culture.md](reference/culture.md) |
| `ai-check [target]` | Extension | Meta-review of AI-assisted analysis | [reference/ai-check.md](reference/ai-check.md) |
| `launch [target]` | Extension | Product/feature launch readiness | [reference/launch.md](reference/launch.md) |
| `rfc [target]` | Extension | Technical RFC / ADR review | [reference/rfc.md](reference/rfc.md) |
| `misuse [target]` | Extension | Abuse-case and harm analysis | [reference/misuse.md](reference/misuse.md) |
| `reversibility [target]` | Extension | One-way vs two-way door classification | [reference/reversibility.md](reference/reversibility.md) |
| `record [target]` | Extension | Decision record / ADR artifact | [reference/record.md](reference/record.md) |

Reference-only (no dedicated command): [bias-catalog.md](reference/bias-catalog.md) · [ai-anti-patterns.md](reference/ai-anti-patterns.md) · [decision-record-template.md](reference/decision-record-template.md)

Plus management commands: `pin <command>` and `unpin <command>`.

### Routing rules

1. **No argument**: context-aware menu. If `NO_CONTEXT_MD`, lead with `/redteam init` as the top recommendation with one line on why. Otherwise recommend 2–3 highest-value commands based on what the user is working on, then show the full table. Never auto-run a command.
2. **First word matches a command** (table above or `pin` / `unpin`): load its reference and follow it. Everything after the command name is the target.
3. **First word doesn't match, but intent maps clearly** (e.g. "stress-test this plan" → `challenge`, "what could go wrong" → `premortem`, "base rates" → `outside-view`, "game the metric" → `incentives`, "is this AI analysis trustworthy" → `ai-check`, "launch checklist" → `launch`, "what playbook" → `sequence`): load that command's reference and proceed.
4. **No clear match**: general red team invocation. Apply setup, principles, and the user's full argument as context. Default to `challenge` flow unless a specific technique fits better — ask once if two techniques are equally plausible.

If the first word is `init`, or routing rule 3 maps to a from-scratch decision capture, `reference/init.md` owns the rest of the flow after setup.

## Pin / Unpin

**Pin** creates a standalone shortcut so `$<command>` invokes `$redteam <command>` directly. **Unpin** removes it.

```bash
node <skill-dir>/scripts/pin.mjs <pin|unpin> <command>
```

Valid `<command>` is any command from the table above. Report the script's result concisely.

## Output conventions

When writing artifacts to `.redteam/`:

- Reviews → `.redteam/reviews/<slug>.md`
- Session notes → `.redteam/sessions/<date>-<slug>.md`
- Use ISO dates in filenames. Slug from the target topic (lowercase, hyphenated).
- `/redteam init` runs `node <skill-dir>/scripts/init.mjs` to create `.redteam/` (`reviews/`, `sessions/`, `config.json`, `CONTEXT.template.md`) without overwriting existing files.

Always tell the user what was written and where. In chat-only mode (no `.redteam/`), deliver the full analysis in the response; offer to persist with `/redteam init` if useful.

## What this is NOT

- Not penetration testing, vulnerability scanning, or exploit development.
- Not instructions to deceive, manipulate, or socially engineer people.
- Not a license to be contrarian without substance. Every challenge should tie to evidence, logic, or an explicit assumption.
