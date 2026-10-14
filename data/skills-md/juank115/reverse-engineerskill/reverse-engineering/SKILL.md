---
name: reverse-engineering
description: Safely analyze, disassemble, decompile, or debug unknown binaries, executables, DLLs, malware, firmware, and packed or obfuscated code. Use for reverse engineering, suspicious-file triage, unpacking, Ghidra/IDA/radare2/x64dbg/GDB help, IOC extraction, YARA, or questions about what a binary does.
license: MIT
compatibility: claude-code, opencode, codex, cursor
metadata:
  author: juank.ai12
  version: 1.2.1
  audience: beginners
  language: en
  topics: static-analysis, dynamic-analysis, malware, firmware, disassembly, debugging
---

# Reverse Engineering Skill for Beginners

This skill helps you analyze unknown binaries, executables, malware samples, firmware images, and obfuscated code step by step. It assumes you are a beginner and prioritizes safety, clarity, and repeatable workflows.

## When to use this skill

- The user drops a suspicious file, binary, or executable and asks "what does this do?"
- The user wants to understand how a program works without source code.
- The user mentions disassembly, decompilation, debugging, malware, firmware, obfuscation, or unpacking.
- The user needs help choosing tools or interpreting output from reverse engineering utilities.

## Quick start: run the triage script first

