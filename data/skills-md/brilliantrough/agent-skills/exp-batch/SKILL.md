---
name: exp-batch
description: Execute one bounded research experiment branch in the current session with ponytail-for-experiments taste. Use when explicitly requested, or for a single coherent batch of runs with known configuration (one method × dataset × budget, or one ablation branch of a campaign). First check the branch was not already pruned or answered, grill only unresolved config decisions, preflight environment and resources, run per project conventions, and land metrics in the shared table in a shape the final figures can use directly. Prefer exp-discuss when the idea is still fuzzy and needs talking through; prefer exp-campaign when the work needs staged pruning across branches; prefer exp-probe for one-off spot checks.
---

# Exp Batch: confirm necessity → clarify config → preflight → run → land metrics

Small but complete: one branch, done right, plottable. Do not expand scope sideways into other branches; do not shrink rigor to save time.

## 1. Confirm the branch is still necessary

- Check project memory, the campaign plan, and existing results: has a probe already pruned this branch? Is the metric already measured under an equivalent configuration? If yes, say so and stop (or record why the earlier pruning does not apply).
- Restate in 2-3 sentences: what this batch adds to the final table/figure, which cells it fills, and its acceptance metric. No plan document.

## 2. Grill only unresolved config decisions

- Facts (paths, device availability, cache locations, prior configs) are yours to inspect. Ask the user only for choices that change the scientific meaning: hyperparameters not pinned by protocol, seed count, which split, callback-vs-reload coverage, formal vs exploratory status.
- Keep the batch's **metric contract identical to sibling runs**: same splits, same metric definitions, same surfaces. A batch measured differently cannot share a figure with the others — flag any deviation explicitly in the record.
- Ask one round of structured questions; a second round is allowed only when an answer opened a genuinely new scientific choice. If config decisions explode, the work is actually a campaign — propose `exp-campaign`.

## 3. Preflight: environment and resources

A run that starts without this pass is the run that fights someone else for the default device. It takes seconds, needs no approval, and happens before every launch — probe or formal, long or short. Skipping ceremony is the point (no scaffolding, no defensive code, no extra approval rounds); this one look is not ceremony.

- **Environment:** interpreter/environment activation, working directory, the dependency versions that are actually importable now, input paths present, output and checkpoint directories writable.
- **Know the platform first:** use the device platform the project's memory, conventions, or the session already names (CUDA / Ascend / MUSA / PPU-class / …). If it is genuinely unknown, read it off the environment (installed toolkit, device files, what the project's own launcher sets) or ask once; then work in that platform's own tool and variable vocabulary — wrong-platform errors are self-inflicted and cost runs.
- **Resources as they are, not as they usually are:** read the live device state with whatever this box uses — `nvidia-smi`, Ascend's `npu-smi`, MUSA's `mthreads-smi`, or the platform's equivalent — for utilization, memory, and **which process owns each device** (other people's jobs and this project's own parallel branches both count). Decide from that read and pass the device explicitly through the platform's visible-device variable (`CUDA_VISIBLE_DEVICES`, `ASCEND_RT_VISIBLE_DEVICES`, `MUSA_VISIBLE_DEVICES`, …); never let a run fall through to the default device. Disk for checkpoints/logs, and RAM/CPU when the job is not device-bound, come from the same look.
- **Collisions:** leftover jobs from earlier attempts ("did the last one really die?") and sibling branches are the usual hidden claim on a card; owner, name, and elapsed time in the process list settle it.
- **Cost:** an honest duration/memory estimate for this configuration, so later contention reads as contention instead of being blamed on the code.
- **Then run** under the project's rules on who launches what. If the free resources do not fit the configuration, do not start and do not silently shrink it: state what is short, and pick between waiting, another device, or an agreed config change.

## 4. Implement in this session, run under project conventions

