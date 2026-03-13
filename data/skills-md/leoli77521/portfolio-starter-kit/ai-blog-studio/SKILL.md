---
name: ai-blog-studio
description: "AI Blog Studio: Complete blog writing and enhancement toolkit for tolearn.blog. Combines writing, research, SEO, and content enhancement into one unified workflow. Triggers on: 'write blog', 'blog post', 'article', 'tutorial', 'tolearn', 'enhance article', 'improve blog', 'enrich content', 'add data', 'research topic', 'complete blog', 'full article', 'publish-ready'."
version: "2.0.0"
author: "tolearn.blog"
tags: ["blog-writing", "content-enhancement", "seo", "research", "ai-programming"]
---

# AI Blog Studio

Complete blog writing and enhancement toolkit for tolearn.blog.
专为 tolearn.blog 设计的统一博客创作工具，整合写作、研究、SEO和内容增强功能。

---

## Quick Start

| Command | Description |
|---------|-------------|
| `write [topic]` | Full workflow: research → outline → draft → enhance → validate |
| `enhance [path]` | Enhance existing article with data, visuals, language refinement |
| `analyze [path]` | Quality analysis only, with scoring and suggestions |
| `research [topic]` | Search for latest data and statistics with citations |

---

## Capabilities

### 1. Writing (写作)
- 4 article templates (Tutorial, Comparison, Explainer, List)
- Structured outlines with clear sections
- Voice guidelines for conversational yet professional tone
- Code examples with best practices

### 2. Research (研究)
- Real-time WebSearch for latest data (2025-2026)
- Source hierarchy with authority levels
- Citation formatting with proper attribution
- Trend and statistic discovery

### 3. SEO Optimization (SEO优化)
- Title optimization (50-60 characters)
- Meta description guidelines
- Keyword strategy (primary, secondary, long-tail)
- Schema markup for tutorials
- Internal/external linking strategy

### 4. Enhancement (增强)
- Language refinement (formal → conversational)
- Data-backed claims insertion
- Visual suggestions with MDX templates
- Transition phrase optimization

### 5. Visual Content (视觉内容) ✨
- **Mermaid图表自动生成**: 根据内容类型推荐合适的图表 (流程图、架构图、时序图、状态图、类图)
- **免费图库搜索**: 推荐Unsplash/Pexels/Pixabay等图库，提供搜索关键词策略
- **AI图片提示词**: DALL-E/Midjourney提示词模板 (Hero图、技术架构、对比图、数据可视化)

### 6. Validation (验证)
- SEO checklist verification
- MDX syntax validation
- Quality scoring (structure, data, visuals, readability)
- Pre-publish checklist

---

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              AI Blog Studio - Complete Workflow             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. RESEARCH (研究)                                          │
│     └─ WebSearch → Collect latest data → Format citations   │
│                                                             │
│  2. OUTLINE (大纲)                                           │
│     └─ Select template → Plan structure → Define key points │
│                                                             │
│  3. DRAFT (初稿)                                             │
│     └─ Apply style guide → Add code examples → Insert data  │
│                                                             │
│  4. ENHANCE (增强)                                           │
│     └─ Language polish → Image suggestions → Internal links │
│                                                             │
│  5. VALIDATE (验证)                                          │
│     └─ SEO check → MDX syntax → Quality scoring             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Commands

### `write [topic]`

Create a complete blog post from scratch using the full workflow.

**Usage:**
```
/ai-blog-studio write "Building AI Agents with Claude"
```

**Process:**
1. **Research Phase**: Use WebSearch to gather latest statistics, trends, and case studies
2. **Outline Phase**: Generate structured outline based on best-fit template
3. **Draft Phase**: Write content following style guide and voice guidelines
4. **Enhance Phase**: Add data citations, suggest images, refine language
5. **Validate Phase**: Run SEO checks, verify MDX syntax, generate quality report

**Output:** Complete MDX article ready for publishing

---

### `enhance [path]`

Enhance an existing article with research, data, and polish.

**Usage:**
```
/ai-blog-studio enhance app/blog/posts/my-article.mdx
```

