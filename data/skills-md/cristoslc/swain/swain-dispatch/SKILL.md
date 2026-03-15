---
name: swain-dispatch
description: "Dispatch swain artifacts to background agents via GitHub Issues. Creates a GitHub Issue with the artifact content and triggers the Claude Code Action workflow for autonomous implementation. Use when the user wants to offload work to a background agent."
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob
metadata:
  short-description: Dispatch artifacts to background agents via GitHub
  version: 1.0.0
  author: cristos
  license: MIT
  source: swain
---
<!-- swain-model-hint: sonnet, effort: low -->

# Agent Dispatch

Dispatches swain-design artifacts to background agents via GitHub Issues. The agent runs autonomously using `anthropics/claude-code-action@v1` on a GitHub Actions runner.

## Prerequisites

Three things must be in place before dispatch works:

1. **Claude GitHub App** — installed on the repo from https://github.com/apps/claude (grants Contents, Issues, Pull Requests read/write)
2. **Workflow file** — `.github/workflows/claude.yml` (or `agent-dispatch.yml`) with the `claude-code-action` step
3. **`ANTHROPIC_API_KEY` repo secret** — API key (not Max/Pro subscription; per-token billing required)

## Step 0 — Preflight check

Run this before every dispatch. If any check fails, stop and show the setup instructions.

```bash
# 1. Check gh auth
gh auth status 2>/dev/null || { echo "FAIL: gh not authenticated"; exit 1; }

# 2. Check workflow file
WORKFLOW_FILE=""
for f in .github/workflows/claude.yml .github/workflows/agent-dispatch.yml; do
  [[ -f "$f" ]] && WORKFLOW_FILE="$f" && break
done

# 3. Check API key secret
OWNER_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
HAS_KEY=$(gh api "repos/${OWNER_REPO}/actions/secrets" --jq '.secrets[].name' 2>/dev/null | grep -c ANTHROPIC_API_KEY || true)
```

**If workflow file is missing**, show:
> **Dispatch setup required.** No workflow file found.
>
> Create `.github/workflows/claude.yml`:
> ```yaml
> name: Claude Code
>
> on:
>   issue_comment:
>     types: [created]
>   pull_request_review_comment:
>     types: [created]
>   issues:
>     types: [opened, assigned]
>
> jobs:
>   claude:
>     if: |
>       (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
>       (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
>       (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
>     runs-on: ubuntu-latest
>     permissions:
>       contents: write
>       issues: write
>       pull-requests: write
>       id-token: write
>     steps:
>       - uses: actions/checkout@v4
>
>       - uses: anthropics/claude-code-action@v1
>         with:
>           anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
> ```
>
> Then commit and push before retrying dispatch.

**If API key secret is missing**, show:
> **Missing `ANTHROPIC_API_KEY` repo secret.**
>
> Set it with: `gh secret set ANTHROPIC_API_KEY --repo {owner}/{repo}`
>
> Note: This must be an API key (per-token billing), not a Max/Pro subscription token.

## Dispatch workflow

### Step 1 — Resolve the artifact

Parse the user's request to identify the artifact ID (e.g., `SPEC-025`, `SPIKE-007`).

```bash
ARTIFACT_ID="SPEC-025"  # from user input
ARTIFACT_PATH="$(find docs/ -path "*${ARTIFACT_ID}*" -name "*.md" -print -quit)"
```

If not found, report the error and stop.

### Step 2 — Read the artifact

Read the full artifact content. This becomes the issue body.

### Step 3 — Read dispatch settings

Check `swain.settings.json` for dispatch configuration:

```bash
jq -r '.dispatch // {}' swain.settings.json 2>/dev/null
```

Defaults:
- `model`: `claude-sonnet-4-6`
- `maxTurns`: `15`
- `labels`: `["agent-dispatch", "swain"]`
- `autoTrigger`: `true`

### Step 4 — Create the GitHub Issue

```bash
gh issue create \
  --title "[dispatch] ${ARTIFACT_TITLE}" \
  --body "$(cat <<'EOF'
## Dispatched Artifact: ${ARTIFACT_ID}

This issue was created by `swain-dispatch` for background agent execution.

### Instructions

Implement the artifact below. Follow the acceptance criteria. Create a PR when done.

---

${ARTIFACT_CONTENT}
EOF
)" \
  --label "agent-dispatch" --label "swain"
```

Capture the issue number from the output.

### Step 5 — Trigger the workflow

If `autoTrigger` is true (default):

```bash
OWNER_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
gh api "repos/${OWNER_REPO}/dispatches" \
  -f event_type="agent-dispatch" \
  -f client_payload[artifact]="${ARTIFACT_ID}" \
  -f client_payload[issue_number]="${ISSUE_NUMBER}" \
  -f client_payload[model]="${MODEL}" \
  -f client_payload[max_turns]="${MAX_TURNS}"
```

### Step 6 — Report

Tell the user:
> Dispatched ${ARTIFACT_ID} to background agent.
> Issue: ${ISSUE_URL}
> Workflow will run on the next available runner.
> Monitor progress in the issue comments.

## Manual dispatch

If the user prefers manual dispatch (or `autoTrigger` is false), skip Step 5 and tell them:
> Issue created: ${ISSUE_URL}
> To trigger the agent, comment `@claude` on the issue.

## Checking dispatch status

When the user asks about dispatch status:

```bash
gh issue list --label agent-dispatch --state open --json number,title,updatedAt
```

Show open dispatch issues with their last update time.

## Trigger timing

The Claude Code Action workflow fires on different GitHub events depending on how `@claude` is mentioned:

| Mention location | Event | When it fires |
|------------------|-------|--------------|
| Issue body at creation | `issues.opened` | Immediately when issue is created |
| Comment on existing issue | `issue_comment.created` | When the comment is posted |

**Gotcha:** If the workflow file didn't exist when the issue was created, the `issues.opened` event was missed. In that case, add a follow-up comment containing `@claude` to trigger via `issue_comment.created` instead.

The default dispatch workflow (Step 4 + Step 5) uses `repository_dispatch` which is independent of `@claude` mentions. The timing gotcha only applies when:
- Using manual dispatch (Step 5 skipped)
- The workflow relies on `issues.opened` or `issue_comment.created` events
