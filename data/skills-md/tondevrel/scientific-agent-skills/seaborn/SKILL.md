---
name: seaborn
description: A Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics. Great for exploring relationships between variables and visualizing distributions. Use for statistical data visualization, exploratory data analysis (EDA), relationship plots, distribution plots, categorical comparisons, regression visualization, heatmaps, cluster maps, and creating publication-quality statistical graphics from Pandas DataFrames.
version: 0.13
license: BSD-3-Clause
---

# Seaborn - Statistical Data Visualization

Seaborn helps you explore and understand your data through beautiful, informative statistical plots. It automates complex tasks like calculating confidence intervals, aggregating data, and creating faceted grids.

## When to Use

- Visualizing complex relationships between multiple variables (relplot)
- Examining univariate and bivariate distributions (displot, kdeplot)
- Comparing categories with statistical summaries (catplot, boxplot, violinplot)
- Visualizing linear regression models and their uncertainty (regplot, lmplot)
- Creating heatmaps and cluster maps for large matrices
- Building multi-plot grids based on data subsets (FacetGrid)
- Setting high-level aesthetic themes for Matplotlib figures

## Reference Documentation

**Official docs**: https://seaborn.pydata.org/  
**Example gallery**: https://seaborn.pydata.org/examples/index.html  
**Search patterns**: `sns.load_dataset`, `sns.relplot`, `sns.catplot`, `sns.set_theme`, `sns.heatmap`

## Core Principles

### Figure-Level vs. Axes-Level Functions

| Function Type | Examples | Key Characteristic |
|---------------|----------|-------------------|
| Figure-Level | relplot, displot, catplot | Creates its own figure (FacetGrid). Best for subplots (col, row). |
| Axes-Level | scatterplot, histplot, boxplot | Plots onto a specific ax. Best for integration with Matplotlib layouts. |

### Use Seaborn For

- Statistical analysis and exploratory data research (EDA).
- Working directly with Pandas DataFrames in "tidy" (long-form) format.
- Automatic calculation of 95% confidence intervals (error bars).
- Rapidly changing visual themes and color palettes.

### Do NOT Use For

- Very low-level custom graphics (use Matplotlib).
- Interactive web visualizations (use Plotly).
- 3D plotting (use Matplotlib mplot3d or PyVista).
- Network graphs (use NetworkX with Matplotlib).

## Quick Reference

### Installation

```bash
pip install seaborn
```

### Standard Imports

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Apply the default theme
sns.set_theme()
```

### Basic Pattern - Tidy Data Mapping

```python
import seaborn as sns

# Load an example dataset
tips = sns.load_dataset("tips")

# Create a scatter plot with semantic mapping
sns.relplot(
    data=tips,
    x="total_bill", y="tip", 
    hue="smoker", style="time", size="size",
)
plt.show()
```

## Critical Rules

### ✅ DO

- Use Tidy Data - Ensure your DataFrame is in "long-form" (one row per observation).
- Prefer Figure-Level Functions - Use relplot/displot/catplot for better default layouts and faceting.
- Use the data= parameter - Always pass the DataFrame to keep code clean.
- Set Themes - Use `sns.set_theme(style="whitegrid", palette="muted")` early in your script.
- Leverage hue - Use semantic color mapping to add extra dimensions to 2D plots.
- Context matters - Use `sns.set_context("paper")` for publications or "talk" for presentations.

### ❌ DON'T

- Pass 1D arrays manually - Avoid `sns.plot(x_array, y_array)`; it ignores the power of Pandas integration.
- Ignore the Index - Unlike Matplotlib, Seaborn mostly ignores the DataFrame index (use columns instead).
- Overcrowd plots - Too many semantic mappings (hue, size, style) make graphs unreadable.
- Forget Matplotlib - Remember that Seaborn functions return Matplotlib objects; use `ax.set_title()` to tweak them.

## Anti-Patterns (NEVER)

```python
import seaborn as sns
import matplotlib.pyplot as plt

# ❌ BAD: Iterating through groups to plot manually
for s in df['species'].unique():
    subset = df[df['species'] == s]
    plt.scatter(subset['x'], subset['y'], label=s)

# ✅ GOOD: Let Seaborn handle grouping and legend
sns.scatterplot(data=df, x='x', y='y', hue='species')

# ❌ BAD: Mixing Seaborn and Matplotlib titles incorrectly
sns.displot(data=df, x='val')
plt.title("My Title") # ⚠️ Might apply to the wrong axis in a FacetGrid!

# ✅ GOOD: Use the returned object
g = sns.displot(data=df, x='val')
g.set_axis_labels("Value", "Count")
g.figure.suptitle("Correct Global Title", y=1.05)
```

## Relational Plots (relplot)

### Scatter and Line Plots

```python
# Multi-faceted scatter plot
sns.relplot(
    data=tips, x="total_bill", y="tip",
    col="time", hue="day", style="sex",
    kind="scatter"
)

# Line plot with automatic aggregation (mean + 95% CI)
fmri = sns.load_dataset("fmri")
sns.relplot(
    data=fmri, x="timepoint", y="signal",
    hue="event", style="region",
    kind="line", errorbar="sd" # "sd" for standard deviation instead of CI
)
```

## Distribution Plots (displot)

### Histograms and KDEs

```python
penguins = sns.load_dataset("penguins")

# Histogram with Kernel Density Estimate
sns.displot(data=penguins, x="flipper_length_mm", hue="species", kde=True)

# Bivariate distribution (Heatmap style)
sns.displot(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="species", kind="kde")

