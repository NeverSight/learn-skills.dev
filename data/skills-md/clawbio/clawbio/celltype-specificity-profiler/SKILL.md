---
name: celltype-specificity-profiler
description: Given a gene and a single-cell atlas, compute how cell-type-specific its expression is — the tau specificity index, Sarle's expression bimodality coefficient, and the cell types that drive the signal; a pure analytic transform that chains downstream of scrna-embedding.
license: MIT
metadata:
  version: "0.1.0"
  author: Jacky Siu
  domain: single-cell
  tags:
    - scrna
    - single-cell
    - specificity
    - tau
    - bimodality
    - target-prioritization
    - marker-gene
    - h5ad
  inputs:
    - name: atlas
      type: file
      format:
        - h5ad
      description: Annotated single-cell expression matrix (log-normalized X; cell-type labels in an obs column). In the chain, this is the output of upstream scrna-embedding.
      required: false
    - name: gene
      type: string
      format:
        - txt
      description: HGNC gene symbol to profile (e.g. CD276). Required unless --demo.
      required: false
  outputs:
    - name: profile
      type: file
      format:
        - json
      description: Specificity profile — tau, bimodality coefficient, ranked cell types, per-cell-type stats, optional trial prior.
    - name: per_celltype
      type: file
      format:
        - csv
      description: Tidy per-cell-type expression table for plotting.
  dependencies:
    python: ">=3.10"
    packages:
      - scanpy
      - anndata
      - numpy>=1.23
      - scipy>=1.9
      - pandas>=2.0
  demo_data:
    - path: examples/expected_demo_profile.json
      description: Reference output of `--demo` on scanpy's bundled real pbmc3k dataset (gene MS4A1).
  endpoints:
    cli: python skills/celltype-specificity-profiler/profiler.py --gene {gene} --atlas {atlas} --output {output_dir}
  openclaw:
    requires:
      bins:
        - python3
    always: false
    emoji: "🎯"
    homepage: https://github.com/ClawBio/ClawBio
    os:
      - darwin
      - linux
    install:
      - kind: uv
        package: scanpy
      - kind: uv
        package: anndata
      - kind: uv
        package: numpy
      - kind: uv
        package: scipy
      - kind: uv
        package: pandas
    trigger_keywords:
      - cell-type specificity
      - cell type specificity
      - specificity index
      - tau index
      - tau specificity
      - bimodality
      - bimodality coefficient
      - cell-type-specific expression
      - expression specificity
      - marker gene specificity
---

# 🎯 Cell-Type Specificity Profiler

You are **Cell-Type Specificity Profiler**, a specialised ClawBio agent for single-cell analysis. Your role is to quantify, for a single gene, how cell-type-specific its expression is across an annotated atlas.

## Trigger

**Fire this skill when the user says any of:**
- "how cell-type-specific is <gene>?"
- "compute the tau specificity index for <gene>"
- "is <gene> a broad or restricted marker?"
- "which cell types express <gene>, and is its expression bimodal?"
- "expression specificity / bimodality coefficient for my target"
- "profile target specificity (optionally with the trial-success prior)"

**Do NOT fire when:**
- The user wants to *build* the embedding / integrate batches / cluster cells → that is `scrna-embedding` or `scrna-orchestrator`.
- The user wants differential expression between conditions → that is `rnaseq-de` / `proteomics-de`.
- The user wants generic target evidence (GWAS, tractability, known drugs) rather than a single-cell specificity metric → that is `omics-target-evidence-mapper` / `target-validation-scorer`.

**Design note:** This skill consumes an already-annotated matrix and returns one focused metric set. It does not fetch, embed, or cluster.

## Why This Exists

Target prioritization, off-target safety triage, and marker-gene discovery all hinge on cell-type specificity. ClawBio's existing single-cell skills (`scrna-embedding`, `omics-target-evidence-mapper`) embed and annotate cells, but **none return a per-gene specificity metric**.

- **Without it**: Users hand-roll pseudobulk aggregation and ad-hoc specificity scores, with no standard tau / bimodality contract for downstream skills.
- **With it**: One command returns a clean specificity profile (`tau`, `bimodality_coefficient`, ranked cell types) plus a tidy table, ready for `target-validation-scorer` and `clinical-trial-finder`.
- **Why ClawBio**: It is a **pure analytic transform — it does not fetch data**. Data access stays upstream (`scrna-embedding` pulls real atlases from CELLxGENE Census); this skill computes metrics on the matrix it is handed, keeping it a clean, chainable citizen rather than a competing data connector, and preserves the reproducibility-bundle contract.

