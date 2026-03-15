---
name: kicad
description: Analyze KiCad EDA projects and PDF schematics — schematics, PCB layouts, Gerbers, footprints, symbols, design rules, netlists. Review designs for bugs, suggest improvements, extract BOMs, trace nets, cross-reference schematic to PCB, verify DRC/ERC, check DFM, analyze power trees and regulator circuits. Also analyze PDF schematics from dev boards, reference designs, eval kits, and datasheets — extract subcircuits, component values, and connectivity for incorporation into KiCad projects. Supports KiCad 5–9. Use whenever the user mentions KiCad files (.kicad_sch, .kicad_pcb, .kicad_pro), PCB design review, schematic analysis, PDF schematics, reference designs, Gerber files, DRC/ERC, netlist issues, BOM extraction, signal tracing, power budget, design for manufacturing, or wants to understand, debug, compare, or review any hardware design. Also use when the user says things like "check my board", "review before fab", "what's wrong with my schematic", "is this design ready to order", "check my power supply", "verify this motor driver circuit", or asks about any electronics/PCB design topic.
---

# KiCad Project Analysis Skill

## Related Skills

| Skill | Purpose |
|-------|---------|
| `bom` | BOM extraction, enrichment, ordering, and export workflows |
| `digikey` | Search DigiKey for parts (prototype sourcing) |
| `mouser` | Search Mouser for parts (secondary prototype source) |
| `lcsc` | Search LCSC for parts (production sourcing, JLCPCB) |
| `jlcpcb` | PCB fabrication & assembly ordering |
| `pcbway` | Alternative PCB fabrication & assembly |

**Handoff guidance:** Use this skill to parse schematics/PCBs and extract structured data. Hand off to `bom` for BOM enrichment, pricing, and ordering. Hand off to `digikey`/`mouser`/`lcsc` for part searches and datasheet fetching. Hand off to `jlcpcb`/`pcbway` for fabrication ordering and DFM rule validation.

## PDF Schematic Analysis

This skill also handles **PDF schematics** — reference designs, dev board schematics, eval board docs, application notes, and datasheet typical-application circuits. Common use cases:

- Analyze a manufacturer's reference design to understand the circuit
- Extract a subcircuit (power supply, USB interface, sensor front-end) to incorporate into your own KiCad design
- Compare a PDF reference design against your own schematic
- Extract a full BOM from a PDF schematic
- Validate component values in a PDF against current datasheets

**Workflow:** Read the PDF pages visually → identify components and connections → extract structured data → translate to KiCad symbols and nets → validate against datasheets.

For the full methodology — component extraction, notation conventions, net mapping, subcircuit extraction, KiCad translation, and validation — read `references/pdf-schematic-extraction.md`.

For deep validation of extracted circuits against datasheets (verifying values, checking patterns, detecting errors), use the methodology in `references/schematic-analysis.md`.

## Analysis Scripts

This skill includes Python scripts that extract comprehensive structured JSON from KiCad files in a single pass. Run these first, then reason about the output.

Read analyzer JSON output directly with the Read tool rather than writing ad-hoc extraction scripts. The JSON schema has specific field names (documented below and in `references/output-schema.md`) that are easy to get wrong in custom code. To extract a specific section: `python3 -c "import json; d=json.load(open('file.json')); print(json.dumps(d['key'], indent=2))"`.

**Before writing any ad-hoc Python to process analyzer output**, run `--schema` to see the exact field names and types:
```bash
python3 <skill-path>/scripts/analyze_schematic.py --schema
python3 <skill-path>/scripts/analyze_pcb.py --schema
python3 <skill-path>/scripts/analyze_gerbers.py --schema
```
This prevents format-string bugs and wrong field names. Use f-strings or `json.dumps()` for output formatting — never `%s` with non-string types. See `references/output-schema.md` for the full schema with common extraction patterns.

In all commands below, `<skill-path>` refers to this skill's base directory (shown at the top of this file when loaded).

