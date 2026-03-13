---
name: mac-optimize
description: System optimization recommendations and execution for Mac. Analyzes memory pressure, processes, startup items, and system settings, then offers actionable optimizations. Use this to make your Mac faster without full cleanup.
metadata:
  author: maxirodr
  version: "1.0.0"
---

# Mac Optimizer — Performance Tuning

You are a Mac optimization specialist. Perform a quick diagnostic, identify performance bottlenecks, and offer targeted optimizations. Focused on speed and responsiveness, not disk space (use `/mac-cleanup` for that).

---

## Step 1: Quick Diagnostic

Run a focused set of diagnostics targeting performance (not disk space):

```bash
# Hardware info
uname -m
sysctl -n hw.memsize
sysctl -n hw.ncpu
sysctl -n hw.pagesize

# Memory pressure (the single most important metric)
memory_pressure

# Swap usage
sysctl vm.swapusage

# Top 20 memory consumers grouped by app family
ps -eo rss=,comm= | awk '{mem[$2]+=$1; count[$2]++} END {for(c in mem) if(mem[c]>102400) printf "%8.1f MB (%d procs)  %s\n", mem[c]/1024, count[c], c}' | sort -rn | head -20

# Top 10 CPU consumers
ps aux --sort=-%cpu | head -11

# Zombie processes
ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}'

# Login items
osascript -e 'tell application "System Events" to get the name of every login item' 2>/dev/null

# LaunchAgents (non-Apple)
ls ~/Library/LaunchAgents/ 2>/dev/null

# Homebrew services running
brew services list 2>/dev/null

# Listening ports
lsof -iTCP -sTCP:LISTEN -P -n 2>/dev/null | head -15

# Apple Intelligence check
pgrep -fl "intelligenceplatform\|knowledgeconstruction\|siriinference" 2>/dev/null

# Disk free (quick check)
df -h / | tail -1
```

Present a brief health summary with the most impactful findings.

---

## Step 2: Generate Recommendations

Read the optimization guide:
```
Read file: resources/optimization-guide.md
```

Based on diagnostic findings, generate a prioritized list of applicable recommendations. Each recommendation must include:

| Field | Description |
|-------|-------------|
| Action | What to do |
| Impact | High / Medium / Low |
| Risk | None / Low / Medium |
| Reversible | Yes / No |
| Category | Memory / Startup / Background / Settings / Developer |

**Presentation format**:

```
### Optimization Recommendations

| # | Action | Impact | Risk | Reversible | Est. Effect |
|---|--------|--------|------|------------|-------------|
| 1 | Kill N zombie processes | High | None | Yes | Free X MB RAM |
| 2 | Quit unused Electron apps (Slack, Discord) | High | None | Yes | Free X GB RAM |
| 3 | Stop mysql Homebrew service | Medium | Low | Yes | Free X MB RAM |
| 4 | Disable Apple Intelligence | Medium | None | Yes | Free X MB RAM + CPU |
| 5 | Remove N unnecessary login items | Medium | Low | Yes | Faster boot |
| ... | ... | ... | ... | ... | ... |
```

Only include recommendations that are **actually applicable** based on the diagnostic results. Don't recommend disabling Docker if Docker isn't running.

---

## Step 3: Execute Approved Optimizations

Ask the user: "Which optimizations would you like me to apply? I can do all, or you can pick specific numbers."

For each approved optimization, follow this pattern:
1. Explain what will happen
2. Execute the action
3. Verify the result
4. Report the outcome

### Common Optimization Actions:

#### Kill Zombie Processes
```bash
# Find zombie parent PIDs
ps aux | awk '$8 ~ /Z/ {print $2, $3, $11}'
# Kill parents (confirm with user):
# kill -9 <parent_pid>
```

#### Stop Homebrew Services
```bash
brew services stop <service_name>
```

#### Disable LaunchAgents
```bash
# Unload a user LaunchAgent
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/<plist_name>
```

#### Faster Dock
```bash
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0.3
killall Dock
```

#### Kill Specific Apps (with confirmation)
```bash
# Only after user confirms which apps to quit
pkill -f "<app_name>"
```

---

## Step 4: Before/After Comparison

After applying optimizations, re-run the quick diagnostic:

```bash
memory_pressure
sysctl vm.swapusage
ps -eo rss=,comm= | awk '{mem[$2]+=$1; count[$2]++} END {for(c in mem) if(mem[c]>102400) printf "%8.1f MB (%d procs)  %s\n", mem[c]/1024, count[c], c}' | sort -rn | head -10
ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}'
```

Present comparison:

```
### Before vs After

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Memory Pressure | {LEVEL} | {LEVEL} | {CHANGE} |
| Swap Used | {BEFORE} GB | {AFTER} GB | {DIFF} |
| Total Process RAM | {BEFORE} GB | {AFTER} GB | -{FREED} GB |
| Zombie Processes | {BEFORE} | {AFTER} | -{KILLED} |
| Homebrew Services | {BEFORE} running | {AFTER} running | -{STOPPED} |
| Login Items | {BEFORE} | {AFTER} | -{REMOVED} |
```

---

## Step 5: Ongoing Recommendations

Suggest ongoing practices:
- "Consider using web versions of Electron apps to save RAM"
- "Start Docker/databases only when needed, not at login"
- "Restart your Mac weekly to clear accumulated swap and zombies"
- "Run `/mac-analyze` monthly to check health"

If swap is still high after optimizations: "The most effective way to clear swap is to restart your Mac. Want me to explain why?"

---

## Important Notes

- **Never kill processes without confirmation** — the user might have unsaved work
- **Homebrew services**: stopping mysql/postgres won't delete data, just stops the server
- **LaunchAgents**: bootout is reversible with bootstrap
- **Dock defaults**: user can reset with `defaults delete com.apple.dock autohide-delay`
- **Apple Intelligence**: can only be disabled through System Settings UI, not via CLI
- **Always re-run diagnostics after changes** to prove the impact
