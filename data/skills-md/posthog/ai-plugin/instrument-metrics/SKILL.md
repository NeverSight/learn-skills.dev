---
name: instrument-metrics
description: >-
  Add PostHog metric capture to track counters, gauges, and histograms. Use
  after implementing features or reviewing PRs to ensure key operations are
  measured, or when asked to add metrics, counters, or track a value over time.
  Also handles mirroring existing Prometheus/StatsD/OpenTelemetry metrics into
  PostHog and initial OTLP exporter setup.
metadata:
  author: PostHog
---

# Add PostHog metric capture

Use this skill to add PostHog metric capture (counters, gauges, and histograms) for new or changed code. Use it after implementing features or reviewing PRs to ensure key operations are measured, when the user asks to add metrics or counters, or to mirror existing metrics instrumentation into PostHog. Supports any platform or language.

Supported platforms: Web (JavaScript), Node.js, Python via the `posthog.metrics` SDK API, Kubernetes via the metrics agent, and any language via OpenTelemetry (OTLP).

## Instructions

Follow these steps IN ORDER:

STEP 1: Analyze the codebase and detect the platform.
  - Detect the language, framework, and existing metrics setup.
  - Look for dependency files and project files (package.json, requirements.txt, pyproject.toml, go.mod, pom.xml, etc.).
  - Look for existing metrics instrumentation: Prometheus clients (prom-client, prometheus_client), StatsD/Datadog clients, OpenTelemetry meters, or an OpenTelemetry Collector config.
  - Check whether a PostHog SDK (posthog-js, posthog-node, posthog-python) is already installed.

STEP 2: Choose the capture path.
  - If a PostHog SDK is installed (or the platform supports one), use the `posthog.metrics` API — no OpenTelemetry packages needed. Read the matching platform reference now.
  - If the codebase already exports OpenTelemetry metrics, point the existing OTLP metrics exporter (or Collector) at PostHog instead — read the "Other Languages" reference. No application code changes needed beyond exporter config.
  - If neither applies, use the "Other Languages" reference as a fallback — it covers the generic OpenTelemetry approach.

STEP 3: Instrument alongside existing metrics.
  - Where the codebase already records a metric (a Prometheus counter, a StatsD call, an OTel instrument), add the PostHog call next to the existing one, reusing the same metric name and attributes. Do NOT remove or restructure the existing instrumentation.
  - Do not alter the fundamental architecture of existing files. Make additions minimal and targeted.
  - You must read a file immediately before attempting to write it.

STEP 4: Add new metrics where they belong.
  - Where the user asked for new metrics, or key operations have no coverage, add PostHog metric calls at the sites they belong: count successes and failures of critical flows, time external calls and jobs with histograms, gauge queue depths and pool sizes.
  - Pick the right type: counters for things that only go up, gauges for values that go up and down, histograms for distributions like durations. Set an explicit unit on histograms (`ms`, `bytes`).
  - Use stable, descriptive, dot-separated names (`jobs.processed`, `api.request.duration`) and set a service name so systems stay easy to tell apart.

STEP 5: Keep cardinality low.
  - Attributes like `route`, `status`, `plan`, or `queue` are good; user IDs, session IDs, request IDs, and timestamps are not. Every unique attribute combination creates a new series.
  - If something needs per-user or per-request detail, that's a job for PostHog logs or traces, not metrics.

STEP 6: Set up environment variables. (Skip if the PostHog SDK is already configured — `posthog.metrics` reuses the SDK's existing project token.)
  - Check if the project already has PostHog environment variables configured (e.g. in `.env`, `.env.local`, or framework-specific env files). If valid values already exist, skip this step.
  - If the PostHog project token is missing, use the PostHog MCP server's `projects-get` tool to retrieve the project's `api_token`. If multiple projects are returned, ask the user which project to use. If the MCP server is not connected or not authenticated, ask the user for their PostHog project token instead.
  - For the PostHog host URL: check the `projects-get` MCP response for a `region` field — `US` maps to `https://us.i.posthog.com`, `EU` maps to `https://eu.i.posthog.com`. If the region is not available from the MCP response or from existing project configuration, ask the user: "Are you on PostHog US Cloud or EU Cloud?" Do not assume US Cloud.
  - For the OTLP metrics endpoint, use `https://us.i.posthog.com/i/v1/metrics` (US) or `https://eu.i.posthog.com/i/v1/metrics` (EU), matching the region determined above, with the project token as an `Authorization: Bearer` header.
  - Write these values to the appropriate env file using the framework's naming convention.
  - Reference these environment variables in code instead of hardcoding them.

STEP 7: Verify metrics arrive.
  - For short-lived processes (scripts, cron jobs, serverless), flush before exit (`posthog.metrics.flush()`, or the OTel provider's `forceFlush()`/`shutdown()`).
  - Open Metrics in the PostHog sidebar and pick the metric from the name picker; data points should appear within a minute of sending.

## Reference files

- `references/javascript.md` - JavaScript (web) metrics installation
- `references/nodejs.md` - Node.js metrics installation
- `references/python.md` - Python metrics installation
- `references/kubernetes.md` - Kubernetes metrics installation
- `references/other.md` - Other languages metrics installation
- `references/start-here.md` - Getting started with metrics
- `references/basics.md` - Why you need metrics
- `references/architecture.md` - How metrics works
- `references/COMMANDMENTS.md` - Framework-specific rules the integration must follow

Each platform reference contains specific SDK setup, OTLP configuration, and integration patterns. Find the one matching the user's stack.

## Key principles

- **Environment variables**: Always use environment variables for PostHog keys and OpenTelemetry endpoints. Never hardcode them.
- **Minimal changes**: Add PostHog metric capture alongside existing metrics. Don't replace or restructure existing instrumentation.
- **Prefer the SDK**: When a PostHog SDK is present, `posthog.metrics` needs no new packages and no extra authentication. Reserve OTLP setup for codebases already invested in OpenTelemetry or languages without SDK support.
- **Low cardinality**: Every unique attribute combination creates a new series. Attach bounded dimensions like route, status, or plan — never user IDs, session IDs, or request IDs.
