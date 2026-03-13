---
name: blog-writing-mastery
description: Master skill for writing organic, human-like blog content that ranks and converts. Combines copywriting, voice, marketing, and SEO.
skills:
  - blog-copywriting
  - organic-voice
  - content-marketing
  - seo-fundamentals
  - geo-fundamentals
allowed-tools: Read, Glob, Grep, generate_image, run_command, write_to_file, replace_file_content
---

# Blog Writing Mastery

> The ultimate skill for creating blog content that sounds human, ranks organically, and converts readers.

---

## Quick Reference

This skill combines 5 specialized skills. Read them for deep knowledge:

| Skill | Purpose |
|-------|---------|
| [blog-copywriting](../blog-copywriting/SKILL.md) | Headlines, hooks, structure |
| [organic-voice](../organic-voice/SKILL.md) | Human-like writing, anti-AI |
| [content-marketing](../content-marketing/SKILL.md) | SaaS strategy, conversion |
| [seo-fundamentals](../seo-fundamentals/SKILL.md) | Search optimization |
| [geo-fundamentals](../geo-fundamentals/SKILL.md) | AI search optimization |

---

## The Blog Writing Workflow

### Phase 1: Research & Planning

| Step | Action | Output |
|------|--------|--------|
| 1 | Identify target keyword | Primary + 2-3 secondary keywords |
| 2 | Analyze search intent | Understand what reader wants |
| 3 | Research competitors | Find gaps to fill |
| 4 | Map to customer journey | Awareness/Consideration/Decision |
| 5 | Draft outline | H1 → H2s → key points |

### Phase 2: Writing

| Step | Action | Reference Skill |
|------|--------|-----------------|
| 1 | Craft headline | `blog-copywriting` §1 |
| 2 | Write hook (first 2 sentences) | `blog-copywriting` §2 |
| 3 | Structure with H2/H3 | `blog-copywriting` §3 |
| 4 | Apply organic voice throughout | `organic-voice` §2-6 |
| 5 | Add value proposition elements | `content-marketing` §4 |
| 6 | Place strategic CTAs | `content-marketing` §6 |

### Phase 3: Optimization

| Step | Action | Reference Skill |
|------|--------|-----------------|
| 1 | SEO elements (title, meta, H1) | `seo-fundamentals` §4 |
| 2 | Internal/external linking | `seo-fundamentals` §4 |
| 3 | GEO elements (FAQ, data, quotes) | `geo-fundamentals` §5 |
| 4 | Schema markup | `seo-fundamentals` §5 |

### Phase 4: Final Review

| Step | Action | Reference |
|------|--------|-----------|
| 1 | Run Anti-AI Checklist | Below |
| 2 | Run Quality Rubric | Below |
| 3 | Read aloud test | Does it sound human? |

### Phase 5: Cover Image Generation

Generate a cover image using the `generate_image` tool.

**Prompt Template:**
```
Modern, professional blog cover image for: "[BLOG_TITLE]"
Style: Clean, minimalist, abstract illustration
Theme: [KEY_VISUAL_THEME]
Colors: Vibrant gradients (avoid purple), blues, teals, oranges
No text overlay. High quality, 16:9 aspect ratio.
```

**Execution:**
1. Use the `generate_image` tool with the above prompt
2. Save image to `public/blog-covers/[slug].webp`
3. If image generation limit is exceeded, provide the prompt to the user

**Fallback Prompt (when limit exceeded):**
```
🎨 Cover Image Prompt (generate manually):
---
Title: [BLOG_TITLE]
Prompt: [FULL_PROMPT_FROM_TEMPLATE_ABOVE]
Suggested size: 1200x630px (16:9)
Save to: public/blog-covers/[slug].webp
---
```

### Phase 6: Draft to Database

**Blog Data File:** `scripts/blog_data.js`
**Seed Script:** `scripts/seed_blogs.js`

**Step 1: Add blog entry to `blog_data.js`**

```javascript
{
    "title": "[BLOG_TITLE]",
    "slug": "[url-safe-slug]",
    "excerpt": "[150-char compelling excerpt]",
    "content": "[FULL_MARKDOWN_CONTENT]",
    "coverImage": "/blog-covers/[slug].webp"  // Local path or assets URL
}
```

**Step 2: Run seed script**
```bash
node scripts/seed_blogs.js
```

**Step 3: Verify**
- Blog appears in database as draft
- Cover image loads correctly

---

## Execution Checklist

Use this checklist when writing a new blog:

### Blog Creation
- [ ] **Research** — Target keyword + intent identified
- [ ] **Outline** — H1 + H2s + key points drafted
- [ ] **Write** — Apply organic voice + hook + structure
- [ ] **Links** — 3 max, paragraph text only
- [ ] **Anti-AI** — Run banned phrases check
- [ ] **Quality** — Score 32+/40 on rubric

### Cover Image
- [ ] **Generate** — Use `generate_image` tool
- [ ] **Fallback** — If limit hit, provide prompt to user
- [ ] **Save** — To `public/blog-covers/[slug].webp`

### Database
- [ ] **Add entry** — Update `scripts/blog_data.js`
- [ ] **Seed** — Run `node scripts/seed_blogs.js`
- [ ] **Verify** — Blog appears as draft

---

## Anti-AI Checklist

Run this before EVERY publish:

