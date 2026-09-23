---
name: ubuntu-vm
description: Use when creating an Ubuntu Desktop VM on Steam Deck (SteamOS) with KVM/Virt-Manager for AI Agent automation, software testing, or development environments requiring a separate Linux system.
---

# Ubuntu VM on Steam Deck

Create an Ubuntu Desktop VM via KVM with SSH access, so AI Agents (Claude Code, Codex, Gemini…) can directly operate the VM via `ssh user@ip`.

## Parameters

When the user invokes this skill, determine these values from context or ask:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `VM_NAME` | (required) | VM name, e.g. `ubuntu-array30-install` |
| `VM_USER` | `array30` | Username inside the VM |
| `VM_RAM` | `4096` | RAM in MB |
| `VM_CPUS` | `2` | Number of vCPUs |
| `VM_DISK` | `25` | Disk size in GB |
| `VM_LANG` | (ask user) | Install language: `en` or `zh_TW` |

Disk path is always `/home/deck/VMs/${VM_NAME}.qcow2`.

## Critical: Long Commands MUST Be Written to .sh Files

**Never paste multi-word commands directly into terminal.** SteamOS terminal auto-wraps long lines and breaks them mid-argument. Always write commands to `/tmp/*.sh`, then prompt the user to run `sudo bash /tmp/filename.sh`.

## Critical: Always Use system Connection

All `virsh` and `virt-install` commands MUST use `sudo` to operate in the `qemu:///system` session. The `default` network only exists in the system session. Without `sudo`, virt-install runs in `qemu:///session` and cannot find the network.

## Critical: Use BIOS Boot, NOT UEFI

**Always use `--boot cdrom,hd` (BIOS/Legacy mode).** Do NOT use `--boot uefi`.

UEFI on SteamOS KVM has multiple confirmed issues:
1. `--boot uefi` auto-selects `OVMF_CODE.secboot.4m.fd` (Secure Boot), which may block ISO boot
2. Disabling Secure Boot post-creation (`virsh edit` XML) causes firmware mismatch: `Unable to find 'efi' firmware that is compatible with the current configuration`
3. Manually specifying `OVMF_CODE.4m.fd` (non-secboot) results in UEFI Shell with CDROM not in boot device list
4. Ubuntu 24.04 desktop ISO supports BIOS boot — no reason to use UEFI for test VMs

## Phase 1: Infrastructure (First-Time Only)

Skip if `sudo virsh net-info default` succeeds AND Virt-Manager is installed — infrastructure is already set up.

### 1a. KVM + libvirt

Write `/tmp/vm-setup-phase1.sh` (use Write tool):
```bash
#!/bin/bash
set -e
steamos-readonly disable
pacman -S --noconfirm --needed qemu-desktop libvirt dnsmasq virt-install edk2-ovmf
systemctl start libvirtd && systemctl enable libvirtd
usermod -aG libvirt deck
```
Prompt: `sudo bash /tmp/vm-setup-phase1.sh`

### 1b. Virtual Machine Manager (Virt-Manager)

Check if installed:
```bash
flatpak list | grep -i virt
```

If not found, install via Flatpak (no sudo needed, persists across SteamOS updates):
```bash
flatpak install -y flathub org.virt_manager.virt-manager
```

Unlike pacman packages, Flatpak apps survive SteamOS system updates — no need to reinstall.

Write `/tmp/vm-setup-network.sh`:
```bash
#!/bin/bash
set -e
cat > /etc/firewalld/zones/libvirt.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<zone target="ACCEPT">
  <short>libvirt</short>
  <description>The libvirt zone for virtual network interfaces.</description>
  <interface name="virbr0"/>
  <protocol value="icmp"/>
  <protocol value="ipv6-icmp"/>
  <service name="dhcp"/>
  <service name="dhcpv6"/>
  <service name="dns"/>
  <service name="ssh"/>
  <service name="tftp"/>
</zone>
EOF
firewall-cmd --reload
virsh net-start default 2>/dev/null || true
virsh net-autostart default
```
Prompt: `sudo bash /tmp/vm-setup-network.sh`

## Phase 2: Download ISO (If Needed)

Check if ISO already exists in `~/Downloads/`:
```bash
ls ~/Downloads/ubuntu-*-desktop-amd64.iso 2>/dev/null
```

If not found, use WebFetch to load `https://releases.ubuntu.com/24.04/`, find the current `ubuntu-*-desktop-amd64.iso` filename. Then prompt:
```bash
wget -c -P ~/Downloads https://releases.ubuntu.com/24.04/<FILENAME>
```

## Phase 3: Ensure Services Running

After SteamOS reboot, libvirtd and default network may be stopped. Always check:

```bash
sudo systemctl start libvirtd
sudo virsh net-start default 2>/dev/null || true
```

## Phase 4: Create VM

**Full cleanup before creation** — always clean both sessions and delete old disk/NVRAM to avoid ghost definitions from failed attempts:

