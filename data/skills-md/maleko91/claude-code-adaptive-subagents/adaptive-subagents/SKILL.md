---
name: adaptive-subagents
user-invokable: true
description: "Optimize token cost by routing Agent tool delegations to the cheapest sufficient model.\nTRIGGER when: about to use the Agent tool, any multi-step task, implementation, debugging, refactoring, search, exploration, test writing, code review, or any task that could be decomposed into subtasks.\nDO NOT TRIGGER when: single-line fix, trivial question, or user says 'no routing'."
---

# Adaptive Subagent Routing

## Quick Decision (apply to EVERY delegation)

**Default: Haiku.** Escalate only with reason.

1. Is this a **mechanical lookup**? (find files, grep for a string, list structure, check if something exists) → **Haiku**
2. Does it require **comprehension or writing**? (implement, refactor, test, debug, fix, analyze code, explain logic, summarize complex systems) → **Sonnet**
3. Is it **architectural, security-sensitive, or ambiguous**? → **Opus**

**Haiku boundary:** Haiku can *find* things and *format* things. It cannot *understand* or *reason about* code. If the task requires reading code and making a judgment, that's Sonnet.

If unsure between two tiers, pick the cheaper one. Escalate after failure, not before.

Before each delegation, output `**Routing to {Model}:** {brief reason}` on its own line.
When handling work inline, output `**Staying on {Model}:** {brief reason}` instead.

## When to Delegate vs Handle Inline

**Always delegate to a cheaper tier** — the 3x–15x cost savings always outweigh subagent overhead.

**Skip delegation** only when:
- The output is under ~100 tokens (one-liner answers, quick fixes already in context)
- The overhead of spawning a subagent exceeds the work itself
- The subtask needs the same model tier you're already on **and** context is already available

## Routing Rules

| Haiku (1x) | Sonnet (3x) | Opus (15x) |
|---|---|---|
| File search, grep, glob | Implementation, bug fix | Architecture, migration |
| Format/lint existing text | Refactor (< 10 files) | Security review |
| Check if file/string exists | Test writing | Ambiguous/conflicting scope |
| List files, directory structure | Debugging with stack traces | Multi-system design |
| Literal string replacements | Code generation (< 500 lines) | Performance analysis |
| | Summarize/analyze code logic | |
| | Rename across multiple files | |
| | Code review, explain code | |

**Escalate +1 tier:** ambiguous requirements, public-facing output, security-sensitive, production-critical, or 2 consecutive failures.
**Downgrade:** after planning completes, or remaining work is formatting/summarization.

## Cost Ratios

| Model | Relative Cost | Pricing |
|---|---|---|
| Haiku (1x) | Baseline | ~$1/M input, $5/M output |
| Sonnet (3x) | 3x Haiku | ~$3/M input, $15/M output |
| Opus (15x) | 15x Haiku | ~$15/M input, $75/M output |

A 10-delegation task routed to Haiku instead of Opus saves ~93% on those calls.

## Per-Subtask Routing

When a request involves multiple steps:

1. **Decompose first.** Break the request into a todo list of subtasks.
2. **Route each subtask independently.** Most items are cheaper than the overall task.
3. **Downgrade after planning.** If Opus produces a plan, implementation goes to Sonnet. Lookups and cleanup go to Haiku.

Example — "design and implement a caching layer":
- Plan the architecture → Opus
- Search for existing cache usage → Haiku
- Implement the cache module → Sonnet
- Write tests → Sonnet
- Update internal dev notes → Haiku
- Write public API docs → Sonnet (escalated: public-facing)

## Delegation

Choose **agent type by task** and **model by complexity** independently.

| Agent Type | Use When | Tools Available |
|---|---|---|
| `Explore` | Search, grep, read-only exploration | Read, Glob, Grep (no Edit/Write) |
| `general-purpose` | Implementation, edits, multi-step work | All tools |
| `Plan` | Architecture design, implementation planning | Read, Glob, Grep (no Edit/Write) |

Combine freely — `Explore` + `haiku` for file lookups, `general-purpose` + `sonnet` for implementation, `Explore` + `sonnet` for complex investigation, `Plan` + `sonnet` for straightforward design.

```
Agent(subagent_type: "Explore", model: "haiku", description: "...", prompt: "...")
Agent(subagent_type: "general-purpose", model: "sonnet", description: "...", prompt: "...")
Agent(subagent_type: "Explore", model: "sonnet", description: "...", prompt: "...")
Agent(subagent_type: "Plan", model: "sonnet", description: "...", prompt: "...")
```

Keep prompts scoped: relevant files, constraints, expected output format. The `description` parameter is required — use a short 3-5 word summary.

### Expected Output Formats

| Tier | Expected Output |
|---|---|
| Haiku | File paths, grep results, existence checks, formatted text |
| Sonnet | Code diffs, implementation files, test files, error analysis |
| Opus | Numbered plan steps, architecture decisions with rationale, risk assessment |

## Parallel Fan-Out

When a request contains independent subtasks, launch multiple subagents in a single message.

**Before splitting, build a dependency graph.** Does any subtask need another's output, or do they modify the same file? If yes, run them sequentially.

| Pattern | Parallel? | Why |
|---|---|---|
| Separate files, separate concerns | Yes | No shared state |
| Research + unrelated implementation | Yes | Read-only doesn't conflict with writes |
| Implementation + its tests | **No** | Tests depend on the implementation |
| Feature + docs describing that feature | **No** | Docs need to reflect what was built |
| Two features touching different modules | Yes | Independent code paths |
| Refactor + anything in same files | **No** | Refactor changes the baseline |

After all phases return, review outputs for conflicts before applying.

## User Overrides

If the user says any of the following, respect it for the current request:
- **"no routing"** / **"don't delegate"** — handle everything inline on the current model.
- **"use Opus"** / **"use Sonnet"** / **"use Haiku"** — force that tier for all delegations.

Log the override with `**Override:** {what the user requested}` and resume normal routing on the next request.

## Routing Log

After each routing decision, append a line to `routing.log` in the project root using the Bash tool:

```
echo "{model} | {agent_type or inline} | {estimated savings vs Opus, e.g. ~93%} | {brief task description}" >> routing.log
```

Log every `**Routing to**` and `**Staying on**` decision.

## Guardrails

- Max 2 retries per subagent, then escalate or ask the user.
- Max 5 sequential delegations per user request. No limit on parallel.
- Always review subagent outputs before applying — check for conflicts, hallucinated paths, and incomplete work.
- **Do NOT modify project files:** Never write routing rules to CLAUDE.md. Never add hooks to settings.json. This skill is loaded automatically by the plugin.
