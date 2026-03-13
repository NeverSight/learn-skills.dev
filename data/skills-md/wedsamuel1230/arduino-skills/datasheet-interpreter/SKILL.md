---
name: datasheet-interpreter
description: Extracts key specifications from component datasheet PDFs for maker projects. Use when user shares a datasheet PDF URL, asks about component specs, needs pin assignments, I2C addresses, timing requirements, or register maps. Downloads and parses PDF to extract essentials. Complements datasheet-parser for quick lookups.
---

# Datasheet Interpreter

Extracts actionable specifications from component datasheet PDFs.

## Resources

### Scripts
- **scripts/extract_specs.py** - Downloads datasheet PDFs from URLs and extracts specs using pattern matching

### References  
- **references/common-parameters.md** - Guide to understanding datasheet parameters

### Quick Start
```bash
# Extract specs from a datasheet URL
uv run --no-project scripts/extract_specs.py --url "https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf"

# Extract specs with markdown output
uv run --no-project scripts/extract_specs.py --url "https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf" --format markdown

# Extract from local PDF file
uv run --no-project scripts/extract_specs.py --file "local_datasheet.pdf"

# Interactive mode
uv run --no-project scripts/extract_specs.py --interactive
```

---

## When to Use
- "What's the I2C address for this chip?"
- "How do I connect this sensor?"
- "What pins do what on this module?"
- User shares a PDF datasheet URL
- Need timing specs or register info
- Quick reference without full driver generation

## Relationship to Other Skills
- **datasheet-parser**: Full driver library generation (lexus2k-style)
- **datasheet-interpreter** (this): Quick spec extraction for immediate use

---

## Information Extraction Workflow

### Step 1: Request Datasheet

```
Please provide:
1. Component name (e.g., "BME280", "MPU6050")
2. Datasheet PDF file or URL (manufacturer version preferred)
3. What specific information you need:
   □ Pin assignments / pinout
   □ I2C/SPI address and protocol
   □ Operating conditions (voltage, current)
   □ Timing requirements
   □ Register map
   □ Example circuit
   □ All of the above
```

### Step 2: Validate PDF Quality

**Check For:**
- Searchable text (not scanned image)
- Official manufacturer datasheet (not clone/distributor summary)
- Revision/version number noted
- Complete document (includes register tables if applicable)

**If PDF Issues:**
```
⚠️ This appears to be a [scanned image | partial datasheet | third-party summary].

For best results, please provide the official manufacturer datasheet from:
- [Manufacturer website link]
- Or search: "[component] datasheet pdf site:manufacturer.com"
```

---

## Extraction Templates

### Quick Reference Card

Generate this for any component:

```markdown
# [Component Name] Quick Reference

## Basic Info
- **Manufacturer:** [name]
- **Part Number:** [full part number with variants]
- **Datasheet Version:** [rev/date]
- **Description:** [one-line description]

## Electrical Characteristics
| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| Supply Voltage (VDD) | | | | V |
| Operating Current | | | | mA |
| Sleep Current | | | | µA |
| Operating Temp | | | | °C |

## Communication Interface
- **Protocol:** [I2C / SPI / UART / GPIO]
- **Address:** [0xNN (7-bit)] or [selectable via pin]
- **Max Clock:** [frequency]
- **Logic Levels:** [3.3V / 5V tolerant]

## Pinout
| Pin | Name | Type | Description |
|-----|------|------|-------------|
| 1 | VDD | Power | Supply voltage |
| 2 | GND | Power | Ground |
| ... | ... | ... | ... |

## Key Registers (if applicable)
| Address | Name | R/W | Description |
|---------|------|-----|-------------|
| 0x00 | WHO_AM_I | R | Device ID (expect 0xNN) |
| ... | ... | ... | ... |

## Arduino Wiring
| Component Pin | Arduino Uno | ESP32 | Pico |
|---------------|-------------|-------|------|
| VCC | 3.3V | 3.3V | 3V3 |
| GND | GND | GND | GND |
| SDA | A4 | GPIO21 | GP4 |
| SCL | A5 | GPIO22 | GP5 |

## Important Notes
- [Critical warnings from datasheet]
- [Application notes]
```

