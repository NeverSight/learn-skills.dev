---
name: enclosure-designer
description: Guides design and generation of 3D-printable enclosures for Arduino/ESP32/RP2040 projects. Use when user needs a case, box, housing, or enclosure for their electronics project. Provides parametric design guidance, OpenSCAD templates, STL generation tips, and print settings.
---

# Enclosure Designer

Creates 3D-printable enclosures for electronics projects.

## Resources

This skill includes bundled tools and templates:

- **scripts/generate_enclosure.py** - Parametric OpenSCAD generator with PCB database
- **assets/basic-template.scad** - Customizable OpenSCAD template

## Quick Start

**Generate for specific PCB:**
```bash
uv run --no-project scripts/generate_enclosure.py --pcb "Arduino Uno" --output uno_case.scad
uv run --no-project scripts/generate_enclosure.py --pcb "ESP32 DevKit" --output esp32_case.scad
```

**Custom dimensions:**
```bash
uv run --no-project scripts/generate_enclosure.py --width 100 --depth 60 --height 30 --output custom.scad
```

**Interactive mode:**
```bash
uv run --no-project scripts/generate_enclosure.py --interactive
```

**List supported PCBs:**
```bash
uv run --no-project scripts/generate_enclosure.py --list
```

## When to Use
- "I need a case for my project"
- "How do I make an enclosure?"
- "Design a box for my Arduino"
- User has working circuit, needs housing
- Preparing for deployment/presentation

## Design Workflow

### Step 1: Gather Measurements

Ask user for:
```
1. Main board dimensions (L × W × H in mm)
2. Component clearances (tallest component height)
3. Connectors/ports that need access (USB, power jack, etc.)
4. Mounting holes (positions, diameters)
5. Any displays, buttons, LEDs that need cutouts
6. Environment (indoor/outdoor, waterproof?)
```

### Step 2: Design Parameters

```
Enclosure Type: [Box/Clamshell/Snap-fit/Screw-mount]
Material: [PLA/PETG/ABS]
Wall Thickness: [2-3mm typical]
Mounting Style: [Standoffs/Clips/Rails]
Ventilation: [None/Slots/Holes]
Access: [Top-remove/Front-panel/Side-openings]
```

### Step 3: Generate Design

Choose approach:
1. **Parametric OpenSCAD** - Full customization
2. **Pre-made generator** - Quick results
3. **Manual Fusion360/TinkerCAD** - Visual design

---

## Parametric OpenSCAD Template

### Basic Project Box

```openscad
// === PARAMETRIC PROJECT BOX ===
// Customize these values for your project

// Internal dimensions (mm)
inner_length = 70;    // X axis
inner_width = 50;     // Y axis  
inner_height = 30;    // Z axis (internal depth)

// Wall and tolerances
wall = 2.5;           // Wall thickness
lid_tolerance = 0.4;  // Gap for lid fit
corner_radius = 3;    // Rounded corners

// Mounting standoffs
standoff_height = 5;  // PCB clearance from bottom
standoff_dia = 6;     // Standoff outer diameter
screw_hole_dia = 2.5; // M2.5 screw hole

// PCB mounting hole positions (from corner)
// Measure from your board!
pcb_holes = [
    [5, 5],           // Bottom-left
    [65, 5],          // Bottom-right
    [5, 45],          // Top-left
    [65, 45]          // Top-right
];

// Lid attachment
lid_screw_dia = 3;    // M3 screws
lid_screw_positions = [
    [5, 5],
    [inner_length-5, 5],
    [5, inner_width-5],
    [inner_length-5, inner_width-5]
];

// Cutouts (add as needed)
usb_cutout = true;
usb_x = 35;           // Center position
usb_width = 12;
usb_height = 8;

// === MODULES ===

module rounded_box(l, w, h, r) {
    hull() {
        for (x = [r, l-r])
            for (y = [r, w-r])
                translate([x, y, 0])
                    cylinder(h=h, r=r, $fn=32);
    }
}

module standoff(h, outer_d, inner_d) {
    difference() {
        cylinder(h=h, d=outer_d, $fn=24);
        cylinder(h=h+1, d=inner_d, $fn=24);
    }
}

module box_base() {
    outer_l = inner_length + 2*wall;
    outer_w = inner_width + 2*wall;
    outer_h = inner_height + wall;  // Bottom wall
    
    difference() {
        // Outer shell
        rounded_box(outer_l, outer_w, outer_h, corner_radius);
        
        // Inner cavity
        translate([wall, wall, wall])
            rounded_box(inner_length, inner_width, inner_height+1, corner_radius-wall);
        
        // USB cutout
        if (usb_cutout) {
            translate([wall + usb_x - usb_width/2, -1, wall + standoff_height])
                cube([usb_width, wall+2, usb_height]);
        }
    }
    
    // Add standoffs
    for (pos = pcb_holes) {
        translate([wall + pos[0], wall + pos[1], wall])
            standoff(standoff_height, standoff_dia, screw_hole_dia);
    }
}

module box_lid() {
    lid_wall = wall - lid_tolerance;
    outer_l = inner_length + 2*wall;
    outer_w = inner_width + 2*wall;
    lip_h = 5;  // How deep lid inserts
    
    // Lid top
    rounded_box(outer_l, outer_w, wall, corner_radius);
    
    // Lid lip (inserts into box)
    translate([wall + lid_tolerance, wall + lid_tolerance, -lip_h])
        difference() {
            rounded_box(inner_length - 2*lid_tolerance, 
                       inner_width - 2*lid_tolerance, 
                       lip_h, corner_radius - wall);
        }
}

// === RENDER ===

// Uncomment one at a time for printing:
box_base();
// translate([0, inner_width + 20, 0]) box_lid();
```

