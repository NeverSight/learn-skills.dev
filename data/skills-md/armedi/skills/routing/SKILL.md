---
name: routing
description: "Model selection, second opinions, and escalation for OpenCode subagents. Use before every subagent call."
---

Pick the agent by its description, then its row under **Models**. Always pass `model` as
`<id>#<effort>`.

## Handoffs

In every handoff, ask: "Return proof that the work satisfies the request."

A **spec** passes the **spec test**: a careful newcomer could finish from the prompt and tree
alone, making no design decisions. Send it to `general`, ending with: "Follow the spec. If its
approach doesn't fit the code, stop and report why."

A **brief** gives the outcome, constraints, and completion criteria, leaving design decisions to
the child. Send it to `specialist`, asking for objections with evidence.

A **second opinion** goes to a fresh `critic` whose maker differs from that of the model that
wrote the plan or diff under review.

## Models

Use these unless the user names another. Verify the ID in the model catalog. Maker means creator,
not serving provider. Only listed efforts are allowed.

**Benchmark** gives each row's score, with its USD cost per task in parentheses:
FrontierCode 2.0 (would a maintainer merge the change) from
[Cognition](https://cognition.com/frontiercode) and
[Artificial Analysis](https://artificialanalysis.ai/evaluations/frontiercode-2-0) (AA), or
OSWorld 2.1 offline (multistep desktop tasks) as reported by
[OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/).

| Model#effort | Maker | Agents | Benchmark | OpenCode model ID |
|---|---|---|---|---|
| deepseek#high | DeepSeek | `explore` | FrontierCode: Cognition 18.2% ($0.27), AA 16.8% ($0.35) | `acp-cmd/deepseek/deepseek-v4.1-flash` |
| deepseek#max | DeepSeek | `general`, `specialist` | FrontierCode: Cognition 19.3% ($0.38), AA 28.5% ($0.52) | `acp-cmd/deepseek/deepseek-v4.1-flash` |
| terra#high | OpenAI | `computer-use` | OSWorld: 68.7% ($0.51) | `acp-codex/gpt-6.1-terra` |
| sol#high | OpenAI | `critic` | FrontierCode: Cognition 34.8% ($0.65), AA 36.7% ($0.63) | `acp-codex/gpt-6.2-sol` |
| sol#max | OpenAI | `specialist` after escalation | FrontierCode: Cognition 39.0% ($1.03), AA 40.6% ($1.13) | `acp-codex/gpt-6.2-sol` |
| opus#high | Anthropic | Fusion orchestrator; `specialist` after escalation when OpenAI is excluded; `critic` of Sol work | FrontierCode: Cognition 34.5% ($2.42), AA 35.9% ($2.49) | `acp-claude/opus` |

## Escalation

- Before escalating, split the task and spec the parts that pass the spec test.
- A brief that fails on deepseek#max moves to sol#max, or to opus#high when OpenAI is excluded.
  Past that, report the blocker.
- A spec that fails on `general` gets a sharper spec, or goes to another agent as a brief.

## Failures

Provider error: retry once, then switch models. Usage limit: switch now and exclude that
provider's models.
