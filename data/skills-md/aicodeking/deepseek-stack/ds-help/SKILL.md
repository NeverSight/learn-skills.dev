---
name: ds-help
description: "Pick the right deepseek-stack skill for a task and explain how the pack fits together. Use when the user asks which skill to use, what the pack contains, or types /ds-help."
---

# ds-help

Match the task to one skill, say why in one line, then run it.

## Pick a skill

| If the task is... | Use |
|---|---|
| Any coding session (always on) | ds-mode |
| Vague or high stakes | ds-sharpen, then ds-plan-loop |
| More than one file or step | ds-plan-loop |
| A new module or API shape | ds-blueprint |
| Any code change | ds-verify-loop |
| A bug with a cheap test target | ds-tdd |
| The same failure twice | ds-unstick |
| A long run or a full context | ds-context-reset, ds-ledger |
| A hard artifact where one try may miss | ds-best-of-n |
| Wide coverage, audits or races | ds-swarm |
| A review before merge | ds-review-loop, or ds-jury for several models |
| A risky change | ds-blast-radius |
| A new UI | ds-design |
| A UI that looks generic | ds-design-audit |
| Opening a PR | ds-pr |
| Watching CI and bots | ds-watch-pr |
| Change to merged PR, unattended | ds-ship |
| Same, but stop before merge | ds-ready |
| Someone else's PR or branch | ds-adopt |
| An old PR | ds-revive |
| Understanding code | ds-explain |
| Coming back after a long run | ds-catchup |
| Repeated agent mistakes | ds-lessons |
| Writing prose or docs | ds-unslop |
| Rules of thumb | ds-principles |

## Rules

- Recommend one skill. Name a second only if the task clearly has two phases.
- If no skill fits, say so and work with ds-mode alone.
