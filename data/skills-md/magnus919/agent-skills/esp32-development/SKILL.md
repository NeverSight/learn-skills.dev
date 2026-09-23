---
name: esp32-development
description: >-
  Build, configure, flash, test, debug, and recover firmware for ESP32-family boards, including ESP-IDF C/C++, Arduino/PlatformIO, MicroPython, CircuitPython, ESPHome, Zephyr, Rust, and NuttX. Use when identifying an ESP32 board, choosing a framework, wiring GPIO or peripheral buses, integrating sensors or actuators, diagnosing serial/boot/power/network failures, or planning OTA and production security. Do not use as a substitute for the exact board schematic, SoC datasheet, or attached component datasheet.
license: MIT
compatibility: Portable across agent harnesses. Live work requires the selected framework toolchain, a supported ESP32-family board, data-capable USB connection, and platform serial permissions.
metadata:
  source_index: references/source-index.md
  research_checked: "2026-07-15"
---

# ESP32 Development

Treat the board, attached circuit, firmware, and host toolchain as one system. An ESP32 task is complete only when the intended behavior is observed at the hardware boundary, not when compilation or flashing alone succeeds.

## Operating contract

1. Identify the exact board, SoC family, module, flash/PSRAM size, USB transport, power source, and board revision. Do not transfer a pin map between ESP32, S2, S3, C2, C3, C5, C6, H2, or P4 variants.
2. Read the board schematic or pinout, the matching SoC/module datasheet, and every attached component datasheet before choosing pins or voltage levels.
3. Start with read-only host and USB discovery. Opening a serial monitor may toggle DTR/RTS and reset the target; use a no-reset option when the running state matters.
4. Choose one framework based on the product constraint. Reuse its project generator, examples, drivers, build system, flasher, monitor, and debugger before writing wrappers.
5. Bring up one layer at a time: power and boot, serial log, one GPIO, one bus, bus scan or loopback, device identity register, raw readings, calibration, then application behavior.
6. Before the first flash or hardware mutation, confirm the target port, chip family, image/partition layout, rollback or reflashing path, and electrical safety. Never guess a flash offset.
7. Preserve calibration controls for real sensors, clocks, ADCs, PWM devices, and actuators. Physical variation is expected.

## Pre-response evidence gate

Complete this gate before drafting a non-trivial plan or recommendation:

1. Build a claim ledger for every material positive claim, negative claim, command, and numeric design choice. A URL in `source-index.md` is navigation, not evidence; retrieve the exact chip/current-version page or mark the claim `UNKNOWN`.
2. Command help proves syntax only. Record required target state plus reset, DTR/RTS, download-mode, RAM-stub, port, and mutation effects from current documentation. If operational preconditions are unverified, do not present the command as executable.
3. Missing hardware artifacts stay missing. Do not replace them with archetypes, examples, or words such as `usually`, `typical`, or `some modules`; state what the observed label does not establish.
4. Do not invent thresholds, margins, intervals, durations, point counts, percentages, or model forms. Derive them from an authoritative source or a measurement criterion; otherwise leave them `UNKNOWN`.
5. Audit the final response against the ledger. Remove or downgrade every material claim that lacks its required evidence.

## First read-only discovery

```sh
python3 scripts/esp32-preflight.py
python3 scripts/esp32-preflight.py --json
pio device list --json-output       # when PlatformIO is installed
mpremote connect list               # when mpremote is installed
```

The preflight script does not open serial ports. A USB descriptor can identify a bridge or board family, but it does not prove the chip is in download mode or that a firmware-specific protocol is active. Read [decisions and preflight](references/decisions-and-preflight.md) before probing an unknown board.

## Choose the path

