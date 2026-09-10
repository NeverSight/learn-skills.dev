---
name: embedded-fault-debug
description: Use when embedded firmware crashes, traps, faults, resets unexpectedly, jumps to default handlers, corrupts stack, or executes invalid instructions
---

# Embedded Fault Debug

## Overview

Use this skill to preserve crash evidence and find the first failing instruction. The agent should read architecture-specific fault state before reset, map addresses to symbols, and separate root cause from secondary symptoms.

## When To Use

Use this skill when:

- Firmware hits HardFault, BusFault, UsageFault, trap, illegal instruction, default handler, watchdog reset, assert, or panic.
- The board resets unexpectedly or hangs after a repeatable action.
- The user has a register dump, fault log, crash PC, stack dump, watchdog event, or GDB backtrace.

Do not use this skill when the target cannot yet connect or flash; use `mcu-flashing-debug` first.

## First Questions

Ask for:

- Architecture/chip family and toolchain.
- Exact symptom and whether it is reproducible.
- Register dump, backtrace, fault/trap registers, assert log, or reset reason.
- ELF/MAP file that matches the running image.
- Whether the target has been reset since the fault.

## Workflow

1. Preserve state.
   Do not reset or reflash until fault registers, PC, LR/RA, SP, and stack frame are captured.

1. Confirm image-symbol match.
   Ensure the ELF/MAP file matches the firmware currently running on target.

1. Identify the faulting address.
   Map PC, exception return address, `mepc`, stacked PC, or return address to a symbol and source line.

1. Classify the cause.
   Separate invalid memory access, illegal instruction, stack overflow, alignment, bus/peripheral access, watchdog, assert, and default handler cases.

1. Walk backward to the first bad state.
   Inspect caller, input pointers, stack bounds, interrupt context, DMA/cache interactions, and recent initialization.

1. Add a focused verification.
   Use a watchpoint, assertion, guard pattern, stack watermark, or minimal repro to prove the suspected cause.

## Architecture Notes

### Cortex-M

Read SCB fault registers before reset:

```text
CFSR  = 0xE000ED28
HFSR  = 0xE000ED2C
MMFAR = 0xE000ED34
BFAR  = 0xE000ED38
```

Decode stacked `r0-r3`, `r12`, `lr`, `pc`, and `xpsr` from MSP or PSP.

### RISC-V

Read:

```text
mcause, mepc, mtval, mtvec, mstatus, sp
```

Check whether `mcause` is interrupt or exception, and map `mepc` to source/disassembly.

### 8051

Use available evidence:

- Reset reason register if the derivative provides one.
- Stack pointer and internal RAM pressure.
- ISR vector selection and default handler loops.
- Watchdog configuration.
- GPIO heartbeat or serial breadcrumbs around suspected code.

## Common Root Causes

- Stack overflow or ISR stack pressure.
- Null/corrupt function pointer.
- Wrong vector table, trap vector, or interrupt number.
- Accessing peripheral before clock/reset release.
- DMA writing outside buffers.
- Cache coherency issue on cache-enabled MCUs.
- Compiler target flags not matching core features.
- Watchdog not serviced during long init.
- Bootloader/app offset mismatch.

## Verification

Before claiming a fault is understood:

- State the matched ELF/MAP and running firmware identity if known.
- Report faulting PC/address and mapped symbol/source.
- Report architecture-specific fault registers or explain why unavailable.
- State the suspected root cause and the evidence linking it to the fault.
- State the next minimal verification step, such as watchpoint, stack watermark, or assertion.

## Common Failures

- Resetting immediately and losing the only useful fault state.
- Trusting a backtrace when the ELF does not match flashed firmware.
- Fixing the line where the fault occurred instead of the earlier corruption.
- Ignoring interrupt context, stack selection, or DMA/cache side effects.
- Treating watchdog reset as a generic crash without reading reset reason.

## Example

User:

```text
程序跑一会儿就进 HardFault。
```

Agent:

1. Asks for chip, ELF, register dump, CFSR/HFSR, stacked PC, and whether reset happened.
1. Maps stacked PC to source.
1. Checks stack bounds, caller, interrupt context, and invalid memory access evidence.
1. Suggests a focused watchpoint or stack watermark before changing code.
