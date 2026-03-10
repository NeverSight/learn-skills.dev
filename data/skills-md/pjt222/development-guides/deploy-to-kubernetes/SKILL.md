---
name: deploy-to-kubernetes
description: >
  Deploy applications to Kubernetes clusters using kubectl manifests for Deployments,
  Services, ConfigMaps, Secrets, and Ingress resources. Implement health checks, resource
  limits, rolling updates, and Helm chart packaging for production deployments. Use when
  deploying new applications to EKS, GKE, AKS, or self-hosted clusters, migrating from
  Docker Compose to container orchestration, implementing zero-downtime rolling updates,
  or setting up multi-environment deployments across dev, staging, and production.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: kubernetes, k8s, kubectl, deployment, service
---

# Deploy to Kubernetes

Deploy containerized applications to Kubernetes with production-ready configurations including health checks, resource management, and automated rollouts.

## When to Use

- Deploying new applications to Kubernetes clusters (EKS, GKE, AKS, self-hosted)
- Migrating from Docker Compose or traditional VMs to container orchestration
- Implementing zero-downtime rolling updates and rollbacks
- Managing application configuration and secrets in Kubernetes
- Setting up multi-environment deployments (dev, staging, production)
- Creating reusable Helm charts for application distribution

## Inputs

- **Required**: Kubernetes cluster access (`kubectl cluster-info`)
- **Required**: Container images pushed to registry (Docker Hub, ECR, GCR, Harbor)
- **Required**: Application requirements (ports, environment variables, volumes)
- **Optional**: TLS certificates for HTTPS ingress
- **Optional**: Persistent storage requirements (StatefulSets, PVCs)
- **Optional**: Helm CLI for chart-based deployments

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Create Namespace and Resource Quotas

Organize applications into namespaces with resource limits and RBAC.

```bash
# Create namespace
kubectl create namespace myapp-prod

# Apply resource quota
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: myapp-prod
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    persistentvolumeclaims: "5"
    services.loadbalancers: "2"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: myapp-prod
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    type: Container
EOF

# Create service account
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp
  namespace: myapp-prod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
  namespace: myapp-prod
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-rolebinding
  namespace: myapp-prod
subjects:
- kind: ServiceAccount
  name: myapp
  namespace: myapp-prod
roleRef:
  kind: Role
  name: myapp-role
  apiGroup: rbac.authorization.k8s.io
EOF

# Verify namespace setup
kubectl get resourcequota -n myapp-prod
kubectl get limitrange -n myapp-prod
kubectl get sa -n myapp-prod
```

**Expected:** Namespace created with resource quotas limiting compute and storage. LimitRange sets default CPU/memory requests and limits. ServiceAccount configured with least-privilege RBAC.

**On failure:** For quota errors, verify cluster has sufficient resources with `kubectl describe nodes`. For RBAC errors, check cluster-admin permissions with `kubectl auth can-i create role --namespace myapp-prod`. Use `kubectl describe` on rejected resources to see quota/limit violations.

### Step 2: Configure Application Secrets and ConfigMaps

Externalize configuration and sensitive data using ConfigMaps and Secrets.

```bash
# Create ConfigMap from literal values
kubectl create configmap myapp-config \
  --namespace=myapp-prod \
  --from-literal=LOG_LEVEL=info \
  --from-literal=API_TIMEOUT=30s \
  --from-literal=FEATURE_FLAGS='{"newUI":true,"betaAPI":false}'

# Create ConfigMap from file
cat > app.properties <<EOF
database.pool.size=20
cache.ttl=3600
retry.attempts=3
EOF

kubectl create configmap myapp-properties \
  --namespace=myapp-prod \
  --from-file=app.properties

# Create Secret for database credentials
kubectl create secret generic myapp-db-secret \
  --namespace=myapp-prod \
  --from-literal=username=appuser \
  --from-literal=password='sup3rs3cr3t!' \
  --from-literal=connection-string='postgresql://db.example.com:5432/myapp'

# Create TLS secret for ingress
kubectl create secret tls myapp-tls \
  --namespace=myapp-prod \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key

# Verify secrets/configmaps
kubectl get configmap -n myapp-prod
kubectl get secret -n myapp-prod
kubectl describe configmap myapp-config -n myapp-prod
```

