---
name: "gitlab-discussion"
description: "GitLab discussion operations via API. ALWAYS use this skill when user wants to: (1) view threaded discussions on MRs/issues, (2) create new discussion threads, (3) reply to discussions, (4) resolve/unresolve discussions."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Discussion Skill

Threaded discussion management for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List MR discussions | `glab api projects/:id/merge_requests/:iid/discussions` | - |
| List issue discussions | `glab api projects/:id/issues/:iid/discussions` | - |
| Get discussion | `glab api projects/:id/merge_requests/:iid/discussions/:id` | - |
| Create discussion | `glab api projects/:id/merge_requests/:iid/discussions -X POST -f ...` | ⚠️ |
| Reply to discussion | `glab api projects/:id/.../discussions/:id/notes -X POST -f ...` | ⚠️ |
| Resolve discussion | `glab api projects/:id/.../discussions/:id -X PUT -f resolved=true` | ⚠️ |
| Delete note | `glab api projects/:id/.../discussions/:id/notes/:nid -X DELETE` | ⚠️⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "discussion", "thread", "conversation"
- User wants to add code review comments
- User mentions "resolve", "unresolve" discussions
- User wants to reply to existing comments/threads
- User wants line-specific comments on MRs

**NEVER use when:**
- User wants simple notes/comments (use `glab mr note` or `glab issue note`)
- User wants to review MR changes (use gitlab-mr)
- User wants to search comments (use gitlab-search with `notes` scope)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- Read discussions: Reporter+ (for private repos)
- Create discussions: Reporter+
- Resolve discussions: Developer+ (or MR author)

## Available Commands

### List MR Discussions

```bash
# List all discussions on MR
glab api projects/123/merge_requests/1/discussions --method GET

# With pagination
glab api projects/123/merge_requests/1/discussions --paginate

# Using project path
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/merge_requests/1/discussions"
```

### List Issue Discussions

```bash
# List all discussions on issue
glab api projects/123/issues/42/discussions --method GET

# With pagination
glab api projects/123/issues/42/discussions --paginate
```

### Get Specific Discussion

```bash
# Get MR discussion by ID
glab api projects/123/merge_requests/1/discussions/abc123 --method GET

# Get issue discussion by ID
glab api projects/123/issues/42/discussions/def456 --method GET
```

### Create Discussion on MR

```bash
# Create general discussion
glab api projects/123/merge_requests/1/discussions --method POST \
  -f body="This looks good overall, but I have some suggestions."

# Create discussion on specific line (diff note)
glab api projects/123/merge_requests/1/discussions --method POST \
  -f body="This could be simplified using a helper function." \
  -f position[base_sha]="abc123" \
  -f position[head_sha]="def456" \
  -f position[start_sha]="abc123" \
  -f position[position_type]="text" \
  -f position[new_path]="src/app.py" \
  -f position[new_line]=42

# Create discussion on old line (removed code)
glab api projects/123/merge_requests/1/discussions --method POST \
  -f body="Why was this removed?" \
  -f position[base_sha]="abc123" \
  -f position[head_sha]="def456" \
  -f position[start_sha]="abc123" \
  -f position[position_type]="text" \
  -f position[old_path]="src/old.py" \
  -f position[old_line]=15

# Create suggestion
glab api projects/123/merge_requests/1/discussions --method POST \
  -f body='```suggestion
def improved_function():
    return "better implementation"
```'
```

### Create Discussion on Issue

```bash
# Create discussion
glab api projects/123/issues/42/discussions --method POST \
  -f body="I think we should reconsider this approach."
```

### Reply to Discussion

```bash
# Reply to MR discussion
glab api projects/123/merge_requests/1/discussions/abc123/notes --method POST \
  -f body="Good point, I'll fix this."

# Reply to issue discussion
glab api projects/123/issues/42/discussions/def456/notes --method POST \
  -f body="I agree with the above."
```

### Resolve/Unresolve Discussion

```bash
# Resolve MR discussion
glab api projects/123/merge_requests/1/discussions/abc123 --method PUT \
  -f resolved=true

# Unresolve MR discussion
glab api projects/123/merge_requests/1/discussions/abc123 --method PUT \
  -f resolved=false
```

### Update Note

```bash
# Update note in discussion
glab api projects/123/merge_requests/1/discussions/abc123/notes/789 --method PUT \
  -f body="Updated comment text"
```

### Delete Note

```bash
# Delete note from discussion
glab api projects/123/merge_requests/1/discussions/abc123/notes/789 --method DELETE
```

## Position Object for Diff Notes

For line-specific comments on MRs, you need to provide position information:

