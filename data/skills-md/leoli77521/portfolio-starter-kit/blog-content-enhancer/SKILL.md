---
name: blog-content-enhancer
description: "Blog content enhancement skill for improving article quality through real-time research, visual enrichment, and natural language refinement. Triggers on keywords like 'enhance article', 'improve blog', 'enrich content', 'add data', 'research topic', '提升文章', '充实内容', '增强说服力', '图文并茂'."
version: "1.0.0"
author: "tolearn.blog"
tags: ["content-enhancement", "research", "visualization", "persuasion"]
---

# Blog Content Enhancer

专为 tolearn.blog 设计的博客内容增强技能，通过实时研究、数据支撑和视觉优化提升文章质量。

## Core Capabilities

### 1. Real-time Research (实时研究)
- Search for latest statistics, trends, and case studies
- Verify claims with authoritative sources
- Find relevant quotes from industry experts

### 2. Content Analysis (内容分析)
- Evaluate article structure and flow
- Identify gaps in argumentation
- Assess readability and engagement

### 3. Visual Enrichment (视觉增强)
- Suggest strategic image placements
- Recommend diagram types for concepts
- Provide image description templates

### 4. Persuasion Enhancement (说服力增强)
- Add data-backed claims
- Include relevant case studies
- Strengthen arguments with citations

### 5. Language Refinement (语言优化)
- Convert formal language to conversational tone
- Improve sentence flow and transitions
- Ensure active voice usage

---

## Commands

### `research [topic]`
Search for real-time data and statistics on a topic.

**Usage:**
```
/blog-content-enhancer research "AI adoption rates 2025"
```

**Process:**
1. Use WebSearch to find latest data (prioritize 2025-2026 sources)
2. Extract key statistics and trends
3. Format findings with proper citations
4. Return structured research summary

### `analyze content [path]`
Evaluate an article and identify improvement opportunities.

**Usage:**
```
/blog-content-enhancer analyze content app/blog/posts/my-article.mdx
```

**Analysis Criteria:**
- **Structure Score**: Heading hierarchy, section balance
- **Data Density**: Statistics, citations, external references
- **Visual Score**: Image placements, diagram opportunities
- **Readability**: Sentence variety, jargon level
- **Engagement**: Hooks, examples, call-to-actions

**Output Format:**
```markdown
## Content Analysis Report

### Overall Score: X/100

### Strengths
- [List identified strengths]

### Improvement Opportunities
1. [Specific suggestion with location]
2. [Specific suggestion with location]

### Recommended Enhancements
- [ ] Add statistic at [section]
- [ ] Insert image after [paragraph]
- [ ] Strengthen conclusion with CTA
```

### `enhance article [path]`
Complete enhancement workflow for a blog article.

**Usage:**
```
/blog-content-enhancer enhance article app/blog/posts/my-article.mdx
```

**Workflow:**
1. **Read & Analyze**: Load article, assess quality
2. **Research**: Search for relevant data based on topic
3. **Plan Enhancements**: Map out data insertion points, image locations
4. **Execute Changes**: Apply enhancements while preserving voice
5. **Validate**: Check MDX syntax, verify links

### `improve language [path]`
Focus on language refinement only.

**Usage:**
```
/blog-content-enhancer improve language app/blog/posts/my-article.mdx
```

**Transformations:**
- Formal → Conversational
- Passive → Active voice
- Complex → Clear
- Add transition phrases
- Vary sentence structure

### `suggest images [path]`
Analyze article and recommend image placements.

**Usage:**
```
/blog-content-enhancer suggest images app/blog/posts/my-article.mdx
```

**Output:**
```markdown
## Image Suggestions

### Position 1: After Introduction
- **Type**: Hero/conceptual image
- **Suggested content**: [Description]
- **Alt text**: [SEO-optimized alt text]

### Position 2: Section "Getting Started"
- **Type**: Diagram/flowchart
- **Suggested content**: [Description]
- **Alt text**: [SEO-optimized alt text]
```

---

## Enhancement Workflow

