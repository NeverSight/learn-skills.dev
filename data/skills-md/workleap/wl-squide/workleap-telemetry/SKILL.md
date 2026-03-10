---
name: workleap-telemetry
description: |
  Guide for @workleap/telemetry, Workleap's unified telemetry connecting Honeycomb, LogRocket, and Mixpanel with automatic correlation IDs.

  Use this skill when:
  (1) Initializing wl-telemetry in a frontend application
  (2) Correlation values (Telemetry Id, Device Id) and cross-tool data correlation
  (3) Honeycomb tracing, OpenTelemetry spans, and performance monitoring
  (4) LogRocket session replay, user identification, and privacy controls
  (5) Mixpanel analytics, event tracking, and cross-product tracking
  (6) Configuring wl-telemetry diagnostic loggers (LogRocketLogger)
  (7) Storybook/test setup with Noop telemetry clients
  (8) Reviewing or troubleshooting telemetry instrumentation
metadata:
  version: 3.2
---

# Workleap Telemetry (wl-telemetry)

`@workleap/telemetry` is an umbrella package that integrates Honeycomb, LogRocket, and Mixpanel with consistent correlation IDs for unified debugging and analysis.

## Critical Rules

1. **Use umbrella package** — Always use `@workleap/telemetry`, not standalone packages
2. **Do not invent APIs** — Only use documented APIs from references
3. **Correlation is automatic** — Never manually set Telemetry Id or Device Id; never create your own `TelemetryContext` instances
4. **Noop for non-production** — Use `NoopTelemetryClient` in Storybook/tests
5. **Privacy matters** — Never log PII to LogRocket; use `data-public`/`data-private` attributes
6. **productFamily is required** — `initializeTelemetry` requires `"wlp"` or `"sg"` as the first argument

## Reference Guide

For detailed documentation beyond the rules above, consult:

- **`references/api.md`** — Initialization options, TelemetryClient properties, Honeycomb/LogRocket/Mixpanel client APIs, React hooks, Noop clients, LogRocketLogger
- **`references/integrations.md`** — Platform-specific configuration, Honeycomb tracing patterns, LogRocket privacy and user identification, Mixpanel event tracking, cross-platform correlation workflows
- **`references/examples.md`** — Full application setup, Storybook/test configuration, user identification, custom Honeycomb traces, Mixpanel tracking patterns, logging configuration, troubleshooting
