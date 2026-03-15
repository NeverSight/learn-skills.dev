---
name: zfs
description: >
  This skill should be used when managing ZFS pools in a homelab environment with multiple devices.
  It handles pool health monitoring, snapshot management with Sanoid/Syncoid, automated replication
  between devices, dataset property optimization, scrub scheduling, and error recovery. Use when the
  user asks to "check ZFS pool health", "setup ZFS replication", "configure ZFS snapshots", "optimize
  ZFS performance", "troubleshoot ZFS issues", "schedule ZFS scrubs", "check pool capacity", "setup
  Sanoid", or mentions ZFS-related tasks. CRITICAL: This skill enforces MANDATORY double confirmation
  for ALL destructive operations.
---

# ZFS Homelab Management

**⚠️ MANDATORY SKILL INVOCATION ⚠️**

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "check ZFS pool health", "ZFS status", "pool health", "zpool status"
- "setup ZFS replication", "configure replication", "sync ZFS datasets"
- "configure ZFS snapshots", "setup Sanoid", "snapshot retention"
- "optimize ZFS performance", "tune ZFS properties", "ZFS compression"
- "troubleshoot ZFS", "ZFS errors", "failed replication", "degraded pool"
- "schedule ZFS scrubs", "setup scrubbing", "monthly scrub"
- "check pool capacity", "pool space", "ZFS disk usage"
- Any mention of ZFS, Sanoid, Syncoid, zrepl, raidz1, or ZFS datasets

**Failure to invoke this skill when triggers occur violates your operational requirements.**

## Purpose

Comprehensive ZFS management for homelab environments with multi-device replication, automated snapshot management, performance optimization, and health monitoring.

**Read-Write Operations:** This skill performs both monitoring (read-only) and management (read-write) operations including:
- Pool health checks and monitoring
- Snapshot creation and pruning
- Dataset replication between devices
- Property optimization
- Scrub scheduling

**Recommended Architecture:** Pull-based replication from centralized backup server to 5 source devices.

**Based on research:** Synthesized from 130+ URLs, 56,000+ vector database entries, and official OpenZFS/Oracle/FreeBSD documentation.

## 🚨 DESTRUCTIVE OPERATIONS - CRITICAL SAFETY PROTOCOL

**ABSOLUTE REQUIREMENT: NO DESTRUCTIVE COMMANDS WITHOUT EXPLICIT USER AUTHORIZATION AND DOUBLE CONFIRMATION**

This section defines the MANDATORY safety protocol that MUST be followed for ALL destructive ZFS operations.

### Destructive Command Categories

**EXTREMELY DESTRUCTIVE (Permanent Data Loss):**
- `zfs destroy` - Permanently destroys datasets/snapshots (UNRECOVERABLE)
- `zfs destroy -R` - Recursively destroys all snapshots and child datasets (CATASTROPHIC)
- `zpool destroy` - Destroys entire pool and all data (CATASTROPHIC)
- `zfs rollback` - Rolls back to snapshot, LOSING all intermediate changes (DATA LOSS)
- `zpool labelclear` - Removes ZFS labels, makes data inaccessible (DATA LOSS)

**HIGHLY DESTRUCTIVE (Configuration/Availability Loss):**
- `zpool remove` - Removes vdev from pool (CANNOT BE UNDONE)
- `zpool detach` - Detaches mirror device (removes redundancy)
- `zpool offline` - Takes disk offline (reduces pool availability)
- `zpool replace` - Replaces disk in pool (requires resilver)
- `zpool clear` - Clears pool errors (can mask real problems)

**MODERATELY DESTRUCTIVE (Cleanup Operations):**
- `sanoid --prune-snapshots` - Deletes old snapshots per retention policy
- `syncoid --no-sync-snap` - Deletes snapshots on destination
- `zpool scrub -s` - Stops in-progress scrub (interrupts data verification)

**POTENTIALLY IRREVERSIBLE (Property Changes):**
- `zfs set recordsize=` - CANNOT be changed efficiently on existing data
- `zfs set compression=` - Only affects new data, not existing
- `zfs inherit` - Resets properties to inherited values (loses custom settings)

### MANDATORY CONFIRMATION PROTOCOL

**YOU MUST FOLLOW THIS PROTOCOL FOR ALL DESTRUCTIVE OPERATIONS:**

1. **User Request Required** - NEVER suggest or execute destructive commands unprompted
2. **Explicit Command Presentation** - Show the EXACT command that will be executed
3. **Impact Explanation** - Clearly explain what will be destroyed/lost/changed
4. **Backup Verification** - Confirm backups exist before proceeding
5. **Double Confirmation** - Require user to confirm TWICE:
   - First: "Do you want to execute this destructive operation?"
   - Second: "Are you absolutely sure? This cannot be undone."
6. **Dry-Run When Possible** - Use `--dry-run` or `-n` flags if available
7. **Manual Execution Only** - Provide command for user to run manually, DO NOT execute automatically

