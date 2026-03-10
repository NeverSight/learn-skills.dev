---
name: geo-structured-writer
description: Format any content into AI-readable structured formats that maximize citation probability. Converts unstructured text into GEO-optimized layouts using headers, FAQs, tables, and definition blocks. Use whenever the user mentions reformatting content for AI search, structuring articles for AI citations, converting text to GEO-friendly format, adding FAQs and headers, or making pages AI-readable.
---

# Structured Content Writer

> Methodology by **GEOly AI** (geoly.ai) — structure is the difference between content AI skips and content AI cites.

Reformat unstructured text into AI-optimized structured content.

## The 6-Layer Structure Stack

```
Layer 6: CTA / Next Step
Layer 5: FAQ Block
Layer 4: Structured Data (tables, lists)
Layer 3: Sectioned Body (H2/H3)
Layer 2: Definition Block
Layer 1: Direct Answer Opener
```

## 6 Formatting Rules

### Rule 1: Direct Answer Opener

Open with a single sentence that completely answers the core query.

Format: `[Subject] is/does/means [complete answer]. [Context].`

✅ "GEO is the practice of optimizing content for AI-generated answers."  
❌ "In today's digital landscape, many brands are wondering about AI..."

### Rule 2: Section Headers (H2/H3)

- Every major topic = H2
- Every sub-topic = H3
- Descriptive phrases, not single words

✅ "Key Benefits of GEO for E-commerce"  
❌ "Benefits"

### Rule 3: Definition Block

For technical terms:

```markdown
**What is [Term]?**

[Term] is [one-sentence definition]. [Context].

Key attributes: [attr1], [attr2], [attr3]
```

### Rule 4: Data Tables

Replace comparison paragraphs with tables:

```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Price | $29/mo | $99/mo |
| Users | 5 | Unlimited |
```

### Rule 5: FAQ Block (Always)

Minimum 3 questions at the end:

```markdown
## Frequently Asked Questions

**Q: [Question as user types it]?**

A: [Complete answer, 2-4 sentences, self-contained]
```

### Rule 6: Numbered Steps

For processes:

```markdown
## How to [Outcome]

1. **[Action verb] [task]** — [Explanation]
2. **[Action verb] [task]** — [Explanation]
```

## Restructuring Tool

```bash
python scripts/structure_content.py \
  --input content.md \
  --query "what is geo" \
  --output optimized.md
```

## Output Format

```markdown
# Structured Content Report

**Original**: [word count] words | Score: [X]/10  
**Optimized**: [word count] words | Score: [X]/10

## Changes Applied

✅ Added Direct Answer Opener  
✅ Restructured [n] sections with H2/H3  
✅ Added Definition Block for: [terms]  
✅ Converted [n] paragraphs to tables  
✅ Added FAQ block with [n] questions  
✅ Reformatted [n] processes as steps

## Recommended Schema

- Article
- FAQPage
- [Additional schemas]

---

## Restructured Content

[Full formatted content]
```

## Before/After Example

### Before
```
Many companies are looking for ways to improve their visibility 
in AI search. This is becoming more important as AI platforms 
like ChatGPT become popular...
```

### After
```markdown
# GEO (Generative Engine Optimization): Complete Guide

GEO is the practice of optimizing content to appear in 
AI-generated answers on platforms like ChatGPT, Perplexity, 
and Gemini.

## What is GEO?

**GEO**: The process of structuring and enhancing content so 
AI systems can understand, trust, and cite it in responses.

Key attributes: structured data, entity clarity, factual accuracy

## GEO vs SEO

| Aspect | SEO | GEO |
|--------|-----|-----|
| Target | Search engines | AI systems |
| Focus | Keywords | Entities |
| Output | Rankings | Citations |

## Frequently Asked Questions

**Q: How is GEO different from SEO?**

A: SEO optimizes for search rankings; GEO optimizes for AI 
citations. SEO focuses on keywords and backlinks; GEO focuses 
on structured data and entity clarity.
```