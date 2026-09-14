---
name: vflow
description: Scan project state to determine phase completion, write flow_status.md, and orchestrate the full RTL design flow from architecture to documentation
---

# RTL Flow Orchestrator

## Overview

Two responsibilities:

1. **State scan** — inspect project directories to determine each phase's completion for one IP, then write `./flow_status.md`.
2. **Flow execution** — drive the flow by invoking the right skill at the right time, pausing at checkpoints, and looping the debug-fix-retest cycle.

Input is an IP name, optionally followed by a mode keyword.

**Resolve the IP name before anything else — never guess across IPs.** `flow_status.md` and every downstream skill operate on exactly one IP.

**Single-IP-repo assumption.** The bundled scanner assumes the repo holds one IP: its Phase 2 and Phase 3 checks scan *all* of `ddoc/*_req.md` and `rtl/` rather than scoping to `<ip>_top`'s hierarchy. With one IP this is exact. If a repo ever holds two IPs, those two phase counts would mix submodules across IPs — scope them to the `<ip>_top` instantiation hierarchy before relying on the scan (see the note in `scan.sh`).

- Name given → use it.
- Not given, exactly one candidate top-level requirement `.md` in the project root (a `.md` that is not `CLAUDE.md`, `flow_status.md`, or other generated/status doc) → use it.
- Not given, two or more candidates → **stop and ask the user which IP** (list the candidates). No heuristic pick; never run more than one IP per invocation.
- Not given, no candidate → stop and report none found.

### Invocation modes

| Invocation | Behavior |
|------------|----------|
| `vflow [<ip>]` | **Scan and execute** (default): Step 1 → Step 2 → Step 3. |
| `vflow [<ip>] status` (also `scan`, `--scan-only`, `--dry-run`) | **Scan only**: Step 1 → Step 2, present `flow_status.md`, then stop. Touch no file but `flow_status.md`; invoke no downstream skill. |

## Step 1 - Scan Project State

**Never Read a whole `.md` to compute a status symbol.** All status comes from existence / mtime / `grep`/`awk` counts, which the bundled scanner already does. (Enumerating RTL_BUG *locations* for the Step 2 open-issues display is a targeted `grep` of `debug_summary.md`, not a whole-file read — that is allowed.) Run the scanner once from the project root; do not reissue per-check commands inline:

```bash
bash <skill-dir>/scan.sh <ip>
```

`<skill-dir>` is the directory containing this SKILL.md (the running copy — repo `skills/vflow/` or the global `~/.claude/skills/vflow/`). Resolve `scan.sh` as the sibling of this file. If it cannot be located or it errors out, fall back to performing the same existence/mtime/count checks inline rather than skipping the scan.

**Greenfield is normal.** A brand-new IP has only `./ddoc/<ip>.md` and no `./rtl` yet (Phase 1 creates `rtl/`). The scanner treats a missing `./rtl` as the pre-architecture state and reports `P1 PENDING` (everything downstream PENDING) — it does **not** error. `ERR:` is emitted only when `./ddoc` itself is absent (you are not at a project root). So on a greenfield run, proceed straight to Phase 1 (`varch`); do not treat `P1 PENDING` as a problem.

It prints one compact line per phase signal: `P1 DONE|PENDING`, `P2 d/n`, `P3 left=N`, `P4 DONE|PENDING`, `P5 RUN|SCAFFOLDED|NONE`, `P7 DONE|PENDING`, and (only when a run exists) `FAILED=N`, `DEBUG=current|stale|none`, plus `RTLBUG=N` when `DEBUG=current`. A `?` value (`FAILED=?`, `RTLBUG=?`) means the count row was malformed/absent in `run_summary.md`/`debug_summary.md` — inspect that file's breakdown manually rather than assuming `0`. `RTLBUG` is read from the classification breakdown in `debug_summary.md`'s Results section; it depends on that section listing a per-class count. If it prints `ERR: …`, you are not at a project root or the layout is non-standard — stop and resolve that.

