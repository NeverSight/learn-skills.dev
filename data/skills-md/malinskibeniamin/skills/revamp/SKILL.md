---
name: revamp
description: Run a large rewrite, port, or migration with baselines and mechanical-first translation.
disable-model-invocation: true
---

Large rewrites preserve behavior by separating mechanical translation from redesign. Source: https://bun.com/blog/bun-in-rust. Any executor follows repository model routing; invocation alone authorizes no agents.

## 1. Baselines before any code

- Freeze known defects so regressions remain distinguishable from old bugs.
- Benchmark throughput, memory, artifact size, and latency on the same workload/hardware.
- Count assertions; exit with none skipped, weakened, or deleted.

## 2. Tests are implementation-independent

Tests must target a language-independent CLI/API boundary, not the implementation being replaced. If coupled, decouple first as phase 0.

## 3. Mechanical first, idiomatic later

Translate 1:1, preserving architecture, names, and structure. Refactor only after parity. Port plus redesign makes failures ambiguous. Choose and record big-bang when bridges would linger; choose incremental when the system must keep shipping.

## 4. Trial run before fleet

Port three representative files through translate -> compile -> adversarial review -> tests. Use the trial to calibrate prompts, checks, and queue before scaling.

## 5. Mechanical work queue

Rank `cargo check`, `tsc`, or equivalent errors. Without delegation, work sequentially under one owner. With delegation or `/swarm`, isolate independent worktrees; each lane commits only its scope and never stashes, resets, or edits another.

## 6. Adversarial review with fresh context

Review from diff and contract, assuming semantic drift. At a non-trivial PR or ship endpoint, use only repository-permitted foreground cross-model review; otherwise perform a fresh inline evidence pass.

## 7. Semantic-equivalence traps

Probe release-erased assertions/side effects, integer overflow/bounds, copy-versus-reference defaults, recursion/stack limits with deeply nested fixtures, and locale/encoding defaults. Every discovered trap becomes a fixture.

## 8. Repair the process

When an executor fails, fix the prompt/checklist/queue and rerun rather than hand-fixing output. Humans inspect validation, spot-check, ensure CI kept tests, and own merge.

## Exit

- All prior tests pass; zero skipped/deleted; assertion count reconciled.
- Same-workload/hardware benchmark meets the recorded baseline.
- Bug ledger distinguishes pre-existing defects and new regressions.
- Every diff receives adversarial review under repository policy.
- Rollback is documented; old implementation stays shippable until exit.
