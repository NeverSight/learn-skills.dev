---
name: kicad-schematic
description: "Generate, validate, and fix KiCad 8 schematic files (.kicad_sch) programmatically. Use this skill whenever the user wants to create or modify KiCad schematics, generate netlists from circuit descriptions, or fix ERC errors. Triggers on: KiCad, schematic, .kicad_sch, ERC, electrical rules check, circuit design, PCB schematic, netlist generation, S-expression schematic."
---

# KiCad Schematic Agent

Generate ERC-clean KiCad 8 schematics by writing Python scripts that use computed pin positions — never guess coordinates.

## Critical Principle

**The #1 cause of broken schematics is guessed pin positions.** When connecting labels to IC pins, you MUST compute exact coordinates using the symbol definition's pin positions and the coordinate transform formula. The helper library in `scripts/kicad_sch_helpers.py` does this automatically.

### The Y-axis Trap (Most Common Bug)

Symbol libraries (.kicad_sym) use **Y-up** (math convention). Schematics (.kicad_sch) use **Y-down** (screen convention). This means you MUST negate the Y coordinate when transforming from library to schematic space. Forgetting this will place labels 10-50mm away from their pins, causing massive pin_not_connected and label_dangling errors.

**Transform formula** — pin at library (px, py), symbol placed at schematic (sx, sy) with rotation R:
- **Rotation 0**:   schematic position = (sx + px, sy **-** py)
- **Rotation 90**:  schematic position = (sx + py, sy + px)
- **Rotation 180**: schematic position = (sx - px, sy **+** py)
- **Rotation 270**: schematic position = (sx - py, sy - px)

Always use `pin_abs()` from the helper library — never compute these by hand.

## Architecture

```
User describes circuit
        |
Read symbol libraries (.kicad_sym) to get pin positions
        |
Build pin position dictionaries for every multi-pin IC
        |
Write Python script using SchematicBuilder (from helper library)
  - Use connect_pin() for IC pins (computes positions automatically)
  - Use place_2pin_vertical() for passives (knows pin 1/2 positions)
        |
Generate .kicad_sch file
        |
Post-process with fix_subsymbol_names()
        |
Run ERC validation: kicad-cli sch erc --format json
        |
Parse errors -> fix script -> regenerate -> repeat (max 5 iterations)
```

## Step-by-step Workflow

### 0. Ensure kicad-cli is Available

Before running any ERC validation, verify that `kicad-cli` is on the system PATH. Run:

```bash
which kicad-cli 2>/dev/null || where kicad-cli 2>/dev/null
```

If **not found**, check for a local KiCad installation and offer to create a symlink:

**macOS:**
```bash
# Check if KiCad is installed as an app
KICAD_CLI="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
if [ -f "$KICAD_CLI" ]; then
    echo "Found kicad-cli inside KiCad.app. Creating symlink..."
    sudo ln -sf "$KICAD_CLI" /usr/local/bin/kicad-cli
    echo "Done! kicad-cli is now available on PATH."
else
    echo "KiCad not found. Install from https://www.kicad.org/download/macos/"
fi
```

**Linux:**
```bash
# kicad-cli is typically installed alongside KiCad via package manager
# Check common locations
for p in /usr/bin/kicad-cli /usr/local/bin/kicad-cli /snap/kicad/current/bin/kicad-cli; do
    if [ -f "$p" ]; then
        echo "Found kicad-cli at $p"
        # If not on PATH, symlink it
        if ! command -v kicad-cli &>/dev/null; then
            sudo ln -sf "$p" /usr/local/bin/kicad-cli
        fi
        break
    fi
done
# If still not found:
# Ubuntu/Debian: sudo apt install kicad
# Fedora: sudo dnf install kicad
# Arch: sudo pacman -S kicad
# Or install from https://www.kicad.org/download/linux/
```

**Windows:**
```powershell
# Check standard install path
$kicadCli = "C:\Program Files\KiCad\8.0\bin\kicad-cli.exe"
if (Test-Path $kicadCli) {
    Write-Host "Found kicad-cli. Add to PATH:"
    Write-Host '  [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\Program Files\KiCad\8.0\bin", "User")'
} else {
    Write-Host "KiCad not found. Install from https://www.kicad.org/download/windows/"
}
```

Tell the user what you found and ask for confirmation before creating any symlinks. If kicad-cli is truly not installed, provide the download link for their OS and stop — ERC validation requires it.

### 1. Understand the Circuit

