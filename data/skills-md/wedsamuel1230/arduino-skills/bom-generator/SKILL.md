---
name: bom-generator
description: Generates Bill of Materials (BOM) from project descriptions for Arduino/ESP32/RP2040 projects. Use when user needs component lists, parts shopping lists, cost estimates, or asks "what parts do I need". Outputs formatted BOMs with part numbers, quantities, suppliers (DigiKey, Mouser, Amazon, AliExpress), and compatibility warnings. Run scripts/generate_bom.py for xlsx/csv export.
---

# BOM Generator

Creates comprehensive Bill of Materials for maker projects with supplier links and compatibility checks.

## Resources

- **scripts/generate_bom.py** - Python script for xlsx/csv/markdown BOM generation (requires openpyxl)
- **references/example-bom.md** - Complete example BOM
- **assets/example-project.json** - Sample project configuration for script

## Quick Start

Generate BOM interactively:
```bash
uv run --no-project scripts/generate_bom.py --interactive
```

Generate from JSON configuration:
```bash
uv run --no-project scripts/generate_bom.py --json assets/example-project.json --output bom.xlsx
```

List component database:
```bash
uv run --no-project scripts/generate_bom.py --list
```

Export formats: xlsx (default), csv, md, json

## When to Use
- User describes a project and needs parts list
- User asks "what components do I need for X"
- User wants to order parts for a design
- User needs cost estimates

## Workflow

### Step 1: Gather Project Requirements

Ask user for:
```
1. Project description (what does it do?)
2. Target microcontroller (Arduino UNO/Nano/Mega, ESP32, RP2040)
3. Power source (USB, batteries, wall adapter)
4. Quantity (how many units to build?)
5. Budget constraints (optional)
6. Supplier preference (optional)
```

### Step 2: Generate BOM

Run `scripts/generate_bom.py --interactive` for guided generation, or use this template format:

```markdown
# Bill of Materials: [Project Name]

**Generated:** [Date]
**Target Board:** [MCU]
**Quantity:** [N] unit(s)
**Estimated Total:** $[X.XX] - $[Y.YY] (per unit)

## Core Components

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 1 | [MCU Board] | [specs] | $X.XX | [DigiKey](#) / [Amazon](#) |
| ... | ... | ... | ... | ... |

## Sensors & Input

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| ... | ... | ... | ... | ... |

## Output Devices

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| ... | ... | ... | ... | ... |

## Power Components

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| ... | ... | ... | ... | ... |

## Passive Components

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| ... | ... | ... | ... | ... |

## Mechanical & Connectors

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| ... | ... | ... | ... | ... |

## Tools Required (if not owned)
- [ ] Tool 1
- [ ] Tool 2

## Compatibility Warnings
⚠️ [Any voltage/current/timing concerns]

## Substitution Notes
💡 [Alternative components if primary unavailable]
```

## Component Database

### Microcontrollers

| Board | Voltage | GPIO | Flash | Price Range | Best For |
|-------|---------|------|-------|-------------|----------|
| Arduino UNO R3 | 5V | 14 | 32KB | $12-25 | Beginners, most tutorials |
| Arduino Nano | 5V | 14 | 32KB | $3-20 | Compact projects |
| Arduino Mega | 5V | 54 | 256KB | $15-40 | Many I/O, large programs |
| ESP32 DevKit | 3.3V | 34 | 4MB | $5-15 | WiFi, Bluetooth, IoT |
| ESP32-C3 | 3.3V | 22 | 4MB | $4-10 | Low-cost WiFi |
| RP2040 Pico | 3.3V | 26 | 2MB | $4-6 | Dual-core, PIO |
| RP2040 Pico W | 3.3V | 26 | 2MB | $6-8 | Pico + WiFi |

### Common Sensors

| Sensor | Interface | Voltage | Price | Use Case |
|--------|-----------|---------|-------|----------|
| DHT22/AM2302 | 1-Wire | 3.3-5V | $3-8 | Temperature + humidity |
| BME280 | I2C/SPI | 3.3V | $5-15 | Temp + humidity + pressure |
| BMP280 | I2C/SPI | 3.3V | $2-8 | Temp + pressure (no humidity) |
| DS18B20 | 1-Wire | 3-5.5V | $2-5 | Waterproof temperature |
| HC-SR04 | GPIO | 5V | $1-3 | Ultrasonic distance |
| VL53L0X | I2C | 3.3V | $5-12 | Laser distance (accurate) |
| MPU6050 | I2C | 3.3V | $2-8 | Accelerometer + gyroscope |
| BNO055 | I2C | 3.3V | $25-35 | 9-DOF IMU (best accuracy) |
| VEML7700 | I2C | 3.3V | $4-8 | Ambient light (lux) |
| MAX30102 | I2C | 3.3V | $5-12 | Heart rate + SpO2 |

### Displays

| Display | Interface | Resolution | Price | Notes |
|---------|-----------|------------|-------|-------|
| 16x2 LCD | I2C | 16 chars | $3-8 | Need I2C backpack |
| 20x4 LCD | I2C | 20 chars | $5-12 | Larger text display |
| SSD1306 OLED | I2C | 128x64 | $3-8 | Sharp, no backlight needed |
| SSD1306 OLED | I2C | 128x32 | $3-6 | Compact OLED |
| ST7735 TFT | SPI | 128x160 | $5-10 | Color, fast refresh |
| ILI9341 TFT | SPI | 240x320 | $8-15 | Larger color display |
| E-Paper | SPI | Various | $15-40 | Low power, no refresh |

