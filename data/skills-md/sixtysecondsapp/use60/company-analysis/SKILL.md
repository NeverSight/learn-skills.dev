---
name: Company Analysis
description: |
  Deep company analysis covering funding, tech stack, hiring, news, and competitive landscape.
  Use when a user asks "analyze this company", "company deep dive", "tell me about [company]'s business",
  "company intel", or needs comprehensive business intelligence on a target account.
  Returns structured analysis with business model, financials, technology, and growth assessment.
metadata:
  author: sixty-ai
  version: "2"
  category: enrichment
  skill_type: atomic
  is_active: true
  context_profile: research
  agent_affinity:
    - research
    - pipeline
  triggers:
    - pattern: "analyze this company"
      intent: "company_analysis"
      confidence: 0.90
      examples:
        - "analyze this account"
        - "deep analysis of this company"
        - "company analysis for"
    - pattern: "company deep dive"
      intent: "company_deep_dive"
      confidence: 0.90
      examples:
        - "deep dive on this company"
        - "do a deep dive on"
        - "full company breakdown"
    - pattern: "tell me about their business"
      intent: "company_intel"
      confidence: 0.80
      examples:
        - "what does this company do"
        - "tell me about their products"
        - "how does this company make money"
    - pattern: "company intel"
      intent: "company_intelligence"
      confidence: 0.85
      examples:
        - "get intel on this company"
        - "company intelligence report"
        - "account intelligence"
  keywords:
    - "company"
    - "analysis"
    - "deep dive"
    - "intel"
    - "business model"
    - "funding"
    - "tech stack"
    - "account"
    - "research"
  required_context:
    - company_name
  inputs:
    - name: company_name
      type: string
      description: "Name of the company to analyze"
      required: true
    - name: company_website
      type: string
      description: "Company website URL to speed up research"
      required: false
    - name: industry
      type: string
      description: "Industry context to focus the research"
      required: false
  outputs:
    - name: business_overview
      type: object
      description: "Company fundamentals with name, description, business model, products, target market, and leadership"
    - name: financials
      type: object
      description: "Financial intelligence with funding, valuation, revenue signals, and financial health"
    - name: technology
      type: object
      description: "Technology landscape with tech stack, engineering culture, and integration ecosystem"
    - name: market_position
      type: object
      description: "Competitive context with market segment, key competitors, and differentiators"
    - name: growth_assessment
      type: object
      description: "Growth trajectory with evidence, hiring trends, milestones, and risks"
    - name: news_timeline
      type: array
      description: "5-8 recent news items with date, title, source, summary, and significance"
  requires_capabilities:
    - web_search
  priority: high
  tags:
    - enrichment
    - company
    - analysis
    - account-intel
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Company Analysis

## What Separates Analysis from Research

Research collects data. Analysis produces insight. The difference matters.

A research report tells you: "Acme Corp raised $50M Series C in January, has 350 employees, uses React and Python, and recently launched a self-serve tier."

An analysis tells you: "Acme Corp's $50M Series C and simultaneous launch of self-serve pricing signals a strategic shift from enterprise-only to PLG. Their 40% YoY headcount growth is concentrated in engineering (25 open roles) and product (8 open roles), with only 2 sales hires -- confirming the PLG bet. This means their sales team is likely stretched thin managing enterprise accounts while the product team builds the self-serve engine. Entry point: the VP of Sales is probably feeling the pain of scaling without proportional headcount. Position ${company_name} as the tool that lets a lean sales team do more."

Your job is to produce the second kind of output. Every data point should be connected to an insight. Every insight should be connected to a sales implication. The rep who reads your analysis should walk away knowing not just WHAT this company does, but HOW to sell to them.

## Goal

Produce a comprehensive company analysis that equips the sales rep with deep account intelligence for strategic engagement. The output should be structured for scanability but rich enough to inform account strategy, not just first-touch outreach.

## Required Capabilities
- **Web Search**: To research company information across the web (routed to Gemini with Google Search grounding)

## Inputs
- `company_name`: Name of the company to analyze (required)
- `company_website`: Company website URL (if known, speeds up research significantly)
- `industry`: Industry context (if known, helps focus research on the right company and relevant metrics)
- `organization_id`: Current organization context

