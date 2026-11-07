---
name: telegram-bot-payments-stars
description: Implement Telegram Stars or provider checkout, trusted payment fulfillment, recurring subscriptions, refunds, reconciliation, paid media, gifts and Mini App invoices. Use for bot monetization; it does not authorize spending, refunding or gifting on its own.
---

# Telegram payments and Stars

Read [the payment guide](references/guide.md) for rail selection, invoice/checkout handlers, recurring lifecycle, shipping, reconciliation and gifts. Check [sources and versions](references/sources.md) before quoting limits, provider availability or gifting prices.

## Workflow

1. Classify the product and choose Stars for digital goods/services sold inside Telegram; choose an eligible provider for physical goods/services.
2. Persist an order with owner, exact currency/amount, fulfillment and expiry policy. Generate an opaque unique payload; define whether the invoice is one-time or recurring.
3. Build the invoice server-side. On pre-checkout, verify owner, payload, amount/currency and availability, and answer within ten seconds.
4. Fulfill only from trusted successful-payment updates. Atomically record the charge and entitlement; deduplicate Telegram charge IDs and reject conflicting replays.
5. Handle refunds, recurring renewals/cancellation/failure and reconciliation as explicit state transitions. Preserve records and bound retries for money-changing operations.
6. Test mismatches, duplicate/concurrent updates, restart, refund confirmation and expiry offline. Use test/staging payment paths only when authorized.

## Invariants

- Stars use `currency="XTR"`, exactly one price item and an empty provider token (or SDK-supported omission). Amounts are integer Stars. Provider amounts use the currency's documented smallest unit; do not assume every currency has two decimals.
- A pre-checkout approval or Mini App `openInvoice` result is not proof of paid fulfillment.
- `createInvoiceLink` supports Stars recurring invoices with the documented subscription period. A title saying “subscription” does not create recurrence.
- Cancellation stops future renewal; preserve paid access through the recorded period. Refund API success/confirmation is distinct from requesting a refund.
- Webhook authentication and database idempotency solve different problems; keep both.
- Paid-media unlock events, invoice receipts and outgoing Stars expenses have different fields and fulfillment rules; route each to its own ledger/service.
- Tokens stay in the environment/secret manager. Do not put Mini App auth validation snippets here; use the Mini Apps skill's tested implementation.

## Resources

- [scripts/payment_ledger.py](scripts/payment_ledger.py): offline SQLite **one-time credit-order** fulfillment and completed-refund reconciliation. It deliberately does not implement recurring entitlements or contact Telegram.
- [scripts/test_payment_ledger.py](scripts/test_payment_ledger.py): price/user/currency checks, concurrent duplicates, rollback, persistence and user-bound refund replay tests. Run `python -m unittest discover -s telegram-bot-payments-stars/scripts -p 'test_*.py'` from the repository root.

Combine with a framework skill for handlers, Mini Apps for in-app checkout, Keyboards UI for invoice entry points, and Advanced Features for durable queues and operations.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
