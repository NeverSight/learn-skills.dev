---
name: write-local-report
description: Write a comprehensive work report in Traditional Chinese following project report templates. Use when the user wants to create a development progress report, document completed work, or generate a work report from `.github/reports/` templates.
metadata:
  original-prompt: write-local-report.prompt.md
  report-language: 正體中文
---

# Write Local Report

Write a comprehensive work report following project report templates.

## Report Protocol

Development progress is tracked within the `.github/reports` directory. Treat all past reports as immutable references — do not edit or revise them. Generate a new comprehensive work report upon task completion. Refer to naming conventions of existing files to determine an appropriate filename.

Reports must include a detailed account of the work performed, encompassing all relevant code modifications and corresponding test outcomes.

## Instructions

Write the report following `references/REPORT_TEMPLATE.md` and `references/report_guidelines.md` in 正體中文.

Follow the template exactly. Strictly follow `references/REPORT_TEMPLATE.md`.
