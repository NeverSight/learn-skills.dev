---
name: pandas-data-cleaning
description: Cleans messy tabular datasets in pandas end-to-end — fixing dtypes, parsing dates and numbers, standardizing text, handling missing values, removing duplicates, detecting and treating outliers, and reshaping wide/long into tidy data. Use this skill when the user asks to "clean this CSV/Excel/dataframe", "fix data types", "handle missing values / NaNs", "remove duplicates", "deal with outliers", "standardize column names or categories", "parse dates", "melt/pivot/reshape", or to build a reproducible cleaning pipeline before analysis or modeling.
license: MIT
---

# pandas Data Cleaning

## Overview

Keywords: pandas, data cleaning, dtypes, missing values, NaN, imputation, duplicates, outliers, IQR, z-score, tidy data, melt, pivot, normalize, standardize, parse dates, categorical, data quality, ETL preprocessing.

This skill turns a messy DataFrame into a tidy, correctly-typed, analysis-ready dataset using a repeatable, auditable workflow. The core principle: **profile first, decide explicitly, transform with logging, validate after.** Never mutate data silently — every fill, drop, or cast should be a deliberate, documented choice you can defend.

Treat cleaning as a pipeline that produces (1) the cleaned DataFrame and (2) a record of decisions. Prefer chained, non-mutating transforms (`df.assign(...)`, `.pipe(...)`) over scattered in-place edits so the pipeline is reproducible top-to-bottom.

## Workflow

1. **Profile the raw data.** Before changing anything, understand it. Run `scripts/profile_data.py <path>` (or replicate inline) to get shape, dtypes, per-column null counts/percentages, unique counts, sample values, and candidate problems (mixed types, high-cardinality strings, numeric-looking objects, constant columns). See `references/cleaning-checklist.md`.

2. **Fix structure.** Standardize column names (snake_case, strip whitespace, dedupe). Set/verify the index. Drop fully-empty rows/columns and constant columns that carry no signal. Confirm one observation per row, one variable per column (tidy form). If not tidy, defer reshape to step 8.

3. **Coerce dtypes.** Convert numeric-looking strings (`"1,234"`, `"$5.00"`, `"12%"`) to numbers, parse dates with explicit formats, cast low-cardinality strings to `category`, and use nullable dtypes (`Int64`, `boolean`, `string`) where missing values must coexist with non-float types. See `references/dtype-conversion.md`.

4. **Standardize text & categories.** Trim whitespace, normalize case, collapse synonyms ("USA"/"U.S.A."/"United States"), fix encoding artifacts, and map free-text categories to a controlled vocabulary.

5. **Handle missing values.** First distinguish *disguised* missing (`"NA"`, `"-"`, `"unknown"`, `-999`, empty string) from real values and convert them to `NaN`/`pd.NA`. Then choose a strategy per column — drop, constant fill, statistical impute (mean/median/mode), forward/backfill for time series, or model-based — and **document why**. Use the decision framework below.

6. **Remove duplicates.** Detect exact duplicates and key-based duplicates (`subset=[...]`). Decide keep policy (`first`/`last`/aggregate). Watch for near-duplicates from inconsistent text (handle those in step 4 first).

7. **Detect & treat outliers.** Use IQR fences or z-scores to flag, then decide: keep (legitimate extreme), cap/winsorize, transform (log), or remove (data error). Never delete outliers reflexively. See `references/outliers-and-reshaping.md`.

8. **Reshape to tidy.** Use `melt` to go wide→long, `pivot`/`pivot_table` for long→wide, and `str.split`/`explode` to split packed columns. Confirm the result satisfies the three tidy rules.

9. **Validate.** Re-profile. Assert invariants: expected row count range, no unexpected nulls in required columns, dtypes correct, key uniqueness, value ranges/domains. Fail loudly if violated. See the validation section in `references/cleaning-checklist.md`.

10. **Persist the recipe.** Capture the ordered transforms in a single function/notebook cell so the same raw input always yields the same clean output. Use `templates/cleaning_report.md` to summarize what was done and why.

