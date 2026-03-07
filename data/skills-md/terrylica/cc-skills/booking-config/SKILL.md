---
name: booking-config
description: Cal.com event types, schedules, and availability configuration. TRIGGERS - event type, booking page, schedule, availability, create calendar, configure calcom, booking link.
allowed-tools: Read, Bash, Grep, Glob, Write, AskUserQuestion
---

# Booking Configuration

Configure Cal.com event types, schedules, and availability windows via CLI.

## Mandatory Preflight

### Step 1: Check CLI Binary

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

### Step 2: Verify Environment

```bash
echo "CALCOM_OP_UUID: ${CALCOM_OP_UUID:-NOT_SET}"
echo "CALCOM_API_URL: ${CALCOM_API_URL:-NOT_SET}"
```

**All must be SET.** If any are NOT_SET, run the setup command first.

### Step 3: Test API Access

```bash
CALCOM_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom"
$CALCOM_CLI event-types list 2>&1 | head -3
```

## Event Type Management

### Create Event Type

Use AskUserQuestion to collect required fields:

```
AskUserQuestion({
  questions: [{
    question: "What type of booking page do you want to create?",
    header: "Event Type",
    options: [
      { label: "30-min Meeting", description: "Standard 30-minute meeting slot" },
      { label: "60-min Interview", description: "Full hour interview session" },
      { label: "15-min Quick Call", description: "Brief check-in call" },
      { label: "Custom", description: "Specify custom duration and details" }
    ],
    multiSelect: false
  }]
})
```

```bash
CALCOM_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom"

# Create event type with collected details
$CALCOM_CLI event-types create \
  --title "30min Interview" \
  --slug "interview-30" \
  --length 30 \
  --description "Screening interview for VA candidates"
```

### Update Event Type

```bash
# Update title
$CALCOM_CLI event-types update <id> --title "Updated Title"

# Update duration
$CALCOM_CLI event-types update <id> --length 45

# Disable event type
$CALCOM_CLI event-types update <id> --hidden true
```

## Schedule Management

### List Schedules

```bash
$CALCOM_CLI schedules list
```

### Create Schedule

```bash
# Create a weekday schedule (9am-5pm)
$CALCOM_CLI schedules create \
  --name "Business Hours" \
  --timezone "America/New_York" \
  --availability '[
    {"days": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00"}
  ]'
```

### Check Availability

```bash
# Check available slots for a specific date range
$CALCOM_CLI availability check \
  --event-type-id <id> \
  --start "2026-02-15" \
  --end "2026-02-20"
```

## Common Booking Page Patterns

### Candidate Screening Interview

```bash
$CALCOM_CLI event-types create \
  --title "VA Screening Interview" \
  --slug "va-screening" \
  --length 30 \
  --description "BruntWork virtual assistant candidate screening" \
  --requires-confirmation true
```

### Open Office Hours

```bash
$CALCOM_CLI event-types create \
  --title "Office Hours" \
  --slug "office-hours" \
  --length 15 \
  --description "Drop-in office hours for team questions"
```

## Webhook Management

Manage Cal.com webhooks for real-time Pushover notifications via the webhook relay.

### List Webhooks

```bash
CALCOM_API_KEY=$(op item get "$CALCOM_OP_UUID" --vault "Claude Automation" --fields password --reveal)

curl -s "https://api.cal.com/v1/webhooks?apiKey=$CALCOM_API_KEY" | python3 -m json.tool
```

### Register Webhook

```bash
curl -s -X POST "https://api.cal.com/v1/webhooks?apiKey=$CALCOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"subscriberUrl\":\"$WEBHOOK_RELAY_URL\",\"eventTriggers\":[\"BOOKING_CREATED\",\"BOOKING_RESCHEDULED\",\"BOOKING_CANCELLED\"],\"active\":true}"
```

### Delete Webhook

```bash
curl -s -X DELETE "https://api.cal.com/v1/webhooks/<webhook-id>?apiKey=$CALCOM_API_KEY"
```

**Prerequisites**: `WEBHOOK_RELAY_URL` must be set in `.mise.local.toml`. Deploy the relay first via the `infra-deploy` skill.

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
