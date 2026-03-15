---
name: ssh-tunnel-debug
description: >
  Diagnose and fix SSH tunnel issues. Use when a tunnel is not connecting,
  a port is not responding, an SSH tunnel shows as stopped, the user reports
  "Permission denied", "Connection refused", or any SSH tunnel-related error.
---

# SSH Tunnel Debugger

You are diagnosing issues with SSH tunnels managed by the `ssh-tunnels` CLI.
Follow this systematic approach to identify and fix the problem.

## Step 1: Get the current state

```bash
ssh-tunnels status --json
```

Look for tunnels where `enabled: true` but `alive: false` or `portOpen: false`.
These are the broken ones.

## Step 2: Check the logs

For each broken tunnel:

```bash
ssh-tunnels logs <tunnel-id>
```

## Step 3: Diagnose by error message

### "Permission denied (publickey)"
**Cause**: Wrong SSH username or SSH key not authorized on the remote host.
**Fix**:
```bash
ssh-tunnels remove <id>
ssh-tunnels add --name "Same Name" --host <host> --user root --localPort <port> --remoteHost <rhost> --remotePort <rport> --enabled
```
Try `root` first. If that doesn't work, ask the user what username they use
to SSH into that server manually (`ssh <user>@<host>`).

### "Connection refused"
**Cause**: SSH server is not running on the target host, or it's on a non-standard port.
**Checks**:
```bash
# Test SSH connectivity directly
ssh -o ConnectTimeout=5 -o BatchMode=yes <user>@<host> echo "OK" 2>&1
```
If the SSH server is on a non-standard port, recreate the tunnel with `--sshPort`.

### "Connection timed out" or "No route to host"
**Cause**: Host is unreachable — wrong hostname, firewall, or network issue.
**Checks**:
```bash
# Test basic connectivity
ping -c 3 -W 5 <host> 2>&1
# Test SSH port specifically
nc -z -w 5 <host> <ssh-port> 2>&1 && echo "Port open" || echo "Port closed/filtered"
```

### "Host key verification failed"
**Cause**: The server's host key changed or this is the first connection.
**Fix**:
```bash
# Remove the old host key
ssh-keygen -R <host>
# The tunnel manager uses StrictHostKeyChecking=accept-new, so re-enabling should work
ssh-tunnels disable <id> && ssh-tunnels enable <id>
```

### "bind: Address already in use"
**Cause**: Another process is already using the local port.
**Fix**:
```bash
# Find what's using the port
lsof -i :<local-port> -P -n
# Either stop that process or change the tunnel's local port
```
To change the local port, remove and re-add the tunnel with a different `--localPort`.

### "channel 0: open failed: connect failed: Connection refused"
**Cause**: The SSH tunnel is connected, but the remote service is not listening
on the specified remoteHost:remotePort.
**Checks**:
```bash
# SSH in and check if the service is running
ssh <user>@<host> "netstat -tlnp 2>/dev/null | grep <remote-port> || ss -tlnp | grep <remote-port>"
```
The remote service may be down, or `--remoteHost` / `--remotePort` may be wrong.

### Empty log file or no log file
**Cause**: The SSH process crashed immediately or was never spawned.
**Checks**:
```bash
# Check the PID file
cat ~/.ssh-tunnels/pids/<id>.pid 2>/dev/null
# Try a manual SSH connection to see what happens
ssh -v -N -L <localPort>:<remoteHost>:<remotePort> <user>@<host>
```

## Step 4: Verify the fix

After making changes:

```bash
ssh-tunnels status --json
```

Confirm that `alive: true` and `portOpen: true` for the fixed tunnel.

Then test the actual connection through the tunnel:

```bash
# For PostgreSQL (port 5432)
pg_isready -h 127.0.0.1 -p <local-port> 2>&1 || echo "Not ready"

# For HTTP services
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<local-port>/ 2>&1

# For any TCP service (generic check)
nc -z -w 3 127.0.0.1 <local-port> && echo "Port responding" || echo "Port not responding"
```

## Step 5: Check for systemic issues

If multiple tunnels are failing:

```bash
# Check if SSH agent is running and has keys loaded
ssh-add -l 2>&1

# Check if there's a network-level issue
# (all tunnels to the same host failing = host or network problem)
ssh-tunnels status --json | grep -E '"host"|"alive"'

# Force a full re-sync
ssh-tunnels sync
```

## Step 6: Nuclear option — full reset

If nothing else works, reset a specific tunnel:

```bash
ssh-tunnels disable <id>
# Clean up any stale state
rm -f ~/.ssh-tunnels/pids/<id>.pid
ssh-tunnels enable <id>
ssh-tunnels logs <id>
```

## Menu bar app issues

If the menu bar app is not showing or not updating:

```bash
# Check if it's running
pgrep -f "electron.*app.mjs" && echo "Running" || echo "Not running"

# Restart it
pkill -f "electron.*app.mjs"
# The LaunchAgent should restart it automatically, or:
launchctl unload ~/Library/LaunchAgents/com.statechange.ssh-tunnel-manager.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.statechange.ssh-tunnel-manager.plist

# Check launch agent status
launchctl list | grep statechange
```

## Quick reference

| Symptom | Most likely cause | First thing to try |
|---------|-------------------|--------------------|
| "Permission denied" | Wrong SSH user | Recreate with `--user root` |
| Tunnel stops immediately | Auth failure or port conflict | `ssh-tunnels logs <id>` |
| Tunnel starts but port not open | Remote service down | SSH in and check the service |
| All tunnels failing | Network issue or SSH agent | `ssh-add -l`, check connectivity |
| Tunnel works then dies | Server-side timeout | Check ServerAliveInterval |
| "Address already in use" | Port conflict | `lsof -i :<port>` |
