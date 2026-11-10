---
name: mz-terraform-self-managed
description: >-
  Terraform modules for deploying self-managed Materialize on AWS (EKS),
  Azure (AKS), and GCP (GKE). Covers networking, Kubernetes clusters,
  managed PostgreSQL, object storage, the Materialize operator, and
  Materialize instance configuration. Use this skill whenever the user
  asks about deploying self-managed Materialize with Terraform, setting
  up Materialize infrastructure on any cloud, configuring EKS/AKS/GKE
  for Materialize, troubleshooting a self-managed deployment, upgrading
  Materialize instances, customizing Terraform variables for Materialize,
  or working with the materialize-terraform-self-managed repository.
  Also trigger when the user mentions Karpenter node pools for
  Materialize, persist or metadata backend URLs, the Materialize
  operator Helm chart, CRD versions (v1alpha1 vs v1), rollout
  strategies, or NVMe swap configuration for Materialize nodes.
metadata:
  source: https://github.com/MaterializeInc/materialize-terraform-self-managed
  verified-against: 94a87cc5b377
---

# Materialize Terraform Self-Managed Modules

Production-ready Terraform modules for deploying Materialize on AWS, Azure, and GCP, maintained in the [materialize-terraform-self-managed](https://github.com/MaterializeInc/materialize-terraform-self-managed) repository. Each cloud provider has its own set of modules plus shared Kubernetes modules for the operator and Materialize instance.

All file paths in this skill refer to that repository. When you need the actual module code, clone the repository or fetch individual files from GitHub.

## Repository Layout

```
aws/
  modules/         # AWS-specific infra modules
  examples/
    simple/        # Minimal production-like deployment
    enterprise/    # Adds Ory (Kratos + Hydra) for auth
azure/
  modules/         # Azure-specific infra modules
  examples/
    simple/
    enterprise/
gcp/
  modules/         # GCP-specific infra modules
  examples/
    simple/
    enterprise/
kubernetes/
  modules/         # Cloud-agnostic K8s modules (operator, instance, cert-manager)
test/              # Rust-based integration test harness
scripts/           # Migration and utility scripts
```

## How to Use This Skill

1. **User wants to deploy Materialize on a specific cloud**: Start with the relevant `<cloud>/examples/simple/` directory in the repository. Read `main.tf` and `variables.tf` there for the full working configuration.
2. **User asks about a specific module**: Read `<cloud>/modules/<name>/variables.tf` and `main.tf` for that module.
3. **User wants to customize the instance**: Read `kubernetes/modules/materialize-instance/variables.tf` for all instance-level options.
4. **User asks about upgrades or rollouts**: See the Upgrades section below and `kubernetes/modules/materialize-instance/variables.tf` for rollout config.
5. **User wants enterprise/auth setup**: Read `<cloud>/examples/enterprise/`.
6. **User has an existing Terraform project**: See "Using the Modules from an Existing Terraform Project" below.

## Architecture Layers

Every deployment creates two layers:

**Cloud infrastructure** (cloud-specific modules):
- Networking: VPC/VNet, subnets, NAT, security groups
- Kubernetes: EKS/AKS/GKE cluster with autoscaling
- Database: Managed PostgreSQL for Materialize metadata
- Storage: Object storage (S3/Blob/GCS) for persist layer

**Kubernetes application** (shared modules under `kubernetes/modules/`):
- cert-manager for TLS certificates
- Materialize Operator (Helm chart)
- Materialize Instance (custom resource)

## Cloud Provider Modules

### AWS (`aws/modules/`)

| Module | Purpose |
|--------|---------|
| `networking` | VPC, subnets, NAT gateways, security groups |
| `eks` | EKS cluster with OIDC provider |
| `eks-node-group` | Managed node groups for base workloads |
| `karpenter` | Karpenter autoscaler controller |
| `karpenter-ec2nodeclass` | EC2NodeClass for Karpenter provisioning |
| `karpenter-nodepool` | NodePool for Karpenter scheduling |
| `database` | RDS PostgreSQL for metadata |
| `storage` | S3 bucket with IRSA |
| `aws-lbc` | AWS Load Balancer Controller |
| `nlb` | Network Load Balancer |
| `operator` | Materialize operator (Helm) |
| `ebs-csi-driver` | EBS CSI driver |
| `vpc-cni` | VPC CNI with network policy support |

**Key AWS patterns:**
- Node autoscaling via Karpenter (not cluster autoscaler)
- Two Karpenter node classes: generic (t4g.xlarge) and Materialize (r8gd.2xlarge with NVMe swap)
- Storage auth via IRSA (IAM Roles for Service Accounts)
- NLB for external access on ports 6875 (SQL), 6876 (HTTP), 8080 (console)

### Azure (`azure/modules/`)

| Module | Purpose |
|--------|---------|
| `networking` | VNet, subnets, NAT gateway |
| `aks` | AKS cluster with Cilium networking |
| `nodepool` | Additional AKS node pools |
| `database` | PostgreSQL Flexible Server |
| `storage` | Storage Account with workload identity |
| `load_balancers` | Azure Load Balancers |
| `operator` | Materialize operator (Helm) |

**Key Azure patterns:**
- Cilium for networking and network policies
- Workload Identity Federation for storage auth (passwordless OIDC)
- Standard_E4pds_v6 instances for Materialize nodes with swap
- Private DNS zone for PostgreSQL resolution
- Requires registering `EnableAPIServerVnetIntegrationPreview` feature

### GCP (`gcp/modules/`)

| Module | Purpose |
|--------|---------|
| `networking` | VPC, subnets, Cloud NAT |
| `gke` | GKE cluster with Workload Identity |
| `nodepool` | Additional GKE node pools |
| `database` | Cloud SQL PostgreSQL |
| `storage` | Cloud Storage bucket with HMAC keys |
| `load_balancers` | GCP Load Balancers |
| `operator` | Materialize operator (Helm) |

**Key GCP patterns:**
- HMAC keys for S3-compatible GCS access (these modules use the S3-compatible API)
- VPC peering for Cloud SQL private access
- c4a-highmem-8-lssd instances for Materialize nodes with local SSD and swap
- Secondary IP ranges for pods and services (VPC-native)
- Requires enabling multiple GCP APIs (container, compute, sqladmin, servicenetworking, etc.)

## Kubernetes Modules (`kubernetes/modules/`)

| Module | Purpose |
|--------|---------|
| `cert-manager` | Installs cert-manager Helm chart |
| `self-signed-cluster-issuer` | Creates self-signed ClusterIssuer |
| `materialize-instance` | Deploys Materialize CR |
| `coredns` | CoreDNS configuration |
| `grafana` | Grafana monitoring |
| `prometheus` | Prometheus monitoring stack |
| `hpa` | Horizontal Pod Autoscaling |
| `ory-*` | Ory stack (Kratos, Hydra, etc.) for enterprise auth |

### Materialize Instance Module

This is the most important Kubernetes module. Key variables in `kubernetes/modules/materialize-instance/variables.tf`:

| Variable | Default | Notes |
|----------|---------|-------|
| `crd_version` | `v1alpha1` | Use `v1` for v26.30+. See CRD section below. |
| `instance_name` | (required) | Name of the Materialize CR |
| `instance_namespace` | (required) | Namespace for the instance |
| `metadata_backend_url` | (required) | PostgreSQL connection string |
| `persist_backend_url` | (required) | Object storage URL |
| `license_key` | null | Community or enterprise key |
| `environmentd_version` | `v26.29.0` | Materialize version |
| `rollout_strategy` | `WaitUntilReady` | See Rollout Strategies below |
| `authenticator_kind` | `None` | Options: None, Password, Sasl, Oidc |
| `cpu_request` | `1` | CPU request for environmentd |
| `memory_request` | `4095Mi` | Memory request for environmentd |
| `memory_limit` | `4Gi` | Memory limit for environmentd |
| `system_parameters` | `{}` | Map of system config parameters |
| `issuer_ref` | null | cert-manager issuer for TLS |
| `internal_issuer_ref` | null | Override for internal mTLS certs |

## Backend URL Formats

The Materialize instance needs two backend URLs:

**Metadata backend (PostgreSQL):**
```
postgres://user:password@host:5432/database?sslmode=require&options=-c%20statement_timeout%3D15min
```
The `statement_timeout=15min` parameter is required for metadata operations.

**Persist backend (object storage):**

AWS S3:
```
s3://bucket-name/system:serviceaccount:namespace:name
```

Azure Blob:
```
https://storageaccount.blob.core.windows.net/container
```

GCP Cloud Storage (via HMAC/S3-compatible API):
```
s3://hmac-access-id:hmac-secret@bucket-name/materialize?endpoint=https%3A%2F%2Fstorage.googleapis.com&region=us-central1
```

**Storage authentication support:** Materialize currently supports IAM-based authentication for the persist backend on AWS (IRSA) and Azure (Workload Identity Federation) only. Native GCS IAM auth is not supported, which is why the GCP modules use HMAC keys with the S3-compatible API.

## CRD Versions: v1alpha1 vs v1

**v1alpha1** (default, pre-v26.30): Two-step rollout. Change spec, then set `request_rollout` to a new UUID to trigger the rollout. Gives explicit control over timing.

**v1** (recommended for v26.30+): Spec changes automatically trigger rollouts. The operator computes a hash and handles rollout. The `request_rollout` field is removed. Use `force_rollout` with a new UUID for manual triggers.

Set via `crd_version` variable in the example or the materialize-instance module.

## Rollout Strategies

| Strategy | Behavior | Resource impact |
|----------|----------|-----------------|
| `WaitUntilReady` | New pods created, cutover when healthy | Temporarily doubles resources |
| `ManuallyPromote` | New pods created, waits for manual `forcePromote` | Temporarily doubles resources |
| `ImmediatelyPromoteCausingDowntime` | Old pods torn down first | No extra resources, causes downtime |

## Deploying: Quick Start

Each cloud follows the same pattern:

```bash
git clone https://github.com/MaterializeInc/materialize-terraform-self-managed.git
cd materialize-terraform-self-managed/<cloud>/examples/simple

# Create terraform.tfvars with required variables (see below)
terraform init
terraform apply
```

### Variables by Cloud

**AWS** (`aws/examples/simple/`):
```hcl
name_prefix = "my-mz"                # required
aws_profile = "my-profile"            # required
license_key = "your-license-key"      # required
tags        = { environment = "dev" } # required (no default)
aws_region  = "us-east-1"            # optional, defaults to us-east-1
```

**Azure** (`azure/examples/simple/`):
```hcl
subscription_id     = "12345678-..."   # required
resource_group_name = "materialize-rg" # required
name_prefix         = "my-mz"         # required
tags                = { environment = "dev" } # required (no default)
location            = "westus2"        # optional, defaults to westus2
license_key         = "your-key"       # optional (null default), needed for production
```

**GCP** (`gcp/examples/simple/`):
```hcl
project_id  = "my-gcp-project"        # required
labels      = { environment = "dev" }  # required (no default)
license_key = "your-license-key"      # optional (null default), needed for production
name_prefix = "my-mz"                # optional, defaults to "materialize"
region      = "us-central1"           # optional, defaults to us-central1
```

### Common Optional Variables (all clouds)

| Variable | Default | Purpose |
|----------|---------|---------|
| `internal_load_balancer` | `true` | Set `false` for internet-facing LB |
| `ingress_cidr_blocks` | `["0.0.0.0/0"]` | Restrict access to Materialize ports |
| `k8s_apiserver_authorized_networks` | varies | Restrict K8s API access |
| `crd_version` | `v1alpha1` | Use `v1` for v26.30+ |
| `enable_observability` | `false` | Install Prometheus + Grafana |

## Using the Modules from an Existing Terraform Project

You do not need to clone the repository or copy the examples into your project. Reference modules directly with a Git source, pinning to a release tag or commit SHA:

```hcl
module "materialize_instance" {
  source = "github.com/MaterializeInc/materialize-terraform-self-managed//kubernetes/modules/materialize-instance?ref=<tag-or-commit>"

  # module inputs ...
}
```

- The `//` separates the repository URL from the module subdirectory. Any module in the repository can be referenced this way.
- Always pin `ref` to a tag or commit SHA. Never track `main`, or applies become non-reproducible and can pick up breaking changes.
- To update, first check the [version notes](https://materialize.com/docs/self-managed-deployments/upgrading/version-notes/) for breaking changes between your current `ref` and the target, then bump the `ref`, run `terraform init -upgrade`, and review the plan before applying. See [Upgrading Materialize](#upgrading-materialize) for the full path.
- Use the relevant `<cloud>/examples/simple/main.tf` as the reference for how the modules compose, then reproduce that composition in your own project with pinned Git sources. This is the pattern Materialize uses for its own internal deployments.

## Post-Deployment Setup

### Configure kubectl

After `terraform apply`, configure kubectl to talk to the new cluster:

**AWS:**
```bash
aws eks update-kubeconfig --name $(terraform output -raw eks_cluster_name) --region <region>
```

**Azure:**
```bash
az aks get-credentials --resource-group <rg> --name $(terraform output -raw aks_cluster_name)
```

**GCP:**
```bash
gcloud container clusters get-credentials $(terraform output -raw gke_cluster_name) --region <region>
```

### Connecting to Materialize

**Ports:**
- 6875: PostgreSQL-compatible SQL (pgwire)
- 6876: HTTP API
- 8080: Materialize Console (HTTPS)

**With a public (internet-facing) load balancer** (`internal_load_balancer = false`):

AWS (uses NLB DNS):
```bash
psql "postgres://mz_system@$(terraform output -raw nlb_dns_name):6875/materialize"
open "https://$(terraform output -raw nlb_dns_name):8080/materialize"
```

Azure / GCP (uses load balancer IPs):
```bash
psql "postgres://mz_system@$(terraform output -raw balancerd_load_balancer_ip):6875/materialize"
open "https://$(terraform output -raw console_load_balancer_ip):8080/materialize"
```

**With a private (internal) load balancer** (the default):

Use kubectl port-forwarding. The resource ID is in `terraform output materialize_instance_resource_id`:

```bash
kubectl port-forward svc/mz<resource-id>-balancerd 6875:6875 -n materialize-environment
psql "postgres://mz_system@localhost:6875/materialize"
```

```bash
kubectl port-forward svc/mz<resource-id>-console 8080:8080 -n materialize-environment
open "http://localhost:8080"
```

Use the `external_login_password_mz_system` output for the password when authentication is enabled. Create dedicated users after initial setup; avoid using `mz_system` for regular operations.

### Observability

When `enable_observability = true`, Prometheus and Grafana are deployed in the `monitoring` namespace with pre-configured Materialize dashboards:

```bash
kubectl port-forward svc/grafana 3000:80 -n monitoring
# Username: admin, Password: terraform output -raw grafana_admin_password
```

## Upgrading Materialize

1. Check the [version notes](https://materialize.com/docs/self-managed-deployments/upgrading/version-notes/) for the target version first. Some versions have breaking changes or special upgrade requirements that must be handled before bumping.
2. Upgrade one minor version at a time for versions before v26. From v26+ you can skip minor versions.
3. Downgrading is not supported.
4. Upgrade order: operator first, then instances.

**With Terraform:**
Update `environmentd_version` (and optionally `operator_version`) in your variables, then `terraform apply`. For v1alpha1, also update `request_rollout` to a new UUID.

For the full upgrade procedure, see the [upgrading documentation](https://materialize.com/docs/self-managed-deployments/upgrading/), with per-cloud guides in the sibling `upgrade-on-*` pages. Its markdown is at `https://materialize.com/docs/markdown-docs/self-managed-deployments/upgrading/index.md`; the `mz-docs` skill describes how to fetch it. Always review the [version notes](https://materialize.com/docs/self-managed-deployments/upgrading/version-notes/) for breaking changes before upgrading.

## Instance Sizing

Materialize nodes should use memory-optimized instances with NVMe local storage for swap:

| Cloud | Instance Type | vCPUs | Memory | Max cluster size |
|-------|---------------|-------|--------|------------------|
| AWS | r8gd.2xlarge | 8 | 64 GiB | ~300cc |
| AWS | r8gd.4xlarge | 16 | 128 GiB | ~600cc |
| AWS | r8gd.8xlarge | 32 | 256 GiB | ~1200cc |
| AWS | r8gd.16xlarge | 64 | 512 GiB | ~3200cc |
| Azure | Standard_E4pds_v6 | 4 | 32 GiB | varies |
| GCP | c4a-highmem-8-lssd | 8 | 64 GiB | varies |

ARM-based CPUs with a 1:8 vCPU-to-memory ratio and 8:1 local-storage-to-memory ratio are recommended.

## Common Gotchas

- **ECR auth conflicts**: If `terraform apply` fails with 403 pulling public images, run `docker logout public.ecr.aws` and retry.
- **GCP APIs**: You must enable multiple GCP APIs before running Terraform (container, compute, sqladmin, servicenetworking, iamcredentials, iam, storage).
- **Azure preview feature**: Register `EnableAPIServerVnetIntegrationPreview` before deploying on Azure.
- **Self-signed certs**: The simple examples use self-signed TLS. For production, use a real CA or ACME issuer. When using a public ACME issuer (like Let's Encrypt), set `internal_issuer_ref` separately because public CAs cannot sign `*.cluster.local` names.
- **statement_timeout**: The metadata backend URL must include `statement_timeout=15min` or metadata operations may time out.
- **Console slow loads**: If the Console UI is slow, increase `mz_catalog_server` cluster size from 25cc to 50cc via internal SQL port 6877.

## Troubleshooting

**Check operator status:**
```bash
kubectl -n materialize get all
kubectl -n materialize logs -l app.kubernetes.io/name=materialize-operator
```

**Check Materialize instance:**
```bash
kubectl -n materialize-environment get all
kubectl -n materialize-environment logs <pod-name>
kubectl -n materialize-environment describe pod/<pod-name>
```

**Check Materialize CR status:**
```bash
kubectl get materialize -n materialize-environment -o jsonpath='{.items[0].status}'
```
The CR status should show `UpToDate` when healthy.

## Testing

The test harness in `test/` uses Rust and runs full lifecycle tests (init, apply, verify, destroy):

```bash
cd test
cargo run -- run aws --owner "Name" --license-key-file key.txt \
  --aws-region us-east-1 --aws-profile my-profile
```

Verification checks: Materialize CR status is `UpToDate`, all pods (environmentd, console, balancerd, clusterd) are Running, and `SELECT 1` succeeds over SQL.

## Keeping This Skill Up to Date

The `verified-against` value in the frontmatter metadata records the upstream commit this skill was last verified against. To refresh the skill:

1. Diff the upstream repository from that commit to current `main`, focusing on `variables.tf` files, example configurations, and READMEs.
2. Update the affected sections here (variable defaults, module tables, instance types, gotchas).
3. Bump `verified-against` to the new commit SHA.
