---
name: ledger-wallet
description: >
  Build a customer wallet as an append-only ledger with a balance per currency: stored credit topped up by
  Stripe Checkout, orders paid from the wallet, by card, or split between them, refunds that return each part
  to where it came from, and staff adjustments with a required reason. Use when: (1) customers prepay or top
  up a balance and spend it on bookings, tickets, orders or services, (2) a payment must combine a balance
  with a card, or a refund must go back to the balance, (3) balances exist in more than one currency, (4) an
  existing balance or credit module needs auditing, (5) the user mentions: wallet, stored credit, store
  credit, account balance, prepaid balance, top up, top-up, add funds, pay with balance, pay with wallet,
  split payment, hybrid payment, partial balance payment, refund to wallet, balance history, transaction
  history, multi-currency balance, ledger, double-entry, idempotent credit, idempotency key, reconcile
  balance, BalanceLedger, checkout.session.completed, async_payment_succeeded, "credit the customer", "admin
  balance adjustment". Carries a pure ledger core with refs that make every retry a replay, holds that keep
  a mixed payment's balance part reserved until the card pays, per-currency limits floored at Stripe's
  minimum charge, the currency list taken as the skill argument with USD by default, Firestore and Postgres
  stores verified by one conformance suite, and 97 tests. Next.js App Router; the store, auth and tenancy sit
  behind a seam. Not loyalty points, not gift cards, not a crypto wallet, not currency conversion, not
  marketplace payouts.
argument-hint: "[currencies, e.g. USD,EUR,GBP]"
---

# Ledger Wallet

A wallet is a number that must always be explainable. This skill keeps **every balance as the sum of an
append-only ledger, and every movement keyed by a ref derived from what caused it**, so a retried request, a
redelivered webhook or a double click replays the first result instead of moving money twice. Balances are
per tenant and per currency, and one currency is never converted into another.

## When to use

- Customers hold credit and spend it: prepaid visits, top-ups, store credit from refunds or goodwill.
- An order is paid from the wallet, by card, or by both, and refunds must follow the money back.
- Balances in several currencies, with the supported list chosen per app.
- Auditing an existing balance module: [provenance.md](references/provenance.md) has the audit ledger and the
  order of work.

## When NOT to use

- **Event registration with deposits**: the sibling `bookable-events` skill; it takes this wallet through
  its `BalanceLedger` port ([integration.md](references/integration.md)).
- **Payouts, marketplace balances, connected accounts**: the sibling `stripe-connect-subscriptions` skill.
- **Loyalty points, gift cards, vouchers**: separate products with their own expiry and liability rules.
- **Currency conversion or FX wallets**: this wallet never converts; each currency is its own balance.
- **Walk-up terminals**: the sibling `booking-kiosk` skill owns the unattended flow.

## Architecture

```
 customer routes            staff routes               Stripe webhook / sweeper
 (session: tenant, cust)    (staff: tenant, role)      (endpoint: tenant)
        |                          |                          |
        +------------- wallet.post / postInTx(tx) ------------+
                                   |
            one transaction: read balance (lock), read ref
              ref seen: replay | new: applyCommand (pure) | write balance + entry (+ hold)
                                   |
                     WalletStore: Firestore | Postgres | memory
 order code: postInTx inside the order's own transaction (wallet-only payment)
 split:      Checkout, then HOLD; webhook CAPTURE or RELEASE; sweeper for missed events
```

Routes resolve identity through `host.ts`, validate with zod and call the wallet. The wallet reads, checks the
ref, applies the pure core and writes, all in one transaction. Stripe only ever reaches the wallet through the
webhook handler and the sweeper, which share one code path.

### Adaptation contract

The seam lives here rather than in a separate `references/adaptation.md`. The rename table is in
[data-model.md](references/data-model.md).

| Seam | This skill ships | The host supplies |
|---|---|---|
| Domain entities | wallet, entry, hold, top-up, spend, refund, adjustment, and a rename table | its vocabulary (credit, balance, transaction) |
| Tenant scope | `tenantId` on every wallet, entry and hold, from the session or webhook path | its organization, workspace or site |
| Auth | `getCustomerSession`, `getStaffSession`, `customerExists` in `host.ts` | Firebase, Auth.js, Clerk, Supabase, or its own |
| Data access | `WalletStore` port; Firestore, Postgres and in-memory stores | its SDK, driver or ORM |
| Payments | Checkout top-up, split payment, refunds, the webhook handler | Stripe keys and a webhook secret per tenant |
| Orders | `postInTx`, `SplitCallbacks`, `refundOrder` | its order records and their payment fields |
| Currencies | `WALLET_CURRENCIES` in `config.ts`, filled from the skill argument | the list, the default, limit overrides |
| Background work | one sweeper route, every 15 minutes | its cron or scheduler |
| UI primitives | structure, states, semantics | buttons, dialogs, tables, toasts |
| Styling | none | its design system |
| Strings | `wallet.*` keys and error codes | its i18n files, every locale |
| Validation | zod schemas | zod, or its own library |

## Critical facts

