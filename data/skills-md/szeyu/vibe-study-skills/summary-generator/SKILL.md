---
name: summary-generator
description: Condense lengthy materials into digestible summaries. Creates bullet-point summaries, Cornell notes, and cheat sheets with key terms highlighted. Use when summarizing textbooks, lectures, articles, or any study material. Triggers - summarize, create summary, condense notes, key points, cheat sheet, quick summary, TL;DR.
---

# Summary Generator

Transform lengthy content into concise, study-ready summaries.

## Workflow

```mermaid
flowchart LR
    A[Source Material] --> B[Identify Key Points]
    B --> C[Choose Format]
    C --> D[Generate Summary]
    D --> E[Highlight Terms]
```

---

## Summary Formats

### 1. Bullet Point Summary

**Best for:** Quick reference, revision

```markdown
# [Topic] Summary

## Main Ideas
- **Key point 1:** Brief explanation
- **Key point 2:** Brief explanation
- **Key point 3:** Brief explanation

## Important Details
- Supporting fact 1
- Supporting fact 2

## Key Terms
- **Term 1:** Definition
- **Term 2:** Definition
```

### 2. Cornell Notes Format

```markdown
┌─────────────────────────────────────────────────────────────────┐
│                         [Topic Title]                            │
├────────────────┬────────────────────────────────────────────────┤
│                │                                                 │
│   Cue Column   │              Notes Column                       │
│   (Questions)  │          (Main content)                         │
│                │                                                 │
│  What is X?    │  • X is defined as...                          │
│                │  • Key characteristics:                         │
│                │    - Point 1                                    │
│                │    - Point 2                                    │
│                │                                                 │
│  Why does Y?   │  • Y happens because...                        │
│                │  • Related to Z through...                      │
│                │                                                 │
├────────────────┴────────────────────────────────────────────────┤
│                          Summary                                 │
│  2-3 sentence summary of the entire topic.                      │
└─────────────────────────────────────────────────────────────────┘
```

### 3. One-Page Cheat Sheet

```markdown
# [Subject] Cheat Sheet

## Section 1: [Topic]
| Concept | Key Info |
|---------|----------|
| A | ... |
| B | ... |

## Section 2: [Topic]
**Formula:** [equation]
**Steps:** 1 → 2 → 3

## Quick Reference
- **If X:** Do Y
- **If Z:** Do W
```

---

## Summary Length Guidelines

| Original Length | Summary Target |
|-----------------|----------------|
| 1 page | 3-5 bullets |
| 5 pages | 1/2 page |
| Chapter | 1 page |
| Textbook | 5-10 pages |

**Rule of thumb:** 20% of original length

---

## Key Extraction Process

1. **Read once** for overall understanding
2. **Identify main ideas** (usually 1 per paragraph/section)
3. **Find supporting evidence** (examples, data, explanations)
4. **Note key terms** and their definitions
5. **Connect concepts** with relationships

### What to Include
- Main arguments/thesis
- Key facts and figures
- Important definitions
- Cause-effect relationships
- Examples that clarify concepts

### What to Exclude
- Redundant information
- Excessive examples
- Background context (unless essential)
- Transitional phrases
- Author's tangents

---

## Highlighting Patterns

Use consistent formatting:

- **Bold** for key terms
- *Italics* for emphasis
- `Code` for formulas/technical terms
- CAPS for acronyms
- → for cause-effect

---

## Quality Checklist

- [ ] Captures all main ideas
- [ ] Maintains logical structure
- [ ] Uses own words (not copy-paste)
- [ ] Key terms are highlighted
- [ ] Readable without original source
- [ ] Appropriate length for purpose
