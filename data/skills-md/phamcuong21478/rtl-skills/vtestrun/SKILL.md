---
name: vtestrun
description: Run all IP-level testcases from tc_list.md through the bench Makefile, capture results, and write per-failure issue reports with no fix suggestions
effort: medium
model: sonnet
---

# Verilog Testcase Runner

## Overview

This skill runs every IP-level testcase listed in `tc_list.md` through the
Makefile-driven bench that `vtestgen` scaffolded, captures the build/simulation
logs, and writes a structured issue report for each failure.

The input is an IP name. The outputs are:

1. `./issue/<ip>/issue_NNN_<tcname>.md` — one file per failing testcase
2. `./issue/<ip>/run_summary.md` — overall pass/fail count and failure index

**This skill reports failure context only. It does not analyze root cause, propose
fixes, or suggest code changes.**

## Prerequisites

| Tool  | Purpose             | Check             |
|-------|---------------------|-------------------|
| xvlog | compile / lint      | `xvlog --version` |
| xelab | elaborate           | `xelab --version` |
| xsim  | simulate            | `xsim --version`  |
| make  | build orchestration | `make --version`  |

## Step 1 - Read the testcase list

Read `tb/<ip>/tc_list.md` and parse the testcase table into a run list. Include only
rows with status `OK`; skip rows with status `SKIPPED`.

For each entry record: `file` (the `.sv`), `module` (the `tb_*` module, equal to the
file base name), `category`, and `description`. Confirm `tb/<ip>/Makefile` and
`tb/<ip>/script/rtl.f` exist before proceeding.

## Step 2 - Create the output directory

Create `./issue/<ip>/` if absent. Do not delete existing issue files; new files use
the next available `NNN` index (continue from the highest existing index, else start
at `001`).

## Step 3 - Run each testcase

Run from inside `tb/<ip>/`. `vtestrun` is the **authoritative** pass/fail, but it
does **not** need to re-simulate testcases that `vtestgen` already ran — the
verdict is the same `[FINISH]` token. Re-running everything would just repeat
`vtestgen`'s self-check sims. The one thing it must never do is trust a **stale**
result (a `simulate.log` older than an RTL/TB source it depends on — e.g. after a
Phase 6 RTL fix), because the build rule no-ops while a `simulate.log` exists and
`make cleanf` keeps prior PASS dirs.

So **reuse a fresh result, rebuild only a stale (or missing) one** — per testcase:

```bash
# fresh = simulate.log exists AND no RTL/TB source is newer than it
if [ -f sim/tb_<module>/simulate.log ] && \
   [ -z "$(find ../../rtl ../../lib *.vh sti_*.sv sco_*.sv tb_<module>.sv \
                -newer sim/tb_<module>/simulate.log 2>/dev/null)" ]; then
    : # fresh — read its [FINISH] verdict directly, no re-sim
else
    rm -rf sim/tb_<module> && make tb_<module>   # stale/missing — rebuild fresh
fi
```

This makes the **first** run right after `vtestgen` a pure verdict-collection pass
(no second simulation), while a **post-fix** re-test rebuilds every testcase whose
RTL/TB changed (a fix touches `../../rtl`, so all dependent testcases re-run and a
regression is still caught). If you ever want to force the whole suite fresh
regardless of mtimes, use `make retest` (= `clean all`).

`make tb_<module>` produces `sim/tb_<module>/` containing `compile.log`,
`elaborate.log`, and `simulate.log`. After all testcases, `make report` prints a
one-line PASS/FAIL per testcase; use it to cross-check.

### Pass/fail decision

The decision is based **solely on the `[FINISH]` verdict token** in
`simulate.log` (see `.claude/skills/shared/CodingStyle.md`). Do not decide from the
presence of `[ERROR]` text — `[ERROR]` lines are collected only for the issue
report, not for the verdict.

A testcase is a **FAIL** if any of the following is true:
- `compile.log` (xvlog) or `elaborate.log` (xelab) reports an error / the build step failed
- `simulate.log` contains `[FINISH] FAIL`
- `simulate.log` contains no `[FINISH]` line at all (crash, or the run was killed by the timeout)

A testcase is a **PASS** only if `simulate.log` contains `[FINISH] PASS`.

## Step 4 - Write issue reports

For each FAIL, assign the next sequential issue number (zero-padded to 3 digits) and
write `./issue/<ip>/issue_NNN_<module>.md`. Fill every section from the captured logs.
Do not add analysis, speculation, or fix suggestions.

**Section: Testcase**
A table: File (`tb/<ip>/<file>`), Module, Category, Description.

**Section: Failure Summary**
The verbatim first `[ERROR]` line from `simulate.log` (the most diagnostic message).
If there is no `[ERROR]` line — e.g. timeout or crash — use the `[FINISH] FAIL` line,
or the first error line from `compile.log`/`elaborate.log` if the build failed. One
line only.

**Section: Simulation Log**
A fenced code block containing, in order of occurrence, up to the first 10 `[ERROR]`
lines from `simulate.log` and the `[FINISH] FAIL` line. If the build failed, include
the xvlog/xelab error lines from `compile.log`/`elaborate.log` instead and leave the
simulation portion empty. If the testcase timed out, include the last 10 lines of
`simulate.log` before termination.

**Section: Reproduction**
A fenced bash block:
```bash
cd tb/<ip>
make cleanf
make tb_<module>
# logs: sim/tb_<module>/{compile,elaborate,simulate}.log
```

**Closing note**
End the file with: `> This report documents observed failure context only. No fix is proposed.`

Rules for the Simulation Log section:
- Include up to the first 10 `[ERROR]` lines produced by `cpu_read_check` or explicit checks.
- Do not include `[INFO]` lines or Vivado tool banners.
- For a build failure, include the full xvlog/xelab error output.

## Step 5 - Write the run summary

After all testcases run, write `./issue/<ip>/run_summary.md`. Keep the Results
table as the one-metric-per-row shape below: `vflow`'s scanner (`scan.sh`) reads
the `Failed` count from the `| Failed | N |` row to decide whether Phase 6 is
needed, so the count must stay in the second column of that row.

```markdown
# Test Run Summary: <ip>

## Results

| Metric             | Count |
|--------------------|-------|
| Total run          | N     |
| Passed             | N     |
| Failed             | N     |
| Skipped (vtestgen) | N     |

## Failures

| Issue | Testcase | Category | Failure Summary |
|-------|----------|----------|-----------------|
| [001](issue_001_<module>.md) | tb_<name> | <category> | <first [ERROR] or [FINISH] FAIL line, truncated to 80 chars> |

## Skipped Testcases

| Testcase | Reason |
|----------|--------|
| tb_<name> | Skipped self-check in vtestgen |

---
> Run completed: <date and time>
```

If all testcases passed, write the summary with zero failures and omit the Failures
table.

## Known Issues and Fixes

<!-- Append issues found while running this skill. Format:
### [Tool] - <short title>
**Symptom:** ...
**Cause:** ...
**Fix:** ...
-->
