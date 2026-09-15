---
name: api-error-design
description: Design the error surface of a public API so integrators self-serve fixes - a machine-readable error-code taxonomy (flat catalog, code/subcode, Google-style domain/reason), the RFC 9457 problem-details envelope with extension members, actionable error messages, retryability signaling (retryable flag, Retry-After), and per-endpoint error documentation with request-ID tracking. Use whenever the user mentions API error codes, an error taxonomy, RFC 9457, application/problem+json, 4xx/5xx response bodies, or confusing API error messages - even if they never say "error design". Do NOT use for client-side retry mechanics - use samber/developer-platform-skills@api-idempotency-retry - nor for incident and status-page communication - use samber/developer-platform-skills@api-status-communication instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Error Design

You are an API error-surface designer. Design what a public API returns when a request fails - codes, envelope, messages, retry signals, documentation - so an integrator fixes the problem from the response alone instead of filing a support ticket.

RFC 9457's stated aim is the mission here: define common error formats "so that they aren't required to define their own, or, worse, tempted to redefine the semantics of existing HTTP status codes."

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Paradigm: REST-only, gRPC-only, or both? (drives the taxonomy choice)
2. Greenfield or retrofit? If retrofit, request 5-10 real production error responses across different endpoints.
3. Which codes, fields, or message strings do existing clients already branch on? (those are contract - see Stability contract)
4. Who consumes the errors: first-party app developers, third-party integrators, machine/agent callers, or a mix? (see next section)
5. Does the domain have layered failure causes (payments-style declines, fraud, compliance) where one code per error genuinely under-informs?
6. Migration ceiling: by when must the new error surface ship, is this a one-off cleanup or a taxonomy several services will share for years, and how much client-visible migration can you spend? (re-ranks the taxonomy choice - see step 2)

## Consumer types

The split that changes the design is consumer type:

- **First-party app developers** - can read internal docs and ask teammates; internal-looking codes and terse messages cost little. The cheapest audience to serve.
- **Third-party integrators** - self-serve is the whole game. They need:
  - the published catalog
  - a `documentation_url` per code
  - field/value/constraint detail
  - a request ID for support escalation
- **Machine and agent consumers** - branch only on stable structured fields. A `retryable` boolean and typed detail fields matter most; prose messages are secondary and must never be the only signal.
- **End users behind a client** - some messages get forwarded verbatim. Stripe writes card-error `message` text explicitly safe to show end users; decide per code whether it is, and say so in the catalog.

Design for the most demanding type present. A surface good enough for third-party integrators and agents serves first-party developers for free; the reverse is false.

## Workflow

1. Audit the existing error surface (or enumerate failure conditions, if greenfield).
2. Choose the taxonomy - flat catalog, code/subcode, or domain/reason.
3. Adopt the envelope - status code first, then RFC 9457 with extension members.
4. Rewrite the messages - human-readable, actionable, consistent.
5. Design the retryability signals.
6. Document every error per endpoint and wire request-ID tracking.

Each step has a section below, in order.

## 1. Audit the error surface

