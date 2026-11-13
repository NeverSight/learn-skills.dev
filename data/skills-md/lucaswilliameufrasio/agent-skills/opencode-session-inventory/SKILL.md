---
name: opencode-session-inventory
description: >-
  Create or refresh a point-in-time inventory of running OpenCode processes and
  active sessions, and map them to Herdr workspace and tab labels. Use whenever
  the user asks which OpenCode sessions are running or requests a Herdr sidebar
  mapping. This is not a generic saved-session history or handoff.
---

# OpenCode session inventory

Build a concise snapshot of running OpenCode processes and API-confirmed active sessions, then map verified relationships to the workspace and tab labels shown in Herdr. Keep the live inventory separate from saved-session history.

## Workflow

1. **Find the existing report destination.** Search the knowledge base or document store named by the user, read the complete existing report, and preserve its format and history. Update that entry rather than creating a duplicate. Do not hard-code a private page ID, URL, workspace name, or project path into this skill. If no destination is available, ask before creating one.

2. **Inspect local OpenCode processes safely.** Use read-only process and listener inspection appropriate to the host. Identify local OpenCode server processes, their explicit listening ports, process IDs, and working directories. Do not assume a default port. Inspect only the process arguments needed to find explicit session identifiers; never dump full command lines or process environments, and do not read `.env` files.

3. **Query each local server's active-session endpoint.** Request `GET /api/session/active` through loopback for each identified server. Use only the response fields needed to identify active sessions and their project directories. A saved-session listing is not evidence that a session is currently active. Do not include prompts, message history, or conversation contents.

4. **Read Herdr's current state.** Use `herdr api snapshot` for the current Herdr session, or an explicitly selected session. Preserve the workspace and tab `label` values and IDs from `result.snapshot`. For candidate panes, use read-only pane/agent inspection and `herdr pane process-info` as needed. Prefer native session references when available. Do not focus, rename, create, close, or send input to any workspace, tab, or pane.

5. **Match conservatively.** Prefer an exact OpenCode session ID reported by Herdr. Otherwise match process identity/PID and exact working directory. A directory-only match is tentative; if multiple candidates share a directory, mark it ambiguous. Record unmatched processes and tabs instead of inferring a relationship.

6. **Update the report.** Add a dated snapshot with a short scope/method note and a table containing only useful fields, such as process/session, working directory, Herdr workspace label/ID, tab label/ID, pane ID, Herdr state, and match basis/confidence. Keep older captures as history. Distinguish API-confirmed active sessions from processes merely observed in panes.

7. **Handle unavailable APIs honestly.** If the OpenCode endpoint returns `401` or `403`, do not retrieve or reveal credentials to work around authentication. Mark API-derived active status as unavailable; publish only independently verified process/Herdr facts when a clearly labeled partial snapshot still answers the request. If the missing data makes the mapping ambiguous, ask before publishing. If the report destination is unavailable, do not claim it was updated or silently create a local substitute.

## Privacy and safety

- Treat process and session metadata as private operational data. Include only what the requested report needs, and do not copy real session IDs, process IDs, project names, paths, or snapshot contents into this skill, its tests, or shared repositories.
- Never print or publish credentials, process environment values, full potentially sensitive arguments, prompts, or conversation contents.
- Query only the user's local OpenCode and Herdr instances over their documented local interfaces. Do not probe unrelated hosts or ports.
- Treat the result as a point-in-time observation and clearly label tentative, ambiguous, and unavailable data.
- The only writes in this workflow are to the report destination explicitly requested by the user.

## References

- [OpenCode API](https://opencode.ai/v2/docs/api)
- [OpenCode skill discovery](https://opencode.ai/v2/docs/skills)
- [Herdr socket API](https://herdr.dev/docs/socket-api/)
- [Herdr CLI reference](https://herdr.dev/docs/cli-reference/)