```
┌─────────────────────────────────────────────────────────┐
│            Blog Content Enhancement Workflow            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Article Analysis                                    │
│     └─ Read MDX → Parse structure → Generate report    │
│                                                         │
│  2. Real-time Research                                  │
│     └─ Extract topics → WebSearch → Compile citations  │
│                                                         │
│  3. Enhancement Planning                                │
│     └─ Map image spots → Plan data points → Mark edits │
│                                                         │
│  4. Content Enhancement                                 │
│     └─ Insert data → Add images → Refine language      │
│                                                         │
│  5. Validation                                          │
│     └─ Check MDX syntax → Verify links → Compare diff  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Research Guidelines

### Source Hierarchy
1. **Primary Sources**: Official reports, research papers
2. **Industry Reports**: Gartner, McKinsey, Statista
3. **Tech Publications**: TechCrunch, Ars Technica, The Verge
4. **Developer Resources**: Official docs, GitHub stats

### Citation Format
```markdown
According to [Source Name](URL), [statistic or quote]. (Published: Month Year)
```

### Freshness Requirements
- **Strongly Prefer**: 2025-2026 data
- **Acceptable**: 2024 data if more recent unavailable
- **Avoid**: Pre-2023 data unless historically relevant

---

## Visual Guidelines

### Image Template (MDX Format)
```mdx
<figure className="my-8">
  <img
    src="/images/[filename].png"
    alt="[Descriptive alt text for accessibility and SEO]"
    className="w-full h-auto rounded-lg shadow-lg"
  />
  <figcaption className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
    [Figure caption explaining the image]
  </figcaption>
</figure>
```

### Image Placement Rules
1. **After Introduction**: Set context visually
2. **Complex Concepts**: Before or after explanation
3. **Code Examples**: Screenshot of result if applicable
4. **Conclusion**: Summarizing graphic or CTA image

### Alt Text Best Practices
- Describe content, not appearance
- Include relevant keywords naturally
- Keep under 125 characters
- Be specific: "Dashboard showing API response times" not "Screenshot"

---

## Language Patterns

### Formal → Conversational Conversions

| Formal | Conversational |
|--------|----------------|
| "It is important to note that..." | "Here's the key thing:" |
| "This enables users to..." | "This lets you..." |
| "The implementation demonstrates..." | "This shows how..." |
| "Subsequently, one must..." | "Next, you'll need to..." |
| "It should be mentioned that..." | "Worth noting:" |

### Transition Phrases

**Addition:**
- What's more, ...
- On top of that, ...
- Here's another thing: ...

**Contrast:**
- That said, ...
- But here's the catch: ...
- On the flip side, ...

**Example:**
- Take [X] for instance: ...
- Here's a real example: ...
- Case in point: ...

**Conclusion:**
- The bottom line: ...
- So what does this mean? ...
- Here's the takeaway: ...

---

## Quality Checklist

Before completing enhancement, verify:

### Data & Citations
- [ ] All statistics have sources
- [ ] Sources are from 2024-2026
- [ ] Links are valid and accessible
- [ ] Quotes are accurately attributed

### Visual Elements
- [ ] Images have descriptive alt text
- [ ] Figures have captions
- [ ] Placement enhances understanding
- [ ] MDX syntax is correct

### Language & Style
- [ ] Active voice predominates
- [ ] Sentences vary in length
- [ ] Technical jargon is explained
- [ ] Transitions are smooth

### Technical
- [ ] MDX compiles without errors
- [ ] Internal links work
- [ ] No broken external links
- [ ] Metadata is complete

---

## Reference Files

- For research sources: See [references/research-sources.md](references/research-sources.md)
- For visual guidelines: See [references/visual-guidelines.md](references/visual-guidelines.md)
- For language patterns: See [references/language-patterns.md](references/language-patterns.md)

---

## Integration with Other Skills

### With ai-blog-writer
- Use ai-blog-writer for initial draft creation
- Apply blog-content-enhancer for quality improvement
- Flow: Write → Enhance → Publish

### With pseo-engine
- Use pseo-engine for SEO optimization
- Use blog-content-enhancer for content quality
- Flow: Research → Write → Enhance → Optimize SEO
