---
name: review
description: Use for evidence-backed review of diff-introduced defects in branches, PRs, WIP, or releases.
---

# Review

Review to HEAD. Keep one owner; explicit delegation. Do not edit, commit, push, or post.
Posting comments requires explicit intent.

## Review contract

- **Objective**: decide whether the diff achieves its outcome without a credible defect.
- **Guardrails**: diff-introduced only; keep standards separate from product/spec gaps;
  generated files are evidence.
- **Verification**: trace source. Dogfood every runnable change yourself at its real entrypoint;
  tests do not replace experience.
- **Stop**: account for every surface; findings need evidence, impact, priority, fix, and verification.

Ask only if the fixed point is missing. Otherwise set
`BASE=$(PR_BASE_REF="${REVIEW_BASE:-}" "${CLAUDE_PLUGIN_ROOT:-.}/scripts/resolve-pr-base.sh")`,
then inspect the complete diff and log.

## Evidence loop

**inspect -> verify -> classify -> synthesize.**

### Inspect

1. Read the request/spec, rules, complete diff, call sites, and behavior. Do not trust a PR summary over code.
2. For each changed assumption, reverse-trace it to authoritative producers, schemas,
   storage, consumers, and public surfaces. Search by domain concept, field, and emitted
   value, not only the changed symbol.
3. Test surprises against independent artifacts in relevant unchanged code, the base,
   recent history, runtime evidence, and fixtures. Compare fixtures with production shape.
4. Build one behavioral counterexample for a plausible collision. Map permissions and visible
   surfaces; skip formatter-owned style and pre-existing defects.
5. Ask what could still be wrong if tests pass.

### Verify

- Reproduce from source, schema, primary docs or an executable check.
- When safety hinges on one non-local fact, use `/blast-radius`; carry proof, not prose.
- With representative live-scale data, exercise the intended path and one credible failure or recovery path.
  Observe console/network/logs and response time; if unsafe or unavailable, name the blocker.
- Inspect test integrity: public behavior, RED, assertions, coverage, no duration waits.
  Source-text checks are no coverage unless text is public output; delete or replace at a
  public seam. Use static analysis for syntax.
- Challenge additions against required behavior, semantic density, domain clarity, credible
  risk, and demonstrated scale. Never optimize LOC or reward code golf.

Add surface-specific scrutiny only when the diff supplies evidence:

| Surface | Check |
|---|---|
| Customer-facing UI/CLI/report | Render, states, copy, keyboard/a11y, console, viewport |
| Security/privacy/data loss | Trust, authorization, secrets, injection, recovery |
| API/schema/SQL/PostgreSQL | Compatibility, migrations, generated output, actual dialect |
| Go/concurrency/workflows | Ownership, cancellation, races, retries, idempotency |
| Dependency/external API | Primary docs, versions, lockfile, advisories |

### Classify

A finding is diff-introduced, impactful, reproducible or concrete, placed on the tightest changed line,
and paired with the smallest safe fix.

- **P0**: exposure, data loss, outage, or impossible core flow.
- **P1**: user regression, broken contract, false success, or major a11y defect.
- **P2**: useful bounded correction with lower impact.
- Omit optional future work and polish from inline comments.

No performance finding without measurement or a structural bound. No edge-case finding
without credible risk. Evidence can support declining a candidate.

### Synthesize

Lead with findings. Deduplicate by root cause. State path, impact, correction, and verify
step; omit praise and narration. For a re-review, mark each prior finding's state.

## Deep mode

For `--deep`, use the same loop with a complete applicability ledger. Read
[DEEP-AUDIT.md](DEEP-AUDIT.md); cover all surfaces and do not add automatic agents.

## Output

Read [REFERENCE.md](REFERENCE.md) for vocabulary and schema. Report
`[P0|P1|P2] <file:line> <title> - <evidence, consequence, correction, verify command>`.
Append `entrypoint, data, actions, observations, timing, limits`, fixed point, mode, counts,
verdict, and residual limits. A clean review returns only verdict and residual limits.
