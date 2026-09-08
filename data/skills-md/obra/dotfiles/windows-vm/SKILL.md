---
name: windows-vm
description: Create, manage, or connect to a headless Windows 11 VM running in Docker with SSH access. Use when the user wants to spin up, stop, restart, or SSH into a Windows VM.
argument-hint: "[create|start|stop|restart|ssh|status]"
allowed-tools: Bash, Read, Write
---

# Headless Windows 11 VM

Manage a headless Windows 11 VM running via [dockur/windows](https://github.com/dockur/windows) in Docker with KVM acceleration. The VM is accessible via SSH only — no RDP or GUI required.

## Host prerequisites

- Docker
- KVM support (`/dev/kvm` must exist — check with `ls /dev/kvm`)
- `sshpass` (`sudo apt install sshpass`)
- `imagemagick` (optional, for screenshot debugging: `sudo apt install imagemagick`)

## Configuration

- **Container name**: `windows11`
- **VM directory**: `/home/jesse/windows-vm/`
  - `storage/` — VM disk image (managed by dockur, wiped on recreate)
  - `iso/win11x64.iso` — cached Windows ISO (7.3GB, persists across recreates)
  - `oem/install.bat` — post-install script (installs OpenSSH Server)
- **Credentials**: user / password
- **SSH**: `localhost:2222` (bound to 127.0.0.1 only)
- **RDP**: `localhost:3389` (bound to 127.0.0.1 only, fallback)
- **Web console**: `localhost:8006` (VNC in browser, for debugging)
- **Resources**: 8GB RAM, 4 CPU cores, 64GB disk

## Actions

### create — First-time setup or full recreate

1. Ensure directories exist:
   ```bash
   mkdir -p /home/jesse/windows-vm/oem /home/jesse/windows-vm/storage /home/jesse/windows-vm/iso
   ```

2. Ensure `/home/jesse/windows-vm/oem/install.bat` exists with OpenSSH setup:
   ```bat
   @echo off
   echo Installing OpenSSH Server...
   powershell -Command "Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0" 2>nul
   powershell -Command "Get-WindowsCapability -Online -Name OpenSSH.Server* | Add-WindowsCapability -Online" 2>nul
   dism /Online /Add-Capability /CapabilityName:OpenSSH.Server~~~~0.0.1.0 2>nul
   powershell -Command "Start-Service sshd" 2>nul
   powershell -Command "Set-Service -Name sshd -StartupType Automatic"
   powershell -Command "New-ItemProperty -Path 'HKLM:\SOFTWARE\OpenSSH' -Name DefaultShell -Value 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -PropertyType String -Force"
   powershell -Command "New-NetFirewallRule -Name 'OpenSSH-Server' -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22"
   powershell -Command "Get-Service sshd" 2>nul
   echo Done.
   ```

3. If recreating, remove the old container and disk:
   ```bash
   docker stop windows11 && docker rm windows11
   rm -f /home/jesse/windows-vm/storage/data.img
   ```

4. Launch the container. There are two cases:

   **If cached ISO exists** (`/home/jesse/windows-vm/iso/win11x64.iso`):
   ```bash
   docker run -d \
     --name windows11 \
     -p 127.0.0.1:3389:3389 \
     -p 127.0.0.1:2222:22 \
     -p 127.0.0.1:8006:8006 \
     -e RAM_SIZE="8G" \
     -e CPU_CORES="4" \
     -e DISK_SIZE="64G" \
     -e USERNAME="user" \
     -e PASSWORD="password" \
     --cap-add NET_ADMIN \
     --device /dev/kvm \
     -v /home/jesse/windows-vm/storage:/storage \
     -v /home/jesse/windows-vm/oem:/oem \
     -v /home/jesse/windows-vm/iso/win11x64.iso:/boot.iso \
     dockurr/windows
   ```

   **First time (no cached ISO)** — omit the `/boot.iso` mount and add `VERSION`:
   ```bash
   docker run -d \
     --name windows11 \
     -p 127.0.0.1:3389:3389 \
     -p 127.0.0.1:2222:22 \
     -p 127.0.0.1:8006:8006 \
     -e RAM_SIZE="8G" \
     -e CPU_CORES="4" \
     -e DISK_SIZE="64G" \
     -e VERSION="win11" \
     -e USERNAME="user" \
     -e PASSWORD="password" \
     --cap-add NET_ADMIN \
     --device /dev/kvm \
     -v /home/jesse/windows-vm/storage:/storage \
     -v /home/jesse/windows-vm/oem:/oem \
     dockurr/windows
   ```
   After the ISO downloads and Windows boots, **immediately** copy the ISO out before
   the container is ever stopped (dockur wipes `/storage` on recreate):
   ```bash
   cp /home/jesse/windows-vm/storage/win11x64.iso /home/jesse/windows-vm/iso/win11x64.iso
   ```

5. Wait for Windows install + OpenSSH setup to complete. This takes **20-30 minutes** for a
   fresh install (the OEM install.bat runs at the end of Windows OOBE and downloads OpenSSH
   from Microsoft, which is slow). Monitor with:
   ```bash
   docker logs -f windows11
   ```
   You can also watch the VM screen via the web console at `http://localhost:8006`
   (tunnel with `ssh -L 8006:localhost:8006 jesse@magic-kingdom` from another machine).

   To check if SSH is up:
   ```bash
   sshpass -p 'password' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p 2222 user@localhost "whoami"
   ```

6. Once SSH is responding, install Node.js and Claude Code by piping a setup script via stdin
   (avoids PowerShell escaping hell over SSH):
   ```bash
   cat << 'PS' | sshpass -p 'password' ssh -o StrictHostKeyChecking=no -p 2222 user@localhost "powershell -ExecutionPolicy Bypass -Command -"
   # Download and install Node.js silently
   Invoke-WebRequest -Uri 'https://nodejs.org/dist/v22.14.0/node-v22.14.0-x64.msi' -OutFile 'C:\Users\user\node-install.msi'
   Start-Process msiexec.exe -ArgumentList '/i C:\Users\user\node-install.msi /qn /norestart' -Wait -Verb RunAs
   Write-Host "Node.js installed"

   # Install Claude Code globally
   & 'C:\Program Files\nodejs\npm.cmd' install -g @anthropic-ai/claude-code
   Write-Host "Claude Code installed"

   # Add npm global bin and Git to SYSTEM PATH (user PATH is not read by sshd)
   $systemPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
   $additions = @()
   if ($systemPath -notlike '*AppData*npm*') { $additions += 'C:\Users\user\AppData\Roaming\npm' }
   if ($systemPath -notlike '*Git\cmd*') { $additions += 'C:\Program Files\Git\cmd' }
   if ($additions.Count -gt 0) {
       [Environment]::SetEnvironmentVariable('Path', $systemPath + ';' + ($additions -join ';'), 'Machine')
       Write-Host "Added to system PATH: $($additions -join ', ')"
   }

   # Set git config
   git config --global user.name "Jesse Vincent"
   git config --global user.email "jesse@fsck.com"
   Write-Host "Git configured"

   # Set execution policy machine-wide (required for claude.ps1)
   Set-ExecutionPolicy RemoteSigned -Scope LocalMachine -Force -ErrorAction SilentlyContinue

   # Create system-wide PowerShell profile that rebuilds PATH from registry on login.
   # Without this, interactive SSH sessions don't pick up the full system PATH.
   $profileDir = Split-Path $PROFILE.AllUsersAllHosts
   if (-not (Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir -Force }
   @'
   $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
   $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
   $env:Path = "$machinePath;$userPath"
   '@ | Set-Content -Path $PROFILE.AllUsersAllHosts -Force
   Write-Host "PowerShell profile created"

   # Restart sshd so it picks up the new PATH
   Restart-Service sshd -Force
   PS
   ```
   Note: the connection will drop when sshd restarts — that's expected.

7. Clear the stale host key (new VM = new host key) and verify:
   ```bash
   ssh-keygen -f ~/.ssh/known_hosts -R '[localhost]:2222'
   sshpass -p 'password' ssh -o StrictHostKeyChecking=no -p 2222 user@localhost "claude --version"
   ```

### start — Start a stopped VM
```bash
docker start windows11
```

### stop — Stop the VM
```bash
docker stop windows11
```

### restart — Restart the VM
```bash
docker restart windows11
```

### status — Check VM status
```bash
docker ps -f name=windows11 --format "table {{.Status}}\t{{.Ports}}"
docker logs windows11 2>&1 | tail -5
```

### ssh — Connect to the VM
```bash
ssh -p 2222 user@localhost
```
From another tailnet machine via magic-kingdom:
```bash
ssh -J jesse@magic-kingdom -p 2222 user@localhost
```

### screenshot — See what's on the VM screen (for debugging)
```bash
docker exec windows11 bash -c "echo 'screendump /tmp/screen.ppm' | nc -w 2 localhost 7100" > /dev/null 2>&1
sleep 1
docker cp windows11:/tmp/screen.ppm /tmp/screen.ppm
convert /tmp/screen.ppm /tmp/screen.png
```

## Important Notes

- **ISO caching**: The `/storage` volume is managed by dockur and gets wiped on recreate. Store the ISO separately in `/home/jesse/windows-vm/iso/` and mount it as `/boot.iso` to skip the 7.3GB download.
- **`--cap-add NET_ADMIN`** is required for port forwarding to work. Without it, QEMU falls back to user-mode networking and port forwarding silently fails.
- **`--device /dev/kvm`** is required for hardware acceleration.
- **Boot time**: Fresh install takes 20-30 min (Windows install + OpenSSH download from Microsoft). Subsequent boots from existing `data.img` are fast (~2 min).
- Ports are bound to `127.0.0.1` only — not exposed to the network. Access from other machines via Tailscale SSH tunneling.
- Do NOT use `-e VERSION="win11"` when mounting `/boot.iso` — the version is auto-detected from the ISO.

## Post-install gotchas

- **Node.js is not pre-installed** — the Claude Code install script (`irm https://claude.ai/install.ps1 | iex`) will report success but `claude` won't work without Node. Install Node.js via MSI first.
- **npm global bin not in PATH** — Node's MSI adds `C:\Program Files\nodejs` to PATH but not `C:\Users\user\AppData\Roaming\npm` (where `npm install -g` puts binaries). Must add it to the **system** PATH (not user PATH) because OpenSSH's sshd only reads system PATH. After changing system PATH, restart sshd.
- **PowerShell execution policy** — Default policy is `Restricted`, which blocks `claude.ps1`. Must set to `RemoteSigned` at **LocalMachine** scope (not CurrentUser) for it to take effect in SSH sessions.
- **Escaping hell** — Running PowerShell commands over SSH with nested quotes is unreliable. Pipe scripts via stdin using `powershell -ExecutionPolicy Bypass -Command -` instead.
- **Interactive SSH sessions don't get full PATH** — Windows OpenSSH sshd doesn't properly propagate the system PATH to interactive PowerShell sessions. Fix: create a system-wide PowerShell profile (`$PROFILE.AllUsersAllHosts`) that rebuilds `$env:Path` from the registry on every login.
- **winget may not work** — The Microsoft Store certificate can fail in a VM. Use direct MSI/installer downloads instead.
- **Host key changes** — Each recreated VM gets new SSH host keys. Run `ssh-keygen -R '[localhost]:2222'` to clear the old one.
