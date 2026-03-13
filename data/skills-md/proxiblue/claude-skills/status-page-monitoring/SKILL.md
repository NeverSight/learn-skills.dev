---
name: status-page-monitoring
description: Check status pages for down monitors and alert immediately. Uses curl + jq for accurate API parsing. Supports UptimeRobot, PayPal, and other status page providers.
---

# Status Page Monitoring Skill

## Overview
This skill checks the status of all monitored services and alerts immediately if any monitor is showing DOWN status.

**Primary method:** `curl + jq` for accurate JSON parsing (avoids WebFetch AI summarization errors)

Supports multiple status page providers via direct API endpoints.

## When to Use This Skill
- User runs `/status-page-monitoring`
- User asks "check status" or "are sites up?"
- User wants to know if any monitors are down
- User asks about uptime or service status

## Monitoring Workflow

**IMPORTANT: Do NOT read scripts or search for configuration files.** This skill provides all the information you need.

### Step 1: Check Monitor Status

> **CRITICAL: Use curl + jq for accurate results!**
> WebFetch AI summarization is unreliable for parsing status data. Always use curl + jq to fetch and parse API endpoints directly.

#### Option A: curl + jq (PREFERRED - Most Accurate)

Use Bash with curl and jq to fetch raw API data and parse it directly. This avoids AI summarization errors.

**UptimeRobot Example:**
```bash
# Fetch and parse UptimeRobot status
curl -s "https://stats.uptimerobot.com/api/getMonitorList/Zk2EbUnM73" | jq -r '.psp.monitors[] | "\(.name): \(.statusClass)"' | sort
```

**Status class mapping:**
- `success` = UP
- `danger` = DOWN
- `paused` = PAUSED

**Count by status:**
```bash
# Count monitors by status
curl -s "https://stats.uptimerobot.com/api/getMonitorList/Zk2EbUnM73" | jq -r '
  .psp.monitors | group_by(.statusClass) |
  map({status: .[0].statusClass, count: length}) |
  .[] | "\(.status): \(.count)"'
```

**Get DOWN monitors only:**
```bash
# List only DOWN monitors
curl -s "https://stats.uptimerobot.com/api/getMonitorList/Zk2EbUnM73" | jq -r '.psp.monitors[] | select(.statusClass == "danger") | .name'
```

### Known API Patterns by Provider

#### UptimeRobot (Primary - This Project)
```
Status page: https://stats.uptimerobot.com/{PAGE_ID}
API endpoint: https://stats.uptimerobot.com/api/getMonitorList/{PAGE_ID}
```
Example: `https://stats.uptimerobot.com/api/getMonitorList/Zk2EbUnM73`

#### PayPal Status
```bash
# Fetch PayPal component status
curl -s "https://paypal-status.com/api/v1/components" | jq -r '.[] | "\(.name): \(.status)"'
```
Returns all PayPal services: Checkout, APIs, Account Management, Braintree, Venmo, etc.

#### Atlassian Statuspage (Generic)
Many services use Atlassian Statuspage. Try these endpoints with curl + jq:
```bash
# Summary endpoint
curl -s "https://status.example.com/api/v2/summary.json" | jq -r '.components[] | "\(.name): \(.status)"'

# Components endpoint
curl -s "https://status.example.com/api/v2/components.json" | jq -r '.components[] | "\(.name): \(.status)"'

# Status endpoint (simple)
curl -s "https://status.example.com/api/v2/status.json" | jq -r '.status.description'
```

#### AWS Health Dashboard
```
Status page: https://health.aws.amazon.com/health/status
```
AWS Health Dashboard is JavaScript-heavy. Try using lynx if installed:
```bash
lynx -dump "https://health.aws.amazon.com/health/status" 2>/dev/null | grep -E "(disruption|degraded|operational)"
```

If lynx is not available, use WebFetch as a fallback (less reliable).

#### Unknown Provider
If provider is unknown, try these common API patterns with curl:
```bash
# Try in order:
curl -s "https://status.example.com/api/v1/components" | jq '.'
curl -s "https://status.example.com/api/v2/components.json" | jq '.'
curl -s "https://status.example.com/api/v2/summary.json" | jq '.'
curl -s "https://status.example.com/api/status" | jq '.'
```

#### Option B: WebFetch (Fallback Only)
Use WebFetch only when:
- No API endpoint is known
- curl + jq approach doesn't work for the provider

**WARNING:** WebFetch uses AI summarization which can misinterpret status data. Always verify results if using WebFetch.

#### Option C: Text Browsers (For JavaScript-heavy pages)
For pages that require JavaScript rendering and have no API:
```bash
# Try lynx (preferred)
lynx -dump "https://status.example.com" 2>/dev/null

# Or w3m
w3m -dump "https://status.example.com" 2>/dev/null

# Or links
links -dump "https://status.example.com" 2>/dev/null
```

**Note:** Install text browsers if needed:
```bash
apt install lynx    # Debian/Ubuntu
brew install lynx   # macOS
```

### Step 2: Identify Down Monitors

