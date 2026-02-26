---
name: migma
description: Generate, send, validate, and export AI-powered emails from the terminal; manage contacts, segments, tags, domains, and webhooks with Migma CLI.
metadata:
  openclaw:
    requires:
      env:
        - MIGMA_API_KEY
      bins:
        - migma
    primaryEnv: MIGMA_API_KEY
    emoji: "\u2709"
    homepage: https://migma.ai
    install:
      - kind: node
        package: "@migma/cli"
        bins: [migma]
---

# Migma

Create and send professional, on-brand emails with AI. Your agent can design emails from a prompt, send them instantly through a managed domain, and manage an entire audience — all from the terminal.

Always pass `--json` for structured output.

## Authentication

```bash
migma login                          # Authenticate with your API key
migma whoami --json                  # Show current user info
migma logout                         # Remove stored credentials
```

## First-time setup

If the user hasn't set up yet, run these steps once:

```bash
# 1. Create an instant sending domain (no DNS needed)
migma domains managed create <companyname> --json
# → Sends from: hello@<companyname>.migma.email

# 2. Set a default project (brand)
migma projects list --json
migma projects use <projectId>
```

## Before creating an email

Before generating a new email, check if the user wants to build on existing work (series, follow-up, remix, or similar email). List recent emails to find relevant references:

```bash
migma emails list --project <projectId> --limit 5 --json
```

If the user mentions a series, follow-up, remix, or "something similar to…", show the recent emails and ask which to use as a reference. Then pass the conversation ID with `--reference`:

```bash
migma generate "Follow-up to the welcome email" --reference <conversationId> --wait --json
```

If the user is creating something entirely new, skip this step.

## Create an email

When the user asks to create, design, or generate an email:

```bash
migma generate "Welcome email for new subscribers" --wait --json
```

The `--wait` flag blocks until the AI finishes. The JSON response includes `conversationId`, `subject`, and `html`.

To save the HTML locally, add `--save ./email.html`. To include a reference image (screenshot, design mockup), add `--image <url>`. To open the result in the browser, add `--open`.

### Check generation status

```bash
migma generate-status <conversationId> --json
```

## Create an email series or remix

When the user wants to create a series of emails or remix an existing email:

1. List existing emails to find the reference:
   ```bash
   migma emails list --project <projectId> --json
   ```

2. Generate each email in the series using `--reference` to maintain consistency:
   ```bash
   migma generate "Email 1: Welcome to the course" --wait --json
   migma generate "Email 2: Your first lesson" --reference <email1ConversationId> --wait --json
   migma generate "Email 3: Advanced tips" --reference <email2ConversationId> --wait --json
   ```

The `--reference` flag tells MigmaAI to use the referenced email as context — matching its style, tone, and layout while generating new content.

## List and search emails

```bash
migma emails list --project <projectId> --json
migma emails list --project <projectId> --limit 10 --status completed --json
migma emails list --project <projectId> --search "welcome" --json
```

Filters: `--limit <n>` (1-100, default 20), `--status <pending|processing|completed|failed>`, `--search <query>`.

## Send an email

When the user asks to send an email to someone:

```bash
# Send a generated email directly
migma send --to sarah@example.com --subject "Welcome!" \
  --from-conversation <conversationId> \
  --from hello@company.migma.email --from-name "Company" --json

# Or send from a local HTML file
migma send --to sarah@example.com --subject "Hello" \
  --html ./email.html \
  --from hello@company.migma.email --from-name "Company" --json

# Send to an entire segment or tag
migma send --segment <id> --subject "Big News" --html ./email.html \
  --from hello@company.migma.email --from-name "Company" --json

# Personalize with template variables
migma send --to user@example.com --subject "Hi {{name}}" --html ./email.html \
  --from hello@company.migma.email --from-name "Company" \
  --var name=Sarah --var discount=20 --json

# Transactional email (bypasses subscription status and topic filters)
migma send --to user@example.com --subject "Your receipt" \
  --html ./receipt.html --transactional \
  --from hello@company.migma.email --from-name "Company" --json

# Custom reply-to address
migma send --to user@example.com --subject "Hello" \
  --html ./email.html --reply-to support@company.com \
  --from hello@company.migma.email --from-name "Company" --json
```

