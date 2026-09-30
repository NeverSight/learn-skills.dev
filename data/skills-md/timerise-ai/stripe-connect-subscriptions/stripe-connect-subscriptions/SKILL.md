---
name: stripe-connect-subscriptions
description: >
  Build Stripe Connect marketplace money movement and Stripe platform subscription
  billing in a Next.js App Router app. Use when: (1) one buyer charge must split
  across several sellers: separate charges and transfers, transfer groups, escrow,
  rolling reserves, payouts to connected accounts; (2) implementing Connect account
  onboarding, `account.updated` capability flags, or debugging why a connected
  account is never funded; (3) charging tenants a recurring platform fee off-session
  with SetupIntents, saved cards and dunning; (4) reconciling gateway fees, transfer
  reversals, refund or chargeback clawbacks against a ledger; (5) the user mentions:
  Stripe Connect, connected account, transfer_group, source_transaction, separate
  charges and transfers, destination charge, application_fee_amount, acct_,
  marketplace payouts, split payment, Express onboarding, account.updated,
  off_session, SetupIntent, dunning, subscription invoices, whsec_, "merchant never
  gets paid", "Funds can't be sent to accounts located in". Carries settlement
  internals the store's atomic claims and the money tests verify: webhook
  idempotency, single-flight claims, transfer retry with adoption, and the region
  rule that decides whether a connected account can be paid at all. Next.js App
  Router oriented; the data layer is one PaymentsStore seam, so any relational
  backend fits. Not a general checkout or PayPal skill.
---

# Stripe Connect & Subscription Billing

Two money flows on one Stripe account. A **marketplace** charges the buyer once
and fans the proceeds out to many merchants (Connect, *separate charges and
transfers*). A **platform subscription** charges those merchants a recurring fee
off-session (Billing). They share a client, a webhook pair and a money type.

The insight that shapes everything: **the buyer's charge and the merchants'
payouts fail independently.** By the time settlement runs the money has already
moved, so a rejected transfer must never fail the charge or the webhook, and
must stay re-drivable later without paying anyone twice.

## When to use

- One payment splits across several sellers, with the platform taking a cut.
- Sellers onboard to Connect and are paid on a delay (escrow, reserves, KYC).
- The platform bills its own sellers a recurring fee on a saved card.
- A connected account looks healthy but has never received any money.

## When NOT to use

| Not this | Use instead |
|---|---|
| Single-seller checkout, no split | Stripe Checkout / Payment Element directly |
| PayPal Marketplace onboarding + payouts | A PayPal skill; only the seams are shared |
| Card UI, Payment Element styling | Your design system; this skill is server-side |

## Architecture

```
buyer --charge (platform account, transfer_group = orderId)--> platform balance
                |  settlement fan-out (webhook OR read-path sync; leased claim)
   +------------+--+------------------------+----------------+
   v               v                        v                v
transfer:merchant  transfer:partner    escrow hold     rolling reserve
(source_transaction = the charge)      (release_at)    (% withheld)
   |                                        |  release-escrow cron
   v                                        v
connected balance <-- retry-transfers  payable balance --> payout (KYC/risk gated)
                      (unfunded legs)

platform --off_session PaymentIntent (customer + saved PM)--> subscription invoice
             dunning: 3 attempts, 3 days apart, then suspend
```

## Critical facts

1. **Separate charges and transfers, never destination charges.** A charge takes
   one `destination`; a multi-vendor cart needs N transfers under one
   `transfer_group`, so `application_fee_amount` is unusable.
2. **A transfer without `source_transaction` draws on the *available* balance**
   and is rejected while the charge is still settling; on a young platform
   account, that is every transfer. This one flag is what lets a split fund
   while the charge is still settling.
3. **Stripe transfers cross-border only inside US/CA/UK/EEA/CH.** A platform
   elsewhere pays connected accounts in its own country only. Stripe enforces
   this at transfer time, not onboarding time, so the templates apply the
   region rule at onboarding.
4. **Connect events carry a different signing secret** than platform events. Two
   endpoints, two secrets, one URL: verify against both.
5. **A connected account's country is immutable.** A wrong country means
   re-onboarding, not a patch.
6. **Money is never a float.** `numeric(19,4)` strings end to end, `bigint` math,
   minor units only at the SDK edge.

## Hard rules

> **Never let a failed transfer fail the settlement.** Record the leg unfunded
> and continue. The charge has already succeeded, so the webhook must succeed
> too; the retry cron funds the leg later.

