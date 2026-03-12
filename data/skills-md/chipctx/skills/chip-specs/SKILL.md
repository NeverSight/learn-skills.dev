---
name: chip-specs
description: >
  Query authoritative MCU chip specifications including parameters, pin
  definitions, registers, and programming guides. Use when users mention
  chip models (STM32, ESP32, nRF52), ask about peripheral configuration,
  or work with embedded hardware design.
license: MIT
metadata:
  author: chipctx
  version: '1.2.0'
---

# ChipCtx MCU Specs

Authoritative MCU chip specification queries for embedded development.
Real-time access to chip parameters, pin definitions, TRM registers, and programming guides
via the ChipCtx MCP Server.

## MCP Server Setup (MUST check before first query)

This Skill requires the ChipCtx MCP Server. Before making any chip query, you MUST verify the MCP tools are available.

### Step 1: Check Tool Availability

Check if `chip_identify` is available as an MCP tool in the current session. If it is, skip to the Standard Query Flow below.

### Step 2: Auto-Install (if tools not available)

If `chip_identify` is NOT available, install the MCP server using one of these methods:

**Option A — Claude Code Plugin (recommended, auto-configures MCP):**
Tell the user to run these commands and restart:
```
/plugin marketplace add chipctx/skills
/plugin install chipctx@chipctx-marketplace
```

**Option B — Manual MCP setup:**
```bash
claude mcp add --transport http chipctx --scope user https://mcp.chipctx.com
```

### Step 3: Inform User to Restart

After running the install command, tell the user:
> ChipCtx MCP server has been configured. Please restart Claude Code (type `/quit` then relaunch) for the MCP tools to become available. Then retry your query.

**IMPORTANT:** Do NOT attempt to call chip_identify or any other ChipCtx MCP tool after installing — they will not be available until the session is restarted. Do NOT fall back to WebFetch or other workarounds. The user MUST restart first.

### Other Agents

See the [README](./README.md) for MCP configuration on Cursor and other platforms.

## When to Apply

Activate this Skill when ANY of the following conditions are detected:

**1. Explicit — User mentions chip model**
- Specific model: STM32F407VGT6, ESP32-S3-WROOM-1, nRF52840
- Series reference: "STM32F4 series", "ESP32", "nRF52"
- Chip search or comparison: "which chip has BLE and 1MB flash?"

**2. Code Context — Chip-specific headers or APIs**
- Headers: `stm32f4xx.h`, `esp_system.h`, `nrf.h`, `nrf52840.h`
- HAL/SDK calls: `HAL_GPIO_Init()`, `esp_wifi_init()`, `nrf_gpio_cfg_output()`
- Chip-specific register or memory address references

**3. Project Configuration — Build system files**
- STM32CubeMX `.ioc` files
- `platformio.ini` with `board = ...`
- `Makefile`/`CMakeLists.txt` with MCU definitions (`-DSTM32F407xx`)
- ESP-IDF `sdkconfig`, Zephyr `prj.conf`

**4. Topic-Related — Hardware discussion**
- Pin assignments, peripheral configuration, register operations
- GPIO, UART, SPI, I2C, ADC, DMA, Timer topics
- Datasheet, TRM, or hardware design references

## MCP Interface Quick Reference

**MCP Server Endpoint:** `https://mcp.chipctx.com` (Streamable HTTP)

| User Intent | MCP Tool | Input | Output |
|------------|----------|-------|--------|
| Find/identify chip model | `chip_identify` | query (string) | Chip list with id, model, vendor, series, matchScore |
| Chip parameters & specs | `chip_specs` | chipId, category? | Core params, electrical specs, peripheral list |
| Pin definitions & package | `chip_hardware` | chipId, query? | Pin table with AF mapping, package info |
| TRM registers & modules | `chip_trm` | chipId, section? | TRM sections, register/field definitions |
| Programming guide & code | `chip_programming_guide` | chipId, topic | Init steps, code examples, pitfalls |

**Key Principle:** `chipId` bridges all queries. Always call `chip_identify` first to obtain `chipId`, then use it in all subsequent tool calls.

### Intent Routing Matrix

| Keywords in User Query | Tool to Call | Priority |
|----------------------|-------------|----------|
| Model, series, find, compare, identify | `chip_identify` | Always call first |
| Parameters, specs, frequency, flash, RAM, features | `chip_specs` | Basic info |
| Pin, GPIO, package, pinout, AF | `chip_hardware` | Hardware design |
| Register, TRM, module, address, bit field | `chip_trm` | Deep technical |
| Code, init, configure, program, example, HAL | `chip_programming_guide` | Programming |

