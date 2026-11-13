---
name: ux-contact-support
description: Design or critique a contact/support experience — help center, FAQ, contact methods, live chat, point-of-error help, and feedback flows. Leads with self-service deflection (most contacts are UX failures), applies the always-true core (easy access, expectation-setting, honest chat, close the loop) and gates context-dependent levers (which channels and order, chatbot vs. human, help-button placement) with trade-offs. Trigger when the user asks to design or review a contact us page, support page, help center, FAQ, live chat, or feedback form.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Contact & Support Skill

## How this skill behaves (read first)

This is a **generative** skill, and it starts from an uncomfortable fact: **~64% of support contacts are caused by a UX failure** — missing/unclear info, a service problem, a roadblock, or a task that looks too complex. So the default instinct ("add a contact form") treats the symptom. The skill's first move is to *reduce the need* with self-service, then make getting a human easy and predictable when it's genuinely warranted. The common failures: no FAQ/help before the form, a "Contact us" button that drops users into a surprise channel, no wait-time or expectations set, a bot that doesn't admit it's a bot, no help offered at the moment of error, and feedback requests that interrupt and pressure. So this skill gates:

1. **Establish why users contact support and what the team can sustain** — that orders the channels and sizes the self-service investment.
2. **Apply the always-true core** — deflect with good self-service, make contact easy and predictable, close the loop.
3. **Surface the context-dependent decisions** (which channels and order, chatbot vs. human, help-button placement) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, `ux-dark-patterns-audit`, and `ux-mobile-responsiveness-audit`** for validation.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill covers the **support experience and its surfaces** and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the support surface):** the **contact-form field design** via `ux-inputs-and-forms`. **Peers that own a sub-part (defer):** **help search** to `ux-search` and **tooltip craft** to `ux-tooltips` (they own those sub-parts if reached). **Downstream (offer, don't auto-build):** deeper **error-message/recovery design** via `ux-error-recovery`. **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **Why do users contact support here?** The four drivers, by frequency: information missing/unclear, a service problem (failed payment, damaged item), a roadblock they can't pass, or a task that looks too complex. Most are fixable upstream — the most contacted topics are a backlog for self-service and product fixes, not just staffing.
- **What can the team sustain?** Live chat and phone are what users often prefer, but they're the hardest to staff across time zones — channel *order* must reflect both user preference and your capacity, not just one.
- **Platform & entry points** — where will users look for help (web footer / mobile settings), and at which moments (error pages) is contact predictable?

---

## The always-apply core (correct for almost every support experience)

### Deflect first — help users help themselves
- **Lead with self-service.** Offer the FAQ / help content as the first option so users can resolve issues without waiting; reserve human channels for specific, complex problems.
- **Make the help page scannable.** Frequent questions first, organized by category, bite-size paragraphs, bold headings, lists, clear hierarchy, highlighted keywords — people scan for their problem, they don't read.
- **Plain language, with the right format.** No jargon; short active sentences. Use **tooltips** for brief in-context help, and pair step-by-step guides with screenshots/short video *and* a text version (not everyone can or wants to watch).
- **Treat the FAQ as a supplement, and shrink it over time.** Build it from real signals (support tickets, surveys, search queries, forums); the long-term goal is fewer "frequently" asked questions because the product and docs got clearer.

### Make contact easy and predictable
- **Reachable from everywhere.** A support link in the standard spots (web footer, mobile settings) plus the recognizable **? -in-a-circle** help icon; in menus, help sits near the bottom (feedback just above it, sign-out lowest to avoid accidental exits).
- **Offer help at the point of error.** A good error message says what happened and the next action — and when that action is "get help," link the right channel (FAQ/article for simple, an agent for complex) right there.
- **Set expectations before the user commits.** Never let "Contact us" drop someone into a surprise video call. State the response-time estimate, what info they'll need to provide, and — if calls/chats are recorded — say so up front.

### Chat done honestly
- **Label it "Chat" / "Live Chat"** (nothing cuter) and place it where users expect — Help/Contact pages.
- **Disclose the bot immediately.** If a chatbot triages first, say so from the start so users adjust their language and expectations, then hand off to a person for real issues. If live support is offline, say that and offer alternatives (FAQ, email).

### Close the loop
- **Follow up after resolution.** A short "did this resolve your issue?" email while the experience is fresh; for chat, include the transcript for the user's records.
- **Ask for feedback respectfully.** Keep forms short and rating-first (written comment optional); time the ask after a satisfying moment (not mid-task); never use intrusive pop-ups and never make feedback compulsory.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Which channels, and in what order** | Order by user preference *and* team capacity — FAQ/email scale; phone/chat are immediate but staffing-heavy | Advertising 24/7 live chat a small team can't sustain (worse than not offering it) | FAQ first; email next; surface phone/chat prominently only if you can staff them |
| **Chatbot vs. human-first** | A bot to triage and collect info before routing, when volume is high | Hiding that it's a bot, or trapping users with no path to a human | Bot triage *with upfront disclosure* and a clear handoff to a person |
| **Have an FAQ at all** | As a quick-reference supplement built from real questions | As a dumping ground that masks poor product discoverability | Yes as a supplement; treat a growing FAQ as a signal to fix the product |
| **Help-button placement** | Floating button (follows scroll) for constant access; header for complex sites; footer for simple ones | A help link users must hunt for | Match to site complexity; help is never more than a click away |
| **Video vs. text help** | Complex interactions where seeing it helps | Video-only (excludes users who can't/won't watch) | Offer both; text always available |
| **Satisfaction measurement (NPS/CSAT)** | When you'll act on the trend over time | One-off vanity scoring, or interrupting the task to ask | Lightweight, well-timed; tie to improvements (metric validity → PM audits if it feeds OKRs) |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `microcopy`, and `dark-patterns` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — help & documentation (findable, task-focused), visibility of system status (wait times, bot vs. human, chat availability), error recovery routing to the right channel.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — help icon labeling, scannable heading structure, chat keyboard/screen-reader operability, captions/transcripts for help videos.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — a scannable help page over a wall of text, uncluttered contact options.
- **`ux-microcopy-audit`** *(Tier A)* — this skill lives on copy: expectation-setting, bot disclosure, error next-steps, channel labels, FAQ wording, feedback prompts.
- **`ux-dark-patterns-audit`** *(Tier A)* — the support-specific traps: compulsory or guilt-tripping feedback requests, intrusive pop-ups, a chatbot impersonating a human, or making the only path to a human deliberately hard. Asking should be respectful and skippable.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer)* — tap targets on contact options, chat usability on small screens, sticky help-button placement that doesn't cover content.

If the audits surface a conflict (e.g., the business wants a mandatory survey after every chat), resolve back toward the primary task: **the user came with a problem — resolve it, then ask for input gently, never as a toll.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Jump straight to a contact form | Lead with self-service; most contacts are fixable UX failures |
| A wall of help text | Scannable: frequent Qs first, categorized, headings + lists |
| Jargon-filled articles | Plain, short, active language; tooltips for brief help |
| "Contact us" → surprise video call | State channel, response time, info needed, recording notice first |
| Bury the help link | Standard spots + ? icon; floating/header/footer by site complexity |
| No help when an error occurs | Offer the right channel at the point of error |
| A bot pretending to be a person | Disclose the bot upfront; hand off to a human for real issues |
| Advertise 24/7 chat you can't staff | Order channels by user preference *and* team capacity |
| Mandatory or pop-up feedback mid-task | Short, rating-first, optional, well-timed after a good moment |
| Treat a growing FAQ as success | Treat it as a signal to fix product discoverability |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy + dark-patterns + mobile-responsiveness |

---

## Source lessons (Uxcel)

- [Contact Support](https://uxcel.com/lessons/contact-support-960)
- [Design Guidelines for Help Center & Support Pages](https://uxcel.com/lessons/help--feedback-best-practices-040)
