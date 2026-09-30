---
name: social-carousel
description: >
  Turn a post, article, or idea into a complete slide-by-slide carousel script for
  Instagram or LinkedIn, with a hook cover, one-idea-per-slide content slides, a
  recap, and a CTA slide. Use when someone says "make a carousel", "carousel about",
  "slide deck post", or "LinkedIn document post". Every slide ships with its copy plus
  a design note and an image-generation prompt a designer or image model can execute
  directly. Instagram feed carousels and LinkedIn document posts follow different
  size, density, and cover conventions, so the script adapts to the platform chosen.
  Reads social-context.md for brand voice and audience setup so slides sound like the
  brand and land with the right readers.
license: MIT
metadata:
  version: 0.1.0
  category: Create
  topics:
    - carousels
    - instagram
    - linkedin
  examplePrompt: "Make an Instagram carousel from my post on onboarding mistakes"
---

Given source material or a topic, produce a full carousel script — cover hook, 6–10 content slides, recap, CTA — with a design note and image prompt per slide.

## Context

Read `social-context.md` (also check `.agents/social-context.md`) before drafting. You need:

- Brand voice: vocabulary, capitalization habits, whether slides may joke
- Audience: expertise level, which determines how much a single slide can assume
- The Never list, if present: red lines that disqualify a slide or a caption

`social-context.md` does not carry visual identity, so ask the user directly for colors, type feel, and illustration-vs-photo — one question alongside the platform question in step 1.

If the file is missing, offer to run the `social-context` skill first — but do not block. Ask two or three quick questions inline (Instagram or LinkedIn? Who reads this? Any visual style words — minimal, bold, hand-drawn?) and proceed.

## Workflow

1. **Ask the platform first.** Instagram (1080×1350 portrait, tap-through, big type) and LinkedIn (document/PDF, often landscape or square, denser text tolerated) are different media. Do not draft a generic script and relabel it. If the user already named the platform, skip ahead.
2. **Extract one narrative arc from the source.** A carousel carries exactly one argument: problem → tension → resolution, or claim → evidence → payoff. If the source contains three arguments, pick the strongest and say which two you dropped.
3. **Write the cover slide.** It is a hook, not a title: eight words or fewer of large text, optionally a small kicker line. "5 onboarding mistakes" is a title; "Your onboarding is losing users on day one" is a cover. The cover must work as a standalone feed image, because that is how most people will encounter it.
4. **Outline the content slides before writing them.** One idea per slide, in escalating order — strongest point second-to-last, never first. Instagram: 6–8 content slides. LinkedIn: 8–10 is fine; readers expect more substance in a document post. Show the outline as one line per slide and let the user cut or reorder before you invest in full drafts.
5. **Draft each content slide at ≤25 words.** Constraints that keep slides swipeable:
   - Self-contained: each slide parses without its neighbors, because screenshots travel alone.
   - Pull-through: end slides on tension or an open loop where the material allows it.
   - Front-load the slide's noun; no slide begins with "Also", "And", or "Another thing".
   - One number or one image concept per slide — a slide that needs both is two slides.
6. **Write the recap slide.** Compress the arc into 3–5 checklist lines the reader can screenshot. This is the most-saved slide; make it worth saving.
7. **Write the CTA slide.** Instagram: ask for a save or a share ("Save this for your next launch"), plus follow. LinkedIn: ask a discussion question that invites comments, plus follow. One ask primary, never three equal asks.
8. **Attach a design note to every slide.** Three parts, all concrete:
   - **Layout** — text position, alignment, margins ("headline top-third, left-aligned, generous bottom margin").
   - **Visual metaphor** — the one image or diagram that carries the idea ("iceberg with 'signup' above the waterline, 'activation' below").
   - **Text placement** — what is large, what is small, and the single emphasis word or number that gets the accent treatment.
     Keep every note executable by someone who never read the source: "left-aligned headline top-third, iceberg illustration lower-right, the phrase 'day one' in accent color".
9. **Attach an image-generation prompt to every slide** that a designer or image model can run as-is:
   - Subject and composition ("flat illustration of a doorway with a welcome mat, centered, seen straight-on")
   - Style and palette hint, consistent across all slides — one visual system, not ten
   - The explicit instruction to leave clear negative space where the slide text sits
10. **Swipe-check the whole script.** Read only the slide texts in order, ignoring the design notes. The argument must survive on copy alone; if it does not, fix the copy, not the visuals. Then check the reverse: would the visuals alone tell roughly the same story? Finally, check the full script and the caption against every row of the Quality bar and against the Never list — fix any slide or caption that fails a row or trips a red line.
11. **Write the accompanying caption or post text last.** Its first line is a second hook (do not repeat the cover verbatim); it adds one piece of context the slides omit, then hands off: "swipe through".

## Quality bar

|                 | Instagram                        | LinkedIn                                         |
| --------------- | -------------------------------- | ------------------------------------------------ |
| Canvas          | 1080×1350 (4:5 portrait)         | Document/PDF; square or landscape pages          |
| Total slides    | 8–10 (cover + 6–8 + recap + CTA) | 10–12 (cover + 8–10 + recap + CTA)               |
| Words per slide | ≤25, display-sized type          | ≤25 headline; a short support line is acceptable |
| Cover           | Feed-stopping image + ≤8 words   | Bold typographic cover; reads at thumbnail size  |
| Hashtags        | In the caption, never on slides  | None on slides; 0–3 in the post text             |

- Text on slides must be legible at thumbnail size — if a design note implies more than ~3 lines of large text, split the slide.
- No slide may require the previous slide to parse.
- Numbers, arrows, and simple diagrams beat stock-photo metaphors.
- One emphasis element per slide: a single accent word, number, or arrow — two emphases is zero emphases.
- Slide transitions earn the swipe: at least a third of content slides should end on tension or an open loop.
- Alt-text-friendly: every image prompt describes a concrete scene, not "abstract vibes".
- The recap slide is screenshot bait — checklist formatting, no new information, no cleverness.

## Deliverable

Return, in order:

1. One line naming the platform, the narrative arc, and the slide count.
2. The script as a numbered list, one block per slide: **Slide N — [role]**, then **Text:** (the exact copy), **Design:** (layout + metaphor + text placement), **Image prompt:** (ready to run as-is).
3. The post caption (Instagram) or post text (LinkedIn), hook line first.

Nothing else — end there.
