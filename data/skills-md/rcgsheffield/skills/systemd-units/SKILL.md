---
name: systemd-units
description: Create and harden systemd service unit files following modern best practices. Use when writing new systemd units for web applications, background workers, or daemons, or when hardening existing services with security sandboxing and isolation features. Covers service types, dependencies, restart policies, security options, and filesystem restrictions.
---

# Systemd Units

## Overview

This skill provides guidance for creating and hardening systemd service unit files following modern Linux service management best practices. It covers proper service type selection, dependency management, security sandboxing, and filesystem isolation to create reliable, secure services.

## When to Use This Skill

Use this skill when:
- Creating new systemd service units for web applications, APIs, background workers, or daemons
- Hardening existing service files with security and sandboxing options
- Converting traditional init scripts or manual process management to systemd
- Troubleshooting service startup, restart, or permission issues
- Implementing proper service dependencies and ordering

## Workflow Decision Tree

```
User request involves systemd service?
│
├─ Creating a new service?
│  │
│  ├─ Web application/API → Use "Creating a New Service" workflow
│  │                        → Start from assets/basic-webapp.service or assets/hardened-webapp.service
│  │
│  ├─ Background worker/daemon → Use "Creating a New Service" workflow
│  │                            → Start from assets/background-worker.service
│  │
│  └─ One-time initialization → Use "Creating a New Service" workflow
│                              → Start from assets/oneshot-init.service
│
└─ Hardening existing service?
   │
   └─ Use "Hardening an Existing Service" workflow
      → Reference references/systemd_options.md for security options
      → Compare against assets/hardened-webapp.service for patterns
```

## Creating a New Service

When creating a new systemd service, follow these steps:

### 1. Select the Appropriate Template

Start with the most relevant template from `assets/`:

- **`basic-webapp.service`**: Simple web application without heavy sandboxing (development/internal use)
- **`hardened-webapp.service`**: Production web application with full security hardening
- **`background-worker.service`**: Queue processor, scheduled task, or background daemon
- **`oneshot-init.service`**: One-time initialization script or setup task

Copy the template and customize the following sections in order:

### 2. Configure [Unit] Section

Update the service metadata and dependencies:

```ini
[Unit]
Description=Clear description of what this service does
Documentation=https://example.com/docs or man:program(8)
After=network-online.target database.service
Wants=network-online.target
Requires=database.service
```

**Key decisions:**
- **After=**: List services this must start after (ordering dependency)
- **Wants=**: Soft dependencies (service will start even if these fail)
- **Requires=**: Hard dependencies (service fails if these fail)
- For web services, always include `After=network-online.target` and `Wants=network-online.target`

### 3. Configure Service Type and Execution

Select the appropriate service type based on the application's capabilities:

**Recommended service types** (in order of preference):
1. **`Type=notify`**: Application supports sd_notify protocol (best option for reliability)
2. **`Type=exec`**: Standard long-running process (good default)
3. **`Type=oneshot`**: One-time execution that exits (initialization scripts)

**Avoid `Type=simple`** (poor error detection) and **avoid `Type=forking`** (deprecated pattern).

```ini
[Service]
Type=exec
ExecStart=/usr/bin/node /opt/webapp/server.js
WorkingDirectory=/opt/webapp
```

**Always use absolute paths** for `ExecStart=` and related commands.

### 4. Configure User and Environment

Set the execution user and environment variables:

```ini
# Option 1: Dynamic user (recommended for security)
DynamicUser=yes

# Option 2: Specific user/group
User=webapp
Group=webapp

# Environment configuration
Environment="NODE_ENV=production"
EnvironmentFile=-/etc/webapp/webapp.env
```

**Best practice**: Use `DynamicUser=yes` for services that don't need a specific user. For secrets, use `EnvironmentFile=` with restricted permissions instead of embedding credentials in the service file.

### 5. Configure Restart Policy

Set appropriate restart behavior:

```ini
Restart=on-failure    # For web apps (restart on crashes)
RestartSec=10        # Wait 10 seconds before restart
TimeoutStartSec=30   # Fail if startup takes >30 seconds
TimeoutStopSec=30    # Force kill if graceful stop takes >30 seconds
```

**Common patterns:**
- Web applications: `Restart=on-failure` with `RestartSec=10`
- Critical workers: `Restart=always` with `RestartSec=5`
- Oneshot tasks: Omit `Restart=` (default is no restart)

### 6. Apply Security Hardening

For production services, apply progressive security hardening:

