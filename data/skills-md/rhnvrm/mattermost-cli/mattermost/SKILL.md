---
name: mattermost
description: Read and search Mattermost chat using the `mm` CLI. Use this skill whenever the user mentions Mattermost, chat messages, team chat, unread messages, DMs, channel history, mentions, or wants to catch up on what happened in chat. Also triggers when the user asks about specific people's messages, channel activity, searching for something someone said, or checking notifications. The CLI outputs agent-friendly JSON by default with thread IDs, bot detection, and channel refs - no parsing needed.
---

# Mattermost CLI (`mm`)

Read and search Mattermost from the command line. JSON output by default, `--human` for markdown.

## Setup

Check if `mm` is already available:

```bash
mm whoami
```

If that works, skip to "Start here" below.

If `mm` is not found, install it. Pick whichever works in your environment:

```bash
pip install mattermost-cli    # adds `mm` to PATH
# or
pipx install mattermost-cli   # isolated global install
# or
uvx --from mattermost-cli mm  # run without installing (needs uvx)
```

Then authenticate (one-time):

```bash
mm login --url https://your.mattermost.server
mm whoami   # verify
```

The login command will prompt for credentials interactively. If your server supports Personal Access Tokens (Profile > Security > Personal Access Tokens in the Mattermost UI), you can skip the prompt:

```bash
mm login --url https://your.mattermost.server --token YOUR_TOKEN
```

For environment variables, multiple servers, and troubleshooting, see [references/setup.md](references/setup.md).

## Start here: `mm overview`

Always run this first. It returns mentions, unread channels, and active channels in a single call.

```bash
mm overview              # last 6 hours (default)
mm overview --since 1d   # last 24 hours
```

The response has three sections:
- **mentions** - posts that @-mention you, with root message context when it's a reply
- **unread** - channels with unread messages, sorted by count
- **active_channels** - channels with recent posts, sorted by recency

Each entry includes a `ref` field you can pass directly to other commands.

## Reading messages

```bash
mm messages <channel>                   # last 30 messages, chronological
mm messages <channel> --since 2h        # messages from last 2 hours
mm messages <channel> --threads         # thread index: root + reply count + last reply
mm messages @username                   # DMs with someone
```

`<channel>` accepts a name (`off-topic`), `@username` for DMs, or a channel ID (for group DMs from overview output).

### Threads

Every post includes a `thread_id`. Use it to read the full conversation:

```bash
mm thread <thread_id>                   # root + last 9 replies
mm thread <thread_id> --limit 0         # entire thread
mm thread <thread_id> --since 1h        # just recent replies (root always included)
```

## Searching and mentions

```bash
mm search "deployment issue"
mm search "from:alice in:devops after:2025-01-01"
mm mentions                             # @-mentions in last 24h
mm mentions --since 3d
```

Mentions for replies include a `root` field with the original message, so you know what "this" or "it" refers to without a follow-up call.

## Channel context

```bash
mm channel <name>                       # purpose, header, member/pinned count
mm pinned <channel>                     # important/pinned posts
mm members <channel>                    # who's here + online status
mm channels --since 6h                  # all channels with recent activity
mm channels --type dm                   # just DMs
```

## People

```bash
mm user @someone                        # profile, role, status, timezone
```

## Key JSON fields

Every post includes these fields so you can navigate without guesswork:

| Field | What it's for |
|-------|---------------|
| `thread_id` | Pass to `mm thread` to read full conversation |
| `ref` | On channel entries; pass to `mm messages` |
| `is_bot` / `bot_name` | Webhook and bot posts are flagged automatically |
| `root` | On reply-mentions; the original message being replied to |
| `is_reply` / `reply_count` | Thread structure |
| `reactions` | Emoji counts like `{"+1": 3, "white_check_mark": 1}` |

Bot posts from webhooks automatically extract alert content from Slack-format attachments, so you see the actual alert text instead of empty messages.

## Further reading

- [references/scenarios.md](references/scenarios.md) - real use cases: "what did I miss?", "summarize this channel", "is this resolved?", "find that thing someone said"
- [references/workflows.md](references/workflows.md) - command sequences: morning triage, incident investigation, channel discovery
- [references/commands.md](references/commands.md) - full command reference with all options and flags
