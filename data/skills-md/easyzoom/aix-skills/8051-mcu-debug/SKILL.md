---
name: 8051-mcu-debug
description: Use when debugging 8051-compatible microcontrollers, 51 MCU firmware, STC download issues, Keil C51 projects, interrupts, timers, UART, or startup failures
---

# 8051 MCU Debug

## Overview

Use this skill to debug 8051-compatible microcontrollers and 51 MCU firmware systematically. Start by identifying the exact chip family, clock source, download method, toolchain, and failure phase, then prefer observable checks such as reset behavior, UART logs, GPIO toggles, interrupts, and SFR state before changing fuses or boot settings.

## When To Use

Use this skill when:

- The target is an 8051-compatible MCU, such as STC 89/90/12/15/8 series, Nuvoton N76/N79, Silicon Labs C8051, AT89, WCH 8051-like parts, or classic MCS-51 derivatives.
- The user mentions 51 单片机, 8051, Keil C51, SDCC, STC-ISP, ISP/IAP, UART download, `REG52.H`, `intrins.h`, SFR, interrupt vectors, timers, or serial debugging.
- Firmware cannot download, does not run after reset, has no serial output, timer/interrupt behavior is wrong, or peripherals do not respond.

Do not use this skill when:

- The target is Cortex-M, RISC-V, AVR, ESP32, embedded Linux, or another non-8051 architecture.
- The task is only generic C syntax cleanup and does not depend on MCU behavior.
- The user wants to change lock bits, fuses, clock source, or boot configuration before collecting baseline evidence.

## First Questions

Ask for the minimum context needed:

- Exact MCU model and board name.
- Toolchain: Keil C51, SDCC, IAR, vendor IDE, or other.
- Download tool: STC-ISP, Nu-Link, C2 debugger, USB programmer, UART bootloader, or ISP adapter.
- Current symptom: cannot download, no boot, no UART output, timer wrong, interrupt not entered, reset loop, or peripheral failure.
- Clock source and frequency: internal RC, external crystal, PLL, divider, or unknown.
- Power voltage and whether reset, crystal, and UART pins are accessible.
- Available artifacts: source, HEX/IHX, MAP/M51 file, schematic, UART log, programmer output, or logic analyzer capture.

## Workflow

1. Identify the chip family.
   8051 derivatives differ heavily. Confirm the exact part number before assuming SFR names, memory model, bootloader behavior, or download protocol.

1. Classify the failure phase.
   Use these buckets: download failure, reset/startup failure, no observable output, timing error, interrupt error, peripheral error, or memory/model error.

1. Confirm power, reset, and clock.
   Check supply voltage, reset pin state, crystal/clock source, and whether the selected clock matches code assumptions.

1. Establish the safest observation point.
   Prefer UART boot log, GPIO heartbeat, programmer verify, simulator trace, or logic analyzer evidence before changing configuration bytes.

1. Check build artifacts.
   Confirm the generated HEX/IHX belongs to the current source, target model, memory model, and clock assumptions.

1. Inspect only the narrowest next layer.
   For no boot, check reset vector and minimal GPIO toggle before debugging application logic. For timer issues, check oscillator and reload math before rewriting ISR code.

1. Ask before risky operations.
   Lock bits, security bits, config bytes, ISP/IAP settings, erase-all operations, and bootloader changes require explicit user approval.

## Download And Programming Checks

For STC and UART bootloader download issues, check:

- Correct chip model and series selected in the programmer.
- Correct serial port and USB-to-UART driver.
- TX/RX crossed correctly and common ground connected.
- Boot sequence required by the chip, often power-cycle or reset after clicking download.
- Baud rate and auto-baud behavior.
- Whether P3.0/P3.1 or alternate UART pins are shared with other circuits.
- Whether reset, EA, PSEN, BOOT, or vendor-specific boot pins are in the required state.
- Whether the HEX file was rebuilt after source changes.

For adapter/debugger based chips, check:

- Probe driver and target voltage.
- Correct debug protocol, such as C2, ICP, ISP, or vendor-specific interface.
- Whether security or lock bits block read/debug access.
- Whether mass erase is needed and whether the user approves it.

Safe command/tool guidance:

```text
1. Rebuild the project.
1. Confirm the output HEX/IHX path and timestamp.
1. Select the exact MCU model in the programming tool.
1. Try erase/program/verify separately if the tool supports it.
1. Preserve the programmer log for comparison.
```

## Reset And Startup Checks

If firmware downloads but does not run:

- Confirm code is linked for the expected reset vector at `0x0000`.
- Confirm startup code initializes stack pointer as expected.
- Confirm watchdog is disabled or serviced during early boot.
- Add a minimal GPIO toggle at the start of `main()` to prove execution reaches C code.
- Add an early UART byte only after confirming clock and baud-rate math.
- Check whether the chip boots from application flash, bootloader, or external memory.
- Confirm external access settings such as EA pin when relevant.

