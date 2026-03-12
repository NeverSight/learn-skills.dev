---
name: seo-content-strategy
description: Expert guide for content-driven SEO strategy. Use when doing keyword research, planning content clusters, analyzing search intent, building topic authority, evaluating E-E-A-T signals, creating content briefs, or planning content calendars for SEO.
---

# Content-Driven SEO Strategy

---

## Keyword Research Methodology

Keyword research is the foundation of every content strategy. The goal is not to find the highest-volume keyword — it is to find the right keywords that match your audience, intent, and competitive position.

### Seed Keyword Generation

Start with 5-10 seed keywords that define your core topic area. Sources:

| Source | Method |
|--------|--------|
| Product/service descriptions | Extract nouns and noun phrases from what you sell |
| Customer language | Pull terms from support tickets, reviews, sales calls |
| Competitor homepages | Identify category terms competitors target |
| Google Search Console | Export queries already driving impressions |
| Industry glossaries | Capture jargon your audience actually searches |

### Long-Tail Expansion

Expand each seed keyword into 20-50 long-tail variations:

```
Seed:       "project management software"
Long-tail:  "project management software for small teams"
            "free project management software with gantt charts"
            "project management software vs spreadsheet"
            "best project management software for agencies"
            "project management software with time tracking"
```

Expansion techniques:
- **Modifier stacking:** Add adjectives (best, free, cheap, top), qualifiers (for beginners, for enterprise), years (2025, 2026)
- **Autocomplete mining:** Type seed into Google and record all suggestions
- **People Also Ask:** Extract every PAA question from the first 3 SERPs
- **Alphabet soup:** Append a, b, c... z to the seed in autocomplete
- **Forum mining:** Search `site:reddit.com "seed keyword"` for real user phrasing

### Question Keywords

Question keywords are high-value for featured snippets and voice search:

| Prefix | Intent Signal | Example |
|--------|--------------|---------|
| How to | Process/tutorial | "how to set up a content calendar" |
| What is | Definition/explanation | "what is topic authority" |
| Why | Reasoning/justification | "why is keyword research important" |
| When | Timing/conditional | "when to update old blog posts" |
| Can/Does | Capability/feasibility | "can you rank without backlinks" |
| Which | Comparison/selection | "which keyword tool is most accurate" |

### Keyword Difficulty Assessment

| Difficulty Range | Interpretation | Typical Requirements |
|-----------------|----------------|---------------------|
| 0-20 | Very easy | New site can rank with solid on-page SEO |
| 21-40 | Easy | Good content + a few quality backlinks |
| 41-60 | Medium | Strong content + 10-30 referring domains |
| 61-80 | Hard | Authoritative site + strong backlink profile |
| 81-100 | Very hard | Major authority site + extensive link building |

### Search Volume Interpretation

- **0-100/mo:** Hyper-niche. Worth targeting only if high commercial value or part of a content cluster.
- **100-1,000/mo:** Sweet spot for most sites. Lower competition, decent traffic potential.
- **1,000-10,000/mo:** Competitive but achievable for established sites. Often good pillar page targets.
- **10,000+/mo:** Head terms. Rarely target directly — build toward them with cluster authority.

**MCP Tool:** Use `research_keywords` with your seed keyword to get volume, difficulty, and related keyword suggestions. Pass `expand: true` for long-tail generation.

---

## Search Intent Classification

Every keyword has a dominant search intent. Mismatching content format to intent is the #1 reason good content fails to rank.

### The Four Intent Types

| Intent | Goal | SERP Signals | Content Format |
|--------|------|-------------|----------------|
| **Informational** | Learn something | Featured snippets, PAA boxes, knowledge panels | Blog posts, guides, tutorials, videos |
| **Navigational** | Find a specific site/page | Sitelinks, brand knowledge panel | Homepage, product pages, login pages |
| **Commercial Investigation** | Compare before buying | Product carousels, review rich results, comparison tables | Reviews, comparisons, "best of" lists |
| **Transactional** | Complete an action/purchase | Shopping ads, product listings, price info | Product pages, pricing pages, sign-up pages |

