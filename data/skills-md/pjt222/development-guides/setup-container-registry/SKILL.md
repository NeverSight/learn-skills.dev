---
name: setup-container-registry
description: >
  Configure container image registries including GitHub Container Registry (ghcr.io),
  Docker Hub, and Harbor with automated image scanning, tagging strategies, retention
  policies, and CI/CD integration for secure image distribution. Use when setting up a
  private container registry, migrating from Docker Hub to self-hosted registries,
  implementing vulnerability scanning in CI/CD pipelines, managing multi-architecture
  images, enforcing image signing, or configuring automatic cleanup and retention policies.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: basic
  language: multi
  tags: container-registry, docker-hub, ghcr, harbor, vulnerability-scanning
---

# Setup Container Registry

Configure production-ready container registries with security scanning, access control, and automated CI/CD integration.

## When to Use

- Setting up private container registry for organization
- Migrating from Docker Hub to self-hosted or alternative registries
- Implementing image vulnerability scanning in CI/CD pipelines
- Managing multi-architecture images (amd64, arm64) with manifests
- Enforcing image signing and provenance verification
- Configuring automatic image cleanup and retention policies

## Inputs

- **Required**: Docker or Podman installed locally
- **Required**: Registry credentials (personal access tokens, service accounts)
- **Optional**: Self-hosted infrastructure for Harbor deployment
- **Optional**: Kubernetes cluster for registry integration
- **Optional**: Cosign/Notary for image signing
- **Optional**: Trivy or Clair for vulnerability scanning

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Configure GitHub Container Registry (ghcr.io)

Set up GitHub Container Registry with personal access tokens and CI/CD integration.

```bash
# Create GitHub Personal Access Token
# Go to: Settings → Developer settings → Personal access tokens → Tokens (classic)
# Required scopes: write:packages, read:packages, delete:packages

# Login to ghcr.io
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Verify login
docker info | grep -A 5 "Registry:"

# Tag image for ghcr.io
docker tag myapp:latest ghcr.io/USERNAME/myapp:latest
docker tag myapp:latest ghcr.io/USERNAME/myapp:v1.0.0

# Push image
docker push ghcr.io/USERNAME/myapp:latest
docker push ghcr.io/USERNAME/myapp:v1.0.0

# Configure in GitHub Actions
cat > .github/workflows/docker-build.yml <<'EOF'
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
EOF

# Make package public (default is private)
# Go to: github.com/USERNAME?tab=packages → Select package → Package settings → Change visibility

# Pull image (public packages don't require authentication)
docker pull ghcr.io/USERNAME/myapp:latest
```

**Expected:** GitHub token has package permissions. Docker login succeeds. Images push to ghcr.io with proper tagging. GitHub Actions workflow builds multi-architecture images with automated tagging. Package visibility configured correctly.

**On failure:** For authentication errors, verify token has `write:packages` scope and hasn't expired. For push failures, check repository name matches image name (case-sensitive). For workflow failures, verify `permissions: packages: write` is set. For public packages not accessible, wait up to 10 minutes for visibility change to propagate.

### Step 2: Configure Docker Hub with Automated Builds

Set up Docker Hub repository with access tokens and vulnerability scanning.

```bash
# Create Docker Hub access token
# Go to: hub.docker.com → Account Settings → Security → New Access Token

# Login to Docker Hub
echo $DOCKERHUB_TOKEN | docker login -u USERNAME --password-stdin

# Create repository
# Go to: hub.docker.com → Repositories → Create Repository
# Select: public or private, enable vulnerability scanning (Pro/Team plan)

# Tag for Docker Hub
docker tag myapp:latest USERNAME/myapp:latest
docker tag myapp:latest USERNAME/myapp:v1.0.0

# Push to Docker Hub
docker push USERNAME/myapp:latest
docker push USERNAME/myapp:v1.0.0

# Configure automated builds (legacy feature, deprecated)
# Modern approach: Use GitHub Actions with Docker Hub

cat > .github/workflows/dockerhub.yml <<'EOF'
name: Docker Hub Push

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64,linux/arm/v7
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/myapp:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/myapp:${{ github.ref_name }}
          build-args: |
            BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
            VCS_REF=${{ github.sha }}

      - name: Update Docker Hub description
        uses: peter-evans/dockerhub-description@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          repository: ${{ secrets.DOCKERHUB_USERNAME }}/myapp
          readme-filepath: ./README.md
EOF

# View vulnerability scan results
# Go to: hub.docker.com → Repository → Tags → View scan results

# Configure webhook for automated triggers
# Go to: Repository → Webhooks → Add webhook
WEBHOOK_URL="https://example.com/webhook"
curl -X POST https://hub.docker.com/api/content/v1/repositories/USERNAME/myapp/webhooks \
  -H "Authorization: Bearer $DOCKERHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"CI Trigger\",\"webhook_url\":\"$WEBHOOK_URL\"}"
```

