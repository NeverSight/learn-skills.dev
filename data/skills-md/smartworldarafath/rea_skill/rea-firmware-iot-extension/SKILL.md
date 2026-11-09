---
name: rea-firmware-iot-extension
description: Authorized reverse engineering for embedded firmware, IoT images, RTOS/bare-metal binaries (ARM/MIPS/RISC-V), Smart Contracts (EVM bytecode), and RF/signal recordings using REA MCP.
---

# REA Firmware, IoT, EVM & Signal Reverse Engineering Skill

## Scope & Authorization
Covers all first-party reverse engineering tasks beyond standard desktop/web/mobile apps, including embedded firmware images, bootloaders, RTOS binaries, EVM smart contracts, and digital signal recordings.

## Execution Pipeline
1. **Firmware & Embedded Systems (`inspect_firmware_regions`, `extract_firmware`):**
   - Identify partition tables, bootloader headers (U-Boot), compressed filesystems (SquashFS, CramFS, JFFS2, LittleFS), and bare-metal load addresses.
   - Disassemble ARM Cortex-M/A, MIPS, RISC-V, Xtensa (ESP32), or AVR code using REA MCP (`open_binary`, `list_procedures`, `procedure_pseudo_code`) and Rizin/Ghidra.
   - Reconstruct peripheral MMIO register maps (UART, SPI, I2C, GPIO, DMA) and clean C/Rust embedded firmware projects (`Cargo.toml` / `CMakeLists.txt` / `Makefile`).
2. **Smart Contracts & EVM Bytecode (`inspect_evm_interface`):**
   - Extract 4-byte function selectors, event topic hashes, storage slot layouts, and access control modifiers, and reconstruct clean, verified Solidity (`.sol`) contracts with Foundry/Hardhat tests.
3. **RF & Signal Recording Analysis (`decode_signal_recording`, `inspect_signal_decoders`):**
   - Decode captured digital/RF signal recordings, frame preambles, modulation parameters, and payload structures.
