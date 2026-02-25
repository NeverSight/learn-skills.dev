---
name: complex-excel-builder
description: Comprehensive toolkit for creating multi-tab Excel workbooks for startups and scale-ups. Use this skill when building financial models, operational dashboards, board reports, or analytics workbooks that require data organization, complex calculations, pivot tables, visualizations, and documentation across multiple interconnected sheets. Specialized for startup metrics (ARR, MRR, CAC, LTV), board-level reporting, and data-driven decision making.
---

# Complex Excel Builder

## Purpose

This skill guides the creation of sophisticated, multi-tab Excel workbooks that startups and growing companies need for financial planning, operational analytics, and board reporting. It handles the entire workflow from requirements gathering through final delivery, ensuring GAAP-compliant calculations, best-practice visualizations, and maintainable formulas.

## When to Use This Skill

Use this skill when creating Excel workbooks that include:

**Financial Models**:
- Revenue models with unit economics
- Fundraising models and burn analysis
- Budget planning and variance tracking
- Cash flow projections

**Operational Dashboards**:
- Sales pipeline and conversion analysis
- Marketing spend and CAC tracking
- Customer cohort and retention analysis
- Product metrics and KPI tracking

**Board-Level Reports**:
- ARR/MRR progression and composition
- Key metrics rollup (Rule of 40, LTV:CAC, etc.)
- Departmental performance scorecards
- Strategic initiative tracking

**Data Analysis Workbooks**:
- Multi-source data consolidation
- Cross-tab analysis with pivots
- Trend analysis with visualizations
- Scenario modeling and sensitivity analysis

## Core Workflow

### Phase 1: Requirements Gathering (Conversational)

Start by understanding what the user needs. Use a conversational approach that elicits detailed requirements without overwhelming them.

**Option A: Structured Elicitation (Default)**

Ask questions progressively to build a complete picture:

**Initial Questions**:
1. "What's the primary purpose of this workbook?" (financial model, dashboard, analysis, report)
2. "What decisions will this workbook support?" (fundraising, budgeting, monitoring, board updates)
3. "Who is the primary audience?" (founders, board, team, investors)

**Data Questions**:
4. "What data sources will feed this workbook?" (CSV exports, database dumps, manual entry, API data, PDFs, screenshots)
5. "How frequently will data be updated?" (real-time, daily, weekly, monthly, quarterly)
6. "What time periods should be covered?" (historical lookback, forward projections)

**Metrics Questions**:
7. "What are the 3-5 most important metrics to track?" (let user define, then validate against standard definitions)
8. "Are there specific calculations or formulas you need?" (standard SaaS metrics, custom business logic)
9. "What comparisons matter most?" (time-over-time, budget vs actual, cohorts, segments)

**Output Questions**:
10. "What views or visualizations do you need?" (trends, comparisons, composition, distributions)
11. "Do you need scenario modeling capabilities?" (base/upside/downside cases, sensitivity tables)
12. "What documentation should be included?" (assumptions, data sources, calculation methodology)

**Technical Questions**:
13. "Are there any specific formatting or structure requirements?" (corporate templates, color schemes, layout preferences)
14. "Will this integrate with other systems?" (export format needs, data validation requirements)

**Option B: Requirements Dump (User-Initiated)**

If the user provides comprehensive requirements upfront, acknowledge and confirm understanding:

```
"I understand you need [summarize their requirements]. Let me confirm the key elements:
- Data sources: [list]
- Key metrics: [list]
- Calculations: [list]
- Outputs: [list]
- Timeframes: [details]

Before I start building, are there any other considerations like:
- Specific formatting requirements?
- Integration needs?
- Scenario modeling?
- [Any gaps noticed in their requirements]"
```

**Validation Step** (Always):

Before moving to design, summarize the complete requirements:
```
"Here's what I'll build:

DATA LAYER:
- [Data sources and formats]
- [Import/transformation approach]

CALCULATIONS:
- [Key metrics with standard definitions]
- [Custom business logic]
- [Time period coverage]

OUTPUTS:
- [Tabs/sheets structure]
- [Visualizations and chart types]
- [Pivots and cross-tabs]
- [Documentation]

Does this capture everything, or should I adjust anything?"
```

### Phase 2: Architecture Design

After gathering requirements, design the workbook structure. Always include these standard tabs (customize names as appropriate):

**Standard Tab Architecture**:

1. **Overview/Dashboard Tab** (First tab - always)
   - Executive summary with KPIs
   - Key charts and trends
   - Quick navigation to other tabs
   - Last updated date

