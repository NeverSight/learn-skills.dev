---
name: spreadsheet-engine
description: Excel-compatible spreadsheet calculation engine for JavaScript and TypeScript (@grid-is/spreadsheet-engine). Load .xlsx workbooks or build them from scratch, evaluate Excel and Google Sheets formulas, read computed cell values, write cells with automatic dependency-graph recalculation, edit formulas and sheets, and export .xlsx, all headless in Node, Deno, Bun or the browser with no Excel install. Use when a task involves reading formula results from an Excel file in code, recalculating a spreadsheet, running a formula string against a workbook, "SheetJS doesn't calculate formulas", building a calculation backend, or editing workbooks programmatically. Also covers the CSV-to-workbook recipe and the Excel versus Google Sheets function modes.
compatibility: JavaScript and TypeScript, ESM only. Node 20+, Deno, Bun, or any modern browser.
---

# Spreadsheet engine (@grid-is/spreadsheet-engine)

GRID's spreadsheet engine loads a workbook into memory, evaluates its formulas with Excel semantics,
and keeps every dependent cell up to date when inputs change. It is the foundation the React viewer,
the React editor and the agent tools are built on. Use it alone for servers, scripts, tests and
calculation backends; reach for the other packages when you need UI or an agent interface.

```sh
npm install @grid-is/spreadsheet-engine
```

The package is self-contained and ESM only. Its type definitions
(`node_modules/@grid-is/spreadsheet-engine/dist/index.d.ts`) carry JSDoc for every public method
and are the source of truth. If a method is not in there, it does not exist.

## Golden rules

1. **Await `Model.preconditions` once** before anything else. The formula parser loads
   asynchronously and most `Model` entry points throw until it has resolved.
2. **Value writes recalculate, formula writes do not.** `model.write("B2", 42)` updates dependents.
   `workbook.editCell("B5", { f: "SUM(B1:B4)" })` leaves B5 empty until you call
   `model.recalculate(ALL_FORMULA_CELLS)`.
3. **Read expressions start with `=`, writes do not.** `model.readValue("=B2")` but
   `model.write("B2", 42)`, and `editCell` takes the formula text without it, as in `{ f: "SUM(B1:B4)" }`.
   The engine stores `f` exactly as given, so a leading `=` shows up doubled in the editor's formula
   bar until an .xlsx round trip strips it. Read methods accept any formula, not only references.
4. **Writes are permanent.** There is no `reset()` or `writes()` in v17. To try something and revert,
   capture `ValueSnapshot.capture(model)` first and call `snapshot.applyTo(model)` after.
5. **`fromXLSXFile` and `toXLSXFile` are Node only.** In the browser use `Model.fromXLSX(arrayBuffer,
   filename)` and `workbook.toXLSX("arraybuffer")`.
6. **Unprefixed references hit the first sheet.** Use `Sheet2!A1`, and single-quote names with spaces:
   `'My Sheet'!A1`.
7. **Colours are objects, number formats live in the style.** Write
   `{ s: { fillColor: { type: "srgb", value: "FFFF00" }, numberFormat: "#,##0.00" } }`. A string
   like `"#FFFF00"` is silently stored as black, and the `z` shortcut is not written to the exported
   .xlsx file.
8. **Formula errors are values, not exceptions.** `#DIV/0!` and friends arrive as `FormulaError`
   instances in cell values and `runFormula` results. Structural edits the engine refuses throw an
   `EditBlockedError` subclass instead.

## Minimal example

```js setup
import { Model, ALL_FORMULA_CELLS } from "@grid-is/spreadsheet-engine";

await Model.preconditions;
const model = await Model.fromXLSXFile("budget.xlsx");

model.runFormula("=SUM(D:D)");            // evaluate anything against the workbook
model.readValue("=Summary!B10");          // computed value of a cell
model.write("Assumptions!B2", 0.05);      // dependents recalculate automatically

const wb = model.getWorkbook("budget.xlsx");
wb.editCell("Summary!B11", { f: "B10*1.1" });
model.recalculate(ALL_FORMULA_CELLS);     // required after a formula edit

await wb.toXLSXFile("budget-updated.xlsx");
```