- Implementation happens **here, in the same session**, after the researcher issues the go-ahead. No fresh-session handoff (that is exp-campaign's model); the researcher drives execution timing, and formal runs follow the project's rules on who launches them — the researcher runs them or grants explicit permission.
- **Module placement:** put each piece in the module it belongs to; keep experiment-specific code inside the experiment's own directory with its predictable layout, so the experiment is findable by name. Do not create a shared abstraction for one consumer; do split into separate modules when sibling branches would otherwise contend on one file.
- **Loose coupling:** consume stable shared libraries through their existing interfaces. Never modify shared internals to fit this batch, never add batch-specific branches to shared code. If an interface genuinely lacks something, stop and escalate — that is a campaign-level decision.
- **Ponytail research code:** the minimum code that runs the batch correctly. **No defensive programming:** no speculative validation, no "just in case" branches, no swallowed errors — on error, exit with the real error. When a run fails, first suspect the environment (device contention, full disk, stale cache, conflicting job) before the code; only change code when the evidence says the code is wrong.
- Watch for the known failure modes of this project class: OOM (yours or the machine's), NaN, checkpoint serialization, degenerate metric collapse (e.g., all-same-answer), and eviction — a neighbour's job or the kernel taking the device mid-run. On failure: preserve the failing artifact/log, isolate minimally, never report a failed run as a result row.
- **Separate "environment" from "code" before acting:** exit code, the log's last lines, and a fresh device read with the platform's own tool (is my process still alive? who owns the device now?) tell an evicted job apart from a real bug. An evicted run keeps its evidence, gets a free device chosen from the live read, and is requeued with the deviation recorded; only change code when the evidence says the code is wrong. A config changed to fit the resources must be flagged — it can break the metric contract with sibling runs.
- **These shapes are the pattern, not the whole space.** Unforeseen failures are yours to handle on the spot: decide, preserve the evidence, and say what you did. Do not stall waiting for a rule that does not exist, and never let a failure pass as a result.
- Negative results are results: record them with the same schema as successes.

## 5. Wait on long runs with `later` (delegated execution)

Long runs (device hours) must not hold the turn and must not be polled in a loop. The unattended pattern:

- **Delegation is explicit.** "Run it and check the results" delegates execution. If the researcher has not delegated, offer it before launching: "this needs ~Xh; I can run it in the background and resume automatically with the `later` tool — delegate to me?" State that each turn will end with a `later` schedule until the batch lands.
- **Launch in the background** per project conventions (nohup/tmux/launcher), then call the `later` tool: estimate the duration, add ~10% margin (5h run → schedule 5.5h), and write the prompt as a complete instruction to your future self — what to check, what to decide, what to run next.
- **End the turn** after scheduling — the `later` call is the LAST action of the turn: no idling, no spinning, no token-burning polls while waiting. The scheduled prompt arrives as a user message and resumes the session with no human present. Chain wake-ups across runs: each wake-up checks, decides, launches the next run, schedules the next `later`.
- **A timer is an estimate, not a completion signal.** On wake-up, verify the run actually finished and succeeded before recording metrics. If it is still running, re-estimate the remainder from observed progress (log/epoch counters, current throughput — contention can stretch a planned 5h run to 7h), never from the original plan, and schedule another `later` for that remainder plus margin. Repeat until the run actually finishes; there is no wake-up budget.
- If the host has no `later` tool, degrade: tell the researcher the expected duration and when to return, or follow the project's own waiting convention.

## 6. Land the metrics where figures can use them

- Every run lands in the shared results table with: id, config, split, surface, metrics, status, evidence path. Include every epoch/point recorded, not only the chosen one.
- Before finishing, check plottability: does this batch slot into the final figure as its own curve family, with the anchors (baseline reference lines) it needs? If the data shape would force an awkward plot (isolated points, mixed axes), fix the data collection now, not at figure time.
- **Batch report is mandatory — including for partial, blocked, or aborted work.** Write `<batch-or-stage>.report.md` beside the campaign plan (default `docs/experiments/<slug>.stage<N>.report.md`; a standalone branch goes in the project's experiment area) with: 完成情况总表 (per planned run/cell: 完成 / 部分 / 搁置 / 未动 + evidence path), the exact configs and commands that ran, what was not run and why, metric-contract deviations, failures and how they were handled (eviction / OOM / NaN), and what the campaign should reconsider. Never fake a result row, never silently skip a planned run.
- Report the same content concisely in chat. The planning session is **not** woken by this batch — the researcher brings the report back, so the file is what gets reviewed.
