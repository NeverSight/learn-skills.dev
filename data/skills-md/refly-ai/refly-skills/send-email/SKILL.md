---
name: send-email
description: "Send emails with HTML content. Use when you need to: (1) send emails to recipients, (2) compose HTML formatted email content, or (3) include file attachments in emails."
version: 1.0.0
skillId: skp-wyrq1wha0i2ktf9jrbcggaiq
workflowId: c-cuy4kkudipdg0cicfa1i68q6
installationId: skpi-sy53dei9rlmgqe5x8bzskvmh
category: action
---

# Send Email

Send emails with HTML content. Use when you need to: (1) send emails to recipients, (2) compose HTML formatted email content, or (3) include file attachments in emails.

## Input

Provide input as JSON:

```json
{
  "to": "Recipient email address (e.g., user@example.com). Optional - defaults to current user.",
  "subject": "Email subject line",
  "html": "HTML content of the email body",
  "attachments": "Optional array of file attachments using file-content://df-<fileId> format"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-sy53dei9rlmgqe5x8bzskvmh --input '{
  "to": "recipient@example.com",
  "subject": "Test Email",
  "html": "<h1>Hello</h1><p>This is a test email.</p>"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-cuy4kkudipdg0cicfa1i68q6"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm email sent
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## With Attachments

To send email with file attachments:

```bash
RESULT=$(refly skill run --id skpi-sy53dei9rlmgqe5x8bzskvmh --input '{
  "to": "recipient@example.com",
  "subject": "Report with Attachment",
  "html": "<p>Please see attached.</p>",
  "attachments": ["file-content://df-abc123xyz"]
}')
```

## Expected Output

- **Type**: Confirmation
- **Format**: Email delivery status
- **Action**: Confirm email sent successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
