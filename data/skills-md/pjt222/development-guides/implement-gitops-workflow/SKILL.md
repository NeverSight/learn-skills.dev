---
name: implement-gitops-workflow
description: >
  Implement GitOps continuous delivery using Argo CD or Flux with app-of-apps pattern,
  automated sync policies, drift detection, and multi-environment promotion. Manage
  Kubernetes deployments declaratively from Git with automated reconciliation. Use when
  implementing declarative infrastructure management, migrating from imperative kubectl
  commands to Git-driven deployments, setting up multi-environment promotion workflows,
  enforcing code review gates for production, or meeting audit and compliance requirements.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: advanced
  language: multi
  tags: gitops, argocd, flux, sync, drift-detection
---

# Implement GitOps Workflow

Deploy and manage Kubernetes applications using GitOps principles with Argo CD or Flux for automated, auditable, and repeatable deployments.

## When to Use

- Implementing declarative infrastructure and application management
- Migrating from imperative kubectl/helm commands to Git-driven deployments
- Setting up multi-environment promotion workflows (dev → staging → prod)
- Enforcing code review and approval gates for production deployments
- Achieving compliance and audit requirements with Git history
- Implementing disaster recovery with Git as single source of truth

## Inputs

- **Required**: Kubernetes cluster with admin access (EKS, GKE, AKS, or self-hosted)
- **Required**: Git repository for Kubernetes manifests and Helm charts
- **Required**: Argo CD or Flux CLI installed
- **Optional**: Sealed Secrets or External Secrets Operator for secrets management
- **Optional**: Image Updater for automated image promotion
- **Optional**: Prometheus for monitoring sync status

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Install Argo CD and Configure Repository Access

Deploy Argo CD to cluster and connect to Git repository.

```bash
# Create namespace
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Install Argo CD CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# Get initial admin password
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo "Argo CD Admin Password: $ARGOCD_PASSWORD"

# Login via CLI
argocd login localhost:8080 --username admin --password "$ARGOCD_PASSWORD" --insecure

# Change admin password
argocd account update-password

# Add Git repository (HTTPS with token)
argocd repo add https://github.com/USERNAME/gitops-repo \
  --username USERNAME \
  --password "$GITHUB_TOKEN" \
  --name gitops-repo

# Or add via SSH
ssh-keygen -t ed25519 -C "argocd@cluster" -f argocd-deploy-key -N ""
# Add argocd-deploy-key.pub to GitHub repository deploy keys
argocd repo add git@github.com:USERNAME/gitops-repo.git \
  --ssh-private-key-path argocd-deploy-key \
  --name gitops-repo

# Verify repository connection
argocd repo list

# Configure Ingress for UI (optional)
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - argocd.example.com
    secretName: argocd-tls
  rules:
  - host: argocd.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              number: 443
EOF
```

**Expected:** Argo CD installed in argocd namespace. UI accessible via port-forward or Ingress. Admin password changed from default. Git repository added with SSH or token authentication. Repository connection verified.

**On failure:** For pod CrashLoopBackOff, check logs with `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server`. For repository connection failures, verify token has repo access or SSH key added to deploy keys. For Ingress SSL issues, ensure cert-manager issued certificate successfully. For login failures, retrieve password again or reset via `kubectl delete secret argocd-initial-admin-secret -n argocd` and restart server.

### Step 2: Create Application Manifest and Deploy First Application

Define Argo CD Application resource with sync policies and health checks.

```bash
# Create Git repository structure
mkdir -p gitops-repo/{apps,infra,projects}
cd gitops-repo

# Create sample application
mkdir -p apps/myapp/overlays/{dev,staging,prod}
mkdir -p apps/myapp/base

# Base Kustomization
cat > apps/myapp/base/kustomization.yaml <<EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
EOF

cat > apps/myapp/base/deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: ghcr.io/username/myapp:v1.0.0
        ports:
        - containerPort: 8080
EOF

cat > apps/myapp/base/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
EOF

# Production overlay
cat > apps/myapp/overlays/prod/kustomization.yaml <<EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: production
resources:
- ../../base
replicas:
- name: myapp
  count: 5
images:
- name: ghcr.io/username/myapp
  newTag: v1.0.0
EOF

# Commit to Git
git add .
git commit -m "Add myapp application manifests"
git push

# Create Argo CD Application
cat > argocd-apps/myapp-prod.yaml <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-prod
  namespace: argocd
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/USERNAME/gitops-repo
    targetRevision: main
    path: apps/myapp/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true      # Delete resources removed from Git
      selfHeal: true   # Auto-sync on drift detection
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
EOF

# Apply Application via kubectl
kubectl apply -f argocd-apps/myapp-prod.yaml

# Or create via CLI
argocd app create myapp-prod \
  --repo https://github.com/USERNAME/gitops-repo \
  --path apps/myapp/overlays/prod \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# Watch sync status
argocd app get myapp-prod --watch

# Verify application
kubectl get all -n production
argocd app sync myapp-prod  # Manual sync if automated disabled
```

**Expected:** Application synced automatically from Git. Resources created in production namespace. Argo CD UI shows healthy status. Automated sync policies enable prune and self-heal. Sync succeeds within retry limits.

