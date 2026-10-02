---
name: model-routing
description: "Codex · OpenCode · Orca routing: cost/time-efficient pairs, Astra question answering, independent review, dispatch, and escalation. Never invoked standalone."
---

# Model routing (shared)

Classify work by difficulty and latency.

For matt-design, use [Jev batch reports](references/jev-decision.md): strong-model candidates, one advisory report, no intermediate user gates.

## Execution tiers

| Tier | Codex / OpenCode | Claude Code | Use |
|---|---|---|---|
| Fast | gpt-5.6-luna / low | opus / medium | Trivial edits, mechanical transformations |
| Default | gpt-5.6-luna / medium | opus / medium | Small fixes, tests, mechanical conflicts |
| Background | gpt-5.6-luna / max | opus / medium | Bounded work where waiting is acceptable |
| Standard | gpt-5.6-sol / low | opus / medium | Moderate reasoning with latency constraints |
| Deep | gpt-6-astra / low | fable / high | Complex implementation, debugging, architecture |
| Escalated / review | gpt-6-astra / xhigh | Deep | Difficult unresolved reasoning; independent review |

- **Gemini priority.** For design-map implementation/support and OpenCode large-context slots, read [Gemini priority](references/gemini-priority.md): strongest available Gemini, maximum supported thinking/budgets, Codex continuation on quota exhaustion. Answers stay Astra; review follows the workflow.
- **Allowed Codex pairs.** Only the pairs above and the matt-loop overrides below for Codex execution, including Orca and fallback. Claude Code retains native pairs. Astra `xhigh` means extra high; legacy `-max` roles never mean Astra's literal `max`.
- **Answering is separate.** Matt-loop questions/decisions use only `matt-answer` (Astra low) or `matt-answer-deep` (Astra xhigh). Choose per question: low for explanations and local choices; xhigh for interacting constraints, uncertain causal analysis, or architectural tradeoffs. Clear hard questions start xhigh; reevaluate the next question and return to low when sufficient. Never put simple implementation on Astra just because its answer was discussed there.
- **Latency.** PR creation/status and deterministic commands use tools directly. No extra agent for each command. Background is opt-in by workload, not the default for trivial work. Measure latency, checks, and retries.
- **Matt-loop overrides** (including Orca/fallback): `matt-default` = gpt-5.6-luna / max; `matt-reviewer` = gpt-5.6-sol / high; `matt-reviewer-deep` = gpt-5.6-sol / xhigh. Other workflows retain explicit review routes.
- **Review.** Read-only, independent source inspection. Any Astra xhigh implementation/fix in the reviewed diff selects Sol xhigh for both axes and follow-ups; otherwise Sol high. Use ticket/dispatch history including retries, never parent/answer models. Unknown history: report it, default high. Metadata/status needs no review.
- **Execution ladder.** A concrete reasoning limit → next sufficient tier once, skipping Background when waiting is costly. Deep → `matt-deep-max` once, then handoff. Loops may cap roles or start hard strategists escalated. Do not walk every tier mechanically.
- **Context.** Changing effort requires another role/agent, carrying scope, findings, attempts, decisions, and constraints. Stop previous ownership; messages never change effort. Chunk oversized evidence on allowed pairs, then synthesize on Deep.

## Dispatch

- **Codex** — `spawn_agent` by pinned role (`matt-fast/default/batch/standard/deep/deep-max/reviewer/reviewer-deep/answer/answer-deep`; autocode `experimenter-default/deep`, `strategist/strategist-max`), `fork_turns: "none"`, required context and `ROUTED_EXECUTION=1`. Verify installed roles match the table; missing/stale roles require the explicit allowed pair, reported once.
- **Claude Code** — named loop agents pin model/effort; no model override. Fast/Default/Background/Standard map to its Default agent; Deep maps to its Deep agent.
- **OpenCode** — packaged roles under `~/.config/opencode/agents/`; verify provider support for the exact pair. Missing roles may use another mechanism enforcing that pair; otherwise stop dispatch.
- **Orca** — `worker-start --agent codex --model <exact model> --effort <exact effort>` from the table. Use `--retry-of <dispatch>` for reasoning retries; initial hard questions need no failed retry. Claude: `--agent claude --model opus --effort medium` or `--model claude-fable-5-1 --effort high`. OpenCode: `--agent opencode`, role and `ROUTED_EXECUTION=1` in prompt.
- **Unavailable route** — stop and report if no mechanism enforces the required pair. Never omit rejected flags, inherit defaults, or switch providers silently.
- **Explicit free-only mode** retains OpenCode `matt-free/free-fast`; missing agents stop rather than pay.

## Red flags

- Asking the user for effort, escalating merely because a task says “conflict,” or keeping xhigh for the next easy question.
- Astra for trivial implementation; unlisted Codex pairs; Gemini outside its designated slots; Grok fallback.
- Claiming a skill changed the parent session's model: routing selects workers/answer delegates, not the parent UI model.
