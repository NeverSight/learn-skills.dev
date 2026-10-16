---
name: review-and-fix
description: >
  Reviews git diff changes with senior-engineer judgment: investigates context,
  adapts rigor to change type, weighs downstream impact, and guides user-approved
  fixes. Use when reviewing code changes and deciding whether to fix issues.
license: MIT
compatibility: Requires git, file read/write access, and LSP/linter tooling for best results.
metadata:
  author: fang2hou
  version: "2.2"
---

# Review and Fix

Review code changes as a senior engineer would: investigate context first, weigh trade-offs against the change type, then organize findings for user action.

## When to Use

- The user asks to review their changes, the git diff, or a commit range ("review my changes", "check the diff", "code review")
- The user wants issues found and fixed before committing ("review and fix", "fix the issues")
- The user invokes `/review-and-fix`

## When NOT to Use

- Full codebase auditing (use a broader code review tool)
- Security auditing specifically (use a dedicated security skill)
- Performance profiling (different domain)
- Generating tests (separate workflow)

## Inputs

| Input          | Required | Format             | Example                                                        |
| -------------- | -------- | ------------------ | -------------------------------------------------------------- |
| `$ARGUMENTS`   | No       | File paths or refs | `src/auth.rs`, `HEAD~3`, `main..HEAD`                          |
| Git diff scope | No       | Ref or path        | Defaults to all uncommitted changes, including untracked files |

**Scope resolution**: If `$ARGUMENTS` provides paths, review only those files. If it provides git refs, diff those refs. Otherwise, review all uncommitted changes: staged, unstaged, and untracked files.

## Hard Rules

1. **Investigate before judging**: Understand why the code looks the way it does before flagging an issue. History, constraints, and intent matter.
2. **Adapt rigor to context**: A production hotfix needs a different review than a new library API. Adjust your standards accordingly.
3. **No silent fixes**: Present every fix to the user for approval before applying it.
4. **Preserve intent**: Keep what the code does; only fix how it does it.
5. **Evidence-based**: Cite a specific line, rule, or diagnostic for every issue rather than a vague impression.
6. **No suppression shortcuts**: Never suggest `as any`, `@ts-ignore`, `@ts-expect-error`, `unwrap()` to silence errors, or equivalent suppression mechanisms.

## Core Principle: Context Determines Rigor

Before reviewing a line of code, determine the nature of the change. That context dictates which issues matter and which are noise.

| Change Type            | Review Focus                                                            | What to Deprioritize                 |
| ---------------------- | ----------------------------------------------------------------------- | ------------------------------------ |
| Hotfix / minimal patch | Correctness, no regressions, blast radius                               | Style, naming, refactoring           |
| Library / SDK code     | API stability, breaking changes, downstream panic risk, backward compat | Internal style, non-critical perf    |
| New feature            | Architecture, correctness, error handling, API design                   | Minor naming, premature optimization |
| Refactor               | Behavioral equivalence, no regressions                                  | New features, scope creep            |
| Config / infra         | Correct values, security, environment parity                            | Code style                           |

**If you cannot determine the change type, default to "new feature" rigor.** When in doubt, review more rather than less.

## Workflow

### Phase 1: Investigate Before Judging

Build a mental model of the change before evaluating the code.

#### Step 1: Read the Git Diff

1. Get the full diff for the resolved scope. For uncommitted work, run `git diff HEAD` (staged + unstaged in one view) and `git status --porcelain`; `git diff` alone omits staged changes, and no diff form shows untracked files, so read every `??` file in full.
2. Parse each changed file: added lines, removed lines, modified regions
3. **Classify the change type** using the table above (hotfix, library, new feature, refactor, config)
4. Build a mental model: what is the author trying to accomplish?

**Output**: Change summary per file (type, intent, scope).

#### Step 2: Gather External Context

If external context sources exist, use them to sharpen your understanding.

1. Check for linked tickets (issue keys or numbers) in commit messages or branch names
2. Look for design documents: `docs/`, `designs/`, `*.md` files mentioning the feature
3. Read linked wiki or tracker pages when the environment provides access to them
4. Read `AGENTS.md`, `CONTRIBUTING.md`, or project-level documentation for conventions

**Exit when** each listed source has been checked once, or no external context exists; record missing context and move on. Do not broaden the search beyond the change's documented scope.

#### Step 3: Run Automated Diagnostics

Observe the environment, then run what's available. Assume no tool exists until you have seen it, because a missing tool reported as a failure misleads the user.