Minimal observation pattern:

```c
void main(void)
{
    /* Toggle a known test pin before complex init. */
    while (1) {
        TEST_PIN = 0;
        TEST_PIN = 1;
    }
}
```

Use the real pin name from the project or board definition. Do not invent a pin assignment without checking the schematic or existing code.

## Clock And Timing Checks

For wrong baud rate, timer period, PWM, delay, or communication timing:

- Confirm oscillator frequency and whether the MCU uses 12T, 6T, 4T, 2T, or 1T timing.
- Confirm vendor-specific AUXR/CKCON/clock divider settings.
- Confirm timer mode: 13-bit, 16-bit, 8-bit auto-reload, split timer, or PCA.
- Recalculate timer reload values using the actual machine cycle.
- Check whether low-power mode, clock switching, or prescalers affect the peripheral.
- For UART, check SMOD, timer source, reload value, and selected UART pins.

Common timing trap:

```text
Classic 8051 timer tick = Fosc / 12
Many modern 1T derivatives use timer tick = Fosc, unless configured otherwise.
```

## Interrupt Checks

If an interrupt does not fire:

- Confirm global interrupt enable `EA`.
- Confirm peripheral interrupt enable bit, such as `ET0`, `ES`, `EX0`, or vendor-specific bits.
- Confirm interrupt priority does not starve lower-priority handlers.
- Confirm the vector number and Keil `interrupt <n>` value match the target and peripheral.
- Confirm the flag is cleared in the required way.
- Confirm ISR function is not optimized away and uses the correct compiler syntax.
- Confirm shared pins or alternate functions are configured before enabling interrupts.

Keil C51 pattern:

```c
void timer0_isr(void) interrupt 1
{
    /* Clear or reload according to the selected timer mode. */
}
```

SDCC syntax differs. Ask which compiler is used before proposing ISR declarations.

## Memory Model And Stack Checks

For random resets, corrupted variables, or strange calls:

- Confirm memory model: SMALL, COMPACT, LARGE, or SDCC equivalent.
- Check internal RAM, IDATA, XDATA, PDATA, CODE, and BIT usage.
- Inspect the MAP/M51 file for stack location, overlay analysis, and memory overflow.
- Confirm interrupt routines do not exhaust stack or clobber shared variables.
- Mark ISR-shared variables as `volatile`.
- Avoid large local arrays on small internal RAM.
- Confirm external RAM enable and bus pins when using XDATA.

## Peripheral Bring-Up Checks

For GPIO, UART, I2C, SPI, ADC, PWM, PCA, or timers:

1. Confirm the pin exists on the package and board.
1. Confirm pin mode: quasi-bidirectional, push-pull, open-drain, input-only, or analog.
1. Confirm alternate function mapping and crossbar settings on enhanced 8051 chips.
1. Confirm peripheral clock and reset state.
1. Confirm pull-ups, level shifting, and external circuit constraints.
1. Confirm timing with oscilloscope or logic analyzer when possible.

## Safety Rules

- Do not change lock bits, security bits, option bytes, clock source, bootloader, or mass erase settings without explicit user approval.
- Do not assume all 8051 derivatives share the same SFR layout or interrupt vectors.
- Do not trust delay loops until the oscillator and machine-cycle mode are confirmed.
- Do not paste reusable passwords or proprietary programmer keys into chat.
- Do not keep programming retries going without preserving the tool log and exact error message.

## Verification

Before claiming progress:

- State the exact MCU model, toolchain, programmer, clock source, and failure phase.
- Confirm whether download/program/verify succeeded separately.
- Confirm one early observable signal, such as GPIO toggle, UART byte, simulator PC, or programmer reset behavior.
- For timing issues, show the oscillator, machine-cycle mode, timer mode, and reload calculation.
- For interrupt issues, state the enable bits, vector number, flag behavior, and compiler ISR syntax.
- List any risky action skipped or waiting for user approval.

## Common Failures

- Treating STC, Nuvoton, Silabs, and classic 8051 SFRs as interchangeable.
- Selecting the wrong chip model in STC-ISP or vendor programmer.
- Forgetting the power-cycle/reset sequence required for UART bootloader download.
- Calculating timers as 12T when the chip is configured as 1T.
- Using Keil ISR syntax in SDCC projects, or the reverse.
- Debugging UART baud rate before confirming oscillator and SMOD/timer settings.
- Using large local variables on tiny internal RAM.

## Example

User:

```text
STC 51 单片机下载成功但串口没有输出。
```

Agent:

1. Asks for exact STC model, oscillator frequency, toolchain, HEX timestamp, UART pins, and programmer log.
1. Confirms download and verify succeeded separately.
1. Checks whether the code reaches `main()` with a GPIO heartbeat.
1. Recalculates UART baud rate using the actual clock and 1T/12T setting.
1. Reviews UART pin mapping, timer source, SMOD, and interrupt enable bits before changing code.
