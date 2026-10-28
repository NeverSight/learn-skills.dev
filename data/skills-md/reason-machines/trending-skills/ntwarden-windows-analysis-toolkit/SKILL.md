---
name: ntwarden-windows-analysis-toolkit
description: NtWarden is a Windows Analysis and Research Toolkit providing GUI-based inspection of processes, kernel internals, services, network, ETW, and more via ImGui + DirectX 11 with optional kernel driver support.
triggers:
  - "use NtWarden to inspect Windows processes"
  - "analyze process with NtWarden"
  - "kernel callbacks with NtWarden"
  - "set up NtWarden kernel driver"
  - "connect NtWarden remote inspection"
  - "detect hooks with NtWarden"
  - "NtWarden SSDT hook detection"
  - "build and run NtWarden"
---

# NtWarden Windows Analysis and Research Toolkit

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

NtWarden is a Windows system inspection tool built on ImGui + DirectX 11. It covers processes, services, network, kernel internals, ETW, registry, object manager, and more — locally or remotely via WinSysServer. A kernel driver (KWinSys) enables deep kernel-mode analysis including SSDT hooks, kernel callbacks, EPT hook detection, and driver integrity checks.

---

## Architecture

| Component | Role |
|---|---|
| **NtWarden** | GUI app (ImGui + DirectX 11) |
| **WinSys** | Static lib — process, service, network enumeration |
| **KWinSys** | Kernel driver — callbacks, SSDT, kernel modules, pool, etc. |
| **WinSysServer** | Headless TCP server for remote inspection |

---

## Build Requirements

- Visual Studio 2022
- Windows SDK 10.0.26100.0+
- WDK (Windows Driver Kit) — required only for KWinSys kernel driver

---

## Building

```powershell
# Open solution in Visual Studio 2022
# Select Release | x64
# Build All

# Output lands in:
x64/Release/NtWarden.exe
x64/Release/WinSysServer.exe
x64/Release/KWinSys/KWinSys.sys
```

Solution structure:
```
NtWarden.sln
├── NtWarden/          # GUI application
├── WinSys/            # Core static library
├── KWinSys/           # Kernel driver (.sys)
└── WinSysServer/      # Remote TCP server
```

---

## Running NtWarden

Always run as **Administrator** for full functionality.

```powershell
# Run elevated
Start-Process NtWarden.exe -Verb RunAs
```

User-mode features (processes, services, network, ETW, registry, object manager) work without the driver.

---

## Kernel Driver Setup (KWinSys)

> ⚠️ Use only in a test VM. Enable test signing before installing.

```powershell
# Enable test signing (requires reboot)
bcdedit /set testsigning on

# On VMs, may also need:
bcdedit /set nointegritychecks on

# Reboot, then run NtWarden as Administrator.
# Switching to the Kernel Mode tab auto-installs and starts KWinSys.
```

Manual driver management:
```powershell
# Install manually
sc create KWinSys type= kernel binPath= "C:\path\to\KWinSys.sys"
sc start KWinSys

# Stop and remove
sc stop KWinSys
sc delete KWinSys
```

The NtWarden GUI also exposes driver management under the **Driver** menu.

---

## Remote Inspection (WinSysServer)

Deploy to a target machine (typically a VM) and connect from NtWarden.

### Files to copy to target

| File | Source Path | Purpose |
|---|---|---|
| `WinSysServer.exe` | `x64/Release/WinSysServer.exe` | Always required |
| `KWinSys.sys` | `x64/Release/KWinSys/KWinSys.sys` | Kernel features only |

### Starting the server (on target, elevated)

```powershell
# Auto-install driver + start server on default port 50002
WinSysServer.exe --install

# Custom port
WinSysServer.exe --install --port 9000

# If driver already installed manually:
WinSysServer.exe
WinSysServer.exe --port 9000
```

### Connecting from NtWarden (on host)

1. Launch NtWarden
2. Go to **Remote** menu
3. Enter target IP and port (default: `50002`)
4. Click **Connect**

### Protocol notes

- Custom binary protocol over TCP
- 12-byte header: `MessageType`, `DataSize`, `Status`
- **No authentication** — use only in isolated lab/VM environments
- User-mode data (processes, services, network) works without KWinSys on target
- Kernel tabs require KWinSys loaded on the remote target

