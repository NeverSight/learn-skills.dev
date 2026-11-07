---
name: power-bi-semantic-model
description: Use when reasoning about Power BI PBIX, TMDL, XMLA, Tabular models, calculation groups, DAX portability, or boundaries between Power BI semantic models and Excel Power Pivot.
---

# Power BI Semantic Model

## Core Rule

Confirm the host before writing DAX or model guidance. Power BI semantic models and Excel Power Pivot share tabular concepts, but feature support, deployment, refresh, and tooling are not identical.

## Decision Path

1. **Excel workbook target**
   - Use `power-pivot-dax-modeling`.
   - Prefer Excel-compatible DAX patterns such as `ALL`, `FILTER`, and `DIVIDE`.
   - Treat Power BI-specific or newer functions as portability risks until verified.

2. **Power BI semantic model target**
   - Identify whether the task involves PBIX, TMDL, XMLA endpoint, dataset/semantic model refresh, DAX measures, relationships, calculation groups, or deployment pipelines.
   - Use official Microsoft documentation when exact support or current product behavior matters.
   - Separate static DAX/model review from live model deployment or refresh evidence.

3. **Portability review**
   - Compare function support and host assumptions.
   - Flag Excel-only workbook patterns, CUBE formula dependencies, Power Query load targets, and Power BI-only features.
   - If the same measure must work in Excel and Power BI, choose the stricter host or maintain separate variants.

## Validation

- For Excel: run the package's DAX compatibility lint and model-report workflows.
- For Power BI: use model source files or exported metadata when available; do not imply PBIX internals were modified unless a supported tool actually did so.
- For current product behavior, verify against official Microsoft Learn/Fabric documentation.

## Boundaries

- This plugin does not decode or rewrite PBIX binaries by default.
- Static DAX review does not prove model refresh or report visuals.
- Excel `ThisWorkbookDataModel` and Power BI semantic models should not be treated as interchangeable runtime targets.

## References

- Read `references/host-boundary.md` before claiming that an Excel Power Pivot pattern is valid in Power BI, or that a Power BI semantic model pattern is valid in Excel.