For more complex configurations, use YAML manifests:

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: myapp-prod
data:
  nginx.conf: |
    server {
      listen 8080;
      location / {
        proxy_pass http://backend:3000;
        proxy_set_header Host $host;
      }
    }
  app-config.json: |
    {
      "logLevel": "info",
      "features": {
        "authentication": true,
        "metrics": true
      }
    }
---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
  namespace: myapp-prod
type: Opaque
stringData:  # Automatically base64 encoded
  api-key: "sk-1234567890abcdef"
  jwt-secret: "my-jwt-signing-key"
```

**Expected:** ConfigMaps store non-sensitive configuration, Secrets store credentials/keys. Values accessible to Pods via environment variables or volume mounts. TLS secrets properly formatted for Ingress resources.

**On failure:** For encoding issues, use `stringData` instead of `data` in YAML. For TLS secret errors, verify certificate and key format with `openssl x509 -in tls.crt -text -noout`. For access issues, check ServiceAccount RBAC permissions. View decoded secret with `kubectl get secret myapp-secret -o jsonpath='{.data.api-key}' | base64 -d`.

### Step 3: Create Deployment with Health Checks and Resource Limits

Deploy application with production-ready configuration including probes and resource management.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp-prod
  labels:
    app: myapp
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime updates
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: myapp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: myapp
        image: myregistry.io/myapp:v1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: myapp-config
              key: LOG_LEVEL
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: myapp-db-secret
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: myapp-db-secret
              key: password
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /healthz
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        startupProbe:
          httpGet:
            path: /healthz
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30  # 5 minutes for slow startup
        volumeMounts:
        - name: config
          mountPath: /etc/myapp
          readOnly: true
        - name: cache
          mountPath: /var/cache/myapp
      volumes:
      - name: config
        configMap:
          name: myapp-properties
      - name: cache
        emptyDir: {}
      imagePullSecrets:
      - name: registry-credentials
```

Apply and monitor deployment:

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Watch rollout status
kubectl rollout status deployment/myapp -n myapp-prod

# Check pod status
kubectl get pods -n myapp-prod -l app=myapp

# View pod logs
kubectl logs -n myapp-prod -l app=myapp --tail=50 -f

# Describe deployment for events
kubectl describe deployment myapp -n myapp-prod

# Check resource usage
kubectl top pods -n myapp-prod -l app=myapp
```

**Expected:** Deployment creates 3 replicas with rolling update strategy. Pods pass readiness probes before receiving traffic. Liveness probes restart unhealthy pods. Resource requests/limits prevent OOM kills. Logs show successful application startup.

**On failure:** For ImagePullBackOff, verify image exists and imagePullSecret is valid with `kubectl get secret registry-credentials -o yaml`. For CrashLoopBackOff, check logs with `kubectl logs pod-name --previous`. For probe failures, test endpoints manually with `kubectl port-forward` and `curl localhost:8080/healthz`. For OOMKilled pods, increase memory limits or investigate memory leaks.

### Step 4: Expose Application with Services and Load Balancers

Create Service resources to expose applications internally and externally.

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: myapp-prod
# ... (see EXAMPLES.md for complete configuration)
```

Apply and test services:

