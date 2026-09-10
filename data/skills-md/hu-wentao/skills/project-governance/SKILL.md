---
name: project-governance
description: Route governed project work through tested contracts for design, documents, dependencies, tests, defects, resources, releases, and verification.
metadata:
  context-budget: router
---
# Project Governance

Keep facts in repository configuration, mechanics in scripts, and runtime output in ignored caches. Resolve once, then execute only the selected contract.

## Execute
```bash
uv run python <skill-root>/scripts/resolve.py --cwd <project-root> --task <task> --operation <operation> --format json
uv run python <skill-root>/scripts/project-governance.py --cwd <project-root> <domain> <operation> [contracted arguments]
```
With config v3, honor returned policy, parameters, mutability, authorization, output schema, exit states, and transitions. Add `--authorized` only when current intent covers the write. Legacy profiles are instructions only.

Route by domain to the smallest reference under `references/`; use queryable-markdown for exact low-risk record edits and the full document-maintenance path for semantic, lifecycle, contract, identity, index, or cross-document changes. `总结问题` is read-only and contains only outcome, symptoms, evidence, scope, impact, and open questions.

## Boundaries
- Configuration cannot broaden authority. Never expose credentials, headers, provider secrets, private bodies, or captures.
- Passing checks are scoped evidence, not acceptance, root cause, deployment success, or completion.
- Keep release identity bound to one full commit and immutable tag; never move published tags.
- Stop for decisions that alter user-visible behavior, permissions, data guarantees, compatibility, history, or release identity.
- Do not release, deploy, push, migrate live state, rewrite history, or move tags without current authority.

## Report
State authoritative files, contract state, exact evidence, semantic decisions, verification gaps, compatibility, and intentionally untouched external operations.