### Adding Cutouts

```openscad
// === CUTOUT LIBRARY ===

// Round hole (for buttons, LEDs)
module round_cutout(x, y, z, diameter, depth) {
    translate([x, y, z])
        rotate([90, 0, 0])
            cylinder(h=depth, d=diameter, $fn=32);
}

// Rectangle (for displays, SD cards)
module rect_cutout(x, y, z, width, height, depth) {
    translate([x - width/2, -0.1, z])
        cube([width, depth + 0.2, height]);
}

// Slot (for ventilation, cables)
module slot_cutout(x, y, z, width, height, depth) {
    translate([x, y, z])
        hull() {
            translate([0, 0, 0])
                cylinder(h=depth, d=height, $fn=24);
            translate([width-height, 0, 0])
                cylinder(h=depth, d=height, $fn=24);
        }
}

// OLED display cutout (128x64 module)
module oled_cutout() {
    // Visible area
    rect_cutout(inner_length/2, wall, inner_height - 15, 26, 14, wall+1);
    // Mounting holes (if needed)
}

// Common connector dimensions
usb_micro = [8, 3];      // USB Micro
usb_c = [9, 3.5];        // USB-C
barrel_jack = [12, 12];  // 5.5mm DC jack (round)
sd_card = [15, 3];       // SD card slot
```

---

## Online Generators (No CAD Needed)

### Ultimate Box Maker (Thingiverse)
https://www.thingiverse.com/thing:1264391

Parameters:
- Enter internal dimensions
- Choose wall thickness
- Select lid type (snap/screw/slide)
- Add ventilation slots
- Download STL

### Parametric Box by Heartman
https://www.thingiverse.com/thing:1355018

Good for:
- Simple project boxes
- Snap-fit lids
- Basic customization

### FreeCAD + Parametric Enclosure
1. Install FreeCAD
2. Use Spreadsheet workbench for parameters
3. Generate enclosure with formulas
4. Export STL

---

## Common Board Dimensions

### Arduino Family
| Board | L × W × H (mm) | Mounting Holes |
|-------|----------------|----------------|
| UNO R3 | 68.6 × 53.4 × 15 | 4 holes, 3.2mm |
| Nano | 45 × 18 × 8 | 2 holes, 1.5mm |
| Mega 2560 | 101.5 × 53.4 × 15 | 4 holes, 3.2mm |
| Pro Mini | 33 × 18 × 5 | None standard |

### ESP32 Family
| Board | L × W × H (mm) | Mounting Holes |
|-------|----------------|----------------|
| DevKit V1 (38pin) | 55 × 28 × 10 | None (use clips) |
| DevKit V1 (30pin) | 49 × 26 × 10 | None |
| NodeMCU-32S | 51 × 25 × 10 | 2 holes, 3mm |
| ESP32-CAM | 40 × 27 × 12 | 2 holes, 2mm |

### Raspberry Pi Pico
| Board | L × W × H (mm) | Mounting Holes |
|-------|----------------|----------------|
| Pico/Pico W | 51 × 21 × 4 | 4 holes, 2.1mm |

### Common Modules
| Module | L × W × H (mm) | Notes |
|--------|----------------|-------|
| SSD1306 OLED 0.96" | 27 × 27 × 4 | 4 corners 2mm |
| BME280 | 15 × 12 × 3 | 2 holes 2mm |
| SD Card | 42 × 24 × 5 | 4 corners 2mm |
| TP4056 | 26 × 17 × 4 | None |
| 18650 holder | 77 × 21 × 19 | Varies |

---

## Design Guidelines

### Wall Thickness
```
Application              Thickness
─────────────────────────────────────
Desktop/indoor           2.0 mm
Portable/handheld        2.5 mm
Outdoor                  3.0 mm
Structural/load-bearing  4.0+ mm
```

