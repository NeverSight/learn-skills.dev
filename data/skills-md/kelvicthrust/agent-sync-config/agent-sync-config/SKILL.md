---
name: agent-sync-config
description: Set up or check shared native instructions, skills, context references, compatible Claude commands and agents, and MCP configuration for Codex and Claude Code in a project or explicitly selected global scope.
---

# Agent Sync Config

Use the bundled deterministic tool with Python 3.9+ to inspect current native
files and establish shared references. Installing this skill globally makes it available in any
repository; installation never selects execution scope. Keep the tool in its
installer-owned location. Never copy it into shared configuration or projects.

## Select the scope

Honor an explicit project/global request. Global operations always require
`--scope global` and omit `--project`. Never escalate a project request because
resources are missing, malformed, or conflicting.

For an ordinary setup/sync request without an explicit scope, run:

```sh
python3 <skill-directory>/scripts/agent_sync_config.py --project <repository> --json
```

Existing local `.agents`, `.claude`, `.codex`, `AGENTS.md`, `AGENTS.override.md`,
`CLAUDE.md`, or `.mcp.json` selects project scope. Git/worktree discovery resolves
the root; outside Git, use the explicitly selected/current directory.

A fresh noninteractive request returns exit code 2 and `selection_required: true`
without writes. Ask whether to initialize this project or synchronize global
configuration, wait for the choice, then use the explicit scope. Cancellation
makes no changes. If the request already specifies the scope, invoke it directly:

```sh
python3 <skill-directory>/scripts/agent_sync_config.py --scope project --project <repository>
python3 <skill-directory>/scripts/agent_sync_config.py --scope global
```

## Check and share

For checks, planning mode, or read-only environments, audit without writes:

```sh
python3 <skill-directory>/scripts/agent_sync_config.py check --scope project --project <repository>
python3 <skill-directory>/scripts/agent_sync_config.py check --scope global
```

Unscoped check audits project scope. `--dry-run` previews changes without writes.
Reports inventory resources with source/destination, disposition, and compatibility;
name the scope and paths; global reports have no project target. Exit
codes are 0 for success, 1 for conflicts/check drift, and 2 for invalid input,
scope selection, or filesystem failure. Read the report before claiming success.

Project instructions live in AGENTS.md; CLAUDE.md imports them. Global shared
instructions live in ~/.codex/AGENTS.md, with ~/.claude/CLAUDE.md referencing them.
Skills live in .agents/skills (or ~/.agents/skills globally); Claude uses relative
per-skill links. Do not add duplicate .codex/skills entries. Reference existing
context documents from the shared instructions; create no custom context store.

Instruction and skill edits are shared through references immediately. Explicit
sync adopts compatible new ordinary skills or repairs references. Preserve
conflicting files, external dependencies, native overrides, system skills,
provider-managed skills, plugin settings, and unrelated hooks.

## Claude-first resources

Ordinary sync performs supported sharing and adaptation automatically. Do not add
`convert`, `--reference-claude`, replacement flags, new state, or custom roots.

- Portable skills move with supporting files to `.agents/skills` and receive Claude
  links. Simple instruction-only commands become valid shared skills; the legacy
  command is removed only after its replacement and Claude link are verified.
- Commands with arguments, shell preprocessing, execution controls, plugin
  variables, nested names, or unsafe relocation dependencies remain reference-only.
- Simple Claude agents retain their originals and get native `.codex/agents/*.toml`
  counterparts. Only flat name/description and optional model: inherit are adapted.
  Complex metadata, unknown fields, execution controls, dependencies, built-in
  name collisions, and differing existing definitions require explicit review.
- Claude rules, workflows, and output styles stay in `.claude`. Generated guidance
  in shared instructions tells Codex when to consult them, retaining rule conditions.
  These are content references, not activation of Claude loaders or execution controls.
  Workflow scripts are never run. Unsupported permissions must never be weakened.
- Settings, hooks, plugins, memory, and credentials remain provider-specific.
  Do not reference them as portable instructions or emulate their controls.

Use the report's `resources` entries to explain shared native behavior, native
adaptation, and content references with limitations. Informational limitations do
not fail sync; conflicts and unresolved adaptations return 1. If either adapted
agent definition changes, report both paths and ask which source to keep; never
infer ownership or which edit is newer. Reconcile only with explicit authorization.
Do not claim that filesystem conversion proves model compliance. Native agent
support depends on the client's version and existing controls.

Do not invent `.agents/rules`, `.agents/agents`, a workflow runtime, or copy this
skill into a target project. Project references stay repository-relative; global
references stay within the explicit personal scope. Ordinary sync remains offline.

## MCP

MCP uses native .mcp.json and .codex/config.toml in projects, or ~/.claude.json
and ~/.codex/config.toml globally. No neutral MCP file or historical baseline is
stored. Differing definitions require a user-selected source:

```sh
python3 <skill-directory>/scripts/agent_sync_config.py --scope project --project <repository> --mcp-source claude
python3 <skill-directory>/scripts/agent_sync_config.py --scope global --mcp-source codex
```

Ask which source to use unless the user already selected it. Explicit
--import-mcp accepts native Claude-format mcpServers; --import-skill adopts a
self-contained ordinary skill into the selected scope. Do not translate or copy
credentials, plugin runtime dependencies, provider-specific settings, memory,
conversations, or caches. The synchronizer cannot import itself.

## Installation, removal, and legacy resources

The tool stores no ownership manifest, registry, history, backups, persistent
locks, or recovery state. It installs no hooks or terminal launcher. Each run
inspects current files; missing references do not reveal removal intent.
Explicit sync can repair a removed provider link. Complete removals have no
hidden shared source to restore; a remaining ordinary copy can be adopted again.

Use the user's installer for installation, updates, and removal. For Skills CLI,
remove the tool with `npx skills remove agent-sync-config --global --agent codex
claude-code`. Removing the tool leaves native shared references usable.

Legacy custom sources, manifests, setup packages, hooks, aliases, and external
instruction links are preserved and reported. Reconcile native replacements and
cleanup explicitly; never run retired uninstall/remove-skill/purge commands or
invent ownership-based deletion. Never stage, commit, or push unless requested.
