---
name: Lead Research
description: |
  Research a lead or company using web search to find key business intelligence.
  Use when a user asks "research this lead", "look up this company", "find out about [company]",
  "what can you tell me about [person]", or needs enrichment data before outreach.
  Returns structured contact enrichment data with LinkedIn, company details, news, and tech stack.
metadata:
  author: sixty-ai
  version: "2"
  category: enrichment
  skill_type: atomic
  is_active: true
  context_profile: research
  agent_affinity:
    - research
    - prospecting
  triggers:
    - pattern: "research this lead"
      intent: "lead_research"
      confidence: 0.90
      examples:
        - "research this person"
        - "look into this lead"
        - "find info on this lead"
    - pattern: "look up this company"
      intent: "company_lookup"
      confidence: 0.85
      examples:
        - "look up this person"
        - "search for this company"
        - "find this company online"
    - pattern: "what can you tell me about"
      intent: "lead_intel"
      confidence: 0.80
      examples:
        - "what do we know about this person"
        - "find out about this company"
        - "dig up info on this prospect"
    - pattern: "enrich this contact"
      intent: "contact_enrichment"
      confidence: 0.85
      examples:
        - "enrich this lead"
        - "get more data on this contact"
        - "fill in the blanks on this prospect"
  keywords:
    - "research"
    - "lead"
    - "lookup"
    - "enrich"
    - "prospect"
    - "company"
    - "background"
    - "intel"
    - "find"
    - "search"
  required_context:
    - lead_name
    - company_name
  inputs:
    - name: lead_name
      type: string
      description: "Name of the person to research"
      required: false
    - name: company_name
      type: string
      description: "Name of the company to research"
      required: false
    - name: email
      type: string
      description: "Email address of the lead for finding LinkedIn and professional profiles"
      required: false
  outputs:
    - name: lead_profile
      type: object
      description: "Structured profile with name, title, LinkedIn URL, seniority, and background"
    - name: company_overview
      type: object
      description: "Company details with name, website, industry, size, headquarters, and description"
    - name: recent_news
      type: array
      description: "3-5 recent news items with title, source, date, summary, and URL"
    - name: enrichment_data
      type: object
      description: "Additional intelligence with funding, tech stack, hiring signals, and growth indicators"
  requires_capabilities:
    - web_search
  priority: high
  tags:
    - enrichment
    - leads
    - research
    - prospecting
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Lead Research

## Goal

Research a lead or company using web search to gather actionable intelligence for sales outreach. The output should give a rep everything they need to write a personalized, relevant first touch -- and enough context to hold an informed conversation if the prospect responds.

Good lead research is not a data dump. It is a curated intelligence brief that answers three questions: Who is this person? What does their company do? And what should I say to them that will actually get a response?

## Required Capabilities
- **Web Search**: To search the web for lead and company information (routed to Gemini with Google Search grounding)

## Inputs
- `lead_name`: Name of the person to research (if available)
- `company_name`: Name of the company to research (if available)
- `email`: Email address of the lead (if available, useful for finding LinkedIn profiles and confirming identity)
- `organization_id`: Current organization context

## Research Methodology

Lead research follows a three-phase approach: cast a wide net, go deep on what matters, then synthesize into actionable intelligence. See `references/research-playbook.md` for comprehensive search query templates, LinkedIn analysis techniques, time-boxed protocols (5/15/30 minute), and hiring signal interpretation.

### Phase 1: Discovery (Run Searches in Parallel)

Launch 5-7 searches simultaneously to maximize coverage and minimize latency. The goal is breadth -- you want to discover all available data sources before committing to deep dives.

**If you have a person name + company:**
1. `"[Person Name]" "[Company Name]" LinkedIn` -- find their professional profile
2. `"[Person Name]" "[Company Name]" OR [role keywords]` -- find mentions, quotes, content
3. `"[Company Name]" company about` -- official company information
4. `"[Company Name]" news OR announcement OR funding` -- recent activity
5. `"[Company Name]" careers OR hiring OR "open roles"` -- hiring signals and tech stack clues
6. `"[Person Name]" podcast OR speaker OR interview OR article` -- thought leadership and content
7. `"[Company Name]" review OR G2 OR Capterra` -- market reputation

