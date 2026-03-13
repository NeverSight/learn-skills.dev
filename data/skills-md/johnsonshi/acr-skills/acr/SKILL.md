---
name: acr
description: 'Comprehensive Azure Container Registry (ACR) knowledge skill. Use when users ask about: container registries, ACR authentication, private endpoints, geo-replication, ACR Tasks, image signing (Notation), artifact cache, connected registry, vulnerability scanning, customer-managed keys, RBAC, network security, artifact streaming, Helm charts in ACR, ORAS, or any Azure container registry feature. Triggers: "ACR", "container registry", "azurecr.io", "az acr", "docker push/pull to Azure", "registry authentication", "private registry", "geo-replicated registry", "image signing", "Notation", "Ratify".'
---

# Azure Container Registry (ACR) Skill

Comprehensive knowledge for Azure Container Registry - Microsoft's managed container registry service.

## Quick Reference

### Service Tiers
| SKU | Included Storage | Max Capacity | Key Features |
|-----|------------------|--------------|--------------|
| **Basic** | 10 GiB | 40 TiB | Webhooks (2), zone redundancy |
| **Standard** | 100 GiB | 40 TiB | Webhooks (10), anonymous pull |
| **Premium** | 500 GiB | 40 TiB | Geo-replication, private endpoints, CMK, connected registry, artifact streaming |

> **Note**: All tiers support up to 40 TiB max storage capacity. Included storage is what's covered by the base price; additional storage is charged per-GiB.

### Common Commands
```bash
# Login
az acr login --name myregistry

# Build and push
az acr build --registry myregistry --image myapp:v1 .

# List repositories
az acr repository list --name myregistry

# Import image
az acr import --name myregistry --source docker.io/library/nginx:latest --image nginx:latest
```

## Feature Area Navigation

Route to specific feature documentation based on the user's question:

### Authentication & Access
| Feature | Folder | Topics |
|---------|--------|--------|
| [Authentication](feature-area-skill-resources/authentication/) | `authentication/` | Entra ID, service principals, managed identity, tokens, OAuth |
| [RBAC & Authorization](feature-area-skill-resources/rbac-authorization/) | `rbac-authorization/` | Built-in roles, ABAC, custom roles, scope maps |

### Networking & Security
| Feature | Folder | Topics |
|---------|--------|--------|
| [Private Endpoints](feature-area-skill-resources/private-endpoints/) | `private-endpoints/` | Private Link, DNS configuration, NSG rules |
| [Network Security](feature-area-skill-resources/network-security/) | `network-security/` | Firewall rules, service endpoints, service tags |
| [Data Loss Prevention](feature-area-skill-resources/data-loss-prevention/) | `data-loss-prevention/` | Export policy, exfiltration prevention |
| [Dedicated Data Endpoints](feature-area-skill-resources/dedicated-data-endpoints/) | `dedicated-data-endpoints/` | Regional data endpoints |

### High Availability
| Feature | Folder | Topics |
|---------|--------|--------|
| [Geo-Replication](feature-area-skill-resources/geo-replication/) | `geo-replication/` | Multi-region, traffic routing, failover |
| [Zone Redundancy](feature-area-skill-resources/zone-redundancy/) | `zone-redundancy/` | Availability zones |

### Build & Automation
| Feature | Folder | Topics |
|---------|--------|--------|
| [ACR Tasks](feature-area-skill-resources/acr-tasks/) | `acr-tasks/` | Automated builds, YAML, triggers |
| [Task Agent Pools](feature-area-skill-resources/task-agent-pools/) | `task-agent-pools/` | Dedicated compute, VNet integration |

### Security & Trust
| Feature | Folder | Topics |
|---------|--------|--------|
| [Content Trust & Signing](feature-area-skill-resources/content-trust-signing/) | `content-trust-signing/` | Notation, DCT, Ratify verification |
| [Vulnerability Scanning](feature-area-skill-resources/vulnerability-scanning/) | `vulnerability-scanning/` | Defender, quarantine |
| [Customer-Managed Keys](feature-area-skill-resources/customer-managed-keys/) | `customer-managed-keys/` | Key Vault, encryption, rotation |
| [Continuous Patching](feature-area-skill-resources/continuous-patching/) | `continuous-patching/` | Trivy + Copa, automated OS patching |

### Image & Artifact Operations
| Feature | Folder | Topics |
|---------|--------|--------|
| [Image Management](feature-area-skill-resources/image-management/) | `image-management/` | Import, delete, lock, tag, multi-arch |
| [Artifact Cache](feature-area-skill-resources/artifact-cache/) | `artifact-cache/` | Pull-through cache, cache rules |
| [Artifact Streaming](feature-area-skill-resources/artifact-streaming/) | `artifact-streaming/` | Lazy loading for AKS |
| [OCI Artifacts](feature-area-skill-resources/oci-artifacts/) | `oci-artifacts/` | Helm, ORAS, SBOMs |

### Edge & Air-Gapped
| Feature | Folder | Topics |
|---------|--------|--------|
| [Connected Registry](feature-area-skill-resources/connected-registry/) | `connected-registry/` | Edge, Azure Arc, IoT |
| [ACR Transfer](feature-area-skill-resources/acr-transfer/) | `acr-transfer/` | Air-gapped pipelines |

### Lifecycle & Observability
| Feature | Folder | Topics |
|---------|--------|--------|
| [Soft Delete & Retention](feature-area-skill-resources/soft-delete-retention/) | `soft-delete-retention/` | Recovery, purge, lifecycle |
| [Webhooks](feature-area-skill-resources/webhooks/) | `webhooks/` | Event notifications |
| [Event Grid](feature-area-skill-resources/event-grid/) | `event-grid/` | Event Grid integration |
| [Monitoring & Diagnostics](feature-area-skill-resources/monitoring-diagnostics/) | `monitoring-diagnostics/` | Azure Monitor, health |
| [SKUs & Service Tiers](feature-area-skill-resources/skus-tiers/) | `skus-tiers/` | Tier comparison, limits |

## Key Concepts

- **Registry**: Container for repositories (e.g., `myregistry.azurecr.io`)
- **Repository**: Collection of related images (e.g., `myapp`)
- **Tag**: Mutable label (e.g., `v1`, `latest`)
- **Digest**: Immutable SHA-256 hash (e.g., `sha256:abc123...`)
- **Manifest**: JSON describing image layers and configuration

## Source Documentation

### Investigation Reports
- `investigation-reports/repository-layout/` - Repository structure analysis
- `investigation-reports/feature-overview/` - Feature taxonomy and mapping
- `investigation-reports/feature-in-depth/` - Detailed per-feature research

### Submodules
- `submodules/azure-management-docs/articles/container-registry/` - MS Learn documentation
- `submodules/acr/` - Azure/acr GitHub repository with preview features and samples
