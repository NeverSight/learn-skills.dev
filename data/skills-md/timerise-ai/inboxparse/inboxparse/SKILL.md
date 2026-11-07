---
name: inboxparse
description: >
  Build an InboxParse email integration in a Next.js App Router app: a typed server-only client for the V1
  API, a signed webhook receiver, a scheduled sync that stores every email whether or not a webhook arrived,
  and replies sent only after a person approves the exact text. Use when: (1) an app must receive, store,
  search or answer email from Gmail or IMAP mailboxes connected to InboxParse, (2) adding or auditing an
  InboxParse webhook endpoint, sync job or send and reply flow, (3) feeding email into an AI feature without
  letting the email's author steer it, (4) calling the InboxParse API directly for emails, threads, search,
  mailboxes, labels, contacts, webhooks or usage, (5) the user mentions: InboxParse, inboxparse.com, email
  API, email-to-LLM, parse emails, email webhook, X-InboxParse-Signature, whsec_, ip_ API key,
  INBOXPARSE_API_KEY, email.received, email.ai_processed, ai.suggested_response, /api/v1/emails,
  rate_limit_exceeded. Carries the facts the API reference leaves out, checked against the implementation:
  deliveries carry ids, never the email, are retried up to 5 times and disable the subscription after 10
  failures; the signature covers the raw body with no timestamp; the list cursor pages on sent_at alone.
  Next.js App Router; the InboxStore interface is the seam, so Postgres, Supabase or Firestore holds the
  state. Not a mail server, not an email client UI, and not the InboxParse MCP server.
---

# InboxParse in Next.js

InboxParse connects Gmail and IMAP mailboxes and serves every email as markdown with AI-generated labels,
summaries and a suggested reply, through a REST API and webhooks. This skill builds the part of a Next.js app
that receives that mail, keeps it, and answers it.

The idea the design turns on: **a webhook is a hint and the API is the record.** A delivery carries only an
email id, so the receiver verifies it, fetches the email with its own key and returns; a scheduled sync walks
the list and stores whatever is missing. And because every field came from someone outside the app, nothing
an email says is ever sent, run or obeyed without a person.

## When to use

- Building or auditing an app that receives, stores, searches or replies to email through InboxParse.
- Adding an InboxParse webhook, a sync job, an AI feature over email, or a reviewed reply flow.
- Calling the V1 API directly from scripts: see `assets/examples/` and the rules in
  [untrusted-content.md](references/untrusted-content.md).

## When NOT to use

- Running a mail server, SMTP relay or deliverability setup: InboxParse sends through the mailbox's own SMTP.
- Giving an AI assistant direct access to a mailbox: use the InboxParse MCP server at
  `https://inboxparse.com/api/mcp`.
- Other email APIs (Gmail API, Microsoft Graph, SendGrid, Postmark): their own documentation.

## Architecture

```
InboxParse                                     Next.js app (server only)
  event happens --- POST, signed, ids only ---> /api/inboxparse/webhook
                                                  verify raw body, 204, after(): ingestEmail(id)
  GET /emails/:id <--- member key -------------  ingestEmail: fetch once per new id, upsert by id
  GET /emails?date_from <--- member key -------  /api/cron/inboxparse-sync: syncEmails, 48 h window
  POST /emails/reply <--- admin key -----------  approveDraft <- server action <- person submits text
                                                       |
                                                       +-- InboxStore: emails, sync state, drafts
```

- **`lib/inboxparse/`**: `types.ts`, `client.ts`, `signature.ts`, `ingest.ts`, `drafts.ts`, all server-only;
  `store.ts` holds the `InboxStore` seam and a memory store for tests; `instance.ts` exports the host's store.
- **Routes**: the webhook receiver and the cron route; `app/inbox/` holds the email page, the reply form and
  its server action.
- **The seam** is `InboxStore`, specified in [adaptation.md](references/adaptation.md) with the
  Postgres statements that meet it. The host's auth, tenancy, database and UI stay the host's.

## Critical facts

1. **A delivery carries ids, never the email.** `email.received` has `messageId`, `threadId`, `direction`,
   `hasAttachments`; the body comes from `GET /emails/:id`.
2. **The signature is `X-InboxParse-Signature: sha256=<hex>`, HMAC-SHA256 of the exact body.** Any parse and
   re-serialise changes the bytes, so the check runs on `request.text()`.
3. **Nothing in a delivery is unique or timed.** There is no delivery id and no signed timestamp, so a
   replayed delivery verifies; the receiver uses only the id and fetches, which makes a replay a refetch.
4. **Delivery is one attempt with a 10-second timeout, then retries up to 5 attempts.** Ten failures in a row
   disable the subscription until `PATCH /webhooks/:id` sets `is_active: true`.
5. **The webhook secret is returned once**, in the `201` of `POST /webhooks`; no later call shows it.
6. **List items have no content and the list cursor pages on `sent_at` alone.** Emails sharing a page's last
   timestamp need their own exact-timestamp query or they are skipped.
7. **An email becomes listable after it was sent.** Mailbox sync and processing lag, so the sync re-reads a
   lookback window instead of trusting the newest `sent_at` seen.
8. **Member keys read, admin keys write, and `429` is a monthly quota.** It has no `Retry-After`; every call,
   including each search, counts towards `api_calls`.

## Hard rules

1. **Verify the signature over the raw body before parsing it.** Constant-time, length checked first; `401`
   for anything that fails, and nothing is fetched.
2. **A webhook is a hint; the API is the record.** Answer a verified delivery at once, fetch in `after()`, and
   let the sync store what any delivery missed.
