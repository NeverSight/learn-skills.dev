---
name: handoff
description: "Create, accept, or update the persistent `.context/ai-handoff.md` state shared by AI sessions and machines. Use when continuing in a new Claude or Codex session, transferring work between clients, or recording ownership and restart state."
---

# Project Handoff

Use one client-neutral handshake for every route. Before acting, read `../shared/cross-client-handoff.md` completely and follow its schema and state machine.

## Choose the route

- If the user names Claude or Codex, use that client as `to`.
- If the user asks for the next or a fresh session without naming a client, set `to` to the current client. This is the default for Claude-to-Claude and Codex-to-Codex continuation.
- Use `to: either` only when the task is deliberately client-agnostic.
- Set `from` to the current client, or `human` when invoked outside a client session.

All routes write `<project-root>/.context/ai-handoff.md`. Do not create a separate client-specific handoff file.

## Prepare a handoff

1. Resolve the project root from the current working directory or the named project.
2. Read only the relevant durable guidance and state: `CLAUDE.md`, `AGENTS.md`, the latest approved plan, current focus, recent log, and any existing handshake. Never inspect restricted `data/raw/` content.
3. Use the supplied outcome. If none is supplied, infer the highest-priority open loop; ask only if different choices would materially change scope.
4. Reconcile the existing handshake. Preserve still-valid decisions and its log, then create a new `handoff_id` and set `status: ready`.
5. Record the source and target client, source and target machine, branch, commit, exact working-tree ownership, observable acceptance criteria, real commands, and the first concrete action.
6. Validate the YAML frontmatter and Markdown sections against the shared protocol. Check that the file contains no secrets, credentials, transcripts, caches, or restricted data.

Never overwrite project-owned `CLAUDE.md` or `AGENTS.md`: they remain durable client guidance. Never auto-commit or push the handshake.

## Receive a handoff

When `.context/ai-handoff.md` targets the current client or `either`:

1. Read both native guidance files and the handshake before editing.
2. Compare the recorded branch, commit, machine, and changed-file ownership with the actual working tree.
3. Set `status: accepted` and append a timestamped log entry before substantive work.
4. Set `status: in_progress` when execution begins.
5. Maintain acceptance criteria and the log. Finish with `complete`, or use `blocked` with the precise blocker and safe next action.

## Transport and launch

- Same machine: start the receiving client in the project root.
- Dropbox project: let the project sync, then verify the recorded branch/commit and file ownership.
- Git project on another machine: verify the remote, commit/push only with normal authorization, pull there, and run that distribution's documented client installer or sync command before starting the receiving client.

Report the handshake path, route, outcome, status, transport needed, and launch command. A completed handshake stays as a short audit trail until the next handoff reconciles it.

## Compatibility

Root `handoff.md` is retired and ignored. Every new or resumed handoff must use `.context/ai-handoff.md`; it is the only format that supports same-client, cross-client, and cross-machine state tracking.
