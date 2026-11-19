---
name: agent-github-access
description: "Prepare GitHub CLI/API access for an agent using an existing GitHub App."
version: 1.0.0
author: koalyptus
license: MIT
platforms: [linux, macos, windows]
---

# Prepare Agent GitHub Access

Prepare the current repository for GitHub CLI and API calls as a GitHub App bot.

## When to use

- The agent needs to use `gh` or the GitHub API as an installed GitHub App.
- Triggers: "prepare agent GitHub access", "authenticate gh as the bot", "use the GitHub App for this repository".

Do not use this skill to configure commit author identity or `git push` authentication. Use `agent-git-setup` for bot commit attribution. Push authentication remains controlled by Git's configured credential mechanism.

## Requirements

- The GitHub App already exists, has a generated private key, and is installed for the current repository. The account owner creates the App, downloads its key, and grants its installation access.
- The App has only the repository permissions needed for the requested API actions. Installation access controls which repositories the token can reach; this skill does not grant or narrow that access.
- The current checkout has a GitHub.com `origin` remote.
- `gh` and PowerShell 7+ (`pwsh.exe`) on Windows. Run the native workflow in a PowerShell 7 session and keep token minting and subsequent `gh` commands in that same process. On Linux and macOS, Bash, Python 3, and Python `cryptography` are required for token minting.
- The private key file is outside the repository and readable by the agent. The user remains responsible for its file permissions.

## Workflow

1. Select the existing App configuration without asking for PEM paths or reading credential contents into the conversation:
   - Honor `AGENT_GIT_CREDENTIALS` or explicit App credentials already selected by the harness.
   - Otherwise use the default `${XDG_CONFIG_HOME:-$HOME/.config}/agent-git-setup/credentials.env` when it exists.
   - Otherwise inspect only filenames in `${XDG_CONFIG_HOME:-$HOME/.config}/agent-git-setup/credentials.d/`. If exactly one `credentials-<APP_ID>.env` exists, select that App. If several exist, show the public App IDs from their filenames and ask the account owner which App to use. Do not guess or silently choose among multiple Apps. After the account owner selects an ID, pass `--app-id <APP_ID>` to the Bash minter or `-AppId <APP_ID>` to the PowerShell minter. If none exists, stop and report that the one-time App credential setup is missing.
   - Never ask for private-key bytes or display credential-file contents. Do not create or rewrite credentials in this access skill.
2. Mint and export a short-lived token using the platform's bundled minter. On Linux or macOS:

   ```bash
   source <("$MINT_TOKEN_BASH" --shell)
   ```

   Set `MINT_TOKEN_BASH` to the installed skill's bundled `scripts/mint-token.sh`. If an App was selected from a per-App filename, add `--app-id "$SELECTED_APP_ID"`; if the harness provides an explicit credentials path, add `--credentials "$AGENT_GIT_CREDENTIALS"`. Do not pass a repository to the minter; it creates an installation-scoped token using the selected App configuration. Do not write token output to disk.

   On Windows, first verify that the active shell is PowerShell 7 or later with `$PSVersionTable.PSVersion.Major`. If it is below 7, start `pwsh.exe` and continue the entire mint-and-verify workflow there; do not invoke the minter from Windows PowerShell 5.1 (`powershell.exe`). Keep token minting and all subsequent `gh` commands in the same PowerShell 7 process so the exported token is available to them:

   ```powershell
   & $MINT_TOKEN_POWERSHELL -AppId $SelectedAppId
   ```

   Set `MINT_TOKEN_POWERSHELL` to the installed skill's bundled `scripts/mint-token.ps1`. Pass `-AppId $SelectedAppId` only when you selected a per-App file; pass `-Credentials $env:AGENT_GIT_CREDENTIALS` when the harness selected an explicit file. It exports the token and signed attestation into the current PowerShell process. No Bash, Python, or separate .NET package is needed on this path.

3. Verify API access to the current repository with `gh` using the current working directory, for example `gh repo view --json nameWithOwner --jq .nameWithOwner`. If the checkout has no GitHub `origin`, the API check fails, or the token lacks access, follow the account-owner authentication fallback below. Report the bot actor from `AGENT_GIT_TOKEN_ACTOR`; do not claim bot access if verification fails.

## If bot authentication fails

If credential resolution, token minting, signature verification, or repository access fails, stop before making any GitHub changes as the bot. Explain the failure and the action that would be attempted. Ask the account owner explicitly before using their configured GitHub CLI identity:

> GitHub App bot access failed because `<reason>`. May I perform `<requested actions>` on `<repo>` using the currently configured account owner `gh` account for this session? Those actions will be attributed to that account.

- If the account owner declines, gives no answer, or no current GitHub.com `gh` account is configured, stop without making API changes. Explain how to repair App access or authenticate `gh`; never ask the user to paste a token or private key.
- Only after explicit approval, clear `GH_TOKEN`, `GH_ENTERPRISE_TOKEN`, `GITHUB_TOKEN`, and the `AGENT_GIT_TOKEN_*` attestation variables from the active process so `gh` cannot reuse the failed or stale bot token. Do not alter stored `gh` credentials or App credential files.
- Verify the active identity with `gh api user --jq .login`, show the login to the account owner, then verify access to the current repo with `gh repo view --json nameWithOwner --jq .nameWithOwner`. Continue only if both checks succeed and the reported login is the account owner account the user approved. Otherwise stop and report the failure.
- This approval is limited to the named API/CLI actions in the current repo and session. It does not authorize bot-attributed commits, changes to Git identity, credential helpers, remotes, or pushes.

## Later sessions

The existing credentials file contains only the public App ID and PEM path. Installation tokens expire after about one hour and are not persisted. For each new session that performs GitHub operations, run the platform-appropriate minter again using the harness's existing credential selection to export a fresh `GH_TOKEN` and attestation, then verify access against the current repository if authentication or permissions may have changed.

`GH_TOKEN` authenticates `gh` and API requests as the App bot. A failed bot flow can use the account owner's configured `gh` identity only through the explicit session-scoped approval above. Neither path sets Git commit identity, configures a push credential helper, or changes Git remotes, hooks, branches, or worktrees.