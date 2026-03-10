---
name: deploy-ml-model-serving
description: >
  Deploy machine learning models to production serving infrastructure using MLflow,
  BentoML, or Seldon Core with REST/gRPC endpoints, implement autoscaling, monitoring,
  and A/B testing capabilities for high-performance model inference at scale. Use when
  deploying trained models for real-time inference, setting up REST or gRPC prediction
  APIs, implementing autoscaling for variable load, running A/B tests between model
  versions, or migrating from batch to real-time inference.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: mlops
  complexity: advanced
  language: multi
  tags: model-serving, bentoml, seldon, rest-api, grpc
---

# Deploy ML Model Serving


> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.

Deploy machine learning models to production with scalable serving infrastructure, monitoring, and A/B testing.

## When to Use

- Deploying trained models to production for real-time inference
- Setting up REST or gRPC APIs for model predictions
- Implementing autoscaling for variable load patterns
- Running A/B tests between model versions
- Migrating from batch to real-time inference
- Building low-latency prediction services
- Managing multiple model versions in production

## Inputs

- **Required**: Registered model in MLflow Model Registry or trained model artifact
- **Required**: Kubernetes cluster or container orchestration platform
- **Required**: Serving framework choice (MLflow, BentoML, Seldon Core, TorchServe)
- **Optional**: GPU resources for deep learning models
- **Optional**: Monitoring infrastructure (Prometheus, Grafana)
- **Optional**: Load balancer and ingress controller

## Procedure

### Step 1: Deploy with MLflow Models Serving

Use MLflow's built-in serving for quick deployment of scikit-learn, PyTorch, and TensorFlow models.

```bash
# Serve model locally for testing
mlflow models serve \
  --model-uri models:/customer-churn-classifier/Production \
  --port 5001 \
  --host 0.0.0.0

# Test endpoint
curl -X POST http://localhost:5001/invocations \
  -H 'Content-Type: application/json' \
  -d '{
    "dataframe_records": [
      {"feature1": 1.0, "feature2": 2.0, "feature3": 3.0}
    ]
  }'
```

Docker deployment:

```dockerfile
# Dockerfile.mlflow-serving
FROM python:3.9-slim

# Install MLflow and dependencies
RUN pip install mlflow boto3 scikit-learn

# Set environment variables
ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000
# ... (see EXAMPLES.md for complete implementation)
```

Docker Compose for local testing:

```yaml
# docker-compose.mlflow-serving.yml
version: '3.8'

services:
  model-server:
    build:
      context: .
      dockerfile: Dockerfile.mlflow-serving
# ... (see EXAMPLES.md for complete implementation)
```

Test the deployment:

```python
# test_mlflow_serving.py
import requests
import json

def test_prediction():
    url = "http://localhost:8080/invocations"

    # Prepare input data
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Model server starts successfully, responds to HTTP POST requests, returns predictions in JSON format, Docker container runs without errors.

**On failure:** Check model URI is valid (`mlflow models list`), verify MLflow tracking server accessibility, ensure all model dependencies installed in container, check port availability (`netstat -tulpn | grep 8080`), verify model flavor compatibility, inspect container logs (`docker logs <container-id>`).

### Step 2: Deploy with BentoML for Production Scale

Use BentoML for advanced serving with better performance and features.

```python
# bentoml_service.py
import bentoml
from bentoml.io import JSON, NumpyNdarray
import numpy as np
import pandas as pd

# Load model from MLflow
import mlflow
# ... (see EXAMPLES.md for complete implementation)
```

Build and containerize:

```bash
# Build Bento
bentoml build

# Containerize
bentoml containerize customer_churn_classifier:latest \
  --image-tag customer-churn:v1.0

# Run container
docker run -p 3000:3000 customer-churn:v1.0
```

BentoML configuration:

```yaml
# bentofile.yaml
service: "bentoml_service:ChurnPredictionService"
include:
  - "bentoml_service.py"
  - "preprocessing.py"
python:
  packages:
    - scikit-learn==1.0.2
    - pandas==1.4.0
    - numpy==1.22.0
    - mlflow==2.0.1
docker:
  distro: debian
  python_version: "3.9"
  cuda_version: null  # Set to "11.6" for GPU support
```

Kubernetes deployment:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-prediction
  labels:
    app: churn-prediction
spec:
# ... (see EXAMPLES.md for complete implementation)
```

