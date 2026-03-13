---
name: convos-agent
description: |
  This skill should be used when an AI agent needs to join, create, or participate in Convos encrypted messaging conversations.
  Covers the full lifecycle: installing the CLI, joining or creating conversations, running in agent mode with real-time streaming, sending messages/replies/reactions/attachments, reading history, managing profiles, and group administration.
  Includes behavioral principles for being a genuinely great group member, the ndjson agent serve protocol, a bridge script template, and a CLI command reference.
  Use when: user says "join this Convos conversation", "create a Convos group", "send a message on Convos", "set up agent mode", "join via invite link", or any task involving the convos CLI or XMTP messaging.
  Works with any agent that can run shell commands.
---

# Convos Agent Skill

Convos is an encrypted messaging platform built on XMTP. Every conversation creates a unique identity — no cross-conversation linkability. Messages are end-to-end encrypted. Groups support invites, profiles, reactions, attachments, and self-destruction.

Agents participate using the `convos` CLI.

## How to Be a Great Group Agent

Your job is to help groups do things. Your value comes from connecting what others have said — the pattern across conversations, the contradiction nobody caught, the thing someone mentioned once that just became relevant. You're not running the group. You're serving it. Tell people they can train you just by talking to you — the best version of you for this group is one no other group would recognize.

The detailed behavioral rules are delivered to the chatting agent via the bridge script's system message (see the `SYSTEM_MSG` in the bridge below).

## What to Do

If you haven't already been supplied an invite URL, slug, or conversation ID, ask the user for a conversation invite link from the Convos app. Invite links start with `https://popup.convos.org`. Then proceed with setup, joining, and running the bridge script as described below.

## Getting Started

```bash
# Install the CLI
npm install -g @xmtp/convos-cli

# Initialize configuration
convos init --env production
```

This creates `~/.convos/.env`. Each conversation created or joined gets its own isolated identity in `~/.convos/identities/`.

The channel is Convos — everything is already connected. Never ask users which platform they're on, what service they use, or for any API credentials.

## Joining a Conversation

When given an invite URL or slug:

```bash
# Join with a display name
convos conversations join "<invite-url-or-slug>" \
  --profile-name "Your Name" \
  --env production

# Join and capture the conversation ID
CONV_ID=$(convos conversations join "<slug>" \
  --profile-name "Your Name" \
  --json \
  --env production | jq -r '.conversationId')
```

The join command sends a request to the conversation creator and waits up to 120 seconds for acceptance. Use `--timeout` to change the wait duration.

## Creating a Conversation

```bash
# Create a conversation
convos conversations create \
  --name "Group Name" \
  --profile-name "Your Name" \
  --env production

# Create with admin-only permissions
convos conversations create \
  --name "Group Name" \
  --permissions admin-only \
  --profile-name "Your Name" \
  --env production

# Capture the conversation ID
CONV_ID=$(convos conversations create \
  --name "Group Name" \
  --profile-name "Your Name" \
  --json \
  --env production | jq -r '.conversationId')
```

### Generating Invites

```bash
# Generate invite (shows QR code in terminal)
convos conversation invite "$CONV_ID"

# Get invite URL for scripting
INVITE_URL=$(convos conversation invite "$CONV_ID" --json | jq -r '.url')
```

Always display the full unmodified output when generating invites so the QR code renders correctly.

### Processing Join Requests

After someone opens your invite, you must process their join request:

```bash
# Process all pending requests
convos conversations process-join-requests --conversation "$CONV_ID"

# Watch for requests in real-time (if you don't know when they'll open the invite)
convos conversations process-join-requests --watch --conversation "$CONV_ID"
```

Important: the person must open/scan the invite *before* you process. Use `--watch` when you don't know the timing.

## Agent Mode

`convos agent serve` is the core of real-time agent participation. It's a long-lived process that streams messages, processes joins, and accepts commands via ndjson on stdin/stdout.

### Starting

> **You MUST provide either a conversation ID or `--name` to create a new one.**
> Running `convos agent serve` with neither will fail. If joining an existing
> conversation, get the conversation ID from `convos conversations join` first.

