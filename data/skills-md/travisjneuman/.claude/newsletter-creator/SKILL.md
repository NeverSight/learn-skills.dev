---
name: newsletter-creator
description: Company newsletter and content roundup creation with consistent formatting, content curation, and audience segmentation. Use when creating internal newsletters, external digests, or content summaries.
---

# Newsletter Creator

Structured frameworks for creating compelling internal and external newsletters with consistent quality, effective curation, and audience-appropriate tone.

## Newsletter Structure

### Standard Newsletter Sections

```
NEWSLETTER LAYOUT:

1. HEADER
   - Newsletter name / brand
   - Edition number and date
   - Tagline or theme for this edition

2. TL;DR / HIGHLIGHTS (above the fold)
   - 3-5 bullet summary of key items
   - Designed for scanners who won't read the full email
   - Each bullet links to the corresponding section

3. FEATURED STORY (1 item)
   - Primary content piece
   - 150-250 words with a clear takeaway
   - Supporting image or graphic
   - CTA: read more, watch, try

4. NEWS & UPDATES (3-5 items)
   - Brief summaries (50-100 words each)
   - Consistent format: headline, summary, link
   - Categorized if applicable

5. CURATED CONTENT (3-5 items)
   - Third-party articles, tools, or resources
   - Brief annotation explaining relevance
   - Source attribution

6. SPOTLIGHT SECTION (1 item, rotating)
   - Team member spotlight, customer story, tool tip
   - Rotates theme each edition
   - Personal and engaging

7. UPCOMING EVENTS / DATES
   - Relevant events, webinars, deadlines
   - Calendar format or simple list

8. FOOTER
   - Unsubscribe / manage preferences
   - Social media links
   - Feedback prompt ("Reply with your thoughts")
   - Archives link
```

### Internal vs External Newsletter Differences

| Element | Internal Newsletter | External Newsletter |
| --- | --- | --- |
| **Tone** | Casual, transparent, team-oriented | Professional, value-driven |
| **Content** | Company updates, wins, culture | Industry insights, product updates |
| **Frequency** | Weekly or biweekly | Weekly, biweekly, or monthly |
| **Length** | 500-800 words | 300-600 words |
| **CTA** | Participate, recognize, feedback | Read more, try feature, register |
| **Metrics** | Open rate, survey feedback | Open rate, CTR, conversions |
| **Personalization** | By team or department | By segment or interest |

## Content Curation Methodology

### Curation Workflow

```
WEEKLY CURATION PROCESS:

COLLECT (ongoing throughout week):
- Save articles to curation tool (Pocket, Raindrop, Notion)
- Tag with categories and relevance score
- Note key quotes or takeaways
- Track sources for diversity

EVALUATE (1 day before send):
- Review all saved items
- Score each on: relevance, timeliness, quality, uniqueness
- Select top items per section
- Verify links still work
- Check for duplicates from prior editions

CURATE (writing day):
- Write brief annotations for each item (why it matters)
- Arrange in priority order
- Write featured story and transitions
- Add editorial perspective where appropriate

REVIEW (before send):
- Proofread all copy
- Test all links
- Preview in email client (desktop + mobile)
- Check accessibility (alt text, contrast)
- Send test to 2-3 reviewers
```

### Content Scoring Matrix

| Criterion | Weight | 5 (Include) | 3 (Maybe) | 1 (Skip) |
| --- | --- | --- | --- | --- |
| **Relevance** | 30% | Directly applicable | Tangentially related | Off-topic |
| **Timeliness** | 25% | This week / breaking | This month | Old news |
| **Quality** | 20% | Expert source, data-backed | Good but generic | Listicle / fluff |
| **Uniqueness** | 15% | Unlikely readers saw it | Moderately circulated | Viral / everywhere |
| **Actionability** | 10% | Clear takeaway or action | Informational | Abstract / theoretical |

```
THRESHOLD:
  3.5+: Definite include
  2.5-3.4: Include if space permits
  < 2.5: Skip unless slow news week
```