```bash
# Apply services
kubectl apply -f service.yaml

# Get service details
kubectl get svc -n myapp-prod

# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** LoadBalancer Service provisions external LB with public IP/hostname. ClusterIP Service provides stable internal DNS. Endpoints list shows healthy Pod IPs. Curl requests succeed with expected responses.

**On failure:** For pending LoadBalancer, check cloud provider integration and quotas. For no endpoints, verify Pod labels match Service selector with `kubectl get pods --show-labels`. For connection refused, verify targetPort matches container port. Use `kubectl port-forward` to bypass Service layer for debugging.

### Step 5: Configure Horizontal Pod Autoscaling

Implement automatic scaling based on CPU/memory or custom metrics.

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: myapp-prod
# ... (see EXAMPLES.md for complete configuration)
```

Install metrics-server if not available:

```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify metrics-server
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** HPA monitors CPU/memory metrics. When thresholds exceeded, replicas scale up to maxReplicas. When load decreases, replicas scale down gradually (stabilization window prevents flapping). Metrics visible with `kubectl top`.

**On failure:** For "unknown" metrics, verify metrics-server is running and Pods have resource requests defined. For no scaling, check current utilization is actually exceeding targets with `kubectl top pods`. For flapping, increase stabilizationWindowSeconds. For slow scale-up, reduce periodSeconds in scaleUp policies.

### Step 6: Package Application with Helm Chart

Create reusable Helm chart for multi-environment deployments.

```bash
# Create Helm chart structure
helm create myapp-chart
cd myapp-chart

# Edit Chart.yaml
cat > Chart.yaml <<EOF
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Helm chart packages all Kubernetes resources with templated values. Dry-run shows rendered manifests. Install deploys all resources in correct order. Upgrades perform rolling updates. Rollback reverts to previous revision.

**On failure:** For template errors, run `helm template .` to render locally without installing. For dependency issues, run `helm dependency update`. For value override failures, verify YAML path exists in values.yaml. Use `helm get manifest myapp -n myapp-prod` to see actual deployed resources.

## Validation

- [ ] Pods in Running state with all containers ready
- [ ] Readiness probes pass before Pods added to Service endpoints
- [ ] Liveness probes restart unhealthy containers automatically
- [ ] Resource requests and limits prevent OOM kills and node overcommit
- [ ] Secrets and ConfigMaps mounted correctly with expected values
- [ ] Services resolve via DNS (cluster.local) from other Pods
- [ ] LoadBalancer/Ingress accessible from external networks
- [ ] HPA scales replicas up under load and down when idle
- [ ] Rolling updates complete with zero downtime
- [ ] Logs collected and accessible via kubectl logs or centralized logging

## Common Pitfalls

- **Missing readiness probes**: Pods receive traffic before fully started. Always implement readiness probes that verify application dependencies.

- **Insufficient startup time**: Fast liveness probes kill slow-starting apps. Use startupProbe with generous failureThreshold for initialization.

- **No resource limits**: Pods consume unlimited CPU/memory causing node instability. Always set requests and limits.

- **Hardcoded configuration**: Environment-specific values in manifests prevent reuse. Use ConfigMaps, Secrets, and Helm values.

- **Default service account**: Pods have unnecessary cluster permissions. Create dedicated ServiceAccounts with minimal RBAC.

- **No rolling update strategy**: Deployments recreate all Pods simultaneously causing downtime. Use RollingUpdate with maxUnavailable: 0.

- **Secrets in version control**: Sensitive data committed to Git. Use sealed-secrets, external-secrets-operator, or vault.

- **No pod disruption budget**: Cluster maintenance drains nodes and breaks service. Create PodDisruptionBudget to ensure minimum available replicas.

## Related Skills

- `setup-docker-compose` - Container orchestration fundamentals before Kubernetes
- `containerize-mcp-server` - Creating container images for deployment
- `write-helm-chart` - Advanced Helm chart development
- `manage-kubernetes-secrets` - SealedSecrets and external-secrets-operator
- `configure-ingress-networking` - NGINX Ingress and cert-manager setup
- `implement-gitops-workflow` - ArgoCD/Flux for declarative deployments
- `setup-container-registry` - Image registry integration
