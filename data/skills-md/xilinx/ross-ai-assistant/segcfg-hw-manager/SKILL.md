---
name: segcfg-hw-manager
description: Program Versal hardware using Vivado Hardware Manager in Segmented Configuration mode. Use when programming boot.pdi and pld.pdi through the Vivado GUI, programming configuration flash memory, or enabling the segmented configuration dialog for first-generation Versal devices.
license: MIT
compatibility: Requires Vivado Hardware Manager, access to AMD Versal hardware, and matching boot.pdi and pld.pdi images.
metadata:
   version: "1.0.0"
   stage: beta
allowed-tools: Read Bash Write
---

Guide the user through programming Versal hardware via the Vivado Hardware Manager in Segmented Configuration mode.

## Instructions

1. Read `references/hw-manager-guide.md` for Hardware Manager dialog details and flash programming specifics.

2. Ask the user:
   - Which board they are targeting
   - Whether they need JTAG programming only, or flash (configuration memory) programming
   - Whether they are using a first-generation or second-generation Versal device

3. **Enable Segmented Configuration mode in Hardware Manager** (first-gen devices only):
   In the Vivado Tcl Console before opening Hardware Manager:
   ```tcl
   set_param labtools.enableSegmentedConfigFlow 1
   ```
   This exposes the Segmented Configuration programming dialog for first-generation Versal devices.
   For second-generation devices, Segmented Configuration is always active — no parameter needed.

4. **Connect to the hardware target**:
   - Open Vivado Hardware Manager: **Flow Navigator > Program and Debug > Open Hardware Manager**
   - Click **Open Target > Auto Connect** to discover the JTAG chain
   - The Versal device will appear in the Hardware window

5. **Program the device via JTAG**:
   - Right-click the device in the Hardware window → **Program Device**
   - In the Program Device dialog, the Segmented Configuration-specific fields appear:
     - **Enable segmented configuration mode** checkbox (first-gen devices)
     - **Boot PDI File**: browse to `<design>_boot.pdi`
     - **Boot LTX Probe File**: browse to `<design>_boot.ltx` (if ChipScope cores in boot partition)
     - **PLD PDI File**: browse to `<design>_pld.pdi`
     - **PLD LTX Probe File**: browse to `<design>_pld.ltx` (if ChipScope cores in PLD)
   - Hardware Manager loads Boot and PLD images sequentially

6. **Boot-only programming** (test PS domain without PL):
   - In the Program Device dialog, populate only the Boot PDI field
   - Leave the PLD PDI field empty
   - This enables testing the processing domain independently

7. **PLD-only programming** (for PL Reload — boot PDI already loaded):
   - Populate only the PLD PDI field
   - The boot PDI must already be resident on the device
   - Used for PL Reload scenarios and iterative PL debug

8. **Programming configuration flash memory**:
   - Right-click the device → **Add Configuration Memory Device**
   - Select the flash part for your board (e.g., MT25QU02GCBB for VCK190)
   - Right-click the memory device → **Program Configuration Memory Device**
   - In the dialog, set offsets for both boot and PLD PDIs:
     - **Boot PDI offset**: `0x00000000` (start of flash)
     - **PLD PDI offset**: non-zero value, multiple of flash sector size (64KB = 0x10000)
     - Ensure sufficient room for boot PDI before declaring PLD offset
   - Example: if boot PDI is ~10MB, use PLD offset `0x00A00000` (10MB aligned to 64KB)

9. **ChipScope debugging with Segmented Configuration**:
   - Boot partition ILA/VIO are activated when boot PDI loads → LTX file from boot.pdi
   - PLD partition ILA/VIO are activated when pld PDI loads → LTX file from pld.pdi
   - Refresh hardware after each PDI load to discover new debug cores

10. For more information, refer to the [Vivado Design Suite User Guide: Programming and Debugging (UG908)].
