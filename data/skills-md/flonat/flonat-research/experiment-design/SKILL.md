---
name: experiment-design
description: "Design empirical studies through power analysis, pre-analysis planning, QSF parsing, and survey architecture. Use when specifying sampling, measurement, treatment, or analysis before data collection. Not for causal identification alone; use $causal-design."
allowed-tools: Bash(uv*, Rscript*, R*, mkdir*, ls*), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[--mode power|design|pap|survey] [qsf-file or project-path]"
---

# Experiment Design

> Interview-driven design workflow producing design documents, power analysis scripts, and pre-analysis plans.

## Modes

| Mode | What it produces | Entry point |
|------|-----------------|-------------|
| **Power** | Power analysis script + sample size table | "How many participants do I need?" |
| **Design** | Full design document (hypotheses, conditions, measures, randomization) | "Design my experiment" |
| **PAP** | Pre-analysis plan (AEA/OSF/EGAP format) | "Write a PAP" |
| **Survey** | Structured survey specification from natural language or QSF | "Build a survey" / "Parse my Qualtrics" |

Default: **Design**. If user provides a `.qsf` file, auto-select Survey mode.

## When to Use

- Designing a new experiment or survey
- Calculating required sample sizes
- Writing or auditing a pre-analysis plan
- Parsing a Qualtrics `.qsf` file to understand its structure
- Building a survey specification from a natural language description

## When NOT to Use

- Running the analysis → `data-analysis`
- Auditing identification strategy for observational studies → `causal-design`
- Generating synthetic test data → `synthetic-data`

## Shared References

- Method probing questions: `shared/method-probing-questions.md` — ask before designing (Experiments/RCTs, Survey sections)
- Validation tiers: `shared/validation-tiers.md` — tier determines required power and pre-registration
- Escalation protocol: `shared/escalation-protocol.md` — escalate when design has validity threats
- Engagement-stratified sampling: `shared/engagement-stratified-sampling.md` — stratify social media samples by engagement
- Inter-coder reliability: `shared/intercoder-reliability.md` — reliability planning for content analysis designs

---

## Mode: Power

Read `references/power-analysis-recipes.md` for language-specific code patterns.

### Workflow

1. **Interview** — ask for:
   - Primary outcome variable and expected effect size (or domain norms)
   - Design type (between-subjects, within-subjects, factorial, cluster-randomized)
   - Number of conditions/groups
   - Significance level (default: 0.05) and desired power (default: 0.80)
   - Any clustering or stratification
2. **Generate script** — R (`DeclareDesign`/`pwr`) or Python (`statsmodels.stats.power`)
3. **Execute and report** — produce a sample size table showing N for power = {0.80, 0.90, 0.95}
4. **Write to project** — save script to `code/power_analysis.R` (or `.py`), results to `output/power_analysis_results.md`

**HPC escalation:** If the power analysis uses Monte Carlo simulation (e.g., `DeclareDesign` with >10k replications, or a multi-design sweep), move execution to [HPC cluster] — drop the simulation script into `hpc/` with `templates/slurm/array.sbatch` (array over seeds/designs). The SHA-logging snippet in the template pins results to the DGP version. See `docs/guides/hpc.md`.

### Effect Size Guidance

If the user doesn't know the expected effect size, guide them:

| Source | How to use |
|--------|-----------|
| Prior literature | "What did similar studies find?" |
| Pilot data | Calculate from pilot descriptives |
| SESOI | "What's the smallest effect worth detecting?" |
| Domain norms | Cohen's benchmarks as absolute last resort (small=0.2, medium=0.5, large=0.8 for d) |

**Never default to Cohen's benchmarks without acknowledging they are arbitrary.**

---

## Mode: Design

### Workflow

1. **Research question interview** — structured questions:
   - What is the causal question?
   - What is the treatment / intervention?
   - What is the primary outcome? Secondary outcomes?
   - What is the target population?
   - What is the assignment mechanism? (random, stratified, clustered, matched)
2. **Design specification** — produce a structured document covering:
   - Hypotheses (directional, with expected signs)
   - Conditions (treatment arms, control)
   - Randomization procedure
   - Outcome measures and scales
   - Sample and recruitment strategy
   - Timeline
