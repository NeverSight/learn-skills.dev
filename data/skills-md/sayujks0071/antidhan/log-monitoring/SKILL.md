---
name: log-monitoring
description: Monitor current logs in real-time, track log file sizes, watch for new entries, and check log health across system and strategy logs. Use when monitoring live logs, checking log status, watching for errors, or tracking log file growth.
---

# Log Monitoring

Monitor current logs across the OpenAlgo system in real-time. Track log file sizes, watch for new entries, detect log rotation, and check log health.

## Log Sources

### System Logs
- **Location**: `openalgo/log/`
- **Pattern**: `openalgo_YYYY-MM-DD.log` (daily rotation)
- **Rotation**: Midnight rotation, retains 14 days (configurable via `LOG_RETENTION`)
- **Max Size**: 10 MB per file before rotation

### Strategy Logs
- **Location**: `openalgo/strategies/logs/` or `openalgo/log/strategies/`
- **Pattern**: `{strategy_id}_*.log`
- **Access**: Web UI at `/python/logs/<strategy_id>`
- **Reports**: `strategy_report_*.txt` for daily summaries

### Web UI Logs
- **Endpoint**: `/logs` (filterable, searchable)
- **Streaming**: SSE endpoint for real-time log streaming

## Monitoring Workflow

### 1. Check Log Status

```bash
# List all log files with sizes
find openalgo/log -name "*.log*" -type f -exec ls -lh {} \;
find openalgo/strategies/logs -name "*.log" -type f -exec ls -lh {} \;

# Check current log file size
ls -lh openalgo/log/openalgo_*.log | tail -1

# Count log files
find openalgo/log -name "*.log*" | wc -l
```

### 2. Monitor Logs in Real-Time

```bash
# System logs (follow latest)
tail -f openalgo/log/openalgo_$(date +%Y-%m-%d).log

# Strategy-specific log
tail -f openalgo/strategies/logs/{strategy_id}_*.log

# Multiple logs simultaneously
tail -f openalgo/log/openalgo_*.log openalgo/strategies/logs/*.log

# Last N lines then follow
tail -n 100 -f openalgo/log/openalgo_*.log
```

### 3. Watch for Errors

```bash
# Monitor for errors in real-time
tail -f openalgo/log/openalgo_*.log | grep -iE "ERROR|WARNING|CRITICAL|exception|traceback"

# Monitor specific strategy for errors
tail -f openalgo/strategies/logs/{strategy_id}_*.log | grep -iE "ERROR|403|429|400"

# Count errors in recent logs
grep -iE "ERROR|CRITICAL" openalgo/log/openalgo_*.log | wc -l
```

### 4. Check Log Health

```bash
# Verify log rotation is working
ls -lh openalgo/log/openalgo_*.log | tail -5

# Check if logs are being written (recent modification)
find openalgo/log -name "*.log" -mmin -5

# Verify log directory permissions
ls -ld openalgo/log openalgo/strategies/logs

# Check disk space used by logs
du -sh openalgo/log openalgo/strategies/logs
```

## Common Monitoring Patterns

### Monitor All Active Strategies

```bash
# Find all active strategy log files
find openalgo/strategies/logs -name "*.log" -mmin -60 -type f

# Monitor all active strategy logs
find openalgo/strategies/logs -name "*.log" -mmin -60 -type f -exec tail -f {} +
```

### Track Log Growth

```bash
# Watch log file size growth
watch -n 5 'ls -lh openalgo/log/openalgo_*.log | tail -1'

# Check which logs are growing fastest
find openalgo/log openalgo/strategies/logs -name "*.log" -type f -exec sh -c 'echo "$(du -h "$1" | cut -f1) $1"' _ {} \; | sort -hr | head -10
```

### Monitor Log Rotation

```bash
# Check rotation status
ls -lh openalgo/log/openalgo_*.log | tail -15

# Verify rotation count matches retention setting
ls openalgo/log/openalgo_*.log* | wc -l
```

## Log Monitoring Scripts

### Quick Status Check

```bash
#!/bin/bash
# Check current log status
echo "=== System Logs ==="
ls -lh openalgo/log/openalgo_*.log | tail -3
echo ""
echo "=== Strategy Logs ==="
find openalgo/strategies/logs -name "*.log" -mmin -60 -type f | head -10
echo ""
echo "=== Recent Errors ==="
grep -iE "ERROR|CRITICAL" openalgo/log/openalgo_$(date +%Y-%m-%d).log | tail -5
```

### Continuous Monitoring

```bash
#!/bin/bash
# Monitor logs with error highlighting
tail -f openalgo/log/openalgo_$(date +%Y-%m-%d).log | \
  while IFS= read -r line; do
    if echo "$line" | grep -qiE "ERROR|CRITICAL"; then
      echo -e "\033[31m$line\033[0m"  # Red for errors
    elif echo "$line" | grep -qiE "WARNING"; then
      echo -e "\033[33m$line\033[0m"  # Yellow for warnings
    else
      echo "$line"
    fi
  done
```

## Web UI Monitoring

- **Log Viewer**: Access at `http://localhost:5000/logs`
- **Strategy Logs**: Access at `http://localhost:5000/python/logs/<strategy_id>`
- **Features**: Filter by level, search, date range, download

## Monitoring Best Practices

1. **Check log rotation**: Ensure logs rotate properly and don't fill disk
2. **Monitor error rates**: Track ERROR/CRITICAL frequency over time
3. **Watch file sizes**: Alert if logs exceed expected sizes
4. **Verify write access**: Ensure processes can write to log directories
5. **Track log growth**: Monitor disk space usage by logs
6. **Check timestamps**: Verify logs are being written recently

## Output Format

When monitoring logs, provide:

1. **Current Status**: Active log files and their sizes
2. **Recent Activity**: Last modification times
3. **Error Summary**: Count of recent errors/warnings
4. **Health Check**: Rotation status, disk usage, permissions
5. **Recommendations**: Any issues or optimizations needed

## Integration with Other Skills

- Use `log-analyzer` for detailed error analysis
- Use `log-drain-monitor` for observability stack setup
- Use `trading-operations` for strategy-specific log monitoring
