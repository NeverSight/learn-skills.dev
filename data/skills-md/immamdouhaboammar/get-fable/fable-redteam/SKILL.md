---
name: fable-redteam
description: "Execute native agentic ethical penetration testing and automated security audits against staging or authorized application targets. Discovers API logic flaws, BOLA/IDOR vulnerabilities, missing authentication, sensitive file exposures, and security misconfigurations within bounded scope. Produces verified security findings with reproduction PoCs and automatic Fable remediation work cards."
version: 1.0.0
pack: proof
inputs:
  - target_url
  - scan_profile
requires:
  - target_in_scope
produces:
  - redteam_findings
  - remediation_cards
gates:
  - scope_verified
  - non_destructive_mode
fallback: fable-security
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - fable-security
    - fable-verify
  continuations:
    - fable-plan
    - fable-tdd
  lateral_peers:
    - fable-security
    - fable-review
  recovery: fable-recover
---

# Fable RedTeam

Execute safe, bounded, agentic ethical penetration testing and active vulnerability discovery.

## Purpose
Provide an automated, reproducible offensive security audit engine to prove whether application defenses withstand real-world attack vectors. `fable-redteam` verifies API authentication, authorization boundaries, object isolation, and sensitive exposures in authorized staging/local environments, producing immediate remediation cards for implementation.

## When to Use
- Active security testing is needed for local, staging, or authorized test targets.
- Verifying whether API endpoints enforce authentication and authorization (BOLA/IDOR).
- Testing for CORS misconfigurations, missing security headers, or leaked `.env` files.
- Simulating attacker-controlled requests against staging endpoints before release.
- Validating whether a previously applied security patch truly eliminates the vulnerability.

## When NOT to Use
- Pure static code review or threat modeling without live target endpoints (use `fable-security`).
- Functional test runs or assertion checking without security probing (use `fable-verify`).
- Unauthorized public targets outside the explicitly configured scope.
- Stress testing or denial-of-service simulations (strictly out of scope).

## Inputs
- `target`: Target HTTP/HTTPS URL or local repository path.
- `profile`: Scan depth (`passive`, `api-logic`, `comprehensive`, `orchestrated`, `playbook`, `audit`).
- `scopeConfig`: Optional custom scope JSON (defaults to `.fable/redteam.json` or local safe defaults). Supports `allowedCidrs`, `maintenanceWindow`, and automatic cloud metadata protection (`169.254.169.254`).
- `authToken`: Optional Bearer token for authenticated API probes.
- `baseline`: Optional path to prior `.fable/redteam-findings.json` for regression diffing.
- `failOnCvss`: Optional numeric CVSS v3.1 threshold (e.g. 7.0) to exit with status code 1 on CI/CD security violations.
- `suppress`: Optional list of finding fingerprints or IDs to ignore.

## Operating Modes
- **Guidance Mode:** For targeted security queries, threat modeling, architecture review, or verifying a specific candidate finding. Does not write comprehensive audit artifacts or run all phases.
- **Full Audit Mode:** Complete 6-phase audit workflow across all attack surfaces, writing deterministic coverage ledgers and verified findings schemas. Triggered via `get-fable redteam audit` or `--profile audit`.

## Expected Outputs
- `redteam_findings`: Array of validated vulnerability findings with CWE IDs, automated CVSS v3.1 vectors, numeric base scores, compliance taxonomy tags, and reproduction curl commands.
- `docs/security/REDTEAM_REPORT.md`: Comprehensive Markdown audit report with executive risk scorecard (A-F), MTTR estimate, and finding breakdowns.
- `docs/security/REDTEAM_REPORT.sarif`: OASIS SARIF v2.1.0 report for GitHub Advanced Security and enterprise SIEM/SOAR ingestion.
- `findings.json`: Machine-readable structured findings adhering strictly to `report-schema.json`, categorized by verdict (`confirmed`, `needs_validation`, `rejected`).
- `coverage-ledger.json`: Deterministic coverage ledger mapping checked surfaces and canonical RFC 3986 percent-encoded coverage IDs.
- `architecture.md`: Source-grounded threat boundary and component architecture map.
- `FINDINGS-DETAIL.md`: Detailed source traces, reproductions, and minimal effective code fixes.
- `NEEDS-VALIDATION.md`: Source-grounded leads requiring unobserved deployment facts with safe validation plans.
- `.fable/run-attestation.json`: Cryptographic SHA-256 tamper-evident attestation record.
- `remediation_cards`: Actionable Fable work cards ready for `.fable/LEDGER.md`.

