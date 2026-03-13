---
name: excel-na-utils
description: Helper functions for NA/missing value handling in Excel data. Provides Python and VBA implementations following CLAUDE.md NA handling guidelines.
---

# Excel NA Utils Skill

> NA/missing value helper functions for Excel data processing

## Overview

Consistent NA handling across Python and VBA based on CLAUDE.md guidelines:
- Treat empty cells, #N/A, "NA", "N/A" as missing values
- Exclude from numeric aggregates (mean, SD, min, max)
- Track excluded value counts for auditing
- Works with both Python and VBA

## When to Use

- **Python**: Analyzing Excel data with polars/pandas
- **VBA**: Building summary macros with NA filtering
- **Statistics**: Computing aggregates while excluding NA
- **Validation**: Identifying and counting missing data
- **Auditing**: Track excluded value counts

## Python API

```python
from na_helpers import is_na, filter_na, na_ratio, numeric_only

# Check if single value is NA
is_na(None)           # True
is_na("")             # True
is_na("NA")           # True
is_na("#N/A")         # True
is_na(1.5)            # False

# Filter NA from list
data = [1, 2, None, "NA", 3, "#N/A"]
clean = filter_na(data)  # [1, 2, 3]

# Calculate NA ratio
ratio = na_ratio(data)  # 0.5 (3 out of 6)

# Extract only numeric values (after NA filtering)
numbers = numeric_only(data)  # [1, 2, 3]
```

## VBA Templates

```vba
' Check if value is NA
If Not IsNA(cellValue) And IsNumeric(cellValue) Then
    ' Use value for calculation
    AddNumeric arr, n, cellValue
End If

' IsNA function checks:
' - Empty cells
' - Error values (#N/A, #DIV/0!, etc.)
' - Text markers ("NA", "N/A", "na", "n/a")

' AddNumeric adds to array only if not NA
' Result: clean array of valid numbers only
```

## NA Value Definitions

These are treated as missing values:

| Type | Examples | Handling |
|------|----------|----------|
| Empty | `` (blank cell) | Excluded |
| Error | `#N/A`, `#DIV/0!` | Excluded |
| Text markers | `"NA"`, `"N/A"`, `"na"` | Excluded (case-insensitive, trimmed) |

## Output

Functions return:
- **is_na()**: bool
- **filter_na()**: list of non-NA values
- **na_ratio()**: float (0.0-1.0)
- **numeric_only()**: list of numeric values

With auditing:
- Count of excluded NA values
- Count of remaining valid values
- NA ratio for reporting

## Integration

### Python + Excel

```python
from na_helpers import filter_na, na_ratio

# Read from Excel, filter NA
data = [cell.value for cell in range]
clean = filter_na(data)
n_excluded = len(data) - len(clean)

# Report N and exclusions
print(f"N: {len(clean)} (excluded: {n_excluded})")
```

### VBA (in vba.md)

```vba
' Module2 already implements IsNA + AddNumeric
' Example from BuildMetaSummary macro:

If Not IsNA(cellValue) And IsNumeric(cellValue) Then
    AddNumeric arr, n, cellValue
End If

' Result: proper N calculation with excluded count
```

## Files

- `na_helpers.py`: Python implementation
- `na_helpers.vba`: VBA templates (reference)
- SKILL.md: This file

## Related Skills

- **excel-inspector**: Analyze NA ratio per column
- **excel-vba-modifier**: Use for VBA NA handling
- Reference: `vba.md` (full VBA implementation)

## Examples

### Example 1: Calculate mean excluding NA

```python
from na_helpers import filter_na
import statistics

data = [10, 20, None, 30, "NA", 40]
clean = filter_na(data)
mean = statistics.mean(clean)  # 25.0 (10+20+30+40)/4
```

### Example 2: Report statistics

```python
from na_helpers import filter_na, na_ratio

data = [...1000 values...]
clean = filter_na(data)

n_total = len(data)
n_valid = len(clean)
n_na = n_total - n_valid
ratio = na_ratio(data)

print(f"N: {n_valid} (excluded: {n_na}, NA%: {ratio*100:.1f}%)")
```

### Example 3: VBA summary calculation

```vba
' In Module2
If Not IsNA(ageVal) And IsNumeric(ageVal) Then
    AddNumeric ageArr, nAge, ageVal
    If CDbl(ageVal) >= 60 Then
        AddNumeric ageOldArr, nAgeOld, ageVal
    Else
        AddNumeric ageYoungArr, nAgeYoung, ageVal
    End If
End If
```

## Compliance

Follows CLAUDE.md NA Handling Guidelines:
✓ Empty, error, text NA treated consistently
✓ NA excluded from aggregates
✓ Count tracked for auditing
✓ Proper numeric conversion order
✓ Results report N correctly
