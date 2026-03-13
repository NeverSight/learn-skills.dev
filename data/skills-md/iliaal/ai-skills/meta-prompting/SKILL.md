---
name: meta-prompting
description: >-
  Enhanced reasoning via slash commands (/think, /verify, /adversarial, /edge,
  /compare, /confidence, /budget, /constrain, /json, /flip, /assumptions,
  /tensions, /analyze, /trade) or natural language like "argue against" or
  "what could break". Use when asked to stress-test reasoning, find
  counterarguments, or apply structured thinking patterns.
---

# Meta-Prompting

Enhanced reasoning via `/commands` or natural language. Commands combine left-to-right: `/verify /adversarial`. Auto-trigger when context warrants — note which pattern applied.

## Patterns

**`/think`** | `/show` — Show reasoning step-by-step: decision points, alternatives considered, why each accepted/rejected. With `/think doubt`: after each step, flag what could be wrong and why before proceeding.

**`/adversarial`** | `/argue` — After answering, steelman the opposing case. 3 strongest counterarguments ranked by severity. Identify blind spots and unstated assumptions.

**`/constrain`** | `/strict` — Tight constraints: 3 sentences max, cite sources, no hedging. Override inline: `/constrain 5 sentences`.

**`/json`** | `/format` — Respond in valid JSON code block, no surrounding prose unless asked. Default schema:
```json
{"analysis": "", "confidence_score": 0-100, "methodology": "", "limitations": []}
```
Custom keys: `/json {keys: summary, risks, recommendation}`

**`/budget`** | `/deep` — Extended thinking space (~500 words) showing dead ends and reasoning pivots, then clearly separated final answer.

**`/compare`** | `/vs` — Compare options as table. Default dimensions: speed, accuracy, cost, complexity, maintenance. Custom: `/compare [dim1, dim2]`.

**`/confidence`** | `/conf` — Rate each claim 0-100. Flag below 70 as SPECULATIVE. Group by tier: HIGH (85+), MEDIUM (70-84), LOW (<70). Include assumptions made and rate each 1-10 on confidence.

**`/edge`** | `/break` — 5+ inputs/scenarios that break the approach. Code: null/empty, concurrency, overflow, encoding, auth bypass. Strategies: market conditions, timing, dependencies.
*Auto-triggers on: security, validation, parsing contexts.*

**`/verify`** | `/check` — Three phases: (1) **Answer** direct response, (2) **Challenge** 3 ways it could be wrong, (3) **Verify** investigate each, update if needed. Mark final as `VERIFIED ANSWER:` or `REVISED ANSWER:`.
*Auto-triggers on: architecture decisions, critical choices, "Am I right?"*

**`/flip`** | `/alt` — Solve without the obvious approach. What's the second-best solution and when would it actually be better? Override: `/flip 3` for top 3 alternatives.
*Auto-triggers on: architecture decisions where the "easy" answer may break at scale.*

**`/assumptions`** | `/presume` — Before answering, list every implicit assumption in the question/task. Then answer with assumptions explicit. The assumption list is often more valuable than the answer.
*Auto-triggers on: architecture reviews, ambiguous requirements.*

**`/premortem`** | `/postmortem` — Assume the decision/project has already failed. Work backwards: what caused the failure? List 3-5 failure modes by likelihood. Focus on systemic risks, not edge cases.

**`/tensions`** | `/perspectives` — Answer from two named opposing perspectives (e.g., security engineer vs. shipping PM). Focus output on where they *disagree* — that's where the real insight lives. Override roles: `/tensions [devops, security]`.

## Combos

**`/analyze`** = `/think` + `/edge` + `/verify` — Code reviews, architecture, security-sensitive work. Synthesize findings into a unified recommendation — don't just concatenate pattern outputs.
*Auto-triggers on: code review requests.*

**`/trade`** = `/confidence` + `/adversarial` + `/edge` — Trade ideas, position analysis, market thesis.
*Auto-triggers on: trade/position discussions.*

## Conventions

- Separate combined pattern outputs with `---`
- Keep core answer prominent — patterns enhance, not bury the response
- Accept new pattern definitions mid-conversation ("Add `/eli5` for explain like I'm 5") — apply for the session
