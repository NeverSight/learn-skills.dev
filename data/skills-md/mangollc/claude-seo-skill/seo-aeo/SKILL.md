---
name: seo-aeo
description: |
  AI Search Optimization (AEO / Answer Engine Optimization): optimize for Google AI Overviews,
  Perplexity citations, ChatGPT mentions. Structured data for AI consumption, FAQ and entity
  optimization, brand authority signals, brand SERP management.

  USE FOR:
  - "AI search", "AEO", "GEO", "AI overview", "AI optimization"
  - "answer engine optimization", "AI engine optimization", "generative engine optimization"
  - "Perplexity", "ChatGPT visibility", "AI citations"
  - "Google AI Overview", "SGE", "search generative experience"
  - "entity optimization", "knowledge graph", "knowledge panel"
  - "FAQ schema", "structured data for AI"
  - "brand mentions", "authority signals", "brand SERP"
  - "brand search results", "what shows when you Google us"
  - "enhance AEO", "what people ask AI", "LLM queries", "AI question discovery"
  - "people also ask", "autocomplete mining", "Reddit questions", "Quora questions"
  - "AI visibility testing", "AI citation testing"

  Uses firecrawl to analyze AI search results and competitor AI visibility.
  Multi-client: stores results in .seo/clients/{client}/aeo/
---

# AI Search Optimization (AEO)

Load client context first. See seo-keywords [rules/client-setup.md](../seo-keywords/rules/client-setup.md).

## File Organization

```
aeo/
├── ai-overview-audit-{date}.json     # Google AI Overview analysis
├── perplexity-audit-{date}.json      # Perplexity citation analysis
├── entity-optimization.json          # Entity and authority audit
├── brand-serp-{date}.json            # Brand SERP analysis
├── structured-data-audit.json        # AI-focused schema audit
├── enhance-aeo-{date}.json           # Enhanced AEO discovery results
├── question-master-list.json         # All discovered questions (deduplicated)
├── ai-visibility-scorecard.json      # Keyword-by-keyword AI test results
├── aeo-checklist-results/
│   └── {url-slug}-aeo.json           # Per-page AEO scores
└── .firecrawl/
    ├── paa-*.json                    # People Also Ask results
    ├── auto-*.json                   # Autocomplete mining results
    ├── reddit-*.json                 # Reddit question mining results
    ├── quora-*.json                  # Quora question mining results
    ├── atp-*.json                    # AnswerThePublic-style question map
    └── ai-test-*.json                # AI visibility test results
```

## Understanding AI Search Engines

### Google AI Overviews
- Appears at top of Google search results for informational queries
- Synthesizes information from multiple sources
- Cites sources with links — being cited drives traffic
- Favors: well-structured content, direct answers, authoritative sources, recent data

### Perplexity
- AI-powered answer engine that cites sources inline
- Prioritizes: factual accuracy, well-structured content, source diversity, clear attribution
- Being the definitive source for niche topics is key
- Structured data and clear headings improve extraction

### ChatGPT / Bing
- ChatGPT with browsing can cite web sources
- Bing powers much of the web search integration
- Entity signals (Wikipedia, Wikidata) strongly influence answers
- Brand recognition and authority matter heavily

## Google AI Overview Optimization

### Step 1: Identify AI Overview Queries

```bash
# Search target keywords and check for AI Overview presence
firecrawl search "{target-keyword}" --scrape --limit 5 -o .seo/clients/{slug}/aeo/.firecrawl/aio-{slug}.json --json
```

Check search results for AI Overview indicators. Not all queries trigger AI Overviews — focus on those that do.

### Step 2: Analyze Cited Sources

For queries where AI Overviews appear, identify which sources get cited:

**Common traits of AI Overview sources:**
- Direct answer to the query in the first 1-2 sentences
- Well-structured with clear H2/H3 headings
- Uses lists, tables, and structured formats
- Contains specific data, statistics, or facts
- Has proper schema markup (FAQPage, HowTo, Article)
- Is from a recognized authoritative domain
- Content is recent and up-to-date
- Uses concise, factual language (not marketing fluff)

