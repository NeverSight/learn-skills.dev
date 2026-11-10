---
name: synthetic-data
description: "Generate structurally realistic synthetic datasets for pipeline prototyping, test coverage, or prospective power analysis. Use when code or design must be exercised before real data are available or accessible. Never substitute synthetic records for governed raw data."
allowed-tools: Bash(uv*, Rscript*, R*, mkdir*, ls*), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[--mode from-design|from-schema|calibrated]"
---

# Synthetic Data Generation

> Generate structurally realistic synthetic datasets for pilot testing, power analysis, and method development.

## Modes

| Mode | What it produces | Entry point |
|------|-----------------|-------------|
| **From design** | Synthetic data matching an existing experiment design document | "Generate test data for my experiment" |
| **From schema** | Synthetic data from a user-described structure | "Create a dataset with these variables" |
| **Calibrated** | Synthetic data calibrated to published summary statistics | "Make fake data matching these descriptives" |

Default: **From schema**. If an experiment design document exists in `docs/`, auto-select From design. If user provides published statistics, auto-select Calibrated.

## When to Use

- Testing analysis code before real data collection
- Power analysis via simulation (complements `experiment-design` Power mode)
- Method development and debugging estimation pipelines
- Generating pilot data for grant proposals or ethics applications
- Teaching demonstrations with realistic-looking data

## When NOT to Use

- Designing the experiment itself --> `experiment-design`
- Running analysis on real data --> `data-analysis`
- Auditing identification strategy --> `causal-design`

---

## Workflow

### Step 1: Detect Mode

Detect from context or ask:

| Signal | Mode |
|--------|------|
| `docs/experiment-design.md` exists | From design |
| User describes variables, types, relationships | From schema |
| User provides means, SDs, correlations from a paper | Calibrated |
| Ambiguous | Ask |

### Step 2: Interview for Data Structure

Gather the following (adapt questions to mode):