### Clearances
```
Component           Add clearance
─────────────────────────────────────
PCB to wall         1-2 mm
USB/connector       0.5 mm extra per side
Moving parts        2-3 mm
Lid fit             0.3-0.5 mm gap
```

### Mounting Strategies

**PCB Standoffs:**
```
    [Standoff]──┐
        │       │
    [PCB]       │ standoff_height
        │       │
    ────────────┘
        ▲
     box_floor
```

**Edge Rails:**
```
    ┌────────────┐
    │    [PCB]   │
    │  ───────   │
    │ /       \  │  <-- Rails support PCB edges
    └───┘   └────┘
```

**Snap-in Clips:**
```
    ┌──╲   ╱──┐
    │   [PCB] │
    │  ───────│
    └─────────┘
        ▲
     Flexible clips
```

### Ventilation

**When needed:**
- MCU draws >100mA continuously
- Motor drivers
- Power regulators
- Any component getting warm

**Vent patterns:**
```
// Slot pattern (easy to print, good flow)
for (i = [0:5]) {
    translate([10 + i*8, wall/2, 10])
        slot_cutout(20, 3, wall+1);
}

// Honeycomb (looks cool, harder to print)
// Use pre-made pattern from Thingiverse
```

---

## Print Settings

### Material Selection

| Material | Pros | Cons | Best For |
|----------|------|------|----------|
| **PLA** | Easy to print, cheap | Weak to heat (>50°C) | Indoor projects |
| **PETG** | Heat resistant, strong | Stringing, harder | Outdoor, functional |
| **ABS** | Heat resistant, tough | Warps, fumes | Professional |
| **ASA** | UV resistant | Like ABS | Outdoor long-term |

### Recommended Settings

**PLA Enclosure:**
```
Layer height: 0.2mm
Wall count: 3-4 (for 2-3mm wall)
Infill: 15-20%
Support: Usually not needed if designed right
Bed temp: 60°C
Nozzle temp: 200-210°C
```

**PETG Enclosure:**
```
Layer height: 0.2mm
Wall count: 3-4
Infill: 20-25%
Support: Often needed
Bed temp: 80°C
Nozzle temp: 230-245°C
Print slower than PLA
```

### Orientation Tips

```
Print box BASE standing up (opening facing up)
- No supports needed
- Good surface finish inside
- Strong walls

Print LID flat (top surface down)
- Smooth exterior surface
- May need supports for cutouts
```

---

## Waterproofing

### IP Rating Guide
```
IP65 - Dust tight, water jets OK
IP67 - Dust tight, submersible briefly
IP68 - Dust tight, continuous submersion
```

### Strategies

**Rubber Gasket:**
```
Add groove in lid for O-ring:
    ┌───╔═══════╗───┐
    │   ║O-ring ║   │
    │   ╚═══════╝   │
    │    [box]      │
    └───────────────┘
```

**Cable Glands:**
- Use PG7/PG9 cable glands for wires
- Drill precise holes, thread in glands
- Seal with silicone if needed

**Conformal Coating:**
- Spray PCB with conformal coat
- Protects electronics inside box

---

## Example: ESP32 Weather Station Enclosure

```openscad
// ESP32 Weather Station Enclosure
// Components: ESP32 DevKit, BME280, SSD1306 OLED, 18650 battery

// Internal dimensions (measured from components + clearance)
inner_length = 80;
inner_width = 55;
inner_height = 50;  // Room for battery under PCB

wall = 3;  // Outdoor = thicker walls

// ESP32 on standoffs
esp_standoff_h = 25;  // Above battery
esp_holes = [[5, 5], [5, 50], [52, 5], [52, 50]];

// OLED window position (top of enclosure)
oled_x = 40;
oled_y = 15;
oled_w = 28;
oled_h = 16;

// BME280 vent hole
bme_vent_x = 70;
bme_vent_y = 30;
bme_vent_dia = 8;

// USB access
usb_x = 30;
usb_y = inner_height - 15;

// Generate with above parameters...
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Lid too tight | Tolerance too small | Increase to 0.5mm |
| Lid too loose | Tolerance too large | Decrease, add clips |
| Screws strip | Holes too large | Use proper thread inserts |
| Parts don't fit | Measurement error | Remeasure, print test piece |
| Weak walls | Too thin, low infill | Increase wall count |
| Warping | ABS, big flat surfaces | Use brim, enclosure, PETG |

---

## Resources

- **OpenSCAD**: https://openscad.org
- **Thingiverse Customizer**: Parametric designs
- **Printables**: More enclosure designs
- **McMaster-Carr**: Reference for hardware dimensions
