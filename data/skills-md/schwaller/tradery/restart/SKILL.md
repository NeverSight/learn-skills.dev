---
name: restart
description: Restart the Plaiiin application. Use when asked to restart, relaunch, or reboot the app, or after making code changes that need testing.
---

# Restart Plaiiin

Kill any running Plaiiin instance and start fresh.

## Modules

The project has multiple runnable modules. **Restart the module you're currently working on** — infer from context (e.g., if editing tradery-news files, restart intel).

| Module | Start Script | Kill Script | Description |
|--------|--------------|-------------|-------------|
| **tradery-forge** | `scripts/start-forge.sh` | `scripts/kill-forge.sh` | Main UI app |
| **tradery-news** | `scripts/start-intel.sh` | `scripts/kill-intel.sh` | Intel/news app |
| **tradery-data-service** | `scripts/start-data-service.sh` | `scripts/kill-data-service.sh` | Background data service |
| **tradery-desk** | `scripts/start-desk.sh` | `scripts/kill-desk.sh` | Real-time signal desk |
| **tradery-runner** | `./gradlew :tradery-runner:run` | - | Strategy runner |

## Instructions

1. Kill existing processes:
   ```bash
   pkill -f "GradleWorkerMain" 2>/dev/null || true
   pkill -f "com.tradery" 2>/dev/null || true
   sleep 1
   ```

2. Start data service first (all apps depend on it), then the app:
   ```bash
   scripts/start-data-service.sh && sleep 2 && scripts/start-forge.sh
   ```

   Or for intel:
   ```bash
   scripts/start-data-service.sh && sleep 2 && scripts/start-intel.sh
   ```

## Data Service Log

The data service logs to `~/.tradery/logs/dataservice.log` and exposes a `/logs` endpoint:
```
curl -s "http://localhost:$(cat ~/.tradery/dataservice.port)/logs?lines=50"
```

## Notes

- **Use scripts, not gradle commands directly**
- Start data service before any app — they connect to it for aggTrades, funding, etc.
- App window appears within a few seconds
- Strategies auto-reload from `~/.tradery/strategies/` on file changes
