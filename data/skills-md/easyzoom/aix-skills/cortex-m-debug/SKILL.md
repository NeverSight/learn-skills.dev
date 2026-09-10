---
name: cortex-m-debug
description: Use when debugging Cortex-M microcontrollers, firmware bring-up, SWD/JTAG sessions, faults, startup code, or flashing failures
---

# Cortex-M Debug

## Overview

Use this skill to debug ARM Cortex-M firmware systematically. Start by identifying the exact MCU, board state, debug probe, toolchain, and failure phase, then choose the safest inspection path before changing flash, option bytes, clocks, or startup code.

## When To Use

Use this skill when:

- The target is a Cortex-M MCU, such as Cortex-M0/M0+/M3/M4/M7/M23/M33/M55/M85.
- The user mentions SWD, JTAG, J-Link, ST-Link, CMSIS-DAP, OpenOCD, pyOCD, GDB, or vendor IDE debug.
- Firmware does not boot, cannot be flashed, stops in `Reset_Handler`, hits HardFault, or has no UART/log output.
- The task involves vector tables, startup files, linker scripts, clocks, reset behavior, or fault registers.

Do not use this skill when:

- The target is Cortex-R (use `cortex-r5-debug`), embedded Linux, RISC-V, AVR, ESP8266, ESP32 Xtensa, or another non-Cortex-M architecture.
- The user only needs application-level C code review with no target-specific debug context.
- The request is to modify production firmware or security configuration before collecting baseline evidence.

## First Questions

Ask for the minimum context needed:

- MCU part number and board name.
- Core family if known, such as Cortex-M0+, M4F, M7, or M33.
- Current symptom: cannot connect, cannot flash, no boot, crash, hang, wrong peripheral behavior, or no logs.
- Debug probe: J-Link, ST-Link, CMSIS-DAP, DAPLink, ULINK, or onboard probe.
- Debug transport: SWD or JTAG.
- Toolchain and workflow: OpenOCD, pyOCD, J-Link GDB Server, STM32CubeIDE, Keil, IAR, PlatformIO, Zephyr, RTOS, or bare metal.
- Available artifacts: ELF, MAP file, linker script, startup file, OpenOCD config, boot log, fault dump, or GDB transcript.

## Workflow

1. Classify the failure phase.
   Use these buckets: probe cannot connect, flash/download fails, reset/startup fails, runtime fault, peripheral bring-up fails, or low-power/wakeup fails.

1. Establish a non-destructive debug connection.
   Prefer connect-under-reset when firmware may reconfigure SWD pins, enter low power, or crash immediately.

1. Confirm target identity.
   Read the MCU ID, core type, flash size, RAM size, and debug probe target report before trusting assumptions.

1. Load symbols before changing target state.
   In GDB, load the ELF symbols first so addresses, functions, and sections are meaningful.

1. Collect baseline evidence.
   Record reset PC, SP, vector table address, fault registers if applicable, and whether the image in flash matches the expected build.

1. Pick the narrowest next check.
   Do not jump from "no boot" directly to rewriting startup code. Verify reset vector, memory map, clock assumptions, and fault state first.

1. Ask before destructive actions.
   Chip erase, option byte changes, mass erase, readout protection changes, boot mode changes, and flash loader changes require explicit user approval.

## Debug Connection Checklist

For SWD/JTAG connection issues, check:

- Probe driver and permissions.
- Correct target voltage and common ground.
- SWDIO, SWCLK, RESET, GND, and VTref wiring.
- Probe speed. Lower the clock for unstable boards, for example 100 kHz to 1 MHz.
- Reset strategy: normal reset, hardware reset, connect-under-reset, or halt-after-reset.
- Whether firmware disables debug pins, changes clocks too early, enters sleep, or locks the chip.
- Whether readout protection, secure debug, TrustZone, or option bytes block access.

Useful command patterns:

```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
arm-none-eabi-gdb build/firmware.elf
JLinkGDBServer -device <device> -if SWD -speed 4000
pyocd list
pyocd gdbserver --target <target>
```

## GDB Baseline

After GDB connects, collect evidence before editing code:

```gdb
target extended-remote :3333
monitor reset halt
info registers
x/8wx 0x00000000
x/8wx 0x08000000
info files
bt
```

For Cortex-M, pay special attention to:

- `sp`: should point into valid RAM after reset.
- `pc`: should point to `Reset_Handler` or a valid flash/RAM execution address.
- Vector table word 0: initial stack pointer.
- Vector table word 1: reset handler address with Thumb bit set.
- `xpsr`: Thumb state and exception state.
- `VTOR`: vector table location on cores that implement it.

## Fault Debugging

When the target hits HardFault, BusFault, UsageFault, or MemManage:

1. Stop and preserve the fault state.
   Do not reset before reading fault registers.

