---
name: pseo-orchestrate
description: Orchestrate the full programmatic SEO implementation by coordinating all pseo-* skills in the correct order. Use when implementing pSEO from scratch, running the full pSEO pipeline, or when the user asks to "set up programmatic SEO" or "build pSEO pages" without specifying a single skill.
argument-hint: "[mode: full | discover-only | audit-only | implement | validate]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Orchestrator

Coordinate the execution of all pseo-* skills in the correct dependency order to implement or validate a complete programmatic SEO system.

## Skill Dependency Graph

```
pseo-discovery (0)    ← what should we build? what data exists?
    │
    ▼
pseo-audit (1)        ← is the codebase ready for what we want to build?
    │
    ▼
pseo-scale (1.5)      ← CONDITIONAL: only if 10K+ pages planned
    │
    ▼
pseo-data (2)
    │
    ├──────────────┐
    ▼              ▼
pseo-templates (3) pseo-linking (4)
    │              │
    └──────┬───────┘
           │
    ┌──────┴───────┐
    ▼              ▼
pseo-metadata (5)  pseo-schema (6)    ← parallel: both read from data layer
    │              │
    └──────┬───────┘
           │
    ┌──────┴───────┐
    ▼              ▼
pseo-performance   pseo-llm-visibility   ← parallel: independent optimizations
    (7)            (8)
    │              │
    └──────┬───────┘
           ▼
pseo-quality-guard (9)
```

**Note:** metadata and schema are independent of each other — both read from the data layer and render into templates. Run them in parallel in Phase 4.

**Note:** pseo-scale only applies when discovery identifies 10K+ pages. It runs after audit to set up database infrastructure, data sufficiency gating, and CDN architecture before the data layer is built. At < 10K pages, skip it entirely.

## Execution Modes

### `full` (default)
Run the complete pipeline: discover → audit → implement → validate.

### `discover-only`
Run only pseo-discovery. No code changes. Use when the user doesn't yet know what to build.

### `audit-only`
Run pseo-audit and pseo-quality-guard. No code changes. Assumes discovery is done.

### `implement`
Skip discovery and audit, go straight to implementation (assumes both were already done).

### `validate`
Run only pseo-quality-guard against the existing implementation.

## Full Pipeline Procedure

### Phase 0: Discovery
1. Run **pseo-discovery** with scope `all`
2. Present the discovery report: data assets found, proposed page types, rejected candidates
3. Ask the user to confirm which page types to pursue
4. If data enrichment is needed, flag it — implementation cannot produce quality pages without sufficient data

### Phase 1: Audit
5. Run **pseo-audit** with scope `full`, informed by the discovery output (what page types are planned)
6. Present findings to the user
7. Ask the user to confirm which areas to implement
8. Create a prioritized implementation plan based on audit results

### Phase 1.5: Scale Infrastructure (conditional — 10K+ pages only)
9. Run **pseo-scale** to set up database, sufficiency gating, CDN, and monitoring
10. Migrate existing data to database if moving from file-based storage
11. Compute data sufficiency scores and gate thin combinations

### Phase 2: Data Foundation
12. Run **pseo-data** to set up or refactor the data architecture
13. Verify data layer exports are complete and typed
14. Validate slug uniqueness and data integrity

### Phase 3: Page Structure (parallel where possible)
15. Run **pseo-templates** to create or refactor page templates and routing
16. Run **pseo-linking** to build internal linking, breadcrumbs, and hub pages
17. Verify all routes generate correctly and no 404s exist

### Phase 4: SEO Tags
18. Run **pseo-metadata** to implement dynamic metadata on all templates
19. Run **pseo-schema** to add JSON-LD structured data to all templates
20. Verify metadata and schema render correctly on sample pages

### Phase 5: Optimization
21. Run **pseo-performance** to optimize build times, CWV, and caching
22. Run **pseo-llm-visibility** to optimize for AI citation (llms.txt, AI crawlers, content chunking, entity optimization)
23. Run a build to verify it completes successfully at current scale
24. Check bundle size and rendering performance

### Phase 6: Validation
25. Run **pseo-quality-guard** with scope `all` (or `delta` at 10K+ pages)
26. Present quality report to the user
27. Fix any critical issues flagged by the quality guard
28. Re-run quality guard to confirm all issues resolved

## Decision Points

At each phase transition, check with the user:
- Phase 0→1: "Here are the pSEO opportunities. Which page types should we build?"
- Phase 1→1.5: "The audit found these issues. Scale target is N pages — do we need scale infrastructure?" (only if 10K+)
- Phase 1.5→2: "Database and gating are set up. Proceed with data architecture?"
- Phase 1→2: "The audit found these issues. Proceed with implementation?" (if < 10K, skip 1.5)
- Phase 3→4: "Templates and linking are set up. Ready for metadata and schema?"
- Phase 5→6: "Performance and LLM visibility optimizations applied. Ready for final validation?"

## Progress Tracking

Track and report progress as:

```
Phase 0: Discovery        [✓] Complete — 3 page types confirmed, 50K pages planned
Phase 1: Audit            [✓] Complete
Phase 1.5: Scale Infra    [✓] Complete (DB, gating, CDN) — skipped if < 10K
Phase 2: Data             [✓] Complete
Phase 3: Structure        [→] In Progress (templates done, linking in progress)
Phase 4: SEO Tags         [ ] Pending
Phase 5: Optimization     [ ] Pending (performance + LLM visibility)
Phase 6: Validation       [ ] Pending
```

## Important Rules

- Never skip the discovery phase on a new project (unless user already knows exactly what pages to build)
- Never skip the audit phase on a new project (unless user explicitly says to)
- Always run pseo-quality-guard as the final step
- If quality guard finds critical issues, fix them before declaring success
- Commit changes at logical checkpoints (after each phase)
- Keep the user informed at each phase transition

## Framework Note

All code examples across the pseo-* skills use Next.js App Router patterns by default. The concepts, data structures, and SEO principles are framework-agnostic and apply equally to Astro, Nuxt, Remix, SvelteKit, or any SSG/SSR framework. When working with a non-Next.js project, adapt the framework-specific APIs (routing, metadata, static generation) to the equivalent in the target framework.

## What This Skill Does NOT Do

- Does not choose a framework (assumes one is already in place or user will decide)
- Does not create content (assumes data/content exists or user will provide it)
- Does not deploy the site
- Does not set up CI/CD
- Does not configure hosting or DNS
