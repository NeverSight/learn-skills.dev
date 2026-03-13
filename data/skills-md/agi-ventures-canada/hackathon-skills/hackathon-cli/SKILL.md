---
name: hackathon-cli
model: sonnet
description: Use the hackathon CLI tool to manage hackathons from the terminal. Use when the user asks to create hackathons, add judges, manage prizes, or perform hackathon management tasks using the hackathon command-line tool.
activationKeywords:
  - "hackathon cli"
  - "hackathon command"
  - "create a hackathon"
  - "make a hackathon"
  - "add a judge"
  - "set up judging"
  - "add a prize"
  - "publish results"
  - "manage hackathon"
  - "hackathon on"
---

# Hackathon CLI — Oatmeal Command-Line Tool

Manage the Oatmeal hackathon platform from the terminal using the `hackathon` CLI (`@agi-ventures-canada/hackathon-cli`). This skill guides AI agents through using the CLI to create hackathons, manage judges, set up prizes, and publish results.

**For direct REST API access (curl commands, debugging endpoints), use the `hackathon-api` skill instead.**

## Reference Files

- `references/commands.md` — Complete CLI command reference with all flags and options
- `references/workflow-examples.md` — Natural language to CLI command mappings and end-to-end examples

## When to Activate

- User asks to create, update, or manage a hackathon using the CLI or terminal
- User asks to add/remove judges, sponsors, or prizes
- User asks to configure judging criteria or assignments
- User asks to calculate or publish results
- User gives natural language commands like "make me a hackathon on Sunday from 7am to 9pm"
- User mentions "oatmeal" in the context of hackathon management

## When NOT to Activate

- User wants to make direct REST API calls or curl commands (use `hackathon-api`)
- User is working on the Oatmeal codebase itself (editing source code, running tests)
- User is asking about general hackathon concepts (use `hackathon-organizer` or `hackathon-attendee`)
- User is working with the Oatmeal web dashboard UI directly

## Installation

### Install the CLI

```bash
npm install -g @agi-ventures-canada/hackathon-cli
# or
npx @agi-ventures-canada/hackathon-cli
```

Verify installation:

```bash
hackathon --version
```

### For local development (from the repo)

```bash
bun cli <args>           # Runs TypeScript source directly via Bun
```

### Login & Authentication

```bash
# Browser-based login (opens browser, creates API key automatically)
hackathon login

# Login against a local dev instance
hackathon login --base-url http://localhost:3000

# Or provide an API key directly
hackathon login --api-key sk_live_your_key_here

# Or set via environment variable
export HACKATHON_API_KEY=sk_live_your_key_here
export HACKATHON_BASE_URL=http://localhost:3000  # optional
```

Verify your setup:

```bash
hackathon whoami
```

Config is saved to `~/.hackathon/config.json`. The `--base-url` is remembered after login.

```bash
hackathon logout  # Remove saved credentials
```

## Command Structure

The CLI uses **positional arguments** for resource IDs, not `--hackathon` flags:

```
hackathon <resource> <action> <id> [sub-id] [--flags]
```

All commands support `--json` for machine-readable output and `--yes`/`-y` to skip confirmation prompts.

When required flags are omitted in a terminal (TTY), the CLI prompts interactively via `@clack/prompts`.

## Core Commands

### Public Browsing (no auth required)

```bash
hackathon browse hackathons                # Search public hackathons
hackathon browse submissions <slug>        # View submissions for a hackathon
hackathon browse results <slug>            # View published results
hackathon browse org <slug>                # View organization profile
```

### Hackathon Management

```bash
# List your hackathons
hackathon hackathons list

# Create a new hackathon (interactive prompts if flags omitted)
hackathon hackathons create --name "Sunday AI Hackathon" --slug "sunday-ai-hackathon"

# Get hackathon details (supports ID or slug)
hackathon hackathons get <id-or-slug>

# Update settings
hackathon hackathons update <id-or-slug> --name "Updated Name" --description "New description"

# Delete a hackathon
hackathon hackathons delete <id-or-slug>
```

### Judging — Judges

```bash
# List judges
hackathon judging judges list <hackathon-id>

# Add a judge by email (sends invitation if not found)
hackathon judging judges add <hackathon-id> --email judge@example.com

# Add a judge by user ID
hackathon judging judges add <hackathon-id> --user-id user_abc123

# Remove a judge
hackathon judging judges remove <hackathon-id> <participant-id>

# List pending judge invitations
hackathon judging invitations list <hackathon-id>

# Cancel a pending invitation
hackathon judging invitations cancel <hackathon-id> <invitation-id>
```

### Judging — Criteria

```bash
# List criteria
hackathon judging criteria list <hackathon-id>

# Create a criterion
hackathon judging criteria create <hackathon-id> \
  --name "Innovation" \
  --description "How novel and creative is the solution?" \
  --max-score 10 \
  --weight 1.0

# Update a criterion
hackathon judging criteria update <hackathon-id> <criteria-id> --weight 1.5

# Delete a criterion
hackathon judging criteria delete <hackathon-id> <criteria-id>
```

