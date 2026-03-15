---
name: learning-guide-creator
description: >
  Create comprehensive, research-backed ~50-page learning guides (.md) on any topic,
  written for experienced technical professionals. Use this skill whenever the user asks
  to create a learning guide, study guide, research document, guidance document, briefing
  document, or any request to research a topic and produce an educational Markdown document.
  Trigger on phrases like "create a guide on...", "I need to understand...", "research and
  write about...", "help me get up to speed on...", "write a learning guide for...",
  "create learning materials on...", "brief me on...", "what do I need to know about...",
  "teach me about...", or "I want to learn about...". This skill combines thorough web
  research (10-15 searches minimum with web_fetch for full content) with structured writing
  to produce dense, practical, staff-engineer-level guides with decision frameworks,
  architectural thinking, ecosystem maps, real-world scenarios, and trade-off analysis.
  Output is always Markdown (.md), never .docx. No code snippets — focuses on concepts,
  architecture, trade-offs, decision frameworks, and real-world use cases. Always trigger
  this skill even for casual learning requests — the user prefers comprehensive documents
  over conversational explanations.
---

# Learning Guide Creator

## Overview

This skill creates comprehensive ~50-page Markdown learning guides by:
1. Researching the topic thoroughly via web search (10-15 searches minimum, with web_fetch on the best results)
2. Structuring content for an experienced technical professional who needs to get up to speed on a new domain fast
3. Writing a polished Markdown document focused on architecture, decision frameworks, trade-offs, ecosystem maps, and real-world scenarios — no code snippets

## Audience Profile

The reader is a staff software engineer with 20+ years of experience spanning AI/ML engineering, trade compliance, regulatory affairs, and real estate. They learn new domains regularly and need to get up to speed fast.

**What works:**
- Architectural thinking — how systems fit together, why they were designed that way, trade-offs
- Decision frameworks — when to use X vs Y, what factors matter, how to evaluate options
- Mental models — the right way to think about something so they can derive the details
- Historical context that explains WHY things are the way they are — the decisions and constraints that shaped the current state
- Ecosystem maps — key players, what each does, how they relate, where the power/money/influence sits
- Real-world scenarios and use cases showing how concepts play out in practice
- Trade-offs, gotchas, and "what most people get wrong" — failure modes accelerate learning
- Honest maturity assessment — battle-tested or bleeding edge? Where are the gaps?
- Specific numbers, thresholds, dates, and names from actual research — not vague generalities

**What does NOT work:**
- Code snippets and implementation examples — they can write code, they need to understand the domain first
- Beginner-level explanations of basic concepts (networking, databases, APIs, etc.)
- Marketing language or hype
- Padding and filler — every paragraph must earn its place
- Excessive caveats and hedging — be direct, flag uncertainty where it exists, move on

## Output Format

- Single `.md` file. No .docx, no JavaScript, no npm packages, no document generation libraries.
- Clean Markdown: `#`/`##`/`###` headings, `**bold**`, standard tables, `>` blockquotes for callout boxes, `---` dividers.
- Save to `/mnt/user-data/outputs/[topic-slug]-guide.md`

### No Code Snippets Rule

Do NOT include code blocks, API examples, SDK usage, CLI commands, or implementation details in the guide content. The only exception: if the topic IS a programming language/framework, include minimal pseudocode-level examples (no more than 5-10 lines) only where absolutely necessary to illustrate a concept — and even then, prefer plain English explanation. Use cases, architectural patterns, and decision frameworks replace code examples entirely.

### Callout Conventions

Use these callout patterns consistently throughout every chapter:

> **💡 Key Insight:** [Architectural insight or mental model that changes how you think about the topic]

> **⚠️ Watch Out:** [Common mistake, gotcha, or misconception — especially ones that bite experienced engineers]

> **📋 Use Case:** [Real-world scenario showing how this plays out in practice — situation, approach, outcome]

> **🔍 Deep Dive:** [Extra context for those who want to go deeper on a specific sub-topic]

