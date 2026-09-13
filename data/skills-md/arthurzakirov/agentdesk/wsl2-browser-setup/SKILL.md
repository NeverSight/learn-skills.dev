---
name: wsl2-browser-setup
description: Install and configure browsers for Windows plus WSL2. Use when a user wants native Linux Chrome inside WSL to work for normal browsing or sign-in flows, or when a tool in WSL needs a Windows host Chrome or Edge instance exposed over CDP. Prefer this skill before any tool-specific browser automation setup.
---

# WSL2 Browser Setup

This skill owns browser setup only.

It does not install or configure `agent-browser`. Use this skill first to make a browser path work from WSL2, then layer any specific automation client on top.

## Choose A Method

Use one of these methods depending on the task:

- Native WSL Chrome: best for interactive browsing, account sign-in, testing whether WSLg browsing works at all, and any case where the user wants Chrome running inside WSL itself
- Windows host browser bridge: best when a tool in WSL must control a Windows Chrome or Edge instance over CDP

## Method A: Native WSL Chrome

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh"
```

The script:

- verifies WSL2
- installs Linux `google-chrome` if it is missing
- writes the standard Windows `.wslconfig` networking settings
- tells the user when `wsl --shutdown` is required

After the script says restart is needed, have the human run:

```powershell
wsl --shutdown
```

Then reopen WSL and continue with the manual Chrome step.

## Manual Chrome Step

Open Linux Chrome:

```bash
google-chrome
```

In Chrome:

- open `chrome://settings/security`
- set `Use secure DNS` to `Off`
- do not leave it at `OS default (when available)`
- close all Chrome windows
- reopen `google-chrome`
- open `https://example.com`
- open one other normal external HTTPS site
- open the real sign-in page or app you need

If those pages open and the sign-in page renders normally, treat native WSL Chrome as working.

## Method B: Windows Host Browser Bridge

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh"
```

The script:

- verifies WSL2
- finds Windows Edge or Chrome
- launches the Windows browser with remote debugging enabled
- asks Windows for elevation to create the port proxy and firewall rule
- waits until WSL2 can reach the CDP endpoint

This method is still generic browser setup. It exposes a Windows browser to WSL2 over CDP, but it does not connect any specific client to it.

## Safe Smoke Tests

Use these first:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh" --check-only
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh" --check-only
google-chrome >/dev/null 2>&1 &
```

## What To Skip First

Do not start here:

- `dbus-x11`
- Ubuntu `chromium-browser`
- low-level DNS surgery
- random browser flags
- manual Windows firewall edits outside the bridge helper

These were explored and were either unnecessary or only useful after the shorter path had already failed.

## Bundled Resources

- Use [`scripts/setup-native-wsl-chrome.sh`](./scripts/setup-native-wsl-chrome.sh) for native Linux Chrome inside WSL2
- Use [`scripts/setup-windows-host-browser-bridge.sh`](./scripts/setup-windows-host-browser-bridge.sh) for a Windows Chrome or Edge CDP bridge into WSL2
- Use [`references/architecture.md`](./references/architecture.md) to choose between the two browser paths
- Use [`references/troubleshooting.md`](./references/troubleshooting.md) when the browser launches but browsing or sign-in still fails
- Use [`references/dead-ends.md`](./references/dead-ends.md) for the specific fixes that looked promising but did not shorten the path
