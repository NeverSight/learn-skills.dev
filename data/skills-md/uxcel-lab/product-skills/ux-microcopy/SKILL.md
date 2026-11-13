---
name: ux-microcopy
description: Write or improve UX microcopy — button labels, error and empty states, tooltips, form labels, notifications, and confirmations — so it's clear, concise, action-oriented, and on-voice. Trigger when asked to write microcopy, improve a button label or error message, write copy for a flow, or make interface copy clearer or friendlier.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# UX Microcopy Skill


## How this skill behaves (read first)

This is a **generative** skill. Claude's default UX copy tends to be **verbose, clever, or generic** ("Oops! Something went wrong", "Submit", "Are you sure?"). Good microcopy is the opposite: plain, specific, and quietly helpful. The expressive part — *tone* — is context-dependent, so this skill gates:

1. **Establish voice, audience, and the moment** — tone that's right for a celebratory success state is wrong for a payment error.
2. **Apply the always-true core** — clarity, concision, action-orientation, consistency, and inclusive/accessible language hold for all copy.
3. **Choose tone deliberately** — pick the register for the brand and the specific moment; don't default to jokey or to robotic.

Then **hand off to the audits**: the companion `ux-microcopy-audit`, plus `accessibility` (copy that screen readers and all users can follow) and `dark-patterns` (copy must persuade honestly, never manipulate).

---

## Step 0 — Establish context before writing

- **Brand voice** — the product's consistent personality (playful vs. formal, warm vs. neutral).
- **Audience & vocabulary** — use the words users use ("rides", not "commutes"); tech-savviness and reading level.
- **The moment** — celebratory, routine, sensitive (payment/security), or error/recovery? This sets the tone.
- **Locale** — language(s) and platform conventions ("click" desktop vs. "tap" mobile); localization beyond literal translation.

State assumptions if proceeding without answers.

---

## The always-apply core (true for any microcopy)

- **Plain, simple language.** Write for the widest range of users; no jargon or high-register vocabulary unless the audience expects it. Read it aloud to test.
- **Concise.** Say it in as few words as keep the meaning; ~16% read word-by-word, the rest scan. Cut filler.
- **Action-based and specific.** Labels are verbs (+ nouns) describing the outcome — "Get Pro", "Delete file", "Unmute now" — never generic "Yes/No/OK/Submit". A great CTA also conveys the *benefit*.
- **Tell users what's happening and what's next.** Reduce uncertainty: where they are, what an action does, how long it takes.
- **Consistent terminology.** One term per concept across the whole product ("scheduling" everywhere, not "booking" elsewhere); consistent with platform conventions.
- **Human numbers & dates.** "Tomorrow" not "April 1"; "8:45 AM" not "a quarter to nine"; concrete numbers/social proof over vague "many".
- **Inclusive & accessible.** Gender-neutral pronouns (they/them); descriptive link text ("Read more about pricing", not "More"); microcopy as **live text**, not baked into images; persistent labels (not placeholder-only); acknowledge completed actions.
- **Honest, never manipulative.** No confirmshaming, fake urgency, or guilt (→ dark-patterns).

---

## Tone — the gated decision (pick per brand + moment)

Choose the register intentionally; the same message reads differently in each. Don't default to one.

| Tone | Use for | Caution |
|---|---|---|
| **Playful / witty** | Low-stakes moments, light errors, easter eggs | Know your audience; never at the cost of clarity |
| **Enthusiastic / praising** | Encouragement during effort; celebrating an achievement | Don't over-cheer routine actions |
| **Warm / friendly** | Welcomes, everyday guidance (first names, contractions, "you") | Can feel flippant in serious moments |
| **Confident** | Sensitive moments — payments, security, data | Avoid hedging ("maybe", "try to") |
| **Respectful / formal** | Professional, regulated, or sensitive contexts | Can read as dry — still be clear |
| **Honest / direct** | Permission/data requests | Active voice; don't mask intent |
| **Concise** | Dense UI, labels, mobile | Don't strip needed context |

Rule: match tone to the **moment**. A payment error wants confident + clear, not a joke.

---

## Microcopy patterns (quick reference)

- **Buttons:** verb + outcome; descriptive over generic ("Unmute now" > "Yes").
- **Errors/alerts:** explicit (what happened) + constructive (how to fix) + plain language; place next to the problem; polite, no blame/ALL-CAPS.
- **Labels:** specific verbs+nouns, not "OK/Start/Finish".
- **Placeholders:** hints/examples only — never the sole label (they vanish on input).
- **Tooltips:** add genuine value; never state the obvious.
- **Notifications/push:** ask "how does this help the user?"; useful, not intrusive.
- **Empty/success states:** empty = teach the first action; success = confirm + positive moment.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After writing or revising copy, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`microcopy` and `dark-patterns` are Tier A (auto-run); `accessibility` is Tier B (offered)** — under an existing design system `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-microcopy-audit`** *(Tier A)* — the companion audit: clarity, action-orientation, consistency, tone fit across the flow.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — plain language, descriptive links, live text, persistent labels, screen-reader acknowledgments.
- **`ux-dark-patterns-audit`** *(Tier A)* — copy persuades honestly: no confirmshaming, manufactured urgency, or guilt.

If an audit flags it, resolve toward the core: plainer, more specific, on-the-right-tone.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Oops! Something went wrong." | "We couldn't save your changes. Check your connection and try again." |
| "Submit" / "OK" / "Yes" | Verb + outcome: "Create account", "Delete file" |
| Jargon / high-register words | Plain language users actually use |
| Same tone everywhere | Match tone to brand **and** the moment |
| Joke on a payment/security error | Confident, clear, reassuring copy |
| "April 1" / "a quarter to nine" | "Tomorrow" / "8:45 AM" |
| "Register" here, "Join free" there | One consistent term per concept |
| "Click More" link / generic labels | Descriptive: "Read more about pricing" |
| Text baked into an image | Live, selectable text |
| Confirmshaming the opt-out | Neutral, honest dismissals (→ dark-patterns) |

---

## Source lessons (Uxcel)

- [10 Microcopy Tips](https://uxcel.com/lessons/microcopy-tidbits-594)
- [10 UX Writing Tones](https://uxcel.com/lessons/ux-writing-tones-590)
- [Writing Action-Based Messages](https://uxcel.com/lessons/action-based-messages-095)
- [Writing Problem Messages](https://uxcel.com/lessons/problem-messages-893)
- [Patterns in UX Writing](https://uxcel.com/lessons/patterns-313)
- [Accessibility in UX Microcopy](https://uxcel.com/lessons/accessibility-in-microcopy-877)
