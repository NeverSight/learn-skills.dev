---
name: flutter-observability
description: Design, implement, or repair production observability in Flutter using operational logs, error and crash capture, breadcrumbs, traces, release context, privacy controls, and verification. Use for diagnosability and incident signals; not product analytics, profiling-only optimization, or a general code review.
---

# Flutter Observability

Make production failures diagnosable without collecting unnecessary user data. Preserve an existing Sentry, Crashlytics, OpenTelemetry, Dynatrace, Datadog, or other telemetry stack unless the user requests a migration.

## Preflight

Read SDK constraints, entrypoints, flavors/environments, and the complete existing telemetry and delivery wiring before diagnosing a cause or prescribing changes: SDK initialization, error hooks, consent/privacy rules, network and navigation instrumentation, isolate usage, obfuscation, symbol retention/upload, CI, and release identity. Do not infer the root cause from dashboard symptoms alone. When repository or backend evidence is unavailable, lead with the exact artifacts and backend evidence still required, state that diagnosis remains pending, and keep any remediation conditional. Start from a concrete diagnostic question or incident; do not instrument every event by default.

Define a small operational event contract: stable event name, severity, timestamp, release/build, environment, platform, correlation identifier, outcome, duration where meaningful, and a bounded set of redacted attributes. Keep user content, tokens, credentials, payment data, and raw request/response bodies out of telemetry.

Every instrumentation plan must explicitly cover all five governance controls: redaction, consent, sampling, backend retention/access, and bounded offline buffering. State which controls live in client code and which must be verified in the backend; do not imply client configuration alone enforces retention or access.

## Route the work

- For framework, root-isolate, child-isolate, and async error coverage, read [error and crash capture](references/error-and-crash-capture.md).
- For structured logs, breadcrumbs, traces, correlation, sampling, redaction, and consent, read [logging, tracing, and privacy](references/logging-tracing-privacy.md).
- For choosing or preserving a vendor, release metadata, symbols, buffering, and end-to-end proof, read [vendor and verification](references/vendor-and-verification.md).

Load only the references relevant to the request.

## Boundaries

- `flutter-performance` owns profile-mode measurement and optimization decisions; production traces can reveal a regression or candidate bottleneck but are not proof of an optimization.
- `flutter-product-analytics` owns funnels, attribution, conversion, experiments, and business events; operational telemetry answers reliability and incident-diagnosis questions. State this distinction when instrumenting a user journey so analytics events or UI tracking do not leak into the operational contract.
- `flutter-networking` owns HTTP behavior; this skill defines safe correlation and outcome signals around it.
- `flutter-security` owns a broad security review; this skill enforces telemetry minimization, redaction, consent, retention awareness, and least exposure.
- `flutter-build-release` owns artifact and symbol production; this skill verifies release/build identifiers and symbol upload linkage.

## Verification

Test normalization, redaction, sampling, consent, correlation, and adapter behavior. Exercise a handled error and each required controlled unhandled-error class in a non-production backend/environment, then confirm ingestion exactly once, expected release/build/environment, usable symbolicated stack, and safe attributes in the actual dashboard or query surface. Confirm secrets and disallowed personal data are absent. Verify degraded behavior when telemetry is offline, rate-limited, or unavailable.

Do not claim observability works because initialization compiled. State which signals were observed end to end, which were only unit-tested, and what remains vendor- or device-blocked.

## Sources

- [Handling errors in Flutter](https://docs.flutter.dev/testing/errors)
- [PlatformDispatcher.onError](https://api.flutter.dev/flutter/dart-ui/PlatformDispatcher/onError.html)
- [Dart developer log](https://api.dart.dev/dart-developer/log.html)
