---
name: vmware-aiops
description: >
  AI-powered VMware vCenter/ESXi monitoring and operations.
  Manage infrastructure via natural language: inventory queries, health monitoring,
  VM lifecycle (create, delete, power, snapshot, clone, migrate), vSAN management,
  Aria Operations analytics, Kubernetes clusters, and scheduled log scanning.
---

# VMware AIops

AI-powered VMware vCenter and ESXi operations tool. Manage your entire VMware infrastructure using natural language through any AI coding assistant.

> **Also available: [vmware-monitor](vmware-monitor/SKILL.md)** — A read-only version of this skill for safe monitoring without risk of accidental modifications. Use `/vmware-ops:vmware-monitor` in Claude Code.

## When to Use This Skill

- Query VM, host, datastore, cluster, and network inventory
- Check health status, active alarms, hardware sensors, and event logs
- Perform VM lifecycle operations: power on/off, create, delete, snapshot, clone, migrate
- Monitor vSAN health, capacity, disk groups, and performance
- Access Aria Operations (VCF Operations) for historical metrics, anomaly detection, and capacity planning
- Manage vSphere Kubernetes Service (VKS) clusters
- Run scheduled scanning with webhook notifications (Slack, Discord)

## Quick Install

Works with Claude Code, Cursor, Codex, Gemini CLI, Trae, Kimi, and 30+ AI agents:

```bash
npx skills add zw008/VMware-AIops
```

### Claude Code

```
/plugin marketplace add zw008/VMware-AIops
/plugin install vmware-ops
/vmware-ops:vmware-aiops
```

## Architecture

```
User (Natural Language)
  ↓
AI CLI Tool (Claude Code / Gemini / Codex / Aider / Continue / Trae / Kimi)
  ↓ Reads SKILL.md / AGENTS.md / rules
  ↓
vmware-aiops CLI
  ↓ pyVmomi (vSphere SOAP API)
  ↓
vCenter Server ──→ ESXi Clusters ──→ VMs
    or
ESXi Standalone ──→ VMs
```

## Capabilities

### 1. Inventory

| Feature | vCenter | ESXi | Details |
|---------|:-------:|:----:|---------|
| List VMs | ✅ | ✅ | Name, power state, CPU, memory, guest OS, IP |
| List Hosts | ✅ | ⚠️ Self only | CPU cores, memory, ESXi version, VM count, uptime |
| List Datastores | ✅ | ✅ | Capacity, free/used, type (VMFS/NFS), usage % |
| List Clusters | ✅ | ❌ | Host count, DRS/HA status |
| List Networks | ✅ | ✅ | Network name, associated VM count |

### 2. Health & Monitoring

| Feature | vCenter | ESXi | Details |
|---------|:-------:|:----:|---------|
| Active Alarms | ✅ | ✅ | Severity, alarm name, entity, timestamp |
| Event/Log Query | ✅ | ✅ | Filter by time range, severity; 50+ event types |
| Hardware Sensors | ✅ | ✅ | Temperature, voltage, fan status |
| Host Services | ✅ | ✅ | hostd, vpxa running/stopped status |

**Monitored Event Types:**

| Category | Events |
|----------|--------|
| VM Failures | `VmFailedToPowerOnEvent`, `VmDiskFailedEvent`, `VmFailoverFailed` |
| Host Issues | `HostConnectionLostEvent`, `HostShutdownEvent`, `HostIpChangedEvent` |
| Storage | `DatastoreCapacityIncreasedEvent`, SCSI high latency |
| HA/DRS | `DasHostFailedEvent`, `DrsVmMigratedEvent`, `DrsSoftRuleViolationEvent` |
| Auth | `UserLoginSessionEvent`, `BadUsernameSessionEvent` |

### 3. VM Lifecycle

