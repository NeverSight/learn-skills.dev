---
name: swell-backend-api
description: "Use this skill for Swell Backend API operations: querying and aggregation, writes, imports, batch requests and transactions, orders, payments, refunds and subscriptions, products and inventory, accounts, coupons, promotions and gift cards, files, events and webhooks, errors and rate limits. Use it whenever a Backend API request is written or debugged, including `swell api get|post|put|delete` CLI commands and their query parameters. Applies inside Swell apps through function and workflow clients or the Apps SDK Backend client, and to independent integrations using swell-node, explicitly configured Apps SDK clients or direct HTTP. Pair with swell-app for app packaging, runtime setup, models, triggers, permissions and deployment; reuse the client that runtime supplies. Shopper-session operations belong to swell-frontend-api. Proxima / Liquid theme authoring and other platforms are outside scope."
allowed-tools: Read, Grep, Glob, Bash
---

# I. Scope & Authentication

This skill owns Backend API operations in both Swell apps and independent integrations. `swell-app` owns app scaffolding, runtime context, resource declarations, permissions and deployment. Use both when an app performs Backend operations. Shopper-session operations belong to `swell-frontend-api`.

**Inside an app, use the client the runtime supplies** — a function's or a workflow's `req.swell`, or the frontend's Backend client — and do not construct a second one beside it. `swell-app` says how to obtain each and how it reports failures.

The Backend API provides privileged store operations within the caller's credential scope; it does not apply shopper-session ownership. For standalone secret-key HTTP access, use `https://api.swell.store`, HTTP Basic auth with the store ID as username and the secret key as password:

```bash
curl https://api.swell.store/products -u my-store:sk_test_...
```

Keys live in the dashboard under Developer > API keys. The key alone selects the environment, and its prefix is the only visible marker: a **live** secret key is a bare `sk_` plus 32 random characters, a test key is `sk_test_…`, and a key minted in a custom environment carries that environment's slug (`sk_staging_…`). **There is no `sk_live_` prefix** — no environment segment means live, so a guard that greps for `sk_live_` never matches a real key. Public keys follow the same rule (`pk_…` / `pk_test_…`). Environments are not a test/live binary: a store can create arbitrarily named ones. There is no environment header or parameter — mint a key in the environment you target. Secret keys must never reach browsers, storefront bundles, or client-visible config; anything customer-facing belongs on the Frontend API (swell-frontend-api skill).

Outside an app, the client follows from where the code runs:

- **swell-node** (version 6 or later) for a Node.js server or script. Calls resolve with the response body itself — the record or the list envelope, with no wrapper to unpack.

  ```js
  const { swell } = require('swell-node');
  swell.init('my-store', process.env.SWELL_SECRET_KEY);
  const products = await swell.get('/products', { limit: 25, active: true });
  ```

- **Apps SDK `SwellBackendAPI`** for a runtime swell-node does not support, such as an edge runtime: `new SwellBackendAPI({ storeId, secretKey, apiHost: 'https://api.swell.store' })`. Install `@swell/apps-sdk@next`; the `latest` tag is the 1.x theme SDK, a different API.
- **Direct HTTP** from any other language, with JSON bodies. A query goes in the URL in bracket notation (`?where[active]=true&limit=25`) or as a JSON body on the `GET`.
- **`swell api get|post|put|delete '<path>'`** for a one-off look or change from a terminal, as the logged-in CLI user. It targets the **test** environment unless `--live` is passed, so a command that looks like it read or changed the live store did neither.

The clients send the same paths, queries and bodies, so the references give a write as its method, path and body — `PUT /orders/<id>` with `{ canceled: true }` — for whichever client sends it. Queries and examples of several steps are JavaScript in which `swell` stands for that client: `swell.get(path, query)`, and `swell.post`, `put` and `delete(path, body)`. The clients differ in how a failure reaches the code: see "Errors, Rate Limits, Retries".

# II. Data Model & Discovery

Swell is schema-driven: every collection (standard and custom) is described by a live model definition. Discover instead of guessing:

- `GET /:models` — list model definitions; `GET /:models/<name>` — full definition with `fields` (types, required, enums, formulas, links), `events`, and query defaults. It is the authoritative field reference for this store, with what apps and the merchant added.
- The name is not always the collection's path. A collection under `content/` is `/:models/content_<name>`, and an app's collection is `/:models/app_<app_id>.<collection>`; the bare name can answer with another model of the same name. A child collection has no definition of its own: it is described on its field in the parent (`fields.addresses` of `accounts`).
- Custom models and fields are made in the dashboard (Developer > Models) or by an app (`swell-app`).

Paths:

| Records | Path |
| --- | --- |
| A standard collection | `/products`, `/products/<id>` |
| A child collection | `/products/<id>/variants` under one parent, `/products:variants` across all parents |
| An app's collection | `/apps/<app_id>/<collection>`, with its children at `/apps/<app_id>/<collection>/<id>/<child>` and `/apps/<app_id>/<collection>:<child>` |
| A child collection an app adds to a standard model | `/products:apps.<app_id>.<name>` |

An app's own function and frontend clients also reach its collections by the short path, `/<collection>`, in a transaction's operations too. An app's fields on a standard record are under `$app.<app_id>` in the record.

`<app_id>` is the `id` in the app's `swell.json`. The app's record id, 24 hexadecimal characters, which events carry, works in its place.

Records address by `id`, and many collections also by a secondary field usable in the URL: products/categories/pages/`content/blogs`/`content/blog-categories` → `slug`, orders/carts/invoices/payments/shipments/returns/subscriptions → `number`, accounts/contacts → `email`, gift cards and `coupons:codes` → `code`, coupons/promotions/purchase links → `name`. The lookup is generic, not a fixed list — read `secondary_field` on any model's `/:models/<name>` definition.

