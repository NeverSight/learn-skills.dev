---
name: jira
description: Manage Jira issues from the command line. Use when working with Jira issues, creating tasks, updating status, assigning work, or searching for issues.
---

# Jira CLI

Command-line tool for managing Jira issues via `af jira`.

## Setup

Add the following environment variables to your project's `.env` file:
- `JIRA_BASE_URL` — Your Jira instance URL (e.g., `https://company.atlassian.net`)
- `JIRA_EMAIL` — Your Atlassian account email
- `JIRA_API_TOKEN` — API token from https://id.atlassian.com/manage-profile/security/api-tokens

## Quick Reference

Run `af jira --help` for all options.

### Read Operations

- `af jira get <issue-key>` — Get issue details
- `af jira list <project> [--limit N]` — List project issues
- `af jira search "<jql>"` — Search with JQL
- `af jira projects` — List projects
- `af jira types <project>` — List issue types
- `af jira transitions <issue-key>` — List available transitions
- `af jira comment <issue-key>` — List comments

### Write Operations

- `af jira create --project <key> --type <type> --summary "<text>" [--description "<text>"] [--priority <name>] [--labels a,b,c] [--parent <key>]`
- `af jira update <issue-key> [--summary "<text>"] [--description "<text>"] [--priority <name>] [--labels a,b,c]`
- `af jira transition <issue-key> --to "<status>"`
- `af jira assign <issue-key> --to <email>` (use `--to none` to unassign)
- `af jira comment <issue-key> --add "<text>"`
- `af jira attach <issue-key> <file>` — Attach a file (images, PDFs, etc.)
- `af jira delete <issue-key>`

## Output Formats

- Default: Markdown
- JSON: Add `--json` flag

## Common Workflows

### View my assigned issues

```bash
af jira search "assignee = currentUser() AND status != Done ORDER BY priority DESC"
```

### Start working on an issue

```bash
af jira get PROJ-123
af jira transition PROJ-123 --to "In Progress"
af jira comment PROJ-123 --add "Starting work"
```

### Complete an issue

```bash
af jira comment PROJ-123 --add "Done"
af jira transition PROJ-123 --to "Done"
```

### Create a bug with details

```bash
af jira create --project PROJ --type Bug --summary "Login fails on Safari" \
  --description "Users cannot log in using Safari 17. Error: 'Invalid session'" \
  --priority High --labels safari,auth,urgent
```

### Create a subtask

```bash
af jira create --project PROJ --type Sub-task --summary "Write unit tests" \
  --parent PROJ-123
```

### Attach files to an issue

```bash
# Attach a screenshot
af jira attach PROJ-123 ./screenshot.png

# Attach multiple files
for f in ./audit/*.png; do
  af jira attach PROJ-123 "$f"
done
```

### Search examples

```bash
# My open issues
af jira search "assignee = currentUser() AND status != Done"

# Recent bugs in project
af jira search "project = PROJ AND type = Bug ORDER BY created DESC" --limit 10

# Unassigned issues
af jira search "project = PROJ AND assignee IS EMPTY"

# Issues updated this week
af jira search "project = PROJ AND updated >= -7d"

# High priority blockers
af jira search "priority = Highest AND status != Done"
```

## Tips

- **Discover valid values first**: Run `af jira transitions <key>` before transitioning, `af jira types <project>` before creating
- **Use `--json` for scripting**: Pipe output to `jq` for automation
- **Quote JQL queries**: Always wrap JQL in double quotes to handle spaces

## Error Handling

- Errors print to stderr
- With `--json`: `{"error": "message"}`
- Exit codes: `0` success, `1` error
