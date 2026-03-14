---
name: competitor-analysis
description: Comprehensive competitor analysis, competitive intelligence, and comparison page creation. Use when analyzing competitive landscape, creating competitor comparison pages (alternative pages, vs pages, competitor A vs B pages), performing market research, building SWOT analysis, creating feature matrices, pricing comparisons, competitor teardowns, battle cards, or positioning maps. Covers research workflows, SEO-optimized comparison content, data-grounded reports with citations, 7-layer analysis framework, review mining, and sales enablement. Triggers include competitor analysis, competitive analysis, competitor teardown, vs page, alternative page, competitor comparison, market research, competitive intelligence, SWOT analysis, battle card, competitor pricing, market landscape, feature comparison, positioning map.
---

# Competitor Analysis

Comprehensive competitor analysis, competitive intelligence, and comparison page creation using structured research frameworks and data-grounded methodologies.

## Overview

Systematic competitor analysis reveals market positioning, identifies competitive advantages, informs strategic decisions, captures SEO traffic, and enables sales teams with battle cards and comparison content.

## When to Use

- Strategic product and market planning
- Creating SEO comparison pages (alternative pages, vs pages)
- Market entry and pricing strategy
- Feature prioritization and positioning
- Threat assessment and investment decisions
- Sales enablement (battle cards, objection handling)
- Competitive intelligence reports

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

Before creating competitor analysis or comparison pages, understand:

1. **Your Product** - Core value proposition, differentiators, ICP, pricing, strengths/weaknesses
2. **Competitive Landscape** - Direct/indirect competitors, market positioning, search volume
3. **Goals** - SEO traffic, sales enablement, conversion, brand positioning

## Core Principles

### 1. Honesty Builds Trust
- Acknowledge competitor strengths
- Be accurate about your limitations
- Don't misrepresent competitor features
- Readers verify claims

### 2. Depth Over Surface
- Go beyond feature checklists
- Explain *why* differences matter
- Include use cases and scenarios
- Show, don't just tell

### 3. Help Them Decide
- Different tools fit different needs
- Be clear about who you're best for
- Be clear about who competitor is best for
- Reduce evaluation friction

### 4. Data-Grounded Analysis
- Every claim must have a citation
- Use primary sources when possible
- Document when data is unavailable
- Refresh quarterly

## Competitor Identification

**Competitor Types:**

| Type | Definition | Example |
|------|------------|---------|
| **Direct** | Same market, same features | Same product category, same ICP |
| **Indirect** | Different approach, same problem | Alternative solutions to the same pain |
| **Adjacent** | Related market, potential crossover | Could expand into your space |
| **Emerging** | New entrants, potential disruptors | Startups with new approaches |

## Research Workflow (6 Steps)

### Step 1: Extract Business Information

**If website URL provided:**
- Fetch and extract: company name, value proposition, target market, products, pricing, differentiators

**If details provided:**
- Parse information and identify gaps requiring web research

**Required context to gather:**
- Company name and description
- Industry/vertical
- Target customer segment (B2B/B2C, size, geography)
- Core products/services
- Pricing model
- Key value propositions

### Step 2: Define Target Customer Profile (Required)

Understanding the target customer enables accurate assessment of direct vs. indirect competitors.

**Firmographics:**
- Company size (employees, revenue range)
- Industry/vertical focus
- Geographic markets served
- Technology maturity level

**Psychographics & Pain Points:**
- Top 3-5 pain points the product addresses
- Primary goals and desired outcomes
- Current alternatives or workarounds
- Decision-making criteria
- Budgetary constraints

**Behavioral Patterns:**
- How customers currently solve this problem
- Where they search for solutions
- Typical buying process and timeline
- Key stakeholders in purchase decision

**Market Sizing (if discoverable):**
- Total addressable market (TAM) estimates
- Serviceable addressable market (SAM)
- Market growth trends

### Step 3: Identify Top 5 Competitors

Run targeted searches:
- "[company name] competitors"
- "[product category] companies"
- "[industry] [target market] solutions"
- "alternatives to [company name]"

Select based on: similar target market, overlapping offerings, comparable business model, market presence.

### Step 4: Research Each Competitor

For each competitor, gather data across four dimensions:

**4a. Market Positioning & Messaging**
- Fetch homepage and about page
- Extract: tagline, value proposition, target audience messaging
- Note: tone, positioning, key claims

