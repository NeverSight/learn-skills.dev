---
name: zulip-cli
description: Use when the user wants to read, search, send, or inspect Zulip messages, channels, topics, users, or files through the non-interactive zulip CLI. This is for Zulip user and bot accounts, not server deployment or administration.
---

# zulip-cli

Use `zulip` for non-interactive, JSON-first Zulip workflows.

## Install

Install both the CLI and this skill:

```sh
curl -fsSL https://raw.githubusercontent.com/dapi/zulip-cli/v0.2.1/install.sh | sh
```

Manual installation:

```sh
npm install -g github:dapi/zulip-cli#v0.2.1
npx skills add https://github.com/dapi/zulip-cli/tree/v0.2.1 \
  --skill zulip-cli --agent '*' -g -y
```

## Authentication

Set credentials through the environment:

```sh
export ZULIP_SITE=https://zulip.example.com
export ZULIP_EMAIL=agent@example.com
export ZULIP_API_KEY=<api-key>
```

Prefer environment variables loaded from the user's secret manager. Do not put
the API key in a repository, `.env` file, command line, transcript, or response.
Although `--api-key` exists for interoperability, avoid it because command-line
arguments can be exposed in process listings and shell history.

## Execution rules

- Run the needed command directly and inspect the `ok` field before using `data`.
- Use `zulip commands` to discover supported commands and options.
- Read or search before responding about existing conversations.
- Sending requires explicit authorization in the current user request. A request
  to draft, review, summarize, or find a message does not authorize sending it.
- Before sending, resolve the exact channel/topic or direct-message recipients.
  Never guess a similarly named destination.
- Do not send a test message to verify authentication. Use `zulip user-me`.
- Pass multiline or user-authored content via `--content @file` or stdin
  (`--content -`) so formatting and line breaks are preserved.
- `file-upload` creates a private upload. It becomes visible to others only after
  a message containing its returned URL is sent; sending that message still
  requires explicit authorization.
- Do not retry an uncertain send automatically. If a request times out after it
  may have reached Zulip, inspect recent messages before deciding whether to retry.

## Output and exit codes

Success:

```json
{"ok":true,"data":{"messages":[]}}
```

Failure is written to stderr:

```json
{"ok":false,"error":{"code":"AUTH_ERROR","message":"...","details":null}}
```

Exit codes: `0` success, `1` internal error, `2` configuration/authentication,
`3` not found, `4` validation, `5` network/timeout, `6` Zulip API error.

## Common workflows

Verify connectivity and authentication:

```sh
zulip server-info
zulip user-me
```

Discover channels, topics, and users:

```sh
zulip stream-list --subscribed
zulip topic-list --stream-id 42
zulip user-list
```

Read and search raw Markdown messages:

```sh
zulip message-list --limit 50 --raw
zulip message-list --stream general --topic deploy --limit 100 --raw
zulip message-search --query "release failed" --stream general --raw
zulip message-info --message-id 123 --raw
```

Send only when explicitly authorized:

```sh
zulip message-send --stream general --topic deploy --content @message.md
printf '%s\n' 'Hello' | zulip message-send --to user@example.com --content -
```

Delete a message only when explicitly authorized, by numeric ID:

```sh
zulip message-delete --message-id 123
```

Upload a file, then include the returned URL in an authorized message:

```sh
zulip file-upload --file ./report.pdf
```