### Schematic Analyzer
```bash
python3 <skill-path>/scripts/analyze_schematic.py <file.kicad_sch>
```
Outputs structured JSON (~60-220KB depending on board complexity) with:
- **Components & BOM**: inventory with reference, value, footprint, lib_id, type classification, MPN, datasheet; deduplicated BOM with quantities
- **Nets**: full connectivity map with pin-to-net mapping, wire counts, no-connects
- **Signal analysis** (automated subcircuit detection):
  - Power regulators — LDO/switching/inverting topology, Vout estimation via datasheet-verified Vref lookup (~60 families) with heuristic fallback, `vref_source` and `vout_net_mismatch` fields
  - Voltage dividers, RC/LC filters (cutoff frequency), feedback networks, crystal circuits (load cap analysis)
  - Op-amp circuits (configuration, gain), transistor circuits (net-name-aware load classification: motor/heater/fan/solenoid/valve/pump/relay/speaker/buzzer/lamp)
  - Bridge circuits (H-bridge, 3-phase, cross-sheet detection), protection devices (ESD/TVS), current sense, decoupling analysis
  - Domain-specific: RF chains, BMS, Ethernet, memory interfaces, key matrices, isolation barriers
- **Power analysis**: PDN impedance (1kHz–1GHz with MLCC parasitics), power budget, power sequencing (EN/PG chains), sleep current audit (resistive paths + regulator Iq with EN detection), voltage derating, inrush estimation
- **Design analysis**: ERC warnings, power domains, bus detection (I2C/SPI/UART/CAN with COPI/CIPO/SDI/SDO), differential pairs (suffix-pair matching for USB/LVDS/Ethernet/HDMI/MIPI/PCIe/SATA/CAN/RS-485), cross-domain signals (voltage equivalence), BOM optimization, test coverage, assembly complexity, USB compliance
- **Quality checks**: annotation completeness, label validation, PWR_FLAG audit, footprint filter validation, sourcing audit, property pattern audit, generic transistor symbol detection (flags Q_NPN_*/Q_PNP_*/Q_NMOS_*/Q_PMOS_* symbols with datasheet availability check)
- **Structural**: MCU alternate pin summary, ground domain classification, bus topology, wire geometry, spatial clustering, pin coverage, hierarchical label validation

Supports modern `.kicad_sch` (KiCad 6+) and legacy `.sch` (KiCad 4/5). Hierarchical designs parsed recursively.

**Legacy format:** For KiCad 5 legacy `.sch` files, the analyzer parses `.lib` files (cache libraries and project libs) to populate pin data. Pin-to-net mapping, signal analysis, and subcircuit detection all work when `.lib` files are available. Coverage is typically 92–100% — components whose `.lib` files are missing (standard KiCad system libs not in the repo) will lack pin data. Built-in fallbacks cover common symbols (R, C, L, D, LED, transistors).

### Supplementary Data for Legacy Designs

When `analyze_schematic.py` returns incomplete data (components with missing pins due to unavailable `.lib` files), use additional project files to recover full analysis capability. The most valuable source is the `.net` netlist file, which provides explicit pin-to-net mapping that closes any remaining gaps.

For detailed parsing instructions, data recovery workflows, and a priority matrix of supplementary sources (netlist, cache library, PCB cross-reference, PDF exports), read `references/supplementary-data-sources.md`.

**Verify analyzer output against reality.** The analyzer can silently produce plausible-looking but incorrect results — wrong voltage estimates, missing MPNs, wrong pin-to-net mappings. These don't cause script errors; they just produce bad data that flows into your report. In testing across multiple boards, every project had at least one misleading analyzer output. Cross-reference against the raw `.kicad_sch` file:

