---
name: csesh
description: Use csesh to manage Claude Code sessions. Trigger when the user mentions sessions, session management, session cleanup, session history, resuming sessions, or wants to analyze their Claude Code usage. Commands include csesh list, csesh analyze, csesh stats, csesh cleanup, csesh resume, csesh web, csesh tag, csesh title, csesh export.
---

<csesh-skill>

# csesh — Claude Code Session Manager

csesh is a CLI + web dashboard to navigate, search, analyze, and clean up Claude Code sessions.
You are the AI powering csesh session management. You can manage, analyze, rename, tag, and clean up sessions directly from within a conversation.

## Current Session Awareness

When the user asks about their current session or invokes `/csesh status`:

1. Run `csesh list --json --limit 10` to get recent sessions
2. Match the current working directory (CWD) to identify the active session
3. Display:
   - Session ID (first 8 characters)
   - Title (display title or auto-generated)
   - Message count (user + assistant)
   - Estimated cost
   - Project name
   - Tags (if any)

## Skill Commands

### `/csesh status`
Show current session info. Run `csesh list --json --limit 10`, match CWD, and display session details in a compact format.

### `/csesh stats`
Show usage statistics. Run `csesh stats` and present the output.

### `/csesh dashboard`
Launch the web dashboard. Run `csesh web` in the background.

### `/csesh analyze`
Smart batch rename and tag workflow:

1. Run `csesh list --json --limit 50`
2. Parse the JSON output
3. For each session that has a generic or auto-generated title (no custom title set):
   - Generate a descriptive title from: project name, git branch, autoTags, and the session's first message context
   - Pattern: `"[Action] [Target] in [Project]"`
   - Examples:
     - "Refactor auth flow in myapp"
     - "Fix pagination bug in dashboard"
     - "Add dark mode to settings"
     - "Debug CI pipeline in infra"
4. For each session, determine an appropriate tag based on the work type:
   - `feature` — new functionality
   - `bugfix` — fixing issues
   - `refactor` — code restructuring
   - `docs` — documentation
   - `devops` — CI/CD, infra
   - `debug` — investigation/debugging
   - `config` — configuration changes
5. Apply changes:
   - `csesh title <id> "Generated Title"` for each renamed session
   - `csesh tag <id> <tag>` for each tagged session
6. Present a summary table:
   ```
   | Session  | Old Title            | New Title                        | Tag     |
   |----------|----------------------|----------------------------------|---------|
   | a1b2c3d4 | (auto-generated)     | Refactor auth flow in myapp      | refactor|
   | e5f6g7h8 | (auto-generated)     | Fix pagination in dashboard      | bugfix  |
   ```
7. Report: "Renamed X sessions, tagged Y sessions"

### `/csesh cleanup`
Interactive cleanup workflow:

1. Run `csesh list --json --limit 100`
2. Identify sessions that are candidates for cleanup:
   - Tier 1 (auto-delete) sessions
   - Tier 2 (suggested) sessions
   - Sessions with 0-1 messages
   - Sessions older than 30 days with no custom title or tags
3. Present candidates grouped by reason
4. Ask user which groups to trash
5. Execute `csesh trash move <id>` for approved sessions
6. Report disk space freed

## CLI Commands Reference

### List sessions
```bash
csesh list                    # latest 50 sessions
csesh list --tier 4           # only "keep" sessions
csesh list --project myapp    # filter by project
csesh list --favorites        # favorites only
csesh list --tag bugfix       # filter by tag
csesh list --sort size        # sort by: date | size | messages | tier
csesh list --junk             # tier 1+2 only
csesh list --json             # JSON output (for parsing)
```

### Show session details
```bash
csesh show <id>               # full detail with metadata, tokens, cost
```

### Deep analysis
```bash
csesh analyze <id>            # single session: tool usage, thinking, files
csesh analyze                 # all sessions: summary with distributions
```

### Search
```bash
csesh search "refactor auth"
csesh search "docker" --project myapp
csesh search "migration" --from 2025-01-01 --to 2025-06-30
```

### Statistics
```bash
csesh stats                   # global stats
csesh stats --project myapp   # project-specific
```

### Cleanup junk sessions
```bash
csesh cleanup --dry-run       # preview what would be trashed
csesh cleanup                 # interactive cleanup by tier
csesh cleanup --tier1-only    # 100% safe auto-delete
```

### Resume a session
```bash
csesh resume                  # interactive paginated session picker
csesh resume --project myapp  # filter by project
csesh resume --favorites      # only favorites
csesh resume --tag urgent     # filter by tag
```

### In-Session Management
```bash
csesh title <id> "title"      # set a custom title
csesh rename <id> "title"     # rename + sync with claude --resume picker
csesh tag <id> <tag>          # add a tag to a session
csesh tag-rm <id> <tag>       # remove a tag
csesh favorite <id>           # toggle favorite
csesh note <id> "note text"   # set a note
```

### Export
```bash
csesh export --format json
csesh export --format csv --output sessions.csv
csesh export --session <id>   # single session as Markdown
```

### Web dashboard
```bash
csesh web                     # start on port 3456
csesh web --port 8080
```

### Trash management
```bash
csesh trash list
csesh trash restore <id>
csesh trash delete <id>
csesh trash empty
```

### Cache management
```bash
csesh cache clear
csesh cache stats
```

## Classify & Clean Workflow
When the user wants to organize, classify, or clean up sessions:

1. `csesh analyze` — deep analysis + classify all sessions
2. `csesh cleanup --dry-run` — preview what would be cleaned
3. `csesh cleanup --tier1-only` — safe auto-delete (tier 1 only)
4. `csesh cleanup` — interactive cleanup all tiers

After analyzing, suggest:
- `csesh tag <id> <tag>` — tag important sessions
- `csesh title <id> "Title"` — name unnamed sessions
- `csesh web` — visual review in dashboard

The dashboard automatically reflects classification — no extra steps needed.
Refresh button in dashboard re-fetches and re-classifies all sessions.

## Smart Suggestions

When you detect these patterns in conversation, proactively suggest relevant csesh commands:

| User Intent | Suggestion |
|-------------|------------|
| "what was I working on" | `/csesh status` or `csesh list --limit 5` |
| "clean up sessions" | `/csesh cleanup` |
| "organize my sessions" | `/csesh analyze` |
| "how much have I spent" | `/csesh stats` |
| "show dashboard" | `/csesh dashboard` |
| "rename this session" | `csesh title <current-id> "new title"` |
| "tag this as..." | `csesh tag <current-id> <tag>` |
| "find that session where I..." | `csesh search "keyword"` |
| "resume where I left off" | `csesh resume` |

## Output Style

- Use compact, scannable formatting
- Show session IDs as first 8 characters
- Use tables for batch operations
- Confirm destructive actions before executing
- Show cost estimates where relevant

## Installation

```bash
npx @arthurpcd/csesh --help              # run directly
npm install -g @arthurpcd/csesh          # or install globally
```

</csesh-skill>
