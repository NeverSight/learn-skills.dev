---
name: high-risk-review
description: Apply enhanced verification (CoVe-like review, security/arch/perf checks, targeted web research) for high-risk tasks or uncertainty. Use for security, infra, data loss risk, major refactors, or when facts may be outdated.
compatibility: Requires web access for research and ability to run lightweight checks.
allowed-tools: Bash(*) Read WebSearch(*)
metadata:
  intent: Avoid meta-process on trivial answers; focus on risk triggers.
---

# high-risk-review

## Activation gate (anti-noise)
Activate if:
- Security/auth/crypto, infra, permissions, data loss, performance hot paths.
- Uncertain or time-sensitive facts.
- User asks to “zweryfikuj / upewnij się”.

## Procedure
1. Draft solution.
2. Identify 3–5 highest-impact claims/assumptions.
3. Verify independently:
   - Repo evidence (if applicable)
   - Minimal test commands
   - Web research (authoritative sources)
4. Revise solution and mark remaining uncertainties.

## Output
- Final recommendation + explicit verification steps.
