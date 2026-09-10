---
name: low-power-debug
description: Use when debugging embedded sleep, standby, deep sleep, wakeup, current consumption, clock gating, lost debug access, or low-power mode failures
---

# Low Power Debug

## Overview

Use this skill to debug low-power behavior by measuring current and wake sources before changing sleep configuration. Low-power bugs often involve board leakage, clocks, wake flags, debug settings, peripheral state, and firmware sequencing.

## When To Use

Use this skill when:

- Current consumption is too high or unexpectedly low.
- The device fails to enter sleep, cannot wake, wakes immediately, or loses debug access.
- The task involves sleep, stop, standby, deep sleep, retention RAM, wake pins, RTC, watchdog, clock gating, or PMIC sequencing.

Do not use this skill when the board cannot boot at all; establish basic boot first.

## First Questions

Ask for:

- Chip/board and intended low-power mode.
- Measured current, expected current, and measurement setup.
- Wake sources and whether wake flags are available.
- Debug probe attached or detached during measurement.
- Peripherals left enabled before sleep.
- Power rails, external devices, pull-ups, and board revision.

## Workflow

1. Confirm measurement validity.
   Check meter range, sampling rate, burden voltage, shunt placement, rails included, and whether debugger/USB is attached.

1. Separate firmware from board leakage.
   Measure baseline board state, external devices, pull-ups, LEDs, regulators, and sensors.

1. Confirm intended sleep mode.
   Verify the actual mode entered, not just the API called.

1. Capture wake reason.
   Read wake flags immediately after wake before clearing them.

1. Disable peripherals methodically.
   Clocks, UART, ADC, timers, DMA, USB, radio, sensors, and pull configurations can dominate current.

1. Protect debug access.
   Warn that deep sleep may disconnect SWD/JTAG. Use timed wake, GPIO heartbeat, or connect-under-reset recovery.

## Checks

- Debugger and semihosting disabled for current measurement.
- Unused GPIO configured to safe states.
- External pull-ups/pull-downs not causing leakage.
- Regulator and sensor quiescent currents accounted for.
- Wake pins polarity and pull state correct.
- RTC/LPTIM/watchdog clock source active if used.
- SRAM/retention domains configured intentionally.
- Interrupt flags cleared before sleep and read after wake.

## Verification

Before claiming progress:

- State measured current, expected current, mode, and measurement setup.
- State whether debugger/USB was connected.
- Report actual wake source or wake flag evidence.
- List peripherals and rails still enabled.
- State recovery method if debug access may be lost.

## Common Failures

- Measuring through USB while claiming battery current.
- Leaving the debugger attached and trusting sleep current.
- Clearing wake flags before reading them.
- Ignoring external sensors, pull-ups, LEDs, or regulators.
- Entering a shallower sleep mode than intended because a peripheral clock is active.

## Example

User:

```text
进入低功耗后电流还有 5mA，预期几十微安。
```

Agent:

1. Asks for mode, current setup, rails measured, debugger state, wake sources, and board peripherals.
1. Separates board leakage from MCU sleep current.
1. Checks enabled clocks, GPIO states, regulators, and wake flags before code changes.
