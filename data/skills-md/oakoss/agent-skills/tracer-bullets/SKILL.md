---
name: tracer-bullets
description: |
  Builds multi-layer features as vertical end-to-end slices instead of horizontal layers. Each slice is verified before the next begins.

  Use when: starting any task that spans 2+ layers (DB, API, UI, tests), building CRUD features, implementing multi-step flows, decomposing features into subtasks, or planning implementation order.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://www.aihero.dev/tracer-bullets
user-invocable: false
---

# Tracer Bullets

Build features as vertical slices through all layers, verifying each slice before starting the next. From The Pragmatic Programmer: get feedback as quickly as possible. Don't build horizontal layers in isolation (all endpoints, then all UI, then all tests). Build one thin vertical path, verify it works, then expand.

Skip for single-layer changes, one-file bug fixes, or work already decomposed into ordered vertical slices by a task tracker.

## Quick Reference

| Principle                  | Practice                                                              |
| -------------------------- | --------------------------------------------------------------------- |
| Vertical over horizontal   | Build one slice through all layers, not one layer across all features |
| Verify before advancing    | Tests pass, page renders, round-trip works before next slice          |
| One slice per session      | Each slice should be completable in a single agent session            |
| First feature sets pattern | First CRUD establishes conventions; subsequent CRUDs go faster        |
| Check before building      | Task trackers may already decompose the work into slices              |
| Skip when trivial          | Single-layer work or proven patterns don't need this ceremony         |

## CRUD Feature Slices

| Slice | Scope                       | Verifies                                           |
| ----- | --------------------------- | -------------------------------------------------- |
| 1     | Backend/API + tests (no UI) | Data layer works, conventions set, tests prove it  |
| 2     | List page with real data    | Data flows DB -> server -> rendered page           |
| 3     | Create dialog               | Full round-trip: form -> server -> DB -> refresh   |
| 4     | Edit + delete               | Full CRUD cycle, mutation patterns, confirm dialog |
| 5     | E2E test                    | Locks in the whole feature                         |

## Non-CRUD Adaptations

Same principle, different slices:

- **Import flow**: parse one row -> display one row -> validate + dedupe -> review + commit
- **Dashboard**: one widget with real data -> empty/onboarding state -> layout with all widgets
- **Search/palette**: one entity type -> all entity types -> quick actions
- **Multi-step wizard**: first step end-to-end -> add steps one at a time -> final submission

## Common Mistakes

| Mistake                                              | Correct Pattern                                                    |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| Building all API endpoints before any UI             | Build one endpoint + its UI + its test, then the next              |
| Starting UI before the backend is tested             | Slice 1 is backend-only with tests; prove the data layer first     |
| Building the full create/edit/delete UI in one pass  | Create dialog first (slice 3), then edit + delete (slice 4)        |
| Skipping verification between slices                 | Run tests and check output before starting the next slice          |
| Making slices too large for one session              | Split further; a slice that can't finish in one session is too big |
| Applying tracer bullets to trivial single-layer work | Skip for one component, one utility, or patterns already proven    |

## Delegation

- **Decompose into subtasks**: Use the project's task tracker to create ordered vertical subtasks before writing code
- **Isolate each slice**: Delegate each slice to a subagent so failures stay contained and context stays fresh
- **Find slice boundaries for non-CRUD work**: Pick the smallest path through all layers as slice 1, then expand

## References

No reference files. Source: [Tracer Bullets: Keeping AI Slop Under Control](https://www.aihero.dev/tracer-bullets)
