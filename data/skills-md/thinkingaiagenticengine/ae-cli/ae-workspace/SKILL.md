---
name: ae-workspace
version: 1.1.0
description: "Manage AE AgentSpaces with ae-cli: resolve current workspace context, list or update workspace profiles, transfer files, configure Agent/MCP/Skill/knowledge-base capabilities, manage shared-space members, inspect activities, or scope automations and archived conversations. Use for the new Workspace product; legacy sandbox Workspace sync/model behavior is separate."
---

# ae-workspace

Use `ae-cli workspace` for AgentSpace operations. Here, `workspace_id` and `--workspace-id` always mean `AgentSpace.id`; they never mean the legacy sandbox `Workspace.id` or a filesystem directory name.

Before composing a workspace command, read [references/commands.md](references/commands.md). It contains the command matrix, mutation prerequisites, and file-transfer rules.

## Targeting

1. Prefer an explicit `--workspace-id` supplied by the user or returned by `workspace list`.
2. Inside a run, the CLI may use `TE_AGENT_CURRENT_AGENT_SPACE_ID`, derive the ID from the canonical `/spaces/actived/<id>/.conversations/...` runtime directory, or ask the server to resolve `TE_AGENT_CONVERSATION_ID`.
3. When both workspace and conversation are available, send both so the server can reject a scope mismatch.
4. Outside a run, if the target is unknown, run `workspace list` and select from real IDs. Never fall back to an account default.

Use `workspace current` to verify the resolved ID, space type, role, and capabilities before a multi-step mutation.

## Safety

- Read the latest record or revision before mutations that require `--version`.
- Treat capability and membership changes as `high-risk-write`; preview them with `--dry-run` and obtain explicit confirmation before passing `--yes`.
- Treat file and workspace deletion as `high-risk-write`.
- Shared AgentSpace provisioning is administrator-owned. `workspace create` creates only a personal AgentSpace.
- `ae-cli sync` and `ae-cli model` manage the legacy sandbox Workspace. In an AgentSpace runtime, use workspace capability commands instead.

## Related domains

- Memory: `ae-cli memory ...` uses the same strict AgentSpace target.
- Automations: use `ae-cli automation ... --agent-space-id ...` and follow the `ae-automation` Skill.
- Archived conversations: `ae-cli agent +find-archived-conversations|+restore-conversation --workspace-id ...`.

## Transition record

Transition status: transitional
Owning module: te-claude AgentSpace
Current transport: CLI-token REST under `/api/cli/workspace/v1`
Gateway target: TBD
Review after: 2026-12-01
Exit condition: equivalent stable Gateway capabilities exist; keep only commands that still add orchestration, file handling, safety, or stable typed output.
