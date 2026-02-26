---
name: test-review
description: Review test quality and audit test coverage for any module. This skill should be used when reviewing existing tests, auditing test gaps, writing new tests, or when asked to assess test health. It pipelines testing standards into the audit workflow to produce a prioritized gap report. The output is a report, not code — do not write test implementations until the report is reviewed.
---

# Test Review

Review test quality and audit coverage gaps by loading the project testing standards
first, then executing the audit workflow. The pipeline produces a prioritized gap
report — not test code.

## When to Use

- "Review the tests for module X"
- "Audit test coverage for this component"
- "Are these tests any good?"
- "What tests are missing?"
- Before writing new tests (audit first, then write)
- After a significant refactor (verify tests still cover the contract)
- When preparing a module for production

## Pipeline

This skill is a three-phase pipeline. Execute the phases in order. Do not skip
Phase 1 — the standards must be loaded before reviewing any test code.

### Phase 1: Load the Standards

Read the project testing standards to calibrate what "good" looks like:

```
cat skills/test-review/references/testing-standards.md
```

This file defines:
- Anti-patterns to flag (mirror testing, happy-path-only, over-mocking, trivial assertions)
- Required test categories (contract, boundary, failure mode, state transition, integration)
- The self-check checklist for individual tests
- Language-specific standards (Rust, TypeScript/React)
- Coverage expectations by component type
- Naming conventions

**Internalize these before reading any test code.** Every finding in the audit
must reference a specific standard from this file. Do not invent standards — use
the ones defined here.

### Phase 2: Discovery (Haiku Agents)

Spawn Haiku sub-agents to perform the mechanical discovery work — Steps 1 and 2
of the audit workflow. This keeps the main context clean for analysis.

Read the audit workflow first so you understand what the agents need to do:

```
cat skills/test-review/references/audit-workflow.md
```

#### Step 2a: Scope the work

Before spawning agents, determine how many files are involved:

```
Glob tool: **/*.{py,rs,ts,tsx,js,jsx,go,rb} under [MODULE_PATH]
Glob tool: **/*.{test,spec}.* or **/test_*.* or **/tests/**  under [TEST_PATH]
```

Count the source files and test files. This determines the fan-out strategy.

#### Step 2b: Choose fan-out strategy

| Source files | Strategy | Agents |
|---|---|---|
| ≤ 15 | **Single agent** — one Haiku handles everything | 1 |
| 16–60 | **Partition by directory** — one agent per top-level subdirectory (or logical grouping) | 2–4 |
| 60+ | **Partition by file chunks** — split the file list into roughly equal chunks of ~15 files each | up to 6 |

**Partitioning rules:**
- Each agent gets a subset of **source files** to inventory (Step 1)
- Each agent also gets the **full test file list** (tests may cross-cut source boundaries)
- Each agent only produces inventory for its assigned source files
- Partitions should respect directory boundaries when possible (keep related files together)

#### Step 2c: Launch agents in parallel

Launch all Haiku agents in a **single message** so they run concurrently. Each
agent gets the same instructions but a different file partition.

**Do not ask Haiku agents to analyze, prioritize, or judge.** Their job is to
read code and produce a factual inventory. Analysis happens in Phase 3.

**Single agent** (≤ 15 source files):

```
Task tool:
  subagent_type: Explore
  model: haiku
  prompt: |
    Read the audit workflow at skills/test-review/references/audit-workflow.md.
    Then execute Steps 1 and 2 for the module at [MODULE_PATH].

    Step 1 - Map the Public Contract:
    Read every source file in the module. List every public behavior it promises
    as plain-English statements (see audit-workflow.md for format and examples).

    Step 2 - Map Existing Test Coverage:
    Read every test file that covers this module. For each test, record what
    behavior it exercises and whether assertions are meaningful. Mark each
    behavior from Step 1 as:
    - Covered: at least one test verifies this with meaningful assertions
    - Shallow: a test touches this but doesn't properly verify it
    - Missing: no test exercises this behavior

    Return:
    1. Source files read (paths)
    2. Test files read (paths)
    3. Complete behavior list with coverage status markers
    4. For each Shallow entry, note what the test does and why it's insufficient

    Do NOT prioritize, analyze risk, or produce a gap report. Just inventory.
```

**Multiple agents** (16+ source files):

Launch all agents in the same message. Each gets a partition of source files
but the full list of test files.