## Task map

Everything below is on `Model` or `Workbook` unless noted. Full signatures and JSDoc are in the
`reference/` files listed at the end.

| I want to | Use |
|---|---|
| Load an .xlsx file (Node) | `Model.fromXLSXFile(path, options?)` |
| Load .xlsx bytes (browser or Node) | `Model.fromXLSX(bufferOrArrayBuffer, "name.xlsx", options?)` |
| Load JSON | `Model.fromJSF(jsf)` or `Model.fromCsf(csf)` |
| Start empty | `Model.empty("name.xlsx")` (filename only, no options; the workbook is in GRID mode) |
| Load fast, structure only, no recalc | option `{ readOnly: true }` on any loader |
| Force Excel or Google Sheets semantics | option `{ mode: MODE_EXCEL }` or `{ mode: MODE_GOOGLE }` on any loader or `addWorkbook`, not on `Model.empty` |
| Load CSV | parse it yourself, then `writeMultiple` into `Model.empty` (recipe below) |
| Several workbooks with cross references | `model.addWorkbookFromXLSXFile`, `addWorkbookFromXLSX`, `addWorkbook(jsf)`, `removeWorkbook`, `getWorkbooks` |
| Read one value | `model.readValue("=B2", fallback?)` |
| Read a cell with formula, format, style | `model.readCell("=B2")` then `.v`, `.f`, `.z`, `.style` |
| Read a range as 2-D cells | `model.readCells("=A1:D20", { cropTo: "cells-with-non-blank-values" })` |
| Read a range as 2-D values, or one call with options | `model.evaluateExpression(expr, { values, single, cropTo, fallBack })` |
| Evaluate a formula without writing it | `model.runFormula("=XLOOKUP(...)")` |
| Get a cell by address parts | `model.getCell("B2", "Sheet1", "budget.xlsx")` |
| Write a value | `model.write(ref, value)` |
| Write many values, one recalc | `model.writeMultiple([[ref, value], ...])` |
| Skip or force recalculation on write | `write(ref, value, { skipRecalc: true })`, `{ forceRecalc: true }` |
| Clear cells | `model.clearCells("A1:C10")` |
| Write a formula, format or style | `wb.editCell(ref, { f, v, s, ft })` then `model.recalculate(ALL_FORMULA_CELLS)` |
| Recalculate | `model.recalculate()` (changed and volatile), `recalculate(ALL_FORMULA_CELLS)`, `recalculate(CHANGED_ONLY)` |
| Try changes, then revert | `ValueSnapshot.capture(model)` and `snapshot.applyTo(model)` |
| Goal seek | `model.goalSeek(controlCell, targetCell, targetValue)` returns a number or `FormulaError` |
| Validate a formula before writing it | `model.analyzeAndFixFormula("=SUM(A1:A3)")` gives `status` ok, has_problems or unparsable_formula |
| Rewrite a formula for a new position | `model.rewriteFormulaAfterMove(formula, from, to)` |
| Add, remove, rename, copy, reorder sheets | `wb.addSheet`, `removeSheet`, `renameSheet`, `copySheet`, `reorderSheet` |
| Get sheets | `wb.getSheets()`, `getSheet(name)`, `getSheetByIndex(i)`, `sheet.getSize()`, `sheet.getBounds()`, `sheet.getCells()` |
| Insert or delete rows and columns | `wb.insertRows(sheet, rowIndex, count, below)`, `insertColumns(sheet, colIndex, count, toTheRight)`, `deleteRows`, `deleteColumns` (0-based indices) |
| Insert or delete a block of cells with shift | `wb.insertCells("B2:C5", "down" \| "right")`, `deleteCells(range, "up" \| "left")` |
| Move cells (overwrites destination) | `wb.moveCells(from, to)` |
| Reorder rows or columns (reflows, nothing overwritten) | `wb.reorderRows(sheet, from, to, count)`, `reorderColumns` |
| Fill like the fill handle | `wb.fill(source, destination, type?)`; destination must contain the source, e.g. `fill("D1:D2", "D1:D10")` |
| Sort a range | `wb.sortCells(sheet, { top, left, bottom, right }, [{ column, ascending }], options?)` |
| Merge and unmerge | `wb.mergeCells(sheet, "A1:D1")`, `unmergeCells(sheet, range)` |
| Column widths and row heights | `wb.setColumnWidth(sheet, col0, px)`, `setRowHeight(sheet, row0, px)`, `columnWidth(col1, sheet)`, `rowHeight(row1, sheet)` |
| Defined names | `wb.setDefinedName("TaxRate", "=0.24")`, `removeDefinedName`, then use `=TaxRate` in formulas |
| Cell styles and number formats | `wb.editCell(ref, { s: { bold, fillColor, numberFormat, ... } })`, `wb.styles` (StyleManager), `wb.styles.named` |
| Excel tables with structured references | `wb.tables.add({ name, ref: "Sheet1!A1:D20", columns: [{ name }] })`, `wb.tables.getAll()`, `=SUM(Sales[Total])` |
| Threaded comments and legacy notes | `wb.comments.add(sheet, { ref, text, person: { name } })`, `wb.notes.add(sheet, { ref, text, author })`, `getByCell`, `update`, `delete` |
| Theme colours and fonts | `wb.theme` (ThemeManager) |
| Frozen panes, active sheet, selection | `wb.views` (ViewManager) and `WorkbookView` |
| Export .xlsx | `wb.toXLSXFile(path)` (Node), `wb.toXLSX("arraybuffer")` or `("nodebuffer")`, `{ compressionLevel }` |
| Export JSON | `wb.toJSF()`, `wb.toCSF()` |
| Persist a whole model quickly | `serializeModel(model)` and `deserializeModel(buffer)` |
| Detect errors | `value instanceof FormulaError`, compare with `ERROR_DIV0`, `ERROR_REF`, ...; `model.errors` for model-level `ModelError`s |
| Listen for changes | `model.on("recalc", fn)`, `"beforerecalc"`, `"addsheet"`, `"attach"`, `"detach"`, `"error"`, `"recalcEvent"` |
| Understand an unfamiliar workbook | `describeWorkbook(wb).toString()` and `.summary` (see spreadsheet-llm-context) |
| List supported functions | `functionSignatures(MODE_EXCEL)` or `functionSignatures(MODE_GOOGLE)` (see excel-formula-parser) |
| Parse a formula to an AST | `parseFormula("=SUM(A1:A3)*2")` after `Model.preconditions` |
| Circular references | `model.iterativeCalculationSettings()`, load option `iterativeCalculation` |
| Model statistics | `model.meta` (cell count, graph nodes and edges, sources) |