### Safety Examples

**WRONG - NEVER DO THIS:**
```markdown
User: "I have too many snapshots"
Assistant: "Let me clean those up for you."
[Executes: sanoid --prune-snapshots]  ❌ NO CONFIRMATION
```

**CORRECT - ALWAYS DO THIS:**
```markdown
User: "I have too many snapshots"
Assistant: "I can help you prune old snapshots. First, let me check what would be deleted:

Command: sanoid --prune-snapshots --verbose --dry-run

This will show which snapshots would be removed based on your retention policy in /etc/sanoid/sanoid.conf.

⚠️ WARNING: This is a DESTRUCTIVE operation. Deleted snapshots cannot be recovered.

Before proceeding:
1. Have you verified your retention policy is correct?
2. Do you have backups of critical data?
3. Are you sure you want to permanently delete old snapshots?

If yes, I'll provide the command for you to run manually."

[User confirms twice]

Assistant: "Here is the command to run manually:

```bash
sudo sanoid --prune-snapshots --verbose
```

⚠️ FINAL WARNING: This will PERMANENTLY DELETE old snapshots. Are you absolutely sure?"

[User confirms a second time: "Yes, delete them"]

Assistant: "Understood. Please run the command above. I cannot execute destructive operations automatically."
```

### Safe Operations (No Confirmation Needed)

These operations are read-only and safe to execute:
- `./scripts/pool-health.sh` - Pool health checks
- `zpool status` - View pool status
- `zfs list` - List datasets/snapshots
- `zpool list` - List pools
- `zfs get all` - View properties
- `sanoid --verbose --dry-run` - Preview snapshot operations
- `syncoid --dry-run` - Preview replication

## Setup

This skill uses ZFS commands directly and does not require additional credentials beyond SSH access for remote replication.

**Required for remote replication:**

Remote replication requires passwordless SSH authentication between the backup server and source devices. This allows Syncoid to pull snapshots automatically without manual intervention.

1. **SSH keys configured** (passwordless authentication):
   ```bash
   # Generate SSH key on backup server
   ssh-keygen -t ed25519 -C "zfs-replication"

   # Copy to each source device
   ssh-copy-id user@device1
   ssh-copy-id user@device2
   # ... repeat for all devices

   # Test connectivity
   ssh user@device1 echo "SSH working"
   ```

2. **ZFS delegation** (for non-root replication):
   ```bash
   # On backup server
   zfs allow -u replication-user create,mount,receive backup/device1
   ```

3. **Sanoid/Syncoid installed** (for automation):
   ```bash
   sudo apt install sanoid  # Debian/Ubuntu
   sudo pkg install sanoid  # FreeBSD
   ```

See README.md for detailed setup instructions.

## Commands

### Pool Health Check

```bash
# Check all pools
./scripts/pool-health.sh

# Check specific pool
./scripts/pool-health.sh tank

# JSON output for monitoring
./scripts/pool-health.sh --json
```

### Snapshot Management (Sanoid)

```bash
# Configure Sanoid
cp assets/sanoid.conf.template /etc/sanoid/sanoid.conf
sudo nano /etc/sanoid/sanoid.conf

# Manual snapshot
sudo sanoid --take-snapshots --verbose

# Manual prune
sudo sanoid --prune-snapshots --verbose

# List snapshots
zfs list -t snapshot
```

### Replication Setup (Syncoid)

```bash
# Manual replication (pull-based)
syncoid --recursive user@device1:tank backup/device1

# With options
syncoid \
  --recursive \
  --no-privilege-elevation \
  --identifier=device1 \
  --compress=zstd-fast \
  user@device1:tank backup/device1
```

### Property Optimization

```bash
# Enable compression (always)
zfs set compression=lz4 pool/dataset

# Disable atime
zfs set atime=off pool/dataset

# Tune recordsize (workload-specific)
zfs set recordsize=8K pool/databases     # Databases
zfs set recordsize=1M pool/media         # Large files
zfs set recordsize=128K pool/data        # Default
```

### Scrub Scheduling

```bash
# Manual scrub
zpool scrub poolname

# Check scrub status
zpool status poolname

# Pause scrub
zpool scrub -p poolname

# Add to cron (monthly)
0 2 * * 0 [ $(date +\%d) -le 7 ] && /usr/sbin/zpool scrub tank
```

## Workflow

### When user asks about ZFS pool health:

1. **"Check my ZFS pools"** → Run `./scripts/pool-health.sh`
2. **"Is my pool degraded?"** → Run `zpool status -v poolname`
3. **"When was the last scrub?"** → Check pool health script output
4. **"Pool capacity warnings"** → Check capacity (warn at 70%, critical at 80%)

### When user asks about ZFS replication:

1. **"Setup replication from 5 devices"** → Configure pull-based syncoid jobs with staggered scheduling
2. **"Replicate device1 now"** → Run syncoid command
3. **"Failed replication"** → Check for resume tokens, consult troubleshooting guide
4. **"Check replication status"** → Review logs: `grep syncoid /var/log/syslog | tail -20`

