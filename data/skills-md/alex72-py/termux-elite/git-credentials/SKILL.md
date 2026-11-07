---
name: git-credentials
description: Diagnose git clone, fetch, and push authentication failures from Termux without exposing tokens or private keys (HTTPS tokens, SSH keys, host key prompts, wrong account, missing scopes). Use for Authentication failed, HTTP 403, Permission denied (publickey), repeated credential prompts, or key permission warnings. Do NOT use for network outages, wrong remote names, or non-authentication rejections such as non-fast-forward.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "git push failed,permission denied publickey,authentication failed,ssh key,http 403,credential prompt,host key verification failed,cannot push commits,keeps asking for password,github rejects me"
---
# Git Credentials

## Purpose
Diagnose `git clone`, `fetch`, and `push` authentication failures in Termux without ever exposing a token or private key.

## When to use
`Authentication failed`, HTTP 403, `Permission denied (publickey)`, `Host key verification failed`, repeated credential prompts, `UNPROTECTED PRIVATE KEY FILE`, or `Permission to X denied to Y`.

## When NOT to use
Network outages (`termux-network`), wrong remote names, or non-authentication push rejections such as non-fast-forward or protected-branch rules that name no credential problem.

## Preconditions
Run `sh scripts/check-git-auth.sh`. It redacts credentials embedded in remote URLs, lists key file names and modes only, and never reads key contents. If a remote URL embeds a token (`https://user:secret@host/...`), do not repeat it; that is itself a finding to fix.

## Decision tree
1. HTTPS remote: GitHub does not accept account passwords for git. Use a personal access token with minimal scope or `gh auth login` and `gh auth setup-git`. `gh auth status` does not print the token.
2. HTTP 403 with a valid token: the token lacks `repo` (or the fine-grained repository selection), the organization requires SSO authorization of the token, or the branch is protected.
3. `Permission to X denied to Y`: the authenticated account `Y` is not the one with access. Check which identity the credential helper supplies.
4. `credential.helper store` keeps tokens in plaintext in `~/.git-credentials`. Report it as a finding and prefer `gh` as the helper.
5. SSH remote: `Permission denied (publickey)`. List key file names in `~/.ssh` (never contents), confirm the matching `.pub` is registered with the account, and test `ssh -T git@github.com`. A successful GitHub test prints a greeting and exits with status 1; that is normal.
6. `UNPROTECTED PRIVATE KEY FILE`: `~/.ssh` should be mode 700 and private keys 600. Keys on shared storage cannot hold these modes; keep them under `$HOME` (see `storage-permissions`).
7. `Host key verification failed`: compare the fingerprint with the host's published one before accepting. Never set `StrictHostKeyChecking=no` as a fix.
8. Works only sometimes: Termux does not start an `ssh-agent`. Name the key with `IdentityFile` in `~/.ssh/config`, or start an agent per session.
9. Use one method per remote. Do not mix an embedded token and SSH on one repository.

## Example
- Situation: git push returns HTTP 403 although a token is configured.
- Without the skill: Embeds the token in the remote URL and enables `credential.helper store`.
- With the skill: Runs the redacting helper, checks token scope and SSO authorization, switches to `gh auth login` with `gh auth setup-git`, and reports any plaintext credential file as a finding.

## Safety
Generating keys, editing `~/.ssh/config`, storing credentials, and changing remotes mutate state and need confirmation. Never paste tokens or private keys into chat, logs, commits, or URLs. Only a `.pub` file is safe to display.

## Verification
Run the read-only `git ls-remote origin` and confirm refs list without a prompt. Push only when the user asks.

## Rollback
Keep the old remote URL and config lines in the report. Revoke any token or key that was exposed during the session at the provider.

## Handoffs
- `storage-permissions` when keys sit on shared storage.
- `termux-network` when the host is unreachable.
- `github-actions` when the real task is a CI failure.
- `termux-sshd` for inbound login, which is a different problem from git auth.

## Report
Remote scheme and host, the failing layer (token, scope, account, key, permissions, host key), the one change proposed, and the `git ls-remote` result.
