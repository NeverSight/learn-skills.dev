---
name: context-budget
description: Audit an AI agent's per-turn context window like a cost center — rank what actually eats tokens (system prompt, skills, memory, tool schemas, gate code) and fail CI when the agent gets fatter. Use when token costs climb on a long-running autonomous agent or you suspect context bloat.
when_to_use: A long-running or autonomous agent feels "token hungry", context is near the window limit, or you want a pre-commit/CI guard that fails when the always-loaded context grows past a budget. NOT for one-off single-prompt cost estimates.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [token-optimization, context-window, cost, ci, observability]
---

# Context Budget

Measure where an agent's per-turn tokens actually go, then hold the line with a budget.

## Overview

Autonomous agents accrete context. One more skill, one more memory note, one more
gate module — each cheap alone, together a tax paid on **every** request. Nobody
trims it because there's no ruler. `context_budget.py` is the ruler: point it at
the files loaded into context every turn and it ranks them by token weight, shows
each file's share, and returns a non-zero exit code when you blow the budget — so
it drops into CI or a pre-commit hook.

Real run against a production agent's gate layer: **214,588 tokens across 83 files**,
with a single 1,672-line quality gate eating **10.7%** of the whole window. You can't
fix what you can't see; this makes it visible.

## When to use

- Token/$$ cost is climbing on a long-lived agent and you don't know *which* part.
- You want CI to fail the build when the always-loaded context grows past N tokens.
- You're deciding what to prune and need weights, not vibes.

Not for: estimating one user prompt's cost, or counting a single API call.

## The method

1. **Enumerate what loads every turn.** System prompt, skills dir, memory files,
   tool schemas, any gate/middleware code injected into context. These are the
   paths you audit — not your whole repo.
2. **Run the audit.**
   ```bash
   python scripts/context_budget.py \
     ~/.agent/system_prompt.md ~/.agent/skills ~/.agent/memory \
     --budget 40000 --top 15
   ```
   Uses `tiktoken` (cl100k) when installed, else a calibrated chars/4 fallback —
   never hard-fails on a fresh box.
3. **Read the ranking top-down.** The heaviest file is your biggest lever. A
   10%-share file is where an hour of trimming pays back on every future request.
4. **Set a budget and wire it into CI.** The tool exits non-zero over budget:
   ```yaml
   # .github/workflows/context-budget.yml
   - run: python scripts/context_budget.py PATHS --budget 40000
   ```
   Now "the agent got fatter" fails the build instead of silently costing money.
5. **Trim the top, re-measure.** Move detail to on-demand references, delete stale
   memory, split a mega-gate. Re-run; the number is the scoreboard.

## Anti-patterns

- **Auditing the whole repo.** Only files that enter context every turn count.
  Test files and docs you never load are noise here.
- **Trimming by vibes.** Cut the measured top, not the file you happen to dislike.
- **Optimizing away autonomy.** For agents that need rich context to act on "just
  handle it", trim redundancy, not the capability. Weight, then cut carefully.
- **One-and-done.** Bloat regrows. The value is the *budget in CI*, not a single audit.

## Example

```
$ python scripts/context_budget.py ./skills ./memory --budget 20000
   tokens   share  file
    8,928    4.2%  ./skills/deploy/SKILL.md
    5,517    2.6%  ./memory/MEMORY.md
      ...
   34,110  100.0%  TOTAL  (128,402 chars, 41 files)

budget 20,000  [████████████████████████] 171%  → OVER BUDGET
  14,110 tokens over. Heaviest file is 8,928 tok — start there.
$ echo $?
1
```