`--from-conversation` auto-exports the HTML from a generated email — no separate export step.

### Send a test email

```bash
migma send-test <conversationId> --to test@company.com --json
```

### Check batch send status

```bash
migma batch-status <batchId> --json
```

## Validate an email

When the user wants to check an email before sending:

```bash
migma validate all --html ./email.html --json
migma validate all --conversation <conversationId> --json
migma validate all --html ./email.html --subject "Sale today!" --json
```

Returns an overall score plus individual checks: compatibility (30+ email clients), broken links, spelling/grammar, and deliverability/spam score.

Individual checks:

```bash
migma validate compatibility --html ./email.html --json
migma validate links --html ./email.html --json
migma validate spelling --html ./email.html --json
migma validate deliverability --html ./email.html --subject "Sale today!" --json
migma validate deliverability --conversation <conversationId> --subject "Sale today!" --json
```

The `--subject` flag provides the email subject for deliverability/spam analysis.

## Export to platforms

When the user wants to export to an ESP or download a file:

```bash
migma export html <conversationId> --output ./email.html
migma export mjml <conversationId> --output ./email.mjml
migma export pdf <conversationId> --output ./email.pdf --json
migma export klaviyo <conversationId> --type html --json
migma export mailchimp <conversationId> --json
migma export hubspot <conversationId> --json
```

Klaviyo export supports `--type <html|hybrid|code>` (default: html). All export commands support `--output <file>` to save locally.

## Manage contacts

```bash
# Add a contact (full options)
migma contacts add --email user@example.com --first-name John --last-name Doe \
  --country US --language en --tags tag1,tag2 --json

# List contacts with filters
migma contacts list --json
migma contacts list --status subscribed --tags tagId1,tagId2 --search "john" --json
migma contacts list --limit 50 --page 2 --json

# Get, update, remove
migma contacts get <id> --json
migma contacts update <id> --first-name Jane --status subscribed --json
migma contacts remove <id> --json

# Bulk import from CSV
migma contacts import ./contacts.csv --json
```

Contact list filters: `--limit <n>` (default 20), `--page <n>`, `--status <status>`, `--tags <comma-separated>`, `--search <query>`.

## Manage tags

```bash
migma tags create --name "VIP" --color "#FF5733" --description "High-value customers" --json
migma tags list --json
migma tags list --search "vip" --sort-by name --json
migma tags delete <id> --json
```

Tag list options: `--limit <n>` (default 50), `--search <query>`, `--sort-by <createdAt|name>`.

## Manage segments

```bash
migma segments create --name "Active Users" --description "Users active in last 30 days" --json
migma segments create --name "VIP Subscribers" --tags tagId1,tagId2 --status subscribed --json
migma segments list --json
migma segments get <id> --json
migma segments delete <id> --json
```

## Manage sending domains

```bash
# List all domains
migma domains list --json

# Add a custom domain (requires DNS setup)
migma domains add yourdomain.com --json
migma domains add yourdomain.com --region eu-west-1 --json

# Verify DNS records
migma domains verify yourdomain.com --json

# Instant managed domain (no DNS needed)
migma domains managed create companyname --json
# → hello@companyname.migma.email is ready immediately

# Remove a managed domain
migma domains managed delete companyname.migma.email --json
```

## Manage webhooks

```bash
# List webhooks
migma webhooks list --json

# Create a webhook
migma webhooks create \
  --url https://yourserver.com/webhook \
  --events email.sent,email.delivered,email.bounced \
  --description "Production webhook" --json

# Test a webhook (sends a test payload)
migma webhooks test <webhookId> --json

# Delete a webhook
migma webhooks delete <webhookId> --json
```

## Import a brand

When the user wants to set up a new brand from their website:

```bash
migma projects import https://yourbrand.com --wait --json
migma projects use <projectId>
```

This fetches logos, colors, fonts, and brand voice automatically.

## Error handling

On error, `--json` returns:

```json
{"error": {"message": "Not found", "code": "not_found", "statusCode": 404}}
```
