---
name: api-security-review
description: Comprehensive API security review against OWASP API Security Top 10 (2023). Use when reviewing OpenAPI/Swagger specs, auditing REST/GraphQL/gRPC implementations, testing authentication mechanisms, or checking API gateway configurations. Covers BOLA/IDOR, broken auth, mass assignment, rate limiting, SSRF, and more with real-world attack scenarios.
license: CC-BY-4.0
---

# API Security Review

Perform comprehensive API security assessment following `plays/api-security-review.md`.

## Steps

1. **Discovery & Reconnaissance**
   - Parse OpenAPI/Swagger specs or scan code for endpoints
   - Identify authentication mechanisms (JWT, OAuth 2.0, API keys, mTLS)
   - Map API gateway and middleware configurations
   - Enumerate all API versions and deprecated endpoints

2. **Authentication Deep Dive**
   - JWT security (algorithm confusion, weak signing, token expiration)
   - OAuth 2.0 flows (PKCE, state parameter, redirect URI validation)
   - API key exposure and rotation policies
   - Session management and token storage

3. **Assess All 10 OWASP API Risks** with attack scenarios:
   - **API1 BOLA** — IDOR via predictable IDs, batch endpoint bypasses, ownership verification gaps
   - **API2 Broken Authentication** — JWT attacks, OAuth flaws, brute force, credential stuffing
   - **API3 BOPA** — Mass assignment, response over-exposure, field-level authz bypasses
   - **API4 Resource Consumption** — Rate limit bypasses, pagination abuse, GraphQL DoS
   - **API5 BFLA** — Admin endpoint discovery, horizontal/vertical privilege escalation
   - **API6 Business Flows** — Automated abuse, inventory exhaustion, scraping attacks
   - **API7 SSRF** — URL bypasses, DNS rebinding, cloud metadata access
   - **API8 Misconfiguration** — CORS bypasses, verbose errors, missing headers
   - **API9 Inventory** — Shadow APIs, zombie endpoints, version confusion
   - **API10 Unsafe Consumption** — XXE, deserialization, webhook replay attacks

4. **Automated Testing**
   - Run API security scanners (OWASP ZAP, Burp Suite, Postman tests)
   - Test for common vulnerabilities with specific payloads
   - Validate rate limiting and throttling mechanisms

5. **API Gateway & Infrastructure Review**
   - Kong, nginx, Envoy, AWS API Gateway configurations
   - WAF rules and bypass opportunities
   - TLS configuration and certificate validation

## Output

Comprehensive API security report including:
- API surface inventory with authentication mechanisms
- Risk matrix with severity ratings for all 10 categories
- Detailed findings with proof-of-concept examples
- Exploit scenarios and business impact analysis
- Prioritized remediation roadmap with code examples
- Testing artifacts and vulnerability evidence

## OWASP References

- OWASP API Security Top 10 (2023)
- OWASP ASVS v5.0 — V13: API and Web Service
- OWASP Testing Guide: WSTG-APIT
- OWASP Cheat Sheet: REST Security, GraphQL Security, JWT Security, OAuth 2.0
