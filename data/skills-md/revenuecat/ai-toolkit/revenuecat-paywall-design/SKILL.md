---
name: revenuecat-paywall-design
description:
  Must invoke for any request to create, edit, evaluate, understand, or improve a RevenueCat
  Paywall in the dashboard — including questions about a specific paywall or general paywall
  design recommendations. Not for presenting a paywall in app code (use revenuecat-paywall).
---

# Designing and editing RevenueCat Paywalls

This skill covers the **dashboard paywall**: creating, duplicating, editing, auditing, and
publishing. To **display** a configured paywall in the app with RevenueCatUI, use
`revenuecat-paywall` instead.

Paywall advice requires a paywall. An offering whose `paywall_id` is null has no RevenueCat
paywall: its purchase UI is client-side and invisible to you. Say so, and keep your advice to
what RevenueCat actually controls.

Via the `rc` CLI (see the `revenuecat-cli` skill): `rc paywalls generate --prompt "..."`,
`rc paywalls edit --prompt "..."`, `rc paywalls rewind --session <id>`, `rc paywalls publish`,
`rc paywalls show`. Prefer MCP below when you need screenshots or a structured `get-paywall`
read.

## Evaluating a paywall

When evaluating a RevenueCat Paywall, use `render-paywall-screenshot` to look at a static render
of above-the-fold content. The render is for you, not something to display to the user.

For a specific identified paywall, match the tool to the question:

- **Exact configuration** (default package, component bindings, offer-conditional content):
  `get-paywall` with `expand: ["components"]`. Without that expand, component configuration is
  omitted.
- **Visual inspection**: `render-paywall-screenshot`. A screenshot cannot verify
  configuration-dependent details.
- If a tool answer conflicts with what the user reports seeing, verify with `get-paywall` before
  disputing their observation; if `get-paywall` is unavailable, say you could not verify rather
  than disputing them.

Both `get-paywall` and `render-paywall-screenshot` use the draft when available, otherwise the
published version, and cover one paywall — not workflows or multipage paywalls. For general
paywall advice that is not about a specific paywall, answer directly without calling these tools.

If `get-paywall` fails, you may still report observations explicitly visible in a screenshot.
State that configuration-dependent details were not verified; do not silently replace
structure-aware analysis with screenshot reasoning.

## Editing

When the user explicitly asks you to edit an existing paywall, use `edit-paywall-ai`. It starts
an async task: poll `get-paywall-ai-task` with the returned task ID about every 10–15 seconds
until it succeeds or fails. Do not call `edit-paywall-ai` again for the same request unless the
task fails. Image-generation edits can take several minutes.

If the user wants to edit manually, link to the paywall builder:

```
https://app.revenuecat.com/projects/{project id without leading proj prefix}/paywalls/{paywall ID starting with pw}/builder
```

The builder also has a conversational AI editor in the left toolbar; you cannot link to it
directly.

If the user attaches images to the current message and the tool schema accepts them, pass them
through and tell the editor how they should be used. Do not reproduce visual details
unnecessarily. Images from earlier messages are not still attached — ask the user to attach
again.

MCP has no restore-version tool. If the user asks to undo an edit you made via MCP, tell them
they can restore an older version in the paywall editor. If they used the CLI, `rc paywalls rewind --session <id>` undoes the last editor action. Restoring does not publish.

## Duplicating

When the user asks for a paywall that copies, duplicates, or mirrors an existing one, use
`duplicate-paywall` rather than `create-paywall-ai`. `create-paywall-ai` designs from a blank
canvas and a text prompt, so it reproduces only what the prompt describes: images, exact
component structure, and anything unmentioned are regenerated rather than copied.

`duplicate-paywall` copies the source paywall — its current draft by default, or its published
version if you pass `source_version: published` (fails if the paywall has never been published)
— into a new unpublished paywall. Choose deliberately:

