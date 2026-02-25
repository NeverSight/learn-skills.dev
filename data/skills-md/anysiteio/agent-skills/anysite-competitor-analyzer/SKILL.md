---
name: anysite-competitor-analyzer
description: Deep competitive intelligence combining web scraping, LinkedIn data, social media monitoring, leadership analysis, GitHub activity, Glassdoor sentiment, and community insights. Analyzes founders/C-level profiles, tracks real-time signals vs quarterly reports, and creates comprehensive competitor profiles. Use when asked to analyze competitors, research leadership teams, investigate market positioning, compare products/pricing, assess strategic threats, or gather intelligence on founders and key executives.
---

# Competitor Analyzer

Systematic framework for gathering and analyzing competitive intelligence using Anysite MCP tools.

## When to Use This Skill

Trigger this skill when users ask to:
- "Analyze [competitor name]"
- "Research our competitors"
- "Create a competitive analysis of [company]"
- "How does [competitor] position themselves?"
- "What are [competitor]'s strengths and weaknesses?"
- "Compare our product with [competitor]"
- "Who are our main competitors?"
- "Build a battle card for [competitor]"

## Quick Start

**For single competitor analysis:**
```bash
# 1. Generate analysis template
python scripts/analyze_competitor.py "Competitor Name" "https://competitor.com"

# 2. Use Anysite tools to gather data (see workflow below)

# 3. Fill in the JSON template with findings

# 4. Generate final report
python scripts/analyze_competitor.py "Competitor Name" "https://competitor.com" | \
    python -c "import sys,json; exec('from scripts.analyze_competitor import format_markdown_report; print(format_markdown_report(json.load(sys.stdin)))')" \
    > /mnt/user-data/outputs/competitor_report.md
```

## Analysis Workflow

### Phase 1: Foundation (15-20 min)

**Step 1: Initialize Analysis Structure**

Run the analysis script to create structured template:
```bash
python scripts/analyze_competitor.py "Competitor Name" "https://competitor.com" > /tmp/analysis.json
```

**Step 2: Web Presence Reconnaissance**

Scrape key pages to understand positioning:
```python
# Homepage - core messaging
Anysite:parse_webpage({
    "url": "https://competitor.com",
    "only_main_content": true,
    "strip_all_tags": true
})

# Pricing - cost structure
Anysite:parse_webpage({
    "url": "https://competitor.com/pricing",
    "only_main_content": true
})

# About - company background
Anysite:parse_webpage({
    "url": "https://competitor.com/about",
    "only_main_content": true,
    "extract_contacts": true
})
```

**Extract from homepage:**
- H1/H2 headlines → positioning_statement
- Feature bullets → core_features
- Customer logos → customer_logos
- Value prop → value_proposition

**Extract from pricing:**
- Tier names and prices → pricing.tiers
- Cost per unit → pricing.unit_economics
- Free tier details → pricing.free_tier_limits
- Entry price → pricing.entry_price

**Extract from about:**
- Company description → company_overview.description
- Location → company_overview.headquarters
- Team size hints → company_overview.employee_count

### Phase 2: LinkedIn Intelligence (10-15 min)

**Step 3: Find Company Profile**

```python
# Search for company
Anysite:search_linkedin_companies({
    "keywords": "competitor name",
    "count": 5
})

# Get detailed profile using slug from search results
Anysite:get_linkedin_company({
    "company": "company-slug-from-search"
})
```

**Extract:**
- `follower_count` → Online presence indicator
- `employee_count` → Company size
- `description` → Self-positioning
- `headquarters` → Location
- `specialties` → Keywords they emphasize

**Step 4: Analyze Team & Growth**

```python
# Check employee growth signals
Anysite:get_linkedin_company_employees({
    "companies": ["company-slug"],
    "keywords": "engineer developer",
    "count": 50
})

# Find leadership
Anysite:get_linkedin_company_employees({
    "companies": ["company-slug"],
    "keywords": "CEO founder",
    "count": 10
})
```

**Use findings to assess:**
- Team size → growth_indicators.employee_growth
- Eng:sales ratio → GTM strategy signal
- Recent hires → growth phase indicator

**Step 5: Content Strategy**

```python
# Analyze posting activity
Anysite:get_linkedin_company_posts({
    "urn": "company-urn-from-profile",
    "count": 20
})
```

