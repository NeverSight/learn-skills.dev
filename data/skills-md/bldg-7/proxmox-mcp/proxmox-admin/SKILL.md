---
name: proxmox-admin
description: Proxmox Virtual Environment operational expertise for AI agents - VM lifecycle, LXC containers, storage management, backup strategies, HA configuration, and troubleshooting
license: MIT
compatibility:
  - claude-code
  - opencode
  - cursor
  - codex
  - gemini-cli
  - vscode
metadata:
  version: 0.6.0
  focus: operations
  generated: 2026-02-08
---

# Proxmox VE Operations Expertise

> **AI Agent Skill**: Operational knowledge for managing Proxmox Virtual Environment infrastructure

## Overview

This skill provides AI agents with operational expertise for Proxmox VE, covering:
- **VM and LXC lifecycle management** - From creation to decommissioning
- **Storage operations** - Configuration, content management, backup strategies
- **High Availability** - HA groups, resource management, failover
- **Cluster operations** - Multi-node management, migration, replication
- **Certificate management** - Installation, renewal, ACME integration
- **ACME configuration** - Provider setup, certificate ordering, automation
- **Notifications** - Target configuration, delivery verification, alerting
- **Troubleshooting** - Common issues, API quirks, resolution patterns
- **Security** - Permission models, API token best practices
- **Performance** - Monitoring, resource optimization

**Target audience**: AI agents performing day-to-day Proxmox operations, infrastructure automation, or incident response.

---

## Architecture Overview

### Proxmox VE Cluster Concepts

**Node**: Physical server running Proxmox VE
- Hosts VMs and LXC containers
- Provides local storage
- Participates in cluster quorum

**Storage**: Shared or local storage backends
- Types: Directory, LVM, ZFS, Ceph, NFS, iSCSI
- Content types: Images, ISOs, backups, templates
- Can be node-local or cluster-shared

**Networking**: Virtual networking infrastructure
- Linux bridges for VM/LXC connectivity
- VLANs for network segmentation
- SDN (Software Defined Networking) for advanced scenarios

**Cluster**: Group of nodes working together
- Shared configuration via pmxcfs
- HA for automatic failover
- Live migration between nodes

---

## Operations Playbook

### 1. VM Lifecycle Management

**Create → Configure → Monitor → Backup → Delete**

#### Creation
```
1. Get next available VMID
2. Create VM with basic config (CPU, memory, OS type)
3. Add disk(s) from storage
4. Configure network interface(s)
5. Set boot order
6. Start VM
```

**Key considerations**:
- Choose appropriate storage for disk (performance vs capacity)
- Use virtio drivers for best performance (requires guest support)
- Configure QEMU guest agent for better management

#### Configuration
```
1. Review current config
2. Resize resources (CPU, memory, disk) as needed
3. Add/remove network interfaces
4. Configure firewall rules
5. Set up snapshots for rollback capability
```

**Best practices**:
- Snapshot before major changes
- Use cloud-init for automated provisioning
- Enable QEMU guest agent for graceful operations

#### Monitoring
```
1. Check VM status (running, stopped, paused)
2. Monitor resource usage (CPU, memory, disk I/O)
3. Review task history for recent operations
4. Check logs for errors or warnings
```

**Metrics to watch**:
- CPU usage and steal time
- Memory pressure and swap usage
- Disk I/O wait times
- Network throughput

#### Backup
```
1. Create snapshot for quick rollback
2. Schedule backup job (vzdump)
3. Verify backup completed successfully
4. Test restore periodically
5. Prune old backups to manage space
```

**Backup strategies**:
- **Snapshot mode**: Fast, requires storage support
- **Suspend mode**: Pauses VM during backup
- **Stop mode**: Stops VM for consistent backup

#### Decommissioning
```
1. Create final backup
2. Stop VM gracefully
3. Remove from HA if configured
4. Delete VM and associated disks
5. Clean up firewall rules
6. Update documentation
```

---

### 2. LXC Container Management

**Containers vs VMs**:
- Lighter weight (shared kernel)
- Faster startup times
- Lower overhead
- Less isolation than VMs

#### Container Operations
```
1. Create from template
2. Configure resources (CPU, memory, swap)
3. Add mount points for storage
4. Configure network
5. Start container
6. Access via console or SSH
```

**Key differences from VMs**:
- Use `mp0`, `mp1` for mount points (not disk0, disk1)
- No BIOS/UEFI configuration
- Direct kernel access (privileged) or restricted (unprivileged)
- Faster snapshot/restore operations

---

### 3. Storage Management

#### Storage Configuration
```
1. List available storage
2. Add new storage backend (NFS, Ceph, etc.)
3. Configure content types (images, backups, ISOs)
4. Set storage as default for specific content
5. Monitor storage usage
```

#### Content Management
```
1. Upload ISOs/templates to storage
2. Download from URL to storage
3. List storage content
4. Delete unused content
5. Restore files from backups
```

#### Backup Management
```
1. Create backup jobs (manual or scheduled)
2. Configure retention policy
3. Prune old backups automatically
4. Restore from backup
5. Verify backup integrity
```

**Backup best practices**:
- Use compression to save space
- Store backups on separate storage
- Test restore procedures regularly
- Document backup schedules
- Monitor backup job success/failure

---

### 4. High Availability (HA)

#### HA Configuration
```
1. Create HA group (define node priorities)
2. Add VM/LXC to HA management
3. Configure HA settings (max relocate, max restart)
4. Monitor HA status
5. Test failover scenarios
```

**HA States**:
- **started**: Resource running on assigned node
- **stopped**: Resource intentionally stopped
- **fence**: Node fenced, resource will be restarted elsewhere
- **error**: HA manager encountered an error

