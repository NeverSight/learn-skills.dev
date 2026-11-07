---
name: nodejs-security
description: Audit Node.js and TypeScript backends for exploitable security weaknesses, authorization failures, unsafe configuration, data exposure, and resource or cost abuse; then recommend prioritized fixes and implement only the fixes the user selects. Use for backend security reviews, hardening, API abuse prevention, rate or request limits, security headers, secure logging, webhook review, or investigation of possible attack paths.
---

# Node.js Security

Operate audit-first. Inspect, explain, and recommend before modifying security-sensitive behavior. Implement only the findings or hardening actions the user explicitly selects.

## Keep communication concise

Before any write, package install, configuration change, migration, or state-changing command, give a proposal of no more than five short bullets: selected finding IDs, intended changes, affected areas, expected behavior change, and verification. Wait for confirmation and change only that scope. Do not repeat the full audit, paste long code blocks, or explain routine steps unless asked.

## Safety contract

- Default to read-only source, configuration, dependency, and safe local-runtime inspection.
- Do not run load tests, denial-of-service simulations, brute force, credential attacks, exploit payloads, destructive probes, or scans against a deployed target without explicit authorization and a clearly bounded target.
- Do not claim that a review catches every cyberattack. Distinguish confirmed vulnerabilities, hardening gaps, deployment-dependent risks, and unknowns.
- Never expose secrets, personal data, tokens, complete payment payloads, or weaponized exploit instructions in the report.
- Do not install middleware or change authentication, proxy, CORS, cookie, upload, caching, or timeout behavior before presenting the expected effect and receiving approval.

Read [references/audit-playbook.md](references/audit-playbook.md) before conducting an audit.

## Establish scope and trust boundaries

Inspect the backend framework, entrypoints, routes, middleware order, authentication, authorization, persistence, uploads, outbound requests, webhooks, jobs, queues, caches, logging, deployment/proxy configuration, secrets handling, and package manifests. Build a compact inventory of:

- public, authenticated, admin, internal, webhook, and health endpoints;
- actors and tenant boundaries;
- expensive operations and paid third-party calls;
- user-controlled input reaching databases, files, shells, templates, redirects, URLs, or provider SDKs;
- deployment assumptions that cannot be confirmed from code.

## Audit by abuse case

Check at least the applicable areas:

1. **Authentication and sessions**: credential enumeration, brute force protection, token verification, cookie flags, CSRF where cookies authorize state changes, logout/revocation, and recovery flows.
2. **Authorization**: deny by default, checks on every protected request, object ownership, function-level permissions, mass assignment, and cross-tenant access.
3. **Input and injection**: schema validation, parameterized queries, NoSQL operators, command execution, path traversal, unsafe deserialization, ReDoS, prototype pollution, and open redirects.
4. **Resource and cost abuse**: rate and concurrency limits, identity-aware quotas, JSON/form/header/upload limits, pagination and batch caps, execution and upstream timeouts, queue backpressure, AI/email/SMS/storage spending controls, caching abuse, and graceful overload behavior.
5. **Network and platform**: TLS assumptions, exact proxy trust, CORS allowlists, SSRF controls, webhook signature verification with raw bodies, protective headers, removal of unnecessary fingerprint headers, and safe error responses.
6. **Data and operations**: secret storage, encryption needs, least-privilege credentials, dependency exposure, log redaction, audit events, health/readiness endpoints, backups, and graceful shutdown.

Security headers should be configured intentionally, not hidden wholesale. For Express, remove unnecessary fingerprinting such as `X-Powered-By` and use Helmet with settings compatible with the API or pages being served.

## Report before fixing

For every finding, include:

- ID, severity, confidence, and category;
- evidence with file and line number;
- realistic attack or misuse path;
- impact and affected boundary;
- why current controls do not stop it;
- recommended fix and relevant official reference;
- expected compatibility or operational change;
- focused verification to run after the fix.

Rank exploitable findings above generic hardening. Avoid severity inflation. Group repeated instances under one root cause.

Finish the audit with a compact approval table: finding ID, severity, proposed action, and expected behavior change. Ask the user which items to implement. Keep detailed evidence available, but avoid repeating it in the summary. If the user requested only an audit, stop there.

## Implement selected work only

Reconfirm the selected IDs, make the smallest coherent changes, and add regression tests. Preserve provider-specific raw webhook parsing and document proxy-aware rate-limit behavior. Re-run focused tests, the full relevant suite, typecheck/build, and safe local checks.

Report completed fixes, verification evidence, residual risks, and any deployment controls the user must configure outside the repository.
