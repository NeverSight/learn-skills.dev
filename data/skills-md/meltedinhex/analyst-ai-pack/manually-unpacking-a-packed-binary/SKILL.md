---
name: manually-unpacking-a-packed-binary
description: 'Manually unpacks a runtime-packed Windows binary by finding the original entry point
  (OEP) through tail-jump and entropy analysis, then guiding a memory dump at OEP. Activates for
  requests to manually unpack a sample, find the OEP, or unpack a custom/unknown packer that
  generic tools cannot handle.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - unpacking
  - oep
  - packers
  - debugging
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.002
  - T1140
  - T1620
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'MITRE ATT&CK T1027.002 Software Packing — https://attack.mitre.org/techniques/T1027/002/'
  - 'PE Format — https://learn.microsoft.com/windows/win32/debug/pe-format'
---

# Manually Unpacking a Packed Binary

## When to Use

- A sample is runtime-packed by a custom/unknown packer that UPX and generic unpackers cannot
  handle.
- You need to locate the original entry point (OEP) and dump the unpacked image for static
  analysis.

**Do not use** generic auto-unpackers here — this is the manual path for cases where they fail.
Run the sample only inside an isolated, instrumented debugger VM.

## Prerequisites

- A debugger (x64dbg) on an isolated VM and the packed sample.

## Safety & Handling

- The sample executes during unpacking; do this only in a disposable, isolated VM with snapshots.

## Workflow

### Step 1: Characterize the packer statically

```bash
python scripts/analyst.py inspect packed.exe
```

Reports section entropy, suspicious section names (`UPX`, `.vmp`, random), small import tables,
and a write-then-execute section (classic unpacker stub).

### Step 2: Find candidate OEP heuristics

Set a memory breakpoint on the unpacked code section's execution; the packer's tail jump (a far
`jmp`/`ret` into a different section) typically transfers control to the OEP.

### Step 3: Dump at OEP

When stopped at OEP, dump the process image and proceed to import reconstruction (see the
dump-and-rebuild skill).

### Step 4: Verify the dump

Confirm the dumped image has a sane entry point, restored imports, and readable code.

## Validation

- The unpacking stub is identified by a write→execute section transition.
- The tail jump lands in a different section than the stub (OEP candidate).
- The dumped image disassembles cleanly with recognizable runtime startup code.

## Pitfalls

- Stopping at a stage-2 stub rather than the true OEP in multi-layer packers.
- Hardware-breakpoint detection by the packer — vary the breakpoint strategy.
- Dumping before the import table is fully resolved.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the inspector.
- ATT&CK T1027.002 and the PE format spec (linked in frontmatter).