| Operation | Command | Confirmation | vCenter | ESXi |
|-----------|---------|:------------:|:-------:|:----:|
| Power On | `vm power-on <name>` | — | ✅ | ✅ |
| Graceful Shutdown | `vm power-off <name>` | Double | ✅ | ✅ |
| Force Power Off | `vm power-off <name> --force` | Double | ✅ | ✅ |
| Reset | `vm reset <name>` | — | ✅ | ✅ |
| Suspend | `vm suspend <name>` | — | ✅ | ✅ |
| VM Info | `vm info <name>` | — | ✅ | ✅ |
| Create VM | `vm create <name> --cpu --memory --disk` | — | ✅ | ✅ |
| Delete VM | `vm delete <name>` | Double | ✅ | ✅ |
| Reconfigure | `vm reconfigure <name> --cpu --memory` | Double | ✅ | ✅ |
| Create Snapshot | `vm snapshot-create <name> --name <snap>` | — | ✅ | ✅ |
| List Snapshots | `vm snapshot-list <name>` | — | ✅ | ✅ |
| Revert Snapshot | `vm snapshot-revert <name> --name <snap>` | — | ✅ | ✅ |
| Delete Snapshot | `vm snapshot-delete <name> --name <snap>` | — | ✅ | ✅ |
| Clone VM | `vm clone <name> --new-name <new>` | — | ✅ | ✅ |
| vMotion | `vm migrate <name> --to-host <host>` | — | ✅ | ❌ |

### 4. vSAN Management

| Feature | Details |
|---------|---------|
| Health Check | Cluster-wide health summary, per-group test results |
| Capacity | Total/free/used capacity with projections |
| Disk Groups | Cache SSD + capacity disks per host |
| Performance | IOPS, latency, throughput per cluster/host/VM |

> Requires pyVmomi 8.0.3+ (vSAN SDK merged). For older versions, install the standalone vSAN Management SDK.

### 5. Aria Operations (VCF Operations)

| Feature | Details |
|---------|---------|
| Historical Metrics | Time-series CPU, memory, disk, network with months of history |
| Anomaly Detection | ML-based dynamic baselines and anomaly alerts |
| Capacity Planning | What-if analysis, time-to-exhaustion, forecasting |
| Right-sizing | CPU/memory recommendations per VM |
| Intelligent Alerts | Root cause analysis, remediation recommendations |

> REST API at `/suite-api/`. Auth: `vRealizeOpsToken`. Rebranded as VCF Operations in VCF 9.0.

### 6. vSphere Kubernetes Service (VKS)

| Feature | Details |
|---------|---------|
| List Clusters | Tanzu Kubernetes clusters with phase status |
| Cluster Health | InfrastructureReady, ControlPlaneAvailable, WorkersAvailable |
| Scale Workers | Adjust MachineDeployment replicas |
| Node Status | Machine status, ready/unhealthy counts |

> Kubernetes-native API via kubectl/kubeconfig. VKS 3.6+ uses Cluster API specification.

### 7. Scheduled Scanning & Notifications

| Feature | Details |
|---------|---------|
| Daemon | APScheduler-based, configurable interval (default 15 min) |
| Multi-target Scan | Sequentially scan all configured vCenter/ESXi targets |
| Scan Content | Alarms + Events + Host logs (hostd, vmkernel, vpxd) |
| Log Analysis | Regex pattern matching: error, fail, critical, panic, timeout |
| Webhook | Slack, Discord, or any HTTP endpoint |

## Safety Features

| Feature | Details |
|---------|---------|
| Plan → Confirm → Execute → Log | Structured workflow: show current state, confirm changes, execute, audit log |
| Double Confirmation | Power-off, delete, reconfigure require 2 sequential confirmations |
| Audit Trail | All operations logged to `~/.vmware-aiops/audit.log` (JSONL) with before/after state |
| Password Protection | `.env` file loading, never in command line or shell history |
| SSL Self-signed Support | `disableSslCertValidation` for ESXi 8.0 self-signed certs |
| Task Waiting | All async operations wait for completion and report result |
| State Validation | Pre-operation checks (VM exists, power state correct) |