---

## Common Component Categories

### I2C Sensors

**Extract:**
```
□ I2C address (7-bit format, note if configurable)
□ WHO_AM_I register address and expected value
□ Configuration register settings
□ Data registers (where to read measurements)
□ Resolution and range options
□ Conversion time / measurement rate
```

**I2C Address Quick Reference:**
| Component | Address (7-bit) | Config Pin | Alt Address |
|-----------|-----------------|------------|-------------|
| BME280 | 0x76 | SDO→GND | 0x77 (SDO→VDD) |
| BME680 | 0x76 | SDO→GND | 0x77 (SDO→VDD) |
| MPU6050 | 0x68 | AD0→GND | 0x69 (AD0→VDD) |
| SHT30 | 0x44 | ADDR→GND | 0x45 (ADDR→VDD) |
| BH1750 | 0x23 | ADDR→GND | 0x5C (ADDR→VDD) |
| VL53L0X | 0x29 | - | Configurable via software |
| INA219 | 0x40 | A0,A1 | 0x40-0x4F |
| ADS1115 | 0x48 | ADDR→GND | 0x49-0x4B |

### SPI Devices

**Extract:**
```
□ SPI mode (CPOL, CPHA)
□ Max clock frequency
□ Data order (MSB/LSB first)
□ Command format
□ Chip select behavior (active low?)
```

### Motor Drivers

**Extract:**
```
□ Logic voltage (VCC)
□ Motor voltage range (VM)
□ Current per channel (continuous/peak)
□ Control interface (PWM frequency, step/dir)
□ Protection features (thermal, overcurrent)
□ H-bridge or half-bridge
```

### Display Modules

**Extract:**
```
□ Resolution (width x height)
□ Controller IC (SSD1306, ILI9341, etc.)
□ Interface (I2C, SPI, parallel)
□ Memory map / pixel format
□ Initialization sequence
□ Refresh rate
```

---

## Critical Spec Finder

### For Power Planning
```
Search datasheet for:
- "Electrical Characteristics" table
- "Power Consumption" or "Current Consumption"
- "Typical Operating Conditions"
- Sleep/standby modes and their currents
```

**Template Output:**
```markdown
## Power Specs for [Component]

### Operating Modes
| Mode | Typical Current | Conditions |
|------|-----------------|------------|
| Active | XXX mA | [freq, voltage, etc.] |
| Idle | XXX µA | |
| Sleep/Standby | XXX µA | |
| Deep Sleep | XXX nA | |

### Wake-up Time
- From sleep: XXX ms
- From deep sleep: XXX ms
```

### For Timing Requirements
```
Search datasheet for:
- "Timing Characteristics"
- "AC Characteristics"
- Setup/hold times
- Clock specifications
```

### For Pin Tolerance
```
Search datasheet for:
- "Absolute Maximum Ratings"
- "ESD protection"
- "5V tolerant" mentions
- Input voltage specifications
```

---

## Register Map Extraction

### Structured Format
```cpp
// [Component] Register Definitions
// Extracted from datasheet v[X.Y], p.[N]

// === REGISTER ADDRESSES ===
#define REG_NAME          0x00  // Description

// === BITFIELD DEFINITIONS ===
// REG_NAME (0x00) - [Description]
// Bit 7-6: FIELD_A - [description]
// Bit 5:   FIELD_B - [description]
// Bit 4-0: FIELD_C - [description]

#define REG_NAME_FIELD_A_MASK    0xC0
#define REG_NAME_FIELD_A_POS     6
#define REG_NAME_FIELD_B_BIT     5
#define REG_NAME_FIELD_C_MASK    0x1F
```

### Common Register Patterns

**Configuration Register:**
```
- Enable/disable features
- Set operating mode
- Configure interrupt behavior
```

**Status Register:**
```
- Data ready flags
- Error/fault indicators
- Interrupt sources
```

**Data Registers:**
```
- Usually consecutive addresses
- Note byte order (MSB first or LSB first)
- Signed vs unsigned interpretation
```