### Phase status from the scan output

| Phase | DONE | Otherwise |
|-------|------|-----------|
| 1 – Architecture | `P1 DONE` | PENDING |
| 2 – Design | `P2 d/n` with `n>0 && d==n` | `⚠ IN PROGRESS (d/n)`; `n==0` means nothing to design yet → PENDING (Phase 1 not DONE), never DONE |
| 3 – Implementation | `P3 left=0` (and Phase 2 DONE) | `⚠ IN PROGRESS` (markers remain) |
| 4 – Synthesis | `P4 DONE` | PENDING |
| 5 – IP Testing | `P5 RUN` | `⚠ IN PROGRESS` if `SCAFFOLDED`, else PENDING |
| 6 – Debug | `FAILED=0`, or `DEBUG=current` with `RTLBUG=0` | failures + `DEBUG=none`/`stale` → debug pending; `DEBUG=current` with `RTLBUG>0` → `⚠ IN PROGRESS` (awaiting fix) |
| 7 – Documentation | `P7 DONE` | PENDING |

Caveats (one rule each):
- **Phase 3** reports marker state only — absence of `//@` is not proof lint/sim passed. Sim-pass is enforced at execution time (Phase 3 pauses on failure), so a re-scan must not upgrade a module on marker absence alone while a known sim failure is unresolved.
- **Phase 6 currency** — `vtestrun` overwrites `run_summary.md` each re-test while a prior `debug_summary.md` lingers; `DEBUG=stale` means that report predates the latest run and does NOT satisfy Phase 6. Treat debug as not-yet-run for the current failures.

## Step 2 - Write flow_status.md

Overwrite `./flow_status.md` (a live snapshot, not history).

- **Header** — IP name and scan date.
- **Phase table** — one row per phase. Symbols: `✓ DONE`, `⚠ IN PROGRESS (N/M)`, `✗ PENDING`, `✗ BLOCKED (<reason>)`, `✗ ERROR (<reason>)`. BLOCKED = a prerequisite phase isn't DONE; ERROR = the phase's skill aborted (see Orchestration Rules).
- **Next action** — one line for the immediate next step. Normally a skill invocation + target (e.g. `vfill → rtl/foo_ctrl.v`). May instead be a non-skill state: **wait** (parked at a user gate, e.g. `WAITING on user RTL fix (Phase 6B)`), **blocked** (what must finish first), or **error** (which phase errored).
- **Open issues** _(only if `run_summary.md` shows `FAILED>0`)_ — the Failed count. If `DEBUG=current`, list each `RTL_BUG` root-cause location (one line per unique location); if `stale`, note debug must be re-run.

## Step 3 - Execute the Flow

**Scan-only mode stops here** — present `flow_status.md` and invoke no skill.

Otherwise execute the next incomplete phase. A DONE phase is skipped entirely.

---

### Phase 1 — Architecture `[CHECKPOINT]`

**When:** Phase 1 PENDING.

Run `varch` on the IP requirement file; it writes `ddoc/<ip>_arch.md` and derives the per-submodule `_req.md` files and `rtl/<ip>_top.v`.

**Checkpoint:** present the module decomposition and interfaces; wait for explicit approval. On change requests, edit `ddoc/<ip>_arch.md` and re-run `varch` (it regenerates only affected submodules and reports the change set), then re-present. No advance without approval.

---

### Phase 2 — Design `[CHECKPOINT per submodule]`

**When:** Phase 2 PENDING or IN PROGRESS.

For each submodule in `ddoc/` lacking `rtl/<module>.v`:

1. Run `vdesign` on `ddoc/<module>_req.md`.
2. **Checkpoint:** present that proposal; wait for approval before the next submodule. Revise and re-present on change requests.

One at a time. Do not batch-approve.

---

### Phase 3 — Implementation `[AUTO]`

**When:** Phase 3 PENDING or IN PROGRESS.

