---
name: email-smtp-send
description: Send emails through an SMTP server using environment-based credentials and message fields. Use when tasks need reliable outbound email delivery (single or repeated recipients), SMTP connectivity checks, or scripted test sends.
---

# Email SMTP Send

## Core Goal
- Send outbound email via SMTP with env-configured credentials.
- Validate SMTP configuration before delivery.
- Return machine-readable JSON status/error output.

## Workflow
1. Configure SMTP env vars (see `references/env.md` and `assets/config.example.env`).
2. Validate configuration:

```bash
python3 scripts/smtp_send.py check-config
```

3. Send one email:

```bash
python3 scripts/smtp_send.py send \
  --to recipient@example.com \
  --subject "SMTP test" \
  --body "Hello from email-smtp-send"
```

## Output Contract
- `check-config` prints sanitized SMTP config JSON.
- `send` success prints a `type=status` record with:
  - `event=smtp_sent`
  - sender, recipient summary, subject, SMTP host/port
- `send` failure prints `type=error` with `event=smtp_send_failed` to stderr.

## Parameters
- `send --to`: required recipient, repeatable or comma-separated.
- `send --cc`: optional CC recipients.
- `send --bcc`: optional BCC recipients.
- `send --subject`: optional subject (defaults from env).
- `send --body`: optional body (defaults from env).
- `send --content-type`: `plain` or `html`.
- `send --from`: optional sender override.

Environment defaults:
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_SSL`, `SMTP_STARTTLS`
- `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM`, `SMTP_CONNECT_TIMEOUT`
- `SMTP_SUBJECT`, `SMTP_BODY`, `SMTP_CONTENT_TYPE`

## Error Handling
- Invalid env config exits with code `2`.
- Send failure exits with code `1` and JSON error detail.

## References
- `references/env.md`

## Assets
- `assets/config.example.env`

## Scripts
- `scripts/smtp_send.py`