**Analyze posts for:**
- Frequency → content_strategy.blog_frequency
- Themes → content_strategy.key_topics
- Engagement → online_presence.linkedin.engagement_quality
- Tone → content_strategy.tone_of_voice

### Phase 3: Deep Social & Community Research (20-30 min)

**Step 6: Twitter Deep Dive**

**A. Company Account Analysis**
```python
# Get profile stats
Anysite:get_twitter_user({
    "user": "competitor_handle"
})

# Recent activity (analyze more posts)
Anysite:get_twitter_user_posts({
    "user": "competitor_handle",
    "count": 100
})
```

**Extract from company account:**
- Followers → reach indicator
- Tweet frequency → activity level
- Content mix (product updates, thought leadership, customer engagement)
- Response time to mentions
- Tone of voice
- Most engaging tweets (viral content patterns)

**B. Founder/Executive Twitter Presence**
```python
# Find and analyze founder accounts
Anysite:get_twitter_user({
    "user": "founder_handle"
})

Anysite:get_twitter_user_posts({
    "user": "founder_handle",
    "count": 100
})
```

**Leadership Twitter signals:**
- Personal brand strength
- Technical credibility (what they share)
- Customer engagement quality
- Industry thought leadership
- Follower quality (who follows them)
- Retweet patterns (what they amplify)

**C. Brand Mentions & Sentiment**
```python
# Comprehensive mention search
Anysite:search_twitter_posts({
    "query": "competitor_name OR @handle OR #competitor_hashtag",
    "count": 200
})

# Problem/complaint mentions
Anysite:search_twitter_posts({
    "query": "competitor_name (problem OR issue OR bug OR slow OR expensive)",
    "count": 100
})

# Positive sentiment
Anysite:search_twitter_posts({
    "query": "competitor_name (love OR great OR amazing OR best OR solved)",
    "count": 100
})

# Competitive mentions
Anysite:search_twitter_posts({
    "query": "competitor_name vs OR competitor_name alternative OR switching from competitor_name",
    "count": 100
})
```

**Sentiment scoring:**
```
For each mention batch, calculate:
- Positive mentions: praise, recommendations, success stories
- Negative mentions: complaints, frustrations, churn signals
- Neutral mentions: questions, feature discussions
- Competitive mentions: comparisons with alternatives

Sentiment Score = (Positive - Negative) / Total
Range: -1.0 (very negative) to +1.0 (very positive)
```

**D. Customer Voice Analysis**
```python
# Find actual users
Anysite:search_twitter_posts({
    "query": "using competitor_name OR tried competitor_name",
    "count": 100
})

# Power users
Anysite:search_twitter_posts({
    "query": "@handle thanks OR @handle helped OR @handle support",
    "count": 50
})
```

**Extract:**
- Real use cases (what customers actually do)
- Pain points (what they struggle with)
- Success stories (what works well)
- Feature requests (what they want)
- Support quality (how fast company responds)

**Step 7: Reddit Deep Community Intelligence**

**A. Brand Presence Mapping**
```python
# General mentions across Reddit
Anysite:search_reddit_posts({
    "query": "competitor_name",
    "count": 100
})

# Industry-specific subreddits
relevant_subs = [
    "SaaS", "startups", "Entrepreneur",  # Business
    "webdev", "programming", "devops",    # Tech
    "nocode", "automation",               # No-code
    "datascience", "analytics"            # Data
]

for sub in relevant_subs:
    Anysite:search_reddit_posts({
        "query": "competitor_name",
        "subreddit": sub,
        "count": 50
    })
```

**B. Competitive Discussions**
```python
# Direct comparisons
Anysite:search_reddit_posts({
    "query": "competitor_name vs",
    "count": 100
})

# Alternative searches
Anysite:search_reddit_posts({
    "query": "alternative to competitor_name",
    "count": 100
})

Anysite:search_reddit_posts({
    "query": "better than competitor_name",
    "count": 50
})

# Problem space
Anysite:search_reddit_posts({
    "query": "[problem they solve] tools OR solutions",
    "count": 100
})
```

**C. Deep Thread Analysis**

For high-engagement threads, get comments:
```python
# Get specific post details
Anysite:get_reddit_post({
    "post_url": "reddit.com/r/subreddit/comments/..."
})

# Get all comments
Anysite:get_reddit_post_comments({
    "post_url": "reddit.com/r/subreddit/comments/..."
})
```

