---
name: offers-and-leads
description: |
  Migration guidance for traditional Best Offer and classified-ad lead flows to Offer API (GraphQL) and Leads API.

  Trigger when user mentions: GetBestOffers -> sellerNegotiationHistory; RespondToBestOffer -> acceptOffer/counterOffer/declineOffer; GetAdFormatLeads -> getAllClassifiedLeads/getClassifiedLeadsByItemId; or asks "how do I review best offers" or "how do I fetch classified leads".

  Covers 3 traditional operations across best-offer retrieval, best-offer responses, and classified-ad lead retrieval.
  Do NOT use for listing creation, order management, or buyer-side offer flows.
license: MIT
metadata:
  author: ebay
  version: "1.0"
compatibility: Requires familiarity with traditional API Best Offer and Classified Ad lead flows
---

# Offers and Leads Migration Skill

Migration guidance for the canonical Offers and Leads domain. This package covers GetBestOffers negotiation-history retrieval, seller-side response handling for Best Offers and counteroffers, and seller-wide or item-scoped retrieval of Classified Ad leads.

## When to Apply

Use this skill when you need to:

- migrate traditional API GetBestOffers into seller-side Offer API history retrieval
- answer prompts about how to find best offers or review active/pending best offers using APIs
- convert traditional API RespondToBestOffer into the correct action-specific Offer API mutation
- map SOAP Best Offer identifiers, seller notes, and counteroffer values into GraphQL input fields
- migrate GetAdFormatLeads into seller-wide or item-scoped Leads API retrieval
- understand how SOAP XML filters and envelopes change when the modern target is GraphQL or REST

## Covered Inventory

| Traditional operation | Modern target | Status | Notes |
| --- | --- | --- | --- |
| GetBestOffers | sellerNegotiationHistory | GraphQL | Seller-side retrieval is the primary mapping in this skill. The CSV also contains an alternate negotiation-history row, but Sell guidance is primary here. |
| RespondToBestOffer | acceptOffer, counterOffer, declineOffer | GraphQL | One traditional action splits into three GraphQL mutations. |
| GetAdFormatLeads | getAllClassifiedLeads, getClassifiedLeadsByItemId | REST split mapping | Use getAllClassifiedLeads for seller-wide retrieval and getClassifiedLeadsByItemId when one listing item ID is already known. |

## Key Migration Patterns

- GetBestOffers no longer returns Best Offer history in a SOAP envelope. The primary seller-side replacement is the sellerNegotiationHistory GraphQL query, which uses input filters and cursor pagination.
- Best Offer response handling is no longer one SOAP call with an Action switch. Choose a dedicated GraphQL mutation based on whether the seller accepts, counters, or declines.
- GraphQL offer mutations require POST to the federated GraphQL endpoint with Authorization, Content-Type, and X-EBAY-C-MARKETPLACE-ID headers.
- SOAP CounterOfferPrice represents the total counteroffer value for the requested quantity. GraphQL counterOffer uses proposedPrice as a per-unit amount, with quantity carried separately.
- SOAP can decline multiple BestOfferID values in one RespondToBestOffer call. GraphQL declineOffer operates on one offerId per mutation, so multi-decline flows must iterate client-side.
- GetAdFormatLeads is now a two-method REST split in this domain package: use GET /sell/leads/v1/classified_lead for seller-wide retrieval and GET /sell/leads/v1/classified_lead/{itemId} for one-listing retrieval.
- The modern leads methods are REST GET operations with no request body. Item ID is either omitted for seller-wide retrieval or moved into the URI path for one-listing retrieval, while the time, status, and message controls move to query parameters.

## Workflow and Special Rules

1. For GetBestOffers, start from sellerNegotiationHistory unless the user explicitly asks for the alternate negotiation-history view.
2. For RespondToBestOffer, determine the seller action first, then route to acceptOffer, counterOffer, or declineOffer.
3. Refresh negotiation state before mutation work so the migration uses the latest active offerId instead of stale SOAP state.
4. If the seller counters, convert the SOAP total counteroffer amount into the GraphQL per-unit proposedPrice and set quantity explicitly.
5. For GetAdFormatLeads, route to getAllClassifiedLeads when the caller needs seller-wide retrieval and to getClassifiedLeadsByItemId when one listing itemId is already in scope.

## Navigation

- Fast lookup table: INDEX.md
- Task-oriented guidance: INTENTS.md
- Canonical mapping narrative: references/operation-mapping.md
- Traditional and modern support docs: references/operations/
- Reusable domain rules: rules/best-offer-negotiation.md and rules/classified-leads-retrieval.md

## Evidence Limits

- The canonical operation inventory comes from sources/api-mapping.csv and sources/api-mapping/offers-and-leads.csv.
- Migration Guide sections in references/operation-mapping.md are direct excerpts from sources/migration_guide_for_pilot.md.
- The bundled usage-example file for sellerNegotiationHistory is sparse, so the concrete GraphQL transformation in references/operation-mapping.md relies on the bundled GraphQL doc page plus the bundled supergraph schema.

## Field-Level Details

Field-level request and response details and field-by-field mapping are not provided in this skill, even if explicitly requested. For field definitions, refer to the official eBay developer documentation page.