**Process:**
1. Read and analyze current article
2. Search for relevant data to support claims
3. Identify image placement opportunities
4. Refine language for engagement
5. Validate all changes

---

### `analyze [path]`

Generate a quality report without making changes.

**Usage:**
```
/ai-blog-studio analyze app/blog/posts/my-article.mdx
```

**Output:**
```markdown
## Content Analysis Report

### Overall Score: X/100

### Scores by Category
- Structure: X/25
- Data Density: X/25
- Visual Elements: X/25
- Language Quality: X/25

### Strengths
- [Identified strengths]

### Improvement Opportunities
1. [Specific suggestion with location]
2. [Specific suggestion with location]

### Recommended Actions
- [ ] Add statistic at [section]
- [ ] Insert image after [paragraph]
- [ ] Strengthen conclusion with CTA
```

---

### `research [topic]`

Search for real-time data and compile research summary.

**Usage:**
```
/ai-blog-studio research "AI adoption rates 2026"
```

**Process:**
1. Use WebSearch with optimized queries
2. Prioritize 2025-2026 sources
3. Extract key statistics and quotes
4. Format with proper citations

**Output:**
```markdown
## Research Summary: [Topic]

### Key Statistics
- [Statistic 1] — [Source](URL) (2026)
- [Statistic 2] — [Source](URL) (2025)

### Expert Quotes
> "[Quote]" — [Name], [Title] at [Company]

### Trends & Insights
1. [Trend 1]
2. [Trend 2]

### Recommended Sources
- [Source 1](URL) - [Why it's relevant]
- [Source 2](URL) - [Why it's relevant]
```

---

## Writing Guidelines

### Target Audience
- English-speaking developers and tech enthusiasts in US/Europe
- Skill levels: beginner to intermediate
- Interest areas: AI tools, LLMs, practical programming tutorials

### Voice & Tone
- Conversational but professional
- First-person perspective ("I discovered...", "Let me show you...")
- Avoid overly formal academic language
- Use humor sparingly and appropriately
- Be direct and actionable

### Content Structure

```
1. Hook (1-2 sentences) - Grab attention with a problem or question
2. Introduction (2-3 paragraphs) - Context and what reader will learn
3. Main Content - Step-by-step with code examples
4. Practical Tips - Real-world applications
5. Conclusion - Summary + Call to action
```

### Code Examples
- Always explain BEFORE showing code
- Include comments in code
- Show complete, runnable examples
- Specify language for syntax highlighting
- Break long code into digestible chunks

---

## Research Guidelines

### Source Hierarchy

| Priority | Source Type | Examples |
|----------|-------------|----------|
| 1 | Primary/Official | Anthropic Research, OpenAI Blog, Google AI |
| 2 | Industry Reports | Gartner, McKinsey, Statista |
| 3 | Tech Publications | TechCrunch, Ars Technica, The Verge |
| 4 | Developer Resources | Official docs, GitHub stats, Stack Overflow |

### Freshness Requirements
```
2026        ████████████ Strongly Preferred
2025        ██████████   Preferred
2024        ██████       Acceptable
Pre-2024    ████         Only for historical context
```

### Citation Format
```markdown
According to [Source Name](URL), [statistic or quote]. (Published: Month Year)
```

---

## SEO Guidelines

### Title Optimization
- **Length**: 50-60 characters
- **Format**: `[Action Verb] + [Topic] + [Benefit/Year]`
- **Power words**: How, Why, Guide, Best, Ultimate, Easy

### Meta Description
- **Length**: 150-160 characters
- Include primary keyword naturally
- End with call-to-action or benefit

### Keyword Strategy
| Type | Placement |
|------|-----------|
| Primary | Title, H1, first paragraph, URL slug |
| Secondary | H2 headings |
| Long-tail | Subheadings, body content |
| LSI | Natural body content |

