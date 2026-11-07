---
name: lovable-ship-checklist
description: >-
  Use when I say I'm about to launch, ship, go live, release, or ask if the app
  is production-ready. Run the checklist and report pass/fail per item. Not for
  feature building, refactors, or SEO copywriting from scratch.
---

# Launch / ship checklist

Walk every section. Report **pass**, **fail**, or **needs manual check**. Do not say "ready to launch" until all pass or are explicitly waived.

## Account flows

- Sign-up, sign-in, sign-out, password reset work end to end.
- Signed-out users cannot access protected routes.
- Post-login redirect lands on the correct page.

## Core surfaces

- Home and primary routes render without console errors.
- Lists/feeds have real **empty states** (not "No data" alone).
- Long actions show loading; errors offer retry or clear message.
- Mobile (~375px): no horizontal scroll; primary actions reachable.

## Data and permissions

- User tables have **RLS enabled** (see `supabase-rls-and-auth` if fixing).
- Cross-account access blocked — flag **needs manual check**; ask for second test account.
- Destructive actions (delete, cancel, refund) require confirmation.
- No tenant or user ID accepted from request bodies for authorization.

## Billing (if payments are part of the product)

- Stripe webhook endpoint configured, signature verified, idempotent (`stripe-payment-webhooks`).
- `subscriptions` / `orders` table is the source of truth — no client query-string entitlement.
- Test cards work in test mode; live keys only on production env.
- Failed-payment banner + Customer Portal link (`payment-failed-and-recovery`).

## Content and trust

- App name, favicon, OG image, meta description set on public pages.
- Privacy policy and terms links work (footer).
- No placeholder copy ("Lorem ipsum", "TODO", "Your headline here").

## Accessibility (quick pass)

- Every input has a visible label; icon-only buttons have `aria-label`.
- Keyboard: Tab order makes sense; modal Escape closes; visible focus ring.
- Text contrast ≥ 4.5:1 on body text.

## Environment and secrets

- No `localhost`, dev URLs, or test API keys (`sk_test_*`) in production paths.
- No service-role or webhook secrets exposed in `VITE_*` variables.
- Required env vars set in Lovable / hosting; secrets configured in Supabase for edge functions.
- Analytics/events fire on signup, activation, and key conversions.

## Observability

- Errors visible (Sentry/PostHog/Logflare or at least Supabase function logs).
- 404 and 500 pages exist and link home.

## Final output

1. Summary of failures and manual checks, **priority order**.
2. Go / no-go with explicit blockers.
3. List items waived (and why) so they are not forgotten next ship.
