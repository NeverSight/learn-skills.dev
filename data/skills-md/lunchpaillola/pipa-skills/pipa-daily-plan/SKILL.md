---
name: pipa-daily-plan
description: "Use only when `pipa-daily-plan` is explicitly invoked or `pipa-define-work` delegates to it."
metadata:
  version: 0.1.1
---

# Pipa Daily Plan

Create a brief for one workday. Route recurring or scheduled setup to `pipa-manage`.

Follow this workflow. Keep a todo list to track each step.

## Workflow

1. Read [references/gotchas.md](references/gotchas.md) and [references/output-contract.md](references/output-contract.md).
2. Use the system date for today. For another date, use the user's request or calendar. Ask one question only if the target day is unclear.
3. Read `~/.pipa/profile.md` and `~/.pipa/CONNECTORS.md` when present. Use the profile for goals and preferences. Use mapped tools when present. For unmapped capabilities, use `composio-mcp` discovery to find tools for `~~project tracker`, `~~calendar`, and `~~code hosting`.
4. Verify live access before reading a source. Use `~~project tracker` and `~~calendar` as core sources. Use `~~code hosting` for code delivery. Use prior briefs, chat, email, or a knowledge base only to answer a specific planning question.
5. Gather due work, current or active work, priorities, dependencies, calendar commitments, and stated goals or profile preferences.
6. Find work the user can advance today. If due work is blocked, select an unblock step. If none exists, flag the block and continue to executable work.
7. Choose the main focus in this order: overdue or due-today work, current or active work, then the best ticket that supports the user's goals or preferences. Do not estimate task size or forecast capacity.
8. Write the read-only brief with [references/output-contract.md](references/output-contract.md). Show each exact external write and require separate approval before execution; report its result. End with a short sources line that names only the apps and material records used.
