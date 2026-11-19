---
name: zeronews-manage-platform-domains
description: Add a ZeroNews platform subdomain, list account domains and ports, delete ports or empty domains. Use when the user wants a random subdomain, a new zeronews.cc-style prefix, to clean up domains in the console, or delete a port mapping—not for exposing a local HTTP port (use expose-service).
license: MIT
metadata:
  author: zeronews
  version: "1.1"
compatibility: Requires logged-in `zeronews` CLI. Subdomain prefix must match 6–12 lowercase letters and digits.
---

# Manage Platform Domains

## Local execution (mandatory)

All `zeronews` CLI, install scripts, Docker, browser login, and local port discovery **must run on the user's computer**, not in an Agent **sandbox** or remote-only workspace.

- Shell from the IDE: **disable sandbox** (full local permissions); **不要沙箱中执行，都在用户本地电脑中执行。**
- With MCP: run `zeronews-mcp` locally; use MCP tools instead of sandbox CLI against workdir.
- If the agent cannot run on the user's machine, say so—do not fake install/login/expose.

Full rules: [LOCAL-EXECUTION.md](../_shared/references/LOCAL-EXECUTION.md).

Account-level **domains** and **ports** (console-equivalent), via CLI `--json`.

**MCP mapping**: `list_account_domains`, `add_domain`, `delete_domain`, `delete_port`.

Reference: [ACCOUNT-CLI-JSON.md](../_shared/references/ACCOUNT-CLI-JSON.md) · [CLI-JSON-PATHS.md](./references/CLI-JSON-PATHS.md) · [DELETE-CONFIRMATION.md](./references/DELETE-CONFIRMATION.md) · subdomain rules: [SUBDOMAIN-PREFIX.md](./references/SUBDOMAIN-PREFIX.md)

## Prerequisites

- `login: true` on `{WORKDIR}` — else `zeronews-configure-client`
- Mutations need user confirmation for **delete port** and **delete domain**

## Workflow

### Step 1: List domains (read-only)

```bash
zeronews --workdir {WORKDIR} show domains --json
```

Optional pagination (same as MCP `list_account_domains`):

- `--workspace-id {ID}`
- `--page N`
- `--size N`

Parse list rows per [CLI-JSON-PATHS.md](./references/CLI-JSON-PATHS.md): domain **`items[].id`**, nested **`items[].ports[].id`** for `delete port`.

Show numbered list: domain name, port count, each port’s public target if present.

### Step 2: Add platform domain

When the user wants **a new subdomain** but did not give a prefix:

1. Do not invent a prefix silently.
2. Offer **four random 8-character** prefixes (`a-z`, `0-9`) plus let them type a custom prefix — see [SUBDOMAIN-PREFIX.md](./references/SUBDOMAIN-PREFIX.md).
3. After they choose, validate `^[a-z0-9]{6,12}$`.

```bash
zeronews --workdir {WORKDIR} add domain --subdomain {PREFIX} --json
```

Optional: `--workspace-id` per CLI help.

On errors such as no entitlement or no available domain, report CLI message; do not retry with random prefixes without user consent.

### Step 3: Delete port

When `port_id` is unknown, list domains and nested ports (Step 1), numbered picker.

Then follow [DELETE-CONFIRMATION.md](./references/DELETE-CONFIRMATION.md): **separate explicit confirm**, then:

```bash
zeronews --workdir {WORKDIR} delete port {PORT_ID} --json
```

### Step 4: Delete domain

**Only when the domain has no ports left** (delete ports first).

After picker + **explicit confirmation** (DELETE-CONFIRMATION), run:

```bash
zeronews --workdir {WORKDIR} delete domain {DOMAIN_ID} --json
```

If CLI says ports remain, list them and hand off to Step 3.

## Output

Return created subdomain/domain ids from `--json`, or deletion result fields.

## Safety rules

- every delete port / delete domain: picker then **second-step** confirm — [DELETE-CONFIRMATION.md](./references/DELETE-CONFIRMATION.md)
- never pass placeholder tokens like `__custom_input__` to CLI
- adding a domain does not by itself map a local port — user may still need `zeronews-expose-service`

## Handoff

- map local app to public URL → `zeronews-expose-service`
- account tunnels list/delete → `zeronews-manage-account-tunnels`
