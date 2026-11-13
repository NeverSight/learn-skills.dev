---
name: vllm-pytorch-ci-triage
description: Root-cause a vLLM torch-nightly CI regression report. Reads the pre-fetched, ANSI-stripped cluster logs from the triage artifact, identifies the real exception per regressed cluster, groups clusters by shared root cause, routes each cause to pytorch/pytorch, infra, or vllm-project/vllm, and writes findings.md / findings.json. Inputs are produced upstream; it has no Buildkite/ClickHouse access, files no issues, and retries no jobs. Use in the vLLM torch-nightly triage cron's root-cause step.
---

# vLLM × PyTorch torch-nightly CI root-cause

Read-only root-cause analysis for the vLLM torch-nightly triage cron. The upstream
`triage` job runs the A/B (torch nightly vs same-commit baseline), parses the logs, and
hands off artifacts; this skill reads that artifact, root-causes each regressed
cluster, groups by shared cause, routes each cause to the right repo, and writes its
findings to `findings.md` / `findings.json`. It has no Buildkite/ClickHouse access, files
no issues, and retries no jobs — tools are `Read`, `Glob`, `Grep`, `Write`.

Routing knowledge derived from the multi-week triage of vLLM PR #40077 (torch 2.12.0 +
triton 3.7.0), which filed 16+ issues under umbrella `pytorch/pytorch#180899`.

---

## Step 1: Read the cluster logs

The upstream `triage` job already produced the files — you do not run the parser or
fetch anything. Your tools are `Read`, `Glob`, `Grep`, `Write`; there is no Python
execution and no Buildkite / ClickHouse access. Read what is on disk in the triage input
dir:

- `report.md` — a concise, human-readable A/B summary and regressed clusters. Its
  **Test-set regressions** list deliberately renders each new failed test only as
  ``<test_id> — <pytest_exception_class>``; it does not include tracebacks.
- `report.json` — the structured companion: `torch_nightly_build`,
  `baseline_build`, `commit`, the `regressed` / `both` job lists, and
  `regressed_tests`. Each `regressed_tests.new_failures` entry is a complete
  `FailedTest` signature (`test_id`, `pytest_exception_class`,
  `exception_chain`, `inline_message`, `test_is_infra`). Each shared failure has
  complete `torch_nightly` and `baseline` `FailedTest` entries.
- `cluster-logs/<safe-cluster-name>.log` — parsed pytest failures when available,
  bounded failure windows, plus an unconditional cleaned raw tail for each job-state
  `regressed` cluster.
- `both-cluster-logs/nightly_*.log` — supplementary lossy raw nightly context for
  surfaced `regressed_tests` clusters. No baseline raw-context artifact is produced.

### Cluster-log artifact format

Every file opens with a header:

```
# cluster: <cluster key>
# job: <job name>
# url: <buildkite job url>
# state: <state> exit_status: <n>
```

**Job-state form** — `cluster-logs/<safe-cluster-name>.log` uses
`capture_mode: nightly_failure_context` and contains ranked failure windows followed by
an unconditional cleaned `## raw_tail`. When pytest parsing succeeds, a `# parsed N
failing test(s)` section lists every failure's test ID, exception class, infra tag, and
parsed exception chain before the windows. Window counts report candidates, emitted
windows, and truncation. The header also includes `job_is_infra: true|false`; when it is
true, treat the cluster as transient infrastructure rather than a torch regression.
The windows are lossy evidence, not root-cause classifications or proof that a window
belongs to a particular test.

Parsed pytest records for surfaced `regressed_tests` clusters, including complete
nightly-only and shared nightly/baseline failures, are in `report.json.regressed_tests`.

`both-cluster-logs/nightly_*.log` uses `capture_mode: both_failure_context` and is
supplementary lossy raw nightly context for the same surfaced clusters. No
`baseline_*.log` artifact is produced.

**Infra is not a torch regression.** A job artifact tagged `job_is_infra: true` or a
surfaced pytest failure tagged `test_is_infra: true` is transient infrastructure
evidence; call it out as infra. Do not let a high-scoring infra message such as a
low-GPU-memory startup failure override the explicit infra tag.