**When to use HA**:
- Critical services requiring high uptime
- Automatic failover needed
- Cluster has 3+ nodes (for quorum)

---

### 5. Migration

#### Live Migration (Online)
```
1. Verify target node has resources
2. Check shared storage access
3. Initiate migration
4. Monitor migration progress
5. Verify VM running on new node
```

**Requirements**:
- Shared storage for VM disks
- Network connectivity between nodes
- Compatible CPU types (or CPU flags masked)

#### Offline Migration
```
1. Stop VM/LXC
2. Migrate to target node
3. Start on new node
```

**Use cases**:
- No shared storage available
- Maintenance on source node
- CPU incompatibility

---

## Troubleshooting Guide

### Common Issues

#### 1. VM Won't Start
**Symptoms**: Start operation fails or VM immediately stops

**Causes**:
- Insufficient resources on node
- Storage unavailable
- Lock file present
- Configuration error

**Resolution**:
```
1. Check node resources (memory, CPU)
2. Verify storage is mounted and accessible
3. Remove lock file if stale
4. Review VM config for errors
5. Check logs: /var/log/pve/tasks/
```

#### 2. Migration Fails
**Symptoms**: Migration operation errors or times out

**Causes**:
- Network connectivity issues
- Storage not shared
- CPU incompatibility
- Insufficient resources on target

**Resolution**:
```
1. Verify network between nodes
2. Check storage is accessible from both nodes
3. Review CPU flags compatibility
4. Ensure target node has capacity
5. Try offline migration if live fails
```

#### 3. Backup Job Fails
**Symptoms**: Backup task shows error status

**Causes**:
- Insufficient storage space
- VM locked by another operation
- Snapshot creation failed
- Network timeout (for remote storage)

**Resolution**:
```
1. Check storage space availability
2. Verify no other operations running on VM
3. Try manual backup to isolate issue
4. Review backup job logs
5. Prune old backups to free space
```

#### 4. HA Failover Not Working
**Symptoms**: VM doesn't restart on another node after failure

**Causes**:
- Cluster quorum lost
- HA service not running
- Fencing not configured
- All nodes in HA group unavailable

**Resolution**:
```
1. Check cluster quorum status
2. Verify HA service running on all nodes
3. Review HA group configuration
4. Check fencing configuration
5. Manually start VM if needed
```

#### 5. Storage Performance Issues
**Symptoms**: Slow VM performance, high I/O wait

**Causes**:
- Storage backend overloaded
- Network bottleneck (for remote storage)
- Disk cache settings suboptimal
- Too many VMs on same storage

**Resolution**:
```
1. Monitor storage backend performance
2. Check network throughput to storage
3. Adjust VM disk cache settings
4. Distribute VMs across multiple storage
5. Consider faster storage tier
```

**More troubleshooting**: See [proxmox-troubleshooting.md](references/proxmox-troubleshooting.md)

---

## Security Best Practices

### API Token Management

**Token creation**:
1. Create dedicated user for automation
2. Assign minimal required permissions
3. Generate API token (not password)
4. Store token securely (environment variables, secrets manager)
5. Rotate tokens periodically

**Permission model**:
- Use roles to group permissions
- Assign roles to users/tokens
- Follow principle of least privilege
- Audit permission usage regularly

### Access Control

**User management**:
- Use realms (PAM, LDAP, AD) for authentication
- Create groups for role-based access
- Assign users to groups
- Review access periodically

**Network security**:
- Restrict API access by IP (firewall rules)
- Use SSL/TLS for API connections
- Enable two-factor authentication for users
- Monitor authentication logs

---

## Performance Optimization

### Resource Allocation

**CPU**:
- Don't overcommit CPU cores excessively
- Use CPU limits for non-critical VMs
- Pin CPUs for latency-sensitive workloads
- Monitor CPU steal time

**Memory**:
- Enable ballooning for dynamic allocation
- Set appropriate memory limits
- Monitor swap usage (should be minimal)
- Use hugepages for large memory VMs

**Disk I/O**:
- Use virtio-scsi for best performance
- Enable discard/TRIM for SSDs
- Configure appropriate I/O scheduler
- Monitor disk latency and throughput

### Monitoring Strategy

**Key metrics**:
- Node CPU, memory, disk usage
- VM resource consumption
- Storage performance (IOPS, latency)
- Network throughput
- Task completion times

**Monitoring tools**:
- Built-in Proxmox metrics (RRD data)
- External monitoring (Prometheus, Grafana)
- Log aggregation (syslog, ELK stack)
- Alerting for critical thresholds

---

## Operational Workflows

For detailed step-by-step workflows, see:
- **[proxmox-workflows.md](references/proxmox-workflows.md)** - Common operational patterns

For troubleshooting details, see:
- **[proxmox-troubleshooting.md](references/proxmox-troubleshooting.md)** - API quirks and solutions

---

## Quick Reference

### VM States
- **running**: VM is powered on
- **stopped**: VM is powered off
- **paused**: VM execution suspended
- **suspended**: VM state saved to disk

### Storage Types
- **dir**: Directory-based storage
- **lvm**: LVM volume groups
- **zfs**: ZFS pools
- **ceph**: Ceph RBD
- **nfs**: NFS shares
- **iscsi**: iSCSI targets

### Backup Modes
- **snapshot**: Fast, requires storage support
- **suspend**: Pauses VM during backup
- **stop**: Stops VM for backup

### HA States
- **started**: Running on assigned node
- **stopped**: Intentionally stopped
- **fence**: Node fenced, restarting elsewhere
- **error**: HA manager error

---

## License

MIT License - Part of @bldg-7/proxmox-mcp package
