---
name: gcp-gke-cost-optimization
description: |
  Analyzes and optimizes Google Kubernetes Engine costs through right-sizing resources,
  comparing cluster modes, and implementing autoscaling strategies. Use when analyzing
  GKE spending, comparing Autopilot vs Standard billing models, configuring Spot VMs
  for batch workloads, right-sizing pod resources, setting up budget alerts, or
  tracking cost per service. Includes per-pod billing analysis and resource utilization
  optimization patterns.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Cost Optimization

## Purpose

Reduce GKE spending while maintaining performance and reliability. This skill covers cost analysis, resource right-sizing, cluster mode comparison, and budget monitoring strategies.

## When to Use

Use this skill when you need to:
- Analyze GKE spending and identify cost optimization opportunities
- Compare Autopilot vs Standard billing models for your workload
- Right-size pod resource requests and limits
- Configure Horizontal/Vertical Pod Autoscaling to reduce waste
- Set up Spot VMs for batch or non-critical workloads
- Create budget alerts and track cost per service
- Optimize resource utilization

Trigger phrases: "optimize GKE costs", "reduce Kubernetes spending", "right-size resources", "Autopilot vs Standard pricing", "GKE budget alerts"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Understand Your Billing Model](#step-1-understand-your-billing-model)
  - [Step 2: Analyze Current Resource Usage](#step-2-analyze-current-resource-usage)
  - [Step 3: Right-Size Pod Resources](#step-3-right-size-pod-resources)
  - [Step 4: Configure Horizontal Pod Autoscaling](#step-4-configure-horizontal-pod-autoscaling-hpa)
  - [Step 5: Use Spot VMs](#step-5-use-spot-vms-gke-standard-only)
  - [Step 6: Set Up Cost Monitoring](#step-6-set-up-cost-monitoring)
  - [Step 7: Analyze Cost by Namespace/Service](#step-7-analyze-cost-by-namespaceservice)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Analyze and optimize costs in three steps:

```bash
# 1. Check current resource usage
kubectl top pods -n wtr-supplier-charges

# 2. Analyze resource requests vs actual usage
kubectl describe deployment supplier-charges-hub -n wtr-supplier-charges | grep -A 10 "resources:"

# 3. Compare Autopilot vs Standard pricing for your workload
# Autopilot: Pay per pod per second for requests
# Standard: Pay per provisioned node per hour (regardless of usage)
```

## Instructions

### Step 1: Understand Your Billing Model

#### GKE Autopilot (Per-Pod Billing - Recommended)

**Cost Calculation:**
```
Monthly Cost = (vCPU requests * $0.04 + Memory requests GB * $0.004 + Disk GB * $0.0001) * seconds per month
```

**Example for Supplier Charges Hub:**
- 2 replicas, each requesting: 1 vCPU + 2 GB memory
- Monthly cost ≈ (2 * 1 * $0.04 + 2 * 2 * $0.004) * 2.592M seconds ≈ $260

**Advantages:**
- Pay only for what pods request (not what entire cluster capacity is)
- No idle resource costs
- Perfect for variable workloads (scales up/down automatically)
- Up to 60% cheaper than Standard for typical workloads

#### GKE Standard (Node Billing)

**Cost Calculation:**
```
Monthly Cost = Number of nodes * Machine type hourly rate * 730 hours per month
```

**Example for Supplier Charges Hub:**
- 3 `n2-standard-4` nodes (standard pool) = ~$400/month
- Even if pods use only 30% of capacity, you pay for 100%

**Advantages:**
- Predictable costs (great for committed use discounts)
- Full control over infrastructure
- Better for stable, high-utilization workloads

### Step 2: Analyze Current Resource Usage

Check if pods are over-provisioned:

```bash
# View actual vs requested resources
kubectl top pods -n wtr-supplier-charges -o wide

# Compare to requests
kubectl get pods -n wtr-supplier-charges -o jsonpath='{.items[*].spec.containers[*].resources.requests}'
```

**Analysis Questions:**
- Are actual values significantly lower than requests?
- Is memory usage consistently below 75% of limits?
- Is CPU usage consistently below 70% of requests?

**If Yes → Right-size resources (reduce requests)**

### Step 3: Right-Size Pod Resources

Use Vertical Pod Autoscaler (VPA) recommendations:

```bash
# Apply VPA to deployment
cat <<EOF | kubectl apply -f -
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: supplier-charges-hub-vpa
  namespace: wtr-supplier-charges
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: supplier-charges-hub
  updatePolicy:
    updateMode: "Off"  # Only provide recommendations, don't auto-update
  resourcePolicy:
    containerPolicies:
    - containerName: supplier-charges-hub-container
      minAllowed:
        cpu: 500m
        memory: 1Gi
      maxAllowed:
        cpu: 2
        memory: 4Gi
EOF

# Wait 1 week for data collection, then view recommendations
kubectl describe vpa supplier-charges-hub-vpa -n wtr-supplier-charges | grep -A 20 "Recommendation"
```

**Recommended VPA Values:**
```yaml
resources:
  requests:
    cpu: 500m        # Reduced from 1000m if usage averages 300m
    memory: 1.5Gi    # Reduced from 2Gi if usage averages 1Gi
  limits:
    cpu: 500m        # Match requests for Guaranteed QoS
    memory: 1.5Gi
```

### Step 4: Configure Horizontal Pod Autoscaling (HPA)

Let Kubernetes scale replicas based on demand:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: supplier-charges-hub-hpa
  namespace: wtr-supplier-charges
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: supplier-charges-hub
  minReplicas: 1          # Scale down to 1 during low traffic
  maxReplicas: 5          # Scale up to 5 during peak
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

**Cost Savings:** Reduces off-peak replicas from 2 to 1 = ~30% savings if traffic varies.

### Step 5: Use Spot VMs (GKE Standard Only)

For non-critical or fault-tolerant workloads, use Spot VMs (91% discount):

```bash
# Create Spot node pool
gcloud container node-pools create spot-pool \
  --cluster=shared-gke-standard-01-euw2 \
  --region=europe-west2 \
  --spot \
  --machine-type=n2-standard-4 \
  --num-nodes=2 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=10

# Add toleration to workloads that can run on Spot
tolerations:
- key: cloud.google.com/gke-spot
  operator: Equal
  value: "true"
  effect: NoSchedule
```

**Use Cases:** Batch processing, CI/CD build workers, non-critical background jobs

**Not for:** Production APIs (Supplier Charges Hub should NOT use Spot)

### Step 6: Set Up Cost Monitoring

Create budget alerts:

```bash
# Create budget with 50%, 90%, 100% thresholds
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="GKE Labs Environment" \
  --budget-amount=500USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100 \
  --notification-rule-name=email-alert
```

### Step 7: Analyze Cost by Namespace/Service

Export billing data for detailed analysis:

```bash
# Tag namespace for cost tracking
kubectl label namespace wtr-supplier-charges \
  cost-center=supplier-charges \
  environment=labs

# Later, filter GCP Billing reports by labels
# In Cloud Console: Billing → Reports → Filter by labels
```

## Examples

### Example 1: Optimize Supplier Charges Hub Deployment

```bash
#!/bin/bash
# Step-by-step optimization

DEPLOYMENT="supplier-charges-hub"
NAMESPACE="wtr-supplier-charges"

echo "=== GKE Cost Optimization ==="

echo ""
echo "1. Current Resource Usage:"
kubectl top pods -l app=$DEPLOYMENT -n $NAMESPACE

echo ""
echo "2. Current Resource Requests:"
kubectl get deployment $DEPLOYMENT -n $NAMESPACE \
  -o jsonpath='{.spec.template.spec.containers[0].resources}'

echo ""
echo "3. Applying VPA for recommendations:"
cat <<EOF | kubectl apply -f -
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ${DEPLOYMENT}-vpa
  namespace: $NAMESPACE
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: $DEPLOYMENT
  updatePolicy:
    updateMode: "Off"
EOF

echo "VPA created. Wait 1 week for recommendations."

echo ""
echo "4. Applying HPA for automatic scaling:"
cat <<EOF | kubectl apply -f -
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ${DEPLOYMENT}-hpa
  namespace: $NAMESPACE
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: $DEPLOYMENT
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
EOF

echo "HPA created. Replicas will auto-scale based on demand."

echo ""
echo "5. Estimated Savings:"
echo "   - Autopilot: ~$260/month (current)"
echo "   - With HPA (avg 1.5 replicas): ~$195/month"
echo "   - Savings: ~$65/month (25%)"
```

### Example 2: Autopilot vs Standard Cost Comparison

```bash
#!/bin/bash
# Compare pricing for your workload

# Supplier Charges Hub specifications
REPLICAS=2
CPU_PER_POD="1000m"
MEMORY_PER_POD="2Gi"
DISK_PER_POD="10Gi"

# Autopilot pricing (europe-west2)
CPU_PRICE=0.04
MEMORY_PRICE=0.004
DISK_PRICE=0.0001
SECONDS_PER_MONTH=2592000

TOTAL_CPU=$(echo "$REPLICAS * 1" | bc)
TOTAL_MEMORY=$(echo "$REPLICAS * 2" | bc)
TOTAL_DISK=$(echo "$REPLICAS * 10" | bc)

AUTOPILOT_COST=$(echo "($TOTAL_CPU * $CPU_PRICE + $TOTAL_MEMORY * $MEMORY_PRICE + $TOTAL_DISK * $DISK_PRICE) * $SECONDS_PER_MONTH / 3600 / 24 / 30" | bc)

echo "=== Cost Comparison: Autopilot vs Standard ==="
echo ""
echo "Workload: $REPLICAS replicas, ${CPU_PER_POD}m CPU, ${MEMORY_PER_POD} memory each"
echo ""
echo "AUTOPILOT (Per-Pod Billing):"
echo "  Monthly cost: ~\$${AUTOPILOT_COST}"
echo ""
echo "STANDARD (Node-Based Billing):"
echo "  3x n2-standard-4 nodes @ \$400/month"
echo "  3x cloud-sql-proxy sidecars @ \$50/month"
echo "  Total: ~\$450/month"
echo ""
echo "SAVINGS with Autopilot: ~\$190/month (42%)"
```

### Example 3: Set Up Cost Tracking and Alerts

```bash
#!/bin/bash
# Set up cost monitoring

BILLING_ACCOUNT="000000-A1B2C3-D4E5F6"  # Replace with your billing account
NAMESPACE="wtr-supplier-charges"
PROJECT_ID="ecp-wtr-supplier-charges-labs"

echo "=== Setting Up Cost Monitoring ==="

echo ""
echo "1. Tag resources for cost tracking"
kubectl label namespace $NAMESPACE \
  cost-center=supplier-charges \
  environment=labs \
  --overwrite

echo ""
echo "2. Create billing budget"
gcloud billing budgets create \
  --billing-account=$BILLING_ACCOUNT \
  --display-name="GKE Labs - Supplier Charges Hub" \
  --budget-amount=500USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100 \
  --notification-rule-name="Budget Alert"

echo ""
echo "3. Enable Cost Analysis"
echo "   Go to: https://console.cloud.google.com/billing/reports"
echo "   Filter by: labels.cost-center = supplier-charges"

echo ""
echo "4. Track GKE Costs"
echo "   Go to: https://console.cloud.google.com/monitoring/dashboards"
echo "   Create dashboard filtering: resource.type=k8s_cluster AND resource.labels.cluster_name"
```

## Requirements

- GKE cluster running (Autopilot or Standard)
- `kubectl` access to view pod metrics and deployments
- `gcloud` CLI access for billing and monitoring setup
- Metrics server enabled (usually on by default)
- For billing: access to GCP billing account

## See Also

- [gcp-gke-cluster-setup](../gcp-gke-cluster-setup/SKILL.md) - Understand cluster modes and their costs
- [gcp-gke-deployment-strategies](../gcp-gke-deployment-strategies/SKILL.md) - Optimize deployment replicas
- [gcp-gke-monitoring-observability](../gcp-gke-monitoring-observability/SKILL.md) - Monitor resource utilization
