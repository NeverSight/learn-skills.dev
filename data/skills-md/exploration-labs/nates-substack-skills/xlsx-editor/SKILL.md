---
name: xlsx-editor
description: Specialized guidance for editing EXISTING Excel files with emphasis on preserving formulas, formatting, and structure across multiple tabs. Use this skill when modifying, updating, or adding data to existing .xlsx files where maintaining integrity is critical—particularly for multi-tab workbooks, complex formulas, formatted tables, and data that must maintain sort order and relationships across sheets.
---

# Excel Editor - Editing Existing Files

## Overview

This skill provides specialized workflows for editing existing Excel files while preserving their integrity. It addresses the unique challenges of modifying live workbooks: maintaining formula relationships across tabs, preserving formatting and structure, ensuring data insertion maintains sort order, and guaranteeing completeness of multi-tab updates.

## When to Use This Skill

Use this skill when:
- Modifying existing Excel files (not creating new ones)
- Working with multi-tab workbooks where changes must cascade correctly
- Adding data that needs to integrate with existing tables while maintaining sort order
- Updating formulas that reference cells across multiple sheets
- Preserving complex formatting, merged cells, or conditional formatting
- Ensuring all related tables across tabs are updated completely

## Critical Principles for Editing Existing Files

### 1. Always Analyze Before Editing
Never dive directly into making changes. First understand the file's structure, dependencies, and relationships.

### 2. Preserve, Don't Replace
The existing file has established patterns. Maintain its structure, formulas, and formatting conventions rather than imposing new ones.

### 3. Multi-Tab Completeness is Mandatory
If data appears in multiple tabs, ALL instances must be updated. Missing one tab is a critical failure.

### 4. Validate Exhaustively
After edits, verify formulas, check for blank rows, confirm sort order, and ensure multi-tab consistency.

## Pre-Edit Analysis Workflow

**MANDATORY: Always perform this analysis before making any edits.**

```python
from openpyxl import load_workbook
import pandas as pd

# Load file without modifying it
wb = load_workbook('existing.xlsx', data_only=False)

# 1. INVENTORY ALL SHEETS
print("Sheets in workbook:", wb.sheetnames)
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"\n{sheet_name}:")
    print(f"  Dimensions: {sheet.dimensions}")
    print(f"  Max row: {sheet.max_row}, Max col: {sheet.max_column}")

# 2. IDENTIFY DATA STRUCTURES
# For each sheet, identify:
# - Table boundaries (first/last row and column)
# - Header rows
# - Sort keys (which columns determine order)
# - Merged cells
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"\nMerged cells in {sheet_name}:", list(sheet.merged_cells))

# 3. MAP FORMULAS AND DEPENDENCIES
# Find all formulas and note cross-sheet references
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    formulas = []
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                formulas.append({
                    'cell': cell.coordinate,
                    'formula': cell.value,
                    'cross_sheet': '!' in cell.value
                })
    if formulas:
        print(f"\n{sheet_name} has {len(formulas)} formulas")
        cross_sheet = [f for f in formulas if f['cross_sheet']]
        if cross_sheet:
            print(f"  {len(cross_sheet)} have cross-sheet references")
            for f in cross_sheet[:3]:  # Show first 3 examples
                print(f"    {f['cell']}: {f['formula']}")

# 4. UNDERSTAND SORT ORDER
# Read data to understand current ordering
for sheet_name in wb.sheetnames:
    df = pd.read_excel('existing.xlsx', sheet_name=sheet_name)
    if not df.empty:
        print(f"\n{sheet_name} current sort:")
        print(f"  First 5 rows of first column: {df.iloc[:5, 0].tolist()}")
        print(f"  Last 5 rows of first column: {df.iloc[-5:, 0].tolist()}")
```

**Document findings before proceeding:**
- Which sheets contain related data?
- What formulas reference other sheets?
- What determines sort order?
- Where are merged cells or complex formatting?
- What is the established naming/structure pattern?

## Core Editing Workflows

### Workflow 1: Updating Cell Values While Preserving Formulas

**Use case:** Changing data values without breaking formula dependencies.

```python
from openpyxl import load_workbook

# Load with formulas intact
wb = load_workbook('existing.xlsx', data_only=False)
sheet = wb['SheetName']

# CORRECT: Update value, preserve formula context
cell = sheet['A5']
if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
    print(f"WARNING: A5 contains formula: {cell.value}")
    print("Updating this will DELETE the formula. Proceed? (update dependent formulas instead)")
else:
    cell.value = new_value

# For cells with formulas, update the formula itself or its dependencies
sheet['B10'] = '=SUM(A1:A9)'  # Updates formula, preserving calculation logic

wb.save('existing.xlsx')
```

