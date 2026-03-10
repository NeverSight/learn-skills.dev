---
name: setup-local-kubernetes
description: >
  Set up a local Kubernetes development environment using kind, k3d, or minikube for fast
  inner-loop development. Covers cluster creation, ingress configuration, local registry
  setup, and integration with development tools like Skaffold and Tilt for automatic
  rebuild and redeploy workflows. Use when needing a local Kubernetes environment for
  development, testing manifests or Helm charts before production deployment, wanting fast
  automatic rebuild-and-redeploy cycles, or learning Kubernetes without cloud costs.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: basic
  language: multi
  tags: kind, k3d, minikube, local-development, skaffold, tilt, docker, kubernetes
---

# Setup Local Kubernetes

Create a local Kubernetes development environment for fast iteration and testing.

## When to Use

- Need local Kubernetes environment for application development
- Want to test Kubernetes manifests and Helm charts before deploying to production
- Require fast inner-loop development with automatic rebuild and redeploy
- Testing multi-service applications with service dependencies
- Learning Kubernetes without cloud costs
- CI/CD pipeline testing locally before pushing changes
- Need isolated environment for experimentation and debugging

## Inputs

- **Required**: Docker Desktop or Docker Engine installed
- **Required**: At least 4GB RAM available for cluster
- **Required**: Choice of local cluster tool (kind, k3d, or minikube)
- **Optional**: Application source code to deploy
- **Optional**: Kubernetes version preference
- **Optional**: Development tool preference (Skaffold, Tilt, or manual)
- **Optional**: Number of worker nodes needed

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.

### Step 1: Install Local Kubernetes Cluster Tool

Choose and install kind, k3d, or minikube based on your requirements.

**Install kind (Kubernetes in Docker):**
```bash
# Linux example
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify installation
kind version
```

**Install k3d (k3s in Docker):**
```bash
# Linux/macOS
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Verify installation
k3d version
```

**Install minikube:**
```bash
# Linux example
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

Install kubectl if not already present:
```bash
# Linux example
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

> See references/EXAMPLES.md for macOS and Windows installation commands.

**Expected:** Tool binary installed and in PATH. Version command returns expected version. kubectl available for cluster interaction.

**On failure:**
- Ensure Docker is running: `docker ps`
- Check system PATH includes installation directory
- For permission issues, verify sudo/admin rights
- On macOS, may need to allow binary in Security & Privacy settings
- Windows users: ensure running terminal as Administrator

### Step 2: Create Local Cluster with Configuration

Create a multi-node cluster with ingress and local registry support.

**Create kind cluster:**
```yaml
# kind-config.yaml (abbreviated)
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: dev-cluster
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
  - containerPort: 443
    hostPort: 443
- role: worker
- role: worker
```

```bash
# Create cluster
kind create cluster --config kind-config.yaml

# Install ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Create local registry
docker run -d --restart=always -p 5000:5000 --name kind-registry registry:2
docker network connect kind kind-registry
```

> See references/EXAMPLES.md for complete kind-config.yaml with registry mirrors and ingress configuration.

**Create k3d cluster:**
```bash
# Create cluster with ingress and registry
k3d cluster create dev-cluster \
  --port "80:80@loadbalancer" \
  --port "443:443@loadbalancer" \
  --agents 2 \
  --registry-create k3d-registry:5000
```

**Create minikube cluster:**
```bash
# Create cluster with multiple nodes
minikube start \
  --nodes=3 \
  --cpus=2 \
  --memory=4096 \
  --driver=docker \
  --addons=ingress,registry,metrics-server
```

Test cluster:
```bash
# Deploy test application
kubectl create deployment hello --image=k8s.gcr.io/echoserver:1.4
kubectl expose deployment hello --type=NodePort --port=8080
kubectl port-forward service/hello 8080:8080

# Clean up test
kubectl delete deployment,service hello
```

**Expected:** Multi-node cluster running with control plane and worker nodes. Ingress controller installed and ready. Local registry accessible at localhost:5000. kubectl context set to new cluster. Test deployment successful.

**On failure:**
- Check Docker has sufficient resources (4GB+ memory recommended)
- Verify no port conflicts: `lsof -i :80,443,5000,6550`
- For kind: ensure Docker desktop Kubernetes is disabled (conflicts)
- For k3d: check Docker network connectivity
- For minikube: try different driver (virtualbox, hyperv, kvm2)
- Review cluster creation logs: `kind get clusters`, `k3d cluster list`, `minikube logs`

### Step 3: Configure Development Workflow Tools

