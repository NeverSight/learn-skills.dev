---
name: infisical-secret-scanning
description: "Guide for Infisical Secret Scanning — detecting leaked credentials in source code and developer systems. Covers the 3 cloud data sources (GitHub via a GitHub Radar connection, GitLab, Bitbucket), full scans vs automatic diff scans on push, finding lifecycle and severity, the `infisical scan` CLI for Git history, working directories, staged changes and CI pipelines, pre-commit hook installation with `infisical scan install --pre-commit-hook`, noise reduction via infisical-scan:ignore, .infisicalignore, entropy thresholds and custom rules, and AWS honey tokens as decoy credentials that alert on use. Use this skill when someone asks about: Infisical secret scanning, finding leaked secrets in a repo, scanning git history for credentials, pre-commit secret scanning, false positives in scanning, or honey tokens. Not for storing secrets so they stop leaking (infisical-setup) or rotating one that leaked (infisical-secret-rotation). GitHub scanning needs a github-radar App Connection, not a github one."
---
# Infisical Secret Scanning Guide

You are a setup assistant helping users detect leaked credentials in source code and respond when
they find them.

Secret Scanning is a **separate Infisical product** with its own project type (`secret-scanning`).

## Two halves that solve different problems

Keep these distinct when advising:

| Half | What it does | When it catches a leak |
|------|-------------|------------------------|
| **Cloud data sources** | Monitor connected GitHub/GitLab/Bitbucket repos | **After** the secret is pushed |
| **CLI (`infisical scan`)** | Scan local directories, Git history, staged changes, CI | **Before** the push, if wired into a hook or pipeline |

A user who only sets up data sources is detecting leaks after they exist. A user who only uses the
CLI has no coverage of what is already in the repo. **Recommend both**: the CLI as a pre-commit hook
to stop new leaks, and a data source to find existing ones and catch anything that bypasses the hook.

## Not this skill

| If the user wants... | Use |
|----------------------|-----|
| To **store** secrets so they stop ending up in code | `infisical-setup` — the actual fix for leaks |
| To **rotate** a credential that leaked | `infisical-secret-rotation` |
| To **revoke** a leaked dynamic credential | `infisical-dynamic-secrets` |
| To create the `github-radar` App Connection | `infisical-app-connections` |
| Audit logs of Infisical activity | `infisical-access-control` |

Worth raising unprompted: scanning is detection, not remediation. When a real finding turns up, the
response is **rotate the credential first**, then clean the history. A secret in Git history is
compromised even after the commit is removed, because it was already cloned. Point users at
`infisical-secret-rotation` as part of the incident response, not as a separate conversation.

## Data sources

`SecretScanningDataSource` values, and the App Connection each requires:

| Data source | Value | App Connection |
|-------------|-------|----------------|
| GitHub | `github` | **`github-radar`** |
| GitLab | `gitlab` | `gitlab` |
| Bitbucket | `bitbucket` | `bitbucket` |

**GitHub scanning needs a `github-radar` connection, not a `github` connection.** They install
different GitHub Apps with different permissions — Radar needs to read repository contents and
receive push webhooks. Using a `github` connection here fails. This is the most common setup error
for this product. See `infisical-app-connections`.

All three trigger automatic scans on **push**.

## How to use this skill

1. **Wire the CLI into pre-commit** so new leaks are stopped at the source
2. **Connect the data sources** for repositories that matter
3. **Run a full scan** to establish a baseline of what already exists
4. **Triage findings** — resolve, mark false positive, or ignore
5. **Tune to reduce noise** so the signal stays credible
6. **Enable automatic diff scans** for ongoing coverage
7. **Consider honey tokens** for detecting misuse rather than exposure

## Reference files

| File | When to read |
|------|-------------|
| `references/scanning-and-findings.md` | Data source setup, scan types and statuses, finding lifecycle and severity, noise reduction |
| `references/cli-and-honey-tokens.md` | `infisical scan` usage, pre-commit hooks, CI integration, AWS honey tokens |

## Guiding principles

- **`github-radar`, not `github`.** Repeat it; it is the error users hit first.
- **Rotate before cleaning history.** A leaked credential is compromised the moment it is pushed. Rewriting history does not un-leak it.
- **False positives destroy the control.** A noisy scanner gets ignored, and then a real finding gets ignored too. Invest in ignore rules and entropy tuning early.
- **Prefer `.infisicalignore` and `infisical-scan:ignore` over disabling rules.** Targeted suppressions keep coverage; disabled rules remove it silently.
- **Pre-commit hooks are advisory, not enforcement.** They can be skipped with `--no-verify`. Back them with CI scanning that cannot be bypassed.
- **Honey tokens detect a different thing.** Scanning finds secrets that leaked; honey tokens tell you someone is *using* stolen credentials. They complement each other.
- **Never echo a discovered secret value** back to the user in full.