**Critical checks:**
- Verify you're not overwriting formula cells with values
- Check if other cells reference the cell you're updating
- Test a few formulas to ensure they still work after the change

### Workflow 2: Adding Rows While Maintaining Structure

**Use case:** Inserting new data into existing tables.

```python
from openpyxl import load_workbook
import pandas as pd

# 1. UNDERSTAND CURRENT STRUCTURE
df = pd.read_excel('existing.xlsx', sheet_name='Data')
# Identify sort key(s)
# Example: sorted by date (column A), then by category (column B)

# 2. DETERMINE INSERTION POINT
# Find where new row belongs in sort order
new_data = {'Date': '2024-06-15', 'Category': 'Sales', 'Amount': 1500}

insertion_row = None
for idx, row in df.iterrows():
    if row['Date'] > new_data['Date']:
        insertion_row = idx + 2  # +2 because: +1 for header, +1 for 1-based indexing
        break
if insertion_row is None:
    insertion_row = len(df) + 2  # Append at end

# 3. INSERT ROW
wb = load_workbook('existing.xlsx')
sheet = wb['Data']
sheet.insert_rows(insertion_row)

# 4. POPULATE WITH CORRECT STRUCTURE
# CRITICAL: Copy formatting from adjacent row
source_row = insertion_row - 1 if insertion_row > 2 else insertion_row + 1
for col in range(1, sheet.max_column + 1):
    # Copy formatting
    source_cell = sheet.cell(source_row, col)
    target_cell = sheet.cell(insertion_row, col)
    if source_cell.has_style:
        target_cell.font = source_cell.font.copy()
        target_cell.border = source_cell.border.copy()
        target_cell.fill = source_cell.fill.copy()
        target_cell.number_format = source_cell.number_format
        target_cell.alignment = source_cell.alignment.copy()

# 5. SET VALUES
sheet.cell(insertion_row, 1, new_data['Date'])
sheet.cell(insertion_row, 2, new_data['Category'])
sheet.cell(insertion_row, 3, new_data['Amount'])

# 6. UPDATE FORMULAS THAT REFERENCE THIS RANGE
# If there are SUM formulas like =SUM(A2:A100), they may need adjustment
# Check all sheets for formulas referencing this sheet
for ws_name in wb.sheetnames:
    ws = wb[ws_name]
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                if 'Data!' in cell.value:  # References the sheet we modified
                    print(f"REVIEW: {ws_name}!{cell.coordinate} formula may need adjustment: {cell.value}")

wb.save('existing.xlsx')
```

**Critical checks:**
- [ ] New row is in correct sort position
- [ ] Formatting matches surrounding rows
- [ ] No blank rows introduced
- [ ] Formulas referencing the range are still valid

### Workflow 3: Adding Columns While Preserving Formulas

**Use case:** Adding new data columns to existing tables.

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb['Data']

# 1. IDENTIFY INSERTION POINT
# Example: Insert after column C (before column D)
insert_col = 4  # Column D

# 2. INSERT COLUMN
sheet.insert_cols(insert_col)

# 3. COPY FORMATTING FROM ADJACENT COLUMN
source_col = insert_col - 1
for row_idx in range(1, sheet.max_row + 1):
    source_cell = sheet.cell(row_idx, source_col)
    target_cell = sheet.cell(row_idx, insert_col)
    if source_cell.has_style:
        target_cell.font = source_cell.font.copy()
        target_cell.border = source_cell.border.copy()
        target_cell.fill = source_cell.fill.copy()
        target_cell.number_format = source_cell.number_format
        target_cell.alignment = source_cell.alignment.copy()

# 4. SET HEADER
sheet.cell(1, insert_col, 'New Column Header')

# 5. ADD FORMULAS OR DATA
for row_idx in range(2, sheet.max_row + 1):
    # Example: Formula referencing other columns in same row
    sheet.cell(row_idx, insert_col, f'=B{row_idx}*C{row_idx}')

wb.save('existing.xlsx')
```

**Critical checks:**
- [ ] Formulas in other columns still reference correct cells
- [ ] Cross-sheet references are not broken
- [ ] Column widths are appropriate

### Workflow 4: Multi-Tab Data Updates (CRITICAL WORKFLOW)

**Use case:** Updating data that appears in multiple sheets (THE most common source of errors).

**THE PROBLEM:** When the same entity (customer, product, date, etc.) appears across multiple tabs, ALL instances must be updated. Missing even one tab creates data inconsistency.

**THE SOLUTION:** Systematic multi-tab update workflow.

```python
from openpyxl import load_workbook
import pandas as pd