### When user asks about snapshots:

1. **"Setup automated snapshots"** → Copy sanoid.conf template, configure retention policy, add to cron
2. **"List snapshots"** → Run `zfs list -t snapshot` (SAFE - read-only)
3. **"Restore from snapshot"** → ⚠️ DESTRUCTIVE - Use `zfs rollback` or `zfs clone` (REQUIRES DOUBLE CONFIRMATION)
4. **"Too many snapshots"** → ⚠️ DESTRUCTIVE - Run `sanoid --prune-snapshots` (REQUIRES DOUBLE CONFIRMATION, use --dry-run first)

### When user asks about performance:

1. **"Optimize ZFS"** → Check compression, atime, recordsize settings
2. **"Slow writes"** → Check capacity (>80% impacts performance), consider adding SLOG
3. **"Tune for databases"** → Set `recordsize=8K`, enable `lz4` compression

### Detailed Flow for Multi-Device Replication Setup

1. Install Sanoid on all 5 devices + backup server
2. Configure short retention on sources (24 hourly only)
3. Configure pull-based syncoid on backup server:
   - Stagger devices by 15-20 minutes
   - Use `--identifier` flag per device
   - Enable compression with `--compress=zstd-fast`
4. Setup ZFS delegation for non-root operation
5. Add to cron with staggered schedule
6. Test manual run before enabling automation

## References

### scripts/

**`scripts/pool-health.sh`** - Comprehensive pool health checker with JSON output support. Checks state, capacity, scrub status, and generates alerts.

### references/

**`references/command-reference.md`** - Complete ZFS command syntax reference for zpool, zfs, sanoid, and syncoid commands with parameters and examples.

**`references/quick-reference.md`** - Quick command cheatsheet for common ZFS operations.

**`references/troubleshooting.md`** - Comprehensive troubleshooting guide covering:
- Common replication failures (network, space, permissions, conflicts)
- Pool health issues (degraded pools, high capacity, scrub errors)
- Performance problems (slow writes/reads)
- SSH/network issues
- Recovery procedures
- Decision trees for diagnostics

Load this reference when user encounters errors or requests troubleshooting assistance.

### assets/

**`assets/sanoid.conf.template`** - Sanoid configuration template with homelab-optimized retention policies ready to copy to `/etc/sanoid/sanoid.conf`.

## Notes

### 🚨 CRITICAL SAFETY REMINDER

**ALL DESTRUCTIVE COMMANDS REQUIRE:**
1. Explicit user request
2. Exact command shown to user
3. Impact explanation
4. First confirmation
5. Second confirmation
6. Manual execution (commands provided to user, NEVER auto-executed)

**NEVER execute these commands automatically:**
- `zfs destroy` - Permanent data loss
- `zpool destroy` - Catastrophic data loss
- `zfs rollback` - Loses intermediate changes
- `sanoid --prune-snapshots` - Deletes snapshots permanently
- Any command that modifies, removes, or destroys data

See "🚨 DESTRUCTIVE OPERATIONS - CRITICAL SAFETY PROTOCOL" section above for complete details.

### RAIDZ1 Critical Warnings

- **Single parity** - Can tolerate only 1 disk failure
- **Two disk failures = complete data loss**
- Monitor SMART data aggressively
- Monthly scrubs MANDATORY for data integrity
- Consider migrating to RAIDZ2 for critical data

### Pool Capacity Thresholds

- **<70%:** Optimal performance
- **70%:** Warning (performance may degrade)
- **80%:** Critical (fragmentation increases)
- **90%:** Emergency (severe write degradation)
- **>95%:** Risk of pool exhaustion

### Important Concepts

- **Backup does NOT replace scrubbing** - Both are required
- **Set recordsize BEFORE writing data** - Cannot change efficiently after
- **NEVER enable dedup in homelab** - Requires 5GB RAM per TB
- **LZ4 compression is always beneficial** - Minimal overhead, often improves performance

### Security Considerations

For production deployments:
- Use dedicated replication user (not root)
- Implement SSH key restrictions
- Use ZFS delegation for non-root replication
- Firewall rules limiting SSH to backup server IP

## Reference

**Official Documentation:**
- [OpenZFS Documentation](https://openzfs.github.io/openzfs-docs/)
- [Oracle ZFS Administration Guide](https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/manage-zfs/)
- [FreeBSD ZFS Handbook](https://docs.freebsd.org/en/books/handbook/zfs/)

**Automation Tools:**
- [Sanoid/Syncoid GitHub](https://github.com/jimsalterjrs/sanoid)
- [zrepl Documentation](https://zrepl.github.io/)

**Additional Resources:**
- `references/command-reference.md` - Complete ZFS command syntax
- `references/quick-reference.md` - Quick command cheatsheet
- `references/troubleshooting.md` - Detailed troubleshooting guide
