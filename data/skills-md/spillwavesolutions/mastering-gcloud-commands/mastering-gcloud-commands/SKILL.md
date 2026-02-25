---
name: mastering-gcloud-commands
description: |
  Expert-level Google Cloud CLI (gcloud) skill for managing GCP resources. Use when working
  with "gcloud commands", "cloud run deploy", "alloydb", "cloud sql", "workload identity
  federation", "iam permissions", "vpc networking", "secret manager", or "artifact registry".
  Covers installation, authentication, IAM, Cloud Run, Cloud Storage, VPC, AlloyDB, Firebase,
  and CI/CD integration with GitHub Actions and Cloud Build.
triggers:
  - gcloud
  - gcp
  - google cloud
  - google cloud cli
  - cloud run
  - cloud run deploy
  - cloud scheduler
  - alloydb
  - cloud sql
  - cloud storage
  - gcs
  - firebase deploy
  - github actions gcp
  - workload identity federation
  - wif
  - iam gcp
  - service account
  - secret manager
  - vpc connector
  - vpc networking
  - artifact registry
  - cloud build
  - gcloud auth
  - gcloud config
metadata:
  version: 1.0.0
  category: cloud-infrastructure
  author: Richard Hightower
  license: MIT
---

# Google Cloud CLI Expert Skill

A unified tool to manage Google Cloud resources from the terminal. This guide focuses on gcloud CLI patterns, practical examples, and production deployment workflows.

## Contents

