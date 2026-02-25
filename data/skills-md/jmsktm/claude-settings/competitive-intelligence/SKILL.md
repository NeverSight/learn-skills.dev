---
name: Competitive Intelligence
slug: competitive-intelligence
description: Deep competitive research and monitoring using OSINT techniques and automated tracking
category: research
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "competitive intelligence"
  - "competitor research"
  - "analyze competitor"
  - "track competition"
tags:
  - competitive-analysis
  - osint
  - market-intelligence
  - competitor-tracking
---

# Competitive Intelligence

Expert OSINT (Open Source Intelligence) agent that conducts deep competitive research, monitors competitor activities, and provides strategic intelligence. Specializes in product analysis, pricing intelligence, marketing strategy reverse-engineering, and early warning systems for competitive threats.

This skill uses advanced web scraping, change detection, and data synthesis to build comprehensive competitive profiles and maintain ongoing intelligence. Essential for product strategy, sales enablement, and strategic planning.

## Core Workflows

### Workflow 1: Deep Competitor Profile

**Objective:** Build a comprehensive intelligence dossier on a specific competitor

**Steps:**
1. **Company Intelligence**
   - Corporate structure and ownership
   - Funding history and investors (Crunchbase, PitchBook)
   - Leadership team and key hires (LinkedIn, company site)
   - Office locations and headcount
   - Use Firecrawl to scrape company about pages, press releases

2. **Product Intelligence**
   - Product portfolio and features
   - Pricing and packaging
   - Technology stack (BuiltWith, Wappalyzer)
   - Product roadmap signals (job postings, patents, press)
   - Use Firecrawl to extract from product pages, documentation

3. **Customer Intelligence**
   - Target customer segments
   - Customer case studies and testimonials
   - Customer reviews (G2, Capterra, TrustRadius)
   - Win/loss patterns
   - NPS and satisfaction scores

4. **Marketing Intelligence**
   - Positioning and messaging
   - Marketing channels and spend (SimilarWeb, SEMrush approach)
   - Content strategy and themes
   - SEO strategy and rankings
   - Social media presence and engagement
   - Use Firecrawl to analyze blog, social profiles, ad copy

5. **Sales Intelligence**
   - Sales methodology and process
   - Pricing and discounting patterns
   - Sales team size and territories
   - Partnerships and channel strategy
   - Contract terms and SLAs

6. **Financial Intelligence**
   - Revenue (public companies: SEC filings; private: estimates)
   - Profitability and burn rate
   - Valuation and multiples
   - Growth rate and trajectory

**Deliverable:** 360° competitor profile with SWOT analysis and strategic recommendations

### Workflow 2: Product Feature Comparison

**Objective:** Create detailed feature parity analysis across competitors

**Steps:**
1. **Feature Discovery**
   - Scrape product pages, documentation, and help centers
   - Review product tours and demos
   - Analyze user reviews for feature mentions
   - Test free trials or freemium versions
   - Use Firecrawl to extract feature lists systematically

2. **Categorize Features**
   - Core features (table stakes)
   - Advanced features (differentiators)
   - Nice-to-have features
   - Unique features (only 1 competitor has)

