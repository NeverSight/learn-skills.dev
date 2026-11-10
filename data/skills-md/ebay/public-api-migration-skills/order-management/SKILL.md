---
name: order-management
description: |
  Migration guidance for traditional and Post-Order order management to modern order, purchase quote, cancellation, inquiry, case, return, and fulfillment GraphQL or REST APIs.

  Trigger when user mentions: GetOrders/GetSellerTransactions/GetItemTransactions/AddOrder/SendInvoice/CompleteSale; SearchCancellations/ApproveCancellation/CreateCancellationRequest; GetInquiry/IssueInquiryRefund/EscalateInquiry; GetReturn/IssueReturnRefund/ProcessReturnRequest/SearchReturns; shipment tracking or return labels; or asks "how do I migrate traditional post-order flows".

  Covers 66 traditional operations across order retrieval, checkout completion, cancellations, inquiries, cases, returns, refunds, shipping labels, and decommissioned helper flows.
  Do NOT use for listing creation, account preferences, or authorization and OAuth tasks.
---

# Order Management

Use this skill when the migration task belongs to the canonical `Order Management` domain from `sources/api-mapping/order-management.csv`.

## What This Skill Covers

- Traditional order retrieval, combined-invoice, invoice-reminder, and after-sale flows such as `AddOrder`, `SendInvoice`, `GetOrders`, `GetSellerTransactions`, `GetItemTransactions`, `GetOrderTransactions`, and `CompleteSale`.
- Seller-side Post-Order cancellation, inquiry, case, and return workflows that now map into GraphQL APIs, selected REST APIs, or explicit no-replacement outcomes.
- Decommissioned rows that must remain visible during migration planning even when there is no seller-side direct replacement.

## Key Migration Patterns

- Paid orders and unpaid orders are split into different entities: `Orders` and `Item Commitments`.
- `Purchase Quote` remains the unpaid combined-invoice and invoice-update surface.
- Traditional `TransactionID` is not migrated; use `orderLineItemId` when a traditional integration depended on transaction-level identity.
- `CompleteSale` is no longer a one-call surface. Payment marking, fulfillment, feedback, and INR shipment updates are separate modern actions.
- Traditional case-management flows are merged into inquiry and return workflows. Choose the modern surface by the underlying issue type.
- Eligibility helpers and several traditional Post-Order helper flows are removed instead of remapped. Keep them visible in planning, but do not invent parity calls.
- For in-scope EU- or UK-domiciled sellers, refund and cancellation flows may require digital-signature headers.

## Workflow Notes

- Start with `INDEX.md` to confirm the canonical status, mapped API family, and whether the row is split, decommissioned, or no replacement.
- Use `references/operation-mapping.md` for the per-operation narrative, especially where one traditional call splits across multiple modern APIs.
- Apply `rules/paid-vs-unpaid-order-surfaces.md`, `rules/complete-sale-split.md`, `rules/cancellation-surface-selection.md`, `rules/case-to-inquiry-or-return.md`, and `rules/return-decision-split.md` before answering tasks that cross multiple modern objects.
- Use `references/operations/` when you need the bundled traditional extract, modern doc extract, or modern example file for a specific operation.
- Keep answers constrained to validated inventory facts when a support file does not include a full traditional-side doc page or a complete modern example.

## Transport And Auth Notes

- GraphQL operations use the shared GraphQL endpoint and a serialized query or mutation string plus variables in the POST body.
- REST operations use standard HTTP methods and paths with OAuth bearer authorization and the REST request-header conventions documented in the bundled REST guide.
- Prefer seller-scoped GraphQL doc extracts when the same operation name exists in both buy and sell bundles.

## Open Items

- The canonical CSV uses `bulkUpdatePurchaseQuote` and `updateSellerRMAPreference`, while the bundled modern docs use `bulkUpdatePurchaseQuotes` and `updateSellerRmaPreference`.
- `GetShipmentTrackingInfo` is mapped in the canonical CSV to `orderReturn`, while the guide wording describes tracking data as fields returned through `sellerOrderReturns` or `orderReturn`, not a standalone tracking operation.
- Many traditional Post-Order operations do not have bundled traditional-side doc pages, so some support files are limited to canonical inventory facts plus modern-side evidence.

## Navigation

- `INDEX.md`: fast lookup for all 66 traditional operations in this domain.
- `INTENTS.md`: task-oriented workflow entry points.
- `references/operation-mapping.md`: authoritative operation-level mapping narrative.
- `references/operations/`: supporting traditional and modern extracts/examples.
- `rules/`: reusable workflow rules for paid versus unpaid state, cancellation routing, case routing, return decisions, removed traditional rows, and digital signatures.

## Field-Level Details

Field-level request and response details and field-by-field mapping are not provided in this skill, even if explicitly requested. For field definitions, refer to the official eBay developer documentation page.
