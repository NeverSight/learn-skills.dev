---
name: segcfg-design-considerations
description: Understand Segmented Configuration design constraints for IO banks, CPM/PCIe use cases, and Gen 2 device-specific features (VCU, ISP, ASU, DPDC, 10GbE). Use before finalizing a design that straddles PS and PL domains.
license: MIT
compatibility: Applies to AMD Versal and Versal Gen 2 Segmented Configuration designs in Vivado.
metadata:
   version: "1.0.0"
   stage: beta
allowed-tools: Read Bash Write
---

Explain Segmented Configuration design constraints and help the user evaluate their design against known restrictions.

## Instructions

1. Read `references/io-bank-guide.md` for IO bank and clocking constraints.
   Read `references/cpm-pcie-guide.md` for CPM/PCIe-specific requirements.
   Read `references/gen2-features.md` for Gen 2 device-specific features.

2. Ask the user which aspects of their design they want to review:
   - IO bank sharing (PS and PL on same bank)
   - CPM/PCIe use cases
   - Gen 2 device features (VCU, ISP, ASU, DPDC, 10GbE)
   - General PS-PL boundary awareness

3. Explain **Mixed IO Banks** (applies to all Versal):
   - The boot image programs all IO in any bank required for DDR access (entire bank granularity)
   - IO connecting to PL logic becomes active *before* PL domain is configured
   - These IO cannot change functionality during PL Reload (they remain active until full-device reconfiguration)
   - Run SEGCONFIG-1 DRC to identify shared IO banks
   - PL ports in shared IO banks must use LVCMOS IOSTANDARD (SEGCONFIG-2 DRC)

4. Explain **X5IO Granularity** (Gen 2 devices only):
   - The third X5IO bank from a DDR site can be allocated to PL when only two half-banks are used by DDR5
   - Supported only for specific DDR5 configurations: Comp(DDR5) x4 with 16/20 data width, LPDDR5 x16/x32
   - Master bank (bank 700, left-most) must be in the boot partition if used by DDR
   - Run SEGCONFIG-5 DRC for master bank validation

5. Explain **CPM Use Cases**:
   - CPM Root Port mode: must be held in reset until PLD PDI is loaded; also must be held in reset during PL Reload
   - CPM end point (PCIe): Segmented Configuration auto-enables Tandem Configuration for 120ms link training
   - Do NOT select Tandem Configuration manually in CPM customization
   - To load PLD PDI over QDMA (Gen 1 CIPS): add `boot_device { pcie }` to the boot.bif (line after `id = 0x2`)
   - To load PLD PDI over QDMA (Gen 2 PS Wizard): set Secondary Boot = MMI_PCIe in Boot Mode (PLM) settings
   - PCIe Extended Configuration Space, QDMA multi-function: NOT available until PL is configured

6. Explain **Gen 2 device-specific features** that depend on PL:
   - **VCU & ISP**: Bundled with PL domain — unavailable until PLD PDI is loaded
   - **10GbE FIFO and TSU**: FIFO can be sourced from PL; TSU can use PL clock. Both require PL to be loaded
   - **ASU Soft Crypto Extension**: PL extension enabled in PS Wizard; programmed by PLD PDI
   - **DPDC (Display Controller)**: Live/Mixed modes require PL clock. Enable "DP required before PL Config"
     checkbox to use PS-based GPU_CLK initially, then switch after PL loads (driver support in future release)
   - **SYSMON auxiliary ports**: MIO/HDIO pins for external channel monitoring not available until PL is configured

7. Explain **CIPS-inferred PL logic** (all Gen 1 Versal):
   - Some CIPS features are not entirely in hard blocks
   - SYSMON auxiliary port measurements from external pins not possible until pins are configured

8. Provide guidance: for each concern identified, recommend whether to:
   - Redesign to avoid the constraint
   - Accept and document the behavior gap during the PS-only phase
   - Use DRC checks to validate before PDI generation