3. **Build Comparison Matrix**
   - Binary (has/doesn't have)
   - Quality rating (1-5 scale based on reviews)
   - Maturity assessment (beta, GA, mature, legacy)
   - Pricing tier where available

4. **Gap Analysis**
   - Features you have that competitors don't (advantages)
   - Features competitors have that you don't (gaps)
   - Features no one has yet (opportunities)

5. **Roadmap Implications**
   - Must-have features for parity
   - Differentiation opportunities
   - Low-ROI features to avoid

**Deliverable:** Feature comparison spreadsheet with strategic gap analysis

### Workflow 3: Pricing Intelligence

**Objective:** Reverse-engineer competitor pricing strategies and positioning

**Steps:**
1. **Extract Published Pricing**
   - Use Firecrawl to scrape pricing pages
   - Identify all tiers and packaging
   - Calculate price per feature/user/unit
   - Document discounts and promotional pricing

2. **Uncover Hidden Pricing**
   - Quote requests and sales conversations
   - Reviews mentioning pricing
   - Job postings mentioning quotas/ACV
   - Conference presentations and case studies
   - SEC filings for public companies

3. **Analyze Pricing Strategy**
   - Pricing model (per user, per feature, usage-based, etc.)
   - Price anchoring and tiering
   - Freemium vs. free trial strategy
   - Contract terms (monthly, annual, multi-year)
   - Discounting patterns (annual prepay, volume, nonprofit, etc.)

4. **Positioning Analysis**
   - Premium, mid-market, or budget positioning
   - Value metric alignment
   - Price elasticity signals
   - Competitive price gaps

5. **Track Pricing Changes**
   - Set up monitoring for pricing page changes
   - Document historical pricing (Wayback Machine)
   - Identify pricing trends and patterns

**Deliverable:** Pricing intelligence report with strategic recommendations

### Workflow 4: Marketing Strategy Analysis

**Objective:** Reverse-engineer competitor marketing and GTM strategies

**Steps:**
1. **Channel Analysis**
   - Organic search (SEO keywords, rankings)
   - Paid search (ad copy, keywords)
   - Social media (platforms, frequency, engagement)
   - Content marketing (blog, videos, podcasts)
   - Email marketing (sign up for lists, analyze cadence)
   - Events and webinars
   - Use WebSearch and Firecrawl to gather channel data

2. **Messaging Analysis**
   - Value proposition and positioning
   - Target personas and use cases
   - Key messaging pillars
   - Competitive differentiation claims
   - Analyze website, ads, sales decks, case studies

3. **Content Strategy**
   - Content types and formats
   - Publishing frequency
   - Topic clusters and themes
   - Content quality and depth
   - Use Firecrawl to catalog all content assets

4. **Campaign Analysis**
   - Recent launches and campaigns
   - Seasonal patterns
   - Campaign themes and creative
   - Estimated spend and reach

5. **Partnership & Ecosystem**
   - Technology partnerships
   - Reseller/channel partnerships
   - Integration ecosystem
   - Co-marketing activities

**Deliverable:** Marketing intelligence report with channel breakdown and messaging analysis

### Workflow 5: Competitive Monitoring & Alerts

**Objective:** Set up ongoing competitive intelligence gathering

**Steps:**
1. **Define Monitoring Scope**
   - Key competitors to track (3-7 companies)
   - Critical intelligence areas (product, pricing, hiring, funding)
   - Update frequency (daily, weekly, monthly)

2. **Set Up Data Sources**
   - RSS feeds for company blogs
   - Google Alerts for news mentions
   - Social media monitoring (LinkedIn, Twitter)
   - Review site monitoring (G2, Capterra)
   - Job posting tracking (LinkedIn, Glassdoor)
   - Website change detection (Visualping approach)
   - SEC filings for public companies

3. **Create Alert Rules**
   - Pricing changes
   - Product launches
   - Executive changes
   - Funding announcements
   - Partnership announcements
   - Significant customer wins

4. **Intelligence Synthesis**
   - Weekly digest of competitive activity
   - Monthly competitive landscape update
   - Quarterly strategic intelligence report

5. **Distribution & Enablement**
   - Sales team competitive battlecards
   - Product team feature gap updates
   - Executive team strategic briefings

**Deliverable:** Automated competitive monitoring system with regular intelligence reports

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Full competitor profile | "Research [competitor name] comprehensively" |
| Feature comparison | "Compare features of [product] vs [competitors]" |
| Pricing analysis | "Analyze pricing strategy of [competitor]" |
| Marketing analysis | "Reverse-engineer [competitor] marketing" |
| Set up monitoring | "Monitor [competitor] for changes" |
| Quick SWOT | "Generate SWOT for [competitor]" |

## OSINT Sources & Techniques

### Company Intelligence Sources
- **Crunchbase:** Funding, investors, leadership, acquisitions
- **PitchBook:** Private company financials and metrics
- **LinkedIn:** Employee count, hiring trends, key personnel
- **AngelList:** Startup profiles, jobs, investors
- **BuiltWith:** Technology stack and tools
- **SimilarWeb:** Traffic, sources, engagement metrics

### Product Intelligence Sources
- **Product Pages:** Use Firecrawl for systematic extraction
- **Documentation:** API docs, help centers, knowledge bases
- **Product Hunt:** Launch data, reviews, community reception
- **G2/Capterra/TrustRadius:** User reviews and ratings
- **App Stores:** Mobile app reviews and ratings
- **GitHub:** Open source projects, activity, technology choices

### Marketing Intelligence Sources
- **SEMrush/Ahrefs Approach:** Organic and paid keyword analysis
- **Wayback Machine:** Historical website/pricing analysis
- **Email Newsletters:** Sign up for all marketing communications
- **Social Media:** LinkedIn, Twitter, Facebook, Instagram presence
- **YouTube:** Video content, webinars, demos
- **Podcasts:** Guest appearances, owned podcasts

### Sales Intelligence Sources
- **Glassdoor:** Sales compensation, team reviews, interview questions
- **LinkedIn Sales Navigator Approach:** Sales team mapping
- **Public RFPs:** Government contracts, enterprise requirements
- **Case Studies:** Customer profiles, use cases, results
- **Press Releases:** Partnership and customer announcements

## Best Practices

- **Ethical boundaries:** Only use publicly available information; never use deception or unauthorized access
- **Verify information:** Cross-reference across multiple sources
- **Track confidence levels:** Note when information is confirmed vs. inferred
- **Date all intelligence:** Market conditions change; context matters
- **Respect privacy:** Focus on corporate intelligence, not personal information
- **Document sources:** Always cite where information came from
- **Update regularly:** Competitive landscapes evolve; refresh intelligence quarterly
- **Focus on actionable insights:** Every data point should inform strategy
- **Avoid analysis paralysis:** Perfect intelligence is impossible; act on good-enough data
- **Maintain objectivity:** Acknowledge competitor strengths; don't just focus on weaknesses

## Competitive Battlecard Format

```markdown
# Competitive Battlecard: [Competitor Name]

**Last Updated:** [Date]

## Quick Facts
- **Founded:** [Year]
- **Funding:** $XX million (Series X)
- **Employees:** ~XXX
- **Customers:** ~X,XXX
- **Positioning:** [One sentence]

## When You'll Compete
- [Target segment/use case overlap]

## Their Strengths (Be Honest)
- Strength 1 with evidence
- Strength 2 with evidence

## Their Weaknesses (Our Advantages)
- Weakness 1 → How we're better
- Weakness 2 → How we're better

## Pricing Comparison
| Tier | Their Price | Our Price | Value Gap |
|------|-------------|-----------|-----------|
| ... | ... | ... | ... |

## Key Differentiators (Why We Win)
1. Differentiator 1 with proof point
2. Differentiator 2 with proof point

## Landmine Questions (Ask Prospects)
- Question designed to expose their weakness 1
- Question designed to expose their weakness 2

## If We're Losing...
- Common objections and how to handle them
- When to walk away vs. fight harder

## Recent News & Updates
- [Date]: Notable event or change
```

## Integration with Other Skills

- **Use with `market-research-analyst`:** Context for competitive positioning
- **Use with `seo-analyst`:** Track competitor SEO performance
- **Use with `financial-analyst`:** Model competitive financial performance
- **Use with `trend-spotter`:** Identify competitor response to trends
- **Use with `user-research`:** Validate competitive claims with customers

## Red Flags & Warning Signs

Monitor for these signals of competitive threats:

- **Product Signals:**
  - Aggressive hiring in specific functions (engineering, sales)
  - Patent filings in your space
  - Technology stack changes (scaling infrastructure)
  - Job postings mentioning features you're building

- **Market Signals:**
  - Major funding round closed
  - New executive hires (especially from competitors or big tech)
  - Geographic expansion announcements
  - Rebranding or repositioning

- **Customer Signals:**
  - Increased win rate against you
  - Customers mentioning competitive features
  - Review sentiment changes
  - Unusual customer churn patterns

## Analysis Frameworks

### SWOT Analysis Template
**Strengths:** Internal advantages (product, team, technology, brand)
**Weaknesses:** Internal disadvantages (gaps, resource constraints)
**Opportunities:** External favorable conditions (trends, market gaps)
**Threats:** External challenges (new entrants, substitutes, regulations)

### Porter's Five Forces
- **Threat of New Entrants:** Barriers to entry, capital requirements
- **Bargaining Power of Suppliers:** Dependency on key inputs
- **Bargaining Power of Buyers:** Customer concentration, switching costs
- **Threat of Substitutes:** Alternative solutions to customer needs
- **Competitive Rivalry:** Number and strength of competitors

### Feature Priority Matrix
Plot competitor features on 2x2 matrix:
- **X-axis:** Implementation Difficulty (Low → High)
- **Y-axis:** Customer Value (Low → High)
- **Quadrants:** Quick wins, Strategic, Fill-ins, Avoid