1. **Language-server diagnostics**: Use the environment's language-server diagnostics on each changed file when available. If no server covers that file type, skip silently.
2. **Linter discovery**: Observe project files and dependencies to find what it uses. Scan the declarations relevant to the changed language:
   - JavaScript/TypeScript: `package.json`, ESLint/Prettier config, `tsconfig`
   - Python: `pyproject.toml`, `setup.cfg`, `tox.ini`, `noxfile.py`
   - Rust/Go: `Cargo.toml`, `go.mod`, and `Makefile` or task-runner configs
     Verify each project-declared command is installed before running it. If nothing is found, skip.
3. **Build / type-check**: If discovered from observation, run it. If none found, skip.

**Key principle**: Every tool is optional. Missing tools are report notes, not errors. Record each attempted or skipped diagnostic and its reason.

#### Step 4: Historical and Codebase Context

For each changed file, understand its role in the larger system.

1. `git log --oneline -20 <file>`: check how mature the file is.
2. `git blame` on changed regions: check who wrote what, when, and why they might have done it that way.
3. **High-churn files (50+ commits)**: review carefully; changes here carry history and constraints.
4. **Library/SDK files**: check downstream consumers for panics, breaking changes, or behavioral shifts.
5. **New files**: check whether similar files exist and match established patterns.
6. **External research**: when a change uses an unfamiliar library, framework pattern, or domain concept, look up documentation and real-world usage before forming opinions.

**Research exit criterion**: For each unfamiliar library, framework pattern, or domain concept, stop when you have authoritative documentation or a real-world example that explains the relevant behavior and how it applies here. After two targeted searches without authoritative evidence, record the uncertainty and proceed conservatively; do not keep searching indefinitely.

**Investigation exit criteria**: End Phase 1 after every changed file has a change summary, relevant external and historical context has been checked, available diagnostics are recorded, and each unfamiliar concept is resolved with evidence or documented as uncertain. Do not continue investigating once these conditions are met.

### Phase 2: Apply Judgment

Now that you have full context, think like a senior engineer. For detailed review dimensions, read [references/review-criteria.md](references/review-criteria.md).

#### Step 5: Deep Review

Review each changed region with the rigor appropriate to its change type (see table above).

**Universal checks** (apply to all change types):

1. **Correctness**: Logic errors, off-by-one, wrong conditions, missing edge cases
2. **Error handling**: Swallowed errors, missing propagation, empty catches
3. **Security**: Injection, hardcoded secrets, missing validation (only when the change touches trust boundaries)

**Context-dependent checks** (apply based on change type):

| Dimension          | Hotfix | Library | New Feature | Refactor |
| ------------------ | :----: | :-----: | :---------: | :------: |
| Type safety        |   ○    |   ●●●   |     ●●      |    ●●    |
| API design         |   —    |   ●●●   |     ●●      |    ●     |
| Naming             |   —    |    ●    |     ●●      |    ○     |
| Complexity         |   ○    |    ●    |     ●●      |    ●●    |
| Performance        |   —    |    ○    |      ●      |    ○     |
| Concurrency safety |   ●    |   ●●●   |     ●●      |    ●●    |
| Downstream impact  |   ●●   |   ●●●   |      ●      |    ●●    |

**Legend**: ●●● = critical, ●● = important, ● = nice-to-have, ○ = only if obvious, — = skip

**For each issue found, record**:

- File, line(s)
- Category
- Severity: `critical` / `warning` / `suggestion`
- **Why it matters in this context** (cite the concrete failure mode, not generic "best practice")
- The specific risk or consequence if left unfixed

**When to search for more context during review**:

- You see an unfamiliar library function → search its docs before flagging usage as wrong
- The pattern looks odd but might be intentional → check git history for why it exists
- The change affects a public API → search for downstream consumers before suggesting breaking changes
- You're unsure about a language idiom → look it up, don't guess

**Search exit**: Stop a context search when you have evidence sufficient to explain the behavior and its consequence for this change. If two targeted searches yield no reliable answer, record the uncertainty and do not flag the behavior as wrong solely on assumption.

#### Step 6: Synthesize Findings

Evaluate findings together rather than as isolated items:

1. Merge issues from automated diagnostics (Step 3) and manual review (Step 5).
2. Deduplicate overlapping findings.
3. **Weigh fix cost against benefit** for each issue:
   - High benefit + low cost → recommend
   - High benefit + high cost → recommend, but flag scope
   - Low benefit + any cost → mention as optional, do not push
   - Issue exists but the change is a hotfix → note it, don't block the fix
4. **Think about cascading impact**: Will fixing issue A break B? Are there related issues that should be fixed together?
5. **Consider the library stability dimension**: If the change is in library/SDK code, any fix must preserve backward compatibility and not introduce panics for downstream consumers

### Phase 3: Present to User

#### Step 7: Present Findings and Interactive Fix Selection

Present a structured report covering context, findings, and rationale:

1. **Context summary**: What you reviewed, what change type you identified, what tools you ran
2. **Findings table** with severity, description, and **why it matters in this context**:

