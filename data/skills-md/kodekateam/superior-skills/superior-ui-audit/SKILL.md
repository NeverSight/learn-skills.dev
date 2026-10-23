---
name: superior-ui-audit
description: Perform a read-only audit of an existing product interface, prove UI findings from governing design evidence and runtime paths, and prepare implementation-ready recommendations or plans. Use for review and design-system drift analysis; do not use when the user asks to implement fixes directly.
---

# Superior UI Audit

Audit one coherent product surface against the system that actually governs it. Prefer a small set of well-proven findings to a long list of stylistic opinions.

## Boundaries

- Treat product source as read-only.
- Do not install dependencies, format files, or modify generated artifacts while auditing.
- Render or interact with the UI only when requested or when available read-only tooling makes it necessary to prove a visual claim.
- Keep functional bugs, accessibility defects, performance issues, and code quality outside the report unless the user includes them in scope.
- If the user asks to fix the UI, this audit skill does not override that request; use the implementation workflow instead.

## Trace the surface

Start from the route, screen, component family, or user journey in scope. Follow the actual path through layouts, compositions, components, variants, tokens, and resolved styles. Similar names and nearby files are candidates, not proof that an owner affects the surface.

Record the surface, relevant owners, design sources, explicit exceptions, and the current revision when available.

## Reconstruct the local contract

Use current, governing evidence only:

- accepted design or brand documentation;
- shipped tokens and component contracts;
- representative surfaces proven to share ownership;
- direct contradictions within one user journey;
- rendered evidence supplied or inspected for this audit.

Drafts and proposals describe future intent unless the repository marks them as accepted. Missing documentation is not itself a UI defect.

## Prove each finding

A finding survives only when it has:

1. **Observation:** an exact interface consequence on the selected surface;
2. **Contract:** evidence showing what should govern that property;
3. **Connection:** proof that the cited owner reaches the affected surface;
4. **Correction:** one determined change that does not invent product intent.

Reject a candidate when the evidence supports multiple incompatible fixes, the difference is an intentional exception, or the proposed correction primarily changes business behavior.

Re-open the cited sources and actively look for counterevidence before reporting.

## Report

Return no more than five findings, ordered by user impact, confidence, reach, and correction cost:

```markdown
## Audit scope
- Surface:
- Governing evidence:
- Runtime owners:
- Explicit exceptions:

## Findings
| # | Observed problem | Evidence and connection | Required correction | Reach | Confidence |
|---|---|---|---|---|---|

## Highest-leverage change
<One finding, or “No supported recommendation.”>
```

If nothing passes the proof test, say so plainly. Do not pad the report.

## Plan selected work

When the user selects a finding or explicitly requests a plan, read [references/change-plan.md](references/change-plan.md). Write one self-contained plan per root correction. The executor must not need the audit conversation to understand ownership, scope, preservation requirements, or validation.
