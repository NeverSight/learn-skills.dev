---
name: rail-review
description: Two-axis review of the diff since a fixed point — Standards and Spec. Use when reviewing a branch, PR, or WIP changes — not as part of rail-build.
---

# Rail Review

Review `git diff <fixed-point>...HEAD` on two axes in **parallel sub-agents**:

- **Standards** — repo coding standards + Fowler smell baseline (repo docs win on conflict)
- **Spec** — faithfulness to the originating `docs/monorail/**/spec.md` and/or task file

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — commit SHA, branch, tag, `main`, `HEAD~5`, etc. If missing, ask.

Capture: `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`.

Confirm `git rev-parse <fixed-point>` and a non-empty diff before continuing.

### 2. Identify the spec source

Order:

1. Path the user passed as an argument
2. `docs/monorail/<feature>/spec.md` plus the task file being built
3. Ask the user where the spec is
4. If none, Spec axis reports "no spec available"

Check each candidate path on disk with the shell (`ls`, or read it) before falling through to the next — search tools skip gitignored paths, so an empty Glob/Grep result is **not** evidence the spec is absent.

Never fetch GitHub/GitLab issues for spec source — local files only.

### 3. Identify the standards sources

Anything documenting how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, etc.).

On top of repo docs, Standards always carries a **smell baseline** (Fowler, _Refactoring_ ch.3). Rules:

- **The repo overrides.** Documented repo standard wins.
- **Always a judgement call** for baseline smells — labelled heuristics, not hard violations. Skip anything tooling already enforces.

Smell list (what → fix): Mysterious Name → rename; Duplicated Code → extract; Feature Envy → move method; Data Clumps → bundle type; Primitive Obsession → domain type; Repeated Switches → polymorphism/map; Shotgun Surgery → gather change; Divergent Change → split module; Speculative Generality → delete; Message Chains → hide walk; Middle Man → cut; Refused Bequest → composition.

### 4. Spawn both sub-agents in parallel

Send a single message with two Agent/Task tool calls. Use the general-purpose (or equivalent) subagent for both. If the harness cannot spawn parallel sub-agents, run Standards then Spec **sequentially** — do not skip an axis.

**Standards sub-agent prompt** — include:

- The full diff command and commit list
- The list of standards-source files from step 3, plus the smell baseline pasted in full (the sub-agent has no other access to it)
- Brief: report per file/hunk (a) documented-standard violations with cite; (b) baseline smells named + hunk quoted. Distinguish hard violations from judgement calls. Skip tooling-enforced items. Under 400 words.

**Spec sub-agent prompt** — include:

- The diff command and commit list
- Path or contents of the spec/task
- Brief: (a) missing/partial requirements; (b) scope creep; (c) wrong implementations. Quote spec lines. Under 400 words.

If the spec is missing, skip the Spec sub-agent and note that in the final report.

### 5. Aggregate

Present under `## Standards` and `## Spec` separately. Do not merge or rerank across axes. End with one-line counts per axis, and label any **blocking** findings clearly.

**Blocking vs non-blocking:**

- **Blocking (Spec):** missing/partial acceptance behaviour the task or `spec.md` required; clearly wrong implementation of a quoted requirement
- **Blocking (Standards):** hard violation of a **documented** repo standard (cite file + rule)
- **Non-blocking:** Fowler smell-baseline heuristics; style nits tooling already covers; speculative scope the task did not ask for (still report under Spec as scope creep, but not blocking unless it contradicts the task)

Do not commit or push as part of review. Do not set task `Status: done`.