Write `/tmp/vm-create.sh` with all parameters substituted:
```bash
#!/bin/bash
set -euo pipefail

VM_NAME="${VM_NAME}"
DISK_PATH="/home/deck/VMs/${VM_NAME}.qcow2"
ISO_PATH="/home/deck/Downloads/${ISO_FILENAME}"

# Clean up BOTH sessions (user + system) and old artifacts
virsh --connect qemu:///session destroy "$VM_NAME" 2>/dev/null || true
virsh --connect qemu:///session undefine "$VM_NAME" --nvram 2>/dev/null || true
sudo virsh destroy "$VM_NAME" 2>/dev/null || true
sudo virsh undefine "$VM_NAME" --nvram 2>/dev/null || true
rm -f "$DISK_PATH"
sudo rm -f "/var/lib/libvirt/qemu/nvram/${VM_NAME}_VARS.fd"

# Ensure services
sudo systemctl start libvirtd
sudo virsh net-start default 2>/dev/null || true

mkdir -p /home/deck/VMs

sudo virt-install \
    --connect qemu:///system \
    --name "$VM_NAME" \
    --ram ${VM_RAM} --vcpus ${VM_CPUS} \
    --disk "path=$DISK_PATH,size=${VM_DISK},format=qcow2" \
    --cdrom "$ISO_PATH" \
    --os-variant ubuntu24.04 \
    --network network=default \
    --graphics spice \
    --video qxl \
    --boot cdrom,hd \
    --noautoconsole
```
Prompt: `bash /tmp/vm-create.sh`

## Phase 5: Ubuntu Installation (User-Interactive)

Auto-launch Virt-Manager:
```bash
flatpak run org.virt_manager.virt-manager &>/dev/null &
```

If auto-launch fails, tell user: **點左下角啟動器 → 搜尋「虛擬系統管理器」開啟（英文名 Virtual Machine Manager）。**

1. In Virt-Manager, double-click `${VM_NAME}` to open the console
2. **Important:** Click **"Install Ubuntu"** — not just use the Live session
3. Installation language: remind user based on `VM_LANG` parameter
4. After install, ask user for the username and password they chose
5. Ask user to run inside VM terminal:
   ```bash
   sudo apt install -y openssh-server ssh-askpass-gnome
   ```

## Phase 6: SSH Setup

**Get VM IP** (no guest agent needed):

Write `/tmp/vm-get-ip.sh`:
```bash
#!/bin/bash
sudo virsh net-dhcp-leases default
```
Prompt: `bash /tmp/vm-get-ip.sh`

Parse the IP (e.g. `192.168.122.x`) — match by VM's MAC address or hostname.

**Setup key auth** (run on host):
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" 2>/dev/null || true
ssh-copy-id ${VM_USER}@<ip>
```
User enters VM password when prompted.

**Verify:**
```bash
ssh ${VM_USER}@<ip> echo "VM ready"
```

**Eject ISO** after SSH is verified (not before — reboot could change IP):

Write `/tmp/vm-eject.sh`:
```bash
#!/bin/bash
CDROM=$(sudo virsh domblklist ${VM_NAME} | awk '/iso/{print $1}')
[ -n "$CDROM" ] && sudo virsh change-media ${VM_NAME} "$CDROM" --eject || true
```
Prompt: `bash /tmp/vm-eject.sh`

## Phase 7: Post-Setup Summary

After SSH is verified, output a summary block for the user:

```
VM ready:
  Name:  ${VM_NAME}
  IP:    ${VM_IP}
  SSH:   ssh ${VM_USER}@${VM_IP}
  Disk:  /home/deck/VMs/${VM_NAME}.qcow2
```

## Managing Existing VMs

**Start a stopped VM:**
```bash
sudo virsh start ${VM_NAME}
```

**Shut down a VM:**
```bash
sudo virsh shutdown ${VM_NAME}
```

**Delete a VM completely:**
```bash
sudo virsh destroy ${VM_NAME} 2>/dev/null || true
sudo virsh undefine ${VM_NAME} --nvram 2>/dev/null || true
rm -f /home/deck/VMs/${VM_NAME}.qcow2
sudo rm -f /var/lib/libvirt/qemu/nvram/${VM_NAME}_VARS.fd
```

**List all VMs:**
```bash
sudo virsh list --all
```

## Known Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `Network not found: no network with matching name 'default'` | virt-install ran without `sudo`, using `qemu:///session` instead of `qemu:///system` | Always use `sudo virt-install --connect qemu:///system` |
| UEFI: VM boots to Shell or "No bootable device" | OVMF Secure Boot blocks CDROM; non-secboot OVMF doesn't auto-enable CDROM boot device | **Don't use UEFI.** Use `--boot cdrom,hd` (BIOS mode) |
| UEFI: `Unable to find 'efi' firmware that is compatible` | Changed Secure Boot XML after creation, firmware/NVRAM mismatch | Delete VM + NVRAM, recreate with BIOS mode |
| Failed virt-install leaves ghost definition | Residual in `qemu:///session` from running without sudo | Clean both sessions: `virsh --connect qemu:///session undefine` + `sudo virsh undefine` |
| `virsh net-start default` → "can't find libvirt zone" | firewalld zone missing/broken XML | Write correct zone XML → `firewall-cmd --reload` |
| `virt-install` → disk space error | `/var/lib/libvirt/images/` on system partition (~200MB free) | Use `~/VMs/` on home partition |
| VM → "No bootable device" (BIOS mode) | User exited Live CD without installing | Reattach ISO: `sudo virsh change-media ${VM_NAME} <dev> <iso-path> --insert` then `sudo virsh start ${VM_NAME}` |
| `virsh domifaddr` returns empty | No qemu-guest-agent in VM | Use `sudo virsh net-dhcp-leases default` instead |
| Packages gone after SteamOS update | SteamOS resets system partition | Re-run Phase 1 |
| SSH from agent sandbox fails | No askpass / password auth only | Install `ssh-askpass-gnome` in VM + key auth on host |
| VM boots but screen is black (audio plays) | `--video virtio` incompatible with Ubuntu Live desktop in BIOS mode | Use `--video qxl` instead of `--video virtio` |
