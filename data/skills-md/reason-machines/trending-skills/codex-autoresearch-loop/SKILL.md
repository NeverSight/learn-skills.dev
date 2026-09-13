---
name: codex-autoresearch-loop
description: Self-directed iterative research skill for Codex that continuously cycles through modify, verify, retain or discard, and repeat until a measurable goal is reached.
triggers:
  - run autoresearch on my codebase
  - iterate autonomously until tests pass
  - improve my code overnight without interruption
  - set up a modify verify loop
  - keep improving coverage until I say stop
  - eliminate all type errors automatically
  - run codex autoresearch skill
  - continuously optimize this metric
---

# Codex Autoresearch

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Codex Autoresearch is a Codex skill that runs an autonomous modify→verify→keep/revert loop on your codebase. You describe a measurable goal in one sentence; Codex confirms the plan, then iterates unattended — every improvement stacks in git, every failure reverts automatically — until interrupted or a cap is reached. Inspired by Karpathy's autoresearch concept, generalized beyond ML training to any software metric.

---

## Installation

**Option A — manual copy into your project:**

```bash
git clone https://github.com/leo-lilinxiao/codex-autoresearch.git
cp -r codex-autoresearch your-project/.agents/skills/codex-autoresearch
```

**Option B — Codex skill installer:**

```text
$skill-installer install https://github.com/leo-lilinxiao/codex-autoresearch
```

The skill lives at `.agents/skills/codex-autoresearch/` inside your project. No config file is required before first use.

---

## How to Activate

Open Codex in your project directory and prefix your goal with `$codex-autoresearch`:

```text
$codex-autoresearch
I want to get rid of all `any` types in my TypeScript code
```

Codex will:
1. Scan the repo and infer scope, metric, verify command, and guard command.
2. Present a confirmation summary — reply `go` (or correct anything).
3. Run the loop unattended until you interrupt it or the goal is met.

You never write config. Codex infers everything.

---

## Confirmation Flow

Before the loop starts Codex always shows what it found and asks you to confirm. Example exchange:

```
Codex: I found 47 `any` occurrences across src/**/*.ts.

       Confirmed:
       - Target: eliminate `any` types in src/**/*.ts
       - Metric: `any` count (current: 47), direction: lower
       - Verify: grep + tsc --noEmit as guard

       Need to confirm:
       - Run until all gone, or cap at N iterations?

       Reply "go" to start, or tell me what to change.

You:   Go, run overnight.

Codex: Starting — baseline: 47. Iterating until interrupted.
```

Up to five confirmation rounds are possible. After that, Codex proceeds.

---

## The Loop (internals)

```
PHASE 0: Probe environment (CPU/GPU/RAM/toolchains), check for session resume
PHASE 1: Read context + lessons file from prior run (if any)

LOOP (forever or N times):
  1. Review current state, git history, results log, lessons
  2. Pick ONE hypothesis (apply perspectives, filter by environment)
     -- or N hypotheses if parallel mode is active
  3. Make ONE atomic change
  4. git commit (before verification)
  5. Run verify command  →  did the target metric improve?
     Run guard command   →  did anything else break?
  6. Improved → keep (extract lesson)
     Worse    → approved rollback strategy (git revert)
     Crashed  → fix or skip
  7. Log the result to results log
  8. Health check (disk, git, verify health)
  9. If 3+ discards → REFINE; 5+ → PIVOT; 2 PIVOTs → web search
 10. Repeat. Never stop. Never ask.
```

The loop runs **unbounded** unless you say `Iterations: N` during confirmation.

---

## Dual-Gate Verification

Two commands serve distinct purposes:

| Gate | Purpose | Fails means |
|------|---------|-------------|
| **Verify** | Did the target metric improve? | Change discarded, reverted |
| **Guard** | Did anything else break? | Change reworked (up to 2 attempts), then reverted |

Guard files are **never modified** by the loop.

Example verify + guard pair for a Python coverage run:

```text
Verify: pytest --cov=src --cov-report=term 2>&1 | grep TOTAL | awk '{print $NF}'
Guard:  python -m mypy src --ignore-missing-imports
```

