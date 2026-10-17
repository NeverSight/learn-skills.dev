---
name: sgdk-debug
description: Diagnose SGDK build errors, Mega Drive ROM faults, graphics glitches, and frame-time problems using the SGDK Docker toolchain, target symbols, and measured workloads.
---

# SGDK debugging

Find the first failing stage, reproduce it, and change the smallest thing that
explains the evidence. Keep a working ROM for comparison.

## Start with evidence

- Record the container image, SGDK version, command, first relevant error, and
  emulator/device and region. Respect a project's selected image. Otherwise use
  `ewrogers/sgdk:latest`.
- Run `doctor` through that image. It contains Linux ARM64 and AMD64 tools;
  Docker chooses the host architecture. A host emulator remains outside Docker.
  Windows needs Docker's Linux-container backend. Do not force AMD64 on an ARM
  machine unless comparing architectures.
- Read the actual `/opt/sgdk/inc` declaration and relevant `/opt/sgdk/src`
  implementation before proposing an API call. Use `grep` or Python inside the
  image; `rg` is not installed. Upstream examples and documentation are evidence,
  not permission to invent a similar-sounding API.
- Separate compiler/resource errors, linker errors, ROM startup faults, rendering
  problems, and workload overruns. Preserve the full log on disk and summarize
  the first cause instead of chasing every follow-on error.

## Choose the investigation

- **Build failure or crash:** read [builds-and-faults.md](references/builds-and-faults.md)
  for clean builds, exact-ELF address lookup, memory accounting, and emulator limits.
- **Slow game or visual corruption:** read [performance.md](references/performance.md)
  for SGDK's measurement semantics, VBlank/DMA and sprite limits, and useful comparisons.
- **Large ROM or sound/bus fault:** read [banking-and-audio.md](references/banking-and-audio.md)
  for cartridge mapping, padding, mapped-pointer lifetimes and FM/PSG ownership.
- **Which ROM is this?** Run `python3 scripts/rom_report.py /path/to/rom.bin`
  from this skill's directory, adding `--json` for automation. This only reads
  header facts and file size/hash. Its notes are advisory; it cannot prove that a
  ROM runs, calculate RAM use, or validate SGDK's checksum scheme.

For Python on Windows, use `py -3` if `python3` is unavailable. Helpers use only
the standard library and accept paths with spaces.

## Prove the fix

Rebuild the affected configuration and repeat the failing input/workload. For
performance, compare optimized builds with matching region, emulator speed,
graphics, audio, and instrumentation. Include worst-case spikes, not only an
average or an idle title screen. For graphics/audio, compilation is not a
playtest. Report what was measured, what was only inspected, and what still needs
an emulator or hardware check.

Keep `out/rom.bin`, its matching `out/rom.out` ELF, source revision and image
digest together when preserving a failure. Do not upload ROMs or project assets
without the user's instruction.
