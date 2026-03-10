---
name: geo-citation-writer
description: Write AI-citable content in proven formats including FAQ pages, definition articles ("What is X?"), comparison guides (A vs B), how-to guides, and original data/statistics roundups. Creates content optimized for ChatGPT, Perplexity, Gemini, and Claude citations. Use whenever the user mentions writing content for AI citations, creating FAQ pages, writing definition articles, building comparison content, making how-to guides, or generating statistics roundups that AI will reference.
---

# AI Citation Content Writer

> Methodology by **GEOly AI** (geoly.ai) — write content in the formats AI platforms love to cite.

Create content assets in formats most frequently cited by AI platforms.

## Quick Start

Generate AI-citable content:

```bash
python scripts/generate_content.py --format <format> --topic "<topic>" --output article.md
```

Example:
```bash
python scripts/generate_content.py --format faq --topic "project management software" --output faq.md
python scripts/generate_content.py --format comparison --topic "Notion vs Asana" --output comparison.md
```

## The 5 High-Citation Formats

### 1. Definition Article ("What is X?")

**Why AI cites it:** Direct answers to definitional queries

**Best for:**
- Introducing concepts
- Building topical authority
- Capturing informational queries

**Structure:**
```markdown
# What is [Term]? (Complete Guide)

[Term] is [single-sentence definition with key attributes].

## Key Characteristics
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

## How [Term] Works
[2-3 paragraph explanation with mechanism]

## [Term] vs [Related Term]

| Aspect | [Term] | [Related Term] |
|--------|--------|----------------|
| [Factor] | [Value] | [Value] |
| [Factor] | [Value] | [Value] |

## Examples of [Term] in Practice
- [Concrete example 1]
- [Concrete example 2]

## Frequently Asked Questions About [Term]

**Q: [Question]?**

A: [Complete, self-contained answer]

**Q: [Question]?**

A: [Complete, self-contained answer]
```

**Schema markup:** Article + FAQPage

---

### 2. FAQ Page

**Why AI cites it:** FAQ schema feeds AI conversational answers directly

**Best for:**
- Support content
- Addressing objections
- Common questions

**Structure:**
```markdown
# [Topic] — Frequently Asked Questions

## General Questions

**Q: [Most common question]?**

A: [Complete, self-contained answer. 2-5 sentences. Don't assume context.]

**Q: [Second question]?**

A: [Answer with specific details]

## [Sub-topic] Questions

**Q: [Question]?**

A: [Answer]

## Troubleshooting / Edge Cases

**Q: [Question]?**

A: [Answer]
```

**Schema markup:** FAQPage
**Best practices:**
- 5-15 questions
- Answers 50-150 words
- Match actual search queries
- Include data in answers

---

### 3. Comparison Guide (A vs B)

**Why AI cites it:** Comparison prompts are extremely common in AI search

**Best for:**
- Competitive positioning
- Commercial intent queries
- Decision-stage content

**Structure:**
```markdown
# [Brand A] vs [Brand B]: [Year] Comparison

## Quick Answer
[Brand A] is better for [use case A]. [Brand B] is better for [use case B].

## Side-by-Side Comparison

| Feature | [Brand A] | [Brand B] |
|---------|-----------|-----------|
| [Feature 1] | [Value] | [Value] |
| [Feature 2] | [Value] | [Value] |
| Pricing | [Price] | [Price] |
| Best for | [Use case] | [Use case] |

## Detailed Analysis

### [Brand A] Strengths
- [Strength 1]
- [Strength 2]

### [Brand B] Strengths
- [Strength 1]
- [Strength 2]

### Which Should You Choose?

Choose [Brand A] if:
- [Use case criteria]
- [Use case criteria]

Choose [Brand B] if:
- [Use case criteria]
- [Use case criteria]

## Verdict
[2-3 clear recommendation sentences based on use case]
```

**Schema markup:** Article + FAQPage
**Best practices:**
- Be objective (builds trust)
- Include specific data
- Address multiple use cases
- Update annually

---

### 4. How-To Guide

**Why AI cites it:** Step-by-step instructions are #1 for how-to answers

**Best for:**
- Tutorial content
- Process documentation
- Feature walkthroughs

**Structure:**
```markdown
# How to [Achieve Outcome]: Step-by-Step Guide

**What you need:** [prerequisites list]  
**Time required:** [estimate]  
**Difficulty:** [Easy/Medium/Hard]

## Step 1: [Action verb + outcome]
[Clear instruction. One action per step.]

✅ **Result:** [What the user will see/have after this step]

## Step 2: [Action verb + outcome]
[instruction]

✅ **Result:** [Expected outcome]

[Continue for each step...]

## Common Mistakes to Avoid

**[Mistake]:** [How to avoid]

## Frequently Asked Questions

**Q: [Question about the process]?**

A: [Answer]
```

**Schema markup:** HowTo + FAQPage
**Best practices:**
- Numbered steps
- One action per step
- Include expected results
- Add troubleshooting

---

### 5. Original Data / Statistics Roundup

**Why AI cites it:** AI heavily cites original statistics and research

**Best for:**
- Building authority
- Attracting backlinks
- PR coverage

**Structure:**
```markdown
# [N] Key Statistics About [Topic] ([Current Year])

**Key finding:** [Most impactful stat in one sentence]

## [Sub-category] Statistics

- **[Stat]%** of [metric] — [Source, Year]
- **[Number] [unit]** [finding] — [Source, Year]
- **[Stat]%** [finding] — [Source, Year]

## [Sub-category] Statistics
[Continue...]

## Methodology
[How the data was collected/sourced]

## Key Takeaways
- [Insight 1]
- [Insight 2]
- [Insight 3]
```

**Schema markup:** Article
**Best practices:**
- Cite sources
- Keep current (update annually)
- Visualize data (charts)
- Include methodology

## Format Selection Guide

| Goal | Recommended Format |
|------|-------------------|
| Build topical authority | Definition article |
| Address support questions | FAQ page |
| Capture commercial intent | Comparison guide |
| Drive product adoption | How-to guide |
| Attract PR/links | Statistics roundup |

## Content Generation Tools

### Interactive Generator

```bash
python scripts/generate_content.py --interactive
```

Walks through format selection and content creation interactively.

### From Template

```bash
python scripts/generate_content.py --format definition --topic "generative engine optimization"
```

Uses templates to generate content structure.

### Batch Generation

```bash
python scripts/batch_generate.py --format faq --topics-file topics.txt --output-dir ./content/
```

Generate multiple pieces from a list of topics.

## Writing Best Practices

### Universal Rules

1. **Lead with the answer** — First sentence should answer the question
2. **Be specific** — Use data, names, dates
3. **Write standalone answers** — Each section should make sense alone
4. **Use headers** — H2 every 300-500 words
5. **Add FAQs** — Every format benefits from FAQ section
6. **Include schema** — Use `geo-schema-gen` skill for markup

### Brand Integration

- Mention brand 2-3 times naturally
- Include in first 100 words
- Add to author/publisher schema
- Don't force it (credibility first)

## See Also

- Content templates: [references/templates.md](references/templates.md)
- Format examples: [references/examples.md](references/examples.md)
- Schema pairing: [references/schema-pairing.md](references/schema-pairing.md)