3. **Ingest is keyed by the email id.** One detail fetch per new id, an upsert, and `onNewEmail` once, however
   many deliveries and sync runs name it.
4. **Email content is untrusted data.** Rendered as text, never as HTML, never interpolated into code, never
   obeyed by a model, and `ai.*` fields are treated the same.
5. **Nothing is sent without a person approving the exact text.** `ai.suggested_response` only prefills the
   form; one rendered form sends at most once.
6. **Keys stay on the server, and each path holds the least it needs.** Reads use the member key; only the
   approval path reads the admin key; no key or body is logged.

## Quick start

Copy every code block as written to the path on its first line. The only edits are the host's renames in
[adaptation.md](references/adaptation.md) and the reply section's two lines. Agents have added each of these,
and each is wrong here: an in-flight map around `ingestEmail` (it does not span instances, and `saveEmail`
already runs `onNewEmail` once); a walk from the start of the archive or a periodic full scan (each run spends
the monthly quota; an archive import is a stored walk the operator starts, in [sync.md](references/sync.md));
a file or SQLite database (lost and unshared on a serverless host, like memory); a method on `InboxStore`,
such as a list for an index page (every host must then implement it; the module ships one page per email and
no list); dropping the error from a log line (an `InboxParseError` carries the API's message, never the
email's); another test runner.

1. Install `server-only` and `vitest` with npm, set `INBOXPARSE_API_KEY`, and write the types and client:
   [client.md](references/client.md). The package registry is not an external service: install even where a
   task says none is reachable, and never vendor a package.
2. Implement `InboxStore` on the host's database and export it from `lib/inboxparse/instance.ts`:
   [adaptation.md](references/adaptation.md). A host with no database keeps the memory store `instance.ts`
   ships, even when the task says no email may be lost: which database holds the mail is the operator's
   decision, and the handover asks for it. Never add one, `node:sqlite` or a file included, nor its variable.
3. Add `syncEmails`, the cron route and its `vercel.json` entry with `CRON_SECRET`, and run it once:
   [sync.md](references/sync.md).
4. Add the signature check and the webhook route, register the subscription with
   `assets/examples/setup-webhook.sh`, store the secret as `INBOXPARSE_WEBHOOK_SECRET`, and send the test
   event: [webhooks.md](references/webhooks.md).
5. Add the email page, which renders from the store alone, under the rules for rendering, models and logs:
   [untrusted-content.md](references/untrusted-content.md). Who may open it is the host's auth; never invent a
   login or a variable for it.
6. If the app replies, add the drafts, the server action, the form and the reply section, wire
   `currentUserId` to the session and set `INBOXPARSE_ADMIN_API_KEY`: [replies.md](references/replies.md).
7. Add the suite, run by Vitest from `npm test`, 21 tests or 16 without replies:
   [testing.md](references/testing.md).

**Handover.** The final message itself, not only a README it links, tells the operator by name to register the
webhook with `assets/examples/setup-webhook.sh` and store its one-time secret as `INBOXPARSE_WEBHOOK_SECRET`,
to set `INBOXPARSE_API_KEY` and `CRON_SECRET` and call the sync route once, and, whichever applies: that the
memory store loses every email on a cold start until the operator chooses a database, that `/inbox` is open
until the host's auth covers it, and that nothing sends until `currentUserId` is wired and
`INBOXPARSE_ADMIN_API_KEY` is set. An operator reads the message, not the files.

For any other endpoint, [api-reference.md](references/api-reference.md); for an error,
[error-codes.md](references/error-codes.md). The scripts in `assets/examples/` (`list-emails.sh`,
`get-email.sh`, `search-emails.sh`, `send-email.sh`, `setup-webhook.sh`) call the API from a shell with the
key read from the environment.

No InboxParse variable is required at build time, and `client.ts`'s module-level `BASE_URL` stays where it is:
it has a default, and the server reads it again when it loads the module. `npm run typecheck`, `npm run build`
and `npm test` pass with none of them set and no network.

## Reference directory

| Task | Keywords | Reference |
|---|---|---|
| Client, keys, types | API key, ip_, member, admin, Bearer, X-API-Key, fetch, types, V1Email, format, compact, 429 | [client.md](references/client.md) |
| Webhook receiver | webhook, signature, X-InboxParse-Signature, HMAC, whsec_, email.received, email.ai_processed, retries, disabled, test event | [webhooks.md](references/webhooks.md) |
| Sync | sync, poll, cron, CRON_SECRET, vercel.json, cursor, date_from, backfill, missed emails, lookback | [sync.md](references/sync.md) |
| Replies and sending | reply, send, draft, approve, suggested_response, server action, reply section, mailbox_id, smtp_error | [replies.md](references/replies.md) |
| Email page, untrusted content | email page, show email, prompt injection, sanitize, dangerouslySetInnerHTML, HTML email, model, AI summary, logging | [untrusted-content.md](references/untrusted-content.md) |
| Seam and host integration | store, database, no database, Postgres, Supabase, Firestore, tenancy, multi-tenant, auth, rename, order of work | [adaptation.md](references/adaptation.md) |
| Tests | test, vitest, npm test, registry, fake API, concurrency, 21 tests | [testing.md](references/testing.md) |
| Any endpoint | threads, search, mailboxes, IMAP, labels, contacts, usage, deliveries, MCP | [api-reference.md](references/api-reference.md) |
| Errors | error code, 401, 403, 404, 409, 429, 502, unauthorized, forbidden, rate_limit_exceeded | [error-codes.md](references/error-codes.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