Run `vfill` on each `rtl/<module>.v` (not `<ip>_top.v`) that still has `//@` markers. The top skeleton's `//@` are integration notes, not fill directions — never `vfill` it.

Process pending submodules sequentially, no checkpoints. If `vfill` fails lint or sim, report and pause — do not continue while errors are unresolved.

---

### Phase 4 — Synthesis `[AUTO]`

**When:** Phase 3 DONE, Phase 4 PENDING.

Run `vsynth` on the full IP — target the top module `<ip>_top`, so the report lands at `synth/<ip>_top/synth_report.md` (the path the scan checks). No checkpoint; include the Fmax/utilization one-liner in the status and continue.

---

### Phase 5 — IP Testing `[AUTO]`

**When:** Phase 4 DONE, Phase 5 PENDING or IN PROGRESS.

Run `vtestgen` (scaffold + generate the suite), then `vtestrun`. If the bench is already scaffolded with `tc_list.md` (was IN PROGRESS), resume — don't re-scaffold. After `vtestrun`, read `FAILED`:
- `0` → skip Phase 6, go to Phase 7.
- `>0` → Phase 6.

---

### Phase 6 — Debug and Fix Loop `[AUTO + GATE]`

**When:** Phase 5 DONE and failures exist.

#### 6A — Debug
Run `vdebug` in batch mode on the IP.

#### 6B — Gate: await user RTL fix
Present: total open failures; every `RTL_BUG` (classification, file, module, block, one-line description); `TC_BUG` entries (need testcase fixes); `DOC_AMBIGUITY` entries (need clarification). State explicitly: **"RTL fixes are required before the flow can continue. Signal when fixes are applied."**

`TC_BUG`/`DOC_AMBIGUITY` don't block. If no `RTL_BUG` remains, skip the gate and go to Phase 7.

#### 6C — Re-test after fix
On the user's signal:

1. Run `vtestrun` again — the test result is ground truth that the fix took effect. `vtestrun` rebuilds every testcase whose RTL/TB sources are newer than its last `simulate.log`; an RTL fix touches `rtl/`, so **all** dependent testcases re-simulate (a regression in a previously-passing testcase is caught, not skipped) while unrelated results are reused. (This overwrites `run_summary.md`, making the old `debug_summary.md` stale per the currency rule.)
2. New failures → run `vdebug` on them (writes a current `debug_summary.md`) and return to 6B.
3. None → Phase 7.

Repeat until clear or the user stops.

---

### Phase 7 — Documentation `[AUTO]`

**When:** all prior phases DONE and no open `RTL_BUG`. That precondition is established by 6B/6C, or by Phase 5 with zero failures — Phase 7 is reachable only those ways; by any other path, return to Phase 6.

Run `vdoc` on the IP. Then re-run **Step 1–2** (scan + write `flow_status.md`) — not the whole skill — and present the all-DONE status as the completion summary.

---

## Orchestration Rules

- **Never skip a CHECKPOINT.**
- **Never re-run a DONE phase** unless asked.
- **Never proceed past a Phase 3 lint/sim failure.**
- **Stop on any phase abort.** A *result* (skill completed, reported failures/timing miss) is handled by the phase's rules; an *abort* (missing input, crashed tool, exception, malformed artifact) is not — stop, mark the phase `✗ ERROR (<reason>)`, surface the skill's output verbatim, never advance. Applies to the `[AUTO]` phases too. (Tool-unavailable is the one pre-classified abort → `✗ BLOCKED`, below.)
- **No RTL probe cleanup needed.** `vdebug` never edits `rtl/`/`lib/`; its probes live only in a disposable testbench include and `vdebug` removes them.
- **Always update `flow_status.md`** after each phase.
- **Never fabricate tool output.** If a required tool is absent (Vivado for P4, xsim for P5), mark that phase `✗ BLOCKED (tool unavailable: <tool>)`, report it, and continue scanning the rest.

## Known Issues and Fixes

<!-- Add entries as discovered. Format:
### <short issue title>
**Symptom:** / **Cause:** / **Fix:**
-->
