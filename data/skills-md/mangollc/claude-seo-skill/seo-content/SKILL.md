---
name: seo-content
description: |
  Content optimization for SEO: on-page scoring (0-100), E-E-A-T analysis, title/meta
  optimization, heading structure, keyword density, SERP preview, content readability,
  featured snippet optimization, content gap and decay detection, pre-publish checklists.

  USE FOR:
  - "optimize this page", "content score", "on-page SEO", "page score"
  - "title tag", "meta description", "heading structure"
  - "E-E-A-T", "content quality", "content audit"
  - "pre-publish checklist", "before I publish"
  - "content gap", "what content should I create"
  - "keyword density", "content optimization"
  - "SERP preview", "how does this look in Google"
  - "featured snippet", "position zero"
  - "content decay", "stale content", "refresh content"
  - "readability", "Flesch-Kincaid"

  Uses firecrawl to scrape pages for analysis.
  Multi-client: stores results in .seo/clients/{client}/content/
---

# Content Optimization

Load client context first. See seo-keywords [rules/client-setup.md](../seo-keywords/rules/client-setup.md).

## File Organization

```
content/
├── page-scores/
│   └── {url-slug}-score.json      # Individual page scores
├── content-gaps.json              # Gap analysis
├── content-decay.json             # Decay detection results
├── cannibalization.json           # Pages competing for same keywords
├── pre-publish-checklist.md       # Reusable checklist template
└── serp-previews/
    └── {url-slug}-preview.md      # SERP preview renders
```

## On-Page SEO Scoring (0-100)

Scrape the target page:

```bash
firecrawl scrape {url} --format markdown,links -o .seo/clients/{slug}/content/.firecrawl/page-{slug}.json
firecrawl scrape {url} --html -o .seo/clients/{slug}/content/.firecrawl/page-{slug}.html
```

### Scoring Rubric

| Category | Points | Checks |
|----------|--------|--------|
| **Title Tag** | 15 | Length 50-60 chars (deduct 5 if outside range), primary keyword in first half (5 pts), unique across site (5 pts), SERP truncation safe (5 pts) |
| **Meta Description** | 10 | Length 120-155 chars (deduct 5 if outside), contains keyword (3 pts), has CTA/action word (4 pts), unique (3 pts) |
| **H1 Tag** | 10 | Exactly one H1 (5 pts), contains primary keyword (5 pts) |
| **Heading Hierarchy** | 10 | Proper H1>H2>H3 nesting with no skipped levels (5 pts), keywords in at least 2 subheadings (3 pts), sufficient subheadings for content length (2 pts) |
| **Content Depth** | 15 | Word count >= avg of top 5 competitors (8 pts), covers all major subtopics (7 pts) |
| **Keyword Usage** | 10 | Density 1-2% (4 pts), keyword in first 100 words (3 pts), LSI/semantic variations used (3 pts) |
| **Internal Links** | 10 | Min 3 internal links (4 pts), relevant anchor text (3 pts), links to pillar/related content (3 pts) |
| **Image Optimization** | 10 | All images have alt text (4 pts), descriptive filenames (2 pts), modern format WebP/AVIF (2 pts), lazy loading on below-fold (2 pts) |
| **URL Structure** | 5 | Short slug < 60 chars (2 pts), contains keyword (2 pts), no parameters/IDs (1 pt) |
| **Social Meta** | 5 | og:title + og:description + og:image present (3 pts), twitter:card present (2 pts) |

### How to Check Each

**Title tag**: Extract `<title>` from HTML. Count characters. Check keyword position.

**Meta description**: Extract `<meta name="description">`. Count characters. Look for action words (discover, learn, get, find, try, start, compare).

**H1 tag**: Count `<h1>` occurrences. Should be exactly 1. Check keyword presence.

**Heading hierarchy**: List all headings in order. Verify H2 follows H1, H3 follows H2. Flag skipped levels (H1 → H3).

