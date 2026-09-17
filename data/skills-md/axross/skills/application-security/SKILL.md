---
name: application-security
description: Writing or reviewing code that handles untrusted input, secrets, outbound requests, rendered content, or third-party dependencies — the OWASP Top 10:2025 lens in two modes, writing secure-by-default code and judging the risk a change introduces. Triggers on "is this safe", "secure by default", "harden", "security", "secret", "privacy", "PII", "XSS", "injection", "SSRF", "safe fetch", "access control", or a dependency review. Covers secrets and environment variables, input validation, output encoding, SSRF, access control and data exposure, and supply-chain risk.
user-invocable: false
---

# Application Security

Use this capability whenever you write or review code that handles untrusted input, secrets, outbound requests, rendered content, or third-party dependencies. It runs in two modes over the same set of rules:

- **Build** — write the code secure by default. Choose the construction that is safe by shape (parse at the boundary, encode at the sink, allowlist the host) rather than the one you must remember to guard later.
- **Review** — read a change for the risk it introduces and flag it with a severity, so the fix lands before merge. The review rules name a severity (Critical / Major / Minor) for each risk; align them to the host project's review severity vocabulary when it defines one.

The framing is the **OWASP Top 10:2025**. Each reference below carries both modes for one risk. The references are written against a common web-application shape — a framework with a public/client-exposed env-var prefix, a content renderer, an image optimizer, metadata routes. When your project differs, apply the same rule to your project's equivalent surface rather than skipping it; when a rule depends on another discipline (dependency justification, review scoping), it points to that discipline in words, so this capability stays usable on its own.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html).

## OWASP Top 10:2025 Coverage

Two 2025 relocations matter for routing: **SSRF** is no longer its own category — it folded into **A01 Broken Access Control** — and vulnerable/outdated components expanded into the new **A03 Software Supply Chain Failures**.

| Risk topic                     | Primary OWASP Top 10:2025 category                        | Reference                       |
| ------------------------------ | --------------------------------------------------------- | ------------------------------- |
| Secrets & environment vars     | A04 Cryptographic Failures, A02 Security Misconfiguration | `secret-handling`               |
| Input validation               | A05 Injection                                             | `input-validation`              |
| Injection & output encoding    | A05 Injection                                             | `injection-and-output-encoding` |
| SSRF & outbound fetch          | A01 Broken Access Control                                 | `ssrf-and-embeds`               |
| Access control & data exposure | A01 Broken Access Control, A02 Security Misconfiguration  | `privacy-and-exposure`          |
| Supply chain                   | A03 Software Supply Chain Failures                        | `supply-chain`                  |

## Secret and Environment-Variable Handling

See [secret-handling.md](./references/secret-handling.md) for:

- writing code that reads secrets through one env boundary and keeps them out of logs, telemetry, and client bundles
- reviewing a diff for a committed credential, a `process.env` access outside the whitelist, or a secret exposed through a client-prefixed env var
- keeping example env files and `.env.example` documentation honest without real values

## Input Validation

See [input-validation.md](./references/input-validation.md) for:

- parsing and coercing every request input at the boundary before it reaches the data layer, an outbound `fetch`, or a rendering pipeline
- treating route params, query params, bodies, and stored records as untrusted regardless of their static types
- reviewing a handler, server action, data-access function, or file upload for a missing runtime check

## Injection and Output Encoding

See [injection-and-output-encoding.md](./references/injection-and-output-encoding.md) for:

- encoding untrusted content per output context and rendering it only through the framework's safe sinks
- allowlisting URL schemes and sanitizing rich-text HTML when the format permits it
- reviewing a render component, custom node, or pipeline change for a raw-HTML sink or a bypassed encoding path

## SSRF and Outbound Fetch

See [ssrf-and-embeds.md](./references/ssrf-and-embeds.md) for:

- fetching a user- or CMS-controlled URL safely: allowlist over denylist, resolve-and-validate against reserved ranges, redirect and DNS-rebinding handling, tight timeouts
- the outbound-fetch triage diagram and the reserved-range / cloud-metadata reference table
- reviewing a new fetch caller, image host entry, metadata route, or mutation endpoint for an SSRF or CSRF gap

## Access Control and Data Exposure

See [privacy-and-exposure.md](./references/privacy-and-exposure.md) for:

- defaulting to the least data on public surfaces and gating unpublished, preview, and admin content behind an explicit check
- keeping internal identifiers, storage keys, and environment-derived values out of public responses, metadata, and analytics
- reviewing a diff for a public route, metadata generator, or localhost-gated path that leaks non-public data

## Supply Chain

See [supply-chain.md](./references/supply-chain.md) for:

- admitting a dependency deliberately: justified, maintained, platform-agnostic, lockfile-pinned, and installed without unvetted lifecycle scripts
- preferring a standard-library or platform API over a thin new dependency
- reviewing a manifest or lockfile change for an unjustified, heavyweight, or risky addition
