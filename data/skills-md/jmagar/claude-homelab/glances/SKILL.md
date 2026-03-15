---
name: glances
description: Monitor system health via Glances REST API (CPU, memory, disk, network, sensors, containers, processes). Use when the user asks to "check glances", "system stats", "CPU usage", "memory usage", "glances status", "server health via glances", "disk space", "network traffic", "container stats", "process list", "sensor temperatures", or mentions Glances/system monitoring.
---

# Glances System Monitoring Skill

**⚠️ MANDATORY SKILL INVOCATION ⚠️**

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "Glances stats", "system health", "CPU usage"
- "memory usage", "disk space", "container stats"
- "check Glances", "server monitoring", "process list"
- Any mention of Glances or system resource monitoring

**Failure to invoke this skill when triggers occur violates your operational requirements.**

Monitor system health via the Glances REST API (v4). Get real-time stats on CPU, memory, disk, network, sensors, containers, and processes.

## Purpose

This skill provides **read-only** access to system metrics from a Glances server:
- CPU usage (total, per-core, load average)
- Memory and swap usage
- Disk I/O and filesystem space
- Network traffic (per interface)
- Temperature and fan sensors
- Docker/Podman container stats
- Process list (top consumers)
- System alerts and warnings

All operations are **GET-only** and safe for monitoring/reporting.

## Setup

1. **Start Glances in server mode** on the target system:
   ```bash
   glances -w --disable-webui  # API only
   # or
   glances -w                  # API + Web UI
   ```

2. **Add credentials to .env file**: `~/.homelab-skills/.env`

```bash
GLANCES_URL="http://localhost:61208"
GLANCES_USERNAME=""  # Optional: leave empty if no auth
GLANCES_PASSWORD=""  # Optional: leave empty if no auth
```

**Variable details:**
- `GLANCES_URL`: Glances server URL (default port 61208)
- `GLANCES_USERNAME`: HTTP Basic auth username (optional, leave empty if no auth)
- `GLANCES_PASSWORD`: HTTP Basic auth password (optional, leave empty if no auth)

## Commands

All commands output JSON. Use `jq` for formatting or filtering.

### Quick Overview

Get a quick system overview (CPU, memory, swap, load):

```bash
./scripts/glances-api.sh quicklook
```

### System Info

```bash
./scripts/glances-api.sh system      # Hostname, OS, platform
./scripts/glances-api.sh uptime      # System uptime
./scripts/glances-api.sh core        # CPU core count (physical/logical)
```

### CPU Stats

```bash
./scripts/glances-api.sh cpu         # Overall CPU usage
./scripts/glances-api.sh percpu      # Per-core CPU usage
./scripts/glances-api.sh load        # Load average (1/5/15 min)
```

### Memory Stats

```bash
./scripts/glances-api.sh mem         # Memory usage (total/used/free/percent)
./scripts/glances-api.sh memswap     # Swap usage
```

### Disk Stats

```bash
./scripts/glances-api.sh fs          # Filesystem usage (mount points, space)
./scripts/glances-api.sh diskio      # Disk I/O (read/write bytes/s)
./scripts/glances-api.sh raid        # RAID array status (if available)
./scripts/glances-api.sh smart       # S.M.A.R.T. disk health (if available)
```

### Network Stats

```bash
./scripts/glances-api.sh network     # Network interface traffic
./scripts/glances-api.sh ip          # IP addresses
./scripts/glances-api.sh wifi        # WiFi signal (if available)
./scripts/glances-api.sh connections # TCP connection states
```

### Sensors

```bash
./scripts/glances-api.sh sensors     # Temperature, fan, battery sensors
./scripts/glances-api.sh gpu         # GPU stats (if available)
```

### Processes

```bash
./scripts/glances-api.sh processlist           # Full process list
./scripts/glances-api.sh processlist --top 10  # Top 10 by CPU
./scripts/glances-api.sh processcount          # Process counts by state
```