**4b. Pricing & Business Model**
- Search "[competitor] pricing"
- Document: pricing tiers, model (subscription/one-time/freemium), entry price
- If not public, note this and search for indirect indicators

**4c. Product/Feature Comparison**
- Review product pages and feature lists
- Identify: core features, unique capabilities, integrations, limitations
- Note recent product launches

**4d. Funding & Company Size**
- Search "[competitor] funding" and "[competitor] company size"
- Check: Crunchbase, LinkedIn company size, press releases
- Document: funding rounds, total raised, employee count, founding year

### Step 5: Identify Market Gaps & Opportunities

**Underserved customer segments:**
- Which customer types or use cases do competitors ignore?
- Geographic, size, or industry segments with limited options?

**Feature/capability gaps:**
- What functionality is missing across all competitors?
- What do customers request that no one provides well?
- What emerging needs are competitors slow to address?

**Positioning gaps:**
- What market positions are unclaimed? ("affordable enterprise-grade", "developer-first")
- Price points without strong offerings?
- Business models competitors avoid?

Document 3-5 specific gaps with supporting evidence.

### Step 6: Synthesize Report

Generate markdown report with cited sources (see [references/competitive-analysis-framework.md](references/competitive-analysis-framework.md) for full template).

## The 7-Layer Analysis Framework

| Layer | What to Analyze | Data Source |
|-------|----------------|-------------|
| **1. Product** | Features, UX, quality | Screenshots, free trial |
| **2. Pricing** | Plans, pricing model, hidden costs | Pricing page, sales call |
| **3. Positioning** | Messaging, tagline, ICP | Website, ads |
| **4. Traction** | Users, revenue, growth | Web search, press, funding |
| **5. Reviews** | Strengths, weaknesses from users | G2, Capterra, App Store |
| **6. Content** | Blog, social, SEO strategy | Website, social profiles |
| **7. Team** | Size, key hires, background | LinkedIn, About page |

## Comparison Page Formats (for SEO)

### Format 1: [Competitor] Alternative (Singular)

**Search intent**: User actively looking to switch from specific competitor

**URL pattern**: `/alternatives/[competitor]` or `/[competitor]-alternative`

**Target keywords**: "[Competitor] alternative", "alternative to [Competitor]"