## Standard Query Flow

Every chip-related query follows this flow:

```
Step 0: Verify chip_identify tool is available (see MCP Server Setup above)
        If NOT available -> auto-install and ask user to restart. STOP here.
Step 1: Extract chip model keywords from user input or project context
Step 2: chip_identify(query) -> validate model, get chipId
Step 3: Check matchScore -> confirm unique match or ask user to select
Step 4: Route to appropriate tool based on user intent
Step 5: Format and present results, generate code if requested
```

**Critical:** Step 0 is mandatory on the first chip query in a session. If MCP tools are missing, do NOT proceed — install and ask for restart. Never skip Step 2. All other tools require `chipId` from `chip_identify`.

## Hardware-Aware Identification

The chip identification flow supports automatic detection from project context:

**Automatic Detection Sources:**
- C/C++ header includes: `#include "stm32f4xx.h"` -> STM32F4 series
- Platform IO config: `board = esp32-s3-devkitc-1` -> ESP32-S3
- CMake definitions: `-DNRF52840_XXAA` -> nRF52840
- STM32CubeMX `.ioc` files: project chip configuration

**matchScore Thresholds:**
- >= 0.9: High confidence, proceed directly
- 0.7-0.9: Moderate confidence, confirm with user
- < 0.7: Low confidence, present candidates for user selection

**Multi-Candidate Handling:**
When multiple chips match, present a numbered list with model, vendor, and description. Ask the user to select. Never silently pick a low-confidence match.

See `rules/flow-chip-identify.md` for detailed flow and error handling.

## Context Injection Strategy

After chip identification, inject specification data progressively:

### Layer 1: Always Inject (after identification)
- Chip model, vendor, series
- CPU core (e.g., ARM Cortex-M4), max frequency
- Flash and RAM capacity, operating voltage

### Layer 2: On-Demand Inject (when discussing peripherals)
- Peripheral specs (UART count, SPI features, etc.)
- Pin definitions and alternate functions for specific peripherals
- Package info (pin count, dimensions)

### Layer 3: Deep Inject (when writing low-level code)
- TRM register definitions (name, address, bit fields, access type)
- Programming guide with init sequences and code examples
- Both HAL-level and register-level implementations

### Context Management
- **Avoid overflow:** Do NOT load all chip data at once. Load only what the current task needs.
- **Prioritize relevance:** When discussing UART, load UART data, not all peripherals.
- **Chip switching:** When user switches to a different chip, clear old context completely and load new chip data. Never mix data from different chips.

See `rules/flow-context-inject.md` for detailed injection flow.

## Supported Chip Families

| Vendor | Series | Example Models |
|--------|--------|---------------|
| STMicroelectronics | STM32F0/F1/F2/F3/F4/F7/H7/L0/L1/L4/G0/G4/U5/WB/WL | STM32F407VGT6 |
| Espressif | ESP32/ESP32-S2/S3/C3/C6/H2 | ESP32-S3-WROOM-1 |
| Nordic Semiconductor | nRF52810/832/833/840 | nRF52840 |

## Rule Categories

Detailed rules are organized in `rules/` for progressive loading:

| File | Impact | Description |
|------|--------|-------------|
| `rules/flow-chip-identify.md` | HIGH | Chip identification triggers, 5-step flow, matchScore handling, error recovery |
| `rules/flow-context-inject.md` | HIGH | 3-layer injection strategy, context window management, chip switching protocol |
| `rules/api-chip-identify.md` | HIGH | chip_identify interface: fuzzy matching, alias recognition, response format |
| `rules/api-chip-trm.md` | HIGH | chip_trm interface: section filtering, Register/RegisterField data format |
| `rules/api-chip-specs.md` | MEDIUM | chip_specs interface: 4 category queries, electrical specs with limits |
| `rules/api-chip-hardware.md` | HIGH | chip_hardware interface: pin/function filtering, AF mapping, package info |
| `rules/api-chip-programming.md` | MEDIUM | chip_programming_guide: SDK/HAL code, init sequences, dual implementations |

**Section index:** See `rules/_sections.md` for loading order and strategy.

## Full Compiled Document

For platforms that prefer a single file with all rules, see `AGENTS.md` — a compiled version of all rule files in this Skill.
