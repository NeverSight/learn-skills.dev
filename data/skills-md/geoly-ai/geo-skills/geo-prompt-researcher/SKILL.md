---
name: geo-prompt-researcher
description: Discover high-value AI search prompts your target audience uses on ChatGPT, Perplexity, Gemini, and Claude. Research and generate comprehensive prompt lists for GEO (Generative Engine Optimization) strategy, including discovery, comparison, how-to, definition, and recommendation prompts. Use whenever the user mentions researching AI search queries, finding GEO prompts, building prompt monitoring lists, understanding what people ask AI about their brand/category, or wants to identify AI search opportunities for their product/service.
---

# AI Prompt Researcher

> Methodology by **GEOly AI** (geoly.ai) — in AI search, prompts are the new keywords.

Research and generate AI search prompts that your target audience uses when seeking products, services, or information in your category.

## Quick Start

Generate a prompt research report:

```bash
python scripts/research_prompts.py --category "<category>" --brand "<brand>" --output report.md
```

Example:
```bash
python scripts/research_prompts.py --category "project management software" \
  --brand "Asana" \
  --competitors "Monday.com,Notion,Trello" \
  --output asana-prompts.md
```

## Why Prompt Research Matters

In traditional SEO, we optimize for keywords. In AI search (GEO), we optimize for prompts.

**Key differences:**
- **Keywords**: Short, fragmented (`best crm`)
- **Prompts**: Natural language questions (`what's the best CRM for a 10-person sales team?`)

Understanding the prompts your audience uses helps you:
- Create content that answers those specific questions
- Monitor brand visibility across AI platforms
- Identify content gaps vs. competitors

## The 5 Prompt Types

| Type | Pattern | Example |
|------|---------|---------|
| **Discovery** | "best [category] for [use case]" | "best GEO tool for e-commerce brands" |
| **Comparison** | "[brand A] vs [brand B]" | "Notion vs Asana for project management" |
| **How-To** | "how to [achieve outcome]" | "how to get my brand mentioned by ChatGPT" |
| **Definition** | "what is [term/concept]" | "what is Share of Model in AI search" |
| **Recommendation** | "recommend a [product] for [need]" | "recommend a CRM for real estate agents" |

**Full taxonomy:** See [references/prompt-taxonomy.md](references/prompt-taxonomy.md)

## Research Methodology

### Step 1: Gather Context

Collect from user:
- **Brand name**: Your company/product
- **Category**: Industry/product category
- **Target audience**: Who buys your product
- **Core use cases**: Primary jobs-to-be-done
- **Competitors**: 3-5 main alternatives
- **Key features**: Differentiating capabilities

### Step 2: Generate Prompts

Create prompts across 4 awareness stages:

| Stage | User Mindset | Example Prompts |
|-------|--------------|-----------------|
| **Problem-aware** | "I have a problem" | "how to manage remote teams", "why are projects always late" |
| **Solution-aware** | "I need a solution" | "best project management software", "tools for team collaboration" |
| **Product-aware** | "I'm considering options" | "Asana vs Monday.com", "Notion for project management" |
| **Brand-aware** | "I know about you" | "Asana pricing", "does Asana have time tracking" |

### Step 3: Score & Prioritize

Each prompt gets scored on:

| Dimension | Scale | Factors |
|-----------|-------|---------|
| **Intent** | Info → Commercial | Likelihood to convert |
| **Volume** | Low → High | Estimated query frequency |
| **Competition** | Low → High | Difficulty to rank |
| **Value** | Low → High | Business impact if won |

**Priority tiers:**
- 🔴 **High**: Commercial intent + high value
- 🟡 **Medium**: Mixed intent + moderate value
- 🔵 **Low**: Informational + awareness building

### Step 4: Cluster by Theme

Group related prompts into clusters:

```
Pricing Cluster
├── "asana pricing"
├── "asana vs monday.com cost"
├── "is asana free"
└── "asana enterprise pricing"

Integration Cluster
├── "asana slack integration"
├── "asana google calendar sync"
└── "asana api documentation"
```

## Output Format

### Research Report Structure

```markdown
# AI Prompt Research Report

**Brand**: [Name]  
**Category**: [Industry]  
**Date**: [YYYY-MM-DD]

## Executive Summary

- Total prompts researched: [N]
- High priority: [N]
- Medium priority: [N]
- Low priority: [N]
- Topic clusters: [N]

## 🔴 High Priority Prompts

| # | Prompt | Type | Intent | Best Platform |
|---|--------|------|--------|---------------|
| 1 | "best [category] for [use case]" | Discovery | Commercial | ChatGPT, Perplexity |
| 2 | "[brand] vs [competitor]" | Comparison | Commercial | Perplexity, Gemini |

## 🟡 Medium Priority Prompts

[Table of informational/commercial mixed prompts]

## 🔵 Low Priority Prompts

[List of awareness-stage prompts]

## Topic Clusters

### Cluster: [Theme]
- [Prompt 1]
- [Prompt 2]
- ...

### Cluster: [Theme]
...

## Platform-Specific Insights

### ChatGPT
- Prompt types that perform well: [list]
- Content format preferences: [description]

### Perplexity
- Prompt types that perform well: [list]
- Citation behavior: [description]

### Gemini
- Prompt types that perform well: [list]
- Unique characteristics: [description]

## Recommended Actions

1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

## Monitoring Setup

Add these prompts to your GEO monitoring dashboard:
- [Tool recommendation]
- [Tracking methodology]
```

## Advanced Usage

### Competitor Prompt Analysis

Research what prompts mention competitors but not you:

```bash
python scripts/competitor_prompts.py --brand "YourBrand" \
  --competitors "CompetitorA,CompetitorB" \
  --category "your category"
```

### Trending Prompts

Identify emerging prompt patterns:

```bash
python scripts/trending_prompts.py --category "your category" --days 30
```

### Prompt Monitoring

Set up ongoing monitoring:

```bash
python scripts/monitor_prompts.py --prompts-file prompts.json --frequency weekly
```

## Tools & Resources

- **Google "People also ask"**: Real user questions
- **AnswerThePublic**: Query visualization
- **AlsoAsked**: PAA expansion
- **Perplexity**: Test how prompts are answered
- **ChatGPT**: Explore prompt variations

## See Also

- Prompt taxonomy: [references/prompt-taxonomy.md](references/prompt-taxonomy.md)
- Platform differences: [references/platform-guide.md](references/platform-guide.md)
- Prompt templates: [references/prompt-templates.md](references/prompt-templates.md)
- Research examples: [references/examples.md](references/examples.md)