**Page structure**:
1. Why people look for alternatives
2. Summary: You as the alternative
3. Detailed comparison (features, pricing, service)
4. Who should switch (and who shouldn't)
5. Migration path
6. Social proof from switchers
7. CTA

### Format 2: [Competitor] Alternatives (Plural)

**Search intent**: User researching options, earlier in journey

**URL pattern**: `/alternatives/[competitor]-alternatives`

**Page structure**:
1. Why people look for alternatives
2. What to look for in an alternative
3. List of alternatives (you first, include 4-7 real options)
4. Comparison table
5. Detailed breakdown of each
6. Recommendation by use case
7. CTA

### Format 3: You vs [Competitor]

**Search intent**: User directly comparing you to competitor

**URL pattern**: `/vs/[competitor]`

**Page structure**:
1. TL;DR summary
2. At-a-glance comparison table
3. Detailed comparison by category
4. Who [You] is best for
5. Who [Competitor] is best for
6. Customer testimonials from switchers
7. Migration support
8. CTA

### Format 4: [Competitor A] vs [Competitor B]

**Search intent**: User comparing two competitors (not you)

**URL pattern**: `/compare/[competitor-a]-vs-[competitor-b]`

**Page structure**:
1. Overview of both products
2. Comparison by category
3. Who each is best for
4. The third option (introduce yourself)
5. Comparison table (all three)
6. CTA

See [references/comparison-page-templates.md](references/comparison-page-templates.md) for detailed templates.

## Feature Comparison Matrix

### Structure

```markdown
| Feature | Your Product | Competitor A | Competitor B | Competitor C |
|---------|:---:|:---:|:---:|:---:|
| Real-time collaboration | ✅ | ✅ | ❌ | ✅ |
| API access | ✅ | Paid only | ✅ | ❌ |
| SSO/SAML | ✅ | Enterprise | ✅ | Enterprise |
| Mobile app | ✅ | iOS only | ✅ | ✅ |
```

### Rules

- ✅ = Full support
- ⚠️ or "Partial" = Limited or conditional
- ❌ = Not available
- Note conditions: "Paid only", "Enterprise tier", "Beta"
- Lead with features where YOU win
- Be honest about competitor strengths

## Pricing Comparison

### Structure

```markdown
| | Your Product | Competitor A | Competitor B |
|---------|:---:|:---:|:---:|
| **Free tier** | Yes, 5 users | Yes, 3 users | No |
| **Starter** | $10/user/mo | $15/user/mo | $12/user/mo |
| **Pro** | $25/user/mo | $30/user/mo | $29/user/mo |
| **Enterprise** | Custom | Custom | $50/user/mo |
| **Billing** | Monthly/Annual | Annual only | Monthly/Annual |
| **Annual discount** | 20% | 15% | 25% |
| **Min seats** | 1 | 5 | 3 |
| **Hidden costs** | None | Setup fee $500 | API calls metered |
```

### What to Look For

- Minimum seat requirements
- Annual-only billing
- Feature gating between tiers
- Overage charges
- Setup/onboarding fees
- Contract lock-in periods

## SWOT Analysis

Create SWOT for each competitor (and yourself):

```markdown
### Competitor A — SWOT

| Strengths | Weaknesses |
|-----------|------------|
| • Strong brand recognition | • Slow feature development |
| • Large integration ecosystem | • Complex onboarding (30+ min) |
| • Enterprise sales team | • No free tier |

| Opportunities | Threats |
|--------------|---------|
| • AI features not yet shipped | • New AI-native competitors |
| • Expanding into mid-market | • Customer complaints about pricing |
| • International markets untapped | • Key engineer departures (LinkedIn) |
```

**Strategy Recommendations:**

**Leverage strengths:**
- Market mobile-first advantage
- Highlight superior support in sales
- Emphasize quick deployment (faster ROI)

**Address weaknesses:**
- Develop enterprise features roadmap
- Increase marketing/brand investment
- Expand partnerships for integrations

**Capitalize opportunities:**
- Launch enterprise edition (higher ACV)
- Plan international expansion
- Build AI feature suite aggressively

**Mitigate threats:**
- Strengthen customer lock-in (switching costs)
- Build ecosystem of partners
- Focus on customer success/retention
- Invest in differentiation

## Positioning Map

A 2x2 matrix showing where competitors sit on two meaningful dimensions.

**Choose Meaningful Axes:**

| Good Axes | Bad Axes |
|-----------|----------|
| Simple ↔ Complex | Good ↔ Bad |
| SMB ↔ Enterprise | Cheap ↔ Expensive (too obvious) |
| Self-serve ↔ Sales-led | Old ↔ New |
| Specialized ↔ General | Small ↔ Large |

**Template:**

```
                    Enterprise
                        │
           Competitor C │  Competitor A
                ●       │       ●
                        │
  Simple ──────────────────────────── Complex
                        │
            You ●       │  Competitor B
                        │       ●
                        │
                      SMB
```

## Review Mining

### Where to Find Reviews

| Platform | Best For | URL Pattern |
|----------|----------|-------------|
| G2 | B2B SaaS | g2.com/products/[product]/reviews |
| Capterra | Business software | capterra.com/software/[id]/reviews |
| App Store | iOS apps | apps.apple.com |
| Google Play | Android apps | play.google.com |
| Product Hunt | Launches | producthunt.com/posts/[product] |
| Reddit | Honest opinions | reddit.com/r/[relevant-sub] |

### What to Extract

| Category | Look For |
|----------|---------|
| **Most praised** | What features do happy users mention most? |
| **Most complained** | What do unhappy users say? (= your opportunity) |
| **Switching reasons** | Why do users leave? What triggers switching? |
| **Feature requests** | What's missing that users want? |
| **Comparison mentions** | When users compare, what do they say? |

## Competitive Matrix

```markdown
| Dimension | Your Product | Competitor A | Competitor B | Competitor C |
|-----------|--------------|--------------|--------------|--------------|
| **Positioning** | Mid-market | Premium | Budget | Enterprise |
| **Target Customer** | SMBs | Enterprise | Startups | Large orgs |
| **Pricing Model** | Subscription | Annual | Freemium | Custom |
| **Entry Price** | $10/mo | $50/mo | Free | Contact |
| **Key Differentiator** | Ease of use | Integration depth | Price | Scalability |
| **Primary Weakness vs You** | N/A | Complex setup | Limited features | High cost |
| **Funding Stage** | Series A | Series C | Bootstrapped | Public |
| **Est. Company Size** | 25 | 500 | 10 | 5000 |
```

## SEO Considerations

### Keyword Targeting

| Format | Primary Keywords |
|--------|-----------------|
| Alternative (singular) | [Competitor] alternative, alternative to [Competitor] |
| Alternatives (plural) | [Competitor] alternatives, best [Competitor] alternatives |
| You vs Competitor | [You] vs [Competitor], [Competitor] vs [You] |
| Competitor vs Competitor | [A] vs [B], [B] vs [A] |

### Internal Linking
- Link between related competitor pages
- Link from feature pages to relevant comparisons
- Create hub page linking to all competitor content

### Schema Markup
Consider FAQ schema for questions like "What is the best alternative to [Competitor]?"

## Citation Requirements

**Inline citations are mandatory.** Every factual claim must include `[Source N](#Sources)` reference.

- Number sources sequentially
- Include exact URL in Sources section
- If information from multiple sources, cite all: `[Source 1, 3](#Sources)`
- For unverified claims, state: "Unable to verify from public sources"
- Prefer primary sources (company websites, press releases) over secondary (news, blogs)

## Deliverable Formats

### Executive Summary (1 page)

```markdown
## Competitive Landscape Summary

**Market:** [Category] — $[X]B market growing [Y]% annually

**Key competitors:** A (leader), B (challenger), C (niche)

**Our positioning:** [Where you sit and why it matters]

**Key insight:** [One sentence about biggest opportunity]

| Metric | You | A | B | C |
|--------|-----|---|---|---|
| Users | X | Y | Z | W |
| Pricing (starter) | $X | $Y | $Z | $W |
| Rating (G2) | X.X | Y.Y | Z.Z | W.W |
```

### Detailed Report (per competitor)

1. Company overview (size, funding, team)
2. Product analysis (features, UX screenshots)
3. Pricing breakdown
4. SWOT analysis
5. Review analysis (top praised, top complained)
6. Positioning vs. you
7. Opportunity summary

See [references/competitive-analysis-framework.md](references/competitive-analysis-framework.md) for complete report template.

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Only looking at features | Misses positioning, pricing, traction | Use 7-layer framework |
| Biased analysis | Loses credibility | Be honest about competitor strengths |
| Outdated data | Wrong conclusions | Date all research, refresh quarterly |
| Too many competitors | Analysis paralysis | Focus on top 3-5 direct competitors |
| No "so what" | Data without insight | End each section with implications |
| Feature-only comparison | Doesn't show positioning | Include pricing, reviews, positioning map |

## Quality Checklist

Before finalizing:

- [ ] Target Customer Profile completed with firmographics, pain points, behavioral patterns
- [ ] All competitors researched across all dimensions
- [ ] Every factual claim has inline citation
- [ ] Competitive matrix complete (use "N/A" or "Not disclosed" if needed)
- [ ] Market Gaps section identifies at least 3 specific gaps with evidence
- [ ] SWOT items are specific and evidence-based, not generic
- [ ] Recommendations are actionable and tied to findings
- [ ] Sources section includes all referenced URLs

## Error Handling

**If competitor website inaccessible:** Note in report, use available search results and news coverage.

**If pricing not public:** State "Pricing not publicly disclosed" and note indirect indicators (e.g., "enterprise sales model suggested by 'Contact Us' pricing page").

**If funding data unavailable:** Search for alternative signals: LinkedIn employee count, office locations, news mentions of growth.

**If fewer than 5 clear competitors exist:** Include available competitors and note market context (e.g., "Emerging market with limited direct competitors").

## Reference Files

- [references/competitive-analysis-framework.md](references/competitive-analysis-framework.md) - Complete report template with detailed sections
- [references/comparison-page-templates.md](references/comparison-page-templates.md) - SEO page templates for all 4 formats
- [references/content-architecture.md](references/content-architecture.md) - Centralized competitor data structure

## Best Practices

**DO:**
- Analyze current and emerging competitors
- Monitor competitor activities regularly
- Understand customer perception of competition
- Use competitive insights to inform strategy
- Focus on differentiation, not just comparison
- Include market trends in analysis
- Update competitive analysis quarterly
- Share insights across organization
- Use data to back up claims
- Consider indirect competitors

**DON'T:**
- Obsess over competitor pricing
- Copy competitor features blindly
- Ignore emerging threats
- Use only marketing materials for analysis
- Focus only on feature comparison
- Neglect customer feedback on competition
- Make analysis too complex
- Hide uncomfortable truths
- Change strategy based on every competitor move
- Ignore your competitive advantages
