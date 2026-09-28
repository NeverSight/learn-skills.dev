---
name: conversation-history-brief
description: Pull full conversation history for a CRM contact — fetch associated threads across all inboxes, retrieve message content, and assemble structured data for account briefs showing channel types, thread statuses, last activity, and key message excerpts.
triggers:
  - "conversation history"
  - "conversations for contact"
  - "account brief conversations"
  - "contact chat history"
  - "threads for contact"
  - "messages for contact"
  - "what did we discuss"
  - "recent conversations"
  - "inbox history"
  - "conversation brief"
---

Requires the `conversations` command group from hub-cli PR #251. `hubspot conversations --help` is authoritative. Also read `communication-history/SKILL.md` for CRM activity history (calls, emails, notes) — this skill covers the Conversations inbox surface only.

## How threads associate to contacts

`conversations threads list` accepts `--associated-contact-id`. You must also supply `--inbox-id` — there is no portal-wide contact thread lookup without knowing the inbox. To cover all inboxes, enumerate them first (step 1), then query per inbox.

## Paging: never collect a full result set with `--format jsonl`

Every conversations `list` command defaults to `--limit 100` and returns a cursor for the next page. **`--format jsonl` prints only the data rows — the cursor is surfaced only by `--format json`, at `.meta.next`.** Piping `--format jsonl` into a file therefore silently truncates at the first 100 rows, and raising `--limit` is not a fix because the endpoint caps the page size.

Use this helper for anything that must see every row:

```bash
# conv_page <output-file> <conversations list args...>
# Pages a conversations list endpoint to exhaustion, writing one JSON object
# per line to <output-file>.
conv_page() {
  out=$1; shift
  after=""
  : > "$out"
  while :; do
    if [ -n "$after" ]; then
      page=$(hubspot "$@" --format json --after "$after") || return 1
    else
      page=$(hubspot "$@" --format json) || return 1
    fi
    printf '%s' "$page" | jq -c '.data[]' >> "$out"
    after=$(printf '%s' "$page" | jq -r '.meta.next // empty')
    [ -n "$after" ] || break
  done
}
```

A bare `--format jsonl` is still fine for eyeballing the first page interactively.

## 1. Enumerate inboxes

```bash
conv_page /tmp/inboxes.jsonl conversations inboxes list
# {"id":"123","name":"Support Inbox","createdAt":"...","updatedAt":"..."}
# {"id":"124","name":"Sales Chat","createdAt":"...","updatedAt":"..."}
```

## 2. Find all threads for a contact

Loop over inbox IDs and collect threads associated with the contact:

```bash
CONTACT_ID=73235
: > /tmp/contact_threads.jsonl   # truncate output file

while IFS= read -r inbox; do
  inbox_id=$(echo "$inbox" | jq -r '.id')
  conv_page /tmp/inbox_threads.jsonl conversations threads list \
    --inbox-id "$inbox_id" \
    --associated-contact-id "$CONTACT_ID"
  cat /tmp/inbox_threads.jsonl >> /tmp/contact_threads.jsonl
done < /tmp/inboxes.jsonl

echo "Total threads found: $(wc -l < /tmp/contact_threads.jsonl)"
```

Thread output shape:
```json
{"id":"111","status":"OPEN","createdAt":"2026-07-28T10:02:00Z","latestMessageTimestamp":"2026-07-30T14:22:00Z","assignedTo":"A-78901","inboxId":"123","originalChannelId":"1000","originalChannelAccountId":"148662","associatedContactId":"73235","spam":false,"archived":false}
```

Two fields that are easy to assume and are **not** on a thread:

- **No `channelType`.** A thread names its originating channel by id only, in `originalChannelId`. Resolve it to a human-readable type by joining against `conversations channels list`, which returns `{"id":"1000","name":"Support Email","type":"EMAIL","inboxId":"123"}` (step 3 below).
- **No guaranteed `subject`.** `status` (`OPEN`/`CLOSED`), timestamps, `assignedTo` and the channel ids are the dependable fields. Always read a subject through a `// "(no subject)"` fallback.

## 3. Resolve channel ids to channel types

```bash
: > /tmp/channels.jsonl
while IFS= read -r inbox; do
  inbox_id=$(echo "$inbox" | jq -r '.id')
  conv_page /tmp/inbox_channels.jsonl conversations channels list --inbox-id "$inbox_id"
  cat /tmp/inbox_channels.jsonl >> /tmp/channels.jsonl
done < /tmp/inboxes.jsonl

# {"1000":"EMAIL","1001":"LIVE_CHAT"}
jq -s 'map({key: (.id|tostring), value: .type}) | from_entries' \
  /tmp/channels.jsonl > /tmp/channel_types.json
```

Helper used by the steps below to label a thread:

```bash
CHANNEL_TYPES=$(cat /tmp/channel_types.json)
```

## 4. Fetch messages for each thread

`messages list` pages like every other list endpoint, so page it rather than taking the first 100:

```bash
: > /tmp/all_messages.jsonl

while IFS= read -r thread; do
  tid=$(echo "$thread" | jq -r '.id')
  conv_page /tmp/thread_messages.jsonl conversations messages list --thread-id "$tid"
  jq -c --argjson thread "$thread" --argjson types "$CHANNEL_TYPES" \
    '. + {
       _threadId: $thread.id,
       _subject: ($thread.subject // "(no subject)"),
       _channelType: ($types[($thread.originalChannelId | tostring)] // "UNKNOWN")
     }' /tmp/thread_messages.jsonl \
  >> /tmp/all_messages.jsonl
done < /tmp/contact_threads.jsonl
```

Message output shape:
```json
{"id":"222","type":"MESSAGE","text":"Hello, I have a billing question.","sender":{"actorId":"A-456","name":"Jane Doe"},"createdAt":"2026-07-30T14:20:00Z"}
```

To get a single message in full detail:

```bash
hubspot conversations messages get --thread-id 111 --message-id 222 --format jsonl
```

## 5. Compact timeline for an account brief

Produce a human-readable thread summary ordered by most recent activity. Note the `-s`: the file is JSONL, so without slurping, `sort_by` is handed one object at a time and jq exits 5 with `Cannot index string with string` instead of printing a timeline.

```bash
echo "=== Conversation History for Contact $CONTACT_ID ==="
jq -sr --argjson types "$CHANNEL_TYPES" \
  'sort_by(.latestMessageTimestamp) | reverse[] |
   "\(.latestMessageTimestamp[0:10])  \($types[(.originalChannelId | tostring)] // "?")  [\(.status)]  \(.subject // "(no subject)")"' \
  /tmp/contact_threads.jsonl
```

Key message excerpts (first message per thread):

```bash
echo ""
echo "=== First message per thread ==="
while IFS= read -r thread; do
  tid=$(echo "$thread" | jq -r '.id')
  subject=$(echo "$thread" | jq -r '.subject // "(no subject)"')
  first_msg=$(hubspot conversations messages list --thread-id "$tid" --limit 1 --format jsonl \
    | jq -r '.text // .richText // "(no text)" | .[0:200]')
  echo "[$tid] $subject: $first_msg"
done < /tmp/contact_threads.jsonl
```

## 6. Structured account brief section

Emit a JSON block suitable for embedding in a larger account brief:

```bash
jq -n \
  --argjson threads "$(jq -s '.' /tmp/contact_threads.jsonl)" \
  --argjson types "$CHANNEL_TYPES" \
  --arg contact_id "$CONTACT_ID" \
  '{
    conversations: {
      contact_id: $contact_id,
      total_threads: ($threads | length),
      open_threads: ($threads | map(select(.status=="OPEN")) | length),
      channels: ($threads | map($types[(.originalChannelId | tostring)] // "UNKNOWN") | unique),
      latest_activity: ($threads | sort_by(.latestMessageTimestamp) | last | .latestMessageTimestamp),
      threads: ($threads | map({
        id: .id,
        subject: (.subject // "(no subject)"),
        status: .status,
        channel: ($types[(.originalChannelId | tostring)] // "UNKNOWN"),
        last_activity: .latestMessageTimestamp,
        assigned_to: (.assignedTo // null)
      }))
    }
  }'
```

## Combining with CRM activity history

For a full pre-call brief, combine this skill with `communication-history/SKILL.md`:

```bash
CONTACT_ID=73235

echo "=== CRM Activity (calls, emails, notes) ==="
hubspot activities list --contact $CONTACT_ID --limit 10 \
| jq -r '"\(.timestamp[0:10])  \(.type)  \(.title)"'

echo ""
echo "=== Conversations Inbox Threads ==="
# ... run the thread loop from step 2 above ...
```


## Known constraints

- `threads list` requires `--inbox-id` — must loop over all inboxes to get a full picture.
- No server-side filter on date range — filter with `jq` client-side using `latestMessageTimestamp`.
- Every `list` command pages at 100 rows and only `--format json` exposes the cursor (`.meta.next`). Use `conv_page` for anything that must be complete; a bare `--format jsonl` redirect silently truncates.
- Threads carry no `channelType` — join `originalChannelId` against `conversations channels list` to get a type. A thread can also switch channels mid-conversation, so `originalChannelId` describes where the thread *started*, not every channel it used.
- `subject` is not a guaranteed field on a thread; always use a `// "(no subject)"` fallback.
- `text` vs `richText`: some message types carry formatted content in `richText` rather than `text`. Check both fields when extracting excerpts.
