---
name: email-triage
displayName: Email Triage
description: "Triage Joel's email inboxes via the joelclaw email CLI. Scan, categorize, archive noise, surface actionable items, and draft replies. Use when: 'check my email', 'scan inbox', 'triage email', 'what needs a reply', 'clean up inbox', 'archive junk', 'email summary', 'anything important in email', or any request involving email inbox review or cleanup."
version: 2.0.0
author: Joel Hooks
tags: [joelclaw, email, triage, inbox, front]
---

# Email Triage

Scan Joel's email inboxes (Front), triage conversations by importance, archive noise, and surface items needing attention. All operations use the `joelclaw email` CLI.

## Front Search API Reference

The search endpoint is `GET /conversations/search/{url_encoded_query}`.
Results sorted by last activity date (not configurable).

### Valid `is:` statuses
`open`, `archived`, `assigned`, `unassigned`, `snoozed`, `trashed`, `unreplied`, `waiting`, `resolved`

**There is NO `is:unread`.** Use `is:unreplied` for conversations where the last message was inbound.

Status conflicts (cannot combine):
- `archived` ↔ `open` ↔ `trashed` ↔ `snoozed` (mutually exclusive)
- `assigned` ↔ `unassigned` (mutually exclusive)

### Date filters — UNIX TIMESTAMPS ONLY
- `before:<unix_seconds>` — messages/comments created before this timestamp
- `after:<unix_seconds>` — messages/comments created after this timestamp
- `during:<unix_seconds>` — messages/comments on same day as timestamp

**Front does NOT accept `before:YYYY-MM-DD`** — always convert to unix seconds.
The CLI `--before` and `--after` flags accept `YYYY-MM-DD` and convert automatically.

### Recipient filters
- `from:<handle>` — sender (email, social handle)
- `to:<handle>` — recipient (includes to/cc/bcc)
- `cc:<handle>`, `bcc:<handle>` — specific fields
- `recipient:<handle>` — any role (from, to, cc, bcc)
- Multiple same-type filters use **OR** logic: `from:a@x.com from:b@x.com` → either
- Different filter types use **AND** logic: `from:a@x.com to:b@x.com` → both

### Entity filters (use IDs, not names)
- `inbox:<inbox_id>` — e.g. `inbox:inb_41w25`
- `tag:<tag_id>` — e.g. `tag:tag_13o8r1`
- `assignee:<teammate_id>` — e.g. `assignee:tea_hjx3`
- `participant:<teammate_id>`, `author:<teammate_id>`, `mention:<teammate_id>`, `commenter:<teammate_id>`
- `contact:<contact_id>`, `link:<link_id>`
- `custom_field:"<name>=<value>"`

### Free text
Bare words search subject + body. Phrases in quotes: `"exact phrase"`.

### No negation
Front search has **no negation** — no `-from:`, no `NOT`, no exclusion operators.

### Max 15 filters per query.

## CLI Commands

### Scan inbox
```bash
joelclaw email inbox                          # default: is:open, 50 results
joelclaw email inbox -n 100                   # more results
joelclaw email inbox -q "is:open is:unreplied"  # awaiting reply
joelclaw email inbox --from notifications@github.com  # by sender
joelclaw email inbox --before 2026-02-01      # auto-converts to unix ts
joelclaw email inbox --after 2026-01-15       # auto-converts to unix ts
joelclaw email inbox --page-token "TOKEN"     # pagination (from previous response)
```

Flags can be combined:
```bash
joelclaw email inbox --from matt@totaltypescript.com --after 2026-02-01 -n 20
```

### Archive single
```bash
joelclaw email archive --id cnv_xxx
```

### Archive multiple by ID (fast, parallel, batched)
```bash
joelclaw email archive-ids --ids cnv_abc,cnv_def,cnv_ghi
```
Runs 10 concurrent requests. Best for triaging a page of results — grab the IDs of noise and blast them.

### Archive bulk by query (dry-run by default)
```bash
joelclaw email archive-bulk -q "is:open from:notifications@github.com"           # dry run — shows count + sample
joelclaw email archive-bulk -q "is:open from:notifications@github.com" --confirm  # execute
joelclaw email archive-bulk -q "is:open from:notifications@github.com" --limit 100 --confirm  # batch size
```

### Read a conversation
```bash
joelclaw email read --id cnv_xxx
```

### List inboxes
```bash
joelclaw email inboxes
```

