---
name: iblai-marketing-ai-seo
description: "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimization,' 'AI Overviews,' 'optimize for ChatGPT,' 'optimize for Perplexity,' 'AI citations,' 'AI visibility,' 'zero-click search,' 'how do I show up in AI answers,' 'LLM mentions,' or 'optimize for Claude/Gemini.' Use this whenever someone wants their content to be cited or surfaced by AI assistants and AI search engines. For traditional technical and on-page SEO audits, see iblai-marketing-seo-audit. For structured data implementation, see iblai-marketing-schema-markup."
globs:
alwaysApply: false
metadata:
  version: 1.2.0
---

# /iblai-marketing-ai-seo

Make content discoverable, extractable, and citable by AI search systems —
Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, Copilot. The goal
is to get cited as a source in AI-generated answers.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pull this context:

### 1. Current AI Visibility
- Does your brand appear in AI-generated answers today?
- Have you checked ChatGPT, Perplexity, or Google AI Overviews for key queries?
- Which queries matter most to the business?

### 2. Content & Domain
- Content types you produce (blog, docs, comparisons, product pages)
- Domain authority / traditional SEO strength
- Existing structured data (schema markup)?

### 3. Goals
- Get cited as a source in AI answers?
- Win AI Overviews for specific queries?
- Compete with specific brands already getting cited?
- Optimize existing content, or create new AI-optimized content?

### 4. Competitive Landscape
- Top competitors in AI search results
- Are they cited where you're not?

---

## How AI Search Works

### The Landscape

| Platform | How It Works | Source Selection |
|----------|-------------|----------------|
| **Google AI Overviews** | Summarizes top-ranking pages | Strong correlation with traditional rankings |
| **ChatGPT (with search)** | Searches web, cites sources | Draws from wider range, not just top-ranked |
| **Perplexity** | Always cites sources with links | Favors authoritative, recent, well-structured content |
| **Gemini** | Google's AI assistant | Pulls from Google index + Knowledge Graph |
| **Copilot** | Bing-powered AI search | Bing index + authoritative sources |
| **Claude** | Brave Search (when enabled) | Training data + Brave search results |