Before writing any code, gather:
- Component list with specific part numbers
- Power architecture (voltage rails, regulators)
- Signal connections (which pins connect to which)
- Symbol libraries needed (standard KiCad libs + any custom .kicad_sym files)

### 2. Read Symbol Libraries (NON-NEGOTIABLE)

For **every IC and multi-pin component**, read its .kicad_sym definition to get exact pin names, numbers, positions, and types. You cannot connect pins correctly without this data.

```python
from kicad_sch_helpers import SymbolLibrary

lib = SymbolLibrary()
lib.load_from_kicad_sym("path/to/library.kicad_sym")

# Now you know exact pin positions
ad9363 = lib.get("AD9363ABCZ")
for pin in ad9363.pins:
    print(f"{pin.name} ({pin.number}): at ({pin.x}, {pin.y}), type={pin.pin_type}")
```

**For manual/inline approaches**, build a pin dictionary from the library:
```python
# Extract from .kicad_sym file — these are LIBRARY coordinates (Y-up)
AD_PINS = {
    'TX1A_P': (-17.78, 25.40),
    'TX1A_N': (-17.78, 22.86),
    'SPI_CLK': (-17.78, -10.16),
    # ... all pins
}

# SOT-23-5 packages (common for LDOs like AP2112K, ME6211):
SOT5_PINS = {
    'VIN':  (-7.62,  2.54),   # Pin 1 - top left
    'GND':  ( 0.00, -7.62),   # Pin 2 - bottom center
    'EN':   (-7.62, -2.54),   # Pin 3 - bottom left
    'NC':   ( 7.62, -2.54),   # Pin 4 - bottom right  <- NOT VOUT!
    'VOUT': ( 7.62,  2.54),   # Pin 5 - top right     <- THIS is VOUT!
}
```

**WARNING — SOT-23-5 pin trap:** VOUT is at (7.62, **+2.54**) and NC is at (7.62, **-2.54**). These are only 5.08mm apart. Confusing them means your LDO output goes nowhere. Always verify from the actual library file.

### 3. Write the Generator Script

Use `SchematicBuilder` for all schematic construction. The key method is `connect_pin()` which computes exact pin positions automatically:

```python
from kicad_sch_helpers import SchematicBuilder, SymbolLibrary, snap

lib = SymbolLibrary()
lib.load_from_kicad_sym("custom_symbols.kicad_sym")

sch = SchematicBuilder(symbol_lib=lib, project_name="my_project")
sch.set_lib_symbols(lib_symbols_content)  # Raw S-expression for embedded symbols

# Place an IC
sch.place("CubeSat_SDR:AD9363ABCZ", "U1", "AD9363ABCZ",
          x=320, y=200, footprint="CubeSat_SDR:AD9363_BGA144")

# Connect pins by NAME — coordinates computed automatically
sch.connect_pin("U1", "TX1A_P", "TX1A_P", wire_dx=-5.08)
sch.connect_pin("U1", "SPI_CLK", "SPI_CLK", wire_dy=-5.08)
sch.connect_pin("U1", "GND", "GND", wire_dy=5.08)

# For unused pins, add no-connect flags
sch.connect_pin_noconnect("U1", "AUXDAC1")

# For 2-pin passives, use convenience helpers
from kicad_sch_helpers import place_2pin_vertical
place_2pin_vertical(sch, "Device:C", "C1", "100nF",
                    x=snap(230), y=snap(155),
                    top_net="VCC_3V3", bottom_net="GND",
                    footprint="Capacitor_SMD:C_0402_1005Metric")
```

**If using inline pin dictionaries** (without SymbolLibrary), use `pin_abs()`:
```python
from kicad_sch_helpers import pin_abs, snap

GRID = 1.27

def wl(sch, sx, sy, pin_name, pins_dict, net, dx=0, dy=0, rot=0, label_angle=0):
    """Wire + Label: connect an IC pin to a net label."""
    px, py = pin_abs(sx, sy, pins_dict[pin_name][0], pins_dict[pin_name][1], rot)
    ex, ey = snap(px + dx), snap(py + dy)
    if dx != 0 or dy != 0:
        sch.w(px, py, ex, ey)
    sch.label(net, ex, ey, label_angle)

# Usage:
wl(sch, 320, 200, 'TX1A_P', AD_PINS, "TX1A_P", dx=-7.62)
```

### 4. Handle the lib_symbols Section

Every symbol referenced must be embedded in the schematic's lib_symbols. Three critical rules:

1. **Parent symbols** use the full lib_id: `(symbol "Device:R" ...)`
2. **Sub-symbols** must NOT have the library prefix: `(symbol "R_0_1" ...)` not `(symbol "Device:R_0_1" ...)`
3. **Always post-process** with `fix_subsymbol_names()` to catch any mistakes

Use `fix_subsymbol_names()` as a post-processing step:
```python
from kicad_sch_helpers import fix_subsymbol_names

content = sch.build(title="My Schematic")
content = fix_subsymbol_names(content)
```

The regex-based fixer handles nested sub-symbols at any depth and any library prefix format.

### 5. Grid Snapping (Prevents 90% of Warnings)

**Every coordinate** in the schematic must be a multiple of 1.27mm. Use `snap()`:
```python
from kicad_sch_helpers import snap

# snap() rounds to nearest 1.27mm grid point
x = snap(123.45)  # -> 124.46 (nearest multiple of 1.27)
```

Apply `snap()` to: component positions, wire endpoints, label positions, no-connect positions, and PWR_FLAG positions. The `connect_pin()` and `pin_abs()` functions do this automatically.

### 6. Add PWR_FLAG Symbols

For every power net that originates from a voltage regulator (not a power symbol), add a PWR_FLAG to prevent "power_pin_not_driven" errors:

```python
# Define PWR_FLAG in lib_symbols (see references/kicad_sexpression_format.md)
# Then place on each power net:
sch.place_pwr_flag(x=70, y=78, net_name="VCC_3V3A")
```

**Rule of thumb**: If a net is driven by a component whose output pin type is `passive` (not `power_out`), that net needs a PWR_FLAG. This includes most LDO regulators.

Also place PWR_FLAG on GND nets that don't have a dedicated GND power symbol driving them.

### 7. No-Connect Flags

Every unused pin on every IC MUST have a no-connect flag. Missing no-connect flags cause `pin_not_connected` errors.

```python
# Using SchematicBuilder:
sch.connect_pin_noconnect("U1", "AUXDAC1")

# Or manually with pin_abs:
px, py = pin_abs(sx, sy, pin_x, pin_y, rotation)
sch.nc(px, py)
```

### 8. Validate with kicad-cli

```python
from kicad_sch_helpers import run_erc

result = run_erc("output/schematic.kicad_sch")
print(f"Errors: {result['errors']}, Warnings: {result['warnings']}")

if result['errors'] > 0:
    for detail in result['details']:
        if detail.get('severity') == 'error':
            print(f"  {detail['type']}: {detail.get('description', '')}")
```

### 9. Automated Fix Loop

For complex schematics, use the validation loop:

```python
from kicad_sch_helpers import validate_and_fix_loop

def my_fixer(erc_result, iteration):
    """Analyze ERC errors and apply fixes. Return True if fixes applied."""
    error_types = erc_result.get('error_types', {})

    if 'pin_not_connected' in error_types:
        # Read the schematic, find unconnected pins, add connections
        # ... fix logic ...
        return True

    if 'label_dangling' in error_types:
        # Move labels to correct pin positions
        # ... fix logic ...
        return True

    return False  # No fixable errors found

final = validate_and_fix_loop("output/schematic.kicad_sch", my_fixer)
```

## Common Patterns

### Decoupling Capacitor Array
```python
for i, (ref, val) in enumerate(zip(refs, values)):
    place_2pin_vertical(sch, "Device:C", ref, val,
                        x=snap(start_x + i * 8), y=snap(cap_y),
                        top_net=power_net, bottom_net="GND",
                        footprint=f"Capacitor_SMD:{fp}")
```

### 2-Pin Passives (R, C, L)
Standard KiCad 2-pin passive symbols have:
- Pin 1 at library (0, 2.54) — top when vertical
- Pin 2 at library (0, -2.54) — bottom when vertical

With rotation 0 at schematic (sx, sy):
- Pin 1 schematic position: (sx, sy - 2.54)
- Pin 2 schematic position: (sx, sy + 2.54)

```python
place_2pin_vertical(sch, "Device:C", "C1", "100nF",
                    x=snap(100), y=snap(150),
                    top_net="VCC_3V3", bottom_net="GND",
                    footprint="Capacitor_SMD:C_0402_1005Metric")
```

