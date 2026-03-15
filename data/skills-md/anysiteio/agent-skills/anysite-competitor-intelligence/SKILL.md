---
name: anysite-competitor-intelligence
description: Competitive intelligence gathering using anysite MCP server across LinkedIn, social media, Y Combinator, and the web. Track competitor activities, analyze hiring patterns, monitor content strategies, benchmark market positioning, research startup competitors, and gather strategic intelligence. Supports LinkedIn (companies, employees, posts), Instagram, Twitter/X, Reddit, YouTube, Y Combinator, and web scraping. Use when users need to analyze competitors, track competitive movements, research market positioning, monitor hiring velocity, or gather strategic market intelligence.
---

# anysite Competitor Intelligence

Comprehensive competitive intelligence gathering using anysite MCP server. Track competitors across LinkedIn, social media, and the web to understand their strategies, monitor their activities, and identify competitive opportunities.

## Overview

The anysite Competitor Intelligence skill helps you:
- **Track competitor companies** on LinkedIn and Y Combinator
- **Monitor hiring patterns** to identify growth areas and strategic priorities
- **Analyze content strategies** across social platforms
- **Benchmark positioning** and messaging
- **Identify key employees** and leadership changes
- **Track competitive movements** like funding, launches, partnerships

This skill provides 90% coverage of competitive intelligence capabilities with excellent LinkedIn and social media monitoring.

## Supported Platforms

- ✅ **LinkedIn** (Primary): Company pages, employee search, post monitoring, job listings, growth tracking
- ✅ **Y Combinator**: Startup competitor research, funding data, batch analysis
- ✅ **Twitter/X**: Social presence monitoring, content strategy, engagement analysis
- ✅ **Reddit**: Community sentiment, product discussions, competitor mentions
- ✅ **Instagram**: Brand presence, visual content strategy, influencer partnerships
- ✅ **YouTube**: Video content, channel growth, community engagement
- ✅ **Web Scraping**: Company websites, press releases, blog content
- ✅ **SEC**: Public company filings for competitors

## Quick Start

### Step 1: Identify Competitors

Choose your competitor identification method:

| Goal | Primary Tool | Output |
|------|-------------|--------|
| Find similar companies | `search_linkedin_companies` | Company list with metrics |
| Research startup competitors | `search_yc_companies` | YC startups by industry/batch |
| Discover by employee search | `search_linkedin_users` → companies | Companies from employee profiles |
| Find by keywords/industry | `search_linkedin_companies` + keywords | Filtered company list |

### Step 2: Gather Competitive Intelligence

Execute MCP tools to collect competitor data:

**Company Profile Analysis**
```
Tool: mcp__anysite__get_linkedin_company
Parameters:
- company: "competitor-name" or LinkedIn URL
Returns: Description, size, location, website, specialties
```

**Employee Intelligence**
```
Tool: mcp__anysite__search_linkedin_users
Parameters:
- company_keywords: "Competitor Inc"
- title: "VP OR Director OR Head" (for leadership)
- count: 50
Returns: Key employees, org structure insights
```

**Hiring Velocity Analysis**
```
Tool: mcp__anysite__get_linkedin_company_employee_stats
Parameters:
- urn: <company URN from search>
Returns: Growth metrics, department distribution
```

**Content Strategy**
```
Tool: mcp__anysite__get_linkedin_company_posts
Parameters:
- urn: <company URN>
- count: 20
Returns: Recent posts, engagement, messaging themes
```

### Step 3: Process and Analyze

Analyze gathered data for:
- **Growth signals**: Hiring velocity, funding, expansion
- **Strategic priorities**: Department hiring, job postings, content themes
- **Market positioning**: Messaging, target audience, value props
- **Competitive threats**: New products, partnerships, key hires

### Step 4: Format Output

**Chat Summary**: Competitive insights with key findings
**CSV Export**: Competitor comparison matrix
**JSON Export**: Complete data for tracking over time

## Common Workflows

### Workflow 1: Comprehensive Competitor Profile

**Scenario**: Deep dive on a specific competitor

**Steps**:

1. **Company Overview**
```
get_linkedin_company("competitor")
→ Size, industry, description, website, founding year
```

