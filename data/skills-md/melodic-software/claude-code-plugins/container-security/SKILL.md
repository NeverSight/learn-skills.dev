---
name: container-security
description: Container and Kubernetes security patterns including Docker hardening, image scanning, pod security standards, network policies, RBAC, secrets management, and runtime protection. Use when securing containerized applications, building secure images, or configuring Kubernetes security controls.
---

# Container Security

## Overview

This skill covers security best practices for containerized applications, including Docker image hardening, Kubernetes security configurations, image vulnerability scanning, and runtime protection.

**Keywords:** container security, Docker, Kubernetes, image scanning, Dockerfile, pod security, network policies, RBAC, container runtime, Trivy, Falco, gVisor, seccomp, AppArmor, distroless, rootless containers

## When to Use This Skill

- Building secure Docker images
- Configuring Kubernetes pod security
- Setting up container vulnerability scanning
- Implementing Kubernetes RBAC
- Configuring network policies
- Managing secrets in Kubernetes
- Setting up runtime security monitoring

## Container Security Layers

| Layer | Controls | Tools |
| --- | --- | --- |
| **Image** | Minimal base, vulnerability scanning, signing | Trivy, Cosign, Grype |
| **Build** | Multi-stage builds, non-root, no secrets | Docker, Buildah, Kaniko |
| **Registry** | Scanning, signing verification, access control | Harbor, ECR, ACR |
| **Runtime** | Seccomp, AppArmor, read-only root | gVisor, Kata, Falco |
| **Orchestration** | Pod security, RBAC, network policies | Kubernetes, OPA/Gatekeeper |
| **Secrets** | Encrypted at rest, external providers | Vault, Sealed Secrets, ESO |

## Secure Dockerfile Patterns

### Minimal Secure Dockerfile

```dockerfile
# Use specific version, not :latest
FROM node:20.10-alpine3.19 AS builder

# Create non-root user early
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

WORKDIR /app

# Copy dependency files first (layer caching)
COPY package*.json ./

# Install dependencies with security flags
RUN npm ci --only=production --ignore-scripts && \
    npm cache clean --force

# Copy application code
COPY --chown=appuser:appgroup . .

# Build if needed
RUN npm run build

# --- Production Stage ---
FROM node:20.10-alpine3.19 AS production

# Security: Don't run as root
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Security: Remove unnecessary packages
RUN apk --no-cache add dumb-init && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Copy only production artifacts
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json ./

# Security: Read-only filesystem support
RUN mkdir -p /app/tmp && chown appuser:appgroup /app/tmp

# Switch to non-root user
USER appuser

# Security: Use dumb-init to handle signals
ENTRYPOINT ["dumb-init", "--"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node healthcheck.js || exit 1

# Expose port (non-privileged)
EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### Distroless Production Image

```dockerfile
# Build stage with full toolchain
FROM golang:1.22-alpine AS builder

RUN apk add --no-cache git ca-certificates

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags='-w -s -extldflags "-static"' \
    -o /app/server ./cmd/server

# --- Distroless production image ---
FROM gcr.io/distroless/static-debian12:nonroot

# Copy binary and CA certs
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server /server

# Run as non-root (65532 is the nonroot user in distroless)
USER 65532:65532

EXPOSE 8080

ENTRYPOINT ["/server"]
```

## Image Scanning

### Trivy Scanning

```bash
# Scan image for vulnerabilities
trivy image --severity CRITICAL,HIGH myapp:latest

# Scan with SBOM generation
trivy image --format cyclonedx --output sbom.json myapp:latest

# Scan filesystem (for CI before building)
trivy fs --security-checks vuln,secret,config .

# Scan with exit code for CI
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed myapp:latest
```

### CI Pipeline Image Scanning

```yaml
# .github/workflows/container-security.yml
name: Container Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH
          exit-code: '1'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-results.sarif

      - name: Run Dockle linter
        uses: erzz/dockle-action@v1
        with:
          image: myapp:${{ github.sha }}
          failure-threshold: high

      - name: Sign image with Cosign
        if: github.ref == 'refs/heads/main'
        env:
          COSIGN_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
        run: |
          cosign sign --key env://COSIGN_KEY myapp:${{ github.sha }}
```

## Kubernetes Pod Security

### Pod Security Standards (PSS)

```yaml
# Enforce Pod Security Standards at namespace level
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # Enforce restricted policy
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    # Warn on baseline violations
    pod-security.kubernetes.io/warn: baseline
    pod-security.kubernetes.io/warn-version: latest
    # Audit all violations
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
```

### Secure Pod Specification

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  labels:
    app: secure-app
spec:
  # Prevent privilege escalation across containers
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault

  # Service account with minimal permissions
  serviceAccountName: app-minimal-sa
  automountServiceAccountToken: false

  containers:
    - name: app
      image: myapp:v1.0.0@sha256:abc123...
      imagePullPolicy: Always

      # Container-level security context
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        runAsNonRoot: true
        runAsUser: 1000
        capabilities:
          drop:
            - ALL
        seccompProfile:
          type: RuntimeDefault

      # Resource limits (prevent DoS)
      resources:
        limits:
          cpu: "500m"
          memory: "256Mi"
          ephemeral-storage: "100Mi"
        requests:
          cpu: "100m"
          memory: "128Mi"

      # Writable directories via emptyDir
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache

      # Health probes
      livenessProbe:
        httpGet:
          path: /health
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 10
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5

  volumes:
    - name: tmp
      emptyDir:
        sizeLimit: 10Mi
    - name: cache
      emptyDir:
        sizeLimit: 50Mi

  # DNS policy for security
  dnsPolicy: ClusterFirst

  # Host settings (all disabled for security)
  hostNetwork: false
  hostPID: false
  hostIPC: false
```

