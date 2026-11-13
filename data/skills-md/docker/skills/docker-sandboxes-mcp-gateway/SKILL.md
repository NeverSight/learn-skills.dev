---
name: docker-sandboxes-mcp-gateway
description: Use this skill when giving an agent in a local Docker Sandbox (sbx) access to MCP servers, even if the user just says "my sandboxed Claude can't see the GitHub tools", "add Notion MCP to my sandbox", or "take this MCP server away from the sandbox". Covers sbx mcp add/load/unload/ls/rm/auth/inspect, static vs dynamic mode, --static-mcp, host-side execution, OAuth and header secrets, untrusted URLs, and removal order.
license: Apache-2.0
compatibility: Requires the standalone sbx CLI (Docker Sandboxes) in local gateway mode. sbx was not installed where this skill was written, so flags come from Docker docs and must be re-checked with `sbx mcp <subcommand> --help`. Behavior boundaries - sbx mcp unload 0.48.0+, command-server approval in environment files 0.50.0+, --static-mcp none and mcp.useServerNamePrefixes 0.51.0+.
---

# Docker Sandboxes MCP Gateway

## Overview
Every local Docker Sandbox starts a host-side MCP gateway. The agent inside the microVM sees one MCP endpoint, while `sbx mcp` registers servers, holds OAuth and header credentials, and decides which servers each sandbox can use. This skill owns `sbx mcp` and the static/dynamic loading model. It does not cover the Docker Desktop MCP Toolkit (`docker mcp`), which is a separate product.

## When to use this skill
Activate this skill when:
- The user wants an agent in a local `sbx` sandbox to use a remote or host-run MCP server.
- The user asks to register, authorize, inspect, load, unload, list, or delete an MCP server for sandboxes.
- The user wants a sandbox to expose a fixed set of MCP servers (`--static-mcp`), or none.
- The user is debugging missing MCP tools, an OAuth or header-secret failure, or a server still reachable after "removal".
- The user asks whether an MCP server runs inside or outside the sandbox.

## Do not use this skill when
Do not use this skill when:
- The task uses `docker mcp` (MCP Toolkit profiles, `docker mcp gateway run`, `docker mcp client connect`). It is a different product with separate server settings; use `docker-docs` to look up current Toolkit docs.
- The task is creating, stopping, or removing the sandbox itself; use `docker-sandboxes-lifecycle`.
- The task is egress allow/deny rules or credentials unrelated to an MCP server; use `docker-sandboxes-network-credentials`.
- The task is writing the `mcp` block of a checked-in `sbxenv.yaml`; use `docker-sandboxes-env`.
- The task is declaring MCP toolsets in a Docker Agent `agent.yaml`; use `docker-agent-config`.
- The sandbox is a cloud sandbox or uses a hosted gateway; see the scope rule below.

## Core guidance

### Preflight and scope
- Run `sbx login` first if the user is not authenticated. Docker must be running on the host for `--local` OCI servers and explicit `docker` commands.
- Use `sbx mcp` for agents inside Docker Sandboxes and `docker mcp` only for agents on the host. Servers enabled in the MCP Toolkit are not shared with Docker Sandboxes, and the Toolkit is not required.
- Register once on the host rather than editing the sandboxed agent's own MCP config, so credentials, loading and governance stay in one place.
- The guidance below describes the local gateway. Before unload, header-secret or `mcp.*` setting advice, confirm which gateway the sandbox uses. A hosted (SaaS) gateway may be selected for the account, and `mcp.forceLocalGateway` can force the local one. Hosted gateways do not support `sbx mcp unload`, and the hosted gateway rejects header registrations unless `--oauth-authorization-server` is given. Before changing `mcp.forceLocalGateway`, state to the user that it is host-global, needs `sbx daemon restart`, and does not override organization governance, and get their agreement.
- Cloud sandboxes do not use local `sbx mcp add` registrations. Connect the server in Docker Agentic Platform, then run `sbx --cloud mcp load <server-name> --sandbox <sandbox>`; inspect with `sbx --cloud mcp ls [sandbox]`.

