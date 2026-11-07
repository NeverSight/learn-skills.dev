---
name: spree-marketplace
description: Use when building or extending a multi-vendor marketplace on Spree 6 — sellers/vendors, seller onboarding requirements, seller product review (submit/approve/reject), split checkout into order groups, commissions (rates, rules, commission lines, commission tax), seller payouts and the transfer/payout ledger, Stripe Connect, a custom payout provider, the seller panel (`@spree/seller-dashboard`), or the Seller API (`/api/v3/seller`, `@spree/seller-sdk`). Common phrasings include "marketplace", "multi-vendor", "vendor", "seller", "Spree::Seller", "invite/approve a seller", "onboarding checklist", "seller requirements", "order group", "isOrderGroup", "split order per seller", "commission rate", "commission line", "seller payout", "payout provider", "SweepDueJob", "Stripe Connect", "seller API", "X-Spree-Seller-Id", "seller dashboard".
---

# Spree Marketplace (Sellers, Commissions, Payouts)

Everything in this skill ships in open-source Spree 6 — sellers, onboarding, product review, order splitting, commissions, the payout ledger, Stripe Connect and the seller panel. There's no "marketplace mode" switch: a store becomes a marketplace when it has sellers. Most marketplaces are **configuration, not code**; write code only for a new requirement kind, commission rule, payout provider, or a bespoke seller app.

Spree Enterprise only: refund clawbacks and netting across settlements, reconciliation against provider statements, KYC operations, seller tax reporting (DAC7), and marking a seller `platform` for tax remittance (marketplace-facilitator). Don't promise these on OSS.

## The model

| Model | Prefix | What it is |
|---|---|---|
| `Spree::Seller` | `sel_` | A vendor inside a store (single-store resource, paranoid). Owns products, stock locations, delivery methods, package types, policies, its own team via roles |
| `Spree::Product#seller_id` | — | `nil` = the marketplace's own stock. `LineItem#seller_id` is **snapshotted** from the variant/product while the line is still being chosen and frozen at placement |
| `Spree::ProductSubmission` | `prodsub_` | Review record: `pending` / `approved` / `rejected` / `withdrawn`; rows accumulate, latest is live |
| `Spree::SellerRequirement` (STI) | `selreq_` | One checklist row, an instance of a registered kind |
| `Spree::SellerRequirementSubmission` | `selsub_` | What a seller submitted: `pending` / `accepted` / `rejected` / `waived` |
| `Spree::OrderGroup` | `ogrp_` | One checkout that reached several sellers; holds customer, addresses, payment, summed totals |
| `Spree::PaymentSplit` | `paysp_` | A seller order's share of the group's single payment |
| `Spree::CommissionRate` / `CommissionRule` | `crate_` / `comrule_` | Configuration: what to charge, and when |
| `Spree::CommissionLine` | `cline_` | Frozen record of one charge (per item, plus per fulfillment when delivery is commissioned) |
| `Spree::SellerTransfer` | `vtr_` | Ledger row, `kind` `earning` or `refund_reversal` |
| `Spree::SellerPayout` | `vpo_` | A settlement batch of transfers, one per currency |

### Seller statuses

`has_status :pending, :invited, :canceled, :onboarding, :ready_for_review, :approved, :rejected, :suspended` (default `pending`). There's no state machine. Each move is a workflow, and the Admin API exposes each one as its own member action:

```
pending ─invite→ invited ─(invitation accepted)→ onboarding ─submit_for_review→ ready_for_review ─approve→ approved
ready_for_review ─reopen_onboarding→ onboarding          onboarding|ready_for_review ─reject→ rejected
approved ─suspend→ suspended ─approve→ approved           rejected ─approve→ approved
```

Workflows live in `Spree::Sellers::{Create, Invite, StartOnboarding, SubmitForReview, Approve, Reject, Suspend, ReopenOnboarding}`. Each one declares `hooks :validate, :after_<verb>`, so you extend them with `Spree.hooks.register('sellers.approve.validate', ->(wf) { wf.reject!('…') if … })` (see `spree-workflows`). **Never write `seller.update(status: 'approved')`.** That skips the checks, the mail and the hooks. Only `approved` sellers outside holiday mode sell (`Spree::Seller.sellable`), and sellers pause themselves with `holiday_mode_until`. `Sellers::Create` also provisions the seller's stock location.