```bash
# Attach to an existing conversation (REQUIRES conversation ID)
convos agent serve "$CONV_ID" \
  --profile-name "Your Name" \
  --env production

# Create a new conversation and start serving (use --name instead of conv ID)
convos agent serve \
  --name "Group Name" \
  --profile-name "Your Name" \
  --env production

# With periodic health checks
convos agent serve "$CONV_ID" \
  --profile-name "Your Name" \
  --heartbeat 30 \
  --env production
```

When started, agent serve:
1. Creates or attaches to the conversation
2. Prints a QR code invite to stderr
3. Emits a `ready` event with the conversation ID and invite URL
4. Processes any pending join requests
5. Streams messages in real-time
6. Accepts commands on stdin
7. Automatically adds new members who join via invite

### Events (stdout)

One JSON object per line. Each has an `event` field.

| Event | Meaning | Key fields |
|-------|---------|------------|
| `ready` | Session started | `conversationId`, `inviteUrl`, `inboxId` |
| `message` | Someone sent a message | `id`, `senderInboxId`, `content`, `contentType`, `sentAt`, `senderProfile` |
| `member_joined` | New member added | `inboxId`, `conversationId` |
| `sent` | Your message was delivered | `id`, `text`, `replyTo` |
| `heartbeat` | Health check | `conversationId`, `activeStreams` |
| `error` | Something went wrong | `message` |

Messages with `catchup: true` were fetched during a stream reconnection — they're messages you missed while disconnected. Consider whether you should respond to old catchup messages or ignore them.

### Message Content Types

The `content` field is always a string. The format depends on `contentType.typeId`:

| typeId | Example |
|--------|---------|
| `text` | `Hello everyone` |
| `reply` | `reply to "Hello everyone" (<msg-id>): Thanks!` |
| `reaction` | `reacted 👍 to <msg-id>` |
| `attachment` | `[attachment: photo.jpg (image/jpeg)]` |
| `remoteStaticAttachment` | `[remote attachment: video.mp4 (4521 bytes) https://...]` |
| `group_updated` | `Alice changed group name to "New Name"` |

Replies and reactions reference another message by ID. If you need context about a referenced message, look it up in messages you've already seen or fetch history.

`group_updated` examples:
- `Alice changed group name to "New Name"`
- `Bob joined by invite`
- `Alice added Bob` / `Alice removed Bob`
- `Alice made Bob an admin`
- `Bob changed their name to Robert`
- `Alice updated their profile photo`

### Commands (stdin)

One JSON object per line. Must be compact (no pretty-printing).

```jsonl
{"type":"send","text":"Hello!"}
{"type":"send","text":"Replying","replyTo":"<message-id>"}
{"type":"react","messageId":"<message-id>","emoji":"👍"}
{"type":"react","messageId":"<message-id>","emoji":"👍","action":"remove"}
{"type":"attach","file":"./photo.jpg"}
{"type":"attach","file":"./photo.jpg","replyTo":"<message-id>"}
{"type":"rename","name":"New Group Name"}
{"type":"lock"}
{"type":"unlock"}
{"type":"explode"}
{"type":"explode","scheduled":"2025-03-01T00:00:00Z"}
{"type":"stop"}
```

## Bridge Scripts

> **AI AGENTS: YOU MUST USE A BRIDGE SCRIPT.**
>
> Do not try to manually run `agent serve` and send messages separately — that
> creates race conditions and you will miss messages. You cannot natively pipe
> stdin/stdout to a long-running process. Write the bridge script below, run it,
> and let it handle the event loop.
>
> The bridge is not optional. It is the correct way to participate in a conversation.

### How It Works

1. Write the bridge script to a file (use the template below)
2. Make it executable (`chmod +x bridge.sh`)
3. Run it as a **separate background process** (`./bridge.sh "$CONV_ID" &`)

**The bridge MUST run as its own process.** Do not source it, run it inline, or
execute it in the same shell as other commands. If other processes share the
bridge's file descriptors, their output can leak into agent serve's stdin and
get sent as chat messages (e.g., npm install output appearing in the conversation).

### Bridge Script

This bridge uses `openclaw agent` for reply generation. The OpenClaw runtime
gives the sub-session full tool access (read, exec, edit, write) and retains
conversation history via `--session-id`.

**OpenClaw:** The agent also has context from its workspace bootstrap files
(AGENTS.md, SOUL.md). No extra priming needed.

**Other backends:** Replace the two `openclaw agent` calls in the `ready` and
`message` handlers with your AI backend. If session-based, deliver the
`SYSTEM_MSG` on the first call only. If stateless, prepend it to every call.

