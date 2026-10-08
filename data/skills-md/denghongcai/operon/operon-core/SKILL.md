---
name: operon-core
description: Use when an agent needs to understand what Operon is, inspect config.yaml, choose the right Operon surface, or safely start any Operon task.
---

# Operon Core

Operon is a capability runtime over an already reachable private network. It is not a VPN, relay, mesh router, or global routing layer. Use the CLI as the default agent surface, use the TypeScript SDK for application code, and use the gRPC protocol directly only when a custom client is needed.

Start every task by identifying the config path:

- Default: `$HOME/.operon/config.yaml`.
- Override: `operon --config <path> ...`.

Before operating on nodes, run:

```bash
operon --config <path> config explain
```

Use `operon --config <path> --json config explain` when a script or agent needs structured daemon, client, auth, policy, service, and secrets information without reading raw YAML.

Use `operon <command> --help` for exact syntax. Skills explain scenarios and command choice; CLI help is the source of truth for flags and arguments.

Core workflow:

1. Explain config.
2. Inspect nodes with `operon node list`, `operon node resolve`, or `operon node ping`.
3. Inspect allowed capabilities with `operon capability list <node>`.
4. Choose the narrowest command family: `fs`, `exec`, `service`, `audit`, `trace`, or `run`.
5. Confirm destructive or externally visible operations before running them.
6. Verify mutating work with `operon audit show <node>` and, for graphs, `operon trace show <trace.json>`.

Policy is authoritative. Do not bypass denied capabilities, do not infer full trust from network reachability, and do not ask users to expose daemon ports outside their intended private network.