- [Quick Start](#quick-start)
- [When Not to Use](#when-not-to-use)
- [Decision Trees](#decision-trees)
- [Global Flags](#global-flags)
- [Environment Variables](#environment-variables)
- [Workflows](#workflows)
- [Reference Files](#reference-files)
- [Scripts](#scripts)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [Pre-Deployment Checklist](#pre-deployment-checklist)

## Quick Start

```bash
# Verify installation
gcloud --version

# Interactive login
gcloud auth login

# Set default project and region
gcloud config set project PROJECT_ID
gcloud config set compute/region us-central1

# Verify identity
gcloud auth list
gcloud config list
```

## When Not to Use

- **Terraform/Pulumi** — This skill covers gcloud CLI, not Infrastructure as Code tools
- **GCP Console UI** — CLI-focused; use GCP documentation for console walkthroughs
- **AWS/Azure CLI** — Use mastering-aws-cli or azure-cli skills instead
- **Client libraries** — For Python/Go/Java SDK code, use programming documentation
- **Kubernetes kubectl** — For K8s cluster operations, use kubectl documentation

## Decision Trees

### Compute & Containers
```
Need compute?
├── Serverless containers ──────────► Cloud Run (references/cloud-run-deployment.md)
├── Virtual machines ───────────────► GCE (gcloud compute instances)
├── Kubernetes ─────────────────────► GKE (gcloud container clusters)
└── Serverless functions ───────────► Cloud Functions (gcloud functions)
```

### Data & Databases
```
Need database?
├── PostgreSQL (managed) ───────────► AlloyDB (references/alloydb-management.md)
├── MySQL/PostgreSQL/SQL Server ────► Cloud SQL (gcloud sql instances)
├── NoSQL document ─────────────────► Firestore (references/firebase-management.md)
└── NoSQL key-value ────────────────► Bigtable (gcloud bigtable)
```

### Networking
```
Need networking?
├── Custom VPC/subnets ─────────────► VPC (references/vpc-networking.md)
├── Cloud Run → private DB ─────────► VPC Connector (references/vpc-networking.md)
├── Private Google API access ──────► Private Service Connect
└── Firewall rules ─────────────────► VPC Firewall (references/vpc-networking.md)
```

### Security & Identity
```
Need security/access?
├── Users, roles, policies ─────────► IAM (references/iam-permissions.md)
├── GitHub Actions → GCP ───────────► WIF (references/authentication.md)
├── Secrets & credentials ──────────► Secret Manager (references/secret-manager.md)
└── Service accounts ───────────────► SA (references/iam-permissions.md)
```

### Build & Deploy
```
Need CI/CD?
├── GitHub Actions ─────────────────► WIF + deploy (references/cicd-integration.md)
├── Container builds ───────────────► Cloud Build (references/cicd-integration.md)
├── Container registry ─────────────► Artifact Registry (references/cicd-integration.md)
└── Deployment automation ──────────► Scripting (references/scripting-patterns.md)
```

## Global Flags

| Flag | Description |
|:-----|:------------|
| `--project=PROJECT_ID` | Override default project |
| `--region=REGION` | Specify region (e.g., `us-central1`) |
| `--zone=ZONE` | Specify zone (e.g., `us-central1-a`) |
| `--format=FORMAT` | Output: `json`, `yaml`, `table`, `value(FIELD)` |
| `--filter=EXPRESSION` | Filter results (e.g., `status=RUNNING`) |
| `--quiet` | Disable prompts (critical for CI/CD) |
| `--verbosity=debug` | Enable debug output |
| `--log-http` | Show HTTP request/response |

## Environment Variables

| Variable | Purpose | Example |
|:---------|:--------|:--------|
| `CLOUDSDK_CORE_PROJECT` | Default project | `my-project` |
| `CLOUDSDK_COMPUTE_REGION` | Default region | `us-central1` |
| `CLOUDSDK_COMPUTE_ZONE` | Default zone | `us-central1-a` |
| `CLOUDSDK_CORE_DISABLE_PROMPTS` | Non-interactive mode | `1` |
| `GOOGLE_APPLICATION_CREDENTIALS` | SA key file path | `/path/to/key.json` |
| `CLOUDSDK_CORE_VERBOSITY` | Log level | `debug` |

## Workflows

### Installation

**macOS (recommended):**
```bash
brew install --cask google-cloud-sdk
gcloud init
```

For other platforms: `references/installation-macos.md`, `references/installation-linux.md`, `references/installation-windows.md`

### Authentication

```bash
# User login (interactive)
gcloud auth login

# Service account (automation)
gcloud auth activate-service-account --key-file=key.json

# Application Default Credentials
gcloud auth application-default login

# Impersonation (recommended over keys)
gcloud config set auth/impersonate_service_account SA@PROJECT.iam.gserviceaccount.com
```

For WIF, impersonation patterns, and ADC details, see `references/authentication.md`.

### Multi-Account Configuration

```bash
# Create named configurations
gcloud config configurations create dev
gcloud config set project dev-project-123
gcloud config set compute/region us-west1

# Switch contexts
gcloud config configurations activate prod

# Override for single command
gcloud --configuration=prod compute instances list
```

For complete multi-account patterns, see `references/multi-account-management.md`.

### Cloud Run Deployment

**Phase 1: Prepare**
```bash
# Verify project and region
gcloud config get-value project
gcloud config get-value compute/region
```

**Phase 2: Build & Push (container deployments)**
```bash
# Build and push to Artifact Registry
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG
```

**Phase 3: Deploy (zero-traffic)**
```bash
# Deploy from source (builds automatically)
gcloud run deploy SERVICE --source . --region us-central1 --no-traffic --quiet

# Or deploy from container
gcloud run deploy SERVICE --image IMAGE --region us-central1 --no-traffic --quiet
```

**Phase 4: Validate & Shift Traffic**
```bash
# Verify revision is ready
gcloud run revisions list --service=SERVICE --region=us-central1

# Shift traffic (full or canary)
gcloud run services update-traffic SERVICE --to-latest --region=us-central1
# Or canary: --to-tags canary=10
```

For VPC connectivity, secrets, and advanced patterns, see `references/cloud-run-deployment.md`.

### IAM Permissions

```bash
# Grant project role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:user@example.com" \
  --role="roles/viewer"

# Grant resource role
gcloud run services add-iam-policy-binding SERVICE \
  --region=REGION \
  --member="serviceAccount:sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

For custom roles and governance, see `references/iam-permissions.md`.

### Secret Manager

```bash
# Create secret
echo -n "my-secret-value" | gcloud secrets create SECRET_NAME --data-file=-

# Access secret
gcloud secrets versions access latest --secret=SECRET_NAME

# Mount in Cloud Run
gcloud run deploy SERVICE --set-secrets="ENV_VAR=SECRET_NAME:latest"
```

For IAM bindings and rotation, see `references/secret-manager.md`.

### VPC Networking

```bash
# Create custom VPC
gcloud compute networks create my-vpc --subnet-mode=custom

# Create subnet with Private Google Access
gcloud compute networks subnets create my-subnet \
  --network=my-vpc --region=us-central1 --range=10.0.1.0/24 \
  --enable-private-ip-google-access

# Create VPC connector for Cloud Run
gcloud compute networks vpc-access connectors create my-connector \
  --region=us-central1 --network=my-vpc --range=10.8.0.0/28
```

For firewall rules, peering, and Private Service Connect, see `references/vpc-networking.md`.

### AlloyDB

```bash
# Create cluster
gcloud alloydb clusters create CLUSTER --region=us-central1 --password=PASSWORD --network=default

# Create instance
gcloud alloydb instances create INSTANCE --cluster=CLUSTER --region=us-central1 \
  --instance-type=PRIMARY --cpu-count=2
```

For backups and connections, see `references/alloydb-management.md`.

### CI/CD Integration

**GitHub Actions with WIF (recommended):**
```yaml
permissions:
  id-token: write
  contents: read

- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
    service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}
```

For Cloud Build, multi-environment, and Firebase, see `references/cicd-integration.md`.

### Enable APIs

```bash
# Core APIs for Cloud Run deployment
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    iam.googleapis.com \
    iamcredentials.googleapis.com
```

For complete API list, see `references/api-enablement.md`.

## Reference Files

| Reference | Description | Key Triggers |
|:----------|:------------|:-------------|
| [Installation (macOS)](references/installation-macos.md) | Homebrew, Apple Silicon setup | `install gcloud`, `macos` |
| [Installation (Linux)](references/installation-linux.md) | apt, dnf/yum, Docker | `install gcloud`, `linux` |
| [Installation (Windows)](references/installation-windows.md) | Installer, PowerShell | `install gcloud`, `windows` |
| [Authentication](references/authentication.md) | OAuth, SA, WIF, impersonation | `gcloud auth`, `wif`, `service account` |
| [Multi-Account](references/multi-account-management.md) | Configurations, switching | `config`, `switch project` |
| [IAM Permissions](references/iam-permissions.md) | Roles, policies, governance | `iam`, `role`, `permission` |
| [Cloud Run](references/cloud-run-deployment.md) | Deploy, traffic, secrets | `cloud run`, `deploy` |
| [Cloud Scheduler](references/cloud-scheduler.md) | Cron jobs, triggers | `scheduler`, `cron` |
| [Cloud Storage](references/cloud-storage.md) | Buckets, objects, IAM | `storage`, `gcs`, `bucket` |
| [AlloyDB](references/alloydb-management.md) | Clusters, instances | `alloydb`, `postgresql` |
| [VPC Networking](references/vpc-networking.md) | VPCs, subnets, firewall, connectors | `vpc`, `subnet`, `firewall` |
| [Secret Manager](references/secret-manager.md) | Secrets, versions, IAM | `secret`, `secrets manager` |
| [CI/CD Integration](references/cicd-integration.md) | GitHub Actions, Cloud Build | `github actions`, `cloud build` |
| [Scripting Patterns](references/scripting-patterns.md) | Error handling, batch ops | `script`, `automation` |
| [Firebase](references/firebase-management.md) | Functions, Hosting, Firestore | `firebase`, `firestore` |
| [API Enablement](references/api-enablement.md) | Required APIs by service | `enable api` |
| [Verification](references/verification-patterns.md) | Setup verification | `verify`, `check` |
| [Auth Reset](references/authentication-reset.md) | Credential cleanup | `reset auth`, `revoke` |
| [Troubleshooting](references/troubleshooting.md) | Debug, logs, common errors | `debug`, `error`, `logs` |

## Scripts

| Script | Description |
|:-------|:------------|
| `scripts/verify-gcp-setup.sh` | Comprehensive GCP setup verification |
| `scripts/setup-gcloud-configs.sh` | Initialize multi-environment configs |
| `scripts/switch-gcloud-project.sh` | Switch between projects |
| `scripts/reset-gcloud-auth.sh` | Complete auth reset |
| `scripts/deploy-cloud-run.sh` | Cloud Run deployment helper |
| `scripts/setup-wif-github.sh` | WIF setup for GitHub Actions |

## Troubleshooting

### Quick Debug Commands

```bash
# Check configuration
gcloud config list
gcloud auth list

# Enable debug output
gcloud COMMAND --verbosity=debug --log-http

# View logs
gcloud logging read 'resource.type="cloud_run_revision"' --limit=50
```

### Common Errors

| Error | Solution |
|:------|:---------|
| `PERMISSION_DENIED` | Check IAM roles: `gcloud projects get-iam-policy PROJECT_ID` |
| `API not enabled` | Enable API: `gcloud services enable API_NAME` |
| `VPC connector failed` | Check connector status, may need recreation |
| `Container failed to start` | Check Cloud Run logs, test locally first |

For complete troubleshooting guide, see `references/troubleshooting.md`.

## Best Practices

| Category | Recommendation |
|:---------|:---------------|
| **Security** | Use Workload Identity Federation over service account keys |
| **Security** | Use Secret Manager for sensitive configuration |
| **Scripting** | Always use `--quiet` flag in automation |
| **Scripting** | Use `--format=json` or `--format=value()` for parsing |
| **Safety** | Use `gcloud ... --verbosity=debug` to troubleshoot |
| **Performance** | Use `--filter` to reduce API response size |
| **Regions** | Explicitly set region in scripts to avoid surprises |

## Common Mistakes

Avoid these anti-patterns:

| Mistake | Problem | Correct Approach |
|:--------|:--------|:-----------------|
| `gcloud auth activate-service-account --key-file=key.json` | Keys can leak, hard to rotate | Use WIF or impersonation |
| `gcloud run deploy SERVICE --source .` (no region) | Deploys to random default region | Always specify `--region` |
| `echo $SECRET` in logs | Exposes secrets in CI logs | Use `--format=value()` quietly |
| Hardcoding project ID in scripts | Breaks portability | Use `gcloud config get-value project` |
| Missing `--quiet` in CI/CD | Scripts hang on prompts | Always add `--quiet` for automation |
| Using `roles/editor` or `roles/owner` | Over-privileged, security risk | Use specific roles like `roles/run.admin` |

**Bad vs Good Examples:**

```bash
# BAD: No region, no quiet, hardcoded project
gcloud run deploy my-service --source . --project my-project-123

# GOOD: Explicit region, quiet mode, portable
gcloud run deploy my-service \
  --source . \
  --region="${REGION:-us-central1}" \
  --project="$(gcloud config get-value project)" \
  --quiet
```

```bash
# BAD: Using service account key file
gcloud auth activate-service-account --key-file=key.json

# GOOD: Using impersonation (no key file needed)
gcloud config set auth/impersonate_service_account deploy-sa@PROJECT.iam.gserviceaccount.com
```

## Pre-Deployment Checklist

Run before every Cloud Run deployment:

```
[ ] 1. Verify identity: gcloud auth list
[ ] 2. Confirm project: gcloud config get-value project
[ ] 3. Check APIs enabled: gcloud services list --enabled | grep -E "run|build|artifact"
[ ] 4. Verify SA permissions: gcloud projects get-iam-policy PROJECT_ID --filter="bindings.members:SA_EMAIL"
[ ] 5. Test locally: docker run -p 8080:8080 IMAGE && curl localhost:8080/health
[ ] 6. Check secrets exist: gcloud secrets list --filter="name:SECRET_NAME"
[ ] 7. Verify VPC connector (if needed): gcloud compute networks vpc-access connectors describe CONNECTOR --region=REGION
[ ] 8. Deploy with --no-traffic first: gcloud run deploy SERVICE --image=IMAGE --no-traffic
[ ] 9. Verify revision ready: gcloud run revisions list --service=SERVICE --region=REGION
[ ] 10. Shift traffic: gcloud run services update-traffic SERVICE --to-latest --region=REGION
```
