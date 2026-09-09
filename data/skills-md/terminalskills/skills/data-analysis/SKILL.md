---
name: data-analysis
description: >-
  Analyze spreadsheet data, generate insights, and create visualizations.
  Use when a user asks to analyze data, explore a dataset, find trends,
  generate statistics, create charts from CSV or Excel data, summarize
  data, or answer questions about tabular data.
license: Apache-2.0
compatibility: "Requires Python 3.8+ with pandas, matplotlib, and seaborn"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["data-analysis", "pandas", "visualization", "statistics", "csv"]
  use-cases:
    - "Analyze a CSV or Excel file and generate summary statistics"
    - "Create charts and visualizations from tabular data"
    - "Answer specific questions about patterns and trends in datasets"
  agents: [claude-code, openai-codex, gemini-cli, cursor]
---

# Data Analysis

## Overview

Analyze tabular data from CSV, Excel, or other structured formats. Generate summary statistics, discover patterns, answer specific questions, and produce visualizations. Uses Python with pandas for data manipulation and matplotlib/seaborn for charts.

## Instructions

When a user asks you to analyze data, follow this process:

### Step 1: Verify dependencies

Ensure required Python packages are available:

```bash
python3 -c "import pandas; import matplotlib; import seaborn; print('All packages available')" 2>/dev/null || \
  pip install pandas matplotlib seaborn openpyxl
```

### Step 2: Load and inspect the data

Read the file and understand its structure:

```python
import pandas as pd

# Load the data (auto-detect format)
df = pd.read_csv("data.csv")        # For CSV
# df = pd.read_excel("data.xlsx")   # For Excel
# df = pd.read_json("data.json")    # For JSON

# Initial inspection
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
```

Report the dataset structure to the user before proceeding:
- Number of rows and columns
- Column names and data types
- Missing value counts
- Any obvious data quality issues

### Step 3: Generate summary statistics

```python
# Numeric summary
print(df.describe())

# Categorical summary
for col in df.select_dtypes(include='object').columns:
    print(f"\n{col} - unique values: {df[col].nunique()}")
    print(df[col].value_counts().head(10))

# Correlations between numeric columns
print(df.select_dtypes(include='number').corr())
```

### Step 4: Answer specific questions or explore patterns

Based on the user's request, perform targeted analysis:

**Filtering and aggregation:**

```python
# Group by category and compute stats
summary = df.groupby('category').agg(
    count=('id', 'count'),
    avg_value=('value', 'mean'),
    total=('value', 'sum')
).sort_values('total', ascending=False)
```

**Time series analysis:**

```python
df['date'] = pd.to_datetime(df['date'])
monthly = df.resample('M', on='date').agg({'revenue': 'sum', 'orders': 'count'})
```

**Outlier detection:**

```python
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['value'] < Q1 - 1.5*IQR) | (df['value'] > Q3 + 1.5*IQR)]
print(f"Found {len(outliers)} outliers")
```

### Step 5: Create visualizations

Save charts as image files:

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Bar chart
df.groupby('category')['revenue'].sum().plot(kind='bar', ax=ax)
ax.set_title('Revenue by Category')
ax.set_ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('chart_revenue_by_category.png', dpi=150)
plt.close()

# Line chart for trends
fig, ax = plt.subplots(figsize=(10, 6))
monthly['revenue'].plot(ax=ax)
ax.set_title('Monthly Revenue Trend')
plt.tight_layout()
plt.savefig('chart_monthly_trend.png', dpi=150)
plt.close()

# Correlation heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap='coolwarm', ax=ax)
plt.tight_layout()
plt.savefig('chart_correlation.png', dpi=150)
plt.close()
```

### Step 6: Present findings

Summarize the analysis with:
- Key statistics (totals, averages, medians)
- Notable patterns or trends discovered
- Outliers or anomalies
- Visualizations with descriptions
- Actionable insights or recommendations

## Examples

### Example 1: Analyze sales data

**User request:** "Analyze this sales CSV and tell me what's trending"

**Actions:**

1. Load `sales.csv` and inspect (columns: date, product, category, quantity, price, region)
2. Compute total revenue (quantity * price), group by month
3. Identify top products and categories by revenue
4. Detect growth trends by comparing recent months to prior months
5. Create a monthly revenue trend line chart and a category breakdown bar chart

**Output:** "Sales totaled $2.4M over 12 months. Revenue grew 15% quarter-over-quarter. Electronics is the top category (42% of revenue). The Southwest region underperforms at 8% of total sales despite covering 20% of stores. See the attached charts for trends."

### Example 2: Compare two datasets

**User request:** "Compare last year's performance to this year"

**Actions:**

1. Load both CSV files
2. Align on common columns (date, metric)
3. Compute year-over-year changes for key metrics
4. Highlight improvements and regressions
5. Create a side-by-side comparison chart

**Output:** A comparison table showing each metric with last year vs. this year values, percentage change, and a trend indicator.

### Example 3: Find anomalies in log data

**User request:** "Are there any anomalies in this server metrics CSV?"

**Actions:**

1. Load metrics data (timestamp, cpu_usage, memory, response_time, error_rate)
2. Compute rolling averages and standard deviations
3. Flag data points beyond 2 standard deviations
4. Correlate anomalies across metrics (did CPU spike with errors?)
5. Plot a timeline highlighting anomaly windows

**Output:** "Found 3 anomaly windows: Jan 15 2-4pm (CPU 95%, errors 12x normal), Feb 3 11am (memory spike to 98%), Mar 20 all day (elevated response times). The Jan 15 event correlates with a deployment at 1:55pm."

## Guidelines

- Always inspect the data before analyzing. Report shape, types, and quality to the user.
- Handle missing values explicitly: report them, then decide whether to drop or fill.
- Use appropriate chart types: line for trends, bar for categories, scatter for correlations, heatmap for matrices.
- Save all charts as PNG files with descriptive filenames and 150 DPI for readability.
- Present numbers with context: "Revenue is $1.2M" is less useful than "Revenue is $1.2M, up 15% from last quarter."
- For large datasets (100K+ rows), work with samples or aggregations to avoid slow operations.
- Always label chart axes, add titles, and use readable fonts.
- When the user's question is vague ("analyze this"), provide a comprehensive overview covering distribution, trends, correlations, and outliers.
