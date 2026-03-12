---
name: seo-article-writing
description: A comprehensive workflow for creating high-ranking SEO blog articles with keyword research, competitive analysis, AI-generated unique images, and optimized content structure
---

## When to Use

- Setting up a blog section for SEO
- Writing blog articles for organic traffic
- Creating comparison/review content
- Building content marketing assets
- Any project needing a file-based blog CMS

## Prerequisites

Before writing articles, ensure:
1. Blog infrastructure is set up (see [Blog Setup](#blog-infrastructure-setup))
2. AI image generation capability is available
3. MDX support is configured in your bundler

---

## Quick Start

```bash
# 1. Set up blog infrastructure (first time only)
# Copy assets from this skill to your project

# 2. Create article folder
mkdir -p src/content/blog/{slug}

# 3. Generate unique article image using AI
# See Image Generation section below

# 4. Write article using template
# Use assets/templates/article.mdx as base
```

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SETUP (One-time)                                            │
│     └─> Blog infrastructure                                     │
├─────────────────────────────────────────────────────────────────┤
│  2. RESEARCH                                                    │
│     └─> Keywords → Competitors → Content gaps                   │
├─────────────────────────────────────────────────────────────────┤
│  3. OUTLINE                                                     │
│     └─> Structure → Tables → FAQs                               │
├─────────────────────────────────────────────────────────────────┤
│  4. IMAGE GENERATION                                            │
│     └─> AI-generate unique image for article content            │
├─────────────────────────────────────────────────────────────────┤
│  5. WRITE                                                       │
│     └─> Draft → Optimize → Review                               │
├─────────────────────────────────────────────────────────────────┤
│  6. PUBLISH                                                     │
│     └─> MDX file → Sitemap → Verify                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Image Generation (CRITICAL)

### Philosophy

**Every article MUST have a unique, content-specific image.** Do NOT use generic pattern backgrounds. Generate a custom image that:

1. Visually represents the article topic
2. Includes relevant text/title overlay
3. Has a consistent brand style (dark theme, orange accents)
4. Is sized 1200x630 pixels for OG sharing

### Image Generation Process

For EACH article, use AI image generation with this template:

```
A sophisticated hero image for "[ARTICLE TITLE]" blog article.
[DESCRIBE VISUAL CONCEPT THAT MATCHES CONTENT]
Dark background (#0f172a or #1e293b) with orange (#f97316) accents.
Modern, minimalist, professional SaaS style like Linear or Vercel.
Include text overlay: "[TITLE]" and optional subtitle.
1200x630 pixels.
```

### Example Prompts by Article Type

#### Comparison Article
```
A sophisticated hero image for "Sunsama Alternatives" comparison article.
Modern minimalist design with floating app icons and comparison cards.
Deep navy background (#0f172a) with orange (#f97316) gradient accents.
Show multiple tools being compared with visual hierarchy.
Include title text overlay. Professional SaaS marketing style.
1200x630 pixels.
```

#### Guide/Tutorial Article
```
A sophisticated hero image for "Time Blocking Guide" tutorial article.
Modern minimalist design showing calendar grid with colorful time blocks.
Dark slate background (#1e293b) with vibrant orange (#f97316) blocks.
Clean 3D floating elements suggesting productivity and organization.
Include title: "TIME BLOCKING GUIDE" and subtitle "Master Your Day".
1200x630 pixels.
```

#### VS/Comparison Article
```
A sophisticated hero image for "Time Blocking vs To-Do Lists" comparison.
Split design: left side shows organized calendar blocks, right side shows
scattered checklist items. Visual contrast between order and chaos.
Dark background with orange (#f97316) and blue (#3b82f6) accents.
Include title text. Editorial style. 1200x630 pixels.
```

#### Self-Hosted/Technical Article
```
A sophisticated hero image for "Self-Hosted Productivity Apps" article.
Server/cloud icon with data flowing to personal devices.
Emphasizes privacy and control with lock/shield symbols.
Dark navy background with green (#22c55e) security accents and orange highlights.
Include title and tagline about privacy/control. 1200x630 pixels.
```

#### Routine/Habit Article
```
A sophisticated hero image for "Daily Planning Routine" habit article.
Morning scene with coffee, notebook, and digital calendar interface.
Soft gradient from deep purple to warm orange (#f97316).
Floating UI elements showing checklist items.
Calm, productive, aspirational mood. Include title. 1200x630 pixels.
```

### Image Naming Convention

Save images with descriptive names:
```
public/blog-{slug}.png

Examples:
- blog-sunsama-alternatives.png
- blog-time-blocking-guide.png
- blog-self-hosted.png
- blog-daily-planning-routine.png
```

### Updating Frontmatter

After generating, update the article frontmatter:
```javascript
export const frontmatter = {
  // ...other fields
  image: "/blog-{slug}.png"
};
```

---

## Blog Infrastructure Setup

### Required Files

Copy these from `assets/` to your project:

```
your-project/
├── src/
│   ├── content/
│   │   └── blog/           # MDX articles go here
│   │       └── {slug}/
│   │           └── index.mdx
│   ├── types/
│   │   └── blog.ts         # Copy from assets/templates/
│   ├── lib/
│   │   └── blog.ts         # Copy from assets/templates/
│   ├── components/
│   │   └── blog/
│   │       ├── blog-card.tsx
│   │       └── blog-layout.tsx
│   └── routes/
│       ├── blog.tsx        # Blog listing
│       └── blog.$slug.tsx  # Individual post
└── public/
    └── blog-{slug}.png     # Generated images per article
```

### Vite/React Setup

For Vite projects, use `import.meta.glob` to load MDX files:

```typescript
// src/lib/blog.ts
const modules = import.meta.glob('../content/blog/*/index.mdx', { eager: true });
```

### Next.js Setup

For Next.js projects, use `@next/mdx` or `contentlayer`:

```typescript
// next.config.js
import mdx from '@next/mdx';
const withMDX = mdx({ extension: /\.mdx?$/ });
export default withMDX({ pageExtensions: ['ts', 'tsx', 'mdx'] });
```

---

## Keyword Research

### Step 1: Primary Keyword Selection

Use web search to research your topic:

```
Search queries to run:
- "[topic] 2026"
- "best [topic]"
- "[topic] alternative"
- "[topic] vs [competitor]"
```

### Step 2: Classify Search Intent

| Intent | Indicators | Content Type | Priority |
|--------|-----------|--------------|----------|
| Transactional | "best", "alternative", "buy" | Comparison, review | HIGH |
| Informational | "how to", "what is", "guide" | Tutorial, explainer | MEDIUM |
| Navigational | Brand names, specific tools | Feature page | LOW |

### Subagent Prompt: Keyword Research

```
You are an SEO expert. Research keywords for [TOPIC].

Use web search to find:
1. Primary keyword with highest search intent
2. 5 secondary keywords (long-tail variations)
3. Top 5 competitor URLs for analysis
4. Content gaps competitors are missing

Return:
- Prioritized keyword list with intent classification
- Recommended content angle
- Estimated search volume (HIGH/MEDIUM/LOW)
```

---

## Article Structure

### Frontmatter Template

```javascript
export const frontmatter = {
  title: "SEO Title Under 60 Characters with Primary Keyword",
  description: "Meta description 150-160 chars with keyword and compelling hook.",
  date: "2026-01-30",
  author: "Team Name",
  tags: ["primary-tag", "secondary-tag", "category"],
  readingTime: 10,
  image: "/blog-your-article-slug.png"  // UNIQUE image per article!
};
```

### Article Outline Template

```markdown
# [Primary Keyword in H1 Title]

## Introduction
- Hook with statistic or pain point
- What reader will learn
- Establish credibility (1-2 paragraphs)

## [Section 2: Definition/Background]
- What is [topic]?
- Why it matters (2-3 paragraphs)

## [Section 3: Core Content / How-To]
- Main value proposition
- Step-by-step if tutorial
- Numbered list for scanability

## [Section 4: Comparison Table]

| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Price   | Free     | $10/mo   | $25/mo   |
| Feature | ✅       | ✅       | ❌       |

## [Section 5: Detailed Analysis]
- 3-4 paragraphs per option
- Pros and cons
- Best use cases

## Frequently Asked Questions

### What is [primary keyword]?
[2-3 sentence answer targeting featured snippet]

### Is [option A] better than [option B]?
[Honest comparison with recommendation]

## Conclusion
- Summary of key points
- Clear CTA with link to action
```

---

## Writing Guidelines

### SEO Best Practices

| Element | Guideline |
|---------|-----------|
| Title | Primary keyword, under 60 characters |
| Meta description | 150-160 chars, keyword, compelling hook |
| H2 headers | Include secondary keywords naturally |
| Keyword density | 1-2% for primary keyword |
| Internal links | 2-3 links to relevant pages |
| External links | 1-2 authoritative sources |

### Word Count Targets

| Content Type | Minimum Words | Optimal |
|--------------|---------------|---------|
| Comparison/Review | 2,000 | 2,500 |
| Complete Guide | 2,500 | 3,500 |
| How-To Tutorial | 1,500 | 2,000 |
| Thought Leadership | 1,800 | 2,200 |

---

## Complete Article Creation Workflow

### Step 1: Research
```
Use keyword research agent to identify:
- Primary keyword
- Secondary keywords  
- Top 5 competitors
- Content gaps
```

### Step 2: Generate Image
```
Use AI image generation with article-specific prompt.
Save to public/blog-{slug}.png
```

### Step 3: Create Article Folder
```bash
mkdir -p src/content/blog/{slug}
touch src/content/blog/{slug}/index.mdx
```

### Step 4: Write Content
```
Use article writer agent with:
- Keyword targets
- Word count requirement
- Comparison tables
- FAQ section
```

### Step 5: Update Frontmatter
```javascript
export const frontmatter = {
  title: "...",
  description: "...",
  date: "YYYY-MM-DD",
  author: "Team Name",
  tags: ["..."],
  readingTime: X,
  image: "/blog-{slug}.png"  // Your generated image
};
```

### Step 6: Add to Sitemap
```xml
<url>
  <loc>https://yoursite.com/blog/{slug}</loc>
  <lastmod>{date}</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

### Step 7: Verify
- Image displays correctly on blog listing
- Article renders properly
- All links work
- Sitemap is valid

---

## Subagent Prompts

### Image Generation Agent

```
Generate a unique blog hero image for: "[ARTICLE TITLE]"

Topic: [brief description]
Style: Dark background, orange accents, modern SaaS aesthetic
Include: Title text overlay, relevant visual elements
Size: 1200x630 pixels

Save as: blog-{slug}.png
```

### Article Writer Agent

```
Write a [WORD_COUNT]+ word SEO article on [TOPIC].

Primary keyword: [KEYWORD]
Secondary keywords: [KEYWORD_LIST]

Include:
1. Frontmatter with all required fields
2. Introduction with hook/statistic
3. Comparison table with 4+ options
4. Detailed breakdown (3-4 paragraphs per option)
5. FAQ section with 5+ questions using h3 headers
6. Conclusion with CTA linking to [PAGE]

Image has been generated at: /blog-{slug}.png
Include this in frontmatter.
```

### FAQ Writer Agent

```
Write 7 FAQ questions for article about [TOPIC].

Target keywords:
- [keyword 1]
- [keyword 2]
- [keyword 3]

Use h3 headers (###) for each question.
Each answer should be 2-3 sentences.
Target featured snippet format (direct, concise).
```

---

## Publishing Checklist

- [ ] **Unique image generated** for this specific article
- [ ] Image saved to `public/blog-{slug}.png`
- [ ] Image path in frontmatter matches file
- [ ] Primary keyword in title
- [ ] Meta description optimized (150-160 chars)
- [ ] At least 1 comparison table
- [ ] At least 5 FAQ questions
- [ ] Internal links added (2-3)
- [ ] Reading time calculated
- [ ] Tags assigned (2-4)
- [ ] Date set correctly
- [ ] Article added to sitemap.xml

---

## File References

See `assets/` folder for:

| File | Purpose |
|------|---------|
| `templates/blog-types.ts` | TypeScript interfaces |
| `templates/blog-utils.ts` | Utility functions for loading MDX |
| `templates/article.mdx` | Article template |
| `components/blog-card.tsx` | Card component for listing |
| `components/blog-layout.tsx` | Layout for individual posts |
| `scripts/setup-blog.sh` | Quick setup script |

---

## Updates

- **v1.1** (2026-01-31): Updated to require unique AI-generated images per article
- **v1.0** (2026-01-30): Initial skill with complete workflow
