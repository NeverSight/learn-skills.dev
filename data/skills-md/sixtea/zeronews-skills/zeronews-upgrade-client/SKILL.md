---
name: zeronews-upgrade-client
description: Upgrade ZeroNews when the user asks to update the client (device download-resolve + device upgrade, or binary from download_url). Install tasks use zeronews-install-client UPGRADE-ON-INSTALL (platform download/latest only, no client_id)—not this skill unless the user explicitly wants console-style device upgrade.
license: MIT
metadata:
  author: zeronews
  version: "1.2"
compatibility: Requires logged-in CLI supporting device download-resolve and device upgrade when using remote upgrade. Target must be online for device upgrade; offline may need zeronews-install-client binary replace path.
---

# Upgrade Client

## Local execution (mandatory)

All `zeronews` CLI, install scripts, Docker, browser login, and local port discovery **must run on the user's computer**, not in an Agent **sandbox** or remote-only workspace.

- Shell from the IDE: **disable sandbox** (full local permissions); **不要沙箱中执行，都在用户本地电脑中执行。**
- With MCP: run `zeronews-mcp` locally; use MCP tools instead of sandbox CLI against workdir.
- If the agent cannot run on the user's machine, say so—do not fake install/login/expose.

Full rules: [LOCAL-EXECUTION.md](../_shared/references/LOCAL-EXECUTION.md).

Aligns with MCP **`upgrade_client`** and **`install_client`** upgrade precheck: compare version, skip if latest, **otherwise upgrade immediately**.

**MCP mapping**: `upgrade_client` (optional `client_id` picker for online devices).

## Install vs upgrade

| Situation | Skill |
|-----------|--------|
| No binary / first setup | `zeronews-install-client` |
| Probe only, no download | `zeronews-install-client` probe branch — **no upgrade** |
| Install task + binary exists | **`zeronews-install-client`** runs [UPGRADE-ON-INSTALL.md](../zeronews-install-client/references/UPGRADE-ON-INSTALL.md) — **platform latest + binary replace only** (no `client_id`); **not** this skill's `device download-resolve` chain |
| User only says «升级» | **this skill** |
| Reinstall after reset | `zeronews-install-client` after `zeronews-reset-client` |

## Prerequisites

- `zeronews --workdir {WORKDIR} status --json` → `login: true` when using `device download-resolve` / `device upgrade`
- Resolve **target `client_id`**:
  - **This machine**: from `status --json` or inspect
  - **Another device**: `show devices --json` → numbered picker when id unknown

Hand off to `zeronews-manage-account-clients` if the user only wanted to list devices.

## Workflow

### Step 1: Precheck

```bash
zeronews --workdir {WORKDIR} device download-resolve {CLIENT_ID} --json
```

- **`is_latest`** → report current version; **stop** (no upgrade commands).
- Upgrade available → note `current_version`, `target_version`, `download_url` if present.
- Precheck fails → report error; for **install-triggered** flow, fall back to steps in UPGRADE-ON-INSTALL (official binary / install script).

### Step 2: Upgrade (no confirmation)

**Do not ask** «是否要升级» / «confirm upgrade» — proceed after precheck shows not latest.

Briefly **inform** the user what will run (current → target; client may restart). Then:

```bash
zeronews --workdir {WORKDIR} device upgrade {CLIENT_ID} --json
```

If remote upgrade fails or target offline:

- Replace binary from precheck **`download_url`** per platform (see [UPGRADE-ON-INSTALL.md](../zeronews-install-client/references/UPGRADE-ON-INSTALL.md)) — **no** `service restart`; client self-handles. Then `reload` or `start` only if not running.

Re-run `download-resolve` after success until latest or report failure.

### Step 3: Verify

- `zeronews-inspect-client` or `status --json` for `version` and `running`
- **Install-path upgrade:** do not call manage-client-service restart — see UPGRADE-ON-INSTALL.md.

## Output

Return: client_id, versions before/after, commands run, verification result.

## Safety rules

- no upgrade confirmation prompts (picker for **which device** is OK when id unknown)
- do not upgrade without a resolved target id (except install path using local machine id from status)
- one upgrade chain at a time

## References

- Install-triggered auto upgrade: [UPGRADE-ON-INSTALL.md](../zeronews-install-client/references/UPGRADE-ON-INSTALL.md)
- [ACCOUNT-CLI-JSON.md](../_shared/references/ACCOUNT-CLI-JSON.md)
- [MCP-SKILLS-PARITY.md](https://docs.zeronews.cc/raw/ai/zeronews-mcp-setup.md)
