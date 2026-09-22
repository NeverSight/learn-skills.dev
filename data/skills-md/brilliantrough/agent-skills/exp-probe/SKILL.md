---
name: exp-probe
description: Run one-off research spot experiments with minimal ceremony. Use when explicitly requested, or for a missing datapoint, a rerun after failure (OOM, crash), a sanity check of one configuration, a minimal bug reproduction, or a cheap measurement that a campaign needs before deciding. At most one focused question; run, record, report in one line. Escalate to exp-batch if the spot check turns into a branch, or exp-campaign if it reveals a decision tree; if the question itself is still fuzzy, route back to exp-discuss.
---

# Exp Probe: ask once if needed → run → record → one line

A probe exists to answer one question cheaply. Everything about it is minimal except honesty.

- **Define the single question first** ("does config X fit in memory", "is this NaN reproducible", "what is the missing anchor value"). If you cannot name the question, this is not a probe.
- **Shrink, don't distort:** reduce sample counts and steps, never the semantics being measured (sequence length, batch semantics, dtype). State exactly what was shrunk when reporting.
- **Reproduce the real entry point:** probes run through the same launcher/flags as the real run (e.g., a preflight mode), not a rewritten ad-hoc path — a probe that bypasses the real path proves nothing about it. Probe code lives in the project's scratch/experiment area, isolated per probe, and follows the same rule as all research code: **no defensive programming** — minimum code, real errors exit as-is; environment failures (device contention, disk full) are diagnosed as environment, not patched around.
- **Preflight even when cheap:** the same pass as a real run, one look — environment active, and a live device read with the platform's own tool (`nvidia-smi`, `npu-smi`, `mthreads-smi`, …) that picks a free device and passes it explicitly through the platform's visible-device variable (never the default). A probe that lands on someone else's device wastes their run and yours.
- Probes are meant to be cheap, so waiting inline is normal. If a probe's run is long (full-size model sanity check, slow dataset), use the same delegated pattern as exp-batch: background launch + `later` wake-up instead of holding the turn.
- **One question to the user at most**, and only if the question itself is ambiguous. No plan docs, no grilling rounds, no sub-agents.
- **Record where the campaign can find it:** scratch area per project rules, with config, observation, and exit status. If the probe's answer prunes campaign cells, the claim and its evidence belong in the campaign's pruning ledger — say which cells it affects.
- **Report in one line:** question, observed answer, cost, and what it unblocks or rules out. If the answer is "unknown/inconclusive", say that and propose the next smallest probe — do not upgrade it silently into a batch.