# STEP 1: IDENTIFY ALL OCCURRENCES
# Find which sheets contain the data to be updated
target_value = "Customer X"  # Example: updating customer name
occurrences = {}

wb = load_workbook('existing.xlsx', data_only=True)  # Read values
for sheet_name in wb.sheetnames:
    df = pd.read_excel('existing.xlsx', sheet_name=sheet_name)
    
    # Search for target value in all cells
    found_locations = []
    for col in df.columns:
        mask = df[col].astype(str).str.contains(target_value, case=False, na=False)
        if mask.any():
            locations = df[mask].index.tolist()
            found_locations.extend([(col, idx+2) for idx in locations])  # +2 for header and 1-based
    
    if found_locations:
        occurrences[sheet_name] = found_locations
        print(f"Found '{target_value}' in {sheet_name}: {len(found_locations)} locations")

if not occurrences:
    print(f"ERROR: '{target_value}' not found in any sheet!")
else:
    print(f"\nTotal sheets containing '{target_value}': {len(occurrences)}")

# STEP 2: UPDATE ALL OCCURRENCES
wb = load_workbook('existing.xlsx', data_only=False)  # Now load with formulas

new_value = "Customer X - Updated"
update_count = 0

for sheet_name, locations in occurrences.items():
    sheet = wb[sheet_name]
    for col_name, row_idx in locations:
        # Convert column name to index
        df = pd.read_excel('existing.xlsx', sheet_name=sheet_name, nrows=0)
        col_idx = list(df.columns).index(col_name) + 1
        
        cell = sheet.cell(row_idx, col_idx)
        
        # Check if it's a formula
        if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
            print(f"WARNING: {sheet_name}!{cell.coordinate} is a formula. Skipping.")
        else:
            cell.value = new_value
            update_count += 1
            print(f"Updated {sheet_name}!{cell.coordinate}")

print(f"\nTotal cells updated: {update_count}")

# STEP 3: VERIFY ALL SHEETS WERE UPDATED
print("\nVerifying updates...")
wb.save('existing_updated.xlsx')
wb_verify = load_workbook('existing_updated.xlsx', data_only=True)

for sheet_name in wb_verify.sheetnames:
    df = pd.read_excel('existing_updated.xlsx', sheet_name=sheet_name)
    old_count = df.astype(str).apply(lambda x: x.str.contains(target_value, case=False, na=False)).sum().sum()
    new_count = df.astype(str).apply(lambda x: x.str.contains(new_value, case=False, na=False)).sum().sum()
    
    if old_count > 0:
        print(f"❌ {sheet_name}: Still has {old_count} instances of old value!")
    else:
        print(f"✅ {sheet_name}: All instances updated (found {new_count} new values)")
```

**Critical checks:**
- [ ] ALL sheets searched, not just obvious ones
- [ ] Update count matches expected number of occurrences
- [ ] Verification confirms zero instances of old value remain
- [ ] No formulas were accidentally overwritten

### Workflow 5: Cascading Formula Updates Across Tabs

**Use case:** Changing a formula that must be propagated to other sheets.

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')

# EXAMPLE: Update formula pattern across all sheets
# Old formula: =SUM(B2:B10)
# New formula: =SUMIF(B2:B10,">0")  # Only sum positive values

for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    
    changes_in_sheet = 0
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                if cell.value.startswith('=SUM(') and not 'SUMIF' in cell.value:
                    # Extract range from SUM formula
                    old_formula = cell.value
                    # Example: =SUM(B2:B10) -> =SUMIF(B2:B10,">0")
                    range_part = old_formula[5:-1]  # Extract "B2:B10"
                    new_formula = f'=SUMIF({range_part},">0")'
                    
                    cell.value = new_formula
                    changes_in_sheet += 1
                    print(f"{sheet_name}!{cell.coordinate}: {old_formula} -> {new_formula}")
    
    if changes_in_sheet > 0:
        print(f"  {sheet_name}: {changes_in_sheet} formulas updated")

wb.save('existing.xlsx')
```

**Critical checks:**
- [ ] Formula pattern correctly identified across all sheets
- [ ] New formula syntax is valid
- [ ] All sheets were checked (not just the first few)
- [ ] Edge cases handled (formulas with different ranges, nested functions)

### Workflow 6: Handling Merged Cells

**Use case:** Working with tables that have merged cells (common in headers/formatting).

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb['Data']