**If you have only a person name:**
1. `"[Person Name]" LinkedIn [any known context]` -- find the right profile
2. `"[Person Name]" [industry or city or any disambiguating info]` -- narrow down identity
3. If email domain is available, use domain to identify company, then expand searches

**If you have only a company name:**
1. `"[Company Name]" company about` -- official info
2. `"[Company Name]" founders OR CEO OR leadership` -- identify key people
3. `"[Company Name]" funding OR investors OR Crunchbase` -- financial context
4. `"[Company Name]" news recent` -- recent developments
5. `site:[company-domain.com]` -- what they publish about themselves

**If you have only an email:**
1. Extract the domain. If it's a corporate domain (not gmail/yahoo/outlook), search for the company.
2. Search for the email address directly -- it may appear in press releases, conference bios, or public directories.
3. Once you have a company, expand to the full search pattern above.

### Phase 2: Deep Dive (Fetch Promising URLs)

Based on Phase 1 results, fetch and extract from the most valuable pages. Prioritize in this order:

1. **LinkedIn profile** (highest value for person research) -- current role, tenure, employment history, education, activity, shared connections
2. **Company About/Team page** -- official description, leadership, product lines, mission
3. **Company Pricing/Product page** -- what they sell, pricing model, target market
4. **Crunchbase/PitchBook profile** -- funding history, investors, valuation, growth metrics
5. **Recent blog posts or press releases** (last 6 months) -- strategic direction, product launches, partnerships
6. **Job postings** (current openings) -- tech stack, growth areas, team structure, priorities
7. **Conference bios or speaker pages** -- speaking topics, areas of expertise, professional interests
8. **Review sites** (G2, Capterra, Trustpilot) -- market reputation, strengths, weaknesses

**Time budget guidance:** Spend roughly 60% of research effort on the person, 40% on the company. The rep needs to connect with a human, not a logo. The company context exists to make the person conversation better.

### Phase 3: Synthesis (Merge and Validate)

Compile all findings into the structured output. During synthesis:

1. **Cross-reference identity.** Confirm that the person you found is actually the right person at the right company. Name collisions are common. Verify by cross-checking title, company, location, and timeline.
2. **Resolve conflicting data.** If LinkedIn says "Senior Director" but the company website says "VP," note both and use the most recently updated source. The person's own LinkedIn is usually the freshest.
3. **Assess data freshness.** Note when each piece of information was last updated. LinkedIn profiles updated in the last 3 months are high confidence. Company websites may not reflect recent changes.
4. **Identify gaps.** Explicitly note what you could NOT find. "Phone number: not found via web search" is more useful than silently omitting the field.
5. **Extract connection points.** The most valuable output of research is not data -- it's connection points. Things the rep can reference in outreach that show they did their homework: a recent post, a career move, a company announcement, a shared interest.

## LinkedIn Intelligence Extraction

LinkedIn is the single most valuable source for lead research. Here is what to extract and why each matters:

### Profile Basics
- **Current title + company**: Confirms identity and role
- **Headline**: Often more revealing than title -- people write their own headlines to signal what they care about
- **Location**: Time zone context for scheduling; local references in outreach

### Career Trajectory
- **Tenure at current company**: <6 months = new in role (high openness to new tools). 2+ years = established (harder to change but knows the org well).
- **Previous companies**: If they came from a company in your customer base, mention it. If they came from a competitor's customer base, they may have familiarity with the category.
- **Career pattern**: Rapid promotions suggest a high performer. Lateral moves suggest breadth. Long tenures suggest loyalty. Frequent moves suggest restlessness. Each tells you something about how to approach them.

### Content and Activity
- **Recent posts**: What topics do they post about? These are their professional interests and priorities.
- **Articles published**: Indicates thought leadership and areas of deep expertise.
- **Comments and engagement**: Even if they don't post, what do they react to? This reveals interests.
- **Recommendations given/received**: Reveals professional relationships and what people value about them.

### Network Signals
- **Shared connections**: If anyone at ${company_name} is connected to this person, flag it immediately. Warm introductions are gold.
- **Group memberships**: Professional groups reveal community affiliations and interests.
- **Followed companies/influencers**: Reveals what they pay attention to in the market.

## Company Research Shortcuts

When time is limited, here is where to find the best data fastest, in priority order:

