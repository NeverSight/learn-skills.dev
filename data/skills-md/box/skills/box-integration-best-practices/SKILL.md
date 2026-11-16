---
name: box-integration-best-practices
description: Build, debug, or review repeatable Box API integrations and agent workflows for efficient calls, bulk work, and 429 handling.
---

# Box integration best practices

Preserve result coverage and permissions when reducing calls. For bulk work or 429 errors, estimate calls per completed item and peak request rate by Box actor and endpoint. Budget uploads and search against their separate limits. Check the current [rate limits](https://developer.box.com/guides/api-calls/permissions-and-errors/rate-limits); user, endpoint, enterprise, and temporary quality-of-service limits may apply.

## Reduce calls

For reviews, trace Box requests through loops and retry paths before changing concurrency or seeking more capacity.

- Reuse cached access tokens. Request fields needed for a decision in the list response when supported, and reuse returned data instead of fetching each item again. `fields` reduces call count only when it replaces a follow-up read.
- Use the largest useful supported page size. For large or changing collections, use [marker pagination](https://developer.box.com/guides/api-calls/pagination/marker-based) where supported; follow `next_marker` to completion and do not treat a marker as a durable checkpoint.
- Use webhooks or events with a catch-up path instead of repeated full scans. Deduplicate deliveries; checkpoint event stream positions after successful processing. Query supported [enterprise metadata templates](https://developer.box.com/guides/metadata/queries/limitations) instead of fetching metadata for every file.
- When content stays in Box, prefer Box-side copy, move, or update operations over download and re-upload.

## Control bulk work and retries

- Bound concurrency across workers sharing a Box actor, accounting for endpoint and enterprise limits. On 429, honor `Retry-After` across affected workers. Current official SDKs retry 429s; check the installed version before adding another retry layer. For direct HTTP, use bounded backoff with jitter.
- For long-running jobs, persist per-item outcomes so work can resume. Reconcile uncertain writes before retrying them.
- Refresh expired tokens on 401; pause if failures persist. For 403, record item-specific denials and pause when failures indicate actor or app access is wrong.
- If necessary traffic still exceeds available capacity after removing avoidable calls, surface the capacity need. Do not rotate identities to evade limits.

## Check the result

Record Box calls and 429s by actor, endpoint, and status; compare calls per completed item and completed-job throughput on a representative workload. Use the [Platform Activity report](https://support.box.com/hc/en-us/articles/4415109521171-Platform-Activity-Report) for historical per-app totals. If a token reaches a browser or other client-side component, [downscope it](https://developer.box.com/guides/authentication/tokens/downscope).
