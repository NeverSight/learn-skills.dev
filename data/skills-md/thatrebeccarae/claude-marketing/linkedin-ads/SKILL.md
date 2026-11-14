---
name: linkedin-ads
description: LinkedIn Ads platform expertise. Audit campaigns, optimize targeting (job title, company, seniority, industry), creative strategy, Lead Gen Forms, conversion tracking, and ABM campaigns. Use when the user asks about LinkedIn advertising, B2B paid social, LinkedIn campaign optimization, Lead Gen Forms, Matched Audiences, or professional audience targeting.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: linkedin-ads
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# LinkedIn Ads

B2B advertising on LinkedIn — campaigns, targeting, creative, Lead Gen Forms, and ABM.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/linkedin-ads ~/.claude/skills/
```

## Campaign Types

| Type | Objective | Best For |
|------|-----------|----------|
| Sponsored Content | Brand awareness, engagement, conversions | Thought leadership, content promotion |
| Message Ads | Direct outreach at scale | Event invites, demo requests, high-value offers |
| Text Ads | Cost-efficient clicks | Always-on brand visibility |
| Dynamic Ads | Personalized (follower, spotlight, jobs) | Follower growth, personalized CTAs |
| Document Ads | Lead gen through gated content | Whitepapers, reports, guides |
| Video Ads | Brand awareness, engagement | Product demos, testimonials, thought leadership |
| Conversation Ads | Multi-CTA interactive messages | Complex offers, event + content combos |
| Lead Gen Forms | In-platform lead capture | Gated content, demo requests, newsletter signups |

## Targeting Capabilities

### Professional Targeting (LinkedIn-Exclusive)

| Dimension | Examples | Use Case |
|-----------|---------|----------|
| Job Title | VP Marketing, CMO, Head of Growth | Role-specific targeting |
| Job Function | Marketing, Sales, Engineering | Broad function targeting |
| Seniority | C-Suite, VP, Director, Manager, Entry | Decision-maker targeting |
| Company Name | Specific company lists | ABM campaigns |
| Company Size | 1-10, 11-50, 51-200, 201-500, 500+ | Segment by org size |
| Company Industry | SaaS, Healthcare, Finance, etc. | Vertical targeting |
| Skills | Digital Marketing, SEO, Data Analysis | Interest/expertise targeting |
| Groups | LinkedIn Group membership | Community targeting |
| Years of Experience | 1-2, 3-5, 6-10, 10+ | Career stage |
| Education | Degree, field of study, school | Academic targeting |

### Matched Audiences

| Type | Source | Use Case |
|------|--------|----------|
| Contact Targeting | Email lists (300+ match) | CRM retargeting, ABM |
| Company Targeting | Company name lists | ABM account lists |
| Website Retargeting | Insight Tag pixel | Site visitor retargeting |
| Lookalike Audiences | Expand from any source | Scale proven audiences |
| Engagement Retargeting | Ad/page engagers | Warm audience nurturing |
| Event Retargeting | LinkedIn Event attendees | Post-event follow-up |

### Audience Size Guidelines

| Campaign Type | Minimum | Recommended | Maximum |
|--------------|---------|-------------|---------|
| Sponsored Content | 50,000 | 100,000-300,000 | 500,000+ |
| Message Ads | 15,000 | 30,000-100,000 | 200,000 |
| Lead Gen Forms | 50,000 | 100,000-300,000 | 500,000+ |
| ABM (Company List) | 300 companies | 500-1,000 companies | 5,000 |

## Benchmarks

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| CTR (Sponsored Content) | >0.8% | 0.4-0.8% | <0.4% |
| CTR (Message Ads) | >3% | 1-3% | <1% |
| CPC (Sponsored Content) | <$5 | $5-10 | >$10 |
| CPM | <$30 | $30-60 | >$60 |
| Cost per Lead (Lead Gen) | <$50 | $50-150 | >$150 |
| Lead Gen Form completion | >15% | 10-15% | <10% |
| Video view rate | >25% | 15-25% | <15% |
| Social engagement rate | >0.5% | 0.3-0.5% | <0.3% |

## Audit Workflow

### Step 1: Account Structure
- Campaign groups organized by objective/audience
- No overlapping audiences competing against each other
- Budget allocation matches business priorities
- Naming convention: `[Objective]-[Audience]-[Creative Type]-[Date]`

### Step 2: Targeting Assessment
- Audience size within recommended ranges
- No conflicting targeting layers (too narrow)
- Exclusions applied (current customers, competitors, employees)
- Matched Audiences utilizing CRM data

### Step 3: Creative Review
- Ad format matches objective
- Intro text under 150 characters (before truncation)
- Image specs: 1200x627 (sponsored content), 1200x1200 (carousel)
- Video: 15-30 seconds, captions, square or vertical for mobile
- CTA button aligned with landing page intent

### Step 4: Conversion Tracking
- Insight Tag installed and firing
- Conversion events configured (lead, purchase, signup)
- Offline conversion import set up (if applicable)
- Attribution window appropriate (30-day for B2B)

### Step 5: Budget & Bidding
- Daily budget sufficient for target audience size
- Bid strategy aligned with maturity (auto for new, manual for optimized)
- Cost caps set based on target CAC

## Best Practices

### Creative
- Single-image > carousel for awareness (simpler, higher CTR)
- Document ads for lead gen (native PDF viewer, no landing page needed)
- Video with captions (85% of LinkedIn video watched without sound)
- Refresh creative every 4-6 weeks (frequency fatigue sets in fast)

### Targeting
- Start broad, then narrow based on performance data
- Layer max 2-3 targeting dimensions (avoid over-segmentation)
- Use exclusions aggressively (exclude converted leads, competitors)
- ABM: combine company list + seniority for precision

### Lead Gen Forms
- Max 3-4 fields (pre-filled from profile = high completion)
- Include a thank-you page with next step
- Integrate with CRM (Zapier, native, or API) for instant follow-up
- Speed-to-lead matters: contact within 5 minutes = 9x higher connect rate

## Integration with Other Skills

- **google-ads** — Cross-platform campaign comparison
- **facebook-ads** — Meta vs LinkedIn targeting overlap analysis
- **account-structure-review** — Multi-platform structural audit
- **wasted-spend-finder** — Identify wasted LinkedIn spend
- **copywriting-frameworks** — Apply PAS/AIDA to LinkedIn ad copy
