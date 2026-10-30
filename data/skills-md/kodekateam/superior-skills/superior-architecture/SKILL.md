---
name: superior-architecture
description: Design, implement, or assess project structure, module ownership, dependency boundaries, and safe file or folder organization. Use when project architecture, feature placement, separation of responsibilities, or architectural refactoring is a primary concern, including new framework projects. For a read-only assessment, do not modify files unless the user also requests changes; do not activate merely because ordinary feature work adds a file.
---

# Superior Architecture

Organize code around real responsibilities, supported framework conventions, and maintainable dependencies. Treat Clean Architecture as a set of boundaries, not a required directory tree or an instruction to add layers.

## Establish scope and evidence

Determine whether the user wants a design, read-only assessment, or implementation. Inspect repository instructions, framework entrypoints and discovery rules, existing feature owners, imports, tests, and relevant documentation. For a new project, inspect the actual framework scaffold and supported conventions. Identify existing public contracts and what must remain unchanged.

An architecture assessment alone does not authorize moving files, changing dependencies, or restructuring unrelated code. Ask for direction only when materially different architectures cannot be resolved from the request and project evidence.

## Choose ownership and grouping

Read [references/project-structure-and-boundaries.md](references/project-structure-and-boundaries.md) when establishing a project's structure, placing a feature across several responsibilities, or deciding whether a file or module needs to be split.

- Place new code near the feature or module that owns its behavior. Use feature-based, layer-based, or mixed organization according to current conventions, change patterns, and framework requirements.
- Separate domain policy from UI, transport, and persistence where it protects a real contract or supports independent testing. Keep dependency direction consistent with established boundaries and user requirements.
- Start with the smallest structure the current work needs. Do not create empty layers, interfaces, repositories, adapters, or service containers solely to match a named pattern.
- Extract shared code only when there is a real shared responsibility or contract. Avoid generic catch-all folders and one file per trivial function.
- Consider splitting a file when it combines distinct responsibilities, changes for unrelated reasons, obscures a trust boundary, or is difficult to navigate or test. Line count is a signal for inspection, not a hard threshold.
- Preserve the project's established architecture unless the user explicitly requests a change. Limit refactoring to the authorized scope and explain material tradeoffs.

## Move and verify safely

Before moving code, trace imports and indirect consumers, including framework discovery, routes, configuration, registrations, package exports, tests, build scripts, and documented public APIs. Preserve behavior, validation, error handling, security, and compatibility; update affected consumers together. Keep or plan a compatibility path when a public contract requires it.

Verify affected behavior using existing targeted tests and the project's relevant discovery, type, lint, or build checks. Report chosen owners, dependency direction, meaningful tradeoffs, compatibility impact, checks run, and unresolved risks. Do not claim an architecture is clean based only on folder names.

## Work with other skills

- Use `superior-logic` for behavior, state transitions, and business contracts.
- Use `superior-lean` to assess unjustified complexity and safe removal.
- Use `superior-code-review` for a read-only review of a change; add this skill when structural boundaries are the main concern.
- Use `superior-docs` to record verified material changes or update architecture decisions when they change.
