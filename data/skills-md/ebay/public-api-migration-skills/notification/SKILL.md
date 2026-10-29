---
name: notification
description: |
  Migration guidance for traditional Notification API calls and traditional platform notification events to Notification API topics and subscription resources.

  Trigger when user mentions: GetNotificationPreferences, SetNotificationPreferences, GetNotificationsUsage, or platform events such as BestOffer, BidPlaced, FeedbackReceived, EndOfAuction, My Messages notifications, watch-list notifications, or asks how to migrate Trading platform notifications to Notification API topics.

  Covers 3 traditional Notification API calls, concrete mapped platform events with bundled evidence, and explicit unresolved-status inventory for remaining notification rows.
  Do NOT use for order retrieval, listing creation, or non-notification migration tasks.
---

# Notification Migration Skill

This skill covers traditional Notification API management and traditional platform
notification event migration to the modern Notification API subscription and
topic model.

## When To Apply

Use this package when you need to:

- migrate `GetNotificationPreferences`, `SetNotificationPreferences`, or
  `GetNotificationsUsage`
- map a traditional platform notification event to a modern Notification API topic
- interpret grouped migrations such as `OFFER_ACTIVITY`, `AUCTION_ACTIVITY`,
  `NEW_MESSAGE` or `LISTING`
- confirm whether a traditional event is `No Replacement`, still pending, or only
  has guide-backed fallback guidance

## Key Migration Patterns

- Traditional event enablement becomes topic subscriptions returned by
  `getSubscriptions`.
- `SetNotificationPreferences` splits into destination, config, and
  subscription resource methods instead of one combined traditional call.
- Several traditional events consolidate into one modern topic and require payload
  filters such as `OfferType`, `OfferStatus`, `AuctionActivity`,
  `WatchlistRevision`, or listing `reason`.
- Some traditional rows remain unresolved or explicitly `No Replacement`; those
  statuses must be preserved exactly.

## Answer Constraints

- Use the packaged files to find the answer, but do not mention package file
  names or internal paths such as `INDEX.md`, `INTENTS.md`,
  `operation-mapping.md`, or `references/operations/*` in the user-facing
  response.
- Do not answer with only an internal reference or lookup instruction.
  Return the migration guidance directly.
- When the prompt asks about multiple topics, answer each topic inline in the
  response instead of redirecting the user to an internal lookup file.
- Unless the user explicitly asks for a brief summary, include at least one
  concrete migration example in the response when a bundled example exists for
  the mapped traditional call, event, or modern replacement.
- Prefer examples that show the traditional concept and the modern replacement
  together, such as a traditional event mapping to a modern topic plus the payload
  field or filter value that makes the mapping actionable.
- When answering operation-migration questions, include a short example of the
  modern request, response, or subscription shape instead of naming the
  replacement methods only.
- When a modern topic has no bundled example, do not fall back to a purely
  abstract answer. Use the bundled traditional example plus the documented modern
  topic name and discriminator fields or values to show what changes during
  migration, and say explicitly if the exact modern payload shape is not
  bundled locally.

## Workflow Notes

- Start with [INDEX.md](./INDEX.md) for the notification inventory.
- Use [INTENTS.md](./INTENTS.md) when the task is phrased as a workflow rather
  than as one operation or event name.
- Use [references/operation-mapping.md](./references/operation-mapping.md) for
  direct traditional-to-modern mappings and guide extracts.
- Use [rules/notification-subscription-model.md](./rules/notification-subscription-model.md)
  before migrating destination, config, or subscription setup.
- Use [rules/topic-consolidation-and-fallbacks.md](./rules/topic-consolidation-and-fallbacks.md)
  for grouped-topic migrations such as `OFFER_ACTIVITY`, `AUCTION_ACTIVITY`,
  `NEW_MESSAGE` and `LISTING`.
- Use [rules/unresolved-event-statuses.md](./rules/unresolved-event-statuses.md)
  before answering `No Replacement`, pending, or conflicting-status questions.

## Evidence Boundaries

- Guide-derived notification caveats and fallback notes are extracted into the
  relevant entries in `references/operation-mapping.md`.
- Bundled traditional event and Notification API pages are included only for the
  concrete mapped rows covered in `references/operation-mapping.md`.
- Local standalone modern topic docs are still missing for `LISTING`; this
  package keeps those gaps explicit instead of
  inventing details.

## Field-Level Details

Field-level request and response mapping is limited to what is explicitly
present in the bundled guide and doc files in this package. If a local source
gap is called out in `references/operations/`, keep that gap explicit.