1. **Company website /about page**: 60 seconds for company description, founding year, leadership, mission
2. **LinkedIn company page**: 30 seconds for employee count, growth trend, headquarters, industry
3. **Crunchbase**: 30 seconds for funding, investors, key people, employee count history
4. **Job postings (careers page or LinkedIn jobs)**: 2 minutes for tech stack, growth areas, team priorities
5. **Google News search**: 1 minute for recent announcements, funding, product launches
6. **G2/Capterra page**: 1 minute for market category, competitor set, customer sentiment

**Total: you can build a solid company profile in under 5 minutes if you know where to look.**

## News Analysis: Signal vs Noise

Not all company news is relevant for sales outreach. Here is how to filter:

### High-Signal News (always include)
- **Funding announcement**: New capital = new budget, new hiring, new tool purchases. The 90 days after a funding round is the best window for vendor outreach.
- **New product launch**: Indicates strategic direction and where they're investing. If ${company_name}'s products (from Organization Context) enable their new product, that's a direct talking point.
- **Leadership change**: New CTO/VP Engineering = new tool stack review. New CEO = strategic pivot. New VP Sales = new process evaluation.
- **Partnership/acquisition**: Reveals strategic priorities and potential integration needs.
- **Expansion** (new office, new market, international growth): Signals budget, growth, and potential scaling challenges that ${company_name}'s solutions can address.

### Medium-Signal News (include if relevant to ${company_name}'s products)
- **Industry awards or rankings**: Nice for flattery in outreach ("Congrats on the Inc 5000 listing") but not a buying signal.
- **Conference speaking/sponsoring**: Shows where they invest attention and marketing budget.
- **New customer wins (theirs)**: Indicates growth and potentially new requirements.

### Low-Signal / Noise (skip unless directly relevant)
- **Generic press releases**: Product updates, seasonal announcements, corporate boilerplate.
- **Industry analyst mentions**: Usually too abstract to be actionable.
- **Social media corporate posts**: Rarely reveals anything useful for sales intelligence.

## Tech Stack Detection

Understanding a prospect's technology stack tells you about their sophistication, budget, and potential integration needs. Here are the best detection methods:

### Job Postings (highest value)
Job descriptions are the most honest source of tech stack data. Companies list the actual tools they use because they need candidates who know them.
- Search: `"[Company Name]" jobs OR careers [tool category]`
- Look for: "Experience with [tool]", "Proficiency in [technology]", "We use [platform]"
- Engineering posts reveal development stack. Marketing posts reveal marketing tools. Sales posts reveal sales stack.

### Website Analysis
- View the website source or use technology detection services (BuiltWith, Wappalyzer)
- Look for: analytics tags (Google Analytics, Segment, Mixpanel), chat widgets (Intercom, Drift), CMS indicators (WordPress, Webflow), CDN (Cloudflare, Fastly)
- Pricing page technology indicators: Stripe billing, Chargebee, usage-based metering tools

### Engineering Blog / Technical Content
- Many companies publish their stack decisions on their engineering blog
- Search: `"[Company Name]" engineering blog OR tech stack OR architecture`
- Conference talks by their engineers often reveal stack choices

### Integration Ecosystem
- If the company is a SaaS product, check their integrations page. The tools they integrate with are often the tools their customers (and they themselves) use.

## Hiring Signal Analysis

Job postings reveal more about a company's priorities than almost any other public data source. Here is what different hiring patterns signal:

### Volume Signals
- **Hiring aggressively (10+ open roles)**: Growth mode. Likely has budget. May be experiencing scaling pain that ${company_name}'s solutions can address.
- **Minimal hiring (0-2 roles)**: Either stable/profitable or constrained. Check other signals (funding, layoff news) for context.
- **Hiring spree followed by pause**: Possible pivot, budget tightening, or reorganization. Timing may be wrong.

### Role Type Signals
- **Hiring for ${company_name}'s product category**: (e.g., hiring a role related to the solutions described in Organization Context) -- STRONG buying signal. They're investing in the function ${company_name}'s product serves.
- **Hiring SDRs/AEs**: Building out sales motion. May need sales tools, CRM, enablement.
- **Hiring engineers**: Building product. May need dev tools, infrastructure, CI/CD.
- **Hiring a Head of [Function]**: New leader = new strategy, tool review, vendor evaluation. Prime window.

