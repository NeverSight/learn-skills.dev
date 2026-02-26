---
name: system-watchdog
version: 1.0.0
description: System resource monitoring that detects wasteful or suspicious processes. Outputs structured JSON for any consumer.
---

# System Watchdog

Monitor system resources and flag wasteful or suspicious processes. Works standalone as a bash script — see `openclaw.md` for scheduled cron setup.

## Standalone Usage

Run the check script directly — no OpenClaw required:

```bash
bash check.sh
```

Outputs a JSON object to stdout. Parse it however you like — pipe to `jq`, feed to an agent, integrate into your own monitoring stack.

### Output Format

```json
{
  "suspicious": true,
  "summary": {
    "ram": "12.3/31.2 GB (39%)",
    "swap": "0.5/8.0 GB (6%)",
    "load": "1.2/0.8/0.6",
    "cores": 8,
    "disk": "120/256 GB (45%)"
  },
  "issues": [
    {
      "type": "high_ram",
      "description": "claude (PID 1234) 4650MB RAM",
      "details": { "pid": 1234, "name": "claude", "cpu_pct": 2.1, "mem_mb": 4650, "elapsed": "3d" }
    }
  ],
  "top_processes": [
    { "pid": 1234, "name": "claude", "cpu_pct": 2.1, "mem_mb": 4650, "elapsed": "3d" }
  ]
}
```

- `suspicious: true` → at least one issue exceeded a threshold
- `suspicious: false` → system looks healthy

### Thresholds

| Check | Threshold | Issue Type |
|-------|-----------|------------|
| Process RAM | > 4096 MB | `high_ram` |
| Process CPU | > 50% | `high_cpu` |
| Stale processes | Running > 2 days AND using > 100 MB or > 1% CPU | `stale` |
| Disk usage | > 80% on root mount | `disk` |

### Common Offenders

- `claude` / `codex` — AI coding agents left running for days
- `whisper` / `whisper-server` — speech-to-text servers consuming GPU/RAM
- `python` / `python3` — runaway scripts or leaked processes
- `node` — dev servers or builds that never stopped

## Agent Workflow (for AI agents)

1. Run `check.sh`
2. Parse the JSON output
3. If `suspicious` is `false` → do nothing (no report needed)
4. If `suspicious` is `true` → format a concise report and notify the user

### Suggested Report Format

```
⚠️ System Watchdog Report

📊 System: RAM 12.3/31.2 GB (39%) | Swap 0.5/8.0 GB (6%) | Load 1.2/0.8/0.6
💾 Disk: / 45% (120/256 GB)

🔴 Issues Found:

HIGH RAM — claude (PID 1234)
  CPU: 2.1% | RAM: 4650 MB | Running: 3 days
  → Likely stale, safe to kill

💡 Suggested: kill 1234
```

## Platform Notes

- **macOS only** — `check.sh` uses `sysctl`, `vm_stat`, and macOS `ps` flags. It won't work on Linux without adaptation (replace with `free`, `/proc/meminfo`, etc.).
- **Intermittent jq-style parse error** — the script occasionally fails on first run due to a race in process scanning. Retry once before reporting failure.
