---
name: firewatch
description: Query GitHub PR activity using the Firewatch CLI (fw). Fetch, cache, filter, and act on PR comments, reviews, commits, and CI status. Outputs JSONL for jq composition. Use when checking PR status, finding review comments, querying activity, resolving feedback, or working with GitHub pull requests.
user-invocable: true
metadata:
  author: outfitter-dev
  version: "3.0"
---

# Firewatch

Query, filter, and act on GitHub PR activity using the Firewatch CLI (`fw`).

## Quick Start

```bash
fw --refresh --summary --open    # Sync and see what needs attention
fw --type comment --pr 42       # Comments on PR #42
fw --type comment | jq 'select(.author != .pr_author)'  # External feedback only
```

## Core Concepts

### JSONL Output

Firewatch outputs one JSON object per line. Each entry is **denormalized** — it contains full PR context (title, state, author, labels) so you never need joins.

```bash
fw --type comment --limit 1
```

```json
{
  "id": "IC_kwDOK...",
  "type": "comment",
  "subtype": "review_comment",
  "author": "alice",
  "body": "Consider adding error handling here",
  "file": "src/auth.ts",
  "line": 42,
  "pr": 123,
  "pr_title": "Add user authentication",
  "pr_state": "open",
  "pr_author": "bob",
  "created_at": "2025-01-14T10:00:00Z"
}
```

### Entry Types

| Type      | Subtype          | Meaning                                     |
| --------- | ---------------- | ------------------------------------------- |
| `comment` | `review_comment` | Inline code comment (actionable)            |
| `comment` | `issue_comment`  | General PR comment                          |
| `review`  | —                | Review submission (approve/request changes) |
| `commit`  | —                | Commit pushed to PR branch                  |
| `ci`      | —                | CI/CD status check                          |
| `event`   | —                | Lifecycle event (opened, closed, merged)    |

## Querying

### Filter Flags

```bash
fw --type comment              # By type
fw --since 24h                 # By time (30s, 5m, 24h, 7d, 2w, 1mo)
fw --pr 42                    # By PR number
fw --author alice              # By author
fw --open                      # Open PRs only
fw --active                    # Open or draft PRs
fw --mine                      # PRs assigned to me
fw --reviews                   # PRs I need to review
```

Combine filters (AND logic):

```bash
fw --type review --author alice --since 7d --open
```

### Aggregation

Per-PR summary instead of individual entries:

```bash
fw --summary --open
```

### Composing with jq

CLI filters handle common cases; jq handles everything else:

```bash
# Only approved reviews
fw --type review | jq 'select(.state == "approved")'

# Comments mentioning "TODO"
fw --type comment | jq 'select(.body | test("TODO"; "i"))'

# External feedback (not self-comments)
fw --type comment | jq 'select(.author != .pr_author)'

# Count by type
fw | jq -s 'group_by(.type) | map({type: .[0].type, count: length})'
```

**Tip:** Use CLI filters first, then jq. CLI filters are faster because they skip JSON parsing for non-matching entries.

See [references/jq-cookbook.md](references/jq-cookbook.md) for more patterns.

## Taking Action

### Post a Comment

```bash
fw add 42 "LGTM, merging!"
```

### Reply to a Review Comment

Every comment entry has an `id` field:

```bash
fw add 42 "Fixed in latest commit" --reply IC_kwDOK...
```

### Reply and Resolve

```bash
fw add 42 "Done" --reply IC_kwDOK... --resolve
```

### Resolve Without Replying

```bash
fw close IC_kwDOK...
```

Resolve multiple threads:

```bash
fw close IC_abc IC_def IC_ghi
```

## Staleness Tracking

Review comments can become stale when the file is modified. Run `fw check` to populate staleness data:

```bash
fw check
```

Then query for unaddressed comments:

```bash
fw --type comment | jq 'select(.file_activity_after.modified == false)'
```

The `file_activity_after` field shows:

- `modified` — Whether file was changed after the comment
- `commits_touching_file` — How many commits touched the file
- `latest_commit` — SHA of the most recent commit to the file

