---
name: pseo-engine
description: Programmatic SEO automation engine with keyword research, content optimization, technical audits, competitor analysis, and batch page generation. Triggers on commands like "seo audit", "SEO分析", "keyword research", "分析关键词", "optimize content", "优化文章", "generate pseo", "生成pSEO", "build internal links", "构建内链", "analyze competitor", "分析竞争对手".
---

# pSEO Automation Engine

高度自动化的程序化SEO引擎，具备完整的SEO能力矩阵。

## Capabilities Overview

| Module | Trigger Commands | Function |
|--------|-----------------|----------|
| Keyword Research | `keyword research [topic]`, `分析关键词 [topic]` | SERP analysis, long-tail discovery, intent classification |
| Content Optimizer | `optimize content [path]`, `优化文章 [path]` | Score content, suggest improvements, auto-fix safe issues |
| Technical Audit | `seo audit`, `SEO诊断` | Full site technical SEO health check |
| Competitor Analysis | `analyze competitor [url]`, `分析竞争对手 [url]` | Gap analysis, content comparison, opportunity identification |
| pSEO Generator | `generate pseo`, `生成pSEO页面` | Batch generate programmatic SEO pages |
| Internal Linking | `build internal links`, `构建内链` | Build site-wide internal link graph |
| Full Analysis | `seo analysis`, `SEO分析` | Comprehensive site analysis with prioritized recommendations |

---

## Module 1: Keyword Research

**Trigger**: `keyword research [topic]` / `分析关键词 [主题]`

### Workflow

1. **Search SERP Data** - Use WebSearch to get real-time results for target keywords
2. **Long-tail Discovery** - Generate variations: `[topic] + tutorial/guide/for [role]/best practices`
3. **Intent Classification** - Categorize as Informational/Navigational/Transactional
4. **Competition Analysis** - Assess difficulty based on SERP results
5. **PAA Extraction** - Identify "People Also Ask" opportunities
6. **Featured Snippet Opportunities** - Identify featured snippet potential

### Output Format

```markdown
## Keyword Research Report: [Topic]

### Primary Keywords
| Keyword | Intent | Difficulty | Opportunity Score |
|---------|--------|------------|-------------------|

### Long-tail Variations
- [keyword variation 1]
- [keyword variation 2]

### Content Recommendations
1. [Recommended article topic and angle]
2. [Recommended article topic and angle]

### PAA Questions to Target
- [Question 1]
- [Question 2]
```

---

## Module 2: Content Optimization

**Trigger**: `optimize content [path]` / `优化文章 [路径]`

### Analysis Criteria

1. **Title Optimization** (50-60 chars, includes power words)
2. **Meta Description** (150-160 chars, compelling CTA)
3. **Heading Hierarchy** (H1 → H2 → H3 logical flow)
4. **Keyword Density** (Primary keyword in first paragraph, natural distribution)
5. **Internal Links** (2-3 related posts, descriptive anchor text)
6. **Image Optimization** (Alt text present, descriptive)
7. **Schema Opportunity** (FAQ, HowTo, Article schema)
8. **Content Freshness** (Outdated references, version numbers)

### Auto-Fix (Safe Modifications)
- Add missing alt text
- Adjust meta description length
- Add missing Schema markup
- Insert internal links to related content

### Manual Review Queue
- Title changes (require user confirmation)
- Content restructuring
- Major rewrite suggestions

### Output Format

```markdown
## Content Optimization Report: [filename]

### SEO Score: [X]/100

### Quick Wins (Auto-fixable)
- [ ] [Issue 1] → [Fix]
- [ ] [Issue 2] → [Fix]

### Manual Review Required
- [ ] [Issue with explanation]

### Internal Link Suggestions
Link from: "[anchor text]" → /blog/[related-post]
```

---

## Module 3: Technical SEO Audit

**Trigger**: `seo audit` / `SEO诊断`

### Checks Performed

1. **Core Checks** (via /api/seo-health)
   - Sitemap accessibility
   - Robots.txt configuration
   - Homepage meta tags
   - Structured data validation
   - Page speed basics
   - Mobile friendliness

2. **Extended Checks**
   - Schema coverage (BlogPosting/Course/HowTo/FAQ)
   - Canonical tags consistency
   - Internal link health
   - Orphan page detection
   - Redirect chain analysis
   - Core Web Vitals indicators

### Output Format

```markdown
## Technical SEO Audit Report

### Overall Score: [X]/100 [Status Badge]

### Critical Issues (Fix Immediately)
- [Issue with impact and fix instructions]

### Warnings (Should Fix)
- [Issue with impact]

### Passed Checks
- [X] [Check name]

### Recommendations Priority Queue
1. [Highest impact fix]
2. [Second priority]
```

---

## Module 4: Competitor Analysis

**Trigger**: `analyze competitor [url]` / `分析竞争对手 [URL]`

### Analysis Points

1. **Content Structure** - Length, headings, media usage
2. **Keyword Coverage** - What keywords they rank for that we don't
3. **Schema Implementation** - Their structured data strategy
4. **SERP Features** - Featured snippets, PAA presence
5. **Internal Linking** - Their link architecture

### Output Format

```markdown
## Competitor Analysis: [URL]

### Content Comparison
| Metric | Competitor | Our Site | Gap |
|--------|------------|----------|-----|
| Avg. Content Length | | | |
| Schema Types | | | |

### Keyword Gap (They Rank, We Don't)
- [keyword 1]
- [keyword 2]

### Actionable Opportunities
1. [Opportunity with implementation suggestion]
```

---

## Module 5: pSEO Page Generator

**Trigger**: `generate pseo` / `生成pSEO页面`

