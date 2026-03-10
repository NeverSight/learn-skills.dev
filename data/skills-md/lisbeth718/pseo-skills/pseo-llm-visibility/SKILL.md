---
name: pseo-llm-visibility
description: Optimize programmatic SEO pages for visibility and citation in AI-generated answers from ChatGPT, Perplexity, Google AI Overviews, and other LLM-powered search. Use when optimizing for LLM citation, implementing llms.txt, configuring AI crawler access, structuring content for AI extraction, or when the user asks about generative engine optimization (GEO), AI search visibility, or getting cited by AI.
argument-hint: "[focus: all | llms-txt | crawlers | content | schema | entities]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO LLM Visibility

Optimize programmatic pages for citation and visibility in AI-generated answers. This is a distinct layer on top of traditional SEO — different crawlers, different extraction patterns, different signals.

## Why This Matters for pSEO

- AI-driven search traffic is growing rapidly and represents a significant share of organic discovery
- LLMs cite only a handful of domains per response vs. 10 blue links in traditional search
- Traditional SEO rank is a weak predictor of AI citation — many cited pages rank outside the top 20 in Google
- Content freshness, structure, and extractability matter more than backlinks for LLM visibility
- Google AI Overviews appear on a large and growing share of searches, and most AI-assisted searches result in fewer outbound clicks

## Core Principles

1. **Extractable, not just readable**: Content must be structured in self-contained chunks that LLMs can pull verbatim
2. **Answer-first**: Lead with the direct answer, then provide supporting context
3. **Entity-rich**: Reference entities and relationships, not just keywords
4. **Multi-engine**: Optimize for Bing (ChatGPT), Google (AI Overviews), and direct AI crawlers (Perplexity) simultaneously
5. **Machine-readable**: Schema, llms.txt, and clean HTML structure help LLMs understand page semantics

## Implementation Steps

### 1. Create llms.txt

Place a Markdown file at the site root (`/llms.txt`) that guides LLMs to the most important content. This is a proposed standard gaining rapid adoption — think of it as a curated sitemap for AI.

```markdown
# [Site Name]

> [One-sentence description of what this site covers]

## Key Pages

- [Category Hub A](/category-a): Description of this category
- [Category Hub B](/category-b): Description of this category

## Content Types

- [Page Type]: [What these pages contain and why they're useful]

## Data Sources

- [Where the data comes from, how often updated]

## Full Content

- [/llms-full.txt](/llms-full.txt): Complete content index
```

Also create `/llms-full.txt` — a comprehensive version with more detail that LLMs can fetch when they need deeper context.

For pSEO specifically, the llms.txt should:
- List all category hub pages
- Describe what each page type contains
- Note the data source and update frequency (freshness signal)
- Link to the sitemap for full page discovery

### 2. Configure AI Crawler Access in robots.txt

robots.txt creation is owned by **pseo-linking** (section 8). This skill defines which AI crawler rules to include. AI crawlers serve two purposes: **training** (building the model) and **retrieval** (fetching real-time answers). You typically want to allow retrieval crawlers and may want to block training crawlers.

**AI retrieval crawlers — ALLOW (needed for citation):**
```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Applebot-Extended
Allow: /
```

**AI training crawlers — BLOCK if you don't want content used for training:**
```
User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /
```

See `references/ai-crawlers.md` for the full list of known AI crawlers and their purposes.

