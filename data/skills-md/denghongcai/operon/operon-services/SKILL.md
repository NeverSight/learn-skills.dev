---
name: operon-services
description: Use when an agent needs to inspect service metadata, run service health checks, or create explicit local TCP or UDP forwards to policy-allowed Operon services.
---

# Operon Services

Use this skill when a remote node exposes service metadata in policy and the local machine should consume that service through an explicit forward. Operon assumes the two Operon nodes are already reachable through the user's private network.

Inspect exact syntax first:

```bash
operon service --help
operon service list --help
operon service check --help
operon service forward --help
operon service forward-udp --help
```

Command choice:

- List allowed services: `operon service list <node>`.
- Check service health: `operon service check <node> <service_id>`.
- TCP forward: `operon service forward <node> <service_id> --listen 127.0.0.1:<port>`.
- UDP/datagram forward: `operon service forward-udp <node> <service_id> --listen 127.0.0.1:<port>`.

Example scenario:

1. `node-a` has a policy-allowed service for `127.0.0.1:80`.
2. On `node-b`, run a local TCP forward on `127.0.0.1:8080`.
3. Local tools on `node-b` use `127.0.0.1:8080` as if the service were local.

Confirm before binding a public listen address such as `0.0.0.0:<port>`. Prefer loopback addresses unless the user explicitly asks for broader exposure. Verify service usage through `audit show` and stop forwards when the task is complete.