It implements the two complementary single-cell features from *The Virtual Biotech* (Zhang et al., 2026): cell-type-specific targets progress further in clinical trials with fewer adverse events. The bimodality coefficient is a cross-domain transfer from psychometrics, only moderately correlated with tau (ρ≈0.54), so the two carry complementary signal. The paper's trial-success scoring is an *optional* layer (`--trial-prior`), so the core capability is not locked to one preprint's coefficients.

## Core Capabilities

1. **Tau Specificity Index**: Yanai et al. 2005 index over pseudobulk per-cell-type means, in [0, 1] (0 = ubiquitous → 1 = single-cell-type restricted).
2. **Bimodality Coefficient**: Sarle's BC (bias-corrected skewness/kurtosis) over expressing cells — an "on/off" expression signal.
3. **Cell-Type Ranking**: Top expressing cell types with mean expression and fraction expressing, plus full per-cell-type stats.
4. **Optional Trial Prior**: With `--trial-prior`, attach the published Zhang et al. 2026 odds ratios (labelled, correlational).
5. **Reproducibility Bundle**: Emit `commands.sh`, `environment.yml`, and SHA-256 checksums.

## Scope

**One skill, one task.** This skill computes per-gene cell-type specificity metrics from an annotated matrix and nothing else. It does not fetch data, embed, cluster, annotate, or run differential expression — those belong to other skills.

## Input Formats

| Format | Extension | Required Fields | Example |
|--------|-----------|-----------------|---------|
| AnnData annotated matrix | `.h5ad` | Log-normalized (non-negative) expression in `X`; cell-type labels in an `obs` column; gene in `var` index | `lung_atlas.h5ad` |
| Demo mode | n/a | none — uses scanpy's bundled, real `pbmc3k` dataset | `--demo` |

In the chain, the `.h5ad` is the **output of upstream `scrna-embedding`**, not fetched here.

## Workflow

1. **Load**: Read the `.h5ad` (or `--demo`); resolve the cell-type `obs` column (`--cell-type-key`, auto-detected from common names).
2. **Resolve gene**: Map the symbol against the atlas `var` index (small alias map, e.g. CD276 ↔ B7-H3); fail loudly on a genuinely missing symbol rather than returning zeros. *(Prescriptive.)*
3. **Subset**: If `--tissue` is given, restrict to that label; error if absent. *(Prescriptive.)*
4. **Aggregate & score**: Pseudobulk mean expression per cell type → `tau`; bimodality coefficient over expressing cells; set `low_expression` when the gene is expressed in <1% of cells. *(Prescriptive.)*
5. **Generate**: Write `profile.json`, `per_celltype.csv`, and the reproducibility bundle; if `--trial-prior`, attach the labelled odds ratios. *(Prescriptive.)*

## CLI Reference

```bash
# Standard usage — profile a gene against your own atlas
python skills/celltype-specificity-profiler/profiler.py \
  --gene CD276 --atlas lung_atlas.h5ad --output <report_dir>

# Restrict to a tissue and attach the paper's trial-success prior
python skills/celltype-specificity-profiler/profiler.py \
  --gene CD276 --atlas lung_atlas.h5ad --tissue lung --trial-prior --output <report_dir>

# Demo mode (real scanpy-bundled pbmc3k; default gene MS4A1)
python skills/celltype-specificity-profiler/profiler.py --demo --output <report_dir>

# Via ClawBio runner
python clawbio.py run celltype-specificity-profiler --demo
```

## Demo

```bash
python clawbio.py run celltype-specificity-profiler --demo
```

The demo runs on scanpy's bundled, **real** `pbmc3k` 10x dataset (2,638 cells, annotated cell types) — no synthetic data. The default gene `MS4A1` is a canonical B-cell marker, so it scores as highly cell-type-specific. A reference of this output ships at `examples/expected_demo_profile.json`.

## Algorithm / Methodology

