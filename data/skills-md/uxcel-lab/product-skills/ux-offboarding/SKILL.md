---
name: ux-offboarding
description: Design or critique an offboarding flow — canceling a subscription, unsubscribing, or deleting an account. Leads with the ethical stance (leaving must be easy and respectful — hiding the exit is a dark pattern), applies the always-true core (findable exit, preserve goodwill, prevent accidental destruction, explain consequences, ask feedback respectfully, offer genuine alternatives, close with a recovery path) and gates the retention levers (incentive offers, value reminders, confirmation friction, pause-vs-delete) with trade-offs so they don't tip into manipulation. Trigger when the user asks to design or review a cancel/unsubscribe/delete-account flow, a subscription cancellation, a churn/retention exit flow, or an account-deletion or deactivation experience.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Offboarding Skill

## How this skill behaves (read first)

This is a **generative** skill, and offboarding is the single most dark-pattern-prone flow in a product. The business wants to keep the user; the temptation is to bury the cancel link, confirmshame ("No thanks, I don't want to save money"), force a retention gauntlet, or make deletion frictionless to avoid the awkward conversation. Both extremes break trust: hiding the exit is manipulation, and a one-click permanent delete invites catastrophic accidents. Good offboarding holds two truths at once — **leaving must be easy and respectful**, *and* destructive actions must be **deliberate and recoverable**. Done well, a graceful exit preserves goodwill, earns referrals, and leaves the door open for users to return. So this skill gates:

1. **Establish what's being offboarded and how reversible it is** — a subscription cancel (billing, usually reversible) is not an account delete (data loss, often permanent); this sets the right amount of friction and which alternatives to offer.
2. **Apply the always-true core** — findable exit, goodwill over blame, prevent accidental destruction, explain consequences, respectful feedback, genuine alternatives, recovery path.
3. **Surface the context-dependent decisions** (retention incentives, value reminders, confirmation friction, pause-vs-delete) with trade-offs — these are exactly where offboarding tips into a dark pattern.