| Field | Required | Description |
|-------|:--------:|-------------|
| `base_sha` | Yes | SHA of the base commit (target branch) |
| `head_sha` | Yes | SHA of the head commit (source branch) |
| `start_sha` | Yes | SHA of the start commit |
| `position_type` | Yes | `text` for code, `image` for images |
| `new_path` | For new/modified | Path in new version |
| `new_line` | For new/modified | Line number in new version |
| `old_path` | For deleted | Path in old version |
| `old_line` | For deleted | Line number in old version |

### Get SHAs for Position

```bash
# Get MR details to find SHAs
mr_info=$(glab api projects/123/merge_requests/1)
base_sha=$(echo "$mr_info" | jq -r '.diff_refs.base_sha')
head_sha=$(echo "$mr_info" | jq -r '.diff_refs.head_sha')
start_sha=$(echo "$mr_info" | jq -r '.diff_refs.start_sha')

echo "Base: $base_sha"
echo "Head: $head_sha"
echo "Start: $start_sha"
```

## Common Workflows

### Workflow 1: Review MR with Comments

```bash
project_id=123
mr_iid=1

# Get diff refs
mr_info=$(glab api projects/$project_id/merge_requests/$mr_iid)
base_sha=$(echo "$mr_info" | jq -r '.diff_refs.base_sha')
head_sha=$(echo "$mr_info" | jq -r '.diff_refs.head_sha')
start_sha=$(echo "$mr_info" | jq -r '.diff_refs.start_sha')

# Add comment on line 42 of new file
glab api projects/$project_id/merge_requests/$mr_iid/discussions --method POST \
  -f body="Consider adding error handling here." \
  -f position[base_sha]="$base_sha" \
  -f position[head_sha]="$head_sha" \
  -f position[start_sha]="$start_sha" \
  -f position[position_type]="text" \
  -f position[new_path]="src/handler.py" \
  -f position[new_line]=42
```

### Workflow 2: Resolve All Discussions

```bash
# Get all unresolved discussions
glab api projects/123/merge_requests/1/discussions --paginate | \
  jq -r '.[] | select(.notes[0].resolvable == true and .notes[0].resolved == false) | .id' | \
  while read discussion_id; do
    echo "Resolving: $discussion_id"
    glab api projects/123/merge_requests/1/discussions/$discussion_id --method PUT \
      -f resolved=true
  done
```

### Workflow 3: List Unresolved Discussions

```bash
# Show unresolved discussions with content
glab api projects/123/merge_requests/1/discussions --paginate | \
  jq -r '.[] | select(.notes[0].resolvable == true and .notes[0].resolved == false) | "[\(.id)] \(.notes[0].author.username): \(.notes[0].body | split("\n")[0])"'
```

### Workflow 4: Add Suggestion

```bash
project_id=123
mr_iid=1

mr_info=$(glab api projects/$project_id/merge_requests/$mr_iid)
base_sha=$(echo "$mr_info" | jq -r '.diff_refs.base_sha')
head_sha=$(echo "$mr_info" | jq -r '.diff_refs.head_sha')
start_sha=$(echo "$mr_info" | jq -r '.diff_refs.start_sha')

# Create suggestion (multi-line needs proper escaping)
glab api projects/$project_id/merge_requests/$mr_iid/discussions --method POST \
  -f body='```suggestion
const result = await fetchData();
return result.data;
```' \
  -f position[base_sha]="$base_sha" \
  -f position[head_sha]="$head_sha" \
  -f position[start_sha]="$start_sha" \
  -f position[position_type]="text" \
  -f position[new_path]="src/api.js" \
  -f position[new_line]=25
```

### Workflow 5: Summarize Discussion Activity

```bash
# Count discussions by state
glab api projects/123/merge_requests/1/discussions --paginate | \
  jq '{
    total: length,
    resolved: [.[] | select(.notes[0].resolved == true)] | length,
    unresolved: [.[] | select(.notes[0].resolvable == true and .notes[0].resolved == false)] | length
  }'
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Missing position fields | Include all required position fields |
| 404 Discussion not found | Invalid discussion ID | Check discussion exists |
| Cannot resolve | Not resolvable or not authorized | Check note type and permissions |
| Position invalid | Wrong SHAs or line numbers | Get fresh diff_refs from MR |
| Note empty | Body not set | Check `-f body=...` parameter |

## Discussion vs Note

- **Discussion**: A thread that can have multiple notes/replies
- **Note**: A single comment within a discussion
- **Resolvable**: Discussions on MR diffs can be resolved/unresolved
- **System notes**: Auto-generated (commits, status changes) - not editable

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Discussions API](https://docs.gitlab.com/ee/api/discussions.html)
