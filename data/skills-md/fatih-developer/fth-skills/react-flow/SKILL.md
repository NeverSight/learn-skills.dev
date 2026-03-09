---
name: react-flow
description: Analyze, repair, migrate, and scaffold @xyflow/react codebases. Use when users ask to debug React Flow behavior, fix node/edge state wiring, improve type safety or performance, upgrade legacy React Flow APIs, preserve persisted graph compatibility, or generate a complete React Flow starter from scratch.
---

# React Flow Repair, Migration, And Build Protocol

Execute this protocol in order. Keep fixes small, reversible, and validated.

## Required Outputs

1. Produce a short audit report of the current React Flow architecture.
2. Produce a prioritized fix list with risk and expected impact.
3. Apply safe fixes in small patches when requested.
4. Generate missing typed scaffolding when the project is incomplete.
5. Report verification results and any residual risks.

## Workflow

1. Discover project shape.
   - Locate all React Flow usage (`ReactFlow`, `useNodesState`, `useEdgesState`, `addEdge`, custom node/edge components).
   - Confirm framework/runtime details (`vite`, `next`, TypeScript config, lint setup).
2. Validate graph model contracts.
   - Centralize `Node` and `Edge` type definitions.
   - Validate id strategy, `data` schema stability, and custom type names.
3. Validate state and event wiring.
   - Ensure `onNodesChange`, `onEdgesChange`, and `onConnect` are correctly bound.
   - Detect duplicated or conflicting state sources.
4. Validate rendering and performance.
   - Keep `nodeTypes` and `edgeTypes` references stable.
   - Detect avoidable re-renders and unsafe inline object creation in hot paths.
5. Apply auto-fixes.
   - Apply highest-impact, low-risk fixes first.
   - Preserve behavior unless an explicit bug fix requires a behavior change.
   - Include migration notes for any public API or schema changes.
6. Run migration pass when legacy APIs are present.
   - Detect legacy package/import usage and map to modern `@xyflow/react`.
   - Migrate types first, then runtime wiring, then persistence compatibility.
   - Add migration guard for old payload versions when needed.
7. Scaffold from scratch when needed.
   - Generate a minimal typed baseline with custom node support and layout helper.
   - Ensure resulting scaffold compiles in a standard TS React setup.
8. Verify.
   - Run available tests or static checks.
   - If checks are missing, provide manual verification steps.

## Guardrails

- Preserve existing business logic unless the bug requires change.
- Keep node and edge ids stable across operations and persistence cycles.
- Avoid introducing a second state manager unless explicitly requested.
- Keep templates framework-agnostic unless the repository enforces a framework.
- Prefer typed interfaces over `any` for flow `data` payloads.

## References

- Use `references/CHECKLIST.md` for systematic auditing.
- Use `references/FIX_PATTERNS.md` for common issue-to-fix mapping.
- Use `references/EXAMPLES.md` for prompt and output patterns.
- Use `references/MIGRATION_CHECKLIST.md` and `references/API_RENAMES.md` for upgrade work.
- Use `references/MIGRATION_EXAMPLES.md` for migration request patterns.

## Templates

- Start from `templates/Flow.tsx.tmpl` for baseline flow container.
- Start from `templates/nodeTypes.tsx.tmpl` and `templates/edgeTypes.tsx.tmpl` for typed registries.
- Use `templates/layout.ts.tmpl` for deterministic starter layout behavior.
- Use `templates/migration-plan.md.tmpl` for patch-by-patch upgrade planning.
- Use `templates/compat-adapter.ts.tmpl` when backward compatibility is required.
