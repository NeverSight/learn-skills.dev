---
name: ux-dark-patterns-audit
description: Audit a UI, flow, or copy for dark (deceptive) patterns — design that manipulates users into unintended actions. Produces a prioritized findings list naming each pattern, its intent, severity, and an honest-design fix. Use when reviewing conversion flows, checkouts, paywalls, sign-ups, or cancellation flows for ethical design issues.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Dark Patterns Audit Skill


## How this skill behaves (read first)

This is an **evaluative** skill — it reviews existing work, auto-runs, and is built to be **called as a validation step** by generative skills, especially ones touching **conversion, pricing, sign-up, subscription, or cancellation** (`pricing`, `login-signup`, `checkout-payment`, `onboarding`, `offboarding`). It's the systematic version of the ethics guardrail those skills carry inline.

It owns **intent to deceive/manipulate**. Deliberate deferrals so it doesn't duplicate:

- **Honest usability problems** (a confusing-but-not-deliberate layout, unclear label) → the **heuristics audit**. A UX *mistake* is not a dark pattern.
- **Visual clutter / overdesign** → the **aesthetics audit**.
- **Accessibility** → the **accessibility audit**.

The line is **intent**: this audit asks whether the design exploits the gap between *what users think they're doing* and *what the product actually does*.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier A — always-relevant, auto-runs**. Explicit scope always wins.

---

## What this skill changes vs. default behavior

By default, manipulation only gets flagged when it's blatant, with no framework, no severity, and a tendency to either miss subtle patterns (preselection, forced continuity, manufactured FOMO, bad defaults) or over-accuse honest mistakes. This skill forces:

1. **A systematic sweep** of the named pattern catalog — not just the obvious offenders.
2. **Intent classification** — Dark vs. Grey vs. honest Mistake — so findings are fair, not alarmist.
3. **A concrete, honest-design fix** for each.
4. **Decision tests** (the Newspaper Test, the intent-gap question) that surface the subtle cases.

---

## The core lens: intent and the dark / grey / mistake spectrum

A dark pattern is a UI **deliberately** designed to lead users into unintended actions. The keyword is *deliberately*.

- **Dark** — exploits the gap between user intent and product behavior for the company's gain (hidden renewal after "Buy Now"). Flag and fix.
- **Grey** — not hidden, often industry-standard, but the default serves the business over the user (a pre-checked "email me offers" box). Flag as caution; nudge toward the user.
- **Mistake** — accidental confusion with no manipulative intent. Not a dark pattern → route to the heuristics audit.

Every finding should say which of the three it is. Driver to name: most dark patterns come from **conversion/A/B-test optimization** that wins a short-term metric and loses long-term trust.

---

## The pattern catalog — what to check and what each looks like

Sweep all categories. For each finding: **pattern name**, **classification** (Dark/Grey), **severity**, **fix**.

### Sneaking (hiding or smuggling information)
**Flag when:** costs/fees/taxes appear only at checkout (**hidden costs**); items added to the cart the user didn't choose (**sneak into basket**); a subscription auto-renews with the renewal buried in fine print (**forced continuity**); the user gets a different outcome than the one presented (**bait and switch**).
- ❌ "$9 flight" that becomes $40 after mandatory fees at the last step.
- ✅ Total cost, fees, and renewal terms shown up front, before commitment.

### Obstruction (making the un-profitable choice hard)
**Flag when:** cancellation/downgrade is far harder than sign-up (**roach motel**); the design blocks **price comparison** (no per-unit price, deliberately unclear tiers).
- ❌ Subscribe in one click; cancel only by calling support during business hours.
- ✅ Cancelling is as easy as subscribing.

### Misdirection & visual/wording tricks
**Flag when:** flashy elements distract from what's actually happening (**misdirection**); checkboxes/copy use confusing or double-negative wording (**trick questions**); ads masquerade as content or controls (**disguised ads**); options that benefit the company are **preselected**; **bad defaults** (most expensive plan or all notifications pre-on).
- ❌ "Uncheck if you do not want to not receive emails."
- ✅ Plain, single-meaning labels; opt-ins unchecked by default.

### Nagging
**Flag when:** the user is repeatedly re-prompted to do something they already declined.
- ❌ A newsletter pop-up that returns every visit after being dismissed.
- ✅ Respect a decline; ask again only with good reason, much later.

### Forced action & privacy
**Flag when:** access/benefit is gated behind unrelated permissions or contact-list access used to message others (**friend spam**); data shared for one purpose is reused outside that context (**privacy zuckering**).
- ❌ "Allow contacts access to continue" → then messages all of them on the user's behalf.
- ✅ Request only the data the feature needs, for the purpose stated.

