---
name: how-to-read-code
description: >-
  A disciplined workflow for reading and analyzing unfamiliar source codebases.
  Use when the user asks to "read/analyze/explain a codebase or module", "how
  does X work internally", "investigate this open source project",
  "帮我读一下这个项目 / 分析一下这个模块的实现", or any deep source-code comprehension
  task. Converts the methodology from codedump's essay "How to Read Code" (2021)
  into an agent workflow: run it, clarify purpose, mainline vs subplot,
  horizontal vs vertical reading, scenario analysis, data structures first,
  active questioning, written report. Produces a structured code reading
  report, not just a verbal answer.
metadata:
  author: codedump (lichuang)
  version: "1.0.0"
  source: "How to Read Code (2021) — https://www.codedump.info/en/post/20200605-how-to-read-code/"
license: Apache-2.0
---

# How to Read Code (Agent Workflow)

Read an unfamiliar codebase like a senior engineer, not a tourist. The method below converts codedump's code-reading methodology ([How to Read Code](https://www.codedump.info/en/post/20200605-how-to-read-code/)) into agent-executable actions.

## Core principle: reading must produce output

Passive reading ("just look at the code") produces shallow understanding. Every phase in this workflow must end in a **durable artifact**: a note, a diagram, a runnable repro, or a written report. If a phase produces no artifact, it did not happen.

**The deliverable** is a structured code reading report (see `templates/report-template.md`). Do not end with a chatty answer only.

## Workflow

Follow the phases in order. Phases 2–4 alternate interactively in practice; the order below is the default entry order. The phases are **prerequisites, not bureaucracy**—skip them and the analysis becomes shallow guesswork.

### Phase 1 — Get it running (先跑起来)

Build a minimal runnable/debuggable environment **before reading any code deeply**.

- Locate build instructions (README, Makefile, CMakeLists, package.json, Dockerfile) and get the project compiling and running.
- **Reduce noise to the minimum**: prefer single-process, non-optimized, debug builds.
  - C/C++: `-O0 -g`, no LTO. Multi-process servers (e.g. Nginx-style): set workers = 1 so there is exactly one process to attach to.
  - Prefer debug entry points (e.g. run one test binary instead of the whole system).
- If the project cannot run locally (external deps, hardware, licensing), state this explicitly in the report and fall back to test cases + static reading. Do **not** hide the limitation.

Exit criteria: the target module's code path can be reached by an actual execution, or a documented reason why not.

### Phase 2 — Clarify the purpose (明确自己的目的)

Never start reading without a purpose. Determine, in this order:

1. What does the user actually want to know? If ambiguous, ask **one** focused question before reading. Examples: "understand one module's implementation" vs "understand overall framework architecture" vs "understand one algorithm".
2. Write the purpose down as the report's "Scope" section. Every later phase is judged against this purpose.

A purposeless full read-through wastes time and enthusiasm. This phase may shrink the scope by 10x—use it.

### Phase 3 — Mainline vs subplot (区分主线和支线剧情)

With the purpose fixed, classify every piece of code you encounter:

- **Mainline**: directly serves the user's stated purpose. Read it vertically, line by line.
- **Subplot**: everything else. **Treat it as a black box**—document only its external interface (name, input, output, effect), then move on. Do not descend into its implementation.

A typical example from the original methodology: "how is this dict implemented" is a subplot when your purpose is a business flow that merely *uses* the dict.

Self-check before diving into any file: "Is this mainline or subplot?" If subplot → interface note only.

### Phase 4 — Horizontal first, then vertical (纵横交替)

Two reading directions, deliberately alternated:

- **Horizontal** (横向): across modules, to understand the overall architecture. Do this FIRST for an unfamiliar project.
- **Vertical** (纵向): following one execution path in order, for a specific flow or algorithm. Do this only after horizontal context exists.

Rules of alternation:

1. **Whole before parts.** Never go deep into a detail before the overall picture is clear.
2. When you meet an unresolved function/data structure that does not block the whole picture, treat it as a black box (input/output), note it in the report's "black boxes" list, and move on.
3. After finishing a vertical pass, return to horizontal and check: does the new detail change the architecture picture? If yes, update the diagram before continuing.

### Phase 5 — Scenario analysis (情景分析)

