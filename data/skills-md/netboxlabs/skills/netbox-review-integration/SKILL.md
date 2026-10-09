---
name: netbox-review-integration
description: >
  Review and audit NetBox integration code for correctness, performance, and reliability.
  Use when reviewing scripts or applications that interact with NetBox APIs, checking for
  pagination bugs, authentication issues, performance anti-patterns, error handling gaps,
  and SDK misuse.
license: Apache-2.0
---

# NetBox Integration Code Review

> **Your knowledge of NetBox APIs may be outdated.** Verify specific API behaviors, limits, and patterns against current documentation before flagging issues.

**Target:** NetBox 4.5–4.7 (current 4.7.2). Several rules flip between 4.6 and 4.7 — establish the target version (`GET /api/status/` → `netbox-version`, or the project's pin) before applying version-tagged rules.

## Retrieval Sources

| Source | URL / Method | Use for |
|--------|-------------|---------|
| NetBox REST API docs | `https://netboxlabs.com/docs/netbox/integrations/rest-api/` | Current endpoint behavior |
| pynetbox repo | `https://github.com/netbox-community/pynetbox` | SDK method signatures |
| Diode Python SDK | `https://github.com/netboxlabs/diode-sdk-python` | Ingestion API patterns |
| NetBox MCP server | If configured — verify object schemas and filter availability | Field validation |

## Review Workflow

Follow this checklist when reviewing NetBox integration code:

1. **Verify retrieval** — Check current API docs for any endpoints/patterns you're unsure about
2. **Read the full file** — understand the integration's intent before flagging issues
3. **Check authentication** — token format, header usage, credential storage
4. **Check pagination** — all list endpoints must handle pagination
5. **Check performance** — config_context handling (version-dependent), brief mode / field selection, filter specificity
6. **Check error handling** — HTTP errors, rate limits, timeouts, partial failures
7. **Check data integrity** — correct use of PATCH vs PUT, bulk operation atomicity
8. **Provide evidence** — reference specific line numbers and explain why something is wrong

## Critical Rules

### Authentication (AUTH)

| ID | Rule | Severity |
|----|------|----------|
| AUTH-1 | Use `nbt_`-prefixed v2 tokens on NetBox 4.5+ | High |
| AUTH-2 | Never hardcode tokens in source — use env vars or secrets manager | Critical |
| AUTH-3 | Use `Bearer` prefix in Authorization header (not `Token` on 4.5+) | High |
| AUTH-4 | Verify token has required permissions for all accessed endpoints | Medium |
| AUTH-5 | Flag reliance on v1 (`Token <plaintext>`) tokens — deprecated in 4.6, **removed in v5.0**; migrate to v2. On 4.6.1+ the v2 plaintext is shown once at creation, in the response `token` field (`key` is only the public identifier) — capture it then | High |
| AUTH-6 | Never create tokens with `?background=true` (4.7.0/4.7.1 recorded plaintexts in job results; 4.7.2 returns 400), and never rely on a client-chosen `token` value on create (ignored on 4.7+) | High |
| AUTH-7 | Executing custom scripts via `POST /api/extras/scripts/<id>/` on 4.7+ requires a write-enabled token — flag read-only tokens used for it | Medium |

### Pagination (PAG)

| ID | Rule | Severity |
|----|------|----------|
| PAG-1 | All list endpoint calls MUST handle pagination (follow `next` links) | Critical |
| PAG-2 | Never assume all results fit in one response — even small collections grow | High |
| PAG-3 | Set explicit `limit` parameter — don't rely on server default (50) | Medium |
| PAG-4 | GraphQL queries MUST include `pagination: {limit: N}` at every list level | Critical |
| PAG-5 | Nested GraphQL lists need their own pagination parameters | High |
| PAG-6 | Prefer cursor pagination over deep offsets for large reads — REST `?start=<id>` (4.6+), GraphQL `pagination: {start: N, limit: M}` (4.5.2+); flag deep `?offset=` scans | Medium |

### Performance (PERF)

| ID | Rule | Severity |
|----|------|----------|
| PERF-1 | **4.5–4.6:** device/VM list queries MUST send `?exclude=config_context` (or `?omit=config_context`, 4.5.2+). **4.7+:** `?exclude=config_context` is silently ignored and config context is cached — do not flag its absence; flag code that *depends* on it for payload size and suggest `?fields=`/`?omit=`/`?brief=True` | Critical (4.5–4.6) / Low (4.7+) |
| PERF-2 | Use `?brief=True` for reference lookups and dropdowns | High |
| PERF-3 | Use specific filters (`name__ic=`, `site_id=`) instead of `?q=` at scale | High |
| PERF-4 | Use `?fields=` to select only needed fields | Medium |
| PERF-5 | Parallelize independent API calls — don't serialize unrelated requests | Medium |
| PERF-6 | Use bulk endpoints (POST/PATCH/DELETE arrays) instead of per-object calls | High |
| PERF-7 | GraphQL depth must stay ≤ 3, never exceed 5 | High |

### Error Handling (ERR)

| ID | Rule | Severity |
|----|------|----------|
| ERR-1 | Handle HTTP 4xx/5xx responses — don't assume success | Critical |
| ERR-2 | Implement retry with backoff for 429 (rate limit) and 5xx errors | High |
| ERR-3 | Handle bulk failures — all-or-nothing on every version. On 4.7+ the body is `{"detail", "errors": [{"index" or "id", "errors"}]}`: map errors back to submitted objects (`index` for creates and malformed entries, `id` for updates/deletes) and resubmit only those; on 4.5–4.6 only the first failure's field errors are returned | Medium |
| ERR-4 | Check `response.errors` on Diode ingestion responses | High |
| ERR-5 | Handle branch async job failures (poll until terminal status) | High |
| ERR-6 | `?background=true` (4.7+): 202 is *accepted*, not *succeeded* — code must poll `job.url` to a terminal status and check `data.status_code`. Flag 202 treated as success, `If-Match` combined with background (400), and missing 503 handling (no worker) | High |

### Data Integrity (DATA)

| ID | Rule | Severity |
|----|------|----------|
| DATA-1 | Use PATCH for updates — PUT replaces entire objects, clearing omitted fields | Critical |
| DATA-2 | Include `id` in each object for bulk PATCH/DELETE operations | High |
| DATA-3 | Use natural keys (slug/name) for readability but be aware of uniqueness constraints | Medium |
| DATA-4 | Validate dependency order for REST creates (parent before child) | High |
| DATA-5 | IPAddress values MUST include CIDR prefix length (`/24`, not bare IP) | High |
| DATA-6 | For tag edits, prefer write-only `add_tags`/`remove_tags` (4.6+) over read-modify-write of the full `tags` list — the latter clobbers concurrent writers' tags | Medium |
| DATA-7 | For read-modify-write on a single object under concurrency, use ETag + `If-Match` (4.6+); a 412 response means the object changed — re-fetch and retry rather than blind overwrite | Medium |
| DATA-8 | On 4.7+, selection/multi-selection custom fields read as `{"value", "label"}` objects — flag `custom_fields["x"] == "raw"` comparisons and code that writes the read object back (fails validation); write the raw value | High |
| DATA-9 | Services: use `port_mappings` (`["tcp/80"]`) over the deprecated `protocol`/`ports` pair on 4.7+ (removed in 5.0); flag `protocol__ic`-style and `port__empty` filters (gone in 4.7) | Medium |

## Anti-Patterns to Flag

| Anti-Pattern | Why It Matters | Fix |
|-------------|---------------|-----|
| No pagination loop | Silently drops data beyond first page | Follow `next` links until null |
| `?q=` for bulk filtering | Full-text search is slow at scale | Use specific filter expressions |
| PUT for partial updates | Clears fields you didn't intend to change | Use PATCH |
| Hardcoded token in source | Security vulnerability | Use environment variable |
| Sequential single-object creates | 100x slower than bulk | Use array POST to list endpoint |
| Ignoring `config_context` in list queries (4.5–4.6) | 10-100x slower responses | Add `?exclude=config_context`; on 4.7+ it is ignored — use `?fields=`/`?omit=`/`?brief=True` for payload size only |
| Treating HTTP 202 from `?background=true` as success (4.7+) | Validation and the write happen later in the worker | Poll the job URL; check `status` and `data.status_code` |
| `custom_fields["env"] == "prod"` on 4.7+ | Selection values are `{"value", "label"}` dicts — the comparison is always False | Compare `["value"]`; unwrap defensively for mixed 4.6/4.7 fleets |
| Creating API tokens via `?background=true` | Plaintext lands in job results (4.7.0/4.7.1); 400 on 4.7.2 | Create tokens synchronously; run ≥ 4.7.2 |
| Catching bare `Exception` on API calls | Hides real errors | Catch `requests.HTTPError` specifically |
| No timeout on HTTP requests | Hangs indefinitely on network issues | Set `timeout=30` |
| GraphQL without pagination params | Omitting `pagination` returns **all** rows; `pagination` without `limit` returns Strawberry's default **100** (not the REST default of 50) — both silently differ from expectations | Always pass `pagination: {limit: N}` explicitly |
| Polling branch jobs without backoff | Wastes API calls, may trigger rate limits | Exponential backoff (1s → 30s) |

## Scope

This skill covers **code that calls NetBox APIs**. It does NOT cover:
- NetBox plugin internals → use [netbox-plugin-development](../netbox-plugin-development/SKILL.md)
- Data model design quality → use [netbox-review-datamodel](../netbox-review-datamodel/SKILL.md)
- NetBox server administration → use [netbox-administration](../netbox-administration/SKILL.md)

## Principles

- **Be certain.** Retrieve current API docs before flagging version-specific issues.
- **Provide evidence.** Reference line numbers and explain the actual failure mode.
- **Focus on correctness.** A working integration that's slightly verbose is better than a broken clever one.
- **Severity matters.** Critical issues break functionality. High issues degrade performance or reliability. Medium issues affect maintainability.
- **Don't over-flag.** If code works correctly for its specific use case (e.g., small dataset that fits in one page), note the limitation but don't mark it critical.