Per-platform deep dive on ranking factors: [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

### The Key Difference From Traditional SEO

Traditional SEO ranks you. AI SEO gets you **cited**.

In traditional search you need page 1. In AI search a well-structured page on page 2 or 3 can still get cited — AI systems pick sources by content quality, structure, and relevance, not just rank position.

**Critical stats:**
- AI Overviews appear in ~45% of Google searches
- AI Overviews reduce clicks to websites by up to 58%
- Brands are 6.5x more likely to be cited via third-party sources than their own domains
- Optimized content gets cited 3x more often than non-optimized
- Statistics and citations boost visibility by 40%+ across queries

---

## AI Visibility Audit

Audit current presence before optimizing.

### Step 1: Check AI Answers for Key Queries

Test 10-20 of your most important queries across platforms:

| Query | Google AI Overview | ChatGPT | Perplexity | You Cited? | Competitors Cited? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |
| [query 2] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |

**Query types to test:**
- "What is [your product category]?"
- "Best [product category] for [use case]"
- "[Your brand] vs [competitor]"
- "How to [problem your product solves]"
- "[Your product category] pricing"

### Step 2: Citation Pattern Analysis

When competitors get cited and you don't, look at:
- **Content structure** — more extractable than yours?
- **Authority signals** — more citations, stats, expert quotes?
- **Freshness** — more recently updated?
- **Schema markup** — structured data you're missing?
- **Third-party presence** — cited via Wikipedia, Reddit, review sites?

### Step 3: Extractability Check

Per priority page:

| Check | Pass/Fail |
|-------|-----------|
| Clear definition in first paragraph? | |
| Self-contained answer blocks (work without surrounding context)? | |
| Statistics with sources cited? | |
| Comparison tables for "[X] vs [Y]" queries? | |
| FAQ section with natural-language questions? | |
| Schema markup (FAQ, HowTo, Article, Product)? | |
| Expert attribution (author name, credentials)? | |
| Recently updated (within 6 months)? | |
| Heading structure matches query patterns? | |
| AI bots allowed in robots.txt? | |

### Step 4: AI Bot Access Check

Each AI platform has its own crawler. Block it and that platform can't cite you.

- **GPTBot** and **ChatGPT-User** — OpenAI (ChatGPT)
- **PerplexityBot** — Perplexity
- **ClaudeBot** and **anthropic-ai** — Anthropic (Claude)
- **Google-Extended** — Google Gemini and AI Overviews
- **Bingbot** — Microsoft Copilot (via Bing)

Audit your robots.txt for `Disallow` rules targeting these. If they're blocked, you have a business choice: blocking prevents training but also prevents citation. A middle ground is blocking training-only crawlers (like **CCBot** from Common Crawl) while allowing the search bots above.

Full robots.txt configuration: [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

---

## Optimization Strategy

### The Three Pillars

```
1. Structure (make it extractable)
2. Authority (make it citable)
3. Presence (be where AI looks)
```

### Pillar 1: Structure — Make It Extractable

AI systems extract passages, not pages. Every key claim must work standalone.

**Content block patterns:**
- **Definition blocks** for "What is X?" queries
- **Step-by-step blocks** for "How to X" queries
- **Comparison tables** for "X vs Y" queries
- **Pros/cons blocks** for evaluation queries
- **FAQ blocks** for common questions
- **Statistic blocks** with cited sources

Block templates: [references/content-patterns.md](references/content-patterns.md).

**Structural rules:**
- Lead every section with a direct answer — don't bury it
- Hold key answer passages to 40-60 words (optimal for snippet extraction)
- H2/H3 headings that match how people phrase queries
- Tables beat prose for comparison content
- Numbered lists beat paragraphs for process content
- One clear idea per paragraph

### Pillar 2: Authority — Make It Citable

AI systems prefer sources they trust.

**The Princeton GEO research** (KDD 2024, studied across Perplexity.ai) ranked 9 optimization methods:

| Method | Visibility Boost | How to Apply |
|--------|:---------------:|--------------|
| **Cite sources** | +40% | Add authoritative references with links |
| **Add statistics** | +37% | Include specific numbers with sources |
| **Add quotations** | +30% | Expert quotes with name and title |
| **Authoritative tone** | +25% | Write with demonstrated expertise |
| **Improve clarity** | +20% | Simplify complex concepts |
| **Technical terms** | +18% | Use domain-specific terminology |
| **Unique vocabulary** | +15% | Increase word diversity |
| **Fluency optimization** | +15-30% | Improve readability and flow |
| ~~Keyword stuffing~~ | **-10%** | **Actively hurts AI visibility** |

**Best combination:** Fluency + Statistics = maximum boost. Low-ranking sites gain even more — up to 115% visibility lift with citations.

**Statistics and data** (+37-40% citation boost)
- Specific numbers with sources
- Cite original research, not summaries of research
- Date every statistic
- Original data beats aggregated data

**Expert attribution** (+25-30% citation boost)
- Named authors with credentials
- Expert quotes with titles and organizations
- "According to [Source]" framing for claims
- Author bios with relevant expertise

**Freshness signals**
- "Last updated: [date]" displayed prominently
- Regular refreshes (quarterly minimum for competitive topics)
- Current year references and recent statistics
- Remove or update stale info

**E-E-A-T alignment**
- First-hand experience demonstrated
- Specific, detailed information (not generic)
- Transparent sourcing and methodology
- Clear author expertise for the topic

### Pillar 3: Presence — Be Where AI Looks

AI doesn't only cite your website — it cites where you appear.

**Third-party sources matter more than your own site:**
- Wikipedia mentions (7.8% of all ChatGPT citations)
- Reddit discussions (1.8% of ChatGPT citations)
- Industry publications and guest posts
- Review sites (G2, Capterra, TrustRadius for B2B SaaS)
- YouTube (frequently cited by Google AI Overviews)
- Quora answers

**Actions:**
- Keep your Wikipedia page accurate and current
- Participate authentically in Reddit communities
- Get featured in industry roundups and comparison articles
- Maintain updated profiles on relevant review platforms
- Create YouTube content for key how-to queries
- Answer relevant Quora questions with depth

### Machine-Readable Files for AI Agents

AI agents aren't just answering — they're becoming buyers. When an agent evaluates tools on behalf of a user, it needs structured, parseable info. If pricing is locked in a JS-rendered page or behind a "contact sales" wall, agents skip you and recommend competitors they can actually parse.

Add these files at site root:

**`/pricing.md` or `/pricing.txt`** — Structured pricing for AI agents

```markdown
# Pricing — [Your Product Name]

## Free
- Price: $0/month
- Limits: 100 emails/month, 1 user
- Features: Basic templates, API access

## Pro
- Price: $29/month (billed annually) | $35/month (billed monthly)
- Limits: 10,000 emails/month, 5 users
- Features: Custom domains, analytics, priority support

## Enterprise
- Price: Custom — contact sales@example.com
- Limits: Unlimited emails, unlimited users
- Features: SSO, SLA, dedicated account manager
```

**Why this matters:**
- AI agents increasingly compare products programmatically before a human visits
- Opaque pricing gets filtered out of AI-mediated buying journeys
- A markdown file is trivially parseable by any LLM — no rendering, no JS, no login walls
- Same principle as `robots.txt` (for crawlers), `llms.txt` (for AI context), `AGENTS.md` (for agent capabilities)

**Rules:**
- Consistent units (monthly vs. annual, per-seat vs. flat)
- Specific limits and thresholds, not just feature names
- List what's included at each tier, not just deltas
- Keep it updated — stale pricing is worse than no file
- Link from your sitemap and main pricing page

**`/llms.txt`** — Context file for AI systems (see [llmstxt.org](https://llmstxt.org))

If you don't have one, add an `llms.txt` that gives AI systems a quick overview of what your product does, who it's for, and links to key pages (including pricing).

### Schema Markup for AI

Structured data helps AI understand your content. Key schemas:

| Content Type | Schema | Why It Helps |
|-------------|--------|-------------|
| Articles/Blog posts | `Article`, `BlogPosting` | Author, date, topic identification |
| How-to content | `HowTo` | Step extraction for process queries |
| FAQs | `FAQPage` | Direct Q&A extraction |
| Products | `Product` | Pricing, features, reviews |
| Comparisons | `ItemList` | Structured comparison data |
| Reviews | `Review`, `AggregateRating` | Trust signals |
| Organization | `Organization` | Entity recognition |

Content with proper schema gets 30-40% higher AI visibility. Implementation: use the **iblai-marketing-schema-markup** skill.

---

## Content Types That Get Cited Most

Not all content is equally citable. Prioritize:

| Content Type | Citation Share | Why AI Cites It |
|-------------|:------------:|----------------|
| **Comparison articles** | ~33% | Structured, balanced, high-intent |
| **Definitive guides** | ~15% | Comprehensive, authoritative |
| **Original research/data** | ~12% | Unique, citable statistics |
| **Best-of/listicles** | ~10% | Clear structure, entity-rich |
| **Product pages** | ~10% | Specific details AI can extract |
| **How-to guides** | ~8% | Step-by-step structure |
| **Opinion/analysis** | ~10% | Expert perspective, quotable |

**Underperformers for citation:**
- Generic blog posts without structure
- Thin product pages with marketing fluff
- Gated content (AI can't access it)
- Content without dates or author attribution
- PDF-only content (harder for AI to parse)

---

## Monitoring AI Visibility

### What to Track

| Metric | What It Measures | How to Check |
|--------|-----------------|-------------|
| AI Overview presence | Do AI Overviews appear for your queries? | Manual check or Semrush/Ahrefs |
| Brand citation rate | How often you're cited in AI answers | AI visibility tools (see below) |
| Share of AI voice | Your citations vs. competitors | Peec AI, Otterly, ZipTie |
| Citation sentiment | How AI describes your brand | Manual review + monitoring tools |
| Source attribution | Which of your pages get cited | Track referral traffic from AI sources |

### Visibility Monitoring Tools

| Tool | Coverage | Best For |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, Google AI Overviews | Share of AI voice tracking |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude, Copilot+ | Multi-platform monitoring at scale |
| **ZipTie** | Google AI Overviews, ChatGPT, Perplexity | Brand mention + sentiment tracking |
| **LLMrefs** | ChatGPT, Perplexity, AI Overviews, Gemini | SEO keyword → AI visibility mapping |

### DIY Monitoring

Monthly manual check:
1. Pick your top 20 queries
2. Run each through ChatGPT, Perplexity, and Google
3. Record: Are you cited? Who is? What page?
4. Log to a spreadsheet, track month over month

---

## AI SEO by Content Type

### SaaS Product Pages

**Goal:** Get cited for "What is [category]?" and "Best [category]" queries.

**Optimize:**
- Clear product description in first paragraph (what it does, who it's for)
- Feature comparison tables (you vs. category, not just competitors)
- Specific metrics ("processes 10,000 transactions/sec," not "blazing fast")
- Customer count or social proof with numbers
- Visible pricing (AI cites pages with visible pricing). Add a `/pricing.md` so AI agents can parse plans without rendering your page (see "Machine-Readable Files" above)
- FAQ section covering common buyer questions

### Blog Content

**Goal:** Get cited as an authoritative source on topics in your space.

**Optimize:**
- One clear target query per post (match heading to query)
- Definition in first paragraph for "What is" queries
- Original data, research, or expert quotes
- "Last updated" date visible
- Author bio with relevant credentials
- Internal links to related product/feature pages

### Comparison / Alternative Pages

**Goal:** Get cited for "[X] vs [Y]" and "Best [X] alternatives" queries.

**Optimize:**
- Structured comparison tables (not just prose)
- Fair and balanced — AI penalizes obvious bias
- Specific criteria with ratings or scores
- Up-to-date pricing and feature data
- Build these with `/iblai-marketing-competitor-alternatives`

### Documentation / Help Content

**Goal:** Get cited for "How to [X] with [your product]" queries.

**Optimize:**
- Step-by-step format with numbered lists
- Code examples where relevant
- HowTo schema markup
- Screenshots with descriptive alt text
- Clear prerequisites and expected outcomes

---

## Common Mistakes

- **Ignoring AI search entirely** — ~45% of Google searches now show AI Overviews; ChatGPT/Perplexity are growing fast
- **Treating AI SEO as separate from SEO** — Good traditional SEO is the foundation; AI SEO layers structure and authority on top
- **Writing for AI, not humans** — If content reads like algorithm-gaming, it won't get cited or convert
- **No freshness signals** — Undated content loses to dated content; AI weights recency heavily
- **Gating everything** — AI can't access gated content. Keep your most authoritative pages open
- **Ignoring third-party presence** — You may get more citations from a Wikipedia mention than from your own blog
- **No structured data** — Schema markup gives AI explicit context about your content
- **Keyword stuffing** — Unlike traditional SEO where it's just ineffective, stuffing actively reduces AI visibility by 10% (Princeton GEO study)
- **Hiding pricing behind "contact sales" or JS-rendered pages** — AI agents evaluating you on behalf of buyers can't parse what they can't read. Add `/pricing.md`
- **Blocking AI bots** — If GPTBot, PerplexityBot, or ClaudeBot are blocked in robots.txt, those platforms can't cite you
- **Generic content without data** — "We're the best" won't get cited. "Our customers see 3x improvement in [metric]" will
- **Forgetting to monitor** — Check AI visibility at least monthly

---

## Tool Integrations

See the [tools registry](../../tools/REGISTRY.md).

| Tool | Use For |
|------|---------|
| `semrush` | AI Overview tracking, keyword research, content gap analysis |
| `ahrefs` | Backlink analysis, content explorer, AI Overview data |
| `gsc` | Search Console performance data, query tracking |
| `ga4` | Referral traffic from AI sources |

---

## Task-Specific Questions

1. What are your top 10-20 most important queries?
2. Have you checked if AI answers exist for those queries today?
3. Do you have structured data (schema markup) on your site?
4. What content types do you publish? (Blog, docs, comparisons, etc.)
5. Are competitors being cited where you're not?
6. Do you have a Wikipedia page or presence on review sites?

---

## Related Skills

- **iblai-marketing-seo-audit**: For traditional technical and on-page SEO audits
- **iblai-marketing-schema-markup**: For implementing structured data
- **iblai-marketing-content-strategy**: For planning what content to create
- **iblai-marketing-competitor-alternatives**: For building comparison pages that get cited
- **iblai-marketing-programmatic-seo**: For SEO pages at scale
- **iblai-marketing-copywriting**: For writing content that's both human-readable and AI-extractable
