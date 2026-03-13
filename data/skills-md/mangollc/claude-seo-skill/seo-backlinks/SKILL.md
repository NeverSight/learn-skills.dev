---
name: seo-backlinks
description: |
  Backlink analysis and link building strategy: competitor backlink profiling, outreach plan
  generation, monthly SEO reporting framework, toxic link identification, link opportunity
  scoring, and unlinked mention discovery.

  USE FOR:
  - "backlinks", "link building", "outreach", "link profile"
  - "competitor backlinks", "who links to my competitors"
  - "toxic links", "disavow", "link audit", "spammy links"
  - "outreach plan", "link building strategy", "link opportunities"
  - "SEO report", "monthly report", "reporting template"
  - "unlinked mentions", "brand mentions without links"

  Uses firecrawl to research competitor link sources and find outreach targets.
  Multi-client: stores results in .seo/clients/{client}/backlinks/
---

# Backlinks & Reporting

Load client context first. See seo-keywords [rules/client-setup.md](../seo-keywords/rules/client-setup.md).

## File Organization

```
backlinks/
├── competitor-profiles/
│   └── {competitor-slug}.json     # Per-competitor backlink data
├── opportunities.json             # Scored link opportunities
├── outreach-plan-{date}.json      # 90-day outreach plan
├── toxic-links.json               # Toxic backlink report
├── unlinked-mentions.json         # Brand mentions without links
└── disavow.txt                    # Google disavow file format

reports/
├── monthly-{year}-{month}.md      # Monthly SEO reports
└── quarterly-{year}-q{n}.md       # Quarterly summaries
```

## Competitor Backlink Profiling

For each competitor in client config, discover their link sources:

```bash
# Find pages linking to competitor
firecrawl search "link:{competitor-domain}" --limit 50 -o .seo/clients/{slug}/backlinks/.firecrawl/links-{comp}.json --json &

# Find brand mentions (potential link sources)
firecrawl search "\"{competitor-name}\" -{competitor-domain}" --limit 30 -o .seo/clients/{slug}/backlinks/.firecrawl/mentions-{comp}.json --json &

# Find guest posts by competitor
firecrawl search "\"{competitor-name}\" guest post OR contributed by OR written by" --limit 20 -o .seo/clients/{slug}/backlinks/.firecrawl/guest-{comp}.json --json &

wait
```

**For each discovered link source, analyze:**
- Source domain and page
- Link context: editorial mention, directory listing, guest post, resource page, forum, comment
- Anchor text used
- Follow vs nofollow
- Topical relevance to client's industry
- Domain signals: established site vs thin/spammy

### Output Format

```json
{
  "competitor": "Competitor Name",
  "domain": "competitor.com",
  "link_sources": [
    {
      "source_url": "https://referring-site.com/article",
      "source_domain": "referring-site.com",
      "link_type": "editorial|guest-post|directory|resource-page|forum|comment|partnership",
      "anchor_text": "anchor text used",
      "follow": true,
      "relevance": "high|medium|low",
      "replicable": true,
      "notes": "Blog post about industry topic, could pitch similar content"
    }
  ],
  "summary": {
    "total_sources_found": 45,
    "editorial_links": 20,
    "guest_posts": 8,
    "directories": 10,
    "resource_pages": 5,
    "other": 2
  }
}
```

## Link Opportunity Scoring

Score each prospect on a 0-100 scale across 4 dimensions:

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **Relevance** | 25 pts | Industry match, topical alignment, audience overlap |
| **Authority** | 25 pts | Domain reputation, traffic indicators, content quality |
| **Achievability** | 25 pts | Accepts guest posts? Has resource pages? Responded to outreach before? Open contact info? |
| **Traffic Potential** | 25 pts | Referral traffic value, audience size, social engagement |

**Priority tiers:**
- **Tier 1** (75-100): Pursue immediately — high relevance + achievable
- **Tier 2** (50-74): Include in outreach plan — good potential
- **Tier 3** (25-49): Secondary targets — nice to have
- **Tier 4** (0-24): Skip — low value or unachievable

## 90-Day Outreach Plan

### Phase 1: Low-Hanging Fruit (Days 1-30)

**Targets:**
- Directories and listings the client is missing but competitors have
- Unlinked brand mentions (found via mention search — just need to ask for a link)
- Broken link opportunities: find 404 links on resource pages, offer client content as replacement
- Industry associations and chamber of commerce listings
- Existing relationships (partners, vendors, clients who could link)

**Actions:**
- Submit to 10-15 relevant directories
- Send personalized outreach to 10 unlinked mention sites
- Find 5-10 broken link opportunities
- Claim all relevant association listings

### Phase 2: Content-Based Link Building (Days 31-60)

**Targets:**
- Guest post opportunities on industry blogs
- Resource page inclusion (sites with "resources" or "useful links" pages)
- HARO / journalist queries (Help a Reporter Out)
- Podcast guest appearances
- Expert roundup participation

**Actions:**
- Pitch 15-20 guest post targets (send personalized pitch with topic ideas)
- Submit client content to 10 resource pages
- Sign up for HARO and respond to 2-3 relevant queries per week
- Identify 5 industry podcasts accepting guests

