---
name: token-saver
description: Cuts token use and stretches usage limits (5-hour, weekly and monthly caps, credits, API spend) of any AI coding agent while keeping output quality. Agent-neutral; use it for agents without a dedicated token-saver skill (Gemini CLI, Windsurf, Cline, Roo Code, Kiro, Amp and others) or when several agents are in play. Use when the user hits or nears a usage limit, sees high cost, has a long session, or asks to audit instruction files, rules, MCP servers, models or reasoning effort for efficiency. Triggers include "usage limit", "rate limit", "token saving", "reduce cost", "context is full", "使用量", "トークン節約", "節約", "5時間制限", "週間制限", "月間制限", "上限".
license: MIT
compatibility: Works with any agent that supports Agent Skills. The audit script needs Node.js 18+ and knows Claude Code, Codex, GitHub Copilot, Cursor and OpenCode layouts.
metadata:
  version: "0.1.0"
  agent: any
---

# Token Saver

This skill has two jobs:

1. **Work lean** while it is active: follow the core rules below on every step.
2. **Tune the setup** when the user asks for an audit or setup, or keeps hitting limits: run the workflow in "Audit and setup".

For Claude Code, Codex, GitHub Copilot, Cursor and OpenCode, the dedicated `token-saver-<agent>` skills carry the exact commands and settings for that agent. This skill is the agent-neutral version.

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

## Levers every agent has

Find the local name for each of these in the agent's docs or its `/help`; [references/levers.md](references/levers.md) maps them for common agents.

| Lever | What to do |
| --- | --- |
| New session | Start fresh for unrelated work; old context is resent with every request |
| Compaction | Summarize a long session at a natural break, not mid-task |
| Model picker | Cheap model for routine work, flagship for hard problems; switch at task boundaries |
| Reasoning effort or thinking | Low for scoped edits, high only where reasoning pays off |
| Always-loaded instructions | Keep the instruction file short; move task-specific parts into scoped rules or skills |
| Tools and MCP servers | Disable what the task does not need; prefer CLIs |
| Subagents | Only for large read-only exploration, parallel independent work or a clean-context review; on a cheap model, returning conclusions only |
| Ignore files | Keep build output, logs and generated files out of indexing and context |

## Audit and setup

When the user asks to audit, set up, or cut usage, or keeps hitting limits:

1. Run `node <this skill's directory>/scripts/audit.mjs` from the project root. It detects Claude Code, Codex, Copilot, Cursor and OpenCode configuration (force one with `--agent <name>`, or all with `--agent all`), is read-only, and prints warnings with fixes. For other agents, check the levers above by hand.
2. Report the findings ranked by expected savings, in a few lines each. Always-loaded content usually matters most because it is paid on every request.
3. Propose concrete edits. Configuration and instruction files belong to the user: show the diff and apply it only after they agree.
4. Offer to add the always-on snippet: skills load only when triggered, so the lean-work rules need a short permanent home. Append [assets/always-on.md](assets/always-on.md) to the agent's always-loaded instruction file (for example `AGENTS.md`), unless an equivalent section is already there.

## References

- [references/levers.md](references/levers.md): where each lever lives in common agents, plus official sources. Read before changing configuration.
- [references/budget.md](references/budget.md): how to pace work against 5-hour, weekly and monthly windows. Read when the user asks when to use the expensive model or how to avoid running out.
