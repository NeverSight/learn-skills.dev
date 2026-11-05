---
name: flutter-in-app-purchases
description: Implement, repair, or review Flutter purchases of digital goods and subscriptions through app stores, including catalog, transaction updates, verification, entitlements, acknowledgement, consumption, restoration, and sandbox testing. Use for App Store or Google Play billing; not physical-goods checkout, advertising, or generic payment forms.
---

# Flutter In-App Purchases

Model store billing as an asynchronous reconciliation system, not a button callback. Preserve the project's current store package, subscription service, backend, account model, and state management unless migration is explicitly requested.

Do not create products, change pricing, upload builds, or mutate live store configuration without explicit authorization.

## Preflight

Read `pubspec.yaml`, SDK constraints, supported platforms, store package and native configuration, product identifiers, purchase listener ownership, entitlement source of truth, backend verification, authentication, persistence, tests, flavors, and sandbox setup. Distinguish consumables, non-consumables, and subscriptions before editing the flow.

Keep three concepts separate:

- Store catalog: products, localized price, availability, offers, and store metadata.
- Transaction: pending, purchased, restored, cancelled, failed, consumed, acknowledged, or finished as supported by the store.
- Entitlement: the product capability the application currently grants to an account or device.

Never grant an entitlement from a button tap, client assertion, unverified payload, or pending transaction. Process verified completed transactions idempotently, then perform the store-required acknowledgement, consumption, or finish step exactly as the product type requires.

## Load references conditionally

- Read [purchase lifecycle and entitlements](references/purchase-lifecycle-and-entitlements.md) for listener ownership, verification, idempotency, pending transactions, acknowledgement, consumption, and account attribution.
- Read [subscriptions and restoration](references/subscriptions-and-restoration.md) for renewals, grace and hold states, expiration, restore or reconcile flows, upgrades, downgrades, and account switching.
- Read [store testing and release](references/store-testing-and-release.md) for sandbox accounts, product readiness, interrupted flows, platform matrices, and release evidence.

## Boundaries

- `flutter-authentication` owns account sign-in and session lifecycle; this skill binds verified transactions to the correct account and prevents entitlement leakage during account switching.
- `flutter-networking` owns generic transport; this skill owns store and entitlement protocol semantics.
- `flutter-persistence` owns durable local storage; cached entitlement state must expose freshness and never override authoritative revocation.
- `flutter-security` owns broad threat review; this skill requires trusted verification and minimizes purchase-token exposure.
- `flutter-product-analytics` may observe purchase funnel events but must not become the entitlement source of truth.
- `flutter-build-release` owns signed application artifacts and uploads. Store publication remains an explicit external action.

## Verification

Use fakes for deterministic state-machine tests and store sandbox or test tracks for end-to-end evidence. Cover success, cancellation, failure, pending completion after restart, duplicates, delivery-before-acknowledgement recovery, restore, account switching, offline reconciliation, subscription state changes, and unavailable products.

For sandbox-readiness work, do not stop at a scenario checklist. Explicitly require inspection of application and bundle identifiers, flavors and environments, Android and Apple signing, entitlements or manifests, existing store products, test accounts, and backend routing before changing configuration. Provide concrete reproducible cases with preconditions, actions and interruption point, expected store and entitlement states, acknowledgement or finish outcome, and observable pass/fail evidence. Include at least one interrupted purchase and one restore or reconciliation case when those flows are in scope.

State which store, product type, account mode, platform, and backend path were exercised. A successful purchase sheet or client callback alone does not prove verification, entitlement delivery, acknowledgement, cross-device restoration, or renewal handling.

## Sources

- [Flutter in-app purchases overview](https://docs.flutter.dev/resources/in-app-purchases-overview)
- [Google Play Billing integration](https://developer.android.com/google/play/billing/integrate)
- [Google Play backend integration](https://developer.android.com/google/play/billing/backend)
- [Apple In-App Purchase](https://developer.apple.com/documentation/storekit/in-app-purchase)