1. **Component count** — grep for `(symbol (lib_id` blocks, subtract power symbols. Must match analyzer count exactly.
2. **Pin-to-net mapping** — verify the analyzer's pin-to-net mapping against the raw schematic for each component. Read the symbol block, trace wires/labels to confirm connections. Cross-reference IC pin assignments against the manufacturer's datasheet pin table. This is the highest-value verification step — a wrong pin mapping produces a non-functional board and is invisible to DRC/ERC.
3. **Physical correctness (not just consistency)** — consistency checks (schematic=PCB=analyzer all agree) are necessary but not sufficient. They only confirm the design is internally coherent — not that it matches the real-world part. The most dangerous case: a transistor symbol encodes a pinout assumption (like `Q_NPN_BEC` = pin 1=B, 2=E, 3=C) that doesn't match the actual part. Everything passes consistency checks, but the board is wrong. To catch this:
   - For transistors (BJT/MOSFET) in SOT-23, SOT-223, TO-252 and similar packages, the KiCad `lib_id` suffix encodes a pin ordering assumption. SOT-23 BJTs exist in at least 6 pinout variants (BEC, BCE, EBC, ECB, CBE, CEB); SOT-23 MOSFETs in GDS, GSD, SGD, DSG. If no MPN is specified, there's no way to verify the assumption — flag this as a critical ambiguity.
   - When an MPN is specified, verify the symbol's pin-to-pad assignment against the datasheet's pinout diagram for that specific package.
   - This principle extends beyond transistors — any component where multiple pin orderings exist for the same package (voltage regulators with different pin assignments, connectors with vendor-specific pinouts) needs MPN-level verification.
   - **When verification isn't possible, assess plausibility.** Not all unverified choices carry equal risk. Some align with strong conventions (the most common SOT-23 NPN pinout is BCE; 2N2222 in SOT-23 is almost always BCE); others go against convention or are genuinely ambiguous (SOT-23 MOSFETs have no dominant standard). When an MPN is missing and you can't verify, use domain knowledge — typical pinouts for that device type and package, manufacturer conventions, what the majority of parts in that category do — to assess whether the assumed pinout is likely correct, unusual, or a coin flip. Report the confidence level: "matches the most common convention" is different from "could go either way." This same reasoning applies to passive values (is 4.7kΩ a typical pull-up value for this bus?), circuit topologies (is this a standard application circuit?), and component selection (is this part commonly used for this purpose?).
4. **Net trace** — trace power rails and critical signal nets end-to-end through wires/labels. Verify the analyzer's pin list is complete for each net.
5. **Regulator Vout** — check the `vref_source` field. `"lookup"` means datasheet-verified (~60 families); `"heuristic"` means it's a guess that needs manual verification. The `vout_net_mismatch` field flags estimated Vout differing >15% from the output rail name voltage.
6. **Hierarchical connectivity** — on multi-sheet designs, verify sub-sheet connections are reflected in the net data.

See `references/schematic-analysis.md` Step 2 for the full verification checklist. If the script fails or returns unexpected results, see `references/manual-schematic-parsing.md` for the complete fallback methodology.

