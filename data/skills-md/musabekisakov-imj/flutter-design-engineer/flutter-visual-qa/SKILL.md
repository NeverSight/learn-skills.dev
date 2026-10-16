---
name: flutter-visual-qa
description: Verify rendered Flutter interfaces through screenshots, golden tests, breakpoint comparisons, state matrices, and structured visual critique. Use when asked to compare designs, inspect polish, validate responsive or theme behavior, diagnose visual regressions, or confirm implementation quality after UI changes.
---

# Flutter Visual QA

Rendered output is the evidence. Source inspection alone cannot establish visual quality.

## Build a Matrix

Select the smallest representative matrix covering:

- compact and expanded constraints;
- light and dark themes when supported;
- primary, loading, empty, error, and destructive states as applicable;
- default and enlarged text;
- LTR and RTL for localized products.

Record the exact viewport, device-pixel ratio, theme, locale, and fixture state. Read `references/visual-qa.md`.
For connected or multi-domain products, also read `references/connected-product-workflows.md` and include partial-source failure in the matrix.

## Inspect

Review hierarchy and scan path first, then layout, type, spacing rhythm, color roles, controls, content realism, edge behavior, and pixel-level defects. Compare related states side by side. Distinguish implementation defects from subjective preference.

Prioritize:

1. task-blocking clipping, overlap, invisibility, or unreachable controls;
2. broken hierarchy, contrast, state communication, or adaptive composition;
3. inconsistency and polish defects;
4. optional aesthetic refinements.

## Golden Tests

Use golden tests for stable components and deterministic fixtures. Control fonts, animations, time, network content, and pixel ratio. Do not approve broad golden updates without inspecting diffs.

## Close the Loop

Require at least one refinement pass for material findings and recapture affected states. Report the matrix inspected, fixes made, unverified combinations, and artifact paths.
