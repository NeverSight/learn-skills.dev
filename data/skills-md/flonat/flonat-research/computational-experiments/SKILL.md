---
name: computational-experiments
description: "Scaffold, execute, analyse, and publish computational research experiments through a reproducible staged workflow. Use when a research question requires simulations or computational sweeps rather than a one-off script."
allowed-tools: Bash(uv*, pytest*, mkdir*, ls*, cp*), Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
argument-hint: "[project-path] [--mode scaffold|experiment|figures|full] [--budget <minutes>] [--scaffold standard|robustness|replication]"
agent-dependencies: [code-review]
skill-dependencies: [multi-perspective]
---

# Computational Experiments

> Lifecycle skill for algorithmic research projects where the code IS the scientific contribution.

## Modes

| Mode | What it does | Phases |
|------|-------------|--------|
| **Scaffold** | Create/audit package structure + algorithm skeleton | 1–2 |
| **Experiment** | Design and run pre-specified sweep campaigns | 1, 3–4 |
| **Explore** | Adaptive experiment loop: modify → run → evaluate → keep/discard | 1, 3E–4 |
| **Autonomous** | Parallel self-correcting sweep with sub-agents | 1, 3A–4 |
| **Figures** | Generate publication output from results | 1, 4 |
| **Full** | Complete pipeline | 1–5 |

Default: **Full**. Detect mode from user request or ask if ambiguous.

### `--scaffold` Flag

Sets a **stage progression template** for the experiment campaign. Templates provide structured checklists and exit criteria for each stage.

| Scaffold | Stages | Best for |
|----------|--------|----------|
| `standard` | Init → Tune → Creative → Ablate | Algorithm development, ML, simulation |
| `robustness` | Main spec → Alternatives → Placebo → Sensitivity | Causal inference, econometrics |
| `replication` | Exact → Our data → Extensions → Robustness | Replicate-and-extend papers |

Templates live in `templates/experiments/`. When a scaffold is active:
1. Present the current stage's checklist before starting work
2. Gate progression: don't move to the next stage until exit criteria are met
3. Log stage transitions in the experiment breadcrumb

Default (no flag): user-defined stages (current behavior). Scaffold is a guide, not a cage — users can skip stages or reorder with explicit acknowledgment.

### `--budget` Flag

Sets a **campaign-level time budget** in minutes for the entire experiment run. When set:

1. **Record start time** at the beginning of Phase 3 (any variant)
2. **Check remaining budget** before launching each new config, sweep batch, or explore iteration
3. **Soft stop** when budget is exhausted: finish the current run, save all results collected so far, skip remaining configs
4. **Never hard-kill** a running experiment mid-execution — always let the current run complete

| Mode | How budget applies |
|------|-------------------|
| **Experiment** | Skip remaining sweep configs when time is up |
| **Explore** | Exit the explore loop at the next iteration boundary |
| **Autonomous** | Do not spawn new agent batches; let running batches finish |
| **Figures** | Budget does not apply (figure generation is fast) |

**Reporting:** When a budget triggers early stop, append to the breadcrumb:
```
- **Budget:** Stopped after <N>/<M> configs (budget: <X> min, elapsed: <Y> min)
```

**Default:** No budget (run all configs to completion). Typical values: `--budget 30` for quick exploration, `--budget 120` for overnight sweeps.