### Phase 3: Digital PR & Partnerships (Days 61-90)

**Targets:**
- Data-driven content / original research that earns links naturally
- Infographics and visual assets for link bait
- Strategic partnerships with complementary businesses
- Local sponsorships and community involvement
- Industry award submissions

**Actions:**
- Create 1-2 pieces of link-worthy content (data study, tool, comprehensive guide)
- Develop 2-3 partnership link exchanges with complementary businesses
- Submit to 5 industry award programs
- Sponsor or participate in 2 local/industry events

### Outreach Email Templates

**Guest Post Pitch:**
```
Subject: Content idea for {site_name}: {topic}

Hi {editor_name},

I noticed {site_name} covers {topic area} and thought your readers might enjoy an article on {specific topic idea}.

I'm {author_name}, {brief credential}. I'd cover:
- {Point 1}
- {Point 2}
- {Point 3}

I'll make sure the piece is original, well-researched, and a great fit for your audience. Would this be of interest?

{name}
{title}, {company}
```

**Unlinked Mention:**
```
Subject: Thanks for mentioning {brand}!

Hi {name},

I noticed you mentioned {brand} in your article "{article title}" — thank you!

Would you mind adding a quick link to {url} where you reference us? It helps our readers find us and would be a nice complement to your article.

Thanks!
{name}
```

**Broken Link:**
```
Subject: Broken link on {page title}

Hi {name},

I was reading your helpful resource page "{page title}" and noticed the link to {broken resource} appears to be broken (returns a 404).

We have a similar resource at {client url} that covers the same topic. Would you consider updating the link?

{name}
```

## Toxic Backlink Identification

Search for links that could harm the client:

```bash
firecrawl search "link:{client-domain}" --limit 100 -o .seo/clients/{slug}/backlinks/.firecrawl/all-links.json --json
```

**Toxic link patterns to flag:**
- PBN characteristics: thin content, generic design, excessive outbound links, exact-match anchor domains
- Spammy directories: low-quality directories with no editorial standards
- Irrelevant foreign-language sites linking with keyword anchor text
- Comment spam: links from blog comments or forums
- Link farms: sites that exist solely to sell/exchange links
- Excessive exact-match anchors: unnatural anchor text profile

### Disavow File Format

```
# Toxic backlinks identified on {date}
# Client: {client_name}
# Domain: {client_domain}

# Individual URLs
https://spammy-site.com/page-with-link
https://another-spam.com/article

# Entire domains
domain:spam-domain.com
domain:link-farm.net
```

## Unlinked Mention Discovery

Find brand mentions without links:

```bash
# Search for brand mentions excluding own site
firecrawl search "\"{brand_name}\" -{client-domain}" --limit 50 -o .seo/clients/{slug}/backlinks/.firecrawl/brand-mentions.json --json

# Also search for common misspellings or variations
firecrawl search "\"{brand_variation}\" -{client-domain}" --limit 20 -o .seo/clients/{slug}/backlinks/.firecrawl/brand-variations.json --json
```

For each mention, scrape the page to verify:
1. The mention exists and is relevant
2. No link to client domain already exists
3. The context is positive or neutral (not a complaint)
4. The site is worth pursuing (not spammy)

## Monthly Reporting Framework

Generate a reusable monthly report covering all SEO activities and results.

### Report Template Structure

```markdown
# Monthly SEO Report — {Month} {Year}
## {Client Name} | {Domain}

Prepared by {Agency Name} | {Date}

---

## Executive Summary
{2-3 sentences: key wins, changes in performance, top priority for next month}

## Technical Health
- Overall Score: {score}/100 (vs {previous_score}/100 last month)
- Issues Fixed: {count}
- New Issues Found: {count}
- Top remaining issue: {description}

## Keyword Performance
- Total keywords tracked: {count}
- Keywords in top 10: {count} ({change} vs last month)
- Keywords in top 3: {count} ({change} vs last month)
- New keyword opportunities identified: {count}
- Top keyword wins: {list top 3 improvements}

## Content
- New pages published: {count}
- Pages optimized/refreshed: {count}
- Average on-page score: {score}/100
- Content gaps remaining: {count}

## Local SEO (if applicable)
- GBP posts published: {count}
- GBP views: {metric if available}
- New reviews: {count} (avg rating: {stars})
- Citations updated: {count}

## Backlinks
- New links acquired: {count}
- Links lost: {count}
- Outreach emails sent: {count}
- Response rate: {percent}
- Top new links: {list top 3}

## AI Search Visibility (AEO)
- AI Overview appearances: {observed/not observed}
- Brand mentions in AI results: {count}
- Schema markup coverage: {percent of pages}

## Priorities for Next Month
1. {Priority 1}
2. {Priority 2}
3. {Priority 3}

---

## Appendix: Detailed Data
{Link to JSON data files in .seo/ directory}
```

### Report Generation Steps

1. Load all data from `.seo/clients/{slug}/` subdirectories
2. Compare against previous month's data (if available)
3. Calculate trends and changes
4. Highlight wins and regressions
5. Generate action items for next month
6. Save to `.seo/clients/{slug}/reports/monthly-{year}-{month}.md`