# Empirical Cumulative Distribution (ECDF)
sns.displot(data=penguins, x="flipper_length_mm", hue="species", kind="ecdf")
```

## Categorical Plots (catplot)

### Comparisons and Distribution within categories

```python
# Boxplot (Show quartiles and outliers)
sns.catplot(data=tips, x="day", y="total_bill", kind="box")

# Violin plot (Show density and quartiles)
sns.catplot(data=tips, x="day", y="total_bill", hue="sex", kind="violin", split=True)

# Swarm plot (Show every point without overlap)
sns.catplot(data=tips, x="day", y="total_bill", kind="swarm")

# Bar plot (Show mean and error bars)
sns.catplot(data=tips, x="day", y="total_bill", kind="bar", errorbar=("pi", 95))
```

## Regression Plots

### Visualizing Linear Trends

```python
# Simple regression with scatter
sns.regplot(data=tips, x="total_bill", y="tip")

# Faceted regression
sns.lmplot(data=tips, x="total_bill", y="tip", col="smoker", hue="time")

# Logistic regression (for binary data)
sns.lmplot(data=df, x="variable", y="binary_outcome", logistic=True)
```

## Matrix Plots

### Heatmaps and Clustering

```python
flights = sns.load_dataset("flights").pivot(index="month", columns="year", values="passengers")

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(flights, annot=True, fmt="d", cmap="YlGnBu")

# Cluster map (Hierarchical clustering)
sns.clustermap(flights, standard_scale=1, cmap="mako")
```

## Grid Objects (Advanced)

### Custom Multi-plot Layouts

```python
# JointPlot (Scatter + Marginals)
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="species", kind="kde")

# PairPlot (All-against-all relations)
sns.pairplot(data=penguins, hue="species", corner=True)

# Custom FacetGrid
g = sns.FacetGrid(tips, col="time",  row="sex")
g.map(sns.scatterplot, "total_bill", "tip")
```

## Styling and Aesthetics

### Themes and Palettes

```python
# Set overall look
sns.set_style("darkgrid") # white, dark, whitegrid, ticks
sns.set_context("talk")   # paper, notebook, talk, poster

# Custom palettes
sns.set_palette("husl") # Set global palette
my_pal = sns.color_palette("rocket", as_cmap=True) # Get palette as object

# Viewing a palette
sns.palplot(sns.color_palette("Set2"))
```

## Practical Workflows

### 1. Exploratory Data Analysis (EDA) Pipeline

```python
def initial_eda(df, target_col):
    """Generate basic visual summary of a dataset."""
    # 1. Distribution of target
    sns.displot(data=df, x=target_col, kde=True)
    
    # 2. Pairwise relations of numeric features
    sns.pairplot(data=df, hue=target_col if df[target_col].nunique() < 10 else None)
    
    # 3. Correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")

# initial_eda(iris, "species")
```

### 2. Scientific Result Comparison

```python
def plot_experiment_results(df):
    """Plot results of an experiment with multiple conditions."""
    g = sns.catplot(
        data=df, kind="bar",
        x="condition", y="metric", hue="group",
        palette="viridis", alpha=.6, height=6
    )
    g.despine(left=True)
    g.set_axis_labels("Experimental Condition", "Accuracy (%)")
    g.legend.set_title("User Group")
    return g
```

### 3. Time-Series Trends by Category

```python
def plot_trends(df, time_col, val_col, cat_col):
    """Visualizes trends over time with confidence intervals."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=df, x=time_col, y=val_col, hue=cat_col,
        marker="o", err_style="bars"
    )
    plt.xticks(rotation=45)
    plt.tight_layout()
```

## Common Pitfalls and Solutions

### Legend Outside the Plot

```python
# ❌ Problem: Legend covers data in narrow plots
# ✅ Solution: Move legend manually using Matplotlib logic
g = sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")
sns.move_legend(g, "upper left", bbox_to_anchor=(1, 1))
```

### Slow Performance with Large Data

```python
# ❌ Problem: sns.pairplot(large_df) hangs
# ✅ Solution: Sample data or use simpler plots
sns.pairplot(df.sample(1000), hue='category') 
# OR use hist instead of scatter
sns.jointplot(data=df, x='x', y='y', kind="hist")
```

### Overlapping Labels

```python
# ❌ Problem: Categorical labels on X-axis overlap
# ✅ Solution: Rotate labels using Matplotlib
g = sns.boxplot(data=df, x='very_long_category_name', y='value')
g.set_xticklabels(g.get_xticklabels(), rotation=45, horizontalalignment='right')
```

## Best Practices

1. **Use tidy data format** - Ensure your DataFrame is in long-form (one row per observation)
2. **Prefer figure-level functions** - Use `relplot`, `displot`, and `catplot` for better default layouts and faceting
3. **Always use the `data=` parameter** - Pass the DataFrame directly to keep code clean and readable
4. **Set themes early** - Use `sns.set_theme()` at the beginning of your script for consistent styling
5. **Leverage semantic mappings** - Use `hue`, `size`, and `style` to add dimensions to your plots
6. **Choose appropriate context** - Use `sns.set_context("paper")` for publications or "talk" for presentations
7. **Remember Seaborn returns Matplotlib objects** - Use Matplotlib methods like `ax.set_title()` for fine-tuning
8. **Don't overcrowd plots** - Limit semantic mappings to maintain readability
9. **Use figure-level functions for faceting** - They handle subplot layouts automatically
10. **Sample large datasets** - Use `df.sample()` before plotting to improve performance with big data

Seaborn makes statistical visualization a joy by providing high-level abstractions that produce beautiful, publication-quality graphics with minimal effort.
