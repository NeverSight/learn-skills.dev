---
name: sector-style-intelligence
description: "Visual direction by industry for 20+ sectors: color psychology, typography norms, component conventions, spacing philosophy, motion personality, trust signals, and sector anti-patterns. Use when a design must read as credible for fintech, healthcare, SaaS, e-commerce, or education."
---

# Sector Style Intelligence — Visual Direction by Industry

## Why Sector-Specific Style Matters

Visual design does not exist in a vacuum. Every industry carries implicit expectations that users absorb through years of interaction with competing products, regulatory contexts, and cultural norms. A fintech application that uses playful rounded shapes and saturated candy colors will unconsciously erode trust — not because those choices are inherently bad, but because the sector has conditioned users to associate financial credibility with precision typography, muted palettes, and clinical spacing. Conversely, a wellness app that adopts the dense, data-heavy aesthetic of a trading platform will feel cold and clinical when users expect warmth, breathing room, and organic softness. Sector context is the single most important constraint that separates a technically competent UI from one that genuinely resonates.

The differences run deeper than color palettes. Trust signals vary dramatically: healthcare apps earn credibility through accessibility compliance and clinical precision, while social media platforms build trust through social proof and content velocity. Typography norms diverge — SaaS productivity tools lean on geometric sans-serifs that optimize for information density, while luxury e-commerce demands refined serif typefaces that communicate premium positioning. Spacing philosophy shifts from the deliberate density of a dashboard (where every pixel of screen real estate carries data value) to the generous whitespace of an editorial layout (where breathing room itself communicates sophistication). Even motion design carries sector-specific meaning: a fintech confirmation animation must feel precise and instantaneous, while a meditation app transition should feel slow, deliberate, and calming.

Understanding these sector conventions does not mean blindly following them. The most innovative products in any sector succeed by knowing the rules deeply enough to break them strategically. Stripe revolutionized fintech aesthetics by borrowing editorial elegance from publishing. Duolingo disrupted education by importing gaming mechanics wholesale. But these innovations worked precisely because their creators understood the baseline expectations and chose specific, intentional departures rather than accidental violations. This skill provides that baseline — the deep sector knowledge that makes both convention and strategic deviation possible.

## Sector Coverage

| Sector | Style Archetype | Key Reference Apps |
|---|---|---|
| **Fintech & Banking** | Precision trust, clean data density | Stripe, Cash App, Robinhood, Wise, Revolut, Mercury |
| **Healthcare (Clinical)** | Accessible precision, HIPAA-conscious | One Medical, Epic MyChart, Zocdoc, Teladoc |
| **Wellness & Fitness** | Warm organic, breathing space | Headspace, Calm, Peloton, MyFitnessPal, Apple Health |
| **Social Media** | Content-first, viral loops, dark mode | TikTok, Threads, Discord, BeReal, Mastodon |
| **Creator Tools** | Canvas-centric, minimal chrome | Notion, Figma, Arc, Framer, Obsidian |
| **SaaS & Productivity** | Keyboard-first, information density | Linear, Superhuman, Slack, Raycast, Cron |
| **Enterprise SaaS** | Professional calm, role-based density | Salesforce, Workday, ServiceNow, Datadog |
| **E-Commerce** | High-quality imagery, conversion-optimized | Shopify, Nike SNKRS, StockX, Etsy, SSENSE |
| **Marketplace** | Trust badges, two-sided design | Airbnb, DoorDash, Uber, TaskRabbit |
| **Education** | Gamification, progress, celebration | Duolingo, Khan Academy, Coursera, Brilliant |
| **Entertainment & Media** | Immersive, content-forward, minimal UI | Spotify, Netflix, Apple TV+, YouTube Music |
| **Gaming** | High contrast, achievement systems | Roblox, Steam, Xbox, PlayStation |
| **Travel & Hospitality** | Aspirational imagery, date-driven flows | Airbnb, Booking.com, Hopper, Google Travel |
| **Real Estate** | Map-first, listing cards, filter-heavy | Zillow, Redfin, Trulia, Compass |
| **Food & Beverage** | Appetite appeal, quick ordering flows | DoorDash, Uber Eats, Starbucks, Sweetgreen |
| **Automotive** | Configurator UX, premium materials | Tesla, Rivian, BMW, Porsche |
| **Legal & Compliance** | Document-centric, formal hierarchy | Clio, LegalZoom, DocuSign |
| **Developer Tools** | Terminal aesthetic, code-first, monospace | GitHub, Vercel, Railway, Supabase |
| **AI & ML Products** | Conversational UI, generative patterns | ChatGPT, Claude, Midjourney, Runway |
| **Luxury & Fashion** | Editorial, serif typography, negative space | SSENSE, Mr Porter, Net-a-Porter, Hermes |
| **Non-Profit & Civic** | Accessible, mission-forward, warm | charity: water, ACLU, Code.org |

