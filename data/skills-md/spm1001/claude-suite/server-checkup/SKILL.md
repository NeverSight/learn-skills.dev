---
name: server-checkup
description: Systematic Linux server management. Use BEFORE making changes to capture baseline, then AFTER for verification. Triggers on 'check this server', 'audit', 'set up this machine', 'security audit', 'harden this Pi', 'fresh Pi setup', 'provision this server'. (user)
---

# Server Maintenance

Systematic Linux server management with autonomous execution, risk assessment, and documentation.

## When to Use

- Setting up a new server or Pi
- Security audit or hardening
- Health check on existing infrastructure
- Before and after major changes (baseline → verify)
- Post-reflash configuration

## When NOT to Use

- Non-Linux systems (macOS, Windows)
- Cloud-managed services (use provider tools)
- Quick one-off commands (just run them)

## Execution Modes

### Interactive Mode (default)
Claude executes each phase, reports findings, asks for decisions on fixes.

### Auto Mode (advanced)
Spawns subagents for each phase automatically. Faster but less control.

**Trigger auto mode:** "full server audit" or "audit thoroughly"

### Partial Audits
- "security audit: <host>" → Phases 0, 2 only
- "setup maintenance: <host>" → Phases 0, 3 only
- "tailscale check: <host>" → Phases 0, 4 only

## Phase Workflow

### Phase 0: Context Discovery (NEW)

**Check for existing documentation FIRST:**

1. **Look for server-specific docs:**
   ```bash
   ls -la | grep -iE '(server|setup|readme|hostname)\.md'
   ls -la .claude/CLAUDE.md 2>/dev/null
   ```

2. **If found, read and extract:**
   - Services that should be running
   - Expected configurations (ports, paths, versions)
   - Known issues/quirks
   - Previous maintenance history
   - Setup steps that reveal intent

3. **Store context for validation:**
   - Compare actual state vs documented state
   - Flag discrepancies as findings
   - Incorporate known good configs

**Example:** If docs say "reboot at 04:00" but config shows "02:00" → flag for review.

### Phase 1: Connect & Triage

**CRITICAL: Capture baseline FIRST (before any changes):**

```bash
echo "=== BASELINE $(date +'%Y-%m-%d %H:%M') ===" | tee /tmp/server-baseline.txt
echo "Memory:" | tee -a /tmp/server-baseline.txt
free -h | tee -a /tmp/server-baseline.txt
echo -e "\nDisk:" | tee -a /tmp/server-baseline.txt
df -h / | tee -a /tmp/server-baseline.txt
echo -e "\nPackages:" | tee -a /tmp/server-baseline.txt
dpkg -l | grep -c '^ii' | tee -a /tmp/server-baseline.txt
echo -e "\nServices:" | tee -a /tmp/server-baseline.txt
systemctl list-units --type=service --state=running --no-pager | wc -l | tee -a /tmp/server-baseline.txt
```

**System discovery:**

1. **Check for errors:**
   ```bash
   # Without sudo (may fail, that's ok)
   dmesg 2>/dev/null | grep -iE 'error|fail|warn' | tail -20

   # With sudo if needed
   sudo dmesg | grep -iE 'error|fail|warn' | tail -20
   ```

2. **Hardware & OS:**
   ```bash
   uname -a && cat /etc/os-release | head -5
   free -h && df -h /
   dpkg -l | grep -c '^ii'  # package count
   ```

3. **Initial assessment:**
   - Note unusual errors
   - Check if disk space concerning (>80%)
   - Check if memory concerning (<500MB available)

### Phase 2: Security Audit

**SSH Configuration:**
```bash
grep -E '^(Password|PermitRoot|X11)' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null | grep -v '^#'
```

**Target state:**
- `PasswordAuthentication no` ✅
- `PermitRootLogin no` ✅
- `X11Forwarding no` ✅ (headless servers)

