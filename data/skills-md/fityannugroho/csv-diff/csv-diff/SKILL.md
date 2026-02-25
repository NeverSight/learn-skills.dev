---
name: csv-diff
description: Compare two CSV files and generate a unified diff file showing line-by-line differences.
---

# CSV Diff

Compare two CSV files to identify changes, additions, or deletions between them and generate a unified diff output similar to `git diff`.

## When to use

Use this when you need to:
- Compare two CSV files and see what changed between them, especially for large datasets.
- Generate a unified diff file for tracking changes in tabular data.

## Quick start

Compare two CSV files:

```bash
csvdiff old.csv new.csv
```

This will generate a `result.diff` file showing the differences.

## Documentation

- Run `csvdiff --help` to see available options and usage.
- Read the [documentation](https://github.com/fityannugroho/csv-diff) for more details.

## Output

The tool generates a unified diff output similar to the following:

```diff
--- old.csv
+++ new.csv
@@ -2,3 +2,3 @@
 0,Alice,70000
-1,John,50000
+1,John,55000
 2,Jane,60000
```

The output shows:
- Lines prefixed with `-` were removed or changed
- Lines prefixed with `+` were added or changed
- Context lines (no prefix) show unchanged data for reference

## Notes

- CSV files must have a header row.
- Output is saved to a `.diff` file (default: `result.diff`).

## Requirements

The `csv-diff-py` package must be installed in your environment. You can install it globally via `uv` (or user-preferred python package manager):

```bash
uv tool install csv-diff-py
```

Alternatively, run it directly with `uvx` (or user-preferred python package runner):

```bash
uvx --from csv-diff-py csvdiff file1.csv file2.csv
```
