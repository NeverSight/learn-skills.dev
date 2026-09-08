---
name: "code-review"
description: "Review a runner candidate or standalone PR, commit, local diff, or requested scope read-only for regressions, evidence gaps, and overclaims."
---

# Code Review

Owns: read-only review findings for one frozen scope. It never edits files, runs a quality
loop, produces a Verification Record, decides the final claim ceiling, or mutates
Git/provider state.

Use the semantic vocabulary and required fields from the canonical
[Verification Record](../verification-audit/references/verification-record.md). Flag
missing or contradictory inputs; do not reconstruct a second evidence/gate policy.

## Inputs

Accept one acquisition route:

- **Runner handoff:** frozen diff, CandidateRef, normalized Ticket Envelope, acceptance
  criteria, decisions, baseline, observed evidence, and draft record when one exists.
- **Standalone acquisition:** acquire a PR, commit, local diff, or user-requested scope
  read-only; record its observed head/commit/worktree identity, request constraints,
  relevant repository rules, and available baseline/evidence.

Do not parse Markdown to infer a Ticket Envelope. If standalone context has no normalized
ticket, review against the explicit request and repository contract. If the diff changes,
return `stale-candidate` and stop.

## Volatile intake bound

- `max_volatile_bytes`: `107656` normalized UTF-8 bytes per invocation. This is the
  observed 96,393-byte candidate-diff high-water mark plus maxima of 2,380 bytes for the
  ticket body, 4,459 for the implementation handoff, and 4,424 for simplification. The
  corpus is the run's TK-01/TK-02/TK-05/TK-07/TK-08 normalized
  `git diff --no-ext-diff --no-color` observations, its nine ticket bodies, and compact
  leaf results.
- `max_single_output_bytes`: `32596`, the observed TK-02 executable-code candidate diff.

Count every diff, raw file slice, pasted handoff, evidence body, and tool result after CRLF
or lone-CR normalization to LF. Acquire the expected manifest first; truncate command
output before it enters context and continue larger diffs by file or hunk. Prefer path plus
SHA-256 references over pasted artifacts, loading referenced content only when a review
axis requires it. If the next required read would exceed a cap, return a schema-3 partial
result with exact inspected/remaining scope and `budget-exhausted`; do not skip scope or
downgrade a finding to fit the bound.

## Bounded runner handoff

When the runner supplies a schema-3 bounded `LeafContext`, treat its
CandidateRef, canonical phase contract, expected file manifest, prior
inspection, remaining scope, and resource limits as the authoritative
continuation boundary. Do not rediscover already-inspected immutable scope for
the same CandidateRef.

End every runner-owned review turn with one schema-3 result, including timeout,
interruption, or resource exhaustion. Persist the exact CandidateRef and review
phase contract, ordered expected/inspected/remaining files, commands, findings,
current phase, canonical remaining-phase suffix, and a non-empty stop reason
for partial results.

Include normalized schema-3 `execution` from the observed route. A shared-context or
unknown isolation is not independent; report that limitation instead of upgrading it.

A complete review must reach `handoff-ready`, inspect the declared scope, and
return a validated structured finding list. A partial result is usable
continuation state but never a pass. A real finding may return the pipeline to
implementation and consume a quality failure; timeout, interruption, and
resource exhaustion do not. CandidateRef drift invalidates the handoff.

## Review axes

Review each axis separately and report only evidence-backed findings:

1. **Standards and maintainability** — project conventions, clarity, accidental
   complexity, unsafe error handling, security, data integrity, and unrelated scope.
2. **Ticket acceptance** — every criterion has a concrete implementation path and
   observable check; non-goals remain untouched.
3. **Semantic regression** — externally meaningful behavior is preserved or explicitly
   authorized. Compare changed boundaries and invariants to the supplied baseline.
4. **Causal coverage** — tests/evidence exercise the changed mechanism, not merely an
   adjacent success path. Identify mocked or simulated boundaries explicitly.
5. **Claim safety** — wording does not exceed the evidence and open gates represented in
   the canonical record.

Inspect raw files and diffs rather than trusting summaries. Do not call
`verification-audit`; the caller supplies findings to its single audit pass.

## Finding format

Sort by severity:

```text
[blocker|should-fix|nit] path:line - problem and impact. Suggested fix.
```

- `blocker`: correctness, security, data loss, ticket failure, missing causal coverage, or
  a material unsupported claim.
- `should-fix`: meaningful maintainability or non-critical coverage problem.
- `nit`: optional polish only.

For every finding, name the violated acceptance criterion, invariant, boundary item, or
repository rule when available. If no finding exists, say so and list residual evidence
limits. A standalone output is a read-only draft; it cannot claim ticket completion or release.
Never report PASS for a CandidateRef or standalone scope you did not inspect.
