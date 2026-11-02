---
name: polythis
description: Language-fit audit for any codebase in any language. Use when the user asks whether a project, service, or module should be rewritten or partly ported to another language (C, C++, Rust, Go, C#, Java, Zig, Swift, etc.), whether the current language is the right choice, or where a native addon, WebAssembly, a sidecar, or a language consolidation would pay off. Also use when hot paths, GC pauses, CPU-bound work in an interpreted runtime, memory blowups, slow startup, or bug-prone low-level code suggest a different language might fit better, including Electron, Node, Python, JVM, and .NET native-module decisions.
license: MIT
metadata:
  author: marquezinii
  version: "1.0.0"
  homepage: https://github.com/marquezinii/polythis
---

# polythis: the right language for every part

## Overview

You are auditing **language fit**. For each meaningful part of the repository, decide whether the language it is written in is the best tool for that job and, if it is not, whether moving it is worth what the move costs.

**Core principle: the default verdict is KEEP.** A port must beat two cheaper options first: optimizing in place and adopting an existing native-backed library. It must still win after paying for the boundary, the build, the distribution, and the people who will maintain it. Most real wins are one narrow, hot, stable module behind a coarse interface. Whole-project rewrites are almost never the answer.

This skill is an **audit**. Deliver the report and stop. Do not port, rewrite, or scaffold code unless the user explicitly asks; if they do, follow [After the verdict](#after-the-verdict).

## When to use

- "Should this be in Rust / C++ / Go / C# instead?" or "Is JavaScript / Python the right choice here?"
- A module is CPU-bound in an interpreted or GC runtime: image, audio, video, compression, crypto, parsing, simulation, search, geometry, ML inference glue.
- Latency spikes from GC pauses, event-loop blocking, GIL contention, cold start, or memory bloat.
- Recurring bug classes the language invites: null/undefined crashes, type confusion, memory corruption in C/C++, data races.
- Deciding between a native addon, WebAssembly, a sidecar process, or a microservice for one component.
- Desktop and Electron apps that might move heavy work into native modules; mobile apps weighing shared native cores.
- A repo with too many languages, where consolidating would remove a toolchain.

**Not for:** choosing a stack for a greenfield project with no code (answer directly, using [language-profiles](references/language-profiles.md) if useful), general refactoring with no language question, or micro-optimizing one function.

## Workflow

Copy this checklist into your task list and complete every item in order.

```
- [ ] 1. Frame the goal and constraints
- [ ] 2. Inventory the repository
- [ ] 3. Shortlist candidate seams (max ~5) plus consolidation candidates
- [ ] 4. Gather evidence for each candidate, labelled by strength
- [ ] 5. Walk the options ladder for each candidate
- [ ] 6. Score with the rubric and apply the hard gates
- [ ] 7. Write the report from the template
```

### 1. Frame

Infer from the request and the repo; ask only if a wrong guess would change the verdict.

- **Goal:** throughput, latency, memory, startup time, reliability/safety, maintainability, hosting cost, binary size, hiring.
- **Constraints:** deployment targets (browser, Electron, serverless, mobile, embedded, server OS/arch), team languages, release cadence, licensing.
- **Scope:** whole repo, one service, or one module.

If the user gave no goal, assume "general language-fit health check" and state the assumption at the top of the report. **The deployment target constrains everything**: a browser can only take WebAssembly; serverless punishes big native binaries and slow cold starts; Electron needs ABI-matched native builds per platform.

### 2. Inventory

Run the bundled inventory (Node 18+, no dependencies, read-only):

```bash
node <path-to-this-skill>/scripts/inventory.mjs <repo-root> --months 12
```

It reports languages and line counts, build manifests, existing interop (FFI, addons, WASM, sidecars), per-module mix, hotspots (size × churn), bug-fix and perf-fix commit density, and files with heavy compute patterns in dynamic languages. Add `--json` for machine-readable output.

If Node is unavailable, approximate with `git ls-files`, a line count per extension, and `git log --since=12.months --format= --name-only | sort | uniq -c | sort -rn | head -30`.

Then read the build manifests, entry points, architecture docs, CI config, and deployment config. Write down the runtime and the deployment target for each module.

### 3. Shortlist candidate seams

Partition the code into modules (packages, directories, services). Classify each module's dominant workload:

| Workload | Typical signal |
|---|---|
| CPU-bound compute | tight loops over numbers, bytes, pixels, samples; profiler shows self-time in user code |
| I/O-bound / glue | awaits on network, disk, DB; CPU mostly idle |
| Latency-critical | p99 targets, real-time audio/video/input, trading, games |
| Memory-heavy | large in-memory datasets, many small objects, GC pressure |
| Concurrency-heavy | many connections, parallel pipelines, shared mutable state |
| Correctness-critical | parsers, protocols, crypto, money, auth, file formats |
| Blocking a UI or event loop | CPU or sync I/O on a UI thread, Electron main process, Node event loop, or async handler |
| UI | views, components, styling |
| Tooling / scripts | build, codegen, CI, one-off scripts |
| Data / query | filtering, joins, aggregations done in app code |

Use the signal catalog in [references/signals.md](references/signals.md) to find candidates. Only CPU-bound, latency-critical, memory-heavy, concurrency-heavy, and correctness-critical modules are usually worth porting. I/O-bound glue and UI almost never are. Data/query work usually belongs in the database, not in a faster app language.

**Blocking is about *where* code runs, not how fast it is.** A freeze caused by work on a UI thread or event loop is fixed by moving the work off that thread (rung 1). A faster language on the same thread only shortens the freeze. Fix the placement first, then judge speed separately.

Also look for the reverse problem, **language sprawl**: a third language used for a few hundred lines of tooling the main language handles fine, or two services in different languages doing the same job. These are CONSOLIDATE candidates.

Keep at most about five candidates. Breadth without evidence is noise.

### 4. Gather evidence

Rank evidence by strength and label every claim in the report:

| Label | Meaning |
|---|---|
| `[measured]` | production metrics, traces, or profiles |
| `[benchmarked]` | a reproducible benchmark you or the repo ran |
| `[profiled]` | a profiler run on representative input |
| `[history]` | git history, issues, incident notes (e.g. repeated fixes of one bug class) |
| `[inferred]` | reading the code |

Add `, synthetic` to the label when the input was made up rather than representative (`[benchmarked, synthetic]`). Synthetic results support medium confidence at most.

**Never invent numbers.** If running something is cheap and safe (an existing benchmark, timed tests, `node --cpu-prof`, `py-spy`, `perf`, `dotnet-counters`, `go test -bench`, JFR), run it. Otherwise state exactly which measurement would settle the question and on what input.

**Benchmarking rules for an audit:**
- Write benchmark scripts **outside the repository** (a temp or scratch directory) and import the repo's code from there. Never modify the repo.
- Never install dependencies, toolchains, or candidate libraries without asking. If a rung-2 library cannot be tried, label its expected gain `[inferred]` or cite the library's published benchmarks as `[external]`.
- Keep runs short and safe: no network calls, no writes outside the scratch directory, no production data.

**Do the Amdahl check for every performance claim.** If the module takes a fraction *p* of end-to-end time, the best possible overall speedup is `1 / (1 - p)`. A 50× faster module at 10% of runtime yields at most 1.11× overall. Write the number down. If *p* cannot be measured, give your estimate with its basis, label it `[inferred]`, and name the measurement that would pin it down.

### 5. Walk the options ladder

For each candidate, evaluate the rungs in order and stop at the first one that meets the goal:

0. **KEEP**: the problem is not real, not large, or not worth the cost.
1. **OPTIMIZE IN PLACE**: better algorithm or data structure, batching, caching, fewer allocations, streaming, worker threads or multiprocessing, vectorized libraries, JIT-friendly code, a faster runtime (Bun, PyPy, GraalVM, .NET AOT).
2. **ADOPT LIBRARY**: a maintained, native-backed library already does it (sharp, orjson, polars, simdjson, re2, libvips, ffmpeg, ONNX Runtime).
3. **EXTRACT**: move only this module into another language behind a coarse boundary (addon, FFI, WASM, sidecar).
4. **REWRITE SERVICE**: replace one deployable service.
5. **REWRITE PROJECT**: almost never; needs overwhelming evidence and a funded plan.

Pick the target language with [references/language-profiles.md](references/language-profiles.md). Pick the boundary with [references/interop.md](references/interop.md). The boundary is a first-class design decision: a fast module behind a chatty boundary is slower than the original.

**Verdict vocabulary.** Use exactly these words:

| Verdict | Meaning |
|---|---|
| KEEP | leave it as is |
| OPTIMIZE IN PLACE | same language: better algorithm, data layout, threading, or placement |
| ADOPT LIBRARY | replace hand-written code with a maintained (often native-backed) library |
| PILOT | time-boxed spike of a port behind a flag, with a pass/fail metric |
| EXTRACT | move one module to another language behind a boundary |
| REWRITE SERVICE | replace one deployable service |
| REWRITE PROJECT | replace everything (almost never) |
| CONSOLIDATE | port a small-footprint language into the main one to drop a toolchain |
| REMOVE | delete the code; the platform or an existing tool already does it (e.g. `npm version` replacing a release script) |

When the right answer is staged, chain verdicts with `→` in order of execution: `OPTIMIZE IN PLACE → ADOPT LIBRARY` means "fix this now, then do that". Each step needs its own justification.

### 6. Score

Score only candidates whose ladder reached rung 3 or higher. If the ladder stopped at rung 0 to 2, write `Not scored: stopped at rung N` with the reason, and move on. Do not score rejected port options "for reference".

Score each remaining candidate 1 (low) to 5 (high):

| Benefit | What it measures |
|---|---|
| **Gain** | improvement on the user's goal **after** the Amdahl check |
| **Fit** | how much better the target language suits this workload |
| **Pain** | bugs, incidents, workarounds attributable to the current language |

| Cost | What it measures |
|---|---|
| **Boundary** | call frequency, marshalling, async/thread-model mismatch |
| **Migration** | size, test coverage, behavioral parity risk |
| **Ops** | toolchains, CI matrix, prebuilt binaries per OS/arch, ABI, image size |
| **Team** | who maintains it, current skills, bus factor, hiring |

`net = 2 × Gain + Fit + Pain − (Boundary + Migration + Ops + Team)`

| net | Verdict |
|---|---|
| ≥ 6 | EXTRACT / REWRITE SERVICE |
| 2 to 5 | PILOT: time-boxed spike behind a flag, with a pass/fail metric |
| ≤ 1 | fall back to OPTIMIZE IN PLACE, ADOPT LIBRARY, or KEEP |

**Hard gates (override the score):**

- No EXTRACT or REWRITE when Gain rests only on `[inferred]` evidence. The ceiling is PILOT, and the pilot must name the measurement that would upgrade it.
- No REWRITE PROJECT unless every major module independently scores EXTRACT and the user's goal cannot be met incrementally.
- No port of code without a parity oracle (tests, golden files, or a reference implementation to diff against). Building that oracle becomes step 1 of the plan.
- A target language nobody on the team can maintain caps the verdict at PILOT unless the user explicitly accepts that risk.

### 7. Report

Write the report with [references/report-template.md](references/report-template.md): verdict table first, then one section per candidate with evidence, options considered, score, boundary design, risks, and the next concrete step. Lead with what to do Monday morning. Use [references/case-studies.md](references/case-studies.md) for calibration on what good verdicts look like.

## Quick reference: workload to usual best fit

Starting points to test against evidence, not answers:

| Workload | Usually strongest | Usually avoid moving to |
|---|---|---|
| Hot numeric / byte / pixel loops in JS, Python, Ruby, PHP | Rust, C++, C, Zig; WASM in browsers | another dynamic language |
| Low-latency, no-GC-pause paths | C++, Rust, C; tuned Java/C# with zero-alloc code | languages with stop-the-world GC and no tuning |
| High-concurrency network services | Go, Rust (tokio), Java (virtual threads), C#, Elixir/Erlang | single-threaded runtimes without a worker strategy |
| Parsers, protocols, untrusted input | Rust, memory-safe managed languages | C or C++ without fuzzing and sanitizers |
| Windows desktop, Office/COM, Unity | C# / .NET | C++ unless profiling demands it |
| Shared core for iOS + Android + desktop | Rust (uniffi), C++, Kotlin Multiplatform | duplicating logic per platform |
| Data transformation and aggregation | SQL in the database, Polars/DuckDB, Spark | a faster general-purpose language |
| CLI tools needing one static binary | Go, Rust, Zig, .NET AOT | runtimes that need an interpreter installed |
| Glue, orchestration, I/O-bound APIs | keep the current language | any rewrite |

## Red flags: stop and re-check

- "X is faster" with no profile, benchmark, or Amdahl number.
- Recommending a port of I/O-bound code.
- A boundary crossed per item inside a hot loop (chatty FFI, per-row IPC).
- Porting code that has no tests or golden outputs to compare against.
- Distribution ignored: prebuilt binaries for Windows, macOS arm64/x64, Linux glibc/musl, Electron ABI, mobile.
- Recommending the language you like rather than the one the workload needs.
- Rewriting something that takes 5% of runtime.
- Recommending a whole-project rewrite.

**Any of these means: go back to step 4 and get evidence, or downgrade the verdict.**

## Rationalizations to reject

| Thought | Reality |
|---|---|
| "Rust/C++ is obviously faster" | Only for CPU-bound work, only on the hot path, only after the boundary cost. Show the numbers. |
| "A rewrite will also clean up the design" | That is a refactor; do it in the current language first. Rewrites reproduce old bugs and add new ones. |
| "The team can learn it" | Price it: ramp-up time, review quality, on-call. Without a named owner, cap at PILOT. |
| "It's only a small module" | Small code with a large ops cost (native builds on every platform) is not small. |
| "No profiler is available, so I'll estimate" | Estimate, label it `[inferred]`, and let the gates cap the verdict. |
| "The user wants a rewrite, so I should recommend one" | The user wants the right answer. Say KEEP when KEEP is right, and explain why. |

## After the verdict

Only when the user asks to proceed with an EXTRACT or PILOT:

1. Freeze the interface: types in, types out, errors, threading model.
2. Build the parity oracle: characterization tests or golden files from the current implementation.
3. Build the benchmark harness on representative input and record the baseline.
4. Implement the new module behind the same interface with a feature flag or fallback path.
5. Run both implementations and diff outputs (shadow mode) before switching.
6. Wire CI for every target platform and ship prebuilt binaries where needed.
7. Switch over, keep the fallback for one release, then delete the old path.

Report the measured before/after numbers, not the predicted ones.