### Schema Markup (for tutorials)
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [Action]",
  "step": [
    {"@type": "HowToStep", "name": "Step 1", "text": "..."}
  ]
}
```

---

## Visual Guidelines

### Image Placement Rules
| Position | Purpose | Image Type |
|----------|---------|------------|
| After intro | Set context | Hero, conceptual |
| Before complex section | Prepare reader | Diagram, overview |
| After explanation | Reinforce | Example, screenshot |
| At data points | Visualize stats | Chart, infographic |
| Before conclusion | Summarize | Summary graphic |

### MDX Image Template
```mdx
<figure className="my-8">
  <img
    src="/images/[filename].png"
    alt="[Descriptive text for accessibility and SEO]"
    className="w-full h-auto rounded-lg shadow-lg"
  />
  <figcaption className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
    [Caption explaining the image]
  </figcaption>
</figure>
```

### Alt Text Best Practices
- Describe content, not appearance
- Include relevant keywords naturally
- Length: 50-125 characters
- Be specific: "Dashboard showing API response times" not "Screenshot"

### Mermaid图表 (自动生成)

根据内容类型自动建议图表代码：

| 内容类型 | 图表类型 | 示例场景 |
|---------|---------|---------|
| 步骤说明 | flowchart TD | 教程、配置指南 |
| 系统设计 | flowchart LR + subgraph | 架构概览 |
| API交互 | sequenceDiagram | 请求流程 |
| 状态变化 | stateDiagram-v2 | 生命周期 |
| 数据结构 | classDiagram | 类型定义 |

### 免费图库

| 图库 | 特点 | 推荐用途 |
|------|------|---------|
| Unsplash | 高质量摄影 | Hero图、背景 |
| Pexels | 综合素材 | 通用配图 |
| unDraw | 技术插画 | 技术博客 |

### AI图片提示词模板

提供按场景分类的DALL-E/Midjourney提示词：
- **Hero概念图**: 科技简约风格，渐变色彩
- **技术架构图**: 等距立体风格，标注组件
- **对比图**: 分屏设计，对比色彩
- **数据可视化**: 抽象数据流，未来感

详见 [image-guidelines.md](references/visuals/image-guidelines.md)

---

## Quality Checklist

### Before Publishing

#### Content & Structure
- [ ] Title is 50-60 characters and compelling
- [ ] Meta description is 150-160 characters
- [ ] First paragraph hooks the reader
- [ ] Headings follow H2 → H3 hierarchy
- [ ] Reading time is appropriate (5-10 min ideal)

#### Code & Technical
- [ ] All code examples are tested and working
- [ ] Code blocks specify language
- [ ] Technical jargon is explained on first use

#### Data & Citations
- [ ] All statistics have sources
- [ ] Sources are from 2024-2026
- [ ] Links are valid and accessible
- [ ] Quotes are accurately attributed

#### Visual Elements
- [ ] Images have descriptive alt text
- [ ] Figures have captions
- [ ] Strategic image placement (every 300-500 words)

#### SEO & Links
- [ ] Internal links to 2-3 related posts
- [ ] Descriptive anchor text (not "click here")
- [ ] Call-to-action in conclusion

#### Language
- [ ] Active voice predominates (>80%)
- [ ] Sentences vary in length
- [ ] Tone is conversational and professional
- [ ] No grammar/spelling errors

---

## Reference Files

| Category | File | Description |
|----------|------|-------------|
| Writing | [templates.md](references/writing/templates.md) | 4 article templates |
| Writing | [style-guide.md](references/writing/style-guide.md) | Voice, tone, language patterns |
| Writing | [code-examples.md](references/writing/code-examples.md) | Code formatting best practices |
| SEO | [seo-guide.md](references/seo/seo-guide.md) | Complete SEO reference |
| Research | [sources.md](references/research/sources.md) | Source hierarchy and citations |
| Visuals | [image-guidelines.md](references/visuals/image-guidelines.md) | Image templates and alt text |

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_outline.py` | Generate structured outlines | `python scripts/generate_outline.py tutorial "Topic"` |
| `seo_check.py` | Analyze SEO of markdown files | `python scripts/seo_check.py path/to/article.md` |

---

## Integration with Other Skills

### With pseo-engine
- Use ai-blog-studio for content creation
- Use pseo-engine for advanced SEO analysis and programmatic pages
- Flow: Research → Write → Enhance → Optimize SEO → Publish
