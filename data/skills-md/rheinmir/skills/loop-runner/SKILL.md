---
name: loop-runner
disable-model-invocation: true
description: Deterministic guardrailed agent-loop driver — wrap any step with propose → deterministic-verify → (critique → revise) and enforce hard termination guards (max_iter, wall-clock budget, no-progress via state-hash, escalate-to-human). The control loop + guards + progress detection are deterministic; the LLM critique/revise step is the one quarantined adapter. Trigger when an agent fix-loop must not spin forever and must not be able to argue its way around a failing test.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [harness/scripts/loop-runner.py]
---

# Skill: loop-runner

## WHAT

### Purpose và context
- **Purpose:** Drive an autonomous fix loop that CANNOT run away. VERIFY is a shell command whose exit-code 0
  means pass (pytest / tsc / a lint) — preferred over LLM self-judgment, because the agent cannot
  argue its way around a red exit code. The termination guards are MANDATORY and all deterministic.
- **Trigger (when to use):**
  - An agent loops edit-then-check repeatedly (fix failing tests, satisfy a typechecker/lint).
  - You need a hard guarantee it stops: bounded iterations, bounded wall-clock, stop-on-stall, escalate.
  - You want a replayable run-log + a reflexion lesson trail, without trusting the model to "decide it's done".
- **Non-goals:** not an LLM judge of "done"; not a place to tune guard values outside the config; no auto-invocation (`disable-model-invocation: true`).

### Mental model
`PROPOSE (workspace state) → VERIFY (shell exit code) → GUARDS (max_iter · budget_seconds · no_progress_k · escalate_after_iter) → REFLEXION (lesson line) → CRITIQUE → REVISE (quarantined adapter) → repeat`. Everything except CRITIQUE/REVISE is deterministic.

Build-now / adapt-later boundary:
- DETERMINISTIC (built + tested now): control loop, all guards, state-hash progress detection,
  run-log artifact, reflexion. → `harness/scripts/loop-runner.py`
- QUARANTINED adapter (`verified: false`): the LLM critique/revise step + the tunable guard values.
  → `harness/loop-runner.config.yaml` (the ONE file you edit to adapt). The default revise step is a
  no-op / shell stub, so the whole loop runs and self-tests WITHOUT an LLM.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | `--verify` | có | shell cmd; exit 0 = pass |
| In | `--config` | không | guard defaults (`harness/loop-runner.config.yaml`); CLI flags override config |
| In | `--revise` | không | shell cmd or real LLM-revise adapter; default no-op stub |
| In | `--state` | không | glob for state-hash; without it `no_progress_k` is off |
| In | `--log` | không | run-log path |
| Out | Run-log JSON | có | iterations, verdicts, termination reason at `run_log.path` |
| Out | Episodic lessons | on failure | appended to `reflexion.episodic_memory_page` (lazily created with valid frontmatter + `## Origin`) |
| Out | exit code | có | 0 SUCCESS · 2 MAX_ITER · 3 TIMEOUT · 4 NO_PROGRESS · 5 ESCALATE |

### Rules và capabilities
- RULE-01 (MUST): VERIFY is deterministic (exit code). NEVER let the LLM self-judge "done".
- RULE-02 (MUST): The guards are mandatory — never remove one to "let it finish".
- RULE-03 (MUST): Quarantined values (guard params + the revise hook) live ONLY in the config. The same value in two places is a leak.
- RULE-04 (MUST): Under `verified: false`, behave fail-safe: assume the revise guess is wrong until conformance proves otherwise.
- RULE-05 (MUST): The self-test must stay green and must NOT write into the real wiki (its episodic page is redirected to a temp dir).
- Capabilities: run shell commands (verify/revise); hash workspace files; write run-log + episodic wiki page.