3. **Identification check** — state the estimand, identifying assumptions, and potential threats
4. **Write design document** — save to `docs/experiment-design.md` or project-appropriate location
5. **Lock the design** — record in `MEMORY.md` Estimand Registry (if project has one) or flag for the user to lock before analysis

This design document is what `data-analysis` Phase 3 checks for before allowing estimation.

---

## Mode: PAP

Read `references/pap-template.md` for the full template structure.

### Workflow

1. **Check for existing design** — look for design document in `docs/`, `log/plans/`, or `.context/`
2. **If no design exists** — run Design mode first, then continue
3. **Generate PAP** — structured pre-analysis plan following AEA/OSF/EGAP conventions:
   - Study information (title, authors, IRB, registration)
   - Design overview (hypotheses, conditions, randomization, sample)
   - Data collection (instruments, timing, blinding)
   - Analysis plan (main specification, inference, multiple testing corrections)
   - Robustness and sensitivity analyses
   - Power analysis (reference or embed results from Power mode)
4. **Output** — save to `docs/pre-analysis-plan.md` (or `.tex` if user prefers LaTeX)
5. **Registration prompt** — remind user to register at AEA RCT Registry, OSF, or EGAP

---

## Mode: Survey

Survey mode is a first-class capability with two entry points: QSF parsing and natural language construction.

### Entry Point A: QSF Parsing

When user provides a Qualtrics `.qsf` file:

1. **Parse the JSON** — extract survey flow, blocks, questions, embedded data, skip logic
2. **Map question types** — read `references/qsf-parsing-guide.md` for type mapping:
   - Matrix, Likert, slider, numeric, constant sum, rank order, best-worst scaling
   - Text entry (single-line, multi-line, essay)
   - Multiple choice (single answer, multiple answer)
3. **Detect design elements:**
   - Factorial conditions from randomizer blocks and embedded data
   - Attention checks and comprehension checks
   - Known validated scales (read `references/known-scales-registry.md`)
   - Skip/display logic and branching
4. **Produce structured summary** — questions, conditions, scales, logic flow, warnings
5. **Flag issues** — missing attention checks, unbalanced conditions, potential order effects

### Entry Point B: Natural Language Construction

When user describes an experiment in natural language:

1. **Parse the design** — extract factorial structure from text
   - Example: "3 (Source: AI vs Human vs None) x 2 (Product: Hedonic vs Utilitarian)" → 3x2 between-subjects
2. **Interview for details:**
   - What DVs to measure? (recommend appropriate scale types)
   - What manipulation checks?
   - What attention/comprehension checks?
   - Demographics and control variables?
3. **Generate survey specification** — structured document with:
   - Survey flow (consent → demographics → manipulation → DVs → manipulation check → debrief)
   - Question text and response options for each item
   - Condition assignments and randomization logic
   - Attention check placement (read `references/survey-design-checklist.md`)
4. **Scale recommendations** — read `references/known-scales-registry.md` for validated scales matching the constructs

### Survey Quality Checks

Read `references/survey-design-checklist.md` for the full checklist. Key checks:

- **Attention checks:** At least 1 per 5 minutes of survey length. Calibrated pass rates (85-95%). See Krosnick (1991), Meade & Craig (2012).
- **Response style mitigation:** Flag scales vulnerable to acquiescence bias. Recommend reverse-coding for scales with 4+ items in the same direction.
- **Scale quality:** Semantic type detection (satisfaction, trust, intention, risk). Reverse-coded item flagging. Well-known scale recognition.
- **Order effects:** Randomize question order within blocks where appropriate. Flag potential priming from early questions.

---

## Cross-References

| Resource | When read |
|----------|-----------|
| `references/power-analysis-recipes.md` | Power mode |
| `references/pap-template.md` | PAP mode |
| `references/survey-design-checklist.md` | Survey mode (quality checks) |
| `references/identification-strategies.md` | Design mode (identification check) |
| `references/qsf-parsing-guide.md` | Survey mode (QSF parsing) |
| `references/known-scales-registry.md` | Survey mode (scale recognition) |
| `design-before-results` rule | Design + PAP modes produce the locked design |
| `data-analysis` skill | Consumes the design document |
| `causal-design` skill | For observational identification (not experiments) |
| `synthetic-data` skill | For generating pilot data |
