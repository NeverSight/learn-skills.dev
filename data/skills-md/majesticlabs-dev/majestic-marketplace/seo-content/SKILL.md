---
name: seo-content
description: Create SEO-optimized content that ranks AND reads like a human wrote it. Takes a target keyword/cluster and produces publication-ready articles. Includes AI-detection avoidance patterns and E-E-A-T signals.
triggers:
  - seo content
  - write article for
  - blog post about
  - seo article
  - content for keyword
  - write for ranking
  - create blog post
allowed-tools: Read Write Edit Grep Glob WebSearch WebFetch AskUserQuestion
---

# SEO Content Workflow

Transform a keyword target into **publication-ready content** that answers search intent completely, sounds human-written, and is structured for both readers and search engines.

---

## Conversation Starter

Use `AskUserQuestion` to gather context:

"I'll help you create SEO content that ranks and reads well.

**Quick info needed:**

1. **Target keyword**: What's the primary keyword to rank for?
2. **Related keywords**: Any secondary/related terms to include?
3. **Search intent**: Informational, commercial, or transactional?
4. **Content type** (pick one):
   - **Pillar guide** - Comprehensive 5,000+ word authority piece
   - **How-to** - Step-by-step tutorial (2,000-3,000 words)
   - **Comparison** - X vs Y analysis
   - **Listicle** - Numbered list format
   - **Answer post** - Direct answer to specific question
5. **Unique angle**: What perspective makes this different?
6. **Brand voice**: Casual, professional, technical, etc.

I'll research competitors, create an outline, and produce publication-ready content."

---

## The Workflow

```
RESEARCH → BRIEF → OUTLINE → DRAFT → HUMANIZE → OPTIMIZE → REVIEW
```

---

## Phase 1: Research

Before writing, understand what you're competing against.

### SERP Analysis

Search the target keyword (if WebSearch available) and analyze top results:

**For each result, note:**
- Content type (guide, listicle, tool page, etc.)
- Approximate word count
- Structure (headers, sections)
- Unique angles or data
- What they do well
- What they miss or get wrong
- How recent (publish/update date)

**Extract from SERP features:**
- People Also Ask questions (answer ALL of these)
- Featured Snippet format (match it to win it)
- AI Overview presence (what it includes/excludes)

### Gap Analysis

After reviewing competitors, identify:

1. **What's missing?** — Questions unanswered, angles unexplored
2. **What's outdated?** — Old information, deprecated methods
3. **What's generic?** — Surface-level advice anyone could give
4. **What's your edge?** — Unique data, experience, perspective

---

## Phase 2: Content Brief

Before drafting, create a brief covering: primary/secondary keywords, search intent, content type, target word count (from competitor analysis), audience, unique angle, key points, PAA questions to answer, competitor gaps to fill, and CTA.

---

## Phase 3: Content Type Structures

### Pillar Guide (5,000-8,000 words)

```
1. Hook Intro (150-250 words)
   - Answer the title question immediately
   - Why this matters NOW
   - Who this is for (and who it's not for)

2. Quick Answer Section (200-300 words)
   - Direct answer for Featured Snippet
   - TL;DR for skimmers

3. Core Sections (3-5 major sections)
   - Each 800-1,500 words
   - Each answers a major sub-question
   - H2 headers with keyword variations

4. Implementation (300-500 words)
   - Specific actionable steps
   - Decision framework if applicable

5. FAQ Section (5-10 questions)
   - From PAA research
   - Schema-ready format

6. Conclusion with CTA (150-200 words)
   - Summarize key takeaway
   - Clear next action
```

### How-To Tutorial (2,000-3,000 words)

Result shown first + prerequisites -> step-by-step instructions (one action per step, troubleshooting inline) -> variations/advanced tips -> common mistakes -> CTA.

### Comparison (2,500-4,000 words)

Quick verdict ("Choose X if... Choose Y if...") -> comparison table (8-12 differentiators) -> deep dive each option -> head-to-head scenarios -> FAQ -> final recommendation with CTA.

---

## Phase 4: Draft

### The First Paragraph Rule

Answer the search query in the first 2-3 sentences. Don't make them scroll.

**Bad:**
> "In today's rapidly evolving digital landscape, marketers are increasingly turning to artificial intelligence to streamline their workflows..."

**Good:**
> "AI marketing tools can automate 60-80% of repetitive marketing tasks. Here are the 10 that actually work, based on testing them across 50+ client accounts."

### The "So What?" Chain

For every point, ask "so what?" until you hit something the reader cares about:

> Feature: "Automated email sequences"
> So what? "Sends follow-ups without you remembering"
> So what? "You wake up to replies instead of a blank inbox"
> So what? "Close deals while you sleep"

Write from the bottom of the chain.

### Specificity Over Generality

**Weak:** "This tool saves time."
**Strong:** "This tool cut our email outreach from 4 hours to 15 minutes per day."

Numbers, examples, specifics. Always.

---

## Phase 5: Humanize (CRITICAL)

