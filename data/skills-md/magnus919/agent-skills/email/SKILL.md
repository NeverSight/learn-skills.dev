---
name: email
description: >-
  Send and diagnose transactional email through Twilio SendGrid from a
  terminal or agent: send messages, check deliverability (bounces and spam
  reports), and verify Signed Event Webhook signatures (ECDSA P-256) — with a
  bundled email-cli script that is read-only by default and gates every send
  behind a --dry-run/--yes confirmation. Use when an agent needs to send a
  transactional email, triage bounces or spam complaints, or confirm an
  inbound SendGrid webhook is authentic. Do not use for marketing or bulk
  email campaigns (that is SendGrid Marketing Campaigns), building email
  template systems, or other email providers (that is their own tooling).
license: MIT
compatibility: >-
  The bundled email-cli script runs on Python 3.9+ with only the standard
  library, including the self-contained ECDSA P-256 webhook verifier. --help,
  deliverability checks, and signature verification need no network; sending
  requires a SendGrid API key with mail.send access and network access to
  api.sendgrid.com.
metadata:
  source: https://www.twilio.com/docs/sendgrid
  source_index: references/00-source-index.md
  research_checked: "2026-08-03"
---

# Transactional Email Operations (SendGrid)

Use this skill to send transactional email through **Twilio SendGrid** and to diagnose delivery: bounces, spam complaints, and the Signed Event Webhook. This is a **tool skill** for one vendor (SendGrid). Marketing campaigns, template builders, and other providers are out of scope; this skill owns the operational loop for application-triggered email: send it, check it landed, and verify the events claiming so are authentic.

## Operating contract

1. **Read-only discovery before any mutation.** Check deliverability signals (bounces, spam reports) freely. The bundled `email-cli` script makes reads without writing anything.
2. **Confirm the target, scope, and rollback path before acting.** Sending email puts words in recipients' inboxes in your organization's name: it requires an explicit human directive naming the recipients, sender, and content, plus `--dry-run` preview and `--yes` confirmation through `email-cli`. There is no reliable "un-send" for delivered mail.
3. **Respect bounded reads.** Suppression listings cap results with `--limit`; never page past what the task needs.
4. **Verify webhooks before trusting them.** SendGrid's Signed Event Webhook signs every request; verify the ECDSA signature and timestamp before acting on event data. Unverified webhook endpoints accept forged delivery/bounce events.
5. **Keep evidence bounded.** Quote short message previews and email addresses; never paste API keys, full message bodies, or suppression lists into chat.
6. **Never send to unverified addresses or real users without a directive.** Deliverability triage reads are safe; the send path is always gated.

## The email-cli script

`scripts/email-cli` is an agent-first, stdlib-only CLI over the SendGrid v3 API, including a self-contained ECDSA P-256 signature verifier with no third-party crypto dependency.

```bash
email/scripts/email-cli --help                              # no key or network needed
email/scripts/email-cli --json --limit 20 deliverability bounces
email/scripts/email-cli --json --limit 20 deliverability spam-reports
email/scripts/email-cli send --to user@example.com --from no-reply@example.com \
  --subject "Password reset" --body "..." --dry-run          # preview only
email/scripts/email-cli send --to user@example.com --from no-reply@example.com \
  --subject "Password reset" --body "..." --yes              # confirmed send
email/scripts/email-cli webhook verify --body-file body.json \
  --signature "MEUC..." --timestamp 1712345678 --public-key-file public-key.pem
```

Exit codes: 0 success, 1 API error or failed verification, 2 usage error. Sends are guarded: without `--dry-run` or `--yes` the script refuses with exit 1 and never calls the API. Reads are bounded by `--limit` (default 20, max 100).

## Operating loop