## Triage Workflow

### 1. Load inbox state

```bash
joelclaw email inbox -n 50
```

Parse the JSON result. Each conversation has: `id`, `subject`, `from` (name + email), `date`, `status`, `tags`.

Useful follow-up queries:
```bash
joelclaw email inbox -q "is:open is:unreplied" -n 50   # awaiting reply
joelclaw email inbox --before 2026-01-01 -n 50          # old stuff to clean
joelclaw email inbox --from notifications@github.com    # CI noise check
```

### 2. Categorize using inference

Read each conversation and **decide** its category based on sender, subject, and context. Do NOT use hardcoded domain lists. Use judgment:

- **Reply needed** — Real people expecting a response. Colleagues, collaborators, friends, business contacts with personal messages. Look for reply threads (`Re:`), questions, invitations to specific meetings, requests.
- **Read later** — Interesting content worth saving. Newsletters Joel subscribes to intentionally (The Information, Astral Codex Ten, Lenny's Newsletter), industry news, technical deep-dives.
- **Actionable** — Requires action but not a reply. Bills, security alerts, expiring trials, tax documents, delivery updates for real orders, calendar invites needing RSVP.
- **Archive** — No value. Marketing spam, promotional offers, cold outreach, duplicate notifications, resolved alerts, automated reports nobody reads, vendor upsells.

### 3. Present triage summary

Organize findings for Joel. Lead with what matters:

```
## 🔴 Reply needed (N)
- **Name** — Subject (why it needs a reply)

## ⚡ Actionable (N)
- **Sender** — Subject (what action)

## 📖 Read later (N)
- **Source** — Subject

## 🗑️ Archive candidates (N)
- Count by type (e.g., "14 marketing, 8 CI failures, 5 duplicate notifications")
```

### 4. Execute decisions

**Fastest path for noise:** scan a page, collect noise IDs, use `archive-ids`:
```bash
joelclaw email archive-ids --ids cnv_aaa,cnv_bbb,cnv_ccc,cnv_ddd
```

**For sender-based cleanup:** use `archive-bulk` with `from:` filter:
```bash
joelclaw email archive-bulk -q "is:open from:notifications@github.com" --limit 100 --confirm
```

**Rate limiting:** Front allows ~50 req/s. If archiving large batches (>200), add pauses between batches or expect 429s. The CLI handles batching for `archive-ids` (10 concurrent), but `archive-bulk` iterates page-by-page and may hit limits on very large sets.

**Read before deciding:**
```bash
joelclaw email read --id cnv_xxx
```

## Key Context

- Joel has 8 Front inboxes across joel@egghead.io, joelhooks@gmail.com, joel@skillrecordings.com, joel@badass.dev, joel.hooks@vercel.com, LinkedIn, DMs, and Inngest
- `joelclaw email inboxes` lists them all with IDs
- Joel's teammate ID: `tea_hjx3`
- The CLI handles Front API auth automatically via `secrets lease front_api_token`
- Draft-then-approve for replies — never send directly
- Front search results are eventually consistent — recently archived items may still appear in search for a few minutes
- Pagination: responses include `next_page_token` when more results exist; pass via `--page-token`

## Signals for "Reply Needed"

These are heuristics, not rules. Use judgment for each:

- `Re:` prefix + real person sender (not a bot/noreply)
- `[aih]` prefix — AI Hero collaboration (Matt Pocock, Alex Hillman)
- Direct questions in subject line
- Meeting invitations from known contacts
- Threads where Joel was the last sender and someone replied
- Slack notification summaries (may indicate missed conversations worth checking)

## Signals for "Archive"

- `noreply@`, `no-reply@`, `notifications@` senders with no actionable content
- Marketing subject patterns: "LAST chance", "% off", "deal", "unlock", "limited time"
- Duplicate conversations (same subject from same sender — archive all but most recent)
- Resolved monitoring alerts (`RESOLVED` in subject)
- CI failure notifications older than 24h (stale — either fixed or won't be)
- Cold outreach from unknown senders with sales language

## Common Noise Senders (bulk-archive candidates)

These are historically high-volume, low-signal senders. Use `archive-bulk` with `from:` filter:
```
notifications@github.com        — CI failures, dependabot, PR notifications
alerts@alerts.betterstack.com   — resolved uptime alerts
no-reply@is.email.nextdoor.com  — neighborhood spam
```
Always dry-run first to verify the query matches what you expect.