1. Load atlas; resolve gene against `var` (with alias map) and subset (and `--tissue` if given).
2. Aggregate to **pseudobulk mean expression per cell type** (expects log-normalized, non-negative input).
3. **tau** = Σᵢ(1 − xᵢ/x_max) / (n − 1) over n cell types; xᵢ = mean expression in cell type i. NaN for n < 2. Following Zhang et al. 2026, cell types with **fewer than 20 cells are excluded** from the tau computation (their pseudobulk means are unreliable and, via the max-normalization, can distort tau); they remain in `per_celltype_stats`, and the profile records `n_cell_types_used_for_tau` / `n_cell_types_excluded_small`.
4. **Bimodality coefficient** = (g1² + 1) / (g2 + 3·(n−1)²/((n−2)(n−3))), g1/g2 = bias-corrected sample skewness/excess kurtosis over expressing cells. NaN for n < 4 or zero variance.
5. Rank cell types by mean expression; if `--trial-prior`, label tau against `tau_threshold` and attach the published ORs.

**Key thresholds / parameters**:
- `TAU_THRESHOLD = 0.69` — tau > 0.69 → "cell-type-specific". This is **not** a universal constant: Zhang et al. 2026 (Extended Methods) derived it as the midpoint of a K-means (k=2) split of *their trial-level* tau distribution, so it is cohort-specific. Treat continuous `tau` as the real output and recalibrate the cut on your own distribution if you binarize.
- `MIN_CELLS_FOR_TAU = 20` — cell types with <20 cells are dropped from the tau computation (source: Zhang et al. 2026).
- `LOW_EXPRESSION_FRACTION = 0.01` — gene expressed in <1% of cells flags an unreliable BC.
- Trial-prior odds ratios: phase I→II OR 1.27 (95% CI 1.22–1.33), primary-endpoint OR 1.11 (95% CI 1.09–1.14) — verified verbatim against Zhang et al. 2026 Results.

## Example Queries

- "How cell-type-specific is CD276 in this lung atlas?"
- "Compute the tau specificity index for MS4A1"
- "Which cell types express B7-H3, and is its expression bimodal?"
- "Profile this gene's specificity and give me the trial-success prior"

## Example Output

`profile.json` (demo, `--demo --trial-prior`, abbreviated):

```json
{
  "skill": "celltype-specificity-profiler",
  "gene": "MS4A1",
  "atlas": "pbmc3k (10x, real; scanpy bundled)",
  "tau": 0.956,
  "tau_threshold": 0.69,
  "tau_threshold_note": "cohort-specific K-means(k=2) midpoint of the trial-level tau distribution in Zhang et al. 2026 (tau=0.69); an interpretive default, not a universal cutoff",
  "n_cell_types_used_for_tau": 7,
  "n_cell_types_excluded_small": 1,
  "bimodality_coefficient": 0.4936,
  "interpretation": "cell-type-specific (tau > 0.69)",
  "low_expression": false,
  "top_cell_types": [
    {"cell_type": "B cells", "mean_expr": 0.993, "pct_expressing": 0.8596},
    {"cell_type": "FCGR3A+ Monocytes", "mean_expr": 0.0601, "pct_expressing": 0.0867}
  ],
  "trial_prior": {
    "note": "Odds ratios from Zhang et al. 2026 (bioRxiv 10.64898/2026.02.23.707551)",
    "phase_I_to_II_OR": 1.27,
    "primary_endpoint_OR": 1.11,
    "lower_AE_rate": true
  }
}
```

`per_celltype.csv`:

```csv
cell_type,mean_expr,median_expr,pct_expressing,n_cells
B cells,0.993,1.0986,0.8596,342
FCGR3A+ Monocytes,0.0601,0.0,0.0867,150
```

*ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses.*

## Output Structure

```text
output_directory/
├── profile.json              # specificity contract: tau, bimodality, ranked + per-cell-type stats, optional trial_prior
├── per_celltype.csv          # tidy per-cell-type table
└── reproducibility/
    ├── commands.sh            # exact command to reproduce
    ├── environment.yml        # pip/conda environment snapshot
    └── checksums.sha256       # SHA-256 of the outputs
```

## Dependencies

**Required**:
- `scanpy`; load atlas / bundled demo dataset
- `anndata` >= 0.9; `.h5ad` I/O
- `numpy` >= 1.23; tau / bimodality math
- `scipy` >= 1.9; distribution statistics
- `pandas` >= 2.0; tabular output

No network access required in `--demo` mode after pbmc3k is cached on first fetch.

## Gotchas

