---
name: github-bot
description: Interact with the GitHub API as the joelclawgithub[bot] app. Use when creating PRs, pushing commits, managing issues, checking CI status, listing repos, or any GitHub API operation. Triggers on "create a PR", "push to GitHub", "open an issue", "check CI", "list repos", "merge PR", "GitHub API", or any task requiring programmatic GitHub access. All actions appear as joelclawgithub[bot], not as @joelhooks.
---

# GitHub Bot

Interact with GitHub API via the `joelclawgithub[bot]` GitHub App. Acts as a bot identity with access to all 280+ repos across @joelhooks personal and org accounts.

## Authentication

Generate a 1-hour installation token:

```bash
TOKEN=$(SKILL_DIR/scripts/github-token.sh)
```

Use in API calls:

```bash
curl -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/...
```

Token expires in 1 hour. Generate a new one if a request returns 401.

## Secrets

Stored in agent-secrets (do not hardcode):

| Secret | Content |
|---|---|
| `github_app_id` | App ID (2867136) |
| `github_app_client_id` | Client ID |
| `github_app_installation_id` | Installation ID |
| `github_app_pem` | RSA private key |

## Bot Identity

- Commits: `joelclawgithub[bot] <2867136+joelclawgithub[bot]@users.noreply.github.com>`
- All API actions (comments, reviews, PRs) show as `joelclawgithub[bot]`
- Has read/write access to: contents, issues, PRs, actions, deployments, environments, secrets, packages, workflows, checks, statuses, hooks, projects

## Logging

Log all GitHub write operations with slog:

```bash
slog write --action "ACTION" --tool "github-bot" --detail "what was done" --reason "why"
```

Actions: `create-pr`, `push-commit`, `create-issue`, `merge-pr`, `create-release`, `update-workflow`, etc.

## Pagination

GitHub API paginates at 100 items. For full listing:

```bash
PAGE=1
while true; do
  RESULT=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/endpoint?per_page=100&page=$PAGE")
  # process $RESULT
  [ "$(echo "$RESULT" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')" -lt 100 ] && break
  PAGE=$((PAGE+1))
done
```
