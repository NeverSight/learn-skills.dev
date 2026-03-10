---
name: llm-challenge
description: >
  Manage the LLM Challenge benchmark: run benchmarks, create/modify problems,
  analyze results, and improve SDK based on failures.
  Use when user mentions "llm-challenge", "challenge", "benchmark", or "lc".
---

# LLM Challenge

Benchmark for `@tailor-platform/sdk` AI-friendliness. Located at `llm-challenge/`.

Read `llm-challenge/README.md` for commands, scoring, and verification details.

## Core Rule

When AI fails a challenge, **improve the SDK** (JSDoc, error messages, types, CLAUDE.md) — NEVER add hints to `problem.md`.

## Prerequisite

ALWAYS build SDK before running: `pnpm -C packages/sdk build`

## Problem Conventions

Structure: `problems/<id>-<name>/` with `meta.json`, `problem.md`, `scaffold/`, `solution/`, `tests/`

**meta.json rules**:

- `id`: 3-digit zero-padded, sequential
- `scoring`: Category defaults — tailordb: 20/20/60, resolver/executor/workflow: 15/15/70, config: 30/20/50, fix-broken: 15/15/70
- Fix-broken problem: same file appears in both `implement` and `scaffold`

**problem.md rules**:

- Sections: Goal → Domain Context/Instructions → What to Build → Requirements → Reference
- NEVER include SDK code examples — AI must discover API from the SDK package itself
- Always end with "Refer to the installed SDK package for ..."

## Writing Tests

- Read existing tests in `problems/*/tests/` for patterns
- Helpers: `shared/test-helpers.ts` (`createWorkDirContext`, `importPath`, `expectFieldType`, etc.)
- Mocks: `shared/mocks.ts` (`setupTailordbMock`, `setupWorkflowMock`)
- ALWAYS use `describe.skipIf(!workDirReady)` guard

## Creating a New Problem

1. Next sequential ID (e.g., `013`)
2. Write solution first, then tests
3. Verify: `pnpm -C llm-challenge challenge --problem <id> --use-solution` → must be 100/100

## SDK Improvement Cycle

1. `pnpm -C llm-challenge challenge:solve --retry 2` → analyze failures
2. Improve SDK source (NOT problem descriptions)
3. `pnpm -C packages/sdk build` → `pnpm -C llm-challenge challenge:verify-solution`
4. Re-run benchmark to measure improvement
