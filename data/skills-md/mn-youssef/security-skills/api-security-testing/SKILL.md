---
name: api-security-testing
description: Use when testing REST, GraphQL, gRPC, or WebSocket APIs against the OWASP API Security Top 10 — object- and function-level authorization (BOLA/BFLA), excessive data exposure, mass assignment, unrestricted resource consumption, and GraphQL-specific abuse. For apps you own or are authorized to test.
---

# API Security Testing (FIND/EXPLOIT — OWASP API Top 10)

## Overview
Modern apps are API-first, and APIs fail differently from web pages: the bugs are in
*authorization per object/field* and *resource limits*, not rendering. Test the API directly,
bypassing the UI entirely.

**Core principle:** The UI is one client; attackers talk to the API raw. Every endpoint, field,
and method must enforce authz and limits on its own — the front-end protects nothing.

## Applies when / Skip when
- **Applies when:** the app exposes a programmatic API — REST, GraphQL, gRPC, or WebSocket —
  including the API *behind* a SPA or mobile client.
- **Skip when:** the app is purely server-rendered HTML with no API anyone calls → N/A.
- **If N/A:** report "api-security-testing: N/A — no API surface" and stop.

## ⚠️ Authorization
Your own/authorized API. Use test accounts and a non-production instance for stateful tests.

## Get the spec first
Pull the contract, then test every operation it (and the UI) reveals:
- OpenAPI/Swagger (`/swagger`, `/openapi.json`, `/api-docs`), GraphQL **introspection**,
  gRPC reflection, Postman collections, mobile-app traffic via proxy.
- Diff documented endpoints vs. what the app actually calls — **undocumented endpoints** are gold.

## OWASP API Top 10 — the checklist
| # | Risk | Test |
|---|------|------|
| API1 | **BOLA** (object authz) | Swap object ids across accounts → see `access-control-testing` |
| API2 | Broken authentication | Weak tokens/JWT/keys → see `authentication-testing` |
| API3 | **BOPLA** (property authz) | Read fields you shouldn't (excessive exposure) / write fields you shouldn't (mass assignment) |
| API4 | Unrestricted resource consumption | No rate/size/page limits; expensive queries; cost/DoS |
| API5 | **BFLA** (function authz) | Call admin/privileged operations as a normal user |
| API6 | Unrestricted access to business flows | Automate a flow meant to be human-paced (scalping, spam) |
| API7 | SSRF | Server fetches a URL you supply → see `file-upload-and-ssrf` |
| API8 | Misconfiguration | Verbose errors, permissive CORS, missing security headers |
| API9 | Improper inventory | Old `/v1` next to `/v2`, staging APIs, undocumented endpoints |
| API10 | Unsafe third-party consumption | App trusts an external API's response blindly |

See `references/api-attacks.md` for REST, GraphQL, gRPC, and WebSocket recipes.

## Excessive data exposure vs. the UI
The API often returns more than the UI shows (full user objects with `passwordHash`, internal
flags, other users' fields). **Inspect raw JSON responses**, not the rendered page.

## GraphQL specifics (high-value)
- **Introspection** enabled → full schema map. Pull it.
- **Batching / aliasing** → bypass rate limits, brute-force via one request.
- **Query depth/complexity** → nested recursive queries for DoS.
- **Field-level authz** → a field guarded in one query exposed via another path/mutation.

## Output
Per finding: endpoint/operation, method, account used, the raw request/response, which API-Top-10
class, and impact. BOLA/BFLA findings are typically High–Critical.

## Hand-off
Deep authz → **`access-control-testing`**; auth/JWT → **`authentication-testing`**; flow abuse →
**`business-logic-testing`**; reproduce → **`active-pentest`**; fix → **`security-hardening`**.

## Common mistakes
- Testing through the UI only — hit the API directly; that's the real attack surface.
- Reading the rendered page instead of the raw JSON — that's where over-exposure hides.
- Forgetting GraphQL introspection/batching and gRPC reflection — they hand you the whole map.
- Ignoring old API versions — `/v1` often lacks `/v2`'s fixes.
