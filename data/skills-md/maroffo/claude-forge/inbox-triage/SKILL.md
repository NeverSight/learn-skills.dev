---
name: inbox-triage
description: "Review and prioritize Gmail inbox. Use when user wants to check email, review inbox, or see what needs attention."
tools: Bash, Read, Write, Edit
---

# ABOUTME: Gmail inbox triage - classify unread by priority, suggest actions
# ABOUTME: P1-P4 priority system with CLI tool for classification and batch archival

# Inbox Triage Skill

**Gmail:** See `../_GMAIL.md` for account config and commands.

## Workflow

### Step 1: Classify Inbox

Pipe gog search output through the CLI tool:

```bash
gog gmail search "is:unread in:inbox" --json --max=30 --account=maroffo@gmail.com \
  | uv run --project ~/.claude/skills/inbox-triage -- inbox-triage classify
```

This outputs a markdown summary grouped by priority and saves state to `/tmp/inbox-triage-state.json`.

### Step 2: Review with User

Present the CLI output to the user. The summary includes:
- **P1 - Urgent**: Direct messages from known contacts, time-sensitive
- **P2 - Important**: Work-related, newsletters worth reading, personal correspondence
- **P3 - Normal**: General updates, notifications
- **P4 - Low Priority**: Promotions, social, automated noise

### Step 3: Archive

Use the archive subcommand for batch operations:

```bash
# Dry run (shows commands without executing)
uv run --project ~/.claude/skills/inbox-triage -- inbox-triage archive p3 p4

# Execute
uv run --project ~/.claude/skills/inbox-triage -- inbox-triage archive p3 p4 --yes
```

### Step 4: Handle Remaining Items

For P1/P2 threads that need action:
```bash
# Open in browser
gog gmail url <threadId>

# Star for follow-up
gog gmail thread modify <threadId> --account=maroffo@gmail.com --add=STARRED

# Mark as read without archiving
gog gmail thread modify <threadId> --account=maroffo@gmail.com --remove=UNREAD
```

## Classification Rules

Rules are in `~/.claude/skills/inbox-triage/rules.yaml` (user-editable). First match wins:

1. Sender exact email match
2. Sender domain match (`@domain.com`)
3. Gmail label match
4. Gmail category fallback (`CATEGORY_PROMOTIONS`, etc.)
5. Default (P3)

## Rules

1. **Summarize first** - don't read full content unless asked
2. **Respect privacy** - don't read personal emails in detail without permission
3. **Batch operations** - group similar actions (archive all promos, etc.)
4. **Confirm destructive actions** - always confirm before trash/delete
5. **Open in browser** - use `gog gmail url <threadId>` for user to read full email