2. **Data Tab(s)** (Hidden after setup unless user needs visibility)
   - Raw imported data
   - Organized, deduplicated, validated
   - Clearly structured for formula references
   - Data source documentation

3. **Calculations Tab** (Core model)
   - All intermediate calculations
   - Assumption cells (clearly labeled, blue text)
   - Time series calculations
   - Metric definitions

4. **Summaries Tab(s)** (As needed)
   - Aggregated views by time period
   - Segmented analyses (by product, region, customer type, etc.)
   - Variance analysis (actual vs budget, current vs prior)

5. **Charts Tab** (Visualizations)
   - All charts in one place for easy review
   - Consistent sizing and formatting
   - Clear titles indicating insight

6. **Pivots Tab(s)** (Interactive analysis)
   - Pivot tables for user exploration
   - Slicers for filtering
   - Multiple perspectives on data

7. **Documentation Tab** (Last tab - always)
   - Data sources and refresh dates
   - Calculation methodology
   - Assumptions and their rationale
   - Change log
   - Instructions for updating

**Communicate the design**:
```
"I'll create a workbook with these tabs:
1. [Dashboard] - [What it shows]
2. [Data] - [What it contains]
3. [Calculations] - [What it computes]
...
[Etc.]

This structure ensures [explain benefits: maintainability, auditability, usability]."
```

### Phase 3: Data Processing

Before building Excel formulas, process and prepare data:

**Step 3.1: Load and Inspect Data**

```python
import pandas as pd
from openpyxl import Workbook
import json

# Handle different data formats
if file.endswith('.csv'):
    df = pd.read_csv(file)
elif file.endswith('.json'):
    df = pd.read_json(file)
elif file.endswith('.xlsx'):
    df = pd.read_excel(file)
elif file.endswith('.pdf'):
    # Extract tables from PDF using tabula or camelot
    # Document extraction method in Documentation tab
    pass
# For screenshots: inform user OCR extracted, verify accuracy

# Inspect data
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Data types:\n{df.dtypes}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Sample:\n{df.head()}")
```

**Step 3.2: Clean and Transform**

```python
# Standardize columns
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Handle missing values
# Document decisions: "Missing dates filled forward", etc.

# Parse dates consistently
date_columns = ['date', 'created_at', 'transaction_date']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Add derived columns useful for analysis
if 'date' in df.columns:
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%Y-%m')

# Sort chronologically if time series
if 'date' in df.columns:
    df = df.sort_values('date')

# Remove duplicates
df = df.drop_duplicates()
```

**Step 3.3: Validate Data**

```python
# Check for data quality issues
issues = []

# Check date ranges
if 'date' in df.columns:
    date_range = f"{df['date'].min()} to {df['date'].max()}"
    print(f"Date range: {date_range}")
    
# Check for negative values in fields that shouldn't be negative
numeric_cols = df.select_dtypes(include=['number']).columns
for col in ['revenue', 'amount', 'quantity']:
    if col in df.columns and (df[col] < 0).any():
        issues.append(f"Warning: Negative values found in {col}")

# Check for outliers (values > 3 std dev from mean)
for col in numeric_cols:
    mean = df[col].mean()
    std = df[col].std()
    outliers = df[(df[col] > mean + 3*std) | (df[col] < mean - 3*std)]
    if len(outliers) > 0:
        issues.append(f"Warning: {len(outliers)} potential outliers in {col}")

if issues:
    print("Data quality issues to review:")
    for issue in issues:
        print(f"  - {issue}")
```

### Phase 4: Excel Construction

**Step 4.1: Initialize Workbook**

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

wb = Workbook()

# Create all tabs upfront
tab_names = ['Dashboard', 'Data', 'Calculations', 'Summary', 'Charts', 'Pivots', 'Documentation']
for name in tab_names:
    if name == 'Dashboard':
        ws = wb.active
        ws.title = name
    else:
        ws = wb.create_sheet(name)