### Containers

```bash
./scripts/glances-api.sh containers            # Docker/Podman containers
./scripts/glances-api.sh containers --running  # Running only
```

### Alerts & Status

```bash
./scripts/glances-api.sh alert       # Active alerts/warnings
./scripts/glances-api.sh status      # API status check
./scripts/glances-api.sh plugins     # List available plugins
./scripts/glances-api.sh amps        # Application monitoring (AMPs)
```

### Raw Plugin Access

```bash
./scripts/glances-api.sh plugin <name>         # Get any plugin data
./scripts/glances-api.sh plugin <name> <field> # Get specific field
```

### Dashboard (All-in-One)

```bash
./scripts/glances-api.sh dashboard   # Comprehensive system overview
```

## Workflow

When the user asks about system health:

1. **"How's the server doing?"** → Run `./scripts/glances-api.sh dashboard`
2. **"CPU usage?"** → Run `./scripts/glances-api.sh cpu`
3. **"Memory?"** → Run `./scripts/glances-api.sh mem`
4. **"Disk space?"** → Run `./scripts/glances-api.sh fs`
5. **"What's using resources?"** → Run `./scripts/glances-api.sh processlist --top 10`
6. **"Container stats?"** → Run `./scripts/glances-api.sh containers`
7. **"Any problems?"** → Run `./scripts/glances-api.sh alert`
8. **"Temperatures?"** → Run `./scripts/glances-api.sh sensors`

## Output Examples

### Quick Look
```json
{
  "cpu": 12.5,
  "cpu_name": "AMD Ryzen 9 5900X",
  "mem": 45.2,
  "swap": 0.0,
  "load": 2.15
}
```

### Memory
```json
{
  "total": 32212254720,
  "available": 17637244928,
  "percent": 45.2,
  "used": 14575009792,
  "free": 1234567890
}
```

### Filesystem
```json
[
  {
    "device_name": "/dev/nvme0n1p2",
    "fs_type": "ext4",
    "mnt_point": "/",
    "size": 500107862016,
    "used": 125026965504,
    "free": 375080896512,
    "percent": 25.0
  }
]
```

## Notes

- Glances API v4 is used (default since Glances 4.x)
- Requires network access to your Glances server
- Default port is 61208
- Some plugins may return empty data if not applicable (e.g., `gpu` without GPU, `raid` without RAID)
- Authentication is optional; configure in Glances with `--username` and `--password`
- All calls are **read-only GET requests**

## Multiple Servers

To monitor multiple Glances servers, use numbered environment variables in `.env`:

```bash
# In ~/.homelab-skills/.env
GLANCES1_URL="http://server1.local:61208"
GLANCES1_USERNAME=""
GLANCES1_PASSWORD=""

GLANCES2_URL="http://server2.local:61208"
GLANCES2_USERNAME=""
GLANCES2_PASSWORD=""
```

Then use with server number:
```bash
# Server 1 (default)
./scripts/glances-api.sh cpu

# Server 2
SERVER_NUM=2 ./scripts/glances-api.sh cpu
```

**Note**: Multi-server support requires script updates (not yet implemented)

## Reference

- [Glances REST API Documentation](references/api-endpoints.md) — Full endpoint reference
- [Glances Official Docs](https://glances.readthedocs.io/en/latest/api/restful.html)

---

## 🔧 Agent Tool Usage Requirements

**CRITICAL:** When invoking scripts from this skill via the zsh-tool, **ALWAYS use `pty: true`**.

Without PTY mode, command output will not be visible even though commands execute successfully.

**Correct invocation pattern:**
```typescript
<invoke name="mcp__plugin_zsh-tool_zsh-tool__zsh">
<parameter name="command">./skills/SKILL_NAME/scripts/SCRIPT.sh [args]</parameter>
<parameter name="pty">true</parameter>
</invoke>
```
