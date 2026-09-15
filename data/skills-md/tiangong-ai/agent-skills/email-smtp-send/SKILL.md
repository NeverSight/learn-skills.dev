---
name: email-smtp-send
description: Send emails through SMTP with optional local attachments and optional IMAP APPEND sync to Sent mailbox. Use when tasks need reliable outbound email delivery, attachment sending, SMTP connectivity checks, or cross-client sent-mail visibility (for example appending to "Sent Items" after SMTP send).
---

# Email SMTP Send

## Core Goal
- Send outbound email via SMTP with env-configured credentials.
- Attach local files into MIME email payload when requested.
- Optionally append the sent message to IMAP sent mailbox for cross-client visibility.
- Validate SMTP and sent-sync configuration before delivery.
- Return machine-readable JSON status/error output.

## Workflow
1. Configure SMTP env vars (see `references/env.md` and `assets/config.example.env`).
2. Optional: configure IMAP sent-sync env vars and install `imapclient` when sync is enabled.
3. Validate configuration:

```bash
python3 scripts/smtp_send.py check-config
```

4. Send one email:

```bash
python3 scripts/smtp_send.py send \
  --to recipient@example.com \
  --subject "SMTP test" \
  --body "Hello from email-smtp-send"
```

5. Send with attachments:

```bash
python3 scripts/smtp_send.py send \
  --to recipient@example.com \
  --subject "Package delivery" \
  --body "See attachments." \
  --attach ./report.pdf \
  --attach ./appendix.xlsx
```

6. Send and sync to sent mailbox:

```bash
python3 scripts/smtp_send.py send \
  --to recipient@example.com \
  --subject "Synced send" \
  --body "This message will be appended to Sent Items." \
  --sync-sent \
  --sent-mailbox "Sent Items"
```

## Output Contract
- `check-config` prints sanitized SMTP config + defaults + sent-sync config JSON.
- `send` success prints one `type=status` JSON object containing:
  - `event=smtp_sent`
  - sender, recipient summary, subject, SMTP host/port
  - `message_id`
  - `attachment_count` and `attachments[]` metadata
  - `sent_sync` object with `enabled`, `required`, `appended`, and sync metadata/error
- `send` failures print `type=error` JSON to stderr with one of:
  - `event=smtp_send_invalid_args`
  - `event=smtp_send_failed`
  - `event=smtp_sent_sync_failed` (only when sync is required and sync fails)

## Parameters
- `send --to`: required recipient, repeatable or comma-separated.
- `send --cc`: optional CC recipients.
- `send --bcc`: optional BCC recipients.
- `send --subject`: optional subject (defaults from env).
- `send --body`: optional body (defaults from env).
- `send --content-type`: `plain` or `html`.
- `send --from`: optional sender override.
- `send --attach`: optional local attachment path, repeatable or comma-separated.
- `send --max-attachment-bytes`: max bytes allowed per attachment.
- `send --message-id`: optional Message-ID header.
- `send --in-reply-to`: optional In-Reply-To header.
- `send --references`: optional References header.
- `send --sync-sent|--no-sync-sent`: force-enable/disable IMAP sent sync for this send.
- `send --sent-mailbox`: override sent mailbox.
- `send --sent-flags`: IMAP APPEND flags, comma-separated (default `\Seen`).
- `send --sent-sync-required`: return non-zero if SMTP succeeds but sent sync fails.

Environment defaults:
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_SSL`, `SMTP_STARTTLS`
- `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM`, `SMTP_CONNECT_TIMEOUT`
- `SMTP_SUBJECT`, `SMTP_BODY`, `SMTP_CONTENT_TYPE`
- `SMTP_MAX_ATTACHMENT_BYTES`
- `SMTP_SYNC_SENT`, `SMTP_SYNC_SENT_REQUIRED`
- `SMTP_SENT_IMAP_HOST`, `SMTP_SENT_IMAP_PORT`, `SMTP_SENT_IMAP_SSL`
- `SMTP_SENT_IMAP_USERNAME`, `SMTP_SENT_IMAP_PASSWORD`
- `SMTP_SENT_IMAP_MAILBOX`, `SMTP_SENT_IMAP_FLAGS`, `SMTP_SENT_IMAP_CONNECT_TIMEOUT`
- compatibility fallbacks: `IMAP_HOST`, `IMAP_PORT`, `IMAP_SSL`, `IMAP_USERNAME`, `IMAP_PASSWORD`, `IMAP_CONNECT_TIMEOUT`

## Dependency
- Sent-sync mode requires `imapclient`:

```bash
python3 -m pip install imapclient
```

## Error Handling
- Invalid env config exits with code `2`.
- Send failure exits with code `1`.
- If sync is required (`--sent-sync-required` or `SMTP_SYNC_SENT_REQUIRED=true`), sync failure exits with code `1`.

## References
- `references/env.md`

## Assets
- `assets/config.example.env`

## Scripts
- `scripts/smtp_send.py`