Use **Experiment** when the design space is known upfront (grid/random sweep). Use **Explore** when the design space is unknown and the agent should adaptively search (inspired by Karpathy's [autoresearch](https://github.com/karpathy/autoresearch)).

## When to Use

- "Set up experiments for my algorithm" / "Scaffold the project"
- "Run the benchmark" / "Design the sweep"
- "Explore what auction parameters reduce collusion" / "Try different architectures"
- "Generate convergence plots" / "Make publication figures from results"
- Any project where algorithms, simulations, or optimisation loops are the contribution

## When NOT to Use

- Empirical data analysis (observational/survey data) → `data-analysis`
- Experimental design for human subjects → `experiment-design`
- Causal inference strategy → `causal-design`
- LaTeX compilation → `latex`

## Workflow

### Phase 1: Detect & Configure

1. **Read project context:** `CLAUDE.md`, `MEMORY.md`, `.context/project-recap.md` if they exist
2. **Detect structure:** Scan for `src/`, `experiments/`, `tests/`, `pyproject.toml`, `setup.py`
3. **Detect language:** Check existing files. Default: Python with uv. Ask if ambiguous.
4. **Read MEMORY.md:** Look for `[LEARN:code]` tags, notation registry, key decisions — apply established conventions
5. **Determine mode:** From user request or ask. If existing package exists, skip scaffold.
6. **Inventory existing code:** Map modules, entry points, config objects, result files

Read `references/package-scaffold.md` if scaffold mode is active.

### Phase 2: Scaffold

**Skip if:** Package structure already exists and user requested experiment/figures mode.

1. **Package structure:** Create `src/<pkg>/`, `tests/`, `experiments/configs/`, `scripts/`
2. **Build config:** `pyproject.toml` with hatchling, dev dependencies (pytest, matplotlib, numpy)
3. **Algorithm skeleton:** Base classes (`Algorithm`, `Experiment`, `Metric`) with `# TODO:` markers. For multi-agent projects, use `BaseAgent`, `Environment`, `MultiAgentSimulation` instead — see `references/multi-agent-patterns.md`
4. **Test skeleton:** Unit test stubs, convergence test template, smoke test
5. **Experiment infrastructure:** Config dataclass template, runner script template
6. **Gitignore:** Add `results/`, `*.pkl`, `wandb/`, `__pycache__/`

Read `references/algorithm-templates.md` for skeleton code. Read `references/package-scaffold.md` for directory layout.

**Gate:** Verify package installs with `uv pip install -e ".[dev]"` before proceeding.

### Phase 3: Experiment Design

**Prerequisite:** Working package (Phase 2 or pre-existing).

1. **Config schema:** Python dataclass with validation, defaults, serialization to/from YAML
2. **Config hashing:** SHA-256 fingerprint for reproducibility tracking (see `references/experiment-patterns.md`)
3. **Sweep definitions:** Grid sweep (all combinations), random sweep (budget-limited), manual configs
4. **Seed management:** `np.random.default_rng(seed)` everywhere. Seeds passed through config, never global state.
5. **Runner script:** Config → initialize → loop → collect → save. Reads config, runs `n_seeds` repetitions, saves per-seed results.
6. **Baseline implementations:** Same interface as main algorithm, registered in config
7. **Result aggregation:** Per-seed CSV → aggregated stats (mean ± std). Canonical column naming.
8. **Parallelization:** `concurrent.futures.ProcessPoolExecutor` for independent seeds/configs. **For large sweeps (10+ configs × 10+ seeds, GPU-bound, or >30-min runs):** move to [HPC cluster] HPC — see `docs/guides/hpc.md` in Task Management and copy `templates/slurm/{array,gpu}.sbatch` into `hpc/` with `sync-up.sh` / `sync-down.sh`. Recent reference implementations: `Projects/NLP/{example-project-a,example-project-b}/hpc/`.
9. **Checkpointing:** Save intermediate results to allow resume on crash
10. **Dual output:** Dated archive + "latest" symlink for quick access (see `references/experiment-patterns.md`)

**For multi-agent simulations, also include:**

11. **Agent composition:** Heterogeneous population specs with distribution presets (uniform, weighted, custom)
12. **Feature toggles:** Opt-in capabilities per agent type (memory, messaging) — enables ablation studies
13. **Messaging service:** Round-based broadcast channel for inter-agent communication
14. **Multi-level metrics:** Agent-level (individual performance) + system-level (aggregate outcomes) + emergent-level (herding, convergence)

See `references/multi-agent-patterns.md` for all multi-agent patterns.

Read `references/experiment-patterns.md` for config, sweep, and runner patterns.

**Gate:** Run a smoke test — single config, single seed, verify output files are created.

### Phase 3E: Explore Loop (Adaptive Experiments)

**Use instead of Phase 3 when:** The design space is unknown, the user wants to adaptively search rather than run a pre-specified sweep, or the user says "explore", "try things", "see what works".

Read `references/explore-loop.md` for the full protocol. Summary:

1. **Branch:** Create `experiments/<tag>` branch (e.g. `experiments/mar14-collusion-params`)
2. **Baseline:** Run the code as-is, record baseline metric in `results.tsv`
3. **Loop** (autonomous until interrupted or budget exhausted):
   - Propose a modification based on results so far (informed by prior keep/discard outcomes)
   - Apply the change to the target file(s)
   - `git commit` the change
   - Run with time budget: `timeout <budget>s uv run python <script> > run.log 2>&1`
   - Extract metric from output
   - Log to `results.tsv`: commit hash, metric, status (keep/discard/crash), description
   - If improved → **keep** (advance branch)
   - If not improved → **discard** (`git reset --hard HEAD~1`)
   - If crashed → attempt fix once, else discard and move on
4. **Stop when:** user interrupts, `--budget` time exhausted (campaign-level), per-run timeout exceeded, or N consecutive discards with no progress

**Key principles:**
- One change per iteration — never stack multiple untested changes
- Log every attempt, including discards and crashes
- The TSV is the ground truth — it captures the full exploration history
- Simplicity criterion: prefer changes that simplify the code for equal or better metrics

**Gate:** `results.tsv` exists with at least a baseline entry before entering the loop.

### Phase 3A: Autonomous Sweep (Parallel Self-Correcting)

**Use instead of Phase 3 when:** 10+ configs, known failure-prone experiments, or user says "autonomous", "hands-off", "self-correcting sweep".

Read `references/autonomous-sweep.md` for the full protocol. Summary:

1. **Batch configs** into groups of max 4 parallel agents
2. **Spawn sub-agents** — each runs its batch, detects failures by signature (shape mismatch, NaN, empty array, timeout), diagnoses, fixes, retries (max 3 cycles)
3. **Aggregate results** — coordinator collects batch results, reports success/fixed/unresolved counts
4. **Generate figures** for all successful configs

**Key constraints:**
- Max 4 parallel agents
- Max 3 retry cycles per config
- Agents must not modify shared code simultaneously
- Each fix is committed for traceability

**Graceful degradation:** If some batches fail while others succeed, collect all successful results and report failures. Only stop entirely if ALL batches fail. See `shared/skill-design-patterns.md` (Graceful Degradation section).

**Gate:** At least one config must succeed. If all fail, report the unresolved errors and stop.

**Breadcrumb:** After any Phase 3 variant completes, append to `.planning/state.md` (if exists) or `.context/current-focus.md`:
```
### [computational-experiments] Experiments complete [YYYY-MM-DD HH:MM]
- **Done:** [N configs run, N seeds, mode: experiment/explore/autonomous]
- **Outputs:** [result files at <path>, N successful / N total]
- **Next:** Publication output (figures/tables)
```

### Phase 4: Publication Output

**Prerequisite:** Result files exist in `results/` or `experiments/results/`.

1. **Convergence plots:** Metric vs iteration/budget (mean ± std across seeds, multiple methods)
2. **Comparison charts:** Bar chart or table comparing methods across problems
3. **Ablation plots:** Performance with/without each component (for multi-agent: use feature toggle ablation configs)
4. **Sensitivity analysis:** Metric vs parameter (line plot with shaded confidence band)
5. **Tables:** Performance tables exported as `.tex` via `\input{}` — **never hard-code results**
6. **Figure script:** `scripts/make_all_figures.py` that regenerates all figures from saved results

Read `references/figure-recipes.md` for matplotlib recipes.

**Output routing:**
- Figures → `paper/figures/` as PDF (per `overleaf-separation` rule)
- Tables → `paper/tables/` as `.tex` (per `no-hardcoded-results` rule)
- Figure scripts → `scripts/` (never inside `paper/`)

### Phase 5: Audit & Save

1. **Reproducibility check:**
   - Seed determinism: same config + seed → same output?
   - Config completeness: can results be regenerated from saved configs?
   - Output freshness: are figures newer than their source data?
   - Dependency pinning: are versions locked in `pyproject.toml` or `uv.lock`?
2. **Code review:** Invoke the `code-review` agent on all generated scripts (via skill-routing mechanism)
3. **Record learnings:** Write `[LEARN:code]` tags for project-specific conventions discovered
4. **Suggest next steps:** compilation with `latex`, additional experiments, `replication-package`

**Breadcrumb:** After Phase 5 completes, append to `.planning/state.md` (if exists) or `.context/current-focus.md`:
```
### [computational-experiments] Phase 5 complete [YYYY-MM-DD HH:MM]
- **Done:** [reproducibility check, code review score, N learn tags recorded]
- **Outputs:** [figures at <path>, tables at <path>]
- **Next:** [suggested next steps]
```

## Evolution Protocol

This skill improves with each invocation on a project:

1. **Before work:** Read `MEMORY.md` for existing `[LEARN:code]` entries and Key Decisions
2. **During work:** Note any convention, naming pattern, or structural choice that should persist
3. **After work:** Record `[LEARN:code]` tags and update Key Decisions table

Examples of learnings to capture:
- `[LEARN:code] This project uses ElicitationConfig dataclass, not YAML files`
- `[LEARN:code] Metrics are in src/utils/metrics.py, not a separate package`
- `[LEARN:code] Seeds are managed via utils/seeds.py with MASTER_SEED + offset`

## Cross-References

| Resource | When read |
|----------|-----------|
| `references/package-scaffold.md` | Phase 2 (project structure) |
| `references/algorithm-templates.md` | Phase 2 (skeleton code) |
| `references/experiment-patterns.md` | Phase 3 (configs, sweeps, runners, config hashing, dual output) |
| `references/multi-agent-patterns.md` | Phase 2–3 (agent composition, messaging, multi-level metrics) |
| `references/multi-agent-infrastructure.md` | Phase 2–3 (feature toggles, config hashing, simulation runner, visualization) |
| `references/explore-loop.md` | Phase 3E (adaptive explore loop) |
| `references/autonomous-sweep.md` | Phase 3A (parallel self-correcting sweep) |
| `references/figure-recipes.md` | Phase 4 (matplotlib recipes) |
| `shared/publication-output.md` | Phase 4 (table/figure format standards) |
| `shared/multi-language-conventions.md` | Phase 1 (if non-Python) |
| `docs/guides/hpc.md` (Task Management) | Phase 3 (move to [HPC cluster] for large/GPU/long sweeps) |
| `templates/slurm/*.sbatch` (Task Management) | Phase 3 (drop-in SLURM templates; all log git-SHA to OUT_DIR) |
| `no-hardcoded-results` rule | Phase 4 (output routing) |
| `overleaf-separation` rule | Phase 4 (file placement) |
| the `code-review` agent | Phase 5 (auto-invoked) |
| `data-analysis` skill | Redirect if task is empirical, not computational |
| `replication-package` skill | Phase 5 (suggested next step) |
| `cross-language-check` skill | Phase 5 (suggested next step for verification) |
| `references/multi-analyst-design.md` | Phase 3–5 (many-analysts robustness diagnostic) |
| `shared/worker-critic-protocol.md` | Phase 3–4 (inline review of generated code/results) |
| `shared/checkpoint-resumability.md` | All phases (save/resume on crash) |
| `templates/experiments/standard.md` | `--scaffold standard` (init/tune/creative/ablate) |
| `templates/experiments/robustness.md` | `--scaffold robustness` (econometrics robustness) |
| `templates/experiments/replication.md` | `--scaffold replication` (replicate-and-extend) |
| `figure-feedback` skill | Phase 4 (VLM analysis of generated plots) |