## Network Policies

### Default Deny All

```yaml
# Default deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### Application-Specific Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Allow from ingress controller only
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080

    # Allow from specific services
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080

  egress:
    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53

    # Allow database access
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432

    # Allow external HTTPS
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 10.0.0.0/8
              - 172.16.0.0/12
              - 192.168.0.0/16
      ports:
        - protocol: TCP
          port: 443
```

## Kubernetes RBAC

### Minimal Service Account

```yaml
# Service account with no auto-mounted token
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-minimal-sa
  namespace: production
automountServiceAccountToken: false
---
# Role with minimal permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
  # Only allow reading configmaps
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["app-config"]
    verbs: ["get"]
  # Only allow reading specific secrets
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["app-credentials"]
    verbs: ["get"]
---
# Bind role to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: app-minimal-sa
    namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

### Audit RBAC Permissions

```bash
# List all cluster-admin bindings (high risk)
kubectl get clusterrolebindings -o json | jq '.items[] |
  select(.roleRef.name == "cluster-admin") |
  {name: .metadata.name, subjects: .subjects}'

# Check service account permissions
kubectl auth can-i --list --as=system:serviceaccount:production:app-minimal-sa

# Find overly permissive roles (using wildcards)
kubectl get roles,clusterroles -A -o json | jq '.items[] |
  select(.rules[]?.resources[]? == "*" or .rules[]?.verbs[]? == "*") |
  {name: .metadata.name, namespace: .metadata.namespace}'
```

## Secrets Management

### External Secrets Operator

```yaml
# SecretStore pointing to HashiCorp Vault
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production-role"
          serviceAccountRef:
            name: "vault-auth-sa"
---
# External Secret syncing from Vault
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        DATABASE_URL: "{{ .database_url }}"
        API_KEY: "{{ .api_key }}"
  data:
    - secretKey: database_url
      remoteRef:
        key: production/app
        property: database_url
    - secretKey: api_key
      remoteRef:
        key: production/app
        property: api_key
```

### Sealed Secrets

```bash
# Install sealed-secrets controller
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system

# Seal a secret
kubectl create secret generic my-secret \
  --from-literal=password=supersecret \
  --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-secret.yaml

# The sealed secret can be safely committed to git
cat sealed-secret.yaml
```

## Runtime Security

### Falco Rules

```yaml
# Custom Falco rules
- rule: Unauthorized Process in Container
  desc: Detect unauthorized processes running in containers
  condition: >
    spawned_process and
    container and
    not proc.name in (allowed_processes) and
    not container.image.repository in (trusted_images)
  output: >
    Unauthorized process started (user=%user.name command=%proc.cmdline
    container=%container.name image=%container.image.repository)
  priority: WARNING
  tags: [container, process]

- rule: Write to Sensitive Directories
  desc: Detect writes to sensitive directories in containers
  condition: >
    open_write and
    container and
    (fd.name startswith /etc/ or
     fd.name startswith /bin/ or
     fd.name startswith /sbin/ or
     fd.name startswith /usr/bin/)
  output: >
    Write to sensitive directory (file=%fd.name user=%user.name
    container=%container.name image=%container.image.repository)
  priority: ERROR
  tags: [container, filesystem]

- rule: Container Shell Spawned
  desc: Detect shell spawned in container
  condition: >
    spawned_process and
    container and
    proc.name in (shell_binaries) and
    not proc.pname in (allowed_shell_parents)
  output: >
    Shell spawned in container (user=%user.name shell=%proc.name
    parent=%proc.pname container=%container.name)
  priority: WARNING
  tags: [container, shell]

- list: shell_binaries
  items: [bash, sh, zsh, ash, dash, ksh, tcsh, csh]

- list: allowed_shell_parents
  items: [crond, sshd, sudo]
```

## Quick Reference

### Dockerfile Security Checklist

| Check | Command/Pattern |
| --- | --- |
| No latest tag | `FROM image:specific-version` |
| Non-root user | `USER 1000` |
| No secrets in image | `trivy fs --security-checks secret .` |
| Multi-stage build | Separate builder and production stages |
| Read-only filesystem | `--read-only` or `readOnlyRootFilesystem: true` |
| Minimal base image | Alpine, distroless, or scratch |
| Signed image | `cosign sign` / `cosign verify` |

### Kubernetes Security Checklist

| Check | Setting |
| --- | --- |
| Non-root | `runAsNonRoot: true` |
| No privilege escalation | `allowPrivilegeEscalation: false` |
| Drop capabilities | `capabilities: {drop: [ALL]}` |
| Read-only root | `readOnlyRootFilesystem: true` |
| Resource limits | `resources.limits` defined |
| Network policies | Default deny + explicit allow |
| Seccomp profile | `seccompProfile: {type: RuntimeDefault}` |
| No host namespaces | `hostNetwork/PID/IPC: false` |

## References

- **Dockerfile Hardening**: See `references/dockerfile-security.md` for detailed patterns
- **Kubernetes Security**: See `references/kubernetes-security.md` for comprehensive K8s guidance
- **Container Scanning**: See `references/container-scanning.md` for scanner configurations

---

**Last Updated:** 2025-12-26