**Analyze thread comments for:**
- Detailed user experiences
- Technical discussions
- Feature comparisons
- Pricing discussions
- Customer support experiences
- Decision factors (why they chose/didn't choose)

**D. Sentiment & Voice Analysis**

**Positive signals:**
- "I love [competitor]"
- "Works perfectly for..."
- "Best tool for..."
- "Highly recommend"
- "Switched to [competitor] and..."

**Negative signals:**
- "Disappointed with..."
- "Overpriced"
- "Customer support is..."
- "Buggy/unreliable"
- "Looking for alternative"
- "Switched away from..."

**Neutral/informational:**
- "How does [competitor] work?"
- "Anyone tried [competitor]?"
- "Pricing question"
- Feature clarifications

**E. Community Size & Engagement**

**Calculate metrics:**
```
Brand Awareness Score:
- Total unique mentions (last 30 days)
- Number of different subreddits mentioned in
- Average upvotes per mention
- Comment volume per mention

Community Health:
- Positive/Negative mention ratio
- Response rate to questions
- Problem resolution in comments
- Community helping each other
```

**Step 7.5: Cross-Platform Insight Synthesis**

**Compare Twitter vs Reddit:**

**Twitter typically shows:**
- Official company narrative
- Marketing messaging
- Quick customer service interactions
- Surface-level sentiment
- Broader reach

**Reddit typically reveals:**
- Unfiltered user opinions
- Detailed technical discussions
- Pricing sensitivity
- Competitive comparisons
- Real problems and workarounds

**Look for disconnects:**
- Company claims strong product (Twitter) but users complain (Reddit)
- High Twitter engagement but low Reddit mentions → Marketing-driven, not organic
- Reddit loves it but low Twitter presence → Word-of-mouth, under-marketed
- Consistent messaging → Authentic product-market fit

### Phase 4: Leadership & Founders Intelligence (15-20 min)

**Step 8: Identify Key Leaders**

```python
# Find founders and C-level
Anysite:search_linkedin_users({
    "company_keywords": "competitor-name",
    "title": "founder OR CEO OR CTO OR CPO",
    "count": 10
})

# Get detailed profiles
Anysite:get_linkedin_profile({
    "user": "founder-linkedin-username",
    "with_experience": true,
    "with_education": true,
    "with_skills": true
})
```

**Extract for each leader:**
- Full career history → their experience and expertise
- Previous companies → track record
- Education background → academic credentials
- Skills → technical depth
- Languages → market reach
- Recommendations → credibility signals

**Step 9: Analyze Leadership Activity**

```python
# Get personal posts
Anysite:get_linkedin_user_posts({
    "urn": "user-urn-from-profile",
    "count": 50
})

# Check comments on others' posts
Anysite:get_linkedin_user_comments({
    "urn": "user-urn",
    "count": 30
})

# See what they're engaging with
Anysite:get_linkedin_user_reactions({
    "urn": "user-urn",
    "count": 50
})
```

**Analyze for:**
- Posting frequency and themes
- Technical depth in posts
- Market perspective
- Customer engagement
- Thought leadership quality
- Network quality (who engages with them)

**Step 10: Twitter Leadership Presence**

```python
# Founder Twitter activity
Anysite:get_twitter_user({
    "user": "founder_handle"
})

Anysite:get_twitter_user_posts({
    "user": "founder_handle",
    "count": 100
})
```

**Leadership indicators:**
- Personal brand strength
- Technical credibility
- Customer relationships
- Industry influence
- Communication style
- Transparency level

### Phase 5: Technical & Data Discovery (10-15 min)

**Step 11: Documentation Quality**

```python
# Scrape docs homepage
Anysite:parse_webpage({
    "url": "https://competitor.com/docs",
    "only_main_content": true
})

# Check API reference
Anysite:parse_webpage({
    "url": "https://competitor.com/api",
    "only_main_content": true
})
```

**Step 11: Documentation Quality**

```python
# Scrape docs homepage
Anysite:parse_webpage({
    "url": "https://competitor.com/docs",
    "only_main_content": true
})

# Check API reference
Anysite:parse_webpage({
    "url": "https://competitor.com/api",
    "only_main_content": true
})
```

**Assess:**
- Documentation completeness
- Code examples presence
- Interactive explorer
- SDK availability
→ Feed into technical_capabilities

**Step 12: GitHub Presence (if applicable)**

```python
# Parse GitHub profile page
Anysite:parse_webpage({
    "url": "https://github.com/competitor-org",
    "only_main_content": true
})

# Check main repository
Anysite:parse_webpage({
    "url": "https://github.com/competitor-org/main-repo",
    "only_main_content": true
})
```

**Extract:**
- Star count (developer interest)
- Fork count (actual usage)
- Commit frequency (development velocity)
- Contributors count (community size)
- Issue response time (support quality)
- Open source components (ecosystem play)

**Step 13: Alternative Data Sources**

```python
# Glassdoor reviews (if company page exists)
Anysite:parse_webpage({
    "url": "https://www.glassdoor.com/Reviews/competitor-name",
    "only_main_content": true
})
```

**What to extract:**
- Overall rating (employee satisfaction)
- CEO approval rating (leadership quality)
- Salary ranges (compensation level)
- Interview difficulty (hiring standards)
- Work-life balance (culture signal)
- Recent reviews (current state)

**Step 14: Integration Ecosystem**

```python
# Get sitemap to find all pages
Anysite:get_sitemap({
    "url": "https://competitor.com/sitemap.xml",
    "count": 50
})

# Parse integrations page
Anysite:parse_webpage({
    "url": "https://competitor.com/integrations",
    "only_main_content": true
})
```

**Step 14: Integration Ecosystem**

```python
# Get sitemap to find all pages
Anysite:get_sitemap({
    "url": "https://competitor.com/sitemap.xml",
    "count": 50
})

# Parse integrations page
Anysite:parse_webpage({
    "url": "https://competitor.com/integrations",
    "only_main_content": true
})
```

**Extract:**
- Integration partners → technical_capabilities.integrations
- Platform focus (Zapier, enterprise tools, etc.)
- API-first vs GUI-first

### Phase 6: Synthesis (15-20 min)

**Step 15: Competitive Analysis**

Compare findings against your own product:

**Strengths (what they do well):**
- Identify 3-5 clear advantages they have
- Based on features, pricing, market position, or execution

**Weaknesses (where they struggle):**
- Identify 3-5 clear gaps or problems
- Missing features, high prices, poor UX, etc.

**Opportunities (what you can exploit):**
- Their weaknesses that you can capitalize on
- Underserved segments they're missing
- Messaging/positioning gaps

**Threats (what you need to watch):**
- Their strengths that could hurt you
- Recent funding or growth
- Feature development velocity

**Step 16: Strategic Insights**

Synthesize everything into:

**Key Takeaways (3-5 bullets):**
- Most important findings
- Clear, actionable insights

**Competitive Threats (2-3 bullets):**
- What they could do to hurt your position
- Their strategic advantages

**Opportunities to Exploit (3-5 bullets):**
- How to position against them
- Their vulnerabilities to target
- Market gaps they're missing

**Watch Areas:**
- Things to monitor quarterly
- Signals of strategic shifts

**Step 17: Generate Final Report**

Update the JSON template with all findings, then generate markdown:

```python
import json
from scripts.analyze_competitor import save_analysis

# Load populated template
with open('/tmp/analysis.json', 'r') as f:
    data = json.load(f)

# Generate reports
json_path, md_path = save_analysis(data)
print(f"Reports saved:\n  JSON: {json_path}\n  Markdown: {md_path}")
```

Move final files to outputs:
```bash
cp /tmp/analysis.json /mnt/user-data/outputs/
cp /tmp/analysis.md /mnt/user-data/outputs/
```

## Advanced Techniques

### Multi-Competitor Analysis

For analyzing 3-5 competitors simultaneously:

1. Run analysis workflow for each competitor
2. Create comparison matrix in spreadsheet format
3. Focus on key differentiators:
   - Pricing comparison table
   - Feature matrix (rows=features, cols=competitors)
   - Market position map (price vs capabilities)
   - Social presence comparison

### Ongoing Monitoring

For quarterly updates (not full re-analysis):

**Quick check (30 min):**
```python
# 1. Re-scrape pricing
Anysite:parse_webpage({"url": "competitor.com/pricing"})

# 2. Check recent posts
Anysite:get_linkedin_company_posts({"urn": "...", "count": 10})

# 3. Employee growth
Anysite:get_linkedin_company_employees({"companies": ["..."], "count": 20})

# 4. Recent mentions
Anysite:search_twitter_posts({"query": "competitor", "count": 50})
```

Update only changed sections in JSON template.

### Battle Card Creation

For sales team quick reference:

**Focus on:**
1. Quick facts (1-2 sentences)
2. Head-to-head feature comparison (table format)
3. Pricing comparison (clear numbers)
4. 3 reasons we win
5. 3 reasons we might lose
6. Talk tracks ("When they say X, we say Y")

Keep to 1-2 pages maximum.

## Reference Files

When you need detailed guidance:

- **Data collection methodology:** See [data_collection.md](references/data_collection.md)
  - Use when unsure which Anysite tools to use
  - Use when planning data gathering strategy
  - Contains detailed tool parameters and extraction techniques

- **Analysis frameworks:** See [analysis_frameworks.md](references/analysis_frameworks.md)
  - Use when analyzing specific company types (SaaS vs Enterprise vs Consumer)
  - Use when creating battle cards or competitive matrices
  - Contains templates for different output formats

## Common Patterns

### Pattern 1: Rapid Assessment (30-45 min)

For quick competitive scan:
1. Homepage + pricing scrape
2. LinkedIn company profile
3. Recent social posts (20 total)
4. Fill core sections only (skip deep dives)
5. Generate brief summary (1 page)

### Pattern 2: Deep Intelligence (2-3 hours)

For comprehensive analysis:
1. Full web presence (7-10 pages)
2. Complete LinkedIn intelligence
3. Social media deep dive (50-100 posts/mentions)
4. Community sentiment analysis
5. Technical documentation review
6. Full JSON template populated
7. Detailed markdown report

### Pattern 3: Pricing Focus

For pricing-specific analysis:
1. Scrape all pricing pages
2. Calculate unit economics
3. Map tier structures
4. Compare to market
5. Identify pricing strategy
6. Generate pricing comparison table

### Pattern 4: Leadership Focus

For founder/team intelligence:
1. Identify all founders and C-level
2. Deep dive into founder LinkedIn profiles
3. Analyze personal posting activity (50+ posts)
4. Track Twitter presence and influence
5. Map previous company experience
6. Assess thought leadership quality
7. Evaluate public credibility

**Use when:**
- Considering partnerships
- Evaluating acquisition targets
- Assessing strategic threats
- Understanding company DNA

## Tips for Effective Analysis

**Be Systematic:**
- Follow the phase order
- Don't skip LinkedIn intelligence (best growth signals)
- Always check pricing (most volatile data)

**Think Strategically:**
- Not just "what" they do, but "why"
- Look for patterns in their behavior
- Consider their constraints (funding, team size)

**Verify Claims:**
- Marketing copy ≠ reality
- Cross-reference multiple sources
- Note confidence levels (verified vs estimated)

**Focus on Actionable Insights:**
- Don't just describe, analyze implications
- What should YOUR company do based on findings?
- What threats need immediate response?

**Document Data Freshness:**
- Always note analysis date
- Mark which data is recent vs stale
- Plan update frequency based on importance

## Output Quality Standards

**Good competitive analysis includes:**
- ✅ Clear positioning statement
- ✅ Quantified metrics (prices, follower counts, team size)
- ✅ Specific examples (actual quotes, feature lists)
- ✅ Strategic implications explained
- ✅ Data sources noted
- ✅ Confidence levels indicated

**Avoid:**
- ❌ Vague assessments ("they seem good at X")
- ❌ Unsupported claims ("probably losing money")
- ❌ Missing pricing details
- ❌ Outdated data without date stamps
- ❌ Pure feature lists without analysis

## Troubleshooting

**"Can't find LinkedIn company":**
- Try variations of company name
- Search for CEO name, find company from profile
- Check if they use different legal name

**"Pricing page missing/unclear":**
- Check /plans, /buy, /subscribe URLs
- Look for pricing calculator
- Note "Contact Sales" as signal (enterprise focus)

**"No social media presence":**
- Still document the absence (itself a signal)
- Check founder personal accounts
- Look for employee posting activity

**"Too much data, overwhelmed":**
- Start with Phase 1 & 2 only (foundation + LinkedIn)
- Generate partial report
- Add Phase 3 & 4 if needed for depth
