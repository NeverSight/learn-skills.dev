---
name: mcu-flashing-debug
description: Use when MCU firmware download, flashing, erase, verify, probe connection, boot mode, read protection, or programmer tool operations fail
---

# MCU Flashing Debug

## Overview

Use this skill to debug MCU programming failures safely. Separate connection, erase, program, verify, and reset problems before recommending mass erase, option byte changes, security unlock, or boot configuration changes.

## When To Use

Use this skill when:

- Firmware cannot be downloaded or flashed to an MCU.
- The programmer reports connect, erase, program, verify, timeout, locked, protected, or target voltage errors.
- The user mentions ST-Link, J-Link, CMSIS-DAP, OpenOCD, pyOCD, STC-ISP, WCH-Link, Nu-Link, vendor programmers, boot pins, ISP, IAP, DFU, or UART bootloader.

Do not use this skill for application-level bugs after a confirmed successful program/verify/run cycle. For probe-specific debugging (OpenOCD scripts, J-Link config, adapter speed), use `openocd-jlink-stlink-debug`.

## First Questions

Ask for:

- MCU part number and board.
- Programmer/probe and connection method.
- Tool name and exact error output.
- Firmware artifact path/type: ELF, HEX, BIN, IHX, UF2, or vendor package.
- Whether erase, program, verify, and reset are separate steps in the tool output.
- Target voltage, reset wiring, boot pins, and whether the board is externally powered.

## Workflow

1. Classify the failing step.
   Do not treat "download failed" as one problem. Identify connect, erase, program, verify, reset, or run failure.

1. Confirm physical and electrical basics.
   Check power, ground, target voltage sense, reset line, boot pins, and signal wiring before changing software.

1. Confirm tool-target match.
   Verify exact chip model, flash algorithm, probe interface, target config, and firmware address.

1. Lower risk before increasing force.
   Try lower adapter speed, connect-under-reset, separate erase/program/verify, and fresh rebuild before mass erase.

1. Preserve logs.
   Capture programmer output and avoid repeated blind retries.

1. Ask before destructive operations.
   Mass erase, security unlock, option byte writes, readout protection changes, bootloader erase, and config fuse changes require explicit approval.

## Method Checks

### SWD/JTAG

- Confirm SWDIO/TMS, SWCLK/TCK, RESET, GND, and VTref.
- Lower adapter clock for long wires or unstable power.
- Try connect-under-reset when firmware disables debug pins or enters low power.
- Confirm the debug probe can see target voltage.
- Confirm readout protection or secure debug is not blocking access.

### UART/ISP/IAP

- Confirm TX/RX cross, common ground, boot pin state, reset/power-cycle sequence, and baud behavior.
- Confirm the chip actually contains a ROM bootloader or vendor ISP mode.
- Confirm USB-to-UART voltage level matches target IO voltage.
- Confirm selected chip model and serial port.

### USB DFU/Bootloader

- Confirm boot mode entry sequence.
- Confirm USB enumeration and permissions.
- Confirm package format and target address.
- Preserve existing bootloader or calibration regions unless explicitly approved.

## Verification

Before claiming flashing is fixed:

- Report connect, erase, program, verify, and reset/run status separately.
- State the programmer, target chip, interface, adapter speed, firmware artifact, and programmed address.
- Confirm whether destructive actions were avoided, skipped, or explicitly approved.
- If verify fails, report the first failing address or range if the tool provides it.

## Common Failures

- Recommending mass erase before confirming wiring and target voltage.
- Selecting a similar but wrong MCU in the programmer.
- Flashing a binary to the wrong base address.
- Ignoring verify failures because program appeared to succeed.
- Forgetting boot pin or reset timing for UART bootloaders.

## Example

User:

```text
OpenOCD 连接 STM32 总是 timeout，下载不了。
```

Agent:

1. Asks for exact chip, probe, OpenOCD configs, wiring, target voltage, and error log.
1. Separates connect failure from flash failure.
1. Suggests lower SWD speed and connect-under-reset before erase.
1. Asks before readout protection or mass erase operations.