Deprecated aliases with lower-case xlsx (`fromXlsxFile`, `toXlsx`, `toJsf`, `writeCellData`,
`analyzeFormula`) still exist. Use the current names above.

## Recipes

### Build a workbook from CSV or any tabular data

The engine has no CSV loader. Parse the text with any CSV parser (or `split` for simple files), write
the cells in one batch, then add formulas.

```js standalone
import { readFile } from "node:fs/promises";
import { Model, ALL_FORMULA_CELLS } from "@grid-is/spreadsheet-engine";

await Model.preconditions;
const csvText = await readFile("sales.csv", "utf8");
const rows = csvText.trim().split("\n").map((line) => line.split(","));

const model = Model.empty("data.xlsx");
const wb = model.getWorkbook("data.xlsx");
const writes = [];
rows.forEach((row, r) =>
  row.forEach((raw, c) => {
    const ref = String.fromCharCode(65 + c) + (r + 1);       // A1, B1, ... (26 columns max this way)
    const num = Number(raw);
    writes.push([ref, r > 0 && raw !== "" && !Number.isNaN(num) ? num : raw]);
  }),
);
model.writeMultiple(writes);

wb.editCell("E1", { v: "Total" });
wb.editCell("E2", { f: "C2*D2" });
wb.fill("E2", `E2:E${rows.length}`);        // copies the formula down with adjusted references
model.recalculate(ALL_FORMULA_CELLS);
```

