---
name: token-saver-cursor
description: Stretches Cursor's monthly included usage (Cursor models pool and other models pool) and on-demand spend while keeping output quality. Use when the user is running out of Cursor usage, sees high on-demand charges, asks when to use Auto, Composer, Max Mode or a frontier model, or asks to audit .cursor/rules, .cursorrules, AGENTS.md, .cursorignore or MCP servers for efficiency. Triggers include "usage limit", "included usage", "on-demand", "Max Mode", "token saving", "reduce cost", "context limit", "使用量", "トークン節約", "節約", "月間制限", "上限", "従量課金".
license: MIT
compatibility: Designed for Cursor (editor agent and CLI). The audit script needs Node.js 18+.
metadata:
  version: "0.1.0"
  agent: cursor
---

# Token Saver for Cursor

This skill has two jobs:

1. **Work lean** while it is active: follow the core rules below on every step.
2. **Tune the setup** when the user asks for an audit or setup, or keeps running out: run the workflow in "Audit and setup".

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

## Cursor specifics

Apply these on top of the core rules.

- **Two pools.** Paid plans include a monthly pool for Cursor's own models (Composer and others listed in the docs) and one for third-party models billed at their API price. Routine work on Auto or Composer leaves the other pool for hard tasks.
- **Max Mode multiplies cost.** It widens the context window and bills more per request. Suggest it only when normal context is genuinely too small.
- **Always-apply rules ride along with every request.** Keep them to a handful of lines.
- **What to suggest to the user** (they do these; you cannot):

| Situation | Suggest |
| --- | --- |
| Starting unrelated work | A new chat |
| Long chat on one task, context meter high | `/summarize` or a new chat with a short summary, before the hard limit |
| Routine work on a frontier model | Auto or Composer |
| Narrow question | `@` the specific files instead of the whole codebase |
| Large generated files show up in context | Add them to `.cursorignore` |
| Worried about the bill | Check the Spending tab; set an on-demand limit |

## Audit and setup

When the user asks to audit, set up, or cut usage, or keeps running out:

1. Run `node <this skill's directory>/scripts/audit.mjs --agent cursor` from the project root. It is read-only and prints warnings with fixes. Without Node.js, check the same items by hand using [references/levers.md](references/levers.md).
2. Report the findings ranked by expected savings, in a few lines each.
3. Propose concrete edits (rule types and globs, `.cursorignore`, MCP servers, model habits) from [references/levers.md](references/levers.md). Show the diff and apply only after the user agrees.
4. Offer to add the always-on snippet: skills load only when triggered, so the lean-work rules need a short permanent home. Save [assets/always-on.md](assets/always-on.md) as `.cursor/rules/token-discipline.mdc` with `alwaysApply: true` front matter (or append it to `AGENTS.md`), unless an equivalent rule already exists.

## References

- [references/levers.md](references/levers.md): rules, context, models, MCP and spending controls. Read before changing configuration.
- [references/facts.md](references/facts.md): plan and usage facts with sources and date. Read when the user asks about pricing or limits, and verify on the linked page if the answer matters.
- [references/budget.md](references/budget.md): how to pace a monthly pool that does not roll over.
