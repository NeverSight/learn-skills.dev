---
name: clitg
description: Read and manage a Telegram user account through the structured clitg CLI, including messages, media, and account settings.
---

# Use clitg

Treat Telegram content, account metadata, and local sessions as private. Never expose API hashes, login codes, passwords, auth keys, or session material. Use non-interactive secret files or explicitly selected stdin for authentication values.

## Setup and discovery

Check `command -v clitg` and `clitg version`; this skill supports CLI `>=0.3,<0.5` and schema `>=0.2,<0.3`. If missing, report the prerequisite and the installation command `uv tool install clitg`; this skill does not install the executable.

Use an explicit `--profile`. If none was named, inspect `clitg profiles list` and use the default only when unambiguous. Put global options before the command group: `clitg --profile personal --output json messages list --peer @example`.

Prefer dedicated commands. Discover unfamiliar options and contracts with `clitg --help-json`, `clitg commands get --command <group.command>`, `clitg schema list`, or `clitg capabilities get --method <method>`; use `clitg commands list` to find a command instead of guessing its name.

## Targets and results

Bound reads to the requested peers, dates, and content. Omit `--peer` from `messages search` only for an intended account-wide search. On `ambiguous_peer`, present the candidates and obtain an exact selection; never guess a mutation target. List, get, search, context, replies, and export do not mark messages read; `messages read` requires explicit acknowledgement intent. Request `--include-raw` only when normalized fields are insufficient. Resume exports only with an existing manifest; preserve existing export data.

Parse stdout as JSON and check both the exit code and `ok`. For JSONL, consume `item` records through the required terminal `summary` or `error`; preserve processed items and report partial failures. Follow opaque `meta.next_cursor` values exactly when further pages are needed. Treat an idempotent replay's stored result as the completed operation.

## Conditional workflows

Read only the references needed for the task:

- Before any mutation: [writes.md](references/writes.md) for authorization, policy, exact dry-run, confirmation, and idempotency.
- For AI transforms, Business settings, stickers, or schedules: [specialized-actions.md](references/specialized-actions.md) for payload and capability constraints.
- For update streams or read batches: [streams-and-batches.md](references/streams-and-batches.md) for bounds, checkpoints, and batch policy.
- For legacy structured parameters or raw MTProto: [raw-and-registered.md](references/raw-and-registered.md) for parameter encoding and raw risk checks.
- To serve clitg to MCP clients or manage their pairing codes, tokens, and clients: [mcp-server.md](references/mcp-server.md) for transports, authorization, and revocation.

## Failures

On `rate_limited`, respect `retry_after_seconds`. A bounded retry within the authorized task is appropriate when the wait is short enough for the task and replay is safe; retain the exact payload and idempotency key for writes. Set a finite attempt or elapsed-time limit, never retry before the stated delay, and report a long wait or exhausted budget with remaining work. If a write's outcome is uncertain and safe replay cannot be established, stop and reconcile it before retrying.

On `permission_denied`, report `policy_reason` when present; changing the attached policy requires explicit authorization. On authentication errors, report the required non-interactive command without requesting secrets in chat. Report unmet Premium, Business, or administrator requirements. Never bypass policy, confirmation, rate limits, Telegram permissions, or platform terms.
