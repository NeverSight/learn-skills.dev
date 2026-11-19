---
name: zeronews-expose-webhook
description: Create a ZeroNews webhook tunnel with `zeronews add --feature=webhook`—WeChat Pay, WeChat Contract, or standard webhook proxy. Use for payment or callback URLs, not for generic port expose or folder share. Requires login, running client, and a known local callback port (use LOCAL-LISTENERS if the user did not specify a port).
license: MIT
metadata:
  author: zeronews
  version: "1.1"
compatibility: Requires authenticated client, running local runtime, and supported webhook feature configs.
---

# Expose Webhook

## Local execution (mandatory)

All `zeronews` CLI, install scripts, Docker, browser login, and local port discovery **must run on the user's computer**, not in an Agent **sandbox** or remote-only workspace.

- Shell from the IDE: **disable sandbox** (full local permissions); **不要沙箱中执行，都在用户本地电脑中执行。**
- With MCP: run `zeronews-mcp` locally; use MCP tools instead of sandbox CLI against workdir.
- If the agent cannot run on the user's machine, say so—do not fake install/login/expose.

Full rules: [LOCAL-EXECUTION.md](../_shared/references/LOCAL-EXECUTION.md).

Wrapper around `zeronews add https --port={PORT} --feature=webhook --feature-config '{…}'`.

**MCP mapping**: `add_tunnel` with `feature=webhook` + `feature_config` + optional `bw`.

## Supported webhook modes

- standard reverse-proxy webhook
- verified WeChat Pay (`wechat_pay`)
- verified WeChat Contract (`wechat_contract`)

Configs: [FEATURE-CONFIGS.md](../zeronews-expose-service/references/FEATURE-CONFIGS.md)

## Workflow

### Step 0: Gate (always first)

Same as `zeronews-expose-service`:

1. `login: true` + client **running** (`zeronews-inspect-client`).
2. Hand off to `zeronews-configure-client` / `zeronews-manage-client-service` / finish `login_pending` as needed.

Do not ask webhook mode or port before the gate passes.

### Step 1: Resolve local port

**User gave a port** (callback server already listening):

- Use that port; do not substitute another.

**User did not give a port**:

- Do not default to 3000/8080.
- Follow [LOCAL-LISTENERS.md](../zeronews-expose-service/references/LOCAL-LISTENERS.md): enumerate TCP LISTEN, numbered list, user picks, then continue.

### Step 2: Webhook options

Ask only what is still unknown:

1. mode: standard proxy, WeChat Pay, or WeChat Contract
2. optional public domain or server allocation
3. inline `--feature-config` or YAML path per FEATURE-CONFIGS
4. optional **`--bw=N`** Mbps

### Step 3: Create

```bash
zeronews --workdir {WORKDIR} add https --port={PORT} --feature=webhook --feature-config '{...}'
```

Add `--domain` / `--bw` when requested.

After accept, wait for endpoint delivery; no reload/restart unless user asked repair.

## Safety rules

- only supported verify scenes in FEATURE-CONFIGS
- Step 0 before `add`
- no invented webhook schemas

## Handoff

- non-webhook HTTP/TCP → `zeronews-expose-service`
- directory share → `zeronews-share-files`
