---
name: data-analysis
description: Generate statistical analysis code with 4-round review. Select appropriate statistical tests, interpret results, and produce analysis reports with p-values, effect sizes, and confidence intervals. Use when analyzing experimental data for a paper.
argument-hint: [data-source]
---

# Data Analysis

Generate rigorous statistical analysis code with multi-round review.

## Input

- `$0` — Data source (CSV, JSON, pickle, or experiment logs)
- `$1` — Research goal or hypothesis to test

## References

- 4-round code review prompts: `~/.claude/skills/data-analysis/references/review-prompts.md`

## Scripts

### Statistical summary and comparison
```bash
python ~/.claude/skills/data-analysis/scripts/stat_summary.py --input results.csv --compare method --metric accuracy --output summary.json
python ~/.claude/skills/data-analysis/scripts/stat_summary.py --input results.csv --describe
```

Detects data types, recommends tests, runs comparisons, outputs effect sizes and significance stars. Requires numpy, scipy.

### Format p-values
```bash
python ~/.claude/skills/data-analysis/scripts/format_pvalue.py --values "0.001 0.05 0.23" --format stars
python ~/.claude/skills/data-analysis/scripts/format_pvalue.py --csv results.csv --column pvalue --format latex
```

Formats p-values with stars, LaTeX notation, or plain text. Stdlib-only.

## Workflow

### Step 1: Generate Analysis Code
Structure the code with these sections:
1. `# IMPORT` — pandas, numpy, scipy, statsmodels, sklearn
2. `# LOAD DATA` — Load from original data files
3. `# DATASET PREPARATIONS` — Missing values, units, exclusion criteria
4. `# DESCRIPTIVE STATISTICS` — Summary tables if needed
5. `# PREPROCESSING` — Dummy variables, normalization
6. `# ANALYSIS` — Statistical tests per hypothesis
7. `# SAVE ADDITIONAL RESULTS` — Extra results to pickle

### Step 2: 4-Round Code Review
1. **Round 1 — Code Flaws**: Mathematical/statistical errors, wrong calculations, trivial tests
2. **Round 2 — Data Handling**: Missing values, units, preprocessing, test choice
3. **Round 3 — Per-Table**: Sensible values, measures of uncertainty, missing data
4. **Round 4 — Cross-Table**: Completeness, consistency, missing variables

### Step 3: Produce Results
- Every nominal value must have uncertainty (CI, STD, or p-value)
- Statistical tests must be appropriate for the data type
- Results must match actual data — never hallucinate

## Allowed Packages

`pandas`, `numpy`, `scipy`, `statsmodels`, `sklearn`, `pickle`

## Statistical Test Selection

| Data Type | Test |
|-----------|------|
| Two groups, normal | Independent t-test |
| Two groups, non-normal | Mann-Whitney U |
| Paired samples | Paired t-test / Wilcoxon |
| Multiple groups | ANOVA / Kruskal-Wallis |
| Categorical | Chi-square / Fisher's exact |
| Correlation | Pearson / Spearman |
| Regression | OLS / Logistic / Mixed effects |

## Rules

- Always report p-values for statistical tests
- Account for relevant confounding variables
- Use inherent package functionality (e.g., `formula = "y ~ a * b"` for interactions)
- Do not manually implement available statistical functions
- Access dataframes using string-based column names, not integer indices

## Related Skills
- Upstream: [experiment-code](../experiment-code/), [experiment-design](../experiment-design/)
- Downstream: [table-generation](../table-generation/), [figure-generation](../figure-generation/), [backward-traceability](../backward-traceability/)
- See also: [math-reasoning](../math-reasoning/)