This is the core technique. **Construct concrete scenarios and debug them**, instead of reading code statically and hoping to guess the flow.

- Pick an entry function relevant to the purpose, set a breakpoint (or add print/instrumentation log), then run a real input that triggers the code path.
- When it hits, capture: stack backtrace, key variable values, per-branch decisions. A single backtrace can outline an entire pipeline.
- Repeat for a few scenarios covering main cases (and one edge/error case when feasible).
- When a debugger is impractical, fall back to: unit tests, small written repro programs, temporary logging, or code tracing with explicit "unverified" markers.

Rationale: this converts a needle-in-haystack search into a bounded scenario, and the observed path is ground truth, not speculation.

### Phase 6 — Test cases are scenario documents (利用好的测试用例)

Good projects (e.g. etcd, Google OSS) ship rich tests. Tests are **pre-built scenarios**: single-scenario, self-contained inputs that exercise one path.

- Read tests for the target module as entry points for Phase 5, not as an afterthought.
- Prefer running/stepping through one test over reading ten source files.

### Phase 7 — Core data structures before code (理清核心数据结构的关系)

"Programs = algorithms + data structures"—in practice, **the data structures define the architecture**. "Bad programmers worry about the code. Good programmers worry about data structures and their relationships." (Linus Torvalds)

- Identify the handful of core data structures (types that appear in most module boundaries).
- Map their ownership & relationships in a diagram (who creates/holds/mutates; pointer or copy; lifetime).
- The house analogy: data structures are the building's frame; algorithms are the rooms. If you don't know the frame, you get lost no matter how carefully you read the rooms.
- This phase alternates with Phase 5 (scenario analysis), not ordered after it: read structures → run scenarios → refine the structure map → repeat until the user's question is answered.

### Phase 8 — Active questioning (多问自己问题)

Do not just extract facts; interrogate the code:

- Why was this data structure chosen for this problem? What do similar projects use in the same scenario?
- If I were to design this, would I do it the same way? What are the tradeoffs?
- Is there anything suspicious—dead code, duplicated logic, missing error handling?

Record the answers (or open questions) in the report. Output quality is proportional to learning quality; unasked questions are lost insights.

### Phase 9 — Write the report (写读码笔记)

Write the final artifact as if explaining to someone unfamiliar with the project (or to yourself six months later).

Rules (from the original methodology):

- **Prefer diagrams over prose over code.** Architecture and data-structure relationships belong in diagrams (mermaid where supported).
- **Avoid pasting large code blocks.** Large pastes fake understanding; use pseudo-code or reduced snippets instead. If line-level annotation is genuinely useful, suggest forking the project with comments (as the author did: [`etcd-3.1.10-codedump`](https://github.com/lichuang/etcd-3.1.10-codedump)).
- Imagine the reader is yourself months later. Optimize for future re-reading.

## Report requirements

The final deliverable is a report (template at `templates/report-template.md`) containing, at minimum:

1. Scope & purpose (Phase 2), and whether the project ran locally (Phase 1).
2. Architecture overview (horizontal pass) — with a diagram.
3. Core data structures & relationships — with a diagram.
4. Vertical analysis of the target flow(s) — with call path / sequence diagram.
5. Black boxes consciously left unopened, with their interfaces.
6. Active questions & design tradeoff commentary (Phase 8), including at least one "what would I do differently".
7. Open questions / suggested follow-ups.

## Depth calibration

Not every task needs all phases in full. Calibrate by the user's purpose:

| Purpose | Phases to run in full | Notes |
|---|---|---|
| "How does X work?" (one mechanism) | 1, 2, 3, 4 (light), 5, 7 (for X only), 9 | Keep it narrow |
| "Understand this project overall" | 1, 2, 3, 4, 6, 7, 9 | No deep vertical pass unless asked |
| "Why is this buggy/slow?" (investigation) | 1, 5 (heavily), 7, 8, 9 | Scenario analysis is the star |
| "Should we adopt/fork/learn from it?" | 1, 2, 3, 6, 7, 8, 9 | Emphasize 6 & 8 |

Anti-patterns to refuse:
- "Read the whole codebase thoroughly" without a purpose → push back, get a purpose first (Phase 2).
- Answering architecture questions purely from static file-listing without a scenario/check (Phase 5) → mark conclusions as static-analysis-only.