---
name: atlassian
description: >
  Interact with Jira and Confluence via the `acli` CLI tool (Atlassian CLI). Use this skill
  whenever the user wants to manage Jira work items (create, edit, transition, search, comment,
  assign, bulk ops), manage sprints or boards, list/view Jira projects, or work with Confluence
  pages, blogs, and spaces — all from the terminal without opening a browser. Also trigger when
  the user says things like "ดู issue ของฉัน", "transition ไป In Progress", "สร้าง bug ใน Jira",
  "search ด้วย JQL", "ดู sprint ปัจจุบัน", "bulk transition", "ดู Confluence page", หรือ
  อะไรก็ตามที่ต้องการโต้ตอบกับ Atlassian products ผ่าน command line. Always use `acli` via
  the Bash tool — never use the Atlassian MCP for tasks this skill covers.
---

# Atlassian CLI (acli) Skill

Use `acli` (installed at `/opt/homebrew/bin/acli`) to interact with Jira and Confluence from the terminal.

## Authentication

Check auth status before running any commands if uncertain:
```bash
acli jira auth status
acli confluence auth status
```

If not authenticated:
```bash
# With API token (recommended for scripting)
echo <token> | acli jira auth login --site "yoursite.atlassian.net" --email "you@example.com" --token

# With browser OAuth
acli jira auth login --web
```

---

## Jira

### View & Search Work Items

```bash
# View a single issue
acli jira workitem view KEY-123
acli jira workitem view KEY-123 --json                          # structured output
acli jira workitem view KEY-123 --fields "summary,status,comment,description"

# Search with JQL
acli jira workitem search --jql "assignee = currentUser() AND sprint in openSprints()"
acli jira workitem search --jql "project = PROJ AND status = 'In Progress'" --fields "key,summary,status,assignee"
acli jira workitem search --jql "..." --json
acli jira workitem search --jql "..." --csv                     # for reports
acli jira workitem search --jql "..." --paginate               # fetch all results
acli jira workitem search --jql "..." --count                  # count only
acli jira workitem search --jql "..." --limit 50
```

See `references/jql-patterns.md` for common JQL patterns for developers.

### Create Work Items

```bash
# Quick create
acli jira workitem create --summary "Fix login bug" --project "PROJ" --type "Bug"

# With details
acli jira workitem create \
  --summary "Add retry logic" \
  --project "PROJ" \
  --type "Task" \
  --description "Implement exponential backoff for API calls" \
  --assignee "@me" \
  --label "backend,reliability"

# From JSON (use --generate-json to get template first)
acli jira workitem create --generate-json > workitem.json
# edit workitem.json, then:
acli jira workitem create --from-json workitem.json --project "PROJ" --type "Task"

# Bulk create
acli jira workitem create-bulk --from-json bulk-workitems.json
```

### Edit Work Items

```bash
# Edit single issue
acli jira workitem edit --key "KEY-123" --summary "Updated summary"
acli jira workitem edit --key "KEY-123" --description "New description" --yes

# Bulk edit via key list
acli jira workitem edit --key "KEY-1,KEY-2,KEY-3" --assignee "@me" --yes

# Bulk edit via JQL
acli jira workitem edit --jql "project = PROJ AND status = 'To Do' AND assignee is EMPTY" \
  --assignee "dev@company.com" --yes --ignore-errors

# Add/remove labels
acli jira workitem edit --key "KEY-123" --labels "frontend,urgent"
acli jira workitem edit --key "KEY-123" --remove-labels "old-label"
```

### Transition Work Items (Change Status)

```bash
# Single transition
acli jira workitem transition --key "KEY-123" --status "In Progress"
acli jira workitem transition --key "KEY-123" --status "Done" --yes

# Bulk transition via key list
acli jira workitem transition --key "KEY-1,KEY-2,KEY-3" --status "Done" --yes

# Bulk transition via JQL
acli jira workitem transition \
  --jql "project = PROJ AND sprint in openSprints() AND status = 'In Review'" \
  --status "Done" --yes --ignore-errors
```

