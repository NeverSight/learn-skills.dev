---
name: aikido-security-remediator
description: Access Aikido Security through its API, pull open issue groups, triage findings, and execute first-pass fixes in your repository. Use when asked to review Aikido alerts, remediate dependency or SAST findings, or close security issues.
---

# Aikido Security Remediator

Use an API-first workflow for Aikido findings. Start by fetching open issues from Aikido, then fix the highest-impact findings directly in code or package manifests.

## Required Environment

- `AIKIDO_CLIENT` and `AIKIDO_SECRET` in `.env` (for OAuth client credentials).
- Optional `AIKIDO_ACCESS_TOKEN` in `.env` to skip OAuth exchange.
- Optional `AIKIDO_API_BASE` in `.env` (default: `https://app.aikido.dev/api`).

Do not `source .env` in shell sessions; parse it as plain text because the repository may contain values that are not shell-safe.

## Workflow

1. Fetch open issue groups first:
   - `python scripts/aikido_open_issue_groups.py --base-url "https://app.aikido.dev/api" --details --output /tmp/aikido-open-issues.json --markdown-summary`
2. Build a remediation queue:
   - Prioritize by severity (`critical` -> `high` -> `medium` -> `low`), then exploitability and blast radius.
   - Prefer findings with clear package/file ownership in the repository.
3. Attempt fixes before reporting:
   - For `SAST`: patch vulnerable code paths first.
   - For dependency/SCA findings: update `package.json`/workspace manifests or `overrides`, then regenerate lock data.
4. Verify every change:
   - Run targeted tests for touched apps/packages.
   - Run build for touched app/package when changes are substantial.
5. Report unresolved findings only after at least one concrete fix attempt.

## Lockfile Policy

- Never hand-edit lockfiles (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`).
- Change the manifest (`package.json`, workspace dependency, or override) and let the package manager update the lockfile automatically.
- For targeted dependency upgrades, prefer scoped commands.

## API Endpoints

Base URL: `https://app.aikido.dev/api` (docs at `https://apidocs.aikido.dev/`).

- `POST /oauth/token` — exchange client credentials for bearer token
- `GET /public/v1/open-issue-groups` — list open issue groups
- `GET /public/v1/issues/groups/{issueGroupID}` — get issue group detail
- `PUT /public/v1/issues/groups/{issueGroupID}/ignore` — ignore an issue group
- `PUT /public/v1/issues/groups/{issueGroupID}/snooze` — snooze an issue group

See `references/remediation-playbook.md` for endpoint usage, triage rules, and fix sequencing.

## Execution Rules

- Query Aikido API before searching local code for assumptions about findings.
- Keep fixes minimal and local to the reported vulnerability.
- Avoid broad refactors while remediating security findings.
- If a finding is not reproducible or not in scope for this repo, document exact evidence and blockers.