**Exception: a hang and its orphan cascade is not infra.** A `Free memory on device cuda:N
... less than desired` failure carries the infra tag from its message text alone, which
cannot see that an earlier command in the same job hung. When a `Killing process N that
didn't stop within 5 minutes` line precedes it and about 20 GiB or more is held, the earlier
hang is the head cause and the tag does not stand: attach the failure to that hang (see
"Cascade from an orphaned process is not GPU contention" below). A `timed_out` job with no
exception is likewise not infra unless an infra signature is present.

**Contested infra is not infra.** A header line `# infra_contested: /<pattern>/ matched
on N regressed clusters ...` means the triage withheld the infra tag: a CUDA-init or
startup free-memory signature hit N regressed clusters, every one of which passes on
the baseline. Transient agent trouble does not do that, so treat the signature as a
candidate torch regression; ROUTING.md has the routing.

## Step 2: NEW vs pre-existing

Classification is decided **upstream** by the torch-nightly vs same-commit-baseline
A/B. Each job is already bucketed in the report:

- `regressed` — fails on torch nightly, passes on the baseline → new, torch-attributable.
- ordinary `both` entries — fail on both and remain pre-existing; ignore them.
- `regressed_tests` — surfaced `both` clusters with a torch-nightly-only pytest
  failure; analyze them as new test-set regressions. Shared failures are context.
- `baseline_only` — fails only on the baseline → ignore.

Rate `new_failure_confidence` (high/med/low) per group from its bucket plus the infra /
agent-concentration evidence in the report. For scale definitions, see
[CONFIDENCE.md](CONFIDENCE.md).

## Step 3: Group remaining failures by root cause

Only genuinely new failures reach this step.

ONE group per root cause, not per job. From real data: 22 failing jobs
grouped into 10 root causes.

For failed clusters, use the selected windows and raw tail. Scan upward from wrappers such as
`Engine core initialization failed. See root cause above.` to find the real exception.
For surfaced `regressed_tests`, use the complete nightly-only and shared records in
`report.json` in combination with the both-cluster-logs/nightly_*.log.

Rate `shared_root_cause_confidence` (high/med/low) per member as you assign it to a group.

For grouping patterns, see [GROUPING.md](GROUPING.md). A `timed_out` cluster with no exception is
still a cause: see "A job that hangs without an exception" under the gotchas below.

## Step 4: Classify each group

Match each group's exception pattern against the routing cheat-sheet in
[ROUTING.md](ROUTING.md). Its **Routing** column is one of the three canonical values
(`pytorch/pytorch` | `vllm-project/vllm` | `infra`) — the same set the triage workflow
emits. Map routing to classification:

- `pytorch/pytorch` → `TORCH_REGRESSION`
- `vllm-project/vllm` → `VLLM_REGRESSION`
- `infra` → not a regression — call it out as infra and do not file (see Step 1)

For scale definitions, see [CONFIDENCE.md](CONFIDENCE.md).

## Gotchas the parser does NOT catch

The parser filters soft-fails, `waiting_failed`, never-ran jobs, marker/timestamp noise, and tags transient-infra signatures. The following are **not** filtered — apply them yourself when reading the `cluster-logs/*.log` files:

- **PyPI vs test channel:** `ERROR: No matching distribution found for torch==2.12.0` isn't infra — the release isn't on PyPI yet. It arrives as a non-pytest failure (treated as novel). Note it in the findings; it's not a bug to root-cause.
- **`Python-only Installation` job has multiple unrelated failure modes:** (a) torch not on PyPI — expected, skip. (b) `metadata is still not available after N attempts` / `precompiled wheel for commit X is available` — vLLM's own precompiled-wheel infra hiccup, not torch. Both arrive as non-pytest failures (treated as novel) → ignore.
- **An infra-killed baseline job is not a baseline.** The A/B buckets trust the baseline job's state. A baseline job hit by `exit 125` / `nvidia-container-cli` (or otherwise never running the tests) still lands in `BAD_STATES`, so the same job failing on torch nightly is bucketed `both` (pre-existing) — **masking a real regression** rather than surfacing it. (The failing baseline was infra, not the same test.) When the baseline build has many B200 jobs killed by infra, do NOT trust a `both` verdict on those jobs; the pair is **inconclusive** because the baseline never ran the test. Flag it as inconclusive and recommend retrying the corresponding baseline job rather than concluding anything. The inverse mistake — treating a broken baseline as if the test passed there — produced a wrongful issue (#182549, retracted 2026-05-05).
- **Compile-on vs `--enforce-eager` CI gap:** fake-kernel / Inductor stride bugs only surface when compile is on. Many gpt-oss CI lanes (`tests/evals/gpt_oss/test_gpqa_correctness.py`, `--enforce-eager` parametrizations) bypass torch.compile entirely and never trace the fake kernel. If a custom-op stride mismatch only shows up on the torch-bump test PR, the bug almost certainly exists on main too — vLLM CI is just hiding it. Call out this coverage gap in the findings.
- **`Dockerfile.cpu` seeds `requirements/test/cpu.in` from `requirements/test/cuda.in`** (literal `COPY ... cuda.in cpu.in`), so the top-line `--extra-index-url https://download.pytorch.org/whl/test/cu130` carries over to the CPU build. Combined with `uv pip compile --torch-backend cpu` (which forces stable cpu channel), torch 2.12 wheels go missing. Fix: sed-rewrite the index-url to `whl/test/cpu` AND drop `--torch-backend cpu`.
- **`uv --torch-backend <name>` overrides extra-index-url for torch.** Only stable channels (`cpu`, `cu128`, etc.) are presets — there is no `test-cpu` preset. To pin torch to the test channel, use `--extra-index-url` explicitly (or `UV_EXTRA_INDEX_URL` env) and *don't* pass `--torch-backend`.

### Use cases the first version of this skill missed

