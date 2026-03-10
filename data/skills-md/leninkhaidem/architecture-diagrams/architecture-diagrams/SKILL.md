---
name: architecture-diagrams
description: Use when creating professional architecture diagrams, cloud infrastructure visuals, network topologies, Kubernetes cluster diagrams, or microservices architecture diagrams as PNG/SVG images using Python Diagrams library with real provider icons (AWS, Azure, GCP, K8s, OnPrem, Generic)
---

# Architecture Diagrams

**Portable Claude Agent Skill**

Professional architecture diagram generator using the [Diagrams](https://diagrams.mingrammer.com/) Python library. Produces publication-quality diagrams with real cloud provider icons (AWS, Azure, GCP, K8s, OnPrem, Generic).

**Portability:** This entire `architecture-diagrams/` folder is self-contained. Copy it to `~/.claude/skills/` or any project's `.claude/skills/` directory. Run `./scripts/setup.sh` once per location.

## Installation & Setup

### System Prerequisite

Graphviz must be installed system-wide (provides the `dot` binary):

```bash
# Ubuntu/Debian
sudo apt install graphviz

# macOS
brew install graphviz

# RHEL/Fedora
sudo dnf install graphviz
```

### One-Time Setup (Per Installation Location)

```bash
cd <path-to>/architecture-diagrams/
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This creates `.venv/`, installs Python dependencies, and verifies graphviz.

### Automated Setup Check

```bash
cd <path-to>/architecture-diagrams/
if [ ! -d ".venv" ]; then
  ./scripts/setup.sh
fi
echo "Skill ready"
```

## Quick Start

```bash
# 1. Navigate to your project directory
cd ~/projects/my-project/

# 2. Set skill path for convenience
SKILL_DIR=~/.claude-wa/.claude/skills/architecture-diagrams

# 3. Verify setup
if [ ! -d "$SKILL_DIR/.venv" ]; then cd "$SKILL_DIR" && ./scripts/setup.sh && cd -; fi

# 4. Activate venv
source "$SKILL_DIR/.venv/bin/activate"

# 5. Create a diagram script in your project
cat > my-diagram.py << 'EOF'
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB

with Diagram("My Architecture", show=False):
    lb = ELB("Load Balancer")
    with Cluster("Web Tier"):
        web = [EC2("Web 1"), EC2("Web 2")]
    lb >> web
EOF

# 6. Generate PNG (output goes to ./output/png/ in current directory)
python "$SKILL_DIR/scripts/generate.py" my-diagram.py

# Output: ~/projects/my-project/output/png/my-diagram.png
```

## File Structure

```
architecture-diagrams/        <-- Skill root (portable)
  SKILL.md                    # This file
  requirements.txt            # Python deps (diagrams, graphviz)
  .venv/                      # Python virtual environment (created by setup.sh)
  scripts/
    setup.sh                  # Creates .venv and installs deps
    generate.py               # Runs diagram script, outputs to cwd/output/png/
  src/
    templates/                # Starter templates — copy these
      basic-template.py       # Minimal template with TODOs
    examples/                 # Working example diagrams
      cisco-network.py        # Network topology with routers, switches, firewall
      aws-architecture.py     # AWS cloud architecture with VPC, ALB, RDS
      kubernetes-cluster.py   # K8s cluster with namespaces, services, monitoring
  docs/
    icon-reference.md         # Index with top icons + navigation (load this first)
    icons/                    # Provider-specific icon catalogs (load on demand, all ≤450 lines)
      generic.md              # Generic infrastructure (26 icons)
      aws.md                  # Amazon Web Services (562 icons)
      azure-compute-network.md # Azure: Compute, Network, Database, Storage (~400 icons)
      azure-app-devops.md     # Azure: App Services, DevOps, Identity, Integration, IoT (~240 icons)
      azure-web-security.md   # Azure: Management, Security, Web Services (~170 icons)
      gcp.md                  # Google Cloud Platform (144 icons)
      kubernetes.md           # Kubernetes (69 icons)
      onprem.md               # On-Premise tools (211 icons)
      saas.md                 # SaaS providers (42 icons)
      programming.md          # Languages & frameworks (81 icons)
      elastic-firebase.md     # Elastic Stack, Firebase (~109 icons)
      digitalocean-ibm.md     # DigitalOcean, IBM Cloud (~309 icons)
      oracle-openstack.md     # Oracle OCI, OpenStack (~415 icons)
      outscale-alibaba-misc.md # Outscale, Alibaba, GIS, Custom, C4 (~220 icons)
```

## Output Path Behavior

Diagrams are generated in `./output/png/` **relative to your current working directory** (not the skill directory). This means output appears in your project folder:

```bash
# From your project directory
cd ~/projects/my-project/
python <skill>/scripts/generate.py diagram.py
# Output: ~/projects/my-project/output/png/diagram.png

# Custom output directory
python <skill>/scripts/generate.py diagram.py --output-dir ./diagrams/
# Output: ~/projects/my-project/diagrams/diagram.png

# Absolute path
python <skill>/scripts/generate.py diagram.py --output-dir /tmp/diagrams/
# Output: /tmp/diagrams/diagram.png
```

## Icon Reference (Progressive Disclosure)

**2634 icons** across 17 providers, organized for efficient context loading:

1. **Start with `docs/icon-reference.md`** — Main index (~130 lines) with navigation table, top 30 most-used icons, and quick-start imports
2. **Load provider files on demand** from `docs/icons/` — Only load the specific provider file you need (e.g., `docs/icons/aws.md` for AWS icons)

| Provider File | Icons | When to Load |
|--------------|-------|-------------|
| `icons/generic.md` | 26 | Network devices, OS, compute, storage |
| `icons/aws.md` | 562 | AWS cloud architecture |
| **Azure (split):** | **810** | **Microsoft Azure - load as needed** |
| `icons/azure-compute-network.md` | ~400 | Azure compute, network, database, storage |
| `icons/azure-app-devops.md` | ~240 | Azure app services, DevOps, identity, IoT |
| `icons/azure-web-security.md` | ~170 | Azure management, security, web |
| `icons/gcp.md` | 144 | GCP architecture |
| `icons/kubernetes.md` | 69 | K8s clusters, pods, services |
| `icons/onprem.md` | 211 | Self-hosted infra, databases, CI/CD |
| `icons/saas.md` | 42 | SaaS providers |
| `icons/programming.md` | 81 | Languages, frameworks |
| **Other Clouds (split):** | **689** | **Other cloud providers - load as needed** |
| `icons/elastic-firebase.md` | ~109 | Elastic Stack, Firebase |
| `icons/digitalocean-ibm.md` | ~309 | DigitalOcean, IBM Cloud |
| `icons/oracle-openstack.md` | ~415 | Oracle OCI, OpenStack |
| `icons/outscale-alibaba-misc.md` | ~220 | Outscale, Alibaba, GIS, Custom, C4 |

## Core Concepts

### Diagram Context Manager

Every diagram uses the `Diagram` context manager:

```python
from diagrams import Diagram, Cluster, Edge

with Diagram(
    "Diagram Title",          # Title shown on diagram
    filename="output-name",   # Output filename (no extension)
    outformat="png",          # png, jpg, svg, pdf, dot
    show=False,               # Don't auto-open
    direction="TB",           # TB, BT, LR, RL
    graph_attr={...},         # Graphviz attributes
):
    # nodes and connections here
```

### Direction

| Value | Meaning | Best For |
|-------|---------|----------|
| `TB` | Top to bottom | Hierarchical architectures, network topologies |
| `BT` | Bottom to top | Data flow upward |
| `LR` | Left to right | Pipelines, data flow, timelines |
| `RL` | Right to left | Reverse flows |

### Graph Attributes

```python
graph_attr = {
    "fontsize": "14",       # Title font size
    "bgcolor": "#ffffff",   # Background color
    "pad": "0.5",           # Padding around diagram
    "nodesep": "0.6",       # Horizontal spacing
    "ranksep": "0.8",       # Vertical spacing between ranks
    "splines": "spline",    # Edge routing: spline, ortho, curved, polyline
    "concentrate": "true",  # Merge parallel edges
}
```

## Node Providers Quick Reference

### Generic (Network Infrastructure)

```python
from diagrams.generic.network import Firewall, Router, Switch, Subnet, VPN
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage
from diagrams.generic.device import Mobile, Tablet
from diagrams.generic.place import Datacenter
from diagrams.generic.os import Ubuntu, Windows, LinuxGeneral, Debian, RedHat, CentOS
from diagrams.generic.virtualization import Vmware, Virtualbox, Qemu
from diagrams.generic.blank import Blank  # Invisible node for layout control
```

### AWS

```python
# Compute
from diagrams.aws.compute import EC2, ECS, Lambda, Fargate, ElasticBeanstalk, Batch
# Database
from diagrams.aws.database import RDS, Aurora, Dynamodb, ElastiCache, Neptune, Redshift
# Network
from diagrams.aws.network import ELB, Route53, CloudFront, VPC, APIGateway, DirectConnect
# Storage
from diagrams.aws.storage import S3, EFS, FSx
# Security
from diagrams.aws.security import Cognito, WAF, IAM, KMS, CertificateManager
# Integration
from diagrams.aws.integration import SQS, SNS, Eventbridge, StepFunctions
# Management
from diagrams.aws.management import Cloudwatch, Cloudformation, Cloudtrail, AutoScaling
# Analytics
from diagrams.aws.analytics import Kinesis, Athena, Glue, EMR
# General
from diagrams.aws.general import Users, Client
```

### Azure

```python
from diagrams.azure.compute import VM, FunctionApps, ContainerInstances, KubernetesServices
from diagrams.azure.database import CosmosDb, SQLDatabases, CacheForRedis
from diagrams.azure.network import LoadBalancers, ApplicationGateway, DNS, VirtualNetworks
from diagrams.azure.storage import BlobStorage, StorageAccounts
from diagrams.azure.security import KeyVaults, ActiveDirectory
from diagrams.azure.integration import ServiceBus, EventGrid
from diagrams.azure.web import AppServices
```

### GCP

```python
from diagrams.gcp.compute import GCE, GKE, Functions, Run, AppEngine
from diagrams.gcp.database import SQL as GcpSQL, Spanner, Firestore, BigTable, Memorystore
from diagrams.gcp.network import LoadBalancing, CDN, DNS as GcpDNS, VPC as GcpVPC
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import BigQuery, PubSub, Dataflow
from diagrams.gcp.security import IAP, KMS as GcpKMS
```

### Kubernetes

```python
from diagrams.k8s.compute import Pod, Deployment, StatefulSet, ReplicaSet, Job, CronJob, DaemonSet
from diagrams.k8s.network import Ingress, Service, NetworkPolicy
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.k8s.rbac import ServiceAccount, Role, ClusterRole
from diagrams.k8s.infra import Node as K8sNode, Master
from diagrams.k8s.clusterconfig import HPA, ConfigMap, Secret
from diagrams.k8s.podconfig import Container
```

### On-Premise

```python
# Network
from diagrams.onprem.network import Nginx, HAProxy, Traefik, Istio, Envoy, Consul, Kong, Apache
# Database
from diagrams.onprem.database import PostgreSQL, MySQL, MongoDB, Cassandra, Redis as OnPremRedis
from diagrams.onprem.database import Neo4J, CockroachDB, InfluxDB, Clickhouse
# Queue
from diagrams.onprem.queue import Kafka, RabbitMQ, ActiveMQ, Celery, Nats
# Container
from diagrams.onprem.container import Docker
# CI/CD
from diagrams.onprem.ci import Jenkins, GithubActions, GitlabCI, CircleCI
from diagrams.onprem.cd import Spinnaker, Tekton
from diagrams.onprem.gitops import ArgoCD, Flux
# Monitoring
from diagrams.onprem.monitoring import Prometheus, Grafana, Datadog, Splunk, Nagios
from diagrams.onprem.logging import Loki, Fluentbit
from diagrams.onprem.tracing import Jaeger, Tempo
# IAC
from diagrams.onprem.iac import Terraform, Ansible
# VCS
from diagrams.onprem.vcs import Git, Github, Gitlab
# Analytics
from diagrams.onprem.analytics import Spark, Hadoop, Flink
# Auth/Security
from diagrams.onprem.security import Vault, Trivy
# Workflow
from diagrams.onprem.workflow import Airflow, Kubeflow, Nifi
# In-Memory
from diagrams.onprem.inmemory import Redis, Memcached
# Compute
from diagrams.onprem.compute import Server, Nomad
```

### Custom Icons

```python
from diagrams.custom import Custom

# Use any local PNG/JPG image as a node icon
my_service = Custom("My Service", "./path/to/icon.png")
```

## Clusters (Grouping)

```python
with Cluster("VPC"):
    with Cluster("Public Subnet"):
        web = EC2("Web")
    with Cluster("Private Subnet"):
        api = EC2("API")
        db = RDS("Database")
```

**Cluster attributes:**

```python
with Cluster("Styled Group", graph_attr={
    "bgcolor": "#e8f4fd",     # Background color
    "style": "dashed",        # solid, dashed, dotted, rounded
    "color": "#2196F3",       # Border color
    "penwidth": "2.0",        # Border width
    "fontsize": "12",         # Label font size
    "fontcolor": "#333333",   # Label color
    "labeljust": "l",         # Label alignment: l, r, c
}):
    pass
```

## Edges (Connections)

### Basic Connections

```python
# Forward direction
node_a >> node_b

# Backward direction
node_a << node_b

# Bidirectional (no arrows)
node_a - node_b

# One-to-many
node_a >> [node_b, node_c, node_d]

# Chain
node_a >> node_b >> node_c
```

### Styled Edges

```python
from diagrams import Edge

node_a >> Edge(
    label="HTTPS",        # Text label on the edge
    color="blue",         # Edge color (name or hex)
    style="dashed",       # solid, dashed, dotted, bold
    minlen="2",           # Minimum edge length (ranks)
) >> node_b
```

### Edge Style Patterns

| Connection Type | Color | Style | Example |
|----------------|-------|-------|---------|
| Synchronous API | `blue` or `navy` | `solid` | REST/gRPC calls |
| Async messaging | `orange` or `green` | `dashed` | Kafka, SQS, events |
| Database access | `purple` or `red` | `solid` | SQL queries |
| Replication | `gray` | `dashed` | DB replication |
| Monitoring | `gray` | `dotted` | Metrics/logs |
| External API | `brown` or `gold` | `solid` | Third-party |
| Cache | `red` | `solid` | Redis/Memcached |
| Storage | `brown` | `dotted` | S3, NFS, iSCSI |

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| PNG | `png` (default) | Documentation, presentations |
| SVG | `svg` | Scalable web embedding |
| PDF | `pdf` | Print-quality documents |
| JPG | `jpg` | Compressed images |
| DOT | `dot` | Graphviz source for manual editing |

```python
# Single format
with Diagram("Title", outformat="svg"): ...

# Multiple formats at once
with Diagram("Title", outformat=["png", "svg", "pdf"]): ...
```

## Generate Script Usage

```bash
# Set skill path
SKILL=~/.claude-wa/.claude/skills/architecture-diagrams

# Activate venv first
source "$SKILL/.venv/bin/activate"

# Generate from example (output in ./output/png/)
python "$SKILL/scripts/generate.py" "$SKILL/src/examples/cisco-network.py"

# Custom output name
python "$SKILL/scripts/generate.py" "$SKILL/src/examples/cisco-network.py" --name my-network

# SVG format
python "$SKILL/scripts/generate.py" "$SKILL/src/examples/aws-architecture.py" --outformat svg

# Custom output directory
python "$SKILL/scripts/generate.py" "$SKILL/src/examples/aws-architecture.py" --output-dir ./my-diagrams/

# Generate in a project directory
cd ~/projects/my-project/
python "$SKILL/scripts/generate.py" my-diagram.py
# Output: ~/projects/my-project/output/png/my-diagram.png
```

## Common Diagram Patterns

### Network Topology
Layout: `TB`. Use `diagrams.generic.network` for Router, Switch, Firewall, VPN, Subnet. Cluster for DMZ, Internal, Management zones. See `src/examples/cisco-network.py`.

### Cloud Architecture
Layout: `TB`. Use AWS/Azure/GCP provider icons. Cluster for VPC, subnets, AZs. Edge labels for protocols. See `src/examples/aws-architecture.py`.

### Kubernetes Cluster
Layout: `TB`. Use `diagrams.k8s` for Pod, Deployment, Service, Ingress. Cluster for namespaces. OnPrem for monitoring stack (Prometheus, Grafana). See `src/examples/kubernetes-cluster.py`.

### Microservices
Layout: `TB` or `LR`. Mix providers: OnPrem for services, AWS for infra. Cluster for service groups. Edge styles differentiate sync/async/data flows.

### CI/CD Pipeline
Layout: `LR`. Use `diagrams.onprem.ci` and `diagrams.onprem.cd`. Linear flow with branching for environments.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `ModuleNotFoundError: diagrams` | Activate venv first: `source .venv/bin/activate` |
| `ExecutableNotFound: dot` | Install graphviz: `sudo apt install graphviz` |
| Diagram opens in viewer | Set `show=False` in Diagram() |
| File saved in wrong directory | Output goes to `cwd/output/png/` — run from your project directory, or use `--output-dir` |
| Import error for provider class | Check exact class name at diagrams.mingrammer.com/docs/nodes/ |
| Cluttered edges overlapping | Use `"splines": "ortho"` or `"concentrate": "true"` in graph_attr |
| Nodes too close together | Increase `nodesep` and `ranksep` in graph_attr |
| Diagram too large/small | Adjust `pad`, `fontsize`, and node count per cluster |
| Custom icon not found | Path must be relative to the script's working directory |
| Multiple outputs not working | Pass list to outformat: `outformat=["png", "svg"]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `setup.sh` fails | Ensure Python 3.7+ and graphviz binary are installed |
| `.venv` creation fails | Try `python3 -m venv .venv --clear` to recreate |
| Blank/empty output | Verify nodes are defined inside the `with Diagram()` block |
| Permission denied on output | Check write permissions for `output/png/` directory |
| Slow generation | Large diagrams with many nodes are normal — reduce clusters or nodes |
| `dot` segfault | Update graphviz: `sudo apt install --only-upgrade graphviz` |
