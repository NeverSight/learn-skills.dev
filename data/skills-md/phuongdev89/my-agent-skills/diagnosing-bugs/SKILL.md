---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Quy định Session Directory (Bắt buộc)

Mọi hoạt động điều tra lỗi, tạo harness kiểm thử, lưu snapshot lỗi hoặc ghi log vết trong quá trình chẩn đoán phải được cô lập trong thư mục session:
- **Thư mục gốc**: `./.scratch/`
- **Cú pháp định danh**: `./.scratch/yyyy-mm-dd_diagnosing-bugs_công-việc-viết-không-dấu`
  - *Ví dụ*: `./.scratch/2026-09-22_diagnosing-bugs_fix-audio-sync-issue`
- **Cấu trúc thư mục con bắt buộc**:
  - `input/` (hoặc `raw/`): Chứa dữ liệu lỗi đầu vào, HAR files, raw log dumps, replay payload, fixtures gây crash.
  - `output/`: Chứa báo cáo chẩn đoán (`DIAGNOSIS_REPORT.md`), patch đề xuất, nhật ký xác minh fix lỗi.
  - `scripts/`: Chứa các test harness tạm, throwaway repro scripts, bisection scripts (thay vì viết trực tiếp ở root repo).
  - `temp/`: Chứa log tạm thời (tagged `[DEBUG-...]`), trace capture, profile dumps, intermediate snapshots.
- **Quy tắc cấm xả rác**: Tuyệt đối không tạo file repro script, ghi log tạm, lưu network dump xả ra root repo (`cwd`). Mọi file phát sinh trong quá trình chẩn đoán phải nằm trọn vẹn trong session directory.

Khởi tạo session trước khi thực hiện chẩn đoán:
```bash
SESSION_DIR="./.scratch/2026-09-22_diagnosing-bugs_ten-cong-viec"
mkdir -p "$SESSION_DIR/input" "$SESSION_DIR/output" "$SESSION_DIR/scripts" "$SESSION_DIR/temp"
```

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug — one that goes red on _this_ bug — you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server (lưu script vào `$SESSION_DIR/scripts/test_curl.sh`).
3. **CLI invocation** with a fixture input (đặt fixture tại `$SESSION_DIR/input/fixture.json`), diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network (lưu script tại `$SESSION_DIR/scripts/ui_repro.js`).
5. **Replay a captured trace.** Save a real network request / payload / event log to disk (lưu vào `$SESSION_DIR/input/trace.json`); replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call (lưu tại `$SESSION_DIR/scripts/harness.py`).
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode (lưu script tại `$SESSION_DIR/scripts/fuzz.py`).
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it (lưu harness tại `$SESSION_DIR/scripts/bisect.sh`).
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs (lưu output diff tại `$SESSION_DIR/temp/diff.log`).
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `$SESSION_DIR/scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you (lưu tại `$SESSION_DIR/temp/hitl_out.log`).

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight — a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion — a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (paste the invocation and its output), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to _catch this specific bug_.
- [ ] **Deterministic** — same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via `$SESSION_DIR/scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop — jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2 — Reproduce + minimise

Run the loop. Watch it go red — the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (hoặc lưu trữ lại trong `$SESSION_DIR/temp/` / `$SESSION_DIR/scripts/` để tham khảo)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns
- [ ] Báo cáo chẩn đoán và nghiệm thu được lưu tại `$SESSION_DIR/output/DIAGNOSIS_REPORT.md`

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) hand off to the `/improve-codebase-architecture` skill with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.
