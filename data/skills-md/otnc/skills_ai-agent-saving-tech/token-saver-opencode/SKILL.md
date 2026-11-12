---
name: token-saver-opencode
description: Stretches OpenCode usage, including OpenCode Go's 5-hour, weekly and monthly limits, an OpenCode Zen pay-as-you-go balance, and bring-your-own-key provider spend, while keeping output quality. Use when the user hits or nears an OpenCode Go limit, burns through a Zen balance, asks which model to use for cost, or asks to audit opencode.json (model, small_model, compaction, instructions, agents, MCP) or AGENTS.md for efficiency. Triggers include "OpenCode Go", "OpenCode Zen", "usage limit", "5-hour limit", "weekly limit", "balance", "token saving", "reduce cost", "使用量", "トークン節約", "節約", "5時間制限", "週間制限", "月間制限", "上限".
license: MIT
compatibility: Designed for OpenCode. The audit script needs Node.js 18+.
metadata:
  version: "0.1.0"
  agent: opencode
---

# Token Saver for OpenCode

This skill has two jobs:

1. **Work lean** while it is active: follow the core rules below on every step.
2. **Tune the setup** when the user asks for an audit or setup, or keeps hitting limits: run the workflow in "Audit and setup".

<!-- core-rules:start (synced from shared/core-rules.md by scripts/sync.mjs; edit the shared file) -->
## Core rules: work lean, stay correct

Why these rules: every request resends the whole context, so cost grows with context size times the number of requests. Output tokens cost several times more than input tokens. Rework costs the most of all. Cut the first two only in ways that never cause the third.

**Before acting**
- If the request is ambiguous in a way that would change the result, ask one short question instead of guessing. For multi-file or risky changes, outline the plan before editing.
- Stop exploring once you know enough to act. Do not survey the whole codebase for a narrow request.

**Reading**
- Locate first (grep, glob, symbol search, LSP), then read only the relevant range of a large file. Do not re-read a file that is already in context and unchanged.
- Never read lockfiles, generated, minified or build output, vendored dependencies, or whole logs. Search them instead.

**Tool output**
- Prefer summary forms: `git status -s`, `git diff --stat` before a full diff, `git log --oneline -n 20`, and `ls` of one directory rather than a recursive tree.
- Run the narrowest check that proves the change (one test file or case, a typecheck of the touched files) with quiet flags. Pipe long output through `tail -n 40` or `grep -E "FAIL|Error|error:"`. Run the full suite once at the end if it is needed.
- Send independent tool calls together in one turn, and make all edits to one file in one pass.

**Delegation: do it yourself by default**
- A subagent is not free. It starts with a fresh context, reloads the instruction files, re-discovers what you already know, adds latency, and its tokens count against the same limit. Its summary also drops detail you may need later.
- Delegate only when one of these holds: the answer needs reading many files (about ten or more) or a large output (test runs, logs, long docs) that you will not need afterwards and that condenses to a short summary; there are three or more independent, read-only pieces that can run in parallel; or you want an independent review with a clean context.
- Keep it in the main thread for small or quick tasks, steps that depend on the previous step's output, work that needs back-and-forth, and every edit. Keep writes in one thread and never let two agents edit the same file.
- When you delegate, use a cheaper model, give a precise brief (goal, paths, what to return, a length cap), ask for conclusions with `path:line` references, and do not redo the subagent's reading yourself.

**Answers**
- Lead with the result. Do not restate the request, recap what did not change, or dump a whole file when an edit or a `path:line` reference will do.
- Size the answer to the question. Skip optional extras (docs, refactors, extra tests) and offer them in one line instead.

**Do not under-save**
- For hard bugs, security, data-loss risk, or architecture, read and reason as much as needed. One correct attempt is cheaper than two cheap wrong ones.
- Never skip verification to save tokens. Make it targeted instead.

**Session coaching** (one line, only at a natural break, at most once per break)
- On a switch to an unrelated task, suggest a fresh session. On a long session about one task, suggest compacting with a focus hint.
- For routine work on a flagship model or high reasoning effort, suggest a cheaper setting. For a hard problem on a small model, suggest upgrading.
<!-- core-rules:end -->

## OpenCode specifics

Apply these on top of the core rules.

- **Model choice dominates on Go.** Each model has its own monthly dollar allowance and price, so the estimated number of requests per month differs by more than 100x between models. Routine work belongs on the cheap, high-allowance models; save the expensive ones for hard tasks.
- **Go limits are nested.** A 5-hour window allows 20% of the month and a week 50%, so a burst of heavy work stops at the 5-hour cap long before the monthly one.
- **Cheap models for side work, not more agents.** Let `small_model` handle titles and other light tasks. When the delegation rule above holds, point the `explore` subagent at a cheap model; otherwise do the work in the main session.
- **What to suggest to the user** (they do these; you cannot):

| Situation | Suggest |
| --- | --- |
| Starting unrelated work | `/new` |
| Long session on one task | `/compact` at a natural break |
| Routine work on an expensive model | `/models` and pick a cheaper one |
| Went down a wrong path | `/undo` instead of more correction turns |
| Hit a Go limit with work that cannot wait | Enable "Use balance" to fall back to a Zen balance, or switch to a free Zen model |

## Audit and setup

When the user asks to audit, set up, or cut usage, or keeps hitting limits:

1. Run `node <this skill's directory>/scripts/audit.mjs --agent opencode` from the project root. It is read-only and prints warnings with fixes. Without Node.js, check the same items by hand using [references/levers.md](references/levers.md).
2. Report the findings ranked by expected savings, in a few lines each.
3. Propose concrete edits to `opencode.json` (project) or `~/.config/opencode/opencode.json` (user) from [references/levers.md](references/levers.md). Show the diff and apply only after the user agrees.
4. Offer to add the always-on snippet: skills load only when triggered, so the lean-work rules need a short permanent home. Append [assets/always-on.md](assets/always-on.md) to the project `AGENTS.md` or `~/.config/opencode/AGENTS.md`, unless an equivalent section is already there.

## References

- [references/levers.md](references/levers.md): opencode.json keys, agents, commands and habits that affect usage, with a lean example config. Read before changing configuration.
- [references/facts.md](references/facts.md): Go and Zen limits and pricing with sources and date. Read when the user asks about limits or pricing, and verify on the linked page if the answer matters.
- [references/budget.md](references/budget.md): how to pace work against 5-hour, weekly and monthly windows.
