---
name: meta-optimizer
version: 1.0.0
description: "Optimize title tags and meta descriptions for CTR and rankings. Analyzes current meta tags, generates SERP previews, and suggests improvements based on keyword targeting, character limits, and competitor patterns."
---

# Meta Optimizer

Rewrite title tags and meta descriptions to improve click-through rates and keyword targeting. Analyze single pages or batch-process entire sites.

## When to Use

- Launching new pages that need meta tags
- Auditing existing pages with low CTR in GSC
- After a keyword mapping update changes target keywords
- Competitor analysis reveals better title patterns in SERPs
- Post-migration to verify no meta tags were lost or duplicated

## Inputs

Ask the user for:

1. **Target URL(s)**: Single URL, list of URLs, or sitemap URL for batch processing
2. **Target keyword per URL**: The primary keyword each page should rank for
3. **Secondary keywords** (optional): Additional terms to weave in naturally
4. **Brand name**: For consistent brand suffix formatting
5. **Brand position preference**: End (default) or omit entirely

If the user provides a sitemap URL, parse it and extract all `<loc>` entries. If they provide a CSV or list, process each row.

## Title Tag Rules

### Character Limits
- **Target**: 50-60 characters (Google truncates at ~600px width, roughly 60 chars)
- **Minimum**: 30 characters (shorter titles look thin in SERPs)
- Count characters precisely. Flag any title over 60 or under 30.

### Keyword Placement
- Primary keyword within the first 40 characters
- Front-load the keyword when possible without sacrificing readability
- Never repeat the exact keyword twice in a title

### Structure Patterns (ranked by typical CTR impact)
1. **Keyword + Modifier + Brand**: `Technical SEO Audit Checklist (2026) | Brand`
2. **Number + Keyword + Benefit**: `13 SEO Skills That Cut Audit Time by 60%`
3. **How-to + Keyword**: `How to Fix Crawl Budget Waste in 30 Minutes`
4. **Keyword + Comparison**: `Screaming Frog vs Claude Code for Site Audits`

### CTR Boosters
- **Numbers**: Specific numbers outperform ranges ("13" beats "10+")
- **Brackets/Parentheses**: `[Template]`, `(2026)`, `[Free Tool]` add 33% CTR lift per HubSpot research
- **Power words**: Free, New, Proven, Complete, Step-by-Step, Ultimate, Fast
- **Year**: Append current year for queries where freshness matters (reviews, stats, tools)
- **Emotional modifiers**: Avoid clickbait but use curiosity ("surprising", "overlooked", "hidden")

### Common Mistakes to Flag
- **Brand-first titles**: `Brand | Keyword Here` wastes prime keyword real estate
- **Keyword stuffing**: `SEO Tools - Best SEO Tools for SEO Professionals` reads as spam
- **Duplicate titles**: Multiple pages with identical or near-identical titles
- **Truncation**: Titles over 60 chars that cut off mid-word in SERPs
- **Missing intent match**: Informational title for a transactional page
- **Boilerplate**: Same template across all pages (`Blog - Brand` on every post)

## Meta Description Rules