- When the source has a published version (`get-paywall`'s `published_at` is non-null), pass
  `source_version: published` — that is the paywall the user means when they reference one by
  name or link.
- Take the `draft` default only when the user is explicitly asking to copy in-progress
  unpublished edits, or the source has never been published.

Say which version you copied. Pass `offering` (`lookup_key` and `display_name`) to also
duplicate the source paywall's offering — packages only — and attach the copy to it; omit
`offering` to leave the copy unattached. When the user's framing is offering-first — a second
offering that should carry the same paywall — use `duplicate-offering` instead, which copies the
packages and the attached paywall together. Then apply differences with `edit-paywall-ai`, and
describe the result as a copy of the original rather than as a new design.

Duplication does not cover every paywall — multipage paywalls are not supported. If duplication
is unavailable or fails, you may fall back to `create-paywall-ai`, but tell the user the result
is a reconstruction from a description, not a copy, and that details such as images will differ.

## Creating

When the user asks you to create a new paywall, use `create-paywall-ai` to create a **draft
only**. It starts an async task: poll `get-paywall-ai-task` about every 30 seconds until it
succeeds or fails. Image-heavy creation can take 5–10 minutes; do not call `create-paywall-ai`
again for the same request unless the task fails.

Prefer creating the paywall for an existing offering when the user names one or when you can
confidently identify a suitable offering. If they do not name an offering, use `list-offerings`,
`get-offering`, `get-offering-prices`, `list-products`, `list-apps`, `get-app`,
`get-project-ui-config`, and `list-paywalls` to understand the app, products, pricing, brand
conventions, and existing paywalls first. Inspect the app/codebase and pass concise
`codebase_context` (premium features, brand colors, visual direction, tone, products, audience)
and `app_context` when you can infer it. Recommend the best offering when there is a clear fit;
if the user declines or no clear offering is known, create an unattached draft.

An offering can have at most one attached RevenueCat Paywall. If the offering has a
`paywall_id`, do not pass that offering as `offering_id` to `create-paywall-ai`. Explain that it
already has a paywall, and pick the option that matches:

- The new paywall should look like the existing one: duplicate it. This is the right choice
  whenever the user said "same as", "like", "copy", or "mirror".
- The existing paywall should change: `edit-paywall-ai`.
- The new paywall is a genuinely different design: choose a different or unattached offering, or
  create an unattached draft using the offering's products and pricing as context.

Do not present an unattached `create-paywall-ai` draft as the way to satisfy a duplication
request.

Fold gathered context into the prompt: app identity, target audience, core value proposition,
product durations, trials, price points, existing paywall patterns, brand colors or fonts, and
any user-stated design direction. Keep the prompt concrete enough for a one-shot draft and do
not ask the tool to publish.

A duplicated or newly created paywall is an unpublished draft. Do not publish unless the user
explicitly asks, except when preparing a treatment offering for an experiment (see
`revenuecat-experiments`).

# Overall ideas and guidance

## Collecting ideas

Search the RevenueCat blog and docs for paywall design and best practices. Markdown docs are at
the page URL with `.md` appended.

## Disallowed practices

Apple's App Review guidelines are strict. Patterns often touted as best practices can lead to a
rejected update or a store ban:

- **Trial toggle.** A toggle to enable/disable the trial. Apple rejects this as misleading.
- **Delayed close button.** A dismissible paywall that cannot be closed for a few seconds.
  Apple considers this misleading.
- **Second offer on dismiss / purchase cancel.** Least clear of the four; showing the exact
  same product after cancelling has been rejected as tricking users into unwanted purchases.
- **Non-IAP digital goods in-app.** Stripe or other non-IAP SDKs in the app or an in-app
  webview for digital goods. Linking out to web purchases in an external browser is a different
  (US) path; the purchase must not happen inside the app.

## Paywall placement

Try different placements: beginning or end of onboarding, as a feature gate, etc. Onboarding
paywalls tend to be very successful: they capture the highest number of potential customers
(nobody has churned yet) and motivation is high just after download.

## Always experiment

Results of different paywall designs are highly variable. Continuously test. At thousands of
new users per day, A/B testing with RevenueCat Experiments is the best validation. At hundreds
per day, tests can still be directional. Below that, ship and observe conversion over time. Use
the `revenuecat-experiments` skill to set up a test.

# Auditing existing paywall designs

Analyze the paywall and identify conversion issues. Prioritize conversion over aesthetic
consistency when they conflict. Audit in this order of impact.

### Visual issues (highest impact — fix these first)

**CTA Button** — single highest-impact element, address this FIRST.

- **CTA color is the #1 priority.** Look at the CTA button background color, then scan every
  other colored element (icons, badges, borders, card accents). If the CTA shares the same hue
  as ANY of them, it must change to a contrasting color that nothing else on the page uses. A
  CTA that blends in with the page accent kills conversion.
- If the CTA copy is generic ("Continue", "Subscribe"), it needs to be specific and
  action-oriented (e.g. "Start Yearly Plan", "Get Unlimited Access").
- If a free trial exists and the CTA does not mention it, the CTA should include trial language
  (e.g. "Start Free Trial", "Try for Free"). Trial info buried in small print is a conversion
  miss.

**Plan Card Differentiation**

- The recommended plan MUST be impossible to miss. It needs at least TWO of: a different
  background color, a colored border, a "Best Value" / "Most Popular" badge, or a larger/
  elevated card. A single subtle border change is not enough.
- If there is no default plan selected, one needs to be set.
- Equal-weight cards cause decision paralysis — differentiate the recommended plan.
- If a badge overlaps text, the selection indicator, or other content, reposition it.

**Price Anchoring** — required when multiple plans exist.

- If savings are not immediately visible (no crossed-out price, no "Save X%", no per-day
  comparison), the recommended plan needs a savings signal.
- The signal must be concrete. Vague phrases like "Save with annual billing" do not count. Show
  real values: a computed discount, a free-period callout, or a per-period price comparison.
  Never hardcode discount percentages or savings amounts.
- Use ONE clear anchoring signal. Stacking crossed-out price + savings badge + absolute
  discount + original price creates visual noise.

**Price Visibility.** Every package card MUST display its price.

**Content Reduction.** Count content rows between the headline and the packages/CTA. If there
are more than 4–5, remove the weakest. Every row above the fold competes with the CTA.

**Layout.** Packages and the CTA MUST be above the fold. Keeping the purchase action (and
ideally the packages) always visible regardless of scroll is the strongest pattern. Never
remove the purchase button or the privacy footer.

- The package group and the purchase button must be adjacent. Content between them should move.
- There must be visible spacing between packages and the purchase button (at least 12px).

**Trust Signals** — required. Every paywall MUST have a short reassurance line below the
purchase button (between the button and the privacy footer): "Cancel anytime", "No commitment",
trial terms. Order: packages → purchase button → reassurance text → privacy footer. If a free
trial exists, trial terms should be visible near the CTA (e.g. "7-day free trial, then $X/month").

### Trial presentation (when a free trial exists)

- Mention the trial in the CTA. "Start Free Trial" converts better than "Subscribe" with trial
  details in small print.
- The trial should be in the headline, the CTA, or both — not just legal text.
- For a multi-day trial (7+ days) using a trial-timeline archetype, check that steps are clear:
  start date, reminder date, charge date.
- If trial terms (length, price after trial) are not visible anywhere, add them near the CTA.

### Anti-pattern checks

- **Generic CTA copy**: "Subscribe", "Continue", or "Choose" tells users what to DO, not what
  they GET. Rewrite to action + benefit.
- **Identical feature lists on multiple plan cards**: remove the duplicates; comparison should
  be pricing only.
- **Negative-only value proposition**: "No ads, No interruptions, No limits" sells removal.
  Rewrite at least some items to what users GAIN.
- **Legal text as primary content**: terms and renewal policies drowning the sales pitch belong
  behind links. This does NOT apply to the privacy footer.
- **Missing CTA button**.
- **Missing privacy footer** with Terms and Privacy Policy links — App Store compliance.

### Copy issues (fix these last)

- Generic or feature-led copy → outcome-led. "Access all features" → "Master any language".
- Paragraphs longer than two lines should be shorter or become bullets.
- Headlines that describe the product → address the user. "AI-powered photo editor" → "Make
  every photo stunning".