### Banned Phrases (Search & Remove)

- [ ] "In today's [digital/fast-paced] world"
- [ ] "Furthermore", "Moreover", "Additionally"
- [ ] "It's worth noting", "Needless to say"
- [ ] "In conclusion", "To sum up"
- [ ] "Let's dive in", "Without further ado"
- [ ] "Leverage", "Utilize", "Optimize" (use simpler words)

### Human Signals (Must Have)

- [ ] At least 3 uses of "I" (personal experience)
- [ ] At least 5 uses of "you" (direct address)
- [ ] Contractions used naturally (don't, you'll, it's)
- [ ] At least 1 specific, personal example or anecdote
- [ ] At least 1 opinion/stance (not just neutral facts)
- [ ] Sentence length varies (short + medium + long)
- [ ] At least 1 fragment for emphasis

### The Friend Test

> Read the intro aloud. Would you say this to a friend over coffee?
> If no → Rewrite until yes.

---

## Linking Strategy

### Rules

| Rule | Details |
|------|---------|
| **Max 3 links per blog** | Don't over-link. Quality over quantity. |
| **Paragraph text only** | Links go ONLY in body paragraphs |
| **No links in** | Headlines, subheadings, bullet points, CTAs |

### Link Placement

| ✅ Do | ❌ Don't |
|-------|----------|
| Link keywords naturally in sentences | Link in H1, H2, H3 headings |
| Use descriptive anchor text | Link in bullet point items |
| Spread links across the post | Cluster all links in one section |

### Anchor Text

| Good | Bad |
|------|-----|
| "best bookmark manager tools" | "click here" |
| "organize your browser tabs" | "this article" |
| "Markify's tagging feature" | "learn more" |

---

## Quality Rubric

Score each element 1-5, target: 35+ total

| Element | 1 (Poor) | 5 (Excellent) | Score |
|---------|----------|---------------|-------|
| **Headline** | Generic, no hook | Specific, curiosity-inducing |  |
| **Hook** | Boring, slow start | Grabs attention in 2 sentences |  |
| **Structure** | Wall of text | Clear H2s, scannable |  |
| **Voice** | Robotic, AI-like | Conversational, personal |  |
| **Value** | Fluff, obvious info | Actionable, unique insights |  |
| **SEO** | No optimization | Keywords natural, schema added |  |
| **CTA** | None or weak | Clear, benefit-focused |  |
| **Credibility** | No proof | Data, examples, expertise shown |  |

**Minimum passing:** 32/40 (80%)

---

## Markify Brand Voice Guide

### Tone

| Attribute | Description |
|-----------|-------------|
| **Helpful** | Like a friend who happens to be organized |
| **Direct** | No fluff, get to the point |
| **Relatable** | We've had bookmark chaos too |
| **Smart** | Knowledgeable but not academic |
| **Light** | Occasional humor, never stuffy |

### Voice Examples

| ❌ Not Markify | ✅ Markify Voice |
|---------------|------------------|
| "Leverage our AI-powered solution" | "Let our AI handle the organizing" |
| "Optimize your workflow" | "Find anything in seconds" |
| "Users benefit from..." | "You'll love how..." |
| "Markify is a bookmark manager" | "Markify saves your links—and your sanity" |

### Key Messages

| Topic | Messaging |
|-------|-----------|
| **Problem** | Bookmark chaos, lost links, wasted time |
| **Solution** | Smart organization that works automatically |
| **Outcome** | Find anything instantly, never lose a link |
| **Differentiator** | AI-powered, beautifully simple |

---

## Content Templates

### Template: How-To Post

```
# How to [Achieve Specific Outcome]

[Hook: 2-sentence pain point or question]

[Promise: What they'll learn/achieve]

## Why [Topic] Matters
[Brief context, connect to their pain]

## Step 1: [Action]
[Explanation + screenshot/example]

## Step 2: [Action]
[Explanation + screenshot/example]

## Step 3: [Action]
[Explanation + screenshot/example]

## Pro Tips
- Tip 1
- Tip 2

## Wrapping Up
[1-2 sentence summary]

[CTA: Try Markify / Related post]

## FAQ
### Q1?
A1.
### Q2?
A2.
```

### Template: Comparison Post

```
# [Product A] vs [Product B]: Which Is Better in 2025?

[Hook: "Choosing between X and Y? Here's what you need to know."]

## Quick Verdict
[Winner + 1-sentence reason for readers in a hurry]

## Overview
| Feature | [Product A] | [Product B] |
|---------|-------------|-------------|
| ... | ... | ... |

## [Comparison Point 1]
[Analysis]

## [Comparison Point 2]
[Analysis]

## [Comparison Point 3]
[Analysis]

## Who Should Use [Product A]?
[Ideal user profile]

## Who Should Use [Product B]?
[Ideal user profile]

## Final Verdict
[Recommendation + CTA]
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **Starting with product** | Start with the reader's problem |
| **Too formal** | Write conversationally |
| **No personal examples** | Add 1-2 "I/we" experiences |
| **Generic advice** | Add specific, actionable steps |
| **Wall of text** | Break up every 2-3 sentences |
| **Weak ending** | Summarize value + clear CTA |
| **AI clichés** | Run banned phrases check |

---

> **Remember:** The best blog post is one that helps the reader AND sounds like it came from a real person who cares about them.
