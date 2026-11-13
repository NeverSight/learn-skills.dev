---
name: ux-login-signup
description: Design or critique a login / sign-up screen. Applies the always-true core (separate pages, minimal fields, inline validation, full password-reset flow) and gates context-dependent choices (social login, 2FA, "stay logged in", username vs. email) with trade-offs. Trigger when designing auth screens, sign-up forms, registration flows, or password recovery.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Login & Sign-up Screen Skill


## How this skill behaves (read first)

This is a **generative** skill, so it does **not** blindly apply every best practice — login/sign-up has a set of context-dependent levers (social login, "stay logged in", username vs. email, 2FA) where applying everything is wrong for some products and right for others. Auto-applying all of them produces a bloated, insecure, or privacy-hostile screen.

So the skill works in three moves:

1. **Establish context** (one quick question if it's not already known).
2. **Apply the always-true core** — the patterns that are correct for essentially every auth screen.
3. **Surface the context-dependent decisions** with their trade-offs and a recommendation, and let the user choose — don't silently pick.

Then it **hands the result to the audit skills** for validation: call the **heuristics audit** (`ux-heuristics-audit`) and the **accessibility audit** (`ux-accessibility-audit`) on the generated screen. This skill deliberately does *not* re-derive contrast/keyboard/screen-reader rules — that's the accessibility skill's job.

---

## Step 0 — Establish context before designing

Auth design changes sharply with these. If they aren't known, ask:

- **Platform** — mobile (tight horizontal space → top-aligned/floating labels, contextual keypads, ≥38px touch targets) vs. desktop.
- **Security sensitivity** — casual consumer app vs. banking/health/enterprise. This is the single biggest driver of the gated decisions below.
- **Audience** — mainstream consumers (favor social login, low friction) vs. security-conscious or regulated users.

State the assumption if you proceed without an answer (e.g. "Assuming a standard consumer SaaS on web").

---

## The always-apply core (correct for almost every auth screen)

**Structure**

- **Separate login and sign-up** into distinct pages/views. Don't merge them — users try the wrong one and get frustrated.
- **Make switching obvious**: a clear title states which page you're on, and a "Don't have an account? Sign up" (or vice-versa) link sits *above* the inputs where users look. Social buttons appear on both pages.
- **Keep sign-up to one short screen.** Ask only the essentials (identifier + password). Collect everything else *later, contextually*, after the user has experienced value.

**CTAs**

- **Visually distinct labels.** Avoid the "Sign in" / "Sign up" near-collision — prefer **"Log in"** vs. **"Sign up"** or **"Register"**.
- **Button hierarchy**: the primary action gets the brand/primary color and weight; the secondary action is muted or a text button. One dominant action per screen.
- CTA visible without scrolling; on long mobile forms, fix it to the bottom.

**Password field**

- **Show/hide toggle** (eye icon) that works both ways — typo prevention, especially on mobile. This also lets you drop the "confirm password" field.
- **Password requirements visible while typing** (a live checklist), not revealed only on error.

**Password recovery** (the most-abandoned path — design the whole flow, not just a link)

1. **Reset link below the password field**, where users expect it, clearly labeled (it's the "emergency exit" — Nielsen's user control & freedom).
2. Ask for **only 1–2 fields** (email or phone) to verify identity.
3. **Confirmation page** telling the user what happens next ("check your inbox").
4. **Clear next-step instructions** in the email/SMS — a prominent link or code, minimal text.
5. **Reset page** with the new-password input and requirements visible.
6. **Success acknowledgement**, then redirect to login (or the intended destination).

**Validation & submit states**

- **Inline validation** as the user leaves each field — never wait until Submit to reveal all errors. Show the result next to the field; green check for success, red for failure.
- Submit shows a **loading state**, then a **success message** or a **clear error**.
- **Security caveat on errors**: use a generic "Invalid username or password" rather than revealing which one was wrong.
- Error copy is **plain, polite, specific** — what went wrong + how to fix it. No jargon, no ALL CAPS, no blame.

**Form mechanics** (mobile-sensitive)

- **Top-aligned or floating labels** — never placeholder-only (placeholders vanish on focus and force recall).
- **Helper text** below fields that need it (e.g. why a phone number is required).
- **Contextual keypads** (numeric pad for phone/code) and **input masks** for formatted data.
- **Touch targets ≥ ~38px**; inputs 32–40px tall; primary button width matched to inputs for balance.

---

## The context-dependent decisions (surface, don't auto-apply)

For each, present the trade-off and a recommendation tied to the Step 0 context, then let the user decide. **Applying all of these by default is a mistake.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Social login** (Google/Apple/etc.) | Mainstream consumer apps — ~80% of users prefer it; cuts friction, verifies email for you | Privacy-sensitive audiences, enterprise SSO contexts, or where you need data control | Offer it for consumer apps; pair with an email option. Ask before adding. |
| **Identifier: email/phone vs. username** | Username only if social identity/handles matter to the product | Username as a *requirement* — harder to recall, more failed logins | Default to email or phone; offer username only as an option |
| **"Keep me logged in" / "Remember me"** | Low-stakes apps where re-entry is annoying | Banking/health/enterprise — auto-logout after inactivity; remember the *username* only, not the session | Sensitivity-dependent — this is why Step 0 matters |
| **2FA / biometrics** | High-stakes or regulated data; biometrics for quick secure mobile login | Casual low-risk apps where it adds needless friction | Recommend for sensitive data; optional elsewhere |
| **Single screen vs. progressive profiling** | Almost always start minimal | — | Minimal now, ask more contextually later |

When the product is high-security (banking, health), the convenience levers (stay-logged-in, social) flip toward the secure choice and 2FA/biometrics become recommended rather than optional.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `dark-patterns` are Tier A (auto-run); `accessibility` and `aesthetics` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — checks feedback/status on submit, error recovery, consistency, recognition (e.g. visible password requirements).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — label/contrast/keyboard/focus specifics, which this skill intentionally defers.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — visual hierarchy and the overdesign check: did the gated levers (social buttons, 2FA, password rules) clutter the screen or bury the primary action?
- **`ux-dark-patterns-audit`** *(Tier A)* — if sign-up adds marketing opt-ins, forced social connect, or over-broad permissions: checks for preselection, forced action, and confirmshaming.

If the audits surface a conflict (e.g. you added social login, a "remember me", 2FA prompt, *and* a long password policy, and minimalism now suffers), resolve back toward the primary task: getting the user in.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Merge login and sign-up into one ambiguous form | Separate pages with a clear title and an above-the-form switch link |
| "Sign in" next to "Sign up" | "Log in" vs. "Sign up" / "Register" — visually distinct |
| Ask for many fields at sign-up | Identifier + password only; collect the rest contextually later |
| Placeholder-only fields | Top-aligned or floating labels that persist |
| Reveal all errors after Submit | Inline validation as the user leaves each field |
| "Error: invalid input" / ALL CAPS | Plain, polite, specific message next to the field |
| Reveal whether the username *or* password was wrong | Generic "Invalid username or password" |
| Hide the password with no reveal option | Eye icon to show/hide; drop "confirm password" |
| Just a "Forgot password?" link with no flow | Design the full recovery flow through to success + redirect |
| Auto-apply social login + stay-logged-in everywhere | Surface them as context-dependent choices with trade-offs |
| Keep users logged into a banking app indefinitely | Auto-logout on inactivity; remember username only |
| Ship without checking | Hand off to the heuristics + accessibility audits |

---

## Source lessons (Uxcel)

- [Best Practices for Designing Login & Signup Flows](https://uxcel.com/lessons/loginsignup-best-practices-854)
- [Designing Mobile Logins, Signups, & Other Forms](https://uxcel.com/lessons/logins-signups-and-other-forms-462)
- [Resetting Password](https://uxcel.com/lessons/resetting-password-363)
- [Best Practices for Designing Forms](https://uxcel.com/lessons/forms-best-practices-423)
- [Submitting a Form](https://uxcel.com/lessons/submitting-a-form-507)
