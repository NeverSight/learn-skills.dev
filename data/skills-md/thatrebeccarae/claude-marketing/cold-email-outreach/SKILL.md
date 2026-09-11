---
name: cold-email-outreach
description: Cold email and outreach sequence design with personalization, deliverability optimization, follow-up cadence, and compliance (CAN-SPAM/GDPR). Use when the user asks about cold email, outreach sequences, email prospecting, cold outreach, or email deliverability for outbound.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: strategy
  domain: cold-email
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Cold Email & Outreach

Design, optimize, and scale cold email outreach with high deliverability and compliance.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/cold-email-outreach ~/.claude/skills/
```

## Deliverability Fundamentals

### Authentication (Required)

| Record | Purpose | Check |
|--------|---------|-------|
| SPF | Authorizes sending servers | `dig TXT domain.com` |
| DKIM | Cryptographic message signing | DKIM selector lookup |
| DMARC | Policy for failed auth | `dig TXT _dmarc.domain.com` |

### Domain Warming

New domains or IPs need gradual volume ramp:

| Week | Daily Volume | Notes |
|------|-------------|-------|
| 1 | 5-10 | Known contacts only |
| 2 | 15-25 | Mix of known and new |
| 3 | 30-50 | Monitor bounce/spam rates |
| 4 | 50-100 | Scale if rates healthy |
| 5+ | 100-200 | Max per domain/day |

**Dedicated sending domain:** Use a subdomain (outreach.company.com) to protect your primary domain reputation.

### Health Benchmarks

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Bounce rate | <2% | 2-5% | >5% |
| Spam complaint | <0.1% | 0.1-0.3% | >0.3% |
| Open rate | >40% | 20-40% | <20% |
| Reply rate | >5% | 2-5% | <2% |

## Sequence Design

### Optimal Sequence Structure

```
Email 1 (Day 0)  — Value-first introduction
Email 2 (Day 3)  — Follow-up with new angle
Email 3 (Day 7)  — Social proof / case study
Email 4 (Day 14) — Breakup email (last attempt)
```

### Timing

- **Best send days:** Tuesday, Wednesday, Thursday
- **Best send times:** 8-10am recipient timezone
- **Avoid:** Monday morning, Friday afternoon, weekends
- **Follow-up spacing:** 3-5 days between emails (never daily)

### Subject Line Formulas

| Formula | Example | Open Rate |
|---------|---------|-----------|
| Question | "Quick question about [company] growth?" | High |
| Mutual connection | "Saw your talk at [event]" | Very high |
| Specific result | "[Company] could save $40K/year on [X]" | High |
| Curiosity | "Idea for [specific initiative]" | Medium-high |
| Direct | "15-min call about [pain point]?" | Medium |

**Rules:** Under 50 characters. No ALL CAPS. No spam triggers (free, guarantee, act now). Personalized > generic.

### Email Body Framework

```
Line 1: Personalized opener (research-based, NOT "I hope this finds you well")
Line 2-3: Pain point or observation specific to them
Line 4-5: How you solve it (one sentence, with social proof)
Line 6: Low-friction CTA (question, not demand)
```

**Length:** 50-125 words. 3-5 sentences max. Mobile-readable.

### Personalization Tiers

| Tier | Effort | When | Example |
|------|--------|------|---------|
| **Researched** | High (5+ min/email) | Top 50 accounts | Reference specific blog post, recent funding, or LinkedIn activity |
| **Templated** | Medium (1 min) | Mid-tier prospects | Company name, industry pain point, role-specific angle |
| **Dynamic** | Low (automated) | Scale outreach | First name, company name, industry via merge fields |

## Compliance

### CAN-SPAM (US)

- Clear sender identity (real name and company)
- Accurate subject line (not misleading)
- Physical mailing address in footer
- Unsubscribe mechanism (honor within 10 days)
- Mark as advertisement if applicable

### GDPR (EU/UK)

- Legitimate interest basis for B2B cold email (document it)
- Clear identity and purpose in first email
- Easy opt-out mechanism
- Do not email personal email addresses without consent
- Data retention policy for prospect data

### Best Practices

- Always include unsubscribe link
- Respect opt-outs immediately (automated)
- Never buy email lists
- Verify emails before sending (reduce bounces)
- Keep records of consent and opt-outs

## Anti-Patterns

1. **Mass blasting** — sending same email to 1000+ at once kills deliverability
2. **No personalization** — "Dear Sir/Madam" or obviously templated
3. **Feature dumping** — listing product features instead of addressing pain
4. **Aggressive follow-ups** — daily follow-ups = spam reports
5. **No unsubscribe** — illegal under CAN-SPAM and GDPR
6. **Misleading subjects** — "Re:" or "Fwd:" on first contact
7. **Too many links/images** — triggers spam filters
8. **No domain warming** — sending 500 emails day 1 from new domain

## Integration with Other Skills

- **copywriting-frameworks** — Apply PAS, BAB, QUEST to cold email copy
- **icp-research** — Define ideal customer profile before building prospect lists
- **email-composer** — General email writing (cold-email-outreach is specifically for outbound sequences)
- **klaviyo-analyst** — For marketing automation email (different from cold outreach)