### Signal Words by Intent

```
Informational:     how to, what is, why, guide, tutorial, learn, examples,
                   tips, ideas, definition, meaning, difference between

Navigational:      [brand name], [product name], login, sign in, homepage,
                   official site, contact, support, [brand] pricing

Commercial:        best, top, review, comparison, vs, alternative to,
                   [product] vs [product], pros and cons, which is better

Transactional:     buy, price, cheap, discount, coupon, order, download,
                   free trial, sign up, subscribe, hire, get quote
```

### SERP Feature Indicators

| SERP Feature | Dominant Intent |
|-------------|----------------|
| Featured snippet (paragraph) | Informational — definitional |
| Featured snippet (list/table) | Informational — process/comparison |
| People Also Ask | Informational |
| Knowledge panel | Navigational or Informational |
| Shopping results | Transactional |
| Local pack | Transactional (local) |
| Product carousels | Commercial investigation |
| Video carousel | Informational — how-to |
| Image pack | Varies — visual topics |
| Sitelinks | Navigational |

**MCP Tool:** Use `analyze_serp` with the target keyword to see what content types rank, which SERP features appear, and what intent Google is rewarding.

---

## Content Cluster Architecture

Content clusters build topical authority by creating a network of related content that demonstrates comprehensive coverage of a subject.

### Pillar Page Design

A pillar page is the authoritative hub for a broad topic:

| Element | Specification |
|---------|--------------|
| Word count | 3,000-5,000+ words |
| Target keyword | Broad, high-volume head term |
| Scope | Covers the entire topic at moderate depth |
| Internal links | Links OUT to every cluster page |
| Incoming links | Receives links FROM every cluster page |
| Format | Long-form guide with table of contents |
| Update frequency | Quarterly review and refresh |

### Cluster Topic Mapping

For each pillar, create 8-15 cluster pages that cover subtopics in depth:

```
PILLAR: "Content Marketing" (3,500 words)
  |
  +-- Cluster: "How to Create a Content Calendar" (1,800 words)
  +-- Cluster: "Content Marketing ROI Measurement" (2,000 words)
  +-- Cluster: "B2B Content Marketing Strategy" (2,200 words)
  +-- Cluster: "Content Repurposing Guide" (1,500 words)
  +-- Cluster: "Content Distribution Channels" (1,800 words)
  +-- Cluster: "Content Marketing Tools Comparison" (2,500 words)
  +-- Cluster: "Content Marketing for Startups" (1,800 words)
  +-- Cluster: "Content Brief Template" (1,200 words)
  +-- Cluster: "Content Marketing Metrics" (1,500 words)
  +-- Cluster: "Content Audit Process" (2,000 words)
```

### Internal Linking Strategy

| Link Direction | Purpose | Anchor Text |
|---------------|---------|-------------|
| Pillar -> Cluster | Passes authority to subtopics | Descriptive, keyword-rich |
| Cluster -> Pillar | Reinforces pillar as the hub | Broad topic keyword |
| Cluster -> Cluster | Connects related subtopics | Contextual, natural |

Rules:
- Every cluster page MUST link back to the pillar page
- The pillar page MUST link to every cluster page
- Cross-link between cluster pages where contextually relevant (aim for 2-3 cross-links per page)
- Use descriptive anchor text — never "click here" or "read more"
- Place links within body content, not just in sidebars or footers

### Siloing Strategy

Content silos separate your site into distinct topical sections:

```
Site Root
  |
  +-- /content-marketing/          (Pillar: Content Marketing Guide)
  |     +-- /content-calendar/     (Cluster page)
  |     +-- /content-roi/          (Cluster page)
  |     +-- /content-tools/        (Cluster page)
  |
  +-- /seo/                        (Pillar: SEO Guide)
  |     +-- /keyword-research/     (Cluster page)
  |     +-- /technical-seo/        (Cluster page)
  |     +-- /link-building/        (Cluster page)
```

- Keep URLs within the silo's path hierarchy
- Minimize cross-silo linking (keep it intentional, not random)
- Use breadcrumbs to reinforce silo structure
- Align navigation with silo architecture