Then it **hands off to `ux-dark-patterns-audit`, `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-microcopy-audit`, and (when mobile) `ux-mobile-responsiveness-audit`** for validation.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill owns the **leaving experience** — the cancel/delete flow, its copy, retention moments, and recovery — and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the flow):** **the feedback-form fields** via `ux-inputs-and-forms`. **Peers that own a sub-part (defer):** **confirmation-modal mechanics** to `ux-modals-and-dialogs`, the **settings/billing entry point** to `ux-settings`, and the **undo / safety-net pattern** (reactivation, restore window), whose backbone is shared with `ux-error-recovery` (they own those sub-parts if reached). **Downstream (offer, don't auto-build):** **plan-change / downgrade pricing UI** via `ux-pricing`. **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **What's being offboarded, and how reversible is it?** *Unsubscribe / cancel subscription* mostly affects billing and is usually reversible (access continues until period end; reactivation is easy). *Delete account* can mean permanent data loss and lost access to important documents. The more irreversible the action, the more deliberate the confirmation and the clearer the consequence-explanation must be.
- **Why might users be leaving, and what's the business model?** People leave for neutral reasons (task finished, seasonal) as often as unhappy ones. If the product has a free tier, the reminder is about *subscription* benefits; if it's subscription-gated, it's about losing access entirely. Student/seasonal audiences are prime candidates for *pause* rather than delete.
- **Data & regulatory reality.** Be able to answer truthfully: is data deleted immediately or after a window? Can the account be restored? Does a profile stay public after deactivation? The flow must state what actually happens, not a comforting guess.
- **Platform & entry point.** Where the exit lives (web settings/billing vs. mobile settings) and how it's reached.

---

## The always-apply core (correct for almost every offboarding flow)

### Make leaving easy and findable
- **Show the exit plainly.** A visible, clearly-labeled Cancel / Unsubscribe / Manage Subscription / Delete Account control in the expected place (profile, settings, or billing). It should look clickable and be easy to notice.
- **Never hide it or trap the user.** Burying the cancel link or using friction to retain users "at any cost" kills loyalty and trust. If users want to leave, they will — your job is to leave a good impression on the way out.

### Be gracious, never blaming
- **Preserve goodwill.** Avoid any blaming or guilt-tripping tone. A respectful exit means referrals and return visits later; a punitive one means a bad review.

### Make destruction deliberate and clear
- **Confirm intent.** Prevent accidental clicks on a destructive action with a confirmation step — and use that moment honestly (a brief value reminder), never to beg or pressure.
- **Add a roadblock proportional to the consequence.** For irreversible data loss, require an intentional extra step — typing "delete" or re-entering the password — so the choice is conscious, not a slip.
- **Explain the consequences before the final action.** State clearly what happens to the account and data: Is it permanent? Can they restore it? Is deletion immediate or dated? How long does access remain?

### Learn, offer alternatives, and close well
- **Ask why — respectfully and optionally.** Offboarding is a feedback goldmine. Offer preset reasons plus an open "Other" field; never make it mandatory or pushy.
- **Offer genuine alternatives to a hard exit.** Pause, temporarily deactivate, downgrade, or change plan — each with a plain explanation of what it implies for data, billing, and visibility. (For a student app, "pause over summer" may be exactly right.)
- **Confirm the exit with gratitude and a way back.** Acknowledge and respect the decision, thank them, and let them know they're welcome to return. For cancellations, state how long access continues and send a follow-up email with a reactivation link — an "emergency exit" for the accidental or changed-mind user (user control & freedom).

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user decide. **These levers are where offboarding becomes a dark pattern — applying them aggressively is the mistake.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Retention incentive (discount / free upgrade)** | A genuine, easy-to-decline offer when a loyal user is about to leave | Repeated nagging, multi-step "are you *really* sure" gauntlets, or an offer that's hard to refuse | Offer once, friendly, one tap to decline and continue leaving |
| **Value reminder / consequences of leaving** | A brief, informative note on what they'd lose or keep | Language that begs for sympathy, guilt-trips, or confirmshames ("No, I don't care about my data") | Short and neutral; state facts, not pleas |
| **Confirmation friction level** | Type-to-confirm or password re-entry for permanent data loss | Heavy friction on a simple, reversible unsubscribe | Match friction to reversibility — light for cancel, deliberate roadblock for delete |
| **Pause / deactivate / downgrade vs. delete** | Offer as a real alternative when data retention genuinely helps the user (seasonal, financial) | Presenting pause as the *only* smooth path while the true delete is buried or grayed | Offer alternatives *alongside* an easy, honest delete — never as a substitute for it |
| **Feedback request** | When you'll actually act on the reasons | Mandatory, or blocking the exit until a form is filled | Optional, preset reasons + "Other", skippable |
| **Reactivation / win-back follow-up** | One reactivation email so a changed mind or accidental cancel can be reversed | Turning it into win-back spam or making "stay" easier to click than "stay gone" | A single, easy-to-ignore reactivation email with a clear unsubscribe |

High-consequence offboarding (permanent account/data deletion, regulated data) flips defaults toward more deliberate confirmation, an explicit and truthful data/restore explanation, and a serious, respectful tone over playful copy.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`dark-patterns`, `heuristics`, and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-dark-patterns-audit`** *(Tier A)* — the primary check here. Hunt for the roach-motel (easy in, hard out), a hidden/disguised cancel link, confirmshaming copy, a retention gauntlet, pre-selected "pause instead" that masks true deletion, asymmetric button emphasis (loud "Stay", whispered "Cancel"), or mandatory feedback as a toll. Leaving should be as easy as joining.
- **`ux-heuristics-audit`** *(Tier A)* — user control & freedom (a clear emergency exit, undo via reactivation), visibility of system status (what happens to data, when access ends), error prevention (deliberate confirmation for destructive actions).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — the destructive action and its confirmation are keyboard- and screen-reader-operable; consequences aren't signaled by color alone; the type-to-confirm step is accessible.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — symmetrical, honest emphasis between "stay" and "leave"; an uncluttered confirmation that doesn't bury the real action.
- **`ux-microcopy-audit`** *(Tier A)* — this flow lives on tone: gracious not guilt-trippy, clear consequence language, honest button labels (no "Yes/No" on a delete), respectful feedback prompts.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer)* — tap-target size and spacing on the confirm/cancel controls so the destructive and safe choices aren't a mis-tap apart; the exit reachable in mobile settings.

If the audits surface a conflict (e.g., the business wants a five-step retention gauntlet or a hidden cancel link), resolve back toward the principle: **the user has decided to leave — make it easy, honest, and recoverable; earn the next visit with a good exit, never trap them in this one.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Hide or disguise the cancel/delete link | Show it plainly in settings/billing with a clear label |
| Blame or guilt-trip the leaver | Preserve goodwill; thank them and leave the door open |
| One-click permanent delete | Deliberate roadblock (type "delete" / re-enter password) for irreversible loss |
| "Are you sure?" with no explanation | State exactly what happens to data, access, and timing |
| Confirmshame ("No, I hate saving money") | Neutral, factual value reminder; honest decline option |
| Force a feedback form before they can leave | Optional, preset + "Other", fully skippable |
| Offer only "pause" while burying real delete | Offer pause/downgrade *alongside* an easy, honest delete |
| Loud "Stay" button, whispered "Cancel" | Symmetrical, honest emphasis on both choices |
| Retention gauntlet of repeated offers | One easy-to-decline incentive, then let them go |
| No way back after an accidental cancel | Reactivation link / follow-up email; access until period end |
| Ship without checking | Hand off to dark-patterns + heuristics + accessibility + aesthetics + microcopy (+ mobile-responsiveness) |

---

## Source lessons (Uxcel)

- [Deleting Account](https://uxcel.com/lessons/deleting-account-728)
- [Canceling Subscription](https://uxcel.com/lessons/canceling-subscription-727)
