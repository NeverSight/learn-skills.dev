---
name: xlsx-code-mode
description: Use this skill any time an Excel file (.xlsx, .xlsm) needs to be read, explored, understood, or modified. You cannot read .xlsx files with cat, head, or normal file-reading tools — this is the only way to inspect them. Trigger when you or the user need to open, look at, or explore a workbook; find out what sheets it has or where specific data lives; read cells, rows, columns, or ranges; search for values, labels, or patterns; trace formula dependencies or understand how a cell is calculated; run what-if scenarios by changing inputs and reading recalculated outputs; or edit cells, rows, columns, and sheets. Trigger when the user references a spreadsheet file by name or path — even casually (e.g. 'check the xlsx', 'what's in report.xlsx') — and also when you need to inspect a workbook yourself as part of a larger task. The tool runs sandboxed JavaScript against the workbook server-side via `witan xlsx exec`."
---

## Setup

Files are cached server-side by content hash so repeated operations skip re-upload. If `WITAN_STATELESS=1` is set (or `--stateless` is passed), files are processed but not stored.

The CLI automatically applies per-attempt request timeouts and retries transient API failures (`408`, `429`, `500`, `502`, `503`, `504`, plus timeout/network errors). Non-retryable `4xx` responses fail immediately.

## Quick Reference

```bash
# Explore — map out sheets and find data
witan xlsx exec model.xlsx --stdin <<'WITAN'
const sheets = await xlsx.listSheets(wb)
print("Sheets:", sheets.map(s => s.sheet))

const found = await xlsx.findCells(wb, "Revenue", { context: 1 })
print("Revenue cells:", found.length)
return { sheets, found }
WITAN

# Read from sheets with spaces, apostrophes, or parentheses — all safe
witan xlsx exec model.xlsx --stdin <<'WITAN'
const a = await xlsx.readCell(wb, "'Workers' Compensation'!B50")
const b = await xlsx.readRangeTsv(wb, { sheet: "Reserve Summary (Net)", from: {row:1,col:1}, to: {row:10,col:5} })
return { a: a.value, b }
WITAN

# What-if — change an input and read the recalculated output
witan xlsx exec model.xlsx --stdin <<'WITAN'
const result = await xlsx.setCells(wb, [
  { address: "Inputs!B5", value: 1.10 }
])
return { touched: result.touched, errors: result.errors }
WITAN

# Simple one-liner (--expr is fine when there are no special characters)
witan xlsx exec model.xlsx --expr 'xlsx.listSheets(wb)'
```

## Exit Codes

| Command | Code | Meaning                                                             |
| ------- | ---- | ------------------------------------------------------------------- |
| `exec`  | `0`  | Script completed successfully (`ok: true`)                          |
| `exec`  | `1`  | Transport/API error, invalid request, or script error (`ok: false`) |

## exec — Workbook Scripting

Runs JavaScript against a workbook via the Witan API. The workbook is opened server-side; scripts interact through the `xlsx` and `wb` globals.

### Invocation patterns

**Recommended: `--stdin` with heredoc** — safe for all sheet names, supports multi-line scripts, and batches multiple operations into a single CLI invocation:

```bash
witan xlsx exec report.xlsx --stdin <<'WITAN'
const sheets = await xlsx.listSheets(wb)
const cell = await xlsx.readCell(wb, "'My Sheet'!A1")
return { sheets, cell }
WITAN
```

The single-quoted heredoc delimiter (`<<'WITAN'`) prevents all shell expansion. Apostrophes, parentheses, double quotes, and glob characters in sheet names pass through verbatim to JavaScript — no escaping needed.

**Other invocation patterns** (use only when `--stdin` is impractical):

```bash
# Expression — simple one-liners with no special characters
witan xlsx exec report.xlsx --expr 'xlsx.listSheets(wb)'

# Script file — reusable scripts, e.g. parameterized scenarios
witan xlsx exec report.xlsx --script scenario.js --input-json '{"rate": 1.05}'
```

Provide exactly one code source: `--expr`, `--code`, `--script`, or `--stdin`. They are mutually exclusive.

### Flags

| Flag                 | Short | Default | Description                                                            |
| -------------------- | ----- | ------- | ---------------------------------------------------------------------- |
| `--expr`             |       | —       | Expression shorthand; wraps as `return (<expr>);`                      |
| `--code`             |       | —       | Inline JavaScript source                                               |
| `--script`           |       | —       | Path to a JavaScript file                                              |
| `--stdin`            |       | —       | Read JavaScript source from stdin                                      |
| `--input-json`       |       | `{}`    | JSON value passed as `input` to the script                             |
| `--timeout-ms`       |       | —       | Execution timeout in milliseconds (> 0); omit to use server default    |
| `--max-output-chars` |       | —       | Maximum stdout characters to capture (> 0); omit to use server default |
| `--save`             |       | `false` | Persist changes to the workbook file                                   |
| `--json`             |       | `false` | Print the full response envelope as JSON                               |

### Runtime globals

| Name    | Type            | Description                                                         |
| ------- | --------------- | ------------------------------------------------------------------- |
| `xlsx`  | object          | Curated API surface — all functions listed below                    |
| `wb`    | WorkbookContext | The opened workbook handle; pass as first arg to all `xlsx.*` calls |
| `input` | any             | Parsed value from `--input-json` (defaults to `{}`)                 |
| `print` | function        | Output to stdout (like `console.log` but captured in response)      |

Top-level `await` is supported. No imports allowed (static or dynamic).

### API reference

Functions are grouped by purpose. All are async and take `wb` as the first argument.

**Reading**

| Function                | Signature                 | Description                                                                                |
| ----------------------- | ------------------------- | ------------------------------------------------------------------------------------------ |
| `listSheets`            | `(wb)`                    | List all sheets with used ranges                                                           |
| `getWorkbookProperties` | `(wb)`                    | Workbook-level metadata                                                                    |
| `getSheetProperties`    | `(wb, sheet, filter?)`    | Get sheet properties (view, format, columns, rows, merges); `filter.columns/rows` to limit |
| `getUsedRange`          | `(wb, sheetName)`         | Used range for a sheet                                                                     |
| `listDefinedNames`      | `(wb)`                    | All defined names                                                                          |
| `readCell`              | `(wb, cell, opts?)`       | Read a single cell; `opts.context` adds surrounding cells                                  |
| `readRange`             | `(wb, range)`             | Read all cells in a range                                                                  |
| `readRow`               | `(wb, sheet, row, opts?)` | Read a row; `opts.startCol/endCol` to limit                                                |
| `readColumn`            | `(wb, sheet, col, opts?)` | Read a column; `opts.startRow/endRow` to limit                                             |
| `readRangeTsv`          | `(wb, range, opts?)`      | Read range as TSV text; `opts.includeEmpty`                                                |
| `readColumnTsv`         | `(wb, sheet, col, opts?)` | Read column as TSV text                                                                    |
| `readRowTsv`            | `(wb, sheet, row, opts?)` | Read row as TSV text                                                                       |
| `getStyle`              | `(wb, cell)`              | Get style properties (fill, font, alignment, border, numberFormat, richText) of a cell     |

**Searching**

| Function       | Signature                                | Description                                                                         |
| -------------- | ---------------------------------------- | ----------------------------------------------------------------------------------- |
| `findCells`    | `(wb, matcher, opts?)`                   | Find cells by value or pattern; `opts.in`, `context`, `limit`, `offset`, `formulas` |
| `findRows`     | `(wb, matcher, opts?)`                   | Find rows by value or pattern; `opts.in`, `context`, `limit`, `offset`              |
| `detectTables` | `(wb)`                                   | Auto-detect table-like regions                                                      |
| `tableLookup`  | `(wb, { table, rowLabel, columnLabel })` | Look up a value by row and column labels                                            |

`matcher` accepts: string, string array (OR match), number, boolean, RegExp, or RegExp array. Searches are fuzzy and case-insensitive by default.

**Tracing**

| Function            | Signature               | Description                                           |
| ------------------- | ----------------------- | ----------------------------------------------------- |
| `getCellPrecedents` | `(wb, address, depth?)` | Cells that feed into this cell; `depth` defaults to 1 |
| `getCellDependents` | `(wb, address, depth?)` | Cells that depend on this cell                        |
| `traceToInputs`     | `(wb, cell)`            | Trace all the way to leaf input cells (no formula)    |
| `traceToOutputs`    | `(wb, cell)`            | Trace all the way to terminal output cells            |

**Computing**

| Function           | Signature               | Description                                  |
| ------------------ | ----------------------- | -------------------------------------------- |
| `evaluateFormula`  | `(wb, sheet, formula)`  | Evaluate a formula string in a sheet context |
| `evaluateFormulas` | `(wb, sheet, formulas)` | Evaluate multiple formulas at once           |

**Validating**

| Function | Signature        | Description           |
| -------- | ---------------- | --------------------- |
| `lint`   | `(wb, options?)` | Find potential issues |

**Rendering**

| Function        | Signature     | Description                                                         |
| --------------- | ------------- | ------------------------------------------------------------------- |
| `previewStyles` | `(wb, range)` | Generate a PNG screenshot of a cell range; image is auto-registered |

**Writing (ephemeral)**

| Function                | Signature                    | Description                                                            |
| ----------------------- | ---------------------------- | ---------------------------------------------------------------------- |
| `setCells`              | `(wb, cells)`                | Write values/formulas to cells; returns `{ touched, changed, errors }` |
| `scaleRange`            | `(wb, range, factor, opts?)` | Multiply numeric cells by a factor; `opts.skipFormulas` (default true) |
| `insertRowAfter`        | `(wb, sheet, row, count?)`   | Insert rows after a given row                                          |
| `deleteRows`            | `(wb, sheet, row, count?)`   | Delete rows starting at a given row                                    |
| `insertColumnAfter`     | `(wb, sheet, col, count?)`   | Insert columns after a given column                                    |
| `deleteColumns`         | `(wb, sheet, col, count?)`   | Delete columns starting at a given column                              |
| `addSheet`              | `(wb, name)`                 | Add a new sheet                                                        |
| `deleteSheet`           | `(wb, name)`                 | Delete a sheet                                                         |
| `renameSheet`           | `(wb, oldName, newName)`     | Rename a sheet                                                         |
| `addDefinedName`        | `(wb, name, range, scope?)`  | Add a defined name                                                     |
| `setWorkbookProperties` | `(wb, properties)`           | Set workbook-level properties                                          |
| `setSheetProperties`    | `(wb, sheet, properties)`    | Set sheet-level properties (columns, rows, merges, view)               |
| `setStyle`              | `(wb, target, style)`        | Apply styles to a cell or range                                        |

### The ephemeral write contract

By default, `exec` **does not write workbook bytes back to disk**. All write operations (`setCells`, `scaleRange`, inserts, deletes) take effect in the server-side session only. The `result.touched` map contains the recalculated formatted text values — read answers from there.

This means:

- No risk of corrupting the original file
- No `reset()` needed — each invocation starts clean
- Multiple scenarios = multiple `exec` invocations

To persist changes back to the workbook file, pass the `--save` flag.

### setCells result shape

```ts
{
  touched: Record<string, string>  // address → formatted text value
  changed: string[]                // addresses whose values changed
  errors: Diagnostic[]             // cells that errored after recalc
}
```

Read the output value from `result.touched["Sheet!Address"]`. Never compute the answer in JavaScript.

### Circular reference convergence

When a workbook has **iterative calculation** enabled (circular references between
cells), `setCells` returns **partially-converged intermediate values** in
`result.touched` — this is expected and not an error. Do not try to debug or
"fix" these intermediate values.

To fully converge circular references after setting formulas, run:

```bash
witan xlsx calc model.xlsx --show-touched
```

This recalculates all formulas with iterative solving and saves the converged
values back to the file. After running calc, inspect the output to verify that
all cells have the expected values.

### Response format

When `--json` is used, the full response envelope is returned:

**Success:**

```json
{
  "ok": true,
  "stdout": "...",
  "result": "<json>",
  "writes_detected": false,
  "accesses": [...]
}
```

**Failure:**

```json
{
  "ok": false,
  "stdout": "...",
  "error": { "type": "...", "code": "...", "message": "..." }
}
```

The `accesses` array documents all cell reads and writes with operation type and address.

## render — Visual Screenshot

Renders a sheet range as a PNG image, useful for inspecting layout, merged cells, formatting, and labels.

```bash
# Render a range to a temporary file (path printed to stdout)
witan xlsx render report.xlsx -r "Sheet1!A1:Z50"

# Render to a specific output path
witan xlsx render report.xlsx -r "'My Sheet'!B5:H20" -o snapshot.png

# Higher resolution (DPR 1-3, default auto)
witan xlsx render report.xlsx -r "Sheet1!A1:F10" --dpr 2

# Diff against a baseline — highlights changes in a new PNG
witan xlsx render report.xlsx -r "Sheet1!A1:F10" --diff before.png
```

| Flag       | Short | Default | Description                                         |
| ---------- | ----- | ------- | --------------------------------------------------- |
| `--range`  | `-r`  | —       | Sheet-qualified range to render (**required**)      |
| `--output` | `-o`  | —       | Output path (default: temporary file)               |
| `--dpr`    |       | auto    | Device pixel ratio 1-3                              |
| `--format` |       | `png`   | Output format: `png` or `webp`                      |
| `--diff`   |       | —       | Compare against a baseline PNG and write diff image |

The `previewStyles` exec function (see Rendering in the API reference) provides the same capability from within a script.

## Error Guide

| Error                                                             | Fix                                                                       |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `exactly one of --code, --script, --stdin, or --expr is required` | Provide exactly one code source flag                                      |
| `--code, --script, --stdin, and --expr are mutually exclusive`    | Only use one code source flag per invocation                              |
| `exec code must not be empty`                                     | Provide non-empty code                                                    |
| `Import statements are not allowed`                               | No `import` in exec scripts; use the `xlsx` global                        |
| `EXEC_SYNTAX_ERROR`                                               | Fix JavaScript syntax in your script                                      |
| `EXEC_RUNTIME_ERROR`                                              | Fix runtime error (check the message for details)                         |
| `EXEC_RESULT_TOO_LARGE`                                           | Return less data; use `print()` for large output instead of return values |
| `--timeout-ms must be > 0`                                        | Omit the flag (no timeout) or provide a positive value                    |
| `invalid --input-json`                                            | Provide valid JSON                                                        |
| `Sheet 'X' not found`                                             | Check the sheet name; use `listSheets` to enumerate                       |
| Shell quoting errors with sheet names                             | Use `--stdin <<'WITAN'` heredoc — it avoids all shell quoting issues      |
| `findCells` returns empty                                         | Try synonym arrays, broader search, or check spelling                     |
| `setCells` result missing expected output                         | The output cell may not be a dependent; trace the formula chain           |

### Full Type Definitions

````ts
type CellAddressOrCoordinates =
  | string
  | {
      sheet: string;
      row: number;
      col: number | string;
    };
type RangeAddressOrCoordinates =
  | string
  | {
      sheet: string;
    }
  | {
      sheet: string;
      from: {
        row?: number;
        col?: number | string;
      };
      to: {
        row?: number;
        col?: number | string;
      };
    };
type VisibilityType = "visible" | "outsidePrintArea" | "collapsed" | "hidden";
interface SheetInfo {
  address: string;
  from: {
    row: number;
    col: number;
  };
  to: {
    row: number;
    col: number;
  };
  rows: number;
  cols: number;
  sheet: string;
  hidden?: boolean;
  printArea?: string;
}
interface WorkbookProperties {
  sheets: SheetInfo[];
  activeSheetIndex: number;
  defaultFont: {
    name: string;
    size: number;
  };
  metadata?: {
    author?: string;
    title?: string;
    subject?: string;
    company?: string;
    created?: string;
    modified?: string;
  };
  themeColors?: {
    dark1: string;
    light1: string;
    dark2: string;
    light2: string;
    accent1: string;
    accent2: string;
    accent3: string;
    accent4: string;
    accent5: string;
    accent6: string;
    hyperlink: string;
    followedHyperlink: string;
  };
}
/** Get workbook-level properties including sheets, theme, and metadata. */
function getWorkbookProperties(wb): Promise<WorkbookProperties>;
/**
 * Set workbook-level properties.
 * Supports partial updates - only specified properties are modified.
 */
function setWorkbookProperties(
  wb,
  properties: {
    activeSheetIndex?: number;
    defaultFont?: {
      name?: string;
      size?: number;
    };
    metadata?: {
      author?: string;
      title?: string;
      subject?: string;
      company?: string;
    };
    themeColors?: {
      dark1?: string;
      light1?: string;
      dark2?: string;
      light2?: string;
      accent1?: string;
      accent2?: string;
      accent3?: string;
      accent4?: string;
      accent5?: string;
      accent6?: string;
      hyperlink?: string;
      followedHyperlink?: string;
    };
  },
): Promise<void>;
/** List all sheets with their used ranges and visibility. */
function listSheets(wb): Promise<SheetInfo[]>;
/** Get the bounding range of non-empty cells in a sheet. */
function getUsedRange(wb, sheetName: string): Promise<SheetInfo>;
interface DefinedName {
  name: string;
  range: string;
  scope: string | null;
}
/** List all named ranges in the workbook. */
function listDefinedNames(wb): Promise<DefinedName[]>;
/** Create a named range, optionally scoped to a sheet. */
function addDefinedName(
  wb,
  name: string,
  range: string,
  scope?: string,
): Promise<DefinedName>;
/** Add a new worksheet to the workbook. */
function addSheet(wb, name: string): Promise<string>;
/** Remove a worksheet from the workbook. */
function deleteSheet(wb, name: string): Promise<void>;
/** Rename a worksheet. */
function renameSheet(wb, oldName: string, newName: string): Promise<void>;
interface Value {
  address: string;
  sheet: string;
  row: number;
  col: number;
  colLetter: string;
  value: string | number | boolean | null;
  formula?: string;
  type: "string" | "number" | "bool" | "date" | "error" | "blank";
  text: string;
  format?: string;
  /** Format-derived numeric classification (e.g., percent, currency). */
  numberType?:
    | "currency"
    | "percent"
    | "fraction"
    | "exponential"
    | "date"
    | "text"
    | "number";
  /** Cell visibility: visible, hidden, collapsed, or outsidePrintArea */
  visibility: VisibilityType;
  /** Self-locating TSV of surrounding cells when context was requested. */
  context?: string;
}
/** Read a single cell's value, formula, and metadata. */
function readCell(
  wb,
  cell: CellAddressOrCoordinates,
  opts?: {
    context?: number;
  },
): Promise<Value>;
/** Read a rectangular range of cells as a 2D array. */
function readRange(wb, range: RangeAddressOrCoordinates): Promise<Value[][]>;
/** Read all cells in a column within the used range. */
function readColumn(
  wb,
  sheetName: string,
  col: number | string,
  opts?: {
    startRow?: number;
    endRow?: number;
  },
): Promise<Value[]>;
/** Read all cells in a row within the used range. */
function readRow(
  wb,
  sheetName: string,
  row: number,
  opts?: {
    startCol?: number;
    endCol?: number;
  },
): Promise<Value[]>;
/** Read a range as tab-separated values with row/column headers. */
function readRangeTsv(
  wb,
  range: RangeAddressOrCoordinates,
  opts?: {
    includeEmpty?: boolean;
  },
): Promise<string>;
/** Read a column as tab-separated values. */
function readColumnTsv(
  wb,
  sheetName: string,
  col: number | string,
  opts?: {
    startRow?: number;
    endRow?: number;
    includeEmpty?: boolean;
  },
): Promise<string>;
/** Read a row as tab-separated values. */
function readRowTsv(
  wb,
  sheetName: string,
  row: number,
  opts?: {
    startCol?: number;
    endCol?: number;
    includeEmpty?: boolean;
  },
): Promise<string>;
declare class SearchResults<T> extends Array<T> {
  truncated?: boolean;
}
type MatcherInput = string | string[] | number | boolean | RegExp | RegExp[];
/**
 * Search for cells matching a value, substring, or regex pattern.
 * When `formulas` is true, matches against formulas instead of text/values;
 * cells without formulas are skipped.
 * Examples:
 * - text: findCells(wb, "Revenue")
 * - number: findCells(wb, 42)
 * - boolean: findCells(wb, true)
 * - text synonyms: findCells(wb, ["Rev", "Revenue"])
 * - regex: findCells(wb, /rev(enue)?/i)
 * - regex array: findCells(wb, [/invest/i, /sales/i]) // OR matching - matches if any regex matches
 * - formula search: findCells(wb, "SUM", { formulas: true })
 */
function findCells(
  wb,
  matcher: MatcherInput,
  opts?: {
    in?: RangeAddressOrCoordinates | string;
    context?: number;
    limit?: number;
    offset?: number;
    formulas?: boolean;
  },
): Promise<
  SearchResults<{
    type: "cell";
    address: string;
    value: any;
    text: string;
    formula?: string;
    row: number;
    col: number;
    colLetter: string;
    sheet: string;
    visibility: VisibilityType;
    context?: string;
    role: string;
  }>
>;
/** Search for rows containing a matching cell; returns full row data. */
function findRows(
  wb,
  matcher: MatcherInput,
  opts?: {
    in?: RangeAddressOrCoordinates | string;
    context?: number;
    limit?: number;
    offset?: number;
  },
): Promise<
  SearchResults<{
    type: "row";
    row: number;
    sheet: string;
    matchedAt: string;
    range: string;
    tsv: string;
    visibility: VisibilityType;
    context?: string;
  }>
>;
/** Detect tabular regions by analyzing header patterns across all sheets. */
function detectTables(wb): Promise<
  Record<
    string,
    {
      /** Full range covering the row headers + column headers + data rows */
      address: string;
      /** Top labels as TSV with addresses (format: ColRow|Value\tColRow|Value) */
      headerRows: string;
      /** Side labels as TSV with addresses (format: ColRow|Value\nColRow|Value), null when no row labels */
      headerCols: string | null;
      /** Excel table name for Data Tables, absent for heuristic-detected tables */
      tableName?: string;
    }
  >
>;
/**
 * Look up values in a table by row and column labels.
 *
 * Searches the first column for rowLabel and the first row for columnLabel,
 * returning all matching intersections sorted by match quality.
 */
function tableLookup(
  wb,
  args: {
    /** Range address for the table (eg. "Sheet1!A1:D10") */
    table: string;
    /** Row label to search for in the first column */
    rowLabel: string | number | boolean;
    /** Column label to search for in the first row */
    columnLabel: string | number | boolean;
  },
): Promise<
  {
    address: string;
    value: any;
    text: string;
    row: number;
    col: number;
    colLetter: string;
    sheet: string;
    visibility: VisibilityType;
    rowLabelFoundAt: string;
    /** Text of the cell that matched the row label */
    rowLabelFound: string;
    columnLabelFoundAt: string;
    /** Text of the cell that matched the column label */
    columnLabelFound: string;
  }[]
>;
interface Diagnostic {
  code: string;
  detail?: string;
  address: string;
  formula?: string;
}
interface InvalidatedTile {
  sheet: string;
  tileRow: number;
  tileCol: number;
}
interface UpdatedSheetInfo {
  name: string;
  usedRange: {
    startRow: number;
    startCol: number;
    endRow: number;
    endCol: number;
  } | null;
  tileRowCount: number;
  tileColCount: number;
}
interface SetCellsResult {
  /** Map of cell address to formatted text value */
  touched: Record<string, string>;
  /** Cell addresses whose values or formulas were changed by this operation */
  changed: string[];
  /** Cells that resulted in error values after calculation */
  errors: Diagnostic[];
  /** Tiles that need re-rendering */
  invalidatedTiles: InvalidatedTile[];
  /** Updated sheet metadata for affected sheets */
  updatedSheets: UpdatedSheetInfo[];
}
/** Write to one or more cells in a single operation. */
function setCells(
  wb,
  cells: Array<{
    address: CellAddressOrCoordinates;
    value?: unknown;
    formula?: string;
    format?: string;
  }>,
): Promise<SetCellsResult>;
/**
 * Multiply all numeric cells in a range by a scale factor.
 * Formula cells are skipped by default.
 */
function scaleRange(
  wb,
  range: RangeAddressOrCoordinates,
  factor: number,
  opts?: {
    skipFormulas?: boolean;
  },
): Promise<SetCellsResult | null>;
/** Insert one or more rows after the specified row. */
function insertRowAfter(
  wb,
  sheetName: string,
  row: number,
  count?: number,
): Promise<void>;
/** Delete one or more rows starting at the specified row. */
function deleteRows(
  wb,
  sheetName: string,
  row: number,
  count?: number,
): Promise<void>;
/** Insert one or more columns after the specified column. */
function insertColumnAfter(
  wb,
  sheetName: string,
  column: number | string,
  count?: number,
): Promise<void>;
/** Delete one or more columns starting at the specified column. */
function deleteColumns(
  wb,
  sheetName: string,
  column: number | string,
  count?: number,
): Promise<void>;
type RichTextRun = {
  text: string;
  style?: {
    name?: string;
    size?: number;
    color?: string;
    bold?: boolean;
    italic?: boolean;
    strike?: boolean;
    underline?: string;
    verticalAlign?: string;
  };
};
type StyleObj = {
  fill?: {
    color?: string;
    pattern?: string;
    patternColor?: string;
    gradient?: {
      type: string;
      degree?: number;
      color1: string;
      color2: string;
      top?: number;
      bottom?: number;
      left?: number;
      right?: number;
    };
  };
  font?: {
    name?: string;
    size?: number;
    color?: string;
    bold?: boolean;
    italic?: boolean;
    strike?: boolean;
    underline?: string;
    verticalAlign?: string;
  };
  alignment?: {
    horizontal?: string;
    vertical?: string;
    rotation?: number;
    wrapText?: boolean;
    shrinkToFit?: boolean;
    indent?: number;
  };
  border?: {
    top?: {
      style: string;
      color: string;
    };
    bottom?: {
      style: string;
      color: string;
    };
    left?: {
      style: string;
      color: string;
    };
    right?: {
      style: string;
      color: string;
    };
    diagonal?: {
      style: string;
      color?: string;
      up?: boolean;
      down?: boolean;
    };
  };
  numberFormat?: string;
  centerContinuousSpan?: number;
  richText?: RichTextRun[];
};
/** Get the style properties of a cell. */
function getStyle(wb, cell: CellAddressOrCoordinates): Promise<StyleObj>;
/**
 * Apply style properties to a cell or range.
 * Available fields: bold/italic/underline (booleans), color/background (hex strings),
 * align/valign (horizontal/vertical alignment), format (number format string),
 * border (thin|medium|thick), wrapText (boolean), fontSize/fontName, and indent (number).
 */
function setStyle(
  wb,
  target: CellAddressOrCoordinates | RangeAddressOrCoordinates,
  style: StyleObj,
): Promise<void>;
interface SheetProperties {
  view: {
    showGridLines: boolean;
    zoomScale: number;
  };
  format: {
    defaultRowHeight: number;
    defaultColWidth: number;
    font?: {
      name?: string;
      size?: number;
    } | null;
  };
  columns: Record<
    string,
    {
      col: string;
      width: number;
    }
  >;
  rows: Record<
    number,
    {
      row: number;
      height: number;
    }
  >;
  merges?: string[] | null;
}
/**
 * Set worksheet properties using a hierarchical structure.
 * Supports partial updates - only specified properties are modified.
 */
function setSheetProperties(
  wb,
  sheetName: string,
  properties: {
    view?: {
      showGridLines?: boolean;
      zoomScale?: number;
    };
    format?: {
      defaultRowHeight?: number;
      defaultColWidth?: number;
      font?: {
        name?: string;
        size?: number;
      };
    };
    columns?: Record<
      number | string,
      {
        width: number;
      }
    >;
    rows?: Record<
      number,
      {
        height: number;
      }
    >;
    merges?: string[];
  },
): Promise<void>;
/**
 * Get worksheet properties in a hierarchical structure.
 * Always includes sheet-wide defaults (view/format); columns/rows are returned
 * for the specified filters or for all known dimensions when no filters are provided.
 */
function getSheetProperties(
  wb,
  sheetName: string,
  filter?: {
    columns?: (number | string)[];
    rows?: number[];
  },
): Promise<SheetProperties>;
interface DependencyResult {
  cells: {
    address: string;
    depth: number;
    formula?: string;
    referenceType?: "direct" | "range" | "named" | "table";
  }[];
  warnings?: Diagnostic[];
}
/** Get cells that the given cell depends on (its precedents) */
function getCellPrecedents(
  wb,
  address: CellAddressOrCoordinates,
  depth?: number,
): Promise<DependencyResult>;
/**
 * Get cells that depend on the given cell (its dependents) */
function getCellDependents(
  wb,
  address: CellAddressOrCoordinates,
  depth?: number,
): Promise<DependencyResult>;
/** Trace backwards from a cell to find all input cells that feed into it */
function traceToInputs(
  wb,
  cell: CellAddressOrCoordinates,
): Promise<
  {
    address: string;
    referenceCount: number;
    text?: string;
    /** Label from adjacent cell, left or above (heuristic, may be incorrect) */
    nearbyLabel?: string;
    /** TSV of surrounding cells (only present when nearbyLabel is missing) */
    context?: string;
  }[]
>;
/** Trace forwards from a cell to find all output cells that depend on it */
function traceToOutputs(
  wb,
  cell: CellAddressOrCoordinates,
): Promise<
  {
    address: string;
    formula?: string;
    text?: string;
    visibility: VisibilityType;
    /** Label from adjacent cell, left or above (heuristic, may be incorrect) */
    nearbyLabel?: string;
    /** TSV of surrounding cells (only present when nearbyLabel is missing) */
    context?: string;
  }[]
>;
interface FormulaResult {
  formula: string;
  /** Computed value: number, string, boolean, null, 2D array, or error string */
  value: number | string | boolean | null | unknown[][];
  /** Error details if value is an error */
  error?: {
    code: string;
    detail?: string;
  };
}
/**
 * Evaluate multiple formulas in the context of a specific worksheet.
 * Useful for ad-hoc calculations; formulas are evaluated without modifying any cells.
 *
 * The `sheet` parameter specifies which worksheet the formulas are evaluated in.
 * This affects how unqualified cell references (like `A1`) and sheet-scoped
 * named ranges are resolved.
 *
 * @example
 * ```typescript
 * const results = await evaluateFormulas(wb, "Sheet1", [
 *   "=SUM(A1:A10)",           // Resolved as Sheet1!A1:A10
 *   "=AVERAGE(B:B)",          // Resolved as Sheet1!B:B
 *   "=MAX('Other Sheet'!C1:C100)", // Explicit sheet reference
 * ]);
 * ```
 */
function evaluateFormulas(
  wb,
  sheet: string,
  formulas: string[],
): Promise<FormulaResult[]>;
/**
 * Evaluate a single formula in the context of a specific worksheet.
 * Useful for ad-hoc calculations; the formula is evaluated without modifying any cells.
 *
 * The `sheet` parameter specifies which worksheet the formula is evaluated in.
 * This affects how unqualified cell references (like `A1`) and sheet-scoped
 * named ranges are resolved.
 *
 * @example
 * ```typescript
 * // Unqualified references resolved in Sheet1's context
 * const sum = await evaluateFormula(wb, "Sheet1", "=SUM(A1:A100)");
 * console.log(sum.value); // 1500
 *
 * // Named ranges resolved with sheet scope
 * const total = await evaluateFormula(wb, "Data", "=SUM(Revenue)");
 *
 * // Cross-sheet formulas work with explicit references
 * const diff = await evaluateFormula(wb, "Summary", "='Sheet1'!A1 - 'Sheet2'!A1");
 *
 * // Array formula result
 * const unique = await evaluateFormula(wb, "Sheet1", "=UNIQUE(A1:A10)");
 * console.log(unique.type); // "array"
 * console.log(unique.value); // [["Apple"], ["Banana"], ["Cherry"]]
 * ```
 */
function evaluateFormula(
  wb,
  sheet: string,
  formula: string,
): Promise<FormulaResult>;
/**
 * Lint the workbook to find potential issues and code smells.
 *
 * Returns diagnostics for issues like:
 * - Empty cell coercion (D003)
 * - Non-numeric values in aggregate functions (D005)
 * - Duplicate values in lookup arrays (D007)
 * - Spelling errors (D031)
 *
 * @example
 * ```typescript
 * // Get all diagnostics
 * const result = await lint(wb);
 * console.log(`Found ${result.total} issues`);
 * for (const diag of result.diagnostics) {
 *   console.log(`[${diag.severity}] ${diag.ruleId}: ${diag.message} at ${diag.location}`);
 * }
 *
 * // Lint only specific ranges
 * const rangeResult = await lint(wb, { rangeAddresses: ["Sheet1!A1:B10", "Sheet2!C1:C20"] });
 *
 * // Skip spelling checks
 * const warnings = await lint(wb, { skipRuleIds: ["D031"] });
 *
 * // Only check for empty cell coercion
 * const coercionIssues = await lint(wb, { onlyRuleIds: ["D003"] });
 * ```
 */
function lint(
  wb,
  options?: {
    /** Array of cell ranges to analyze (e.g., ["Sheet1!A1:B10", "Sheet2!C1:C20"]). If omitted, analyzes entire workbook. */
    rangeAddresses?: string[];
    /** Array of rule IDs to skip (e.g., ["D031"] to skip spelling checks) */
    skipRuleIds?: string[];
    /** Array of rule IDs to exclusively run (e.g., ["D003"] to only check empty cell coercion) */
    onlyRuleIds?: string[];
  },
): Promise<{
  diagnostics: {
    /** Severity level */
    severity: "Info" | "Warning" | "Error";
    /** Rule ID that generated this diagnostic (e.g., "D003") */
    ruleId: string;
    /** Human-readable description of the issue */
    message: string;
    /** Cell location where the issue was found (e.g., "Sheet1!A1"), or null for workbook-level issues */
    location: string | null;
    /** Visibility at the diagnostic location cell, or null for workbook-level issues */
    visibility: VisibilityType | null;
  }[];
  total: number;
}>;
/**
 * Generate a PNG screenshot of a specified cell range.
 */
function previewStyles(wb, range: RangeAddressOrCoordinates): Promise<void>;
````

## Scope

This skill is for reading and manipulating Excel spreadsheets (.xlsx, .xlsm) only. It does not handle non-spreadsheet documents (PDF, DOCX, PPTX, HTML, text).