**Sudo configuration:**
```bash
sudo ls -la /etc/sudoers.d/
```

**Network exposure:**
```bash
# Listening ports (external only)
ss -tlnp 2>/dev/null | grep -v '127.0.0' | grep -v tailscale

# Firewall status
sudo systemctl status ufw 2>&1 | head -5 || sudo iptables -L -n | head -10
```

**Security scoring (auto-applied):**

| Finding | Risk Level | Fix Command |
|---------|------------|-------------|
| Password auth enabled | **CRITICAL** | `echo "PasswordAuthentication no" \| sudo tee -a /etc/ssh/sshd_config.d/99-hardening.conf && sudo systemctl reload sshd` |
| Root login enabled | **CRITICAL** | `echo "PermitRootLogin no" \| sudo tee -a /etc/ssh/sshd_config.d/99-hardening.conf && sudo systemctl reload sshd` |
| No firewall + port forwarding + external exposure | **HIGH** | Install ufw: `sudo apt install ufw` |
| No firewall + behind NAT + VPN only | **LOW** | Router + VPN provide protection |
| X11Forwarding on headless | **MEDIUM** | `echo "X11Forwarding no" \| sudo tee -a /etc/ssh/sshd_config.d/99-hardening.conf && sudo systemctl reload sshd` |

### Phase 3: Maintenance Setup

**Check unattended-upgrades:**
```bash
dpkg -l unattended-upgrades 2>&1 | grep '^ii'
```

**If missing:** `sudo apt install unattended-upgrades`

**Review configuration:**
```bash
sudo grep -E '^(Unattended-Upgrade::(Allowed-Origins|Remove|Automatic-Reboot))' /etc/apt/apt.conf.d/50unattended-upgrades | head -20
```

**Target configuration:**
- All packages (not just security) - see references/unattended-upgrades.md
- Auto-reboot enabled with specific time
- Unused packages removed
- Custom repos included (Tailscale, Plex, etc.)

**Verify service:**
```bash
systemctl status unattended-upgrades --no-pager | head -8
```

**Check reboot time is uncommented:**
```bash
sudo grep "Automatic-Reboot-Time" /etc/apt/apt.conf.d/50unattended-upgrades
```

### Phase 4: Tailscale (if applicable)

**Check if Tailscale installed:**
```bash
which tailscale && tailscale version || echo "Not installed"
```

**If installed, check status:**
```bash
tailscale status --self 2>&1 | head -3
tailscale status 2>&1 | grep -E 'exit node|subnet' | head -5
```

**Verify IP forwarding persisted:**
```bash
cat /etc/sysctl.d/99-tailscale.conf 2>/dev/null
```

**Should contain:**
```
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

**Post-setup reminder:** Disable key expiry in admin console for always-on nodes.

### Phase 5: Cleanup

**Identify unnecessary packages:**
```bash
dpkg -l | grep -E '^ii.*(man-db|bluetooth|bluez|avahi|pulseaudio|alsa)' | awk '{print $2}' | sort
```

**Check unnecessary services:**
```bash
systemctl list-unit-files | grep enabled | grep -E '(bluetooth|avahi|serial-getty)'
```

**Common removals for headless servers:**

| Package/Service | Why Remove | Risk | Command |
|----------------|------------|------|---------|
| man-db | Slows apt updates rebuilding man pages | **LOW** | `sudo apt remove --purge -y man-db` |
| avahi-daemon | mDNS not needed with Tailscale/static IPs | **LOW** | `sudo systemctl disable --now avahi-daemon.service avahi-daemon.socket` |
| bluetooth packages | Not used on servers | **LOW** | Keep libs, remove daemon if running |
| serial-getty | Not needed on headless | **LOW** | `sudo systemctl disable serial-getty@ttyS0` |

**Subagent decision matrix:**

| Scenario | Use Subagent? | Rationale |
|----------|---------------|-----------|
| Remove 1-2 packages | ❌ | Use `apt remove \| tail -10` |
| Remove 5+ packages | ✅ | Verbose output exhausts context |
| Check 1-2 services | ❌ | Direct commands fine |
| Full service audit | ✅ | Lots of parsing needed |

**Rule:** If operation produces >200 lines, use subagent.

**CRITICAL: Use terse output to avoid context exhaustion:**
```bash
# Good - terse
sudo apt remove -y pkg1 pkg2 pkg3 2>&1 | tail -10

