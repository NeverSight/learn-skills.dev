---
name: conversation-inbox-triage
description: Audit and triage conversation inboxes — list open and unassigned threads, find stale conversations, assign threads to team members, archive resolved threads in bulk, and produce a status summary by inbox and channel.
triggers:
  - "triage inbox"
  - "unassigned conversations"
  - "stale threads"
  - "assign conversation"
  - "archive conversation"
  - "conversation inbox"
  - "inbox triage"
  - "conversations triage"
  - "open threads"
  - "bulk archive conversations"
  - "conversation summary"
---

Requires the `conversations` command group from hub-cli PR #251. `hubspot conversations --help` is authoritative. Archive uses the dry-run/digest/confirm guard pattern — follow it exactly.

## Paging: never triage from a `--format jsonl` redirect

Every conversations `list` command defaults to `--limit 100` and returns a cursor for the next page. **`--format jsonl` prints only the data rows — the cursor is surfaced only by `--format json`, at `.meta.next`.** So `threads list --format jsonl > file` silently stops at 100 threads: on a busy inbox the operator sees a clean run while every thread past the first page is never assigned, never archived, and missing from the counts. Raising `--limit` does not fix it — the endpoint caps the page size.

Use this helper for every bulk or counting operation:

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

The bare `--format jsonl` calls in steps 2–4 are fine for eyeballing the first page interactively. Steps 6–8 mutate or count, so they page.

## 1. Discover inboxes

Inbox IDs are portal-specific. Always enumerate at the start of a session — never hardcode.

```bash
conv_page /tmp/inboxes.jsonl conversations inboxes list
# {"id":"123","name":"Support Inbox","createdAt":"...","updatedAt":"..."}
# {"id":"124","name":"Sales Chat","createdAt":"...","updatedAt":"..."}
```

To see channels inside an inbox (email, live chat, form, etc.):

```bash
conv_page /tmp/channels.jsonl conversations channels list --inbox-id 123
# {"id":"456","name":"Support Email","type":"EMAIL","inboxId":"123"}
```

## 2. List open threads

`threads list` requires `--inbox-id`. Filter client-side on `.status` for a focused view:

```bash
# all threads in an inbox
hubspot conversations threads list --inbox-id 123 --format jsonl

# only OPEN threads
hubspot conversations threads list --inbox-id 123 --format jsonl \
| jq -c 'select(.status == "OPEN")'
```

Output shape per row:
```json
{"id":"111","status":"OPEN","createdAt":"2026-07-28T10:02:00Z","latestMessageTimestamp":"2026-07-30T14:22:00Z","assignedTo":"A-78901","inboxId":"123","originalChannelId":"456","originalChannelAccountId":"148662","associatedContactId":"73235","spam":false,"archived":false}
```

A thread has **no `channelType`** — it names its originating channel by id, in `originalChannelId`, which you join against `channels list` (step 8). `subject` is also not guaranteed; read it through a `// "(no subject)"` fallback.

## 3. Find unassigned threads

`assignedTo` is null or absent for unassigned threads:

```bash
hubspot conversations threads list --inbox-id 123 --format jsonl \
| jq -c 'select(.status == "OPEN") | select(.assignedTo == null or .assignedTo == "")'
```

## 4. Find stale threads (no reply within N hours)

`latestMessageTimestamp` is ISO 8601 and compares lexicographically.

```bash
# macOS: threads with no activity in 24 hours
CUTOFF=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)
# Linux: CUTOFF=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)

hubspot conversations threads list --inbox-id 123 --format jsonl \
| jq -c --arg cutoff "$CUTOFF" \
    'select(.status == "OPEN") | select(.latestMessageTimestamp < $cutoff)'
```

For 48-hour and 72-hour variants change `-v-24H` to `-v-48H` / `-v-72H`.

## 5. Look up an actor ID

`assign` takes an actor ID. Get a team member's actor ID by their agent ID or email. HubSpot actor IDs use the `A-` prefix:

