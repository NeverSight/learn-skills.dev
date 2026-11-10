---
name: test-iterate-loop
description: "Autonomously diagnose a codebase, apply minimal fixes, and rerun tests until they pass or a real blocker is reached. Use when the user explicitly requests an iterative fix-until-green loop across Python, R, Julia, or HPC workflows."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv*), Bash(pytest*), Bash(Rscript*), Bash(julia*), Bash(docker*), Bash(make*), Bash(git*), TaskCreate, TaskUpdate, AskUserQuestion
argument-hint: "[project-path] [--max-iter N] [--mock-hpc] [--container <image>]"
skill-dependencies: [computational-experiments]
---

# Test-Iterate Loop — Autonomous Bug Fix Cycle

> Autonomous loop: run tests → root-cause failures → apply minimal fix → retry. Bounded by iteration cap and same-error-repeat detector. Never commits — leaves clean working tree + markdown report. Generic across Python (pytest), R (testthat), Julia (Pkg.test), and HPC pipelines (mock-HPC Docker).

## Hard Rules

### Existential — block proceed

1. **Never `git commit`, `git push`, or modify `.git/` state.** All changes go into the working tree only. The user reviews the final clean tree + report and decides what to commit. Enforced via the standard forbid-list per `subagent-write-guard.md` if dispatching sub-agents.
2. **Bounded iteration: max 10 iterations OR 3-same-error-repeat — whichever first.** Hardcoded ceiling. Past that, stop and summarise. Don't ask "continue?" — exhaustion is the signal.
3. **Each iteration must change ≥1 file.** A no-op iteration (Claude couldn't propose a fix) counts as a same-error-repeat.
4. **Memory bug detector**: flag any iteration that adds a model load, env var change, or version pin without a corresponding test — these are common failure-cause patterns from past HPC sessions.

### Format — catch in review

5. Every iteration logged to `log/test-iterate/<project>-YYYY-MM-DD-HHMM.md` with: hypothesis, fix applied, result.
6. Final report at the same path summarises iterations, terminal state, and remaining failures (if any).
7. Use `TaskCreate`/`TaskUpdate` for live progress tracking — the user can see what iteration is running and why.

## When to Use

- A pipeline / library has failing tests and you want them fixed autonomously
- Pre-flight before submitting an HPC job (catch torch/transformers/CUDA mismatches in mock-HPC Docker before the real job queues)
- Refactor cycles: change → run tests → fix breaks → repeat
- Reproducing a failure on a fresh checkout

## When NOT to Use

- The test suite itself is broken (fix the tests first, or you'll loop trying to fix code to match wrong tests)
- The failure root cause is *external* (network, third-party API, hardware) — the active agent cannot fix those
- You want to *write* tests, not fix them — use `computational-experiments` or direct work
- The fix requires research / design decisions, not just code adjustment

## Modes

| Invocation | Behaviour |
|---|---|
| `test-iterate-loop` | Auto-detects test runner; iterates up to 10 |
| `test-iterate-loop --max-iter 5` | Lower iteration cap |
| `test-iterate-loop --mock-hpc` | Run tests inside the mock-HPC Docker container (catches HPC-specific torch/CUDA bugs pre-submission) |
| `test-iterate-loop --container <image>` | Custom Docker image |
| `test-iterate-loop --no-fix` | Run tests once, root-cause failures, stop without applying fixes (diagnostic mode) |

## Architecture

```
Phase 1 (detect)    → which test runner? pytest, testthat, julia, custom?
Phase 2 (initial)   → run tests, capture full failure log
Phase 3 (loop)      → for each iteration: hypothesis → fix → re-run → log
Phase 4 (terminate) → all-pass | iter-cap | same-error-3x → final report
```

## Phase 1: Detect test runner

Heuristics in priority order:

| Signal | Runner |
|---|---|
| `pyproject.toml` with `[tool.pytest]` or `tests/` dir + `*.py` | `uv run pytest --maxfail=1 -x` |
| `package.json` with `"scripts": {"test": ...}` | `npm test` |
| `DESCRIPTION` (R package) + `tests/testthat/` | `Rscript -e 'devtools::test()'` |
| `Project.toml` (Julia) | `julia --project -e 'using Pkg; Pkg.test()'` |
| `Makefile` with `test:` target | `make test` |
| `noxfile.py` or `tox.ini` | `nox` / `tox` |
| Custom runner specified by user (`--runner '<cmd>'`) | use that |

If multiple match, ask the user which.

## Phase 2: Initial run

Run the test command. Capture:
- Exit code
- Full stdout + stderr to `/tmp/test-iterate-<run-id>.log`
- Failure count, error types, first few failing test names

If exit 0: print "All green ✓" and exit. No iteration needed.

## Phase 3: Iteration loop

Per iteration:

1. **Hypothesis** — read the failure log; identify the root cause. Use the `Read` tool on the test file + the implementation file to confirm. Write the hypothesis to the iteration log:

   ```
   Iteration 3 — 2026-05-10 14:23
   Hypothesis: pytest fails on test_inventory_split because the function
   returns a list when it should return a dict (matches old API).
   ```

2. **Fix** — make the minimal edit to address the hypothesis. Document the file + line range in the iteration log.

3. **Re-run** — same test command.

4. **Log result** — pass / new failure / same failure:

   - **All pass** → exit loop, terminal state PASS.
   - **New failure** → fresh hypothesis next iteration.
   - **Same failure (3rd time consecutively)** → exit loop, terminal state STUCK.

5. **Memory-bug check** — if this iteration's fix added a `from <model>` import, a `.cuda()` call, an `os.environ[]` set, or a version pin (`torch==X.Y`), flag in the log with `[MEMORY-BUG-RISK]`. These are the patterns that bit past [HPC cluster] runs.

## Phase 4: Termination + report

Final report at `log/test-iterate/<project>-YYYY-MM-DD-HHMM.md`:

```markdown
# Test-Iterate Loop — <project>

**Started:** YYYY-MM-DD HH:MM
**Ended:** YYYY-MM-DD HH:MM
**Terminal state:** PASS | STUCK (same error 3x) | EXHAUSTED (hit iter cap)

## Iterations

| # | Hypothesis | Fix | Result |
|---|---|---|---|
| 1 | ... | ... | new failure |
| 2 | ... | ... | new failure |
| 3 | ... | ... | PASS |

## Final test output

```
<paste of last test run>
```

## Files modified

- `src/foo.py` (lines 42-58) — fix iteration 1
- `tests/conftest.py` (lines 12-15) — fix iteration 2
- ...

## Working tree

Clean (no commits made). User decides whether to commit, what to amend, or what to revert.

## Memory-bug flags

- Iteration 2: `[MEMORY-BUG-RISK]` — added `torch.cuda.empty_cache()` without a paired test
```

## HPC mock mode (`--mock-hpc`)

Use when iterating before submitting to [HPC cluster]. Runs inside a Docker container that mirrors [HPC cluster]'s environment:

- Default image: `user/hpc-mock:latest` (built from `scripts/hpc/Dockerfile.hpc-mock`)
- Container has same CUDA, torch, transformers, slurm-mock as [HPC cluster]
- Test command runs inside the container; failures bubble out to the iteration log

**Hard rule:** never run `--mock-hpc` against a project whose data lives outside the project directory — the Docker mount won't see it. Verify data paths first.

If `user/hpc-mock:latest` doesn't exist on the current machine, print the build instructions and exit.

## Standard forbid-list (when dispatching sub-agents)

If for very large iteration loops (>5 files modified concurrently) the orchestrator decides to dispatch sub-agents, each gets:

```
This sub-agent has a narrow scope. It does NOT inherit the orchestrator's
authorisation for any other action.

- Do NOT run `git add`, `git commit`, `git push`, or any other git write command.
- Do NOT modify files outside the scope I've named below.
- Do NOT run latexmk, pip install, uv add, or any package-management command.
- Do NOT modify CI configs or pyproject.toml dependencies.
- Read-only access except for the explicit edit scope.

Scope: <file paths>
Task: <hypothesis + fix>

Report your changes as a diff. The orchestrator runs the tests.
```

## Cross-References

| Skill / Rule | Relationship |
|---|---|
| `subagent-write-guard.md` | Sub-agent dispatch (when needed) follows this rule |
| the `code-review` agent | Run AFTER test-iterate-loop terminates PASS — quality scorecard |
| `computational-experiments` | The skill that *writes* the tests this loop iterates on |
| `code-paper-auditor` agent | Code-paper consistency check — orthogonal concern |

## Anti-Patterns

- **Don't** loop without a same-error-repeat detector — an agent can spin on the same issue forever.
- **Don't** auto-commit even on PASS — leave the clean tree for the user to review and stage as they want.
- **Don't** treat warnings as failures — only test exit code 0 means PASS. Warnings get logged but don't trigger iterations.
- **Don't** apply fixes to test files — that's a smell that you're fitting tests to broken code. Fix the code.
- **Don't** skip the memory-bug flag — past HPC sessions had `torch.cuda` and `TRANSFORMERS_OFFLINE` bugs that would have been caught with this signal.