## Tone and Voice Guidelines

### Voice Framework by Audience

```
INTERNAL NEWSLETTER VOICE:

Personality: Friendly colleague who's well-informed
Tone: Warm, transparent, sometimes playful
Language: First-person plural ("we"), casual contractions
Avoid: Corporate jargon, overly formal language, spin

EXAMPLE:
"Big week for the product team — they shipped the new
dashboard that's been in the works since Q3. If you haven't
tried it yet, you're missing out. Here's a quick walkthrough."

──────────────────────────────────────────────────────

EXTERNAL NEWSLETTER VOICE:

Personality: Trusted industry insider
Tone: Authoritative but approachable, value-focused
Language: Second-person ("you"), professional but not stiff
Avoid: Self-promotion overload, clickbait, assumptions

EXAMPLE:
"This week, three major shifts in the data infrastructure
space caught our attention. Here's what they mean for your
stack — and what to do about it."
```

### Annotation Style Guide

```
CONTENT ANNOTATION FORMULA:

[HEADLINE] (linked)
[1-2 sentence summary of what it covers]
[1 sentence on why it matters to your audience]

EXAMPLE:
"The State of Developer Experience 2025" (link)
GitHub's annual report surveying 12,000 developers on tooling,
AI adoption, and workflow satisfaction. Worth reading for the
data on how teams are actually using AI coding assistants —
the gap between hype and reality is illuminating.

BAD ANNOTATION:
"The State of Developer Experience 2025" (link)
Check out this report from GitHub.

(No context, no why-it-matters, no reason to click)
```

## Layout and Formatting Best Practices

### Email Design Principles

```
FORMATTING RULES:

WIDTH:
- Max content width: 600px
- Single column preferred (reliable rendering)
- 2-column only for desktop-specific sections

TYPOGRAPHY:
- Body: 16px minimum (mobile readability)
- Headlines: 20-24px
- Line height: 1.5-1.6
- Font: System fonts or web-safe (Arial, Georgia, Helvetica)

IMAGES:
- Width: 100% of container (responsive)
- Alt text on every image
- File size: < 200KB per image
- Use sparingly — many clients block images by default

SPACING:
- Section dividers between major sections
- Generous padding (20px+) between items
- White space > cramped content

MOBILE:
- Test on iOS Mail, Gmail app, Outlook app
- Buttons: minimum 44x44px touch target
- Text should be readable without zooming
- Stack columns vertically on mobile
```

### Template Structure (HTML)

```
EMAIL TEMPLATE SKELETON:

<!-- Preheader text (shows in inbox preview) -->
<!-- Max 150 chars, summarize key content -->

[HEADER: Logo + Edition Info]

[TL;DR BOX: 3-5 bullet highlights]

[DIVIDER]

[FEATURED STORY: Image + Text + CTA Button]

[DIVIDER]

[NEWS SECTION: 3-5 items, consistent format]

[DIVIDER]

[CURATED LINKS: 3-5 external items with annotations]

[DIVIDER]

[SPOTLIGHT: Rotating section]

[DIVIDER]

[EVENTS: Simple list or calendar]

[FOOTER: Unsubscribe, social, feedback]
```

## Subject Line Optimization

### Subject Line Formulas

```
PROVEN FORMATS:

CURIOSITY: "The one metric most teams get wrong"
NUMBER:    "5 things we learned shipping v3.0"
QUESTION:  "Is your CI pipeline costing you hours?"
NEWS:      "Big changes coming to [product] this quarter"
PERSONAL:  "[Name], your weekly engineering digest"
EMOJI:     "This week in product" (use sparingly, max 1)

CHARACTER LIMITS:
- Ideal: 30-50 characters
- Max: 60 characters (mobile truncation)
- Preheader: extend subject with 40-90 chars of context

A/B TEST PAIRS:
- Short vs. long
- Question vs. statement
- With emoji vs. without
- Specific vs. vague
- Personalized vs. generic
```