### Character Limits
- **Target**: 150-160 characters (Google truncates at ~920px width)
- **Minimum**: 120 characters (shorter descriptions get replaced by Google's auto-generated snippet)

### Content Requirements
- Include the primary keyword naturally (Google bolds matching terms in SERPs)
- State the value proposition: what does the reader get from this page?
- End with an implicit or explicit call to action
- Write in active voice
- Make it specific to the page content, not generic

### Structure Pattern
`[What the page covers] + [What the reader gains] + [CTA or differentiator]`

Example: `Run a full technical SEO audit in Claude Code's terminal. Covers crawl errors, Core Web Vitals, schema validation, and internal links. Free skill included.`

### Common Mistakes to Flag
- **Duplicate descriptions**: Same description across multiple pages
- **Missing descriptions**: No meta description tag at all (Google generates one, often poorly)
- **Keyword stuffing**: Forcing the keyword 3+ times into 160 characters
- **Too vague**: "Learn more about SEO on our website" tells the searcher nothing
- **Cut-off sentences**: Description truncates mid-thought

## SERP Preview Generation

For each URL analyzed, generate a visual SERP preview in this format:

```
[SERP Preview]
Title:  Technical SEO Audit With Claude Code (Free Skill) | ccforseo
        ─────────────────────────────────────────────────────────────
URL:    ccforseo.com/skills/seo-audit
Desc:   Run a complete technical SEO audit from your terminal. Covers
        crawl errors, Core Web Vitals, schema, and internal links.
        Free Claude Code skill included.
Chars:  Title: 57 | Description: 152
Status: Title: OK | Description: OK
```

Flag any issues:
- `TRUNCATED` if over character limit
- `TOO SHORT` if under minimum
- `MISSING KEYWORD` if primary keyword absent
- `DUPLICATE` if another page shares the same title or description

## Intent Alignment Check

Before suggesting a title, verify the search intent of the target keyword:

1. **Informational** ("what is", "how to", "guide"): Title should promise learning/answers
2. **Navigational** (brand + feature): Title should include the brand prominently
3. **Transactional** ("buy", "pricing", "tool"): Title should include value props, pricing signals
4. **Commercial investigation** ("best", "vs", "review"): Title should include comparisons, numbers

If the current title targets a different intent than the keyword implies, flag it as a mismatch.

## Competitor Title Analysis

For each target keyword:

1. Search Google for the keyword (or use provided SERP data)
2. Extract titles from the top 10 ranking pages
3. Identify patterns:
   - What modifiers do top results use? (year, numbers, brackets)
   - How long are their titles?
   - Where do they place the keyword?
   - Do they use brand names?
4. Find gaps: what angle are competitors NOT using that could differentiate?

Present as:

```
Competitor Title Analysis: "claude code seo audit"

| Rank | Title                                          | Chars | Keyword Position | Modifiers     |
|------|------------------------------------------------|-------|-----------------|---------------|
| 1    | How to Run SEO Audits With Claude Code          | 43    | Position 4      | How-to        |
| 2    | Claude Code SEO Audit: Complete Guide (2026)    | 47    | Position 1      | Year, Guide   |
| 3    | Technical SEO Auditing in the Terminal           | 42    | Position 3      | None          |

Gap: No results use numbers or templates. Opportunity: "13-Point SEO Audit Template for Claude Code"
```

## Batch Processing

When given multiple URLs:

1. Crawl or fetch each URL's current `<title>` and `<meta name="description">`
2. Analyze all at once
3. Flag cross-page issues: duplicates, cannibalization of keywords across titles
4. Output a single table

### Output Table Format

```
| URL | Current Title | Suggested Title | Chars | Current Description | Suggested Description | Chars | Target Keyword | Issues |
|-----|--------------|-----------------|-------|--------------------|-----------------------|-------|---------------|--------|
| /blog/seo-audit | Blog - Brand | Technical SEO Audit With Claude Code | 38 | (missing) | Run a full technical audit... | 148 | seo audit claude code | Missing desc, Brand-first |
```

## A/B Testing Recommendations

For high-traffic pages (1,000+ monthly impressions in GSC), suggest A/B title tests:

1. **Control**: Current title
2. **Variant A**: Front-loaded keyword version
3. **Variant B**: Number/bracket CTR booster version

Provide the test hypothesis:
- "Adding [2026] to the title should increase CTR by 5-15% for freshness-sensitive queries"
- "Moving the keyword to position 1 should improve both rankings and CTR"

Recommend running each test for 2-4 weeks with enough impression volume for statistical significance. Use GSC's performance report filtered by page to measure CTR changes.

## Cross-References

- Use **keyword-cluster** output as the source for target keywords per page
- Use **seo-audit** to find pages with missing or duplicate meta tags at scale
- Use **cannibalization** to detect pages competing for the same keyword in titles
- Use **content-brief** to align title/description with the full content strategy for a page
- Feed optimized titles into **schema-gen** for consistent `headline` fields in Article schema

## Example Session

```
User: Optimize meta tags for these 3 URLs targeting these keywords:
- /blog/site-audit → "claude code seo audit"
- /blog/keyword-research → "keyword research claude code"
- /skills → "claude code seo skills"

Assistant analyzes current tags, generates SERP previews, checks competitors,
and outputs the recommendation table with suggested titles, descriptions,
character counts, and flagged issues.
```
