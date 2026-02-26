---
name: yandex-cloud-cli
description: |
  Manage Yandex Cloud infrastructure via the yc CLI.
  Use when the user asks to create, configure, manage, or troubleshoot any
  Yandex Cloud resource: VMs, disks, networks, security groups, databases
  (PostgreSQL, MySQL, ClickHouse, Redis/Valkey, MongoDB, OpenSearch, Greenplum, Kafka),
  Kubernetes, serverless functions/containers, S3 storage, CDN, load balancers,
  Lockbox secrets, KMS, certificates, DNS, container registry, DataProc,
  Data Transfer, logging, audit trails, organizations, WAF, or any other YC service.
  Triggers: Yandex Cloud, yc CLI, YC, managed-postgresql, managed-kubernetes,
  compute instance, serverless function, vpc network, alb, lockbox, yandex cloud.
---

# Yandex Cloud CLI (yc)

## Essentials

### Command Structure

```
yc <service-group> <resource> <command> [<NAME|ID>] [flags] [global-flags]
```

### Global Flags

| Flag | Purpose |
|------|---------|
| `--profile NAME` | Use named profile |
| `--cloud-id ID` | Override cloud |
| `--folder-id ID` | Override folder |
| `--folder-name NAME` | Override folder by name |
| `--token TOKEN` | Override OAuth token |
| `--impersonate-service-account-id ID` | Act as service account |
| `--format text\|yaml\|json\|json-rest` | Output format |
| `--jq EXPR` | Filter JSON output (jq syntax) |
| `--async` | Non-blocking (returns operation ID) |
| `--retry N` | gRPC retries (0=disable, default 5) |
| `--debug` | Debug logging |
| `--no-user-output` | Suppress user-facing output |
| `-h, --help` | Help for any command |

### Output & Scripting

Always use `--format json` combined with `jq` for scripting:

```bash
# Get resource ID by name
yc compute instance get my-vm --format json | jq -r .id

# List all instance external IPs
yc compute instance list --format json | jq -r '.[].network_interfaces[0].primary_v4_address.one_to_one_nat.address'

# Use --jq shortcut (no piping needed)
yc compute instance get my-vm --format json --jq .id

# Get multiple fields
yc compute instance list --format json | jq -r '.[] | [.name, .status] | @tsv'
```

### Configuration & Profiles

```bash
yc init                              # Interactive setup (OAuth, cloud, folder)
yc config list                       # Current config
yc config set folder-id <ID>         # Set default folder
yc config set compute-default-zone ru-central1-d
yc config set format json            # Default output format

# Profile management
yc config profile create <NAME>
yc config profile activate <NAME>
yc config profile list
yc config profile get <NAME>
yc config profile delete <NAME>

# S3 storage config
yc config set storage-endpoint storage.yandexcloud.net
```

### Authentication Methods

1. **OAuth token** (personal use): `yc config set token <OAUTH-TOKEN>`
2. **Service account key** (automation): `yc config set service-account-key key.json`
3. **Instance metadata** (on YC VMs): `yc config set instance-service-account true`
4. **Federation** (SSO): `yc init --federation-id <ID>`

```bash
yc config list           # Show current profile, cloud, folder, token
yc iam create-token      # Get IAM token for API calls
```

### Operations

Long-running operations (create cluster, etc.) can be tracked:

```bash
yc <service> <resource> create ... --async   # Returns operation ID
yc operation get <OPERATION-ID>              # Check status (poll until done=true)
```

Without `--async`, commands block until the operation completes.

### Availability Zones

- `ru-central1-a` — Moscow, zone A
- `ru-central1-b` — Moscow, zone B
- `ru-central1-d` — Moscow, zone D

Note: `ru-central1-c` is deprecated. Use `ru-central1-d` for new resources.

## Service Quick Reference

### All Service Groups

