---
name: observability
description: Writes and reviews Swift observability code on Apple platforms - unified logging (Logger, OSLog, privacy redaction, log levels and persistence), signposts and Instruments, activity tracing, MetricKit metrics and diagnostics (launch, hangs, crashes, OOM, disk writes), crash reports and symbolication, OSLogStore log export, Xcode Organizer, and shipping telemetry to your own backend or third-party SDKs. Use when adding logging, instrumenting performance, wiring MetricKit, diagnosing production crashes or hangs, exporting logs for support, or choosing between print, Logger, signposts, and analytics SDKs.
license: MIT
metadata:
  author: Anton Novoselov
  version: "1.0"
---

Write and review Swift code that makes an app observable: emit the right signal (log, signpost, metric, diagnostic) at the right level, keep user data out of the logs, and get the data back from production in a form you can actually read - symbolicated, aggregated, and attributed to the right release.

Review process:

1. Establish the signal model (three pillars, unified logging architecture, levels and persistence, dev vs production visibility) using `references/fundamentals.md`.
1. Confirm each emission uses the right signal via the decision tree below; reroute if it does not (print where a Logger belongs, a log where a signpost belongs, a hand-rolled timer where MetricKit already measures).
1. Validate `Logger` usage (subsystem/category structure, level choice, privacy annotations, interpolation performance, wrapper design) using `references/logger-api.md`.
1. Validate log retrieval workflows (Console.app, `log` CLI predicates, logging profiles, sysdiagnose) using `references/log-cli-and-console.md`.
1. Validate in-app log access and support-log export using `references/oslogstore.md`.
1. Validate signpost instrumentation (`OSSignposter`, IDs, intervals, points of interest, Instruments wiring) using `references/signposts.md`.
1. Validate cross-flow correlation (activities, correlation IDs) using `references/activity-tracing.md`.
1. Validate MetricKit adoption (subscription timing, payload handling, histograms, diagnostics, the iOS 27 `MetricManager` API) using `references/metrickit.md`.
1. Validate crash/hang/OOM observability (what leaves a report and what does not, exit reasons, Organizer) using `references/crash-reporting.md`.
1. Validate symbolication (dSYM handling, UUID matching, atos, MetricKit call stacks) using `references/symbolication.md`.
1. Validate the production pipeline (export format, units, aggregation strategy, launch-metric skew, alerting) using `references/production-monitoring.md`.
1. Validate network-request observability (error taxonomy and noise filtering, non-fatal report design, `URLSessionTaskMetrics`, aggregate monitoring) using `references/network-telemetry.md`.
1. Validate third-party SDK integration (crash-handler exclusivity, dSYM upload, bridging, privacy) using `references/third-party-sdks.md`.
1. Catch common mistakes using `references/anti-patterns.md`.

If doing partial work, load only the relevant reference files.


## Task-based routing

Match the user's goal to the read order. Load only what you need.

### "Add (proper) logging to my app / replace print statements"
1. `references/logger-api.md` - Logger setup, categories, levels, privacy
2. `references/fundamentals.md` - which levels persist, who can see what

### "My interpolated values show as <private> / I need to hide user data in logs"
1. `references/logger-api.md` - privacy annotations, `.private(mask: .hash)`, equality tracking

### "Read logs from a device / filter the noise in Console / capture logs while debugging"
1. `references/log-cli-and-console.md` - Console.app workflow, `log stream/show/collect`, predicates, scripted simulator/device capture tiers

### "Let users send me their logs / show logs inside the app"
1. `references/oslogstore.md` - OSLogStore, scope limits, export design
2. `references/logger-api.md` - persistence rules decide what is even retrievable

### "Measure how long an operation takes / find what is slow"
1. `references/signposts.md` - OSSignposter intervals, Instruments os_signpost
2. `references/production-monitoring.md` - if the measurement must come from the field

### "Trace a user flow across subsystems / correlate related logs"
1. `references/activity-tracing.md` - activities, correlation IDs, when signposts fit better

### "Collect performance/battery/launch metrics from production"
1. `references/metrickit.md` - MXMetricManager, payloads, histograms, custom mxSignpost metrics
2. `references/production-monitoring.md` - exporting, aggregating, alerting

### "Why is my app crashing / hanging / getting killed in production?"
1. `references/crash-reporting.md` - crash pipeline, exit reasons, OOM, watchdog, hangs
2. `references/metrickit.md` - diagnostic payloads carry the stacks
3. `references/symbolication.md` - make the stacks readable

### "Symbolicate this crash log / MetricKit stack"
1. `references/symbolication.md` - dSYMs, UUID matching, atos recipes

