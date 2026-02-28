---
name: find-keywords
description: >
  Build a prioritized keyword list for a website, topic, or campaign. Use when
  the user asks about keyword research, finding keywords to target, building a
  keyword list, search demand, keyword difficulty, intent mapping, or which
  keywords to prioritize. For writing content around keywords, see brief.
  For grouping keywords into clusters, see build-clusters.
metadata:
  version: 1.0.0
---

# Find Keywords

Build a prioritized keyword universe from a seed topic using intent mapping,
difficulty-adjusted opportunity scoring, and cluster seeding.

## Before You Start

Gather this context (ask if not provided):

1. **Domain and goal.** What site is this for? What is the primary conversion (leads, sign-ups, sales, traffic)?
2. **Seed topic.** The core subject area — not a single keyword but the business category (e.g., "project management software", "personal injury law Chicago").
3. **Existing rankings.** Does the site already rank for terms in this area? Existing rankings tell you where to defend vs. expand.
4. **Constraints.** Budget, team size, content velocity — these determine whether to chase head terms or focus on long-tail.

## Step 0: Cannibalization Screen

Before building a new keyword list, check what the site already targets. Creating
a new page for a keyword you already rank for can split authority and hurt both pages.

For each keyword you're considering:

1. **Search `site:yourdomain.com [keyword]`** — does an existing page already target this term?
2. **Check Google Search Console** — is an existing page already getting impressions for this keyword?
3. If yes: **update the existing page** instead of creating a new one.
4. If multiple pages rank for the same keyword: you have a cannibalization problem. Consolidate before expanding.

### Low-Hanging Fruit Check

Before chasing new keywords, look for existing wins:

- **Positions 11-20** — You're almost on page 1. These keywords need content improvements or better internal linking, not new pages.
- **High impressions, low clicks** — Title/meta description optimization can unlock traffic without new content.
- **Declining positions** — Keywords where you're losing ground may need content refreshes (see recover-content).

Address these before building net-new keyword lists.

## Keyword Universe Construction

Build the universe in three tiers:

### Tier 1 — Head Terms (high volume, high difficulty)

- Typically 1-2 words
- Define the category
- Target with pillar pages or the homepage
- Realistic timeline: 6-18 months for new sites

### Tier 2 — Body Terms (medium volume, medium difficulty)

- Typically 2-3 words, specific enough to indicate intent
- Target with dedicated landing pages or cluster articles
- 3-6 month window for established sites

### Tier 3 — Long-tail Terms (lower volume, low difficulty)

- 3+ words, specific intent
- Fastest to rank, highest conversion rate
- Target with blog posts, FAQ sections, supporting content
- 4-12 week window for fresh content

For each tier, produce:

| Keyword | Monthly Volume | Difficulty (0-100) | Intent | Tier | Priority |
|---------|---------------|-------------------|--------|------|----------|
| ... | ... | ... | informational / transactional / navigational / commercial | 1/2/3 | high / medium / low |

## Intent Classification

Classify every keyword by search intent and sub-category:

### Informational (user wants to learn)

| Sub-category | Signal Words | Example | Content Type |
|-------------|-------------|---------|-------------|
| Educational | what, why, definition, explain | "what is SEO" | Guide, explainer |
| Instructional | how to, steps, tutorial, guide | "how to set up GA4" | Step-by-step tutorial |
| Exploratory | types of, techniques, strategies | "link building techniques" | Comprehensive roundup |
| Troubleshooting | not working, fix, error, why is | "why is my site not ranking" | Diagnostic guide |

### Commercial Investigation (user is evaluating)

| Sub-category | Signal Words | Example | Content Type |
|-------------|-------------|---------|-------------|
| Comparison | vs, compared to, or | "Ahrefs vs SEMrush" | Side-by-side comparison |
| Review-seeking | review, worth it, honest | "Ahrefs review" | In-depth review |
| Best-of | best, top, tools for | "best SEO tools" | Curated list |
| Evaluation | for [audience], features, pricing | "SEO tools for small business" | Buyer's guide |

