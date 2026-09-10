---
name: cmbacktrace-integration
description: Use when integrating, porting, configuring, or debugging CmBacktrace on Cortex-M faults, stack traces, firmware metadata, fault handlers, or crash logs
---

# CmBacktrace Integration

## Overview

Use this skill to integrate CmBacktrace as a Cortex-M crash diagnosis tool. The key is to preserve fault context, provide correct firmware metadata, route output safely, and verify that backtraces map to the running ELF.

## When To Use

Use this skill when:

- The target is Cortex-M and the user wants automatic fault diagnosis or stack backtraces.
- The issue involves HardFault, fault handlers, register dumps, firmware name/version/hardware version, or crash logs.
- The project uses or plans to use CmBacktrace.

Do not use this skill for non-Cortex-M faults. Use `embedded-fault-debug` or the architecture-specific debug skill instead.

## First Questions

Ask for:

- MCU/core, compiler, optimization level, and build flags.
- Fault handler code and whether the system resets immediately.
- Output backend for crash text: UART, RTT, flash, EasyLogger, shell, or custom.
- Firmware metadata values and where they are defined.
- Whether the ELF/MAP file matching the running image is available.
- Current fault output or absence of output.

## Integration Checklist

1. Integrate in the fault path.
   Call CmBacktrace from the HardFault/fault handling path before reset and before clearing fault state.

1. Provide metadata.
   Firmware name, hardware version, software version, and platform identifiers should be meaningful enough for field logs.

1. Keep output safe.
   Crash output must not block forever, allocate heavily, or depend on services that may be corrupted.

1. Match symbols.
   Ensure the saved crash output can be mapped to the exact ELF/MAP file used to build the flashed image.

1. Account for compiler behavior.
   Optimization, frame pointer omission, link-time optimization, and stripped symbols can reduce backtrace quality.

1. Verify with a controlled fault.
   Trigger a known null pointer or assert in a lab build, then confirm the report identifies the expected function.

## Porting Checks

- Fault handler does not reset before CmBacktrace runs.
- Stack pointer and fault stack frame are still valid when called.
- Output route is initialized early or has a crash-safe fallback.
- RTOS task stack ranges are known if task-aware backtracing is expected.
- Watchdog timeout is long enough to emit crash data or is handled intentionally.
- Crash logs stored to flash do not erase unrelated data without approval.

## Common Failures

- No output because UART/logger is not safe inside HardFault.
- Backtrace points to wrong functions because ELF does not match firmware.
- System resets before crash report completes.
- Optimized build produces shallow or confusing backtrace.
- Crash handler recursively faults while printing too much.

## Verification

Before claiming CmBacktrace works:

- State MCU/core, compiler, output backend, and firmware metadata.
- Confirm a controlled crash produces a report.
- Confirm the report maps to the expected function in the matching ELF.
- Confirm reset/watchdog behavior after report.
- State whether persistent crash storage is used and how data loss is avoided.

## Example

User:

```text
想在 Cortex-M 项目里接 cmbacktrace，HardFault 后能看到调用栈。
```

Agent:

1. Asks for MCU, compiler flags, HardFault handler, output backend, and matching ELF.
1. Ensures CmBacktrace runs before reset and output is crash-safe.
1. Uses a controlled fault to verify report generation and symbol mapping.
