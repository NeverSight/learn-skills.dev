---
name: zeronews-share-files
description: Share a local directory through ZeroNews with `file_share` on `zeronews add`. Use when asked to publish a folder or remote file browsing—not for mapping a generic HTTP port (use expose-service). Requires login and a running client before `add`.
license: MIT
metadata:
  author: zeronews
  version: "1.1"
compatibility: Requires authenticated `config.yml`, running local client, and the `zeronews` CLI.
---

# Share Files

## Local execution (mandatory)

All `zeronews` CLI, install scripts, Docker, browser login, and local port discovery **must run on the user's computer**, not in an Agent **sandbox** or remote-only workspace.

- Shell from the IDE: **disable sandbox** (full local permissions); **不要沙箱中执行，都在用户本地电脑中执行。**
- With MCP: run `zeronews-mcp` locally; use MCP tools instead of sandbox CLI against workdir.
- If the agent cannot run on the user's machine, say so—do not fake install/login/expose.

Full rules: [LOCAL-EXECUTION.md](../_shared/references/LOCAL-EXECUTION.md).

Feature-focused wrapper: `zeronews add … --feature=file_share`.

**MCP mapping**: `add_tunnel` with `tunnel_kind=lfs` / `file_share` + `root_path` + `admin_password` + optional `bw`.

## Workflow

### Step 0: Gate (always first)

Same as `zeronews-expose-service`:

1. `login: true` and client **running** (prefer `zeronews-inspect-client`).
2. Not configured → `zeronews-configure-client`.
3. Not running → `zeronews-manage-client-service` or `zeronews start`.
4. `login_pending` → finish login before `add`.

Do not ask for `root_path` until the gate passes.

### Step 1: Collect share settings

Ask only what is still unknown:

1. absolute **local directory** (`root_path`)
2. **admin_password** (≥ 8 characters; required on create)
3. optional public **domain**, or server allocation
4. optional bandwidth **`--bw=N`** Mbps (same as expose; default often 1 Mbps if omitted)

Do not ask for a local app port for LFS; file_share does not use the expose port-discovery flow.

### Step 2: Create the tunnel

```bash
zeronews --workdir {WORKDIR} add https --feature=file_share --feature-config '{...}'
```

Add `--domain=…` and `--bw=…` only when the user asked.

Minimum feature config:

```json
{
  "file_share": {
    "root_path": "/absolute/path",
    "admin_password": "<at least 8 characters>"
  }
}
```

See `../zeronews-expose-service/references/FEATURE-CONFIGS.md` for supported shapes.

If an admin password is set but the client has not been upgraded, the public URL may still serve anonymous read-only. Do not promise password-gated login on an old client.

After accept, do not reload/restart unless the user asked for repair; wait for the endpoint.

## Safety rules

- absolute `root_path` only
- never omit `admin_password` on create
- do not use `--feature=file_share` without the JSON block above
- gate before `add` (Step 0)

## Handoff

- HTTP port / generic tunnel → `zeronews-expose-service`
- webhook → `zeronews-expose-webhook`