## Reference Architecture

This skill is organized into deeply researched sector reference files:

| File | Sectors Covered | Lines |
|---|---|---|
| `references/fintech-banking-style.md` | Fintech, Banking, Payments, Crypto | 500+ |
| `references/health-wellness-style.md` | Healthcare (Clinical), Wellness, Fitness | 500+ |
| `references/creator-social-style.md` | Social Media, Creator Tools, Community | 500+ |
| `references/saas-productivity-style.md` | SaaS, Productivity, Developer Tools | 500+ |
| `references/ecommerce-marketplace-style.md` | E-Commerce, Marketplace, Luxury | 500+ |
| `references/education-entertainment-style.md` | Education, Entertainment, Gaming | 500+ |

### Page Template Reference Files

Complete page-level templates with block sequences, typography maps, color application, spacing rhythm, component selection, responsive behavior, and React/TSX skeletons:

| File | Pages Covered | Lines |
|---|---|---|
| `references/saas-page-templates.md` | 10 SaaS pages (landing, pricing, onboarding, dashboard, settings, team, billing, integrations, changelog, docs) with 3 style variants each (Minimal/Warm/Bold) | 1499 |
| `references/fintech-page-templates.md` | 10 Fintech pages (dashboard, transactions, transfer, portfolio, card, bills, loan, budget, insights, KYC) with 2 style variants (Clean Modern/Bold Fintech) + compliance and security patterns | 1002 |
| `references/ecommerce-page-templates.md` | 10 E-Commerce pages (listing, detail, cart, checkout, confirmation, tracking, account, wishlist, returns, reviews) with 2 style variants (Premium/Marketplace) + conversion optimization | 859 |
| `references/healthcare-education-templates.md` | 5 Healthcare pages (portal, booking, records, telemedicine, medications) + 5 Education pages (catalog, detail, dashboard, lesson, quiz) with accessibility and engagement patterns | 1149 |
| `references/creative-developer-templates.md` | 5 Creative/Portfolio pages (landing, case study, about, contact, blog) + 5 Developer pages (docs, API reference, CLI landing, changelog, status) | 1254 |

### Each Style Reference File Includes

1. **Color Psychology** — What colors mean in the sector, palettes from leading apps with hex values
2. **Typography Norms** — Exact fonts top apps use and the reasoning behind those choices
3. **Component Conventions** — Border radius, elevation, density, card styles, button styles with specific px values
4. **Spacing Philosophy** — Dense vs spacious approaches with specific spacing scale values
5. **Motion Personality** — Animation timing, easing curves, transition patterns
6. **Trust Signals** — What makes users trust apps in this sector
7. **Anti-Patterns** — Sector-specific mistakes that erode credibility
8. **Reference Apps** — 6+ apps with specific lessons to learn from each
9. **W3C Design Token Starter Kit** — JSON tokens ready for implementation
10. **Inspiration Links** — Mobbin/Screenlane filters for browsing real patterns

## Cross-References

This skill works in concert with several other sumi skills:

- **ui-visual-design-system** — For foundational color theory, typography scales, and spacing systems that underpin all sector-specific guidance
- **design-systems-architecture** — For token architecture and multi-brand/multi-sector design system strategies
- **interaction-motion-design** — For detailed motion design principles that sector-specific motion personalities build upon
- **desktop-app-design** — For desktop-specific patterns in SaaS, productivity, and enterprise sectors
- **component-patterns-code** — For implementation-ready component code (React, SwiftUI, CSS) that can be styled with sector tokens
- **accessibility-inclusive-design** — For WCAG compliance requirements that apply across all sectors but have heightened importance in healthcare, education, and civic tech
- **cognitive-psychology-ux** — For the psychological principles behind sector-specific trust signals and engagement patterns
- **cross-cultural-i18n-ux** — For adapting sector styles across cultural contexts and markets

## How to Use This Skill

### With the `/style` Command
```
/style fintech — Get complete style direction for a fintech app
/style healthcare clinical — Get clinical healthcare style direction
/style e-commerce luxury — Get luxury e-commerce style direction
```

### With the `/benchmark` Command
```
/benchmark my-app against stripe — Compare your app's visual language against Stripe
/benchmark my-app fintech — Compare against the fintech sector baseline
```

### Direct Reference
When designing for a specific sector, read the relevant reference file to understand the sector's visual language conventions, then apply or strategically deviate from those conventions based on your product's positioning.