```
# Agent 1 of N — launched in parallel with all other agents
Task tool:
  subagent_type: Explore
  model: haiku
  prompt: |
    Read the audit workflow at skills/test-review/references/audit-workflow.md.
    Then execute Steps 1 and 2 for the following SOURCE FILES ONLY:
    [LIST OF FILES IN THIS PARTITION]

    The test files that may cover these sources are at:
    [FULL TEST FILE LIST OR TEST DIRECTORY PATH]

    Step 1 - Map the Public Contract:
    Read ONLY the source files listed above. List every public behavior each
    promises as plain-English statements (see audit-workflow.md for format).

    Step 2 - Map Existing Test Coverage:
    Read the test files and identify which tests exercise behaviors from YOUR
    source files. Mark each behavior as:
    - Covered: at least one test verifies this with meaningful assertions
    - Shallow: a test touches this but doesn't properly verify it
    - Missing: no test exercises this behavior

    Return:
    1. Source files you read (paths)
    2. Test files you read (paths)
    3. Complete behavior list with coverage status markers
    4. For each Shallow entry, note what the test does and why it's insufficient

    Do NOT prioritize, analyze risk, or produce a gap report. Just inventory.

# Agent 2 of N — same structure, different file partition
# ...
# Agent N of N
```

#### Step 2d: Merge inventories

Once all agents return, merge their results into one unified inventory:

1. **Concatenate** all behavior lists (each agent covers different source files,
   so there should be minimal overlap)
2. **Deduplicate** any behaviors that appear in multiple agents' results (can
   happen when source files in different partitions share interfaces)
3. **Prefer the more-specific status** when merging duplicates: if one agent
   says Covered and another says Shallow for the same behavior, keep Shallow
   (investigate the discrepancy in Phase 3)
4. **Compile** the full list of source files and test files read across all agents

The merged inventory feeds into Phase 3 exactly as if a single agent produced it.

### Phase 3: Analysis and Report

Using the merged Haiku inventory, **you** (the main agent) perform the deeper
analysis work — Steps 3 and 4 of the audit workflow:

- **Step 3: Adversarial analysis** — probe input boundaries, error handling,
  state, integration seams. Use the questions from audit-workflow.md against the
  behavior inventory. You may need to read specific source files to answer them.
- **Step 4: Produce the gap report** — assign P0/P1/P2 priorities using the
  criteria defined in audit-workflow.md, cite testing-standards.md rules, and
  produce the full report in the format specified.

The adversarial analysis and priority assignment require judgment that only the
main agent should perform. Do not delegate these to a sub-agent.

## Operating Rules

1. **Standards first, always.** Read testing-standards.md before opening any test file. If
   context has been compressed and the standards are no longer loaded, read them again.

2. **Report, do not fix.** The output is a gap report. Do not write test code unless
   explicitly asked to implement specific gaps from an approved report.

3. **Cite the standard.** Every finding must name which testing-standards.md rule it
   violates or which audit-workflow.md criterion it fails. Findings without citations
   are opinions, not audit results.

4. **Read the source, not just the tests.** The audit requires reading the module
   source to map the public contract (Step 1 of audit-workflow.md). Do not audit tests
   in isolation — the whole point is to find gaps between what the code does and what
   the tests verify.

5. **Do not manufacture gaps.** If a module is well-tested, say so. The gap report
   has a "Well-Tested" section for exactly this purpose.

## Modes

### Full Audit (default)

Execute all three phases. Produces the full gap report.

Use when: "audit tests for module X", "review test coverage", preparing for production.

### Quick Review

Load testing-standards.md, then review specific test files against the anti-patterns and
self-check checklist only. Skip Phase 2 (Haiku discovery) and the adversarial analysis.

Use when: reviewing a PR's test changes, spot-checking a single test file,
"are these tests ok?"

### Write Mode

Execute a full audit first, present the gap report, then — only after approval —
write test implementations for approved gaps following the standards in testing-standards.md.

Use when: "audit and fix tests for module X", "write missing tests".

## Common Mistakes

- **Skipping testing-standards.md** — Reviewing tests without loading the standards
  produces generic feedback. The standards are project-specific and opinionated.
- **Writing tests before the report** — The audit produces findings. The user decides
  which to implement. Do not jump ahead.
- **Auditing tests without reading source** — Cannot identify missing coverage without
  knowing what the code does.
- **Citing severity without justification** — P0/P1/P2 assignments have specific
  criteria defined in audit-workflow.md. Use those criteria, not gut feeling.
