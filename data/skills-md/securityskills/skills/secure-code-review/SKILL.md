---
name: secure-code-review
description: Perform a security-focused code review — map trust boundaries, audit input paths and auth flows, and use vulnerability-class-driven checklists instead of line-by-line skimming. Use on any PR or codebase with security implications.
---

# Secure Code Review

Review code for vulnerabilities systematically, not line-by-line.

## 1. Orient

- What does this code do? Identify: entry points, trust boundaries, data stores, privileged operations
- Read the tests — what invariants do they reveal?
- Check the diff's blast radius: auth logic? parsing? file handling? crypto?

## 2. Trace Untrusted Data

Follow each input from entry point to sink:

| Sink Class | What to Verify |
|---|---|
| SQL/NoSQL | Parameterized; no string-built queries; identifiers whitelisted |
| Command exec | No user data in shell strings; argv-array APIs; no shell=True |
| HTML/rendering | Contextual auto-escaping; raw/unsafe HTML flags justified |
| File paths | Basename/allowlist; canonicalize + prefix check; no user paths in includes |
| Deserialization | Typed formats (JSON) over object serializers; validation post-parse |
| Redirects | Relative-only or allowlisted targets |
| Eval/dynamic code | Justified and input-free, or rejected |

## 3. Audit Auth and Access Control

- Every endpoint enforces authz server-side; role checks at the resource, not the controller only
- Object-level checks (IDOR): does the query filter by the caller's tenant/user ID?
- Session management: rotation, invalidation, secure cookie flags
- Password reset flows: token entropy, expiry, single-use, no account enumeration

## 4. Audit Secrets and Config

- No hardcoded credentials/keys/API tokens; no secrets in logs or error messages
- Crypto: approved algorithms, library primitives (not hand-rolled), correct modes, random from CSPRNG

## 5. Race and State

- TOCTOU on file checks, check-then-use on quotas/credits
- Concurrency on mutable shared state; missing transactions on multi-step writes

## Communication

Report findings with severity, the specific code path, an exploit sketch, and a suggested fix. Distinguish "must fix" from "harden later."