2. **Leadership Team**
```
search_linkedin_users(
  company_keywords="Competitor Inc",
  title="C-level OR VP OR SVP OR President"
)
→ C-suite and VP-level executives
```

3. **Organizational Structure**
```
get_linkedin_company_employee_stats(urn)
→ Total employees, growth rate, department breakdown

For each department:
  search_linkedin_users(company_keywords, title=<department_title>)
→ Team sizes, key roles
```

4. **Hiring Intelligence**
```
search_linkedin_jobs(keywords="Competitor Inc")
→ Open positions, hiring priorities, expansion areas
```

5. **Content Strategy**
```
get_linkedin_company_posts(urn, count=50)
→ Posting frequency, themes, engagement levels

get_twitter_user("competitor")
get_twitter_user_posts("competitor", count=50)
→ Social media presence and strategy
```

6. **Product/Market Intelligence**
```
parse_webpage("https://competitor.com")
→ Positioning, messaging, product offerings

parse_webpage("https://competitor.com/blog")
→ Content topics, thought leadership

search_reddit_posts(query="Competitor Inc", count=20)
→ Customer sentiment, product feedback
```

**Expected Output**:
- Complete company profile
- Leadership team roster (10-20 executives)
- Hiring velocity and priorities
- Content strategy analysis
- Product positioning insights
- Customer sentiment summary

### Workflow 2: Competitive Landscape Mapping

**Scenario**: Map all competitors in your space

**Steps**:

1. **Identify Competitors**
```
search_linkedin_companies(
  keywords="<your industry keywords>",
  industry="<industry>",
  employee_count=["51-200", "201-500", "501-1000"],
  count=50
)
```

2. **Filter and Prioritize**
```
For each company:
  get_linkedin_company(company)
  → Review description for relevance
  → Check employee count and growth
  → Verify competitive overlap
```

3. **Categorize Competitors**
```
Direct: Same products, same market
Indirect: Similar products, different market
Potential: Adjacent space, could expand
```

4. **Size and Growth Metrics**
```
For each competitor:
  get_linkedin_company_employee_stats(urn)
  → Employee count, growth rate
  → Department distribution
```

5. **Positioning Analysis**
```
For each competitor:
  get_linkedin_company_posts(urn, count=10)
  → Key messaging themes

  parse_webpage(website + "/about")
  → Value proposition, target market
```

6. **Funding and Traction** (for startups)
```
search_yc_companies(query="<industry>")
→ YC competitors with funding data

For each YC company:
  get_yc_company(company)
  → Batch, team size, description
```

**Expected Output**:
- 20-50 competitors identified
- Categorized by competitive threat level
- Size and growth metrics for each
- Positioning and messaging summaries
- Competitive landscape map

### Workflow 3: Hiring Velocity Tracking

**Scenario**: Monitor competitor hiring to identify growth areas

**Steps**:

1. **Baseline Employee Count**
```
get_linkedin_company_employee_stats(competitor_urn)
→ Current total employees
→ Department distribution
```

2. **Track Open Positions**
```
search_linkedin_jobs(keywords="Competitor Inc")
→ All open positions

Group by department:
- Engineering roles
- Sales roles
- Marketing roles
- Operations roles
```

3. **Analyze Recent Hires**
```
search_linkedin_users(
  company_keywords="Competitor Inc",
  count=100
)
→ Get all employees

Filter for recent joins:
get_linkedin_user_experience(urn)
→ Start date at current company
→ Identify hires from last 3-6 months
```

4. **Track Key Departures**
```
For former employees:
search_linkedin_users(keywords="Competitor Inc")
→ Filter profiles showing "Former" or past employment

Identify:
- Leadership departures
- Team exodus (multiple from same department)
- Moves to other competitors
```

5. **Competitive Recruiting Analysis**
```
Identify where competitors hire from:
- For each new hire: get previous companies
- Track talent pipelines
- Identify poaching patterns
```

**Expected Output**:
- Hiring velocity (hires per month/quarter)
- Department growth priorities
- Key hires and their backgrounds
- Leadership changes
- Talent pipeline insights