```bash
hubspot conversations actors get --id A-123456 --format jsonl
```

To map owner IDs to actor IDs, cross-reference `hubspot owners list --format jsonl` (returns `.email` and `.id`) and use the actor ID format `A-<ownerId>` as a starting point — verify with `actors get` that the ID resolves.

`owners list` needs a service key. Under an OAuth login it returns `403 This endpoint does not support user-level OAuth tokens`, so set `HUBSPOT_ACCESS_TOKEN` to a service key before the owner-to-actor lookup. The `conversations` commands themselves work under either auth mode.

## 6. Assign a thread

```bash
hubspot conversations threads assign --id 111 --actor-id A-123456
# {"id":"111","ok":true}
```

Bulk assign (all unassigned open threads to one actor). Two things matter here: read the id list from a **file**, not a pipe — a pipeline-fed `while` runs in a subshell, so counters and failure lists are discarded when it ends — and report a non-zero status at the end, so a partial run is never mistaken for a complete one.

```bash
ACTOR=A-123456
conv_page /tmp/threads.jsonl conversations threads list --inbox-id 123

jq -r 'select(.status == "OPEN")
       | select(.assignedTo == null or .assignedTo == "")
       | .id' /tmp/threads.jsonl > /tmp/assign_ids.txt

assign_threads() {
  actor=$1; ids=$2
  assigned=0
  : > /tmp/assign_failed.txt

  while read -r tid; do
    if out=$(hubspot conversations threads assign --id "$tid" --actor-id "$actor" 2>&1); then
      assigned=$((assigned + 1))
    else
      printf '%s\t%s\n' "$tid" "$out" >> /tmp/assign_failed.txt
    fi
  done < "$ids"

  failed=$(wc -l < /tmp/assign_failed.txt)
  echo "Assigned $assigned of $(wc -l < "$ids"); $failed failed"
  [ "$failed" -eq 0 ] || { echo "Failures:"; cat /tmp/assign_failed.txt; return 1; }
}

assign_threads "$ACTOR" /tmp/assign_ids.txt
```

## 7. Archive resolved threads

Archive is guarded: run `--dry-run` first to get a digest, then re-run with `--digest` and `--confirm` (value = thread ID).

```bash
# Single thread — two steps
hubspot conversations threads archive --id 111 --dry-run
# {"id":"111","digest":"blast-29cfdd48b583","ok":true,"executed":false,"dry_run":true}

hubspot conversations threads archive --id 111 --digest blast-29cfdd48b583 --confirm 111
# {"id":"111","ok":true}
```

### Bulk archive — preview, then execute

Bulk archive runs as two separate phases with a human decision between them. Do **not** collapse them into one loop that dry-runs and archives each thread in turn: that starts destroying threads before anyone has seen the full candidate set, and there is no point at which the operation can be declined as a whole.

**Phase 1 — preview. Read-only; nothing is mutated.**

```bash
INBOX=123
conv_page /tmp/threads.jsonl conversations threads list --inbox-id "$INBOX"

jq -c 'select(.status == "CLOSED")
       | {id, last_activity: .latestMessageTimestamp, assigned_to: .assignedTo}' \
  /tmp/threads.jsonl > /tmp/archive_candidates.jsonl

echo "Candidates for archive: $(wc -l < /tmp/archive_candidates.jsonl)"
jq -r '"\(.id)  \(.last_activity // "?")  \(.assigned_to // "unassigned")"' \
  /tmp/archive_candidates.jsonl
```

**Stop here and get the candidate list approved.** Re-run phase 1 as often as you like; it changes nothing.

> Persist candidate **ids**, not digests. A digest is only valid for 5 minutes (`DIGEST_TTL_SECONDS` in `src/hub/guard.rs`), so digests minted during preview would come back `digest_expired` after any realistic review pause. Phase 2 therefore mints each digest immediately before it uses it.

**Phase 2 — execute. Only after the list above is approved.**