Deploy to Kubernetes:

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Test endpoint
EXTERNAL_IP=$(kubectl get svc churn-prediction-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -X POST http://$EXTERNAL_IP/predict \
  -H 'Content-Type: application/json' \
  -d '{"instances": [{"tenure": 12, "monthly_charges": 70.35}]}'
```

**Expected:** BentoML service builds successfully, container runs and serves predictions, Kubernetes deployment creates 3 replicas, load balancer exposes external endpoint, health checks pass.

**On failure:** Verify BentoML installation (`bentoml --version`), check model exists in BentoML store (`bentoml models list`), ensure Docker daemon running, verify Kubernetes cluster access (`kubectl cluster-info`), check resource limits not exceeded, inspect pod logs (`kubectl logs <pod-name>`), verify service selector matches pod labels.

### Step 3: Implement Seldon Core for Advanced Features

Use Seldon Core for multi-model serving, A/B testing, and explainability.

```python
# seldon_wrapper.py
import logging
from typing import Dict, List, Union
import numpy as np
import mlflow

logger = logging.getLogger(__name__)

# ... (see EXAMPLES.md for complete implementation)
```

Seldon deployment configuration:

```yaml
# seldon-deployment.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: churn-classifier
  namespace: seldon
spec:
  name: churn-classifier
# ... (see EXAMPLES.md for complete implementation)
```

A/B testing configuration:

```yaml
# seldon-ab-test.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: churn-classifier-ab
spec:
  name: churn-classifier-ab
  predictors:
# ... (see EXAMPLES.md for complete implementation)
```

Deploy to Kubernetes:

```bash
# Install Seldon Core operator
kubectl create namespace seldon-system
helm install seldon-core seldon-core-operator \
  --repo https://storage.googleapis.com/seldon-charts \
  --namespace seldon-system \
  --set usageMetrics.enabled=true

# Create namespace for models
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Seldon Core operator installed successfully, model deployment creates pods, REST endpoint responds to predictions, A/B test splits traffic correctly, Seldon Analytics records metrics.

**On failure:** Verify Seldon Core operator running (`kubectl get pods -n seldon-system`), check SeldonDeployment status (`kubectl describe seldondeployment`), ensure image registry accessible from cluster, verify model URI resolution, check RBAC permissions for Seldon operator, inspect model container logs.

### Step 4: Implement Monitoring and Observability

Add comprehensive monitoring for model serving infrastructure.

```python
# monitoring.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import logging

logger = logging.getLogger(__name__)

# Prometheus metrics
# ... (see EXAMPLES.md for complete implementation)
```

Prometheus configuration:

```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'model-serving'
    kubernetes_sd_configs:
# ... (see EXAMPLES.md for complete implementation)
```

Grafana dashboard JSON:

```json
{
  "dashboard": {
    "title": "ML Model Serving Metrics",
    "panels": [
      {
        "title": "Predictions Per Second",
        "targets": [
          {
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Prometheus scrapes metrics successfully, Grafana dashboards display prediction throughput, latency percentiles, error rates, and active requests in real-time.

**On failure:** Verify Prometheus scrape targets are UP (`http://prometheus:9090/targets`), check metrics endpoint accessibility (`curl http://model-pod:8000/metrics`), ensure Kubernetes service discovery configured, verify Grafana data source connection, check firewall rules for metrics port.

### Step 5: Implement Autoscaling

Configure horizontal pod autoscaling based on request load.

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: churn-prediction-hpa
  namespace: seldon
spec:
  scaleTargetRef:
# ... (see EXAMPLES.md for complete implementation)
```

Apply autoscaling:

```bash
# Enable metrics server (if not already installed)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Apply HPA
kubectl apply -f hpa.yaml

# Check HPA status
kubectl get hpa -n seldon
kubectl describe hpa churn-prediction-hpa -n seldon

# Load test to trigger scaling
kubectl run -it --rm load-generator --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://churn-prediction-service/predict; done"

# Watch scaling
kubectl get hpa -n seldon --watch
```

**Expected:** HPA monitors CPU/memory/custom metrics, scales replicas up under load, scales down after stabilization period, min/max replica limits respected.

**On failure:** Verify metrics-server running (`kubectl get deployment metrics-server -n kube-system`), check pod resource requests defined (HPA requires requests), ensure custom metrics available if used, verify RBAC permissions for HPA controller, check stabilization windows not too restrictive.

### Step 6: Implement Canary Deployment Strategy

Gradually roll out new model versions with traffic shifting.

```yaml
# canary-deployment.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: churn-classifier-canary
spec:
  name: churn-classifier-canary
  predictors:
# ... (see EXAMPLES.md for complete implementation)
```

Gradual rollout script:

```python
# canary_rollout.py
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Canary deployment starts with 0% traffic, gradual traffic shift occurs automatically, health checks pass at each stage, rollback triggered if metrics degrade, complete rollout after all stages pass.

**On failure:** Verify Seldon deployment has multiple predictors, check traffic percentages sum to 100, ensure canary image exists and is pullable, verify Prometheus metrics available for health checks, check rollback logic executes correctly, inspect pod logs for both versions.

## Validation

- [ ] Model server responds to prediction requests
- [ ] REST/gRPC endpoints functional and documented
- [ ] Docker containers build and run successfully
- [ ] Kubernetes deployment creates expected replicas
- [ ] Load balancer exposes external endpoint
- [ ] Health checks (liveness/readiness) pass
- [ ] Prometheus metrics exported and scraped
- [ ] Grafana dashboards display real-time metrics
- [ ] Autoscaling triggers under load
- [ ] A/B test splits traffic correctly
- [ ] Canary deployment rolls out gradually
- [ ] Rollback works when canary fails

## Common Pitfalls

- **Cold start latency**: First request slow due to model loading - use readiness probes with adequate delay, implement model caching
- **Memory leaks**: Long-running servers accumulate memory - monitor memory usage, implement periodic restarts, profile code
- **Dependency conflicts**: Model dependencies incompatible with serving framework - use exact pinned versions, test in Docker before deployment
- **Resource limits too low**: Pods OOMKilled or CPU throttled - profile resource usage, set appropriate limits based on load testing
- **Missing health checks**: Kubernetes routes traffic to unhealthy pods - implement proper liveness/readiness probes
- **No rollback strategy**: Bad deployment without easy rollback - use canary deployments, keep previous version available
- **Ignoring latency**: Focusing only on accuracy, not inference speed - benchmark latency, optimize model/code, use batching
- **Single replica**: No high availability, downtime during deployments - use min 2 replicas, configure anti-affinity
- **No monitoring**: Issues not detected until customers complain - implement comprehensive metrics from day one
- **GPU not utilized**: GPU available but not used - set CUDA visible devices, verify GPU allocation in Kubernetes

## Related Skills

- `register-ml-model` - Register models before deploying them
- `run-ab-test-models` - Implement A/B testing between model versions
- `deploy-to-kubernetes` - General Kubernetes deployment patterns
- `monitor-ml-model-performance` - Monitor model drift and degradation
- `orchestrate-ml-pipeline` - Automate model retraining and deployment
