---
name: gcp-gke-deployment-strategies
description: |
  Implements zero-downtime deployments on GKE using rolling updates, blue-green
  strategies, and health checks. Use when deploying new versions, rolling back failed
  deployments, configuring Spring Boot health probes (liveness/readiness), managing
  rollout status, or implementing progressive rollout patterns. Includes automated
  health verification and rollback procedures.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Deployment Strategies

## Purpose

Deploy applications to GKE with zero-downtime updates using rolling deployments and health checks. This skill covers deployment configuration, monitoring rollout progress, rollback procedures, and Spring Boot health probe integration.

## When to Use

Use this skill when you need to:
- Deploy a new version of an application to GKE
- Configure rolling update strategies for zero-downtime deployments
- Set up liveness and readiness probes for Spring Boot apps
- Monitor rollout progress and verify deployment health
- Roll back failed deployments
- Implement blue-green deployment patterns
- Debug deployment issues

Trigger phrases: "deploy to GKE", "rolling update", "rollback deployment", "configure health probes", "zero-downtime deployment"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Configure Rolling Update Strategy](#step-1-configure-rolling-update-strategy)
  - [Step 2: Configure Spring Boot Health Probes](#step-2-configure-spring-boot-health-probes)
  - [Step 3: Deploy Application](#step-3-deploy-application)
  - [Step 4: Monitor Rollout Progress](#step-4-monitor-rollout-progress)
  - [Step 5: Verify Health Checks Passing](#step-5-verify-health-checks-passing)
  - [Step 6: View Rollout History](#step-6-view-rollout-history)
  - [Step 7: Rollback If Needed](#step-7-rollback-if-needed)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Standard zero-downtime rolling update:

```bash
# 1. Configure rolling update strategy
kubectl apply -f deployment.yaml  # With maxSurge: 50%, maxUnavailable: 0%

# 2. Update image
kubectl set image deployment/supplier-charges-hub \
  supplier-charges-hub-container=new-image:v2.0.0 \
  -n wtr-supplier-charges

# 3. Monitor rollout
kubectl rollout status deployment/supplier-charges-hub \
  -n wtr-supplier-charges

# 4. Verify (or rollback if needed)
kubectl rollout undo deployment/supplier-charges-hub \
  -n wtr-supplier-charges
```

## Instructions

### Step 1: Configure Rolling Update Strategy

Set up zero-downtime deployments with proper surge and unavailability settings:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-hub
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 50%          # Can create 1 extra pod (2 * 50% = 1)
      maxUnavailable: 0%     # Zero downtime - no pods removed until new ones ready
  minReadySeconds: 10        # Wait 10s after pod is ready before proceeding
  progressDeadlineSeconds: 300  # Fail rollout if not complete in 5 min
  revisionHistoryLimit: 3    # Keep last 3 revisions for rollback
  selector:
    matchLabels:
      app: supplier-charges-hub
  template:
    metadata:
      labels:
        app: supplier-charges-hub
    spec:
      containers:
      - name: supplier-charges-hub-container
        image: europe-west2-docker.pkg.dev/.../supplier-charges-hub:latest
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 15
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 15
          failureThreshold: 3
```

**Strategy Explanation:**
- `maxSurge: 50%` - Allows 1 extra pod during rollout (temporary spike in resources)
- `maxUnavailable: 0%` - No pods removed until replacement is ready (zero downtime)
- `minReadySeconds: 10` - Prevents premature progression if pod is flaky
- `progressDeadlineSeconds: 300` - Detects stuck rollouts after 5 minutes

### Step 2: Configure Spring Boot Health Probes

Enable Spring Boot Actuator health endpoints that Kubernetes will check:

```yaml
# application.yml
management:
  endpoint:
    health:
      probes:
        enabled: true
      show-details: always
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
```

**Health Endpoint Distinctions:**

| Probe | Path | Purpose | Failure Action |
|-------|------|---------|----------------|
| **Liveness** | `/actuator/health/liveness` | Is the app broken? | Restart pod |
| **Readiness** | `/actuator/health/readiness` | Can the app serve requests? | Stop traffic |
| **Startup** | `/actuator/health/liveness` | Slow startup complete? | Wait before liveness checks |

### Step 3: Deploy Application

Apply your deployment manifest:

```bash
kubectl apply -f deployment.yaml -n wtr-supplier-charges
```

Kubernetes will immediately start the rollout with your configured strategy.

### Step 4: Monitor Rollout Progress

Track the deployment update in real-time:

```bash
# Watch rollout status (blocks until complete)
kubectl rollout status deployment/supplier-charges-hub \
  -n wtr-supplier-charges \
  --timeout=5m

# Or check status without waiting
kubectl get deployment supplier-charges-hub \
  -n wtr-supplier-charges \
  -o wide
```

**Expected Output During Rollout:**
```
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
supplier-charges-hub   2/2     1            2           5m
  # Shows: 1 new pod being created, 2 old pods still serving traffic
```

### Step 5: Verify Health Checks Passing

Check that pods are actually ready:

```bash
# View detailed pod status
kubectl get pods -n wtr-supplier-charges -o wide

# Check health probe status
kubectl describe pod <pod-name> -n wtr-supplier-charges | grep -A 5 "Readiness"

# Test health endpoint manually
kubectl exec deployment/supplier-charges-hub -n wtr-supplier-charges -- \
  curl -s localhost:8080/actuator/health/readiness | jq .
```

### Step 6: View Rollout History

Track previous deployments for rollback capability:

```bash
# List all revisions
kubectl rollout history deployment/supplier-charges-hub \
  -n wtr-supplier-charges

# Details of specific revision
kubectl rollout history deployment/supplier-charges-hub \
  -n wtr-supplier-charges \
  --revision=1
```

### Step 7: Rollback If Needed

If deployment fails or has issues, quickly rollback:

```bash
# Rollback to previous version
kubectl rollout undo deployment/supplier-charges-hub \
  -n wtr-supplier-charges

# Rollback to specific revision
kubectl rollout undo deployment/supplier-charges-hub \
  -n wtr-supplier-charges \
  --to-revision=2

# Monitor rollback status
kubectl rollout status deployment/supplier-charges-hub \
  -n wtr-supplier-charges
```

## Examples

### Example 1: Complete Deployment with Rolling Update

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-hub
  namespace: wtr-supplier-charges
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 50%
      maxUnavailable: 0%
  minReadySeconds: 10
  progressDeadlineSeconds: 300
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: supplier-charges-hub
  template:
    metadata:
      labels:
        app: supplier-charges-hub
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      serviceAccountName: app-runtime
      containers:
      - name: supplier-charges-hub-container
        image: europe-west2-docker.pkg.dev/ecp-artifact-registry/wtr-supplier-charges-container-images/supplier-charges-hub:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "labs"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: http
            scheme: HTTP
          initialDelaySeconds: 20
          periodSeconds: 15
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: http
            scheme: HTTP
          initialDelaySeconds: 20
          periodSeconds: 15
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 1000m
            memory: 2Gi
        securityContext:
          runAsNonRoot: true
          allowPrivilegeEscalation: false
      - name: cloud-sql-proxy
        image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.11.4
        args:
        - "--structured-logs"
        - "--port=5432"
        - "--auto-iam-authn"
        - "$(DB_CONNECTION_NAME)"
        env:
        - name: DB_CONNECTION_NAME
          valueFrom:
            configMapKeyRef:
              name: db-config
              key: DB_CONNECTION_NAME
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
          limits:
            cpu: 250m
            memory: 256Mi
        securityContext:
          runAsNonRoot: true
          allowPrivilegeEscalation: false
```

Deploy it:
```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/supplier-charges-hub -n wtr-supplier-charges
```

### Example 2: Automated Deployment Update

```bash
#!/bin/bash
# Update deployment with automated rollback on failure

DEPLOYMENT="supplier-charges-hub"
NAMESPACE="wtr-supplier-charges"
IMAGE="europe-west2-docker.pkg.dev/ecp-artifact-registry/wtr-supplier-charges-container-images/supplier-charges-hub:${1:-latest}"

echo "Deploying: $IMAGE"

# Update image
kubectl set image deployment/$DEPLOYMENT \
  supplier-charges-hub-container=$IMAGE \
  -n $NAMESPACE

# Wait for rollout with timeout
if kubectl rollout status deployment/$DEPLOYMENT \
  -n $NAMESPACE \
  --timeout=5m; then
  echo "Deployment successful!"
  exit 0
else
  echo "Deployment failed! Rolling back..."
  kubectl rollout undo deployment/$DEPLOYMENT -n $NAMESPACE
  kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE
  exit 1
fi
```

### Example 3: Blue-Green Deployment (Advanced)

```bash
#!/bin/bash
# Blue-green deployment for zero-risk updates

BLUE_VERSION="v1.2.2"
GREEN_VERSION="v1.2.3"
SERVICE="supplier-charges-hub"
NAMESPACE="wtr-supplier-charges"

echo "Deploying GREEN version: $GREEN_VERSION"

# Deploy green version (separate deployment)
kubectl apply -f deployment-green.yaml

# Verify green is healthy
echo "Waiting for green deployment to be ready..."
kubectl rollout status deployment/supplier-charges-hub-green \
  -n $NAMESPACE \
  --timeout=5m

# Test green version via separate service/ingress
echo "Testing green version..."
GREEN_POD=$(kubectl get pods -l version=green -n $NAMESPACE -o jsonpath='{.items[0].metadata.name}')
kubectl exec $GREEN_POD -n $NAMESPACE -- \
  curl -s localhost:8080/actuator/health/readiness

# Switch traffic to green by updating service selector
echo "Switching traffic from BLUE to GREEN..."
kubectl patch service $SERVICE \
  -n $NAMESPACE \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Verify
echo "Verifying GREEN is serving traffic..."
kubectl get endpoints $SERVICE -n $NAMESPACE

# Keep blue around for quick rollback
echo "Blue version $BLUE_VERSION still available for immediate rollback"
```

### Example 4: Health Probe Debugging

```bash
#!/bin/bash
# Debug health check issues

POD="$1"
NAMESPACE="wtr-supplier-charges"

if [ -z "$POD" ]; then
  POD=$(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[0].metadata.name}')
fi

echo "=== Health Probe Configuration ==="
kubectl describe pod $POD -n $NAMESPACE | grep -A 15 "Probes"

echo ""
echo "=== Testing Liveness Probe Endpoint ==="
kubectl exec $POD -n $NAMESPACE -- \
  curl -v http://localhost:8080/actuator/health/liveness

echo ""
echo "=== Testing Readiness Probe Endpoint ==="
kubectl exec $POD -n $NAMESPACE -- \
  curl -v http://localhost:8080/actuator/health/readiness

echo ""
echo "=== Full Health Status ==="
kubectl exec $POD -n $NAMESPACE -- \
  curl -s http://localhost:8080/actuator/health | jq .
```

## Requirements

- GKE cluster with running pods
- Spring Boot application with Actuator enabled (endpoints exposed)
- `kubectl` access to the cluster
- Deployment resource already created
- Health endpoints accessible on port 8080 (customizable)

## See Also

- [gcp-gke-cluster-setup](../gcp-gke-cluster-setup/SKILL.md) - Understand cluster configuration
- [gcp-gke-troubleshooting](../gcp-gke-troubleshooting/SKILL.md) - Debug deployment issues
- [gcp-gke-monitoring-observability](../gcp-gke-monitoring-observability/SKILL.md) - Monitor deployments
