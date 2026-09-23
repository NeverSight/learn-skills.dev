---
name: "office-excel"
description: "Read and write Microsoft Excel (.xlsx) files. Use when the user asks to read, analyze, create, or convert Excel spreadsheets."
---

## Read an Excel file

Converts all sheets of an `.xlsx` to Markdown tables:

```bash
uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/read_excel.py "<path_to_xlsx>"
```

Read a specific sheet:

```bash
uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/read_excel.py "<path_to_xlsx>" "SheetName"
```

Save as `.md` file:

```bash
uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/read_excel.py "<path_to_xlsx>" "<output.md>"
```

## Write an Excel file

### Preferred: Directly from markdown content (no intermediate file)

Pipe markdown table content directly into the script using `--stdin`. This avoids creating temporary files:

```bash
echo '<markdown_content>' | uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/write_excel.py --stdin "<output.xlsx>"
```

For multi-line content, use a heredoc:

```bash
uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/write_excel.py --stdin "<output.xlsx>" <<'EOF'
## Sheet Name

| Col1 | Col2 |
|------|------|
| a    | b    |
EOF
```

### From an existing Markdown file

If a `.md` file with tables already exists, use it directly:

```bash
uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/write_excel.py "<input.md>" "<output.xlsx>"
```

If you had to create the `.md` file as an intermediate step (it didn't exist before), delete it after generating the Excel.

### From JSON

Create a `.json` file with an array of objects, then:

```bash
uv run --with openpyxl ~/.kiro/skills/office-excel/scripts/write_excel.py "<input.json>" "<output.xlsx>"
```

## Notes

- Each Markdown table becomes a separate sheet when writing
- Headings before tables are used as sheet names
- JSON input must be a non-empty array of objects
- Headers are auto-bolded and columns auto-sized
- IMPORTANT: Do NOT create intermediate markdown files if you can pipe content directly via `--stdin`. If you must create one (e.g., content is too large for a heredoc), always delete it after generating the Excel.