On any unknown file, start with the [bundled triage script](scripts/triage.py) (read-only, pure Python, no dependencies):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/triage.py" <sample>
```

If `CLAUDE_SKILL_DIR` is not set in your environment, run it from this skill's directory instead. It reports hashes, entropy, format (PE/ELF/Mach-O), sections, packer hints, possible anti-analysis indicators, and extracted strings — enough to decide the next step. Treat every heuristic as a lead to verify, not proof of malicious behavior.

## Bundled resources

This skill ships supporting files. Load a reference only when the task matches its domain:

| Resource | Load when... |
|----------|--------------|
| [`references/windows-pe.md`](references/windows-pe.md) | Analyzing Windows PE files (.exe, .dll, .sys): headers, imports, packers, manual unpacking |
| [`references/linux-elf.md`](references/linux-elf.md) | Analyzing Linux/Unix ELF binaries: headers, symbols, GDB workflow, anti-analysis |
| [`references/malware-analysis.md`](references/malware-analysis.md) | The sample may be malicious: lab setup, unpacking tactics, MITRE-mapped behaviors, YARA |
| [`references/firmware-iot.md`](references/firmware-iot.md) | Firmware images or embedded devices: binwalk extraction, emulation, UART/JTAG |
| [`references/cheatsheet.md`](references/cheatsheet.md) | You need a specific command: x64dbg, GDB, radare2, Ghidra, WinDbg shortcuts |
| [`references/static-analysis-example.md`](references/static-analysis-example.md) | A beginner needs a complete static-analysis example |
| [`references/dynamic-analysis-example.md`](references/dynamic-analysis-example.md) | A beginner needs a complete isolated dynamic-analysis example |
| [`scripts/triage.py`](scripts/triage.py) | Running read-only first-pass triage |
| [`assets/report-template.md`](assets/report-template.md) | Writing the final analysis report |

## Safety first: mandatory execution gate

Reverse engineering can involve malicious code. **Never run or debug an unknown executable on the host machine.** Static inspection is allowed on the host when the tooling only reads the sample.

Before providing or executing any command that starts a sample, continues a debugger, steps through an unpacking stub, emulates firmware, or connects live hardware, you **MUST verify every applicable item** with the user:

- [ ] Execution will occur in a dedicated, disposable analysis VM or sandbox, not on the host. Shared folders, shared clipboard, drag-and-drop, and host credential integration are disabled.
- [ ] A clean snapshot exists and can be restored after analysis.
- [ ] Networking is disabled or attached only to an isolated fake-net. It is not bridged to a home, corporate, or production network.
- [ ] Monitoring tools are installed and started before the sample.
- [ ] The environment contains no production credentials, personal data, tokens, or trusted devices.
- [ ] For physical firmware work, the device is owned or authorized, isolated from trusted networks, and connected with verified voltage and safe hardware practices.

Ask for explicit confirmation when these facts are not already established. If any applicable item is unconfirmed, **stop at phases 1–3** and offer read-only triage, static analysis, or disassembly only. A warning alone does not satisfy this gate.

Identify files by SHA-256 before execution. Hash lookups are read-only; uploading the sample itself to a public analysis service requires the user's permission because the file may become public.

## Beginner's reverse engineering workflow

Use the same six phases for ordinary binaries, suspected malware, and firmware. Skip an inapplicable phase only when you state why:

1. **Triage**: identify file type, architecture, packing, and entropy.
2. **Static analysis**: read strings, headers, imports, and metadata without executing.
3. **Disassembly / decompilation**: convert machine code to readable form.
4. **Dynamic analysis**: after the execution gate, run or emulate under controlled observation.
5. **Behavioral analysis**: record network, filesystem, registry, process, or device activity.
6. **Reporting**: summarize findings with IOCs, MITRE ATT&CK mappings, and recommendations.

Firmware / IoT is a **conditional domain track, not a seventh phase or a replacement for phase 5**. When the input is firmware or an embedded device, load `references/firmware-iot.md` and apply its acquisition, extraction, architecture, emulation, and hardware guidance within the six phases above. For example, extraction belongs to phases 1–2, native-code review to phase 3, emulation to phase 4, and observed device behavior to phase 5.

## Choose the right tool depth

Start with the lowest-complexity tool that answers the question, then move deeper only when the evidence requires it.

| Level | Start with | Move here when... |
|-------|------------|-------------------|
| Beginner / first pass | Bundled `triage.py`, `file`, `strings`, Detect It Easy, PE-bear | You need format, hashes, strings, sections, or packer clues |
| Guided visual analysis | Ghidra, IDA Free, Cutter; Procmon/System Informer after the execution gate | You need cross-references, decompilation, or observable runtime behavior |
| Advanced / manual work | radare2, GDB with gef/pwndbg, WinDbg, x64dbg unpacking, Scylla/IAT repair | Simpler tools cannot explain control flow, anti-analysis, or a packed payload |

Do not make manual unpacking or IAT repair the beginner's default. Explain the goal of each advanced command and the expected observable result before using it.

## Phase 1: Triage

Start here for every sample.

### Identify the file

Run on the host or a safe analysis VM:

- `file <sample>` — file type and architecture.
- `exiftool <sample>` — metadata, compiler hints, timestamps.
- `sha256sum <sample>` — cryptographic hash for lookups.
- `ssdeep <sample>` — fuzzy hash for similar samples.

### Check for packing / obfuscation

- High entropy sections suggest packing or encryption.
- Few imports combined with large `.text` or `.data` sections suggest a packer.
- Look for section names like `UPX0`, `UPX1`, `.vmp`, `.themida`, `.petite`.

The bundled script highlights known packer section names, high-entropy or writable-executable sections, and possible anti-debugging, timing, or virtualization strings. Confirm these leads in later phases; they can appear in legitimate software.

## Phase 2: Static analysis

Inspect strings, headers, imports, exports, metadata, resources, and signatures without executing the sample.

### Useful static tools

| Tool | Purpose |
|------|---------|
| `file` | Identify file type and architecture |
| `strings` | Extract readable strings |
| `exiftool` | Metadata extraction |
| `binwalk` | Signature analysis and carving |
| `hexdump -C` | Raw byte inspection |
| `pefile` (Python) | Parse PE headers |
| `pyelftools` (Python) | Parse ELF headers |
| `capstone` (Python) | Lightweight disassembly |
| `yara` | Rule-based pattern matching |

## Phase 3: Disassembly & decompilation

Use these tools depending on budget and platform:

| Tool | Type | Best for |
|------|------|----------|
| **Ghidra** | Free, open source | Static analysis, decompilation, cross-platform |
| **IDA Free** | Freemium | Disassembly, beginner-friendly graph view |
| **radare2 / Cutter** | Free, open source | Command-line workflows, scripting |
| **Binary Ninja** | Commercial | Fast analysis, excellent IL |
| **x64dbg** | Free debugger | Windows dynamic analysis |
| **GDB + gef/pwndbg** | Free debugger | Linux dynamic analysis |

### Decompilation tips for beginners

- Rename functions and variables as you understand them.
- Look for `main`, `WinMain`, or entry-point functions first.
- Trace user input (network, files, registry, command line) to dangerous APIs.
- Search for suspicious API calls: `CreateRemoteThread`, `VirtualAllocEx`, `InternetOpenUrl`, `RegSetValueEx`, `WriteProcessMemory`.

## Phase 4: Dynamic analysis & debugging

Do not enter this phase until the mandatory execution gate is fully verified.

### Before execution (MUST verify all applicable items)

- [ ] Dedicated, disposable VM or sandbox confirmed; host integrations disabled.
- [ ] Clean snapshot taken.
- [ ] Network disabled or routed only through an isolated fake-net.
- [ ] Monitoring selected from the table below, installed, and started.
- [ ] No real credentials, sensitive data, or trusted devices are exposed.

### Monitoring tools

| Tool | Platform | What it records | Safety requirement |
|------|----------|-----------------|--------------------|
| **Procmon** | Windows | Registry, file, process events | Start inside the verified VM before sample execution |
| **Process Hacker / System Informer** | Windows | Processes, memory, handles | Use only inside the verified VM for an unknown sample |
| **Wireshark** | Cross-platform | Network traffic | Capture only the isolated VM/fake-net interface, never a trusted LAN |
| **strace / ltrace** | Linux | Syscalls and library calls | These tools execute the sample; the verified VM is mandatory |
| **x64dbg / WinDbg** | Windows | Live debugging | Loading/continuing may execute code; the verified VM is mandatory |
| **GDB** | Linux | Live debugging | Starting/continuing may execute code; the verified VM is mandatory |

### Debugging checklist (only after the gate)

- Set breakpoints on suspicious APIs.
- Step through unpacking stubs if packed, inside the verified VM only.
- Dump unpacked payloads from memory when safe.
- Record the full command-line arguments and environment variables.

## Phase 5: Behavioral analysis

Document observed behavior systematically. For suspected malware, load `references/malware-analysis.md`; for firmware, record services, filesystem changes, device interfaces, and network behavior using `references/firmware-iot.md`.

### Persistence mechanisms

- Registry run keys (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`).
- Scheduled tasks (`schtasks`).
- Startup folders.
- Services and drivers.
- WMI event subscriptions.

