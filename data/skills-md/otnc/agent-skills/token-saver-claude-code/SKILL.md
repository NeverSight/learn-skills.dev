---
name: token-saver-claude-code
description: Stretches Claude Code's 5-hour and weekly plan limits (or API spend) while keeping output quality. Use when the user hits or nears a usage limit, sees high usage in /usage, has a long or slow session, asks to audit or slim down CLAUDE.md, rules, MCP servers, skills, subagents, hooks, model or effort settings, or asks how to use Claude Code more efficiently. Triggers include "usage limit", "rate limit", "session limit", "weekly limit", "token saving", "reduce cost", "context is full", "使用量", "トークン節約", "節約", "5時間制限", "週間制限", "上限に達した", "コンテキストがいっぱい".
license: MIT
compatibility: Designed for Claude Code. The audit script needs Node.js 18+ (already present wherever Claude Code runs).
metadata:
  version: "0.1.0"
  agent: claude-code
---

# Token Saver for Claude Code

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

## Claude Code specifics

Apply these on top of the core rules.

- **Subagents:** apply the delegation rule above. When it holds, the built-in Explore agent (read-only, runs on Haiku) suits codebase searches; otherwise pass `model: "haiku"` or `sonnet` for simple briefs. A fresh subagent reloads CLAUDE.md and has a cold cache; a fork inherits the conversation and reads the parent's cache, so a fork is cheaper to start when the task needs what you already know. Agent teams cost several times a normal session; never start one to save tokens.
- **Cache awareness:** a model switch, an effort change on most models, turning on fast mode, and connecting MCP servers mid-session make the next request re-read the whole history uncached. Suggest those changes only at task boundaries.
- **What to suggest to the user** (they run these; you cannot):

| Situation | Suggest |
| --- | --- |
| Starting unrelated work | `/clear` (free). `/rename` first if they may `/resume` later |
| Long session, same task, context large | `/compact <what to keep>` at a natural break. It costs one large request, so do not repeat it |
| Went down a wrong path | `/rewind` (or Esc twice) instead of arguing the model back; it reuses the cache |
| Routine edits on Opus or high effort | `/model sonnet` or `/effort low`/`medium` at the next task boundary |
| Planning then implementation | `/model opusplan` (Opus plans, Sonnet executes) |
| Unsure where usage goes | `/usage` (plan bars, attribution, cache stats) and `/context` |
| Complex change | Plan mode (Shift+Tab) before editing |

## Audit and setup

When the user asks to audit, set up, or cut usage, or keeps hitting limits:

1. Run `node <this skill's directory>/scripts/audit.mjs --agent claude-code` from the project root. It is read-only and prints warnings with fixes. Without Node.js, check the same items by hand using [references/levers.md](references/levers.md).
2. Report the findings ranked by expected savings, in a few lines each. Always-loaded content (CLAUDE.md, unscoped rules, MCP servers, skill descriptions) usually matters most because it is paid on every request.
3. Propose concrete edits, with the exact settings keys from [references/levers.md](references/levers.md). Settings and CLAUDE.md belong to the user: show the diff and apply it only after they agree. Note that CLAUDE.md edits take effect after `/clear`, `/compact` or a restart.
4. Offer to add the always-on snippet: skills load only when triggered, so the lean-work rules need a short permanent home. Append [assets/always-on.md](assets/always-on.md) to `CLAUDE.md` (project) or `~/.claude/CLAUDE.md` (all projects), unless an equivalent section is already there.

## References

- [references/levers.md](references/levers.md): every Claude Code command, setting, environment variable and hook that affects token use, with examples. Read before changing configuration.
- [references/facts.md](references/facts.md): plan limits, caching and pricing facts with sources and date. Read when the user asks about limits or pricing, and verify on the linked page if the answer matters.
- [references/budget.md](references/budget.md): how to pace work against 5-hour and weekly windows. Read when the user asks when to use the expensive model or how to avoid running out.
