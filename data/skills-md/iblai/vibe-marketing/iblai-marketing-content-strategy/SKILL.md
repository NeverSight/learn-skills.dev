---
name: iblai-marketing-content-strategy
description: When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," "content planning," "editorial calendar," "content marketing," "content roadmap," "what content should I create," "blog topics," "content pillars," or "I don't know what to write." Use this whenever someone needs help deciding what content to produce, not just writing it. For writing individual pieces, see iblai-marketing-copywriting. For SEO-specific audits, see iblai-marketing-seo-audit. For social media content specifically, see iblai-marketing-social-content.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-content-strategy

Plan content that drives traffic, builds authority, and generates leads.
Every piece must be searchable, shareable, or both — in that order.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pull this context:

### 1. Business Context
- What the company does
- Ideal customer
- Primary content goal (traffic, leads, brand, thought leadership)
- Problems the product solves

### 2. Customer Research
- Questions asked before buying
- Objections in sales calls
- Repeated themes in support tickets
- Language customers use for their problems

### 3. Current State
- Existing content; what's working
- Resources (writers, budget, time)
- Producible formats (written, video, audio)

### 4. Competitive Landscape
- Main competitors
- Content gaps in the market

---

## Searchable vs Shareable

Every piece must be searchable, shareable, or both. Prioritize searchable — search traffic is the foundation.

**Searchable content** captures existing demand. Optimized for people actively looking.

**Shareable content** creates demand. Spreads ideas, gets people talking.

### Searchable Content

- Target a specific keyword or question
- Match search intent exactly — answer what the searcher wants
- Clear titles that match search queries
- Headings that mirror search patterns
- Keywords in title, headings, first paragraph, URL
- Comprehensive coverage; don't leave questions unanswered
- Data, examples, and links to authoritative sources
- Optimize for AI/LLM discovery: clear positioning, structured content, brand consistency across the web

### Shareable Content

- Lead with a novel insight, original data, or counterintuitive take
- Challenge conventional wisdom with well-reasoned arguments
- Tell stories that make people feel something
- Make content people share to look smart or help others
- Connect to current trends or emerging problems
- Share vulnerable, honest experiences others can learn from

---

## Content Types

### Searchable Types

**Use-Case Content**
Formula: [persona] + [use-case]. Targets long-tail keywords.
- "Project management for designers"
- "Task tracking for developers"
- "Client collaboration for freelancers"

**Hub and Spoke**
Hub = comprehensive overview. Spokes = related subtopics.
```
/topic (hub)
├── /topic/subtopic-1 (spoke)
├── /topic/subtopic-2 (spoke)
└── /topic/subtopic-3 (spoke)
```
Build the hub first, then the spokes. Interlink strategically.