### Network indicators

- DNS queries.
- HTTP/HTTPS C2 callbacks.
- IP addresses and ports.
- User-Agent strings.

### Data theft / impact

- File enumeration.
- Screenshot capture.
- Keylogging hooks.
- Credential dumping (`lsass`, SAM hive).
- Encryption/ransomware file extensions.

### IOCs to collect

- SHA-256 hashes.
- File paths created.
- Registry keys modified.
- Network indicators.
- Mutexes / event names.
- Dropped filenames.

## Phase 6: Reporting

End every session with a clear report (use `assets/report-template.md` as the deliverable structure):

1. **Executive summary**: what is the sample and why it matters.
2. **Indicators of Compromise (IOCs)**: hashes, IPs, domains, file paths.
3. **Behavior summary**: what the sample does when executed.
4. **MITRE ATT&CK mapping** (for malware): Tactics and Techniques observed.
5. **Tools used**: list of tools and commands.
6. **Recommendations**: containment, detection, and prevention steps.

## Output format

When helping the user, structure your response like this:

```markdown
## TL;DR
One-paragraph summary of the finding or next step.

## Analysis
Step-by-step reasoning, tool output, and interpretation.

## Findings
- Bullet 1
- Bullet 2

## IOCs (if malware)
| Type | Value |
|------|-------|
| SHA-256 | ... |
| IP | ... |

## Next steps
1. Do this next.
2. Then do this.

## Safety reminders
- Reminder 1
- Reminder 2
```

## Example prompts

- "Analyze this executable. Is it malicious?"
- "Decompile this function and explain what it does."
- "Help me unpack this UPX sample."
- "What IOCs can I extract from this memory dump?"
- "Walk me through reversing this firmware image."
- "Explain this assembly snippet line by line."

## Resources

- [Ghidra](https://ghidra-sre.org/)
- [radare2](https://rada.re/n/)
- [Cutter](https://cutter.re/)
- [x64dbg](https://x64dbg.com/)
- [MalwareBazaar](https://bazaar.abuse.ch/)
- [VirusTotal](https://www.virustotal.com/)
- [MITRE ATT&CK](https://attack.mitre.org/)
