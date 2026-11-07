---
name: ae-automation
description: "Manage AE Agent and Agent team automations with ae-cli: create and edit schedules, enable or disable, run now, stop or retry executions, delete, inspect history and read execution results. Use for scheduled tasks and unattended recurring Agent work, from a local computer or an AE sandbox."
---

# AE Automation

See [command risks](references/command_index.md). Read [the command contract](references/cli.md) before writing or executing an automation. Use `ae-cli automation --help` and leaf help to discover flags.

1. Resolve the host and space. A local user signs in with `ae-cli auth login`; a sandbox uses its injected credentials. Pass `--agent-space-id` when the user identifies a space. Without a space, the server uses a bound sandbox space or the personal default. Show the resolved space when it matters.
2. Discover the automation with `automation list` and inspect `automation get`. Use the returned IDs; names are not unique.
3. For creation, select an Agent or team through the corresponding discovery commands. Match configuration to the target type. Preview writes with `--dry-run` when useful; the CLI shows a redacted request and asks the server to validate authentication, space, permissions, target state, fields, and idempotency without applying the operation.
4. Execute the requested operation. Deleting an automation or stopping an execution requires confirmation; use `--yes` only when the user already authorized that action. In a non-interactive shell, these operations fail immediately unless global `--yes` is present.
5. Read the returned run ID, then `automation runs result`. Report acceptance separately from completion. Use `--wait` only when the user needs the final outcome now.

Results are read from the server and work outside the sandbox. This skill does not read complete conversations or continue a chat. Never infer an output from a different execution sharing the same conversation.
