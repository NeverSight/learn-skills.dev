---
name: email-imap-append
description: Compose unsent email drafts (with optional attachments) and append them to an IMAP mailbox via APPEND (typically Drafts) without sending. Use when tasks need to save draft messages for human review, prefill reply templates, stage outbound content inside mailbox folders before manual send, or prepare draft attachments in mailbox-native format.
---

# Email IMAP Append

## Core Goal

- Build RFC 5322 draft messages with subject/body/recipients.
- Attach local files into draft MIME payload when requested.
- Append the draft MIME into an IMAP mailbox using `APPEND`.
- Set draft flags (default `\\Draft`) and keep the message unsent.
- Return machine-readable JSON with append status and server response metadata.

## Workflow
1. Configure IMAP env vars (see `references/env.md` and `assets/config.example.env`).
2. Validate config and defaults:

```bash
python3 scripts/imap_append.py check-config
```

3. Append one draft email to Drafts mailbox:

```bash
python3 scripts/imap_append.py append-draft \
  --to reviewer@example.com \
  --subject "Draft: quarterly update" \
  --body "Please review this draft before sending."
```

4. Append HTML draft with explicit mailbox and flags:

```bash
python3 scripts/imap_append.py append-draft \
  --mailbox "Drafts" \
  --flags "\\Draft,\\Seen" \
  --content-type html \
  --subject "Draft: release note" \
  --body "<p>Release note draft for approval.</p>"
```

5. Append draft with attachments:

```bash
python3 scripts/imap_append.py append-draft \
  --to reviewer@example.com \
  --subject "Draft: WG2 package" \
  --body "See attached draft tables." \
  --attach ./wg2-table.xlsx \
  --attach ./notes.docx
```

## Output Contract
- `check-config` prints sanitized IMAP + append defaults as JSON.
- `append-draft` success prints one `type=status` JSON object containing:
  - `event=imap_draft_appended`
  - `account`, `mailbox`, `subject`, `message_id`
  - recipient lists and counts
  - `flags`
  - `attachment_count` and `attachments[]` metadata
  - `append_uidvalidity` and `append_uid` when server returns `APPENDUID`
- `append-draft` failure prints `type=error` JSON to stderr with `event=imap_append_failed`.

## Parameters
- `append-draft --to`: optional recipient, repeatable or comma-separated.
- `append-draft --cc`: optional CC recipient list.
- `append-draft --bcc`: optional BCC recipient list.
- `append-draft --subject`: optional subject (defaults from env).
- `append-draft --body`: optional body (defaults from env).
- `append-draft --content-type`: `plain` or `html`.
- `append-draft --from`: optional sender override.
- `append-draft --mailbox`: target mailbox (default `IMAP_APPEND_MAILBOX`, then `IMAP_MAILBOX`, then `Drafts`).
- `append-draft --flags`: append flags, comma-separated (default `\\Draft`).
- `append-draft --message-id`: explicit Message-ID header.
- `append-draft --in-reply-to`: optional In-Reply-To header.
- `append-draft --references`: optional References header.
- `append-draft --attach`: local attachment path, repeatable or comma-separated.
- `append-draft --max-attachment-bytes`: max bytes allowed per attachment.

## Required Environment
- `IMAP_HOST`
- `IMAP_USERNAME`
- `IMAP_PASSWORD`

Optional defaults:
- `IMAP_NAME`
- `IMAP_PORT`
- `IMAP_SSL`
- `IMAP_CONNECT_TIMEOUT`
- `IMAP_MAILBOX`
- `IMAP_APPEND_MAILBOX`
- `IMAP_APPEND_FLAGS`
- `IMAP_APPEND_FROM`
- `IMAP_APPEND_TO`
- `IMAP_APPEND_CC`
- `IMAP_APPEND_BCC`
- `IMAP_APPEND_SUBJECT`
- `IMAP_APPEND_BODY`
- `IMAP_APPEND_CONTENT_TYPE`
- `IMAP_APPEND_MAX_ATTACHMENT_BYTES`

## References
- `references/env.md`

## Assets
- `assets/config.example.env`

## Scripts
- `scripts/imap_append.py`
