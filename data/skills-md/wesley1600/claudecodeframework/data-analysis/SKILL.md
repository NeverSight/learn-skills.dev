---
name: data-analysis
description: Analyze data patterns, create visualizations, and generate insights from datasets using statistical methods and data science techniques
---

# Data Analysis Skill

Transform raw data into actionable insights. This skill helps you explore datasets, identify patterns, create visualizations, and generate statistical reports.

## Purpose

This skill enables you to:
- Load and explore datasets of various formats (CSV, JSON, Parquet)
- Perform exploratory data analysis (EDA)
- Create statistical summaries and distributions
- Generate data visualizations and charts
- Identify correlations and trends
- Detect anomalies and outliers
- Build predictive models
- Export analysis reports

## When to Use

Use this skill when you need to:
- Understand a new dataset
- Find trends and patterns in data
- Create reports with visualizations
- Identify data quality issues
- Compare groups or time periods
- Forecast future values
- Build summary dashboards
- Share insights with stakeholders

## Key Features

1. **EDA Tools** - Automated exploratory analysis
2. **Visualizations** - Charts, graphs, and heatmaps
3. **Statistical Analysis** - Descriptive stats, hypothesis testing, correlation
4. **Data Cleaning** - Handle missing values, outliers, duplicates
5. **Time Series** - Seasonal decomposition and forecasting
6. **Machine Learning** - Clustering, classification, regression
7. **Reports** - Professional analysis documents with code
8. **Export Options** - Save to HTML, PDF, or interactive dashboards

## Instructions

When using this skill:

1. **Load Data** - Provide dataset path or CSV/JSON content
2. **Explore** - Generate summary statistics and visualizations
3. **Analyze** - Identify patterns, trends, and relationships
4. **Validate** - Check data quality and handle issues
5. **Visualize** - Create meaningful charts and graphs
6. **Model** - Build predictive models if needed
7. **Report** - Document findings and recommendations

## Guidelines

- **Start Simple**: Begin with univariate analysis before multivariate
- **Visualize First**: Always look at the data before statistics
- **Question Assumptions**: Don't assume patterns are significant
- **Document Methods**: Explain your analytical approach
- **Consider Context**: Interpret results within business context
- **Validate Results**: Confirm findings with domain experts
- **Communicate Clearly**: Use simple language and visual metaphors

## Examples

### Example 1: Customer Purchase Analysis

**Dataset:** Customer transactions with 10,000 records

**Analysis Steps:**
1. Load purchase data (date, customer_id, amount, category)
2. Calculate summary statistics (total spend, average order value)
3. Visualize purchase distribution by category
4. Analyze seasonal trends
5. Identify top customers
6. Detect purchase anomalies

**Output:**
```markdown
# Customer Analysis Report

## Summary Statistics
- Total Revenue: $2.5M
- Average Order Value: $125
- Number of Customers: 3,450
- Date Range: 2023-01-01 to 2024-01-15

## Key Findings
1. Electronics category drives 42% of revenue
2. Top 20% of customers generate 80% of revenue (Pareto principle)
3. Strong seasonal pattern with peak in Q4
4. Average customer lifetime value: $1,200

## Recommendations
- Focus retention efforts on high-value customers
- Increase inventory for Q4 seasonal demand
- Cross-sell opportunities in Electronics + Home categories
```

### Example 2: Website Traffic Analysis

**Dataset:** Daily pageviews, bounce rate, session duration

**Key Metrics Analyzed:**
- Traffic trends over time
- Device type distribution
- Top pages and conversion rates
- User behavior funnels
- Mobile vs. desktop comparison

**Visualizations Generated:**
- Line chart: Daily pageviews over 12 months
- Bar chart: Traffic by device type
- Funnel chart: User conversion flow
- Heatmap: Day/hour traffic patterns

## Analysis Patterns

| Scenario | Analysis Type | Key Metrics |
|----------|--------------|-----------|
| Sales Data | Trend & Seasonal | Growth rate, Seasonality index |
| Customer Data | Segmentation | RFM score, Cohort analysis |
| Website Data | Behavior | Bounce rate, Conversion funnel |
| Time Series | Forecasting | Trend, Seasonality, Residuals |
| A/B Testing | Hypothesis Test | P-value, Effect size |

## Tools and Libraries

This skill uses:
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **matplotlib/seaborn** - Visualizations
- **scipy** - Statistical tests
- **scikit-learn** - Machine learning
- **plotly** - Interactive visualizations

## Data Quality Checks

The skill automatically:
- [ ] Identifies missing values
- [ ] Detects duplicate records
- [ ] Flags outliers
- [ ] Validates data types
- [ ] Checks for referential integrity
- [ ] Reports data completeness

## Common Analyses

### Descriptive Analysis
- Data summaries
- Distribution analysis
- Correlation matrices
- Group comparisons

### Predictive Analysis
- Trend forecasting
- Anomaly detection
- Classification models
- Regression models

### Diagnostic Analysis
- Root cause analysis
- Cohort analysis
- Segmentation
- Attribution modeling

## Related Resources

- [Data Analysis Best Practices](./references/analysis-guide.md)
- [Python Data Science Cheatsheet](./references/python-cheatsheet.md)
- [Visualization Gallery](./assets/examples/visualizations/)
- [Sample Datasets](./assets/examples/datasets/)
- [Analysis Scripts](./scripts/)

## Support

For data analysis help:
1. Review the examples above
2. Check sample datasets in `assets/examples/datasets/`
3. Use helper scripts in `scripts/`
4. Consult the detailed guide in `references/`
