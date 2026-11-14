---
name: brand-voice-guidelines
description: Develop brand voice, tone matrices, messaging frameworks, and brand book documentation. Use when the user asks about brand voice, tone of voice, brand guidelines, messaging framework, or brand consistency.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: strategy
  domain: brand-identity
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Brand Voice & Guidelines

Develop, document, and maintain consistent brand voice across all channels.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/brand-voice-guidelines ~/.claude/skills/
```

## Voice vs Tone

**Voice** = who you are (consistent). **Tone** = how you adapt to context (variable).

- Voice is your brand personality — it does not change
- Tone shifts based on situation: celebration vs crisis, social vs support, blog vs legal

## Voice Development Process

### Step 1: Audit Existing Content

Analyze 10-20 pieces of existing content across channels:
- What adjectives describe the writing?
- What is consistent? What is inconsistent?
- How does your audience describe you?

### Step 2: Define Voice Attributes

Choose 3-5 attributes that define your brand voice. Each attribute sits on a spectrum:

| Attribute | We Are | We Are NOT |
|-----------|--------|-----------|
| **Confident** | Bold, direct, opinionated | Arrogant, dismissive, preachy |
| **Approachable** | Warm, conversational, human | Unprofessional, sloppy, too casual |
| **Expert** | Knowledgeable, precise, credible | Jargon-heavy, condescending, academic |
| **Playful** | Witty, creative, surprising | Silly, forced, distracting |

### Step 3: Brand Personality Archetypes

| Archetype | Voice | Brands |
|-----------|-------|--------|
| **The Sage** | Knowledgeable, thoughtful, guiding | Google, TED, McKinsey |
| **The Creator** | Innovative, expressive, visionary | Apple, Adobe, Figma |
| **The Hero** | Bold, confident, empowering | Nike, Patagonia, Slack |
| **The Jester** | Playful, irreverent, entertaining | Old Spice, Mailchimp, Duolingo |
| **The Caregiver** | Warm, supportive, trustworthy | Dove, TOMS, Headspace |
| **The Rebel** | Provocative, disruptive, direct | Harley-Davidson, Basecamp, Cards Against Humanity |
| **The Explorer** | Adventurous, curious, independent | Airbnb, North Face, REI |
| **The Ruler** | Authoritative, premium, exclusive | Rolex, Mercedes, Bloomberg |
| **The Everyperson** | Relatable, honest, grounded | IKEA, Target, Slack |

### Step 4: Create Tone Matrix

Define how voice adapts across contexts:

| Context | Confidence Level | Formality | Humor | Empathy |
|---------|-----------------|-----------|-------|---------|
| Marketing website | High | Low-medium | Light | Medium |
| Blog post | High | Low | Medium | Medium |
| Social media | Medium-high | Low | High | Medium |
| Customer support | Medium | Medium | None | Very high |
| Error messages | Low (humble) | Low | Light if appropriate | High |
| Legal/compliance | Medium | High | None | Low |
| Crisis comms | High | High | None | Very high |
| Sales emails | High | Medium | Light | High |

### Step 5: Messaging Framework

```markdown
## Brand Promise
[One sentence: what you promise your customers]

## Value Propositions (3-5)
1. [VP 1]: [Proof point]
2. [VP 2]: [Proof point]
3. [VP 3]: [Proof point]

## Tagline Options
- [Tagline 1]
- [Tagline 2]
- [Tagline 3]

## Elevator Pitch (30 seconds)
[2-3 sentences that explain what you do, who you serve, and why it matters]

## Boilerplate (for press/about)
[Standard paragraph used in press releases, about pages, speaker bios]
```

## Writing Style Guide

### Grammar & Mechanics

| Decision | Our Standard | Why |
|----------|-------------|-----|
| Oxford comma | Yes | Clarity |
| Contractions | Yes (we are → we're) | Conversational |
| Exclamation marks | Max 1 per page | Not shouty |
| Emoji | [Platform-specific rules] | Context-dependent |
| Capitalization | Sentence case for headings | Modern, approachable |
| Numbers | Spell out 1-9, numerals 10+ | Standard convention |
| Pronouns | We (company), you (customer) | Direct and personal |

### Vocabulary

| Instead Of | Use | Why |
|-----------|-----|-----|
| Utilize | Use | Simpler |
| Leverage | Use, apply | Less jargon |
| Synergy | Collaboration, combined | Real words |
| Best-in-class | Leading, top-performing | Less cliche |
| Disruptive | [describe what actually changed] | Show, do not label |
| Solution | [name the actual thing] | Be specific |

## Voice Consistency Audit

### Audit Checklist

- [ ] Sample 3 pages per channel (website, email, social, support)
- [ ] Score each on voice attributes (1-5 per attribute)
- [ ] Identify outliers (pages that do not sound like the brand)
- [ ] Check for forbidden vocabulary
- [ ] Verify tone matches context (support should not sound like marketing)
- [ ] Test with the "read it aloud" check — does it sound like one person?

## Deliverable: Brand Voice Document

### Document Structure

```markdown
# [Brand] Voice Guide

## Who We Are (1 paragraph)
## Our Voice Attributes (3-5 with Do/Don't examples)
## Tone Matrix (context-specific adjustments)
## Messaging Framework (promise, VPs, tagline, elevator pitch)
## Writing Style Guide (grammar, vocabulary, formatting)
## Channel-Specific Guidelines (website, email, social, support)
## Examples (before/after rewrites for each voice attribute)
```

## Integration with Other Skills

- **content-creator** — Brand voice analyzer script validates consistency
- **seo-content-writer** — Apply voice guidelines while optimizing for SEO
- **copywriting-frameworks** — Use frameworks within your established voice
- **social-media-strategy** — Platform-specific tone adaptations
- **email-composer** — Maintain voice in professional communications
