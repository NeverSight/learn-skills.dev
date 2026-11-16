---
name: box-sdk-development
description: Build or debug application code using an official Box SDK, especially Python or TypeScript/Node. Covers SDK call correctness, file transfer, bulk work, rate limits, and observability; not one-off CLI or MCP content operations.
---

# Box SDK development

## Before coding

1. Inspect the installed SDK version and types, runtime, authentication, Box actor, existing client wrapper, and expected workload. Keep the project's SDK major version unless migration is required or requested.
2. Choose where the client, token management, rate limiter, retry policy, and logging live. Trace existing request paths for duplicate calls or bypassed controls. For repeated operations, estimate calls, request rate, transfer size, and restart needs before choosing an approach.
3. Verify every Box method's arguments, return type, pagination, and errors against the installed SDK and current Box docs. Python and Node SDK major versions have incompatible interfaces; do not copy calls across versions.
4. Implement and run focused tests plus the project's type check or build. Verify permissions and transfer behavior with an authorized test account when available; compilation alone cannot prove them.

Read the relevant SDK reference: [Python](references/python.md) or [TypeScript/Node](references/typescript.md). For collection-wide jobs, read [bulk operations](references/bulk-operations.md). For uploads or downloads, read [file transfer](references/file-transfer.md).

## Design constraints

- Choose the API for the requested result: original bytes, a preview, metadata, or a listing. Use the file-content endpoint for original bytes and representations for previews; a listing is discovery, not a download. Request needed fields and paginate to the endpoint's actual end, using markers when supported for large or changing collections.
- Prefer Box-side copy, move, or metadata operations when content stays in Box. Use events or webhooks with catch-up instead of repeated full scans when tracking changes.
- Reuse the SDK client and token cache. Include authentication, discovery, retries, and verification in API-call budgets; custom application calls count toward enterprise allocation even without 429s.
- Bound concurrent requests by actor and endpoint. Current Box SDKs retry 429s with `Retry-After`; check the installed version and keep one retry owner. For older SDKs or custom HTTP, use bounded backoff that honors `Retry-After`. Reconcile uncertain writes before retrying; diagnose 401/403 rather than repeating them unchanged.
- Keep client secrets and service-account keys server-side. Use the intended actor and least privilege; never log credentials.

## Observability

Instrument the SDK client or wrapper once. Record successes and failures with operation, item ID, safe actor or tenant ID, status, Box request ID when available, duration, bytes when relevant, and job ID. Capture 429s and retry delay only if SDK hooks or transport instrumentation expose them; hidden retries are unknown, not zero. For bulk jobs, keep durable per-item outcomes and monitor throughput and calls against the plan. Surface throttling or unexpected usage during the run. Configure log volume and retention; omit content, credentials, and signed URLs.

## Completion report

After every SDK task, briefly state what changed and what was verified; the material design choices and their reasons; and viable alternatives with their tradeoffs. For bulk work, include the call-budget assumptions. State any unverified behavior.

## Official sources

- [Node SDK](https://github.com/box/box-node-sdk), [Python SDK](https://github.com/box/box-python-sdk), and [Box API reference](https://developer.box.com/reference/)
- [Rate limits](https://developer.box.com/guides/api-calls/permissions-and-errors/rate-limits/) and [marker pagination](https://developer.box.com/guides/api-calls/pagination/marker-based/)