# Define reusable styles
header_font = Font(bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
input_font = Font(color='0000FF')  # Blue for inputs
formula_font = Font(color='000000')  # Black for formulas
border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
```

**Step 4.2: Build Data Tab**

```python
data_sheet = wb['Data']

# Write dataframe to Excel
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        cell = data_sheet.cell(row=r_idx, column=c_idx, value=value)
        
        # Header formatting
        if r_idx == 1:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        cell.border = border

# Auto-adjust column widths
for column in data_sheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = min(max_length + 2, 50)
    data_sheet.column_dimensions[column_letter].width = adjusted_width

# Convert to Table for structured references
# This makes formulas more readable and maintainable
from openpyxl.worksheet.table import Table, TableStyleInfo
max_row = data_sheet.max_row
max_col = data_sheet.max_column
table_ref = f"A1:{data_sheet.cell(max_row, max_col).coordinate}"
table = Table(displayName='DataTable', ref=table_ref)
style = TableStyleInfo(
    name='TableStyleMedium2',
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False
)
table.tableStyleInfo = style
data_sheet.add_table(table)

# Add data documentation
doc_sheet = wb['Documentation']
doc_sheet['A1'] = 'Data Sources'
doc_sheet['A1'].font = Font(bold=True, size=14)
doc_sheet['A3'] = 'Data Tab:'
doc_sheet['A3'].font = Font(bold=True)
doc_sheet['B3'] = f'Source: [Document source here]'
doc_sheet['B4'] = f'Date range: {date_range if "date_range" in locals() else "N/A"}'
doc_sheet['B5'] = f'Rows: {len(df)}'
doc_sheet['B6'] = f'Last updated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}'
```

**Step 4.3: Build Calculations Tab**

Use best practices from `references/formula_best_practices.md`:

```python
calc_sheet = wb['Calculations']

# Section 1: Assumptions (Blue text, clearly labeled)
calc_sheet['A1'] = 'ASSUMPTIONS'
calc_sheet['A1'].font = Font(bold=True, size=14)

# Example assumptions
assumptions = [
    ('Revenue Growth Rate (YoY)', 0.25, '25%'),
    ('Gross Margin %', 0.75, '75%'),
    ('CAC', 5000, '$5,000'),
]

row = 3
for label, value, formatted in assumptions:
    calc_sheet.cell(row, 1, label)
    cell = calc_sheet.cell(row, 2, value)
    cell.font = input_font  # Blue for inputs
    cell.number_format = formatted.replace('%', '0%').replace('$', '$#,##0')
    row += 1

# Section 2: Calculations (Black text, use Excel formulas)
calc_sheet[f'A{row+2}'] = 'CALCULATIONS'
calc_sheet[f'A{row+2}'].font = Font(bold=True, size=14)

row += 4

# CRITICAL: Use Excel formulas, not hardcoded Python calculations
# Example: Calculate metrics using formulas referencing Data tab

calc_sheet.cell(row, 1, 'Total Revenue')
calc_sheet.cell(row, 2, '=SUM(DataTable[revenue])')  # Structured reference
calc_sheet.cell(row, 2).number_format = '$#,##0'

row += 1
calc_sheet.cell(row, 1, 'Average Deal Size')
calc_sheet.cell(row, 2, '=AVERAGE(DataTable[deal_size])')
calc_sheet.cell(row, 2).number_format = '$#,##0'

row += 1
calc_sheet.cell(row, 1, 'Customer Count')
calc_sheet.cell(row, 2, '=COUNTA(DataTable[customer_id])')

# Use XLOOKUP for lookups, SUMIFS for conditional aggregation
# Follow patterns from formula_best_practices.md
```

**Step 4.4: Build Summary/Analysis Tabs**

```python
summary_sheet = wb['Summary']

# Time series summary example
summary_sheet['A1'] = 'Monthly Summary'
summary_sheet['A1'].font = Font(bold=True, size=14)

headers = ['Month', 'Revenue', 'Customers', 'Avg Deal Size', 'MoM Growth %']
for col, header in enumerate(headers, 1):
    cell = summary_sheet.cell(3, col, header)
    cell.font = header_font
    cell.fill = header_fill

# Use SUMIFS/AVERAGEIFS to aggregate by month
# Example for a month:
row = 4
summary_sheet.cell(row, 1, '2024-01')  # Month
summary_sheet.cell(row, 2, '=SUMIFS(DataTable[revenue], DataTable[month_name], A4)')
summary_sheet.cell(row, 3, '=COUNTIFS(DataTable[month_name], A4)')
summary_sheet.cell(row, 4, '=B4/C4')  # Avg = Total / Count
summary_sheet.cell(row, 5, '=(B4-B3)/B3')  # MoM growth
summary_sheet.cell(row, 5).number_format = '0.0%'

# Copy formulas down for all months
# (Repeat or use Python loop to populate all months)
```

**Step 4.5: Create Charts**

Use best practices from `references/visualization_best_practices.md`:

```python
from openpyxl.chart import LineChart, BarChart, Reference

charts_sheet = wb['Charts']

# Chart 1: Revenue Trend (Line Chart - max 4 lines)
chart1 = LineChart()
chart1.title = "Monthly Revenue Trend"
chart1.style = 2
chart1.y_axis.title = 'Revenue ($)'
chart1.x_axis.title = 'Month'

# Reference data from Summary tab
data = Reference(summary_sheet, min_col=2, min_row=3, max_row=15, max_col=2)
categories = Reference(summary_sheet, min_col=1, min_row=4, max_row=15)
chart1.add_data(data, titles_from_data=True)
chart1.set_categories(categories)

# Chart sizing and placement
chart1.width = 15  # inches
chart1.height = 7.5  # ~2:1 aspect ratio
charts_sheet.add_chart(chart1, 'A1')

# Chart 2: Revenue by Segment (Bar Chart - horizontal)
# Use bar chart for categorical comparisons
chart2 = BarChart()
chart2.type = 'bar'  # Horizontal bars
chart2.title = "Revenue by Customer Segment"
chart2.y_axis.title = 'Segment'
chart2.x_axis.title = 'Revenue ($M)'

# ... configure chart2 data references ...

charts_sheet.add_chart(chart2, 'A30')

# AVOID: Pie charts, 3D charts, crowded line charts (>4 lines)
# PREFER: Bar charts for comparisons, line charts for trends (≤4 lines)
```

**Step 4.6: Create Pivot Tables**

```python
pivots_sheet = wb['Pivots']

# Pivot tables require careful setup
# For complex pivots, document the structure for user to recreate manually
# Or provide the aggregated data that would result from the pivot

pivots_sheet['A1'] = 'Pivot Analysis'
pivots_sheet['A1'].font = Font(bold=True, size=14)
pivots_sheet['A3'] = 'Instructions:'
pivots_sheet['A4'] = '1. Select Data tab'
pivots_sheet['A5'] = '2. Insert > PivotTable'
pivots_sheet['A6'] = '3. Configuration:'
pivots_sheet['A7'] = '   - Rows: [Customer Segment]'
pivots_sheet['A8'] = '   - Columns: [Quarter]'
pivots_sheet['A9'] = '   - Values: Sum of [Revenue]'

# Alternatively, pre-build aggregated tables that mimic pivot outputs
```

**Step 4.7: Build Dashboard**

```python
dashboard = wb['Dashboard']

# Title and date
dashboard['A1'] = '[Company Name] - [Report Title]'
dashboard['A1'].font = Font(bold=True, size=16)
dashboard['A2'] = f'As of: {pd.Timestamp.now().strftime("%B %d, %Y")}'

# KPI cards (large numbers at top)
dashboard['A4'] = 'Key Metrics'
dashboard['A4'].font = Font(bold=True, size=14)

kpis = [
    ('ARR', '=Calculations!B10', '$#,##0'),
    ('MRR', '=Calculations!B11', '$#,##0'),
    ('Customers', '=Calculations!B12', '#,##0'),
    ('NRR', '=Calculations!B13', '0.0%'),
]

col = 1
for label, formula, fmt in kpis:
    dashboard.cell(5, col, label)
    dashboard.cell(5, col).font = Font(bold=True)
    dashboard.cell(5, col).fill = PatternFill(start_color='E7E6E6', fill_type='solid')
    
    cell = dashboard.cell(6, col, formula)
    cell.font = Font(size=20, bold=True)
    cell.number_format = fmt
    
    col += 3  # Space between KPIs

# Embed key charts from Charts tab
# (Charts can be copied to Dashboard for at-a-glance view)

# Navigation
dashboard['A20'] = 'Navigation:'
dashboard['A21'] = '→ Detailed calculations: See "Calculations" tab'
dashboard['A22'] = '→ All visualizations: See "Charts" tab'
dashboard['A23'] = '→ Interactive analysis: See "Pivots" tab'
```

**Step 4.8: Complete Documentation Tab**

```python
doc_sheet = wb['Documentation']

sections = [
    ('Data Sources', [
        'Data Tab: [Source description]',
        'Last updated: [Date]',
        'Update frequency: [Frequency]',
        'Data quality notes: [Any issues or caveats]'
    ]),
    ('Calculation Methodology', [
        'ARR: Sum of annualized recurring revenue from active contracts',
        'MRR: Monthly recurring revenue (ARR / 12)',
        'CAC: Total S&M spend / new customers acquired',
        '[Other metric definitions]'
    ]),
    ('Assumptions', [
        'Growth Rate: Based on [rationale]',
        'Churn Rate: Historical average of [X]%',
        '[Other assumptions]'
    ]),
    ('Usage Instructions', [
        '1. To update data: Replace Data tab with new export',
        '2. To recalculate: Formulas auto-update',
        '3. To modify assumptions: Edit blue cells in Calculations tab',
        '4. To create scenarios: Copy Calculations tab, rename, adjust assumptions'
    ]),
    ('Change Log', [
        f'{pd.Timestamp.now().strftime("%Y-%m-%d")}: Initial version',
    ])
]

row = 1
for section_title, bullets in sections:
    doc_sheet.cell(row, 1, section_title)
    doc_sheet.cell(row, 1).font = Font(bold=True, size=12)
    row += 2
    
    for bullet in bullets:
        doc_sheet.cell(row, 1, f'• {bullet}')
        row += 1
    
    row += 1  # Blank line between sections
```

### Phase 5: Validation and Quality Assurance

**Step 5.1: Recalculate Formulas**

```bash
python /mnt/skills/public/xlsx/recalc.py /home/claude/workbook.xlsx
```

**Step 5.2: Check for Errors**

```python
import json

# Parse recalc output
result = json.loads(recalc_output)

if result['status'] == 'errors_found':
    print(f"⚠️  Found {result['total_errors']} formula errors:")
    for error_type, details in result['error_summary'].items():
        print(f"  {error_type}: {details['count']} occurrences")
        print(f"    Locations: {details['locations'][:5]}")  # First 5
    
    # Fix errors and recalculate
    # Common fixes:
    # - #REF!: Fix cell references
    # - #DIV/0!: Add error handling or check denominators
    # - #VALUE!: Check data types in formula
    # - #NAME?: Fix formula function names or defined names
    
else:
    print("✅ All formulas calculated successfully (zero errors)")
```

**Step 5.3: Validate Against Requirements**

Checklist:
- [ ] All requested metrics calculated correctly
- [ ] Formulas use proper definitions (check against `financial_metrics_gaap.md`)
- [ ] Charts follow best practices (check against `visualization_best_practices.md`)
- [ ] Formulas are maintainable (check against `formula_best_practices.md`)
- [ ] All tabs present and properly named
- [ ] Data is properly structured and documented
- [ ] Zero formula errors
- [ ] Documentation complete

### Phase 6: Final Delivery

**Step 6.1: Move to Outputs**

```bash
cp /home/claude/workbook.xlsx /mnt/user-data/outputs/[descriptive_name].xlsx
```

**Step 6.2: Summary for User**

Provide concise summary:
```
"I've created your [workbook type] with:

📊 STRUCTURE:
- [Number] tabs: [list key tabs]
- [Number] data sources integrated
- [Number] calculated metrics

📈 KEY FEATURES:
- [Highlight 2-3 main capabilities]
- Charts following best practices (bar charts for comparisons, line charts for trends)
- GAAP-compliant financial calculations

📝 USAGE:
- Update data: [Simple instruction]
- Modify assumptions: [Where and how]
- Review documentation: See Documentation tab

[View your workbook](computer:///mnt/user-data/outputs/[filename].xlsx)"
```

**Do NOT** provide overly detailed explanations of every tab and formula. Give user access to the file and concise next steps.

## Key Principles

### Financial Calculations

**Always follow GAAP standards**:
- Reference `financial_metrics_gaap.md` for standard metric definitions
- Use proper revenue recognition (ASC 606)
- Calculate LTV, CAC, churn correctly
- Document any non-GAAP metrics

**Common startup metrics**:
```
ARR = Sum of annual recurring revenue
MRR = ARR / 12
CAC = (Sales + Marketing Expense) / New Customers
LTV = (Avg Revenue per Customer / Churn Rate) × Gross Margin
Payback Period = CAC / (MRR × Gross Margin)
NRR = (Start MRR + Expansion - Contraction - Churn) / Start MRR
Rule of 40 = Growth Rate % + Profit Margin %
```

### Formula Best Practices

**Always** reference `formula_best_practices.md` for:
- Use XLOOKUP, not VLOOKUP
- Use SWITCH/IFS, not nested IFs
- Use SUMIFS/COUNTIFS for conditional aggregation
- Use structured table references, not cell ranges
- Make formulas scalable and auditable
- Never hardcode values - always use cell references

### Visualization Best Practices

**Always** reference `visualization_best_practices.md` for:
- ❌ Avoid: Pie charts, 3D charts, crowded line charts (>4 lines)
- ✅ Use: Bar charts (comparisons), line charts (trends, max 4 lines), waterfall charts (variance)
- Choose right chart type for data story
- Use clean, colorblind-safe colors
- Label clearly with units
- Minimize chart junk

### Color Coding Standards

Follow financial modeling conventions:
- **Blue text**: Hardcoded inputs/assumptions users change
- **Black text**: Formulas and calculations
- **Green text**: References to other sheets in same workbook
- **Red text**: External links to other files
- **Yellow background**: Cells needing attention

### Error Prevention

- Run `recalc.py` after creating/modifying workbook
- Fix ALL errors before delivery (target: zero #REF!, #DIV/0!, #VALUE!, etc.)
- Test edge cases (zeros, negatives, missing data)
- Validate formulas manually for 2-3 sample calculations

## Bundled Resources

### References (Load as Needed)

**`financial_metrics_gaap.md`**: 
- GAAP revenue recognition (ASC 606)
- Standard SaaS metrics (ARR, MRR, CAC, LTV, NRR)
- Growth metrics and ratios
- Common calculation errors to avoid
- Model structure best practices

**`formula_best_practices.md`**:
- Modern Excel functions (XLOOKUP, SWITCH, IFS, SUMIFS)
- Formula anti-patterns to avoid
- Structured table references
- Error handling best practices
- Performance optimization

**`visualization_best_practices.md`**:
- Chart type selection guide
- What NOT to use (pie charts, 3D, etc.)
- Color and formatting guidelines
- Dashboard design principles
- Accessibility and testing

### When to Use References

- **Before building**: Review relevant reference(s) to incorporate best practices
- **During validation**: Check calculations against GAAP standards
- **When stuck**: Consult formula best practices for better approach
- **For charts**: Follow visualization guidelines for professional output

## Common Workbook Patterns

### Pattern 1: Sales Analysis Workbook

**Tabs**: Dashboard | Data | Monthly Summary | Cohort Analysis | Charts | Documentation
**Key Metrics**: Revenue, Deal Size, Win Rate, Sales Cycle, Pipeline Coverage
**Charts**: Monthly revenue trend, deal size distribution, win rate by segment

### Pattern 2: Marketing CAC Workbook

**Tabs**: Dashboard | Spend Data | Conversions | CAC Calculations | Channel Analysis | Charts | Documentation  
**Key Metrics**: CAC by channel, Payback Period, LTV:CAC, Channel ROI
**Charts**: CAC trend over time, spend by channel (bar chart), payback period waterfall

### Pattern 3: Board Metrics Workbook

**Tabs**: Dashboard | ARR/MRR Detail | Customer Metrics | Financial Summary | Charts | Documentation
**Key Metrics**: ARR, MRR, NRR, Growth Rate, Burn Rate, Rule of 40
**Charts**: ARR progression, MRR composition (stacked bar), cohort retention, runway

### Pattern 4: Financial Model

**Tabs**: Dashboard | Assumptions | Historical | Projections | Scenarios | Charts | Documentation
**Key Metrics**: Revenue, Gross Margin, Operating Expenses, EBITDA, Cash
**Charts**: Revenue projection, cash runway, expense breakdown

## Tips for Success

1. **Start with requirements**: Don't jump to building. Understand the need first.
2. **Design before coding**: Plan tab structure before writing formulas.
3. **Use formulas, not hardcoding**: Excel should recalculate, not just display Python results.
4. **Follow standards**: Use GAAP definitions, modern Excel functions, appropriate charts.
5. **Document thoroughly**: Explain data sources, calculations, assumptions.
6. **Validate ruthlessly**: Zero formula errors, test edge cases, check against requirements.
7. **Keep it simple**: Clear is better than clever. Maintainable is better than compact.

## Troubleshooting

**Issue**: Formulas not calculating
**Solution**: Run `recalc.py` script to force recalculation

**Issue**: #REF! errors
**Solution**: Cell references are broken. Check if referenced cells exist.

**Issue**: Data not updating when source changes
**Solution**: Formulas are hardcoded values. Use formulas referencing data, not Python calculations.

**Issue**: Charts are too crowded
**Solution**: Limit line charts to 4 lines max. Use small multiples or filtering.

**Issue**: Metrics don't match standard definitions  
**Solution**: Review `financial_metrics_gaap.md` for correct formulas.

**Issue**: Workbook is slow
**Solution**: Reduce volatile functions (NOW, RAND), use whole-column references carefully, consider manual calculation mode for large models.