1. Read core fault registers.
   Common System Control Block addresses:

```text
SCB_CFSR  = 0xE000ED28
SCB_HFSR  = 0xE000ED2C
SCB_DFSR  = 0xE000ED30
SCB_MMFAR = 0xE000ED34
SCB_BFAR  = 0xE000ED38
SCB_AFSR  = 0xE000ED3C
SCB_SHCSR = 0xE000ED24
```

1. In GDB, read them:

```gdb
x/wx 0xE000ED28
x/wx 0xE000ED2C
x/wx 0xE000ED34
x/wx 0xE000ED38
info registers
bt
```

1. Decode the stacked frame.
   Determine whether MSP or PSP was active, then inspect stacked `r0-r3`, `r12`, `lr`, `pc`, and `xpsr`.

1. Map the faulting PC.

```gdb
info symbol <pc>
list *<pc>
disassemble /m <function>
```

Common causes:

- Invalid vector table or wrong linker script origin.
- Stack pointer outside RAM or stack overflow.
- Calling through a null or corrupted function pointer.
- Unaligned access on cores/configurations that fault.
- Executing from erased flash or invalid memory.
- FPU enabled in compiler flags but not initialized, or ABI mismatch.
- Interrupt handler missing, weak default handler hit, or wrong IRQ name.

## Startup And Linker Checks

If the target fails before `main()`:

- Confirm the linker script Flash and RAM origins match the exact MCU.
- Confirm `.isr_vector` is placed at the boot address expected by the boot mode.
- Confirm initial SP is within RAM and properly aligned.
- Confirm `Reset_Handler` copies `.data`, zeros `.bss`, initializes clocks only after safe reset defaults, and calls `SystemInit`/`main` in the intended order.
- Confirm C library initialization is included if C++ constructors or libc startup are required.
- Confirm vector table relocation, bootloader offset, and application offset agree.

## Flashing And Reset Checks

If flashing fails:

- Identify whether the failure is connect, erase, program, verify, or reset.
- Confirm the target config matches the MCU family and flash bank.
- Lower SWD speed and try connect-under-reset.
- Check target voltage and reset line behavior.
- Ask before mass erase or option byte changes.
- Preserve readout protection and security state unless the user explicitly approves changing it.

If flashing succeeds but the board does not run:

- Compare the programmed address with the linker script origin.
- Confirm boot pins or option bytes select the expected boot source.
- Halt immediately after reset and inspect SP/PC.
- Check whether watchdog, clock setup, or early peripheral init resets the chip.

## Peripheral Bring-Up Checks

For UART, GPIO, SPI, I2C, PWM, ADC, or timers:

1. Confirm the peripheral clock is enabled.
1. Confirm pin mux/alternate function and electrical mode.
1. Confirm reset state and initialization order.
1. Confirm board schematic pin mapping and package pinout.
1. Confirm interrupt enable, priority, vector name, and handler symbol.
1. Confirm DMA channel, request mapping, cache, and alignment on cores where relevant.

## Safety Rules

- Do not mass erase, change option bytes, disable protections, alter boot configuration, or flash unknown binaries without explicit approval.
- Do not assume the MCU family from board branding. Ask for the exact part number or read it from the probe.
- Do not treat Cortex-M0/M0+ like Cortex-M3/M4/M7 for fault decoding. Some registers and features differ.
- Do not trust source-level debugging until the ELF, flash image, and running target are confirmed to match.
- Do not keep retrying at high SWD speed when the target connection is unstable.

## Verification

Before claiming progress:

- State the MCU, core family, probe, transport, and toolchain used.
- Confirm whether the probe can connect and halt the core.
- Report reset `sp`, reset `pc`, and whether they are in valid memory ranges.
- If a fault occurred, report fault registers and the mapped faulting symbol/address.
- If flashing was attempted, report erase/program/verify status separately.
- List any destructive action skipped or waiting for user approval.

## Common Failures

- Debugging the wrong MCU target config.
- Forgetting connect-under-reset when firmware disables SWD pins.
- Fixing startup code before checking reset SP/PC and linker origins.
- Resetting immediately after a fault and losing the fault state.
- Ignoring bootloader offsets when the vector table is not at flash base.
- Assuming all Cortex-M cores expose the same debug and fault registers.

## Example

User:

```text
STM32 Cortex-M4 固件下载后没日志，怀疑没启动。
```

Agent:

1. Asks for MCU part number, board, probe, toolchain, firmware ELF, and whether SWD can connect.
1. Connects with reset halt and loads symbols.
1. Checks initial SP/PC, vector table, linker origin, and whether `Reset_Handler` is reached.
1. If it faults, reads SCB fault registers before resetting.
1. Summarizes evidence and asks before erase, option byte changes, or code modifications.
