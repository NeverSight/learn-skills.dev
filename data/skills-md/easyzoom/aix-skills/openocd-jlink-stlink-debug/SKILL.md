---
name: openocd-jlink-stlink-debug
description: Use when debugging OpenOCD, J-Link, ST-Link, CMSIS-DAP, probe connection, reset scripts, flash algorithms, GDB attach, semihosting, RTT, or SWD/JTAG failures
---

# OpenOCD J-Link ST-Link Debug

## Overview

Use this skill to debug probe sessions by separating physical wiring, probe
firmware, target voltage, reset strategy, transport, target script, flash
algorithm, and GDB behavior. Probe failures are often reset or adapter issues.

## When To Use

Use this skill when:

- The user cannot connect, halt, reset, flash, erase, verify, or attach with
  OpenOCD, J-Link, ST-Link, CMSIS-DAP, pyOCD, or GDB.
- The issue involves SWD/JTAG wiring, adapter speed, reset config, target
  scripts, flash loaders, protected devices, semihosting, RTT, or multicore.
- The same firmware behaves differently under debugger and standalone boot.

Do not use this skill for application fault analysis after a stable debug
session exists. Use the architecture-specific debug skill then. For flash
download failures focused on erase/program/verify, use `mcu-flashing-debug`.

## First Questions

Ask for:

- Probe model, firmware version, debugger tool, target MCU/SoC, board, and OS.
- Wiring: `VTref`, GND, `SWDIO`/`TMS`, `SWCLK`/`TCK`, `nRST`/`SRST`, `SWO`, and
  power ownership.
- Exact command, the `-f interface/*.cfg` and `-f target/*.cfg` scripts,
  `adapter speed`, `transport select`, and full log.
- Reset mode, boot pins, readout protection (STM32 `RDP`), low-power state, and
  external flash.
- Whether connect-under-reset, halt-after-reset, or attach-to-running is needed.

## Launch Reference

- ST-Link: `openocd -f interface/stlink.cfg -f target/stm32f4x.cfg`
  (`stlink.cfg` is the `hla` driver; use `target/stm32f1x.cfg`,
  `stm32h7x.cfg`, `nrf52.cfg` etc. for other parts).
- J-Link: `openocd -f interface/jlink.cfg -c "transport select swd" -f target/stm32f4x.cfg`.
- CMSIS-DAP/DAPLink: `openocd -f interface/cmsis-dap.cfg -c "transport select swd" -f target/stm32f1x.cfg`.
- Force JTAG instead of SWD: `-c "transport select jtag"` (note `stlink.cfg`
  `hla` only supports `hla_swd`/`hla_jtag`).
- Set speed before target script: `-c "adapter speed 1000"` (kHz; deprecated
  alias `adapter_khz`). Pick a probe by serial with `-c "adapter serial <SN>"`
  (older: `hla_serial`).
- Default TCP ports: GDB `3333`, Telnet monitor `4444`, Tcl `6666`.

## Debug Workflow

1. Prove physical connection.
   Check `VTref`, ground, cable length, pinout, `SRST` line, and whether the
   probe powers or only senses the target. In the log confirm a valid
   `SWD DPIDR 0x2ba01477` (Cortex-M3/M4) or JTAG `IDCODE`, not a zero/failed
   read (`SWD DPIDR 0x00000000` / `Error connecting DP: cannot read IDR`).

1. Lower the adapter speed.
   Start with `adapter speed 480` or lower, then raise only after IDCODE, halt,
   reset, and `mdw` reads are stable.

1. Pick the right reset strategy.
   In the target/board cfg set `reset_config`, e.g. `srst_only srst_nogate`
   for connect-under-reset, or `none separate`. Then use
   `reset halt` / `reset init` / `reset run`. Add `-c "reset_config
   connect_assert_srst"` for locked or fast-sleeping parts.

