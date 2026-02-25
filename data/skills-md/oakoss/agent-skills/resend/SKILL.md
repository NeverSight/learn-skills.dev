---
name: resend
description: 'Resend email API for sending transactional and marketing emails. Use when integrating email delivery, managing domains, handling webhooks, building email workflows with React Email, managing contacts, or sending broadcasts. Use for resend, email, transactional, broadcast, contacts, segments, webhooks, domain.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://resend.com/docs
user-invocable: false
---

# Resend

## Overview

Resend is a modern email API built for developers, providing programmatic email sending with support for React Email components, domain management, and webhook-driven event tracking.

**When to use:** Transactional emails (welcome, password reset, receipts), batch email delivery, scheduled sending, webhook-based delivery tracking, domain verification, React Email integration.

**When NOT to use:** High-volume marketing automation (use dedicated ESP), SMS/push notifications, email hosting/inbox management.

## Quick Reference

| Pattern          | API                                         | Key Points                                                    |
| ---------------- | ------------------------------------------- | ------------------------------------------------------------- |
| Send email       | `resend.emails.send({ from, to, subject })` | Returns `{ data, error }`, supports html/text/react content   |
| Send with React  | `resend.emails.send({ react: <Email /> })`  | Node.js SDK only, renders React Email components server-side  |
| Batch send       | `resend.batch.send([...emails])`            | Multiple emails in one request, no attachments/scheduling     |
| Schedule email   | `emails.send({ scheduled_at })`             | ISO 8601 or natural language, cancel before send window       |
| Attachments      | `emails.send({ attachments: [...] })`       | Max 40MB total after encoding, supports content or path       |
| Idempotent send  | `emails.send(params, { idempotencyKey })`   | Prevents duplicate sends on retry                             |
| Retrieve email   | `resend.emails.get(emailId)`                | Check delivery status and metadata                            |
| Add domain       | `resend.domains.create({ name })`           | Returns DNS records for SPF, DKIM, MX                         |
| Verify domain    | `resend.domains.verify(domainId)`           | Triggers DNS record check                                     |
| List domains     | `resend.domains.list()`                     | Returns all domains with status                               |
| Create webhook   | Dashboard or API                            | Subscribe to email lifecycle events                           |
| Verify webhook   | `resend.webhooks.verify({ payload, ... })`  | Validates Svix signature headers                              |
| Tags             | `emails.send({ tags: [...] })`              | Key-value pairs for categorization, ASCII only, max 256 chars |
| Custom headers   | `emails.send({ headers: {...} })`           | Add custom email headers                                      |
| Create contact   | `resend.contacts.create({ email, ... })`    | Global contacts with custom properties                        |
| List contacts    | `resend.contacts.list()`                    | Returns all contacts                                          |
| Create broadcast | `resend.broadcasts.create({ from, ... })`   | Bulk email to a segment, supports template variables          |
| Send broadcast   | `resend.broadcasts.send(id, { segmentId })` | Delivers broadcast to a segment of contacts                   |

## Common Mistakes

| Mistake                                    | Correct Pattern                                                      |
| ------------------------------------------ | -------------------------------------------------------------------- |
| Using root domain for sending              | Use a subdomain like `send.yourdomain.com` to isolate reputation     |
| Not checking `error` in response           | Always destructure `{ data, error }` and handle errors               |
| Sending attachments in batch requests      | Attachments and scheduling are not supported in batch sends          |
| Hardcoding API key in source code          | Use environment variable `RESEND_API_KEY`                            |
| Skipping webhook signature verification    | Always verify using Svix headers before processing events            |
| Using `react` prop outside Node.js SDK     | The `react` prop only works with the Node.js SDK                     |
| Not setting up DMARC after SPF/DKIM verify | Add DMARC record after SPF and DKIM pass to improve deliverability   |
| Exceeding 50 recipients in a single send   | Use batch send or loop for more than 50 recipients per request       |
| Using `&&` for tag name/value characters   | Tag names and values must be ASCII letters, numbers, `_`, or `-`     |
| Ignoring bounce/complaint webhooks         | Monitor `email.bounced` and `email.complained` to protect reputation |

## Delegation

- **Email template design**: Use `Explore` agent to discover React Email component patterns
- **Domain DNS configuration**: Use `Task` agent for step-by-step DNS setup verification
- **Webhook endpoint setup**: Use `Task` agent for route handler implementation

## References

- [Sending emails, batch sending, attachments, scheduling, and idempotency](references/sending-emails.md)
- [Contacts, Segments, Broadcasts, template variables, and bulk sending](references/contacts-and-broadcasts.md)
- [Domain verification, DNS records, and sender identity management](references/domain-management.md)
- [Webhook events, signature verification, and event handling](references/webhooks.md)
