---
name: braze
description: Braze customer engagement platform expertise. Audit campaigns, Canvases, segments, messaging channels, and data architecture. Use when the user asks about Braze, customer engagement, push notifications, in-app messaging, cross-channel orchestration, or lifecycle marketing at scale.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: email-lifecycle
  domain: braze
  updated: 2026-03-11
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Braze Customer Engagement Platform

Expert-level guidance for Braze — auditing, building, and optimizing Canvases, campaigns, segments, data architecture, and cross-channel messaging.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/braze ~/.claude/skills/
```

## Core Capabilities

### Canvas Auditing & Design
- Audit existing Canvases for logic errors, timing issues, and missed opportunities
- Design multi-step, multi-channel Canvases (email, push, SMS, in-app, Content Cards, webhook)
- Implement Canvas Flow features: Action Paths, Audience Paths, Experiment Paths, Decision Splits
- Review entry schedules, exception events, re-eligibility, and rate limiting

### Segmentation & Targeting
- Build segments using Braze's filter system (user attributes, custom events, purchase behavior, engagement)
- Design segment extensions for complex queries (event property filters, nested AND/OR logic)
- Implement predictive audiences (Predictive Churn, Predictive Purchases)
- Connected Audience sync from external CDPs (Segment, mParticle, Amplitude)

### Campaign Strategy
- Plan cross-channel campaigns: email, push, SMS, in-app messages, Content Cards, webhooks
- A/B and multivariate testing with Intelligent Selection
- Personalization with Liquid templating, Connected Content, and Catalogs
- Frequency capping and Intelligent Timing optimization

### Data Architecture
- Design custom event and attribute schemas
- Implement Currents data export (to Snowflake, BigQuery, S3, Mixpanel)
- Plan data migration from other platforms (Klaviyo, Iterable, Salesforce MC)
- API integration patterns (REST API, SDK implementation)

### Deliverability & Compliance
- Email: SPF, DKIM, DMARC, IP warming schedules
- Push: Token management, provisional authorization, opt-in strategies
- SMS: Short code vs long code, compliance (TCPA, CTIA), opt-in management
- GDPR/CCPA data handling and consent management

## Key Benchmarks

| Metric | Good | Great | Warning |
|--------|------|-------|---------|
| Email Open Rate | 20-25% | 30%+ | <15% |
| Email Click Rate | 2-3% | 4%+ | <1.5% |
| Push Open Rate (iOS) | 3-5% | 7%+ | <2% |
| Push Open Rate (Android) | 5-8% | 12%+ | <3% |
| In-App Click Rate | 15-20% | 25%+ | <10% |
| Content Card Click Rate | 10-15% | 20%+ | <5% |
| SMS Click Rate | 8-12% | 15%+ | <5% |
| Unsubscribe Rate (email) | <0.3% | <0.1% | >0.5% |

## Essential Canvas Checklist

1. **Onboarding** — Multi-step cross-channel (push opt-in prompt, email welcome, in-app tutorial)
2. **Activation** — Drive key actions in first 7 days (feature adoption, profile completion)
3. **Re-engagement** — Target lapsed users (7d, 14d, 30d inactivity tiers)
4. **Transactional** — Order confirmations, shipping updates, receipts (use Transactional API)
5. **Promotional** — Scheduled campaigns with audience targeting and frequency caps
6. **Abandoned Cart / Browse** — Trigger-based with exception events for conversion
7. **Winback** — Long-term lapsed users (60d, 90d, 120d)
8. **Feature Announcement** — Targeted by segment, channel preference, and platform
9. **NPS / Feedback** — Post-interaction surveys via in-app or email
10. **Sunset** — Suppress unengaged to protect deliverability

## Workflow: Full Braze Audit

When asked to audit a Braze workspace:

1. **Canvas & Campaign Inventory** — List all active Canvases and campaigns, identify gaps
2. **Channel Coverage** — Map which channels are active (email, push, SMS, in-app, Content Cards)
3. **Segmentation Review** — Evaluate segment definitions, overlap, and growth
4. **Data Architecture** — Custom events, attributes, schema consistency, data freshness
5. **Personalization** — Liquid usage, Connected Content calls, Catalog implementation
6. **Performance Metrics** — Channel-level KPIs, Canvas step conversion rates, variant performance
7. **Deliverability** — Email reputation, push token health, SMS compliance
8. **Frequency & Fatigue** — Global frequency caps, quiet hours, Intelligent Timing usage
9. **Integration Health** — SDK version, Currents export, CDP sync, webhook reliability
10. **Recommendations** — Prioritized by impact with estimated effort (Quick Win / Medium / Large)

## Braze vs Klaviyo Context

When working with teams migrating or comparing:
- **Braze** excels at: Cross-channel orchestration, mobile-first (push, in-app), enterprise scale, real-time event streaming
- **Klaviyo** excels at: E-commerce focus, simpler setup, Shopify-native, strong email/SMS for DTC
- Key migration consideration: Braze's event/attribute model is more flexible but requires upfront schema design

## How to Use This Skill

Ask me questions like:
- "Audit my Braze Canvases and identify gaps"
- "Design an onboarding Canvas for a mobile app"
- "Help me plan a migration from Klaviyo to Braze"
- "What's the best data architecture for a SaaS product in Braze?"
- "My push opt-in rates are low — help me design an opt-in strategy"
- "Build a re-engagement Canvas with Experiment Paths"
- "Plan IP warming for a new Braze workspace"

For detailed Braze data model, Liquid reference, API endpoints, and Canvas patterns, see [REFERENCE.md](REFERENCE.md).