Common status values: `"To Do"`, `"In Progress"`, `"In Review"`, `"Done"` (exact names depend on project workflow).

### Assign Work Items

```bash
acli jira workitem assign --key "KEY-123" --assignee "@me"
acli jira workitem assign --key "KEY-123" --assignee "user@company.com"

# Bulk assign via JQL
acli jira workitem assign \
  --jql "project = PROJ AND sprint in openSprints() AND assignee is EMPTY" \
  --assignee "@me" --yes

# Remove assignee
acli jira workitem assign --key "KEY-123" --remove-assignee
```

### Comments

```bash
# List comments
acli jira workitem comment list --key "KEY-123"

# Add comment
acli jira workitem comment create --key "KEY-123" --body "Fixed in commit abc123"

# Update comment
acli jira workitem comment update --key "KEY-123" --comment-id <id> --body "Updated note"

# Delete comment
acli jira workitem comment delete --key "KEY-123" --comment-id <id>
```

### Sprints

```bash
# View sprint details
acli jira sprint view <sprint-id>

# List all work items in a sprint
acli jira sprint list-workitems <sprint-id>

# List sprints on a board
acli jira board list-sprints <board-id>

# Create sprint
acli jira sprint create --name "Sprint 10" --board <board-id>
```

### Boards

```bash
# Search boards
acli jira board search --name "My Team Board"

# Get board details
acli jira board get <board-id>

# List sprints on a board
acli jira board list-sprints <board-id>

# List projects on a board
acli jira board list-projects <board-id>
```

### Projects

```bash
acli jira project list --paginate          # --paginate is required (or use --limit N or --recent)
acli jira project view --project "PROJ"
acli jira project create --name "New Project" --key "NP" --type "scrum"
```

---

## Confluence

### Pages

```bash
# View a page (need page ID or URL)
acli confluence page view <page-id>
acli confluence page view <page-id> --json
```

### Spaces

```bash
# List all spaces
acli confluence space list

# View space details
acli confluence space view --key "MYSPACE"

# Create a space
acli confluence space create --name "Engineering Docs" --key "ENGDOCS"

# Update space
acli confluence space update --key "MYSPACE" --name "New Name" --description "Updated desc"

# Archive / restore space
acli confluence space archive --key "OLDSPACE"
acli confluence space restore --key "OLDSPACE"
```

### Blogs

```bash
acli confluence blog --help   # check available subcommands for blogs
```

---

## Practical Workflows

### Daily Standup
```bash
# What am I working on?
acli jira workitem search \
  --jql "assignee = currentUser() AND sprint in openSprints() AND status != Done" \
  --fields "key,summary,status"
```

### Start Working on an Issue
```bash
acli jira workitem transition --key "KEY-123" --status "In Progress" --yes
acli jira workitem assign --key "KEY-123" --assignee "@me"
```

### End of Day / Mark Done
```bash
acli jira workitem transition --key "KEY-123" --status "Done" --yes
acli jira workitem comment create --key "KEY-123" --body "Completed. PR: #456"
```

### Bulk Close Sprint Items (when sprint ends)
```bash
acli jira workitem transition \
  --jql "sprint in openSprints() AND status = 'In Review' AND assignee = currentUser()" \
  --status "Done" --yes --ignore-errors
```

### Find Unassigned Bugs in Open Sprints
```bash
acli jira workitem search \
  --jql "issuetype = Bug AND sprint in openSprints() AND assignee is EMPTY" \
  --fields "key,summary,priority,status"
```

---

## Output Tips

- Use `--json` when you need to parse output or pass to other commands
- Use `--csv` for tabular data / reports
- Use `--yes` to skip confirmation prompts in bulk operations
- Use `--ignore-errors` in bulk ops so one failure doesn't stop the rest
- Use `--paginate` when expecting more results than the default limit
