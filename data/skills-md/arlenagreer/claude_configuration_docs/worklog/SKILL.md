---
name: worklog
description: Track billable hours for clients. This skill should be used when the user requests to log work hours, record time spent on client projects, view worklog entries, calculate total billable hours, or summarize recent work. Automatically prompts for missing information (client, hours, description) and validates client names against the invoice skill's client database.
---

# Worklog Skill

Track billable hours for clients with automatic client validation and integration with the invoice skill.

## Purpose

This skill helps track time spent on client work by maintaining a detailed worklog with client names, dates, hours worked, and work descriptions. It integrates with the invoice skill by reading client information from `~/.claude/skills/invoice/clients.json` to ensure consistency and enable accurate billing.

## When to Use This Skill

Use this skill when:
- The user requests to log work hours for a client
- The user asks to record time spent on a project
- The user wants to view past worklog entries
- The user needs to calculate total hours worked (overall or by client/date range)
- The user asks to summarize work done in the current session for logging
- The user mentions tracking billable hours or time tracking

## How to Use This Skill

### Core Workflow

When the user requests to log work:

1. **Determine the current date** - ALWAYS check the system clock using `date +%Y-%m-%d` to get the current date. Never assume the date based on training cutoff.

2. **Identify required information**:
   - **Client name** - If not provided, list available clients using the worklog manager and ask the user to specify
   - **Hours worked** - If not provided, ask the user to confirm the number of hours
   - **Work description** - If not provided, ask the user for a description
   - **Date** - Use current date unless the user specifies a different date for retroactive entry

3. **Validate client name** - The script automatically validates against the invoice skill's client list. Valid client names are:
   - "American Laboratory Trading" (aliases: "ALT", "alt")
   - "Empirico"
   - "Versa Computing"

4. **Create work description**:
   - If user provides a description, use it as-is
   - If user asks to summarize current session's work, analyze the conversation and recent code changes to create a brief but detailed summary
   - Description should be **one paragraph typically**, but can be several paragraphs if needed to accurately describe the work
   - Focus on what was accomplished, problems solved, features implemented, or issues addressed
   - Be specific about technical details when relevant

5. **Add the entry** using the worklog manager script

### Available Operations

#### List Available Clients

```bash
python3 scripts/worklog_manager.py clients
```

This displays all clients from the invoice skill with their billing type and hourly rate (if applicable).

#### Add Worklog Entry

```bash
python3 scripts/worklog_manager.py add \
  --client "Client Name" \
  --hours 2.5 \
  --description "Work description here" \
  --date 2025-11-01  # Optional, defaults to today
```

**Important**:
- Client name must exactly match a name from the invoice skill (or use a supported alias)
- Hours must be a positive number (can include decimals like 2.5)
- Date format must be YYYY-MM-DD
- If date is omitted, the current date is used automatically

#### Client Aliases

For convenience, the worklog skill supports client name aliases:

- **"ALT"** or **"alt"** → "American Laboratory Trading"

You can use these aliases in any command that accepts a client name:

```bash
# These are equivalent:
python3 scripts/worklog_manager.py add --client "ALT" --hours 2 --description "Work done"
python3 scripts/worklog_manager.py add --client "American Laboratory Trading" --hours 2 --description "Work done"

# Aliases also work for filtering and totals:
python3 scripts/worklog_manager.py list --client "ALT"
python3 scripts/worklog_manager.py total --client "alt"
```

All entries are stored using the canonical client name ("American Laboratory Trading"), so aliases are purely a convenience for input.

#### List Worklog Entries

```bash
# List all entries
python3 scripts/worklog_manager.py list

# Filter by client
python3 scripts/worklog_manager.py list --client "American Laboratory Trading"

# Filter by date range
python3 scripts/worklog_manager.py list --start-date 2025-10-01 --end-date 2025-10-31

# Get JSON output for processing
python3 scripts/worklog_manager.py list --format json
```

#### Calculate Total Hours

```bash
# Total hours for all clients
python3 scripts/worklog_manager.py total

# Total for specific client
python3 scripts/worklog_manager.py total --client "Empirico"

# Total for date range
python3 scripts/worklog_manager.py total --start-date 2025-10-01 --end-date 2025-10-31
```

For hourly clients, this also calculates the billable amount using the rate from the invoice skill.

#### Delete Entry

```bash
# First list entries to see indices
python3 scripts/worklog_manager.py list

# Delete entry at index (0-based)
python3 scripts/worklog_manager.py delete 0
```

### Example Interactions

**Example 1: User provides all information**
```
User: "Log 3 hours for American Laboratory Trading - implemented user authentication system with JWT tokens"

Action: Add entry with provided information using current date
```

**Example 2: User asks to log work without details**
```
User: "Log my work hours"

Claude: "I'll help you log your work hours. Which client is this for? Available clients:
- American Laboratory Trading ($100/hr)
- Empirico (subscription)
- Versa Computing ($100/hr)"

User: "American Laboratory Trading"

Claude: "How many hours did you work?"

User: "2.5 hours"

Claude: "What work did you complete?"

User: "Fixed the login bug and updated the database schema"

Action: Add entry with gathered information
```

**Example 3: User asks to summarize session work**
```
User: "Log my work for Versa Computing - summarize what we did today"

Claude: [Analyzes conversation and recent changes, creates summary like:]
"During this session, implemented a new worklog tracking system that integrates with the existing invoice skill. Created a Python script for managing time entries with client validation, date handling, and reporting features. The system maintains worklog data in JSON format and reads client information from the invoice skill to ensure consistency. Added functionality for adding entries, listing work by client and date range, calculating total hours, and deleting entries."

Action: Ask user to confirm hours, then add entry with generated summary
```

**Example 4: Retroactive entry**
```
User: "Add a worklog entry for yesterday - 4 hours on Empirico, worked on the subscription billing integration"

Action: Calculate yesterday's date using system clock, add entry with that date
```

### Data Files

- **Worklog data**: Stored in `~/.claude/skills/worklog/worklog.json`
- **Client data**: Read from `~/.claude/skills/invoice/clients.json` (read-only)

The worklog skill never modifies the invoice skill's client data - it only reads it for validation and billing rate information.

### Integration with Invoice Skill

This skill integrates with the invoice skill by:
1. Reading the client list to validate client names
2. Using client hourly rates to calculate billable amounts in reports
3. Ensuring client names are consistent between worklog entries and invoices

When creating invoices, reference worklog entries to ensure accurate billing.

### Error Handling

- If an invalid client name is provided, the script will list valid clients and prompt for correction
- If hours are zero or negative, an error will be shown
- If the date format is incorrect, an error will be shown with the expected format
- If the invoice skill's clients.json file is not found, an error will be shown

### Best Practices

1. **Get current date first** - Always run `date +%Y-%m-%d` before logging entries to ensure accuracy
2. **Prompt for confirmation** - When hours are not specified, ask the user to confirm
3. **Create detailed descriptions** - When summarizing work, be specific about accomplishments
4. **Validate client names** - Always use exact client names from the invoice skill
5. **Use consistent formatting** - Keep descriptions professional and focused on deliverables