1. **The ref is the idempotency key.** It comes from the thing that caused the movement (a Checkout
   session, an order, a dialog's request id), so every retry finds the first entry and replays it.
2. **Stripe delivers more than once, late, or not at all.** Every webhook branch replays safely, and a
   sweeper settles holds whose events never arrived.
3. **A completed Checkout is not always paid.** Bank debits complete first and pay days later; credit only on
   `payment_status: 'paid'` or `async_payment_succeeded`.
4. **Stored amounts use the currency's own minor unit; Stripe's differ for ISK and UGX.** They are sent x100,
   and every card amount is checked against Stripe's minimum before a session exists.
5. **Delisting a currency never strands money.** Top-ups stop at Checkout; spending, refunds and a Checkout
   already open still work.
6. **Lock order is part of the contract.** Read the balance (locking it) before the ref; on Firestore, every
   read before every write, including in a transaction shared with the host's order.

## Hard rules

1. **Every balance change is an entry, posted through the wallet.** Seeds, imports and corrections included,
   because a balance written anywhere else can no longer be explained or reconciled.
2. **Tenant and customer come from the session or the webhook endpoint, never the request body.** A body
   field lets anyone move money in someone else's wallet or another tenant's.
3. **Money moves once, with what it pays for.** A wallet payment commits in the order's transaction; a mixed
   payment holds and captures only when the card pays, because a debit before the order exists has nothing
   to recover it from.
4. **Credit only what Stripe collected.** The route that opens Checkout credits nothing; the webhook credits
   `amount_total` once, on a paid session, because the redirect is not proof of payment.
5. **Refund what was paid, to where it came from.** The amounts the order recorded when it was paid, per
   source, never its current total, because a total can change after payment and an unpaid order has
   nothing to refund.

## Quick start

Copy every template as written; the host's code goes in `host.ts`, `host-client.ts`, `config.ts`, the
`lib/orders/` examples and files of its own. A template that looks wrong is reported in the handover, not
patched, and the webhook and cron routes are copied, never merged with the host's own.

1. Resolve the currency list from the skill argument, or ask with USD as the default; unattended, take USD:
   [money.md](references/money.md).
2. Model and rename: [data-model.md](references/data-model.md). Core: [engine.md](references/engine.md).
3. Store: [firestore.md](references/firestore.md) or [postgres.md](references/postgres.md).
4. Routes and the host seam: [api-routes.md](references/api-routes.md). With no auth in the app, identity is
   a signed cookie or none (401); never a header, a query or a fallback identity.
5. Top-up and webhook: [stripe-top-up.md](references/stripe-top-up.md).
6. Orders: [integration.md](references/integration.md), then [split-payment.md](references/split-payment.md).
7. Screens: [ui.md](references/ui.md), [admin-ui.md](references/admin-ui.md).
8. Tests, unmodified, after `npm i -D vitest`; one store leaves out the other backend's file:
   [testing.md](references/testing.md), [testing-payments.md](references/testing-payments.md),
   [testing-stores.md](references/testing-stores.md).
9. Go live: [operations.md](references/operations.md). Before changing a template:
   [provenance.md](references/provenance.md).
10. Hand over in the final message itself, not only a README: the currencies and default, the webhook URL per
    tenant and its four events, the 15-minute cron and `CRON_SECRET` (unset, it refuses), the identity seam.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Types, entry kinds, refs, rename | WalletEntry, EntryKind, ref, tenantId, invariants, WalletError | [data-model.md](references/data-model.md) |
| Currencies, minor units, limits | WALLET_CURRENCIES, ISO 4217, ISK, JPY, KWD, parseMajorToMinor, formatMoney, minimum charge | [money.md](references/money.md) |
| Posting, replay, holds, history | applyCommand, createWallet, postInTx, WalletStore, REF_CONFLICT, reconcile | [engine.md](references/engine.md) |
| Firestore store | walletEntries, runTransaction, create(), indexes, security rules, AggregateField | [firestore.md](references/firestore.md) |
| Postgres store | wallet.sql, FOR UPDATE, 23505, bigint as string, keyset cursor, RLS, Supabase | [postgres.md](references/postgres.md) |
| Top-up, webhook, return page | createTopUpCheckout, handleWalletEvent, checkout.session.completed, whsec, stripe listen | [stripe-top-up.md](references/stripe-top-up.md) |
| Wallet plus card, refunds, sweeper | planPayment, startSplitPayment, splitAttempt, HOLD, CAPTURE, RELEASE, refundOrder, CRON_SECRET | [split-payment.md](references/split-payment.md) |
| Orders, other modules, bookable-events | pay in the order transaction, walletPaid, cardPaid, BalanceLedger, toBalanceLedger | [integration.md](references/integration.md) |
| Routes, auth seam, errors | host.ts, getCustomerSession, customerExists, zod, 402, error contract | [api-routes.md](references/api-routes.md) |
| Customer screens | WalletPanel, useWallet, top-up form, ?topUp=success, history, strings | [ui.md](references/ui.md) |
| Staff screens | WalletAdminPanel, adjust dialog, note, requestId, reconciliation flag | [admin-ui.md](references/admin-ui.md) |
| Config, cron, monitoring, seeds | go-live, delist currency, import balances, secret rotation, wallet_short | [operations.md](references/operations.md) |
| Money and engine tests | vitest.config.mts, memory store, money.test, wallet.test | [testing.md](references/testing.md) |
| Stripe and route tests | fake Stripe, webhook replay, split, refunds, route guards | [testing-payments.md](references/testing-payments.md) |
| Real-backend tests | store contract, postgres.test, firestore.test, Firestore emulator, WALLET_PG_URL, order atomicity | [testing-stores.md](references/testing-stores.md) |
| What the audit changed and why | audit, provenance, kept deliberately, added, order of work | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