### Judging — Assignments

```bash
# Auto-assign judges to submissions
hackathon judging auto-assign <hackathon-id> --per-judge 5

# List assignments with progress
hackathon judging assignments list <hackathon-id>

# Manually assign a judge to a submission
hackathon judging assignments create <hackathon-id> --judge <pid> --submission <sid>

# Delete an assignment
hackathon judging assignments delete <hackathon-id> <assignment-id>

# View pick-based results
hackathon judging pick-results <hackathon-id>
```

### Prizes

```bash
# List prizes
hackathon prizes list <hackathon-id>

# Create a prize
hackathon prizes create <hackathon-id> \
  --name "First Place" \
  --description "Grand prize for the winning team" \
  --value "$5,000"

# Update a prize
hackathon prizes update <hackathon-id> <prize-id> --name "Grand Prize"

# Delete a prize
hackathon prizes delete <hackathon-id> <prize-id>

# Reorder prizes
hackathon prizes reorder <hackathon-id> <prize-id-1> <prize-id-2> <prize-id-3>

# Assign a prize to a submission
hackathon prizes assign <hackathon-id> <prize-id> --submission <submission-id>

# Unassign a prize
hackathon prizes unassign <hackathon-id> <prize-id> <submission-id>
```

### Judge Display

```bash
hackathon judge-display list <hackathon-id>
hackathon judge-display create <hackathon-id> --name "Judge Panel" ...
hackathon judge-display update <hackathon-id> <display-id> ...
hackathon judge-display delete <hackathon-id> <display-id>
hackathon judge-display reorder <hackathon-id> <id-1> <id-2> ...
```

### Results

```bash
# Calculate rankings from submitted scores
hackathon results calculate <hackathon-id>

# View results (organizer detail view)
hackathon results get <hackathon-id>

# Publish results (makes public, transitions to completed)
hackathon results publish <hackathon-id>

# Unpublish results
hackathon results unpublish <hackathon-id>
```

### Webhooks

```bash
# List webhooks
hackathon webhooks list

# Create a webhook
hackathon webhooks create \
  --url "https://your-endpoint.com/hook" \
  --events "submission.submitted,participant.registered"

# Delete a webhook
hackathon webhooks delete <webhook-id>
```

### Jobs

```bash
hackathon jobs list
hackathon jobs get <job-id>
hackathon jobs create --type <job-type> ...
hackathon jobs result <job-id>
hackathon jobs cancel <job-id>
```

### Schedules

```bash
hackathon schedules list
hackathon schedules create --name "Daily sync" ...
hackathon schedules get <schedule-id>
hackathon schedules update <schedule-id> ...
hackathon schedules delete <schedule-id>
```

## Global Options

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON instead of formatted table |
| `--yes`, `-y` | Skip confirmation prompts |
| `--base-url` | Override API base URL for this command |
| `--api-key` | Override API key for this command |
| `--help`, `-h` | Show help |
| `--version`, `-v` | Show version |

## Finding the Current Hackathon

When a user says "my current hackathon" or "my hackathon":

```bash
hackathon hackathons list
```

Look for the hackathon with `active` or `published` status. If ambiguous, ask which one they mean.

The CLI supports **slug resolution** — most commands that take a hackathon ID also accept a slug (e.g., `hackathon hackathons get my-hackathon-slug`).

## Date Handling

When users say things like "make me a hackathon on Sunday from 7am to 9pm":

1. **Parse the dates** — convert natural language to ISO 8601 timestamps
2. Use the user's timezone if known, otherwise ask
3. Create the hackathon first, then update dates via the dashboard or API (the CLI `create` command focuses on name/slug/description)
4. Default status is `draft` — remind the user to publish when ready

## Error Handling

Common errors:
- **"Not authenticated"** — run `hackathon login` or set `HACKATHON_API_KEY` env var
- **"Insufficient permissions"** — API key lacks required scope, create a new key with proper permissions
- **"Not found"** — verify the hackathon/resource ID exists with a list command
- **"Conflict"** — duplicate resource (slug already taken, already registered, etc.)

## Tips for AI Agents

1. **Always store IDs** — capture returned `id` values for use in subsequent commands
2. **Use `--json` flag** — parse output programmatically with `--json` for reliable ID extraction
3. **Check before creating** — list existing resources before creating duplicates
4. **Confirm destructive actions** — ask the user before deleting or publishing
5. **Batch operations** — when setting up a full hackathon, create criteria, prizes, then add judges
6. **Default to draft** — create hackathons in draft status, let the user decide when to publish
7. **Use `--yes`** — pass `-y` to skip interactive confirmations when running non-interactively

## Full Reference

For the complete command reference, see `references/commands.md`.

For end-to-end workflow examples, see `references/workflow-examples.md`.
