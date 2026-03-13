---
name: data-wizard
description: >-
  Analyze data and guide ML: EDA, model selection, feature engineering, stats,
  visualization, MLOps. Use for data work. NOT for ETL, database design
  (database-architect), or frontend viz code.
argument-hint: "<mode> <data|task|question> [options]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Data Wizard

Full-stack data science and ML engineering — from exploratory data analysis through model deployment strategy. Adapts approach based on complexity classification.

## Canonical Vocabulary

| Term | Definition |
|------|-----------|
| **EDA** | Exploratory Data Analysis — systematic profiling and summarization of a dataset |
| **feature** | An individual measurable property used as input to a model |
| **feature engineering** | Creating, transforming, or selecting features to improve model performance |
| **hypothesis test** | A statistical procedure to determine if observed data supports a claim |
| **p-value** | Probability of observing data at least as extreme as the actual results, assuming the null hypothesis is true |
| **effect size** | Magnitude of a difference or relationship, independent of sample size |
| **power analysis** | Determining sample size needed to detect an effect of a given size |
| **CUPED** | Controlled-experiment Using Pre-Experiment Data — variance reduction technique for A/B tests |
| **MLOps maturity** | Level 0 (manual), Level 1 (ML pipeline), Level 2 (CI/CD + CT), Level 3 (full automation) |
| **data quality score** | Composite metric across completeness, consistency, accuracy, timeliness, uniqueness |
| **profile** | Statistical summary of a dataset: types, distributions, missing patterns, correlations |
| **anomaly** | Data point or pattern deviating significantly from expected behavior |

## Dispatch

| `$ARGUMENTS` | Action |
|---|---|
| `eda <data>` | **EDA** — profile dataset, summary stats, missing patterns, distributions |
| `model <task>` | **Model Selection** — recommend models, libraries, training plan for task |
| `features <data>` | **Feature Engineering** — suggest transformations, encoding, selection pipeline |
| `stats <question>` | **Stats** — select and design statistical hypothesis test |
| `viz <data>` | **Visualization** — recommend chart types, encodings, layout for data |
| `experiment <hypothesis>` | **Experiment Design** — A/B test design, power analysis, CUPED |
| `timeseries <data>` | **Time Series** — forecasting approach, decomposition, model selection |
| `anomaly <data>` | **Anomaly Detection** — detection approach, algorithm selection, threshold strategy |
| `mlops <model>` | **MLOps** — serving strategy, deployment pipeline, monitoring plan |
| Natural language about data | **Auto-detect** — classify intent, route to appropriate mode |
| Empty | **Gallery** — show common data science tasks with mode recommendations |

### Auto-Detection Heuristic

If no mode keyword matches:

1. Mentions dataset, CSV, columns, rows, missing values → **EDA**
2. Mentions predict, classify, regression, recommend → **Model Selection**
3. Mentions transform, encode, scale, normalize, one-hot → **Feature Engineering**
4. Mentions test, significant, p-value, hypothesis, correlation → **Stats**
5. Mentions chart, plot, graph, visualize, dashboard → **Visualization**
6. Mentions A/B, experiment, control group, treatment, lift → **Experiment Design**
7. Mentions forecast, seasonal, trend, time series, lag → **Time Series**
8. Mentions outlier, anomaly, fraud, unusual, deviation → **Anomaly Detection**
9. Mentions deploy, serve, pipeline, monitor, retrain → **MLOps**
10. Ambiguous → ask: "Which area: EDA, modeling, stats, or something else?"

### Gallery (Empty Arguments)

Present common data science tasks:

| # | Task | Mode | Example |
|---|------|------|---------|
| 1 | Profile a dataset | `eda` | `/data-wizard eda customer_data.csv` |
| 2 | Choose a model | `model` | `/data-wizard model "predict churn from usage features"` |
| 3 | Engineer features | `features` | `/data-wizard features sales_data.csv` |
| 4 | Pick a stat test | `stats` | `/data-wizard stats "is conversion rate different between groups?"` |
| 5 | Choose visualizations | `viz` | `/data-wizard viz time_series_metrics.csv` |
| 6 | Design an experiment | `experiment` | `/data-wizard experiment "new checkout flow increases conversion"` |
| 7 | Forecast time series | `timeseries` | `/data-wizard timeseries monthly_revenue.csv` |
| 8 | Detect anomalies | `anomaly` | `/data-wizard anomaly server_metrics.csv` |
| 9 | Plan deployment | `mlops` | `/data-wizard mlops "churn prediction model"` |

> Pick a number or describe your data science task.

### Skill Awareness

Before starting, check if another skill is a better fit:

| Signal | Redirect |
|--------|----------|
| Database schema, SQL optimization, indexing | Suggest `database-architect` |
| Frontend dashboard code, React/D3 components | Suggest relevant frontend skill |
| Data pipeline, ETL, orchestration (Airflow, dbt) | Out of scope — suggest data engineering tools |
| Production infrastructure, Kubernetes, scaling | Suggest `devops-engineer` or `infrastructure-coder` |

## Complexity Classification

Score the query on 4 dimensions (0-2 each, total 0-8):

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Data complexity** | Single table, clean | Multi-table, some nulls | Messy, multi-source, mixed types |
| **Analysis depth** | Descriptive stats | Inferential / predictive | Multi-stage pipeline, iteration |
| **Domain specificity** | General / well-known | Domain conventions apply | Deep domain expertise needed |
| **Tooling breadth** | Single library suffices | 2-3 libraries needed | Full ML stack integration |

| Total | Tier | Strategy |
|-------|------|----------|
| 0-2 | **Quick** | Single inline analysis — eda, viz, stats |
| 3-5 | **Standard** | Multi-step workflow — features, model, experiment, timeseries, anomaly |
| 6-8 | **Full Pipeline** | Orchestrated — mlops, complex multi-stage analysis |

