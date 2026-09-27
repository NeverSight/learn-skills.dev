---
name: connector-quickbooks
description: >-
  Use the `quickbooks-client` mops package whenever the user asks the canister
  to create/read/update invoices, customers, payments, items, or chart-of-account
  entries in QuickBooks Online (QBO), email an invoice, or run a QuickBooks query.
  The package wraps the QuickBooks Online Accounting API v3 at
  `https://quickbooks.api.intuit.com` via outbound HTTPS calls.
version: 0.2.0
caffeineai-subscription: [none]
compatibility:
  mops:
    quickbooks-client: "~0.2.0"
---

# quickbooks-client

Motoko bindings for a curated slice of the [QuickBooks Online Accounting API
v3](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account):
**Customer, Invoice, Payment, Item, Account**. Schemas were transcribed from
Intuit's official XSD. All 12 operations live in `Apis/DefaultApi.mo`:
`saveCustomer`/`getCustomer`, `saveItem`/`getItem`, `saveAccount`/`getAccount`,
`saveInvoice`/`getInvoice`/`sendInvoice`, `savePayment`/`getPayment`, and `query_`
(trailing underscore — `query` is a reserved word in Motoko).

## Trigger phrases

Reach for this skill on any request mentioning: QuickBooks, QBO, invoice,
"bill a customer", "send an invoice", record/receive a payment, customer,
accounting, bookkeeping, chart of accounts, item/product/service,
"sync to QuickBooks".

**Not in this slice:** Estimate, Bill, Vendor, PurchaseOrder, CreditMemo and the
rest of the QBO entity set — the spec is hand-curated to Customer, Invoice,
Payment, Item and Account. If a request needs one of the others, say so rather
than mapping it onto Invoice; the spec has to be re-spun from Intuit's XSD
first.

## How QuickBooks authentication works (read before wiring)

QBO uses **OAuth 2.0 Authorization Code** — there is no static API key. Each
end-user authorises their QuickBooks company; the app exchanges the authorization
code for a short-lived **Bearer access token** (~1 hour) and passes it to the
client at call time. On expiry the API returns HTTP 401 — surface a
`#Err("auth_expired")` result and re-authenticate off-chain.

Two identifiers travel with every call:
- **`realmId`** — the QuickBooks *company id*, obtained during the OAuth handshake.
  It is the first argument to every operation.
- **`minorversion`** — the API minor version (default `"75"`); pass `""` to omit
  and use the account default.

**The token exchange is itself an on-chain outcall** to Intuit's token endpoint
and needs the app's **Client Secret**. Two hazards (identical to the googlemail
connector):
- **`is_replicated = ?false` on the exchange too** — the token response is
  non-deterministic, so a replicated exchange duplicates across ~13 replicas and
  fails IC consensus.
- **The Client Secret leaks with exported source** — Caffeine can export the app
  to a `.zip` or public GitHub repo, carrying the secret along. Scope it minimally
  and rotate if the source is shared.

Persist the per-user refresh/session token across upgrades (stable memory) so a
redeploy doesn't force re-authentication. OAuth scope: `com.intuit.quickbooks.accounting`.

## Create vs. update vs. delete (important QBO semantics)

- **Create and update BOTH use the `save<Entity>` (POST) operation.** It's an
  *update* when the body carries the entity's `Id` **and** current `SyncToken`
  (fetch them first via `get<Entity>`); set `sparse = ?true` for a partial update.
  Without `Id`/`SyncToken` it's a create.
- **Delete** (transactions only — `Invoice`, `Payment`): call `saveInvoice` /
  `savePayment` with `operation = ?#delete` and a body carrying `Id` + `SyncToken`.
  The `operation` argument is **optional** (`?SaveInvoiceOperationParameter`),
  not a bare variant. Pass **`null` for a normal create or update** — the client
  then omits the query parameter entirely, which is what QBO wants; the spec
  says "Omit for create/update; 'delete' removes the invoice". Only `?#delete`
  is routinely needed. Name-list entities
  (`Customer`, `Item`, `Account`) are **not deletable** — set `Active = ?false`
  to deactivate instead (their `save*` ops take no `operation` argument).