> **⚖️ Trade-off:** [X gives you A but costs you B — when to choose each option and why]

Aim for 2-4 callouts per chapter, mixing types.

## Document Structure Template

Every guide follows this structure. Adapt chapter count to topic complexity (8-12 chapters total).

```markdown
# [Topic]: A Staff Engineer's Guide

> **Last Updated:** [Current Date]
> **Research Sources:** [Number] sources consulted
> **Reading Time:** ~75-90 minutes

---

## How to Use This Guide

[2-3 sentences: what this guide covers, what it assumes you already know, and what you'll be able to do/decide/evaluate after reading it]

---

## Table of Contents

[Generated from headings]

---

## PART 1: FOUNDATIONS & CONTEXT

### Chapter 1: [Topic] in 5 Minutes
- What it is (one clear paragraph — the "explain it to a staff engineer at a different company" version)
- Why it exists — the problem it solves and why previous approaches fell short
- Where it sits in the broader ecosystem (what it connects to, what depends on it)
- Current state: mature/emerging/experimental, adoption level, major users

### Chapter 2: How We Got Here
- Timeline of key inflection points (not exhaustive history — just the decisions that shaped today's landscape)
- What drove each major shift (technology changes, regulation, market forces, failures)
- Why this matters now — what's different about the current moment

### Chapter 3: Architecture & Mental Models
- How the system/domain actually works — the mechanics, end to end
- The right mental model for thinking about it (analogies to systems you already know)
- Key architectural decisions and their trade-offs
- Where the complexity lives and why

---

## PART 2: DEEP DIVE

### Chapters 4-7: Major Domain Areas

Each chapter covers one major aspect of the topic with this structure:

1. **Context & Background** — Why this area matters, how it fits the whole
2. **How It Works** — Mechanics explained conceptually (no code)
3. **Key Players & Ecosystem** — Who does what, market dynamics, relationships
4. **Decision Framework** — When/why/how to evaluate options in this area
5. **Real-World Use Case** — Concrete scenario: situation → approach → outcome → lessons
6. **Trade-offs & Gotchas** — What experienced practitioners get wrong, edge cases, failure modes
7. **Current State & Maturity** — How battle-tested is this? Where are the gaps?

---

## PART 3: STRATEGIC PERSPECTIVE

### Chapter 8: Real-World Scenarios
- 3-5 detailed scenarios showing how the topic plays out in practice
- Each: situation (with enough context to feel real) → decisions made → outcome → what to learn from it
- Include at least one failure scenario — what went wrong and why

### Chapter 9: The Current Landscape
- Market map: major players, their positioning, strengths/weaknesses
- Comparison table where applicable (products, approaches, frameworks)
- Where the industry is heading — supported by specific signals from research
- Open questions and unresolved debates

### Chapter 10: Making Decisions
- Framework for evaluating options in this domain
- Key questions to ask (of vendors, of your team, of the technology)
- Red flags and green flags
- "If I were starting today, here's how I'd approach it"

---

## REFERENCE

### Quick Reference Table
| Concept | Key Point | Why It Matters |
|---------|-----------|----------------|
| [Term/Concept] | [One-line summary] | [Practical relevance] |

### Glossary
| Term | Definition |
|------|-----------|
| [Domain-specific term] | [Clear, precise, practitioner-style definition] |

### Sources & Further Reading
- [Source title — URL — what it's useful for]
- Organized by: Official/Primary Sources, Best Technical Deep-Dives, Staying Current
```

## Workflow

### Phase 1 — Understand the Request

If not clear from the user's message, ask:
- What topic? (required)
- Any specific angle, focus area, or decision you're trying to make? (optional)
- Any areas you already know well and want to skip? (optional)

Default assumptions if not specified: staff engineer audience, no prior domain knowledge of THIS specific topic (but strong general technical/business background), wants both breadth and depth.

### Phase 2 — Research

This is the most important phase. The guide is only as good as the research. Conduct **10-15 web searches** minimum.

**Search strategy (in this order):**

