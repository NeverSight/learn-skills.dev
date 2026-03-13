---
name: ads-landing
description: >
  Landing page quality assessment for paid advertising campaigns. Evaluates
  message match, page speed, mobile experience, trust signals, form
  optimization, and conversion rate potential. Use when user says "landing
  page", "post-click experience", "landing page audit", "conversion rate",
  or "landing page optimization".
---

# Landing Page Quality for Ad Campaigns

## Process

1. Collect landing page URLs from active ad campaigns
2. Read `../ads/references/benchmarks.md` for conversion rate benchmarks
3. Read `../ads/references/conversion-tracking.md` for pixel/tag verification
4. Assess each landing page for ad-specific quality factors
5. Score landing pages and identify improvement opportunities
6. Generate recommendations prioritized by conversion impact

## Message Match Assessment

The #1 landing page issue in ad campaigns — does the page match the ad?

### What to Check
- **Headline match**: landing page H1 reflects ad copy headline/keyword
- **Offer match**: promoted offer (price, discount, trial) is visible above fold
- **CTA match**: landing page CTA matches ad's promised action
- **Visual match**: consistent imagery between ad creative and page
- **Keyword match**: search keyword appears naturally in page content

### Message Match Scoring
| Level | Description | Score |
|-------|-------------|-------|
| Exact match | Headline, offer, CTA all align perfectly | 100% |
| Partial match | Headline matches but offer/CTA differs | 60% |
| Weak match | Generic page, loosely related to ad | 30% |
| Mismatch | Page content doesn't reflect ad promise | 0% |

## Page Speed Assessment

Slow pages kill conversion rates. For every 1s delay, CVR drops ~7%.

### Thresholds (Ad Landing Pages)
| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| LCP | <2.5s | 2.5-4.0s | >4.0s |
| FID/INP | <100ms | 100-200ms | >200ms |
| CLS | <0.1 | 0.1-0.25 | >0.25 |
| Time to Interactive | <3.0s | 3.0-5.0s | >5.0s |
| Page weight | <2MB | 2-5MB | >5MB |

### Common Speed Issues in Ad Pages
- Hero images not compressed (use WebP/AVIF)
- Too many third-party scripts (chat widgets, analytics, heatmaps)
- Render-blocking CSS/JS above fold
- No lazy loading for below-fold content
- Font files not preloaded

## Mobile Experience

75%+ of ad clicks come from mobile. Mobile experience is critical.

### Mobile Checklist
- Tap targets: ≥48x48px with ≥8px spacing
- Font size: ≥16px body text (no pinch-to-zoom needed)
- Form fields: properly sized, keyboard type matches input (email, phone, number)
- CTA button: full-width on mobile, visible without scrolling
- No horizontal scroll
- Images responsive and properly sized
- Phone number clickable (tel: link)
- No interstitials or popups blocking content on load

## Trust Signals

### Above-the-Fold Trust Elements
- Company logo visible
- Social proof (customer count, reviews, ratings)
- Security badges (SSL, payment security, guarantees)
- Recognizable client logos (B2B)
- Star ratings or testimonial snippet

### Below-the-Fold Trust Elements
- Full testimonials with names, photos, companies
- Case study highlights with specific metrics
- Certifications, awards, accreditations
- Privacy policy link
- Physical address/phone number (local service businesses)

## Form Optimization

### Form Length Impact on CVR
| Fields | Expected CVR Impact | Use Case |
|--------|-------------------|----------|
| 1-3 fields | Highest CVR | Top-of-funnel, free offer |
| 4-5 fields | Moderate CVR | Mid-funnel, qualified leads |
| 6-8 fields | Lower CVR | Bottom-funnel, sales-ready |
| 9+ fields | Lowest CVR | Only for high-value offers |

### Form Best Practices
- Pre-fill fields where possible (UTM data, known info)
- Use multi-step forms for 5+ fields (progressive disclosure)
- Show progress indicator on multi-step forms
- Inline validation (don't wait until submit to show errors)
- Error messages are clear and helpful
- Submit button text is specific ("Get My Free Quote" not "Submit")
- Thank you page has clear next steps

## Ad-Specific Landing Page Elements

### UTM Parameter Handling
- UTM parameters captured and stored (for attribution)
- Click IDs preserved: gclid (Google), fbclid (Meta), ttclid (TikTok), msclkid (Microsoft)
- Parameters passed to form submissions or CRM

### Dynamic Content
- Dynamic keyword insertion in headline (Google Ads feature)
- Location-specific content for geo-targeted campaigns
- Audience-specific messaging (different pages for different segments)
- A/B testing active on key elements (headline, CTA, hero image)

### Conversion Tracking
- Thank you page/event fires correctly for all platforms
- Form submission triggers conversion event
- Phone call tracking configured (if applicable)
- Chat/live agent triggers tracked as micro-conversions

## Landing Page Quality by Platform

| Platform | Key Requirement | Notes |
|----------|----------------|-------|
| Google | QS component: landing page experience | Directly affects ad rank and CPC |
| Meta | Page load speed critical | Slow pages = Meta penalizes delivery |
| LinkedIn | Professional, B2B appropriate | Match LinkedIn's professional context |
| TikTok | Mobile-first mandatory | 95%+ TikTok traffic is mobile |
| Microsoft | Desktop-optimized matters more | Higher desktop % than other platforms |

## Output

### Landing Page Assessment

```
Landing Page Health

Message Match:    ████████░░  XX/100
Page Speed:       ██████████  XX/100
Mobile:           ███████░░░  XX/100
Trust Signals:    █████░░░░░  XX/100
Form Quality:     ████████░░  XX/100
```

### Deliverables
- `LANDING-PAGE-REPORT.md` — Per-page assessment with scores
- Message match analysis per ad-to-page combination
- Page speed improvement priorities
- Mobile experience fixes
- Form optimization recommendations
- Quick Wins sorted by conversion impact