# Bad - verbose
sudo apt remove -y pkg1 pkg2 pkg3  # Full output
```

### Phase 6: Verification

**Compare against baseline:**
```bash
echo -e "\n=== AFTER $(date +'%Y-%m-%d %H:%M') ===" | tee -a /tmp/server-baseline.txt
free -h | grep "Mem:" | tee -a /tmp/server-baseline.txt
df -h / | tail -1 | tee -a /tmp/server-baseline.txt
dpkg -l | grep -c '^ii' | tee -a /tmp/server-baseline.txt
systemctl list-units --type=service --state=running --no-pager | wc -l | tee -a /tmp/server-baseline.txt
```

**Key services check:**
```bash
systemctl list-units --type=service --state=running --no-pager | grep -E 'ssh|tailscale|docker|NetworkManager|unattended'
```

**Final summary:**
```bash
echo "=== Memory ===" && free -h | head -2
echo "=== Disk ===" && df -h /
echo "=== Packages ===" && dpkg -l | grep -c '^ii'
```

**Show improvements:**
- Memory freed
- Disk space saved
- Packages removed
- Services disabled

### Phase 7: Report Generation (NEW)

**Create maintenance record:**

**Option A: Append to existing server doc** (if found in Phase 0)
```markdown
## Maintenance History

### YYYY-MM-DD: <Brief Summary>

**Findings:**
- [Risk Level] Finding description
  - Fixed: command/action taken

**Changes Applied:**
- Security: X11 disabled, SSH hardened
- Cleanup: Removed N packages, disabled M services
- Performance: Freed XGB RAM, XGB disk

**System Health:**
- Memory: X available
- Disk: X% used
- Services: N running
- Uptime: N days
```

**Option B: Create new maintenance report**

Save as `MAINTENANCE-YYYY-MM-DD.md`:

```markdown
# Server Maintenance: <hostname>
Date: YYYY-MM-DD
Auditor: Claude Code

## Executive Summary
- **Overall Risk:** Low/Medium/High
- **Findings:** N total (X critical, Y high, Z medium)
- **Time to Fix:** ~N minutes
- **Changes Applied:** N fixes

## Critical Issues
[Auto-populated from Phase 2 findings with CRITICAL/HIGH risk]

## Security Audit
- SSH: ✅/⚠️
- Firewall: ✅/⚠️
- Services: ✅/⚠️

## Maintenance Setup
- Unattended-upgrades: ✅/⚠️
- Auto-reboot: ✅/⚠️
- Custom repos: ✅/⚠️

## Changes Applied
[Commands run with output summary]

## System Health
**Before:**
- Memory: X available
- Disk: X% used
- Packages: N installed

**After:**
- Memory: X available (+Y freed)
- Disk: X% used (+Y freed)
- Packages: N installed (-Y removed)