### Workflow 4: Content Strategy Benchmarking

**Scenario**: Analyze competitor content across platforms

**Steps**:

1. **LinkedIn Content**
```
get_linkedin_company_posts(urn, count=50)

Analyze:
- Posting frequency (posts/week)
- Content types (articles, videos, polls)
- Engagement rates (likes, comments, shares)
- Topics and themes
- Employee advocacy (shares/comments from team)
```

2. **Twitter/X Content**
```
get_twitter_user("competitor")
get_twitter_user_posts("competitor", count=100)

Analyze:
- Tweet frequency
- Engagement metrics
- Content themes
- Use of threads/media
- Response rates
```

3. **YouTube Content**
```
get_youtube_channel_videos("competitor", count=30)

For each video:
  get_youtube_video(video_id)

Analyze:
- Upload frequency
- View counts
- Engagement (likes, comments)
- Content types (demos, webinars, customer stories)
- Video length and production quality
```

4. **Instagram Content** (if B2C)
```
get_instagram_user("competitor")
get_instagram_user_posts("competitor", count=50)

Analyze:
- Post frequency
- Visual style/branding
- Engagement rates
- Use of Reels vs. static posts
- Influencer partnerships
```

5. **Blog/Website Content**
```
parse_webpage("https://competitor.com/blog")
get_sitemap("https://competitor.com")
→ Find all blog posts

Analyze:
- Publishing frequency
- Content topics
- SEO keywords
- Thought leadership positioning
```

6. **Community Sentiment**
```
search_reddit_posts(query="Competitor Inc", count=50)
search_reddit_posts(query="competitor product name", count=50)

Analyze:
- Customer feedback
- Common complaints
- Product strengths
- Feature requests
```

**Expected Output**:
- Cross-platform content strategy matrix
- Engagement benchmarks
- Content themes and messaging
- Platform prioritization insights
- Community sentiment summary

## MCP Tools Reference

### LinkedIn Company Intelligence

**search_linkedin_companies**
- Search for companies by keywords, location, industry, size
- Returns: Company list with basic info and URNs

**get_linkedin_company**
- Get detailed company profile
- Returns: Description, website, size, industry, specialties

**get_linkedin_company_employee_stats**
- Get employee statistics and growth
- Returns: Total employees, growth metrics, department distribution

**get_linkedin_company_posts**
- Get recent company posts
- Returns: Posts with engagement metrics, content, timestamps

### LinkedIn People Intelligence

**search_linkedin_users**
- Find employees at competitor companies
- Filter by title, department, location
- Returns: Employee profiles with titles and URLs

**get_linkedin_profile**
- Get detailed employee profile
- Returns: Work history, education, skills

**get_linkedin_user_experience**
- Get detailed work history
- Returns: All positions with dates and descriptions

### Y Combinator Intelligence

**search_yc_companies**
- Search YC companies by industry, batch, filters
- Returns: Company list with batch, team size, status

**get_yc_company**
- Get detailed YC company profile
- Returns: Description, founders, batch, status, links

**search_yc_founders**
- Search for founders by criteria
- Returns: Founder profiles with company associations

### Social Media Monitoring

**Twitter/X**:
- `search_twitter_posts` - Find competitor mentions
- `get_twitter_user` - Get competitor profile
- `get_twitter_user_posts` - Get recent tweets

**Instagram**:
- `search_instagram_posts` - Find hashtag/keyword mentions
- `get_instagram_user` - Get profile stats
- `get_instagram_user_posts` - Get recent posts

**Reddit**:
- `search_reddit_posts` - Find discussions about competitors
- `get_reddit_post` - Get post details and sentiment

**YouTube**:
- `search_youtube_videos` - Find competitor videos
- `get_youtube_channel_videos` - Get all channel videos
- `get_youtube_video` - Get video details and metrics

### Web Intelligence

**parse_webpage**
- Extract content from competitor websites
- Returns: Text content, links, contacts

**get_sitemap**
- Get all pages on competitor site
- Returns: URL list for comprehensive analysis

**duckduckgo_search**
- Search for competitor mentions across the web
- Returns: Search results with URLs and descriptions