For UptimeRobot, use this command to get only DOWN monitors:
```bash
curl -s "https://stats.uptimerobot.com/api/getMonitorList/Zk2EbUnM73" | jq -r '
  .psp.monitors[] | select(.statusClass == "danger") |
  "DOWN: \(.name)"'
```

For a full summary with counts:
```bash
curl -s "https://stats.uptimerobot.com/api/getMonitorList/Zk2EbUnM73" | jq -r '
  (.psp.monitors | length) as $total |
  (.psp.monitors | map(select(.statusClass == "success")) | length) as $up |
  (.psp.monitors | map(select(.statusClass == "danger")) | length) as $down |
  (.psp.monitors | map(select(.statusClass == "paused")) | length) as $paused |
  "Total: \($total) | UP: \($up) | DOWN: \($down) | PAUSED: \($paused)"'
```

### Step 3: Alert Format

#### If ALL monitors are UP:
```
STATUS: ALL SYSTEMS OPERATIONAL

[count] monitors checked - all UP
[count] monitors PAUSED (intentional)
Last check: [timestamp]
```

#### If ANY monitor is DOWN:
```
ALERT: MONITOR(S) DOWN

DOWN:
  - [Monitor Name] - [URL]
    Status: DOWN for [duration]
    Incident ID: [id]

UP: [count] monitors operational
PAUSED: [count] monitors paused

Recommended Actions:
1. Check the affected URL directly
2. SSH to server and check services
3. Review server logs
```

### Step 4: Quick Status Filters
To check only DOWN monitors:
```bash
mcp-cli call uptimerobot/list-monitors '{"filter": ["DOWN"], "limit": 100}'
```

## Alert Severity Levels

| Status | Severity | Action |
|--------|----------|--------|
| DOWN | CRITICAL | Immediate alert, investigate now |
| PAUSED | INFO | Informational, monitor intentionally stopped |
| UP | OK | No action needed |

## Example Output

### All Systems OK
```
STATUS CHECK COMPLETE

All 22 monitors are UP

Sites monitored:
- NTO Tank (ntotank.com)
- Protank (protank.com)
- PVC Pipe Supplies (pvcpipesupplies.com)
- IBC Tanks (ibctanks.com)

1 monitor PAUSED (Protank & Equipment - intentional)

No action required.
```

### System Down
```
CRITICAL ALERT

1 MONITOR DOWN:

  NTO Tank
  URL: https://www.ntotank.com
  Status: DOWN
  Duration: 5 minutes
  Incident: #269634131363671187

IMMEDIATE ACTIONS:
1. Check https://www.ntotank.com directly
2. SSH to server and check services
3. Review error logs
4. Check DNS/SSL status

21 other monitors operational.
```

## Claude Code Status Bar Integration

Display monitor status directly in the Claude Code status bar for always-visible monitoring.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ [Opus] $0.12 | 21 OK                    <- All systems up   │
│ [Opus] $0.12 | 21 1 (NTO HomePage)      <- 1 monitor down   │
│ [Opus] $0.12 | ? stale                  <- Cache outdated   │
└─────────────────────────────────────────────────────────────┘
```

**Architecture:**
1. **Cron job** runs periodically, invokes Claude CLI with this skill
2. **Claude** uses the skill to fetch and parse status from any supported provider
3. **Bash script** captures Claude's JSON output, writes to cache file
4. **Status bar script** reads cache file, displays in Claude Code status line

This approach leverages Claude's ability to parse multiple status page providers using the skill's documented patterns.

### Setup Instructions

#### Step 1: Scripts Location

The scripts are located in your project:
```
.claude/scripts/status-monitor-cron.sh   # Cron job - fetches & caches status
.claude/scripts/statusline-with-monitors.sh  # Status bar - displays cached status
```

#### Step 2: Configure Cron Job

Add to crontab to run the status check periodically:
```bash
crontab -e
```

Add this line (adjust path to your project):
```bash
# Every 5 minutes (recommended - balances freshness vs API costs)
*/5 * * * * /var/www/html/.claude/scripts/status-monitor-cron.sh