**Expected:** Docker Hub access token created with read/write permissions. Images push successfully with multi-architecture support. Vulnerability scans run automatically (if enabled). README syncs from GitHub. Webhooks trigger on image push.

**On failure:** For rate limit errors, upgrade to Pro plan or implement pull-through cache. For scan failures, verify plan includes scanning (not available on free tier). For multi-arch build failures, ensure QEMU installed with `docker run --privileged --rm tonistiigi/binfmt --install all`. For webhook failures, verify endpoint is publicly accessible and returns 200 OK.

### Step 3: Deploy Harbor Self-Hosted Registry

Install Harbor with Helm for enterprise registry with RBAC and replication.

```bash
# Add Harbor Helm repository
helm repo add harbor https://helm.gopharbor.io
helm repo update

# Create namespace
kubectl create namespace harbor

# Create values file
cat > harbor-values.yaml <<EOF
expose:
  type: ingress
  tls:
    enabled: true
    certSource: secret
    secret:
      secretName: harbor-tls
  ingress:
    hosts:
      core: harbor.example.com
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod

externalURL: https://harbor.example.com

persistence:
  enabled: true
  persistentVolumeClaim:
    registry:
      size: 200Gi
      storageClass: gp3
    database:
      size: 10Gi
      storageClass: gp3

harborAdminPassword: "ChangeMe123!"

database:
  type: internal  # Use external: postgres for production

redis:
  type: internal  # Use external: redis for production

trivy:
  enabled: true
  skipUpdate: false

notary:
  enabled: true  # Image signing

chartmuseum:
  enabled: true  # Helm chart storage
EOF

# Install Harbor
helm install harbor harbor/harbor \
  --namespace harbor \
  --values harbor-values.yaml \
  --timeout 10m

# Wait for pods to be ready
kubectl get pods -n harbor -w

# Get admin password
kubectl get secret -n harbor harbor-core -o jsonpath='{.data.HARBOR_ADMIN_PASSWORD}' | base64 -d

# Access Harbor UI
echo "Harbor UI: https://harbor.example.com"
echo "Username: admin"

# Login via Docker CLI
docker login harbor.example.com
# Username: admin
# Password: (from above)

# Create project via API
curl -u "admin:$HARBOR_PASSWORD" -X POST \
  https://harbor.example.com/api/v2.0/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "myapp",
    "public": false,
    "metadata": {
      "auto_scan": "true",
      "severity": "high",
      "enable_content_trust": "true"
    }
  }'

# Tag and push to Harbor
docker tag myapp:latest harbor.example.com/myapp/app:latest
docker push harbor.example.com/myapp/app:latest

# Configure robot account for CI/CD
# UI: Administration → Robot Accounts → New Robot Account
# Permissions: Pull, Push to specific projects

# Use robot account in CI/CD
docker login harbor.example.com -u 'robot$myapp-ci' -p "$ROBOT_TOKEN"
```

**Expected:** Harbor deploys to Kubernetes with PostgreSQL and Redis. Ingress configured with TLS. Admin UI accessible. Projects created with vulnerability scanning enabled. Robot accounts provide CI/CD authentication. Trivy scans images on push.

**On failure:** For database connection errors, check PostgreSQL pod logs with `kubectl logs -n harbor harbor-database-0`. For Ingress issues, verify DNS points to LoadBalancer and cert-manager issued certificate. For Trivy failures, check if vulnerability database downloaded successfully. For storage issues, verify PVCs bound with `kubectl get pvc -n harbor`.

### Step 4: Implement Image Tagging Strategy and Retention Policies

Configure semantic versioning, immutable tags, and automatic cleanup.

