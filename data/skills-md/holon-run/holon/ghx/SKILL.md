---
name: ghx
description: "GitHub enhanced operations skill. Provides unified context collection and publishing commands for PR/issue workflows."
---

# GHX Skill

`ghx` is an enhanced reliability layer on top of `gh`, used by higher-level skills.
It standardizes common GitHub operations and prevents common agent mistakes (especially shell escaping and multi-line payload issues).

It provides two capabilities:
- Context collection with a stable artifact manifest
- Publishing for PR/review/comment workflows

## Environment Variables

- `GITHUB_OUTPUT_DIR`: artifact directory (caller-provided; defaults to a temp dir when unset)
- `GITHUB_CONTEXT_DIR`: context directory (default `${GITHUB_OUTPUT_DIR}/github-context`)
- `GITHUB_TOKEN` / `GH_TOKEN`: token used by `gh`
- `DRY_RUN`: preview mode for publish commands (`true|false`)

## Commands

Use `scripts/ghx.sh` as the entrypoint.

### Context collection

```bash
scripts/ghx.sh context collect holon-run/holon#123
scripts/ghx.sh context collect 123 holon-run/holon
```

### Publish commands

```bash
scripts/ghx.sh review publish --pr=holon-run/holon#123 --body-file=review.md --comments-file=review.json
scripts/ghx.sh pr create --repo=holon-run/holon --title="Title" --body-file=summary.md --head=feature/x --base=main
scripts/ghx.sh pr update --pr=holon-run/holon#123 --title="New title" --body-file=summary.md
scripts/ghx.sh pr comment --pr=holon-run/holon#123 --body-file=summary.md
# stdin body is also supported
scripts/ghx.sh pr comment --pr=holon-run/holon#123 --body-file=- <<'EOF'
Multiline body from stdin.
EOF
```

### Batch mode

```bash
scripts/ghx.sh batch run --batch=${GITHUB_OUTPUT_DIR}/publish-batch.json
```

Use batch mode when one run needs multiple publish actions.
Use direct commands for single-action publish.

## Contract Boundary

- Public contract for other skills:
  - Call `ghx.sh` commands.
  - Read `${GITHUB_CONTEXT_DIR}/manifest.json` for context artifacts.
  - Read `${GITHUB_OUTPUT_DIR}/publish-results.json` for publish execution results.
  - Use `publish-batch.json` schema when running `ghx.sh batch run` (defined below and in `references/github-publishing.md`).
- Integration guidance for third-party skills:
  - Prefer direct commands for single actions.
  - Use batch mode only when one run needs multiple publish actions.
  - Do not depend on undocumented fields or script internals outside this documented schema.

## Context Output Contract

`context collect` writes:
- `${GITHUB_CONTEXT_DIR}/manifest.json`
- Context files under `${GITHUB_CONTEXT_DIR}/github/` (for example `pr.json`, `pr.diff`, `comments.json`)

`manifest.json` is the source of truth for collected context:

```json
{
  "schema_version": "2.0",
  "provider": "ghx",
  "kind": "pr|issue",
  "ref": "owner/repo#123",
  "success": true,
  "artifacts": [
    {
      "id": "pr_metadata",
      "path": "github/pr.json",
      "required_for": ["review"],
      "status": "present|missing|error",
      "format": "json|text",
      "description": "What this artifact contains"
    }
  ],
  "notes": []
}
```

Consumers must use `artifacts[]` instead of assuming fixed context filenames.

## Publish Output Contract

Publish commands write `${GITHUB_OUTPUT_DIR}/publish-results.json` with per-action status and summary totals.

## Batch Input Contract (Public)

`ghx.sh batch run` consumes `${GITHUB_OUTPUT_DIR}/publish-batch.json` (or any path passed by `--batch`).

```json
{
  "version": "1.0",
  "pr_ref": "owner/repo#123",
  "actions": [
    {
      "type": "post_comment",
      "description": "optional",
      "params": {
        "body": "summary.md"
      }
    }
  ]
}
```

Schema summary:
- Top-level required fields: `pr_ref`, `actions`
- Top-level optional field: `version` (default `1.0`)
- Action required field: `type`
- Action optional fields: `description`, `params`
- `params` is action-specific payload; legacy inline action fields are also accepted.

Supported `type` values:
- `create_pr`
- `update_pr`
- `post_comment`
- `reply_review`
- `post_review`

## Notes

- Prefer `ghx` for multi-step or error-prone GitHub operations.
- `context collect` also prints a human-readable artifact summary; this is informational only.
- For long or multi-line text, never inline shell arguments; always write to a file and pass `--body-file`/`--comments-file`.
- Command selection:
  - single action: use direct commands (`review publish`, `pr create|update|comment`)
  - multiple actions in one run: use `batch run`

## Safety Rules (Text Payloads)

To reduce failure rate from quoting/newline/markdown escaping:

1. Never pass large markdown/JSON payloads inline on command line.
2. Always pass payloads via file arguments:
   - `ghx`: `--body-file`, `--comments-file` (`--body-file=-` is allowed to read from stdin)
   - raw `gh`: `--body-file`
3. Apply this rule to PR reviews, PR comments/description, issue comments, and issue creation.

Good:

```bash
cat > /tmp/issue-body.md <<'EOF'
## Summary
Detailed markdown with quotes, backticks, and newlines.
EOF
gh issue create --repo owner/repo --title "Bug report" --body-file /tmp/issue-body.md
```

Bad:

```bash
gh issue create --repo owner/repo --title "Bug report" --body "## Summary
Detailed markdown with quotes, backticks, and newlines."
```
