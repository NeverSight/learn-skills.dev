---
name: excel-vba-workbook-engineering
description: Use when creating, modifying, or debugging .xlsx/.xlsm/.xlsb/.xls workbooks, VBA modules, macros, buttons, formulas, links, Power Query, or Excel COM/OpenXML automation.
---

# Excel VBA Workbook Engineering

## Core Rule

Treat Excel/VBA work as a binary-artifact engineering task. Inspect the workbook first, edit a copy unless the user explicitly asks otherwise, keep VBA source diffable outside the workbook, then verify by reopening the workbook and running the relevant macros or formula checks.

## Decision Path

1. **Windows desktop Excel available**: Use Excel COM automation for the highest-fidelity workflow. From PowerShell call the `.ps1` scripts directly. From Git Bash call `scripts/invoke_excel_com.sh`, which converts paths and invokes PowerShell.
2. **Linux/macOS or no Excel COM**: Use OpenXML inspection and workbook libraries for `.xlsx`/`.xlsm` structure, formulas, styles, and data. Use `scripts/inspect_openxml.py` for a cross-platform JSON inventory. Do not claim that VBA can be compiled, buttons can be fully validated, Solver can run, or Power Query/data model can refresh without Excel.
3. **Workbook without VBA**: Prefer structured workbook tools or Python/JS libraries for `.xlsx` analysis, formula inspection, formatting, and data extraction.
4. **Workbook with VBA or buttons**: Export VBA components before editing when Excel COM is available. On Linux/macOS, preserve `vbaProject.bin` when editing `.xlsm`, but route final VBA import/compile/run validation to Windows Excel unless the user explicitly accepts manual validation.
5. **Workbook depends on Excel-only features**: Use live Excel for Solver, Power Query refresh, cube formulas, data model, macro buttons, chart objects, ActiveX/Form controls, hidden/very hidden sheets, and legacy `.xls`.
6. **VBA project access is blocked**: Tell the user that Excel's "Trust access to the VBA project object model" setting is required for automated export/import. Continue with manual instructions or workbook-level non-VBA edits if possible.

## Platform Matrix

| Environment | Best path | Can inspect | Can edit workbook | Can import/export VBA | Can compile/run VBA |
|---|---|---:|---:|---:|---:|
| Windows PowerShell + desktop Excel | Excel COM scripts | yes | yes | yes | yes |
| Windows Git Bash + desktop Excel | `invoke_excel_com.sh` wrapper | yes | yes | yes | yes |
| Linux/macOS without Excel | OpenXML/Python/library path | partial | yes for `.xlsx`/some `.xlsm` edits | no automated VBE export/import | no |
| Linux/macOS with LibreOffice | LibreOffice/library path | partial | partial | no VBE-compatible import/export | no reliable Excel VBA validation |

## Required Workflow

1. **Inventory**
   - Record the input workbook path, file type, and whether it contains macros.
   - List sheets, visible state, used ranges, formulas, names, shapes/buttons with `OnAction`, links, queries, and connections.
   - If macros exist, export VBA components to a source folder before changing anything.
   - Use `scripts/inspect_workbook.ps1` or `scripts/invoke_excel_com.sh inspect` when Windows Excel is installed.
   - Use `scripts/inspect_openxml.py` when running on Linux/macOS or when Excel is unavailable.

2. **Plan the workbook shape**
   - Decide which sheets are user-facing, calculation/support, hidden, or deleted.
   - Decide which cells are inputs, formulas, outputs, and diagnostics.
   - Keep user-facing sheets clean; hide support sheets only after validation.
   - Preserve existing visual conventions unless the user asks for redesign.

3. **Edit safely**
   - Work on a copy by default. Never overwrite the only source workbook.
   - Use `.xlsm` for macro-enabled deliverables. Saving as `.xlsx` strips VBA.
   - Keep VBA in exported `.bas`, `.cls`, or `.frm` files under a source folder.
   - Use `Option Explicit`, clear public macro entry points, and late binding when references may be missing on another machine.
   - Do not paste exported `Attribute VB_Name = "..."`
     lines directly into the VBE code pane; those lines are valid in exported files, not manual paste text.

4. **Bind UI**
   - Prefer Form Control buttons or shapes with `.OnAction = "MacroName"` for simple workbooks.
   - Ensure the target macro is `Public Sub MacroName()` in a standard module.
   - When a deliverable depends on buttons, use the package-level `tools/build_vba_button_binding_report.py` with workbook inventory JSON and `lint_vba_source.py` JSON to statically catch stale or missing `OnAction` macros before handoff.
   - Avoid ActiveX controls unless the workbook already uses them or the user requires them.