## Services Inventory
[What's running and why - from Phase 0 context + discovery]

## Recommendations
[Remaining issues sorted by risk level with fix commands]
```

**Ask user:** "Should I append to existing <hostname>.md or create new MAINTENANCE-<date>.md?"

## Decision Logic & Risk Scoring

### Automatic Risk Assessment

Each finding is automatically scored:

**Risk Dimensions:**
1. **Security Impact:** Does this expose the system?
2. **Blast Radius:** Local vs network vs internet exposure?
3. **Exploit Difficulty:** Easy (remote) vs Hard (local only)?

**Risk Levels:**

| Level | Criteria | Action Timeframe |
|-------|----------|------------------|
| **CRITICAL** | Remote exploit possible, privileged access | Fix immediately |
| **HIGH** | Exposure + missing security control | Fix today |
| **MEDIUM** | Unnecessary attack surface, limited exposure | Fix this week |
| **LOW** | Optimization, minimal risk | Optional cleanup |

### Example Decision Trees

**Firewall Assessment:**
```
IF no_firewall AND (port_forwarding OR dmz_host):
  IF tailscale_only_access:
    RISK = MEDIUM  # VPN provides some protection
  ELSE:
    RISK = HIGH    # Direct internet exposure
ELSE IF no_firewall AND behind_nat AND no_port_forwarding:
  RISK = LOW       # Router provides basic protection
```

**Service Assessment:**
```
IF service_running AND service_name IN unnecessary_list:
  IF service_listening_externally:
    RISK = MEDIUM  # Unnecessary exposure
  ELSE IF service_localhost_only:
    RISK = LOW     # Just resource waste
```

## Context Management

**Problem:** apt output, service lists, and package queries exhaust context during routine operations.

**Solutions:**

### 1. Terse Output (always)
```bash
# Good
apt remove pkg 2>&1 | tail -10
dpkg -l | grep -c '^ii'

# Bad
apt remove pkg  # Full output
dpkg -l         # List all packages
```

### 2. Subagents (for verbose operations)

**When to use:**
- Removing 5+ packages
- Auditing all systemd services
- Scanning large log files
- Full security scans

**Example:**
```
Use Task tool with subagent_type=Explore for package removal when >5 packages
```

### 3. Baseline Capture (before changes)
Store initial state, compare after changes to prove improvement.

### 4. Single Command Batching
```bash
# Good - one command
sudo apt remove -y pkg1 pkg2 pkg3 pkg4 pkg5

# Bad - five commands
sudo apt remove -y pkg1
sudo apt remove -y pkg2
...
```

## Quick Reference

### Passwordless sudo
```bash
echo "<user> ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/010_<user>-nopasswd
sudo chmod 440 /etc/sudoers.d/010_<user>-nopasswd
```

### SSH hardening config
```bash
cat <<'EOF' | sudo tee /etc/ssh/sshd_config.d/99-hardening.conf
PasswordAuthentication no
PermitRootLogin no
X11Forwarding no
EOF
sudo sshd -t && sudo systemctl reload sshd
```

### Find unattended-upgrades repo origin
```bash
# Check package policy
apt-cache policy <package> | grep -E 'origin|http'

# Check repo metadata
cat /var/lib/apt/lists/*_InRelease | grep -E '^Origin:|^Label:|^Codename:'
```

### Disable unnecessary service
```bash
sudo systemctl disable --now <service-name>
```

## References

Available in `references/` directory:
- `unattended-upgrades.md` - Repo origin patterns for Debian, Tailscale, Plex, etc.
- `packages-to-remove.md` - Common unnecessary packages for headless servers
- `ssh-hardening.md` - SSH configuration patterns and key-only auth
- `terminal-compat.md` - Ghostty/terminfo fixes for SSH compatibility

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Streaming full apt output | Context exhaustion | `\| tail -10` or subagent |
| Removing packages one-by-one | Slow, verbose | Single `apt remove pkg1 pkg2 pkg3` |
| Skipping baseline | Can't measure improvement | Always capture BEFORE changes |
| Forgetting reboot time | Immediate reboots during day | Verify uncommented + reasonable time |
| Checking config after changes | Can't compare | Baseline first, then changes |
| Not documenting changes | Future confusion | Always generate/update maintenance docs |

## Usage Examples

```
check this server: kube.lan (user: admin)     # Full audit
security audit: vps01 (user: root)            # Security only
full server audit: production-db              # Auto mode
check this server: kube.lan, skip tailscale   # Skip phase
```
