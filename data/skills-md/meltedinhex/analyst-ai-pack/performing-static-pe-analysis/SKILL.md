---
name: performing-static-pe-analysis
description: 'Extracts structure and indicators from a Windows PE file without executing it:
  headers, sections, imports/exports, resources, entropy, and embedded strings to infer
  capability and packing. Activates for requests to statically analyze a PE, EXE, or DLL, or
  inspect imports and headers.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - static-analysis
  - pe
  - imports
  - entropy
  - windows
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1129
  - T1140
d3fend:
  - D3-FA
  - D3-FCR
references:
  - 'Microsoft PE Format specification — https://learn.microsoft.com/windows/win32/debug/pe-format'
  - 'pefile library — https://github.com/erocarrera/pefile'
---

# Performing Static PE Analysis

## When to Use

- You have a Windows executable or DLL and need to infer its capabilities before (or instead
  of) detonation.
- You want to assess packing, suspicious imports, timestamps, and embedded resources.
- You are gathering features for YARA authoring or detection.

**Do not use** import tables alone to conclude behavior — packed samples hide imports until
runtime. If imports are sparse and entropy is high, move to unpacking.

## Prerequisites

- `pefile` (`pip install pefile`) and optionally `capa`/PEStudio for deeper capability ID.
- The sample in neutralized form inside the lab.

## Safety & Handling

- Static only: parse the file, never run it. Keep the neutralized extension.

## Workflow

### Step 1: Parse headers and metadata

```bash
python scripts/analyst.py analyze sample.bin
```

Note the compile timestamp (often forged), subsystem (GUI/console), machine type (x86/x64),
and whether it is a DLL.

### Step 2: Review sections and entropy

Per-section entropy reveals packing. A tiny `.text` plus a huge high-entropy section, or
non-standard section names (`UPX0`, `.themida`), indicate a packer:

```text
.text   entropy 6.4  (normal code)
UPX1    entropy 7.95 (packed)
```

### Step 3: Classify imports

Group imported APIs into behavioral buckets:

```text
Injection : VirtualAllocEx, WriteProcessMemory, CreateRemoteThread   [T1055]
Network   : InternetOpen, HttpSendRequest, WinHttpConnect            [T1071]
Crypto    : CryptEncrypt, CryptAcquireContext                        [T1486]
Persistence: RegSetValueEx, CreateService                            [T1547/T1543]
```

A sample importing only `LoadLibrary`/`GetProcAddress` is resolving APIs dynamically — a
packing/evasion tell.

### Step 4: Inspect resources and strings

Look for embedded PEs in resources (droppers), config blobs, and notable strings (URLs,
mutex names, paths).

### Step 5: Check signing

Verify the Authenticode signature: unsigned, self-signed, or revoked certificates are
suspicious for software claiming to be legitimate.

## Validation

- Section entropy and import counts agree (packed → few imports + high entropy).
- Suspicious import buckets correspond to plausible behavior.
- Embedded PE detection is confirmed by an `MZ`/`PE` header inside a resource.

## Pitfalls

- Trusting the compile timestamp as a real build date — it is trivially forged.
- Concluding "benign" because imports look ordinary; the import table may be a stub for a
  packed payload.
- Ignoring TLS callbacks, which can run code before the entry point.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the analyzer and import
  classification map.
- Microsoft PE Format spec and pefile (linked in frontmatter).
