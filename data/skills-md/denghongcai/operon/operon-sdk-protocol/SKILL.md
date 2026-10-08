---
name: operon-sdk-protocol
description: Use when an agent needs to integrate Operon from application code, the TypeScript SDK, generated gRPC clients, or the documented runtime protocol instead of shelling out to the CLI.
---

# Operon SDK And Protocol

Use the CLI first for operational tasks. Use the TypeScript SDK when writing application code, and use direct gRPC only for custom clients that cannot use the SDK.

Start by reading local protocol and SDK docs:

- `PROTOCOL.md` for direct gRPC connection rules.
- [`proto/operon/runtime.proto`](../../proto/operon/runtime.proto) for service and message definitions.
- [`packages/sdk-js`](../../packages/sdk-js) for the TypeScript SDK.

Use CLI help to confirm behavior before mirroring it in code:

```bash
operon config explain --help
operon fs read --help
operon exec logs --help
operon exec session --help
operon service forward --help
```

Integration guidance:

- Read config with the same assumptions as `operon config explain`.
- Use bearer auth only from configured token sources; do not log token values.
- Prefer streaming APIs for large file reads, file writes, exec stdin, exec
  logs, and PTY-backed exec sessions.
- Preserve and reuse opaque filesystem `version` values when a workflow needs
  stale-write protection; send `expected_version` rather than parsing version
  tokens.
- Preserve audit and trace context when running execution graphs.
- Respect pagination fields on list APIs.
- Use `OpenExecSession` / SDK `openExecSession` for interactive terminal
  workflows, including explicit resize events when the client owns a TTY; use
  `RunExec` / `runExec` for non-interactive commands.
- Treat service forwarding as an explicit user operation, not an automatic background side effect.

After implementing a client workflow, compare it against equivalent CLI behavior and verify with audit or trace output.