The bridge processes sub-session output line by line: lines starting with `{`
are passed directly to agent serve as stdin commands, other lines are sent as
text messages:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Close inherited stdin so nothing leaks into agent serve
exec 0</dev/null

CONV_ID="${1:?Usage: $0 <conversation-id>}"
SESSION_ID="convos-${CONV_ID}"
MY_INBOX=""

# Prevent duplicate bridges for the same conversation
LOCK_FILE="/tmp/convos-bridge-${CONV_ID}.lock"
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "Bridge already running for $CONV_ID (lock: $LOCK_FILE)" >&2
  exit 1
fi

# Named pipes — more stable than coprocess FDs
FIFO_DIR=$(mktemp -d)
FIFO_IN="$FIFO_DIR/in"
FIFO_OUT="$FIFO_DIR/out"
mkfifo "$FIFO_IN" "$FIFO_OUT"
trap 'rm -rf "$FIFO_DIR" "$LOCK_FILE"' EXIT

# Start agent serve with named pipes
convos agent serve "$CONV_ID" --profile-name "OpenClaw Agent" \
  < "$FIFO_IN" > "$FIFO_OUT" 2>/dev/null &
AGENT_PID=$!

# Persistent write FD — stays open for the lifetime of the script
exec 3>"$FIFO_IN"

# Message queue — sends one at a time, waits for "sent" confirmation
QUEUE_FILE="$FIFO_DIR/queue"
: > "$QUEUE_FILE"

# Queue a reply: JSON commands pass through, text gets wrapped
queue_reply() {
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    if [[ "$line" == "{"* ]]; then
      echo "$line" | jq -c . >> "$QUEUE_FILE"
    else
      jq -nc --arg text "$line" '{"type":"send","text":$text}' >> "$QUEUE_FILE"
    fi
  done <<< "$1"
  send_next
}

# Send the next queued command to agent serve
send_next() {
  [[ ! -s "$QUEUE_FILE" ]] && return
  head -1 "$QUEUE_FILE" >&3
  tail -n +2 "$QUEUE_FILE" > "$QUEUE_FILE.tmp"
  mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"
}