Example for TypeScript type cleanup:

```text
Verify: grep -r "any" src --include="*.ts" | wc -l
Guard:  npx tsc --noEmit
```

---

## Modes

Codex maps your sentence to one of seven modes automatically — you never pick a mode explicitly.

### `loop` — iterate toward a measurable target (default)

```text
$codex-autoresearch
Improve test coverage in src/ to at least 80%
```

```text
$codex-autoresearch
Reduce bundle size — it's currently 2.3 MB, get it under 1 MB
```

### `plan` — turn a vague goal into a validated loop config

```text
$codex-autoresearch
I want to make our API faster but I don't know where to start
```

Codex will interview you (p95 latency vs throughput? which endpoint?) and produce a ready-to-run loop config.

### `fix` — repair errors until count reaches zero

```text
$codex-autoresearch
pytest is failing, 12 tests broken after the refactor — fix them all
```

### `debug` — evidence-driven root-cause hunting

```text
$codex-autoresearch
Our API returns 503 randomly under load, no idea why
```

Each iteration tests one falsifiable hypothesis. Codex presents evidence, not guesses.

### `security` — read-only STRIDE + OWASP audit

```text
$codex-autoresearch
Is this code secure?
```

### `ship` — readiness verification and release gating

```text
$codex-autoresearch
Ship it
```

### `exec` — one-shot execution with no loop

```text
$codex-autoresearch
Run the benchmark suite and summarize results
```

---

## Inline Configuration (optional)

You can override defaults inline during the confirmation step — no file edits needed:

| Phrase | Effect |
|--------|--------|
| `Iterations: 20` | Cap the loop at 20 iterations |
| `Parallel: 3` | Test 3 hypotheses concurrently per round |
| `Guard: npm test` | Override the inferred guard command |
| `Verify: <command>` | Override the inferred verify command |
| `Scope: src/api/` | Restrict changes to a subdirectory |

Example during confirmation:

```
You:   Go. Iterations: 30, Guard: npm test, Scope: src/api/
```

---

## Cross-Run Learning

At the end of each iteration Codex writes a structured lesson to `.agents/skills/codex-autoresearch/lessons.md`:

```
Iteration 7 — KEPT
Hypothesis: replace explicit `any` with inferred generic in src/utils/mapper.ts
Change: added <T extends Record<string, unknown>> to mapKeys()
Result: any count 31 → 29
Lesson: Generic constraints on utility functions eliminate clusters of `any` downstream.
```

On session resume Codex reads this file first. Each new run benefits from prior runs.

**To resume an interrupted run:**

```text
$codex-autoresearch
Resume
```

Codex re-reads the lessons file, checks git state, re-establishes the baseline, and continues.

---

## Parallel Experiments

Request parallel mode during confirmation or at any time:

```text
You:   Go, parallel 4
```

Codex runs four hypotheses concurrently, keeps the best result, discards the rest. Useful when hypothesis space is large.

---

## Pivot Protocol

If the loop stalls, escalation happens automatically:

| Consecutive discards | Action |
|---------------------|--------|
| 3 | **REFINE** — narrow hypothesis, try smaller atomic changes |
| 5 | **PIVOT** — change strategy entirely |
| 2 PIVOTs | **Web search** — Codex fetches external references to unstick itself |

You are never asked for permission during escalation. The loop continues.

---

## Real Code Examples

### Example 1 — TypeScript `any` elimination (Python verify script)

If you want a custom verify script instead of a one-liner:

```python
# scripts/count_any.py
import subprocess, sys

result = subprocess.run(
    ["grep", "-r", "--include=*.ts", r"\bany\b", "src/"],
    capture_output=True, text=True
)
count = len(result.stdout.strip().splitlines())
print(count)
sys.exit(0)  # always exit 0; the number is what matters
```

Tell Codex during confirmation:

```text
Verify: python scripts/count_any.py
Guard:  npx tsc --noEmit
```

### Example 2 — pytest coverage loop (Python)