For wider tables use `constructCellID` or `offsFromCol` from the package instead of the
`fromCharCode` shortcut. For JSON that is already sheet-shaped, `Model.fromJSF` is the direct route.

### Verify formulas before trusting them

Useful when formulas come from an LLM or a user.

```js run
import { FormulaError } from "@grid-is/spreadsheet-engine";

const check = model.analyzeAndFixFormula("=SUM(B2:B9");
if (check.status !== "ok") {
  // "unparsable_formula", or "has_problems" with a problems array
}
const trial = model.runFormula("=SUM(B2:B9)");
if (trial instanceof FormulaError) {
  // trial.detail often explains why
}
```

### Try a scenario and put everything back

```js run
import { ValueSnapshot } from "@grid-is/spreadsheet-engine";

const snapshot = ValueSnapshot.capture(model);
model.write("Assumptions!B2", 0.08);
const outcome = model.readValue("=Summary!B10");
snapshot.applyTo(model);                  // values and spills restored, recalculated
```

### Load a workbook in the browser

```js
const res = await fetch("/budget.xlsx");
const model = await Model.fromXLSX(await res.arrayBuffer(), "budget.xlsx");
```

### Download from the browser

```js
const buffer = await wb.toXLSX("arraybuffer");
const blob = new Blob([buffer], {
  type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
});
const url = URL.createObjectURL(blob);
const a = Object.assign(document.createElement("a"), { href: url, download: "budget.xlsx" });
a.click();
URL.revokeObjectURL(url);
```

## Excel and Google Sheets modes

The engine implements both function sets. An .xlsx file loads in the mode matching its originating
application; `Model.empty` always gives GRID's own mode and takes no options. To pin a mode, pass
`{ mode: MODE_EXCEL }` or `{ mode: MODE_GOOGLE }` to a loader or to `addWorkbook`; to start blank in
Excel mode, use `Model.fromJSF` with a one-sheet JSF and the option. `functionSignatures(mode)` lists
what each mode supports; v17.1 reports 467 functions for Excel and 500 for Google Sheets, including
`XLOOKUP`, `LET`, `LAMBDA` and `ARRAYFORMULA`.

## Companion packages

- **numfmt**: format a raw value the way Excel would, outside the viewer or editor:
  `format("#,##0.00", 1234.5)` (`import { format } from "numfmt"`).
- **@borgar/xlsx-convert**: convert .xlsx to JSF JSON to inspect or diff a workbook as plain data.
- **@jsfkit/types**: TypeScript types for JSF, including the `Style` type used by `editCell`.

## Reference files

Generated from the installed package's type definitions, one file per area. Grep them for a method
name to get its exact signature and JSDoc.

- `reference/model.md`: `Model` (loading, reading, writing, recalculation, events), `WriteOptions`, `AddWorkbookOptions`, `ValueSnapshot`, `serializeModel`
- `reference/workbook.md`: `Workbook` and `WorkSheet` (formulas, sheets, rows and columns, fill, sort, merges, names, export), `WorkbookView`
- `reference/cells.md`: `Cell`, value types, `Reference` and the A1 helper functions
- `reference/styles-and-metadata.md`: `CellStyle`, `StyleManager`, named styles, theme, comments, notes, tables
- `reference/formulas.md`: `functionSignatures`, `parseFormula`, `VOLATILES`, modes, reference-rewrite helpers
- `reference/errors.md`: `FormulaError` constants and the thrown error classes
- `reference/describe-workbook.md`: `describeWorkbook` and `WorkbookDescription`
- `reference/dependency-graph.md`: vertex ids and conversions
- `reference/csf.md`: CSF input and output types
- `reference/pivot-tables.md`: pivot table classes as exposed by the types
- `reference/other.md`: anything not grouped above