Present the scoring to the user. User can override tier.

## Mode Protocols

### EDA (Quick)

1. If file path provided, run: `!uv run python skills/data-wizard/scripts/data-profiler.py "$1"`
2. Parse JSON output — present: row/col counts, dtypes, missing patterns, top correlations
3. Highlight: data quality issues, distribution skews, potential target leakage
4. Recommend next steps: cleaning, feature engineering, or modeling

### Model Selection (Standard)

1. Run: `!uv run python skills/data-wizard/scripts/model-recommender.py` with task JSON input
2. Present ranked model recommendations with rationale
3. Read `references/model-selection.md` for detailed guidance by data size and type
4. Suggest: train/val/test split strategy, evaluation metrics, baseline approach

### Feature Engineering (Standard)

1. If file path, run data profiler first for column analysis
2. Read `references/feature-engineering.md` for patterns by data type
3. Load `data/feature-engineering-patterns.json` for structured recommendations
4. Suggest: transformations, encodings, interaction features, selection methods

### Stats (Quick)

1. Run: `!uv run python skills/data-wizard/scripts/statistical-test-selector.py` with question parameters
2. Load `data/statistical-tests-tree.json` for decision tree
3. Read `references/statistical-tests.md` for assumptions and interpretation guidance
4. Present: recommended test, alternatives, assumptions to verify, interpretation template

### Visualization (Quick)

1. Load `data/visualization-grammar.json` for chart type selection
2. Match data characteristics to visualization types
3. Recommend: chart type, encoding channels, color palette, layout

### Experiment Design (Standard)

1. Read `references/experiment-design.md` for A/B test patterns
2. Design: hypothesis, metrics, sample size (power analysis), duration
3. Address: novelty effects, multiple comparisons, CUPED variance reduction
4. Output: experiment brief with decision criteria

### Time Series (Standard)

1. If file path, run data profiler for temporal patterns
2. Assess: stationarity, seasonality, trend, autocorrelation
3. Recommend: decomposition method, forecasting model, validation strategy
4. Address: cross-validation for time series (walk-forward), feature lags

### Anomaly Detection (Standard)

1. Classify: point anomalies, contextual anomalies, collective anomalies
2. Recommend: algorithm (Isolation Forest, LOF, DBSCAN, autoencoder, etc.)
3. Address: threshold selection, false positive management, interpretability
4. Suggest: alerting strategy, root cause investigation framework

### MLOps (Full Pipeline)

1. Read `references/mlops-maturity.md` for maturity model
2. Assess current maturity level (0-3)
3. Design: serving strategy (batch vs real-time), monitoring, retraining triggers
4. Address: model versioning, A/B testing in production, rollback strategy
5. Output: deployment architecture brief

## Data Quality Assessment

Run: `!uv run python skills/data-wizard/scripts/data-quality-scorer.py <path>`

Dimensions scored:

| Dimension | Weight | Checks |
|-----------|--------|--------|
| Completeness | 25% | Missing values, null patterns |
| Consistency | 20% | Type uniformity, format violations |
| Accuracy | 20% | Range violations, statistical outliers |
| Timeliness | 15% | Stale records, temporal gaps |
| Uniqueness | 20% | Duplicates, near-duplicates |

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/statistical-tests.md` | Decision tree for test selection, assumptions, interpretation | Stats mode |
| `references/model-selection.md` | Model catalog by task type, data size, interpretability needs | Model Selection mode |
| `references/feature-engineering.md` | Patterns by data type: numeric, categorical, temporal, text, geospatial | Feature Engineering mode |
| `references/experiment-design.md` | A/B test patterns, CUPED, power analysis, multiple comparison corrections | Experiment Design mode |
| `references/mlops-maturity.md` | Maturity levels 0-3, deployment patterns, monitoring strategy | MLOps mode |
| `references/data-quality.md` | Quality framework, scoring dimensions, remediation strategies | EDA mode, Data Quality Assessment |

**Loading rule:** Load ONE reference at a time per the "Read When" column. Do not preload.

## Critical Rules

1. **Always run data profiler before recommending models or features** — never guess at data characteristics without evidence
2. **Present classification scoring before executing analysis** — user must see and can override complexity tier
3. **Never recommend a statistical test without stating its assumptions** — untested assumptions invalidate results
4. **Always specify effect size alongside p-values** — statistical significance without practical significance is misleading
5. **Model recommendations must include a baseline** — always start with the simplest viable model (logistic regression, linear regression, naive forecast)
6. **Never skip train/test split strategy** — leakage is the most common ML mistake
7. **Experiment designs must include power analysis** — underpowered experiments waste resources
8. **Feature engineering must address target leakage risk** — flag any feature derived from post-outcome data
9. **Time series cross-validation must use walk-forward** — random splits violate temporal ordering
10. **MLOps recommendations must assess current maturity** — do not recommend Level 3 automation for Level 0 teams
11. **Load ONE reference file at a time** — do not preload all references into context
12. **Data quality scores must be computed, not estimated** — run the scorer script on actual data

**Canonical terms** (use these exactly throughout):
- Modes: "EDA", "Model Selection", "Feature Engineering", "Stats", "Visualization", "Experiment Design", "Time Series", "Anomaly Detection", "MLOps"
- Tiers: "Quick", "Standard", "Full Pipeline"
- Quality dimensions: "Completeness", "Consistency", "Accuracy", "Timeliness", "Uniqueness"
- MLOps levels: "Level 0" (manual), "Level 1" (pipeline), "Level 2" (CI/CD+CT), "Level 3" (full auto)