---

## WinSys Static Library — Key Usage Patterns

WinSys is the core library consumed by both NtWarden and WinSysServer. Example integration patterns in C++:

### Process Enumeration

```cpp
#include "WinSys/ProcessManager.h"

// Enumerate all processes (user mode)
auto& pm = WinSys::ProcessManager::Get();
pm.Update();  // Refresh snapshot

for (auto& proc : pm.GetProcesses()) {
    printf("PID: %5u  Name: %s\n",
        proc->Id,
        proc->GetImageName().c_str());
}
```

### Service Enumeration

```cpp
#include "WinSys/ServiceManager.h"

WinSys::ServiceManager svcMgr;
auto services = svcMgr.EnumServices();

for (auto& svc : services) {
    printf("Service: %-40s  State: %u  StartType: %u\n",
        svc.GetName().c_str(),
        svc.Status.dwCurrentState,
        svc.Config.dwStartType);
}
```

### Network Connections

```cpp
#include "WinSys/NetworkManager.h"

WinSys::NetworkManager netMgr;
auto conns = netMgr.GetTcpConnections();

for (auto& conn : conns) {
    printf("PID: %u  Local: %s:%u  Remote: %s:%u  State: %u\n",
        conn.ProcessId,
        conn.LocalAddress.c_str(), conn.LocalPort,
        conn.RemoteAddress.c_str(), conn.RemotePort,
        conn.State);
}
```

### Communicating with KWinSys Driver (IOCTL)

```cpp
#include "WinSys/KernelInterface.h"

// Open handle to driver device
WinSys::KernelInterface ki;
if (!ki.Open()) {
    fprintf(stderr, "Failed to open KWinSys device. Is driver loaded?\n");
    return;
}

// Enumerate kernel modules
auto modules = ki.EnumKernelModules();
for (auto& mod : modules) {
    printf("Base: %p  Size: 0x%X  Path: %s\n",
        mod.Base, mod.Size, mod.FullPath.c_str());
}

// Read kernel callbacks
auto callbacks = ki.EnumProcessCallbacks();
for (auto& cb : callbacks) {
    printf("Callback: %p  Module: %s  Suspicious: %d\n",
        cb.Address,
        cb.OwnerModule.c_str(),
        cb.IsSuspicious ? 1 : 0);
}
```

### Per-Process Security Analysis (Analyze Process)

Accessible via right-click > **Analyze Process** in the GUI, or programmatically:

```cpp
#include "WinSys/ProcessAnalyzer.h"

DWORD targetPid = 1234;
WinSys::ProcessAnalyzer analyzer(targetPid);

auto result = analyzer.Analyze();

// Unbacked executable memory (shellcode indicator)
for (auto& region : result.UnbackedRegions) {
    printf("Unbacked RX region: base=%p size=0x%zX\n",
        region.Base, region.Size);
}

// Hollowing detection
if (result.HollowingDetected) {
    printf("Hollowing: PEB ImageBase=%p vs PE Header ImageBase=%p\n",
        result.PebImageBase, result.PeHeaderImageBase);
}

// Direct syscalls outside ntdll
for (auto& sc : result.DirectSyscalls) {
    printf("Direct syscall at: %p in module: %s\n",
        sc.Address, sc.ModuleName.c_str());
}

// Inline user hooks
for (auto& hook : result.UserHooks) {
    printf("Hook in %s!%s at %p -> %p\n",
        hook.Module.c_str(),
        hook.Function.c_str(),
        hook.Address,
        hook.Target);
}

// Token info
printf("Elevated: %d  IntegrityLevel: %u\n",
    result.Token.IsElevated,
    result.Token.IntegrityLevel);
```

---

## Key Features by Tab

### User Mode (no driver)

| Tab | Capability |
|---|---|
| Processes | Tree view, handles, threads, memory regions, modules |
| Performance | CPU/RAM/GPU/network graphs, overlay mode |
| Services | Status, start type, binary path |
| Network > Connections | TCP/UDP with owning PID |
| Network > Root Certificates | Subject, issuer, thumbprint |
| Network > NDIS | Adapter driver, MAC, speed, media type |
| ETW | Active trace sessions and registered providers |
| IPC | RPC endpoints and named pipes |
| Object Manager | Kernel object namespace browser |
| Registry | Key/value browser |
| Logger | Kernel driver debug logs + GUI logs |