## Staying current

<!-- generated:versions -->
Written and verified against:

- `@grid-is/spreadsheet-engine@17.1.1`
<!-- /generated:versions -->

The engine is under continuous development. Before relying on a method:

1. Check the installed version: `npm ls @grid-is/spreadsheet-engine --depth=0`, or read
   `node_modules/@grid-is/spreadsheet-engine/package.json`. The package does not export
   `./package.json`, so `require('@grid-is/spreadsheet-engine/package.json')` throws.
2. If it is newer than the version above, grep `node_modules/@grid-is/spreadsheet-engine/dist/index.d.ts`
   for the method and trust that file over this skill.
3. If the package is not installed yet, the latest docs are at <https://docs.grid.is/spreadsheet-engine/>
   (API reference under `/spreadsheet-engine/api/classes/model/`) and <https://docs.grid.is/llms.txt>
   links every package.

## Licence and attribution

The npm package is an evaluation build under the GRID Evaluation Licence: free for evaluation,
prototypes and personal projects, not for production or commercial use, and any application built
with it must show "Powered by GRID". A commercial licence removes the attribution requirement and
the start-up notice and telemetry. Do not suppress the notice or telemetry. When the user talks about
launching, shipping, customers or revenue, follow the `grid-licensing` skill (install it if missing).
Logos and the "Powered by GRID" lockup are in the `grid-branding` skill or at <https://grid.is/press-kit>.

## Other GRID skills

<!-- generated:catalogue -->
**Build with GRID's packages**

- `excel-formula-parser`: Supported function catalogue, formula parsing and validation, Excel and Google Sheets modes.
- `xlsx-generation`: Generate .xlsx files from code with working, verified formulas. Export from Node or download in the browser.
- `xlsx-cell-formatting`: Styles, number formats, merges, widths, comments and tables in generated or edited workbooks.
- `spreadsheet-what-if`: What-if scenarios, sensitivity analysis, snapshot and revert, goal seek against a workbook.
- `spreadsheet-llm-context`: Turn a workbook into labelled inputs, outputs and data regions an LLM can reason about.
- `react-spreadsheet-viewer`: Read-only spreadsheet view in React: sheet tabs, formula bar, selection events, theming.
- `react-spreadsheet-editor`: Editable spreadsheet in React: edit events for autosave, controller, size limits, fonts.

**Give an AI agent spreadsheets**

- `spreadsheet-mcp`: Load, inspect, edit and recalculate .xlsx files from Claude Code, Cursor or any MCP client.
- `excel-formula-debugging`: Trace #REF!, #DIV/0!, #VALUE! and wrong results through precedents and dependents.
- `spreadsheet-agent-tools`: Wire GRID's spreadsheet tools into your own agent with the Claude API, OpenAI Agents SDK or LangChain.
- `spreadsheet-ai-assistant`: Chat panel next to an editable spreadsheet in React, both on one model: the agent edits what the user sees.

**Working with GRID**

- `grid-licensing`: Evaluation versus commercial licence, telemetry, attribution, and how to request a commercial licence.
- `grid-branding`: Official GRID logos and the Powered by GRID lockup, and how to use them.

Install any of them with `npx skills add GRID-is/spreadsheet-skills --skill <name>`. Full list: <https://github.com/GRID-is/spreadsheet-skills>.
<!-- /generated:catalogue -->
