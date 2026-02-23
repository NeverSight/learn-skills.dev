---
name: anomaly-detector
description: Detect anomalies in data using statistical and ML methods. Z-score, IQR, Isolation Forest, and time-series anomalies.
allowed-tools: Read Write Edit Bash
---

# Anomaly Detector

**Audience:** Data engineers and analysts detecting outliers in datasets.

**Goal:** Provide production-ready anomaly detection functions for various data types.

## Scripts

Execute detection functions from `scripts/anomaly_detection.py`:

```python
from scripts.anomaly_detection import (
    detect_anomalies_zscore,
    detect_anomalies_iqr,
    detect_anomalies_modified_zscore,
    detect_anomalies_isolation_forest,
    detect_anomalies_lof,
    detect_anomalies_rolling,
    detect_anomalies_stl,
    detect_anomalies_ensemble
)
```

## Method Selection

| Method | Best For | Limitations |
|--------|----------|-------------|
| Z-Score | Normal distributions | Sensitive to outliers |
| IQR | Skewed distributions | Less sensitive overall |
| Modified Z-Score | Robust detection | Slower computation |
| Isolation Forest | High-dimensional data | Requires tuning |
| LOF | Local density anomalies | Computationally expensive |
| Rolling | Time-series with trends | Window size sensitive |
| STL | Seasonal time-series | Requires known period |

## Usage Examples

### Single Column Detection

```python
import pandas as pd
from scripts.anomaly_detection import detect_anomalies_zscore, detect_anomalies_iqr

df = pd.read_csv('data.csv')

# Z-score method (good for normal distributions)
anomalies_z = detect_anomalies_zscore(df['value'], threshold=3.0)

# IQR method (robust to skewed data)
anomalies_iqr = detect_anomalies_iqr(df['value'], multiplier=1.5)

print(f"Z-score found {anomalies_z.sum()} anomalies")
print(f"IQR found {anomalies_iqr.sum()} anomalies")
```

### Multi-Column with Isolation Forest

```python
from scripts.anomaly_detection import detect_anomalies_isolation_forest

numeric_cols = ['revenue', 'quantity', 'price']
anomalies = detect_anomalies_isolation_forest(df, numeric_cols, contamination=0.01)

df_anomalies = df[anomalies]
```

### Ensemble Approach (Recommended)

```python
from scripts.anomaly_detection import detect_anomalies_ensemble

results = detect_anomalies_ensemble(
    df,
    columns=['revenue', 'quantity'],
    methods=['zscore', 'iqr', 'isolation_forest'],
    min_agreement=2  # Flag if 2+ methods agree
)

confirmed_anomalies = df[results['is_anomaly']]
```

### Time-Series Anomalies

```python
from scripts.anomaly_detection import detect_anomalies_rolling, detect_anomalies_stl

# Rolling window (for trending data)
anomalies = detect_anomalies_rolling(df['daily_sales'], window=7, n_std=2.0)

# STL decomposition (for seasonal data)
anomalies = detect_anomalies_stl(df['monthly_revenue'], period=12, threshold=3.0)
```

## Dependencies

```
pandas
numpy
scikit-learn  # For Isolation Forest, LOF
statsmodels   # For STL decomposition
```
