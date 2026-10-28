---
name: vivado-simulate-rtl
description: Runs and diagnoses FPGA RTL simulations through Vivado using XSim, Questa, ModelSim, VCS, Xcelium, Riviera-PRO, or Active-HDL; supports approval-gated interactive repair; creates self-checking testbenches; runs UVM and seeded regressions; closes XSim code and functional coverage; verifies assertions; and captures SAIF or VCD activity. Use when users ask to simulate HDL, interpret or triage existing simulation logs (including Questa, VCS, Xcelium, or other third-party compile, elaboration, or run logs, and simulator crash or tool-defect reports), debug or repair RTL from waveform evidence, run gate-level or timing simulation, measure coverage, run random regression, analyze power activity, or generate portable stimulus.
license: MIT
compatibility: Requires Vivado (validated on 2025.2 and 2026.1) with the Vivado MCP server, and Python 3 for the bundled scripts. Third-party simulators need their own install, license, and version-matched compile_simlib libraries.
metadata:
  author: AMD Skill Developer
  version: "1.0.1"
  stage: beta
allowed-tools: Read Bash Write
---

<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# FPGA RTL Simulation

> **Early Access** - this skill may change before general availability.

Verify behavior against an explicit contract. A clean compile or simulator exit
is not functional proof.

## Tool policy

Use the Vivado MCP for project inspection and Vivado Tcl:

- `Vivado:vivado_start` — start one Tcl session.
- `Vivado:vivado_execute` — open/configure the project and launch simulation.
- `Vivado:vivado_status` — poll a command that is still running.
- `Vivado:vivado_log_messages` — inspect Vivado errors and warnings.
- `Vivado:vivado_doc_search` — verify unfamiliar or release-sensitive commands,
  and find Answer Records, known issues, and documented workarounds for an
  observed failure signature.

Documentation research is part of diagnosis, not an optional extra. A tool
crash, unsupported construct, or library failure is not final until it has
been researched; see
[references/known-issue-research.md](references/known-issue-research.md).

Use the exact configured server prefix if it differs from `Vivado`. Never issue
two `Vivado:vivado_execute` calls concurrently on one session. Keep one project open
while iterating.

Find simulators, licenses and compiled libraries through `PATH`, the
simulator's environment variables (for example `VCS_HOME` or
`MGLS_LICENSE_FILE`), the project's compiled-library settings, and paths the
user supplied. Do not scan the file system (`find /`, home directories,
network mounts) for them; if they are not found that way, report the
prerequisite as missing.

## Read the relevant reference

`references/` and `scripts/` paths are relative to this skill's directory, not
the workspace. Do not search the file system for them.

- XSim execution and artifacts: [references/xsim.md](references/xsim.md)
- Iterative XSim coverage closure:
  [references/xsim-coverage-closure.md](references/xsim-coverage-closure.md)
- XSim UVM, seeded regression, assertions, and functional coverage:
  [references/xsim-advanced-verification.md](references/xsim-advanced-verification.md)
- XSim SAIF, VCD, and portable sub-design stimulus:
  [references/xsim-activity-capture.md](references/xsim-activity-capture.md)
- Questa setup and execution: [references/questa.md](references/questa.md)
- ModelSim: [references/modelsim.md](references/modelsim.md)
- VCS: [references/vcs.md](references/vcs.md)
- Xcelium: [references/xcelium.md](references/xcelium.md)
- Riviera-PRO: [references/riviera.md](references/riviera.md)
- Active-HDL: [references/activehdl.md](references/activehdl.md)
- Release snapshot and shared third-party rules:
  [references/other-vivado-simulators.md](references/other-vivado-simulators.md)
- Failure diagnosis: [references/diagnostics.md](references/diagnostics.md)
- XSim error signatures and what they mean:
  [references/xsim-error-signatures.md](references/xsim-error-signatures.md)
- Answer Records and documented workarounds:
  [references/known-issue-research.md](references/known-issue-research.md)
- Deciding design defect versus simulator defect:
  [references/cross-simulator-arbitration.md](references/cross-simulator-arbitration.md)
- Reducing a failure to a reportable case:
  [references/minimal-reproducer.md](references/minimal-reproducer.md)
- Host, library, and license preflight:
  [references/environment-preflight.md](references/environment-preflight.md)
- Finding the release that introduced a regression:
  [references/version-bisect.md](references/version-bisect.md)
- Compile, elaborate, and runtime performance:
  [references/simulation-performance.md](references/simulation-performance.md)
- Waveform evidence without a GUI:
  [references/headless-waveform.md](references/headless-waveform.md)
- Approval-gated waveform-first repair:
  [references/guided-interactive-repair.md](references/guided-interactive-repair.md)
- Adding a backend: [references/adding-a-simulator.md](references/adding-a-simulator.md)

Read only the references needed for this request.

## Required inputs

Discover from the workspace and project before asking the user:

1. `.xpr` project, or explicit non-project source list
2. simulation set and top module
3. backend: default `xsim`; never silently substitute another backend
4. mode: behavioral, post-synthesis functional, post-implementation
   functional, or post-implementation timing
5. test contract and terminal PASS condition
6. bounded runtime or testbench-controlled termination
7. selected UVM test, seed list, plusargs, expected assertions, and coverage
   targets when advanced verification is requested
8. warm-up interval, measurement interval, hierarchy, and object set for SAIF,
   VCD, or portable-stimulus capture
9. requested artifacts: transcript, waveform, coverage, activity, generated
   testbench, and scripts

Ask only for inputs that cannot be discovered. For third-party simulators,
require the user-provided installation, license, and compiled-library paths.
Never guess site-specific paths.

## Preflight

1. Start or reconnect to a Vivado MCP session.
2. Open the `.xpr` project once, or load the non-project source list.
3. Confirm part, project mode, simulator, simulation sets,
   top modules, source files, compile order, include directories, defines, and
   language mix.
4. Confirm that the selected mode is available. Post-synthesis and
   post-implementation modes require the corresponding completed design stage.
5. Confirm a finite runtime. Do not use an unbounded `run all` unless the
   self-checking testbench has a proven watchdog and terminal `$finish`.
6. For a third-party backend, complete its reference preflight before changing
   `target_simulator`.
7. When a previous run failed to launch, linked against the wrong libraries, or
   the host is unfamiliar, run the environment doctor first. It is bundled at
   `scripts/sim_env_doctor.py` in this skill's directory; see
   [references/environment-preflight.md](references/environment-preflight.md).

Do not modify design RTL during preflight. Adding or editing verification-only
files is allowed when the user requested a testbench or coverage improvement.

## Common simulation workflow

Track this sequence for each target:

```text
- [ ] Discover project, simulation set, top, backend, mode, and contract
- [ ] Complete backend preflight
- [ ] Run a bounded simulation
- [ ] Read the complete transcript and identify the first failure
- [ ] Classify the result
- [ ] Research a documented cause and workaround for a tool or host failure
- [ ] Preserve transcript, waveform, scripts, and coverage artifacts
- [ ] Modify verification code only when requested
- [ ] Re-run the full applicable regression
- [ ] Report evidence, exclusions, and remaining risk
```

### 1. Discover

Use Vivado Tcl to query, not assume:

```tcl
get_filesets -filter {FILESET_TYPE == SimulationSrcs}
get_property TOP [get_filesets <simset>]
get_files -of_objects [get_filesets <simset>]
get_property target_simulator [current_project]
```

Update compile order before launch. Do not add duplicate sources already owned
by the project.

### 2. Run

Use the backend reference. Prefer a self-checking testbench and batch execution.
Close a prior active simulation before relaunching. A long-running
`launch_simulation` is blocking; allow an appropriate tool timeout and poll
status if the MCP reports it as still running.

### 3. Determine the verdict

Read the transcript and require all applicable gates:

- compile and elaboration succeeded;
- simulator returned normally;
- explicit terminal PASS marker or equivalent test-framework result exists;
- every required test completed;
- no unexpected error, fatal assertion, or timeout occurred.
- UVM summary has zero unexpected errors/fatals and the selected test completed;
- assertion results match the test plan without ignore or severity downgrade;
- randomized failures replay with the exact seed before being called
  reproducible;
- in timing mode, the simulator reported that SDF annotation succeeded. A
  skipped or ignored SDF means a zero-delay run, not a timing PASS.

Classify non-PASS as `design`, `testbench`, `environment`, `timeout`, or
`tool_defect` (reproducible tool failure on legal input) using
[references/diagnostics.md](references/diagnostics.md). Quote the first causal
error and its simulation time. Later cascaded errors are secondary.

### 4. Diagnose with focused evidence

Select clock/reset, transaction qualifiers, inputs, expected values, observed
outputs, and test status. Prefer interface and testbench signals; add internal
DUT signals only when necessary and available in the elaborated snapshot.

Do not edit RTL merely because a simulation failed. If the user asked only to
diagnose, stop after the evidence-backed diagnosis. If a DUT change is needed,
obtain approval and apply the smallest change that satisfies the contract.

#### Guided interactive repair (optional)

When the user requests step-by-step repair, waveform-first debugging, or an
approval pause before RTL changes, read
[references/guided-interactive-repair.md](references/guided-interactive-repair.md).
Preserve focused FAIL evidence, stop for an explicit repair/more-evidence/stop
decision, then—only after approval—make the smallest justified change, rerun
the affected test and applicable regression, and capture comparable PASS
evidence.

Do not enable this mode by default. Its pauses are inappropriate for unattended
CI, batch regressions, diagnosis-only requests, and pre-runtime failures with no
waveform.

### 5. Resolve environment and tool failures