```bash
jq -r '.id' /tmp/archive_candidates.jsonl > /tmp/archive_ids.txt

archive_threads() {
  ids=$1
  archived=0
  : > /tmp/archive_failed.txt

  while read -r tid; do
    preview=$(hubspot conversations threads archive --id "$tid" --dry-run 2>&1)
    digest=$(printf '%s' "$preview" | jq -r '.digest // empty' 2>/dev/null)
    if [ -z "$digest" ]; then
      printf '%s\tdry-run\t%s\n' "$tid" "$preview" >> /tmp/archive_failed.txt
      continue
    fi

    if out=$(hubspot conversations threads archive --id "$tid" --digest "$digest" --confirm "$tid" 2>&1); then
      archived=$((archived + 1))
    else
      printf '%s\tarchive\t%s\n' "$tid" "$out" >> /tmp/archive_failed.txt
    fi
  done < "$ids"

  failed=$(wc -l < /tmp/archive_failed.txt)
  echo "Archived $archived of $(wc -l < "$ids"); $failed failed"
  [ "$failed" -eq 0 ] || { echo "Failures (id / phase / error):"; cat /tmp/archive_failed.txt; return 1; }
}

archive_threads /tmp/archive_ids.txt
```

A failing thread is recorded and the run continues, but the function returns non-zero and prints every failure, so a partially drained inbox is never reported as a clean run. Re-running phase 2 on the same id file is safe — already-archived threads simply fail and are listed.

To undo, use `restore`:

```bash
hubspot conversations threads restore --id 111
```

## 8. Produce a triage summary

Count threads by status across an inbox:

```bash
echo "=== Inbox 123 triage summary ==="
conv_page /tmp/threads.jsonl conversations threads list --inbox-id 123

echo "Total threads:      $(wc -l < /tmp/threads.jsonl)"
echo "Open:               $(jq -c 'select(.status=="OPEN")' /tmp/threads.jsonl | wc -l)"
echo "Closed:             $(jq -c 'select(.status=="CLOSED")' /tmp/threads.jsonl | wc -l)"
echo "Unassigned (open):  $(jq -c 'select(.status=="OPEN") | select(.assignedTo==null or .assignedTo=="")' /tmp/threads.jsonl | wc -l)"

# Breakdown by channel type. Threads carry originalChannelId, not a type name,
# so build a channelId -> type map from `channels list` and join on it.
conv_page /tmp/channels.jsonl conversations channels list --inbox-id 123
CHANNEL_TYPES=$(jq -s 'map({key: (.id|tostring), value: .type}) | from_entries' /tmp/channels.jsonl)

echo ""
echo "=== By channel type ==="
jq -r --argjson types "$CHANNEL_TYPES" \
  '$types[(.originalChannelId | tostring)] // "UNKNOWN"' /tmp/threads.jsonl \
| sort | uniq -c | sort -rn
```

For a multi-inbox summary, loop over all inbox IDs from step 1 and aggregate.

## Known constraints

- `threads list` requires `--inbox-id` — there is no portal-wide thread listing.
- No server-side filter on `status` or `assignedTo` — filter client-side with `jq`.
- Every `list` command pages at 100 rows and only `--format json` exposes the cursor (`.meta.next`). Bulk and counting steps must use `conv_page`; a bare `--format jsonl` redirect silently truncates and makes a partial run look complete.
- Threads carry no `channelType` — join `originalChannelId` against `channels list` for a type. A thread can switch channels mid-conversation, so this describes where it *started*.
- Bulk archive cannot be collapsed into a single pipe through `--digest`/`--confirm`; each thread must be archived individually with its own two-step flow, and the candidate set must be previewed and approved before any of it executes.
- Digests expire 5 minutes after the `--dry-run` that minted them, so they cannot be collected up front and applied later — mint each one immediately before use.
- Drive bulk loops from a file rather than a pipe: a pipeline-fed `while` body runs in a subshell, so failure counts collected inside it are lost when the loop exits.
- `actors get` looks up a single actor by ID; there is no actors list command. Start from `hubspot owners list` for owner-to-actor mapping.