| Group | Alias | Purpose |
|-------|-------|---------|
| **Compute & Infrastructure** | | |
| `compute` | — | VMs, disks, images, snapshots, instance groups, filesystems, GPU clusters |
| `vpc` | — | Networks, subnets, security groups, addresses, gateways, route tables |
| `dns` | — | DNS zones and records |
| `cdn` | — | CDN resources, origin groups, cache management |
| `load-balancer` | `lb` | Network Load Balancer (L4) |
| `application-load-balancer` | `alb` | Application Load Balancer (L7) |
| **Identity & Security** | | |
| `iam` | — | Service accounts, roles, keys, tokens |
| `resource-manager` | `resource` | Clouds, folders |
| `organization-manager` | — | Organizations, federations, groups, OS Login |
| `kms` | — | Symmetric encryption keys |
| `lockbox` | — | Secrets management |
| `certificate-manager` | `cm` | TLS certificates (Let's Encrypt, imported) |
| `smartwebsecurity` | `sws` | WAF security profiles (rules, smart protection, geo/IP filtering) |
| `smartcaptcha` | `sc` | Captcha management (checkbox, slider, challenges) |
| `quota-manager` | — | View quotas and request limit increases |
| **Containers & Serverless** | | |
| `managed-kubernetes` | `k8s` | Kubernetes clusters, node groups |
| `container` | — | Container registry, repositories, images |
| `serverless` | `sls` | Functions, triggers, containers, API gateways |
| **Databases** | | |
| `managed-postgresql` | `postgres` | PostgreSQL clusters |
| `managed-mysql` | — | MySQL clusters |
| `managed-clickhouse` | — | ClickHouse clusters |
| `managed-mongodb` | — | MongoDB clusters |
| `managed-redis` | — | Redis clusters |
| `managed-kafka` | — | Kafka clusters |
| `managed-opensearch` | `opensearch` | OpenSearch clusters |
| `managed-greenplum` | — | Greenplum clusters |
| `ydb` | — | YDB databases (serverless or dedicated) |
| **Data & Analytics** | | |
| `dataproc` | — | DataProc (Hadoop/Spark) clusters and jobs |
| `datatransfer` | `dt` | Data Transfer endpoints and transfers |
| **Storage** | | |
| `storage` | — | Object storage (S3-compatible), buckets |
| **Observability** | | |
| `logging` | `log` | Cloud Logging (groups, read, write) |
| `audit-trails` | — | Audit trail management |
| **Other** | | |
| `backup` | — | Cloud Backup (VMs, policies) |
| `iot` | — | IoT Core (registries, devices, MQTT) |
| `marketplace` | — | Marketplace products |
| `loadtesting` | — | Load testing |

### Standard CRUD Pattern

Most resources follow:

```bash
yc <service> <resource> list [--folder-id ID]
yc <service> <resource> get <NAME|ID>
yc <service> <resource> create [<NAME>] [flags]
yc <service> <resource> update <NAME|ID> [flags]
yc <service> <resource> delete <NAME|ID>
```

Many also support: `add-labels`, `remove-labels`, `list-operations`, `list-access-bindings`, `add-access-binding`, `remove-access-binding`, `move` (between folders).

## Detailed References

Read the reference file matching the service you need:

- **Compute** (VMs, disks, images, snapshots, snapshot schedules, instance groups, filesystems, placement groups, GPU clusters) → [references/compute.md](references/compute.md)
- **Networking** (VPC networks, subnets, security groups, addresses, gateways, route tables, DNS zones/records) → [references/networking.md](references/networking.md)
- **IAM & Resource Manager** (service accounts, roles, all key types, access bindings, clouds, folders) → [references/iam.md](references/iam.md)
- **Serverless** (functions, versions, triggers, containers, API gateways, runtimes, scaling) → [references/serverless.md](references/serverless.md)
- **Kubernetes** (clusters, node groups, kubeconfig, autoscaling, full setup example) → [references/kubernetes.md](references/kubernetes.md)
- **Databases** (PostgreSQL, MySQL, ClickHouse, Redis, MongoDB, OpenSearch, Greenplum, YDB, Kafka — clusters, users, databases, backups, resource presets) → [references/databases.md](references/databases.md)
- **Storage, Secrets, Certificates** (S3 buckets, s3/s3api commands, Lockbox secrets, KMS encryption, Certificate Manager — Let's Encrypt & imported) → [references/storage-secrets-certs.md](references/storage-secrets-certs.md)
- **Container Registry** (registries, repositories, images, Docker auth, lifecycle policies) → [references/container-registry.md](references/container-registry.md)
- **Load Balancers** (ALB — target groups, backend groups, HTTP routers, virtual hosts, routes, listeners; NLB — network load balancers, target groups, health checks) → [references/load-balancers.md](references/load-balancers.md)
- **CDN** (origin groups, CDN resources, caching, SSL, compression, headers, security, cache purge/prefetch) → [references/cdn.md](references/cdn.md)
- **Logging & Audit** (Cloud Logging groups/read/write, Audit Trails, Cloud Backup) → [references/logging-audit.md](references/logging-audit.md)
- **Data Platform** (DataProc clusters/subclusters/jobs, Data Transfer endpoints/transfers) → [references/data-platform.md](references/data-platform.md)
- **Organization, Security & Quotas** (Organization Manager, federations, groups, OS Login, Smart Web Security WAF with rules/conditions, SmartCaptcha, Quota Manager, IoT Core) → [references/organization.md](references/organization.md)

## Guidelines

- Always verify the active profile and folder before mutating commands: `yc config list`
- Use `--format json | jq` for extracting IDs and values in scripts
- Use `--async` for long operations, then check: `yc operation get <OP-ID>`
- Prefer `--name` over `--id` in interactive use; prefer `--id` in scripts for reliability
- For any unfamiliar command, run `yc <service> <resource> <command> --help` — the built-in help is authoritative and always up-to-date
- When creating resources that depend on others (VM needs subnet, subnet needs network), create dependencies first
- Use `--deletion-protection` on production databases, clusters, and secrets
- For S3 operations, create a static access key via `yc iam access-key create`
- Custom security groups with no rules deny all traffic; the auto-created default SG allows all — always create explicit SGs for production
- Use labels consistently (`--labels env=prod,team=backend`) for cost tracking and filtering
- For managed databases, always specify `--security-group-ids` to restrict access
- When creating K8s clusters, specify two service accounts (can be the same): `--service-account-name` for cluster resources and `--node-service-account-name` for node operations (registry, logs)