## Analysis Methodology

### Phase 1: Discovery (Run Searches in Parallel)

Execute these searches simultaneously:

1. `"[Company Name]" company about` -- official site, Wikipedia, Crunchbase
2. `"[Company Name]" product OR platform OR pricing` -- what they sell and how
3. `"[Company Name]" funding OR investors OR Crunchbase OR valuation` -- financial context
4. `"[Company Name]" news OR announcement OR launch 2025 OR 2026` -- recent activity
5. `"[Company Name]" competitors OR alternative OR "compared to"` -- competitive landscape
6. `"[Company Name]" careers OR hiring OR jobs` -- growth signals and tech stack
7. `"[Company Name]" review G2 OR Capterra OR Trustpilot` -- market reputation

If a domain is known:
8. `site:[domain.com] blog OR engineering OR about` -- first-party content
9. `"[Company Name]" "companies house" OR "SEC filing" OR revenue` -- financial records

### Phase 2: Deep Dive (Fetch and Analyze Key Pages)

Based on Phase 1 results, fetch the most valuable pages:
- Company About page, Product page, Pricing page
- Crunchbase or PitchBook profile
- Recent blog posts and press releases (last 6 months)
- Engineering blog (if it exists)
- Careers page (current job listings)
- G2 or Capterra profile
- LinkedIn company page

### Phase 3: Synthesis and Insight Generation

This is where analysis diverges from research. For each data section, follow this pattern:
1. **State the fact** with a source
2. **Interpret the fact** -- what does it mean?
3. **Connect to sales implication** -- why does this matter for selling to them?

## Business Model Analysis Framework

Understanding how a company makes money is the foundation of all other analysis. Without this, everything else is context without purpose. Consult `references/analysis-frameworks.md` for the complete framework library including Porter's Five Forces (sales-adapted), SWOT templates, Business Model Canvas extraction, competitive moat assessment, and growth trajectory scoring with worked examples.

### Revenue Model Identification

Determine which model(s) the company uses:

| Model | Indicators | Sales Implication |
|-------|-----------|-------------------|
| **SaaS (subscription)** | Monthly/annual pricing page, per-seat or per-usage pricing | Predictable budget cycles. Likely evaluates tools annually. |
| **Usage-based** | Pay-as-you-go language, API pricing, metered billing | Budget scales with growth. May be cost-sensitive per unit. |
| **Marketplace/platform** | Two-sided value prop, take rate, GMV references | Revenue depends on participant volume. Growth = more complexity. |
| **Services/consulting** | Time-based pricing, project pricing, SOW references | Budget tied to project cycles. Longer sales cycles. |
| **Freemium/PLG** | Free tier, self-serve signup, product-led language | Bottom-up adoption. Champion may be a user, not a buyer. |
| **Enterprise license** | "Contact sales", custom pricing, negotiated contracts | Top-down sales. Budget controlled by procurement. |
| **Hardware + software** | Physical product + subscription, device + cloud | Longer evaluation cycles. Multiple stakeholders. |

### Unit Economics Signals

You rarely get exact numbers, but you can triangulate:
- **Revenue per employee**: If you know revenue and employee count, divide. SaaS companies typically generate $150K-300K revenue per employee. Below $100K suggests early stage or low efficiency. Above $400K suggests high efficiency or enterprise pricing.
- **Funding-to-employee ratio**: Total funding / employee count. If they've raised $100M and have 50 employees, they're either burning slow (good) or very early (spending on product). If they've raised $20M and have 500 employees, they may be revenue-funded (strong signal).
- **Pricing tier range**: If pricing page shows $50-500/month, they sell mid-market. If pricing page says "Contact sales," they sell enterprise. If pricing shows $0-20/month, they sell SMB with volume.

### Moat Assessment

What protects this company from competition? This matters because moated companies are more stable customers (lower churn risk) and more confident buyers (less likely to penny-pinch on tools).

