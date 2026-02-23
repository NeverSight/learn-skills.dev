---
name: housekeeping
description: Repository housekeeping workflows for AGENTS/CLAUDE architecture, progressive disclosure, and migration of legacy monolithic instruction files.
---

# Housekeeping (AGENTS/CLAUDE Architecture)

Use this skill when work is about organizing or modernizing `AGENTS.md`/`CLAUDE.md` context systems.

## Operating rules
- Keep root `AGENTS.md` concise: critical guardrails, task router, canonical commands, and links.
- Prefer scoped instruction files in dense areas (`apps/frontend`, `infra`, `apps/agent`, etc.).
- Move deep or volatile details into `.agents/repo-context/*`, not root `AGENTS.md`.
- Curate continuously: deduplicate, resolve contradictions, and remove stale guidance.
- Preserve behavior intent during migrations; change structure first, then tighten wording.

## Workflow
1) Assess current state (concise router vs mixed/legacy monolith).
2) Select target architecture from references.
3) Migrate content into scoped `AGENTS.md` files and deep docs.
4) Rewrite root `AGENTS.md` as a short router.
5) Add freshness metadata for volatile facts where feasible.
6) Verify links/routes and remove conflicting duplicate rules.

## Reference triggers (open when clearly relevant)
- AGENTS/CLAUDE architecture, progressive disclosure, or context-memory organization -> `skills/housekeeping/references/agents-architecture.md`
- Legacy monolithic AGENTS cleanup, contradiction pruning, or migration planning -> `skills/housekeeping/references/migration-playbook.md`

## References
- `skills/housekeeping/references/index.md` - References index for this skill
- `skills/housekeeping/references/agents-architecture.md` - Target architecture, file tree, and root template
- `skills/housekeeping/references/migration-playbook.md` - Legacy-to-modern migration workflow and checklist