### Step 3: Optimize Content for AI Citation

For each target page:

1. **Lead with the answer**: First 50 words should directly answer the likely query
2. **Use definition format**: "X is Y that Z" for concept queries
3. **Structure for extraction**: Use H2 headings that match common questions
4. **Include data**: Statistics, percentages, specific numbers are preferred
5. **Add comparison tables**: AI loves structured data it can reference
6. **Keep paragraphs short**: 2-3 sentences max for easy extraction
7. **Use authoritative language**: Cite sources, link to studies, reference standards

## Perplexity Citation Optimization

### What Perplexity Prioritizes
- **Factual accuracy**: verifiable claims with sources
- **Comprehensive coverage**: thorough treatment of the topic
- **Clear structure**: headings, lists, tables that make extraction easy
- **Source credibility**: established domains with good reputation
- **Unique information**: original data, research, or perspectives
- **Recency**: up-to-date content with current data

### Optimization Tactics

1. **Become the definitive source**: For niche topics, create the most comprehensive resource
2. **Original data**: Publish surveys, studies, or data analysis that others cite
3. **FAQ format**: Question-and-answer format maps directly to how Perplexity answers queries
4. **Entity clarity**: Make it unambiguous what entity/brand/concept the content is about
5. **Cross-reference**: Link to authoritative sources to build credibility
6. **Update frequency**: Keep content fresh with regular updates and current year references

## ChatGPT / Bing Optimization

### Bing SEO Fundamentals
Bing weighs some factors differently than Google:
- **Exact-match keywords**: Bing is more keyword-literal than Google
- **Social signals**: Bing considers social media activity more
- **Multimedia**: Bing favors pages with images and video
- **Domain age**: Established domains get more credit
- **Official sources**: Bing strongly favors .gov, .edu, and Wikipedia

### Entity Signals for ChatGPT

ChatGPT's knowledge includes entities from:
- **Wikipedia**: Having a Wikipedia page significantly increases brand/entity recognition
- **Wikidata**: Structured entity data feeds into AI knowledge bases
- **Social profiles**: Consistent entity data across LinkedIn, Twitter/X, Crunchbase
- **News coverage**: Press mentions train AI models on brand associations
- **Schema.org Organization**: sameAs links to all official profiles

**Action items:**
1. Check if brand/founder has a Wikipedia page (if notable enough to qualify)
2. Verify Wikidata entry exists and is accurate
3. Ensure consistent brand information across all platforms
4. Build press coverage and news mentions
5. Implement Organization schema with comprehensive sameAs links

## Structured Data for AI Consumption

Beyond standard SEO schema, these types specifically help AI extraction:

### FAQPage Schema
Most impactful for AEO — provides direct Q&A pairs AI can quote:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is {topic}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Concise, direct answer here. {topic} is..."
      }
    }
  ]
}
```

### HowTo Schema
Step-by-step instructions AI can present directly:

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to {do thing}",
  "step": [
    { "@type": "HowToStep", "name": "Step title", "text": "Step description" }
  ]
}
```

### DefinedTerm Schema
For glossary/definition content AI frequently references:

```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "Term Name",
  "description": "Clear definition of the term"
}
```

### Speakable Property
Mark content suitable for voice assistants:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-takeaway"]
  }
}
```

### Organization with Comprehensive sameAs
Link all brand profiles for entity recognition:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{brand}",
  "url": "{domain}",
  "sameAs": [
    "https://www.linkedin.com/company/{brand}",
    "https://twitter.com/{brand}",
    "https://www.facebook.com/{brand}",
    "https://www.youtube.com/{brand}",
    "https://en.wikipedia.org/wiki/{brand}",
    "https://www.wikidata.org/wiki/{entity_id}",
    "https://www.crunchbase.com/organization/{brand}"
  ]
}
```