### Kernel Mode (requires KWinSys)

| Tab | Capability |
|---|---|
| Process Objects | EPROCESS enumeration, hidden process detection |
| Modules | Kernel drivers + LolDrivers check |
| Callbacks | Process/thread/image/registry/object/power callbacks + integrity |
| SSDT | Entries with owner and hook detection |
| Kernel Pool | Big pool allocations and tag stats |
| Memory R/W | Read/write kernel memory by address |
| Timers | Per-CPU interrupt and DPC counters |
| Filter | Minifilter drivers with altitude/instance |
| Descriptor Tables | GDT/IDT entries |
| IRP Dispatch | IRP dispatch table for any driver |
| WFP | WFP callout drivers and filters |
| DSE Status | Driver Signature Enforcement state |
| CI Policy | Code Integrity policy and enforcement level |
| Kernel Integrity | Verify kernel .text vs on-disk image |
| Hypervisor Hooks | EPT hook detection via timing analysis |

---

## Common Patterns

### Check if driver is loaded before using kernel features

```cpp
#include "WinSys/KernelInterface.h"

WinSys::KernelInterface ki;
bool driverAvailable = ki.Open();

if (driverAvailable) {
    // Use kernel-mode features
    auto ssdt = ki.GetSSDTEntries();
} else {
    // Fall back to user-mode only
    fprintf(stderr, "KWinSys not loaded — kernel features unavailable.\n");
}
```

### Detect hidden processes (cross-reference EPROCESS list vs user-mode list)

```cpp
WinSys::KernelInterface ki;
ki.Open();

auto kernelProcs = ki.EnumProcessObjects();  // Via EPROCESS walk
auto& pm = WinSys::ProcessManager::Get();
pm.Update();
auto userProcs = pm.GetProcesses();

// Build set of user-visible PIDs
std::unordered_set<DWORD> visiblePids;
for (auto& p : userProcs) visiblePids.insert(p->Id);

// Find PIDs in kernel list but not user list
for (auto& kp : kernelProcs) {
    if (visiblePids.find(kp.ProcessId) == visiblePids.end()) {
        printf("HIDDEN PROCESS: PID=%u Name=%s\n",
            kp.ProcessId, kp.ImageName.c_str());
    }
}
```

---

## Troubleshooting

### NtWarden won't show kernel tabs
- Ensure KWinSys.sys is in the same directory as NtWarden.exe (or `x64/Release/KWinSys/`)
- Run NtWarden as Administrator
- Confirm test signing is enabled: `bcdedit /enum | findstr testsigning`
- Check **Logger** tab for driver load errors

### Driver fails to install
```powershell
# Verify test signing is on
bcdedit /enum | Select-String "testsigning"

# Check for existing broken service entry
sc query KWinSys
sc delete KWinSys  # if stuck, delete and retry

# Some VMs also need:
bcdedit /set nointegritychecks on
# Then reboot
```

### WinSysServer connection refused
```powershell
# Verify server is running on target
netstat -ano | findstr 50002

# Check Windows Firewall on target
netsh advfirewall firewall add rule name="WinSysServer" `
  dir=in action=allow protocol=TCP localport=50002
```

### Capstone not found (user hooks tab shows no data)
- User hook detection with disassembly requires Capstone
- Build WinSys with Capstone linked, or the hook scanner will report bytes without disassembly

### Performance overlay not visible
- Launch NtWarden, go to **Performance** tab
- Enable overlay mode — it renders over other windows using DirectX 11 transparency

### Build errors — missing WDK
- KWinSys requires the Windows Driver Kit
- If you only need user-mode features, exclude KWinSys project from build in Visual Studio (right-click project > **Unload Project**)

---

## Tested Windows Versions

- Windows 11 23H2 (Build 22631.6199)
- Windows 10 22H2 (Build 19045.2006)
- Windows 10 1703 (Build 15063.13)

---

## References

- [zodiacon](https://github.com/zodiacon) — Primary inspiration
- [WinArk](https://github.com/BeneficialCode/WinArk) — Kernel-mode feature reference
- [LolDrivers](https://www.loldrivers.io/) — Vulnerable driver database used in Modules tab