### Workflow

1. **Load/Create Data Source** - `data/pseo_data.json`
2. **Generate Tech+Role Pages** - `app/templates/[tech]/[role]/page.tsx`
3. **Generate Feature Pages** - `app/solutions/[feature]/page.tsx`
4. **Ensure Content Uniqueness** - Unique titles, descriptions, FAQs
5. **Update Sitemap** - Add new routes to sitemap.ts
6. **Build Verification** - Run `npm run build` to validate

### Data Structure (pseo_data.json)

```json
{
  "technologies": [
    {
      "slug": "nextjs",
      "name": "Next.js",
      "description": "The React Framework for the Web",
      "features": ["SSR", "SSG", "API Routes"],
      "relatedPosts": []
    }
  ],
  "roles": [
    {
      "slug": "frontend-developer",
      "name": "Frontend Developer",
      "keywords": ["React", "CSS", "JavaScript"],
      "challenges": ["responsive design", "performance"]
    }
  ],
  "features": [
    {
      "slug": "dark-mode",
      "name": "Dark Mode",
      "description": "Eye-friendly dark theme support",
      "benefits": ["reduced eye strain", "battery saving"]
    }
  ],
  "templates": {
    "techRole": {
      "titlePattern": "Best {tech} Portfolio for {role}s | Build Your Developer Portfolio",
      "descriptionPattern": "Create a stunning {role} portfolio with {tech}. Features include {features}."
    }
  }
}
```

### Generated Page Structure

```tsx
// app/templates/[tech]/[role]/page.tsx
export async function generateStaticParams() {
  // Returns all tech × role combinations
}

export async function generateMetadata({ params }) {
  // Dynamic meta tags based on tech + role
}

export default function TemplatePage({ params }) {
  // Unique content for each combination
  // - Hero section
  // - Features grid
  // - Related blog posts
  // - FAQ section with Schema
  // - CTA
}
```

---

## Module 6: Internal Link Builder

**Trigger**: `build internal links` / `构建内链`

### Strategy

1. **Hub-and-Spoke Model**
   - Topic Hubs as central nodes
   - Blog posts as spokes
   - Guides as deep-dive connections

2. **Natural Anchor Text**
   - Identify keyword-rich phrases in content
   - Match with relevant target pages
   - Avoid over-optimization

3. **Link Distribution**
   - New posts → 2-3 internal links
   - Orphan pages → Add incoming links
   - High-authority pages → Use as link sources

### Output

```markdown
## Internal Link Report

### Site Link Graph Summary
- Total pages: X
- Average links per page: X
- Orphan pages: X

### Recommended Link Insertions
| Source | Anchor Text | Target | Reason |
|--------|-------------|--------|--------|

### Orphan Page Rescue
- [page] → Suggested link from [source]
```

---

## Module 7: Full SEO Analysis

**Trigger**: `seo analysis` / `SEO分析`

### Comprehensive Workflow

```
Step 1: Technical Health Check
    ↓
Step 2: Content Batch Scoring (all blog posts)
    ↓
Step 3: Keyword Gap Analysis (WebSearch for core topics)
    ↓
Step 4: Generate Prioritized Improvements
    ↓
Output: Comprehensive Report + Executable Fix List
```

### Output

```markdown
## Comprehensive SEO Analysis Report

Generated: [timestamp]

### Executive Summary
- Overall Health Score: [X]/100
- Critical Issues: X
- Quick Wins Available: X
- Estimated Impact: [High/Medium/Low]

### Technical Health
[Technical audit results]

### Content Analysis
[Batch content scoring]

### Keyword Opportunities
[Gap analysis results]

### Prioritized Action Items
1. [Highest impact, easiest fix]
2. [High impact]
3. ...

### One-Click Fixes Available
Run `apply seo fixes` to automatically fix X issues.
```

---

## Integration with Existing Infrastructure

### Leveraged Components

| Component | Usage |
|-----------|-------|
| `/api/seo-health` | Base for technical audit |
| `lib/schemas.ts` | Schema generation (if exists) |
| `lib/content-similarity.ts` | Related content for internal links |
| `lib/topic-hubs.ts` | Hub pages for pSEO |
| `lib/guides.ts` | Guide data for link building |
| `sitemap.ts` | Add pSEO routes |

### Collaboration with ai-blog-writer

```
ai-blog-writer creates content
        ↓
pseo-engine optimizes content
        ↓
Publish optimized article
```

---

## Safety Guidelines

### Auto-Apply (Safe)
- Meta description length adjustments
- Missing alt text additions
- Schema markup insertions
- Sitemap updates

### Require Confirmation
- Title changes
- Content restructuring
- Deleting/replacing content
- Creating new pages

### Never Auto-Apply
- Removing existing links
- Changing URLs
- Modifying canonical tags

---

## Reference Files

- Optimization Rules: [references/optimization-rules.md](references/optimization-rules.md)
- Schema Templates: [references/schema-templates.md](references/schema-templates.md)
- SERP Patterns: [references/serp-patterns.md](references/serp-patterns.md)
- Keyword Cache: [references/keyword-database.json](references/keyword-database.json)

---

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `seo audit` | Run technical SEO health check |
| `keyword research [topic]` | Research keywords for a topic |
| `optimize content [path]` | Analyze and optimize a specific article |
| `optimize all content` | Batch analyze all blog posts |
| `generate pseo` | Generate programmatic SEO pages |
| `build internal links` | Analyze and suggest internal links |
| `analyze competitor [url]` | Analyze competitor page |
| `seo analysis` | Full comprehensive SEO analysis |
| `apply seo fixes` | Apply all safe auto-fixes |
