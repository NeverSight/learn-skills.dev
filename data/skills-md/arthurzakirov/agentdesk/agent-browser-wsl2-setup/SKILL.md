---
name: agent-browser-wsl2-setup
description: Install and configure `agent-browser` on a Windows machine with WSL2 after a browser path is already working. Use when a user wants the `agent-browser` CLI, its downloaded runtime, the `vercel-labs/agent-browser` repository, or an `agent-browser` attachment to a Windows host browser bridge from WSL2.
---

# Agent Browser WSL2 Setup

This skill owns `agent-browser` setup only.

Browser availability belongs in [`$wsl2-browser-setup`](../wsl2-browser-setup/SKILL.md). Use that skill first if neither of these is already true:

- native Linux `google-chrome` inside WSL2 works for real browsing and sign-in
- a Windows host browser bridge is reachable from WSL2 on `/json/version`

## Bootstrap Split

On a new machine, run these two commands directly from the AI:

```bash
npm install -g agent-browser
agent-browser install
```

Then have the human run this interactive command:

```bash
npx skills add vercel-labs/agent-browser
```

Important:

- `npm install -g agent-browser` is non-interactive and should be run by the AI when possible
- `agent-browser install` is non-interactive and should be run by the AI when possible
- `npx skills add vercel-labs/agent-browser` is interactive and should be run by the human

After the human finishes the interactive `npx skills add ...` flow, continue with the runtime setup script.

## Runtime Setup

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/agent-browser-wsl2-setup/scripts/setup-agent-browser-runtime.sh"
```

The script:

- installs `agent-browser` if missing
- runs `agent-browser install` if needed
- clones `vercel-labs/agent-browser` if missing

## Mode A: Native WSL Browser

If the browser path from `$wsl2-browser-setup` is native Linux Chrome inside WSL2, test `agent-browser` directly:

```bash
agent-browser doctor --offline --quick
agent-browser open https://example.com
agent-browser snapshot -i -c
```

If this still hangs even though manual browsing works, stop debugging the browser here and use Mode B.

## Mode B: Windows Host Browser Bridge

If the browser path from `$wsl2-browser-setup` is a Windows host browser bridge, attach `agent-browser` to that existing CDP endpoint:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/agent-browser-wsl2-setup/scripts/connect-windows-browser.sh" --session windows-host --bridge-port 9333
agent-browser --session windows-host get title
agent-browser --session windows-host snapshot -i -c
```

This was the proven control path before the native browser path was cleaned up.

## Legacy Combined Wrapper

[`scripts/setup-agent-browser-wsl2.sh`](./scripts/setup-agent-browser-wsl2.sh) still exists as a compatibility wrapper for the older one-shot Windows bridge flow.

Prefer the split skills instead:

1. `$wsl2-browser-setup`
2. `$agent-browser-wsl2-setup`

## Bundled Resources

- Use [`scripts/setup-agent-browser-runtime.sh`](./scripts/setup-agent-browser-runtime.sh) to install the CLI, runtime, and repo clone
- Use [`scripts/connect-windows-browser.sh`](./scripts/connect-windows-browser.sh) to attach `agent-browser` to a Windows browser bridge that is already reachable from WSL2
- Use [`references/architecture.md`](./references/architecture.md) for the boundary between browser setup and `agent-browser` setup
- Use [`references/troubleshooting.md`](./references/troubleshooting.md) when `agent-browser` itself fails
- Use [`references/dead-ends.md`](./references/dead-ends.md) for the coupling mistakes this split is meant to avoid
