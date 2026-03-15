---
name: presentation-builder
description: Transform scripts into Apple-inspired HTML presentations with animations, color psychology, and lead magnet CTAs. Triggers on requests to create presentations, build slides, or generate HTML decks from scripts.
---

# Presentation Builder Skill

## Trigger Conditions

Activate when the user:
- Asks to create/build/make a presentation or slides
- References a script file with a style request ("in the style of...")
- Wants an HTML presentation for YouTube, speaking, or video

---

## Companion Files (Read These)

This skill has three supporting files in the same directory — read them before building:

- `styles-catalog.md` — Visual DNA of every style reference (colors, fonts, background, card patterns). Use this instead of reading external style reference files.
- `boilerplate.md` — The complete HTML scaffold with all required CSS, animation JS, navigation, and layout. Always start from this.
- `script-examples.md` — Script-to-slide transformation examples, the narrative formula, and CTA templates.

---

## Workflow

### 1. Read Before Building
- Read the script fully — identify the narrative arc and emotional journey
- If a style reference is named, check `styles-catalog.md` for its visual DNA (do NOT read the external file unless the style isn't in the catalog)
- If mood is ambiguous, ask ONE question: "Should this feel urgent/dark, exciting/light, or educational/clean?"

### 2. Map the Presentation
- Apply The Ran Nahmany Formula to the narrative arc (see `script-examples.md`)
- Plan slide count: target 15-20, max 35 for complex topics
- Identify which slides need sequential animations vs. immediate reveal

### 3. Build from Boilerplate
- Start from the template in `boilerplate.md`
- Apply the style DNA from `styles-catalog.md`
- Transform script content using rules in `script-examples.md`
- ALWAYS end with a Lead Magnet CTA slide

### 4. Save
- Save to: `Finished Presentations/[topic]-[style].html`
- Single self-contained file, no external dependencies

---

## Core Rules (Non-Negotiable)

### Color Psychology
| Color | Meaning | Use For |
|-------|---------|---------|
| Red `#ef4444` | Problem / Old Way / Expensive | Before state, pain points, `.badge-danger` |
| Green `#22c55e` | Solution / New Way / Benefit | After state, wins, `.badge-success` |
| Cyan `#22d3ee` | Technology / Innovation / You | AI refs, CTA, `.badge-primary`, `.glow-text` |
| Amber `#f59e0b` | Caution / Transition | Warnings, `.badge-warning` |

### Typography Limits (NEVER exceed)
| Element | Max Size | Weight |
|---------|---------|--------|
| `h1` | 60px (`clamp(36px, 5vw, 60px)`) | 900 |
| `h2` | 24px (`clamp(18px, 2.2vw, 24px)`) | 600 |
| `.big` | 28px (`clamp(20px, 2.8vw, 28px)`) | 700 |
| `.huge` | 72px (`clamp(42px, 6vw, 72px)`) | 900 |

### Slide Content Rules
- One new concept per slide
- Mic-drop moments get their own slide
- Same-category list items → one slide
- Distinct ideas → separate slides
- Max 12 elements per slide (prefer 4-6)
- Comparisons: always left=red/problem, right=green/solution

### Animation Rules
- All animatable elements start `opacity: 0`
- Only `.animate-in` class reveals them (never CSS auto-delays on `.visible`)
- Non-animated slides: show all content immediately via `initializeSlideElements()`
- Nested elements (badges inside cards) animate separately: parent first, children after
- Space / Right Arrow = next step or next slide
- Left Arrow = previous slide (replay all animations)

### Forbidden
- `::after` pseudo-elements for duplicate text
- Font sizes above listed maximums
- Slide padding exceeding 100px vertical
- Content without flexbox centering
- `.slide.visible .badge:not(.animate-in)` CSS patterns
- Multiple CTAs on the final slide
- Auto-playing content without user trigger

---

## Pre-Delivery Checklist

- [ ] Narrative arc: hook → problem → opportunity → proof → urgency → CTA
- [ ] Final slide is a Lead Magnet CTA (specific benefits, single action)
- [ ] Color psychology applied consistently
- [ ] Typography within size limits
- [ ] All grids/panels have `margin: auto`
- [ ] Animated elements start `opacity: 0`
- [ ] Non-animated slides show content immediately
- [ ] Nested animation order correct (parent → children)
- [ ] No content cut off at any viewport size
- [ ] Mobile responsive breakpoints present
- [ ] Short viewport breakpoints (`max-height: 700px`) present
- [ ] Navigation dots don't overlap content