## Missing-Value Decision Framework

| Situation | Recommended strategy |
|---|---|
| Column >50–60% missing, not critical | Drop the column |
| A few rows missing in a required key/target | Drop those rows |
| Numeric, missing-at-random, skewed | Impute **median** |
| Numeric, roughly symmetric | Impute **mean** (or median for robustness) |
| Categorical | Impute **mode**, or add explicit `"Missing"` category |
| Time series / ordered | `ffill`/`bfill`, or interpolate (`.interpolate()`) |
| Missingness is itself informative | Keep `NaN` + add boolean `was_missing` flag |
| Need non-float ints with NaN | Cast to nullable `Int64`, don't fill |

Rule of thumb: imputing changes the distribution. For modeling, prefer adding a missingness indicator alongside the imputed value so the model can learn from "was missing."

## Outlier Decision Framework

1. **Flag, don't auto-delete.** Compute IQR fences (`Q1 - 1.5*IQR`, `Q3 + 1.5*IQR`) or |z| > 3.
2. **Investigate.** Is it a data-entry error (age = 999), a unit mistake (cm vs m), or a real rare event?
3. **Treat by cause:** error → fix or remove; legitimate extreme but distorting → winsorize/cap at the fence or log-transform; legitimate and meaningful → keep.
4. Use robust methods (IQR, median) over mean/std on skewed data, since mean/std are themselves dragged by outliers.

## Worked Example (condensed)

Given a column `price` of strings like `"$1,299.00"`, `"N/A"`, `""`:

```python
df["price"] = (
    df["price"]
      .replace({"N/A": pd.NA, "": pd.NA})
      .str.replace(r"[$,]", "", regex=True)
      .pipe(pd.to_numeric, errors="coerce")   # bad parses -> NaN
)
df["price"] = df["price"].fillna(df["price"].median())  # documented: skewed
```

See `examples/clean_messy_sales.md` for a full raw→clean walkthrough with a 12-column messy sales file, and run `scripts/clean_pipeline.py --help` for a configurable end-to-end cleaner.

## Best Practices

- **Profile before and after.** You cannot clean what you have not measured, and you cannot trust a clean you did not verify.
- **Prefer non-mutating chains.** Build the cleaned frame with `.assign`/`.pipe` so the whole recipe is one readable, rerunnable block. Avoid sprinkling `inplace=True`.
- **Coerce with `errors="coerce"`**, then inspect the new NaNs — they reveal unparseable values you'd otherwise miss.
- **Use explicit date formats** (`pd.to_datetime(s, format="%Y-%m-%d")`) to avoid silent misparsing of ambiguous `01/02/03`.
- **Use nullable dtypes** (`Int64`, `boolean`, `string`) instead of forcing floats just to hold NaN.
- **Document every destructive choice** (drop/fill/cap) in the cleaning report so reviewers can challenge it.
- **Validate with assertions** at the end; treat a cleaning script that produces silently-wrong data as a bug.
- **Keep the raw file immutable.** Always read raw, write cleaned to a new path.

## Common Pitfalls

- **Disguised missing values** (`"unknown"`, `-999`, `"-"`, whitespace) left as real data, poisoning means and joins. Always normalize these to NaN first.
- **`inplace=True` chaining bugs** and accidental `SettingWithCopyWarning` from chained indexing — use `.loc` and reassignment.
- **Auto-deleting outliers** before checking whether they're legitimate, throwing away the most interesting rows.
- **Mean-imputing skewed columns**, dragging the central tendency and shrinking variance.
- **`float64` columns full of `1.0`/`2.0`** because NaN forced float — cast to `Int64` after cleaning.
- **Ambiguous date parsing** (`dayfirst` vs default) silently swapping day/month.
- **Dropping duplicates before standardizing text**, so `"Acme "` and `"acme"` survive as distinct.
- **Pivot collisions** — using `pivot` when index/column pairs aren't unique; use `pivot_table` with an explicit `aggfunc`.
- **No post-clean validation**, shipping a dataset whose row count or domain quietly broke.
