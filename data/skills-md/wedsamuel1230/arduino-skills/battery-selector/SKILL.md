---
name: battery-selector
description: Helps choose the right battery type and charging solution for Arduino/ESP32/RP2040 projects. Use when user asks about battery options, charging circuits, power source selection, or says "what battery should I use". Covers chemistry selection, safety, voltage regulation, and charging circuits.
---

# Battery Selector

Guides battery chemistry and charging circuit selection for embedded projects.

## Resources

This skill includes bundled tools and references:

- **scripts/compare_batteries.py** - Battery comparison calculator with 15+ battery types
- **references/safety-guidelines.md** - Comprehensive safety guide for all chemistries

## Quick Start

**Interactive selection:**
```bash
uv run --no-project scripts/compare_batteries.py --interactive
```

**Command line:**
```bash
# Find battery for 50mA project, 24h runtime
uv run --no-project scripts/compare_batteries.py --current 50 --hours 24

# Require rechargeable
uv run --no-project scripts/compare_batteries.py --current 100 --hours 12 --rechargeable

# List all batteries in database
uv run --no-project scripts/compare_batteries.py --list
```

## When to Use
- "What battery should I use?"
- "How do I charge this project?"
- "Lithium vs alkaline?"
- "Is this battery safe?"
- Planning portable/battery-powered projects

## Decision Flowchart

```
START
  │
  ▼
Is project rechargeable? ──No──► Alkaline/Lithium Primary
  │                              (Disposable batteries)
  Yes
  │
  ▼
What voltage does MCU need?
  │
  ├── 5V ──► LiPo + Boost converter
  │          OR 3x/4x NiMH
  │
  ├── 3.3V ──► Single LiPo (3.0-4.2V)
  │            Directly compatible!
  │
  └── 12V+ ──► Multi-cell LiPo pack
               OR Lead-acid
  │
  ▼
How much current?
  │
  ├── <50mA ──► Small LiPo (500-1000mAh)
  │             OR Coin cell (CR2032)
  │
  ├── 50-500mA ──► Standard LiPo (1000-3000mAh)
  │                OR 18650 cells
  │
  └── >500mA ──► Large LiPo (3000mAh+)
               OR Multiple 18650s
               External power recommended
```

## Battery Chemistry Comparison

### Quick Reference

| Chemistry | Voltage | Rechargeable | Energy Density | Cost | Safety |
|-----------|---------|--------------|----------------|------|--------|
| Alkaline | 1.5V/cell | No | Medium | Low | Very safe |
| Lithium Primary | 3V | No | High | Medium | Safe |
| NiMH | 1.2V/cell | Yes | Medium | Medium | Safe |
| LiPo/Li-ion | 3.7V | Yes | Very High | Medium | ⚠️ Needs care |
| LiFePO4 | 3.2V | Yes | High | High | Safer than LiPo |
| Lead-acid | 2V/cell | Yes | Low | Low | ⚠️ Acid hazard |

### Alkaline (AA/AAA/9V)

**Pros:**
- Cheap, available everywhere
- No charging circuit needed
- Very safe
- Long shelf life (5-10 years)

**Cons:**
- Not rechargeable (e-waste!)
- Voltage drops as discharged
- Poor at high current
- Heavy for capacity

**Best For:**
- Low-power projects (<20mA average)
- Beginner projects
- Remote/deployment where charging impractical
- Backup power

**Voltage Configurations:**
```
Cells   Voltage    Use With
────────────────────────────
2x AA   3.0V       3.3V MCUs (with LDO)
3x AA   4.5V       5V MCUs (direct or LDO)
4x AA   6.0V       5V MCUs (with regulator)
9V      9.0V       With 5V/3.3V regulator
```

---

### NiMH (AA/AAA Rechargeable)

**Pros:**
- Rechargeable (500-1000 cycles)
- Same size as alkaline
- Safer than lithium
- No memory effect

**Cons:**
- Lower voltage (1.2V vs 1.5V)
- Self-discharge (~20%/month)
- Need proper charger
- Heavier than LiPo

**Best For:**
- Projects replacing disposable batteries
- Educational settings
- Where LiPo is too risky
- Budget rechargeable solution

**Charging:**
- Use dedicated NiMH charger
- Don't mix brands/capacities
- Eneloop/Eneloop Pro recommended

---

### LiPo / Li-ion (3.7V)

**Pros:**
- High energy density (light + powerful)
- Rechargeable (300-500 cycles)
- Flat discharge curve
- Many form factors

**Cons:**
- ⚠️ Fire risk if abused
- Needs protection circuit
- Temperature sensitive
- Ages even unused

**Best For:**
- Most portable projects
- Weight-sensitive applications
- When you need runtime
- Professional builds

**Critical Safety Rules:**
```
✅ DO:
- Use protected cells with BMS
- Store at 40-60% charge
- Use proper TP4056/similar charger
- Monitor temperature during charge
- Use battery with JST-PH connector (prevents polarity swap)

❌ DON'T:
- Puncture, crush, or bend
- Charge below 0°C
- Discharge below 3.0V
- Leave charging unattended (first few times)
- Use damaged/puffy batteries
```

---

### LiFePO4 (3.2V)

**Pros:**
- Much safer than LiPo (no thermal runaway)
- Longer cycle life (2000+ cycles)
- Flat discharge curve
- Tolerates abuse better

**Cons:**
- Lower energy density
- Lower voltage (may need boost)
- More expensive
- Less common in small sizes

**Best For:**
- Safety-critical applications
- Outdoor/rugged deployments
- Long-term installations
- When LiPo risk unacceptable

---

### CR2032 / Coin Cells