```python
# scripts/coverage_pct.py
import subprocess, re, sys

out = subprocess.check_output(
    ["pytest", "--cov=src", "--cov-report=term", "-q"],
    stderr=subprocess.STDOUT, text=True
)
match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", out)
if match:
    print(int(match.group(1)))
    sys.exit(0)
print(0)
sys.exit(0)
```

```text
$codex-autoresearch
Improve test coverage — target 85%

Verify: python scripts/coverage_pct.py
Guard:  python -m mypy src
Direction: higher
Target: 85
Iterations: 50
```

### Example 3 — bundle size loop (Node.js project)

```bash
# scripts/bundle_size.sh
#!/usr/bin/env bash
npm run build --silent 2>/dev/null
du -k dist/bundle.js | awk '{print $1}'
```

```text
$codex-autoresearch
Reduce our JS bundle size, currently ~2300 KB, target under 900 KB

Verify: bash scripts/bundle_size.sh
Guard:  npm test
Direction: lower
Target: 900
```

### Example 4 — lint warning count (any language)

```bash
# scripts/lint_count.sh
#!/usr/bin/env bash
npx eslint src/ --format json 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(sum(len(f['messages']) for f in d))"
```

```text
$codex-autoresearch
Get our ESLint warning count to zero

Verify: bash scripts/lint_count.sh
Direction: lower
Target: 0
```

---

## Unattended Runs

For overnight or long runs, ensure Codex CLI approval settings do not interrupt `git commit` or `git revert` commands. The simplest option is to run in a disposable or sandboxed repo clone:

```bash
git clone . /tmp/autoresearch-sandbox
cd /tmp/autoresearch-sandbox
# launch Codex here with full permissions
```

Results accumulate in git history. Pull the winning commits back to your main repo when done:

```bash
# in your main repo
git fetch /tmp/autoresearch-sandbox main
git cherry-pick <winning-commit-sha>
```

---

## Session Artifacts

| File | Contents |
|------|----------|
| `.agents/skills/codex-autoresearch/lessons.md` | Structured lessons from every iteration |
| `.agents/skills/codex-autoresearch/results.log` | Full per-iteration log (metric value, kept/reverted, elapsed) |
| `.agents/skills/codex-autoresearch/session.json` | Current session state for resume |

These files persist across Codex sessions. Delete them to start fresh.

---

## Troubleshooting

**Loop reverts every change:**
- Verify command may be returning a non-numeric value. Test it manually: `bash -c "<your verify command>"` should print a single number.
- Metric direction may be wrong. Confirm `Direction: lower` or `Direction: higher` during setup.

**Guard fires on unrelated files:**
- Narrow scope: `Scope: src/specific-module/`
- Or tell Codex explicitly: `Do not touch tests/` during confirmation.

**Session resume picks up wrong baseline:**
- Delete `session.json` to force a fresh baseline: `rm .agents/skills/codex-autoresearch/session.json`

**Parallel mode produces merge conflicts:**
- Codex handles this internally via the pivot protocol, but if it gets stuck, reduce parallelism: `Parallel: 2`

**Codex asks questions mid-loop:**
- This means a guard crash produced ambiguous output. Pre-empt it by specifying `Guard: <command> || true` if guard failures should be non-fatal, or by giving Codex fuller sandbox permissions so it can run git commands freely.

**Loop hits PIVOT but makes no progress:**
- Supply a seed hypothesis during confirmation: `Hint: try tree-shaking unused imports first`
- Or run `plan` mode first to produce a richer hypothesis list before switching to `loop`.

---

## Quick Reference

```text
# Start a loop
$codex-autoresearch
<your goal in one sentence>

# Resume interrupted run
$codex-autoresearch
Resume

# Bounded run
$codex-autoresearch
<goal> — Iterations: 25

# Parallel hypotheses
$codex-autoresearch
<goal> — Parallel: 4

# Force a mode
$codex-autoresearch fix
pytest has 8 failures, repair them

# Read-only audit
$codex-autoresearch security
Audit src/api/ for injection vulnerabilities
```