**Note:** Most content lives fine under `/blog`. Reserve dedicated hub/spoke URL structures for major topics with layered depth (e.g., Atlassian's `/agile` guide). For typical blog posts, `/blog/post-title` is enough.

**Template Libraries**
High-intent keywords + product adoption.
- Target searches like "marketing plan template"
- Standalone immediate value
- Show how the product enhances the template

### Shareable Types

**Thought Leadership**
- Name concepts everyone feels but hasn't named
- Challenge conventional wisdom with evidence
- Share vulnerable, honest experiences

**Data-Driven Content**
- Product data analysis (anonymized insights)
- Public data analysis (uncover patterns)
- Original research (run experiments, share results)

**Expert Roundups**
15-30 experts answering one specific question. Built-in distribution.

**Case Studies**
Structure: Challenge → Solution → Results → Key learnings

**Meta Content**
Behind-the-scenes transparency. "How We Got Our First $5k MRR," "Why We Chose Debt Over VC."

For programmatic content at scale, use `/iblai-marketing-programmatic-seo`.

---

## Content Pillars and Topic Clusters

Pillars are 3-5 core topics your brand will own. Each pillar spawns a cluster of related content.

Most content can live under `/blog` with good internal linking between posts. Dedicated pillar pages with custom URL structures (`/guides/topic`) are only needed when you're building comprehensive resources with multiple depth layers.

### How to Identify Pillars

1. **Product-led** — what problems does your product solve?
2. **Audience-led** — what does your ICP need to learn?
3. **Search-led** — what topics have volume in your space?
4. **Competitor-led** — what are competitors ranking for?

### Pillar Structure

```
Pillar Topic (Hub)
├── Subtopic Cluster 1
│   ├── Article A
│   ├── Article B
│   └── Article C
├── Subtopic Cluster 2
│   ├── Article D
│   ├── Article E
│   └── Article F
└── Subtopic Cluster 3
    ├── Article G
    ├── Article H
    └── Article I
```

### Pillar Criteria

Good pillars:
- Align with your product/service
- Match what your audience cares about
- Have search volume and/or social interest
- Are broad enough for many subtopics

---

## Keyword Research by Buyer Stage

Map topics to the buyer's journey using these modifiers:

### Awareness
Modifiers: `what is`, `how to`, `guide to`, `introduction to`

Example: customers ask about project management basics
- "What is Agile Project Management"
- "Guide to Sprint Planning"
- "How to Run a Standup Meeting"

### Consideration
Modifiers: `best`, `top`, `vs`, `alternatives`, `comparison`

Example: customers evaluate multiple tools
- "Best Project Management Tools for Remote Teams"
- "Asana vs Trello vs Monday"
- "Basecamp Alternatives"

### Decision
Modifiers: `pricing`, `reviews`, `demo`, `trial`, `buy`

Example: pricing comes up in sales calls
- "Project Management Tool Pricing Comparison"
- "How to Choose the Right Plan"
- "[Product] Reviews"

### Implementation
Modifiers: `templates`, `examples`, `tutorial`, `how to use`, `setup`

Example: support tickets show implementation struggles
- "Project Template Library"
- "Step-by-Step Setup Tutorial"
- "How to Use [Feature]"

---

## Ideation Sources

### 1. Keyword Data

If the user provides keyword exports (Ahrefs, SEMrush, GSC), analyze for:
- Topic clusters (group related keywords)
- Buyer stage (awareness/consideration/decision/implementation)
- Search intent (informational, commercial, transactional)
- Quick wins (low competition + decent volume + high relevance)
- Content gaps (keywords competitors rank for that you don't)

Output as a prioritized table:
| Keyword | Volume | Difficulty | Buyer Stage | Content Type | Priority |

### 2. Call Transcripts

From sales or customer call transcripts:
- Questions asked → FAQ content or blog posts
- Pain points → problems in their own words
- Objections → content to address proactively
- Language patterns → exact phrases to use (voice of customer)
- Competitor mentions → what they compared you to

Output content ideas with supporting quotes.

### 3. Survey Responses

Mine for:
- Open-ended responses (topics and language)
- Common themes (30%+ mention = high priority)
- Resource requests (what they wish existed)
- Content preferences (formats they want)

### 4. Forum Research

Use web search:

**Reddit:** `site:reddit.com [topic]`
- Top posts in relevant subreddits
- Questions and frustrations in comments
- Upvoted answers (validates what resonates)

**Quora:** `site:quora.com [topic]`
- Most-followed questions
- Highly upvoted answers

**Other:** Indie Hackers, Hacker News, Product Hunt, industry Slack/Discord

Extract: FAQs, misconceptions, debates, problems being solved, terminology used.

### 5. Competitor Analysis

**Find their content:** `site:competitor.com/blog`

**Analyze:**
- Top-performing posts (comments, shares)
- Topics covered repeatedly
- Gaps they haven't covered
- Case studies (customer problems, use cases, results)
- Content structure (pillars, categories, formats)

**Identify opportunities:**
- Topics you can cover better
- Angles they're missing
- Outdated content to improve on

### 6. Sales and Support Input

From customer-facing teams:
- Common objections
- Repeated questions
- Support ticket patterns
- Success stories
- Feature requests and the problems underneath them

---

## Prioritizing Ideas

Score each idea on four factors:

### 1. Customer Impact (40%)
- How often did this topic appear in research?
- What % of customers face this challenge?
- How emotionally charged is the pain?
- Potential LTV of customers with this need?

### 2. Content-Market Fit (30%)
- Aligns with problems your product solves?
- Unique insights from customer research?
- Customer stories to support it?
- Will it naturally lead to product interest?

### 3. Search Potential (20%)
- Monthly search volume?
- Competitiveness?
- Related long-tail opportunities?
- Search interest growing or declining?

### 4. Resource Requirements (10%)
- Expertise to create authoritative content?
- Additional research needed?
- Assets (graphics, data, examples) required?

### Scoring Template

| Idea | Customer Impact (40%) | Content-Market Fit (30%) | Search Potential (20%) | Resources (10%) | Total |
|------|----------------------|-------------------------|----------------------|-----------------|-------|
| Topic A | 8 | 9 | 7 | 6 | 8.0 |
| Topic B | 6 | 7 | 9 | 8 | 7.1 |

---

## Output Format

When building a content strategy, ship:

### 1. Content Pillars
- 3-5 pillars with rationale
- Subtopic clusters per pillar
- How pillars connect to the product

### 2. Priority Topics

Per piece:
- Topic/title
- Searchable, shareable, or both
- Content type (use-case, hub/spoke, thought leadership, etc.)
- Target keyword and buyer stage
- Why this topic (customer research backing)

### 3. Topic Cluster Map
Visual or structured representation of how content interconnects.

---

## Task-Specific Questions

1. What patterns emerge from your last 10 customer conversations?
2. What questions keep coming up in sales calls?
3. Where are competitors' content efforts falling short?
4. Which unique insights from customer research aren't being shared elsewhere?
5. Which existing content drives the most conversions, and why?

---

## References

- **[Headless CMS Guide](references/headless-cms.md)**: CMS selection, content modeling for marketing, editorial workflows, platform comparison (Sanity, Contentful, Strapi)

---

## Related Skills

- **iblai-marketing-copywriting**: Writing individual pieces
- **iblai-marketing-seo-audit**: Technical SEO and on-page optimization
- **iblai-marketing-ai-seo**: Optimizing content for AI search engines / LLM citations
- **iblai-marketing-programmatic-seo**: Scaled content generation
- **iblai-marketing-site-architecture**: Page hierarchy, navigation design, URL structure
- **iblai-marketing-email-sequence**: Email-based content
- **iblai-marketing-social-content**: Social media content
