---
name: astro-forms
description: Form infrastructure for Astro. Zod validation, email, rate limiting, Turnstile, GDPR, Sheets. FAIL = no conversion.
---

# Astro Forms Skill

**Form infrastructure. Backend only. UI is separate.**

## Purpose

Server-side form handling. Validation, email, storage, spam protection.

## Output

```yaml
form_ready: true
data_contract: [lead_id, source_page, timestamp, gdpr_consent]
post_submit_flow: [email, thank_you, analytics]
conversion_verdict: PASS | WARN | FAIL
```

## Primary Conversion Declaration

**One form per page is THE conversion.**

```yaml
primary_conversion:
  type: form
  id: "contact-form"
  page: "/contact"
```

All other forms are secondary (newsletter, etc.).

## Page Exclusion Rules

| Page Type | Forms Allowed |
|-----------|---------------|
| landing | ✅ Primary only |
| service | ✅ Primary only |
| calculator | ❌ Use calculator skill |
| thank-you | ❌ Forbidden |
| 404 | ❌ Forbidden |

**Form on forbidden page = FAIL.**

## Data Integrity Contract

**Every submission MUST contain:**

```yaml
data_contract:
  required:
    - lead_id          # Unique, generated
    - source_page      # URL where submitted
    - timestamp        # ISO datetime
    - gdpr_consent     # true + timestamp
    - ip_hash          # Anonymized
  optional:
    - utm_source
    - utm_medium
    - utm_campaign
```

**Missing required field = submission invalid.**

## Post-Submit Flow Contract

**All three MUST happen:**

```yaml
post_submit_flow:
  1_confirmation_email: required
  2_thank_you_redirect: required
  3_analytics_event: required
```

| Step | What | FAIL if |
|------|------|---------|
| Email | Confirmation to customer | Not sent |
| Thank You | Redirect to /thank-you | No redirect |
| Analytics | GTM event fired | No event |

**Any missing = FAIL.**

## Progressive Disclosure

**Personal data only AFTER value established.**

| Step | Can Ask |
|------|---------|
| 1 | Service type, location |
| 2 | Details, preferences |
| 3+ | Name, email, phone |

**Email on step 1 = WARN.** GDPR and CRO critical.

## Core Features

| Feature | Implementation |
|---------|----------------|
| Validation | Zod server-side |
| Email | Resend → Brevo fallback |
| Rate limit | Cloudflare KV |
| CAPTCHA | Turnstile (invisible) |
| Storage | Google Sheets |
| Spam | Honeypot + time-check |
| GDPR | Required checkbox + timestamp |

## Spam Protection (All Required)

```yaml
spam_protection:
  honeypot: true          # Empty field trap
  time_check: 3000ms      # Min fill time
  turnstile: true         # Cloudflare CAPTCHA
  rate_limit: 5/hour/ip   # KV-based
```

**Any missing = WARN.**

## GDPR Consent

```yaml
gdpr:
  checkbox_required: true
  timestamp_stored: true
  text: "Elfogadom az adatvédelmi szabályzatot"
  link: "/privacy-policy"
```

**Missing checkbox or timestamp = FAIL.**

## Conversion Verdict

```yaml
conversion_verdict: PASS | WARN | FAIL
issues: []
```

| Condition | Verdict |
|-----------|---------|
| Form on forbidden page | FAIL |
| Missing data contract field | FAIL |
| Post-submit flow incomplete | FAIL |
| GDPR missing | FAIL |
| Spam protection incomplete | WARN |
| Email on step 1 | WARN |
| All pass | PASS |

## FAIL States

| Condition |
|-----------|
| Form on thank-you page |
| Missing lead_id/timestamp |
| No confirmation email |
| No thank-you redirect |
| No GTM event |
| GDPR checkbox missing |

## WARN States

| Condition |
|-----------|
| Honeypot missing |
| Time-check missing |
| Personal data on step 1 |
| Rate limiting not configured |

## Environment Variables

```env
RESEND_API_KEY=re_xxxxx
BREVO_API_KEY=xkeysib-xxxxx
GOOGLE_SHEETS_WEBHOOK_URL=https://...
TURNSTILE_SITE_KEY=0x...
TURNSTILE_SECRET_KEY=0x...
```

## References

- [schemas.md](references/schemas.md) — Zod schemas
- [email.md](references/email.md) — Email templates
- [resend-setup.md](references/resend-setup.md) — Resend provider setup
- [cloudflare-setup.md](references/cloudflare-setup.md) — Turnstile, KV, Pages
- [modifiers.md](references/modifiers.md) — Form variations
- [schema-cta.md](references/schema-cta.md) — CTA structure

## Definition of Done

- [ ] Primary conversion declared
- [ ] Data contract fields all present
- [ ] Post-submit flow complete (email + thank-you + event)
- [ ] GDPR checkbox + timestamp
- [ ] Spam protection configured
- [ ] Progressive disclosure followed
- [ ] conversion_verdict = PASS
