---
name: fastapi-streamlit
description: Dual skill for deploying scientific models. FastAPI provides a high-performance, asynchronous web framework for building APIs with automatic documentation. Streamlit enables rapid creation of interactive data applications and dashboards directly from Python scripts. Load when working with web APIs, model serving, REST endpoints, interactive dashboards, data visualization UIs, scientific app deployment, async web frameworks, Pydantic validation, uvicorn, or building production-ready scientific tools.
version: FastAPI 0.109 / Streamlit 1.31
license: MIT / Apache-2.0
---

# FastAPI & Streamlit - Deployment & Interaction

This combination allows scientists to move from a Jupyter Notebook to a production-ready system. FastAPI handles the backend (model serving, data processing), while Streamlit provides the frontend (interactive widgets, real-time plotting).

## FIRST: Verify Prerequisites

```bash
pip install fastapi uvicorn streamlit pydantic
```

## When to Use

### FastAPI:
- Serving Machine Learning models as REST APIs.
- Creating microservices for heavy scientific computations.
- Building backends that require high concurrency (async/await).
- Automatically generating API documentation (Swagger/Redoc).

### Streamlit:
- Building interactive dashboards for data exploration.
- Creating "Apps" to demonstrate scientific results to non-technical stakeholders.
- Rapid prototyping of UIs for internal tools.
- Visualizing complex datasets with interactive sliders, maps, and charts.

## Reference Documentation

- FastAPI docs: https://fastapi.tiangolo.com/
- Streamlit docs: https://docs.streamlit.io/
- Search patterns: `fastapi.app`, `pydantic.BaseModel`, `st.slider`, `st.cache_data`, `st.sidebar`

## Core Principles

### FastAPI: Type Safety and Async
FastAPI is built on Pydantic for data validation and Starlette for web capabilities. Every input is validated against Python type hints. It is one of the fastest Python frameworks thanks to async/await.

### Streamlit: Execution Model
Streamlit scripts run from top to bottom every time a user interacts with a widget. It uses a "magic" caching system to prevent expensive scientific functions from re-running unnecessarily.

## Quick Reference

### Installation

```bash
pip install fastapi uvicorn streamlit pydantic
```

### Standard Imports

```python
# FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Streamlit
import streamlit as st
import requests # To communicate with FastAPI
```

### Basic Pattern - FastAPI Model Server

```python
# main_api.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModelInput(BaseModel):
    temperature: float
    pressure: float

@app.post("/predict")
def predict(data: ModelInput):
    # Imagine a complex physical model here
    result = data.temperature * 0.5 + data.pressure * 0.2
    return {"prediction": result}

# Run with: uvicorn main_api:app --reload
```

### Basic Pattern - Streamlit Dashboard

```python
# main_ui.py
import streamlit as st
import pandas as pd

st.title("Scientific Data Explorer")

# 1. Widgets for input
val = st.slider("Select a threshold", 0.0, 100.0, 50.0)

# 2. Logic/Processing
df = pd.DataFrame({"x": range(100), "y": [x**2 for x in range(100)]})
filtered_df = df[df["y"] > val]

# 3. Visualization
st.line_chart(filtered_df)
st.write(f"Points above threshold: {len(filtered_df)}")

# Run with: streamlit run main_ui.py
```

## Critical Rules

### ✅ DO

- **Use Pydantic Schemas (FastAPI)** - Always define your API inputs and outputs using classes inheriting from `BaseModel`.
- **Use st.cache_data (Streamlit)** - Wrap heavy data loading or heavy math functions with `@st.cache_data` to keep the UI responsive.
- **Use Async/Await (FastAPI)** - For I/O bound tasks (database, API calls), use `async def` to maximize throughput.
- **Set Page Config (Streamlit)** - Use `st.set_page_config(layout="wide")` for scientific dashboards that need space for plots.
- **Handle Exceptions** - Use FastAPI's `HTTPException` to return clear error codes (400, 404, 500) to the user.
- **Modularize** - Keep your scientific logic in a separate file/package, imported by both API and UI.

### ❌ DON'T

- **Don't Run Heavy Logic in UI Thread** - In Streamlit, if a function takes >1s, it must be cached or the UI will feel broken.
- **Don't Block the Async Loop (FastAPI)** - If a function is CPU-intensive (e.g., heavy NumPy math), use standard `def` instead of `async def`; FastAPI will run it in a thread pool.
- **Don't Store Sensitive Data in UI Code** - Use environment variables or `.streamlit/secrets.toml`.
- **Don't Over-nest Widgets** - Streamlit's "top-down" execution gets confusing if the UI logic is too complex.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Manual JSON parsing in FastAPI
# @app.post("/data")
# def handle_data(raw_json: dict):
#     val = raw_json.get("value") # No validation!

# ✅ GOOD: Pydantic validation
class DataPoint(BaseModel):
    value: float

@app.post("/data")
def handle_data(data: DataPoint):
    return data.value # Guaranteed to be a float

# ❌ BAD: Loading data in every Streamlit rerun
# data = pd.read_csv("massive_data.csv") # Re-reads every time you move a slider!

