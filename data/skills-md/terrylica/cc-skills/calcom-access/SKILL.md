---
name: calcom-access
description: Access Cal.com API via CLI with 1Password API key. Use when user wants to list bookings, create event types, manage schedules, or mentions cal.com access. TRIGGERS - calcom, cal.com, bookings, list bookings, event types, schedules, availability, create booking page.
allowed-tools: Read, Bash, Grep, Glob, Write, AskUserQuestion
---

# Cal.com Access

Manage Cal.com bookings and event types programmatically via Claude Code CLI.

## MANDATORY PREFLIGHT (Execute Before Any Cal.com Operation)

**CRITICAL**: You MUST complete this preflight checklist before running any Cal.com commands. Do NOT skip steps.

### Step 1: Check CLI Binary Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

**If BINARY_NOT_FOUND**: Build it first:

```bash
cd ~/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli && bun install && bun run build
```

### Step 2: Check CALCOM_OP_UUID Environment Variable

```bash
echo "CALCOM_OP_UUID: ${CALCOM_OP_UUID:-NOT_SET}"
```

**If NOT_SET**: You MUST run the Setup Flow below. Do NOT proceed to Cal.com commands.

### Step 3: Verify 1Password Authentication

```bash
op account list 2>&1 | head -3
```

**If error or not signed in**: Inform user to run `op signin` first.

### Step 4: Test API Connectivity

```bash
CALCOM_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom"
$CALCOM_CLI event-types list 2>&1 | head -5
```

---

## Setup Flow (When CALCOM_OP_UUID is NOT_SET)

Follow these steps IN ORDER. Use AskUserQuestion at decision points.

### Setup Step 1: Check 1Password CLI

```bash
command -v op && echo "OP_CLI_INSTALLED" || echo "OP_CLI_MISSING"
```

**If OP_CLI_MISSING**: Stop and inform user:

> 1Password CLI is required. Install with: `brew install 1password-cli`

### Setup Step 2: Discover Cal.com API Keys in 1Password

```bash
op item list --vault "Claude Automation" --format json 2>/dev/null | jq -r '.[] | select(.title | test("calcom|cal.com|calendar"; "i")) | "\(.id)\t\(.title)"'
```

**Parse the output** and proceed based on results.

### Setup Step 3: User Selects API Credentials

**If items found**, use AskUserQuestion with discovered items.

**If NO items found**, guide the user:

1. Log into the Cal.com instance (self-hosted or cal.com)
2. Go to Settings > Developer > API Keys
3. Generate a new API key with appropriate scopes
4. Store in 1Password Claude Automation vault:

```bash
op item create --category "API Credential" --title "Cal.com API Key" \
  --vault "Claude Automation" \
  "credential=<api-key>" \
  "api_url=<cal.com-instance-url>"
```

### Setup Step 4: Configure mise

After user selects an item (with UUID), use AskUserQuestion to confirm adding to `.mise.local.toml`:

```toml
[env]
CALCOM_OP_UUID = "<selected-uuid>"
```

### Setup Step 5: Reload and Verify

```bash
mise trust 2>/dev/null || true
cd . && echo "CALCOM_OP_UUID after reload: ${CALCOM_OP_UUID:-NOT_SET}"
```

### Setup Step 6: Test Connection

```bash
CALCOM_OP_UUID="${CALCOM_OP_UUID}" $HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom event-types list
```

---

## Cal.com Commands (Only After Preflight Passes)

```bash
CALCOM_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom"

# List event types
$CALCOM_CLI event-types list

# List bookings
$CALCOM_CLI bookings list -n 10

# List bookings by status
$CALCOM_CLI bookings list --status upcoming -n 20

# Get booking details
$CALCOM_CLI bookings get <booking_id>

# Create event type
$CALCOM_CLI event-types create --title "30min Interview" --slug "interview-30" --length 30

# Update event type
$CALCOM_CLI event-types update <event_type_id> --title "Updated Title"

# List schedules (availability)
$CALCOM_CLI schedules list

# JSON output (for parsing)
$CALCOM_CLI bookings list -n 10 --json
```

## Cal.com API v2 Reference

| Endpoint     | CLI Command          | Description               |
| ------------ | -------------------- | ------------------------- |
| Event Types  | `event-types list`   | List all event types      |
| Event Types  | `event-types create` | Create new event type     |
| Bookings     | `bookings list`      | List bookings             |
| Bookings     | `bookings get`       | Get booking details       |
| Bookings     | `bookings cancel`    | Cancel a booking          |
| Schedules    | `schedules list`     | List availability windows |
| Schedules    | `schedules create`   | Create availability       |
| Availability | `availability check` | Check slot availability   |

## Environment Variables

| Variable         | Required | Description                         |
| ---------------- | -------- | ----------------------------------- |
| `CALCOM_OP_UUID` | Yes      | 1Password item UUID for API key     |
| `CALCOM_API_URL` | No       | API base URL (default: self-hosted) |

## References

- [calcom-api-setup.md](./references/calcom-api-setup.md) - Cal.com API key setup guide
- [mise-setup.md](./references/mise-setup.md) - Step-by-step mise configuration

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
- [ ] References exist and are linked
