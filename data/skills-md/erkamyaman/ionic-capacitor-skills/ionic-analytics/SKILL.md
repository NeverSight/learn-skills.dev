---
name: ionic-analytics
description: Add product analytics to an Ionic Capacitor app — Firebase Analytics or PostHog. Trigger when adding event tracking, screen views, funnel analytics, A/B testing, or user behavior tracking to an Ionic mobile app.
license: MIT
metadata:
  author: erkamyaman
  version: '1.0'
---

# Analytics

Two viable choices for product analytics on Ionic Capacitor — pick one. Don't run both.

| | Firebase Analytics | PostHog |
|---|---|---|
| Pricing | Free | Free up to 1M events/mo |
| Funnels / cohorts | Yes (Looker / BigQuery integration) | Yes (built-in) |
| A/B testing | Via Firebase Remote Config | Built-in feature flags |
| Session replay | No (use Sentry / Hotjar) | Yes |
| Self-host | No | Yes |
| Mobile SDK | Native via `@capacitor-firebase/analytics` | JS SDK works in WebView; native plugin available |
| Best for | Already-on-Firebase teams; simple needs | Product-led teams; flag-driven experimentation |

## When to consult

- **Firebase Analytics setup + tracking**: [firebase-analytics.md](references/firebase-analytics.md)
- **PostHog setup + tracking**: [posthog.md](references/posthog.md)
- **Common event taxonomy** (what to track): [event-taxonomy.md](references/event-taxonomy.md)

## Hard rules

- ✅ Track events with **stable, snake_case names**. Renaming an event later orphans the old data.
- ✅ Send the user ID after sign-in (`identify`/`setUserId`) so events stitch across sessions.
- ✅ Respect ATT denial on iOS — don't send IDFA-related identifiers when the user has denied tracking.
- ✅ For EU/UK users, defer analytics calls until consent is captured (see [`../ionic-cmp-consent/`](../ionic-cmp-consent/SKILL.md) — UMP returns analytics consent separately from ad consent).
- ❌ Don't ship event names like `button_clicked_v2` and `button_clicked_v3` — version your **schema**, not your event names.
- ❌ Don't track PII (raw email, IP, full name) as event properties unless legal has approved.
