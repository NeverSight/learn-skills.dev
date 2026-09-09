---
name: experiments
description: Design, launch, analyze, and stop GrowthBook A/B tests, and search or record durable Learnings across experiments. Use for experiments, split tests, variations, hypotheses, sample size, guardrail metrics, SRM, chance to win, lift, declaring a winner, "what have we learned", "have we tested this before", or "record this learning". For bandits, identify them and direct the user to GrowthBook UI. For feature flags and rollouts, use feature-flags. For product analytics or metric catalog work, use analytics. For API key configuration, use gb-setup.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/gb-call *), Bash(sleep *)
---

# experiments

Domain router for GrowthBook experiments and the durable Learnings distilled from them. Each workflow lives in a reference file under `references/`. Read this router, pick the workflow that matches where the user is, then read that one file and follow it.

Experiments use the **v1 API** (`/api/v1/experiments`). When a workflow also touches a feature flag, the flag calls are v2 — the reference file spells out which is which.

All API calls go through the bundled helper. Under the Claude Code plugin install, it lives at `${CLAUDE_PLUGIN_ROOT}/scripts/gb-call` (the plugin root). Under `npx skills install`, it lives at `scripts/gb-call` relative to this skill's directory. Resolve that path once and substitute it whenever a reference example says `gb-call`; do not assume `gb-call` is on `PATH`. It reads `GB_API_KEY` from the environment first, then falls back to `~/.config/growthbook/.env` (written by **gb-setup**); environment variables take precedence.

## Pick a workflow

The experiment lifecycle runs brainstorm → design → launch → analyze → stop. `learnings` sits before design when checking prior knowledge and after analysis when evidence supports a durable conclusion.

These workflows target `type: "standard"` experiments. GrowthBook's REST API also supports multi-armed bandit experiments and separate Enterprise beta Contextual Bandit resources, but neither lifecycle is implemented here. If the request is about either kind of bandit, identify it accurately and direct the user to GrowthBook UI; do not apply the standard-experiment workflows to it.

| Read this | When the user wants to |
| --- | --- |
| `references/experiment-brainstorm.md` | Get ideas for what to test, grounded in past stopped experiments (proposes only) |
| `references/experiment-design.md` | Turn an idea into a launchable spec — hypothesis, variations, metrics, sample size (writes nothing) |
| `references/experiment-launch.md` | Create the experiment, prep or reuse the flag, wire the experiment-ref rule, and start it |
| `references/experiment-analyze.md` | Read results — refresh the snapshot if stale, then interpret (read-only) |
| `references/experiment-stop.md` | Stop a running experiment, optionally declare a winner and roll it out |
| `references/learnings.md` | Search and read prior conclusions, or create, update, and delete curated Learnings across experiments |

If the user has an idea but no hypothesis, start at `experiment-design`; it routes back to `experiment-brainstorm` when the idea needs grounding. If they hand you a name rather than an ID, `experiment-analyze` and `experiment-stop` both open with a resolve-by-name step.

## Methodology authority

`references/experiment-launch.md` was authored directly by GrowthBook's head of data science and is the **canonical voice** on statistical framing, hypothesis discipline, goal-metric counts, and guardrail requirements. When another reference file appears to disagree with it on methodology, follow `experiment-launch` and flag the drift. Do not resolve such a conflict by reasoning from general A/B testing intuition — GrowthBook's defaults are its own (Bayesian by default, no multiple-comparison correction on guardrails, sequential testing widens intervals).

This router deliberately carries no statistical guidance of its own. Interpretation rules live in the reference files.

## Shared conventions

- **Metrics must already exist.** No workflow here creates a metric. When one is missing, the user creates it in the GrowthBook UI first; the reference file says where.
- **Metrics must live on the experiment's datasource** or the experiment POST fails.
- **Don't mix `templateId` with `datasourceId` / `assignmentQueryId`** on create.
- **`winnerVariationId` is a variation ID string** (e.g. `var_abc123`) — not an integer index, not a variation name.
- **Resolve-by-name uses `q`,** which matches name, tracking key, description, and hypothesis. It rejects `!`, `~`, `^`, `>`, `<`, `=` with a 400 — send plain `field:value` tokens and free text. Filter bandits with `bandits`, never `type` (`type` is not a list param; `implementationType` is a different axis).
- **`result` is the recorded result and survives a restart,** so `result=won` can return a running experiment. Pair it with `status=stopped`.
- **`limit` caps at 100** on the experiments list.
- **Show users the experiment name and link `<host>/experiment/<id>`,** not raw ids alone.
- **An empty Learning corpus is not an empty experiment record.** Fall back to stopped-experiment history before concluding the team has no prior evidence.

## Read-only vs. write

`experiment-brainstorm`, `experiment-design`, and `experiment-analyze` never write — brainstorm and design are proposal-only and must not POST an experiment into existence, and analyze must not stop or modify one. `experiment-launch` and `experiment-stop` write experiment state. The `learnings` search/list paths are read-only; its create, update, and delete paths require explicit confirmation immediately before the write.

## Budget

GrowthBook rate-limits at 60 rpm. `experiment-brainstorm` fans out across paginated history and `experiment-analyze` polls for snapshot completion behind an explicit iteration cap with `sleep` between polls. Keep both caps — they're what stops a busy org from pinning the limit.

## Handoffs

- The **feature-flags** skill — anything about the flag itself: creating it, its targeting rules, its rollout, publishing its draft, cleaning it up after a test ships.
- The **analytics** skill — picking metrics out of the catalog before designing, or charting product data that isn't an experiment readout.
- **gb-setup** — when `gb-call` reports a missing or invalid `GB_API_KEY`.