| Need | Read first |
|---|---|
| Identify board, host, port, transport, or framework | [decisions and preflight](references/decisions-and-preflight.md) |
| Select safe pins, power, protection, pull-ups, or level shifting | [hardware and electrical safety](references/hardware-and-electrical-safety.md) |
| Choose ESP-IDF, Arduino, MicroPython, CircuitPython, ESPHome, Zephyr, Rust, or NuttX | [firmware frameworks](references/firmware-frameworks.md) |
| Create, build, flash, monitor, test, or debug using native CLIs | [native tool workflows](references/native-tool-workflows.md) |
| Use GPIO, ADC, DAC, PWM, touch, I2C, SPI, UART, I2S, RMT, PCNT, TWAI/CAN, or USB | [peripherals and buses](references/peripherals-and-buses.md) |
| Integrate a sensor, display, LED, relay, motor, servo, solenoid, or other load | [sensors, actuators, and calibration](references/sensors-actuators-and-calibration.md) |
| Add Wi-Fi, BLE, ESP-NOW, Zigbee/Thread, sleep, OTA, or production power behavior | [connectivity, power, and OTA](references/connectivity-power-and-ota.md) |
| Diagnose boot, flashing, crashes, brownouts, buses, networking, or security state | [debugging, recovery, and security](references/debugging-recovery-and-security.md) |
| Refresh a command or version-sensitive claim | [source index](references/source-index.md) |

## Minimal bring-up sequence

1. Fill in `templates/hardware-bringup.md` and record the exact source for every pin and voltage decision.
2. Run `scripts/esp32-preflight.py`; then use the selected framework's own board list and project generator.
3. Build without hardware. Resolve every warning that changes pin, partition, flash, or security behavior.
4. Connect only power and USB. Capture the boot log before attaching peripherals.
5. Flash a framework example or generated minimal project using the framework-produced offsets and image metadata.
6. Verify serial output, reset behavior, and chip identity. Then add one peripheral or load at a time.
7. For buses, prove electrical idle levels and run a scan/loopback before introducing a driver. For actuators, test the control signal without the load, then use an external driver and supply.
8. Run the requested behavior through repeated reset and power-cycle tests. If OTA is in scope, prove rollback or serial recovery before relying on it.

## Templates and helper

- `templates/hardware-bringup.md` — board, power, pin, component, and recovery worksheet.
- `templates/component-contract.md` — datasheet-led sensor or actuator integration record.
- `templates/esp-idf-main.c` — small ESP-IDF GPIO task with explicit configurable pins.
- `templates/platformio.ini` — minimal PlatformIO environment with explicit board/framework and version-pinning placeholders.
- `templates/micropython-i2c-scan.py` — configurable I2C electrical/identity probe.
- `templates/esphome-device.yaml` and `templates/esphome-secrets.yaml.example` — safe ESPHome bring-up configuration with external secrets and explicit framework choice.
- `templates/zephyr-esp32.overlay` — minimal devicetree GPIO/I2C overlay pattern.
- `scripts/esp32-preflight.py` — dependency-free, non-mutating host/tool/port classifier; run `--self-test` for its deterministic check.

## Hard boundaries

- ESP32 GPIO is not generally 5 V tolerant. Use the exact datasheet limits and a level shifter or driver when required.
- Do not power motors, relays, solenoids, servos, high-current LEDs, or large capacitive loads from a GPIO. Use a rated driver, external supply, shared reference where appropriate, and flyback protection for inductive loads.
- Do not treat a GPIO number as universally safe. Strapping, flash/PSRAM, USB/JTAG, input-only, ADC, and wake restrictions vary by chip, module, board, and boot mode.
- Do not erase flash as a generic first troubleshooting step. Capture the boot log, image metadata, partitions, calibration/NVS implications, and recovery artifacts first.
- Secure boot, flash encryption, eFuses, and download-mode restrictions can be irreversible. Read the matching SoC and ESP-IDF security documentation and prove the recovery path on disposable hardware before production provisioning.
- Never put Wi-Fi, API, OTA, or signing secrets in public templates or source control.

## When not to use

Do not use this skill alone for PCB layout certification, RF/antenna design, mains-voltage work, functional-safety certification, medical devices, or a component whose authoritative datasheet is unavailable. Escalate those tasks to the appropriate electrical, RF, safety, or compliance discipline. For a non-ESP32 target, use that platform's own skill and tooling.

## Exit criteria

The exact target and sources are recorded; electrical limits and pin choices are justified; the native build and flash tools complete without unexplained errors; logs show the intended image booted; each bus or device passes an identity-level check; calibrated behavior is observed at the physical boundary; and reset, power-cycle, and recovery behavior match the requested deployment mode.