- **Network effects**: More users = more value (marketplaces, collaboration tools, social platforms)
- **Switching costs**: Hard to leave once adopted (deeply integrated tools, data lock-in, workflow dependencies)
- **Data advantages**: Proprietary data that improves with usage (ML companies, analytics platforms)
- **Brand/trust**: Established reputation in a trust-sensitive category (security, compliance, finance)
- **Regulatory**: Certifications or compliance that are expensive to obtain (SOC2, HIPAA, FedRAMP)
- **Scale**: Cost advantages from volume (infrastructure, logistics, manufacturing)

## Financial Health Assessment

Go beyond "they raised $X" to assess the company's actual financial position. See `references/financial-indicators.md` for the complete financial health indicator guide, including funding round significance, revenue inference methods, burn rate estimation, public company metrics (gross margin, NRR, Rule of 40), and warning sign detection.

### Funding Analysis

| Signal | Interpretation |
|--------|---------------|
| Recent funding (<6 months) | Fresh capital, active hiring, tool evaluation window open |
| No funding in 2+ years | Either profitable (good) or struggling to raise (concerning). Check other signals. |
| Down round (lower valuation than prior round) | Stress signal. May be tightening budgets. |
| Bridge round / extension | Between major rounds. Moderate concern -- runway may be limited. |
| Multiple rounds from same investors | Strong investor conviction. Positive signal. |
| Strategic investors (not just VCs) | Industry validation. May have specific strategic direction. |
| Debt financing | May indicate profitable operations leveraging debt, or equity-averse founders. |

### Revenue Signal Detection

Since most private companies don't share revenue, look for proxies:
- **"Revenue milestone" press releases**: Companies announce when they hit $10M, $50M, $100M ARR.
- **Award rankings**: Inc 5000, Deloitte Fast 500, SaaS Mag rankings often include revenue ranges.
- **G2/Capterra review volume**: Rough proxy for customer count. 100+ reviews = likely 500+ customers.
- **LinkedIn headcount + industry benchmarks**: Employee count x industry-average revenue-per-employee = rough revenue estimate.
- **Pricing page + estimated customer count**: If you know the price range and can estimate customer count, you can estimate revenue.

### Burn Rate and Runway Estimation

For venture-backed companies:
- Total funding raised - estimated revenue = approximate total capital consumed
- Recent funding amount / estimated monthly burn = rough runway estimate
- Headcount x average fully-loaded cost ($150K-200K/yr in tech) = estimated annual burn
- If burn appears to exceed revenue significantly and last raise was 18+ months ago, there may be funding pressure

### Financial Health Rating

Based on all signals, assign one of:
- **Strong**: Profitable or recently well-funded with clear runway. Confident buyer.
- **Stable**: Adequate funding/revenue, no distress signals. Normal buyer.
- **Cautious**: Some concerning signals (old fundraise, layoff mentions, down round). May be budget-constrained.
- **Concerning**: Multiple negative signals (layoffs + no recent funding + shrinking). High risk of deal stalling.
- **Unknown**: Insufficient data to assess. Note what data would resolve this.

## Technology Landscape Analysis

Tech stack analysis tells you about the company's sophistication, spending patterns, and potential integration needs.

### Stack Assessment

Organize discovered technologies into layers:

```
TECHNOLOGY STACK
+-- Infrastructure
|   +-- Cloud (AWS / GCP / Azure / hybrid)
|   +-- CDN (Cloudflare, Fastly, Akamai)
|   +-- Monitoring (Datadog, New Relic, Grafana)
+-- Development
|   +-- Languages (Python, TypeScript, Go, Java, etc.)
|   +-- Frameworks (React, Next.js, Django, Rails, etc.)
|   +-- CI/CD (GitHub Actions, CircleCI, Jenkins)
+-- Data
|   +-- Databases (PostgreSQL, MongoDB, Redis)
|   +-- Analytics (Snowflake, BigQuery, Databricks)
|   +-- BI (Looker, Tableau, Metabase)
+-- Business Applications
|   +-- CRM (Salesforce, HubSpot, Pipedrive)
|   +-- Marketing (HubSpot, Marketo, Mailchimp)
|   +-- Sales (Outreach, Apollo, Salesloft)
|   +-- CS (Zendesk, Intercom, Freshdesk)
+-- Security & Compliance
    +-- Auth (Okta, Auth0, custom)
    +-- Security (CrowdStrike, SentinelOne)
    +-- Compliance (Vanta, Drata, Secureframe)
```

