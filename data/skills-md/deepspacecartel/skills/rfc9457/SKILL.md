---
name: rfc9457
description: How to design and review "problem details" error responses for HTTP APIs per RFC 9457 (https://www.rfc-editor.org/info/rfc9457/, obsoletes RFC 7807) - project-agnostic. Covers the application/problem+json (and +xml) media type, the type/status/title/detail/instance members, extension members, defining new problem types, the about:blank default, and security considerations around leaking implementation details in errors. Use when designing an HTTP API's error/exception response format, reviewing an error response for spec compliance, or deciding what an API should return on a 4xx/5xx.
---

# Problem Details for HTTP APIs (RFC 9457)

A machine-readable JSON (or XML) format for HTTP error bodies, so APIs
stop inventing bespoke error shapes. Full text at
[rfc-editor.org/rfc/rfc9457](https://www.rfc-editor.org/rfc/rfc9457).
Obsoletes [RFC 7807](https://www.rfc-editor.org/info/rfc7807) — same
media types and wire format, so existing 7807 responses are still
valid 9457.

Media type: `application/problem+json` (XML: `application/problem+xml`,
see the RFC's Appendix B). The HTTP status code itself still carries
the real semantics for generic software (proxies, caches, client
libraries) — problem details add API-specific detail on top, they
don't replace the status code.

## The object

Five defined members, all **optional**, all at the top level of a flat
JSON object:

| Member | Type | Meaning |
|---|---|---|
| `type` | string (URI reference) | Identifies the problem *type*. Defaults to `"about:blank"` when absent. |
| `status` | number | The HTTP status code for this occurrence — **advisory only**, see below. |
| `title` | string | Short, human-readable summary of the *type* (not this occurrence). |
| `detail` | string | Human-readable explanation of *this* occurrence. |
| `instance` | string (URI reference) | Identifies this specific occurrence. |

```json
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json

{
  "type": "https://example.com/probs/out-of-credit",
  "title": "You do not have enough credit.",
  "detail": "Your current balance is 30, but that costs 50.",
  "instance": "/account/12345/msgs/abc",
  "balance": 30,
  "accounts": ["/account/12345", "/account/67890"]
}
```

`balance` and `accounts` are extension members — see below.

## What each member is actually for

- **`type`** — the primary identifier of the problem type. If it's an
  `http(s)` URI, dereferencing it **SHOULD** return human-readable
  docs, but consumers **SHOULD NOT** auto-dereference it except for
  developer/debugging tooling. Non-resolvable schemes (e.g. `tag:`)
  are allowed, but the RFC encourages resolvable URIs — switching a
  non-resolvable `type` to a resolvable one later is a breaking
  identity change for that problem type.
- **`status`** — **MUST** match the actual HTTP status code on the
  response; it exists only so consumers can recover the original code
  after an intermediary (proxy, cache) has changed it, or once the
  body is persisted without its HTTP envelope. Generic HTTP software
  still goes by the real status line, not this field. See Security
  Considerations below for why a mismatch is a real risk, not just
  sloppiness.
- **`title`** — stable across occurrences of the same type (only
  localization should change it). It's a fallback for consumers who
  can't or won't look up the `type` URI — not the primary explanation.
- **`detail`** — occurrence-specific and meant to help the client
  *fix* the problem, not to dump debugging info. Consumers **SHOULD
  NOT** parse it programmatically — put anything a machine needs to
  act on in an extension member instead (see the validation-errors
  example below).
- **`instance`** — identifies *this* occurrence, not the type. May or
  may not be dereferenceable; if not, it's still a legitimate opaque
  ID for support/forensic purposes ("the time Joe was out of credit
  last Thursday").

## Extension members

Anything beyond the five core members is a problem-type-specific
*extension*, defined by that type's own documentation:

```json
{
  "type": "https://example.net/validation-error",
  "title": "Your request is not valid.",
  "errors": [
    { "detail": "must be a positive integer", "pointer": "#/age" },
    { "detail": "must be 'green', 'red' or 'blue'", "pointer": "#/profile/color" }
  ]
}
```

- Consumers **MUST** ignore extensions they don't recognize, so types
  can evolve without breaking old clients.
- If a member's value doesn't match its documented type, treat it as
  absent — don't error on it.
- Naming, if you want XML interop (Appendix B): start with a letter,
  stick to letters/digits/`_`, and prefer 3+ characters.

## Defining a new problem type

Before minting one, check whether you actually need it:
- A **generic** condition that applies to any resource (e.g. "write
  access disallowed") is usually better left as a bare status code
  (`403`) — don't wrap something already self-explanatory.
- If the response is a normal resource representation, or your API
  already has an application-specific error format, prefer that over
  bolting on problem details.
- **Never** use it as a debugging channel for the implementation —
  it's for the HTTP interface's semantics, not stack traces (see
  Security Considerations).

When you do define one, the RFC requires documenting:
1. A type URI (typically `http`/`https`, under your control and
   stable over time).
2. A title (short).
3. The HTTP status code it's used with.

Optionally: whether `Retry-After` applies, and any extension members
(each documented with its own meaning/type). A type URI **SHOULD**
resolve to HTML docs explaining how to fix the problem.

Check the [IANA "HTTP Problem Types" registry](https://iana.org/assignments/http-problem-types)
first — reuse an existing type when one already fits, rather than
minting a near-duplicate.

### `about:blank`

The one type this RFC registers itself. Means "no semantics beyond the
HTTP status code" — it's also the implicit default when `type` is
omitted entirely. When used, `title` **SHOULD** be the standard status
phrase for that code (`"Not Found"` for 404, etc.), optionally
localized.

## Multiple problems in one response

When several distinct problems (different types) apply, pick the most
relevant/urgent one and report just that — don't invent a generic
"batch" wrapper, it doesn't map cleanly onto HTTP semantics. Within a
*single* problem type, encode multiple items as an extension array
(like `errors`/`pointer` above) instead.

## Content negotiation

- Both request `Accept` and response `Content-Type` participate in
  normal HTTP proactive negotiation (RFC 9110 §12.1).
- A server **MAY** return `application/problem+json` even if the
  client didn't list it in `Accept` — HTTP allows this for error
  responses.
- Human-readable strings (`title`, `detail`) can be localized via
  `Accept-Language` / `Content-Language`, same as any other content.

## Security considerations (don't skip this)

- Vet everything that goes into a problem type's fields — `detail`,
  extensions, and links to occurrence info are all exposure surface.
  Don't expose stack dumps, internal paths, or other implementation
  internals through the HTTP interface.
- `status` duplicates the real HTTP status code, and the two *can*
  disagree (e.g. an intermediary changed the status in transit). There
  is no defined precedence between them — treat a mismatch as a signal
  something in the path altered the response, not as a spec violation
  to silently resolve one way.

## Gotchas

- `type` and `instance` are URI *references* — when relative, they
  resolve against the response document's base URI, so the **same**
  relative value on two different endpoints resolves to two
  **different** absolute URIs. Prefer absolute URIs for both; if you
  must use relative ones, use a full path (`/types/123`), not a bare
  fragment like `example-problem`.
- All five core members are optional and independently omittable —
  don't assume `type` or `status` will be present when writing a
  consumer; missing `type` means `about:blank`, not "malformed".
- `status` is advisory and **MUST** equal the real response status
  code — never set them to different values on purpose.