### Failure boundaries
- VERIFY exit 0 → **succeeded** (SUCCESS, exit 0).
- `max_iter` reached → **failed** (MAX_ITER, exit 2).
- `budget_seconds` exceeded → **failed** (TIMEOUT, exit 3).
- State-hash unchanged K iterations → **blocked** (NO_PROGRESS, exit 4).
- `escalate_after_iter` hit → hand off to a human (ESCALATE, exit 5).

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | — | `python3 harness/scripts/loop-runner.py selftest` (5 guard scenarios, no LLM) | green | red → fix runner first, stop |
| W02 | deterministic | workspace | PROPOSE — current workspace state | state | → W03 |
| W03 | deterministic | `--verify` | VERIFY — run shell cmd | exit 0 → SUCCESS | non-zero → W04 |
| W04 | deterministic | counters, state-hash, clock | GUARDS — max_iter, budget_seconds, no_progress_k, escalate_after_iter | continue or terminal code 2/3/4/5 | terminal → write run-log, stop |
| W05 | effect | verdict | REFLEXION — append one lesson line to episodic page | lesson | → W06 |
| W06 | judgment | failure output | CRITIQUE → REVISE via quarantined adapter (LLM, stub or shell cmd) | new workspace state | → W02 |

Chi tiết từng bước (nguồn chân lý cho W01–W06):

#### How to run
```
# self-test — 5 deterministic guard scenarios, no LLM, no deps
python3 harness/scripts/loop-runner.py selftest

# real loop around a verify command (config supplies the guard defaults)
python3 harness/scripts/loop-runner.py run \
  --config harness/loop-runner.config.yaml \
  --verify "pytest -q" \
  --revise "<shell cmd, or the real LLM-revise adapter>" \
  --state "src/**" --log harness/out/loop-runner-run.json
```
CLI flags override config. Process exit: 0 SUCCESS · 2 MAX_ITER · 3 TIMEOUT · 4 NO_PROGRESS · 5 ESCALATE.

#### The loop (one iteration)
1. PROPOSE — the current workspace state (initial proposal, or the last iteration's revise).
2. VERIFY — run the shell cmd; exit 0 → stop SUCCESS.
3. GUARDS (checked every iteration, all enforced):
   - `max_iter` — hard backstop (always on; cannot be disabled).
   - `budget_seconds` — wall-clock budget (0 = off).
   - `no_progress_k` — state-hash unchanged for K consecutive iterations → NO_PROGRESS (off if no `state_paths`).
   - `escalate_after_iter` — hand off to a human → ESCALATE (0 = off).
4. REFLEXION — append one "lesson" line to the episodic-memory wiki page on failure.
5. CRITIQUE → REVISE — the quarantined adapter (the LLM, or a stub / shell cmd). Then repeat.

#### Output
- Run-log JSON (iterations, verdicts, termination reason) at `run_log.path`.
- Episodic-memory lessons appended to `reflexion.episodic_memory_page` (lazily created with valid frontmatter + `## Origin`).

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | capability_optional | `--state` / `state_paths` given | enable `no_progress_k` state-hash stall detection | absent → guard off | W04 |
| B02 | user_optional | `budget_seconds` or `escalate_after_iter` > 0 | enforce wall-clock budget / human escalation | 0 → off (`max_iter` stays always on) | W04 |
| B03 | capability_optional | real LLM-revise adapter wired | W06 uses the LLM; `verified: false` → fail-safe (RULE-04) | not wired → no-op / shell stub | W02 |

### Validation và stopping
Stopping is decided only by exit codes and guards, never by the model. `max_iter` cannot be disabled, so every run terminates. Selftest must stay green and write nothing into the real wiki.

### Examples
- **Positive:** `run --verify "pytest -q" --state "src/**"`, revise fixes the failing test on iteration 2 → VERIFY exit 0 → SUCCESS, process exit 0, run-log lists 2 iterations.
- **Boundary/failure:** revise stub never changes files under `src/**`, `no_progress_k=2` → state-hash equal 2 iterations → NO_PROGRESS, exit 4, lesson appended; the model cannot argue it's done.