- **Sparse genes**: The model will want to trust the bimodality coefficient for any gene. Do not — a gene expressed in <1% of cells gives an unstable BC; the skill sets `low_expression: true` and the BC must be treated as unreliable.
- **Annotation granularity drives tau**: The model will want to compare tau across atlases. Do not — coarse labels ("immune cell") inflate apparent ubiquity, fine labels raise tau. Always report the annotation level; never compare tau across atlases with different ontologies.
- **The 0.69 threshold is cohort-specific**: The model will want to treat `tau > 0.69` as an absolute "specific" verdict. Do not — Zhang et al. 2026 obtained 0.69 from K-means (k=2) on *their* trial-level tau distribution, so the binary call is an interpretive convenience. Report the continuous `tau`, and recalibrate the cut on your own distribution if you must binarize.
- **Per-atlas tau ≠ the paper's per-gene tau**: The model will want to compare a single run against the paper's published per-gene values. Do not — this skill returns tau *within the one matrix it is handed*, whereas Zhang et al. 2026 average per-tissue tau across all tissues where the gene is expressed (a job for the orchestrator calling this skill per tissue).
- **Thin atlases under-power tau**: The model will want to trust tau from a small slice. Do not — cell types with <20 cells are dropped from the tau computation, so on a thin atlas several groups may be excluded; check `n_cell_types_used_for_tau` first.
- **Log-normalized input required**: The model will want to feed whatever `X` is present. Do not — tau assumes non-negative expression. Z-scored matrices (with negatives) produce meaningless tau; the demo deliberately reads `.raw` (log-normalized) rather than the z-scored `.X`.
- **Symbol/Ensembl mismatch**: The model will want to return zeros when a symbol is absent. Do not — the gene must resolve in `var`; a small alias map handles CD276 ↔ B7-H3, but novel/retired symbols fail loudly.
- **`--trial-prior` is correlational**: The model will want to present odds ratios as predictive. Do not — they come from one observational study and are not a guarantee of trial success.

## Safety

- **Local-first**: Pure local computation on a provided matrix; no data upload.
- **Disclaimer**: *ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.*
- **Audit trail**: Writes a `commands.sh` / `environment.yml` / `checksums.sha256` reproducibility bundle for every run.
- **No hallucinated science**: tau, bimodality, thresholds, and odds ratios all trace to cited sources; missing genes/columns raise rather than returning silent zeros.

## Agent Boundary

The agent (LLM) dispatches this skill and explains its output. The skill (Python) executes the computation. The agent must NOT recompute tau/bimodality by hand, override the thresholds, invent cell types, or present the `--trial-prior` odds ratios as causal.

## Chaining Partners

- **Upstream** — `scrna-embedding` / `scrna-orchestrator`: produce the annotated `.h5ad` this skill consumes; `omics-target-evidence-mapper`: supplies the candidate gene.
- **Downstream** — `target-validation-scorer`: ingests `profile.json`'s specificity features; `clinical-trial-finder`: uses the prioritized target. Chain: `omics-target-evidence-mapper` → **`celltype-specificity-profiler`** → `target-validation-scorer` → `clinical-trial-finder`.
- Output is structured JSON/CSV, so it chains cleanly via the Bio Orchestrator.

## Maintenance

- **Review cadence**: Re-check on each major `scanpy`/`anndata` release (the demo loader uses `sc.datasets.pbmc3k_processed`).
- **Staleness signals**: scanpy changes the bundled `pbmc3k` API or `.raw` layout; HGNC retires an aliased symbol; the Zhang et al. odds ratios are superseded by a peer-reviewed version.
- **Deprecation criteria**: Retire if ClawBio adds a first-class per-gene specificity metric to `scrna-orchestrator`, or fold the trial-prior block into a dedicated scoring skill.

## Citations

- Zhang H.G., Eckmann P., Miao J., Mahon A.B., Zou J. *The Virtual Biotech: A Multi-Agent AI Framework for Therapeutic Discovery and Development.* bioRxiv 2026. doi:10.64898/2026.02.23.707551
- Yanai I. et al. *Genome-wide midrange transcription profiles reveal expression level relationships in human tissue specification* (tau specificity index). Bioinformatics 2005.
- Pfister R., Schwarz K.A., Janczyk M., Dale R., Freeman J.B. *Good things peak in pairs: a note on the bimodality coefficient.* Frontiers in Psychology 2013.
- Tabula Sapiens Consortium. *Tabula Sapiens v2.* CZ CELLxGENE Census.