# 1. IDENTIFY MERGED CELLS
merged_ranges = list(sheet.merged_cells.ranges)
print(f"Found {len(merged_ranges)} merged cell ranges:")
for merged_range in merged_ranges:
    print(f"  {merged_range}")

# 2. WHEN INSERTING ROWS/COLUMNS NEAR MERGED CELLS
# Merged cells will NOT expand automatically. Must handle manually.

# Example: Inserting row in middle of merged region
insert_row = 5

# Check if insertion point is in a merged range
for merged_range in merged_ranges:
    if merged_range.min_row <= insert_row <= merged_range.max_row:
        print(f"WARNING: Row {insert_row} is within merged range {merged_range}")
        print("Unmerging, inserting, then re-merging with expanded range")
        
        # Unmerge
        sheet.unmerge_cells(str(merged_range))
        
        # Insert row
        sheet.insert_rows(insert_row)
        
        # Re-merge with expanded range
        new_range = f"{merged_range.min_col}{merged_range.min_row}:{merged_range.max_col}{merged_range.max_row+1}"
        sheet.merge_cells(new_range)

wb.save('existing.xlsx')
```

**Critical checks:**
- [ ] Merged cells are preserved or appropriately expanded
- [ ] Values in merged cells are maintained
- [ ] Formatting of merged cells is preserved

## Post-Edit Validation Checklist

**MANDATORY: Complete this checklist after ANY edits.**

### 1. Formula Integrity Check

```python
# Run recalc.py to identify formula errors
import subprocess
import json

result = subprocess.run(['python', 'recalc.py', 'existing.xlsx'], 
                       capture_output=True, text=True)
recalc_result = json.loads(result.stdout)

if recalc_result['status'] == 'errors_found':
    print(f"❌ ERRORS FOUND: {recalc_result['total_errors']} formula errors")
    for error_type, details in recalc_result['error_summary'].items():
        print(f"\n{error_type}: {details['count']} occurrences")
        for location in details['locations'][:5]:  # Show first 5
            print(f"  - {location}")
else:
    print("✅ All formulas calculated successfully (zero errors)")
```

- [ ] Zero formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- [ ] All formulas return expected values
- [ ] Cross-sheet references still work

### 2. Structural Integrity Check

```python
from openpyxl import load_workbook
import pandas as pd

wb = load_workbook('existing.xlsx')

# Check for blank rows in data tables
for sheet_name in wb.sheetnames:
    df = pd.read_excel('existing.xlsx', sheet_name=sheet_name)
    
    # Identify blank rows (all NaN)
    blank_rows = df[df.isnull().all(axis=1)]
    if not blank_rows.empty and len(blank_rows) > 0:
        print(f"⚠️  {sheet_name}: Found {len(blank_rows)} blank rows at indices: {blank_rows.index.tolist()}")
    
    # Check for unexpected blank cells in key columns (first column)
    if not df.empty and len(df.columns) > 0:
        blank_cells = df[df.iloc[:, 0].isnull()]
        if not blank_cells.empty and len(blank_cells) > 0:
            print(f"⚠️  {sheet_name}: First column has {len(blank_cells)} blank cells")
```

- [ ] No unexpected blank rows in data tables
- [ ] No blank cells in key identifier columns
- [ ] Table boundaries are clean (no trailing empty rows/columns)

### 3. Sort Order Verification

```python
# Verify data maintains expected sort order
df = pd.read_excel('existing.xlsx', sheet_name='Data')

# Example: Should be sorted by Date ascending, then Category ascending
expected_sort_cols = ['Date', 'Category']

# Check if sorted
is_sorted = df[expected_sort_cols].equals(df[expected_sort_cols].sort_values(expected_sort_cols))

if is_sorted:
    print("✅ Data is in correct sort order")
else:
    print("❌ Data is NOT sorted correctly")
    print("First 10 rows of sort columns:")
    print(df[expected_sort_cols].head(10))
```

- [ ] Data maintains expected sort order
- [ ] New rows inserted at correct position
- [ ] Sort keys (if any) are consistent

### 4. Multi-Tab Consistency Check

```python
# Verify related data is consistent across tabs

# Example: Check that customer names are consistent across Summary and Detail sheets
df_summary = pd.read_excel('existing.xlsx', sheet_name='Summary')
df_detail = pd.read_excel('existing.xlsx', sheet_name='Detail')

customers_summary = set(df_summary['Customer'].dropna().unique())
customers_detail = set(df_detail['Customer'].dropna().unique())

in_summary_not_detail = customers_summary - customers_detail
in_detail_not_summary = customers_detail - customers_summary

if in_summary_not_detail:
    print(f"⚠️  Customers in Summary but not Detail: {in_summary_not_detail}")