### Multi-pin IC Connection
```python
# Always use connect_pin — never compute positions manually
signal_map = {
    "TX1A_P": "TX1A_P",
    "TX1A_N": "TX1A_N",
    "SPI_CLK": "SPI_CLK",
    # ... all signal pins
}
for pin_name, net_name in signal_map.items():
    sch.connect_pin("U1", pin_name, net_name, wire_dx=-7.62)

# Power pins
for pin_name in ["VDDD1P3", "VDDA1P3", "VDDD1P8"]:
    sch.connect_pin("U1", pin_name, f"VCC_{pin_name}", wire_dy=5.08)

# Unused pins — EVERY unused pin needs this
for pin_name in ["AUXDAC1", "AUXDAC2", "AUXADC", "TEMP_SENS"]:
    sch.connect_pin_noconnect("U1", pin_name)
```

### Power Regulator with PWR_FLAG
```python
sch.place("CubeSat_SDR:AP2112K", "U4", "AP2112K-3.3",
          x=snap(100), y=snap(180),
          footprint="Package_TO_SOT_SMD:SOT-23-5")
wl(sch, 100, 180, 'VIN',  SOT5_PINS, "VCC_5V",  dx=-7.62)
wl(sch, 100, 180, 'EN',   SOT5_PINS, "VCC_5V",  dx=-7.62)
wl(sch, 100, 180, 'GND',  SOT5_PINS, "GND",     dy=5.08)
wl(sch, 100, 180, 'VOUT', SOT5_PINS, "VCC_3V3", dx=7.62)
# NC pin — no-connect flag, NOT a label
nc_x, nc_y = pin_abs(100, 180, *SOT5_PINS['NC'])
sch.nc(nc_x, nc_y)
# PWR_FLAG on output net
sch.place_pwr_flag(x=snap(115), y=snap(178), net_name="VCC_3V3")
```

## Lessons Learned (Battle-Tested)

These lessons came from debugging a real 119-component CubeSat SDR schematic:

1. **Never guess pin positions.** Even being off by 1.27mm (one grid unit) causes ERC errors. Always read the .kicad_sym file and use computed positions.

2. **The Y-axis flip is the #1 source of bugs.** Library Y-up vs schematic Y-down means you must negate Y. A pin at library (0, 25.4) is at schematic (sx, sy - 25.4) — NOT (sx, sy + 25.4). Getting this wrong places labels 50mm from their pins.

3. **SOT-23-5 VOUT vs NC confusion** silently breaks LDO circuits. VOUT=(7.62, 2.54), NC=(7.62, -2.54). They differ only in Y sign. After the Y-flip, VOUT is above NC in the schematic. Always verify against the library.

4. **Sub-symbol naming breaks KiCad silently.** If you write `(symbol "Device:R_0_1" ...)` instead of `(symbol "R_0_1" ...)`, KiCad may open the file but all symbols appear broken. Always run `fix_subsymbol_names()`.

5. **PWR_FLAG is needed more often than you think.** Any net driven by a regulator with passive-type output pins needs one. Also add one on GND. Missing PWR_FLAGs cause power_pin_not_driven errors on every component on that net.

6. **Grid snapping prevents hundreds of warnings.** A single off-grid component cascades into off-grid warnings for all connected wires and labels. Snap everything from the start.

7. **Account for every pin.** Go through the pin list systematically. Every pin must be either: connected via wire+label, connected to a power symbol, or flagged with no_connect. Missing even one pin produces an error.

8. **Parenthesis balance check.** KiCad S-expressions must have perfectly balanced parentheses. Add a check at the end of generation:
   ```python
   depth = sum(1 if c == '(' else -1 if c == ')' else 0 for c in content)
   assert depth == 0, f"Parenthesis imbalance: depth={depth}"
   ```

## Reference Files

- `scripts/kicad_sch_helpers.py` — Python helper library (always use this)
- `references/kicad_sexpression_format.md` — KiCad S-expression format specification, coordinate system, common ERC errors and fixes

Read `references/kicad_sexpression_format.md` before generating any schematic to understand the coordinate system, sub-symbol naming rules, and PWR_FLAG requirements.

## Checklist Before Delivery

1. All coordinates snapped to 1.27mm grid via `snap()`
2. Every IC pin either connected via `connect_pin()` / `wl()` or flagged with `connect_pin_noconnect()` / `nc()`
3. Sub-symbol names fixed with `fix_subsymbol_names()`
4. PWR_FLAG on every voltage regulator output net AND on GND
5. ERC validation run (0 errors target, warnings acceptable)
6. Parenthesis balance verified (depth 0 at end of file)
7. Pin positions verified against .kicad_sym library (not guessed)
8. SOT-23-5 VOUT vs NC positions double-checked for all LDOs
