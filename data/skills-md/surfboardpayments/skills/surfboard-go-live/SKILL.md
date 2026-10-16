---
name: surfboard-go-live
description: "Move a Surfboard Payments integration from Demo to Live: certification, production credentials, PCI scope, supported markets and payment methods, settlements and reporting, monitoring, and support escalation. Use when an integration is built and verified in Demo and the user is preparing for real transactions."
---

# Going live

Read `surfboard-payments` first.

## An agent cannot do this

Going live requires a signed contract, a certification call with Surfboard, and
production credentials issued to a person. **Do not attempt to provision Live access.**
Your job is to get the integration ready and hand over a clear list.

## The sequence

1. Sign the contract and receive approval
2. Complete an onboarding call to test and certify the integration
3. Receive production credentials
4. Update the base URL from Demo to Live
5. Start accepting live payments

<https://developers.surfboardpayments.com>

## Readiness checklist

Work through this before the certification call. Items the agent can fix, fix.

**Configuration**
- [ ] Base URL, key, secret, and merchant ID all come from configuration, never source
- [ ] `.env` is gitignored; no secret has ever been committed
- [ ] Demo and Live credentials cannot be mixed. Separate config, separate deploys
- [ ] Secrets are in a real secret store in production, not a `.env` on the box

**Correctness**
- [ ] Amounts are integers in minor units everywhere, including tax and tips
- [ ] Currency is the numeric ISO 4217 code as a string
- [ ] `status` is checked on every response, not just the HTTP code
- [ ] Pagination terminates on empty `data` or `x-total-items`, never a short page
- [ ] Order and payment IDs are persisted against your own records

**Webhooks**
- [ ] Signature verified against the raw body before parsing
- [ ] Handler is idempotent; the same event twice is a no-op
- [ ] Returns 2xx quickly, work happens off the request path
- [ ] Endpoint is publicly reachable and monitored
- [ ] Fulfilment happens on the webhook, not on the browser redirect

**Money**
- [ ] Declines, cancellations, and timeouts each have a user-visible path
- [ ] Refund, void, and capture are chosen by settlement state
- [ ] Recurring charges are idempotent per billing period
- [ ] Reconciliation against settlement reports exists

**Scope**
- [ ] No PAN, CVV, or track data anywhere in the codebase, logs, or analytics
- [ ] No card data in error reporting or session replay

## PCI scope

Card capture happens on a Surfboard hosted page, on the terminal, or in the SDK. That
boundary is what keeps the integrator out of PCI scope, and it holds only as long as no
card data touches their systems.

Two things quietly break it: logging a full request body from a self-hosted checkout,
and session-replay tools recording a payment form. Check both.

Surfboard is PCI DSS, PCI PTS, and EMV Level 1 and 2 certified, licensed by
Finansinspektionen, multi-cloud across three PCI-certified providers, 99.99% uptime.

## Markets

Live in twelve European markets: Sweden, Denmark, Finland, Norway, UK, France, Ireland,
Estonia, Latvia, Lithuania, Poland, and Hungary.

**Payment methods and terminal availability differ by market.** `CARD` is everywhere;
`SWISH` is Sweden; Tap to Pay on iPhone is Sweden, Denmark, Finland, Norway, UK, and
France. Do not hard-code a method list; read it per store.

## Settlements and reporting

Reconciliation, payout reports, and transaction history:
`references/guides/settlements-reporting.md` and
`references/guides/transactions-and-reports.md`.

Build reconciliation before going live, not after the first disputed payout.

## After the handoff

Tell the user plainly what is done and what is theirs:

- The integration is verified in **Demo**, against these order IDs
- Physical terminal behaviour is **not** proven, because Demo is payment page mode only
- Live requires certification, which is a call with Surfboard
- Support: <https://developers.surfboardpayments.com>, integrations@surfboard.se

## Bundled guides

`references/guides/` holds: EMV terminal integration, settlements and reporting,
transactions and reports.
