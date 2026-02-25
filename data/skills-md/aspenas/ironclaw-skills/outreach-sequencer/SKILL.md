---
name: outreach-sequencer
description: Create and manage multi-step outreach sequences — LinkedIn messages, cold emails, and follow-ups with personalization. Use when asked to "send outreach", "create email sequence", "follow up with leads", "start a drip campaign", "send LinkedIn messages", "personalized outreach", or any automated multi-step communication workflow.
metadata: { "openclaw": { "emoji": "📨" } }
---

# Outreach Sequencer — Multi-Step Personalized Campaigns

Design, schedule, and execute multi-step outreach sequences across LinkedIn and email. Each message is personalized per lead using their profile data from DuckDB.

## Sequence Templates

### Template 1: LinkedIn Connection + Message
```
Day 0: Send LinkedIn connection request (with note)
Day 1: If accepted → Send intro message
Day 3: If no reply → Follow-up message
Day 7: If no reply → Break-up / value-add message
```

### Template 2: Cold Email Sequence
```
Day 0: Initial cold email
Day 3: Follow-up (reply to original thread)
Day 7: Value-add email (case study, resource)
Day 14: Break-up email ("closing the loop")
```

### Template 3: Multi-Channel
```
Day 0: LinkedIn connection request
Day 2: Cold email (if not connected on LinkedIn)
Day 4: LinkedIn message (if connected) OR email follow-up
Day 7: Final touch (whichever channel they engaged on)
```

## Personalization Engine

Each message is generated per-lead using their DuckDB profile data. Use these variables:

| Variable | Source | Example |
|----------|--------|---------|
| `{first_name}` | Name field (split) | "Jane" |
| `{company}` | Company field | "Acme Corp" |
| `{title}` | Title field | "CTO" |
| `{mutual}` | Shared connections/background | "Stanford" |
| `{trigger}` | Why reaching out now | "saw your Series A" |
| `{value_prop}` | What you offer them | "AI-powered analytics" |
| `{pain_point}` | Their likely challenge | "scaling engineering team" |

### Personalization Rules
- **Never use generic openers** like "I hope this finds you well"
- **Reference something specific**: recent post, company news, shared background
- **Keep LinkedIn messages under 300 chars** (connection note limit)
- **Keep cold emails under 150 words** (respect attention)
- **Vary language across leads** — don't send identical messages to people at the same company
- **Match tone to seniority**: C-suite gets concise/strategic, ICs get technical/peer-level

### Message Generation Pattern
```
1. Read lead profile from DuckDB
2. Identify personalization hooks:
   - Shared background (school, company, location)
   - Recent company news (web search if needed)
   - Role-specific pain points
3. Select message template for sequence step
4. Generate personalized message
5. Store message + status in DuckDB
```

## Execution

### LinkedIn Messages (via Browser)
```
browser → open LinkedIn messaging
browser → search for recipient
browser → open conversation
browser → type personalized message
browser → send
→ Update DuckDB status: "Sent"
```

### Email (via gog CLI)
```bash
gog gmail send \
  --to "{email}" \
  --subject "{subject}" \
  --body "{personalized_body}" \
  --account patrick@candlefish.ai
```

For follow-ups (reply to thread):
```bash
gog gmail reply \
  --thread-id "{thread_id}" \
  --body "{follow_up_body}"
```

## Sequence Status Tracking

Track in DuckDB with these status fields:

| Field | Values | Notes |
|-------|--------|-------|
| Outreach Status | Queued, Sent, Replied, Converted, Bounced, Opted Out | Main status |
| Sequence Step | 1, 2, 3, 4 | Current step in sequence |
| Last Outreach | date | When last message was sent |
| Next Outreach | date | When next step is due |
| Outreach Channel | LinkedIn, Email, Both | Active channel |
| Reply Received | boolean | True if they responded |
| Thread ID | text | Gmail thread ID for email chains |

```sql
-- Find leads due for next sequence step
SELECT "Name", "Email", "Outreach Status", "Sequence Step", "Next Outreach"
FROM v_leads
WHERE "Outreach Status" = 'Sent'
  AND "Reply Received" = false
  AND "Next Outreach" <= CURRENT_DATE
ORDER BY "Next Outreach";
```

## Cron Integration

Set up automated sequence execution:

```
Schedule: Every 2 hours during business hours (9am-5pm Mon-Fri)
Action:
1. Query leads due for next step
2. For each due lead:
   a. Generate personalized message for their current step
   b. Send via appropriate channel
   c. Update status + advance step
   d. Set next outreach date
3. Report: "Sent 12 messages (8 LinkedIn, 4 email). 3 replies received."
```

### Cron Job Setup (for OpenClaw)
```json
{
  "name": "Outreach Sequencer",
  "schedule": { "kind": "cron", "expr": "0 9,11,13,15 * * 1-5", "tz": "America/Denver" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run outreach sequence check. Query DuckDB for leads with Next Outreach <= today. Send personalized messages for their current sequence step. Update statuses. Report results.",
    "timeoutSeconds": 300
  }
}
```

## Safety & Compliance

- **Daily send limits**: Max 50 LinkedIn connection requests/day, 100 messages/day
- **Email limits**: Max 100 cold emails/day (avoid spam flags)
- **Opt-out handling**: If someone replies "not interested" / "unsubscribe", immediately set status to "Opted Out" and never contact again
- **Bounce handling**: If email bounces, mark as "Bounced" and try alternate email patterns
- **CAN-SPAM compliance**: Include sender identity, physical address option, and opt-out mechanism in emails
- **LinkedIn ToS**: Keep connection notes professional, don't spam InMails
- **Cool-down**: If a lead hasn't replied after full sequence, wait 90 days before any re-engagement

## Analytics

After each sequence run, track:
```
Active Sequences: 85 leads
├── Step 1 (Initial): 20 leads
├── Step 2 (Follow-up): 35 leads
├── Step 3 (Value-add): 18 leads
├── Step 4 (Break-up): 12 leads
│
Outcomes:
├── Replied: 23 (27% reply rate)
├── Converted: 8 (9.4% conversion)
├── Opted Out: 3 (3.5%)
├── Bounced: 2 (2.4%)
└── No Response (completed): 15 (17.6%)
```
