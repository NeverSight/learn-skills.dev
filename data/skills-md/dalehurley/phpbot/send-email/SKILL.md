---
name: send-email
description: "Send emails via SMTP or API. Use this skill when the user asks to send an email, email someone, compose and send a message via email, or notify someone by email. Supports attachments, HTML body, and multiple recipients."
tags: [email, smtp, send, mail, notification, utility]
version: 0.1.0
---

# Skill: send-email

## When to Use

Use this skill when the user asks to:

- Send an email
- Email someone a message
- Compose and send an email
- Notify someone via email
- Send an email with an attachment

## Required Credentials

Retrieve these via the `get_keys` tool before executing:

| Key Store Key | Environment Variable | Description                                  |
| ------------- | -------------------- | -------------------------------------------- |
| `smtp_host`   | `SMTP_HOST`          | SMTP server hostname (e.g., smtp.gmail.com)  |
| `smtp_port`   | `SMTP_PORT`          | SMTP port (587 for TLS, 465 for SSL)         |
| `smtp_user`   | `SMTP_USER`          | SMTP username (usually email address)        |
| `smtp_pass`   | `SMTP_PASS`          | SMTP password or app password                |
| `email_from`  | `EMAIL_FROM`         | Sender email address (defaults to SMTP_USER) |

### Gmail Setup

For Gmail, use an App Password:

1. Enable 2-Step Verification on your Google account
2. Go to Security > App passwords > Generate
3. Use `smtp.gmail.com` port `587` with the app password

## Input Parameters

| Parameter    | Required | Description                         | Example                |
| ------------ | -------- | ----------------------------------- | ---------------------- |
| `to`         | Yes      | Recipient email(s), comma-separated | user@example.com       |
| `subject`    | Yes      | Email subject line                  | Meeting Tomorrow       |
| `body`       | Yes      | Email body content                  | Hi, just a reminder... |
| `attachment` | No       | File path to attach                 | /path/to/report.pdf    |
| `html`       | No       | Send body as HTML (flag)            | --html                 |
| `cc`         | No       | CC recipients, comma-separated      | boss@example.com       |

## Procedure

1. Retrieve SMTP credentials: use `get_keys` with keys `[smtp_host, smtp_port, smtp_user, smtp_pass, email_from]`
2. If any credentials are missing: try `search_computer`, then `ask_user`, then `store_keys`
3. If recipient, subject, or body not provided, ask the user via `ask_user`
4. Send the email:
   ```bash
   python3 skills/send-email/scripts/send.py \
     --to "recipient@example.com" \
     --subject "Hello" \
     --body "This is the message body"
   ```
   With attachment:
   ```bash
   python3 skills/send-email/scripts/send.py \
     --to "recipient@example.com" \
     --subject "Report attached" \
     --body "Please find the report attached." \
     --attachment /path/to/report.pdf
   ```
5. Verify the script reports success
6. Report delivery status to the user

## Bundled Scripts

| Script            | Type   | Description         |
| ----------------- | ------ | ------------------- |
| `scripts/send.py` | Python | Send email via SMTP |

### Script Usage

```bash
# Set credentials as environment variables (from get_keys), then:

# Simple email
python3 scripts/send.py --to "user@example.com" --subject "Hello" --body "Hi there!"

# With attachment
python3 scripts/send.py --to "user@example.com" --subject "Report" --body "See attached." --attachment report.pdf

# HTML email
python3 scripts/send.py --to "user@example.com" --subject "Newsletter" --body "<h1>Hello</h1><p>Content</p>" --html

# Multiple recipients
python3 scripts/send.py --to "a@example.com,b@example.com" --cc "c@example.com" --subject "Team Update" --body "..."
```

## Example

```
send an email to john@example.com saying "meeting at 3pm"
email the report to my boss
send an email with the PDF attached
compose an email to the team about the project update
```