### PCB Layout Analyzer
```bash
python3 <skill-path>/scripts/analyze_pcb.py <file.kicad_pcb>
python3 <skill-path>/scripts/analyze_pcb.py <file.kicad_pcb> --proximity  # add crosstalk analysis
```
Outputs structured JSON (~50-300KB depending on board complexity) with:
- **Core**: footprint inventory (pads, courtyards, net assignments, extended attrs, schematic cross-reference), track/via statistics, zone summaries, board outline/dimensions, routing completeness
- **Zones & copper presence**: zone outline vs filled polygon bounding boxes, fill ratio, cross-layer copper presence at every pad (which components have zone copper on the opposite layer and which don't), same-layer foreign zone detection
- **Via analysis**: type breakdown (through/blind/micro), annular ring checks, via-in-pad detection, BGA/QFN fanout patterns, current capacity, stitching via identification, tenting
- **Signal integrity**: per-net trace length, layer transition tracking (ground return paths), trace proximity/crosstalk (with `--proximity`)
- **Power & thermal**: current capacity per net, power net routing summary, ground domain identification (AGND/DGND), zone stitching via density, thermal pad detection and via counting
- **Manufacturing**: placement analysis (courtyard overlaps, edge clearance), decoupling cap distances, DFM scoring (JLCPCB standard/advanced tier), tombstoning risk (0201/0402 thermal asymmetry), thermal pad via adequacy, silkscreen documentation audit

Add `--full` to include individual track/via coordinates. Supports KiCad 5 legacy format.

**Zone fills must be current.** The copper presence analysis uses KiCad's filled polygon data, which is computed when the user runs Edit → Fill All Zones (shortcut `B`) and stored in the `.kicad_pcb` file. If the board was modified after the last fill, the filled polygon data may be stale and the copper presence results will be inaccurate. When reviewing copper presence data, note whether the `fill_ratio` seems reasonable — a zone with 0 filled area or `is_filled: false` likely hasn't been filled.

**Zone outline ≠ actual copper.** The zone `outline_bbox` is the user-drawn boundary; `filled_bbox` is where copper actually exists after clearances, keepouts, and priority cuts. The `copper_presence` section shows which components have zone copper on the opposite layer — use this for capacitive touch pad isolation, antenna keep-out, and thermal analysis instead of inferring copper presence from zone outlines.

**Verify after every run:** Confirm footprint count and board outline dimensions against the raw `.kicad_pcb` file. Verify pad-to-net assignments for IC footprints against the schematic's pin-to-net mapping — this catches library footprint errors where pad numbering doesn't match the symbol pinout. If the script fails, see `references/manual-pcb-parsing.md` for the fallback methodology.

### Gerber & Drill Analyzer
```bash
python3 <skill-path>/scripts/analyze_gerbers.py <gerber_directory/>
```
Outputs: layer identification (X2 attributes), component/net/pin mapping (KiCad 6+ TO attributes), aperture function classification, trace width distribution, board dimensions, drill classification (via/component/mounting), layer completeness, alignment verification, pad type summary (SMD/THT ratio). Add `--full` for complete pin-to-net connectivity dump. ~10KB JSON.

If the script fails or returns unexpected results, see `references/manual-gerber-parsing.md` for the complete fallback methodology for parsing raw Gerber/Excellon files directly.

All scripts output JSON to stdout by default. Use `--output file.json` to write to a file, `--compact` for single-line JSON.

**Analyzer JSON is worth keeping** — these are expensive to regenerate (large schematics take time). Use `--output` to save them for multi-pass analysis. They're not worth committing to git, but don't delete them between analysis steps.

### Generated Files

The analysis workflow creates files in the project tree. Analyzer JSON and design review reports use user-chosen filenames, so track what you create:

1. **Tell the user** what files were created and where
2. **Record them** in the project's `CLAUDE.md` under a "Generated files" section (create one if needed) so future sessions can find or clean them up
3. **When the user asks to clean up**, remove generated reports and analyzer JSON. Check `CLAUDE.md` for the file list — filenames vary per session.

| File Type | Example | Regenerable? | Commit to git? |
|-----------|---------|-------------|----------------|
| Analyzer JSON (`--output`) | `schematic_analysis.json` | Yes (expensive) | No |
| Design review report | `review.md`, `power_tree_review.md` | Yes | Optional — user may want to keep for reference |

See also the `bom` skill's cleanup section for datasheets, order CSVs, and backups.

### Output JSON Schema Quick Reference

**Schematic analyzer top-level keys:**
```
file, kicad_version, file_version, title_block, statistics, bom, components,
nets, subcircuits, ic_pin_analysis, signal_analysis, design_analysis,
connectivity_issues, labels, no_connects, power_symbols, annotation_issues,
label_shape_warnings, pwr_flag_warnings, footprint_filter_warnings,
sourcing_audit, ground_domains, bus_topology, wire_geometry,
simulation_readiness, property_issues, placement_analysis, hierarchical_labels
```
Optional (present when non-empty): `text_annotations`, `alternate_pin_summary`, `pin_coverage_warnings`, `instance_consistency_warnings`, `pdn_impedance`, `sleep_current_audit`, `voltage_derating`, `power_budget`, `power_sequencing`, `bom_optimization`, `test_coverage`, `assembly_complexity`, `usb_compliance`, `inrush_analysis`, `sheets`

Key nested structures:
- `statistics`: `{total_components, unique_parts, dnp_parts, total_nets, total_wires, total_no_connects, component_types, power_rails, missing_mpn, ...}`
- `bom[]`: `{reference, references[], value, footprint, mpn, manufacturer, datasheet, quantity, dnp, ...}`
- `components[]`: `{reference, value, footprint, lib_id, type, mpn, datasheet, dnp, in_bom, parsed_value, ...}`
- `nets{net_name}`: `{pins[], wires, labels[], ...}` — each pin: `{component, pin_number, pin_name, pin_type, ...}` (NOT `ref` or `pin`)
- `signal_analysis`: `{power_regulators[], voltage_dividers[], rc_filters[], opamp_circuits[], transistor_circuits[], bridge_circuits[], crystal_circuits[], current_sense[], decoupling_analysis[], protection_devices[], buzzer_speaker_circuits[], design_observations[], ...}`

**PCB analyzer top-level keys:**
```
file, kicad_version, file_version, statistics, layers, setup, nets,
board_outline, component_groups, footprints, tracks, vias, zones,
connectivity, net_lengths
```
Optional: `power_net_routing`, `decoupling_placement`, `ground_domains`, `current_capacity`, `thermal_analysis`, `layer_transitions`, `placement_analysis`, `silkscreen`, `dfm`, `board_metadata`, `dimensions`, `groups`, `net_classes`, `tombstoning_risk`, `thermal_pad_vias`, `copper_presence`, `trace_proximity`

Key nested structures:
- `net_lengths` is a **list** (not dict): `[{net, net_number, total_length_mm, segment_count, via_count, layers{}}, ...]` sorted by length descending
- `power_net_routing` is a **list**: `[{net, track_count, total_length_mm, min_width_mm, max_width_mm, widths_used[]}, ...]`
- `footprints[]`: `{reference, value, footprint, layer, pads[], sch_path, sch_sheetname, sch_sheetfile, connected_nets[], ...}`
- `statistics`: `{footprint_count, copper_layers_used, smd_count, tht_count, zone_count, via_count, routing_complete, ...}`

**Gerber analyzer top-level keys:**
```
statistics, completeness, alignment, drill_classification, pad_summary,
board_dimensions, gerbers, drills
```

**Workflow:** When analyzing a KiCad project, scan the project directory for all available file types and run every applicable analyzer — not just the one the user mentioned. A complete analysis uses all the data available:

1. **Scan the project directory** for `.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, gerber directories, and `.net`/`.xml` netlist files
2. **Run all applicable scripts** — if the schematic exists, run `analyze_schematic.py`. If the PCB exists, run `analyze_pcb.py`. If gerbers exist, run `analyze_gerbers.py`. Run them in parallel when possible.
3. **Sync datasheets** (see Datasheet Acquisition below) — datasheets are required for proper verification, not optional. Get them before proceeding to verification.
4. **Read the `.kicad_pro`** project file directly (it's JSON) for design rules, net classes, and DRC/ERC settings
5. **Cross-reference outputs** between schematic and PCB (see section below) — this catches the most dangerous bugs (swapped pins, missing nets, footprint mismatches)
6. **Verify each output** against the raw files and datasheets before using the data in your report
7. **Produce a unified report** covering schematic analysis, PCB layout analysis, and cross-reference findings. See `references/report-generation.md` for the report template.

The more data sources you combine, the more confident the analysis. A schematic-only review misses layout issues; a PCB-only review misses design intent. Always use everything available.

### Analysis Depth

Default to thorough analysis unless the user asks for a quick review. The reason: the bugs that kill boards are the ones that look correct at a glance. A spot-check might confirm 5 ICs are correct while the 6th has pins 3 and 4 swapped — and that's the one that kills the board. Thoroughness principles:

- **Verify all components, not a sample.** Pin-to-net errors on "simple" parts (reversed diode, wrong resistor in a divider, connector with wrong pin ordering) are just as fatal as swapped IC pins. Cover the full design.
- **Use datasheets as ground truth.** The analyzer and raw schematic tell you what the design *says* — the datasheet tells you what it *should* say. A library symbol with a wrong pin mapping is the most dangerous class of bug precisely because the design is internally consistent. See "Datasheet Acquisition" below.
- **Assess plausibility, not just verifiability.** When something can't be verified (missing MPN, missing datasheet), don't stop at "unverified." Use domain knowledge to assess whether the design choice aligns with common conventions or looks unusual. A 10kΩ I2C pull-up is unremarkable; a 100Ω I2C pull-up warrants a closer look even without a datasheet to check against. An SOT-23 NPN with BCE pinout matches the most common convention; one with CEB is unusual enough to flag. The goal is to distinguish "unverified but probably fine" from "unverified and suspicious." This applies to pinouts, passive values, circuit topologies, and component selection.
- **Think beyond what the analyzer detects.** The analyzer only finds patterns it's programmed for. When a section has no automated data, consider whether that's because the design doesn't need it (fine — say so briefly) or because the analyzer can't detect it (reason about it manually). Not every section needs a paragraph — "Not applicable: battery-powered, no mains input" is sufficient. But don't let empty data create blind spots in areas that matter for the specific design.

### Datasheet Acquisition

Datasheets are what separate a consistency check from a correctness check. Without them, you can confirm the design agrees with itself — but not that it matches the real-world parts. Obtain datasheets early in the workflow.

**Automated sync (preferred):** Run datasheet sync scripts early in the workflow. They download datasheets for all components with MPNs into a shared `datasheets/` directory with an `index.json` manifest. Run the preferred source first; if some parts fail, try others — they share the same directory and skip already-downloaded files.

```bash
python3 <digikey-skill-path>/scripts/sync_datasheets_digikey.py <file.kicad_sch>
python3 <lcsc-skill-path>/scripts/sync_datasheets_lcsc.py <file.kicad_sch>
python3 <element14-skill-path>/scripts/sync_datasheets_element14.py <file.kicad_sch>
python3 <mouser-skill-path>/scripts/sync_datasheets_mouser.py <file.kicad_sch>
```

DigiKey is best (direct PDF URLs). element14 is reliable (no bot protection). LCSC works for LCSC-only parts. Mouser is a last resort (often blocks downloads).

**Check for existing datasheets:** Before downloading, look for:
- `<project>/datasheets/` with `index.json` (from a previous sync)
- `<project>/docs/` or `<project>/documentation/`
- PDF files in the project directory whose names contain MPNs
- `Datasheet` property URLs embedded in the KiCad symbols

**Fallback methods when automated sync isn't available or misses parts:**
1. Use the `Datasheet` property URL from the schematic symbol — many KiCad libraries include direct PDF links
2. Use the `digikey` skill to search by MPN and download individual datasheets
3. Use WebSearch to find the manufacturer's datasheet page
4. **Ask the user** — if a critical component's datasheet can't be found automatically, tell the user which parts are missing and ask them to provide the datasheets. Don't silently skip verification because a datasheet wasn't available. Example: "I couldn't find datasheets for U3 (XYZ1234) and U7 (ABC5678). Can you provide them? I need them to verify the pinout and application circuit."

**What to extract from each datasheet** (note page/section/figure/equation numbers for citations):
- Pin function table (pin number → name → function)
- Absolute maximum ratings (voltage, current, temperature — including max continuous current through VCC/GND pins, which constrains inrush)
- Recommended application circuit and required external components
- Required component values (and the equations that derive them)
- Thermal characteristics

**For passives:** While individual resistor/capacitor datasheets are rarely needed, verify the component values against the IC datasheets that specify them. The IC's datasheet says "use a 10µF input cap" — verify the schematic actually has 10µF there, not 1µF.

### Schematic + PCB Cross-Reference

When both files exist, cross-reference them. This catches the most expensive bugs — swapped pins, missing nets, and footprint mismatches pass DRC/ERC but produce non-functional boards.

1. **Component count**: Schematic count (excluding power symbols) vs PCB footprint count.
2. **Net consistency**: Verify schematic net names appear in PCB net declarations. Missing nets suggest incomplete routing or un-synced changes.
3. **Pin-net assignments**: Compare schematic pin-to-net mapping against PCB pad-to-net mapping. Mismatches reveal swapped pins or library errors. Higher-risk areas:
   - Custom/community library symbols (may not match datasheet pinout)
   - Multi-unit symbols (op-amps, gate arrays) — unit-to-pin assignment errors
   - QFN/BGA packages — pad numbering mistakes
   - Transistors without MPNs — pinout ambiguity (see verification step 3)
   - Polarized components — anode/cathode orientation
   - Connectors — pin 1 orientation
4. **Footprint match**: Schematic `Footprint` property vs actual PCB footprint (e.g., SOT-23 vs SOT-23-5).
5. **DNP consistency**: DNP components in schematic should not have routing on PCB.
6. **Value/MPN consistency**: Values and MPNs match between schematic and PCB properties.

The PCB analyzer's `sch_path`, `sch_sheetname`, and `sch_sheetfile` fields in each footprint enable automated cross-referencing.

## Reference Files

Detailed methodology and format documentation lives in reference files. Read these as needed — they provide deep-dive content beyond what the scripts output automatically.

| Reference | Lines | When to Read |
|-----------|-------|-------------|
| `schematic-analysis.md` | 1117 | Deep schematic review: datasheet validation, design patterns, error taxonomy, tolerance stacking, GPIO audit, motor control, battery life, supply chain |
| `pcb-layout-analysis.md` | 414 | Advanced PCB: impedance calculations, differential pairs, return paths, copper balance, edge clearance, copper-sensitive components (capacitive touch, antennas), custom analysis scripts |
| `file-formats.md` | 361 | Manual file inspection: S-expression structure, field-by-field docs for all KiCad file types, version detection |
| `gerber-parsing.md` | 729 | Gerber/Excellon format details, X2 attributes, analysis techniques |
| `pdf-schematic-extraction.md` | 315 | PDF schematic analysis: extraction workflow, notation conventions, KiCad translation |
| `supplementary-data-sources.md` | 301 | Legacy KiCad 5 data recovery: netlist parsing, cache library, PCB cross-reference |
| `net-tracing.md` | 109 | Manual net tracing: coordinate math, Y-axis inversion, rotation transforms |
| `manual-schematic-parsing.md` | 285 | Fallback when schematic script fails |
| `manual-pcb-parsing.md` | 457 | Fallback when PCB script fails |
| `manual-gerber-parsing.md` | 621 | Fallback when Gerber script fails |
| `report-generation.md` | 479 | Report template (critical findings at top), analyzer output field reference (schematic/PCB/gerber), severity definitions, writing principles, domain-specific focus areas, known analyzer limitations |
| `standards-compliance.md` | 597 | IPC/IEC standards tables: conductor spacing (IPC-2221A Table 6-1), current capacity (IPC-2221A/IPC-2152), annular rings, hole sizes, impedance, via protection (IPC-4761), creepage/clearance (ECMA-287/IEC 60664-1). Consider for all boards; auto-trigger for professional/industrial designs, high voltage, mains input, or safety isolation. |

For script internals, data structures, signal analysis patterns, and batch test suite documentation, see `scripts/README.md`.

## File Types Quick Reference

| Extension | Format | Purpose |
|---|---|---|
| `.kicad_pro` | JSON | Project settings, net classes, DRC/ERC severity, BOM fields |
| `.kicad_sch` | S-expr | Schematic sheet (symbols, wires, labels, hierarchy) |
| `.kicad_pcb` | S-expr | PCB layout (footprints, tracks, vias, zones, board outline) |
| `.kicad_sym` | S-expr | Symbol library (schematic symbols with pins, graphics) |
| `.kicad_mod` | S-expr | Single footprint (in `.pretty/` directory) |
| `.kicad_dru` | Custom | Custom design rules (DRC constraints) |
| `fp-lib-table` / `sym-lib-table` | S-expr | Library path tables |
| `.sch` / `.lib` / `.dcm` | Legacy | KiCad 5 schematic, symbol library, descriptions |
| `.net` / `.xml` | S-expr/XML | Netlist export, BOM export |
| `.gbr` / `.g*` / `.drl` | Gerber/Excellon | Manufacturing files (copper, mask, silk, outline, drill) |

For version detection and detailed field-by-field format documentation, read `references/file-formats.md`.

## Analysis Strategies

### Deep Schematic Analysis

For a thorough datasheet-driven schematic review — identifying subcircuits, fetching datasheets, validating component values against manufacturer recommendations, comparing against common design patterns, detecting errors, and suggesting improvements — read `references/schematic-analysis.md`. Use this reference whenever the user asks to review, validate, or analyze a schematic in depth.

**Fetching datasheets**: When the analysis requires datasheet data, use the DigiKey API as the preferred source (see the `digikey` skill) — it returns direct PDF URLs via the `DatasheetUrl` field without web scraping. Search by MPN from the schematic's component properties. Fall back to WebSearch only for parts not on DigiKey.

### Deep PCB Analysis

For advanced layout analysis beyond what the PCB analyzer script provides — impedance calculations from stackup parameters, DRC rule authoring, power electronics design review techniques, differential pair validation, return path analysis, copper balance assessment, board edge clearance rules, and manual script-writing patterns — read `references/pcb-layout-analysis.md`.

Most routine PCB analysis (via types, annular ring, placement, connectivity, thermal vias, current capacity, signal integrity, DFM scoring, tombstoning risk, thermal pad vias) is handled automatically by `analyze_pcb.py`. Use the reference for deeper manual investigation.

### Quick Review Checklists

**Schematic** — verify: decoupling caps on every IC VCC/GND pair, I2C pull-ups, reset pin circuits, unconnected pins have no-connect markers, consistent net naming across sheets, ESD protection on external connectors, power sequencing (EN/PG), adequate bulk capacitance.

**PCB** — verify: power trace widths for current (IPC-2221), via current capacity, creepage/clearance for high voltage, decoupling cap proximity to IC power pins, continuous ground plane (no splits under signals), controlled impedance traces (USB/DDR), board outline closed polygon, silkscreen readability. Consider `references/standards-compliance.md` for IPC/IEC standard values — conductor spacing and current capacity are relevant for most boards; creepage/clearance and via protection apply to mains-connected or safety-isolated designs.

**Common bugs (ranked by board-killing potential)**: swapped IC pins (library symbol vs datasheet pinout — invisible to DRC/ERC), transistor pinout ambiguity (SOT-23 without MPN — symbol assumes a pin ordering that may not match the real part; assess plausibility against common conventions when verification isn't possible), wrong footprint pad numbering, missing nets from un-synced schematic→PCB, wrong package variant (SOT-23 vs SOT-23-5), floating digital inputs, missing bulk caps, reversed polarity, incorrect feedback divider values, wrong crystal load caps, USB impedance mismatch, QFN thermal pad missing vias, connector pinout errors, unusual passive values (a value that's technically valid but uncommon for the application — e.g., a non-standard pull-up resistance, an unusual decoupling capacitor value).

### Report Generation

When producing a design review report, read `references/report-generation.md` for the standard report template, severity definitions, writing principles, and domain-specific focus areas. The report format covers: overview, component summary, power tree, analyzer verification (spot-checks), signal/power/design analysis review, quality & manufacturing, prioritized issues table, positive findings, and known analyzer gaps. Always cross-reference analyzer output against the raw schematic before reporting findings.

### Design Comparison
When comparing two designs, diff: component counts/types, net classes/design rules, track widths/via sizes, board dimensions/layer count, power supply topology, KiCad version differences.