### Technology Signals
- Job descriptions that list competitor tools: "Experience with [Competitor] a plus" -- they use your competitor. Competitive displacement opportunity.
- Job descriptions that list ${company_name}'s product: "Experience with [${company_name}'s product]" -- they already use it (expansion) or are evaluating it.

## Connection Point Discovery

The #1 goal of lead research is to find connection points that make outreach feel personal and relevant. Here are the best connection points, ranked by effectiveness:

### Tier 1: Direct Relevance (reference in opening line)
- **They posted about a problem you solve.** "I saw your post about [X] -- we help teams like yours handle exactly that."
- **They recently changed roles.** "Congrats on the new role at [Company]. When I joined a new team, one of the first things I evaluated was [relevant category]."
- **Their company just announced something relevant.** "Saw the Series B announcement -- congrats. Companies at your stage often start looking at [your category]."
- **Mutual connection.** "I noticed you're connected with [Name] -- they've been using our product for [use case]."

### Tier 2: Contextual Relevance (reference in body)
- **They spoke at a conference** on a topic related to ${company_name}'s product area.
- **They published an article or blog post** touching on your space.
- **Their company is hiring for a role** in ${company_name}'s product function area.
- **They share a professional background** (same company alumni, same university, same industry transition).

### Tier 3: Light Personalization (use if nothing better)
- **Company milestone** (anniversary, growth achievement, award).
- **Industry trend** they're likely affected by.
- **Geographic connection** (same city, same region).

**Rule of thumb:** Always aim for at least one Tier 1 connection point. If you can't find one, you need to dig deeper or reconsider whether this lead is worth manual outreach (vs. an automated nurture sequence).

## Data Freshness Standards

Data decays fast in B2B. Here are the freshness standards. See `references/source-hierarchy.md` for the complete data source reliability hierarchy, cross-reference rules, conflict resolution methodology, and provider-specific accuracy data.

| Data Type | Fresh | Acceptable | Stale | Action on Stale |
|-----------|-------|------------|-------|-----------------|
| Job title / role | <3 months | 3-6 months | >6 months | Flag as "may have changed" |
| Company size | <6 months | 6-12 months | >12 months | Triangulate with other sources |
| Funding data | <3 months | 3-12 months | >12 months | Note date explicitly |
| Tech stack | <6 months | 6-12 months | >12 months | Cross-check with job postings |
| News / press | <30 days | 30-90 days | >90 days | Only include if highly significant |
| Contact details | <3 months | 3-6 months | >6 months | Verify before outreach |

**Always include the date of the most recent data source.** A profile built on data from 2 weeks ago is dramatically more valuable than one built on data from 8 months ago.

## Output Contract

Return a SkillResult with:
- `data.lead_profile`: Structured profile object with:
  - `name`: Full name
  - `title`: Current job title
  - `linkedin_url`: LinkedIn profile URL (if found)
  - `role_seniority`: "C-level" | "VP" | "Director" | "Manager" | "IC"
  - `tenure_current_role`: How long in current role (if determinable)
  - `tenure_current_company`: How long at current company (if determinable)
  - `background`: Brief professional background summary (2-3 sentences covering career arc)
  - `previous_roles`: Array of last 2-3 roles with company, title, and approximate dates
  - `recent_activity`: Any recent posts, talks, publications, or public activity
  - `content_topics`: Topics they post about or engage with on LinkedIn
  - `decision_authority`: "likely_decision_maker" | "likely_influencer" | "likely_evaluator" | "unknown" (inferred from title + company size)
- `data.company_overview`: Company details with:
  - `company_name`: Official company name
  - `website`: Company website URL
  - `industry`: Industry classification
  - `company_size`: Employee count range
  - `headquarters`: Location
  - `founded`: Year founded (if found)
  - `description`: One-paragraph company description
  - `business_model`: How they make money (SaaS, services, marketplace, etc.)
- `data.recent_news`: Array of 3-5 recent news items (high-signal only) with:
  - `title`: Article/news title
  - `source`: Publication name
  - `date`: Publication date
  - `summary`: One-sentence summary
  - `relevance`: Why this matters for outreach
  - `url`: Link to the article
