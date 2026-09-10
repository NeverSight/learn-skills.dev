---
name: embedded-serial-log-debug
description: Use when collecting or debugging embedded serial UART logs, boot consoles,乱码, missing output, baud-rate issues, or serial terminal access
---

# Embedded Serial Log Debug

## Overview

Use this skill to make serial logs trustworthy before drawing conclusions from them. Confirm wiring, voltage level, port ownership, baud settings, boot timing, and log source before debugging firmware behavior.

## When To Use

Use this skill when:

- The user needs UART boot logs, serial console access, or firmware printf output.
- Serial output is missing, garbled, intermittent, delayed, duplicated, or stops mid-boot.
- The task involves USB-to-UART adapters, `screen`, `picocom`, `minicom`, logic analyzers, boot logs, or console prompts.

Do not use this skill when the problem is already proven to be a higher-level protocol issue unrelated to raw serial capture.

## First Questions

Ask for:

- Board/chip and which UART pins are used.
- USB-to-UART adapter model and voltage level.
- Serial device path, such as `/dev/ttyUSB0` or `/dev/ttyACM0`.
- Baud rate, data bits, parity, stop bits, and flow control if known.
- Whether logs are expected from boot ROM, bootloader, kernel, RTOS, or application.
- Whether TX/RX/GND are accessible and common ground is connected.

## Workflow

1. Confirm electrical compatibility.
   Check voltage level, common ground, TX/RX crossing, and whether pins are shared with boot/download modes.

1. Confirm terminal ownership.
   Ensure no other terminal, programmer, modem manager, or IDE owns the serial port.

1. Start with common settings.
   Use 115200 8N1 no flow control unless the board documentation says otherwise.

1. Capture from reset.
   Open the terminal before reset or power-on so early boot logs are not missed.

1. Classify the symptom.
   Missing output,乱码, only TX visible, only RX visible, stops after bootloader, login prompt only, or application printf missing.

1. Verify with a second observation method.
   Use a logic analyzer, oscilloscope, known-good adapter, or loopback test when serial output is suspect.

## Command Patterns

```bash
picocom -b 115200 /dev/ttyUSB0
screen /dev/ttyUSB0 115200
minicom -D /dev/ttyUSB0 -b 115200
stty -F /dev/ttyUSB0 115200 cs8 -cstopb -parenb -ixon -ixoff
```

For permissions:

```bash
ls -l /dev/ttyUSB0
groups
```

Do not run permission-changing commands unless the user approves them.

## Symptom Guide

| Symptom | Likely checks |
| --- | --- |
| No output | TX pin, ground, voltage, wrong UART, reset timing, firmware not booting |
| Garbled output | Baud, clock source, 1T/12T mode, parity, wrong oscillator |
| Stops after bootloader | App jump, app UART init, logging level, crash after handoff |
| Only input fails | RX wiring, console disabled, flow control, login shell not running |
| Random characters on reset | Floating line, wrong voltage, boot ROM at different baud |

## Verification

Before trusting serial evidence:

- State adapter, serial path, voltage level, wiring assumptions, and terminal settings.
- Confirm capture starts before reset/power-on when boot logs matter.
- Report whether the output is clean, garbled, absent, or partial.
- If logs are absent, state which lower-layer checks passed and which remain unverified.

## Common Failures

- Debugging firmware before confirming the adapter voltage and common ground.
- Opening the terminal after early boot logs already passed.
- Assuming 115200 when the boot ROM or app uses another baud.
- Leaving hardware flow control enabled accidentally.
- Forgetting that programmer tools may also occupy the serial port.

## Example

User:

```text
串口没日志，板子不知道有没有跑起来。
```

Agent:

1. Asks for board, UART pins, adapter voltage, serial path, baud, and expected log source.
1. Opens capture before reset.
1. If no output, checks wiring and uses GPIO heartbeat or logic analyzer before blaming firmware.
