---
name: logfire-frontend
description: Set up and troubleshoot Pydantic Logfire frontend observability and session replays in JavaScript/TypeScript browser applications. Use for browser errors, RUM, Web Vitals, replay recording, privacy controls, or reducing browser telemetry volume. Supports browser entrypoints, React/Vite, and the client side of Next.js; use logfire-instrumentation for server-side telemetry.
---

# Set Up Frontend Observability and Session Replays

The application uses `@pydantic/logfire-browser` and, when replay is requested,
`@pydantic/logfire-session-replay`. Configure one browser provider; preserve an
existing OpenTelemetry provider, proxy, and application initialization pattern.

## Confirm the browser application

Read repository instructions, the application manifest, browser entrypoint,
router, and existing instrumentation. For Next.js, distinguish client code from
server instrumentation before changing either. Respect dependency constraints;
check the installed SDK's types before using a capture or sampling option.

Preserve the exact origin, organization, and project supplied by the user or
setup handoff. Browser-only setup does not require a CLI login, a local SDK
credential, or an ordinary project write token. Use existing native MCP access
for verification when available; otherwise use the Logfire UI.

Create or select the frontend application under **Frontend → Applications** and
use its generated regional URL and restricted frontend token. A normal project
write token, server environment variable, or `.logfire` credential is unsuitable
for browser code. The frontend application owns service identity. If no supported
public API/tool can manage it, use the UI; do not invent a private endpoint.

## Match capture to the request

Read [browser setup](./references/setup.md), then the applicable section of
[capture profiles](./references/capture-profiles.md):

- **Full frontend observability:** automatic page/request/interaction spans and
  Web Vitals. Add replay only when requested.
- **Errors and replays with automatic instrumentation:** retain traces with
  Logfire error-level events or OpenTelemetry error status, while keeping replay
  independently enabled. This also retains other spans in a qualifying trace.
- **Minimal errors and replays:** disable automatic spans and Web Vitals and
  explicitly report application errors. Use when the user requires lower browser
  instrumentation overhead or strictly limits the signals collected.

Preserve existing approved replay rates and masking. Trace sampling, replay
sampling, and metric capture are separate decisions. Do not promise that
`minLevel` filters automatic spans, that a trace sampler retains an entire browser
session, or that every handled application failure is captured automatically.

Session replay is Early Access; check availability for the target organization
and keep an existing application rollout flag. Mask text and inputs, leave
console capture off, and block sensitive regions before recording them. Review
attributes and URLs separately from visible-text masking. Add normalized route
templates and opaque user IDs only when useful; names and emails are optional
personal data.

## Verify the selected behavior

Use [verification and troubleshooting](./references/verification.md) to exercise
the real browser application, check the signals retained and omitted, query
fresh errors in the exact project, and play the matching recording. For a
sampling profile, test successful requests and the failure types the user cares
about; inspect actual exported spans rather than assuming how HTTP status maps
to error severity.

Run the application's normal typecheck/build and focused tests. Report browser
execution, telemetry ingestion, and replay playback separately. A successful
build, flush, upload response, or generated link does not prove all three.
Return the verified project/application, capture policy, and a clean relevant UI
link. If account reads or browser playback are unavailable, mark those parts
unverified and state what evidence is missing.

For server-side Node.js or Next.js setup, use
[application instrumentation](../logfire-instrumentation/SKILL.md).
