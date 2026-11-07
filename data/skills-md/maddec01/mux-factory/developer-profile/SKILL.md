---
name: developer-profile
description: "Enforces my coding style: feature-first simplification; reuse/refactor/delete before adding; project-native, modular, decoupled, strongly typed code."
---

# Developer Profile

Use whenever implementing, refactoring, fixing, reviewing, or extending code; especially new features, behavior changes, refactors, bugs, components/services/utilities/types/tests, or unfamiliar project areas.

## Non-negotiable principles

1. Add code last. First inspect the full feature flow, then reuse, refactor, simplify, or delete existing code before creating anything new.
2. Never stack new code on top of old code. If behavior overlaps, merge/extend the existing path and remove obsolete duplication.
3. A feature diff should improve the whole feature, not only append files. If the change is mostly additions, stop and reassess for reuse/removal/refactor opportunities.
4. Before adding a file/function/component/service/state/type/helper, prove no existing one can be reused or extended with less total code.
5. Prefer less code: avoid wrappers, helpers, abstractions, dependencies, config, or layers unless they clearly reduce total complexity.
6. Match structure to domain: organize folders/files by feature/library/state/etc.; filenames should mirror folder context, e.g. `Feature/Library/State/LibraryState.ts`.
7. Decouple responsibilities: separate UI, state, business logic, data access, formatting, and side effects so each part is reusable/testable/replaceable.
8. Stay project-native: follow existing naming, imports, formatting, state/data patterns, tests, and architecture.

## Required workflow

1. Inspect first: feature flow; similar implementations; folder structure; shared components/services/utilities/types/state/styles; error handling; tests.
2. Reuse/refactor/delete first: remove duplicated/dead/obsolete code; extend fitting abstractions; do not create parallel components, services, types, state, utilities, styles, or architecture.
3. Add only what remains necessary: smallest clean solution; focused diff; no unrelated rewrites; no new dependency/architecture unless justified by net simplification.
4. Keep modular/typed/readable: clear names; explicit types when useful; avoid `any`; no mixed responsibilities; no hidden side effects.
5. Follow project structure exactly: natural location; existing file naming, import style, formatting, conventions, and test structure.
6. Final summary must state: what was reused/extended; what was removed/simplified; why any new code was unavoidable.