- **Responses are wrapped**: `getCustomer` returns `CustomerResponse` with a
  `Customer` field (and a `time`); same shape per entity. `query_` returns a
  `QueryResponse` whose `QueryResponse` field holds arrays per entity type.
  The operation is `query_`, not `query`.
- **Invoice lines and Payment lines are different types.** `Invoice.Line` is
  `[Line]`, where `DetailType` is **required**. `Payment.Line` is
  `[PaymentLine]` — `{Amount, LinkedTxn, …}` with **no** `DetailType`, which is
  what Intuit actually sends when a payment is applied to invoices. They were
  one shared type until 0.2.0, and that made every payment response fail to
  decode.

## Frontend surfaces (two pages)

Like any per-user OAuth connector, an app needs **two** surfaces:
- An **admin-gated Intuit app configuration page** — the **Client ID** and
  **Client Secret** are canister-wide, set once by an admin; never expose the
  Client Secret to ordinary users.
- A **per-user OAuth 2.0 handshake page** — each user connects their own
  QuickBooks company (yielding their `realmId` + token); re-prompt on HTTP 401.

## Usage

```mo:quickbooks-client
import { saveInvoice; getInvoice; sendInvoice; saveCustomer }
  "mo:quickbooks-client/Apis/DefaultApi";
import Invoice "mo:quickbooks-client/Models/Invoice";
import { defaultConfig } "mo:quickbooks-client/Config";

let cfg = {
  defaultConfig with
    auth          = ?#bearer "<off-chain OAuth2 access token>";
    is_replicated = ?false;  // non-replicated: required for writes; reads too
};
let realmId = "<company id from OAuth handshake>";

// Build an invoice: one sales line, $100, item "1", billed to customer "58".
// Invoice has no required fields → init {} then record-update the optionals.
// NOTE: DetailType is REQUIRED on a Line, and its variants are lowercase.
let inv = {
  Invoice.init {} with
    CustomerRef = ?{ value = "58"; name = null };
    Line = ?[ {
      DetailType          = #salesitemlinedetail;   // required; lowercase variant
      Amount              = ?100.0;
      Description         = ?"Consulting";
      SalesItemLineDetail = ?{ ItemRef = ?{ value = "1"; name = null };
                               Qty = ?1.0; UnitPrice = ?100.0; TaxCodeRef = null; ServiceDate = null };
      Id = null; LineNum = null; LinkedTxn = null;
    } ];
};
// saveInvoice(config, realmId, invoice, minorversion, operation)
// `operation` is optional: null omits it — the create/update path.
let created = await* saveInvoice(cfg, realmId, inv, "75", null);
// Email it to the customer (config, realmId, invoiceId, sendTo, minorversion):
// ignore await* sendInvoice(cfg, realmId, "<invoiceId>", "cust@example.com", "75");
```

## Notes

- **Use `is_replicated = ?false` for writes** (`save*`, `sendInvoice`, delete via
  `operation = ?#delete`). These outcalls are non-idempotent and QBO's response is
  non-deterministic; in replicated mode every replica issues the request — creating
  duplicate invoices/payments and failing IC consensus. Reads (`get*`, `query_`)
  also use `?false` (one node, ~13× cheaper).
- **Update needs a fresh `SyncToken`** — always `get<Entity>` first, copy its
  `SyncToken` into the body, then `save<Entity>`. A stale token → HTTP 400
  ("stale object").
- `minorversion` defaults to `"75"`; pass `""` to omit.
- QBO returns errors as an `ErrorResponse` whose list field is `Fault.Error_` —
  note the trailing underscore, `Error` being reserved — so surface
  `Fault.Error_[0].Message` to the caller; never blind-retry a write.
- Sandbox vs production: point the client host at
  `sandbox-quickbooks.api.intuit.com` for the Intuit sandbox company during
  development (edit the server in `Config`), and `quickbooks.api.intuit.com` for
  production.
