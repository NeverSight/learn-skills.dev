---
name: tiktok-ads
description: TikTok Ads platform expertise. Audit campaigns, creative strategy, audience targeting, Spark Ads, TikTok Shop integration, pixel/Events API setup, and performance optimization. Use when the user asks about TikTok advertising, short-form video ads, TikTok Shop, Spark Ads, or social commerce advertising.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: tiktok-ads
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# TikTok Ads

TikTok advertising — campaigns, creative, targeting, Spark Ads, Shop integration, and measurement.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/tiktok-ads ~/.claude/skills/
```

## Campaign Objectives

| Objective | Optimization Goal | Best For |
|-----------|------------------|----------|
| Reach | Maximum impressions | Brand awareness, launches |
| Traffic | Link clicks | Blog, landing page visits |
| Video Views | 6s or 2s views | Content promotion, retargeting pools |
| Community Interaction | Followers, profile visits | Account growth |
| Lead Generation | In-app form submissions | B2C lead capture |
| App Promotion | Installs, in-app events | Mobile app growth |
| Website Conversions | Purchase, signup, add-to-cart | E-commerce, SaaS |
| Product Sales (Shop) | TikTok Shop purchases | Social commerce |

## Ad Formats

| Format | Specs | Best For |
|--------|-------|----------|
| In-Feed Ads | 9:16 vertical, 5-60s, sound on | Standard performance ads |
| Spark Ads | Boost organic posts (yours or creators) | Authenticity, social proof |
| TopView | Full-screen on app open, up to 60s | Maximum reach, launches |
| Branded Hashtag Challenge | Custom hashtag + landing page | UGC, viral campaigns |
| Branded Effects | Custom AR filters/stickers | Interactive engagement |
| Collection Ads | Product cards below video | E-commerce browsing |
| Dynamic Showcase Ads (DSA) | Auto-generated from catalog | Retargeting, catalog scale |
| TikTok Shop Ads | Video Shopping Ads, Live Shopping | Direct social commerce |

## Creative Best Practices

### The TikTok Creative Formula

```
Hook (0-3s) → Value/Story (3-15s) → CTA (last 3s)
```

1. **Hook in first 3 seconds** — the scroll-stopping moment. Use text overlay, unexpected visual, or direct address ("Stop scrolling if you...")
2. **Native aesthetic** — look like a TikTok, not an ad. Phone-shot, real people, trending sounds
3. **Sound on** — 93% of TikTok is consumed with sound. Music and voiceover are critical
4. **Vertical video** — 9:16 only. Never letterboxed horizontal
5. **Text overlays** — 73% of top-performing ads use on-screen text
6. **Fast pacing** — Cut every 2-3 seconds. Static shots die
7. **Creator-led > brand-polished** — UGC-style consistently outperforms studio creative

### Creative Fatigue

- Refresh every 7-14 days (TikTok audiences fatigue 2-3x faster than Meta)
- Maintain 3-5 active creatives per ad group
- Test new hooks on proven body/CTA structures
- Monitor frequency: >3 weekly = fatigue risk

## Targeting

### Interest & Behavior
- Interest categories (broader, for prospecting)
- Video interaction (liked, commented, shared similar content)
- Creator interaction (followed similar creators)
- Hashtag interaction (engaged with relevant hashtags)

### Custom Audiences
- Website traffic (Pixel)
- App activity
- Customer file (email/phone upload)
- Engagement (video views, ad interaction, profile visits)
- TikTok Shop (shoppers, cart abandoners)

### Lookalike Audiences
- Based on any custom audience source
- Broad/Narrow/Balanced options
- Minimum source: 1,000 users

### Smart Targeting
- Automatic audience expansion when optimization allows
- Works well for conversion campaigns with sufficient data
- Requires 50+ conversions per week for optimal learning

## Benchmarks

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| CTR (In-Feed) | >1.5% | 0.8-1.5% | <0.8% |
| CPC | <$0.80 | $0.80-1.50 | >$1.50 |
| CPM | <$8 | $8-15 | >$15 |
| Video view rate (6s) | >15% | 8-15% | <8% |
| CVR (e-commerce) | >2% | 1-2% | <1% |
| ROAS (e-commerce) | >3x | 1.5-3x | <1.5x |
| Cost per lead | <$15 | $15-40 | >$40 |

## Pixel & Events API

### TikTok Pixel Setup
- Base pixel on all pages
- Standard events: ViewContent, AddToCart, InitiateCheckout, CompletePayment
- Custom events for specific actions (signup, demo request)
- Enhanced matching (email, phone) for better attribution

### Events API (Server-Side)
- Complements pixel for iOS 14.5+ signal loss
- Deduplicate with pixel via event_id parameter
- Recommended for all advertisers running conversion campaigns

## Audit Checklist

- [ ] Campaign structure: no more than 3-5 ad groups per campaign
- [ ] Each ad group has 3-5 active creatives
- [ ] Pixel firing correctly on all conversion events
- [ ] Events API configured alongside pixel
- [ ] Budget allows 50+ conversions per week per ad group (for learning phase)
- [ ] Creative refreshed within last 14 days
- [ ] No audience overlap between ad groups
- [ ] Exclusions applied (purchasers, existing customers)
- [ ] Attribution window set appropriately (7-day click, 1-day view standard)
- [ ] Catalog connected (if e-commerce)

## Integration with Other Skills

- **facebook-ads** — Cross-platform creative and audience strategy
- **google-ads** — Full-funnel paid media coverage
- **account-structure-review** — Multi-platform structural audit
- **wasted-spend-finder** — Identify wasted TikTok spend
- **copywriting-frameworks** — Script ad hooks and CTAs