while IFS= read -r event; do
  evt=$(echo "$event" | jq -r '.event // empty')

  case "$evt" in
    ready)
      MY_INBOX=$(echo "$event" | jq -r '.inboxId')
      echo "Ready: $CONV_ID" >&2
      # Fetch profiles NOW so the sub-session already has member data
      # and doesn't need to run commands before its first message
      PROFILES=$(convos conversation profiles "$CONV_ID" --json 2>/dev/null || echo "[]")
      # Build system message with full context — the sub-session may not
      # have the convos-agent skill installed, so include everything here
      SYSTEM_MSG=$(cat <<SYSMSG
[system] You are an AI group agent in Convos conversation $CONV_ID.
Your job is to help this group do things.

YOUR OUTPUT GOES DIRECTLY TO CHAT. Every non-empty line you produce is sent
as a message or command. Follow these rules from your very first output:

Rules:
1. Listen first. Learn who these people are before you contribute.
2. Earn your seat. Only speak when it adds something no one else could.
3. Plain text only. No markdown (no **bold**, \`code\`, [links](url), or lists).
4. Be concise. Protect people's attention. React instead of typing when possible.
5. Reply, don't broadcast. Messages include a msg-id — use it with replyTo.
   Only reply to actual messages — never to system events like group updates.
6. Be the memory. Connect dots across time. Surface things that just became
   relevant. But never weaponize memory.
7. Use names, not inbox IDs. Refresh with: convos conversation profiles "$CONV_ID" --json
8. Never narrate what you are doing. Your stdout IS the chat — every line
   you output is sent as a message to real people. Never say "let me check",
   "reading now", or describe what you're about to do. Do all reasoning and
   tool use silently. Only output words you want humans to read.
9. Honor renames immediately. Run: convos conversation update-profile "$CONV_ID" --name "New Name"
10. Read the room. If people are having fun, be fun. If quiet, respect the quiet.
11. Respect privacy. What's said in the group stays in the group.
12. Tell people they can train you by talking to you.

Output format — each line is processed separately:
- Lines starting with { = JSON commands sent to agent serve
- Other non-empty lines = sent as text messages

JSON commands (compact single-line ndjson):
{"type":"send","text":"Hello!"}
{"type":"send","text":"Replying","replyTo":"<message-id>"}
{"type":"react","messageId":"<message-id>","emoji":"👍"}
{"type":"attach","file":"./photo.jpg"}
{"type":"rename","name":"New Group Name"}

CLI commands (safe to run alongside agent serve):
convos conversation profiles "$CONV_ID" --json
convos conversation messages "$CONV_ID" --json --sync --limit 20
convos conversation update-profile "$CONV_ID" --name "Name"
convos conversation info "$CONV_ID" --json

REMEMBER: every line you output is sent to the chat. Do not output reasoning,
status updates, or narration. Only output messages you intend humans to read.

Current group members:
$PROFILES

Introduce yourself based on your IDENTITY.md. If any members match
someone from your USER.md, acknowledge that you know them.
SYSMSG
)
      reply=$(openclaw agent \
        --session-id "$SESSION_ID" \
        --message "$SYSTEM_MSG" \
        2>/dev/null)
      queue_reply "$reply"
      ;;

    sent)
      # Previous message confirmed — send the next queued one
      send_next
      ;;

    message)
      type_id=$(echo "$event" | jq -r '.contentType.typeId // empty')
      [[ "$type_id" != "text" && "$type_id" != "reply" ]] && continue

      catchup=$(echo "$event" | jq -r '.catchup // false')
      [[ "$catchup" == "true" ]] && continue

      sender=$(echo "$event" | jq -r '.senderInboxId // empty')
      [[ "$sender" == "$MY_INBOX" ]] && continue

      sender_name=$(echo "$event" | jq -r '.senderProfile.name // "Someone"')
      msg_id=$(echo "$event" | jq -r '.id // empty')
      content=$(echo "$event" | jq -r '.content')

      reply=$(openclaw agent \
        --session-id "$SESSION_ID" \
        --message "$sender_name (msg-id: $msg_id): $content" \
        2>/dev/null)

      queue_reply "$reply"
      ;;

    member_joined)
      jq -nc '{"type":"send","text":"Welcome!"}' >&3
      ;;
  esac
done < "$FIFO_OUT"

wait "$AGENT_PID"
```

## In-Conversation CLI Reference

Commands for reading and querying while participating. Always pass `--json` when parsing output programmatically.

### Members and Profiles

```bash
# Members (inbox IDs + permission levels)
convos conversation members "$CONV_ID" --json

# Profiles (display names + avatars)
convos conversation profiles "$CONV_ID" --json
```

Refresh profiles on `member_joined` events or `group_updated` messages about profile changes.

### Message History

```bash
# Recent messages (sync from network first)
convos conversation messages "$CONV_ID" --json --sync --limit 20

# Oldest first
convos conversation messages "$CONV_ID" --json --limit 50 --direction ascending

# Filter by type
convos conversation messages "$CONV_ID" --json --content-type text
convos conversation messages "$CONV_ID" --json --exclude-content-type reaction

# Time range (nanosecond timestamps)
convos conversation messages "$CONV_ID" --json --sent-after <ns> --sent-before <ns>
```

### Attachments

```bash
# Download an attachment
convos conversation download-attachment "$CONV_ID" <message-id>
convos conversation download-attachment "$CONV_ID" <message-id> --output ./photo.jpg

# Send an attachment (small files inline, large files auto-uploaded)
convos conversation send-attachment "$CONV_ID" ./photo.jpg
```

### Profile Management

Profiles are per-conversation — different name and avatar in each group.

```bash
# Set display name
convos conversation update-profile "$CONV_ID" --name "New Name"

# Set name and avatar
convos conversation update-profile "$CONV_ID" --name "New Name" --image "https://example.com/avatar.jpg"

# Go anonymous
convos conversation update-profile "$CONV_ID" --name "" --image ""
```

### Group Management

```bash
# View group info
convos conversation info "$CONV_ID" --json

# View permissions
convos conversation permissions "$CONV_ID" --json

# Update group name
convos conversation update-name "$CONV_ID" "New Name"

# Update description
convos conversation update-description "$CONV_ID" "New description"

# Add/remove members (requires super admin)
convos conversation add-members "$CONV_ID" <inbox-id>
convos conversation remove-members "$CONV_ID" <inbox-id>

# Lock (prevent new joins, invalidate existing invites)
convos conversation lock "$CONV_ID"

# Unlock
convos conversation lock "$CONV_ID" --unlock

# Permanently destroy conversation (irreversible)
convos conversation explode "$CONV_ID" --force
```

### Send Messages (CLI)

For scripting or one-off sends outside of agent mode:

```bash
# Send text
convos conversation send-text "$CONV_ID" "Hello!"

# Reply to a message
convos conversation send-reply "$CONV_ID" <message-id> "Replying to you"

# React
convos conversation send-reaction "$CONV_ID" <message-id> add "👍"

# Remove reaction
convos conversation send-reaction "$CONV_ID" <message-id> remove "👍"
```

## Common Mistakes

| Mistake | Why it's wrong | Correct approach |
|---------|---------------|-----------------|
| Running `agent serve` without a conversation ID or `--name` | The command requires one or the other. It will fail with neither | Pass a conversation ID to join existing, or `--name` to create new |
| Manually polling `agent serve` and sending messages separately | Creates race conditions, you'll miss messages between polls | Write and run a bridge script that uses coprocess stdin/stdout |
| Calling AI sub-session without context | Sub-session needs identity and behavioral rules to participate well | Deliver the `SYSTEM_MSG` from the bridge script on the first call (OpenClaw loads workspace context automatically) |
| Running bridge inline or in shared shell | Output from other commands (npm install, etc.) leaks into coprocess FDs and gets sent as chat messages | Write bridge to a file, run as separate background process |
| Using markdown in messages | Convos does not render markdown. Users see raw `**asterisks**` and `[brackets](url)` | Write plain text naturally |
| Sending via CLI while in agent mode | Agent serve owns the conversation stream. CLI sends create race conditions | Use stdin commands (`{"type":"send",...}`) in agent mode |
| Forgetting `--env production` | Default is `dev` (test network). Real users are on production | Always pass `--env production` for real conversations |
| Replying to system events | `group_updated`, `reaction`, and `member_joined` are not messages | Only `replyTo` messages with `contentType.typeId` of `text`, `reply`, or `attachment` |
| Generating invite but not processing joins | The invite system is two-step: generate, then process | Run `process-join-requests` after the invitee opens the link |
| Referencing inbox IDs in chat | People don't know or care about `0x...` hex strings | Fetch profiles and use display names |
| Announcing tool usage | "Let me check the message history..." breaks immersion | Just do it silently and respond naturally |
| Responding to every message | Agents that talk too much get muted | Only speak when it adds something. React instead of replying when possible |
| Launching the bridge twice for the same conversation | Two bridges split the event stream randomly — messages get swallowed | The bridge template uses `flock` to prevent this. Always check for an existing process before launching |

## Troubleshooting

**`convos: command not found`**
Not installed. Run `npm install -g @xmtp/convos-cli`.

**`Error: Not initialized`**
Run `convos init --env production` to create the configuration directory.

**Join request times out**
The invitee must open/scan the invite URL *before* the creator processes requests.

**Messages not appearing**
Sync from the network first: `convos conversation messages <id> --json --sync --limit 20`.

**Permission denied on group operations**
Check permissions with `convos conversation permissions <id> --json`. Only super admins can add/remove members, lock, or explode.

**Invite expired or invalid**
Generate a new invite with `convos conversation invite <id>`. Locking a conversation invalidates all existing invites.

**Agent serve exits unexpectedly**
Check stderr for error output. Common causes: invalid conversation ID, identity not found (run `convos identity list`), or network issues. Use `--heartbeat 30` to monitor connection health.

## Tips

- **Use `--env production` for real conversations.** The default is `dev`, which uses the test network.
- **Use `--json` when parsing output.** Human-readable output can change between versions.
- **Use `--sync` before reading messages.** Ensures fresh data from the network.
- **Identities are automatic.** Creating or joining a conversation creates one for you. Rarely need to manage them directly.
- **Show full QR code output.** When generating invites, display the complete unmodified output so QR codes render correctly in the terminal. In agent mode, the QR code is saved as a PNG (path in the `ready` event's `qrCodePath` field).
- **Process join requests after the invite is opened.** Use `--watch` if you don't know when someone will open the invite.
- **Lock before exploding.** Lock a conversation first to prevent new joins, then explode when ready.