## FAQ & Entity Optimization

### People Also Ask (PAA) Mining

```bash
# Search target queries to find PAA questions
firecrawl search "{topic} FAQ" --scrape --limit 10 -o .seo/clients/{slug}/aeo/.firecrawl/paa-{slug}.json --json
firecrawl search "what is {topic}" --scrape --limit 5 -o .seo/clients/{slug}/aeo/.firecrawl/whatis-{slug}.json --json
firecrawl search "how does {topic} work" --scrape --limit 5 -o .seo/clients/{slug}/aeo/.firecrawl/howdoes-{slug}.json --json
```

Collect PAA questions and create content that:
1. Uses the exact question as an H2 heading
2. Answers directly in the first sentence below the heading
3. Expands with 2-3 supporting sentences
4. Wraps in FAQPage schema

### Entity-First Writing Style
- Define entities clearly on first mention
- Use consistent terminology (don't switch between "AI search" and "answer engines" randomly)
- Link entities to their canonical references
- Use structured data to disambiguate entities

## Brand Authority Signals Audit

Check these authority indicators:

| Signal | How to Check | Status |
|--------|-------------|--------|
| Wikipedia page | `firecrawl search "{brand} wikipedia" --limit 3` | Present / Absent / Stub |
| Wikidata entry | `firecrawl search "wikidata {brand}" --limit 3` | Present / Absent |
| Knowledge Panel | `firecrawl search "{brand}" --limit 5` — check for KP in results | Triggered / Not triggered |
| Social profiles verified | Check LinkedIn, Twitter/X, Facebook, YouTube | All present / Gaps |
| News coverage | `firecrawl search "{brand}" --sources news --limit 10` | Recent / Stale / None |
| Industry mentions | `firecrawl search "{brand} {industry}" --limit 10` | Strong / Moderate / Weak |
| Schema Organization | Scrape homepage for Organization schema | Present / Incomplete / Missing |
| sameAs links | Check if Organization schema links to all profiles | Complete / Incomplete |

## Brand SERP Management

Analyze what appears when someone searches the brand name:

```bash
firecrawl search "{brand_name}" --scrape --limit 20 -o .seo/clients/{slug}/aeo/.firecrawl/brand-serp.json --json
```

### Audit the First Page

For each result on page 1 of brand search:

| Position | URL | Type | Sentiment | Owned? |
|----------|-----|------|-----------|--------|
| 1 | example.com | Homepage | Positive | Yes |
| 2 | linkedin.com/company/... | Social | Positive | Yes |
| 3 | yelp.com/biz/... | Review | Mixed | No (but manageable) |
| ... | ... | ... | ... | ... |

**Goals:**
- Own positions 1-5 with: homepage, social profiles, blog, about page
- Monitor positions 6-10: review sites, press, directories
- Flag negative results and develop strategy to push them down
- Ensure Knowledge Panel is accurate and complete

### Brand SERP Optimization

1. **Claim and optimize all social profiles**: LinkedIn, Twitter/X, Facebook, YouTube, Instagram, Pinterest, TikTok (whichever are relevant)
2. **Optimize for branded keywords**: Ensure homepage title includes brand name, about page ranks for "about {brand}"
3. **Review management**: Respond to all reviews, encourage positive reviews to improve review site listings
4. **Press and PR**: Create newsworthy content that generates branded press mentions
5. **Knowledge Panel**: Submit edits via Google if panel exists, build entity signals if it doesn't

## Per-Page AEO Checklist

For each important page, score against these AI-readiness factors:

| Factor | Check | Points |
|--------|-------|--------|
| Direct answer in first 50 words | Does the opening directly answer the target query? | 15 |
| FAQ section present | Are there Q&A pairs on the page? | 10 |
| FAQPage schema | Is FAQ content wrapped in JSON-LD? | 10 |
| Clear entity markup | Organization/Person/Product schema present? | 10 |
| Structured data (lists/tables) | Does the page use lists and tables for key data? | 10 |
| Concise definitions | Are key terms defined clearly? | 10 |
| Authoritative sources cited | Does content link to studies, official sources? | 10 |
| Author byline with credentials | Is there a named, credible author? | 10 |
| Updated date visible | Does the page show a recent update date? | 5 |
| speakable content marked | Is key content marked for voice assistants? | 5 |
| sameAs links on entity pages | Do brand/person pages link to all profiles? | 5 |

**Total: 100 points**

Grade: A (85-100), B (70-84), C (55-69), D (40-54), F (< 40)

---

## Enhanced AEO Discovery (AI Question Discovery)

The `/enhance-aeo` command runs 5 deep-discovery modules to find what real people are asking AI engines about your topic, and tests how visible you are in AI-generated answers. No API keys needed — uses Firecrawl search to mine publicly available data.

### Why This Matters

LLMs learn from and cite the same content that appears in:
- Google's "People Also Ask" boxes
- Google autocomplete suggestions
- Reddit threads and Quora answers
- FAQ-style content across the web

By mining these sources, you discover the exact questions people ask AI chatbots — and can create content that AI engines will cite.

### Module 1: People Also Ask (PAA) Chain Mining

PAA questions are the strongest proxy for LLM queries. Google shows these because people commonly ask them — the same people then ask ChatGPT, Perplexity, etc.

Search patterns:
- `{keyword}` — direct PAA boxes
- `what is {keyword}` — definitional questions
- `how to {keyword}` — procedural questions
- `why {keyword}` — reasoning questions
- `{keyword} vs` — comparison questions

Extract and deduplicate all PAA questions, group by intent.

### Module 2: Google Autocomplete Mining

Autocomplete reflects real-time search behavior. Patterns:
- `{keyword} + [a, how, best, for, can, should, is]`

Cross-reference with PAA results — overlapping questions are highest priority.

### Module 3: Reddit & Quora Question Mining

These platforms are where real people ask real questions in natural language — the same format they use with AI chatbots. LLMs are also trained on this data.

Search patterns:
- `site:reddit.com {keyword}` — Reddit threads
- `site:quora.com {keyword}` — Quora questions
- `reddit {keyword} recommendations` — Purchase intent
- `reddit best {keyword}` — Comparison intent

Extract: thread titles (= questions), top-voted answers (= what AI learns from), brand mentions, pain points, decision criteria.

### Module 4: AnswerThePublic-Style Question Mapping

Build a complete question tree using all question word variations:
- who, what, when, where, which, without, with, near me

Creates a visual question map showing all angles people approach the topic from.

### Module 5: Automated AI Visibility Testing

Systematically test each of the client's top keywords (up to 20):

For each keyword:
1. Search via Firecrawl, check results for AI Overview presence
2. Check if client is cited in AI features
3. Identify which competitors ARE cited
4. Scrape top-cited competitor pages
5. Reverse-engineer WHY they get cited (structure, schema, depth, FAQ sections, author credentials)

Output an AI Visibility Scorecard:

| Keyword | AI Overview? | You Cited? | Top Cited | Gap |
|---------|-------------|------------|-----------|-----|
| kw1 | Yes/No | Yes/No | competitor | High/Med/Low |

### Master Question List

After all 5 modules complete, compile a deduplicated master list:
- Total unique questions across all sources
- Ranked by frequency (appeared in multiple modules = higher priority)
- Tagged with source: PAA, Autocomplete, Reddit, Quora, Question Map
- Tagged with intent: Informational, Commercial, Navigational, Transactional
- Tagged with status: Answered on your site / Not answered / Partially answered

### Action Plan Output

1. Top 10 questions to create content for (highest frequency, not yet answered)
2. Top 5 existing pages to restructure for AI citation
3. Schema markup additions needed
4. Content gaps where competitors dominate AI results
5. Reddit/Quora communities to participate in for brand visibility