### Emotional manipulation
**Flag when:** opt-outs shame the user (**confirmshaming**); urgency/scarcity is fake or exaggerated (**FOMO**, fake countdowns, "only 2 left" on unlimited digital goods); fear is used to push action (**scaremongering**).
- ❌ "No thanks, I don't care about saving money."
- ✅ Neutral dismissals: "No thanks" / "Maybe later"; real scarcity only.

### Attention exploitation (well-being)
**Flag when:** the design manufactures compulsive use rather than serving a goal — infinite scroll with no stopping point, autoplay that removes the choice to continue, variable-reward mechanics, streak anxiety, manufactured FOMO (read receipts), notification overload.
- ❌ Onboarding that pushes "enable all notifications" to maximize re-engagement.
- ✅ Mindful defaults; notifications proposed by value, not volume; natural stopping points.

### Microcopy-level
**Flag when:** copy triggers emotion ("sadly", "unfortunately" on cancel), guilt-trips, or uses confusing double negatives / vague "OK/Cancel" on consequential choices.
- ✅ Plain, honest, neutral wording on every consequential action.

---

## Audit tests (use these to catch the subtle cases)

- **The intent-gap question:** does the design exploit the gap between what the user thinks they're doing and what the product records? If yes → Dark.
- **The Newspaper / Front-Page Test:** if a journalist wrote a headline about this feature tomorrow, would the team be comfortable with it?
- **First- and second-order consequences:** the immediate win (more signups, longer sessions) vs. what it causes next (regret, churn, distrust). Dark patterns usually look fine at first order and harmful at second.
- **The default check:** who benefits from each default — the user, or the business? Defaults that only serve the business are at least Grey.

---

## Severity & classification

| Severity | Meaning |
|---|---|
| **Critical (Dark)** | Deliberate deception with real user harm — hidden costs, roach-motel cancellation, preselected paid add-ons, forced continuity, bait-and-switch, privacy zuckering, disguised ads, friend spam. Often a legal/regulatory risk too. Fix before ship. |
| **Major (Manipulative)** | Pressure/emotion tactics — confirmshaming, fake urgency/FOMO, scaremongering, nagging, attention-exploitation patterns. Erodes trust even if not strictly deceptive. |
| **Grey (Caution)** | Business-serving but not hidden — pre-checked opt-ins, bad defaults, mild scarcity. Not a clear violation; recommend re-pointing the default toward the user. |

Classify honestly — labeling an honest mistake "Dark" discredits the audit. When intent is genuinely unclear, say so and apply the intent-gap question.

---

## Audit output format

```
## Dark Patterns Audit — [Screen / Flow]
Context: [platform · what the design is optimizing for, if known]

### Critical (Dark)
- [Pattern name] — what's manipulative → honest-design fix.
### Major (Manipulative)
- …
### Grey (Caution)
- …
### Clean ✓
- [practices that respectfully serve the user]

**Trust verdict:** [trustworthy / some concerns / manipulative] + the top fixes.
```

End with the trust verdict and prioritized fixes — that's what a calling generator (or a team) acts on.

---

## How to run a good audit

1. **Lead with intent.** Classify each finding Dark / Grey / Mistake; route honest mistakes to the heuristics audit instead of flagging them here.
2. **Sweep the whole catalog**, including the subtle/attention patterns — those are what default reviews miss.
3. **Apply the tests** (intent-gap, Newspaper, second-order) to anything ambiguous.
4. **Fix toward honesty, not just compliance** — the constructive alternative, not "remove it."
5. **Don't over-accuse.** Fairness is what makes the audit credible; not every aggressive growth tactic is a dark pattern.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Flag only blatant deception | Sweep the named catalog, including preselection, forced continuity, attention patterns |
| Call every confusing UI a dark pattern | Classify intent — Dark vs. Grey vs. honest Mistake (→ heuristics) |
| "This feels manipulative" | Name the pattern, classify, rate, and give the honest fix |
| Hidden costs / buried renewal | Show full cost and renewal terms before commitment |
| Cancel is harder than subscribe | Make leaving as easy as joining |
| Confirmshaming opt-outs | Neutral dismissals |
| Preselected paid add-ons / bad defaults | Opt-ins off; defaults that serve the user |
| Re-derive usability or clutter issues | Defer to heuristics / aesthetics |

---

## Source lessons (Uxcel)

- [14 Design Dark Patterns You'll Want to Avoid](https://uxcel.com/lessons/dark-patterns-024)
- [Deceptive Patterns](https://uxcel.com/lessons/deceptive-patterns-186)
- [Ethics in Decision Making](https://uxcel.com/lessons/ethics-in-decision-making-346)
- [Attention & Well-being](https://uxcel.com/lessons/attention-well-being-732)
- [Writing Action-Based Messages](https://uxcel.com/lessons/action-based-messages-095)
