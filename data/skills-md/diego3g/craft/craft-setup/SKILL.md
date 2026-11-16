---
name: craft-setup
description: Use when a request to design or create a page, screen or element starts in a project with no DESIGN.md at its root, when the person asks to set up, define or start the design, style, brand or guidelines of a product, or runs /craft-setup (/craft:craft-setup in the Claude Code plugin).
---

# Design setup

## Overview

Before the first screen, agree on what the product is, who it's for, how it should feel and what it should never look like. Write that down in `DESIGN.md`, the brief every later design decision reads first. **Ask, don't invent**: a brand made up by the agent is a guess the person will have to undo. Read what exists, interview the person one question at a time, write the brief, stop for approval, then build the foundations.

## When to use

- A design task and no `DESIGN.md` at the project root.
- "Set up the design", "define our style / brand / guidelines", `/craft-setup` (`/craft:craft-setup` in the Claude Code plugin).

## When NOT to use

- `DESIGN.md` exists and the task is a design: use `craft`.
- Changing one token or one guideline: use `craft-system`.

## Steps

1. **Read first.** README, docs, existing CSS or tokens, the design file, brand folders, any old `DESIGN.md` draft. Write down what they already answer. **If the code already has a design system** (a UI package, token files, a component library), say so with counts, and write "Design system source: `<path>`" into the brief's Brand section. In step 6, offer to import it into the design tool instead of creating foundations; the brand questions it answers are skipped. **Two UI packages** → ask which is the source before skipping any brand question. **Never ask a question these files answer.** Confirm it in one line instead ("Your README says pt-BR only and members over 60, so I'll design for 18px text and 48px taps").
2. **Interview, one question per message.** Follow [the interview](references/interview.md) in its order: product, audience and voice, mood, brand, references, constraints.
   - Offer 3–5 options plus "something else" whenever you can.
   - Skip any question already answered.
   - Stop when the answers are enough to design the first screen. Six good answers beat fifteen.
3. **References are required.** Ask for 2–5 products, sites or images they like. For each one, ask **what to take and what to avoid**. If it's a link or an image you can open, look at it and say what you see before asking.
4. **Write `DESIGN.md`** at the project root from [the template](references/design-md-template.md), with all eight sections: Product, Audience and voice, Mood, Brand, References, Constraints, Decisions log, Open questions.
   - Use their words where you can.
   - Anything you inferred and they didn't confirm goes under Open questions, not into the brief as fact.
5. **Stop and show the person `DESIGN.md`.** Change it until they approve it.
6. **Foundations.**
   - **Design system already in code:** offer the import. On yes, **REQUIRED SUB-SKILL:** `craft-sync` (import). It shows an inventory and asks which components to draw. On no, log "<date> — Import into <tool> declined" in the Decisions log. Offer it even after "skip": it's about the design tool, not the brief.
   - **No system in code:** **REQUIRED SUB-SKILL:** `craft-system` in create mode for the foundations (tokens, type, spacing, interaction rules). It has its own approval stop.
   - Existing tokens and styles are the starting point: extend them, don't rename or move them without asking.

## If the person says "skip" or "just design it"

Don't keep asking. Write a minimal `DESIGN.md` from what you read and what they said:
- every gap becomes an Open question;
- every assumption is marked "(assumed)".

Say in one line which assumptions matter most. "Skip" waives the interview and the brief's approval stop, never step 6:
- **design system in code** → still ask the one import question ("Import it into <tool> now? I'll show what's there and you pick the components"), then continue;
- **no tokens yet** → the foundations step and its stop still run, because `craft` can only draw with system pieces.

Then continue with the task they asked for.

## Before you start

- If no adapter in `references/adapters/` matches your tool, do the same verbs in your tool and say which you mapped by hand. With no design tool at all, build in HTML (`html.md`). If an image is all you have, say that values read from it are estimates.
- `DESIGN.md` is a plain Markdown file in the repo in every tool. Only the optional references board lives in the design tool.

## Rules

| Rule | Why |
|---|---|
| One question per message, with options | A wall of questions gets skimmed and half-answered |
| Read before asking; never ask what the files say | Asking what's in the README tells them you didn't look |
| No invented brand: colours, fonts and mood come from them or are marked "(assumed)" | An invented brand is a guess they have to undo screen by screen |
| References always come with take/avoid | "I like Stripe" is useless; "take the calm spacing, avoid the gradients" is a rule |
| "Never like" is asked explicitly | What to avoid narrows the design faster than what to aim for |
| Don't redesign existing files during setup | Setup records decisions; changing their CSS is a design task they didn't ask for yet |
| No screens during setup | Screens come from `craft`, after the brief and foundations are approved |

## Done when

`DESIGN.md` is approved with its eight sections, and the foundations are settled: created and approved through `craft-system`, or (with a system in code) imported through `craft-sync` or the import declined and logged. After a "skip": `DESIGN.md` is written with its assumptions marked, the foundations exist (approved, or already in the project), and the original task has continued.

## Common mistakes

| Thought | Reality |
|---|---|
| "I'll pick a nice palette and fonts, they can change it" | They can't change what they didn't know was decided. Ask, or mark it "(assumed)". |
| "While I'm here I'll mock the main screens" | That's `craft`'s job, after approval. Setup ends at the brief and foundations. |
| "Let me ask all six questions at once to save time" | One per message, with options. It's faster for them to answer. |
| "Their tokens are messy, I'll restructure them" | Extend them. Restructuring is a separate, approved change. |
| "No references given, I'll skip that section" | Ask for them. If they have none, offer three that fit the mood and ask what to take and avoid from each. |
