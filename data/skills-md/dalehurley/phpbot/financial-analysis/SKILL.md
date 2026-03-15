---
name: financial-analysis
description: "Analyze financial statements from PDF documents. Use when asked to prepare a financial analysis, review financial statements, analyze balance sheets, income statements, or cash flow statements. Triggers include: any mention of 'financial analysis', 'financial statements', 'balance sheet', 'income statement', 'cash flow', 'financial review', 'annual report analysis', or requests to analyze PDF documents containing financial data."
tags: [auto-generated]
version: 0.1.0
---

# Skill: financial-analysis

## When to Use
Use this skill when the user asks to analyze or review financial statements, typically provided as a PDF file.

Example triggers:
- "Prepare a financial analysis of this PDF"
- "Analyze the financial statements in this document"
- "Review the balance sheet and income statement"
- "Summarize the annual report"
- "What are the key financial ratios from this report?"

## Procedure
1. Identify the source PDF document from the user's request.
2. Extract text content from the PDF using available tools (e.g., bash with `pdftotext`, or read the file directly).
3. Parse and identify the key financial statements: balance sheet, income statement, cash flow statement, and notes.
4. Perform year-over-year comparisons where multiple periods are available.
5. Calculate key financial ratios and metrics (liquidity, profitability, leverage, efficiency).
6. Identify strengths, challenges, and strategic opportunities.
7. Generate output documents in multiple formats (markdown, HTML, and/or summary text) in the same directory as the source file.
8. Provide an executive summary highlighting the most important findings and recommendations.

## Example
An example of a request that uses this skill:

```
Prepare a financial analysis of a PDF file
```

## Last Result (truncated)
```
## Task Completed Successfully!

Prepared a comprehensive financial analysis of financial statements. Deliverables included:

1. **README_Analysis_Summary.txt** - Overview, quick start guide, executive summary with key findings
2. **Financial_Analysis.md** - Complete comprehensive analysis in markdown format with year-over-year comparisons, financial ratios and metrics, strengths/challenges/opportunities, strategic recommendations
3. **Financial_Analysis.html** - Same content formatted for browser viewing
```