```bash
# Tagging best practices
# 1. Semantic versioning
docker tag myapp:latest harbor.example.com/myapp/app:v1.2.3
docker tag myapp:latest harbor.example.com/myapp/app:v1.2
docker tag myapp:latest harbor.example.com/myapp/app:v1
docker tag myapp:latest harbor.example.com/myapp/app:latest
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Images tagged with semantic versions, commit SHAs, and environment labels. Retention policies automatically clean old images based on age, pull activity, or count limits. Production tags (v* pattern) retained longer than development branches. Untagged images deleted to save storage.

**On failure:** For retention not triggering, verify cron schedule syntax and Harbor timezone settings. For accidental deletion of production images, implement immutable tags with Harbor tag immutability rules. For storage still growing, check artifact retention includes Helm charts and other OCI artifacts. For policy conflicts, ensure retention rules use `or` algorithm and don't contradict each other.

### Step 5: Configure Kubernetes Image Pull Secrets

Set up registry authentication for Kubernetes clusters.

```bash
# Create Docker registry secret
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=USERNAME \
  --docker-password=$GITHUB_TOKEN \
  --docker-email=user@example.com \
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Image pull secrets created in target namespaces. Pods successfully pull images from private registries. Service accounts include imagePullSecrets. No ImagePullBackOff errors.

**On failure:** For authentication errors, verify credentials with `docker login` manually. For secret not found, check namespace matches Pod namespace. For still failing, decode secret and verify JSON structure with `kubectl get secret ghcr-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq`. For token expiration, rotate credentials and update secrets.

### Step 6: Enable Vulnerability Scanning and Image Signing

Integrate Trivy scanning and Cosign for image provenance.

```bash
# Install Trivy CLI
wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.47.0_Linux-64bit.tar.gz
tar zxvf trivy_0.47.0_Linux-64bit.tar.gz
sudo mv trivy /usr/local/bin/

# Scan local image
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Trivy scans detect vulnerabilities with severity ratings. SARIF results upload to GitHub Security tab. Critical vulnerabilities fail CI/CD builds. Cosign signs images with keypair or keyless (Fulcio). Verification succeeds for signed images. Kyverno blocks unsigned images in Kubernetes.

**On failure:** For Trivy database download failures, run `trivy image --download-db-only`. For false positives, create `.trivyignore` file with CVE IDs and justifications. For Cosign signature failures, verify image digest hasn't changed (signatures apply to specific digest, not tags). For Kyverno policy failures, check image reference pattern matches actual image names. For keyless signing, verify OIDC token has sufficient permissions.

## Validation

- [ ] Registry accessible via Docker CLI login
- [ ] Images push and pull successfully with proper authentication
- [ ] Multi-architecture images build and manifest created
- [ ] Vulnerability scanning runs automatically on image push
- [ ] Retention policies clean old images on schedule
- [ ] Kubernetes clusters can pull images via imagePullSecrets
- [ ] Image signatures verified before deployment
- [ ] Webhook notifications trigger on image updates
- [ ] Registry UI shows scan results and artifact metadata

## Common Pitfalls

- **Public images by default**: GitHub packages are private by default, Docker Hub public. Verify visibility settings match security requirements.

- **Token expiration**: Personal access tokens expire, breaking CI/CD. Use non-expiring tokens for automation or implement rotation.

- **Untagged image accumulation**: Build process creates untagged images consuming storage. Enable automatic cleanup of untagged artifacts.

- **Missing multi-arch support**: Builds only amd64, fails on ARM instances. Use `docker buildx` with `--platform` flag for cross-platform builds.

- **No rate limit protection**: Free Docker Hub accounts limited to 100 pulls/6h. Implement pull-through cache or upgrade plan.

- **Mutable tags**: `latest` tag overwritten breaks reproducibility. Use immutable tags (commit SHA, semantic version) for production.

- **Insecure registry communication**: Self-hosted registry without TLS. Always use HTTPS with valid certificates.

- **No access control**: Single credential shared across teams. Implement RBAC with project-specific robot accounts.

## Related Skills

- `create-r-dockerfile` - Building container images for registry
- `optimize-docker-build-cache` - Efficient image builds for registry push
- `build-ci-cd-pipeline` - Automated registry push in CI/CD
- `deploy-to-kubernetes` - Pulling images from registry
- `implement-gitops-workflow` - Image promotion between registries
