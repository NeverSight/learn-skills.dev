---
name: gerrit-review
description: Interact with Gerrit Code Review via the REST API — query changes, fetch diffs, post reviews with labels and inline comments, and manage change lifecycle.
license: Apache-2.0
compatibility: Requires git, curl, jq, and base64. Optional python3 for URL encoding.
metadata:
  author: Yuriy Novostavskyy (@yurnov)
  version: "1.1"
  repository: https://github.com/yurnov/gerrit-in-5-min
  keywords: [gerrit, code review, code review automation, developer tools]
---

# Gerrit Code Review Skill

This skill enables you to interact with a Gerrit Code Review instance through its REST API. Use it to query open changes, read diffs, post code reviews, and manage change lifecycle (submit, abandon, restore).

## Prerequisites

### Environment Variables

You **must** have the following environment variables set:

| Variable | Description | Example |
|---|---|---|
| `GERRIT_URL` | Base URL of the Gerrit instance (no trailing slash) | `https://gerrit.example.com` |
| `GERRIT_USERNAME` | HTTP username from Gerrit → Settings → Profile | `john.doe` |
| `GERRIT_HTTP_PASSWORD` | HTTP credential token from Gerrit → Settings → HTTP Credentials → Generate Password | `a1b2c3d4e5...` |

> [!IMPORTANT]
> The **HTTP password** is NOT the user's login password. It is a separate token generated in the Gerrit web UI under **Settings → HTTP Credentials → Generate Password**.

### Tools

- `curl` — used for all REST API calls
- `jq` — used for JSON parsing and pretty-printing
- `base64` — used for decoding file content responses

## Quick Start

Use the helper script at `scripts/gerrit_api.sh` (located relative to this SKILL.md) for common operations:

```bash
# Make the script executable (one-time)
chmod +x scripts/gerrit_api.sh

# Query open changes
./scripts/gerrit_api.sh query "status:open+limit:5"

# Get change details
./scripts/gerrit_api.sh get-change 12345

# List files changed in a revision
./scripts/gerrit_api.sh list-files 12345

# Get a file diff
./scripts/gerrit_api.sh get-diff 12345 "src/main/App.java"

# Get raw file content
./scripts/gerrit_api.sh get-content 12345 "src/main/App.java"

# Post a draft comment on a specific line
./scripts/gerrit_api.sh create-draft 12345 current '{"path":"src/main/App.java","line":23,"message":"Consider renaming this.","unresolved":true}'

# Post a review with a Code-Review +1 label
./scripts/gerrit_api.sh review 12345 current '{"message":"Looks good!","labels":{"Code-Review":1}}'

# Submit a change
./scripts/gerrit_api.sh submit 12345

# Abandon a change
./scripts/gerrit_api.sh abandon 12345
```

## Gerrit Concepts

### Changes and Patch Sets
- A **change** is a single reviewable unit (corresponds to one commit).
- Each update to a change creates a new **patch set** (a new commit with the same `Change-Id`).
- Changes live under `refs/changes/` refs in the Git repo.

### Change-Id
- A footer line in the commit message (`Change-Id: I<hex>`) that links commits to Gerrit changes.
- The `commit-msg` hook (installed from Gerrit) auto-generates this.

### Labels
- **Code-Review**: Typically −2 to +2. `+2` means approved.
- **Verified**: Typically −1 to +1. Usually set by CI.
- Label ranges and names are project-specific.

### Workflow
1. Push to `refs/for/<branch>` to create/update a change for review.
2. Reviewers add comments and vote via labels.
3. Amend the commit (`git commit --amend`) and re-push for new patch sets.
4. Once approvals are met, a committer submits the change.

## REST API Reference

### Authentication

All authenticated requests use the `/a/` prefix and HTTP Basic Auth:

```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/?q=status:open+limit:5"
```

### Output Format

Gerrit JSON responses start with an **XSSI prevention prefix** `)]}'` on the first line. You must strip it before parsing:

```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/?q=status:open" | tail -n +2 | jq .
```

### URL Encoding

Project names, file paths, and branch names in URLs must be URL-encoded. Forward slashes in project/file paths become `%2F`:

```
myOrg/myProject  →  myOrg%2FmyProject
src/main/App.java  →  src%2Fmain%2FApp.java
```

### Key Endpoints

#### 1. Query Changes

```
GET /a/changes/?q=<query>&n=<limit>&o=<option>
```

Common query operators:
- `status:open` / `status:merged` / `status:abandoned`
- `owner:self` / `reviewer:self`
- `project:<name>` / `branch:<name>`
- `is:watched` / `is:starred`
- `after:"2025-01-01"` / `before:"2025-12-31"`