**On failure:** For sync failures, check application events with `argocd app get myapp-prod` and `kubectl get events -n production`. For Kustomize build errors, test locally with `kustomize build apps/myapp/overlays/prod`. For namespace errors, verify namespace exists or enable CreateNamespace sync option. For pruning issues, check finalizers and owner references with `kubectl get <resource> -o yaml`.

### Step 3: Implement App-of-Apps Pattern for Multi-Environment Management

Create root application that manages child applications across environments.

```bash
# Create app-of-apps structure
mkdir -p argocd-apps/{projects,infra,apps}

# Define projects for RBAC
cat > argocd-apps/projects/production.yaml <<EOF
apiVersion: argoproj.io/v1alpha1
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Root app manages all child applications. New applications automatically deployed when added to Git. Infrastructure applications deployed before app applications (via sync waves if needed). Projects enforce RBAC boundaries. App tree shows parent-child relationships.

**On failure:** For circular dependencies, use sync waves to control order. For project permission errors, verify sourceRepos and destinations match application requirements. For recursive directory issues, ensure YAML files are valid and don't conflict. For missing child apps, check root app status with `argocd app get root-app`.

### Step 4: Configure Image Updater for Automated Deployments

Set up Argo CD Image Updater to automatically promote new image versions.

```bash
# Install Argo CD Image Updater
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/manifests/install.yaml

# Configure image update strategy via annotations
cat > argocd-apps/myapp-prod-autoupdate.yaml <<EOF
apiVersion: argoproj.io/v1alpha1
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Image Updater monitors registry for new images matching tag patterns. Semantic versioning strategy updates to latest stable release. Git commits created automatically with new image tags. Applications sync with updated images. Staging uses digest strategy for immutable deployments.

**On failure:** For registry access errors, verify image-updater has pull credentials via secret or ServiceAccount. For write-back failures, check git-creds secret has push permissions. For no updates detected, verify tag regex matches actual tags with `argocd-image-updater test ghcr.io/username/myapp`. For authentication issues, check image-updater logs for detailed error messages.

### Step 5: Implement Progressive Delivery with Argo Rollouts

Enable canary and blue-green deployments with automated rollback.

```bash
# Install Argo Rollouts controller
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Install Rollouts kubectl plugin
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Rollout progressively shifts traffic to canary. Analysis runs at each step, validating success rate. Automated promotion on success, rollback on failure. Argo CD syncs Rollout resources. Dashboard shows real-time rollout progress.

**On failure:** For analysis failures, verify Prometheus accessible and query returns valid results. For traffic routing issues, check Ingress annotations and canary service endpoints. For stuck rollouts, manually promote or abort. For revision mismatch, ensure Argo CD sync policy doesn't conflict with Rollouts controller updates.

### Step 6: Configure Drift Detection and Webhook Notifications

Monitor for manual changes and send alerts to Slack/email.

```bash
# Configure drift detection in Application
cat > argocd-apps/myapp-strict.yaml <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-prod
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Self-heal automatically reverts manual kubectl changes. Notifications sent to Slack on sync failures and successful deployments. Webhooks trigger external systems (PagerDuty, monitoring, ITSM). Drift alerts show what changed and who made changes (via Git history).

**On failure:** For self-heal not triggering, verify automated sync policy enabled and refresh interval not too long (default 3m). For notification failures, test Slack token with curl and verify bot added to channels. For ignored differences not working, check JSON pointer syntax matches resource structure. For webhook errors, check endpoint accessibility and authentication headers.

## Validation

- [ ] Argo CD or Flux installed and accessible via UI/CLI
- [ ] Git repository connected with proper authentication
- [ ] Applications sync automatically from Git on commit
- [ ] Manual kubectl changes reverted by self-heal
- [ ] App-of-apps pattern deploys multiple applications
- [ ] Image Updater promotes new images based on tag patterns
- [ ] Argo Rollouts perform progressive canary deployments
- [ ] Notifications sent to Slack/email on sync events
- [ ] Drift detection alerts on out-of-band changes
- [ ] RBAC enforces project-level access controls

## Common Pitfalls

- **Automatic prune disabled**: Resources removed from Git remain in cluster. Enable `prune: true` in sync policy.

- **No sync waves**: Infrastructure applications deployed after apps that depend on them. Use `argocd.argoproj.io/sync-wave` annotations to control order.

- **Ignoring HPA-managed replicas**: Sync fails because HPA changed replica count. Add `/spec/replicas` to ignoreDifferences.

- **Write-back conflicts**: Image Updater commits conflict with manual commits. Use separate branch or fine-grained RBAC for image updater.

- **Missing finalizers**: Application deletion leaves orphaned resources. Add `resources-finalizer.argocd.argoproj.io` to Application metadata.

- **No analysis templates**: Rollouts promote automatically without validation. Implement AnalysisTemplates with metrics queries.

- **Secrets in Git**: Plaintext secrets committed to repository. Use Sealed Secrets or External Secrets Operator.

- **Self-heal too aggressive**: Self-heal reverts legitimate emergency changes. Use annotations to temporarily disable or implement approval gates.

## Related Skills

- `configure-git-repository` - Setting up Git repository structure for GitOps
- `manage-git-branches` - Branch strategies for environment promotion
- `deploy-to-kubernetes` - Understanding Kubernetes resources managed by GitOps
- `manage-kubernetes-secrets` - Sealed Secrets integration with Argo CD
- `build-ci-cd-pipeline` - CI builds images, GitOps deploys them
- `setup-container-registry` - Image promotion between registries
