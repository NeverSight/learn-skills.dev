---
name: hunter
description: "Find emails with Hunter.io. Use when you need to: (1) discover professional email addresses, (2) verify email deliverability, or (3) find contacts at companies."
version: 1.0.0
skillId: skp-g7bj2qtltd8q0wugddjynbu0
workflowId: c-yy5s998sby8jaqrhmjnjq5im
installationId: skpi-a3b3p0zfu2gx7267xt1035ba
category: text-data
---

# Hunter

Find emails with Hunter.io. Use when you need to: (1) discover professional email addresses, (2) verify email deliverability, or (3) find contacts at companies.

## Input

Provide input as JSON:

```json
{
  "company_domain": "Company domain name to search for email addresses (e.g., apple.com, tesla.com)",
  "contact_name": "Full name of the person to find email for (optional, leave empty to search all emails at domain)",
  "email_to_verify": "Specific email address to verify (optional, for direct verification)"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-a3b3p0zfu2gx7267xt1035ba --input '{
  "domain": "example.com",
  "type": "all"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-yy5s998sby8jaqrhmjnjq5im"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get email data from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: Email addresses and contact data
- **Action**: Display email findings to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
