---
name: spreadsheet-tools
description: Guides and code for creating, analyzing, and formatting spreadsheets. Use this skill to work with Excel files programmatically and apply data analysis techniques.
license: MIT
metadata:
  category: data
---
# Spreadsheet Tools Manual

## Overview

This skill provides instructions and code for manipulating spreadsheets, generating formulas, and analyzing data.

## Working with pandas and openpyxl

### Reading and Writing Excel Files

```python
import pandas as pd

# Read Excel file
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Write DataFrame to a new Excel file
df.to_excel('output.xlsx', index=False)
```

### Applying Formulas

```python
from openpyxl import load_workbook

wb = load_workbook('output.xlsx')
ws = wb.active

# Insert formula into cell C2
ws['C2'] = '=SUM(A2:B2)'
wb.save('output_with_formula.xlsx')
```

### Pivot Tables

```python
# Create a pivot table
pivot = df.pivot_table(values='Sales', index='Region', columns='Quarter', aggfunc='sum')
pivot.to_excel('pivot_table.xlsx')
```

### Charts in Excel

```python
import xlsxwriter

workbook = xlsxwriter.Workbook('chart.xlsx')
worksheet = workbook.add_worksheet()
chart = workbook.add_chart({'type': 'line'})

# Write some data
data = [10, 40, 50, 20, 10, 50]
worksheet.write_column('A1', data)

# Configure chart
chart.add_series({'values': '=Sheet1!$A$1:$A$6'})
chart.set_title({'name': 'Sample Data'})
chart.set_x_axis({'name': 'Index'})
chart.set_y_axis({'name': 'Value'})

worksheet.insert_chart('C1', chart)
workbook.close()
```

## Excel Best Practices

- Use separate sheets for raw data, analysis, and results.
- Name ranges and use table references for clarity.
- Avoid hardcoding values in formulas; use cell references.
- Document complex formulas with comments or a README.

## Analytical Techniques

- **Descriptive statistics**: mean, median, standard deviation.
- **Filtering and sorting**: use pandas' `query()` and `sort_values()`.
- **Time series analysis**: convert date columns to datetime objects; resample using `df.resample()`.

## Additional Resources

- pandas documentation.
- openpyxl and xlsxwriter docs.
- Excel Jet for formula tips.