1. **Scope the delivery question**: is this a send (mutation) or a deliverability investigation (read)? Who is the sender, who receives, what is the content?
2. **Read with bounds**: `deliverability bounces` and `deliverability spam-reports` to see who failed to receive and why.
3. **Triage the signal**: map the evidence to the cause (hard bounce → bad or typo'd address; spam complaint → content or frequency problem; suppression list → prior bounce). Check SendGrid's event webhook payloads for delivery/bounce events — after verifying the signature.
4. **Act with confirmation**: only a human directive to send, previewed with `--dry-run` and confirmed with `--yes`.
5. **Verify**: confirm the send response (`x-message-id`), then later confirm delivery via webhook/API evidence rather than assuming.

## Sending transactional email

- **Compose the message**: verified sender (`from`), one or more `to` recipients, `subject`, plain-text `body`, and optionally an `html` body. SendGrid requires the from-address to be a verified sender identity on your account.
- **Preview before sending**: `--dry-run` prints the exact from/to/subject/body preview and never calls the API. `--yes` confirms and posts to `POST /v3/mail/send`, which returns 202 Accepted with the `x-message-id` header.
- **Do not send secrets or tokens by email.** Email is a leak channel; a password-reset link is fine, a raw credential is not.
- SendGrid returns 202 (accepted) — acceptance is not delivery. Confirm delivery from the event webhook or the activity feed before claiming success.

## Deliverability checks

- **Bounces** (`GET /suppression/bounces`): recipients whose mail bounced, with reason and status. Hard bounces (5.x.x permanent) indicate invalid addresses; repeated bounces hurt sender reputation.
- **Spam reports** (`GET /suppression/spam_reports`): recipients who marked mail as spam. Frequent complaints indicate a content or targeting problem.
- Deliverability triage is read-only: diagnose from the suppression lists and webhook events, then change the *next* send (a mutation) only with confirmation.

## Webhook signature verification

SendGrid's Signed Event Webhook signs each request with an ECDSA key pair. To verify:

1. Take the **exact raw request body** bytes — any re-encoding breaks the signature.
2. Check `X-Twilio-Email-Event-Webhook-Timestamp` is recent (replay protection; `email-cli` default window 300s, disable with `--max-age 0`).
3. Compute SHA-256 over `timestamp + raw body` (bytes concatenated, no separator) and verify the ECDSA P-256 signature (`X-Twilio-Email-Event-Webhook-Signature`, base64-decoded ASN.1 DER) against the webhook public key.
4. Reject with 401 if the timestamp is stale or the signature does not verify.

`email-cli webhook verify --body-file body.json --signature <header> --timestamp <header> --public-key-file public-key.pem` runs exactly this check with a stdlib-only P-256 implementation. The public key is shown in the Event Webhook settings when Signed Webhook is enabled; store it as a file, never in code.

## Reference routing

| Load when | Reference |
|---|---|
| Sources, refresh procedure | `references/00-source-index.md` |
| API surface, webhook verification details, deliverability semantics | `references/01-sendgrid-operations.md` |

## Included artifacts

- `scripts/email-cli`: bounded, stdlib-only CLI (send, deliverability bounces/spam-reports, webhook verify with self-contained ECDSA P-256; `--json`; `--limit`; send gated by `--dry-run`/`--yes`).
- `tests/test_email_cli.py`: 15 deterministic tests against a stub SendGrid API plus OpenSSL-generated ECDSA webhook vectors (independent cross-check of the verifier).
- `references/`: dated source index + SendGrid operations reference.
- `evals/evals.json`: six output-quality evaluation cases for agent runs.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| A message was accepted | `email-cli send --yes` exits 0 and returns the `x-message-id` |
| A recipient bounced | `email-cli deliverability bounces --json` lists the address with reason and status |
| A webhook is authentic | `email-cli webhook verify` exits 0 with `verified: true` for the exact body/signature/timestamp |
| Delivery actually happened | Delivery webhook event (verified) or activity feed shows the message as delivered |

## Hard boundaries

- Never send email without a human directive, `--dry-run` preview, and `--yes` confirmation — sent mail is durable, external, and in recipients' inboxes.
- Never trust an inbound webhook without ECDSA signature and timestamp verification.
- Never page reads past `--limit`; never dump full message bodies, API keys, or suppression lists into chat.
- This skill covers SendGrid transactional email only. Marketing campaigns, template systems, and other providers are out of scope.

## When not to use

- **Marketing or bulk email campaigns** (SendGrid Marketing Campaigns, segmentation, blast sends) — that is a different product surface with its own tooling.
- **Other email providers** (Postmark, SES, Mailgun, Resend) — each has its own API; this skill covers SendGrid.
- **Designing email deliverability strategy or domain reputation policy at org scale** — that is operational policy work; this skill operates the SendGrid surface.
- **Building an email feature into an application** (template rendering, transactional flows) — that is application development; see [backend-engineering](../backend-engineering/SKILL.md).
