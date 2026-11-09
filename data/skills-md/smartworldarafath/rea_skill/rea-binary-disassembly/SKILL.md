---
name: rea-binary-disassembly
description: Complete Windows (PE .exe/.dll/.sys/.msi), Linux (ELF .so/.ko/.deb/.rpm/.AppImage/.snap), and macOS (Mach-O .dylib/.app) static & dynamic binary reverse engineering, unpacking, decompilation, and behavioral tracing using REA MCP, Ghidra, IDA, Rizin/Cutter, x64dbg, WinDbg, GDB (pwndbg/GEF), ILSpy/dnSpyEx, strace/ltrace, and ProcMon.
---

# REA Binary Disassembly & Cross-Platform Reverse Engineering Suite (Windows, Linux & macOS)

## Scope & Authorization
Covers all first-party native, managed, and packaged binary reverse engineering, lost source code recovery, and security debugging across Windows, Linux, and macOS.

---

## PART A: Windows 9-Stage Reverse Engineering Toolchain & Checklist

### 1. Environment & Prerequisites
- **Sandbox / VM:** VMware Workstation, VirtualBox, or Hyper-V with snapshots; FLARE VM; Windows SDK & Microsoft Sysinternals Suite.

### 2. File Fingerprinting, Triage & PE Analysis (`.exe`, `.dll`, `.sys`)
- **REA MCP (`open_binary`, `binary_overview`, `inspect_binary_layout`, `inspect_pe_resources`):** Inspects PE headers, sections (`.text`, `.data`, `.rdata`, `.rsrc`), IAT/EAT, and resources.
- **Detect It Easy (DIE) / PE-bear / CFF Explorer / PEStudio:** Identifies compilers/frameworks (MSVC, Clang, MinGW, .NET, Delphi, Go, Rust, Electron, PyInstaller), digital signatures, and section entropy.
- **Capa & FLOSS:** Automatically maps binary capabilities (registry, network, crypto) and extracts static, stack, and decoded obfuscated strings.

### 3. Unpacking & Installer Extraction
- **7-Zip / UniExtract2:** Extracts Inno Setup, NSIS, InstallShield, and WiX installers.
- **`lessmsi` / Orca:** Extracts tables, scripts, and payloads from Windows Installer (`.msi`) packages.
- **Resource Hacker / RisohEditor & REA MCP (`inspect_pe_resources`):** Extracts embedded icons (`RT_ICON` with valid ICO headers), dialogs, manifests (`RT_MANIFEST`), version info, and custom RCDATA blobs.
- **UPX (`upx -d file.exe`):** Unpacks UPX-compressed executables.

### 4. Native Code Disassemblers & Decompilers (C / C++ / Rust / Go / Delphi)
- **REA MCP (`list_procedures`, `procedure_assembly`, `procedure_pseudo_code`, `batch_decompile`, `xrefs`, `get_call_graph`, `trace_call_path`, `trace_native_values`, `inspect_native_data_type`):** Automated static decompilation and cross-reference analysis.
- **Ghidra / IDA Pro & Free / Binary Ninja / Cutter (Rizin):** Interactive disassembly, HLIL/MLIL/decompiler pseudo-C recovery, and control-flow graphing.
- **IDR (Interactive Delphi Reconstructor):** Recovers Delphi VCL forms (`.dfm`) and Object Pascal symbols.
- **GoReSym / Redress & REA MCP (`inspect_go_binary`, `inspect_rust_binary`):** Recovers `.gopclntab` functions, struct types, and Rust crate metadata/vtables from stripped Go and Rust binaries.

### 5. Managed & Framework-Specific Decompilers (.NET, Java, Python, Electron, AutoIt/AHK)
- **.NET (`C# / VB.NET / F#`):** REA MCP (`inspect_managed_artifact`, `inspect_managed_members`, `import_managed_reconstruction`), **ILSpy (`ilspycmd`)**, **dnSpyEx**, and **dotPeek** to export full `.csproj` Visual Studio solutions.
- **Electron / Node.js Apps:** `@electron/asar` (`npx asar extract app.asar out_dir/`) and REA MCP (`inspect_electron_fuses`, `analyze_javascript_application`).
- **Python Executables (`PyInstaller` / `py2exe` / `Nuitka`):** `pyinstxtractor` / `pyinstxtractor-ng` to extract `.pyc` bytecode, followed by `pycdc` (Decompyle++), `uncompyle6`, or `PyLingual` to recover `.py` source files.
- **Java Desktop Apps (`.jar` / Launch4j `.exe`):** `JADX`, `Recaf`, `Bytecode Viewer`.
- **AutoIt / AutoHotkey (AHK):** `Exe2Aut` and `AHK_decompiler`.