### Technical Debt Signals

Look for signs of technical debt that might create buying triggers:
- Job postings mentioning "migration," "modernization," "legacy system replacement"
- Engineering blog posts about scaling challenges
- Multiple tools serving the same function (indicates organic growth without consolidation)
- Very old tech stack components alongside modern ones (suggests partial migration)

### Innovation Pace

Assess how quickly the company adopts new technology:
- **Fast movers**: Latest framework versions in job postings, engineering blog about cutting-edge topics, AI/ML experimentation
- **Steady adopters**: Mainstream, well-established tech choices, occasional upgrades
- **Conservative**: Older, proven technologies, emphasis on stability over innovation
- This affects the sales approach: fast movers are easier to sell new categories to; conservative orgs need more proof and social proof.

## Growth Trajectory Assessment

Growth trajectory tells you about timing, budget, and urgency.

### Leading Indicators (predict future growth)
- **Hiring velocity**: Number of open roles relative to company size. >5% of headcount in open roles = aggressive growth.
- **New market entry**: Launching in new geographies or verticals.
- **Product expansion**: New product lines, new pricing tiers, new integrations.
- **New leadership hires**: Senior executives in growth functions (VP Sales, VP Marketing, CRO).
- **Funding recency**: Capital raised within the last 12 months.

### Lagging Indicators (confirm past growth)
- **Employee count growth**: LinkedIn historical headcount (available on some profiles). >30% YoY = rapid growth.
- **Revenue milestones**: Public announcements of ARR milestones.
- **Customer count growth**: G2 review velocity, case study volume.
- **Office expansion**: New locations, larger headquarters.

### Growth Trajectory Rating

- **Rapid Growth**: Multiple leading indicators firing. 30%+ headcount growth. Recent funding. Aggressive hiring. These companies are the best prospects -- they have budget, urgency, and willingness to buy tools.
- **Steady Growth**: Moderate hiring, some expansion, stable fundamentals. Good prospects with normal sales cycles.
- **Stable/Mature**: Minimal hiring, no recent funding needed, established market position. Longer sales cycles but potentially larger deals. May be replacing existing tools rather than buying new category.
- **Declining**: Layoffs, office closures, leadership departures, no recent positive news. Proceed with caution. May be poor timing.
- **Unknown**: Insufficient data. Note what signals would resolve this.

## Competitive Positioning Analysis

Understanding where the company sits in its competitive landscape helps you sell to them more effectively.

### Market Map Construction

Identify:
1. **Direct competitors**: Companies selling the same thing to the same buyers
2. **Adjacent competitors**: Companies solving adjacent problems that could expand into this space
3. **Upstream/downstream players**: Companies in the value chain that may integrate or compete

### Market Share Signals

Exact market share data is rare for private companies. Use proxies:
- G2/Capterra grid position (Leader, Contender, Niche, High Performer)
- Review volume relative to competitors
- LinkedIn employee count relative to competitors
- Media mention volume relative to competitors
- Job posting volume relative to competitors

### Differentiation Depth

Assess how strongly differentiated the company is:
- **Strong differentiation**: Unique technology, unique approach, loyal customer base, clear "why us" story
- **Moderate differentiation**: Some unique elements but largely comparable to competitors
- **Weak differentiation**: Commodity market, competing primarily on price or distribution
- This matters because strongly differentiated companies are more confident and less price-sensitive as buyers.

## News Timeline Significance Analysis

Not all news is equally significant. For each news item, assess its sales relevance:

### Significance Levels

- **Critical** (directly creates a buying trigger):
  - New CEO/CTO/CRO hired
  - Major funding round
  - Acquisition (acquired or acquiring)
  - Product pivot
  - Major security incident or compliance requirement

- **High** (meaningful context for sales engagement):
  - New product launch
  - Major partnership or integration
  - Expansion to new market
  - Significant customer win
  - Layoffs or restructuring

- **Medium** (useful background):
  - Industry awards
  - Conference sponsorship
  - Minor product updates
  - Team growth milestones

- **Low** (skip unless nothing else is available):
  - Generic PR
  - Social media posts
  - Routine blog content