**Start with these baseline options:**
```ini
# Filesystem protection
ProtectSystem=strict          # Entire filesystem read-only except specified paths
ProtectHome=yes              # Hide /home directories
PrivateTmp=yes               # Private /tmp namespace
ReadWritePaths=/var/lib/myapp /var/log/myapp  # Writable paths whitelist
NoNewPrivileges=yes          # Prevent privilege escalation

# Device and kernel protection
PrivateDevices=yes           # Restrict device access
ProtectKernelTunables=yes    # Prevent /proc/sys, /sys writes
ProtectKernelModules=yes     # Prevent kernel module loading
ProtectControlGroups=yes     # Protect cgroup filesystem
```

**For internet-facing services, add:**
```ini
# Network restrictions
RestrictAddressFamilies=AF_INET AF_INET6  # Only IPv4/IPv6

# Capability restrictions
CapabilityBoundingSet=       # Remove all capabilities

# System call filtering
SystemCallFilter=@system-service
SystemCallArchitectures=native

# Memory protection
MemoryDenyWriteExecute=yes   # W^X protection
LockPersonality=yes
```

**Testing strategy**: Start with maximum restrictions. If the service fails, use `journalctl -xeu <service>` to identify which restriction caused the failure, then selectively relax only that restriction.

Use `systemd-analyze security <service>` to verify the security posture after configuration.

### 7. Configure [Install] Section

Set the target for service enablement:

```ini
[Install]
WantedBy=multi-user.target   # Most common target (non-graphical multi-user system)
```

**Common targets:**
- `multi-user.target`: Standard for most services
- `graphical.target`: Services requiring graphical environment
- `default.target`: Alias for the default system target

### 8. Install and Test the Service

Place the service file and test:

```bash
# Copy to system directory
sudo cp myapp.service /etc/systemd/system/

# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Start and check status
sudo systemctl start myapp
sudo systemctl status myapp

# View logs
journalctl -xeu myapp

# Enable to start on boot
sudo systemctl enable myapp
```

## Hardening an Existing Service

When hardening an existing service file, follow these steps:

### 1. Analyze Current Configuration

Read the existing service file and identify security gaps:

```bash
# Check current security exposure
systemd-analyze security <service-name>

# Review current configuration
systemctl cat <service-name>
```

Look for:
- Missing sandboxing options (ProtectSystem, PrivateDevices, etc.)
- Overly permissive user (running as root unnecessarily)
- Missing filesystem restrictions
- No capability boundaries

### 2. Create Drop-in Override

Rather than modifying the vendor-supplied service file directly, create a drop-in override:

```bash
sudo systemctl edit <service-name>
```

This creates `/etc/systemd/system/<service-name>.service.d/override.conf` and preserves vendor updates.

### 3. Apply Security Options Progressively

Add security options in stages, testing after each stage:

**Stage 1: Basic isolation**
```ini
[Service]
# Filesystem protection
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/lib/myapp  # Add paths service needs to write

# Basic device protection
PrivateDevices=yes
```

Test: `sudo systemctl restart <service>` and check `journalctl -xeu <service>`

**Stage 2: Kernel and capability restrictions**
```ini
[Service]
# Kernel protection
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes

# Remove capabilities
NoNewPrivileges=yes
CapabilityBoundingSet=
```

Test again.

**Stage 3: Network and system call filtering**
```ini
[Service]
# Network restrictions (adjust for service needs)
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX

# System call filtering
SystemCallFilter=@system-service
SystemCallArchitectures=native

# Memory protection
MemoryDenyWriteExecute=yes
LockPersonality=yes
```

Test and verify functionality.

### 4. Handle Common Restriction Failures

If the service fails after adding restrictions:

**Error: "Permission denied" accessing filesystem**
- Add the path to `ReadWritePaths=` or relax `ProtectSystem=` to `full` instead of `strict`

**Error: "Operation not permitted" for network operations**
- Check `RestrictAddressFamilies=` includes needed protocols
- For Unix domain sockets, add `AF_UNIX`

**Error: System call blocked**
- Review `journalctl` for blocked syscall name
- Add exception: `SystemCallFilter=@system-service <syscall-name>`

**Error: Cannot access devices**
- Add specific device to `DeviceAllow=` instead of removing `PrivateDevices=`

### 5. Verify Hardening

After applying all restrictions:

```bash
# Check security score (lower is better)
systemd-analyze security <service-name>

# Verify service functionality
sudo systemctl restart <service-name>
sudo systemctl status <service-name>

# Test application-level functionality
# (Make requests, check logs, verify operations)
```