## Output Formats

### Chat Summary

Provides competitive intelligence highlights:
- Key findings and insights
- Competitive threats identified
- Growth signals and strategic moves
- Recommended actions
- Top 3-5 competitors to watch

### CSV Export

Competitor comparison matrix with:
- Company name, size, location
- Employee count and growth rate
- Posting frequency and engagement
- Key differentiators
- Competitive threat score

### JSON Export

Complete competitive data for:
- Time-series tracking
- Dashboard visualization
- Automated monitoring
- Integration with BI tools

## Advanced Features

### Competitive Intelligence Dashboard

Track competitors over time by storing data and comparing:

**Monthly Snapshot**:
```json
{
  "date": "2026-01-29",
  "competitors": [
    {
      "name": "Competitor A",
      "employees": 350,
      "monthly_growth": 8,
      "open_positions": 25,
      "linkedin_posts": 12,
      "twitter_followers": 5400,
      "funding_stage": "Series B"
    }
  ]
}
```

**Trend Analysis**:
- Employee growth over 6 months
- Content output changes
- Positioning shifts
- Leadership changes

### SWOT Analysis Framework

**Strengths** (from LinkedIn, website, reviews):
- Team expertise (LinkedIn profiles)
- Product features (website, Reddit feedback)
- Market position (company size, growth)
- Brand recognition (social followers, engagement)

**Weaknesses** (from reviews, job postings, employee turnover):
- Customer complaints (Reddit, review sites)
- Hiring challenges (multiple re-postings)
- Employee turnover (LinkedIn departures)
- Product gaps (feature requests in forums)

**Opportunities** (from market analysis):
- Underserved segments (job posting patterns)
- Geographic expansion (new office locations)
- Product expansion (new roles, content themes)

**Threats** (from competitive monitoring):
- New entrants (YC batch analysis)
- Competitive hiring (talent poaching)
- Product launches (company posts, blogs)
- Pricing changes (website updates)

### Win/Loss Analysis

Track deals against specific competitors:

**Data Points to Collect**:
- Competitor encountered (company name)
- Deal stage (lost/won)
- Key differentiators discussed
- Pricing comparison
- Feature comparison
- Decision factors

**Intelligence Gathering**:
```
For each competitor in win/loss:
1. get_linkedin_company → Current positioning
2. parse_webpage(website + "/pricing") → Pricing strategy
3. parse_webpage(website + "/features") → Feature set
4. search_reddit_posts(competitor) → Customer feedback
5. get_linkedin_company_posts → Recent messaging
```

**Analysis**:
- Win rate by competitor
- Common objections
- Competitive advantages/disadvantages
- Pricing positioning
- Feature gaps

## Recommendations

**For Local/Retail Competitors**:
Focus on:
- LinkedIn company presence
- Instagram brand content
- Website location pages
- Reddit community discussions

**For Tech/SaaS Competitors**:
Excellent coverage through:
- LinkedIn (primary intelligence)
- Y Combinator (for startups)
- Twitter (tech community presence)
- Product Hunt mentions

**For Enterprise Competitors**:
- LinkedIn extremely comprehensive
- SEC filings for public companies
- Professional social presence
- Limited need for consumer platforms

## Reference Documentation

- **[ANALYSIS_PATTERNS.md](references/ANALYSIS_PATTERNS.md)** - Competitive analysis frameworks, SWOT templates, and intelligence gathering patterns

## Troubleshooting

### Issue: Competitor Not Found on LinkedIn

**Solution**:
- Try company name variations
- Search for employees and extract company
- Check if using DBA vs. legal name
- Try website domain search

### Issue: Limited Employee Data

**Solution**:
- Employees may have privacy settings
- Try searching by title without company filter
- Focus on public leadership team
- Use website team pages as alternative

### Issue: No Recent Company Posts

**Solution**:
- Company may not be active on LinkedIn
- Check Twitter/Instagram instead
- Use website blog for content analysis
- Focus on employee posts mentioning company

---

**Ready to analyze competitors?** Ask Claude to help you research competitors, track hiring patterns, or benchmark competitive positioning using this skill!
