---
name: qspi-xip-flash-debug
description: Use when debugging QSPI or OSPI NOR flash, execute-in-place XIP, memory-mapped mode, boot from external flash, cache coherency, dummy cycles, or flash timing
---

# QSPI XIP Flash Debug

## Overview

Use this skill to debug QSPI/OSPI flash by separating electrical bring-up,
command mode access, memory-mapped mode, cache policy, linker placement, and
boot flow. XIP failures often come from timing and memory attributes.

## When To Use

Use this skill when:

- The user is bringing up external NOR flash over QSPI, OSPI, OctoSPI, FlexSPI,
  SPIFI, or a similar controller.
- The issue involves JEDEC ID reads, erase/program failures, memory-mapped mode,
  XIP, boot from external flash, random hard faults, or cache corruption.
- The firmware uses external flash for code, assets, filesystem, OTA slots, or
  mapped resources.

Do not use this skill for generic internal flash programming. Use
`mcu-flashing-debug` or `bootloader-debug` instead.

## First Questions

Ask for:

- MCU/SoC, external flash part number, controller, board schematic, and voltage.
- Mode: single/dual/quad/octal, SDR/DDR, memory-mapped, XIP, or command mode.
- Clock speed, dummy cycles, sample shifting, CS timing, and vendor init table.
- Linker script, boot ROM expectations, vector location, and cache/MPU settings.
- Current symptom, JEDEC ID, status registers, and logic analyzer trace if any.

## Debug Workflow

1. Prove command mode slowly.
   Read JEDEC ID, status registers, erase, program, and readback at conservative
   speed before enabling memory mapping.

1. Match flash mode entry.
   Confirm QE bit, opcode set, address width, dummy cycles, wrap mode, and reset
   sequence for the exact flash.

1. Validate memory-mapped mode.
   Read known patterns from mapped address space and compare with command-mode
   reads.

1. Configure cache and MPU.
   Mark flash XIP as executable/cacheable as appropriate, and device registers
   as non-cacheable device memory.

1. Align linker and boot flow.
   Place vectors, code, rodata, assets, and load addresses according to boot ROM
   and startup expectations.

1. Stress timing.
   Test temperature, voltage, max clock, deep power-down, reset, and suspend
   states after the basic path works.

## Common Failures

- Flash part has different dummy cycles or QE-bit location than the example.
- Memory-mapped reads work at low speed but fail at production clock.
- Linker places writable data or vectors in XIP flash incorrectly.
- Cache is enabled without invalidation after programming external flash.
- Boot ROM expects a different image header or flash mode.
- Deep power-down or reset leaves flash in a mode the controller does not expect.

## Verification

Before claiming QSPI/XIP works:

- State flash part, controller, mode, clock, opcode set, and dummy cycles.
- Confirm JEDEC ID, erase/program/readback, and mapped reads.
- Confirm linker placement, vector/boot path, and cache/MPU attributes.
- Confirm reset and cold boot from the selected flash state.

## Example

User:

```text
QSPI XIP 开 cache 后随机 hardfault。
```

Agent:

1. Checks mapped flash attributes, linker placement, and fault address.
1. Compares command-mode and memory-mapped reads.
1. Verifies cache invalidation after programming and MPU region setup.