Common `o` (option) parameters to include extra data:
- `CURRENT_REVISION` — include current revision info
- `DETAILED_LABELS` — include detailed label/vote info
- `DETAILED_ACCOUNTS` — include full account info
- `CURRENT_FILES` — include file list for current revision
- `MESSAGES` — include change messages

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/?q=status:open+owner:self&n=10&o=CURRENT_REVISION&o=DETAILED_LABELS" \
  | tail -n +2 | jq .
```

#### 2. Get Change Details

```
GET /a/changes/<change-id>?o=CURRENT_REVISION&o=DETAILED_LABELS
```

The `<change-id>` can be:
- A numeric change number: `12345`
- The full triplet: `project~branch~Change-Id`
- Just the Change-Id: `I8473b95934b5732ac55d26311a706c9c2bde9940`

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/12345?o=CURRENT_REVISION&o=DETAILED_LABELS&o=DETAILED_ACCOUNTS" \
  | tail -n +2 | jq .
```

#### 3. List Files in a Revision

```
GET /a/changes/<change-id>/revisions/<revision-id>/files/
```

Use `current` as `<revision-id>` for the latest patch set.

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/12345/revisions/current/files/" \
  | tail -n +2 | jq .
```

Response is a map of file paths to `FileInfo` objects:
```json
{
  "/COMMIT_MSG": { "status": "A", "lines_inserted": 7, "size_delta": 551, "size": 551 },
  "src/main/App.java": { "lines_inserted": 5, "lines_deleted": 3, "size_delta": 98, "size": 23348 }
}
```

#### 4. Get File Diff

```
GET /a/changes/<change-id>/revisions/<revision-id>/files/<file-id>/diff
```

The `<file-id>` must be URL-encoded. Add `?intraline` for intraline differences.

Example:
```bash
FILE_PATH="src%2Fmain%2FApp.java"
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/12345/revisions/current/files/$FILE_PATH/diff" \
  | tail -n +2 | jq .
```

Response is a `DiffInfo` entity with `content` array containing `ab` (common), `a` (deleted), and `b` (added) line arrays.

#### 5. Get File Content

```
GET /a/changes/<change-id>/revisions/<revision-id>/files/<file-id>/content
```

Returns **base64-encoded** file content.

Example:
```bash
FILE_PATH="src%2Fmain%2FApp.java"
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  "$GERRIT_URL/a/changes/12345/revisions/current/files/$FILE_PATH/content" \
  | base64 -d
```

#### 6. Post a Review (Set Labels, Comments)

```
POST /a/changes/<change-id>/revisions/<revision-id>/review
Content-Type: application/json
```

**ReviewInput** JSON body:

```json
{
  "message": "Overall review comment shown at the top",
  "labels": {
    "Code-Review": 1
  },
  "comments": {
    "src/main/App.java": [
      {
        "line": 23,
        "message": "Consider renaming this variable for clarity."
      },
      {
        "range": {
          "start_line": 50,
          "start_character": 0,
          "end_line": 55,
          "end_character": 20
        },
        "message": "This block should be refactored."
      }
    ]
  }
}
```

Label values (project-specific, typical):
- **Code-Review**: `-2` (reject), `-1` (looks wrong), `0` (no score), `+1` (looks good), `+2` (approved)
- **Verified**: `-1` (fails), `0` (no score), `+1` (verified)

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Looks good to me!","labels":{"Code-Review":1}}' \
  "$GERRIT_URL/a/changes/12345/revisions/current/review" \
  | tail -n +2 | jq .
```

#### 7. Post a Draft Comment

```
PUT /a/changes/<change-id>/revisions/<revision-id>/drafts
Content-Type: application/json
```

**CommentInput** JSON body:

```json
{
  "path": "src/main/App.java",
  "line": 23,
  "message": "[nit] trailing whitespace",
  "unresolved": true
}
```

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{"path":"src/main/App.java","line":23,"message":"[nit] trailing whitespace","unresolved":true}' \
  "$GERRIT_URL/a/changes/12345/revisions/current/drafts" \
  | tail -n +2 | jq .
```

#### 8. Submit a Change

```
POST /a/changes/<change-id>/submit
```

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  "$GERRIT_URL/a/changes/12345/submit" \
  | tail -n +2 | jq .
```

#### 9. Abandon / Restore a Change

```
POST /a/changes/<change-id>/abandon
POST /a/changes/<change-id>/restore
```

Both accept an optional JSON body with a `message` field:

```bash
# Abandon
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Superseded by change 12346"}' \
  "$GERRIT_URL/a/changes/12345/abandon" \
  | tail -n +2 | jq .

# Restore
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Re-opening for further review"}' \
  "$GERRIT_URL/a/changes/12345/restore" \
  | tail -n +2 | jq .
```

#### 10. Add Reviewer

```
POST /a/changes/<change-id>/reviewers
Content-Type: application/json
```

```json
{
  "reviewer": "jane.roe@example.com"
}
```