### Registration is not attachment
- Always treat `sbx mcp add` as host-only: it stores the definition and does not expose the server to any sandbox.
- Expose a registered server with `--static-mcp` at create/run time, or `sbx mcp load` on an existing sandbox.
- Server names may contain letters, numbers, dots, hyphens and underscores. `none` is reserved.

```bash
# Remote server; OAuth is prompted unless --skip-auth is passed
sbx mcp add notion --url https://mcp.notion.com/mcp
# Attach to a running sandbox; connected agents get a tool-list update
sbx mcp load notion --sandbox my-session
```

All flags and subcommands that were documented are in `references/sbx-mcp-reference.md`.

### Static vs dynamic mode
- Mode is chosen when the sandbox is created and persists across restarts. Dynamic (no `--static-mcp`) pre-loads nothing and lets the agent find and attach registered servers. Static loads only the named servers and exposes no discovery tools (`mcp-find`, `mcp-add`, `mcp-config-set`).
- Every name in `--static-mcp` must already be registered. Pass a comma-separated list or repeat the flag.
- Passing `--static-mcp` when reconnecting to an existing sandbox does not replace its initial set. Reuse the sandbox and use `sbx mcp load`, or create a new one with a new name.
- Use static mode for untrusted repositories or least-privilege sandboxes. Use `--static-mcp none` (0.51.0+) to start with no servers and no discovery; it stays static after the last server is unloaded and after restarts.
- Static mode is not an MCP or network lock. `sbx mcp load` can still attach host-registered servers, the agent may run its own MCP clients, and sandbox egress is governed by `sbx policy` and org MCP policy, which are separate controls.
- Unloading every server from a sandbox created with a named static set only keeps it static for the current session; after a daemon restart the agent can find and attach registered servers.

```bash
sbx mcp add linear --url https://mcp.linear.app/mcp
sbx run claude --name my-session --static-mcp notion --static-mcp linear
sbx run claude --name locked --static-mcp none
```

### Host execution and trust
- Local stdio servers (`--command`, or `--local` with a metadata URL) run on the host, not in the microVM. A server that starts a Docker container uses host Docker isolation. It can reach host files, the host network and credentials it is given.
- Register only commands and URLs the user trusts. Show the resolved command to the user and get confirmation before registering a `--command` server.
- Never pass `--skip-ssrf-check` unless the provider and its redirects are fully trusted. If `--url` resolves to a private, loopback, link-local or cloud-metadata address, `sbx` registers but warns; stop and confirm with the user.
- Keep command-server scripts outside writable sandbox mounts. Environment-file command approval pins the executable path, not file contents.
- Organization MCP policy is enforced at the gateway, separately from the HTTP/HTTPS network proxy; registration can be rejected by it.

### Credentials and OAuth
- OAuth tokens stay on the host (host OS credential store). `mcp:`-prefixed secrets stay on the host and are not injected into sandboxes.
- Check OAuth with `sbx mcp inspect <name>` and re-authorize with `sbx mcp auth <name>`. If a server refuses dynamic client registration, register a client with the provider and pass `--client-id` (`--oauth-authorization-server` if needed) to `sbx mcp add`.
- For header auth use single quotes so the shell keeps the placeholder, then store the value; `sbx secret set` prompts for it, so no token enters shell history:

```bash
sbx mcp add acme --url https://mcp.acme.com/mcp \
  --header 'Authorization: Bearer ${api-key}'
sbx secret set mcp:acme:api-key
sbx mcp inspect acme   # shows header templates and whether secrets are set, never values
```