### 6. Dynamic Analysis & Debuggers (Runtime Inspection)
- **x64dbg / x32dbg (+ Scylla):** User-mode debugging, hardware/memory breakpoints, and IAT reconstruction.
- **WinDbg & REA MCP (`inspect_recorded_crash`):** User-mode debugging, crash dump (`.dmp`) triage, and kernel-mode driver (`.sys`) debugging.
- **System Informer (Process Hacker) / Process Explorer:** Real-time inspection of threads, handles, loaded DLLs, and memory strings.
- **PE-sieve / HollowsHunter:** Detects and dumps runtime-unpacked or injected modules from process memory.

### 7. System, File, Registry & API Monitoring
- **Process Monitor (`ProcMon`):** Real-time file system, Registry, DLL load, and process/thread event capture.
- **API Monitor (Rohitab) & REA MCP (`observe_native_calls`, `instrument_with_frida`):** Hooks and logs Win32 API calls with exact input arguments and return values.
- **Autoruns & Regshot:** Tracks startup persistence and before/after Registry/filesystem diffs.

### 8. Network & Protocol Analysis
- **Wireshark / Fiddler / `mitmproxy` / Burp Suite / TCPView & REA MCP (`inspect_pcap_capture`):** Captures raw TCP/UDP packets, TLS streams, and HTTP/WebSocket traffic.

### 9. Local Storage & Configuration Formats
- **SQLite (`inspect_sqlite_database` / DB Browser for SQLite), Registry (`regedit` / Registry Explorer), and Hex Templates (`ImHex` / `010 Editor` / `HxD`)** across `%AppData%`, `%LocalAppData%`, `%ProgramData%`, and `HKCU`/`HKLM`.

### Standard 5-Step Windows Analysis Workflow Checklist
1. **Isolate:** Snapshot VM / workspace environment.
2. **Triage:** Run `DIE` / `open_binary` / `binary_overview` to identify exact compiler/framework (.NET, C++, Electron, Python, Go, Rust, Delphi) and packing status.
3. **Static Decompilation:** Route `.NET` to `ILSpy`/`dnSpyEx`, native `C/C++/Rust/Go` to `REA MCP`/`Ghidra`/`Rizin`, and `Electron`/`Python` to `asar`/`pyinstxtractor`.
4. **Behavioral Monitoring:** Trace file, registry, and network activity via `ProcMon`, `System Informer`, and `Wireshark`/`Fiddler`.
5. **Runtime Debugging & Full Code Reconstruction:** Verify runtime state via `x64dbg`/`WinDbg`/`Frida`, reconstruct 100% zero-skeleton source code, and verify compilation (`zig cc`, `cl.exe`, `gcc`, `dotnet`, `cargo`, `go`).

---

## PART B: Linux 8-Stage Reverse Engineering Toolchain & Checklist

### 1. Environment & Multi-Architecture Setup
- **Containers & VMs:** QEMU/KVM, Docker/Podman/LXC, REMnux.
- **GNU Binutils (`build-essential`):** `objdump`, `readelf`, `nm`, `strings`, `strip`, `addr2line`, `c++filt`.
- **Cross-Arch Execution:** `qemu-user-static` and `gdb-multiarch` for running and debugging ARM, MIPS, PowerPC, and RISC-V ELF binaries on x86_64 hosts.

### 2. Package, Container & Firmware Unpacking
- **`.deb` (Debian/Ubuntu):** `dpkg-deb -x package.deb out_dir/` and `dpkg-deb -e package.deb out_dir/DEBIAN` (or `ar x`).
- **`.rpm` (RHEL/Fedora):** `rpm2cpio package.rpm | cpio -idmv` and `rpm -qp --scripts package.rpm`.
- **`.AppImage` & `.snap`:** `--appimage-extract` or `unsquashfs`.
- **`.flatpak` & OCI/Docker Images:** `ostree`, **Dive**, `skopeo`, and `tar`.
- **Firmware (`binwalk` / `unblob` & REA MCP `inspect_firmware_regions`, `extract_firmware`):** Recursively extracts SquashFS, CramFS, JFFS2, ext4, and initramfs filesystems.

