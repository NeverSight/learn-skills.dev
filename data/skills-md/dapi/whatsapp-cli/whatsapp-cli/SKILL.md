---
name: whatsapp-cli
description: >
  Use when the user wants to authenticate, sync, read, search, or send WhatsApp
  messages through the local whatsapp-cli user-account client. Also covers
  contacts, chats, joined groups, media downloads, and WhatsApp archive access.
  This is for the unofficial WhatsApp Web client, not the WhatsApp Business API.
---

# whatsapp-cli

Use `whatsapp-cli` for local WhatsApp user-account automation and archive access.

## Install

Install or update the CLI from this repository:

```bash
go install github.com/dapi/whatsapp-cli@main
```

Install this skill for supported agents:

```bash
npx skills add dapi/whatsapp-cli --skill whatsapp-cli --agent '*' -g -y
```

## Execution Rules

- Treat the WhatsApp store as a credential store. Never print, copy, commit, or
  delete its session database. By default it lives in the operating system's
  per-user application configuration directory.
- Use `whatsapp-cli sync` for first-time setup: it displays the QR code and
  captures the initial message history. `auth` links the account without
  running the archive sync.
- `sync` is long-running. Do not start a second instance for the same store.
- Reuse the same default store or the same explicit global `--store DIR` for all
  related commands. A missing store on a read/send command is not a reason to
  create a second store or relink the account.
- Resolve an ambiguous recipient with `contacts search`, `chats list`, or
  `groups list` before sending. Send only when the user's request authorizes it.
- If command syntax is uncertain, run `whatsapp-cli --help` or inspect the
  relevant command help instead of guessing flags.
- Commands return structured JSON. Parse the `success`, `data`, and `error`
  fields instead of scraping human-readable log output.

## Core Commands

### Authenticate and Sync

```bash
whatsapp-cli auth
whatsapp-cli sync
whatsapp-cli version
```

### Read and Search

```bash
whatsapp-cli messages list --limit 50
whatsapp-cli messages list --chat <jid> --limit 50 --page 0
whatsapp-cli messages search --query "meeting" --limit 100
whatsapp-cli contacts search --query "Alice"
whatsapp-cli chats list --query "Team" --limit 20
whatsapp-cli groups list --query "Project"
```

Use the exact JID returned by lookup commands when possible. Direct chats
usually end in `@s.whatsapp.net`; groups end in `@g.us`.

### Send

```bash
whatsapp-cli send --to <phone-or-jid> --message "Hello"
whatsapp-cli send --to <phone-or-jid> --image ./photo.jpg --caption "Photo"
```

`--message` and `--image` are mutually exclusive. Use a group JID returned by
`groups list` rather than constructing one manually.

### Download Media

```bash
whatsapp-cli media download --message-id <id>
whatsapp-cli media download --message-id <id> --chat <jid> --output ./downloads/
```

The message must already be present in the local archive. Run or resume
`whatsapp-cli sync` when the archive does not contain the requested message.