### "Set up Sentry / Crashlytics / Datadog, or decide if I need them"
1. `references/third-party-sdks.md` - what they add over MetricKit, integration rules
2. `references/crash-reporting.md` - the native baseline they compete with

### "Build a metrics dashboard / send telemetry to my backend"
1. `references/production-monitoring.md` - the ASC Power and Performance API, pipeline design, units, buckets, index metrics
2. `references/metrickit.md` - the payload shapes you are exporting

### "Monitor network errors / diagnose slow requests in production"
1. `references/network-telemetry.md` - error taxonomy, non-fatal report design, URLSessionTaskMetrics, aggregate monitoring
2. `references/third-party-sdks.md` - if an off-the-shelf RUM/performance SDK is in play

### "I'm hitting bugs / logs missing / payloads never arrive"
1. `references/anti-patterns.md` - the usual causes
2. `references/fundamentals.md` - persistence and delivery rules


## Decision tree

### Which signal should I emit?

```
Recording a discrete event to reconstruct behavior later?
  -> Logger (unified logging), with the level matching persistence needs

Measuring the duration of an operation for local profiling?
  -> OSSignposter interval + Instruments os_signpost / Points of Interest

Measuring durations or counts across the production fleet?
  -> mxSignpost (MetricKit histograms) or your own telemetry event

Daily launch / hang / battery / disk / memory numbers from production?
  -> MetricKit metric payloads (MXMetricPayload)

Crash, hang, CPU-spin, disk-write, or OOM call stacks from production?
  -> MetricKit diagnostic payloads + Xcode Organizer (+ third-party if you
     need real-time alerting and grouping)

Correlating logs that belong to one user flow across subsystems?
  -> os_activity scopes or an explicit correlation ID in the message

Users need to send you what happened on their device?
  -> OSLogStore export in-app, or a sysdiagnose for deep system issues

Real-time dashboards, alerting, release health, session context?
  -> third-party SDK (Sentry/Crashlytics/Datadog) or your own pipeline
     (OpenTelemetry + OTLP backend is the vendor-neutral build-it route)
```

### Which log level?

```
Only useful while actively developing, high volume?      -> debug / trace
Helpful context, fine if it evaporates after the fact?   -> info
Essential for troubleshooting, must survive on device?   -> notice (default)
Something failed but the app copes?                      -> error
A bug: broken invariant, data loss risk, must stand out? -> fault / critical
```

Persistence follows the level: `debug` is never written to disk, `info` only
during a `log collect`, `notice`/`error`/`fault` persist to the store (until
rotation). If support needs to see it from a user's device, it must be
`notice` or above.


## Core Instructions

