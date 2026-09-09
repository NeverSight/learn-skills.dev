---
name: html-confirm
description: >-
  Produces an openable HTML page when the owner has to LOOK at something to decide or is reacting to a report. Use HTML for images, designs, storyboards, covers, renders, approving a deliverable, or reacting to a report or audit. Use plain chat for a few text choices, scoping questions, yes/no gates, "should I proceed", "which mailbox", "A or B". Use when: "confirm", "which one", "approve", "pick one", "review these", "should I proceed", "make a confirm page".
---

# html-confirm：HTML when there is something to SEE, chat when there is not

> **THE RULE CHANGED ON 2026-08-05. Read this before applying anything below.**
> the owner narrowed the preference herself, unprompted, in her own words:
> 「a-这个是错的，普通的选项就直接在聊天里选项卡就可以了，不要所有的选项都要 html，html is only for report」
>
> So the 2026-06-15 blanket rule ("EVERY confirmation point goes to an HTML page") and its
> 2026-07-29 re-confirmation are **superseded**. The prior wording, the "every confirmation
> point" trigger, and the ban on the app's option-card UI are all retired. The corrections
> ledger contains seven entries logged as violations of the old rule; those are history, not
> a standard to keep enforcing.

## The line to draw

| Situation | Surface |
|---|---|
| She must look at an image, design, storyboard, render, layout, cover, or any generated artifact to decide | **HTML page**, opened locally |
| She is reacting to a report, audit, comparison, options-with-tradeoffs page, or status dashboard | **HTML page** (this is the house rule's territory anyway) |
| The decision needs per-item notes across many rows, or she may answer across several sittings | **HTML page** with the review layer |
| Plain choice among a few text options | **chat**, option cards are fine |
| Session-start scoping, "which mailbox", "should I proceed", yes/no gates | **chat** |
| One-line clarification | **chat**, plain text |

The mechanical test, when unsure: **can the thing she is deciding about fit inside a chat option
card?** If it is a picture, a page, or sixteen variants, it cannot, so build the page. If it is
"A or B", it can, so just ask.

Do not build a page for a small choice. That was the failure mode the owner named: everything became a
page, which is friction, not service.

## Still true regardless of surface (the capture rule)

Before asking anything, answer: **when she is done answering, how do I actually get the answers
back?** This survived the narrowing because it was a separate, real failure:

- 2026-08-04: she filled in a design review layer, clicked export, and the markdown never
  arrived. The template now also writes the export into a selectable, auto-selected `textarea`
  so a blocked download still yields the text.
- 2026-08-04: never hand her an **Artifact** for a decision. The sandboxed iframe breaks
  `localStorage`, downloads, and the clipboard, so a whole round of per-item picks was lost.
  Give her a local file and `open` it.

## What to produce (when HTML is the right surface)

ONE self-contained `.html` file that:
1. **States the decision up top** in plain language plus how to answer ("reply A / B / C, or tell
   me what to tweak"). Lead with the ask.
2. **Shows the actual thing being decided.** This is the whole reason the page exists. Embed the
   images, render options side by side, show before and after, display the artifact under review.
3. **Lists each option** with a one-line tradeoff and **marks your recommendation**.
4. **Terse context** that changes the choice: cost, risk, what is blocked.

Format per the house rule: inline `<style>`, real content only, UTF-8 and CJK-safe, no React/Vue/Tailwind,
**no em dashes**. Reference local images by relative path, or base64-embed when the page must be
portable.

For a REPORT-type page, append the review layer rather than re-authoring it:

```bash
cat ~/Documents/jj-knowledge-vault/system/templates/report-review-layer.html >> <report>.html
```

## Where to save and how to open

- Save where the topic lives, per the house rule: `<project>/docs/<topic>-confirm.html`.
- **Auto-open on your primary desktop:** `open "<path>"`. Skip auto-open on a secondary machine (check its hostname against your own naming convention) or headless/agent runs.
- Print one line: `Opened: <path>`.
- Then stop and wait. Do not also ask the same question in chat.
- **If she says she cannot open it**, do not re-send the same page. Put the decision in chat as a
  short lettered list she can answer with three lines, and ask whether she needs a different
  format (PDF, plain text) for that device.

## Relationship to other skills

- Extends the house rule HTML-First Artifact Convention; this is its *decision/approval* application.
- Heavy multi-page reports go to `/reference-report`.
- Research and comparison artifacts follow the house rule directly, no skill needed.

## Minimal skeleton

```html
<!doctype html><html><head><meta charset="utf-8"><style>
 /* clean, inline, theme-aware; recommendation card highlighted */
</style></head><body>
 <h1>&lt;Decision&gt;</h1>
 <p>Reply <b>A</b>, <b>B</b>, or <b>C</b>, or tell me what to tweak.</p>
 <!-- option cards, recommendation marked -->
 <!-- the visuals being decided: <img src="../path/to/art.png"> -->
</body></html>
```

## History (why this file reads the way it does)

- **2026-06-15** the owner: every confirmation is an opened HTML page. Locked.
- **2026-07-29** offered a narrowing, answered 「保持原样」. Re-confirmed as-is.
- **2026-08-05** the owner narrowed it herself: HTML is for reports and for things she must look at;
  ordinary options go in chat. **This is the live rule.** Recorded because a future session will
  otherwise find the seven ledger entries enforcing the old blanket rule and re-apply it.
