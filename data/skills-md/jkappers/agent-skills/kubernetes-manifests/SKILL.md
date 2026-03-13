---
name: kubernetes-manifests
description: Write and review production-ready Kubernetes manifests with security, resource management, and operational best practices. Use when (1) creating new Kubernetes Deployment, Service, or Ingress manifests, (2) reviewing existing manifests for production readiness, (3) adding health probes, security contexts, or resource limits, (4) setting up Kustomize base/overlay structure, (5) containerizing .NET or React apps for Kubernetes, or (6) configuring PodDisruptionBudgets, topology spread, or autoscaling.
---

# Kubernetes Manifest Authoring

Write and review production-ready Kubernetes manifests following security, resource management, and operational best practices.

## Workflow

1. Identify the application type: .NET API, React SPA, worker service, or other
2. Determine the target resources: Deployment, Service, Ingress, HPA, PDB, NetworkPolicy
3. Generate manifests using the patterns below
4. Apply the security context, resource limits, and health probes
5. Validate against the [Pre-Deployment Checklist](#pre-deployment-checklist)

## Core Manifest Structure

Every manifest includes these four required fields:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: api
    app.kubernetes.io/managed-by: kustomize
spec:
  # ...
```

Use declarative YAML with `kubectl apply`. Store manifests in version control. Express desired state only.

## Security Context

**Apply to every pod and container.** Non-negotiable for production.

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
```

| Setting | Requirement |
|---------|-------------|
| `runAsNonRoot: true` | Required |
| `allowPrivilegeEscalation: false` | Required |
| `readOnlyRootFilesystem: true` | Recommended (mount emptyDir for /tmp) |
| `capabilities.drop: [ALL]` | Recommended |
| `hostNetwork/hostPID/hostIPC` | Never use unless explicitly justified |

For .NET images, use UID `1654` (the `app` user). For nginx-unprivileged, use UID `101`.

## Resource Management

**Always set memory requests and limits.** Set CPU requests; omit CPU limits unless required.

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
```

| Application Type | Memory Request | Memory Limit | CPU Request |
|-----------------|----------------|--------------|-------------|
| .NET API | 256Mi | 512Mi | 100m |
| React/Nginx frontend | 64Mi | 128Mi | 50m |
| Worker service | 128Mi-512Mi | 256Mi-1Gi | 100m-500m |

Set requests = limits for critical services to achieve **Guaranteed QoS** (lowest eviction priority).

## Health Probes

Configure all three probe types. Use dedicated endpoints.

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

| Probe | Purpose | On Failure |
|-------|---------|------------|
| Liveness | Detect deadlocks/hangs | Restart container |
| Readiness | Control traffic routing | Remove from Service endpoints |
| Startup | Handle slow-starting apps | Delay other probes |

Use `startupProbe` for slow-starting apps instead of large `initialDelaySeconds`. Keep probes lightweight.

For .NET apps: `/health/live`, `/health/ready`, `/health/startup`. For React/Nginx: `/health` for both liveness and readiness.

## Labels

Apply the `app.kubernetes.io/` recommended labels to all resources:

```yaml
labels:
  app.kubernetes.io/name: myapp
  app.kubernetes.io/instance: myapp-production
  app.kubernetes.io/version: "1.2.3"
  app.kubernetes.io/component: frontend
  app.kubernetes.io/part-of: my-platform
  app.kubernetes.io/managed-by: kustomize
```

Add custom labels for cross-cutting concerns: `environment`, `team`, `cost-center`, `tier`.

## Container Images

- **Never use `:latest` in production.** Pin semantic versions or git SHAs.
- Use digest references (`@sha256:...`) for maximum reproducibility.
- Use distroless/minimal base images.
- Set `imagePullPolicy: IfNotPresent` for tagged images.

## Graceful Shutdown

Add a `preStop` hook to handle the delay between endpoint removal and ingress controller configuration updates:

```yaml
lifecycle:
  preStop:
    exec:
      command: ["sleep", "10"]
terminationGracePeriodSeconds: 45
```

`terminationGracePeriodSeconds` **must** exceed `preStop` delay + application shutdown timeout.

## High Availability

### Topology Spread

Distribute pods across zones:

```yaml
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: ScheduleAnyway
  labelSelector:
    matchLabels:
      app: myapp
```

### Pod Disruption Budget

Protect against voluntary disruptions (node drains, upgrades):

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: "50%"
  selector:
    matchLabels:
      app: myapp
```

Use percentages for scaling flexibility. **Never** set `maxUnavailable: 0` or `minAvailable: 100%`.

### HPA (Stateless Apps)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

## Services and Ingress

Use `ClusterIP` for inter-service communication. Use `Ingress` over multiple `LoadBalancer` services.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

## ConfigMaps and Secrets

Use ConfigMaps for non-sensitive config. Use Secrets for sensitive data. Prefer volume mounts over environment variables. Enable encryption at rest for Secrets.

```yaml
volumes:
- name: config-volume
  configMap:
    name: app-config
- name: secret-volume
  secret:
    secretName: app-secrets
```

Use immutable ConfigMaps (`immutable: true`) for stable configurations. Keep ConfigMaps under 1 MiB.

## Deployment Strategy

| Strategy | Use Case |
|----------|----------|
| `RollingUpdate` (default) | Stateless web services, APIs |
| `Recreate` | Stateful apps, single-version requirements |
| Blue/Green, Canary | Advanced (requires Flagger, Argo Rollouts) |

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%
    maxUnavailable: 25%
```

## Application-Specific Guidance

For detailed .NET and React/Vite manifest patterns, see:
- [references/dotnet-manifests.md](references/dotnet-manifests.md) — GC configuration, Kestrel ports, structured logging, chiseled images
- [references/react-manifests.md](references/react-manifests.md) — NGINX SPA routing, runtime env vars, non-root NGINX, CSP headers
- [references/kustomize.md](references/kustomize.md) — Base/overlay structure, generators, patches, components, GitOps integration

## Pre-Deployment Checklist

- [ ] Resource requests and limits defined (memory required; CPU requests required, limits optional)
- [ ] All three health probes configured (liveness, readiness, startup)
- [ ] Security context applied: non-root, no privilege escalation, read-only root filesystem
- [ ] Labels applied: `app.kubernetes.io/name`, `version`, `component`, `managed-by`
- [ ] Specific image tags pinned (never `:latest`)
- [ ] ConfigMaps for config, Secrets for sensitive data (mounted as volumes)
- [ ] PodDisruptionBudget defined for critical workloads
- [ ] Topology spread or anti-affinity configured for HA
- [ ] `preStop` hook and `terminationGracePeriodSeconds` configured for graceful shutdown
- [ ] Manifests validated with `kubeconform -strict -summary`