## Procedure
1. **Scope Preflight:** Verify the target URL against allowed host patterns, CIDR subnets, and excluded paths. Enforce cloud metadata guard (`169.254.169.254`) and active maintenance windows. Fail closed immediately if target is out of scope.
2. **Phase 1 — Reconnaissance & Threat Modeling:** Map architecture, lower-trust principals, authorization boundaries, entry surfaces, and execution sinks into `architecture.md` and seed `coverage-ledger.json`.
3. **Phase 2 — Coverage-Led Hunting:** Iterate ledger units across attack classes (Auth, IDOR, Injection, SSRF, Memory Safety, LLM, Supply Chain) with isolated hunter checks.
4. **Phase 3 — Adversarial Candidate Validation:** Subject every candidate to an independent verifier trying to disprove it. Classify findings strictly into:
   - `confirmed`: Complete source trace and demonstrated bounded observed result.
   - `needs_validation`: Source-grounded lead blocked by an unobserved deployment fact, with safe local and deployment plans.
   - `rejected`: Disproved candidate with explicit refutation rationale.
5. **Phase 4 — Structured Output & Schema Validation:** Write `findings.json` sorted by fingerprint and validate against `report-schema.json` using zero-dependency validator `validateFindings()`. Validate coverage ledger via `validateCoverageLedger()`.
6. **Phase 5 — Independent Record Verification:** Verify final source claims, file line citations, and stable fingerprints without mixing evidence.
7. **Phase 6 — Target-Neutral Reporting & Remediation:** Generate `REPORT.md`, `FINDINGS-DETAIL.md`, and `NEEDS-VALIDATION.md`. Convert validated findings into actionable remediation work cards for `.fable/LEDGER.md` and automated regression tests.

## Decision Rules
- If a target host does not match `allowedHosts`, `allowedCidrs`, or loopback defaults, refuse execution immediately without network calls.
- If target resolves to cloud instance metadata (`169.254.169.254`), abort immediately.
- If `safe-mode` is active, never execute database-dropping SQL payloads or unbounded fuzz loops.
- If circuit breaker trips to OPEN state, abort probe operations gracefully and report partial findings.
- If `--fail-on-cvss` is set and any unsuppressed finding meets or exceeds the threshold, exit with non-zero failure status for CI/CD gates.
- When all findings are resolved, transition to `fable-verify` or `fable-release`.

## Tool Policy
- Use native TS HTTP probe (`src/core/redteam/probe.ts`) for zero-dependency execution across any host.
- Use native Cloudflare Audit Adapter (`src/core/redteam/adapters/cloudflare.ts`) and Audit Engine (`src/core/redteam/audit/engine.ts`) for 6-phase coverage-led audits and `report-schema.json` compliance.
- Reference the 14 specialized attack-class domain guides in `skills/fable-redteam/references/cloudflare/` (`AI-AND-LLM.md`, `WEB-PROTOCOL-AND-AUTH.md`, `CLIENT-SIDE.md`, etc.).
- Optional external tools (Nuclei, Nmap, FFuf, Akto, HexStrike, CyberStrike, PentAGI, PentestAgent) may be orchestrated via adapters when available.
- Never write credentials or sensitive data into git-tracked files or public logs.

## Evidence Requirements
- Findings must include the exact target URL, HTTP status code, CVSS v3.1 vector/score, compliance tags, and reproducible `curl` commands.
- Repaired vulnerabilities require a negative re-scan proving the attack vector now returns 401/403/404.
- Cryptographic run attestation verifies findings integrity.

## Failure Handling
- On network connection errors or target timeouts, record the failure as an unresolved endpoint rather than a false negative.
- If rate limits are encountered, throttle request frequency or pause execution with backoff.
- On repeated target server errors, trigger the circuit breaker to prevent cascading denial-of-service.

## Completion Criteria
- Complete execution of the selected scan or audit profile.
- Generated Markdown report at `docs/security/REDTEAM_REPORT.md` and SARIF at `docs/security/REDTEAM_REPORT.sarif`.
- When in audit mode, generated `findings.json`, `coverage-ledger.json`, and `architecture.md` passing schema validation.
- Generated run attestation at `.fable/run-attestation.json`.
- Remediation work cards formatted for `.fable/LEDGER.md`.

