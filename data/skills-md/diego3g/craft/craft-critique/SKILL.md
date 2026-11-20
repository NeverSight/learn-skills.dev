---
name: craft-critique
description: Use when asked to review, critique, refine or polish a design or screen, when something "feels off", "looks busy" or "isn't good yet", after finishing a screen and before showing it, or before handing a design to code.
---

# Design critique

## Overview

Critique the screen people will **see**, not the source you can read: render it first. Run the [rules](references/rules.md) as a checklist, rank what you find by how much it hurts the person using the screen, and **report before you change anything**, unless you were asked to refine. When you refine, fix only what the findings name, then look again.

## When to use

- "Review this", "what's wrong with this screen?", "refine", "polish", "it feels off".
- You just finished a screen and are about to show it.
- Before handing a design to code.

## When NOT to use

- A specific edit ("fix the typo", "make it blue"): make it. You may mention a serious problem you noticed in one line, without fixing it.

## Before you start

0. Read `DESIGN.md` at the project root if it exists: it is the project's design brief.
1. Read the project's design system. **Where it differs from a default in the rules, the project wins.** Don't flag it as a defect; note the difference once.
2. Pick your tool's adapter in `references/adapters/` (`paper.md`, `pen.md`, `figma.md`, `html.md`). If no adapter matches your tool, do the same verbs in your tool and say which you mapped by hand. With no design tool at all, build in HTML (`html.md`). If an image is all you have, say that values read from it are estimates.
3. Decide the mode:
   - **review:** the person asks about a design ("review", "critique", "what's wrong"). Report only.
   - **refine:** the person asks to improve one ("refine", "polish", "fix it", "make it better").
   - **self-check:** your own work that the person hasn't seen yet, including when another design skill calls this one. Fix what you find within the task's scope, render again, then show it with a short list of what the check changed.

## Steps

1. **Render it and look.** Take a screenshot at the size people use, and at a phone width if it's responsive. Look at it as the person using it would, and answer:
   - What do I see first?
   - Is that the most important thing?
   - What is the one next action?

   If you cannot render, say so at the top of your answer, and mark the findings that need a render to confirm.
2. **Run every rule group** in [the rules](references/rules.md): hierarchy, space, stability, interaction feel, contrast and colour, text, consistency, motion. Check each state the screen shows, not only the default.
3. **Rank the findings by impact** on the person:
   - blocks or misleads;
   - slows down;
   - looks careless.

   For each one: the problem, where it is, why it matters, and the fix.
4. **Review mode:** deliver the ranked report and **stop. Don't write a fixed version or edit any file** until the person picks the fixes.
   **Refine and self-check modes:**
   - apply the fixes, **limited to what the findings name**: no new layout, no new sections, no new files, no restructured files;
   - **render again** with the same command and sizes as step 1 (if it worked then, it works now: try it before saying you can't);
   - re-run the checks on what changed;
   - report each fix and anything that is still open.
5. A fix that changes a **shared component** (a button used on twenty screens) is not a local fix. Name it, and hand it to the craft-system process, so every screen that uses the piece changes together.

## Rules (summary; detail in references/rules.md)

| Group | The core check |
|---|---|
| Hierarchy | One thing wins the first glance; at most one primary action; when in doubt, remove |
| Space | No dead or oversized areas, no cramped groups; repeated rows align in fixed-width slots |
| Stability | Nothing changes size when loading, swapping labels, selecting or toggling |
| Interaction feel | Hover is quieter than selected; focus ring only from the keyboard; pointer cursor only on links (on the web, follow the project's convention) |
| Contrast and colour | Small text readable on tinted and grey grounds; one strong colour moment |
| Text | No one-word last lines; titles capped in lines; plain words; says what happens next |
| Consistency | The same piece looks the same everywhere; banners only for whole-app problems |
| Motion | Only where it helps; opening slower than closing; respects reduced motion |

## Done when

- **Review:** a rendered look (or an explicit "couldn't render") and every rule group checked; a ranked report; nothing changed.
- **Refine / self-check:** the named fixes applied, re-rendered and re-checked, and the report says what changed and what's still open.

## Common mistakes

| Thought | Reality |
|---|---|
| "I can read the HTML/CSS, that's enough" | People see pixels. Wrapped titles, overlaps and shifts only show when rendered. Render, or say you couldn't. |
| "I'll include a fixed version so they see the result" | In review mode that's choosing for them. Report; fix what they pick. |
| "The loading button looks broken" | Name the class of problem: it **changes width**. Layout shift is the finding, and the fix is a fixed width with the label hidden under a spinner. |
| "The headline is long" | Check *how* it breaks: a one-word last line is a finding on its own. Balance the lines. |
| "While refining, I'll also add a max width, a phone layout and split the CSS" | Refine fixes the findings. Anything else is a new proposal: list it, don't do it. |
| "I couldn't render after the fixes" (when the first render worked) | Run the same command again. The re-check is the point of refining. |
| "Their hover equals their selected, that's a bug" | Check the project's guide first. If it says so on purpose, it's their rule. Note it, don't flag it. |