1. Validate target scripts.
   Confirm `transport select`, chip family cfg, TAP/DAP IDs (`-expected-id` on
   `jtag newtap`/`swj_newdap`, `-dp-id` for SWD multidrop), `flash bank`, and
   `_TARGETNAME`/work-area RAM. List cores with `targets`.

1. Separate attach from flash.
   Enter the monitor with `telnet localhost 4444`, then `init` and `reset halt`.
   Read state with `targets`, `reg`, `mdw 0x08000000 4`, `mdh`, `mdb`; write with
   `mww 0x40021000 0x01`. Only then flash:
   `program firmware.elf verify reset` or
   `flash write_image erase firmware.bin 0x08000000` /
   `flash erase_sector 0 0 last` / `flash info 0`. `resume` to run,
   `dump_image out.bin 0x08000000 0x10000` to read back.

1. Add extras last.
   Enable `arm semihosting enable`, SWO/`tpiu`, or RTT only after the base debug
   path is reliable (see RTT And Semihosting).

## GDB Attach

```text
arm-none-eabi-gdb firmware.elf
(gdb) target extended-remote localhost:3333
(gdb) monitor reset halt
(gdb) load
(gdb) monitor reg
(gdb) continue
```

Use `target remote` for a single-session attach, `target extended-remote` to
allow reconnect. `monitor <cmd>` forwards any OpenOCD command (e.g.
`monitor reset init`, `monitor flash write_image erase firmware.bin`).

## RTT And Semihosting

- Semihosting: after halt run `arm semihosting enable` (optionally
  `arm semihosting_fileio enable`); `printf`/`puts` output appears on the
  OpenOCD console once the firmware links `libnosys`/semihosting stubs.
- RTT: `rtt setup 0x20000000 2048 "SEGGER RTT"` then `rtt start`; expose a
  channel with `rtt server start 9090 0` and read it via
  `telnet localhost 9090`. Use `rtt channels` to confirm the control block was
  found. The ID string defaults to `"SEGGER RTT"`.

## Common Failures

- `VTref` is missing, so `Error: target voltage may be too low` or the probe
  cannot sense target voltage.
- Adapter speed too high for early boot/low-power/long wires, giving a failed
  DPIDR read (`Error connecting DP: cannot read IDR`), `Error: init mode failed
  (unable to connect to the target)`, or `SWD ack not OK`.
- `SRST` not wired but the script uses `reset_config srst_only`; switch to
  `none`/`connect_assert_srst`.
- Device is readout-protected or locked (`Error: … cannot be programmed`); for
  STM32 clear `RDP` with `stm32f4x unlock 0` / `stm32f1x unlock 0` (mass-erases).
- Wrong target cfg selects the wrong `flash bank` or work-area RAM, so
  `flash write_image`/`program` fails or verify mismatches.
- External QSPI/SPI flash needs a board-specific `flash bank` driver
  (`stmqspi`, `cfi`), not the internal loader.
- `hla` (`stlink.cfg`) cannot do raw `swd`/`jtag` low-level commands or SWD
  multidrop; use `interface/stlink-dap.cfg` or a J-Link/CMSIS-DAP v2 probe.

## Verification

Before claiming the debug path works:

- State probe, tool, exact command, `transport`, `adapter speed`, and reset mode.
- Confirm `SWD DPIDR`/`IDCODE`, `reset halt`, `targets` shows `halted`, a `reg`
  read, and an `mdw` memory read.
- Confirm `program … verify reset` or `flash write_image` plus verify when
  flashing is required.
- Confirm standalone boot still works after `reset run` and power-cycle, i.e.
  after debugger-specific settings.

## Example

User:

```text
OpenOCD 连 STM32 一直 timeout。
```

Agent:

1. Checks `VTref`, ground, SWD pins, `SRST`, and lowers `adapter speed 480`.
1. Retries with `reset_config connect_assert_srst` and the correct
   `target/stm32f4x.cfg`, watching for `SWD DPIDR`.
1. Separates connection evidence (`init`, `targets`, `mdw`) from
   `program`/`flash write_image` errors.
