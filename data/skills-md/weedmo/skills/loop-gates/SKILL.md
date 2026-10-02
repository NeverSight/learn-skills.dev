---
name: loop-gates
description: "How the delegated loops (pr-babysit, autocode, matt-auto's ship step) use the unlazy skill so that \"done\" is a measured verdict: one runnable GATES.md ledger per unit, coordinator-approved, re-verified with gate-check.mjs, a retry bound, Orca boundaries. Reference skill, never invoked standalone."
---

# Loop gates (shared, on top of unlazy)

A loop gets every unit of work back as a delegate's *report*, and a confident "done" is not evidence. unlazy turns completion into a ledger of runnable checks the coordinator re-executes itself; this file is the one convention for it, so a PR, an autocode run, and a matt-auto ship end the same way.

unlazy is not vendored: `npx skills add Leonxlnx/unlazy -g` installs it; the installer and `auto-update.sh` keep it present.

## Locate it, once per run

```bash
UNLAZY_DIR=""
for d in "$HOME/.claude/skills/unlazy" "$HOME/.codex/skills/unlazy" "$HOME/.agents/skills/unlazy"; do
  [ -f "$d/scripts/gate-check.mjs" ] && UNLAZY_DIR="$d" && break
done
```

Present → gates are on; the tally goes on the board. Missing → ask once whether to install it; on decline, or where you cannot ask, say `unlazy absent — verification is the delegate's own checks` once and continue. Gates never block a start, only what counts as finished.

## The ledger

One ledger per unit — a PR, an autocode run, a matt-auto ship — at `.unlazy/<loop>/<unit>.GATES.md`, written **before** dispatch from the unit's own acceptance criteria:

- One gate per required outcome. Runnable (`CHECK:` + `EXPECT:` — the repo's test/build/lint commands, `gh` for PR state, a metric script) wherever a command can decide; manual only when none can, its evidence then the user's explicit answer, never the delegate's.
- `CHECK:` is code. The coordinator writes the commands and therefore approves the ledger itself (`node "$UNLAZY_DIR/scripts/gate-check.mjs" --approve <ledger>`); never approve one you did not write or read. Give every gate `CWD: <repo root relative to the ledger>` when the ledger lives outside the repo root (CHECK resolves relative to the ledger), and wrap regex expectations in `/…/`; otherwise EXPECT is a plain substring.
- Keep `CHECK:` lines stable — thresholds come from files (`state.json`, `program.md`), never baked in — so one approval keeps the loop autonomous.
- Tell the delegate the ledger path defines "done". Keep `.unlazy/` ignored.

## Verify, retry, escalate

- When the delegate returns, the **coordinator** runs `gate-check.mjs --reverify <ledger>` itself. The delegate's claim, a `worker_done`, a "tests pass" — signals, none evidence.
- Unmet gates go back to the same route with the unmet ids, **at most twice**; then the unit stops as a handoff naming them. A stop that is not completion becomes `ABANDON: <id> <reason>` in the ledger, never a quiet success.
- A unit is complete only on `ALL MET`. Work that integrates (a merged branch or PR) is re-verified **after** integration, on the merged code.
- Report the tally (`met/total`) on the board and in the report data (`gates: { met, total }`, `gateList` with `CHECK` and expected-vs-actual for the unmet); an unmet gate the user cannot see is one they cannot act on.

## Boundaries

- Gates verify *execution*, never design readiness: interviews, specs, plans, and hypotheses get no gates and no readiness scores.
- Gates never replace escalation: a material decision still stops the loop, and a gate "passed" on the delegate's say-so is not a pass.
- Under Orca orchestration, Orca owns dispatch, waiting, and retry; unlazy owns gates and evidence. Never unlazy's Parallel/Orchestrated mode (`OWNS:` leases, dispatch waves, `dispatch.json`) alongside Orca — two dispatchers; worktree isolation replaces leases. One Solo ledger per unit; the evidence that counts is produced on the coordinator's machine: fetch the branch, re-verify locally.
- No unlazy Stop hook from a loop, never in worker worktrees; the retry bound is the stop policy.

## Red flags

- A unit complete with unmet gates, or the delegate's "done" instead of `--reverify` → a confident report is not evidence.
- Approving a ledger you did not write or read → `CHECK:` runs on the user's machine.
- A third retry, or a higher tier to "get it green" → that is the handoff moment.
- Gates on design stages, or readiness percentages → verification is for work that ran.
