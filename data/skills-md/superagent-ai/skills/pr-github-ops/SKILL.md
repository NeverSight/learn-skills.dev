---
name: pr-github-ops
description: Post Superagent PR security scan findings as inline GitHub pull request review comments using the authenticated gh CLI. Use whenever you need to comment on a PR scan finding, manage Superagent PR labels, complete a GitHub check run, or avoid posting findings as general PR thread comments. Trigger for any Superagent sandbox PR scan handoff that owns GitHub side effects via gh.
---

# PR GitHub operations

Superagent PR scans run in a sandbox with an authenticated `gh` CLI. You own GitHub side effects after handoff: inline finding comments, managed labels, and check-run completion.

Read `pr-scan-context.json` first. It contains `owner`, `repo`, `prNumber`, `headSha`, `checkRunId`, `reviewedFindingPaths`, and `dismissedFingerprints`.

## Critical rule: inline comments, not thread comments

`gh pr comment` creates **issue comments** on the PR conversation thread. That is wrong for actionable findings.

For each finding with a changed file and diff line, post a **pull request review comment** anchored to that line in the Files changed view.

| Goal | Wrong | Right |
|------|-------|-------|
| Comment on a finding at a diff line | `gh pr comment` | `gh api` review comment or review with `comments[]` |
| Summary-only note with no line anchor | `gh pr comment` is acceptable | optional |

If you already posted findings with `gh pr comment`, delete those issue comments and repost inline before finishing the scan.

## Inspect before posting

```bash
owner=OWNER
repo=REPO
pr=PR_NUMBER

# Existing inline review comments
gh api "repos/${owner}/${repo}/pulls/${pr}/comments" --paginate

# Existing general PR thread comments (avoid duplicating here)
gh api "repos/${owner}/${repo}/issues/${pr}/comments" --paginate

# PR diff files and patches (confirm path + line are in the diff)
gh api "repos/${owner}/${repo}/pulls/${pr}/files" --paginate
```

Skip findings when:
- `file` is in `reviewedFindingPaths`
- fingerprint already exists in an inline comment
- you already posted an inline finding on that `file` this run (one inline finding per file)

## Finding comment body format

Every finding comment must include the Superagent marker and fingerprint.

```markdown
<!-- brin-pr-finding -->
**P0:** Workflow uses pull_request_target trigger for untrusted fork PRs

Short evidence sentence here.

Short recommendation sentence here.

<!-- superagent-finding-fingerprint:HEX_SHA256 -->
```

Severity to priority: `critical` → P0, `high` → P1, `medium` → P2, `low` → P3.

Fingerprint: SHA-256 of the normalized comment body **before** appending the fingerprint line. Lowercase, collapse whitespace, remove the marker and any existing fingerprint comment.

```bash
body='<!-- brin-pr-finding -->
**P1:** Overly broad permissions: write-all in privileged workflow

Grants broad write access to GITHUB_TOKEN.

Replace with least-privilege job permissions.'

printf '%s' "$body" \
  | sed 's/<!-- brin-pr-finding -->//g' \
  | tr '[:upper:]' '[:lower:]' \
  | tr -s '[:space:]' ' ' \
  | sed 's/^ //;s/ $//' \
  | sha256sum \
  | awk '{print $1}'
```

Append the fingerprint as the last line of the comment body.

Use `short_evidence` and `short_recommendation` in inline comments. Keep them terse.

## Post inline review comments with gh api

`line` must be a line number on the **RIGHT** (added) side of the PR diff for `path`. Confirm with the PR files API or diff before posting.

### Single inline comment

```bash
head_sha=HEAD_SHA_FROM_CONTEXT

gh api \
  "repos/${owner}/${repo}/pulls/${pr}/comments" \
  -X POST \
  -f commit_id="$head_sha" \
  -f path=".github/workflows/example.yml" \
  -f side=RIGHT \
  -F line=12 \
  -f body="$comment_body"
```

Use `-F line=12` for numeric fields. Use `-f` for strings.

### Batch inline comments (preferred for multiple findings)

Write `review.json`:

```json
{
  "commit_id": "HEAD_SHA",
  "event": "COMMENT",
  "body": "<!-- brin-pr-finding -->\nSuperagent found 2 security concern(s).",
  "comments": [
    {
      "path": ".github/workflows/example.yml",
      "line": 4,
      "side": "RIGHT",
      "body": "<!-- brin-pr-finding -->\n**P0:** ...\n\n...\n\n<!-- superagent-finding-fingerprint:abc123... -->"
    },
    {
      "path": ".github/workflows/example.yml",
      "line": 8,
      "side": "RIGHT",
      "body": "<!-- brin-pr-finding -->\n**P1:** ...\n\n...\n\n<!-- superagent-finding-fingerprint:def456... -->"
    }
  ]
}
```

Post it:

```bash
gh api \
  "repos/${owner}/${repo}/pulls/${pr}/reviews" \
  -X POST \
  --input review.json
```

Post at most 50 inline comments per review. If you have more findings, split across multiple reviews.

### Fallback when no diff line exists

Only when a finding has no valid `file` + `line` in the PR diff, post a single consolidated issue comment:

```bash
gh api \
  "repos/${owner}/${repo}/issues/${pr}/comments" \
  -X POST \
  -f body="$fallback_body"
```

Never post the same finding both inline and on the thread.

## Delete stale or misplaced comments

```bash
# Delete inline review comment
gh api "repos/${owner}/${repo}/pulls/comments/COMMENT_ID" -X DELETE

# Delete general PR thread comment
gh api "repos/${owner}/${repo}/issues/comments/COMMENT_ID" -X DELETE
```

Delete stale Superagent finding comments whose fingerprints are no longer in the current findings set. Delete thread comments you replaced with inline comments.

## Managed labels

Only touch Superagent managed labels. Preserve all unrelated labels.

```bash
gh pr edit "$pr" --repo "${owner}/${repo}" --add-label "pr:flagged"
gh pr edit "$pr" --repo "${owner}/${repo}" --remove-label "pr:verified"
```

Clean scan:

```bash
gh pr edit "$pr" --repo "${owner}/${repo}" --remove-label "pr:flagged" --add-label "pr:verified"
```

## Complete the check run

Use `checkRunId` from context. Always set `status=completed`.

```bash
check_run_id=CHECK_RUN_ID_FROM_CONTEXT

gh api \
  "repos/${owner}/${repo}/check-runs/${check_run_id}" \
  -X PATCH \
  -f status=completed \
  -f conclusion=action_required \
  -f 'output[title]=PR requires security review' \
  -f 'output[summary]=2 security concern(s) detected.' \
  -f 'output[text]=Optional longer details.'
```

Conclusions:
- `success` — clean scan
- `action_required` — findings need review
- `neutral` — inconclusive scan

## End-to-end workflow

1. Read `pr-scan-context.json` and PR input JSON.
2. Run security analysis (other skills) and produce findings with `file`, `line`, `severity`, `title`, `short_evidence`, `short_recommendation`.
3. List existing inline and thread comments; compute fingerprints; skip dismissed/reviewed/duplicate findings.
4. Post findings as inline review comments with `gh api` (single comment or batch review). Do not use `gh pr comment` for findings.
5. Delete stale or misplaced Superagent finding comments.
6. Set managed PR labels.
7. Complete the check run.
8. Write the agent receipt JSON with `github_operations_completed: true` and `posted_comment_ids` when available.
