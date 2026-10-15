---
name: taste-ux-copy
description: |
  UX writing for agent-built interfaces: voice and tone, headline formulas, button labels, microcopy, error messages, empty states, loading text, pricing labels, and inclusive language — with before/after pairs and a copy checklist. Use whenever generating any interface text. Stack on the design-taste core skill.
triggers:
  - "copywriting"
  - "microcopy"
  - "ux writing"
  - "headline"
  - "button text"
  - "error message"
  - "empty state"
  - "voice and tone"
---

# taste-ux-copy

> Copy is the interface's personality and its instruction manual. Bad copy makes good design look broken.

## 1. VOICE & TONE (Decide It First, Then Write)

Pick a voice from the brand read and lock it:

| Voice | Sounds like | Fits |
|---|---|---|
| Plainspoken | "We tell you when something's wrong. Here's what to do." | Enterprise, fintech, health |
| Direct | "Type less. Ship more." | Developer tools |
| Warm | "You're almost done — one step left." | Consumer, education |
| Dry-humor | "No, this isn't a cult. The newsletter is just that good." | Consumer, indie brands |

Rules that hold in every voice: be concrete ("42 rows" not "some data"), be honest (no "just" — "Just enter your email" is a lie), address the reader as you/your on marketing, no exclamation marks except one-per-page celebrations, no passive voice in errors, no corporate filler ("leverage", "streamline", "robust").

## 2. HEADLINES (Formulas That Work)

- **Outcome + audience:** "Analytics that don't need a data team."
- **Before → after:** "From 'where are my users going?' to 'oh, there.'"
- **Name the pain:** "Your signup form is leaking 63% of visitors."
- **Authority + promise:** "The 2026 pricing guide for indie SaaS."
- **Curiosity with a payoff** (never curiosity alone): "We deleted our dashboard. Here's what we replaced it with."

Rules: H1 under 12 words; one idea; the product name can live in the subline, not the H1; no punctuation theatrics (?!,!!!); no "The Future of X" openers.

## 3. BUTTONS & ACTIONS (The Most-Read Words on the Page)

- Buttons say the action: "Save changes" > "Submit" > "OK". First-person lifts consumer conversion: "Start my free trial".
- Destructive actions say what dies: "Delete project" (never "OK"). Paired with a cancel that's equally visible.
- Loading/disabled states say what's happening, not a promise: "Saving…" > "Please wait". Never "Almost done" if it's not provable.
- The label must survive without context: no icon-only buttons without accessible text.

## 4. ERRORS (Formula: What + Why + Fix)

Every error message has three beats, in order:

1. **What happened**, in plain language ("We couldn't save this section").
2. **Why** (one clause max: "the file is larger than 10 MB").
3. **The fix** (the verb: "Remove some images and try again", or a link).

Before/after pairs:

| Before | After |
|---|---|
| "Error 500 — please try again later" | "This page hit a snag on our side. Reload — your work is saved." |
| "Invalid input" | "Add at least 8 characters. A number helps." |
| "Password incorrect" | "That password doesn't match. Forgot it? Reset here." |

Field-level errors sit next to the field, not in a toast on the other side of the screen. Never blame the user ("You entered…" → "This field needs…").

## 5. EMPTY STATES (Every Empty State Has a Job)

1. **Name the emptiness** ("No projects yet").
2. **Why it's empty** (one line: "Projects show up here when you create them").
3. **The next action** (one button: "Create your first project").
4. **Optional: a tiny win** ("Takes about 4 minutes").

An empty state with no next step is a dead end. A dead end is a product failure.

## 6. STATUS & LOADING

- Progress: verbs, not promises ("Uploading 3 of 8 files…").
- Completion: state what changed, not just "Done" ("8 files uploaded to /reports").
- Notifications: subject + one clause + optional action, under 20 words: "Payment failed — your card was declined. Update it here."
- Skeleton states: never show a skeleton for longer than ~2s without a message.

## 7. INCLUSIVE & LOCALIZED READY

- No "guys", "man-hours", gendered pronouns in generic copy; "they" is fine. Avoid "simply/easily/just" (they insult the reader's context).
- Numbers: "1,024" not "1k" where precision matters; dates spell out where ambiguous (July 3 ≠ 7/3).
- Write for translation: no nested variables mid-sentence ("Your {{count}} friends" → "Friends: {{count}}"), no idioms ("hit the ground running"), no emoji-only messages.

## 8. CHECKLIST (Fail the Copy If…)

- [ ] Any sentence with "leverage", "streamline", "robust", "seamless", "cutting-edge".
- [ ] Any error without a fix.
- [ ] Any button that says "Submit" or "OK" where a real verb exists.
- [ ] Any empty state without a next action.
- [ ] Any headline over 12 words or with a "!".
- [ ] Any claim the page can't support on the same viewport.
- [ ] Two different labels for the same action on one page.