Events: `seller.invited`, `seller.onboarding_started`, `seller.submitted_for_review`, `seller.approved` (payload carries `requirements_overridden` and `unmet_requirements`), `seller.rejected`, `seller.suspended`, `seller.onboarding_reopened`, `seller_requirement_submission.{accepted,rejected,waived}`, `seller_payout.completed`, `order_group.completed`, plus lifecycle `seller.created/updated/deleted` and `product_submission.*`.

## Store preferences (Settings → Marketplace)

All of these can be written via `PATCH /api/v3/admin/store` (`adminClient.store.update({...})`):

| Preference | Default | Notes |
|---|---|---|
| `preferred_payout_provider` | `nil` → `Spree::PayoutProvider::System` | Must be a class name in `Spree.payout_providers`, otherwise the write is refused. A store whose provider vanished from the registry falls back to System |
| `preferred_default_payouts_schedule_interval` | `monthly` | `daily` / `weekly` / `biweekly` / `monthly` / `manual`. A per-seller value wins |
| `preferred_default_minimum_payout_amount` | `0` | Balances below this carry forward |
| `preferred_auto_approve_sellers` | `false` | Admits a seller the moment the checklist is done, with no human review |
| `preferred_auto_approve_seller_products` | `false` | Submit chains straight into approval (the submission row is still written, marked auto-approved) |
| `preferred_send_seller_transactional_emails` | `true` | Turn this off if you front seller comms yourself |
| `preferred_default_commission_tax_rate` | `0` | A **fraction** (`0.23` = 23%). The dashboard shows a percentage |

## Onboarding requirements

The checklist is **configured per store, computed on read**. It's never stored on the seller, so a new requirement applies to everyone immediately. It's **enforced at exactly two moments**: `SubmitForReview` (422 `processing_error` naming the blocker) and `Approve` (refused unless `override_requirements: true`, and the override is recorded on the event). After that it's advisory.

The 13 core kinds (`Spree.seller_requirements`) fall into three groups:
- **Computed**, where Spree reads the seller's data: `accept_terms`, `complete_profile`, `billing_address`, `returns_address`, `delivery_method`, `package_type`, `minimum_products`, `payout_account`, `required_custom_fields`, `policy`.
- **Attested**, where the seller submits: `attestation`.
- **Verified**, where the seller submits and the operator accepts or rejects: `operator_review`, `document`.

A new store gets the first 7 in its default checklist. `attestation`, `operator_review`, `document` and `policy` can appear several times and need a `name`. The rest are one per store. `type` is write-once.

**Always build the checklist UI from `GET /api/v3/admin/seller_requirements/types`** (`adminClient.sellerRequirements.types()`), which returns each kind's `preference_schema`. Never hardcode the list, because custom kinds then show up for free.

A custom kind is an STI subclass, registered like this:

```ruby
# app/models/my_app/seller_requirements/insurance_on_file.rb
module MyApp::SellerRequirements
  class InsuranceOnFile < Spree::SellerRequirement
    preference :minimum_cover, :integer, default: 1_000_000

    def met_by_seller?(seller)           # override this, never #satisfied? (waivers live there)
      seller.get_custom_field('insurance.cover')&.value.to_i >= preferred_minimum_cover
    end

    def applicable?(seller) = true       # false hides the row entirely
  end
end

# config/initializers/spree.rb
Rails.application.config.after_initialize do
  Spree.seller_requirements << MyApp::SellerRequirements::InsuranceOnFile
end
```

A kind that takes submissions overrides the `self.accepts_submissions?`, `self.reviewed_by_operator?`, `self.requires_file?` and `self.accepted_content_types` class methods. Uploaded documents are checked by their bytes (not the filename) and stored privately.

## Product review

A marketplace adds the `proposed` and `rejected` product statuses. Sellers **submit** a product and the operator decides. On the seller side: `sellerClient.products.submit(id)` / `bulkSubmit`, and sellers can always `draft` or `archive` their own listings. On the operator side: `adminClient.products.approve(id)` / `reject(id, { reason })`. The review queue is `products.list({ status_eq: 'proposed' })`. Put the rejection reason on the reject call, which stores it on the submission. Never put it in product `metadata`, because the seller can overwrite that. See `spree-catalog`.

## Split checkout: order groups

