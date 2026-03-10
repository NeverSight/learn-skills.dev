---
name: agentmail-cli
description: Send and receive emails programmatically using the AgentMail CLI. Use when agents need to manage inboxes, send/receive emails, handle threads, drafts, webhooks, and domains via command line.
---

# AgentMail CLI

Use the `agentmail` CLI to send and receive emails programmatically. Requires `AGENTMAIL_API_KEY` environment variable.

## Install

```bash
npm install -g agentmail-cli
```

## Core Commands

### Inboxes

```bash
# Create an inbox
agentmail inboxes create --display-name "My Agent" --username myagent --domain example.com

# List inboxes
agentmail inboxes list

# Get an inbox
agentmail inboxes retrieve --inbox-id <inbox_id>

# Delete an inbox
agentmail inboxes delete --inbox-id <inbox_id>
```

### Send Email

```bash
# Send a message from an inbox
agentmail inboxes:messages send --inbox-id <inbox_id> \
  --to "recipient@example.com" \
  --subject "Hello" \
  --text "Message body"

# Send with HTML
agentmail inboxes:messages send --inbox-id <inbox_id> \
  --to "recipient@example.com" \
  --subject "Hello" \
  --html "<h1>Hello</h1>"

# Reply to a message
agentmail inboxes:messages reply --inbox-id <inbox_id> --message-id <message_id> \
  --text "Reply body"

# Forward a message
agentmail inboxes:messages forward --inbox-id <inbox_id> --message-id <message_id> \
  --to "someone@example.com"
```

### Read Email

```bash
# List messages in an inbox
agentmail inboxes:messages list --inbox-id <inbox_id>

# Get a specific message
agentmail inboxes:messages retrieve --inbox-id <inbox_id> --message-id <message_id>

# List threads
agentmail inboxes:threads list --inbox-id <inbox_id>

# Get a thread
agentmail inboxes:threads retrieve --inbox-id <inbox_id> --thread-id <thread_id>
```

### Drafts

```bash
# Create a draft
agentmail inboxes:drafts create --inbox-id <inbox_id> \
  --to "recipient@example.com" \
  --subject "Draft" \
  --text "Draft body"

# Send a draft
agentmail inboxes:drafts send --inbox-id <inbox_id> --draft-id <draft_id>
```

### Pods

Pods group inboxes together.

```bash
# Create a pod
agentmail pods create --name "My Pod"

# Create an inbox in a pod
agentmail pods:inboxes create --pod-id <pod_id> --display-name "Pod Inbox"

# List threads in a pod
agentmail pods:threads list --pod-id <pod_id>
```

### Webhooks

```bash
# Create a webhook for new messages
agentmail webhooks create --url "https://example.com/webhook" --event-type message.received

# List webhooks
agentmail webhooks list
```

### Domains

```bash
# Add a custom domain
agentmail domains create --domain example.com --feedback-enabled false

# Verify domain DNS
agentmail domains verify --domain-id <domain_id>

# Get DNS records to configure
agentmail domains get-zone-file --domain-id <domain_id>
```

## Global Flags

All commands support: `--api-key`, `--base-url`, `--environment`, `--format`, `--debug`.

## Output Formats

Use `--format` to control output: `json` (default), `pretty`, `yaml`, `jsonl`, `raw`, `explore`.
