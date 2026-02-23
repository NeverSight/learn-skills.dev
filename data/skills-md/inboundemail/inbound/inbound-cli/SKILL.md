---
name: inbound-cli
description: Use the Inbound CLI to manage mailbox profiles, list and read emails, and keep an agent's default mailbox context between sessions.
---

# inbound-cli

Use this skill to operate email workflows through the `inbound` CLI with a persistent mailbox profile (`inbound.json`).

## Setup

- Install globally: `npm i -g inbound-cli`
- Use command name: `inbound`

## When to use

- User asks to check inbox mail, triage unread items, read email threads, or reply using Inbound CLI.
- User asks to set up or switch mailbox defaults for the agent.
- User asks to filter email activity by mailbox address/domain.
- User asks for command-line email operations instead of direct API calls.

Do not use this skill when the task is unrelated to Inbound email workflows.

## Instructions

1. Validate CLI availability.
   - Ensure global install exists: `npm i -g inbound-cli`.
   - Verify command works: `inbound help`.

2. Validate auth before mailbox work.
   - Check `INBOUND_API_KEY` exists.
   - If missing, ask the user for the API key or ask them to export it.

3. Ensure mailbox profile exists for the agent.
   - If no config exists, initialize: `inbound mailbox init`.
   - Add mailbox profile for the agent identity:
     - `inbound mailbox add <key> --name "<Agent Name>" --email <agent@email> [--domain <domain>]`
   - Set default mailbox:
     - `inbound mailbox use <key>`

4. Default mailbox-first inbox workflow.
   - List inbox (defaults to received type):
     - `inbound emails list --limit 25`
   - Read a specific email:
     - `inbound emails get <email_id>`
   - Mark handled email as read:
     - `inbound emails update <email_id> --is_read true`

5. Use filters intentionally.
   - Narrow by status/search/time:
     - `inbound emails list --status unread --search "invoice" --time-range 7d`
   - Override mailbox filters for one run:
     - `inbound emails list --address user@example.com`
     - `inbound emails list --domain example.com`
   - Include non-received types when needed:
     - `inbound emails list --type sent`
     - `inbound emails list --type scheduled`
     - `inbound emails list --type all`

6. Find mailbox profiles by identity.
   - `inbound mailbox find --address user@example.com`
   - `inbound mailbox find --domain example.com`

7. Use thread view for conversation context.
   - `inbound mail threads list --limit 20`
   - `inbound mail threads get <thread_id>`

8. Automation and parsing mode.
   - Use `--json` when the output needs machine parsing.
   - Use human mode by default for operator readability.

## Expected behavior

- Always start from the configured default mailbox unless explicit filter overrides are provided.
- Preserve mailbox context so future runs use the same identity.
- Keep user informed when filters broaden scope (for example `--type all`).

## Quick command cheatsheet

```bash
inbound mailbox list
inbound mailbox show
inbound emails list --status unread --limit 25
inbound emails get <email_id>
inbound emails update <email_id> --is_read true
inbound mail threads list --limit 20
inbound mail threads get <thread_id>
inbound emails list --json
```