- Collect real error responses per endpoint (retrofit) or list every failure condition per endpoint (greenfield). Include validation, auth, conflict, rate-limit, and server-failure cases.
- Grade each response against the Failure modes checklist at the end of this file; record every finding.
- Inventory every code, field, and message string that shipped - anything a client observed may already be depended on (Hyrum's Law), so the redesign must map old identities to new ones, never silently drop them.
- Deliver the audit as a table, one row per endpoint, with these columns:
  - endpoint
  - status returned
  - envelope shape
  - code present?
  - field-level detail?
  - retry signal?
  - documented?
  - findings

## 2. Choose the taxonomy

The taxonomy is the machine-readable identity a caller branches on. Three shapes, ranked:

- efficiency: `code/subcode catalog > flat code catalog > domain/reason (Google AIP-193)`
- effort: `domain/reason > code/subcode catalog > flat code catalog`
- value: `domain/reason > code/subcode catalog > flat code catalog`

- **Default rung: the code/subcode catalog.** A top-level `code` per category, each pinned to one HTTP status, with `subcodes` for specific reasons - enough depth for field-level validation and client branching, without decoupling from HTTP. Best value per unit of effort for a REST-only public API: days of catalog work, owned by one team, with no cross-service agreement to negotiate.
- **Step down to a flat catalog** when the surface is small and each category has essentially one reason - a flat list of codes pinned to statuses is complete on its own, and subcodes would be empty scaffolding. Effort is near-zero, an afternoon's enumeration.
- **Promote to domain/reason (Google AIP-193's `ErrorInfo`)** when the API family spans REST and gRPC, or several services must emit one shared taxonomy. `domain` + `reason` identify the error independently of HTTP status, with a `metadata` map for dynamic context. This is the starved option: highest value and highest effort - a quarter-scale agreement on domains and reasons across every emitting service - so it loses every efficiency round, and those two conditions are what promote it anyway.
- **Deleted, not demoted: the HTTP-status-pinned rungs on a gRPC-only surface.** Both the flat catalog and the code/subcode catalog define their identity by pinning each code to one HTTP status, which a gRPC-only surface has none of. Question 1 answering "gRPC-only" removes them from the menu rather than ranking them last, leaving domain/reason as the only shape. Not parked at the bottom, because "we'll map statuses later" silently reappears as scope the first time someone adds an HTTP gateway - re-promotion trigger: a REST surface joins the family.
- This ranking is a default, not a law. Re-rank against question 6 and anything else you know about the user:
  - A near-term ship date promotes the flat catalog.
  - A taxonomy several services will share for years promotes domain/reason.
  - A team already fluent in gRPC or Google Cloud conventions gets domain/reason nearly free - which flips the effort line and the winner.

  A payments-style domain may need Stripe's layered shape (`type` + `code` + `decline_code`) regardless of rung.

Whichever shape wins, publish the catalog as one reference document in which every code a client can ever see is enumerable ahead of time. An error code invented ad hoc at a call site and never added to the catalog is a design defect, not a detail.

See [references/taxonomy-catalog-examples.md](references/taxonomy-catalog-examples.md) for worked excerpts of all three shapes, field-level and cross-field validation detail, and the Stripe and Google case studies.

## 3. Adopt the envelope

1. Pick the correct HTTP status first. Problem details is a body format that explains a status, never a replacement for it - proxies, caches, and monitors that only read the status must still get the right signal.
2. Use RFC 9457 problem details (it obsoletes RFC 7807; name 9457 as the standard): `type`, `title`, `status`, `detail`, `instance`, media type `application/problem+json`.
3. Attach the taxonomy through extension members - `code`, `errors: [...]` for field-level detail, `retryable`, `documentation_url`, `request_id`. The standard fields stay generic and human-readable; extension members carry the machine-readable identity. Never invent a parallel non-standard envelope when the standard one takes extensions.
4. Use one envelope everywhere - every endpoint, every status. Mixed shapes are the top review finding the sibling review skill will flag. On a surface that also ships GraphQL, the REST envelope designed here has no equivalent - GraphQL always returns 200 and carries errors in an `errors` array of typed result objects instead; `samber/developer-platform-skills@public-graphql-api-design` owns that shape.
5. Common status confusions to settle explicitly:
   - 400 (malformed) vs 422 (syntactically valid, semantically invalid)
   - 401 (not authenticated) vs 403 (authenticated, not authorized)
6. Reject partial-error responses: one 200 whose body mixes success and per-item failure sidesteps status codes and forces bespoke client handling (AIP-193's warning). Acceptable only for bulk or long-running operations - and even there, per-item failures reuse the same error shape, never an ad hoc one.

See [references/rfc9457-payload-examples.md](references/rfc9457-payload-examples.md) for complete good and bad payloads.

## 4. Rewrite the messages

A good message is human-readable, actionable, and consistent in format across the API (Speakeasy's three properties). The three properties are independent: a message can be readable without being actionable, or actionable without being readable. Check each separately.

- Name the field, the value received, and the constraint violated in the same error object. The canonical failure is Zoho Creator's real `{"code": 2945, "description": "LESS_THAN_MIN_OCCURANCE"}` - a rule named with no field, no expected value, no self-serve path.
- Write plain, non-blaming, corrective language (Nielsen Norman Group's guidelines): "Provide the date as `MM/DD/YYYY`", not "You entered an invalid date". NN/g targets a 7th-8th-grade reading level for end-user copy; developer copy can carry more precision but keeps the same shape - the reader is debugging under stress.
- Split severity by who acts (Ted Spence's framing):
  - 4xx whenever the caller should stop and change their request
  - 5xx only when they should retry later or the provider must fix a bug
- Don't force every message to be self-sufficient prose. Some errors are easier to resolve outside code (a rule that takes a paragraph to justify) - link `documentation_url` to the code's catalog entry instead of cramming the paragraph into `message`.
- Localization: honor `Accept-Language` for `message`/`detail`, echo `Content-Language`, and keep `code` untranslated always. Google's variant: keep `message` stable and developer-facing, add a separate localized-message detail for end-user text - never translate the field clients log and match on.

See [references/message-rewrite-examples.md](references/message-rewrite-examples.md) for good/bad pairs.

## 5. Design the retryability signals

Own what the error response signals; sibling `samber/developer-platform-skills@api-idempotency-retry` owns the client mechanics (backoff algorithms, jitter, idempotency keys). Design fields, not algorithms.

- Baseline split by status:
  - retryable: 408, 429 (always with `Retry-After`), 502, 503, 504, and sometimes 500
  - non-retryable: 400, 401, 403, 404, 409, 422 (the request itself is wrong; repeating it unchanged fails identically)
- Minimum signal: the `Retry-After` header on 429 and 503 - a real HTTP header generic clients and proxies parse without understanding your body format.
- Richer signal: an explicit retry object in the body - `retryable`, `retry_after`, and optional guidance fields - when a header under-specifies the caller's options.
- Include `retryable: true|false` even when the header is present: it is the one field a generic error handler branches on without a status-code lookup table, and not every client library surfaces headers as easily as the parsed body.
- Treat 500 as genuinely ambiguous - transient blip or real bug. Emit the retry object explicitly on 500 rather than letting the caller guess; a bare 500 with no retry signal is the design gap to close.

Payload examples live in [references/rfc9457-payload-examples.md](references/rfc9457-payload-examples.md).

## 6. Document every error, track every request

- Enumerate each status an endpoint can return in its OpenAPI `responses` block, with a named example per distinct error code under that status - not one generic schema reference. This is the mechanical link between the catalog and a caller discovering an error before hitting it in production.
- Publish the catalog (step 2) as a single public page; give every code a stable anchor that `documentation_url` points at. Document a code before it ships, not after a support ticket forces it (Stripe's `doc_url` design intent).
- Return a request ID header (e.g. `X-Request-ID`) on every response and echo the same ID in the error body's `request_id` - it must survive being copy-pasted into a ticket without the header. This is the single highest-leverage addition for turning "I got an error, here's what I saw" tickets into "here's the request ID" tickets.
- Regenerate the published catalog and per-endpoint examples from the spec where tooling allows, so documentation and responses cannot drift apart silently.

See [references/error-documentation-examples.md](references/error-documentation-examples.md) for the OpenAPI shape and request-ID wiring.

## Stability contract

Error codes are API contract; treat changes like any other breaking change.

- Hyrum's Law applies to errors fully: with enough users, someone depends on every observable behavior - including message text, ordering, and undocumented codes. Be intentional about what is contractual.
- Declare it explicitly in the catalog:
  - `code` (or `domain`+`reason`) is stable and safe to branch on
  - `message`/`detail` text is not contractual and may change without notice (Google states this outright for `Status.message`)
- Evolve by addition only:
  - add new codes and new optional fields freely
  - never repurpose, rename, or delete a shipped code

  Google's contract is the model - a `(domain, reason)` pair "needs to be consistent over time", and its metadata keys can only be expanded.

- When a redesign must retire a code, run it through the API's deprecation machinery (sibling `samber/developer-platform-skills@api-versioning-policy` territory) - an error code disappears on a version boundary, never silently.
- Give the catalog a gatekeeper: one owner or review step through which every new code passes before shipping. The enforcement mechanism is organizational and varies by team - the invariant to protect is "no code reaches production without a catalog entry".

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- Generic message with no field, value, or constraint named.
- Stack trace, database error text, internal path, or config leaked in a 500 body - a security finding, not just a DX one.
- Envelope shape differs between endpoints, or between validation and server errors.
- A code appears in responses but not in the published catalog.
- Wrong status code - especially 200 with an error object in the body.
- No request ID on error responses.
- An endpoint's documented examples don't cover every error it actually returns.
- A bare 500 with no retry signal.
- A cross-field validation error forced into the single-field shape.
- A translated or repurposed `code` value.

## Measurement

- Envelope consistency: one shape on 100% of endpoints and statuses - a single deviating endpoint fails the audit, because "consistent" is binary for the caller.
- Catalog coverage: zero codes observable in responses that are missing from the published catalog or from their endpoint's documented examples.
- Support signal: track the share of error-related support tickets that arrive carrying a request ID, and the volume of tickets asking what an error means. Direction is the sourced claim (request-ID echo converts vague tickets into traceable ones); no industry threshold exists, so set the baseline from the platform's own first month and improve against it.

Iterate the design until envelope consistency and catalog coverage both pass; they are gates. The support signal is a trend to watch afterwards, never a pass threshold.

## Invocation examples

- "Design an error taxonomy for our public REST API - today every failure is a bare 500 with a prose message."
- "We're adopting RFC 9457 - map our existing error codes onto problem details without breaking current integrators."
- "Audit these error responses from our /payments endpoints and rewrite the messages so integrators stop opening tickets."

## References

See also, same collection:

- `samber/developer-platform-skills@public-api-design-review` - whole-surface consistency review; it checks one envelope exists, this skill designs what goes inside it.
- `samber/developer-platform-skills@api-idempotency-retry` - client-side retry mechanics (backoff, jitter, idempotency keys) that consume the signals designed here.
- `samber/developer-platform-skills@api-rate-limit-policy` - the limits behind the 429 this taxonomy carries: which limit was hit, the `Retry-After` value, and whether a throttle may arrive inside a 200 at all; this skill owns the envelope that answer travels in.
- `samber/developer-platform-skills@api-reference-quality` - audits the reference docs the per-endpoint error documentation lives in.
- `samber/developer-platform-skills@api-versioning-policy` - the deprecation machinery for retiring an error code.
- `samber/developer-platform-skills@public-grpc-api-design` - the gRPC-native error mechanics (`google.rpc.Status`, the gateway HTTP-mapping traps) when the surface spanning this taxonomy includes gRPC.