- `data.enrichment_data`: Additional intelligence with:
  - `funding`: Latest funding round, amount, investors (if available)
  - `tech_stack`: Known technologies and tools (with detection method noted)
  - `hiring_signals`: Recent job postings and what they indicate for your sales motion
  - `growth_indicators`: Revenue, headcount growth, market expansion signals
- `data.connection_points`: Array of 2-5 specific connection points for outreach, ranked by tier (1/2/3), each with:
  - `point`: The connection point
  - `tier`: 1, 2, or 3
  - `suggested_use`: How to reference it in outreach
  - `source`: Where you found it
- `data.data_freshness`: Date of the most recent data source used
- `references`: Array of source URLs used in research

## Quality Checklist

Before returning research results, verify:

- [ ] Person identity is confirmed (not a name collision with someone at a different company)
- [ ] LinkedIn URL is verified as the correct person (not just a search results link)
- [ ] Company description is accurate and current (not a 3-year-old About page for a company that has since pivoted)
- [ ] At least one Tier 1 or Tier 2 connection point is identified (if none found, note this gap explicitly)
- [ ] News items are high-signal, not noise (no generic press releases or industry boilerplate)
- [ ] Tech stack data includes detection method (job posting vs. website analysis vs. integration page)
- [ ] Hiring signals are interpreted, not just listed ("Hiring 3 SDRs" is data; "Building out outbound sales motion -- may need sales enablement tools" is intelligence)
- [ ] All data points have a cited source URL
- [ ] Data freshness is noted for time-sensitive fields (title, company size, funding)
- [ ] Gaps are explicitly called out (what you looked for but could not find)
- [ ] Output is scannable -- a rep can get the key points in 30 seconds

## Guidelines
- Always cite sources with URLs so the rep can verify information
- If the lead name is ambiguous, use company context to disambiguate. If still ambiguous, present the most likely match and note the uncertainty.
- Prioritize recent information (last 6 months) over older data
- If limited information is found, clearly state what could not be determined rather than guessing. "Not found" is always better than fabricated data.
- Use ${company_name} context to tailor research toward relevant competitive and partnership angles
- Flag any connection points between the lead's company and ${company_name} (shared investors, mutual connections, technology overlap)
- Focus on intelligence, not data. The rep doesn't need to know that the company was founded in 2015 in Austin. The rep needs to know that the company just raised $30M and is hiring 5 engineers, which means they're scaling and probably evaluating new tools.

## Error Handling

### No lead name or company name provided
Ask the user for clarification. Provide a template: "To research this lead, I need at minimum a person name and company name. If you have an email address or LinkedIn URL, those help me find the right person faster."

### Ambiguous person (common name, no company context)
Do not guess. Return the top 2-3 possible matches with distinguishing details and ask: "I found multiple people named [Name]. Which of these is the right one?" If company is provided but person is ambiguous within the company, use title/department context to narrow down.

### Company is very small, private, or new
Small companies have less public data. This is expected, not an error. Lean harder on:
1. Founder/CEO LinkedIn profile (often the richest source for small companies)
2. Product Hunt, AngelList, Crunchbase (startup databases)
3. Social media presence (Twitter/X, LinkedIn company page)
4. Website itself (especially the blog, which small companies often use as their primary content channel)

Note limited data availability honestly: "Limited public data available -- [Company] appears to be an early-stage startup with fewer than 20 employees. Profile confidence is medium."

### Web search returns no results for the person
The person may have a minimal online presence. This itself is information:
- Return what you found about the company
- Note: "No significant online presence found for [Name]. This may indicate they are new to the role, prefer a low profile, or the name may be different on professional platforms."
- Suggest alternative approaches: "If you have their LinkedIn URL or email, those would help me confirm their identity."

### Email domain is a personal email (gmail, yahoo, etc.)
Personal email provides no company context. Flag this: "Email is a personal address -- cannot determine company affiliation from the domain. To research this lead, I need a company name or LinkedIn profile." If a name is available, search for the name directly, but note the lower confidence.

### Data sources conflict
When sources disagree (e.g., LinkedIn says 200 employees, Crunchbase says 150):
1. Present both data points with their sources
2. Use the most recently updated source as the primary
3. Note the discrepancy: "Employee count varies by source: LinkedIn company page shows ~200, Crunchbase shows 150 (updated 3 months ago). Using LinkedIn figure as primary."