---

## Wiring Diagram Generator

Generate text-based wiring diagrams:

```
  [Component]          [Arduino Uno]
  ┌─────────┐         ┌───────────┐
  │ VCC ────┼─────────┤ 3.3V      │
  │ GND ────┼─────────┤ GND       │
  │ SDA ────┼─────────┤ A4 (SDA)  │
  │ SCL ────┼─────────┤ A5 (SCL)  │
  │ INT ────┼─────────┤ D2 (INT0) │
  └─────────┘         └───────────┘
  
  Notes:
  - Add 4.7kΩ pull-ups on SDA/SCL if not on module
  - INT is open-drain, needs pull-up
```

---

## Example Code Generator

Based on extracted specs, generate minimal working example:

```cpp
/*
 * [Component] Basic Example
 * Generated from datasheet interpretation
 * 
 * Wiring:
 * - VCC → 3.3V
 * - GND → GND
 * - SDA → A4 (Arduino Uno) / GPIO21 (ESP32)
 * - SCL → A5 (Arduino Uno) / GPIO22 (ESP32)
 */

#include <Wire.h>

#define COMPONENT_ADDR  0x00  // From datasheet p.X
#define REG_WHO_AM_I    0x00  // Expected: 0xNN
#define REG_CTRL        0x00  // Configuration
#define REG_DATA        0x00  // Data output

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  // Verify communication
  Wire.beginTransmission(COMPONENT_ADDR);
  if (Wire.endTransmission() != 0) {
    Serial.println("Component not found!");
    while(1);
  }
  
  // Read device ID
  uint8_t id = readReg(REG_WHO_AM_I);
  Serial.print("Device ID: 0x");
  Serial.println(id, HEX);
  
  // Initialize
  writeReg(REG_CTRL, 0x00);  // [Configuration value from datasheet]
}

void loop() {
  // Read data
  int16_t data = readReg16(REG_DATA);
  Serial.println(data);
  delay(100);
}

uint8_t readReg(uint8_t reg) {
  Wire.beginTransmission(COMPONENT_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(COMPONENT_ADDR, (uint8_t)1);
  return Wire.read();
}

void writeReg(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(COMPONENT_ADDR);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

int16_t readReg16(uint8_t reg) {
  Wire.beginTransmission(COMPONENT_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(COMPONENT_ADDR, (uint8_t)2);
  int16_t val = Wire.read() << 8;  // MSB first (check datasheet!)
  val |= Wire.read();
  return val;
}
```

---

## Quick Lookup Database

### Common Questions Answered

**"What voltage does [component] need?"**
→ Check "Absolute Maximum Ratings" and "Recommended Operating Conditions"

**"Is it 3.3V or 5V?"**
→ Look for "VDD" or "VCC" in electrical characteristics
→ Check if I/O pins are "5V tolerant"

**"How fast can I run the I2C?"**
→ Find "I2C Clock Frequency" in timing specs (usually 100kHz standard, 400kHz fast)

**"How do I wake it from sleep?"**
→ Look for "Power Management" or "Operating Modes" section

**"Why won't it respond at the address I expected?"**
→ Check address selection pins (AD0, ADDR, SA0)
→ Some datasheets show 8-bit address (divide by 2 for 7-bit)

---

## Datasheet Reading Tips

### Where to Find Key Info

| Information | Section Name |
|-------------|--------------|
| I2C Address | "Serial Interface" or "Communication" |
| Voltage/Current | "Electrical Characteristics" |
| Pinout | "Pin Configuration" or "Package Information" |
| Registers | "Register Map" or "Memory Map" |
| Timing | "Timing Characteristics" or "AC Characteristics" |
| Example Circuit | "Application Information" or "Typical Application" |

### Red Flags in Datasheets

- 🚩 Missing absolute maximum ratings
- 🚩 No version/revision number
- 🚩 Inconsistent register descriptions
- 🚩 Machine-translated text
- 🚩 Missing timing diagrams for protocols

→ If you see these, try to find a better quality datasheet from the original manufacturer