Set up Skaffold or Tilt for automated rebuild and redeploy.

**Install Skaffold:**
```bash
# Linux example
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64
chmod +x skaffold
sudo mv skaffold /usr/local/bin
skaffold version
```

**Create Skaffold configuration:**
```yaml
# skaffold.yaml (abbreviated)
apiVersion: skaffold/v4beta7
kind: Config
metadata:
  name: my-app
build:
# ... (see EXAMPLES.md for complete configuration)
```

> See references/EXAMPLES.md for complete skaffold.yaml with profiles, file sync, and port forwarding.

**Install Tilt:**
```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
tilt version
```

**Create Tiltfile:**
```python
# Tiltfile (abbreviated)
allow_k8s_contexts('kind-dev-cluster')

docker_build(
  'localhost:5000/my-app',
  '.',
  live_update=[
    sync('./src', '/app/src'),
  ]
)

k8s_yaml(['k8s/deployment.yaml', 'k8s/service.yaml'])
k8s_resource('my-app', port_forwards='8080:8080')
```

> See references/EXAMPLES.md for complete Tiltfile with live updates, Helm charts, and custom buttons.

Create sample Kubernetes manifests:
```yaml
# k8s/deployment.yaml (abbreviated)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: app
        image: localhost:5000/my-app
        ports:
        - containerPort: 8080
```

> See references/EXAMPLES.md for complete manifests with service, ingress, and resource limits.

Test development workflow:
```bash
# Using Skaffold
skaffold dev --port-forward

# Using Tilt
tilt up

# Add entry to /etc/hosts for ingress
echo "127.0.0.1 my-app.local" | sudo tee -a /etc/hosts
curl http://my-app.local
```

**Expected:** Skaffold or Tilt watching for file changes. Code changes trigger automatic rebuild and redeploy. Hot reload working for supported languages. Port forwarding allows local access. Logs streaming in terminal/UI. Build caching makes rebuilds fast.

**On failure:**
- Verify Docker daemon accessible: `docker ps`
- Check if local registry reachable: `curl http://localhost:5000/v2/_catalog`
- For file sync issues, ensure paths in config match actual structure
- Review Skaffold/Tilt logs for build errors
- Ensure Dockerfile has proper base image and builds successfully: `docker build .`
- Check resource limits not causing OOMKills: `kubectl describe pod -l app=my-app`

### Step 4: Set Up Local Storage and Databases

Configure persistent storage and deploy database services for testing.

**Create local storage class:**
```yaml
# local-storage.yaml (abbreviated)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
# ... (see EXAMPLES.md for complete configuration)
```

> See references/EXAMPLES.md for complete storage configuration with PVC templates.

**Deploy PostgreSQL for development:**
```yaml
# postgres-dev.yaml (abbreviated)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        envFrom:
        - secretRef:
            name: postgres-secret
```

> See references/EXAMPLES.md for complete PostgreSQL StatefulSet with secrets and volume templates.

**Deploy Redis for caching:**
```bash
# Using Helm
helm install redis bitnami/redis \
  --set auth.enabled=false \
  --set replica.replicaCount=0
```

> See references/EXAMPLES.md for kubectl-based Redis deployment.

Test database connectivity:
```bash
# Apply manifests
kubectl apply -f local-storage.yaml
kubectl apply -f postgres-dev.yaml

# Wait for PostgreSQL
kubectl wait --for=condition=ready pod -l app=postgres --timeout=60s

# Test connection
kubectl exec -it postgres-0 -- psql -U devuser -d devdb -c "SELECT version();"
```

**Expected:** Storage class configured for dynamic provisioning. Database pods running and ready. Services accessible via port-forward or from other pods. Data persists across pod restarts. Resource usage appropriate for development (small limits).

**On failure:**
- Check if storage provisioner installed: `kubectl get storageclass`
- Verify PVC bound to PV: `kubectl get pvc,pv`
- Review pod events for mounting errors: `kubectl describe pod postgres-0`
- For permission issues, check if hostPath directory exists and is writable
- Test database startup: `kubectl logs postgres-0` for PostgreSQL errors
- Ensure no port conflicts for port-forwarding

### Step 5: Configure Observability for Local Development

Add minimal monitoring and logging for debugging.

**Deploy lightweight monitoring stack:**
```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# For local clusters, disable TLS verification
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}
]'

# Verify metrics
kubectl top nodes
kubectl top pods -A
```

