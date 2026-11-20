---
name: slide-design
description: Designs presentation decks with one idea per slide, full-sentence assertion titles, a 16:9 grid at 1920 by 1080, at most two typefaces, large body text, a small set of consistent layouts, and data slides that highlight the takeaway, with detail moved to speaker notes. Use when asked to make a deck, fix slides, structure a pitch or talk, or turn a document into a presentation. Not for social carousels, which is social-graphics.
---

# Slide Design

Produces a deck the audience can follow while listening: an outline with one idea per slide, then a slide-by-slide spec or code on a consistent 16:9 grid.

## When to use
- "Make a deck for my talk / pitch / project review."
- Slides are dense, text-heavy, or inconsistent from one to the next.
- Turning a report, document, or thesis into a presentation.
- Creating a reusable template with title, section, content, data, quote, and image layouts.
- Building slides in code (HTML with Reveal.js, Marp) or giving PowerPoint, Keynote, or Google Slides guidance.

## Workflow
1. Clarify the audience, the goal (decide, learn, approve, buy), the length in minutes, and whether the deck is presented live or read alone. If unknown, assume presented live and say so.
2. Write the storyline before any design: a one-sentence main message, 3–5 supporting points, and the evidence for each.
3. Turn it into an outline of assertion titles: each content slide title is a full sentence stating its takeaway ("Support tickets fell after the new onboarding shipped", not "Support"). Reading only the titles must tell the whole story.
4. Assign each slide one layout from a fixed set: title, agenda, section divider, content (one visual or up to 3 short points), data, quote, full-bleed image, comparison, closing.
5. Set up the system: canvas, margins, 12-column grid, type scale, color tokens, and a footer with slide numbers.
6. Design each slide so its evidence (chart, image, diagram, short text) proves the title; remove anything that does not. On data slides, highlight the takeaway (see data-visualization).
7. Move detail, caveats, and the script into speaker notes.
8. Review the deck as thumbnails for consistency, then at full size for readability.

## Rules
**Canvas and grid**
- 16:9 at 1920×1080 px, or 13.33×7.5 in in PowerPoint. Keep content inside a safe margin of at least 80px (about 4% of the width) on every side.
- Align to a 12-column grid; titles sit at the same position on every slide of the same layout.

**Type**
- At most 2 typefaces; one is often enough. Titles 1.5–2× the body size.
- Presented decks: body text at least 24pt on a 13.33×7.5 in slide. On a 1920×1080 canvas that equals 48px (1pt = 2px at that size); on a 1280×720 canvas, 32px. Only sources and footers go smaller.
- Left-align body text; center only on title, section, and quote slides.
- At most about 3 bullets of up to 2 lines each; otherwise split the slide or move text to the notes.
- Read-alone decks may carry more text and smaller type, but keep assertion titles and the grid.

**Color and content**
- Text contrast at least 4.5:1 (WCAG 2.2 AA); aim higher, because projectors wash out low-contrast color.
- One accent color, used only for emphasis: the highlighted bar, the key number.
- One idea per slide, and one chart per slide unless the comparison is the point.
- Full-bleed images at least 1920px wide, never stretched; text over images gets a scrim that restores contrast.

## Output
- Outline: numbered slides with layout name and assertion title, readable as a story on its own.
- Slide-by-slide spec: layout, title, visual or evidence, on-slide text, speaker notes.
- Code when requested: Reveal.js with `width: 1920, height: 1080` in the config, or Marp Markdown with a 1920×1080 custom theme (or the default 1280×720 with type scaled to match). Custom templates use semantic HTML + CSS custom properties; no new dependencies unless asked.
- For PowerPoint, Keynote, or Google Slides: master layout list, type sizes, color tokens, and the layout each slide uses.

## Avoid
- Topic titles ("Results") instead of takeaway sentences.
- Slides used as a teleprompter, with paragraphs the speaker reads aloud.
- More than two typefaces, ad hoc layouts, and title positions that jump between slides.
- Clip art, generic stock photos, and animations that do not reveal information in sequence.
- Charts pasted from spreadsheets with default colors, legends, and gridlines.
- Text placed over busy images without an overlay.

## Final check
- [ ] Reading only the titles tells the full story.
- [ ] Every slide uses a defined layout and stays inside the safe margins.
- [ ] Body text meets the size floor for the canvas (48px at 1920×1080 for presented decks).
- [ ] At most 2 typefaces; text contrast at least 4.5:1.
- [ ] Data slides highlight the takeaway with one accent.
- [ ] Detail lives in the speaker notes.
- [ ] Slide numbers are present and the deck was reviewed as thumbnails.