if in_detail_not_summary:
    print(f"⚠️  Customers in Detail but not Summary: {in_detail_not_summary}")

if not in_summary_not_detail and not in_detail_not_summary:
    print("✅ Customer lists are consistent across tabs")
```

- [ ] Related data exists in ALL expected sheets
- [ ] Counts/totals are consistent across sheets
- [ ] No orphaned data (exists in one sheet but not related sheets)

### 5. Formatting Preservation Check

```python
# Visual inspection is often needed for formatting
# But can programmatically check some basics

from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb['Data']

# Check that new rows have formatting
for row_idx in [5, 10, 15]:  # Example rows you inserted
    cell = sheet.cell(row_idx, 1)
    has_font = cell.font is not None and cell.font != sheet.cell(1, 1).font
    has_fill = cell.fill is not None and cell.fill.start_color.index != '00000000'
    
    print(f"Row {row_idx}: Font={has_font}, Fill={has_fill}")
```

- [ ] New rows/columns match formatting of surrounding cells
- [ ] Borders are continuous (no breaks in table borders)
- [ ] Merged cells are intact
- [ ] Conditional formatting still applies correctly

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Incomplete Multi-Tab Updates

**Problem:** Updating data in Sheet1 but forgetting it also appears in Sheet2 and Sheet3.

**Solution:** Always search ALL sheets before updating. Use the Multi-Tab Data Updates workflow.

**Prevention:**
```python
# Before ANY update, run this search
search_term = "value_to_update"
for sheet_name in wb.sheetnames:
    df = pd.read_excel('file.xlsx', sheet_name=sheet_name)
    found = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any().any()
    if found:
        print(f"'{search_term}' found in {sheet_name}")
```

### Pitfall 2: Breaking Formulas When Inserting Rows

**Problem:** Inserting a row causes formulas like =SUM(A2:A10) to break or not include the new row.

**Solution:** After inserting rows, check if range-based formulas need adjustment.

**Prevention:**
- Insert rows WITHIN existing ranges (not before or after)
- Use entire column references when possible: =SUM(A:A) instead of =SUM(A2:A10)
- After insertion, verify formula ranges programmatically

### Pitfall 3: Inserting Data Out of Sort Order

**Problem:** New row appears at the end instead of in alphabetical/chronological order.

**Solution:** Always determine the correct insertion point based on sort keys BEFORE inserting.

**Prevention:**
```python
# Determine insertion point based on sort logic
insertion_row = None
for idx, row in df.iterrows():
    if should_come_before(new_data, row):  # Define your comparison logic
        insertion_row = idx + 2
        break
```

### Pitfall 4: Introducing Blank Rows

**Problem:** Editing operations create unexpected blank rows in tables.

**Solution:** Never use append() for mid-table insertions. Always use insert_rows() with calculated position.

**Prevention:** Always run blank row check in post-edit validation.

### Pitfall 5: Overwriting Formulas with Values

**Problem:** Updating a cell that contains a formula, replacing it with a hardcoded value.

**Solution:** Always check if cell contains a formula before updating.

**Prevention:**
```python
if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
    raise ValueError(f"{cell.coordinate} contains formula. Cannot overwrite with value.")
```

### Pitfall 6: Not Recalculating After Formula Changes

**Problem:** Formulas are updated but values shown are stale (from before the edit).

**Solution:** ALWAYS run recalc.py after any formula modifications.

**Prevention:** Make recalc.py part of your standard workflow. Never skip it.

### Pitfall 7: Losing Formatting on New Rows/Columns

**Problem:** New rows have default formatting instead of matching the table style.

**Solution:** Always copy formatting from adjacent rows/columns.

**Prevention:** Use the formatting copy code from Workflow 2 and 3 above.

## Summary: Editing Workflow Template

For any editing task, follow this sequence:

1. **Analyze** (Pre-Edit Analysis Workflow)
   - Map all sheets
   - Identify dependencies
   - Document structure

2. **Plan**
   - Determine which sheets need changes
   - Identify formula impacts
   - Calculate insertion points

3. **Execute**
   - Use appropriate workflow
   - Update ALL relevant sheets
   - Preserve formatting

4. **Validate** (Post-Edit Validation Checklist)
   - Check formulas (zero errors)
   - Verify structure (no blank rows)
   - Confirm sort order
   - Ensure multi-tab consistency
   - Validate formatting

5. **Recalculate**
   - Run recalc.py
   - Fix any errors found
   - Run recalc.py again until zero errors

**Never skip steps.** Each step catches different classes of errors.