### Subject Line Anti-Patterns

```
AVOID:
- ALL CAPS (looks like spam)
- Excessive punctuation (!!!)
- Misleading or clickbait subjects
- "Newsletter #47" (boring, no reason to open)
- Repeating the same format every week
- Overly long subjects that get truncated
```

## Metrics and Performance Tracking

### Key Metrics

| Metric | Good | Average | Needs Work | Action |
| --- | --- | --- | --- | --- |
| **Open Rate** | > 40% | 25-40% | < 25% | Improve subject lines, send time |
| **Click Rate** | > 5% | 2-5% | < 2% | Better CTAs, more relevant content |
| **Click-to-Open** | > 15% | 8-15% | < 8% | Content quality, layout |
| **Unsubscribe** | < 0.1% | 0.1-0.3% | > 0.3% | Frequency, relevance review |
| **Reply Rate** | > 1% | 0.5-1% | < 0.5% | Add reply prompts, questions |

### Performance Review Template

```
MONTHLY NEWSLETTER REVIEW:

Edition Stats:
| Edition | Date | Open % | Click % | Unsub % | Top Link |
|---------|------|--------|---------|---------|----------|
| #47     |      |        |         |         |          |
| #48     |      |        |         |         |          |
| #49     |      |        |         |         |          |
| #50     |      |        |         |         |          |

Trends:
- Open rate trend: [up/down/flat]
- Best-performing content type: [___]
- Worst-performing content type: [___]
- Optimal send time (from data): [___]

Actions for Next Month:
- [ ] [specific improvement based on data]
- [ ] [content type to add or remove]
- [ ] [send time or frequency adjustment]
```

## Content Calendar Integration

### Editorial Calendar Template

```
MONTHLY CONTENT CALENDAR:

Week 1: [Theme / Focus]
- Featured: [topic]
- Curated: [2-3 planned sources]
- Spotlight: [team member / customer / tool]

Week 2: [Theme / Focus]
- Featured: [topic]
- Curated: [2-3 planned sources]
- Spotlight: [rotating section type]

Week 3: [Theme / Focus]
- Featured: [topic]
- Curated: [2-3 planned sources]
- Spotlight: [rotating section type]

Week 4: [Theme / Focus]
- Featured: [topic]
- Curated: [2-3 planned sources]
- Spotlight: [rotating section type]

RECURRING SECTIONS:
- Monthly: Industry roundup, metrics review
- Quarterly: Retrospective, reader survey
- Annual: Year in review, predictions
```

### Frequency and Timing Recommendations

| Audience | Recommended Frequency | Best Send Day | Best Send Time |
| --- | --- | --- | --- |
| **Internal (all-company)** | Weekly | Monday or Friday | 9-10 AM local |
| **Internal (team)** | Weekly | Monday | 9 AM local |
| **External (B2B)** | Weekly or biweekly | Tuesday-Thursday | 10 AM ET |
| **External (B2C)** | Weekly | Tuesday or Saturday | 10 AM or 8 PM |
| **Executive summary** | Monthly | First Monday | 8 AM local |

## Newsletter Quality Checklist

| Check | Status |
| --- | --- |
| Subject line is compelling and under 60 chars | [ ] |
| Preheader text adds context (not duplicate of subject) | [ ] |
| TL;DR section captures key highlights | [ ] |
| All links tested and working | [ ] |
| Images have alt text | [ ] |
| Mobile rendering tested | [ ] |
| Tone matches target audience | [ ] |
| Content is curated (not just aggregated) | [ ] |
| Each item has a clear "why it matters" | [ ] |
| Unsubscribe link present and functional | [ ] |
| Send time optimized for audience | [ ] |
| Proofread by at least one other person | [ ] |

## See Also

- [Marketing](../marketing/SKILL.md)
- [Document Skills: DOCX](../document-skills/docx/SKILL.md)
- [Email Systems](../email-systems/SKILL.md)
- [Product Management](../product-management/SKILL.md)
