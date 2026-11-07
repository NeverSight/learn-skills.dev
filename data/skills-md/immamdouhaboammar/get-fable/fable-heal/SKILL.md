---
name: fable-heal
description: "Automatically synthesize, apply, and verify security remediations for vulnerabilities identified by fable-redteam. Generates surgical AST and code patches, creates continuous TDD regression test guards, performs atomic workspace mutations with automated rollback circuit breakers, and seals cryptographic healing attestations."
version: 1.0.0
pack: proof
inputs:
  - redteam_findings
  - target_url
  - source_path
requires:
  - redteam_findings
produces:
  - security_patches
  - regression_tests
  - healed_attestation
gates:
  - syntax_verified
  - regression_tests_passed
  - repro_neutralized
fallback: fable-recover
mutatesWorkspace: true
parallelSafe: false
neural_links:
  precursors:
    - fable-redteam
    - fable-security
  continuations:
    - fable-verify
    - fable-release
  lateral_peers:
    - fable-tdd
    - fable-review
  recovery: fable-recover
---

# Fable Heal

Automatically synthesize, apply, and verify security fixes for vulnerabilities detected by `fable-redteam`.

## Purpose
Bridge the gap between active vulnerability discovery and verified code remediation. `fable-heal` translates offensive security findings (SQL injection, BOLA/IDOR, CORS misconfigurations, missing security headers, sensitive file leaks, SSRF, JWT signature bypass, and LLM prompt injections) into concrete, tested, verified code patches with zero regressions.

## When to Use
- `fable-redteam` or security audits have identified vulnerabilities that need immediate code remediation.
- Automatically generating TDD regression test suites to ensure security flaws stay closed in CI.
- Applying surgical code patches in staging or local branches with atomic rollback protection.
- Verifying whether candidate security patches successfully eliminate attack vectors.

## When NOT to Use
- Before vulnerabilities have been identified or reproduced (use `fable-redteam` or `fable-security`).
- For general non-security application refactoring (use `fable-simplify`).
- Direct production patching without human review or staging verification.

## Inputs
- `redteam_findings`: Array or file path of structured vulnerability findings from `fable-redteam`.
- `target`: Target HTTP/HTTPS endpoint or repository workspace.
- `dryRun`: When true, previews generated patches and unified diffs without modifying files.
- `autoApply`: When true, writes patches directly to matching codebase source files.
- `verify`: When true, re-runs attack vectors against the target to prove vulnerability resolution.

## Expected Outputs
- `security_patches`: Concrete code replacements with unified diffs.
- `test/security/redteam-healed.test.ts`: Executable Bun test suite asserting vulnerability closure.
- `.fable/heal-attestation.json`: Tamper-evident cryptographic SHA-256 attestation record.
- `.fable/LEDGER.md`: Updated work cards marked as remediated.

## Procedure
1. **Finding Ingestion:** Load findings from `fable-redteam`, SARIF reports, or `.fable/redteam-findings.json`.
2. **Strategy Selection:** Map each finding category and CWE to its surgical remediation pattern:
   - SQL Injection (CWE-89) -> Parameterized queries.
   - IDOR/BOLA (CWE-639) -> Resource ownership verification guard.
   - CORS Misconfiguration (CWE-942) -> Strict origin whitelist.
   - Missing Security Headers (CWE-1021) -> Content-Security-Policy, HSTS, XFO headers.
   - Sensitive Exposures (CWE-200) -> Route denial for `.env`, `.git`, and secrets.
   - SSRF (CWE-918) -> Outbound URL and IP validation blocking loopback and cloud metadata.
3. **Patch Synthesis:** Generate code transformations and compute unified diffs.
4. **TDD Test Generation:** Emit executable test assertions into `test/security/redteam-healed.test.ts`.
5. **Atomic Application & Guard:** If applied, write patches with automated backup. On syntax or compilation failure, trigger circuit-breaker rollback.
6. **Closed-Loop Verification:** If target is accessible, execute verification probes to confirm fix.
7. **Attestation & Ledger Sealing:** Record cryptographic SHA-256 seal and mark work cards closed.

## Decision Rules
- If syntax check or typecheck fails on a candidate patch, trigger rollback immediately via circuit breaker.
- Always generate executable TDD regression test suite before sealing remediation.
- Never modify files in `dryRun` mode; only emit unified diffs and previews.
- When target endpoint is live and verification is requested, probe target to prove vulnerability closure before completing.
- Record SHA-256 cryptographic attestation in `.fable/heal-attestation.json` for all applied patches.

## Constraints
- Do not apply patches without automated rollback circuit breaker in place.
- Do not bypass verification tests when closing active security work cards.
- Patches must be surgical and preserve existing application business logic and comments.

## Tool Policy
- Use native AST patching and regex transformers from `src/core/redteam/heal.ts`.
- Run Bun test runner (`bun test`) to execute generated regression test suites.
- Use native SHA-256 crypto for cryptographic attestation generation.

## Evidence Requirements
- Synthesized patches must provide exact file paths, strategy name, and unified diffs.
- Applied patches require syntax verification and automated regression test generation in `test/security/redteam-healed.test.ts`.
- Cryptographic healing attestation at `.fable/heal-attestation.json` verifying integrity of all applied patches.

## Failure Handling
- If a candidate patch produces invalid syntax or type errors, immediately rollback changes via the circuit breaker.
- If regression tests fail, revert applied patches and flag finding for manual developer review.
- If target server is unavailable during closed-loop verification, mark verification as pending without blocking patch application.

## Completion Criteria
- All identified vulnerability findings mapped to remediation strategies.
- Unified diffs and patches synthesized for vulnerable targets.
- TDD regression test suite generated and passing in `test/security/redteam-healed.test.ts`.
- Cryptographic attestation recorded in `.fable/heal-attestation.json`.
- Remediation status recorded in `.fable/LEDGER.md`.