1. **Foundational (3-4 searches):** What is [topic], how [topic] works, [topic] architecture/system design, history of [topic]
2. **Current landscape (3-4 searches):** [topic] [current year] trends, [topic] market landscape, latest [topic] developments, [topic] regulations/standards current
3. **Ecosystem & players (2-3 searches):** [topic] major companies/organizations, [topic] comparison, [topic] vs [alternative]
4. **Practical & critical (2-3 searches):** [topic] real-world use cases, [topic] common mistakes/failures, [topic] best practices, [topic] challenges/limitations
5. **Forward-looking (1-2 searches):** [topic] future direction, [topic] emerging trends

**Research rules:**
- Include the current year in searches for anything that changes (regulations, market data, technology)
- Prefer official sources, technical documentation, academic papers, and reputable industry analysis over blog posts
- Use `web_fetch` on the 5-8 best search results to get full article content — search snippets alone are not enough for a 50-page guide
- Track all sources with URLs for the References section
- When sources conflict, note the disagreement and present both perspectives
- Look for specific numbers: market sizes, adoption rates, performance benchmarks, dates, thresholds
- Do NOT fabricate statistics or sources — if you cannot find a number, say the data is not readily available

### Phase 3 — Build the Outline

Build the chapter outline following the document structure template above. Adapt the number of "deep dive" chapters (Part 2) based on how many major sub-topics the research uncovered. Typical range: 8-12 total chapters.

Present the outline to the user briefly before writing (do not ask for approval — just show it and proceed unless they interrupt).

### Phase 4 — Write the Full Guide

Write the complete guide in a single Markdown file.

**Content principles:**
- Every chapter opens with 1-2 sentences stating what the reader will understand after reading it
- Lead with "why" before "what" — context before detail
- Use specific data from research: names, numbers, dates — not "many companies" or "in recent years"
- Include callout boxes throughout (2-4 per chapter, mix of types: 💡 ⚠️ 📋 ⚖️ 🔍)
- End each chapter with **Key Takeaways** (3-5 bullet points, each one sentence)
- Use comparison tables wherever there are multiple options to evaluate
- No code. No implementation details. Concepts, architecture, decisions, trade-offs only.
- Write at staff engineer level — do not explain what an API is, DO explain why this particular domain chose REST over event-driven or vice versa
- Be direct and opinionated where the evidence supports it: "Option A is clearly better for X because..." not "One might consider..."
- Flag genuine uncertainty honestly: "This is still debated because..."
- Include at least one failure/cautionary real-world scenario

**Tone:**
- Like a senior principal engineer briefing a peer who is moving into a new domain
- Dense but readable — every paragraph earns its place
- Direct, specific, no filler
- Occasional dry humor is fine if natural

**Length target:** 15,000-20,000 words (~50 pages when rendered). Comprehensive but not padded.

### Phase 5 — Save and Present

- Save the `.md` file to `/mnt/user-data/outputs/[topic-slug]-guide.md`
- Present it to the user using `present_files`
- Give a 3-4 sentence summary of what is covered and any notable findings from the research

## Quality Checklist

Verify every item before delivering:

- [ ] 10+ web searches were conducted and results incorporated with specific data (dates, numbers, names)
- [ ] Zero code snippets anywhere in the document
- [ ] Every domain-specific term explained on first use (inline, not glossary-only)
- [ ] Callout boxes distributed throughout every chapter (💡, ⚠️, 📋, ⚖️, 🔍)
- [ ] Comparison tables used wherever multiple options exist
- [ ] At least one failure/cautionary scenario included
- [ ] Key Takeaways at end of each chapter
- [ ] Glossary covers all domain-specific terms used
- [ ] References section lists actual sources with URLs from the research phase
- [ ] "How to Use This Guide" section sets expectations at the top
- [ ] Content is at staff engineer level — assumes strong technical background, zero domain knowledge
- [ ] No filler paragraphs — every section adds concrete value
- [ ] Word count is 15,000-20,000 (check before saving)
