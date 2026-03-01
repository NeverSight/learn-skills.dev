---
name: mt5-log-reader
description: Reads MetaTrader 5 log files to validate indicator execution, unit tests, and compilation errors. Use when user mentions Experts pane, MT5 logs, errors, or asks "did it work". Triggers - check logs, did it work, Experts pane, Print output, runtime errors, debug output. (project)
allowed-tools: Read, Grep, Bash
---

# MT5 Log Reader

## Overview

Read MetaTrader 5 log files programmatically to access Print() output from indicators, scripts, and expert advisors. Implements dual logging pattern where Print() statements go to MT5 logs (human-readable) and CSV files provide structured data for validation.

## When to Use

Use this skill when:
- Validating MT5 indicator/script execution
- Checking compilation or runtime errors
- Analyzing Print() debug output from indicators
- Verifying unit test results (Test_PatternDetector, Test_ArrowManager)
- User mentions checking "Experts pane" or "log" manually
- User asks "did it work?" or "check the output"

## Log File Structure

### Runtime Logs (Experts Pane)

MT5 runtime logs are stored at:
```
$MQL5_ROOT/Program Files/MetaTrader 5/MQL5/Logs/YYYYMMDD.log
```

**File Format**:
- Encoding: UTF-16LE (Little Endian) - Read tool handles automatically
- Structure: Tab-separated fields (timestamp, source, message)
- Size: Grows throughout day (typically 10-100KB, can reach 5MB+)

### Compilation Logs (Per-File)

MetaEditor creates a `.log` file next to each compiled `.mq5`:
```
# Example: Fvg.mq5 creates Fvg.log in the same directory
$MQL5_ROOT/Program Files/MetaTrader 5/MQL5/Indicators/Custom/Development/FVG/Fvg.log
```

**File Format**:
- Encoding: UTF-16LE (often readable with plain `cat`)
- Contains: Compilation progress, error count, warnings, timing
- Success indicator: "0 errors, 0 warnings"

**Important**: Wine/CrossOver returns exit code 1 even on successful compilation. Always check the `.log` file or verify `.ex5` exists.

## Workflow

### Step 1: Construct Log Path

Determine today's date and build the absolute path:

```bash
TODAY=$(date +"%Y%m%d")
LOG_FILE="$MQL5_ROOT/Program Files/MetaTrader 5/MQL5/Logs/${TODAY}.log"
```

### Step 2: Search for Relevant Entries

Use Grep tool to filter log entries (more efficient than reading entire file):

```
Pattern: indicator name, "error", "ERROR", "v0\\.4\\.0", "Phase 2", etc.
Path: Log file from Step 1
Output mode: "content"
-n: true (show line numbers)
-A: 5 (show 5 lines after matches for context)
```

**Common search patterns**:
- `CCI Rising Test|CCI_Rising_Test` - Find specific indicator output
- `error|ERROR|failed` - Find error messages
- `v0\\.4\\.0|v0\\.3\\.0` - Find specific version output
- `Phase \\d+|Test arrow created` - Find initialization messages
- `DEBUG Bar` - Find calculation output

### Step 3: Analyze Results

Check the grep output for:
- **Timestamps** - Verify output matches expected execution time
- **Error messages** - Identify specific failures with context
- **Version numbers** - Confirm correct .ex5 file is loaded
- **DEBUG output** - Validate calculation results
- **Test results** - Verify unit test pass/fail status

## Common Validation Patterns

### Check indicator version loaded

After compilation, verify the new .ex5 file is loaded:

```bash
# Search for version string in recent log entries
Pattern: "v0\\.4\\.0|=== CCI Rising Test"
Output mode: content
Context: -A 2
```

Look for initialization message with version number and timestamp matching the reload time.

### Find runtime errors

```bash
Pattern: "error|ERROR|failed|Failed"
Output mode: content
Context: -A 3 -B 1  # Show 3 lines after, 1 before
```

Analyze error codes (e.g., 4003 = invalid time) and error context.

### Monitor calculation output

```bash
Pattern: "DEBUG Bar"
Output mode: content
Context: -A 0  # No extra context needed
-n: true  # Show line numbers
```

Verify calculation values are reasonable (not EMPTY_VALUE, not reversed).

### Verify test arrow creation

```bash
Pattern: "Phase 2|Test arrow created|Failed to create"
Output mode: content
Context: -A 2
```

Check for success message with timestamp.

## Large Log Files

If log file exceeds 5MB (Read tool limit):

1. Use Grep exclusively (more efficient than reading entire file)
2. Use time-based filtering with `-A` and `-B` context
3. Search for specific indicator names to narrow results

## Integration with Dual Logging

This skill accesses one half of the dual logging pattern:

1. **MT5 Log Files** (this skill) - Human-readable Print() output
2. **CSV Files** (CSVLogger.mqh) - Structured audit trails

Both are accessible programmatically without user intervention.

## Security Considerations

- Log files may contain sensitive trading data (symbol names, account info)
- Do not expose absolute paths unnecessarily in user-facing output
- Filter sensitive information when reporting results
- No file modification operations allowed (read-only access)

## Examples

### Example 1: Verify indicator reloaded after compilation

```
User: "I reloaded the indicator, can you check if v0.4.0 is running?"

Action:
1. Grep for "v0\\.4\\.0|CCI Rising Test v0\\.4"
2. Check most recent match timestamp
3. Verify it's after compilation time (16:59)

Output: "Yes, v0.4.0 loaded at 17:01 on EURUSD M1 chart"
```

### Example 2: Find why histogram is empty

```
User: "The last 19 bars are still empty, check the log"

Action:
1. Grep for "DEBUG Bar|CCI=" pattern
2. Look for EMPTY_VALUE or unusual values
3. Check for error messages with -A 3 context

Output: "Found 'CCI=179769313486231570...' which is EMPTY_VALUE constant. The indicator didn't calculate CCI for those bars."
```

### Example 3: Validate calculation fix

```
User: "Check if the absolute value fix is working"

Action:
1. Grep for "DEBUG Bar.*\\|CCI\\|=" (looking for |CCI|= output)
2. Compare with old format "DEBUG Bar.*CCI=" (without |CCI|)
3. Check timestamp matches latest compilation

Output: "The log shows old format (no |CCI|=) at 16:56. Need to reload to get v0.4.0 from 16:59."
```

## References

- MT5 file locations: `docs/guides/MT5_FILE_LOCATIONS.md`
- Dual logging implementation: `docs/plans/cci-rising-pattern-marker.yaml` Phase 3-4
- CSVLogger library: `Program Files/MetaTrader 5/MQL5/Indicators/Custom/Development/CCINeutrality/lib/CSVLogger.mqh`
