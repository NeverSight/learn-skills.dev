---
name: pipefy-toolkit-setup
description: >
  Guide a first-time user through Pipefy AI toolkit setup (Cursor Marketplace
  plugin, hosted MCP, local install.sh, or Claude Code plugin). Use when the
  user asks to install Pipefy MCP, connect Claude/Cursor to Pipefy, run
  /pipefy:install, or set up mcp.pipefy.com. Do not use for day-to-day Pipefy workflows
  after MCP is already working.
tags: [pipefy, onboarding, install, mcp, setup, claude, cursor]
---

# Pipefy toolkit setup (first-time onboarding)

**Canonical install snippets** live only in the root [`README.md#installation`](../../../README.md#installation) — there is no second copy of the commands. This skill is the agent **checklist** — print or run the README blocks verbatim; do not invent alternate commands. The Cursor Marketplace plugin is the exception: it installs from Cursor's plugin UI, so there is no command to print or run.

Edge cases: [`packages/mcp/README.md`](../../../packages/mcp/README.md). Auth: [`docs/cli/auth.md`](../../../docs/cli/auth.md). Env: [`docs/config.md`](../../../docs/config.md).

---

## When to use

- "Set up Pipefy", "install the MCP", "connect Claude/Cursor to Pipefy"
- User mentions the Cursor Marketplace plugin, `/plugin marketplace add`, `/pipefy:install`, or `mcp.pipefy.com`
- Fresh machine with no `pipefy` on PATH and no Pipefy MCP server

**Do not use** once tools already work — switch to a domain skill (pipes, tables, …).

## Prerequisites

- User has a Pipefy account (Admin access if they need a service account).
- Cursor Marketplace plugin: Cursor, nothing local.
- Hosted MCP: Claude Code CLI (`claude`).
- Local toolkit: a shell that can run `curl` (`install.sh` can install `uv`).

**Who does what**

| Actor | Does |
|-------|------|
| **Agent** | Asks path; prints README commands verbatim; runs shell `claude mcp add` / `install.sh` when the user agrees; checks `claude mcp get` / list. Does **not** run `install.sh --client cursor` when the user chose the Marketplace plugin |
| **User types** | Claude slash commands (`/plugin …`, `/pipefy:…`) — the model cannot invoke them |
| **User in browser** | OAuth for hosted (`claude mcp login …`), Cursor's own sign-in for the Marketplace plugin, or `/pipefy:pipefy-login` / `pipefy auth login` |

## Tools needed

Setup is outside the Pipefy MCP tool surface. After auth succeeds, verify with:

| Tool (MCP) | CLI equivalent | Read-only |
|------------|----------------|-----------|
| `list_organizations` | `pipefy org list` | Yes |
| `get_organization` | `pipefy org get` | Yes |

## Steps

1. **Choose one path** — ask the user; do not pick silently.

   If they only say “Claude Code” (no path), ask a **closed** question:

   > Hosted MCP (zero local Python, `mcp.pipefy.com`) or the Claude Code plugin (slash commands + local CLI)? If you’re unsure, Hosted is the usual first try.

   If they only say “Cursor” (no path), ask a **closed** question:

   > Cursor Marketplace plugin (hosted server, browser sign-in, no local Python) or the Quick-install script (local CLI, plus the tools that read local files)? If you’re unsure, the plugin is the usual first try.

   | Path | README section | Outcome |
   |------|----------------|---------|
   | Cursor Marketplace plugin | [Cursor Marketplace plugin](../../../README.md#6-cursor-marketplace-plugin) | Hosted `mcp.pipefy.com`, browser sign-in, no local Python |
   | Hosted MCP | [Hosted MCP](../../../README.md#1-hosted-mcp-claude-code) | HTTPS `mcp.pipefy.com` (remote-safe tools) |
   | Local toolkit | [Quick install](../../../README.md#3-quick-install-script) | `install.sh` → local server + CLI, including the tools that read local files |
   | Claude Code plugin | [Claude Code plugin](../../../README.md#2-claude-code-plugin) | Marketplace + slash install/login |
   | CLI only | [CLI](../../../README.md#4-cli-only) | `pipefy` on PATH; no MCP |

   **Never** register both a hosted HTTP and a local stdio/plugin Pipefy server, whatever they are named: a second registration shadows the one you meant to use. Switching between paths is remove-then-add — [`docs/uninstall.md`](../../../docs/uninstall.md#switching-channels). On Cursor that applies to the Marketplace plugin and any entry in `~/.cursor/mcp.json`, including one written by `install.sh --client cursor`.

2. **Execute the chosen README block** — run it in the shell, or print it for the user to paste (required for Claude slash commands). Do not reorder the plugin sequence: marketplace → `/plugin install pipefy` → `/pipefy:install` → `/pipefy:pipefy-login`.

   Cursor Marketplace plugin: the user installs **Pipefy** from Cursor's plugin UI and fully restarts Cursor. Nothing to run, and the `/pipefy:…` commands do not exist on this path.

3. **Auth** — Cursor plugin: finish Cursor's own sign-in prompt (Customize / MCP). Hosted: finish the client browser OAuth prompt (`claude mcp login <name>` if status is Needs authentication). Local/plugin/CLI: `pipefy auth login` or `/pipefy:pipefy-login` (see README). Service accounts: [`docs/config.md`](../../../docs/config.md).

4. **Verify**

   - Shell (local / plugin / CLI): `pipefy --version`. The Cursor plugin installs no CLI, so verify it with the MCP call below instead.
   - MCP: call `list_organizations` (needs no id — the natural first read; confirms the credential works and surfaces the org ids other tools need) or another read-only tool the user allows
   - Run `curl -LsSf https://raw.githubusercontent.com/pipefy/ai-toolkit/main/uninstall.sh | sh -s -- --scan` (reports only, removes nothing; `./uninstall.sh --scan` from a checkout does the same) and confirm it reports exactly one registration, for the path you chose. A Marketplace-only install writes nothing to `~/.cursor/mcp.json`, so the plugin is not a finding: on that path the scan should report none. It matches on what an entry **runs** — the `pipefy-mcp-server` command, a known runner invoking it, or the host `mcp.pipefy.com` — so a server registered under any other name is still found. Exit `0` nothing found, `1` findings remain, `2` a source could not be inspected.

## Success criteria

- The `--scan` above reports one registration, for the chosen path (none for the Cursor plugin, which it cannot see; nothing for CLI-only).
- Auth completed.
- Read-only MCP call or `pipefy --version` succeeds.

## Failure modes

| Symptom | Likely cause | Recovery |
|---------|--------------|----------|
| Slash commands missing | Plugin not installed | README [Claude Code plugin](../../../README.md#2-claude-code-plugin) — marketplace + install first |
| More than one Pipefy MCP registration | Hosted + local/plugin both registered, possibly under different names | The `--scan` above names each one and where it lives; remove-then-add recipes in [`docs/uninstall.md`](../../../docs/uninstall.md#switching-channels). A plugin-provided server ranks below user scope, so removing the user entry alone falls through to it: `claude mcp remove <name> -s user` (or the client's settings) |
| Two Pipefy servers in Cursor | Marketplace plugin plus an entry in `~/.cursor/mcp.json` | Keep one. `--scan` names the user-config entry (the key is free text); delete that key, or uninstall the plugin. [`docs/uninstall.md`](../../../docs/uninstall.md#to-the-cursor-marketplace-plugin) |
| `/pipefy:install` or `/plugin …` offered in Cursor | Those are Claude Code commands | Do not run them; they install the CLI. Stay in Cursor's plugin UI. Skills may still appear as `/pipefy-*` palette entries |
| **Pipefy** is missing from Cursor's plugin catalog | The listing is not published yet | Offer README [Quick install](../../../README.md#3-quick-install-script) with `--client cursor`, saying first that it installs the local CLI and server the user was avoiding. From there they are on the Quick install path: `pipefy auth login`, `pipefy --version` |
| Cursor sign-in fails with `unauthorized_client` or `Invalid client credentials` | The plugin's OAuth client is rejected at the token endpoint | Re-triggering repeats the same failing call. Uninstall the plugin, then offer the Quick install fallback above |
| Cursor sign-in never completed, no error | Browser prompt dismissed | Re-trigger sign-in from Cursor Customize (MCP). `pipefy auth login` does not apply; this path has no CLI |
| `Needs authentication` after hosted add | OAuth not finished | `claude mcp login <name>` + browser |
| `pipefy: command not found` | CLI not on PATH | `/pipefy:install` or README [CLI](../../../README.md#4-cli-only); check `$HOME/.local/bin` |
| MCP tools empty / auth errors | Login not done | Re-run login; service accounts → `docs/config.md` |
| macOS `errSecInvalidOwnerEdit` | Keychain write | [`packages/mcp/README.md`](../../../packages/mcp/README.md) |

## See also

- [`README.md#installation`](../../../README.md#installation)
- [`docs/uninstall.md`](../../../docs/uninstall.md) — `uninstall.sh --scan`, teardown, and switching between hosted, local, and plugin
- [`skills/README.md`](../../README.md)