> **Never treat a duplicate webhook insert as "already handled".** The insert is
> a *claim*; the retry after a delivery crashed mid-handling re-runs the
> handlers, so every event runs to completion exactly once.

> **Never re-send a transfer without asking Stripe whether it already exists.** A
> leg recorded unfunded because the *response* was lost pays twice once Stripe's
> 24h idempotency window passes.

> **Never derive settlement exclusivity from a status flag written at the end.**
> Two callers reach settlement routinely; an atomic leased claim is what makes
> inventory and transfers happen once.

> **Never reverse more than a transfer's remaining headroom.** Stacked reversals
> (gateway fee, then a refund) are rejected past the original amount.

## Quick start

The code blocks are the module: copy them verbatim apart from the renames and seams in
[adaptation.md](references/adaptation.md). The seams are the store's implementation, auth, validation and
audit; settlement, retry, onboarding and money logic are never redesigned, and no lock is added around the
leased claim. A template that looks wrong is named in the handover, not patched.

1. Model the money: [money.md](references/money.md), [data-model.md](references/data-model.md),
   [store.md](references/store.md). Install what the module imports: `stripe`, `vitest` and, when the host
   has no database, `pg` for the raw-SQL store. The package registry is not an external service. An
   in-memory store is for tests only.
2. Client, dual webhook secrets, env: [stripe-adapter.md](references/stripe-adapter.md). `.env.example`
   lists all five variables in [operations.md](references/operations.md), empty and tracked; invent none.
3. Onboard accounts on manual payouts; **check the region rule first**:
   [connect-accounts.md](references/connect-accounts.md).
4. Receive events idempotently: [webhooks.md](references/webhooks.md).
5. Settle by claim, fan-out, escrow and reserve: [settlement.md](references/settlement.md). A payout hold
   ("paid out after N days") sets both escrow constants to that window, names kept; the transfer still runs
   at settlement, never later.
6. Converge by retrying legs and reconciling fees: [reconciliation.md](references/reconciliation.md).
7. Bill tenants: [subscriptions.md](references/subscriptions.md); run it with
   [operations.md](references/operations.md).
8. Wire `money.test.ts`, unmodified, to `npm test` under `vitest`; report its ten tests. The final message
   itself, not only a README, names the region check for the platform's country, the two webhook endpoints
   and their secrets, and the crons behind `CRON_SECRET`.

Fit it to your app with [adaptation.md](references/adaptation.md), which carries the
seam contract with the host; the record of the audit is in
[provenance.md](references/provenance.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Why this money model | separate charges and transfers, destination charge, application_fee_amount, transfer_group, ledger | [architecture.md](references/architecture.md) |
| Tables, columns, RLS | schema, migration, payment_intents, transfers, escrow_holds, webhook_events | [data-model.md](references/data-model.md) |
| The data-access contract | store, repository, atomic claim, conditional update, ORM | [store.md](references/store.md) |
| Amounts and rounding | numeric, bigint, minor units, distribute, largest remainder, cents | [money.md](references/money.md) |
| Client and adapter code | stripeClient, apiVersion, constructEvent, whsec_, PaymentIntent, refund, payout | [stripe-adapter.md](references/stripe-adapter.md) |
| Onboarding, account state | Express, Accounts v2, account.updated, charges_enabled, acct_, country, region | [connect-accounts.md](references/connect-accounts.md) |
| Receiving events safely | idempotency, duplicate, replay, raw body, signature, invalid_signature | [webhooks.md](references/webhooks.md) |
| Splitting a paid order | settlement, fan-out, source_transaction, escrow, reserve, single-flight | [settlement.md](references/settlement.md) |
| Fixing what didn't land | retry, unfunded, backoff, adopt, gateway fee, clawback, reversal, headroom | [reconciliation.md](references/reconciliation.md) |
| Recurring platform fees | SetupIntent, off_session, saved card, dunning, invoice, past_due, suspend | [subscriptions.md](references/subscriptions.md) |
| Setup, env, crons, debugging | STRIPE_SECRET_KEY, webhook endpoint, stripe listen, cron, "merchant never paid" | [operations.md](references/operations.md) |
| Fitting it to this app | adapt, host probe, rename, ORM, auth guard, port | [adaptation.md](references/adaptation.md) |
| The audit record | provenance, deviation, kept, added, unverified | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