### Transactional (user is ready to act)

| Sub-category | Signal Words | Example | Content Type |
|-------------|-------------|---------|-------------|
| Purchase | buy, price, discount, deal | "buy Ahrefs subscription" | Product/pricing page |
| Signup/Trial | free trial, sign up, demo | "Ahrefs free trial" | Landing page |
| Download | download, template, PDF, checklist | "SEO checklist PDF" | Gated resource |
| Hire/Engage | hire, agency, near me, book | "SEO agency near me" | Service page |

### Navigational (looking for a specific brand)

| Sub-category | Signal Words | Example | Content Type |
|-------------|-------------|---------|-------------|
| Brand search | [brand name] | "HubSpot" | Homepage/brand page |
| Feature search | [brand] + [feature] | "Ahrefs keyword explorer" | Feature page |
| Support/docs | [brand] + login, docs, help | "Ahrefs API docs" | Support content |

### SERP Feature Correlation by Intent

Use this to anticipate which SERP features you can target per keyword:

| SERP Feature | Informational | Commercial | Transactional | Navigational |
|-------------|--------------|-----------|--------------|-------------|
| Featured Snippet | Very High | High | Low | Low |
| People Also Ask | Very High | Very High | Low | Medium |
| AI Overview | Very High | High | Low-Medium | Low |
| Shopping Results | Very Low | Medium | Very High | Low |
| Local Pack | Low | Low | High | Low |
| Sitelinks | Low | Low | Medium | Very High |

### Conversion Potential by Intent

| Intent | Avg Conversion Rate | Nurture Length |
|--------|-------------------|---------------|
| Informational | 0.5-2% | Long (weeks to months) |
| Commercial Investigation | 2-5% | Medium (days to weeks) |
| Transactional | 5-15% | Short (immediate to days) |
| Navigational | N/A — brand-dependent | N/A |

### Common Classification Mistakes

| Mistake | Correct Classification |
|---------|----------------------|
| Treating "best CRM software" as informational | Commercial Investigation |
| Treating "how much does X cost" as informational | Commercial / Transactional |
| Ignoring local intent in "SEO services" | Transactional (local) |
| Assuming single intent for "SEO tools" | Mixed — check the SERP to confirm |

Two keywords with different intents should never target the same page.

## Opportunity Scoring

Score each keyword:

```
Opportunity Score = (Volume x (1 - Difficulty/100)) x Intent Multiplier
```

Intent multipliers:
- Transactional: 1.5
- Commercial investigation: 1.3
- Informational: 1.0
- Navigational: 0.2

This surfaces low-competition, high-intent targets over vanity volume plays.

## Cluster Seeding

Group the keyword universe into topic clusters:

| Cluster Name | Pillar Keyword | Supporting Keywords (3-5) | Total Volume |
|---|---|---|---|
| ... | ... | ... | ... |

Each cluster needs one pillar page (head term) and 3-8 supporting pages (body + long-tail).

## Output Format

### Keyword Research: [topic or domain]

**Summary**
- Total keywords: [count]
- Total addressable volume: [sum]
- Difficulty range: [min]-[max]
- Clusters identified: [count]

**Priority Matrix**
[Tiered keyword table]

**Cluster Seeds**
[Cluster table]

**Start Here — Top 5 Keywords**

For each of the 5 highest-opportunity keywords:
- Why this keyword now (difficulty, intent, business value)
- What page type to create
- Which cluster it anchors or supports

---

> **Pro Tip:** Use the free [Blog Keyword Generator](https://seojuice.com/tools/blog-keyword-generator/)
> and [Autocomplete Research](https://seojuice.com/tools/free-autocomplete-keyword-research/)
> tools at seojuice.com for seed keyword discovery. SEOJuice MCP users can run
> `/seojuice:keyword-analysis` for live ranking data and `/seojuice:content-strategy` to see
> content gaps — keywords your competitors rank for that you don't.