Only include Critical and High significance items in the news timeline. Medium can be included if fewer than 5 items are available. Low should never be included.

## Entry Point Identification

The most strategically valuable part of a company analysis is identifying WHERE in the organization to start a conversation.

### Ideal Entry Point Characteristics
1. **Pain proximity**: They personally feel the problem that ${company_name}'s product solves
2. **Budget influence**: They can either approve spending or champion it to someone who can
3. **Accessibility**: They're reachable (not behind layers of gatekeepers)
4. **Openness**: Something has recently changed that makes them receptive (new role, new mandate, new challenge)

### Entry Point Strategy by Company Size

| Company Size | Best Entry Point | Why |
|-------------|-----------------|-----|
| 1-50 employees | CEO/Founder or Head of relevant function | Everyone is accessible. Decisions are fast. |
| 50-200 employees | VP or Director of relevant function | Enough org structure for delegation, small enough for direct access. |
| 200-1000 employees | Director or Senior Manager + VP sponsor | Mid-level feels the pain daily; VP controls budget. Need both. |
| 1000+ employees | Multiple stakeholders, start with champion | Enterprise sales requires committee buy-in. Find the internal advocate first. |

### Identifying the Champion

Look for someone who:
- Recently posted about the problem space on LinkedIn
- Recently changed into a role where ${company_name}'s product is relevant
- Has a title that suggests they own the function ${company_name}'s product serves
- Has a history of adopting similar tools at previous companies (check career history)

## ICP Fit Assessment

If ICP criteria are available in the Organization Context above, explicitly map the analyzed company against each ICP dimension:

| ICP Dimension | This Company | Fit |
|--------------|-------------|-----|
| Industry | [Their industry] | Match / Partial / Mismatch |
| Company size | [Their size] | Match / Partial / Mismatch |
| Revenue range | [Estimated revenue] | Match / Partial / Mismatch |
| Geography | [Their location] | Match / Partial / Mismatch |
| Tech stack | [Relevant technologies] | Match / Partial / Mismatch |
| Growth stage | [Their stage] | Match / Partial / Mismatch |

If ICP criteria are not available in the Organization Context, still provide the raw data points so the rep can make their own assessment.

## Output Contract

Return a SkillResult with:
- `data.business_overview`: Company fundamentals with:
  - `company_name`: Official name
  - `website`: URL
  - `description`: 2-3 sentence company description
  - `business_model`: How they make money, with model type identified
  - `unit_economics_signals`: Any estimated metrics (revenue per employee, funding efficiency)
  - `moat`: Identified competitive moat(s) with evidence
  - `products`: Array of main products/services with brief descriptions and target customer
  - `target_market`: Who they sell to (segments, verticals, company sizes)
  - `headquarters`: Location
  - `founded`: Year founded
  - `employee_count`: Estimated headcount or range (with source and date)
  - `leadership`: Array of key executives (name, title, tenure, notable background)
- `data.financials`: Financial intelligence with:
  - `funding_total`: Total funding raised
  - `latest_round`: Most recent funding round (type, amount, date)
  - `investors`: Notable investors with any relevant context
  - `valuation`: Last known valuation (if available)
  - `revenue_signals`: Any public revenue data, estimates, or proxy indicators
  - `burn_rate_estimate`: Rough estimate if calculable
  - `financial_health`: "strong" | "stable" | "cautious" | "concerning" | "unknown" with detailed reasoning
- `data.technology`: Technology landscape with:
  - `tech_stack`: Known technologies organized by layer (infrastructure, development, data, business apps, security)
  - `engineering_culture`: Insights from engineering blog, job postings, or tech talks
  - `infrastructure`: Cloud provider, key platforms
  - `integration_ecosystem`: Key integrations and partners
  - `technical_debt_signals`: Any signs of legacy systems, migrations, or modernization needs
  - `innovation_pace`: "fast_mover" | "steady_adopter" | "conservative" with evidence
- `data.market_position`: Competitive context with:
  - `market_segment`: Primary market category
  - `key_competitors`: Array of 3-5 main competitors with relative positioning
  - `differentiators`: What makes them unique (with differentiation strength rating)
  - `market_share_signals`: Any available market position data or proxies
  - `competitive_dynamics`: Key competitive tensions or opportunities