**Content depth**: Count words in main content (exclude nav, footer, sidebar). Compare against top 5 competitors for the same keyword:

```bash
firecrawl search "{target-keyword}" --scrape --limit 5 -o .seo/clients/{slug}/content/.firecrawl/competitors-{slug}.json --json
```

**Keyword usage**: Count occurrences of primary keyword. Calculate density = (count / total words) * 100. Check if keyword appears in first 100 words. Look for semantic variations and LSI terms.

**Internal links**: From the links data, count links to same domain. Check anchor text diversity.

**Images**: Parse all `<img>` tags. Check `alt` attribute, `src` filename, `loading` attribute, image format.

**URL**: Analyze URL path. Check length, keyword presence, parameter presence.

**Social meta**: Check for og: and twitter: meta tags in HTML head.

## SERP Preview Generator

Show how the page will appear in Google search results:

```
┌─────────────────────────────────────────────────┐
│ {title_tag_truncated_at_60_chars}...            │
│ {display_url}                                    │
│ {meta_description_truncated_at_155_chars}...     │
│                                                  │
│ Rich Results: [FAQ ✓] [Review Stars ✗] [Video ✗]│
└─────────────────────────────────────────────────┘
```

**Check:**
- Title truncation: will Google cut it off? (> 60 chars or > 580px pixel width)
- Description truncation: > 155 chars gets cut
- URL display: clean and readable?
- Rich result eligibility: based on schema markup present

## Content Readability Analysis

Calculate readability metrics from the page content:

- **Flesch-Kincaid Grade Level**: target 7-9 for most web content
  - Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
- **Average sentence length**: target 15-20 words
- **Paragraph length**: target 2-4 sentences per paragraph
- **Passive voice usage**: flag if > 10% of sentences
- **Transition word usage**: should appear in 30%+ of sentences

Provide grade: A (grade 6-8), B (grade 9-10), C (grade 11-12), D (grade 13+).

## E-E-A-T Analysis

Based on Google's Quality Rater Guidelines, evaluate:

### Experience (E1)
- Does the content show first-hand experience?
- Look for: personal anecdotes, original photos, specific details only someone with experience would know
- Score: Strong / Moderate / Weak / Missing

### Expertise (E2)
- Does the author demonstrate subject expertise?
- Check for: author byline, credentials, author page, depth of knowledge in content
- Score: Strong / Moderate / Weak / Missing

### Authoritativeness (A)
- Is this source/author recognized as an authority?
- Check for: brand mentions in other sources, citations, industry recognition, domain age
- Score: Strong / Moderate / Weak / Missing

### Trustworthiness (T)
- Can users trust this content and site?
- Check for: HTTPS, contact information, privacy policy, terms of service, sources cited in content, factual accuracy indicators
- Score: Strong / Moderate / Weak / Missing

**E-E-A-T recommendations should be specific**: "Add author bio with credentials" not "improve E-E-A-T."

## Featured Snippet Optimization

Analyze target keyword for featured snippet opportunity:

```bash
firecrawl search "{keyword}" --scrape --limit 3 -o .seo/clients/{slug}/content/.firecrawl/snippet-{slug}.json --json
```

**Snippet types and how to win them:**

| Type | Format Required | Example |
|------|----------------|---------|
| **Paragraph** | Direct answer in 40-60 words, immediately after an H2 matching the question | "What is [topic]?" → 2-3 sentence definition |
| **List** | Ordered/unordered list with 5-8 items, preceded by H2 with question | "How to [do thing]" → numbered steps |
| **Table** | HTML `<table>` with clear headers, structured comparison data | "Comparison of [X] vs [Y]" → feature comparison |

**Optimization steps:**
1. Check if a featured snippet currently exists for the target keyword
2. Identify the snippet type (paragraph, list, table)
3. Recommend content format changes to match
4. Provide a draft snippet-optimized content block

## Content Gap Analysis

Compare client content against top competitors for a topic cluster:

```bash
# Scrape competitor content for the same topic
firecrawl search "{topic} site:{competitor-domain}" --scrape --limit 10 -o .seo/clients/{slug}/content/.firecrawl/comp-gap-{slug}.json --json
```

**Identify:**
- Subtopics competitors cover that client does not
- Content formats competitors use (video, infographic, interactive, calculator)
- Questions competitors answer that client doesn't address
- Depth differences (word count, number of examples, data points)

Output as prioritized content brief suggestions.

## Content Decay Detection

Identify content that needs refreshing:

**Decay signals (check for each published page):**
1. **Outdated statistics**: years mentioned in content that are 2+ years old
2. **Broken external links**: links to pages that now 404
3. **Stale references**: mentions of deprecated tools, old versions, discontinued products
4. **Competitor improvement**: competitors have published newer, more comprehensive content on the same topic
5. **Thin content**: pages with < 500 words that once ranked but may have been surpassed
6. **Missing current year**: "best X" or "guide to X" content without current year reference

**Detection method:**
1. Scrape the page content with firecrawl
2. Look for year mentions older than 2024
3. Check for "updated" or "published" dates > 12 months old
4. Compare word count against current top 5 for the same keyword
5. Check if competitors have fresher content via search dates

**Output:**
```json
{
  "url": "/blog/old-post",
  "title": "Page Title",
  "decay_signals": ["outdated_statistics", "thin_content"],
  "published_date": "2023-06-15",
  "word_count": 450,
  "competitor_avg_word_count": 1800,
  "refresh_priority": "high",
  "recommended_actions": ["Update statistics to 2026", "Expand content to 1500+ words", "Add FAQ section"]
}
```

## Pre-Publish Checklist

Generate a reusable markdown checklist:

```markdown
## Pre-Publish SEO Checklist

### Target Keyword: _______________

#### Content
- [ ] Word count >= competitor average (target: ___ words)
- [ ] Primary keyword in first 100 words
- [ ] Keyword density 1-2%
- [ ] LSI/semantic keyword variations used
- [ ] Direct answer to target query in first paragraph (for AEO)
- [ ] Readability grade 7-9 (Flesch-Kincaid)

#### HTML Tags
- [ ] Title tag: 50-60 chars, keyword in first half
- [ ] Meta description: 120-155 chars, includes CTA
- [ ] Exactly one H1 containing primary keyword
- [ ] H2/H3 hierarchy correct, keywords in subheadings
- [ ] URL slug short, contains keyword, no parameters

#### Media
- [ ] All images have descriptive alt text
- [ ] Images in WebP/AVIF format
- [ ] Images have width/height attributes
- [ ] Below-fold images have loading="lazy"

#### Links
- [ ] Min 3 internal links with relevant anchor text
- [ ] Links to pillar/cluster content
- [ ] Min 1 external link to authoritative source
- [ ] No broken links

#### Schema & Social
- [ ] Appropriate JSON-LD schema added
- [ ] Open Graph tags (og:title, og:description, og:image)
- [ ] Twitter Card tags

#### E-E-A-T
- [ ] Author byline with credentials
- [ ] Sources cited for claims/statistics
- [ ] Published date and "last updated" date

#### AEO (AI Search)
- [ ] Direct answer in first 50 words
- [ ] FAQ section with FAQPage schema
- [ ] Content structured with clear headings for AI extraction
```

## Title/Meta Description Generator

Given a target keyword and page content, generate optimized options:

**Title tag rules:**
- 50-60 characters
- Primary keyword in the first half
- Include power word (Best, Guide, How to, Complete, Free, Proven)
- Include current year for time-sensitive content
- Brand name at end if space allows: `| Brand`

**Meta description rules:**
- 120-155 characters
- Include primary keyword naturally
- Include a CTA (Learn, Discover, Find out, Get started, Compare)
- Create urgency or curiosity when appropriate
- Unique per page — never duplicate

Generate 3-5 title options and 3-5 meta description options for the user to choose from.