---

## E-E-A-T Signals

Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) framework determines content quality for ranking, especially in YMYL (Your Money or Your Life) topics.

### Experience

Demonstrating first-hand experience with the topic:

| Signal | Implementation |
|--------|---------------|
| Personal anecdotes | "When I migrated 50 sites to HTTPS, the most common issue was..." |
| Original data | Publish your own studies, surveys, experiments |
| Process documentation | Show screenshots, step-by-step workflows from actual work |
| Case studies | Document real projects with specific metrics and outcomes |
| Product usage evidence | Hands-on reviews with original screenshots, not stock images |

### Expertise

Demonstrating deep knowledge of the subject:

| Signal | Implementation |
|--------|---------------|
| Author credentials | Display author bio with relevant qualifications |
| Depth of coverage | Cover edge cases, advanced concepts, not just basics |
| Technical accuracy | Use correct terminology, cite primary sources |
| Structured methodology | Present systematic frameworks, not just opinions |
| Author pages | Dedicated author pages with bio, credentials, published work |

### Authoritativeness

Being recognized as a go-to source:

| Signal | Implementation |
|--------|---------------|
| Backlinks from authorities | Earn links from recognized industry sites |
| Mentions/citations | Be cited by other experts and publications |
| Industry recognition | Awards, speaking engagements, certifications |
| Comprehensive coverage | Be the most complete resource on the topic |
| Brand search volume | People searching for "[your brand] + [topic]" |

### Trustworthiness

Building user and search engine trust:

| Signal | Implementation |
|--------|---------------|
| HTTPS | Mandatory for all pages |
| Contact information | Clear contact page, physical address, phone number |
| Privacy policy | Comprehensive, accessible privacy policy |
| Editorial policy | Transparent editorial standards and fact-checking process |
| Citations | Link to primary sources, studies, official documentation |
| Corrections | Publish corrections when errors are found |
| Reviews/testimonials | Display genuine user reviews with dates |

### YMYL Considerations

YMYL topics require the highest E-E-A-T standards. YMYL categories include:

- **Health & safety:** Medical advice, drug information, mental health
- **Financial:** Investment advice, tax information, loans, insurance
- **Legal:** Legal advice, citizenship, divorce, custody
- **News:** Current events, politics, science, technology
- **Shopping:** Product safety, large purchases
- **Groups of people:** Information about protected groups

For YMYL content: require author credentials, cite medical/legal/financial sources, include disclaimers, get expert review, and maintain strict accuracy standards.

---

## Content Brief Creation

A content brief ensures every piece of content is strategically aligned before writing begins.

### Content Brief Template

```
CONTENT BRIEF
=============

Target keyword:        [primary keyword]
Search volume:         [monthly search volume]
Keyword difficulty:    [0-100 score]
Search intent:         [informational / commercial / transactional / navigational]

Secondary keywords:    [3-8 related keywords to include naturally]
Question keywords:     [2-5 questions to answer in the content]

Content type:          [blog post / guide / comparison / review / landing page]
Word count target:     [based on top-ranking competitor average + 20%]
Target URL:            [/planned-url-slug]

Top 3 competitor URLs:
  1. [url] — [word count] — [strengths/gaps]
  2. [url] — [word count] — [strengths/gaps]
  3. [url] — [word count] — [strengths/gaps]

Heading outline:
  H1: [title with primary keyword]
  H2: [section — secondary keyword]
    H3: [subsection]
    H3: [subsection]
  H2: [section — secondary keyword]
  H2: [FAQ section — question keywords]

Required elements:
  [ ] Table of contents
  [ ] At least 2 original images/diagrams
  [ ] At least 1 data table
  [ ] Internal links to: [list cluster pages]
  [ ] External links to: [2-3 authoritative sources]
  [ ] Author bio with credentials
  [ ] FAQ section with schema markup

Notes for writer:
  - [Specific angle or unique value proposition]
  - [Tone and audience notes]
  - [Topics to avoid or include]
```