# ✅ GOOD: Caching
@st.cache_data
def load_massive_data():
    return pd.read_csv("massive_data.csv")

data = load_massive_data()
```

## FastAPI: Advanced Features

### Dependency Injection (e.g., Database/Model loading)

```python
from functools import lru_cache

@lru_cache()
def load_model():
    # Load your PyTorch or Scikit-learn model here
    return MyHeavyModel().load("weights.pt")

@app.get("/status")
def get_status(model = Depends(load_model)):
    return {"model_version": model.version}
```

### Background Tasks (Long-running computations)

```python
from fastapi import BackgroundTasks

def solve_pde_task(params):
    # Long FEniCS simulation
    pass

@app.post("/run-sim")
def run_simulation(params: Params, background_tasks: BackgroundTasks):
    background_tasks.add_task(solve_pde_task, params)
    return {"message": "Simulation started in background"}
```

## Streamlit: Layout and Interaction

### Multi-column and Sidebars

```python
st.sidebar.header("Settings")
mode = st.sidebar.selectbox("Model Mode", ["Fast", "Accurate"])

col1, col2 = st.columns(2)

with col1:
    st.header("Input Parameters")
    temp = st.number_input("Temperature (K)")

with col2:
    st.header("Results Visualization")
    # Plotly/Matplotlib chart
    st.plotly_chart(fig)
```

### Session State (Keeping track of user data)

```python
if 'results_history' not in st.session_state:
    st.session_state.results_history = []

if st.button("Run Experiment"):
    res = run_model()
    st.session_state.results_history.append(res)

st.write(f"History length: {len(st.session_state.results_history)}")
```

## Practical Workflows

### 1. Scientific Model Serving (FastAPI + PyTorch)

```python
import torch
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = torch.load("model.pth")
model.eval()

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/v1/predict")
def get_prediction(req: PredictionRequest):
    input_tensor = torch.tensor([req.features])
    with torch.no_grad():
        output = model(input_tensor)
    return {"class": output.argmax().item(), "confidence": output.max().item()}
```

### 2. Interactive Data Cleaning Tool (Streamlit + Polars)

```python
import streamlit as st
import polars as pl

st.title("Data Cleaner")
uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file:
    df = pl.read_csv(uploaded_file)
    
    st.write("Original Data Summary", df.describe())
    
    col_to_drop = st.multiselect("Drop columns", df.columns)
    if st.button("Clean Data"):
        df_clean = df.drop(col_to_drop).drop_nulls()
        st.dataframe(df_clean)
        st.download_button("Download Clean CSV", df_clean.write_csv(), "clean.csv")
```

### 3. Real-time Monitoring App

```python
import streamlit as st
import time

placeholder = st.empty()

for i in range(100):
    with placeholder.container():
        st.metric("Current Sensor Reading", f"{get_val()} units")
        st.progress(i + 1)
    time.sleep(1)
```

## Performance Optimization

### 1. FastAPI: Uvicorn Workers

For production, run with multiple workers to handle more requests.

```bash
uvicorn main:app --workers 4
```

### 2. Streamlit: st.cache_resource

Use `cache_resource` for objects that should stay in memory across users/sessions, like Database connections or ML models.

```python
@st.cache_resource
def get_database_connection():
    return create_engine("postgresql://...")
```

### 3. Streamlit: PyArrow

Streamlit uses Apache Arrow for data exchange. Ensuring your data is in Arrow-compatible formats (like Polars or Pandas) makes UI rendering instant.

## Common Pitfalls and Solutions

### FastAPI: Input Data Validation Errors

If a user sends a string where a float is expected, FastAPI returns 422 Unprocessable Entity.

```python
# ✅ Solution: Wrap Pydantic models in try-except if needed, 
# but usually, let FastAPI handle it and customize exception_handlers.
```

### Streamlit: The "Double Rerun"

Sometimes widgets trigger multiple reruns.

```python
# ✅ Solution: Use st.form to group widgets so the script 
# only reruns once when the "Submit" button is clicked.
with st.form("my_form"):
    # ... inputs ...
    submitted = st.form_submit_button("Submit")
```

### Deployment Port Conflict

By default, Streamlit uses 8501 and FastAPI (Uvicorn) uses 8000.

```python
# ✅ Solution: Be explicit in Docker/Compose files about ports.
```

## Best Practices

1. **Separate Concerns** - Keep scientific logic separate from API/UI code for reusability
2. **Type Everything** - Use Pydantic models for all FastAPI endpoints to catch errors early
3. **Cache Aggressively** - In Streamlit, cache any computation that takes >100ms
4. **Use Async Wisely** - FastAPI async is great for I/O, but CPU-bound tasks should be sync
5. **Test Both Separately** - Test your FastAPI endpoints with `httpx` or `requests`, test Streamlit UI manually
6. **Document APIs** - FastAPI auto-generates docs, but add docstrings to your Pydantic models
7. **Handle Errors Gracefully** - Both frameworks have good error handling; use it
8. **Monitor Performance** - Use FastAPI's built-in metrics and Streamlit's execution time display

---

The FastAPI + Streamlit stack is the "Last Mile" of scientific computing. It transforms raw code into accessible tools, making your models useful to the rest of the world.
