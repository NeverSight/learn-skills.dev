---
name: newsleopard-api
description: >
  API reference and code generation for the NewsLeopard EDM API
  (api.newsleopard.com) and SureNotify transactional API
  (mail.surenotifyapi.com). Use when the user asks to write code,
  build integrations, call REST endpoints, or look up API endpoint
  details and field specifications for these specific services.
  Covers contacts, campaigns, A/B testing, reports, templates,
  automation, email, SMS, webhooks, and domain verification.
  Do NOT trigger for: (1) generic email/SMS tasks without
  mentioning NewsLeopard or SureNotify, (2) operational requests
  like sending emails, checking balances, or pausing campaigns
  (even if they mention 電子豹/NewsLeopard — those are MCP Server
  tasks, not API coding tasks), (3) MCP Server operations.
tags:
  - newsleopard
  - surenotify
  - edm
  - api
  - taiwan
  - webhook
  - transactional
---

# NewsLeopard API Integration

Two API sets for email/SMS delivery:

| API | Base URL | Purpose |
|-----|----------|---------|
| EDM API | `https://api.newsleopard.com` | Bulk marketing campaigns |
| SureNotify API | `https://mail.surenotifyapi.com` | Transactional email & SMS |

## Authentication

Both APIs use the `x-api-key` header:

```
x-api-key: YOUR_API_KEY
```

Missing/invalid key returns `{"message": "Forbidden"}`.

## Quick Reference

### EDM API (Bulk Campaigns)

| Action | Method | Endpoint |
|--------|--------|----------|
| Create group | POST | `/v1/contacts/lists/insert` |
| List groups | GET | `/v1/contacts/lists?size=&page=` |
| Import contacts (file) | POST | `/v1/contacts/imports/{list_sn}/file` |
| Import contacts (text) | POST | `/v1/contacts/imports/{list_sn}/text` |
| Check import status | GET | `/v1/contacts/imports/result/{import_sn}` |
| Remove contacts | DELETE | `/v1/contacts/{list_sn}` |
| Submit campaign | POST | `/v1/campaign/normal/submit` (nested body: `form`, `content`, `config`) |
| Single-upload campaign | POST | `/v1/campaign/normal/once` |
| A/B test campaign | POST | `/v1/campaign/testing/submit` (nested body: `form`, `content`, `config`) |
| Single-upload A/B test | POST | `/v1/campaign/testing/once` |
| Delete campaign(s) | DELETE | `/v1/campaign/normal` (body: `campaignSnList`) |
| Pause campaign | PATCH | `/v1/campaign/normal/{sn}` |
| Query campaign status | GET | `/v1/campaign/normal/{sn}` |
| Get campaign codes | GET | `/v1/report/campaigns?startDate=&endDate=` |
| Campaign performance | POST | `/v1/report/campaigns/metrics` |
| Export report | POST | `/v1/report/{campaign_sn}/export` |
| Get report URL | GET | `/v1/report/{campaign_sn}/link` |
| List templates | GET | `/v1/templates` |
| Get template | GET | `/v1/templates/{id}` |
| Trigger automation | POST | `/v1/automation/event` |
| Check balance | GET | `/v1/balance` |

**Variable syntax:** `${CUSTOM_FIELD_NAME}` in subject/content.

### SureNotify API (Transactional)

| Action | Method | Endpoint |
|--------|--------|----------|
| Send email | POST | `/v1/messages` |
| Create/update webhook | POST | `/v1/webhooks` |
| Query webhooks | GET | `/v1/webhooks` |
| Delete webhook | DELETE | `/v1/webhooks` |
| Query email events | GET | `/v1/events` |
| Send SMS | POST | `/v1/sms/messages` |
| SMS webhook CRUD | POST/GET/DELETE | `/v1/sms/webhooks` |
| Query SMS events | GET | `/v1/sms/events` |
| Query exclusive number | GET | `/v1/sms/exclusive-number` |
| Create domain auth | POST | `/v1/domains/{domain}` |
| Verify domain DNS | PUT | `/v1/domains/{domain}` |
| Remove domain | DELETE | `/v1/domains/{domain}` |

**Variable syntax:** `{{variable_name}}` in content.

## Rate Limits

- **EDM API:** 2 req/sec, 300,000 req/day. Report export: 1 req/10 sec.
- **SureNotify:** Max 100 recipients per email request.

## Detailed API References

For full endpoint details, parameters, request/response schemas, and examples:

- **EDM API details:** Read [references/edm-api.md](references/edm-api.md) — contacts, campaigns, A/B testing, reporting, templates, automation
- **SureNotify API details:** Read [references/surenotify-api.md](references/surenotify-api.md) — transactional email, SMS, webhooks, events, domain auth
- **Debugging & QA:** Read [references/debugging-qa.md](references/debugging-qa.md) — common errors, debugging workflows, QA checklists, webhook verification

## Common Integration Patterns

### 1. Campaign Creation Flow (EDM)

```
1. GET  /v1/balance                   → verify sufficient credits
2. GET  /v1/contacts/lists           → get target list SNs
3. GET  /v1/templates/{id}          → fetch template HTML (optional)
4. POST /v1/campaign/normal/submit   → create & schedule campaign
5. GET  /v1/campaign/normal/{sn}    → poll status until sent
6. POST /v1/report/campaigns/metrics → check delivery metrics
```

### 2. Transactional Email Flow (SureNotify)

```
1. POST /v1/domains/{domain}        → set up sender auth (one-time)
2. PUT  /v1/domains/{domain}        → verify DNS records (one-time)
3. POST /v1/messages                → send email with variables
4. GET  /v1/events?id={msg_id}      → check delivery status
```

### 3. SMS Notification Flow (SureNotify)

```
1. POST /v1/sms/messages            → send SMS (include company name per NCC regs)
2. GET  /v1/sms/events?id={msg_id}  → check delivery status
```

## Key Constraints

- **EDM subject:** max 150 chars. **Preheader:** max 60 chars. **From name:** max 50 chars.
- **SureNotify variables:** max 100 chars each.
- **SMS content:** must include company name (NCC regulation). URLs require whitelist approval.
- **Event query window:** 30 days max for both APIs.
- **Import status query:** 30 days max.
- Custom fields must be pre-configured in dashboard before importing contacts.