**Set up local logging:**
```bash
# Install stern (multi-pod log tailing)
curl -Lo stern https://github.com/stern/stern/releases/download/v1.26.0/stern_1.26.0_linux_amd64.tar.gz
tar -xzf stern_1.26.0_linux_amd64.tar.gz
sudo mv stern /usr/local/bin/

# Usage
stern my-app --since 1m
```

> See references/EXAMPLES.md for development dashboard ConfigMaps and useful aliases.

**Expected:** Metrics-server providing resource usage data. kubectl top commands working. k9s or dashboard showing cluster status. Logs accessible via stern or kubectl logs. Low overhead monitoring suitable for development.

**On failure:**
- For metrics-server TLS errors, apply insecure TLS flag patch
- Check if metrics-server pod running: `kubectl get pods -n kube-system -l k8s-app=metrics-server`
- Verify heapster API available: `kubectl get apiservices | grep metrics`
- For stern, ensure kubectl context is set correctly
- Test basic kubectl access before debugging observability tools

### Step 6: Document Workflow and Create Helpers

Create scripts and documentation for team onboarding.

**Create setup script:**
```bash
#!/bin/bash
# setup-local-cluster.sh (abbreviated)
set -e

echo "=== Local Kubernetes Cluster Setup ==="

# ... (see EXAMPLES.md for complete configuration)
```

> See references/EXAMPLES.md for complete setup script with service deployment and verification.

**Create teardown script:**
```bash
#!/bin/bash
# teardown-local-cluster.sh (abbreviated)
echo "=== Tearing Down Local Cluster ==="

if kind get clusters 2>/dev/null | grep -q dev-cluster; then
  kind delete cluster --name dev-cluster
  docker stop kind-registry && docker rm kind-registry
fi

docker system prune -f
```

> See references/EXAMPLES.md for complete teardown script and README template.

**Expected:** Setup script creates cluster in one command. Teardown script cleans everything up. README provides clear instructions for common tasks. Team members can get productive quickly.

**On failure:**
- Test scripts manually before distributing
- Add error handling for each step
- Provide troubleshooting section in README
- Create video walkthrough for complex setups
- Maintain scripts as cluster tool versions update

## Validation

- [ ] Local cluster created with multiple nodes
- [ ] Ingress controller installed and responding
- [ ] Local registry accessible and accepting pushes
- [ ] Sample application deploys successfully
- [ ] File sync working (changes reflected without full rebuild)
- [ ] Port forwarding allows local access to services
- [ ] Database services running and accessible
- [ ] Metrics server providing resource usage
- [ ] Logs accessible via kubectl/stern/Tilt
- [ ] Setup/teardown scripts work reliably
- [ ] Documentation clear and up-to-date
- [ ] Team members can onboard in <30 minutes

## Common Pitfalls

- **Insufficient Resources**: Local clusters need 4GB+ RAM, 2+ CPU cores. Check Docker Desktop settings. Reduce replicas and resource requests for development.

- **Port Conflicts**: Ports 80, 443, 5000 commonly used. Check with `lsof -i :<port>` before cluster creation. Adjust port mappings if needed.

- **Slow Rebuilds**: Without proper caching, Docker rebuilds are slow. Use multi-stage builds, .dockerignore, and BuildKit. Enable Skaffold/Tilt caching.

- **Context Confusion**: Multiple kubectl contexts cause confusion. Use `kubectl config current-context` and `kubectx` tool to switch clearly.

- **File Sync Not Working**: Path mismatches between host and container break sync. Verify paths in skaffold.yaml/Tiltfile match Dockerfile WORKDIR.

- **Ingress Not Resolving**: Forgot to add entry to /etc/hosts. Or ingress controller not ready. Wait for controller pods before testing.

- **Database Data Loss**: Default storage ephemeral. Use PersistentVolumes for data that should survive restarts. Be explicit about storage class.

- **Resource Limits Too High**: Don't copy production resource specs to local. Reduce limits significantly for local development to fit in Docker Desktop.

- **Network Isolation**: Local cluster can't always reach host services. Use `host.docker.internal` (Docker Desktop) or ngrok for reverse proxying.

- **Version Skew**: Local cluster version differs from production. Explicitly set Kubernetes version during creation to match production.

## Related Skills

- `deploy-to-kubernetes` - Application deployment patterns tested locally first
- `write-helm-chart` - Helm charts tested in local cluster
- `setup-prometheus-monitoring` - Monitoring setup tested locally
- `configure-ingress-networking` - Ingress configuration validated locally
- `implement-gitops-workflow` - GitOps tested with local cluster
- `optimize-cloud-costs` - Cost optimization strategies developed locally
