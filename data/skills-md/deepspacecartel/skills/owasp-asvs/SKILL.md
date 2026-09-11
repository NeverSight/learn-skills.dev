---
name: owasp-asvs
description: How to apply and reference the OWASP Application Security Verification Standard (ASVS) v5.0.0 (https://owasp.github.io/www-project-application-security-verification-standard/) - project-agnostic. Covers the three verification levels (L1/L2/L3) and how to pick one, the 17 requirement chapters (encoding, validation, frontend, API, file handling, authentication, session management, authorization, tokens, OAuth/OIDC, cryptography, secure communication, configuration, data protection, secure coding, logging, WebRTC), the `<chapter>.<section>.<requirement>` numbering and versioned-reference format, documentation requirements vs. implementation requirements, and how compliance is actually verified. Use when designing an application's security controls, deciding which security requirements apply to a feature or codebase, writing or reviewing a security requirements checklist, mapping findings to ASVS requirement IDs, or assessing/reporting ASVS compliance.
---

# OWASP Application Security Verification Standard (ASVS)

A catalog of ~350 application security requirements maintained by OWASP,
used as a checklist for building, testing, and procuring secure software.
Current version: **5.0.0** (released May 2025). Full text and all formats
(PDF/Word/CSV/JSON) at
[github.com/OWASP/ASVS](https://github.com/OWASP/ASVS/tree/master/5.0).

ASVS is not prescriptive about *how* to implement a control — that's the
[Cheat Sheet Series](https://cheatsheetseries.owasp.org/) — and not
prescriptive about *how* to test one — that's the Web Security Testing
Guide. ASVS only states the security outcome that must be true.

## What counts as a requirement

Every entry must satisfy all four words in the name:

- **Application** — scoped to the software product itself, not CI/CD,
  hosting, or operational process around it. Components that serve or
  filter HTTP traffic (WAFs, proxies, load balancers) count when a
  control depends on them (rate limiting, cached responses).
- **Security** — must have a demonstrable security impact; omitting it
  must make the application less secure. Functional or style concerns
  are out of scope.
- **Verification** — must be checkable to a clear pass/fail.
- **Requirement** — stated as "must," not "should." ASVS doesn't contain
  recommendations or list multiple valid options; "must" language that
  actually describes one-of-several-options is a smell that the
  wording needs to move up to a documentation requirement instead (see
  below).

## The three levels

Levels are cumulative and priority-ordered by risk-reduction-per-effort,
not by requirement number:

| Level | ~Share of requirements | Cumulative | Who it's for |
|---|---|---|---|
| **L1** | ~20% | ~20% | Minimum baseline for any application. First-layer defenses against attacks that need no precondition — the goal is as *few* requirements as possible to keep the barrier to entry low. Not reliably black-box-penetration-testable. |
| **L2** | ~50% | ~70% (L1+L2) | What most applications handling meaningful data should target. Less common attacks, or protections that need a precondition, or more complex versions of L1 controls (e.g. MFA superseding L1's password-only rules). |
| **L3** | ~30% | 100% | High-assurance applications (e.g. banking). Defense-in-depth and harder-to-implement controls. |

Pick a level from the application's own risk profile and user
expectations — ASVS deliberately does not mandate one. Start at L1 and
move up; don't try to reverse-engineer which level a specific requirement
"belongs to" from its number or section — level is called out per
requirement in the standard's own tables (source markdown, CSV, or JSON
export), not derivable from the ID.

Organizations are explicitly encouraged to **fork** ASVS into an
org-specific profile: drop whole chapters that don't apply (e.g. OAuth,
GraphQL, WebRTC if unused) and pick a level per remaining chapter based
on that chapter's actual risk — as long as requirement IDs stay
traceable back to upstream ASVS numbers.

## Requirement IDs and how to cite them

Format: `<chapter>.<section>.<requirement>`, e.g. `1.2.5` = chapter 1
(Encoding and Sanitization), section 2 (Injection Prevention), 5th
requirement in that section ("protects against OS command injection...").

IDs can shift between ASVS releases, so anything durable (a report, a
ticket, a code comment) should cite the **versioned** form:
`v<version>-<chapter>.<section>.<requirement>` — e.g. `v5.0.0-1.2.5`.
An unversioned ID is read as "latest ASVS." The `v` is always lowercase.

Release semantics (semver-shaped, see [[semver]] for the general rules):
- **Major** (`4.0.3` → `5.0.0`): full reorganization, requirement numbers
  can move, full re-evaluation needed.
- **Minor** (`5.0.0` → `5.1.0`): requirements added/removed, numbering
  otherwise stable, re-evaluation needed but lighter.
- **Patch** (`5.0.0` → `5.0.1`): requirements only removed or relaxed —
  anything compliant with the previous patch stays compliant.

## Documentation requirements vs. implementation requirements

Some controls are too application-specific for ASVS to state as a fixed
rule (allowed file types, business-rule limits, which fields need what
validation). For these, ASVS instead requires that the organization
**document** its own decision, which is then checked for
appropriateness — separately from checking that the implementation
matches what was documented. These always live in the first section of
a chapter (`<chapter>.1`, e.g. `6.1` Authentication Documentation),
when a chapter has them, and pair with a later implementation
requirement that enforces the documented decision. Treat "no
documentation" as a fail on its own, independent of whether the
implementation looks reasonable.

## The 17 chapters

Chapter numbering is stable across the whole standard; sections within a
chapter are listed in [`references/chapters.md`](references/chapters.md).

| # | Chapter | Covers |
|---|---|---|
| V1 | Encoding and Sanitization | Output encoding, injection prevention (SQL/OS/LDAP/XPath/LaTeX/regex/CSV), sanitization, unsafe memory, safe deserialization |
| V2 | Validation and Business Logic | Input validation, business-logic abuse (sequencing, limits, race conditions), anti-automation |
| V3 | Web Frontend Security | Content-type sniffing, cookie flags, CSP/security headers, CORS/origin isolation, subresource integrity |
| V4 | API and Web Service | REST/generic web service security, HTTP message structure validation, GraphQL, WebSocket |
| V5 | File Handling | Upload validation, storage, download, path traversal |
| V6 | Authentication | Passwords, general auth security, MFA, out-of-band and cryptographic authenticators, IdP-based auth (loosely follows NIST SP 800-63B) |
| V7 | Session Management | Session token security, timeout, termination, session-abuse defenses, federated re-auth |
| V8 | Authorization | Authorization design, operation-level (object/function) authorization |
| V9 | Self-contained Tokens | JWT-style token source/integrity and content requirements |
| V10 | OAuth and OIDC | OAuth client/resource-server/auth-server roles, OIDC client/OP roles, consent management |
| V11 | Cryptography | Crypto inventory, implementation hygiene, encryption/hashing/RNG/public-key choices, in-use data crypto |
| V12 | Secure Communication | TLS guidance, HTTPS for external-facing services, service-to-service transport security |
| V13 | Configuration | Backend communication config, secret management, unintended information leakage |
| V14 | Data Protection | Sensitive-data handling, client-side data exposure |
| V15 | Secure Coding and Architecture | Architecture/dependency hygiene, defensive coding, safe concurrency |
| V16 | Security Logging and Error Handling | What to log, security events, log protection, safe error handling |
| V17 | WebRTC | TURN server, media, and signaling security |

Filter chapters by what the application actually does before applying a
level: a machine-to-machine API skips V3 (frontend); an app with no
OAuth/OIDC skips V10; no WebRTC means skip V17 entirely, rather than
recording those requirements as failing.

## How compliance is actually verified

OWASP does not certify anyone — a vendor or auditor claiming "OWASP
ASVS-certified" is not an OWASP endorsement. See
[`references/assessment.md`](references/assessment.md) for the full
guidance; in short:

- A real assessment reports **all** requirements checked, not just
  failures (unlike exception-only pentest reports), including which
  ones were marked not applicable and why.
- Running a DAST/SAST tool is not, by itself, verification — automation
  covers the mechanical requirements (output encoding, some injection
  checks) but not business-logic, access-control, or documentation
  requirements. Application-specific tests (unit/integration-style,
  crafted per requirement) are the recommended way to make higher
  levels continuously verifiable.
- Black-box pentesting without access to docs/source is explicitly
  discouraged as an assurance activity — hybrid, documentation- and
  source-informed testing is the standard's actual recommendation, and
  is close to required for L2/L3.

## Gotchas

- Requirement numbers are **not** stable across major versions — never
  hardcode `4.0.3`-era numbers in tooling or reports; always pair a
  number with its version (`v5.0.0-6.2.1`, not bare `6.2.1`). A
  `mapping_v4.0.3_to_v5.0.0.yml` table ships in the ASVS repo's
  `5.0/mappings/` directory for migrating old references.
- L1/L2/L3 is a *minimum bar per level*, not a partition — L2 compliance
  means all L1 **and** all L2 requirements, not just the ones labeled L2.
- A chapter with no relevant functionality in your app (no GraphQL, no
  WebRTC, no OAuth) should be excluded from scope with a stated reason,
  not silently marked failing or silently skipped without a note in the
  report.
- Don't treat "should" language anywhere in ASVS prose as a requirement
  — only the numbered, "Verify that..." table rows are requirements;
  everything else is explanatory context.
- CWE mappings and the raw requirement list are published in machine-
  readable form (`v5.0.be_cwe_mapping.json`, CSV/JSON exports) — prefer
  those over re-typing requirement text when building tooling.