When a cart spans N sellers, completion creates an `OrderGroup` with one `Order` per seller (plus the operator's own order for first-party items). There's one payment, apportioned as `PaymentSplit`s. A single-seller checkout produces a plain order with no group. The division happens in **`Spree::Orders::Complete`** (the order-side workflow), which both cart checkout and admin-raised draft orders go through. So:

- **`POST /api/v3/store/carts/:id/complete` can return an `OrderGroup` (`ogrp_…`, with `orders[]`) instead of an `Order`.** `@spree/sdk` types `carts.complete` as `Promise<Order | OrderGroup>`; narrow with its `isOrderGroup(result)` guard (keys on `orders[]`). The confirmation page and order history should show the group as one purchase.
- **`PATCH /api/v3/admin/orders/:id/complete` can return a group too.** In `@spree/admin-sdk`, use `isOrderGroup(result)`: `const orders = isOrderGroup(r) ? r.orders : [r]`.
- Group totals are **summed from the children**, not divided. Delivery and order-level fees are **apportioned by item value**.
- Checkout data is copied, not shared: every child order (and the group) carries the checkout-level fields — customer, email, company, market, channel, `customer_note`, `po_number` — and its own deep copy of the cart's `metadata` (customer-writable — never trust it for approval/fraud flags). Editing one sibling's metadata never reaches the others.
- If you finalize orders from custom code, go through `Spree.order_complete_workflow` or `Spree.carts_complete_workflow`, never a status write. Seller attribution, commission and the group all depend on it.
- **One purchase, one confirmation.** Each child order is placed silently (its `order.placed` payload has `notify_customer: false`); the customer and store-owner emails go out once from the group on **`order_group.completed`** (payload carries the purchase's real `notify_customer`) via `Spree::OrderGroupMailer` / `Spree::OrderGroupEmailSubscriber`, tracked by `order_group.confirmation_delivered` / `store_owner_notification_delivered`. A resend from any child order in the admin (`POST /api/v3/admin/orders/:id/resend_confirmation` → `order.resend_confirmation_email`) is forwarded to `order_group.resend_confirmation_email`, so it resends the group's email. If your storefront or ERP sends its own confirmation, subscribe to `order_group.completed` as well as `order.placed` and honor `notify_customer` on both (in Ruby, `order.grouped?` tells you a child order) — otherwise split checkouts get no confirmation or one per seller. Non-split checkouts are unchanged.
- **Orders ≠ parcels.** Several seller orders shipping from one warehouse share one delivery charge (split across them) and one box. For "what will arrive", use `order_group.fulfillment_groups` (`Spree::FulfillmentGroup`: `delivery_method`, `cost`, `line_items`, `sellers`, `orders`), not the child-order count.
- Admin reads only: `adminClient.orderGroups.list()` / `get('ogrp_…', { expand: ['orders'] })`.

## Commissions

Spree charges commission **synchronously on `order.placed`** (`Spree::OrderCommissionSubscriber` → `Spree.commissions_commission_order_service`, idempotent). The charges are grouped by `line_item.seller_id`. Lines with no seller aren't commissioned. Core semantics:

- **Rates are tried in list order and the first match wins.** There's no specificity scoring. A rate with no rules matches everything, so the **catch-all goes at the bottom** (for example `position: 99`). **New rates are created at the top.**
- Within a rate, **every rule must match**. The IDs inside one rule are alternatives. Rule types (`Spree.commission_rules`) are `product_rule`, `category_rule` (matches descendants too), `seller_rule` (an empty one matches **nothing**), and `item_total_rule` (lower bound inclusive, upper bound exclusive). One rule of each type per rate. `rules: [...]` replaces the whole set on update. Discover the types with `GET /admin/commission_rates/rule_types`.
- **No matching rate means no commission.** Spree doesn't invent a default.
- The basis is **net by default** (`tax_inclusive: false`) and always after discounts. `include_shipping` commissions delivery too, but a `fixed` rate **can't** commission shipping.
- Money is stated per currency and never converted. `amounts: { USD: '5.00' }` sets a flat fee, charged **per unit**, and a currency missing from `amounts` falls through to the next rate. `bounds: { EUR: { min_amount, max_amount } }` sets a percentage floor and cap. A percentage still applies uncapped in a currency with no bounds.
- **Commission tax follows the seller's jurisdiction**, resolved in this order: the rate's `commission_tax_rate`, then the tax engine using the seller's billing address, then the store's `preferred_default_commission_tax_rate`. `taxability_reason` is `standard_rated` / `zero_rated` / `reverse_charge`.
- **Lines are frozen snapshots with no write path.** Editing or soft-deleting a rate never rewrites history.
- A commission is not a `Spree::Fee`. The customer never sees it and it's not part of the order total.

Swap points are the `Spree::Dependencies` keys `commissions_resolve_rate_service`, `commissions_resolve_tax_rate_service`, `commissions_calculate_line_service` and `commissions_commission_order_service`. A custom rule subclasses `Spree::CommissionRule`, implements `applicable?(context)` (the context exposes `seller`, `order`, `line_item`, `fulfillment`, `currency`, `product`, `subject`), and is appended to `Spree.commission_rules` inside `Rails.application.config.after_initialize do … end` (same pattern as requirement kinds above).

## Payouts: the ledger

```
order.fulfilled  → SellerTransfer(kind: earning)          = seller's sale − commission, sale currency
refund.created   → SellerTransfer(kind: refund_reversal)  (never edits the earning)
sweep (schedule) → SellerPayout per seller per currency, lists the transfers it settles
complete         → operator (System provider) or provider webhook → seller_payout.completed
```

- Sellers earn **on fulfillment, not payment**. A digital order fulfills, and so earns, immediately.
- Transfers and payouts share the statuses `pending` → `processing` → `completed`, `failed` and `unresolved`. **Only completed payouts debit the balance.** Nothing completes at creation. `unresolved` means the outcome is unknown, so the transfers stay claimed to avoid paying the same money twice. An operator resolves it (or the webhook does).
- The balance is derived, per currency (`adminClient.sellers.balances(id)`). Settle by hand with `adminClient.sellers.settle(id)` (`POST /admin/sellers/:id/payouts`). It returns **201 even on partial failure**, with the failures listed under `meta.failures`, or 422 when there's nothing owed. For the System provider, mark a payout paid with `adminClient.sellerPayouts.complete('vpo_…', { reference })`.
- **Two recurring jobs must be scheduled by the host app.** If they aren't, sellers are silently never paid. Check `server/config/recurring.yml` (Solid Queue) or your own scheduler:

```yaml
production:
  sweep_due_seller_payouts:
    class: Spree::SellerPayouts::SweepDueJob
    schedule: at 3am every day
  execute_pending_seller_transfers:
    class: Spree::SellerTransfers::ExecutePendingDueJob
    schedule: every hour at minute 27
```

Both are cheap no-ops on a store without sellers. The per-seller interval logic runs inside them, so don't try to express it in cron.

**Payout providers.** Providers are registered in `Spree.payout_providers` and chosen per store:
- `Spree::PayoutProvider::System` is the default. It keeps the books and moves no money.
- `SpreeStripe::PayoutProvider` (the `spree_stripe` gem) is Stripe Connect. Sellers onboard through Express. Every earning becomes a transfer with `source_transaction` set to the customer's charge. Payouts run on Spree's schedule (the connected account uses a manual schedule), and `payout.paid` / `payout.failed` arrive at `POST /api/v3/webhooks/payouts/:payment_method_id`. In local dev, use `stripe listen --forward-connect-to …` with `STRIPE_CONNECT_SIGNING_SECRET`. Refunds write a reversal row only, since the Stripe transfer reversal is Enterprise.
- A custom provider subclasses `Spree::PayoutProvider::Base`. See **[references/payout-provider.md](references/payout-provider.md)** for the contract, error semantics, idempotency and the webhook pattern.

When a provider `requires_payout_account?`, add the `payout_account` requirement. Without it, a seller can be approved and sell, but their earnings sit pending.

## Seller API and seller panel

`/api/v3/seller/*` is a separate surface for a signed-in seller's team. `@spree/seller-sdk` wraps it. The key facts:

- Auth is a **JWT only**, with audience `seller_api` (admin and store tokens get 401). There's **deliberately no secret key**. Every call needs `X-Spree-Seller-Id` (except `GET`/`PATCH /seller/me`, the signed-in person's own account). The refresh token is an HttpOnly cookie scoped to `/api/v3/seller/auth`. Store staff who run no seller get 401 at login.
- **403** means no or unknown seller header, or a missing permission key. **404** means not found *for this seller*, and it's also what another seller's record returns, so records can't be enumerated. No endpoint takes a seller ID in its path.
- Sellers **submit** products and can't set `active`. Sellers **can't mark orders delivered**. Ledger endpoints (`balances`, `transfers`, `payouts`) are read-only.
- Seller staff permissions come from roles the seller owns, with the same flat permission keys as the back office but a narrower set (see `spree-auth-permissions`).

```ts
import { createSellerClient } from '@spree/seller-sdk'
const seller = createSellerClient({ baseUrl: 'https://marketplace.example.com' })
const { token, sellers } = await seller.auth.login({ email, password })
seller.setToken(token)
seller.setSeller(sellers[0].id)
await seller.orders.fulfillments.fulfill(orderId, fulfillmentId, { tracking: '1Z…' })
```

The full namespace table, operator Admin endpoints and routes are in **[references/seller-api.md](references/seller-api.md)**.

**Seller panel.** `@spree/seller-dashboard` is a React SPA sharing `@spree/dashboard-core` and `-ui` with the admin dashboard. `create-spree-app` scaffolds it automatically. In an existing project, run `spree add seller-dashboard`, which creates `apps/seller-dashboard/`. It runs on dev port **5174** (the admin dashboard uses 5173), and production serves it at `/sellers`. Things to know:
- Only set `VITE_API_PROXY_TARGET` in `.env.local`. **Don't set `VITE_SPREE_API_URL` in dev**, because it bypasses the proxy and breaks the `SameSite=Lax` refresh cookie.
- Customize in `src/plugins.ts` with `defineDashboardPlugin` imported from `@spree/seller-dashboard` (see `spree-dashboard-plugins`). **Only two slots exist**, `seller.team.actions` and `seller.team.after`. For anything else, add a route. The `seller.form_*` slots belong to the *admin* dashboard.
- It ships **English, Arabic, German, French, Polish and Simplified Chinese** (`src/locales/{en,ar,de,fr,pl,zh-CN}.json`). Each seller user picks a language in the account dialog; it's saved as `selected_locale` on their account (`PATCH /seller/me`) and adopted at sign-in on any browser. Switching reloads the page. To add a language, drop another `src/locales/<code>.json` into the panel — it's discovered from the bundle files, not the API. There's no branding config: restyle through Tailwind and override translation keys for copy.
- The account dialog edits the signed-in person (name, photo, language) via `PATCH /seller/me`; the seller business (public profile) is `PATCH /seller/profile`. Keep that split in custom UIs.

For sample data in development, run `spree rake spree:sellers:sample_data` (native: `bin/rails spree:sellers:sample_data`). It signs in as `seller@example.com` / `spree123` and refuses to run outside development and test.

## Gotchas

- **Storefronts and back offices must handle `OrderGroup` results** from completion. This is the most common marketplace bug.
- **Missing recurring jobs**: the sweep and the pending-transfer retry must be in `recurring.yml` or your scheduler. Nothing warns you if they're absent.
- **The catch-all commission rate sits above specific ones**: everything below it is unreachable, and new rates land on top.
- **A `seller_rule` naming no sellers matches nothing**, and a fixed rate with no amount for a currency is skipped for that currency.
- **Enabling auto-approve on an open marketplace** removes the only human gate.
- **Setting statuses directly** on Seller, Product, SellerPayout or Order. Use the workflows and endpoints.
- **Raising `GatewayError` on a timeout in a payout provider** re-sends money. Raise `Spree::Core::AmbiguousGatewayError` instead.
- **Keep payout webhook handlers idempotent.** Match payouts by `(provider, reference)`, never by amount or recency.
- **Seller-scoped custom endpoints** must root every lookup in the current seller and return 404, not 403, for other sellers' records.
- The `spree:sellers:sample_data` rake task is dev/test only.

## Where to read further

- `node_modules/@spree/docs/dist/developer/core-concepts/sellers.md`, `…/commissions.md`
- `node_modules/@spree/docs/dist/developer/how-to/build-a-marketplace.md`: the end-to-end setup guide
- `node_modules/@spree/docs/dist/developer/providers/payouts.md`: writing a payout provider
- `node_modules/@spree/docs/dist/integrations/payments/stripe-connect.md`
- `node_modules/@spree/docs/dist/api-reference/seller-api/{introduction,authentication,errors}.md`
- https://spreecommerce.org/docs/developer/core-concepts/sellers
- Related skills: `spree-workflows` (hooks), `spree-checkout` (cart completion), `spree-fulfillment` (seller delivery methods, package types), `spree-payments` (Stripe), `spree-dashboard-plugins`, `spree-events-webhooks`
