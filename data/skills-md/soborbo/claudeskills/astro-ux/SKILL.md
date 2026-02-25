---
name: astro-ux
description: UX patterns and section templates for Astro lead generation sites. Hero, features, testimonials, CTAs, FAQ sections. Use for page section design.
---

# Astro UX Skill

## Purpose

Provides UX patterns and section templates for lead generation pages.

## Core Rules

1. **Mobile-first design** — 375px base, scale up
2. **Clear visual hierarchy** — One primary CTA per viewport
3. **Trust before ask** — Social proof before form
4. **Minimal friction** — Short forms, clear labels
5. **Accessible** — Keyboard nav, focus states, contrast

## Section Types

### Conversion Sections

| Section | Purpose | Key Elements |
|---------|---------|--------------|
| Hero | First impression + CTA | Headline, subhead, CTA, trust badge |
| CTA Banner | Mid-page conversion | Headline, button, urgency |
| Form Section | Lead capture | Form, benefits, trust |
| Final CTA | Last chance | Summary, strong CTA |

### Trust Sections

| Section | Purpose | Key Elements |
|---------|---------|--------------|
| Testimonials | Social proof | Quote, name, photo, stars |
| Logos | Authority | Client/partner logos |
| Stats | Credibility | Numbers, context |
| Reviews | Third-party proof | Google/Trustpilot reviews |

### Content Sections

| Section | Purpose | Key Elements |
|---------|---------|--------------|
| Features | Benefits | Icon, title, description |
| How It Works | Process | Numbered steps |
| FAQ | Objection handling | Questions, answers |
| About | Trust building | Story, team, values |

## Mobile Patterns

- Sticky mobile CTA bar
- Thumb-friendly buttons (44px min)
- Collapsible navigation
- Touch-friendly form inputs

## Page Flow

```
Hero (with CTA)
↓
Trust Signal (logos/stats)
↓
Features/Benefits
↓
Social Proof (testimonials)
↓
How It Works
↓
CTA Banner
↓
FAQ
↓
Final CTA
↓
Footer
```

## Related Skills

- `section-skeleton` — Component structure
- `page-structure` — Section ordering
- `astro-components` — UI components

## Definition of Done

- [ ] Mobile-first responsive
- [ ] Clear CTA hierarchy
- [ ] Trust elements before forms
- [ ] Accessible (a11y checked)
- [ ] Fast loading (no heavy assets in viewport)
