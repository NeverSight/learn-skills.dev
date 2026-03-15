---
name: agent-friendly-codebase
description: Make a codebase more AI-agent-friendly. Review and transform bounded work areas so agents can find files faster, make smaller safer changes, verify results with less human help, and hand off work with low ambiguity.
---

# Agent-Friendly Codebase

Apply on a **bounded work area** in one of two modes: `review` or `transform`.

## Work area

A work area is a bounded unit of work defined by:

- primary code paths
- entrypoints
- public contracts
- commands used to build, run, and validate it
- typical change types

If the user names only a path, infer the smallest reasonable work area around it.

## Inputs

Infer these unless asking is necessary:

- target area identifier or path
- goal: `review` or `transform`
- proof command or trusted validation path

## Core principles

These are the Must-level rules from `references/RULE.md`. Read the full file for Should-level guidance and anti-patterns.

### P1. Boundary & entrypoints

- Name the primary paths for the area
- Identify entrypoints
- Identify important dependencies and reverse dependencies

### P2. Commands & environment

- Define canonical install, build, test, lint, and dev commands or clear equivalents
- Keep those commands reproducible inside repository conventions
- Provide at least one automated validation path
- Cover representative task types with tests or repeatable repro steps

### P3. Contracts & change surface

- Expose important public contracts (routes, APIs, schemas, DTOs, env dependencies)
- Make external system boundaries visible through types or docs
- Make the common edit surface observable
- Explain when cross-boundary edits are required and why

### P4. Context hierarchy & economy

- Keep always-loaded rules short and high signal
- Move detail, long examples, and domain explanations into supporting files
- Distinguish repository-wide guidance from area-local guidance
- Let more specific rules refine broader ones
- Budget: root ~100-200 lines, area ~50-150 lines

### P5. Examples, verification & persistence

- Provide at least one canonical or recent example for a representative task type
- Externalize recurring patterns, mistakes, and conventions into docs, skills, tests, or ADRs
- Identify the main logs, error paths, or state checkpoints for the area
- Define a lightweight review rubric and proof path for day-to-day work

## Scoring model

The snapshot score is `ACRS` (Agent Codebase Readiness Score): `S1 + S2 + S3 + S4 + S5`, range `0..20`.

| Category                                 | Evaluates                                                           |
| ---------------------------------------- | ------------------------------------------------------------------- |
| S1. Boundary & entrypoints               | Are area boundary, entrypoints, and starting files explicit?        |
| S2. Commands & environment               | Do canonical build/test/proof paths exist with low setup ambiguity? |
| S3. Contracts & change surface           | Are contract surfaces and blast radius explicit and traceable?      |
| S4. Context hierarchy & economy          | Is guidance high-signal, layered, and low-duplication?              |
| S5. Examples, verification & persistence | Are examples, verification, and knowledge capture easy to find?     |

Each category is scored `0-4`:

| Score | Meaning                                                |
| ----: | ------------------------------------------------------ |
|     0 | absent — effectively unusable                          |
|     1 | weak — mostly implicit                                 |
|     2 | partial — important gaps remain                        |
|     3 | solid — works for normal tasks, moderate friction only |
|     4 | explicit — current, low ambiguity                      |

Bands: **good** `>=16`, **so-so** `10-15`, **bad** `<10`.

Read `references/EVALUATION.md` for detailed per-category anchor interpretations, fixed comparison conditions, and scoring consistency guidelines.

## Output contract

### `review`

Produce:

- area boundary summary
- key entrypoints, contracts, and search starting points
- canonical command and proof path summary
- ACRS readiness snapshot score with per-category breakdown
- top agent-friction gaps
- smallest useful next improvements

### `transform`

Produce:

- the scoped area and agreed proof path
- a current-state summary, unless a still-valid review result can be reused
- the smallest changes that improve the target area
- proof results
- a post-change summary with ACRS score
- what improved
- remaining risks

Prefer the smallest high-value diff over broad cleanups.

## Workflow

### `review`

1. Bound the area
2. Map entrypoints, contracts, and commands
3. Score the current readiness snapshot (ACRS)
4. Report the biggest gaps and next actions

### `transform`

1. Confirm the area, goal, and proof path
2. Reuse a recent valid review when possible, otherwise create a current-state summary
3. Apply the smallest useful changes
4. Run the proof path
5. Create a post-change summary with ACRS score
6. Report what improved and any remaining risks

## Multi-agent modifier

When the user explicitly mentions parallel agents or handoff:

- Map ownership lanes and collision hotspots
- Add handoff boundaries to the area profile
- Include coordination scope in scoring
- Prefer visible ownership and shared proof surfaces over private scratch context

Otherwise default to single-agent scope.

## Guardrails

- Do not treat more documentation as improvement by default.
- Prefer area-scoped guidance over repo-wide blanket rules.
- Prefer executable verification over narrative claims.
- Never claim a transformation is safe unless the named proof path and regression checks were run, or state that safety is unproven.
- Use compact headings and separate facts, scores, decisions, and unknowns.
- Mark partial evidence as estimated or missing.

## References

Read only when deeper detail is needed:

| File                           | When to read                                                            |
| ------------------------------ | ----------------------------------------------------------------------- |
| `references/RULE.md`           | Full rule definitions with Should-level guidance and anti-patterns      |
| `references/EVALUATION.md`     | Detailed scoring anchors, comparison conditions, consistency guidelines |
| `references/CHECKLIST.md`      | Step-by-step checklists for review and transform                        |
| `references/node-monorepo.md`  | Target is a JS/TS monorepo                                              |
| `references/go-service.md`     | Target is a Go service                                                  |
| `references/python-service.md` | Target is a Python service                                              |
| `references/MAINTENANCE.md`    | Maintaining this skill package itself                                   |
