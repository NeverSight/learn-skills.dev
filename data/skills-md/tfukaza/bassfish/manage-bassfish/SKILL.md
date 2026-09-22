---
name: manage-bassfish
description: Install, inspect, configure, recover, and use Bassfish through its human CLI and native Codex, Claude, and OpenCode plugins, including daemon, file-lock diagnostics, thread, and ticket commands. Use when the user asks to manage Bassfish, troubleshoot it, operate shared content from the terminal, reset data, or force-release a turn. Do not use for ordinary agent-to-agent MCP participation.
license: MIT
---

# Manage Bassfish

Use the `bassfish` human CLI for installation, operations, diagnostics, and user-requested terminal content work. Agents participating in shared conversations should use the Bassfish MCP server through `$use-bassfish` instead.

## Inspect before changing state

- Use `bassfish --version`, `bassfish doctor`, `bassfish daemon status`, and `bassfish config show` to establish the current state.
- Run `bassfish --help` before an uncommon command instead of guessing flags.
- Keep `BASSFISH_DATA_DIR` consistent across the CLI and every connected agent host.
- Use `--workspace /absolute/repository/path` when the command is not launched from the intended Git repository. Native Codex, Claude, and OpenCode plugins automatically restore identity from the host session ID. For manual CLI or MCP connections, `--name NAME` supplies explicit attribution but does not create a native host-session binding.
- A timed-out content write is never replayed. Content, revision receipts, notifications, and turn completion share one Turso transaction. If the commit outcome is uncertain, reconnect and inspect the resource and its history before deciding whether another write is needed.

## Preserve authority boundaries

Treat an explicit user request as authorization for the requested operation only. Otherwise, get confirmation immediately before installing software, resetting data, forcing a turn release, deleting content, or changing daemon/configuration state.

- Use `daemon run` only for user-requested foreground diagnostics; normal operation uses `daemon start`, `status`, and `stop`.
- Storage is one embedded Turso database owned by the daemon. Use daemon commands to stop it.
- Do not automatically retry `TURN_BUSY`, a failed mutation.

`bassfish data reset --yes` is a recovery action, not routine cleanup. Stop the daemon first. The command moves the data directory to a timestamped backup; report the backup path. `bassfish turn release TURN_ID --force` can revoke only a claimed turn and cannot interrupt a committing content write. Revoking an advisory file lock cannot stop an external editor from writing.

## Use the CLI deliberately

- Installation and MCP connection are separate: install `@bassfish/cli`, run `bassfish setup`, then install the host integration. Codex and Claude Code use repository marketplace plugins; OpenCode uses `opencode plugin @bassfish/cli --global`.
- Codex CLI 0.154+ queues actionable idle updates and injects them at active boundaries; Claude Code injects at safe boundaries; Claude Code and OpenCode can also resume idle sessions for coalesced activity. OpenCode inserts actionable notification content into busy sessions without aborting them. No separate `bassfish notifications watch` process is needed.
- Native host plugins bind `(project, host, session ID)` to one durable identity. Resuming that session restores its name; `setAgentName` affects only that binding. Concurrent adapters for one binding share identity and notifications but retain separate content-turn and file-lock ownership.
- A manual MCP process without a host session ID registers its own online identity. An omitted name comes from the finite built-in pool and is never automatically reassigned to another identity.
- Thread, ticket, and project commands use the same server-side turn rules as MCP. A busy content command cancels its own request and returns `TURN_BUSY`; it does not wait or retry.
- Use `bassfish turn list` to inspect file paths, owners, and queued or claimed status. File locks use session lifetime; they do not use the content-turn timeout. Native filesystem and Git tools handle file contents and history.
- Use `bassfish sonar` for a live, read-only project dashboard with channel-style threads, ticket dependency graphs, file contention, and retained activity. It waits for a stopped daemon and never registers an agent or acquires turns. Use `sonar --json` for a single observation snapshot, `--workspace PATH` to select a repository, and `--ascii` for ASCII borders.
- Daemon control, forced release, lifecycle changes, history, revision inspection, and export are CLI-only. Do not look for them in the compact MCP tool inventory.
- Interactive terminals receive concise human-readable results. Piped output remains JSON; use `--json` explicitly for automation or `--plain` for unstyled human output. Capture IDs from JSON rather than parsing display text.

Read [the CLI recipes](references/cli-recipes.md) for exact commands and safe operational sequences.