# Every 15 minutes (lower cost)
*/15 * * * * /var/www/html/.claude/scripts/status-monitor-cron.sh
```

**Note:** This invokes Claude CLI which uses API credits. Choose interval based on:
- How critical real-time status is for you
- Your API usage budget
- The skill handles any provider (UptimeRobot, PayPal, AWS, etc.) automatically

> **⚠️ COST ALERT: Review the cost estimates below before configuring cron frequency!**

### Cron Job Cost Estimates

Running this skill via cron invokes Claude CLI, which consumes API credits. Plan your monitoring frequency accordingly.

#### Token Usage Per Check (Estimated)

| Component              | Tokens       |
|------------------------|--------------|
| Prompt + skill context | ~2,000-4,000 |
| Bash (curl + jq) call  | ~50          |
| Bash result            | ~100-200     |
| JSON output            | ~50          |
| **Total**              | **~2,500-4,500** |

*Note: curl + jq uses fewer tokens than WebFetch since it returns raw data without AI summarization overhead.*

#### Cost Per Check (Claude Sonnet Pricing)

| Type   | Tokens | Rate   | Cost    |
|--------|--------|--------|---------|
| Input  | ~4,000 | $3/1M  | $0.012  |
| Output | ~200   | $15/1M | $0.003  |
| **Total** |     |        | **~$0.015** |

#### Daily/Monthly Cost by Interval

| Interval     | Checks/day | Cost/day | Cost/month |
|--------------|------------|----------|------------|
| Every 1 min  | 1,440      | ~$21.60  | ~$648      |
| Every 5 min  | 288        | ~$4.32   | ~$130      |
| Every 15 min | 96         | ~$1.44   | ~$43       |
| Every 30 min | 48         | ~$0.72   | ~$22       |
| Every 1 hour | 24         | ~$0.36   | ~$11       |

#### Recommendations

| Use Case | Recommended Interval | Estimated Cost |
|----------|---------------------|----------------|
| Production-critical sites | Every 5-15 min | $1.50-4.50/day |
| General awareness | Every 15-30 min | $0.70-1.50/day |
| Low-priority/dev sites | Every 30-60 min | $0.35-0.70/day |

**Cost-saving tips:**
- Use longer intervals (15-30 min) for non-critical monitoring
- Consider using free UptimeRobot email alerts as primary notification
- Use this cron integration for status bar visibility, not primary alerting
- curl + jq is more cost-effective than WebFetch (fewer tokens, more accurate)

#### Step 3: Configure Claude Code Status Line

Add to your Claude Code settings file.

**Project-level** (`.claude/settings.local.json`):
```json
{
  "statusLine": {
    "type": "command",
    "command": "/var/www/html/.claude/scripts/statusline-with-monitors.sh"
  }
}
```

**Or user-level** (`~/.claude/settings.json`):
```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/your/project/.claude/scripts/statusline-with-monitors.sh"
  }
}
```

#### Step 4: Verify Setup

1. **Test cron script manually** (this will invoke Claude CLI):
```bash
.claude/scripts/status-monitor-cron.sh
cat /tmp/monitor-status.json
```

Expected output:
```json
{"up": 21, "down": 1, "paused": 1, "down_names": "NTO HomePage", "timestamp": "..."}
```

2. **Test status line script:**
```bash
echo '{"model":{"display_name":"Test"},"cost":{"total_cost_usd":0.05}}' | .claude/scripts/statusline-with-monitors.sh
```

3. **Restart Claude Code** to load the new status line configuration.

### Status Bar Display

| Display | Meaning |
|---------|---------|
| `21 OK` | All 21 monitors are UP (green) |
| `21 1 (Name)` | 21 UP, 1 DOWN - shows name of down monitor |
| `21 3` | 21 UP, 3 DOWN (red) |
| `? stale` | Cache file older than 5 minutes (yellow) |
| `! error` | API fetch failed (yellow) |
| `-` | No cache file found |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STATUS_CACHE_FILE` | `/tmp/monitor-status.json` | Where to store cached status |
| `CLAUDE_CMD` | `claude` | Path to Claude CLI executable |

### Cache File Format

The cron job writes JSON to the cache file:
```json
{
    "up": 21,
    "down": 1,
    "paused": 1,
    "down_names": "NTO HomePage",
    "timestamp": "2026-01-15T22:30:00+00:00",
    "error": false
}
```

### Troubleshooting

**Status bar shows `-`:**
- Cron job hasn't run yet, or cache file doesn't exist
- Run manually: `.claude/scripts/status-monitor-cron.sh`
- Check cache: `cat /tmp/monitor-status.json`

**Status bar shows `? stale`:**
- Cron job not running or failing
- Check cron logs: `grep CRON /var/log/syslog`
- Verify crontab: `crontab -l`

**Status bar shows `! error`:**
- Claude CLI failed or returned invalid output
- Test manually: `.claude/scripts/status-monitor-cron.sh && cat /tmp/monitor-status.json`
- Check Claude CLI is installed: `which claude`
- Check Claude CLI auth: `claude --version`

**Status bar not updating:**
- Claude Code status line updates every 300ms max
- Restart Claude Code if settings changed
- Check script is executable: `chmod +x .claude/scripts/statusline-with-monitors.sh`

**Claude CLI not found:**
- Ensure Claude CLI is in PATH for cron
- Use full path in cron: `CLAUDE_CMD="/path/to/claude" /path/to/status-monitor-cron.sh`

**jq not found:**
- Install jq: `apt install jq` or `brew install jq`

### Customization

**Change cache location:**
```bash
# In crontab
*/5 * * * * STATUS_CACHE_FILE="/custom/path/status.json" /path/to/status-monitor-cron.sh
```

**Specify Claude CLI path:**
```bash
# In crontab (if claude not in PATH)
*/5 * * * * CLAUDE_CMD="/usr/local/bin/claude" /path/to/status-monitor-cron.sh
```

**Extend status bar script** to show additional info by editing `.claude/scripts/statusline-with-monitors.sh`.

## Success Criteria

- Monitor status always visible in status bar
- DOWN monitors highlighted in red
- No latency impact (reads from cache, not API)
- Stale/error states clearly indicated
- Works across Claude Code sessions
