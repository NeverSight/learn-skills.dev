---
name: code-review-and-quality
description: |
  Reviews a code change for correctness, security, maintainability, architecture, performance, and verification gaps, or performs a local code-smell review. Use for review this diff/PR、变更评审、代码审查、代码整洁度. Return evidence-backed findings and a scoped verdict; diagnose without editing unless fixes are requested. Use hai-architecture for system design, react-component-diagnosis for a component deep dive, and write-technical-acceptance-report for executed requirement acceptance.
---

# Code Review and Quality

## Purpose

Find defects and costly design regressions in a defined change. Preserve the useful five-axis
review method of the existing skill while scaling the work to actual risk. A review verdict is
not permission to merge, publish, or message others.

## Modes

- **Change review**: review the named diff/PR/commit. If unspecified, inspect the local staged and
  unstaged changes plus relevant new files; state the baseline and scope.
- **Maintainability**: inspect the named files/functions for code smells. Read
  `references/maintainability.md` and its relevant language/examples guidance. Preserve behavior.
- **Review and fix**: when the user asks for repairs, implement clear in-scope fixes after
  diagnosis and verify them. An audit-only request remains read-only.

## Workflow

1. Read repository instructions, intended behavior, diff, and relevant specs/contracts. Record
   which files and paths were actually reviewed. Preserve unrelated work.
2. Read tests and their assertions, then trace changed behavior into callers, state, error paths,
   persistence, and external effects where relevant. A passing test is only as good as its coverage.
3. Review relevant axes:
   - Correctness: intended behavior, boundary cases, failure handling, state transitions,
     concurrency/idempotency where relevant.
   - Security: real trust/permission boundaries and untrusted data flow.
   - Maintainability: clear responsibility and vocabulary; unnecessary branches, abstractions,
     duplicated authority; project conventions over arbitrary style rules.
   - Architecture: ownership, dependency direction, contract changes, and whether complexity was
     reduced or merely relocated.
   - Performance: evidenced unbounded work, query growth, allocation/render pressure; do not invent
     latency estimates without measurement.
4. For each candidate, verify the triggering scenario and changed code. Distinguish regressions,
   pre-existing issues, and unverified suspicions. Cite real file:line evidence.
5. Rank by user impact and change cost. Omit cosmetic preferences unless requested. Do not reject
   a coherent change solely for its line count, number of implementations, or lack of abstraction.
6. For requested repairs, apply the smallest complete fix and run appropriate checks. Use
   `hai-tdd` for behavior changes where a real RED is possible; structural work uses compiler,
   existing tests, and focused checks. Do not mix unrelated redesign into a bug fix.
7. Read `references/output-template.md` and deliver findings, actual verification, and a scoped
   verdict. No findings means none were found in the inspected scope, not proof of perfection.

## Verification and boundaries

Review code and run relevant non-mutating checks when useful. Do not claim tests passed unless
executed or clearly label the author's/historical evidence. Code inspection does not prove a
deployed workflow passed; requirement-by-requirement acceptance belongs to
`write-technical-acceptance-report`.

Unexplained runtime failures → `hai-debug`. A structural decision exposed by review →
`hai-architecture`; a local naming decision → `hai-naming`; deep React analysis →
`react-component-diagnosis`. Reuse collected evidence when handing off.
