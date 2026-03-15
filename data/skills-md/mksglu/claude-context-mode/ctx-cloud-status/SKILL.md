---
name: ctx-cloud-status
description: |
  Show current Context Mode Cloud sync status.
  Displays connection health, sync config, and event statistics.
  Trigger: /context-mode:ctx-cloud-status
user-invocable: true
---

# Context Mode Cloud Status

Display the current cloud sync configuration, connection health, and event statistics.

## Instructions

1. **Read sync config** using Bash:
   ```
   cat ~/.context-mode/sync.json 2>/dev/null || echo "NOT_CONFIGURED"
   ```

2. **If not configured** (file missing or empty), display:
   ```
   ## context-mode cloud status
   - [ ] Cloud sync: NOT CONFIGURED

   Run `/ctx-cloud-setup` to connect to Context Mode Cloud.
   ```
   Stop here.

3. **If configured**, extract the config values. **Never display the full API token** — mask it as `ctx_****<last4>`.

4. **Run health check** using Bash:
   ```bash
   curl -sf -o /dev/null -w "%{http_code}" \
     -H "Authorization: Bearer <API_TOKEN>" \
     "<API_URL>/api/health"
   ```

5. **Check sync stats** — read the stats file if it exists:
   ```
   cat ~/.context-mode/sync-stats.json 2>/dev/null || echo "NO_STATS"
   ```
   This file may contain: `events_sent`, `last_sync_at`, `errors_count`, `last_error`.

6. **Display results** as markdown directly in the conversation:

   ```
   ## context-mode cloud status

   ### Connection
   - [x] Cloud sync: ENABLED
   - [x] API URL: https://api.context-mode.com
   - [x] API Token: ctx_****abcd
   - [x] Organization: org_abc123
   - [x] Health check: PASS (200 OK)

   ### Sync Settings
   - Batch size: 50
   - Flush interval: 30s

   ### Statistics
   - Events sent: 1,247
   - Last sync: 2 minutes ago
   - Errors: 0
   ```

   Use `[x]` for healthy items, `[ ]` for issues, `[-]` for warnings.

   **Variations:**

   - If `enabled` is `false`:
     ```
     - [-] Cloud sync: DISABLED (config exists but sync is turned off)
     ```

   - If health check fails:
     ```
     - [ ] Health check: FAIL (<http_code> or connection error)
     ```

   - If no stats file exists:
     ```
     ### Statistics
     - No sync data yet. Events will appear after the next Claude Code session.
     ```

   - If there are recent errors:
     ```
     - [-] Errors: 3 (last: "Sync failed: 401 Unauthorized")
     ```

7. **Actionable guidance** — after the status display, add context-specific advice:
   - If everything is healthy: *"Cloud sync is working normally."*
   - If health check fails: *"Run `/ctx-cloud-setup` to reconfigure your connection."*
   - If sync is disabled: *"To re-enable, set `enabled: true` in `~/.context-mode/sync.json`."*
   - If errors are present: *"Check your API token validity in the dashboard: **Settings > API Tokens**."*
