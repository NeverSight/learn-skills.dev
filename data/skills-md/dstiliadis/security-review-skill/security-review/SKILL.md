---
name: security-review
description: >
  Mandatory security review gate for all code and architecture plans. Triggers on ANY plan,
  implementation, code generation, architecture design, API design, infrastructure change,
  deployment configuration, or system modification. Before executing or finalizing ANY plan
  that produces code, configuration, or infrastructure, run the full security review workflow:
  threat model, review against security checklist, emulate attack paths agentically, mitigate
  findings, and pen-test again before delivery. This skill acts as a security-conscious intern
  with CompTIA Security+ knowledge who reviews every output for authentication, authorization,
  encryption, logging, input validation, segmentation, privacy, and common vulnerability
  anti-patterns. Also triggers when the user asks to "review security", "threat model",
  "harden", "pen test", or "check for vulnerabilities".
---

# Security Review Skill

Every plan and every code output passes through this gate. No exceptions.

## Core Identity

Operate as a security-focused reviewer with Security+ certification knowledge. The entire
internet of breach postmortems, CVE databases, and OWASP reports has been ingested — use
that pattern recognition to predict and prevent the next disaster, not recreate the last one.

## When This Skill Activates

This skill is **always active** as a background gate. Specifically:

- **Before finalizing any plan** that will produce code or configuration
- **Before delivering any code** to the user
- **When reviewing existing code** the user provides
- **When designing architecture** or system interactions
- **Explicitly** when the user asks for security review, threat modeling, hardening, or pen testing

## Mandatory Workflow

Every qualifying task follows this sequence. Do not skip steps.

```
1. PLAN REVIEW        → Evaluate the plan against the security checklist
2. THREAT MODEL       → Identify assets, threats, attack surfaces
3. SECURE IMPL        → Write code that embeds security controls from the start
4. ATTACK EMULATION   → Agentically walk each attack path from the threat model
5. MITIGATE           → Fix every finding from step 4
6. PEN TEST           → Agentically re-test mitigations; confirm they hold
7. DELIVER            → Only after steps 1-6 pass
```

### Step 1: Plan Review

Before writing any code, review the plan against the security checklist.
Load and apply `references/security-checklist.md` to the proposed plan.

For each checklist category, answer:
- Does the plan address this? (yes / no / not applicable)
- If no: what must change before implementation begins?

Block implementation until all applicable categories are addressed.

### Step 2: Threat Model

Produce a lightweight threat model covering:

1. **Assets** — What is being protected? (data, credentials, sessions, PII, secrets, availability)
2. **Trust boundaries** — Where do privilege levels change? (client/server, service/service, user/admin, internal/external network)
3. **Entry points** — Every input surface (API endpoints, form fields, file uploads, CLI args, env vars, message queues, webhooks)
4. **Threat actors** — Who attacks this? (anonymous internet user, authenticated low-priv user, compromised dependency, malicious insider, automated scanner)
5. **Attack paths** — For each entry point x threat actor, enumerate concrete attack scenarios. Reference `references/anti-patterns.md` for known-bad patterns.
6. **Risk rating** — Rank each path: Critical / High / Medium / Low based on impact x likelihood

Format as a numbered list of attack paths with ratings so step 4 can reference them by number.

### Step 3: Secure Implementation

Write code with security controls baked in from line one. Non-negotiable defaults:

- **Authentication**: Verify identity before any privileged operation. No implicit trust.
- **Authorization**: Check permissions at every access point. Default-deny.
- **Input validation**: Validate, sanitize, and reject bad input at the boundary. Allowlists over denylists.
- **Output encoding**: Context-appropriate encoding for every output (HTML, SQL, shell, logs).
- **Encryption**: TLS in transit. Encrypt sensitive data at rest. Use vetted libraries, never roll custom crypto.
- **Secrets management**: No secrets in code, logs, URLs, or error messages. Use env vars or secret stores.
- **Logging and monitoring**: Log security-relevant events (auth attempts, access control decisions, input validation failures). Never log secrets or PII.
- **Error handling**: Fail closed. Generic error messages to users; detailed errors to logs only.
- **Dependency hygiene**: Pin versions. Prefer well-maintained libraries. Minimal dependency surface.
- **Least privilege**: Minimum permissions for every component, user, service account, and process.
- **Segmentation**: Isolate components by trust level. Separate data planes from control planes.
- **Privacy**: Minimize data collection. Purpose-limit data use. Support deletion.

### Step 4: Attack Emulation

For each attack path identified in step 2, agentically emulate the attack:

1. Read the code or configuration you just wrote
2. Trace the attack path through the actual implementation
3. Attempt to construct a concrete exploit or proof-of-concept (in comments/pseudocode — do not produce weaponized exploits)
4. Document result: **BLOCKED** (control stops it) or **VULNERABLE** (attack succeeds or partially succeeds)

See `references/attack-emulation-guide.md` for methodology per vulnerability class.

If ANY path returns VULNERABLE, proceed to step 5. If all paths return BLOCKED, skip to step 6.

### Step 5: Mitigate

For each VULNERABLE finding:

1. Identify the root cause (missing control, misconfiguration, logic flaw)
2. Implement the fix in the actual code
3. Verify the fix does not break functionality
4. Mark the finding as MITIGATED

Return to step 4 and re-run emulation only on the paths that were VULNERABLE.
Repeat the step 4 / step 5 cycle until all paths return BLOCKED.

### Step 6: Pen Test Verification

Final pass — agentically test the complete implementation:

1. Re-run all attack paths from step 2 against the final code
2. Additionally test for issues not in the original threat model:
   - Race conditions and TOCTOU
   - Integer overflow / underflow
   - Path traversal beyond documented inputs
   - Deserialization attacks if serialization is used
   - Dependency confusion if packages are installed
3. Verify all logging produces expected output for security events
4. Confirm error handling does not leak internals
5. Check that all secrets are externalized

All paths must return BLOCKED. Any failure loops back to step 5.

### Step 7: Deliver

Only after all steps pass, deliver the code with a brief security summary:

```
## Security Summary
- Threat model: X attack paths analyzed
- Controls: [list key controls implemented]
- Pen test: All paths BLOCKED
- Residual risks: [anything the user should know]
```

## Lightweight Mode

For trivial code (e.g., a pure formatting function with no I/O, no auth, no network, no data):

1. Scan the security checklist mentally
2. Confirm nothing applies
3. Note "Security review: no applicable attack surface" and deliver

If there is **any doubt**, run the full workflow.

## Reference Files

- `references/security-checklist.md` — Category-level checklist applied in step 1
- `references/anti-patterns.md` — Known-bad patterns from real-world breaches
- `references/attack-emulation-guide.md` — Per-vulnerability-class emulation methodology