5. **Validate**
   - Reopen the saved copy in Excel.
   - Compile VBA or run at least one representative macro.
   - Verify key output cells, formula errors, constraints, totals, and formatting.
   - For workbook deliverables with formulas, use package-level `tools/build_formula_quality_report.py` with OpenXML inspection JSON to flag cached formula errors, `#REF!`, local path references, volatile functions, and dynamic references before final handoff.
   - Use package-level `tools/build_workbook_controls_report.py` with OpenXML inspection JSON to review hidden/very hidden sheets, workbook protection, sheet protection, filters, frozen panes, and data validation rules before handoff.
   - Use package-level `tools/build_external_dependency_report.py` with OpenXML inspection JSON before static or client handoff to flag workbook connections, external links, external formulas, defined names, mashup/model markers, and credential-like connection string indicators without printing connection secrets.
   - Check that hidden sheets, links, queries, and buttons are in the intended final state.
   - Save a short validation note or test output when the workbook is a deliverable.
   - If working on Linux/macOS, state which validations were structural only and which still require Excel on Windows or Mac.
   - For package maintenance, the full release gate creates a temporary `.xlsx` workbook and validates `scripts/inspect_workbook.ps1` against live Excel COM inventory fields: worksheet, formula count, workbook name, button shape, `OnAction`, and named range.
   - The full release gate also imports a temporary VBA module into a `.xlsm`, runs the imported macro, and exports the module back out to prove the live import/run/export path. The structural release gate intentionally skips these Excel runtime fixtures.
   - The release gate runs a static formula quality fixture so cached errors, `#REF!`, local paths, volatile functions, and dynamic references are covered without customer workbooks.
   - The release gate runs a static workbook controls fixture so hidden/very hidden sheets, workbook/sheet protection, filters, frozen panes, and data validation are covered without customer workbooks.
   - The release gate runs a static external dependency fixture so workbook connections, link parts, external formulas/names, mashup markers, and redacted credential-like connection string indicators are covered without customer workbooks.
   - The release gate also cross-checks generic button `OnAction` values against public VBA source entries so static button-to-macro binding drift is covered in both full and structural profiles.

## VBA Source Discipline

Use this source layout for nontrivial VBA work:

```text
project/
  deliverables/
    workbook_name.xlsm
  src/
    vba/
      modMain.bas
      modHelpers.bas
      ThisWorkbook.cls
  docs/
    validation.md
```

Use `scripts/export_vba.ps1` to export modules from an existing workbook. Use `scripts/import_vba.ps1` to import standard/class/form modules into a workbook copy. From Git Bash, use `scripts/invoke_excel_com.sh export` and `scripts/invoke_excel_com.sh import`. Read `references/vba-patterns.md` before writing or replacing VBA.

## Excel COM Safety

- Start hidden Excel instances with `Visible = $false` and `DisplayAlerts = $false`.
- Always close workbooks and quit the COM Excel instance in `finally`.
- Release COM objects where practical.
- Do not kill all `EXCEL.EXE` processes. The user may have visible workbooks open. Only stop a process you created and can identify.
- Do not use destructive shell operations to move/delete workbook folders without verifying resolved paths.

## Encoding And Localization

- VBA exported by the VBE is not a reliable UTF-8 interchange format on every Windows machine.
- Prefer ASCII VBA module source when possible. For Chinese sheet names or labels, either reference existing worksheet objects, use values read from the workbook, or build literals with `ChrW$`.
- If Chinese literals are necessary, import and reopen the workbook to verify they survived.
- In terminal validation, avoid relying only on displayed Chinese text because console encoding may garble it. Verify through counts, formulas, cell addresses, and numeric values too.

## References

Load only the reference needed for the task:

- `references/workflow.md`: detailed workbook/VBA workflow, validation checklist, and troubleshooting.
- `references/vba-patterns.md`: VBA coding patterns, macro button binding, Solver/automation notes, and common compile/runtime fixes.

## Scripts

- `scripts/inspect_workbook.ps1 -WorkbookPath <path> [-OutJson <path>]`
  creates a JSON inventory through Excel COM.
- `scripts/invoke_excel_com.sh inspect|export|import ...`
  runs the Excel COM scripts from Git Bash/MSYS/Cygwin on Windows.
- `scripts/inspect_openxml.py <workbook> [--out-json <path>]`
  creates a cross-platform OpenXML inventory for `.xlsx`/`.xlsm` without Excel.
- `scripts/export_vba.ps1 -WorkbookPath <path> -OutDir <folder>`
  exports VBA components for review/editing.
- `scripts/import_vba.ps1 -WorkbookPath <path> -SourceDir <folder> -OutputWorkbookPath <path>`
  copies a workbook and imports VBA modules from a source folder.
- `scripts/lint_vba_source.py <source-dir> [--strict-option-explicit] [--out-json <path>]`
  statically checks exported or drafted `.bas`, `.cls`, and `.frm` files for parseable procedure blocks, duplicate public standard-module entry points, and missing `Option Explicit` before import.

These scripts are helpers, not substitutes for judgment. Read or patch them when a workbook has special requirements.