## Best Practices

### Service Type Selection

1. **Prefer `Type=notify`** for services that can implement sd_notify protocol - provides reliable startup verification
2. **Use `Type=exec`** for standard long-running processes - good error detection
3. **Avoid `Type=simple`** - provides no startup verification and poor error handling
4. **Avoid `Type=forking`** - deprecated pattern, use `Type=notify` or `Type=exec` instead

### Dependency Management

1. **Separate ordering from requirements**: Use both `After=` and `Requires=`/`Wants=`
   - `After=` controls startup sequence
   - `Requires=`/`Wants=` controls dependency relationships
2. **Use `Wants=` for soft dependencies** (tolerate failures)
3. **Use `Requires=` for hard dependencies** (fail if dependency fails)
4. **For network services**: Always include `After=network-online.target` and `Wants=network-online.target`

### Security Hardening

1. **Use `DynamicUser=yes`** unless the service needs a specific user
2. **Start with maximum restrictions and relax selectively** - more effective than progressive hardening
3. **Separate secrets from configuration** - use `EnvironmentFile=` for sensitive values
4. **Always set `NoNewPrivileges=yes`** to prevent privilege escalation
5. **Remove all capabilities by default** with `CapabilityBoundingSet=`, add back only what's needed
6. **Use `systemd-analyze security`** to verify hardening effectiveness

### Filesystem Access

1. **Prefer `ProtectSystem=strict`** with explicit `ReadWritePaths=` whitelist
2. **Always enable `PrivateTmp=yes`** unless sharing /tmp is explicitly required
3. **Enable `ProtectHome=yes`** unless home directory access is needed
4. **Create dedicated directories** under `/var/lib/` for application data

### Restart and Recovery

1. **Web applications**: `Restart=on-failure` with `RestartSec=10`
2. **Critical workers**: `Restart=always` with `RestartSec=5`
3. **Set reasonable timeouts**: `TimeoutStartSec=30` and `TimeoutStopSec=30` (adjust based on application)
4. **Define custom success codes** with `SuccessExitStatus=` if application uses non-zero exits for success

### Logging and Debugging

1. **Use structured logging**: `StandardOutput=journal` and `StandardError=journal`
2. **Set `SyslogIdentifier=`** for easier log filtering
3. **Debug with**: `journalctl -xeu <service>` (shows extended info and follows)
4. **Check dependencies**: `systemctl list-dependencies <service>`

## Resources

### references/systemd_options.md

Comprehensive reference documentation for all systemd unit and service options. Read this file when:
- Looking up specific option syntax or behavior
- Understanding security/sandboxing options in detail
- Reviewing all available service types and their tradeoffs
- Finding additional hardening options beyond the templates

Use grep to search for specific options:
```bash
grep -i "ProtectSystem" references/systemd_options.md
```

### assets/ Templates

Production-ready service file templates:

- **`basic-webapp.service`**: Starting point for web applications without heavy sandboxing
- **`hardened-webapp.service`**: Fully hardened web application with maximum security
- **`background-worker.service`**: Queue processor or background daemon with security hardening
- **`oneshot-init.service`**: One-time initialization script pattern

Use these as starting points and customize for specific application needs.

## Common Troubleshooting

**Service fails to start after hardening:**
1. Check logs: `journalctl -xeu <service>`
2. Look for "Permission denied" or "Operation not permitted" errors
3. Identify the blocked operation (filesystem, syscall, network)
4. Selectively relax the relevant restriction
5. Retest and verify

**Service starts but behaves incorrectly:**
1. Verify `WorkingDirectory=` is correct
2. Check environment variables are loaded (`EnvironmentFile=`)
3. Verify filesystem paths are accessible (`ReadWritePaths=`)
4. Check user/group has appropriate permissions on files

**Service restarts repeatedly:**
1. Check logs for crash reason: `journalctl -xeu <service>`
2. Verify `ExecStart=` path is correct and executable
3. Check if application crashes due to missing dependencies
4. Consider increasing `RestartSec=` to prevent rapid restart loops
5. Check if `Type=` matches application behavior

**Cannot access network after hardening:**
1. Verify `RestrictAddressFamilies=` includes required protocols (IPv4: `AF_INET`, IPv6: `AF_INET6`, Unix sockets: `AF_UNIX`)
2. Check if firewall or network namespace is blocking access
3. For localhost-only services, ensure `AF_INET` is included