**Pros:**
- Tiny and light
- Long shelf life
- 3V output (direct to 3.3V MCU)

**Cons:**
- Very low capacity (220mAh)
- Poor high-current performance
- Not rechargeable
- ⚠️ Danger if swallowed

**Best For:**
- Ultra-low power only (<10µA average)
- RTC backup
- Tiny sensors
- Keyfobs, beacons

**Current Limits:**
```
Continuous: <2mA
Pulse: <15mA (brief)

DON'T use for: WiFi, Bluetooth, motors, LEDs
```

---

## Voltage Regulation

### 3.3V Systems (ESP32, RP2040)

**Single LiPo → 3.3V:**
```
LiPo outputs 3.0-4.2V
Most 3.3V MCUs tolerate this range directly!

Option 1: Direct connection (if MCU allows)
   LiPo(+) → 3.3V/VIN pin
   
Option 2: LDO for clean 3.3V
   LiPo(+) → [AMS1117-3.3] → 3.3V pin
   (Need 4V min input for AMS1117)

Better: Use HT7333 LDO (low dropout, low quiescent)
   Works from 3.3V input!
```

### 5V Systems (Arduino UNO/Nano)

**LiPo → 5V:**
```
Option 1: Boost converter
   LiPo(+) → [MT3608] → 5V → VIN pin
   
Option 2: PowerBoost module (Adafruit)
   Includes charging + boost + protection
   
Option 3: USB power bank
   Already regulated 5V + charging built-in
```

---

## Charging Solutions

### TP4056 Module (Most Popular)

```
┌─────────────────────────────┐
│  TP4056 with Protection     │
│                             │
│  [USB-C] ─► [TP4056] ─► [DW01+FS8205] ─► [B+/B-]
│   IN         Charger     Protection      To Battery
│                             │
│  Features:                  │
│  - 1A max charge current    │
│  - Overcharge protection    │
│  - Overdischarge protect    │
│  - Short circuit protect    │
│  - LED charge indicator     │
└─────────────────────────────┘

Wiring:
  B+ → LiPo positive
  B- → LiPo negative
  OUT+ → Load/MCU positive
  OUT- → Load/MCU negative
```

**⚠️ Get module WITH protection (6 pins, not 4 pins)**

### Adafruit PowerBoost 500C/1000C

Premium solution with:
- LiPo charging via USB
- 5V boost output (500mA or 1A)
- Low battery indicator
- Load sharing (charge while running)

### DIY Charging Don'ts
```
❌ Never charge LiPo with a constant voltage supply
❌ Never charge LiPo with a phone charger directly
❌ Never charge at >1C rate (e.g., 1000mAh → max 1A)
❌ Never charge frozen batteries
```

---

## Battery Sizing Calculator

```
Step 1: Determine average current (from power-budget-calculator)
        I_avg = _____ mA

Step 2: Determine required runtime
        T_required = _____ hours

Step 3: Calculate minimum capacity
        C_min = I_avg × T_required × 1.25 (safety factor)
        C_min = _____ × _____ × 1.25
        C_min = _____ mAh

Step 4: Select battery
        Choose capacity ≥ C_min
        Consider: size, weight, form factor
```

**Example:**
```
Project: Weather station
I_avg: 15mA
T_required: 48 hours (2 days between charges)

C_min = 15 × 48 × 1.25 = 900mAh

Selection: 1000mAh LiPo (gives ~67 hours actual)
```

---

## Common Mistakes

### 1. Using Wrong Charger
```
❌ "My 9V adapter should work"
   LiPo needs CC-CV charging at 4.2V max!
   
✅ Use TP4056 or dedicated LiPo charger
```

### 2. No Low-Voltage Cutoff
```
❌ Draining LiPo below 3.0V
   Permanently damages the cell!
   
✅ Use protection module OR monitor in code:
   if (batteryVoltage < 3.2) {
       enterDeepSleep();  // Protect battery
   }
```

### 3. Ignoring Inrush Current
```
❌ Battery can't handle WiFi TX spike (500mA)
   Causes brownout/reset
   
✅ Add 100-470µF capacitor near MCU
✅ Size battery for peak current, not just average
```

### 4. No Reverse Polarity Protection
```
❌ Swapping battery wires = magic smoke

✅ Use JST-PH connectors (keyed)
✅ Add protection diode or P-FET
```

---

## Recommended Setups by Project Type

### Low-Power Sensor Node
```
Battery: 18650 (3000mAh) or LiPo 2000mAh
MCU: ESP32 with deep sleep
Charger: TP4056 with protection
Runtime: Weeks to months
```

### Handheld Device
```
Battery: LiPo 1000-2000mAh flat pack
MCU: Any
Charger: PowerBoost or TP4056 + boost
Runtime: Hours to days
```

### Robot/High Current
```
Battery: 2S or 3S LiPo pack (7.4V or 11.1V)
Regulator: Buck converter to 5V
Charger: Balance charger (external)
Runtime: Minutes to hours
```

### Ultra-Low Power Beacon
```
Battery: CR2032 or 2x AA
MCU: ESP32-C3 or ATtiny with deep sleep
No charger needed
Runtime: Months to years
```

## Quick Selection Table

| Project Type | Best Battery | Capacity | Charger |
|--------------|--------------|----------|---------|
| Simple Arduino | 4x AA | 2500mAh | None |
| ESP32 portable | 18650 | 2600mAh | TP4056 |
| Wearable | Small LiPo | 500mAh | TP4056 |
| Robot | 2S LiPo | 2200mAh | Balance |
| Ultra-low power | CR2032 | 220mAh | None |
| Solar project | LiFePO4 | 3200mAh | MPPT |
