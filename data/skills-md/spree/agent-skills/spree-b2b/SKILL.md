---
name: spree-b2b
description: Use when building B2B or wholesale commerce on Spree 6 — the end-to-end "build a B2B store" setup, companies/buyer organizations (company trees, divisions, members, invitations, company address book, buying on a company's behalf), catalogs and negotiated pricing (assortments, owned price lists, percentage adjustments, catalog assignment to companies or customer groups, channel default catalogs), customer groups, gated storefronts (`storefront_access` login_required / prices_hidden), the Next.js wholesale portal, minimum order quantity / order multiples / order minimums, PO numbers, and orders on account (pay by invoice, staff-keyed draft orders with negotiated prices, `payment_pending`), and freight shipping (cartons, pallets, unpriced freight rates). Common phrasings include "B2B", "wholesale", "build a B2B store", "pay by invoice", "net terms", "negotiated line price", "draft order for a company", "trade customers", "company account", "Spree::Company", "division", "buyer organization", "negotiated prices", "customer-specific pricing", "catalog", "price list per company", "MOQ", "minimum order quantity", "order multiple", "case pack", "order minimum", "PO number", "purchase order reference", "login to see prices", "members-only store", "wholesale portal", "X-Spree-Channel", "freight", "pallet", "carton".
---

# Spree B2B / Wholesale

In Spree 6, B2B is built from **four open-source building blocks**. They're all configuration, and one storefront plus one backend can serve retail and trade side by side:

| Block | Answers |
|---|---|
| **Company** (`Spree::Company`) | Who is buying: an organization, its people, its addresses, its tax identity |
| **Catalog** (`Spree::Catalog`) | The agreement: what that audience sees, what they pay, how much they must order |
| **Channel** gating (`storefront_access`) | Whether guests can see the catalog or prices at all |
| **Freight** (delivery rules plus the `Freight` rate provider) | How wholesale loads ship: cartons, pallets, containers, quoted after review |

The end-to-end walkthrough is the **Build a B2B Store** guide (`node_modules/@spree/docs/dist/developer/how-to/build-a-b2b-store.md`) — follow it for setup order and dashboard screens; this skill is the rules and traps behind it.

**Seeded for every store:** a `wholesale` channel (`login_required`, guest checkout off), a **Wholesale** customer group (the wholesale portal's approval marker), and a publishable key bound to the wholesale channel. Sample data (`spree sample-data`) adds a demo buyer `wholesale@example.com` / `spree123` — publicly known credentials, so **never load sample data into production** (the task has no environment guard) — a wholesale price list with quantity breaks, the two-level company *Acme Industrial* → *Acme EMEA*, and an **inactive** *Wholesale Assortment* catalog assigned to Acme Industrial.

Spree Enterprise only: company roles and capabilities (the OSS membership `role` is a cosmetic label, and every member can do everything within their standing), order approvals (`approval_required`), spending limits, governance audit history, and a company onboarding/approval flow. Payment terms, net invoicing and quotes are on the Enterprise roadmap. Enterprise governance enforces through the same endpoints, so an OSS storefront keeps working unchanged when it's switched on.

## Companies

- A **tree** with at most **5 levels** (`Spree::Company::MAX_DEPTH`). The root must be `kind: 'company'`. `kind` is `company` (a legal entity that can hold tax registrations) or `division` (an organizational unit that can't). Prefix: `comp_`.
- **Membership covers the subtree.** A member of "Acme Europe" can act for every node below it. Authorization always asks "does this customer have standing on this node or any ancestor?" Memberships (`cmem_`) are always active and always tied to a real customer.
- **Adding people by email.** From the **storefront** (`client.companies.members.create(companyId, { customer_email })` → `POST /api/v3/store/companies/:id/members`) it **always** creates an invitation (`cinv_`), even for an existing customer — typing an address doesn't prove it's the person you mean, and the response doesn't reveal whether the email has an account. From **staff** (dashboard / `POST /api/v3/admin/companies/:id/memberships`, service `Spree::Companies::AddMember`) an existing customer becomes a member at once (`cmem_`) and an unknown email gets an invitation — check the ID prefix. Invitations **expire after 30 days**. Invitees call `companyInvitations.lookup(token)` / `accept(token, { first_name, last_name, password })` without signing in.
- **Address book per company.** Each address is labeled, with default ship-to and bill-to. A delivery site is an address, not a node, so ten warehouses don't need ten companies.
- **Tax resolves through the nearest `company` ancestor** (`company.legal_entity`). The walk **stops at the first company node even if it has no registration**, so a subsidiary never borrows its parent's VAT number. Tax identifiers and exemption certificates live on legal entities only. Read a certificate's `active`, not its status, because `active` also accounts for expiry. See `spree-taxes`.
- Deleting a node removes its whole subtree, and **Spree refuses** if any order exists beneath it. Move a branch by updating `parent_id`.
- There's **no storefront self-registration for companies**: the Store API only offers `show`/`update` on `/store/companies`. Staff create companies in the dashboard or through `POST /api/v3/admin/companies`.

### Buying for a company

```ts
// Store SDK: which companies can the signed-in customer act for?
const { data: memberships } = await client.account.companies()   // m.company.ancestors = path above it

await client.carts.update(cartId, { company_id: 'comp_xxx' })     // must be a node they have standing on
const { data: orders } = await client.companies.orders.list('comp_xxx') // whole-subtree order history
// other members' orders come with gift card codes masked and no digital download links — those stay with the buyer
await client.companies.addresses.create('comp_xxx', { label: 'Northern Warehouse', /* … */ default_shipping: true })
```

A buyer with exactly one membership doesn't need to choose, because the company resolves automatically. `company_id` on the cart is **frozen onto the order at completion**, along with addresses and prices. The cart exposes `company_id`, `company_name` and `po_number_required`. On the backend, `cart.b2b?` / `cart.resolved_company` (in the `Spree::Purchase::Company` concern) are what your code should read.

## Catalogs: the agreement

A catalog (`cat_`) has an **assortment** (`CatalogProduct`), an optional **owned price list**, **assignments** (`cata_`) to a `customer_group` or a `company`, and **commercial terms**.

- **An empty assortment is a pricing overlay**: the audience sees everything, at the catalog's prices. **A non-empty assortment restricts the range**: the audience sees *only* those products. Adding the first product flips the catalog from "everything" to "only this".
- The **price list is owned by exactly one catalog** and has no audience rules of its own. It applies *because* the catalog applies, and it's excluded from normal rule matching. Removing it (`price_list: null`) or deleting the catalog **soft-deletes** the list. Spree never releases it, because an ownerless, ruleless list would price every shopper. A deactivated catalog's list goes dormant.
- Pricing is explicit per-variant `prices` and/or `price_adjustment_percentage` (for example `-15`) with optional `price_adjustment_tiers` quantity bands. The percentage mode only works on catalog-owned lists.
- **Catalogs are created inactive.** Go live with `adminClient.catalogs.activate(id)` (`PATCH /admin/catalogs/:id/activate`). Activation is a workflow (`Spree::Catalogs::Activate`), not a column write, and it's **refused for a catalog with no assignments** (error `no_audience`) unless it's some channel's `default_catalog_id`. Deactivating keeps everything for later; deleting also deletes the owned price list.

```ts
const catalog = await adminClient.catalogs.create({
  name: 'Acme wholesale',
  price_list: { name: 'Acme pricing', price_adjustment_percentage: -15 },
  assignments: [{ assignable_type: 'company', assignable_id: 'comp_xxx' }],
  minimum_order_quantity: 6, order_multiple: 6,          // catalog-wide defaults
  order_minimums: [{ currency: 'EUR', amount: 500 }],    // per currency, never converted
})
await adminClient.catalogs.products.create(catalog.id, ['prod_a', 'prod_b'])  // → restricting mode
await adminClient.catalogs.activate(catalog.id)
```

### Resolution: who sees what, and what they pay

1. **Find the audience. The first source that yields any catalog wins, and the sources don't combine.** In order: the company node **and its ancestors**, then the customer's groups, then the channel's `default_catalog_id`.
2. **Visibility** is the union of those catalogs' assortments. **If any applicable catalog is an overlay (empty assortment), there's no restriction.**
3. **Price**: first the owned lists of applicable catalogs, **nearest node first**. Within one node, when several catalogs apply, **the best price wins**, compared at the quantity being bought. Then ordinary price lists whose rules match. Then the base price. A nearer node's agreement beats a cheaper one further up.

**Company buyers never pick up customer-group catalogs** once any catalog is assigned in their company chain. Model trade tiers as company assignments (a group-wide catalog on the root, tier catalogs on member companies or divisions). Use customer groups (`cg_`) only for buyers who don't buy on behalf of a company, such as a retail loyalty tier, staff, or approved wholesale individuals. For new setups, prefer catalogs over `CustomerGroupRule` price lists.

Gated storefront access (below) is checked **before** catalog resolution.

### Quantity rules and order minimums

- A **per-variant** `minimum_order_quantity` and `order_multiple` (Variant columns) are resolved per field: variant base, then catalog default, then the catalog-and-product override (`Spree::Catalogs::ResolveQuantityRules`, result `Spree::QuantityRule`) — the most specific level that states a rule wins. Steps count from the minimum: MOQ 48 / multiple 24 allows 48, 72, 96 and refuses 50; MOQ 50 / multiple 24 allows 50, 74, 98. Unrestricted variants read `1` / `1`.
- Per-currency order minimums: `adminClient.catalogs.orderMinimums.create(id, { currency: 'USD', amount: '600' })` (or `order_minimums` on create). Read overrides back with `catalogs.products.list(id, { expand: ['quantity_rule'] })`.
- Set per-product overrides as a whole set with `adminClient.catalogs.quantityRules.upsert(id, { terms: { prod_x: { minimum_order_quantity: 48, order_multiple: 24 } } })`. **A term for a product outside the assortment adds it to the assortment**, which switches an overlay catalog into restricting mode.
- Rules are enforced when items are added (`Carts::AddItem`, `UpsertItems`) and again at completion (requirement code `quantity_rule_violated`). The order minimum is an **advisory requirement** (`order_minimum_not_met`) that blocks completion. The cart exposes `order_minimum`, `order_minimum_shortfall` and `below_order_minimum`, and variants expose `minimum_order_quantity`, `order_multiple` and `purchase_unit`, so steppers can move in multiples.
- **Staff-keyed purchases are exempt** (admin drafts, carts with `created_by`), so negotiated exceptions can be recorded. Terms are read live and never stored. Placed orders are not re-validated.

### Catalog price lists: the rules

- Modes combine: `price_adjustment_percentage` (off the shop price), `price_adjustment_tiers` (`[{ min_quantity, percentage }]`), explicit `prices`, and `prices` with `min_quantity` (quantity breaks).
- **Quantity is per line** — ten of one SKU reaches a ten-unit break; five each of two SKUs doesn't.
- **A variant with breaks is priced by its breaks alone** — the catalog percentage doesn't stack on top.
- A break may never cost more than the quantity below it (save refused), and a variant carries at most ten breaks per currency on one list (`Spree::Price::MAXIMUM_BREAKS_PER_VARIANT`).
- Prices are never converted between currencies — state the agreement in every currency the buyer trades in.
- `CustomerGroupRule` / `UserRule` price rules keep working where already used but aren't offered for new lists — target audiences by assigning a catalog.

## Gated channels and the wholesale portal

`Spree::Channel#storefront_access` is one of `public` | `prices_hidden` | `login_required`. When unset, it inherits the store's `preferred_storefront_access`, and defaults to `public`. The **Store API** enforces it, so a storefront can't loosen it:
- `login_required` returns **401** for guest reads (auth, password reset and reference data are exempt).
- `prices_hidden` returns the catalog to guests with **every money field `null`**.
- `guest_checkout` is a separate channel setting.

Signed-in customers are never gated by `storefront_access`. Approving buyers is up to your app, for example by checking membership of a "Wholesale" customer group from `customers/me` → `customer_groups`.

Requests pick the channel with the `X-Spree-Channel` header, set through the SDK's `channel` option or `client.setChannel('wholesale')`, or with a channel-bound publishable key. Spree seeds a `wholesale` channel (`login_required`, with guest checkout off) and a channel-bound publishable key for it.

The Next.js storefront ships an opt-in `/wholesale` portal. Set `SPREE_WHOLESALE_CHANNEL=wholesale` to enable it; when unset, every `/wholesale` route returns 404. `SPREE_WHOLESALE_PUBLISHABLE_KEY` is optional. It uses a separate SDK client, cart cookie and cache keys per surface, with one shared customer JWT. Treat it as a reference implementation you can adapt, for example by gating the main channel for a login-first B2B store. See `spree-storefront`.

## PO numbers

- `po_number` is a plain indexed column on Cart and Order (`Spree::Purchase::PurchaseOrder`, which is *not* `Spree::PurchaseOrder`, the supplier procurement model with prefix `po_`). It's copied to the order at completion.
- Turn on `Spree::Company#po_number_required` for a company. Checkout then emits the requirement `{ step: 'address', field: 'po_number', code: 'po_number_required' }` until one is set: `client.carts.update(id, { po_number: 'PO-4471' })`. Staff-keyed orders are exempt.
- The optional **PO document** lives at `POST/GET/DELETE /api/v3/store/carts/:id/po_document`. It accepts PDF, images or Word files up to 10 MB, checked by content, stored privately and copied to the order. Admins can read it at `GET /admin/orders/:id/po_document`.

## Orders on account

Two ways to take a trade order now and collect later — no payment terms engine in OSS (net 30, credit limits, deposits are Enterprise roadmap):

- **Pay by invoice at checkout.** The built-in `Spree::PaymentMethod::Check` records a payment without contacting a provider; it succeeds at completion and waits as `pending` until staff capture it. Every active storefront-visible method is offered on every order, so to restrict invoice terms to company purchases subclass it:
  ```ruby
  # server/app/models/spree/payment_method/invoice.rb
  class Spree::PaymentMethod::Invoice < Spree::PaymentMethod::Check
    def available_for_order?(order) = super && order.b2b?
  end
  # server/config/initializers/spree.rb
  Rails.application.config.after_initialize { Spree.payment_methods << Spree::PaymentMethod::Invoice }
  ```
- **Staff-keyed draft orders.** `adminClient.orders.create({ customer_id, company_id, channel_id, currency, po_number, use_customer_default_address: true, items: [{ variant_id, quantity, price: '8.75' }] })`. `company_id` (create or update) makes it a company purchase with that company's catalog prices and tax. A `price` on an item is a negotiated line (`price_source: 'manual'`, never repriced; `price: null` returns it to catalog pricing) — only before placement; afterwards change money with fees/discounts. Then `adminClient.orders.complete(id, { payment_pending: true })` places it without processing payments (number assigned, stock allocated, `order.placed` fires, `payment_status` stays `none`). When the invoice is paid: `orders.payments.create(orderId, { payment_method_id, amount })` + `orders.payments.capture(orderId, paymentId)`. The dashboard's Complete action takes payment; `payment_pending` is API-only.

## Freight

- **Carton chain on the variant**: `carton_package_type_id` (a `PackageType` of `kind: 'carton'`), `units_per_carton`, `carton_weight`, `cartons_per_pallet`, and `purchase_unit` (`unit` or `carton`, which only changes how the storefront presents quantities). Stored quantities are always units. An `order_multiple` that straddles carton boundaries is rejected.
- The cart and rates expose **`freight_summary`** (`total_units`, `total_cartons`, `total_pallets`, `total_volume` in m³, `total_weight` in kg, and `complete`). When `complete: false`, some products fell back to unit dimensions, so show the figures as a minimum.
- Freight tiers are ordinary delivery methods using `rate_provider: 'Spree::DeliveryRateProvider::Freight'` with rules. `volume_rule` takes `minimum_volume` / `maximum_volume` in m³. `company_rule` takes `company_orders_only`: true means company orders only, and false means non-company orders only. The provider returns **unpriced rates** (`unpriced: true`, displayed as "Quoted after review", sorted last, never preselected). Checkout still completes, and the freight price is added once quoted. See `spree-fulfillment`.
- Extra charges such as handling or surcharges are `Spree::Fee` rows (always positive, taxable by default). See `spree-order-totals`.

## Gotchas

- **Adding one product to an overlay catalog** hides everything else. So does setting a quantity term for a product outside the assortment.
- **Assigning tier catalogs to customer groups for company buyers** has no effect, because the company chain answers first. Assign them to companies instead.
- **Forgetting `activate`**: a new catalog is inactive and does nothing.
- **Detaching a catalog's price list** soft-deletes it. Spree never frees it for rule matching.
- **Expecting a division to inherit its parent's VAT ID.** It uses the nearest company node, which may have none.
- **Expecting `prices_hidden` to hide prices from signed-in unapproved buyers.** It only gates guests, so approval is your app's job.
- **Validating MOQ only in the UI.** The API enforces it anyway, and staff paths skip it by design.
- **Company self-registration**, `approval_required` gating and company roles aren't in OSS. Don't build against them.

## Where to read further

- **`node_modules/@spree/docs/dist/developer/how-to/build-a-b2b-store.md`** — the end-to-end guide (https://spreecommerce.org/docs/developer/how-to/build-a-b2b-store)
- `node_modules/@spree/docs/dist/developer/core-concepts/{companies,catalogs,channels,freight,fees,customers}.md`
- `node_modules/@spree/docs/dist/developer/storefront/nextjs/wholesale.md`
- `node_modules/@spree/docs/dist/user/how-to/selling-to-businesses.md`: end-to-end setup of one trade customer
- https://spreecommerce.org/docs/developer/core-concepts/companies
- Related skills: `spree-pricing` (price lists, volume rules), `spree-checkout` (requirements registry), `spree-taxes`, `spree-fulfillment`, `spree-storefront`, `spree-auth-permissions`