| Parameter | Question | Default |
|-----------|----------|---------|
| **Variables** | What variables do you need? | — |
| **Types** | Continuous, binary, ordinal, categorical? | Infer from name |
| **Sample size** | How many observations? | 500 |
| **Treatment** | Is there a treatment variable? How many arms? | — |
| **Effect size** | Expected treatment effect (Cohen's d, OR, etc.)? | 0.3 (small-medium) |
| **Correlations** | Which variables should be correlated? How strongly? | — |
| **Clustering** | Are observations nested (e.g., students in classrooms)? | No |
| **Panel structure** | Multiple time periods? How many? | Cross-section |
| **Missing data** | Should the data include realistic missingness? | No |
| **Language** | R or Python? | Detect from project or ask |

For **From design** mode, extract most parameters from the design document automatically and confirm with the user.

For **Calibrated** mode, require the user to provide published summary statistics. Read `references/calibration-targets.md` for the calibration procedure.

### Step 3: Generate Script

Read `references/dgp-recipes.md` for code patterns matching the requested design.

Read `shared/multi-language-conventions.md` for language-specific code style.

Generate a self-contained script that:

1. Sets a random seed (document the seed value)
2. Defines the data generating process with clear comments
3. Generates the dataset
4. Adds realistic noise and distributional features
5. Introduces missing data patterns if requested
6. Saves the dataset as CSV (and optionally `.rds`/`.parquet`)
7. Prints a summary of the generated data

### Step 4: Execute

**For large Monte Carlo sweeps** (10k+ simulations, multi-condition grids, or long-running bootstrap): run on [HPC cluster] instead of locally. Drop the generation script into `hpc/` with `submit.sbatch` (compute partition) or `sweep.sbatch` (array over seeds/conditions) — templates at Task Management `templates/slurm/`, guide at `docs/guides/hpc.md`. All SLURM templates log `git-sha.txt` to `OUT_DIR` so synthetic datasets remain traceable to the DGP code version.

Run the script and verify:

- Dataset has the expected dimensions
- Variable types are correct
- Treatment/control groups are balanced (if applicable)
- Summary statistics are plausible
- No degenerate columns (all zeros, all missing, zero variance)

### Step 5: Save Output

**Output routing:**

| File | Location |
|------|----------|
| Generated dataset | `data/synthetic/{name}.csv` |
| Generation script | `code/generate_synthetic_{name}.R` (or `.py`) |
| Data dictionary | `data/synthetic/{name}_dictionary.md` |

**NEVER write to `data/raw/`.** The `data-sensitivity` rule applies -- synthetic data is not raw data and must be clearly separated.

Create `data/synthetic/` if it does not exist.

### Step 6: Data Dictionary

Produce a markdown data dictionary alongside the dataset:

```markdown
# Data Dictionary: {name}

Generated: {date}
Script: `code/generate_synthetic_{name}.R`
Seed: {seed}
N: {sample_size}

| Variable | Type | Description | Distribution | Parameters |
|----------|------|-------------|-------------- |------------|
| id | integer | Unique identifier | Sequential | 1 to N |
| treatment | binary | Treatment assignment | Bernoulli | p = 0.5 |
| outcome | continuous | Primary outcome | Normal | mu = 0, sigma = 1 (control) |
| ... | ... | ... | ... | ... |

## Treatment Effects
- True ATE: {value}
- True CATE by subgroup: {if applicable}

## Missing Data
- Mechanism: {MCAR/MAR/MNAR}
- Rate: {percentage} of {variable}
```

---

## Key Principles

### Reproducibility
- **Always set random seeds.** Document the seed in the script header and the data dictionary.
- Script must be fully self-contained -- running it again with the same seed produces identical output.

### Realism
- **Match variable types to realistic distributions.** Not everything is normal:
  - Income, reaction times --> log-normal or gamma
  - Likert scales --> ordinal with floor/ceiling effects
  - Count data --> Poisson or negative binomial
  - Proportions --> beta
  - Binary outcomes --> Bernoulli with realistic base rates
- **Include realistic noise.** Treatment effects should be embedded in noisy data, not clean signal.
- **Add heterogeneity.** Real data has heterogeneous treatment effects -- consider adding subgroup variation.

### Missing Data
- If the real data will have missingness, simulate it:
  - **MCAR:** Random deletion at a fixed rate
  - **MAR:** Missingness depends on observed variables (e.g., higher income --> less missing)
  - **MNAR:** Missingness depends on the missing value itself (e.g., depressed people less likely to respond)
- Document the missingness mechanism in the data dictionary.

### Calibration (Calibrated Mode)
- Read `references/calibration-targets.md` for the full procedure.
- Require published summary statistics as input (means, SDs, correlations, effect sizes).
- Validate that the synthetic data matches the targets within tolerance.
- Report discrepancies between target and achieved statistics.

---

## Mode: From Design

### Workflow

1. **Locate design document** -- check `docs/experiment-design.md`, `docs/pre-analysis-plan.md`, `log/plans/`
2. **Extract parameters:**
   - Treatment arms and assignment mechanism
   - Primary and secondary outcomes (types, expected distributions)
   - Covariates and their roles
   - Sample size and any clustering/stratification
   - Expected effect sizes from the power analysis
3. **Confirm with user** -- present extracted parameters and ask for adjustments
4. **Generate** -- follow Steps 3-6 above

### Integration with `experiment-design`

The design document produced by `experiment-design` Design mode contains everything needed:
- Hypotheses with expected signs --> treatment effect directions
- Conditions and randomization --> treatment assignment DGP
- Outcome measures and scales --> variable types and distributions
- Power analysis results --> sample size and effect size

---

## Mode: From Schema

### Workflow

1. **Interview** -- ask user to describe each variable (or provide a sketch)
2. **Infer structure** -- detect relationships from the description:
   - "X causes Y" --> include causal pathway
   - "A and B are correlated" --> induce correlation via shared latent factor
   - "C moderates the effect" --> include interaction term
3. **Generate** -- follow Steps 3-6 above

### Common Requests

| User says | Interpret as |
|-----------|-------------|
| "A standard survey dataset" | Demographics + Likert DVs + treatment + attention checks |
| "Panel data" | Units x time with unit and time fixed effects |
| "Something like [paper name]" | Switch to Calibrated mode, use paper's descriptives |

---

## Mode: Calibrated

### Workflow

1. **Collect targets** -- user provides published summary statistics:
   - Means and standard deviations
   - Correlation matrix (or key correlations)
   - Effect sizes from regression tables
   - Sample size
   - Distribution shapes (skew, kurtosis) if reported
2. **Read `references/calibration-targets.md`** for the calibration procedure
3. **Generate with matching** -- use the Cholesky decomposition or copula method to match the target correlation structure
4. **Validate** -- compare synthetic descriptives to targets, report match quality
5. **Save** -- follow Steps 5-6 above, include calibration targets in the data dictionary

---

## Cross-References

| Resource | When read |
|----------|-----------|
| `references/dgp-recipes.md` | All modes (code patterns for each design type) |
| `references/calibration-targets.md` | Calibrated mode (matching procedure) |
| `shared/multi-language-conventions.md` | All modes (code style) |
| `experiment-design` skill | From design mode (reads its design documents) |
| `data-analysis` skill | Consumes synthetic data for pipeline testing |
| `data-sensitivity` rule | Never write to `data/raw/` |
| `design-before-results` rule | Synthetic data supports locking the design before real data |
