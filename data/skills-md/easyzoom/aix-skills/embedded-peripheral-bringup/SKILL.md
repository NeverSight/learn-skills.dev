---
name: embedded-peripheral-bringup
description: Use when bringing up embedded GPIO, UART, SPI, I2C, PWM, ADC, timers, DMA, interrupts, or board-level peripheral functionality
---

# Embedded Peripheral Bring-Up

## Overview

Use this skill to bring up peripherals from the outside in: board wiring, pin mux, clocks, reset state, electrical mode, driver configuration, interrupts/DMA, and observable signals. Avoid rewriting drivers before proving the peripheral can physically signal.

## When To Use

Use this skill when:

- GPIO, UART, SPI, I2C, PWM, ADC, timer, DMA, or interrupt behavior is wrong.
- A peripheral has no signal, wrong timing, stuck bus, bad data, or only works sometimes.
- The user has schematic snippets, pin mappings, logic analyzer traces, oscilloscope captures, or register dumps.

Do not use this skill when the chip is not booting or the firmware cannot be flashed; resolve those first.

## First Questions

Ask for:

- MCU/SoC and board.
- Peripheral and exact pins.
- Expected behavior versus observed behavior.
- Clock frequency and driver/framework.
- Schematic/pinout evidence and whether signals were measured.
- Whether interrupts, DMA, or low-power modes are involved.

## Workflow

1. Prove the board path.
   Confirm the signal pin, package pin, board net, connector, level shifter, pull-up/down, and external device.

1. Prove pin configuration.
   Check mux/alternate function, electrical mode, drive strength, pull, analog/digital mode, and open-drain requirements.

1. Prove clock and reset.
   Confirm peripheral bus clock, module reset release, prescaler, and any power domain enable.

1. Start with the simplest observable action.
   Toggle GPIO, emit one UART byte, generate one SPI clock burst, scan I2C address, or start one timer output.

1. Add interrupts and DMA last.
   First prove polling or simple blocking transfers, then enable IRQ/DMA and verify vector, priority, buffer alignment, and cache.

1. Compare measurements to configuration.
   Use logic analyzer or oscilloscope evidence for timing, polarity, phase, voltage, and bus contention.

## Peripheral Checks

### GPIO

- Pin mux selects GPIO, not alternate function.
- Output mode and drive strength match load.
- Input mode, pull-up/down, and voltage threshold match circuit.
- Board net is not held by another device.

### UART

- TX/RX crossed correctly.
- Baud calculation matches clock source.
- Pins use correct alternate function.
- Flow control disabled unless wired.
- Logic level matches adapter or peer device.

### SPI

- CPOL/CPHA, bit order, word size, and chip select behavior match the slave.
- SCK frequency is within slave limits.
- MISO/MOSI not swapped.
- CS timing and idle state are correct.

### I2C

- Pull-ups exist and voltage is correct.
- Address is 7-bit versus 8-bit as expected.
- Bus is not stuck low.
- Speed mode matches devices and wiring.
- ACK/NACK is checked before debugging payloads.

### ADC/PWM/Timers

- Pin analog mode or alternate function is correct.
- Reference voltage, sample time, prescaler, period, polarity, and timer clock are verified.
- Timer reload and compare values match actual clock.

## Verification

Before claiming bring-up progress:

- State measured signal evidence or explain why measurement is unavailable.
- Confirm pin, mux, clock, reset, and electrical mode.
- Confirm expected versus observed timing or voltage.
- If IRQ/DMA is involved, confirm the simpler polling path works or state why it cannot be tested.

## Common Failures

- Debugging driver code before checking pin mux and peripheral clock.
- Trusting schematic labels without checking package pin and board net.
- Enabling DMA before proving basic transfers.
- Ignoring pull-ups on I2C or open-drain outputs.
- Confusing logical UART names with physical pins on the board.

## Example

User:

```text
I2C 读不到传感器。
```

Agent:

1. Asks for MCU, pins, pull-ups, address, speed, driver, and logic analyzer result.
1. Checks clock, mux, open-drain mode, and bus idle levels.
1. Confirms ACK during address phase before debugging register reads.