- `data.growth_assessment`: Growth trajectory with:
  - `trajectory`: "rapid_growth" | "steady_growth" | "stable" | "declining" | "unknown"
  - `leading_indicators`: Array of forward-looking growth signals
  - `lagging_indicators`: Array of confirmed growth evidence
  - `hiring_trends`: What roles they're hiring for and what it signals (not just a list of roles)
  - `recent_milestones`: Major achievements or announcements
  - `risks`: Potential concerns or challenges
- `data.entry_points`: Recommended entry points with:
  - `primary`: Best person/role to approach (with reasoning)
  - `secondary`: Backup entry point
  - `champion_profile`: Description of the ideal internal champion for ${company_name}'s product
  - `approach_angle`: How to frame the outreach based on the analysis
- `data.icp_fit`: ICP fit assessment (if ICP criteria available in Organization Context) with dimension-by-dimension mapping
- `data.news_timeline`: Array of 5-8 recent news items (Critical and High significance only) with:
  - `date`: Publication date
  - `title`: Headline
  - `source`: Publication
  - `summary`: One-sentence summary
  - `significance`: "critical" | "high" | "medium"
  - `sales_implication`: Why this matters for selling to them (not just what happened)
  - `url`: Link to article
- `references`: Array of all source URLs used

## Quality Checklist

Before returning the analysis, verify:

- [ ] Every section includes insight, not just data (the "so what?" for each finding)
- [ ] Business model is identified with revenue model type
- [ ] Financial health has a clear rating with reasoning
- [ ] Growth trajectory has a clear rating with evidence
- [ ] At least 3 competitors are identified with relative positioning
- [ ] Entry points are specific (actual roles/names, not just "talk to leadership")
- [ ] News items include sales implications, not just summaries
- [ ] Tech stack is organized by layer, not just a flat list
- [ ] Hiring signals are interpreted (what they mean, not just what the postings say)
- [ ] ICP fit is assessed if criteria are available
- [ ] All data points have cited sources
- [ ] Data freshness is noted for time-sensitive fields
- [ ] Gaps are explicitly called out
- [ ] The analysis is scannable -- key findings in the first paragraph, details below

## Error Handling

### Company name is ambiguous
Multiple companies with the same name is common. Use additional context:
1. If `company_website` or `industry` is provided, use those to disambiguate
2. If not, search for `"[Company Name]" [any contextual clues from the conversation]`
3. If still ambiguous, present the top 2-3 matches with distinguishing details and ask: "I found multiple companies named [Name]. Which one? [Company A - SaaS in Austin, TX, 200 employees] or [Company B - consulting firm in London, 50 employees]?"

### Company is very private or early-stage
Limited data is expected for early-stage companies. Adjust approach:
- Lean on founder LinkedIn profiles, AngelList, Product Hunt
- Check for accelerator/incubator participation (Y Combinator, Techstars)
- Look for demo day presentations, pitch videos, or launch blog posts
- Honestly note: "Limited public data available. This analysis is based on [X sources]. Key gaps: [list]. Recommend direct discovery call to fill in financial and technology details."

### Company is very large (Fortune 500+)
Too much data is the problem, not too little. Focus:
- Latest 12 months only (skip deep history)
- Most relevant business unit or division (if ${company_name}'s product only applies to a segment)
- Most recent strategic initiatives and leadership changes
- Tailor to the specific stakeholder the rep is targeting, if known

### Web search returns conflicting information
Present the most recent and most credible source as primary. Note the conflict:
- "Employee count varies by source: LinkedIn shows ~2,000, Crunchbase shows 1,500 (updated 6 months ago). Using LinkedIn figure as primary."
- For critical conflicts (e.g., different business models described), present both and note which seems more current.

### ${company_name} product information not available
If Organization Context is not available, note this and skip the ICP fit assessment and competitive comparison against ${company_name}'s product. Focus on the target company's analysis standalone. Note: "ICP fit assessment skipped -- organization product context not available."

### Always return at least business_overview
Even if other sections have limited data, always return `business_overview` with whatever is available. A partial analysis with honest gaps is better than nothing. The rep needs something to work with.
