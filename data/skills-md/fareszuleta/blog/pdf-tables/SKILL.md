---
name: pdf-tables
description: "Use when the user asks to extract a table or tabular data from a PDF as CSV, Markdown or JSON. Do not use for plain prose extraction or for summarizing a PDF."
---

# pdf-tables

Extract tables by reading the PDF's layout data, not by running OCR over a flattened page.

## Steps
1. Confirm the PDF has a text layer: run `pdftotext -l 1 file.pdf - | head`. If it prints nothing, the PDF is a scan. Say so, and only then fall back to OCR (`ocrmypdf file.pdf out.pdf`), warning that the structure may be wrong.
2. Install the reader once if needed: `pip install pdfplumber`.
3. Extract the tables from the page the user named (or all pages):
   ```python
   import pdfplumber, csv, sys
   with pdfplumber.open("file.pdf") as pdf:
       for n, page in enumerate(pdf.pages, 1):
           for i, table in enumerate(page.extract_tables(), 1):
               with open(f"page{n}-table{i}.csv", "w", newline="") as f:
                   csv.writer(f).writerows(table)
   ```
4. Open each CSV and check it: same number of columns in every row, headers in the first row, merged header cells not shifted by one column. If a header spans two rows, merge them into one label per column and tell the user.
5. Return the CSV path and show the first rows so the user can confirm.

## Rules
- Never invent or "fix" numbers. If a cell is empty in the PDF, leave it empty.
- Report which pages had no table.