To add as CC instead of reviewer, add `"state": "CC"`.

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"reviewer":"jane.roe@example.com"}' \
  "$GERRIT_URL/a/changes/12345/reviewers" \
  | tail -n +2 | jq .
```

#### 11. Set Topic

```
PUT /a/changes/<change-id>/topic
Content-Type: application/json
```

```json
{
  "topic": "my-feature-branch"
}
```

Example:
```bash
curl -s --user "$GERRIT_USERNAME:$GERRIT_HTTP_PASSWORD" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{"topic":"my-feature-branch"}' \
  "$GERRIT_URL/a/changes/12345/topic" \
  | tail -n +2 | jq .
```

## Code Review Workflow

Here is a recommended workflow for performing a code review with this skill:

### Step 1 — Find changes to review

```bash
./scripts/gerrit_api.sh query "status:open+reviewer:self+-owner:self"
```

### Step 2 — Inspect a change

```bash
# Get change details with labels and current revision
./scripts/gerrit_api.sh get-change 12345

# List modified files
./scripts/gerrit_api.sh list-files 12345

# Read the diff for each relevant file
./scripts/gerrit_api.sh get-diff 12345 "path/to/file.java"
```

### Step 3 — Post your review

You can either post all comments at once using the `review` endpoint, or incrementally build your review using draft comments and publish them together.

**Option A: Incremental Drafts**
Create drafts one by one for different files or lines. This is useful when you are doing a complex review.

```bash
# Add an unresolved draft comment
./scripts/gerrit_api.sh create-draft 12345 current '{"path":"path/to/file.java","line":42,"message":"Consider using a constant here instead of a magic number.","unresolved":true}'

# Once all drafts are created, publish them and add a vote/summary message
./scripts/gerrit_api.sh review 12345 current '{
  "message": "I left a few comments on the implementation. Please take a look.",
  "labels": {"Code-Review": -1},
  "drafts": "PUBLISH"
}'
```

**Option B: Single Step Review**
Post the summary and all inline comments in a single payload.

```bash
./scripts/gerrit_api.sh review 12345 current '{
  "message": "Overall the approach looks solid. A few suggestions below.",
  "labels": {"Code-Review": 1},
  "comments": {
    "path/to/file.java": [
      {
        "line": 42, 
        "message": "Consider using a constant here instead of a magic number.",
        "unresolved": true
      },
      {
        "line": 65,
        "message": "Nice cleanup here.",
        "unresolved": false
      }
    ]
  }
}'
```

The `comments` field in the JSON body follows the `CommentInput` entity schema. Additional supported fields include:
- `notify` (string) — notification level for email notifications (`ALL`, `OWNER`, `NONE`, etc, suggest using `OWNER` to avoid spamming everyone)
- `notify_details` (object) — fine-grained notification control per account
- `in_reply_to` (string) — optional, the URL encoded UUID of the comment to which this comment is a reply.
- `unresolved` (boolean) — optional, whether the comment thread should be marked as unresolved. **Crucial for Agent behavior:** Set to `true` for comments that require action and must be addressed before merging. Set to `false` for informational comments, praise, or purely optional nits. Explicitly declaring this state ensures proper tracking in the review UI.
- `fix_suggestions` (array) — optional, list of suggested fixes for this comment. Each suggestion includes a description and a replacement patch.

### Step 4 — Submit when ready

```bash
./scripts/gerrit_api.sh submit 12345
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `401 Unauthorized` | Check `GERRIT_USERNAME` and `GERRIT_HTTP_PASSWORD`. Re-generate the HTTP password in Gerrit Settings. |
| `404 Not Found` | Verify the change number exists. Check `GERRIT_URL` has no trailing slash. Ensure the `/a/` prefix is present. |
| `409 Conflict` | You may be trying to review a change edit, or submit a change that doesn't meet requirements. |
| JSON parse error | Make sure you strip the XSSI prefix `)]}'\n` from the response before parsing. |
| URL encoding issues | Project paths with `/` must use `%2F`. Use the helper script which handles this automatically. |

## Awareness

- This skill is designed for interactive use and may not handle all edge cases of the Gerrit API. For complex operations, refer to the official API documentation.
- `GERRIT_URL` and `GERRIT_USERNAME` can be used in the output printed by the skill, but **do not** print `GERRIT_HTTP_PASSWORD` or any sensitive information in logs or outputs.
- Ensure that the HTTP credential token (`GERRIT_HTTP_PASSWORD`) is kept secure and not exposed in logs, environment dumps, or error messages. It should only be used for authentication in API calls and never printed or logged in plaintext.

## References

- [Gerrit REST API Documentation](https://gerrit-review.googlesource.com/Documentation/rest-api.html)
- [Gerrit Changes REST API](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html)
- [Gerrit Search Operators](https://gerrit-review.googlesource.com/Documentation/user-search.html)
- [Gerrit in 5 Minutes](https://github.com/yurnov/gerrit-in-5-min)