**Critical**: If GPTBot is blocked, your content will NEVER appear in ChatGPT answers. If Bingbot is blocked, you lose ChatGPT citations entirely (ChatGPT uses Bing's index for web search).

### 3. Structure Content for LLM Extraction

LLMs extract content in "chunks" — self-contained text fragments of ~100-300 tokens (75-225 words) that can stand alone as a complete answer. Optimize page structure for this:

**The Answer Capsule Pattern:**
```html
<section>
  <h2>[Question or topic as heading]</h2>
  <!-- Answer capsule: 134-167 words, self-contained, directly answers the heading -->
  <p>[Direct answer in the first 1-2 sentences. Then supporting detail.
     The entire paragraph should make sense if extracted without any
     surrounding context.]</p>
</section>
```

**Rules for LLM-extractable content:**
- Each section under an H2/H3 should be a complete, self-contained answer (134-167 words optimal)
- Lead with the conclusion/answer, then provide reasoning
- Never assume the reader has seen other sections — each chunk must stand alone
- Use clear heading-to-content mapping (the heading is the question, the content is the answer)
- Pages with 120-180 words between headings get 70% more ChatGPT citations

**What NOT to do:**
- Long unstructured paragraphs with no headings
- Content that requires reading previous sections to understand
- Vague headings that don't indicate what the section answers
- Burying the answer after paragraphs of context

### 4. Add Statistics and Original Data

Research from "GEO: Generative Engine Optimization" (Aggarwal et al., 2024, arXiv:2311.09735) shows statistics addition improves LLM visibility by ~41% and quotation addition by ~28%. These figures are from controlled experiments and may vary in practice.

For pSEO pages, this means:
- Surface numeric data from the content model as explicit statistics ("4.8 average rating from 500+ reviews")
- Include specific numbers, percentages, dates, and measurements
- Cite data sources explicitly ("According to [source], ...")
- If the business has proprietary data, surface it — LLMs prefer content with information not found elsewhere
- Add relevant expert quotations or attributions where possible

### 5. Implement Entity-Based Optimization

LLMs understand entities (people, places, organizations, concepts, products) and their relationships. Traditional keyword optimization is less effective for AI citation.

For pSEO pages:
- Reference the primary entity by its full canonical name, not just abbreviations
- Include entity relationships ("made by [company]", "located in [city]", "similar to [related entity]")
- Use schema markup to explicitly define entities (Organization, Product, Place, Person)
- Link to authoritative entity sources (Wikipedia, official sites) to help LLMs disambiguate
- Use consistent entity naming across all pages (don't alternate between "NYC" and "New York City")

### 6. Ensure Multi-Engine Indexation

Different AI platforms source from different indexes:

| AI Platform | Primary Source | Requirement |
|-------------|---------------|-------------|
| ChatGPT | Bing index | Must be indexed by Bing |
| Google AI Overviews | Google index | Must be indexed by Google |
| Perplexity | Own crawler + Bing | Must allow PerplexityBot |
| Claude | Web search | Must be indexable |

**Action items:**
- Verify Bing indexation via Bing Webmaster Tools (not just Google Search Console)
- Submit sitemap to both Google Search Console and Bing Webmaster Tools
- Verify AI crawlers are not blocked in robots.txt
- Use SSR or SSG — AI crawlers cannot execute JavaScript (client-rendered pages are invisible to them)

### 7. Optimize Content Tone and Format

LLMs preferentially cite content that is:
- **Neutral and factual** — not promotional or salesy
- **Comprehensive but concise** — covers the topic fully without padding
- **Comparative** — comparison/list formats make up ~33% of all AI citations
- **Authoritative** — backed by sources, data, and expertise

For pSEO templates specifically:
- Use neutral, informational tone even on commercial pages
- Include comparison sections where relevant (vs. alternatives, compared to similar options)
- Add "at a glance" summary sections that LLMs can extract as complete answers
- Avoid superlatives without data backing ("best", "top", "#1" without evidence)

### 8. Leverage Freshness Signals

Content updated within 30 days gets significantly more AI citations than stale content.

For pSEO at scale:
- Use ISR with short revalidation intervals to keep pages fresh
- Display a visible "Last updated: [date]" on every page
- Include `dateModified` in schema markup with accurate dates
- If data changes (prices, ratings, availability), reflect changes quickly
- Consider automated data refresh pipelines that trigger page regeneration

## LLM Visibility Checklist

- [ ] `/llms.txt` exists at site root with page type descriptions and category links
- [ ] robots.txt allows GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Bingbot
- [ ] Site is indexed by both Google and Bing (verify in both webmaster tools)
- [ ] All pages use SSR or SSG (no client-side-only rendering)
- [ ] Each content section is a self-contained 134-167 word answer capsule
- [ ] Headings clearly indicate what the section answers
- [ ] Statistics and specific numbers are present on every page
- [ ] Entity names are consistent and schema-defined across all pages
- [ ] Content tone is neutral and factual, not promotional
- [ ] Comparison/list sections are included where relevant
- [ ] "Last updated" date is visible on every page and in schema
- [ ] FAQ sections use Q&A format that matches natural language queries

## Relationship to Other Skills

- **Builds on**: pseo-templates (page structure), pseo-schema (JSON-LD), pseo-metadata (crawlability), pseo-linking (robots.txt, sitemap)
- **Extends**: pseo-performance (SSR/SSG requirement, freshness via ISR)
- **Validated by**: pseo-quality-guard (content quality is the foundation — thin pages won't be cited by LLMs either)