```
┌────┬──────────┬───────────────────────────────────────────┬──────────────────┐
│ #  │ Severity │ Issue                                     │ Why It Matters    │
├────┼──────────┼───────────────────────────────────────────┼──────────────────┤
│ 1  │ critical │ unwrap() on user input can panic          │ Library API —    │
│    │          │                                           │ downstream crash │
│ 2  │ warning  │ Missing error context in fetch            │ Debugging cost   │
│ 3  │ suggest  │ Magic number 404 in handler              │ Low priority     │
└────┴──────────┴───────────────────────────────────────────┴──────────────────┘
```

3. **Ask the user** which fixes to apply. Default: apply all. User can opt out of specific fixes.

#### Step 8: Fix Planning

For each approved fix:

1. Draft a concrete plan: what to change, why, before/after, risk, and dependencies.
2. Order fixes by dependency.
3. Flag risky fixes that need extra verification.
4. **Present the plan for final confirmation.**

See [references/fix-patterns.md](references/fix-patterns.md) for common fix patterns and before/after examples, and adapt them to the project's conventions.

### Phase 4: Execute and Verify

#### Step 9: Execute Fixes

For each approved fix, run this validation loop before proceeding to the next fix:

1. Apply one fix in dependency order.
2. Re-run all available diagnostics on the modified file.
3. If diagnostics are clean, continue to the next approved fix.
4. If diagnostics report a new failure:
   - Stop and identify whether it is caused by the fix.
   - If a follow-up fix is needed and is not covered by the user's approval, present it to the user and obtain approval before applying it.
   - Apply the approved follow-up, then return to step 2.
5. Repeat steps 2–4 until diagnostics for the current fix are clean. Only then proceed.
6. If a fix causes cascading errors: stop, revert, re-assess, and adjust the approach. If the cascade exceeds 5 files, re-plan with the user.
7. Never leave a file in a broken state between fixes.
8. **Match the project's existing conventions** by reading similar files first if needed.
9. If formatting tools are available, run them on modified files.

#### Step 10: Post-Fix Review

1. Enter this gate only after every approved fix has passed the Step 9 validation loop.
2. Re-run all available diagnostics on every changed file.
3. If any diagnostic fails:
   - Stop before generating the report and identify whether the failure is caused by an approved fix.
   - Present any unapproved follow-up fix to the user and obtain approval before applying it.
   - After approval, return to the Step 9 validation loop, then restart this gate.
4. Repeat steps 2–3 until all available diagnostics are clean. This is the gate's diagnostic exit criterion.
5. Run the build if available and run tests if available (unless told not to).
6. If a build or test failure needs a fix, present it to the user for approval, return to Step 9, and restart this gate after the approved fix passes validation.
7. Re-read `git diff` to review final state.
8. Verify every approved fix was applied correctly.
9. Check for unintended side effects.
10. Generate the final report only after all available diagnostics are clean and available build/tests pass or are explicitly unavailable or exempted.

## Gotchas

- **Fix cascading**: A "simple" type fix can cascade into 20 files. If cascade exceeds 5 files, stop and re-plan with the user.
- **Generated files**: Skip review of autogenerated files (look for `// Code generated by`, `@generated` headers).
- **Hotfix review**: When reviewing a hotfix, resist the urge to refactor. The goal is correct + minimal, not beautiful.
- **Library changes**: A cosmetic fix in a library can break downstream consumers. Always consider: "could this change cause a panic or behavioral change for someone using this API?"
- **Unfamiliar patterns**: If something looks wrong but you are unsure, research it before flagging. It may be an established idiom in that stack.

## Output Contract

Keep the human-readable report primary. On completion, return these sections in order:

1. **Context summary**: Change type, tools used, and scope reviewed
2. **Findings**: Each finding includes severity (`critical` / `warning` / `suggestion`), evidence (file/line, rule, or diagnostic), the issue, and why it matters here
3. **Diagnostics before/after**: Comparison of diagnostic results, including the final pass/fail table for each verification check
4. **Fixes applied**: Approved fixes that were applied and their validation results
5. **Fixes skipped with reason**: What the user chose not to fix and why
6. **Issues discovered but out of scope**: New issues found during post-fix review that were not part of the approved work

For downstream consumers, preserve this stable field order (a field contract, not a requirement to emit JSON):

```text
context_summary
findings[]: severity, evidence, issue, rationale
diagnostics_before_after
fixes_applied
fixes_skipped_with_reason
issues_discovered_out_of_scope
```

## References

- [Review Criteria](references/review-criteria.md): review dimensions with context-dependent weighting (Phase 2)
- [Fix Patterns](references/fix-patterns.md): fix principles and examples (Phases 3–4)