An `environment` classification is a starting point, not an answer. When the
simulator crashed, rejected legal source, failed to link, or disagreed with
another tool, continue until the user has either a verified workaround or a
reportable defect:

1. Identify the signature and stage using
   [references/xsim-error-signatures.md](references/xsim-error-signatures.md).
2. Decide design versus simulator with
   [references/cross-simulator-arbitration.md](references/cross-simulator-arbitration.md)
   when another licensed backend is available.
3. Search for a documented cause and workaround with
   [references/known-issue-research.md](references/known-issue-research.md),
   then verify the workaround by rerunning the same bounded test.
4. If the failure is new since an upgrade, locate the boundary with
   [references/version-bisect.md](references/version-bisect.md).
5. If no workaround exists, reduce the case with
   [references/minimal-reproducer.md](references/minimal-reproducer.md) so the
   defect is reportable.

Report the Answer Record consulted, whether it applied, and what any
workaround changes. Never apply a vendor patch, alter the user's project, or
switch the requested backend without approval. Never claim a workaround works
without a rerun.

Slow but correct simulation is a performance question, not a failure; use
[references/simulation-performance.md](references/simulation-performance.md).
A broken viewer or missing display never blocks a verdict; use
[references/headless-waveform.md](references/headless-waveform.md).

### 6. Re-run

After any testbench or approved DUT change:

1. close the prior simulation;
2. rebuild from changed sources;
3. run the affected test;
4. run the full applicable regression;
5. compare the same evidence and acceptance gates.

Never claim success from a stale snapshot.

## Creating self-checking testbenches

When the user requests a testbench or coverage improvement:

- derive legal stimulus and expected behavior from requirements, interfaces,
  existing tests, and protocol documentation;
- reuse existing clocks, resets, agents, scoreboards, and project conventions;
- include deterministic checks with useful expected/actual messages;
- emit one unambiguous terminal marker such as `TEST_PASS`;
- include a watchdog that fails with the current phase and simulation time;
- avoid force/deposit/backdoor access unless the verification plan requires it;
- keep tests deterministic by default; record seed and plusargs when randomized;
- never weaken an assertion, checker, or acceptance gate to obtain PASS.

Generated testbenches are verification artifacts, not proof until they have
been run successfully.

## XSim coverage closure

When coverage is requested, read
[references/xsim-coverage-closure.md](references/xsim-coverage-closure.md) and
iterate:

1. run the unchanged regression and export baseline statement, branch,
   condition, and toggle coverage;
2. identify a reachable uncovered behavior and tie it to a requirement;
3. add focused stimulus plus a self-checking observation;
4. rerun the targeted test and then the full regression;
5. export a new uniquely named coverage database/report and compare deltas;
6. repeat while coverage improves and regression correctness is retained.

Do not game coverage. Never exclude reachable logic, remove checks, add DUT
backdoors, or change RTL solely to increase a metric. Separate untested,
unreachable, and elaborated-out items. Ask before adding exclusions or changing
RTL. Stop at the requested target, a justified plateau, or a blocking
requirement/environment gap.

## XSim advanced verification

For UVM, constrained-random, assertion-aware, or functional-coverage requests,
read [references/xsim-advanced-verification.md](references/xsim-advanced-verification.md).

- create one manifest per test and seed;
- select the UVM test and record every plusarg;
- preserve exact failing seeds and replay before diagnosis;
- report immediate, concurrent, UVM, and checker results separately;
- treat functional bins and crosses as requirement-linked targets;
- merge only compatible passing coverage databases;
- never ignore assertions/coverage or downgrade error/fatal severity to pass.

## XSim activity and portable stimulus

For SAIF, VCD, or sub-design replay, read
[references/xsim-activity-capture.md](references/xsim-activity-capture.md).

- separate reset/warm-up from the bounded measurement interval;
- log only the intended hierarchy or object set;
- close and verify every activity file;
- require the simulation's independent functional PASS;
- treat `create_testbench` output as scaffolding until it has an oracle,
  watchdog, terminal marker, and successful replay;
- do not claim power signoff or cross-simulator portability from artifact
  generation alone.

## Result report

Report:

```text
Backend and version:
Project / simulation set / top:
Mode and runtime:
Functional verdict: PASS | FAIL | INCONCLUSIVE
Failure class and first causal message:
Cross-simulator matrix (when arbitrated):
Known issue / Answer Record and whether it applied:
Workaround, verification result, and what it changes:
Tests run / passed / failed:
Coverage before -> after (if requested):
UVM test / seeds / replay:
Assertions passed / failed / disabled / unsupported:
Activity window and hierarchy:
Artifacts: transcript, waveform, coverage, SAIF, VCD, generated testbench/scripts
Changes made:
Not verified / exclusions / blockers:
```

Do not claim timing closure, CDC correctness, formal proof, equivalence,
security, safety compliance, or hardware validation from simulation alone.