- Placeholders name stored secrets (`${api-key}` reads `mcp:acme:api-key`), not environment variables. Credential headers such as `Authorization` must use a placeholder. Custom headers need a remote HTTP endpoint and cannot be used with `--command` or `--local`.
- Rotate with `sbx secret set` using the same name. After setting, changing or removing a header secret, stop and restart the sandbox or restart `sandboxd`; an existing gateway keeps the old value and a server skipped for a missing secret is not retried. Changing the server endpoint requires setting the secret again for the new endpoint.
- Egress is controlled by `sbx policy`, not by MCP registration. Delegate policy and general secret commands to `docker-sandboxes-network-credentials`.

### Inspect and remove (in this order)
- Inspect: `sbx mcp inspect <name>` for one registration; read `sbx mcp ls --help` first for the host listing, since its columns are not documented in the sources used here.
- Detach from one sandbox: `sbx mcp unload <name> --sandbox <sb>` (0.48.0+, local gateway only). It removes the saved attachment, so the server is not restored after a restart; the host registration, credentials and other sandboxes are untouched.
- Delete the host registration: `sbx mcp rm <name>`. It does not detach servers from sandboxes that already loaded them, and it keeps header secrets (it prints the removal commands, for example `sbx secret rm mcp:acme:api-key`). Unload from each sandbox first, then `rm`, then remove secrets deliberately.
- Unloading is not a lock: in dynamic mode the agent can reattach a registered server, including between `unload` and `rm`. If it does, `rm` leaves that attachment in place.
- To revoke a server, close that window:
  1. List every sandbox that loaded it. For each dynamic-mode one, ask the user to pause its agent (no task running) until step 4.
  2. Run `sbx mcp unload <name> --sandbox <sb>` for each of those sandboxes.
  3. Run `sbx mcp rm <name>`. After this, the agent can no longer find it.
  4. Verify in each sandbox's session that the server's tools are gone before the user resumes the agent. Do not report the server as revoked until this check passes.
- If tools reappeared, unload again from that sandbox. Whether `unload` accepts a name whose registration was already removed is unverified (`checks/verification.md` step 5). If it is rejected, stop that sandbox with `sbx stop` and escalate rather than resuming it.
- For sandboxes that must never reach a server, create them with `--static-mcp none`.
- Removing local state does not revoke provider-side OAuth grants or API keys; revoke those at the provider.

### Tool names and settings
- Use `mcp.useServerNamePrefixes` (0.51.0+) when tool names collide across servers: `sbx settings set mcp.useServerNamePrefixes true`. Settings are host-global; read the current value before changing it and restore it afterwards. The documented set command is `sbx settings set`; get/unset syntax is not verified here, so run `sbx settings --help`.

### Common failures
- Tools missing after `add`: the server was never attached. Run `sbx mcp load`, or create a new sandbox with `--static-mcp`.
- Header server missing after setting its secret: restart the sandbox or `sandboxd`.
- Unload rejected: cloud sandbox or hosted gateway, or sbx older than 0.48.0.
- `command` servers from an environment file ask for approval: expected (0.50.0+); see `docker-sandboxes-env`.

Verify with `checks/verification.md` after any registration, load or removal.

## Related skills
- For creating, reattaching, stopping or removing the sandbox itself, use `docker-sandboxes-lifecycle`.
- For egress policy and general `sbx secret` credentials, use `docker-sandboxes-network-credentials`.
- For the `mcp` block in `sbxenv.yaml`, use `docker-sandboxes-env`.
- For MCP toolsets in a Docker Agent config, use `docker-agent-config`.
- For current docs on the Docker Desktop MCP Toolkit or release-sensitive details, use `docker-docs`.

## References
- `skill.yaml` — routing metadata for this skill.
- `agents/openai.yaml` — Codex discovery metadata.
- `references/sbx-mcp-reference.md` — documented `sbx mcp` subcommands, selected flags, versions and scope table.
- `references/sources.md` — claim-level evidence and unverified items.

## Assets
- None.

## Checks
- `checks/verification.md` — Verification runbook for registering, loading, unloading and removing MCP servers in a local sandbox.
