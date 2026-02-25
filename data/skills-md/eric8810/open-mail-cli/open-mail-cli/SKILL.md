---
name: open-mail-cli
description: >
  Gives the agent the ability to send, receive, search, and manage emails directly from the terminal
  or via a local HTTP API. Use this skill when the agent needs to handle email tasks: sending messages,
  reading inbox, replying, forwarding, managing contacts, organizing with tags/folders/filters,
  scheduling background sync, setting up webhooks for new email events, or automating email workflows.
  Supports structured output (--format json/markdown/html), field selection (--fields), standardized
  exit codes, and a local REST API with OpenAPI docs. Works with IMAP/SMTP providers including Gmail,
  Outlook, QQ Mail, and others. Activates on keywords: send email, check inbox, reply, forward,
  email automation, contacts, email template, notifications, webhook, http api, format json,
  field selection, serve, openapi.
---

# Open Mail CLI - Agent Email Toolkit

This skill equips the agent with a full-featured email client accessible via the `mail-cli` command. The agent can send, receive, search, organize, and automate emails entirely from the terminal through IMAP/SMTP protocols, with offline-first local storage. It also provides a local HTTP API server for programmatic integration.

## Installation

```bash
npm install -g open-mail-cli
# Requirements: Node.js >= 18.0.0
```

## Getting Started

### 1. Configure an Email Account

```bash
# Interactive wizard (recommended)
mail-cli config

# Or manual setup
mail-cli account add --email user@gmail.com --name "My Gmail" \
  --imap-host imap.gmail.com --imap-port 993 \
  --smtp-host smtp.gmail.com --smtp-port 465 \
  --username user@gmail.com --password "app-password" --test
```

### 2. Sync, Read, and Send

```bash
mail-cli sync                # Fetch emails from server
mail-cli list --unread       # Browse unread emails
mail-cli list --format json --fields id,subject,from  # Structured output for parsing
mail-cli read <email-id>     # Read a specific email
mail-cli send --to user@example.com --subject "Hello" --body "Content"
```

## Capabilities Overview

Choose the reference that matches the task at hand. Each reference includes purpose, scenarios, best practices, and full command syntax.

### Output Control & Error Handling
> Reference: [references/output-and-errors.md](references/output-and-errors.md)

Control output format (`--format json/markdown/html`), select specific fields (`--fields`), and handle errors via standardized exit codes and JSON error output. Use this when the agent needs to parse command output programmatically or handle failures gracefully.

### Webhooks & HTTP API
> Reference: [references/webhooks-and-api.md](references/webhooks-and-api.md)

Register webhooks for email events, trigger scripts on new mail, and use the local HTTP API server with OpenAPI documentation. Use this when the agent needs real-time event-driven workflows or REST API integration.

### Sending & Composing
> Reference: [references/sending-and-replying.md](references/sending-and-replying.md)

Send emails, reply to conversations, forward messages, and manage drafts. Use this when the user needs to compose or respond to emails.

### Reading & Searching
> Reference: [references/reading-and-searching.md](references/reading-and-searching.md)

List, filter, read, and search emails. View conversations as threads. Use this when the user wants to check inbox, find specific emails, or follow a conversation.

### Organization
> Reference: [references/organization.md](references/organization.md)

Organize emails with tags, folders, stars, flags, and trash management. Use this when the user wants to categorize, prioritize, or clean up their mailbox.

### Accounts & Sync
> Reference: [references/accounts-and-sync.md](references/accounts-and-sync.md)

Manage multiple email accounts, configure IMAP/SMTP, run background sync daemon. Includes provider settings table (Gmail, Outlook, QQ Mail, etc.) and troubleshooting. Use this for setup, connectivity issues, or multi-account workflows.

### Automation
> Reference: [references/automation.md](references/automation.md)

Email templates with variables, signatures, desktop notifications, spam filtering, contact management, and import/export. Use this when the user wants to automate repetitive email tasks or manage contacts and spam.

## Key Principles

- **Sync before read**: Local storage is offline-first. Always `mail-cli sync` before listing or searching if fresh data is expected.
- **Confirm before send**: Always verify recipient, subject, and content with the user before executing `send`, `reply`, or `forward`.
- **Non-destructive by default**: `delete` moves to trash. Only use `--permanent` when the user explicitly requests irreversible deletion.
- **Use `--yes` for automation**: Skip interactive confirmation prompts in automated workflows.
- **Use `--format json` for parsing**: When the agent needs to parse output programmatically, use JSON format. Use `--format markdown` when output is consumed by an LLM.
- **Use `--fields` to reduce noise**: Request only the fields needed (e.g. `--fields id,subject,from`) to keep output focused and reduce token usage.
- **Check exit codes for error handling**: Exit codes indicate error category (0=success, 1=general, 2=validation, 3=network, 4=auth). Branch logic based on exit code instead of parsing error text.
- **Templates over repetition**: If the user sends similar emails more than twice, create a template.
- **Tags for cross-cutting, folders for exclusive**: An email can have multiple tags but belongs to one folder.