### 3. ELF Binary Triage & Hardening Analysis (`.elf`, `.so`, `.ko`)
- **`file` & `readelf -a` (`eu-readelf`):** Identifies architecture, dynamic vs. static linking, BuildID, ELF headers (`-h`), segments (`-l`), sections (`-S`), dynamic tags (`-d`), and symbols (`-s`).
- **Shared Library Dependencies:** Safe inspection via `readelf -d file | grep NEEDED` or `objdump -p` (or `ldd` / `lddtree`).
- **`checksec` (`pwn checksec`):** Audits **RELRO** (Full/Partial), **Stack Canary**, **NX**, **PIE**, and **FORTIFY_SOURCE**.
- **DIE / Capa / FLOSS:** Identifies GCC/Clang/Go/Rust toolchains, UPX packing, and obfuscated strings.

### 4. Native Disassemblers & Decompilers (C, C++, Rust, Go)
- **REA MCP (`open_binary`, `list_procedures`, `procedure_pseudo_code`, `batch_decompile`, `inspect_go_binary`, `inspect_rust_binary`)**, **Ghidra** (with DWARF support), **IDA Pro**, **Binary Ninja**, and **Rizin / Cutter** (`rz-ghidra`).
- **CLI Utilities:** `objdump -d -M intel`, `nm -C`, `c++filt`, and **GoReSym / Redress**.

### 5. High-Level Language & Framework Binaries on Linux
- **Python (`PyInstaller` / `Nuitka` / `Cython`):** `pyinstxtractor-ng` + `pycdc` / `PyLingual`.
- **Electron (`.AppImage` / `.deb`):** `@electron/asar`.
- **.NET Core / Mono (Linux C# single-file bundles):** `AvaloniaILSpy` / `ilspycmd` & REA MCP `inspect_managed_artifact`.
- **Java (`.jar`) & Compiled Shell Scripts (`shc`):** `JADX` / `Vineflower` and **UnSHc**.

### 6. Dynamic Analysis, Tracing & Runtime Hooking
- **`strace`:** Traces kernel system calls (`strace -f -s 256 ./app` for `openat`, `read`, `write`, `connect`, `execve`).
- **`ltrace`:** Intercepts dynamic library calls (`strcmp`, `malloc`, `getenv`, `SSL_write`).
- **GDB (`start_gdb_session`, `gdb_console`) + `pwndbg` / `GEF` / `peda`** and GUI debuggers (**EDB**, **SeerGDB**).
- **`LD_PRELOAD` Hooking, Frida (`instrument_with_frida`), & eBPF (`bpftrace`, `bcc`):** User-space (`uprobes`) and kernel (`kprobes`) dynamic instrumentation.

### 7. Process, Memory, `/proc` & Kernel Module Inspection
- **`/proc/<PID>/` Forensics:** `/proc/<PID>/maps` (memory layout & `rwx` pages), `/proc/<PID>/mem` (memory dumping), `/proc/<PID>/fd/` (open files/sockets), `/proc/<PID>/exe` (actual binary symlink).
- **System & Kernel Monitoring:** `lsof -p <PID>`, `pspy`, `auditd`, `sysdig`, `falco`, and `modinfo` / `lsmod` for Linux Kernel Modules (`.ko`).

### 8. Network & D-Bus IPC Analysis
- **Packet & Socket Inspection:** `tcpdump`, `tshark`, Wireshark, `ss -tulpan`, `mitmproxy`, and **D-Bus IPC** monitoring (`busctl`, `dbus-monitor`, **Bustle**).

### Standard 5-Step Linux Analysis Workflow Checklist
1. **Isolate & Triage:** Run `file`, `checksec`, `readelf -a`, and `DIE` / `open_binary` to determine architecture, linking type, compiler, and symbol status.
2. **Extract Strings & Dependencies:** Run `strings -a` (or `FLOSS`) and `readelf -d` to list linked `.so` libraries, file paths, and hardcoded configs.
3. **Behavioral Tracing:** Execute under `strace -f` and `ltrace` to observe every file opened, env variable checked, and socket connected.
4. **Static Decompilation:** Decompile in `REA MCP`, `Ghidra`, `Cutter`, or `IDA` to recover full C/C++/Rust/Go/Python/.NET source logic.
5. **Dynamic Debugging & Verification:** Attach `GDB` (`pwndbg`/`GEF`), inspect `/proc/<PID>/maps`, reconstruct 100% compilable source code, and verify with `gcc`/`clang`/`cargo`/`go`.
