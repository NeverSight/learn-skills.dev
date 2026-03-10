---
name: detect-anomalies-aiops
description: >
  Implement AI-powered anomaly detection for operational metrics using time series analysis
  (Isolation Forest, Prophet, LSTM), alert correlation, and root cause analysis. Reduce
  alert fatigue by intelligently identifying true anomalies in system metrics, logs, and traces.
  Use when operations teams are overwhelmed by alert volume, when detecting complex multi-metric
  anomalies beyond static thresholds, when seasonal patterns make thresholds ineffective, or
  when needing to predict issues proactively before they impact users.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: mlops
  complexity: advanced
  language: multi
  tags: aiops, anomaly-detection, isolation-forest, prophet, alert-correlation, time-series
---

# Detect Anomalies for AIOps


> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.

Apply machine learning to detect anomalies in operational metrics, correlate alerts, and reduce false positives.

## When to Use

- Operations team overwhelmed by alert volume (>100 alerts/day)
- Need to detect complex multi-metric anomalies (not just threshold breaches)
- Seasonal patterns make static thresholds ineffective
- Want to predict issues before they impact users (proactive detection)
- Need to correlate related alerts to identify root cause
- Monitoring system generates too many false positives
- Want to detect subtle performance degradation trends

## Inputs

- **Required**: Time series metrics from monitoring system (CPU, memory, latency, error rate)
- **Required**: Historical data (30-90 days minimum)
- **Optional**: Alert history with labels (true positive / false positive)
- **Optional**: System topology (service dependencies)
- **Optional**: Log data for correlation
- **Optional**: Deployment/change events for context

## Procedure

### Step 1: Set Up Environment and Load Data

Install dependencies and prepare time series data for analysis.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install anomaly detection libraries
pip install prophet scikit-learn pandas numpy
pip install tensorflow keras  # for LSTM models
pip install pyod  # Python Outlier Detection library
pip install statsmodels  # for statistical methods
pip install prometheus-api-client  # if using Prometheus

# Visualization
pip install plotly matplotlib seaborn
```

Load and prepare data:

```python
# aiops/data_loader.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Time series data loaded with regular intervals, missing values handled, features engineered for ML models.

**On failure:** If Prometheus connection fails, verify URL and network access, if data gaps exist use forward-fill or interpolation, ensure timestamp column is datetime type, check for memory issues with large date ranges (process in chunks).

### Step 2: Implement Isolation Forest for Multivariate Anomaly Detection

Detect anomalies using unsupervised Isolation Forest algorithm.

```python
# aiops/isolation_forest_detector.py
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from typing import Dict, List
import joblib

# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Model trained on historical data, anomalies detected with scores, typically 0.5-2% of points flagged as anomalies.

**On failure:** If too many anomalies (>5%), reduce contamination parameter or retrain on cleaner baseline period, if too few (<0.1%), increase contamination or check feature scaling, verify features have sufficient variance.

### Step 3: Implement Prophet for Time Series Forecasting and Anomaly Detection

Use Facebook Prophet to model seasonality and detect deviations.

```python
# aiops/prophet_detector.py
from prophet import Prophet
import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Prophet models capture daily/weekly seasonality, anomalies detected when actual values fall outside 99% confidence interval, forecasts generated for capacity planning.

**On failure:** If Prophet takes too long (>5 min per metric), reduce history to 30 days or disable weekly_seasonality, if too many false positives increase interval_width to 0.995, if missing seasonal patterns add custom seasonalities, ensure timezone consistency in timestamps.

### Step 4: Correlate Alerts and Identify Root Cause

Group related anomalies and identify potential root causes.

```python
# aiops/alert_correlation.py
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Dict
from datetime import timedelta
import networkx as nx

# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Related anomalies grouped into incidents, root causes identified based on dependency graph, incident summaries generated for investigation.

**On failure:** If all anomalies separate incidents, increase time_window_minutes, if root cause detection unclear define metric_relationships explicitly based on architecture, verify timestamp sorting is correct.

### Step 5: Integrate with Alerting System

Send intelligent alerts with context and suppression of noise.

```python
# aiops/intelligent_alerting.py
import requests
import logging
from typing import Dict, List
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** High-severity incidents trigger PagerDuty pages, medium-severity go to Slack, low-severity logged only, duplicate alerts suppressed within 15-minute window.

**On failure:** Test webhook URLs with curl first, verify severity calculation produces reasonable values (0.5-0.9 range), check rate limiting doesn't suppress all alerts, ensure timezone handling is correct for last_alerts tracking.

### Step 6: Deploy as Continuous Monitoring Service

Set up automated pipeline that runs periodically.

```python
# aiops/monitoring_service.py
import schedule
import time
import logging
from datetime import datetime, timedelta
from data_loader import MetricsDataLoader
from isolation_forest_detector import IsolationForestDetector
from prophet_detector import ProphetAnomalyDetector
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Service runs continuously, detects anomalies every 5 minutes, alerts sent for incidents, logs all activity.

**On failure:** Verify scheduler process stays alive (use systemd/supervisor for production), check Prometheus connectivity, ensure models are loaded successfully, implement dead man's switch alert if service stops running, monitor memory usage (reload models periodically if memory grows).

## Validation

- [ ] Historical data loaded correctly with no missing timestamps
- [ ] Isolation Forest detects known anomalies from test set
- [ ] Prophet models capture daily/weekly seasonality in visualizations
- [ ] Alert correlation groups temporally-related anomalies
- [ ] Root cause detection identifies upstream issues correctly
- [ ] Intelligent alerting suppresses duplicate alerts
- [ ] Severity calculation produces reasonable scores (0.5-0.9)
- [ ] Monitoring service runs continuously without crashes for 7+ days
- [ ] False positive rate < 10% (validated against labeled data)
- [ ] True positive rate > 80% for critical incidents

## Common Pitfalls

- **Training on anomalous data**: Ensure baseline period used for training is clean (no incidents); manually review or use labeled data
- **Ignoring seasonality**: Static models fail on daily/weekly patterns; use Prophet or add time features
- **Too sensitive thresholds**: 99% confidence intervals may flag normal peaks; start with 99.5% and tune based on false positives
- **Not handling missing data**: Gaps in metrics cause model errors; implement robust preprocessing with interpolation
- **Alert fatigue from low severity**: Filter alerts below severity threshold; focus on high-confidence anomalies
- **Ignoring system topology**: Treating all metrics independently misses cascading failures; define dependency relationships
- **Model drift**: Models trained on old data become stale; retrain monthly or when system changes
- **Resource contention**: Running detection on every metric is expensive; prioritize critical services or sample metrics

## Related Skills

- `monitor-model-drift` - Detect when anomaly detection models degrade
- `monitor-data-integrity` - Data quality checks before anomaly detection
- `setup-prometheus-monitoring` - Collect operational metrics
- `forecast-operational-metrics` - Capacity planning with Prophet forecasts