### Motors & Actuators

| Type | Driver Needed | Price | Notes |
|------|---------------|-------|-------|
| SG90 Servo | None (PWM) | $2-5 | 180°, weak torque |
| MG996R Servo | None (PWM) | $5-10 | Strong, metal gears |
| 28BYJ-48 Stepper | ULN2003 | $3-6 | Cheap, slow, weak |
| NEMA17 Stepper | A4988/DRV8825 | $8-15 | Strong, precise |
| DC Motor + Gearbox | L298N/TB6612 | $5-15 | High speed available |
| Linear Actuator | L298N | $15-40 | Push/pull motion |

### Motor Drivers

| Driver | Channels | Max Current | Voltage | Price |
|--------|----------|-------------|---------|-------|
| L298N | 2 | 2A/ch | 5-35V | $3-8 |
| TB6612FNG | 2 | 1.2A/ch | 4.5-13.5V | $3-8 |
| A4988 | 1 stepper | 2A | 8-35V | $2-5 |
| DRV8825 | 1 stepper | 2.5A | 8.2-45V | $3-6 |
| TMC2209 | 1 stepper | 2A | 4.75-28V | $8-15 |

### Power Components

| Component | Specs | Price | Use Case |
|-----------|-------|-------|----------|
| LM7805 | 5V 1A linear | $0.50 | Simple 5V reg |
| AMS1117-3.3 | 3.3V 1A linear | $0.30 | 3.3V from 5V |
| LM2596 Module | Adj. 3A buck | $2-4 | Efficient step-down |
| MT3608 Module | Adj. 2A boost | $1-3 | Step-up voltage |
| TP4056 Module | LiPo charger | $1-2 | Battery charging |
| 18650 Holder | 1-4 cells | $1-5 | Battery mounting |
| JST Connectors | 2-pin | $2-5/10pk | Battery connections |

### Passive Components (Buy Kits!)

| Kit Type | Typical Contents | Price | Recommendation |
|----------|------------------|-------|----------------|
| Resistor Kit | 600+ pcs, 1/4W | $8-15 | Get once, use forever |
| Capacitor Kit | Ceramic + electrolytic | $10-20 | Essential |
| LED Kit | 5mm various colors | $5-10 | Common needs |
| Button Kit | Tactile switches | $5-8 | Various sizes |
| Diode Kit | 1N4148, 1N4007, etc | $5-8 | Protection circuits |

## Supplier Guide

### Speed vs Cost Trade-offs

| Supplier | Shipping | Price | Best For |
|----------|----------|-------|----------|
| **DigiKey** | 1-3 days | $$$ | Precise specs, datasheets, urgent |
| **Mouser** | 1-3 days | $$$ | Wide selection, quality |
| **Amazon** | 1-2 days | $$ | Quick delivery, returns easy |
| **Adafruit** | 3-5 days | $$$ | Quality, tutorials, support |
| **SparkFun** | 3-5 days | $$$ | Breakout boards, learning |
| **AliExpress** | 2-6 weeks | $ | Bulk, budget, clones |
| **LCSC** | 1-2 weeks | $$ | Chinese components, good quality |

### Part Number Patterns

```
DigiKey: Descriptive codes
  - 1N4007-TP → 1N4007 diode
  - SER0006 → Servo motor

Mouser: Manufacturer part numbers
  - Search by exact MPN

Amazon: ASIN codes
  - Search by product name + specs

AliExpress: Store + product ID
  - Check reviews, sold count
```

## Compatibility Checks

### Voltage Level Matrix

```
                     Can Connect To:
From:        3.3V Logic    5V Logic
─────────────────────────────────────
3.3V MCU     ✅ Direct     ⚠️ Level shifter
5V MCU       ⚠️ Divider    ✅ Direct
3.3V Sensor  ✅ Direct     ⚠️ May work*
5V Sensor    ❌ Damage!    ✅ Direct

* Some 3.3V sensors are 5V tolerant - check datasheet
```

### Current Budget Check

```
Source Limits:
- Arduino 5V pin: 500mA max (from USB)
- Arduino GPIO: 40mA max per pin
- ESP32 3.3V: 500mA max
- ESP32 GPIO: 40mA max
- RP2040 GPIO: 16mA max

Always calculate:
Total current = Σ(component currents)
If total > source limit → external power needed
```

### I2C Address Conflicts

Common I2C addresses to watch:
```
0x3C - SSD1306 OLED
0x27 - PCF8574 LCD backpack  
0x3F - PCF8574A LCD backpack
0x68 - MPU6050, DS3231 RTC
0x76 - BME280 (default)
0x77 - BME280 (alternate), BMP280
0x48 - ADS1115 ADC
0x50 - AT24C32 EEPROM
```

## Output Format Options

### Markdown Table (Default)
Best for documentation, GitHub READMEs.

### CSV Export
```csv
Qty,Component,Specifications,Unit Price,Total,Supplier,Link
1,Arduino UNO R3,ATmega328P,15.00,15.00,Amazon,https://...
```

### Shopping Cart Links
Provide direct "Add to Cart" links where possible.

## Example BOM Output

See [references/example-bom.md](references/example-bom.md) for complete example.