## Graphite Stack Support

Firewatch integrates with Graphite for stack-aware queries. When syncing in a repo with Graphite stacks, entries include stack metadata:

```bash
fw --refresh   # Auto-detects Graphite stacks
```

### Stack Fields

Entries gain a `graphite` object:

```json
{
  "graphite": {
    "stack_id": "abc123",
    "stack_position": 2,
    "stack_size": 4,
    "parent_pr": 101
  }
}
```

- `stack_position` — 1 is the base (closest to main), higher = further up
- `file_provenance` — Which PR in the stack introduced each file

### Quick Stack Queries

```bash
# All entries with stack metadata
fw | jq 'select(.graphite != null)'

# Base PRs only (bottom of stack)
fw --summary | jq 'select(.graphite.stack_position == 1)'

# Comments where file originated in a different PR
fw --type comment | jq 'select(.file_provenance.origin_pr != .pr)'
```

### Stack Workflows

For detailed Graphite workflows (querying stacks, cross-PR fixes, commit patterns):

- [graphite/stack-queries.md](graphite/stack-queries.md) — Querying stack data
- [graphite/cross-pr-fixes.md](graphite/cross-pr-fixes.md) — File provenance and fixing in the right PR
- [graphite/commit-workflow.md](graphite/commit-workflow.md) — `gt modify` vs `gt amend -a`

## Command Reference

| Command              | Purpose                                    |
| -------------------- | ------------------------------------------ |
| `fw [options]`       | Query cached entries (auto-syncs if stale) |
| `fw --refresh`       | Force sync before query                    |
| `fw --summary`       | Aggregate into per-PR summaries            |
| `fw add <pr> [body]` | Post a comment or add metadata             |
| `fw close <id>...`   | Resolve review threads                     |
| `fw check`           | Refresh staleness hints                    |
| `fw status`          | Firewatch state info                       |
| `fw doctor`          | Diagnose auth/cache/repo issues            |
| `fw schema <type>`   | Print JSON schema                          |

### Query Options

| Option               | Description                 |
| -------------------- | --------------------------- |
| `--type <type>`      | Filter by entry type        |
| `--since <duration>` | Time filter (24h, 7d, etc.) |
| `--pr <numbers>`     | Filter by PR number(s)      |
| `--author <name>`    | Filter by author            |
| `--open`             | Open PRs only               |
| `--active`           | Open or draft PRs           |
| `--mine`             | PRs assigned to me          |
| `--reviews`          | PRs I need to review        |
| `--summary`          | Aggregate to per-PR summary |

### Add Options

| Option            | Description                                    |
| ----------------- | ---------------------------------------------- |
| `--reply <id>`    | Reply to a specific comment                    |
| `--resolve`       | Resolve the thread after posting               |
| `--review <type>` | Add review (approve, request-changes, comment) |
| `--label <name>`  | Add label (repeatable)                         |

## Patterns

- [patterns/daily-standup.md](patterns/daily-standup.md) — Morning PR review workflow
- [patterns/implementing-feedback.md](patterns/implementing-feedback.md) — Systematic feedback resolution
- [patterns/resolving-threads.md](patterns/resolving-threads.md) — Reply and resolve patterns

## References

- [references/entry-schema.md](references/entry-schema.md) — FirewatchEntry field reference
- [references/jq-cookbook.md](references/jq-cookbook.md) — Common jq filters
- [references/query-patterns.md](references/query-patterns.md) — Query combinations
- [references/troubleshooting.md](references/troubleshooting.md) — Common issues and fixes

## Agent Tips

1. **CLI filters first, then jq** — More efficient than jq-only filtering
2. **Denormalized = no joins** — Each entry has full PR context
3. **Entry IDs for actions** — Use `id` field with `--reply` and `fw close`
4. **Run `fw check` for staleness** — Populates `file_activity_after` field
5. **Check `.graphite` for stacks** — Null if not in a Graphite stack
6. **File provenance for cross-PR fixes** — See [graphite/cross-pr-fixes.md](graphite/cross-pr-fixes.md)
