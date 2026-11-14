---
name: seo-content-writer
description: "SEO-optimized content creation with brand voice analysis and platform-specific frameworks. Covers blog posts, social media, email marketing, and landing pages. Includes keyword integration, readability optimization, and performance metrics."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: seo
  domain: seo
  updated: 2026-03-13
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# SEO Content Writer

Create SEO-optimized content with consistent brand voice across platforms.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/seo-content-writer ~/.claude/skills/
```

## Core Capabilities

### Brand Voice Development
- Analyze existing content for voice characteristics
- Define personality archetypes and tone attributes
- Build voice consistency guidelines
- Create sample voice documents for team alignment

### SEO Optimization
- Keyword research and natural integration
- Title tag and meta description optimization
- Header hierarchy (H1-H4) structure
- Internal linking strategy
- Content depth recommendations by type
- Readability scoring (Flesch-Kincaid, Gunning Fog)

### Content Frameworks
- **Blog posts:** how-to, listicle, thought leadership, case study, comparison
- **Social media:** LinkedIn, Twitter/X, Instagram
- **Email marketing:** subject lines, preview text, body copy
- **Landing pages:** hero, features, social proof, CTA
- **Product descriptions:** benefit-driven, SEO-optimized

## Workflow

### 1. Define Voice (if not established)

Ask the user for 3-5 examples of content they like. Analyze for:
- Tone (formal ↔ casual)
- Perspective (first person, second person, third person)
- Vocabulary level (technical ↔ accessible)
- Sentence structure (short/punchy ↔ flowing/complex)
- Personality traits (authoritative, friendly, provocative, empathetic)

### 2. Research Keywords

For SEO content:
- Identify primary keyword (1) and secondary keywords (3-5)
- Check search intent (informational, transactional, navigational)
- Note competing content and gaps
- Plan header structure around keyword clusters

### 3. Draft Content

Follow the appropriate framework from REFERENCE.md. Ensure:
- Primary keyword in title, H1, first 100 words, and meta description
- Secondary keywords distributed naturally through H2s and body
- Readability at appropriate level for the audience
- Clear CTA aligned with content goal

### 4. Optimize

- Check keyword density (1-2% for primary, <1% for secondary)
- Verify header hierarchy (single H1, logical H2/H3 nesting)
- Add internal links to related content
- Write meta title (50-60 chars) and meta description (150-160 chars)
- Verify readability score matches target audience

## Content Type Guidelines

| Type | Target Length | Readability | Keywords |
|------|-------------|-------------|----------|
| Blog (how-to) | 1,500-2,500 words | Grade 7-9 | 1 primary + 3-5 secondary |
| Blog (thought leadership) | 800-1,500 words | Grade 9-12 | 1-2 keywords, lighter touch |
| LinkedIn post | 150-300 words | Conversational | 0-1 hashtag-keywords |
| Twitter thread | 5-12 tweets | Punchy, scannable | Topic-relevant, not forced |
| Email body | 100-200 words | Grade 6-8 | None (engagement-focused) |
| Landing page | 500-1,000 words | Grade 6-8 | 1 primary + 2-3 secondary |
| Product description | 150-300 words | Grade 7-9 | 1 primary + 1-2 secondary |

## Key Principles

1. **Write for humans first, search engines second.** Natural language > keyword stuffing.
2. **Match search intent.** Informational queries need guides, not sales pages.
3. **Front-load value.** The first paragraph should answer the core question.
4. **One CTA per piece.** Do not dilute with multiple asks.
5. **Scannable structure.** Headers, bullets, bold key phrases. Most readers skim.

For detailed platform specs, SEO checklists, and content frameworks, see [REFERENCE.md](REFERENCE.md).

## Brand Context (Optional)

If `brand-profile.json` exists in the working directory, read it before drafting content. Use the voice axes and descriptors to calibrate tone, the target audience to frame pain points and aspirations, and brand values to weave into messaging naturally. This profile is produced by the `brand-dna` skill.