- **Never** ship `print` or `NSLog` as the app's logging mechanism. `print` is invisible outside a debugger and never persisted; `NSLog` is synchronous and slow. Use `Logger` (iOS 14+) or `os_log` (iOS 10+).
- Create one `Logger` per subsystem/category pair as a `static let`; use the bundle identifier as the subsystem and a functional area per category (`networking`, `persistence`, `ui`). Do not funnel the whole app through one category.
- **Never** wrap `Logger` behind a function that takes a plain `String`. Interpolation in an `OSLogMessage` is evaluated lazily only if the message is actually emitted; a `String` parameter forces evaluation on every call. If you must abstract, take `@autoclosure () -> String` or expose per-category `Logger`s directly.
- Treat interpolated strings and objects as redacted by default (they log as `<private>` on a device without a debugger). Mark values `privacy: .public` only after confirming they contain no user data; use `privacy: .private(mask: .hash)` when you need to correlate identical values without revealing them.
- **Never** log PII (names, emails, tokens, URLs with credentials, account numbers) as `.public`, and never write it into files or third-party SDKs where the OS redaction cannot protect it. Anyone with the device can read your app's persisted log messages in Console.
- Choose levels for their persistence and cost, not their vibe: `debug` (memory only, near-zero cost when not captured), `info` (memory, persisted only inside a `log collect`), `notice` (persisted default), `error` (persisted, for failures the app handles), `fault`/`critical` (persisted, captures extra state, for actual bugs). Reserve `fault` for programmer errors, not expected failures.
- Static format strings only: interpolate values, never build the message by string concatenation first - concatenation defeats both privacy annotations and lazy evaluation.
- For durations, use `OSSignposter` intervals, not log lines with timestamps. Generate an `OSSignpostID` per operation instance (`makeSignpostID()`), store the returned `OSSignpostIntervalState`, and end with the same name. Use `.pointsOfInterest` category for events you want in the dedicated Instruments track.
- Keep signposts in release builds - they are designed to be cheap and Instruments profiling of release builds depends on them. Gate high-volume ones behind `OSSignposter.disabled` or an environment check if needed.
- Subscribe to MetricKit (`MXMetricManager.shared.add(_:)`) once, early, on a launch path that always runs (App init / didFinishLaunching). `pastPayloads` only returns data if the app was subscribed; a late or conditional subscription silently loses history.
- MetricKit delivers on real devices only - **never** debug it in the simulator. Use Xcode's Debug > Simulate MetricKit Payloads with a device attached, and expect metric payloads at most once per 24h (diagnostics immediately on iOS 15+, crash diagnostics at next launch).
- MetricKit subscriber callbacks arrive on a background queue: do not touch UI, and persist/forward payloads quickly - the payload objects provide `dictionaryRepresentation()`/`jsonRepresentation()` for export.
- When exporting MetricKit histograms, keep Apple's units (`Measurement` values, buckets in the payload's own unit) and convert exactly once at the edge. Verify the unit of every metric before writing transforms - a silent seconds-vs-milliseconds mismatch corrupts a week of dashboards before anyone notices.
- **Never** measure cold launch as "process start to didFinishLaunching" without accounting for prewarming (check `ActivePrewarm` in the environment): since iOS 15 the system may start the process long before the user taps, producing minutes-long fake launches. Prefer MetricKit's `histogrammedTimeToFirstDraw`.
- Watch means and low percentiles, not just p95/p99: prewarming outliers and clamping hide regressions in the middle of the distribution. For a fleet-wide view, convert metrics to a bounded 0-100 score before averaging.
- OOM terminations leave **no crash report**. Observe them via `MXAppExitMetric` memory-related exit reasons (and the memory-exception diagnostic in the new API), and reduce them by lowering background footprint - do not wait for a crash reporter to show them.
- On a memory warning, change caching policy (stop caching, cap sizes, prefer `NSCache` which evicts automatically) rather than eagerly walking and freeing compressed collections - touching compressed pages forces decompression and spikes footprint exactly when you can least afford it.
- **Never** install two crash-reporting SDKs (or a crash SDK plus your own Mach/signal handlers) in one app - handlers chain unreliably and corrupt each other's reports. Pick one; MetricKit does not conflict because it collects out-of-process.
- Archive dSYMs for every shipped build and verify UUID match (`dwarfdump --uuid`) before symbolicating. MetricKit call stacks arrive unsymbolicated as `binaryUUID` + offsets - symbolicate off-device with `atos -i` (the `-i` recovers inlined frames; load address = frame address minus `offsetIntoBinaryTextSegment`). Submit builds to the App Store with symbols so Organizer reports arrive named with jump-to-source.
- Triage hangs by main-thread CPU: near 100% means the work itself is too slow (Time Profiler territory); near idle means blocked on I/O, a lock, IPC, or a priority inversion (System Trace territory) - profiling CPU harder cannot find a blocked thread. Hangs are reported from 250 ms; treat 500 ms+ as severe.
- **Never** validate watchdog behavior in the simulator or under the debugger - the launch watchdog is disabled in both. Test launch standalone on the oldest supported device, and enable Organizer regression notifications so a rising hang or termination rate pages you instead of your users.
- Read `OSLogStore` off the main thread; on iOS it is scoped to your own process (`.currentProcessIdentifier`) and only returns what persistence rules kept - `debug`/`info` messages will not be there in production.
- Use activities (`os_activity`) or an explicit correlation ID to relate logs across a flow; use signposts to measure it. Activities correlate, signposts time - do not bend one into the other.
- Report network failures selectively: decode and post-decode validation failures are contract breaks worth a non-fatal report from every user (wrapped in a custom error with a readable description - never the raw `URLError`, whose shared domain collapses distinct problems into one dashboard row); offline/connection-lost/timeout noise is counted in aggregate, and cancellations you issued are dropped. Diagnose slow requests with `URLSessionTaskMetrics` phases (DNS, connect, TLS, time-to-first-byte, `isReusedConnection`) - see `references/network-telemetry.md`.
- Instrument before optimizing: when chasing a production-only problem, first add the metrics/diagnostics that would prove the hypothesis, ship, and read the data - do not guess from a local repro that does not reproduce.
- Log the decision points, not the noise: state transitions, branch outcomes, inputs at boundaries, and every error path. A log that fires every frame or every scroll tick belongs behind a signpost or should not exist.


## Output Format

If the user asks for a review, organize findings by file. For each issue:

