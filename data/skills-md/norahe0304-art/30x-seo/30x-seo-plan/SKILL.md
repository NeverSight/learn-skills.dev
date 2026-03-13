---
name: 30x-seo-plan
description: >
  SEO strategy planning: competitor analysis, keyword strategy, content
  calendar, and implementation roadmap. Use when user says "SEO plan",
  "SEO strategy", "content calendar", or "SEO roadmap".
allowed-tools:
  - WebFetch
  - Read
---

# SEO Strategy Planning

## What This Skill Does

Create SEO strategy: analyze competitors, plan keywords, create content calendar, output implementation roadmap.

**Does NOT do**:
- Website architecture design → use `site-architecture`
- Technical SEO checks → use `seo-technical`
- Content generation → use `seo-content-writer`

---

## Optional Input

| Input | Source | Description |
|-------|--------|-------------|
| **seo-keywords output** | `/seo keywords` | If keyword research exists, read as strategy input |

> Not a hard dependency. You can plan first then research, or research first then plan.

---

## Process

### Step 1: Discovery

Ask user:
- Business type (SaaS / E-commerce / Local service / Media / Other)
- Target audience (Who are your customers?)
- Main competitors (3-5)
- Goals (Traffic? Conversions? Brand?)
- Existing website? (Yes → analyze current state; No → new site planning)

### Step 2: Competitor Analysis

For each competitor, analyze:

| Dimension | Check Points |
|-----------|--------------|
| **Content** | What pages? Blog frequency? Content depth? |
| **Keywords** | What keywords rank? Content topics? |
| **E-E-A-T** | Author info? Expert endorsements? Trust signals? |
| **Structure** | URL hierarchy? Navigation design? |

Tools: WebFetch + Perplexity

Output: `COMPETITOR-ANALYSIS.md`

### Step 3: Keyword Strategy

If seo-keywords output exists → read and integrate
If not → infer from competitor analysis + user input

Determine:
- Core keywords (3-5)
- Long-tail keywords (10-20)
- Topic clusters

Output: Integrate into `SEO-STRATEGY.md`

### Step 4: Content Planning

Based on keyword strategy, plan:

| Content Type | Example |
|--------------|---------|
| **Pillar pages** | Authoritative long-form on core topics |
| **Cluster pages** | Detailed articles around pillars |
| **Blog posts** | Regular update content |

Output: `CONTENT-CALENDAR.md`

```markdown
# Content Calendar

## Month 1
| Week | Topic | Target Keyword | Type | Priority |
|------|-------|----------------|------|----------|
| 1 | ... | ... | Pillar | High |
| 2 | ... | ... | Cluster | Medium |
```

### Step 5: Implementation Roadmap

Simplified roadmap:

| Phase | Timeline | Focus |
|-------|----------|-------|
| **Launch** | Week 1-2 | Technical foundation (→ seo-technical), core pages |
| **Content** | Week 3-8 | Publish per calendar (→ seo-content-writer) |
| **Optimize** | Week 9-12 | Monitor rankings, adjust strategy |

Output: `IMPLEMENTATION-ROADMAP.md`

---

## Output Files

| File | Content |
|------|---------|
| `SEO-STRATEGY.md` | Complete strategy: goals, keywords, topic clusters |
| `COMPETITOR-ANALYSIS.md` | Competitor analysis report |
| `CONTENT-CALENDAR.md` | Content calendar (for seo-content-writer) |
| `IMPLEMENTATION-ROADMAP.md` | Implementation roadmap |

---

## Integration

```
seo-keywords ──(optional)──> seo-plan
                                │
                                ├──> seo-content-writer (content generation)
                                ├──> site-architecture (architecture design)
                                └──> seo-technical (technical checks)
```

| Skill | When to Use |
|-------|-------------|
| `seo-keywords` | Do keyword research before planning |
| `site-architecture` | When detailed architecture design needed |
| `seo-content-writer` | Generate content per calendar |
| `seo-technical` | Check technical foundation |

---

## Example

```
User: /seo plan
Claude: Please tell me:
1. Business type?
2. Target audience?
3. Main competitors?
4. SEO goals?

User: SaaS project management tool, targeting SMBs, competitors are Asana, Monday, Notion

Claude: [Executing competitor analysis...]
        [Creating keyword strategy...]
        [Planning content calendar...]
        [Outputting 4 files]
```

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
