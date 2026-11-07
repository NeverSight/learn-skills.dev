---
name: token-saver-codex
description: Stretches OpenAI Codex (CLI, IDE extension, cloud) 5-hour and weekly usage limits or credits while keeping output quality. Use when the user hits or nears a Codex limit, sees fast usage in /status, has a long session, asks to audit or tune config.toml (model, reasoning effort, verbosity, compaction, tool output limits, MCP servers, profiles) or AGENTS.md, or asks how to use Codex more efficiently. Triggers include "usage limit", "rate limit", "5-hour limit", "weekly limit", "credits", "token saving", "reduce cost", "使用量", "トークン節約", "節約", "5時間制限", "週間制限", "上限", "クレジット".
license: MIT
compatibility: Designed for OpenAI Codex. The audit script needs Node.js 18+.
metadata:
  version: "0.1.0"
  agent: codex
---

# Token Saver for Codex

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

## Codex specifics

Apply these on top of the core rules.

- **Local and cloud share one allowance.** A cloud task is not free capacity; start one only when it saves real work.
- **Reasoning effort is the biggest per-task lever.** Well-scoped edits need `low`; debugging and multi-file changes `medium` or `high`; `xhigh` only for long, reasoning-heavy work.
- **AGENTS.md is capped** at `project_doc_max_bytes` (32 KiB by default). Past the cap Codex silently drops the rest, so keep it lean and put directory-specific guidance in nested AGENTS.md files.
- **What to suggest to the user** (they run these; you cannot):

| Situation | Suggest |
| --- | --- |
| Starting unrelated work | `/new` |
| Long session, same task | `/compact` at a natural break |
| Want to try an alternative without losing this thread | `/fork` |
| Routine task on a high effort or large model | `/model` and pick a smaller model or lower effort |
| Unsure how much is left | `/status`; add the 5-hour and weekly limits to the status line |
| Speed not needed | Leave fast mode off (it consumes more credits per request) |

## Audit and setup

When the user asks to audit, set up, or cut usage, or keeps hitting limits:

1. Run `node <this skill's directory>/scripts/audit.mjs --agent codex` from the project root. It is read-only and prints warnings with fixes. Without Node.js, check the same items by hand using [references/levers.md](references/levers.md).
2. Report the findings ranked by expected savings, in a few lines each.
3. Propose concrete edits to `~/.codex/config.toml` (or the project's `.codex/config.toml`) with the keys in [references/levers.md](references/levers.md). The config belongs to the user: show the diff and apply it only after they agree.
4. Offer to add the always-on snippet: skills load only when triggered, so the lean-work rules need a short permanent home. Append [assets/always-on.md](assets/always-on.md) to the project `AGENTS.md` or `~/.codex/AGENTS.md`, unless an equivalent section is already there.

## References

- [references/levers.md](references/levers.md): config.toml keys, commands and habits that affect usage, with a lean example config. Read before changing configuration.
- [references/facts.md](references/facts.md): limits, credits and pricing facts with sources and date. Read when the user asks about limits or pricing, and verify on the linked page if the answer matters.
- [references/budget.md](references/budget.md): how to pace work against 5-hour and weekly windows.