A read by id answers with the record, and a list with an envelope that `references/querying.md` describes. Fields are snake_case; dates are ISO-8601 strings.

The commerce object graph in one pass: **products** (with `variants`, options, `purchase_options` for subscriptions, `bundle_items`, stock) are organized by **categories** and **attributes**; **accounts** own `addresses`, `cards`, `credits`; **carts** convert into **orders**, which connect to **payments** (and their **refunds**), **shipments**, **returns**, and **invoices**; **subscriptions** bill on a schedule, generating invoices and optionally orders; **coupons**, **promotions**, and **gift cards** apply discounts and stored value; **content** and **pages** hold structured content; **purchaselinks** define shareable pre-built carts.

Read `references/files-media.md` before uploading or serving images and files — the `/:files` collection, the `file` field type, and the base64 wire formats.

# III. Querying

Read `references/querying.md` before writing any read beyond a get by id: filters, sorting and paging, counting, search, `expand` and `include`, aggregation, and localized or multi-currency values. A query returns at most 1000 records, so reading a whole collection is a loop.

# IV. Writing

Read `references/writes.md` before any write. Four of its rules change a design:

- **An update merges.** Sending a shorter array does not replace the stored one; replacing takes an operator.
- **Nothing can be undone**, and a delete is permanent.
- **Every write sets off the store's webhooks, app functions and notification emails.** The reference says what an import can switch off.
- **A batch is not atomic, and a transaction only partly:** a write that fails validation inside a transaction does not roll the others back.

The reference also covers the update operators, child records, imports that keep their ids, and localized and per-currency values.

# V. Events & Webhooks

Read `references/events-webhooks.md` before reacting to store activity. Four of its rules change a design:

- **An event is a notice, not the record.** Most events carry the record's id and little else, so read the record before acting.
- **Not every change records an `updated` event.** A payment that settles an order records `order.paid` and no `order.updated`.
- **A webhook created through the API is off** until `enabled: true` is sent.
- **A webhook request is signed**: verify it before acting. It can arrive twice or out of order.

The reference also covers the event log and type names, the forms of a webhook's event entries, retries and automatic disabling, reading delivery rows, and reading `/events` in place of a webhook.

# VI. Commerce Lifecycles

Read `references/orders-payments.md` before scripting orders, shipments, payments, refunds, returns, invoices or subscriptions. Five of its rules change a design:

- **State is derived.** `status`, `paid` and `delivered` are read-only: code writes a flag or creates a payment, a shipment or a refund.
- **Creating an order or a subscription takes money in the same request.** An order that is not a draft spends the customer's account credit and charges its billing method, and a subscription without a trial charges its first period.
- **Canceling refunds nothing, and a return moves no money.** A refund is its own write.
- **Nothing checks a payment, a shipment or a return against the order.** Amounts and quantities above what the order has are accepted.
- **`paid` stays true after a refund.** `payment_balance` is what is owed.

Read `references/products-inventory.md` before scripting products, variants or inventory: variants are generated from options, and stock is a ledger of adjustments that a product must opt into.

Read `references/accounts.md` before scripting accounts: deleting an account with history is refused.

Read `references/promotions-discounts.md` before scripting coupons, promotions, gift cards or purchase links: a cart or an order written through this API gets no promotions unless the write asks for them.

# VII. Errors, Rate Limits, Retries

The API answers a failed call in one of three ways, and the clients do not hand them to the code the same way.

- **A missing record is not an error.** A `GET` or `DELETE` for an id that does not exist answers with status 200 and an empty body, which swell-node and the SDK resolve as an empty value: test `if (!record)`.
- **A refused write is not an HTTP error.** A `POST`, `PUT` or `DELETE` that fails field validation writes nothing and answers `{ errors: { <field>: { code, message } } }`. Keys are dotted paths for nested fields (`items.0.quantity`), and detail values sit on the entry itself: `MINVAL` carries `min`, `ENUM` carries `values`.
- **Everything else is an HTTP error.** 401 is a wrong store id or a bad or revoked key, and 402 a canceled plan or an expired trial. The body is plain text, or `{ error: { code, message, status } }` for an error with a code.

| Client | Refused write | HTTP error |
| --- | --- | --- |
| swell-node | **Resolves** with `{ errors }`. Check `result.errors` after every write, or the script reports success while writing nothing | Throws. Branch on `err.status`; `err.code` is the HTTP status text, not the platform's code, and the API's body is at `err.cause.response.data` |
| Apps SDK Backend client | **Throws** a `SwellError` with status 400 and the field map as `err.body` | Throws a `SwellError` with `status`, `code` and `body` |
| Direct HTTP | Status 200 with an `errors` key in the body | The status and the body |

The clients inside an app differ among themselves in other ways; `swell-app` states each contract. Results of a batch or a transaction are per operation: `references/writes.md`.

**Rate limits** apply per store and per environment, to both throughput and concurrency. The figures depend on the plan and are not published; a test environment always has the lower tier. Requests over the limit are queued, not rejected, so a 429 means a request waited more than 60 seconds: the load is sustained, not a spike. Back off with increasing delays, spread bulk work over time, and make each request lighter — every `expand` level and `include` adds to a request's weight. There are no rate-limit response headers to read.

**Retries.** No client repeats a request the API answered with an error. Retry a 429 and a transaction's 409 in your own code, with increasing delays, and do not retry a 400, 401, 403 or 404.

# VIII. Operating Guardrails

Point scripts at the test environment (`sk_test_…`) first; run bulk updates against test records before live. Before any bulk write, print the loaded key's prefix and confirm the environment segment — a bare `sk_` is **live**, not test.