These came out of a hang that has been in the torch-nightly lane since 2026-10-08 (L4
`Distributed Models Shard 1` and H100 `Distributed Features`, filed by hand as test-infra#9212 and
#9213). The triage listed both as regressed clusters on 2026-10-13 and 2026-10-14, but no issue was filed:
most of that day's causes were skipped (several as UNDETERMINED), the hang had no exception line to key on,
an earlier CUDA-init wave (#9038) had hidden it on 10-05..10-07, and the torch-nightly image build failed on
10-16, 10-20, 10-21 and 10-23 so the jobs were `waiting_failed` and the parser dropped them.

- **A job that hangs without an exception is a finding, not "undetermined".** A `timed_out` job (`exit -1`),
  or one whose raw tail ends with `# Received cancellation signal, interrupting` /
  `The command was interrupted by a signal: signal: terminated`, usually has no traceback; the cause is
  *where it stopped*. Read the last progress lines of `## raw_tail`, ignoring the shutdown lines that follow
  the cancellation (`[shutdown] EngineCore: trigger received signal=SIGTERM` is the job being killed, not the
  cause). If the job had been making progress (tests passing) until that line, or the tail stops at the same
  line in two or more clusters, the stopping point is identified. Then:
  - write the cause with `determined: true`; `classification_confidence` is at most `medium`, and
    `new_failure_confidence` is `medium` or `high` when the baseline passes the job;
  - **do not tag it infra** unless an infra signature is present (CUDA init, `nvidia-container-cli`, exit 125,
    registry rate limit). Infra timeouts usually leave one of those lines; a hung engine leaves nothing;
  - choose `signature` from the root cause, as the workflow prompt does:
    - an exception or assert line: copy it verbatim, byte for byte;
    - a silent hang, including an earlier hang that causes an orphan-process cascade:
      `Job hung after: <message text of the last progress line>`, with the logger prefix (process name, pid,
      level, timestamp, `file.py:line`) removed. This is an exception to "copy the line verbatim": the filer's
      `normalize_signature` does not strip those fields, so a raw log line would differ on every run and file a
      duplicate each time. The message text itself stays byte for byte;
    - an orphan-process cascade: the earlier hang's signature, not the downstream free-memory exception;
    - when the last progress line is a pytest summary, remove the elapsed-time suffix (` in <duration>`) from the
      signature so reruns of the same hang give one signature, and keep the original line in the summary (for
      example `5 passed, 2 skipped in 312.45s` gives `Job hung after: 5 passed, 2 skipped`). Doing this in
      `normalize_signature` is a follow-up;
  - routing is `pytorch/pytorch` when the baseline passes and the failing lane differs by torch / triton /
    their pins; say in the summary that the owner is not confirmed without a stack dump;
  - in the summary give how long the job ran compared with the baseline (when the report has durations) and
    whether tests passed before the stop. `N passed` followed by silence is a hang in teardown, which is a
    different cause from a hang mid-test.
  Example: `(EngineCore) INFO ... [utils.py:380] Using LBNHC KV cache layout.` followed by the cancellation
  ~35 minutes later becomes `Job hung after: Using LBNHC KV cache layout.`.
- **A dominant cause hides the next one.** When many clusters share one cause (CUDA init, startup free memory),
  those jobs fail before they reach the code that would fail next, so a second cause can sit behind the first
  for days and appear only after the first is fixed. Read each cluster's own tail and do not absorb a cluster
  into the wave unless its tail contains the wave's signature. For every cause that dominates, say in
  `findings.md` which clusters never got past startup, so a reader knows later steps were not exercised.
- **Cascade from an orphaned process is not GPU contention.** `Killing process N that didn't stop within 5
  minutes` (vLLM's `data_parallel_offline.py` example kills only the parent process, so its `EngineCore`
  children keep their GPU memory) followed by a later command in the same job failing `ValueError: Free memory on device cuda:N (X/Y GiB) ...
  less than desired` means the earlier command is the head cause. Tells: the held memory is large (about
  20-26 GiB per GPU, versus ~2.9 GiB for the nccl2 footprint in #8940) and nearly constant across builds, and
  the later tests passed on the baseline. This is the exception to the infra tag described in Step 1. Group
  the later failures under the earlier hang and use the hang's `Job hung after: ...` signature, not the
  free-memory exception; do not tag them infra and do not file them as startup free-memory.
- **Same job name, different cause on different days.** Match a job to a known cause by its signature, not by
  the job name listed in an older issue: `(H100) Distributed Features` was listed under #8940 (nccl2 memory)
  and #9038 (CUDA init), and its `test_dbo` DeepEP tests were already failing differently from 2026-09-11,
  before the orphan cascade above appeared in it.
- **Job names drift between builds.** A job that exists on only one side may be renamed
  (`(H100) Distributed Features` vs `(H100) [Nightly] Distributed Features`, `(DGX) Spark` vs
  `(DGX Spark)`). Check for a rename before concluding a job was added or removed.
- **What this artifact cannot tell you: say so in `findings.md`.** It covers one nightly build, with no
  history and no package manifests. For any cause where it matters, add a line `Not determinable from this
  artifact:` plus the human follow-up:
  - *onset* (last passing build, first failing build, and whether another cause masked it);
  - *what changed*: diff the `Installed N packages` lists in the image-build logs of the last passing and first
    failing builds (torch / triton / `nvidia-*`), and `git log requirements/cuda.txt` for the window;
  - *jobs never observed*: the parser drops `waiting_failed`, so a failed image build looks like an empty
    report rather than a blind spot.
- **Rule a dependency out with a control, not by timing.** vLLM's own pins (`requirements/cuda.txt`:
  `nvidia-cutlass-dsl`, `tokenspeed-mla`, `flashinfer-python`, `transformers`) reach the stable-torch lane and
  the nightly lane alike. A package at the same version in a passing stable-lane image cannot be the whole
  explanation for a nightly-only failure; only torch, torchvision, torchaudio, triton and what they pin differ
  between the lanes. Several packages usually change in the same nightly window, so name every one rather
  than the first.

---