**MCP Tool:** Use `analyze_serp` for the target keyword to inform competitor analysis. Use `analyze_page` on top-ranking URLs to extract their heading structures and content patterns.

---

## Content Gap Analysis

Content gap analysis reveals topics your competitors cover that you do not.

### Process

1. **Identify competitors:** Select 3-5 direct organic competitors (sites ranking for your target keywords, not just business competitors)
2. **Map their content:** Catalog every piece of content on their site relevant to your niche
3. **Compare coverage:** Identify topics they cover that you have not addressed
4. **Assess opportunity:** Score each gap by search volume, difficulty, and business relevance
5. **Prioritize:** Build a content calendar starting with highest-impact gaps

### Gap Categories

| Gap Type | Description | Action |
|----------|-------------|--------|
| Topic gap | Competitor covers a topic you have not written about | Create new content |
| Depth gap | You cover the topic but competitor goes deeper | Expand existing content |
| Freshness gap | Your content is outdated, competitor's is current | Update existing content |
| Format gap | Competitor uses a better format (video, tool, interactive) | Reformat or supplement |
| Intent gap | Your content targets wrong intent for the keyword | Rewrite with correct intent |

**MCP Tool:** Use `analyze_page` on competitor URLs to extract their heading structures, topics covered, and content depth. Compare against your own content inventory.

---

## Content Freshness and Update Strategy

### When to Update vs. Create New

| Scenario | Action |
|----------|--------|
| Existing page ranks positions 5-20 | **Update** — improve content, add sections, refresh data |
| Existing page ranks positions 21-50 | **Update** — significant expansion, re-optimize for intent |
| Existing page ranks 50+ or not at all | **Evaluate** — may need complete rewrite or new angle |
| No existing page for the keyword | **Create new** content |
| Topic has evolved significantly | **Create new** page targeting updated angle, redirect old if needed |
| Page has strong backlink profile but poor content | **Update** — preserve URL and links, improve content |

### Historical Optimization Process

1. **Audit existing content:** Pull all pages from Google Search Console with declining impressions or CTR
2. **Identify decay candidates:** Pages that lost 20%+ traffic over 6 months
3. **Re-analyze SERP:** Check what currently ranks — has intent shifted?
4. **Update content:** Refresh statistics, add new sections, update examples and screenshots
5. **Update publish date:** Only after making substantial changes (not cosmetic edits)
6. **Resubmit to Google:** Request re-indexing via Search Console after major updates

### Content Calendar Cadence

| Content Type | Creation Frequency | Update Frequency |
|-------------|-------------------|-----------------|
| Pillar pages | 1-2 per quarter | Quarterly review |
| Cluster pages | 4-8 per month | Every 6-12 months |
| News/trend content | As needed | Rarely (time-sensitive) |
| Evergreen guides | 2-4 per month | Annually |
| Data studies | 1-2 per year | Annually (new data) |

---

## Related Skills

- **seo-on-page-optimization** — for optimizing individual page elements (titles, headings, meta)
- **seo-technical-audit** — for crawlability, indexing, and site speed issues
- **seo-schema-structured-data** — for adding FAQ, HowTo, Article, and other schema types
- **seo-off-page-backlinks** — for link building strategy to support content authority
- **seo-local-seo** — for location-based content strategy
- **seo-mcp-tools-expert** — for detailed MCP tool usage patterns

## Key MCP Tools for Content Strategy

| Tool | Use For |
|------|---------|
| `research_keywords` | Keyword discovery, volume/difficulty data, related keywords |
| `analyze_serp` | SERP feature detection, intent analysis, competitor identification |
| `analyze_page` | Content analysis, heading extraction, word count, on-page audit |

See [KEYWORD_RESEARCH_GUIDE.md](KEYWORD_RESEARCH_GUIDE.md) for the complete keyword research process.
See [CONTENT_CLUSTER_TEMPLATES.md](CONTENT_CLUSTER_TEMPLATES.md) for 5 ready-to-use cluster templates.
See [SEARCH_INTENT_PATTERNS.md](SEARCH_INTENT_PATTERNS.md) for the full intent classification reference.