AI content has tells. Remove them ruthlessly.

### Word-Level Tells (KILL THESE)

- delve, dive into, dig into
- comprehensive, robust, cutting-edge
- utilize (just say "use")
- leverage (as a verb)
- crucial, vital, essential
- unlock, unleash, supercharge
- game-changer, revolutionary
- landscape, navigate, streamline
- tapestry, multifaceted, myriad
- foster, facilitate, enhance
- realm, paradigm, synergy
- embark, journey (for processes)

### Phrase-Level Tells (KILL THESE)

- "In today's fast-paced world..."
- "In today's digital age..."
- "It's important to note that..."
- "When it comes to..."
- "In order to..." (just say "to")
- "Whether you're a... or a..."
- "Let's dive in" / "Let's explore"
- "Without further ado"
- "In conclusion"
- "This comprehensive guide will..."

### Structure-Level Tells

- **The Triple Pattern**: Everything in threes. Humans are messier.
- **Perfect Parallelism**: Every bullet same length/structure. Too clean.
- **Hedge Stack**: "While X, it's important to consider Y, but also Z."
- **Fake Objectivity**: "Some experts say... others believe..."
- **Empty Transitions**: "Now that we've covered X, let's move on to Y."

### Voice Injection Points

Add these—AI content lacks them:

**Personal experience:** "I made this mistake for two years. Cost me roughly $40K in lost revenue."

**Admission of limitations:** "This won't work for everyone. If you're in YMYL niches, ignore this entirely."

Also inject: opinions with reasoning, specific client examples with numbers, honest uncertainty.

### The Detection Checklist

```
[ ] No AI words (delve, comprehensive, crucial, leverage, landscape)
[ ] No AI phrases (in today's world, it's important to note)
[ ] Not everything in threes
[ ] At least one personal opinion stated directly
[ ] At least one specific number from real experience
[ ] At least one admission of limitation or uncertainty
[ ] Sentence lengths vary (some under 5 words, some over 20)
[ ] Would I say this out loud to a smart friend?
```

---

## Phase 6: Optimize

### On-Page SEO Checklist

```
[ ] Primary keyword in title (front-loaded if possible)
[ ] Primary keyword in H1 (can match title)
[ ] Primary keyword in first 100 words
[ ] Primary keyword in at least one H2
[ ] Secondary keywords in H2s naturally
[ ] Primary keyword in meta description
[ ] Primary keyword in URL slug
[ ] Image alt text includes relevant keywords
[ ] Internal links to related content (4-8)
[ ] External links to authoritative sources (2-4)
```

### Title Optimization

**Format:** [Primary Keyword]: [Benefit or Hook] ([Year] if relevant)

**Examples:**
- "AI Marketing Tools: 10 That Actually Work (2025)"
- "What is Agentic AI Marketing? The Complete Guide"
- "n8n vs Zapier: Which Automation Tool is Right for You?"

**Rules:**
- Under 60 characters
- Front-load the keyword
- Include a hook or differentiator

### Meta Description

**Format:** [Direct answer to query]. [Proof/credibility]. [CTA or hook].

**Example:**
> "AI marketing tools can automate 60-80% of repetitive tasks. We tested 23 tools over 6 months to find the 10 that deliver. See the results."

- 150-160 characters
- Include primary keyword
- Compelling enough to click

### Featured Snippet Optimization

**For definition snippets:**
- Put definition in first paragraph
- Format: "[Keyword] is [definition in 40-50 words]"

**For list snippets:**
- Use H2 for the question
- Immediately follow with numbered/bulleted list
- Keep list items concise (one line each)

---

## Phase 7: Quality Review

### Content Quality Checklist

```
[ ] Answers title question in first 300 words
[ ] At least 3 specific examples or numbers
[ ] At least 1 personal experience or unique insight
[ ] Unique angle present (not just aggregation)
[ ] All claims supported by evidence or experience
[ ] No generic advice (could apply to anyone)
[ ] Would I bookmark this? Would I share it?
```

### E-E-A-T Signals Checklist

```
[ ] Experience shown (real examples, specific results)
[ ] Expertise demonstrated (depth, accuracy, nuance)
[ ] Author credentials visible
[ ] Sources cited for factual claims
[ ] Updated date visible
[ ] No misleading claims
```

---

## Output Format

```markdown
# [SEO-Optimized Title]

Meta description: [150-160 characters]

---

[Full article content with proper H2/H3 structure]

---

## FAQ

### [Question 1]
[Answer]

### [Question 2]
[Answer]

---

**Internal links included:**
- [Link 1 to related content]
- [Link 2 to related content]
```

---

## Integration

Works with:
- `keyword-research` - Provides target keyword and cluster
- `positioning-angles` - Provides unique angle for differentiation
- `brand-voice` - Provides voice profile for consistent tone
- `direct-response-copy` - For CTAs and conversion elements
- `content-atomizer` - Repurpose into social posts

**Workflow:**
```
keyword-research → positioning-angles → brand-voice → seo-content → content-atomizer
```