1. State the file and relevant line(s).
2. Name the anti-pattern being replaced.
3. Show a brief before/after code fix.

Skip files with no issues. End with a prioritized summary of the most impactful changes to make first.

If the user asks you to write or fix observability code, make the changes directly instead of returning a findings report.

Example output:

### CheckoutService.swift

**Line 31: `print` for a production failure path - invisible and unpersisted.**

```swift
// Before
print("Payment failed for \(user.email): \(error)")

// After - persisted, categorized, PII kept private
private static let logger = Logger(
    subsystem: Bundle.main.bundleIdentifier!, category: "checkout")

Self.logger.error("Payment failed for \(user.email, privacy: .private(mask: .hash)): \(error.localizedDescription, privacy: .public)")
```

**Line 58: hand-rolled timing log - use a signpost interval.**

```swift
// Before
let start = Date()
let receipt = try await submit(order)
logger.info("submit took \(Date().timeIntervalSince(start))s")

// After
private static let signposter = OSSignposter(
    subsystem: Bundle.main.bundleIdentifier!, category: "checkout")

let id = Self.signposter.makeSignpostID()
let state = Self.signposter.beginInterval("SubmitOrder", id: id)
let receipt = try await submit(order)
Self.signposter.endInterval("SubmitOrder", state)
```

### Summary

1. **Privacy (high):** hash-mask the email; the raw value is currently public in a persisted error message.
2. **Signal choice (medium):** move all duration logging to signposts so Instruments and MetricKit can aggregate them.

End of example.


## References

- `references/fundamentals.md` - the observability model: three pillars on Apple platforms, unified logging architecture (binary store, memory vs disk), levels and persistence, who can see what in dev vs production, the signal map.
- `references/logger-api.md` - `Logger` and legacy `os_log`: setup patterns, levels, privacy annotations and masking, formatting/alignment, lazy interpolation, wrapper and multi-destination facade design.
- `references/log-cli-and-console.md` - Console.app workflow, `log stream/show/collect/config`, predicate syntax, logging configuration profiles, sysdiagnose, scripted capture workflows for agent-assisted debugging (simulator stream-to-file, `devicectl` console launch with an env-gated print mirror, timestamped `sudo log collect` device archives).
- `references/oslogstore.md` - reading your own logs at runtime, scope and persistence limits, building a support-log export.
- `references/signposts.md` - `OSSignposter` intervals/events/animation intervals, signpost IDs, legacy `os_signpost`, Instruments os_signpost and Points of Interest, `xctrace`, XCTest metrics, DTrace probes for un-instrumentable processes.
- `references/activity-tracing.md` - `os_activity` in Swift, scopes, `labelUserAction`, correlation IDs, activities vs signposts.
- `references/metrickit.md` - `MXMetricManager`/`MXMetricPayload`/`MXDiagnosticPayload` (iOS 13-25), the iOS 27 `MetricManager` async API, payload cadence, histograms, custom `mxSignpost` metrics, extended launch tracking, testing.
- `references/crash-reporting.md` - what leaves a report and what does not: crash pipeline, exception types, watchdog codes, exit reasons, OOM, the hang tooling matrix (Thread Performance Checker, on-device detection, Organizer hang reports), Xcode Organizer panes and regressions.
- `references/symbolication.md` - dSYMs, UUID matching, `atos`, debug-info tiers and stripped-symbol behavior, Swift demangling, the dyld shared cache, symbolicating .ips files and MetricKit call stack trees, SDK symbol upload.
- `references/production-monitoring.md` - shipping telemetry: the App Store Connect Power and Performance API (metrics, smart insights, diagnostic signatures/logs), OpenTelemetry on iOS (opentelemetry-swift, OTLP exporters, gauge/counter/histogram semantics, TaskLocal span propagation, withSpan facade design, verbosity gating), export pipeline design, units and buckets, lab vs field, launch-metric skew (prewarming), score indexes, percentiles vs means, alerting.
- `references/network-telemetry.md` - request-level network observability: why lab conditions undersell the field, the report/count/drop error taxonomy, non-fatal report design (readable custom errors, userInfo context, embedded breadcrumbs), `URLSessionTaskMetrics` phases and diagnostics (keep-alive, server processing time, latency physics), aggregate monitoring (Firebase Performance / OTel), targeted full-dump collection.
- `references/third-party-sdks.md` - Sentry/Crashlytics/Datadog/Firebase vs the native stack, crash-handler exclusivity, bridging unified logging, dSYM upload automation, privacy manifests and cost.
- `references/anti-patterns.md` - common mistakes LLMs make when generating logging and telemetry code.