## Version Compatibility

| vSphere Version | Support | Notes |
|----------------|---------|-------|
| 8.0 / 8.0U1-U3 | ✅ Full | `CreateSnapshot_Task` deprecated → use `CreateSnapshotEx_Task` |
| 7.0 / 7.0U1-U3 | ✅ Full | All APIs supported |
| 6.7 | ✅ Compatible | Backward-compatible, tested |
| 6.5 | ✅ Compatible | Backward-compatible, tested |

> pyVmomi auto-negotiates the API version during SOAP handshake — no manual configuration needed.

## Supported AI Platforms

| Platform | Status | Config File |
|----------|--------|-------------|
| Claude Code | ✅ Native Skill | `plugins/.../SKILL.md` |
| Gemini CLI | ✅ Extension | `gemini-extension/GEMINI.md` |
| OpenAI Codex CLI | ✅ Skill + AGENTS.md | `codex-skill/AGENTS.md` |
| Aider | ✅ Conventions | `codex-skill/AGENTS.md` |
| Continue CLI | ✅ Rules | `codex-skill/AGENTS.md` |
| Trae IDE | ✅ Rules | `trae-rules/project_rules.md` |
| Kimi Code CLI | ✅ Skill | `kimi-skill/SKILL.md` |
| MCP Server | ✅ MCP Protocol | `mcp_server/` |
| Python CLI | ✅ Standalone | N/A |

## CLI Reference

```bash
# Inventory
vmware-aiops inventory vms [--target <name>]
vmware-aiops inventory hosts [--target <name>]
vmware-aiops inventory datastores [--target <name>]
vmware-aiops inventory clusters [--target <name>]

# Health
vmware-aiops health alarms [--target <name>]
vmware-aiops health events [--hours 24] [--severity warning]

# VM Operations
vmware-aiops vm info <vm-name>
vmware-aiops vm power-on <vm-name>
vmware-aiops vm power-off <vm-name> [--force]
vmware-aiops vm create <name> [--cpu <n>] [--memory <mb>] [--disk <gb>]
vmware-aiops vm delete <vm-name> [--confirm]
vmware-aiops vm reconfigure <vm-name> [--cpu <n>] [--memory <mb>]
vmware-aiops vm snapshot-create <vm-name> --name <snap-name>
vmware-aiops vm snapshot-list <vm-name>
vmware-aiops vm snapshot-revert <vm-name> --name <snap-name>
vmware-aiops vm snapshot-delete <vm-name> --name <snap-name>
vmware-aiops vm clone <vm-name> --new-name <name>
vmware-aiops vm migrate <vm-name> --to-host <host>

# vSAN
vmware-aiops vsan health [--target <name>]
vmware-aiops vsan capacity [--target <name>]
vmware-aiops vsan disks [--target <name>]
vmware-aiops vsan performance [--hours 1]

# Aria Operations
vmware-aiops ops alerts [--severity critical]
vmware-aiops ops metrics <resource-name> [--hours 24]
vmware-aiops ops recommendations [--target <name>]
vmware-aiops ops capacity <cluster-name>

# VKS (Kubernetes)
vmware-aiops vks clusters [--namespace default]
vmware-aiops vks health <cluster-name>
vmware-aiops vks scale <machine-deployment> --replicas <n>
vmware-aiops vks nodes <cluster-name>

# Scanning & Daemon
vmware-aiops scan now [--target <name>]
vmware-aiops daemon start
vmware-aiops daemon stop
vmware-aiops daemon status
```

## Setup

```bash
# 1. Clone & install
git clone https://github.com/zw008/VMware-AIops.git
cd VMware-AIops
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Configure
mkdir -p ~/.vmware-aiops
cp config.example.yaml ~/.vmware-aiops/config.yaml
cp .env.example ~/.vmware-aiops/.env
chmod 600 ~/.vmware-aiops/.env
# Edit config.yaml and .env with your target details
```

## License

MIT
