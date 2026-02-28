---
name: security-audit
description: Comprehensive security audit workflow for reviewing sensitive code and reporting credible security risks with clear attacker prerequisites and evidence. Use when users ask "is this secure?", "check for vulns", or want a security-focused review of authentication/authorization, payments, secrets, PII, file operations, or similar security-critical functionality (including single-file or code-snippet audits).
---

# Security Audit Workflow

Systematic security assessment that prioritizes CRITICAL/HIGH findings early, and optionally includes MEDIUM findings later (without letting them distract from higher impact work).

## How To Start (Natural Language)

Tell me what you want audited and provide the smallest useful scope:
- A whole repo or directory (where the entry points are)
- A specific area/module (what it does, what inputs it accepts)
- A single file (how it is called, what data flows into it)
- A code snippet (what file/function it belongs to, what types/inputs it receives)

If the scope is small (single file/snippet), explicitly list assumptions and what context would change the risk rating.

## Core Principles

- **Prioritize CRITICAL/HIGH early**: Do not let MEDIUM findings crowd out higher-impact issues
- **Evidence over volume**: Show attacker prerequisites and a source → sink chain (or other concrete evidence)
- **Explain token/secret claims concretely**: Do not treat "if attacker has token then ..." as a finding unless you show a feasible way to obtain the token
- **Safe verification**: If runtime verification is requested, test only localhost/authorized environments; avoid destructive/bulk actions
- **No fix recommendations by default**: In the audit report, describe risk and evidence; leave remediation to dev-team discussion unless the user explicitly asks for fix options

For deeper triage rules, analysis techniques, and consistent output formats, read:
- [references/deep-analysis.md](references/deep-analysis.md) - Library-specific analysis and bypass investigation
- [references/triage-and-prereqs.md](references/triage-and-prereqs.md) - Severity guidelines and prerequisite framework
- [references/report-templates.md](references/report-templates.md) - Consistent output formats

Optional helper scripts:
- `scripts/rg-hotspots.sh [path]`: quick, noisy hotspot discovery for common sinks/APIs to review (use as starting point, not final analysis)

## Audit Process

### Phase 1: Deep Static Analysis (Prioritize CRITICAL/HIGH)

Go beyond surface-level scanning (npm audit, basic pattern matching). Perform deep analysis:

**Core vulnerability classes** with required evidence (source → sink):
- **Injection attacks**: SQL/NoSQL, command/OS, template injection, SSRF, XSS
- **Authorization failures**: IDOR, missing checks, privilege escalation  
- **Authentication issues**: token validation, session management
- **Secret exposure**: hardcoded credentials, unsafe handling
- **Deserialization & file handling**: unsafe operations, path traversal

**Library-specific deep analysis** (when security libraries are used):
- **Understand protection mechanisms**: How does the library claim to prevent the vulnerability?
- **Investigate implementation**: Read the actual protection code, not just documentation
- **Test edge cases**: What inputs/patterns might bypass the protection?
- **Check assumptions**: What preconditions must hold for the protection to work?
- **Look for composition issues**: Does combining this library with others create gaps?

Examples of deep analysis:
- Prototype pollution protection: Can you bypass via constructor, __proto__ alternatives, or nested property access?
- XSS sanitizers: What encoding contexts are missed? Can you break out via attribute injection, CSS, or SVG?
- SQL injection prevention: Are there parameterization gaps in dynamic queries, JSON operators, or array handling?
- Path traversal protection: Can you bypass via URL encoding, Unicode normalization, or OS-specific path handling?

Each finding requires:
- Attacker prerequisites (position, capabilities needed)
- Complete source → sink chain with code references
- Analysis of why existing protections fail (if any)
- Minimal safe reproduction steps
- Concrete impact (what attacker gains)

### Phase 2: Runtime Verification (Only If Requested/Available)

When code is runnable (otherwise skip):
- Test only localhost/authorized environments
- Use repo-native commands (README, Makefile, Docker)
- Prove impact with 1-3 safe, deterministic steps
- Avoid destructive operations or bulk actions

### Phase 3: Secondary Pass (Optionally Include MEDIUM)

After the CRITICAL/HIGH pass is complete, optionally collect MEDIUM findings:
- Include MEDIUM only when the evidence is solid and the issue is realistically actionable
- Keep MEDIUM brief: enough to be useful, not a laundry list

If re-testing is requested (for example after changes), re-run the minimal repro steps and relevant tests/build checks.

## Common Noise (Skip Unless Chained)

Skip unless demonstrable path to material impact:
- CORS bypass without protected responses/state changes
- Missing rate limiting by itself
- Account enumeration without takeover path
- Timing attacks without feasible remote measurement
- Swagger/UI exposure in non-prod
- Token-type confusion without capability increase
- npm audit warnings without proof of exploitability in this codebase
- Generic pattern matching (grep for eval/exec) without source → sink analysis

**Surface-level scanning is not sufficient.** Tools like npm audit, Snyk, or basic grep patterns identify potential issues but don't prove exploitability. For each flagged issue:
- Trace the actual data flow (source → sink)
- Analyze whether existing protections are sufficient
- Test edge cases and bypass techniques
- Consider realistic attack scenarios

See [references/triage-and-prereqs.md](references/triage-and-prereqs.md) for detailed escalation criteria and [references/deep-analysis.md](references/deep-analysis.md) for library-specific analysis techniques.
