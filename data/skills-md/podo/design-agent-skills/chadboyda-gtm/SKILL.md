---
name: chadboyda-gtm
description: |
  18 go-to-market agent skills that turn a coding agent into a GTM operator:
  positioning + ICP, AI pricing, sales-motion design, cold outreach, AI SDR,
  lead enrichment, multi-platform and Product Hunt launches, programmatic SEO,
  paid creative, retention/expansion, partner programs, and GTM
  metrics/attribution.
triggers:
  - "agent-gtm-skills"
  - "chadboyda"
  - "GTM operator"
  - "go-to-market skills"
  - "sales motion"
  - "AI SDR"
  - "pricing strategy"
das:
  type: package
  category: product-pm
  upstream: "https://github.com/chadboyda/agent-gtm-skills"
  version: latest
---

# chadboyda-gtm

> Catalogue stub — full package: [chadboyda/agent-gtm-skills](https://github.com/chadboyda/agent-gtm-skills)

## Install the full skill

```bash
# Global
npx skills add chadboyda/agent-gtm-skills -g -y

# Project
npx skills add chadboyda/agent-gtm-skills -y
```

Install a single skill instead:

```bash
npx skills add chadboyda/agent-gtm-skills --skill positioning-icp gtm-metrics
```

## What it does

18 GTM skills across strategy, outbound, inbound, paid, retention, and ops:

| Group | Skills |
|-------|--------|
| Strategy | `positioning-icp`, `ai-pricing`, `sales-motion-design` |
| Outbound | `ai-cold-outreach`, `ai-sdr`, `lead-enrichment`, `video-outreach` |
| Inbound | `multi-platform-launch`, `ai-seo`, `social-selling`, `content-to-pipeline` |
| Paid | `ai-ugc-ads`, `paid-creative-ai` |
| Retention | `expansion-retention`, `partner-affiliate` |
| Operations | `gtm-engineering`, `solo-founder-gtm`, `gtm-metrics` |

## When NOT to use

- Product discovery, PRDs, roadmaps → use `assimovt-productskills` or `deanpeters-pm-skills`
- Product positioning craft (messaging hierarchy) → use `product-position`
- Conversion-rate optimization (onboarding, signup) → use `coreyhaines-marketing`
- Landing-page / product copy → use `copywriting-skill`
