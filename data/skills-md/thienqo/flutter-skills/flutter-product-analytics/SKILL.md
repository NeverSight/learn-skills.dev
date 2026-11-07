---
name: flutter-product-analytics
description: Design, implement, repair, or review product analytics in Flutter using event contracts, identity, consent, funnels, attribution, experiment exposure, delivery semantics, and backend verification. Use for measuring user behavior and business outcomes; not operational logs, crash reporting, profiling, or general UI tracking.
---

# Flutter Product Analytics

Instrument decisions, not widgets. Begin with a product question and a stable event contract, then preserve the project's analytics provider, consent platform, state management, navigation, and data architecture unless migration is requested.

Do not add a vendor, create dashboards, enable collection, or change live retention and consent configuration merely because the skill is selected.

## Preflight

Read `pubspec.yaml`, SDK constraints, current analytics adapters and initialization, environments, consent and privacy controls, event definitions, identity lifecycle, navigation tracking, offline buffering, backend transformations, tests, dashboards or schemas in scope, and release configuration. Identify the question, decision, owner, population, and success definition before adding an event.

Each event needs a semantic trigger, stable name, bounded typed properties, identity and consent policy, delivery expectation, and verification plan. Emit once for the domain occurrence—not from widget `build`, incidental rebuilds, route observers, and button callbacks simultaneously.

When proposing or repairing an event, state the contract instead of asking or deferring to the adapter: which identity is attached (anonymous or authenticated, and what happens on login or account switch), whether consent off drops or queues the event, the delivery semantics (for example at-least-once with a dedupe key), and the rule for retries and process restarts. Where the project does not say, choose the conservative default, label it an assumption, and name who can change it.

## Load references conditionally

- Read [event contracts and ownership](references/event-contracts-and-ownership.md) when defining names, properties, semantic triggers, funnels, revenue events, schema evolution, or duplicate prevention.
- Read [identity, consent, and privacy](references/identity-consent-and-privacy.md) for anonymous and authenticated identity, account switching, opt-in or opt-out, deletion, sensitive data, advertising attribution, and offline buffering.
- Read [verification and experiments](references/verification-and-experiments.md) for DebugView or live-debug tools, backend inspection, environments, funnel validation, experiment exposure, and rollout evidence.

## Boundaries

- `flutter-observability` owns operational errors, logs, traces, release context, and incident diagnosis. Product analytics owns user behavior, funnels, attribution, conversion, and experiments.
- `flutter-in-app-purchases` owns verified transactions and entitlements; analytics may observe their outcomes but never grants access or defines purchase truth.
- `flutter-navigation` owns route correctness; analytics maps meaningful screen or journey semantics without coupling navigation to a vendor.
- `flutter-authentication` owns session state; analytics follows its explicit identity and account lifecycle.
- `flutter-persistence` owns storage mechanics; this skill defines consent-aware bounded buffering and event deletion requirements.
- `flutter-security` owns broad privacy and threat review.

## Verification

Test the provider-neutral adapter and semantic producers deterministically. Cover exact-once emission, property validation, consent transitions, anonymous-to-authenticated identity, logout and account switch, offline queue bounds, retry duplicates, environment separation, and provider failure.

Use an authorized non-production analytics project or debug surface to confirm the event arrives once with the expected name, properties, identity, timestamp, consent state, and environment. Verify the downstream schema, funnel, or experiment consumer when it is part of the task. A successful SDK call or console log is not end-to-end analytics evidence.

When authorized provider or dashboard access is unavailable, explicitly record provider ingestion and each downstream dashboard, funnel, or experiment boundary as unverified because it was not observed. Do not collapse that evidence gap into a generic “pending” status.

## Sources

- [Google Analytics events for Flutter](https://firebase.google.com/docs/analytics/flutter/events)
- [Google Analytics DebugView](https://firebase.google.com/docs/analytics/debugview)
- [Apple user privacy and data use](https://developer.apple.com/app-store/user-privacy-and-data-use/)
- [Google Play user data policy](https://support.google.com/googleplay/android-developer/answer/10144311)
