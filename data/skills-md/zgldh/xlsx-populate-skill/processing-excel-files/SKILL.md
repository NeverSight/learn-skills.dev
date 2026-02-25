---
name: processing-excel-files
description: Edit and create Excel (.xlsx) files while preserving original formatting, merged cells, and styles. Use when working with Excel files, spreadsheets, .xlsx files, or when the user mentions editing Excel without destroying formatting.
version: 2.0.0
license: MIT
tags: [excel, xlsx, spreadsheet, office, data-processing, formatting]
---

# Processing Excel Files

Edit and manipulate Excel files using the xlsx-populate library while perfectly preserving original formatting.

## When to Use

- User wants to edit existing Excel files without destroying formatting
- Working with .xlsx files that have complex layouts or merged cells
- Need to add formulas, styling, or new worksheets to existing files
- Creating Excel reports from templates

## When NOT to Use

- Only need to read data from Excel (use `xlsx` library instead for better performance)
- Creating simple Excel files from scratch without formatting concerns

## Quick Start

```javascript
const XlsxPopulate = require('xlsx-populate');

// Load and edit
const workbook = await XlsxPopulate.fromFileAsync('input.xlsx');
workbook.sheet(0).cell('A1').value('Updated');
await workbook.toFileAsync('output.xlsx');
```

## Installation

```bash
npm install xlsx-populate
```

## Core Operations

### 1. Load and Preserve Formatting

```javascript
const workbook = await XlsxPopulate.fromFileAsync('file.xlsx');
const sheet = workbook.sheet(0);

// All original formatting is preserved automatically
sheet.cell('A1').value('New Value');
await workbook.toFileAsync('output.xlsx');
```

### 2. Add Formulas

```javascript
// Use formulas, not hardcoded values
sheet.cell('D10').formula('=SUM(D2:D9)');
sheet.cell('E5').formula('=(C5-B5)/B5');  // Growth rate
```

### 3. Apply Styles

```javascript
sheet.cell('A1').style({
  bold: true,
  fontSize: 14,
  fill: '4472C4',
  fontColor: 'FFFFFF'
});
```

### 4. Manage Worksheets

```javascript
// Add new sheet
const newSheet = workbook.addSheet('Summary');

// Reorder sheets
workbook.sheets()[2].move(0);

// Rename sheet
workbook.sheet(0).name('Cover Page');
```

### 5. Merge Cells

```javascript
sheet.range('A1:D1').merged(true);
sheet.range('A1:D1').style({
  horizontalAlignment: 'center'
});
```

## Advanced Patterns

**Batch Data Writing**: See [BATCH-OPERATIONS.md] for large dataset handling
**Formula Patterns**: See [FORMULAS.md] for financial modeling standards  
**Style Guide**: See [STYLES.md] for color schemes and formatting
**Complete Examples**: See [EXAMPLES.md] for real-world scenarios

## Best Practices

1. **Always preserve originals**: Never overwrite source files
   ```javascript
   await workbook.toFileAsync('output.xlsx');  // ✅ New file
   // NOT: await workbook.toFileAsync('input.xlsx');  // ❌ Don't overwrite
   ```

2. **Use formulas for calculations**: Let Excel do the math
   ```javascript
   sheet.cell('B10').formula('=SUM(B2:B9)');  // ✅
   // NOT: sheet.cell('B10').value(calculateSum());  // ❌
   ```

3. **Handle errors gracefully**:
   ```javascript
   try {
     const workbook = await XlsxPopulate.fromFileAsync('file.xlsx');
     // ... operations
     await workbook.toFileAsync('output.xlsx');
   } catch (error) {
     console.error('Excel operation failed:', error.message);
   }
   ```

## Common Issues

**Q: File size increased significantly?**  
A: Normal - xlsx-populate preserves more metadata. Use `xlsx` library if file size is critical.

**Q: Formulas not calculating?**  
A: Formulas are preserved but calculated when opened in Excel. Use `data_only=True` to read calculated values.

**Q: How to check merged cells?**  
A: `const merges = sheet._mergeCells;`

## Reference

- [xlsx-populate GitHub](https://github.com/dtjohnson/xlsx-populate)
- Library documentation: `node_modules/xlsx-populate/docs/`
