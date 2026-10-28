---
name: segcfg-pl-reload
description: >
  Guides the Versal Segmented Configuration PL reload workflow for creating and validating
  multiple independently compiled `pld.pdi` variants while keeping `boot.pdi` fixed. Use
  when a user asks how to set up a golden PL reload design, spawn a new PL variant project,
  preserve NoC boot paths with `write_noc_solution`, size address apertures for reload
  compatibility, run `pr_verify -segcfg_only`, or debug `unique_id` / `parent_unique_id`
  mismatches rejected by PLM.
license: MIT
compatibility: Requires Vivado 2025.2+ and routed checkpoints for AMD Versal Segmented Configuration PL reload designs.
metadata:
  version: "1.0.0"
  stage: beta
allowed-tools: Read Bash Write
---

# Segmented Configuration PL Reload

## Overview

**Purpose:** Guide the user through golden project setup, variant spawning, NoC solution reuse, address aperture sizing, `pr_verify`, and UID compatibility for Versal PL reload flows.

**Output:** Guidance plus copy-pasteable Tcl and shell snippets for the user's current PL reload scenario. This skill does not generate `REPORT.md`.

**Supporting references:** Read `references/reload-methodology.md` for the full PL reload flow and `references/address-aperture.md` for aperture flexibility details.

---

## Prerequisites

| Requirement | Details |
|---|---|
| Vivado version | 2025.2 or later (2026.1 or later if combining DFX with Segmented Configuration) |
| Target family | Versal devices using Segmented Configuration |
| Segmented configuration project setting | For first-generation Versal devices where this feature is optional, set `set_property segmented_configuration true [current_project]` before implementation and image generation |
| Design state | Golden design routed before generating the `.ncr` file; golden and variant designs routed before running `pr_verify` |
| Open project | A Vivado project (`.xpr`) or routed checkpoint (`.dcp`) must be available for live validation |
| Vivado session | Connected via the MCP Vivado bridge or an interactive Tcl console |

---

## Efficiency Guidelines

- **Pass `session_id`** to every `vivado_execute` call when a Vivado session is active.
- **Write reports to file** — do not output full report content in chat; give a short summary only.
- **Read reports efficiently** — use `grep`, `sed`, or `awk` via terminal to extract specific sections instead of reading entire files into context. Use `wc -l` + `head` to check size first. Full `read_file` is fine only for small reports (<200 lines).
- **Do NOT** use `shell ls`, `shell find`, or `shell glob` to locate files.
- **Do NOT** use Vivado Tcl (`exec cat`, `open`, `read`) to read files. Use `grep`/`sed` via terminal or `read_file` with line ranges.
- **Do NOT** retry a failed Tcl command with different syntax. Report the error and stop or proceed.

---

## Workflow (Autonomous)

**⚠️ CRITICAL: Execute steps SEQUENTIALLY. Wait for each command to complete.**

Segcfg PL Reload Progress:
- [ ] Step 1: Read the bundled references and identify the user's PL reload scenario
- [ ] Step 2: Confirm or explain the golden design requirements
- [ ] Step 3: Choose a safe variant spawning method
- [ ] Step 4: Preserve NoC solution and address aperture compatibility
- [ ] Step 5: Run `pr_verify -segcfg_only` on routed designs
- [ ] Step 6: Check UID compatibility and summarize the next action

### Step 1: Read the references and identify the scenario

Read `references/reload-methodology.md` and `references/address-aperture.md` before answering detailed methodology questions.

If the user has not already made it clear, ask which scenario they need help with:
- Setting up a golden project from scratch
- Spawning a new PL variant from an existing golden design
- Debugging a `pr_verify` failure
- Understanding address aperture requirements
- Debugging UID compatibility failures at runtime

If live Vivado validation is needed, open the current design with a single-line Tcl command that handles either a checkpoint or a project workspace:

```tcl
set dcp [lindex [glob -nocomplain *.dcp] 0]; if {$dcp != ""} { open_checkpoint $dcp } elseif {[catch {current_design}]} { open_run impl_1 }; puts "Design: [current_design]"
```

Use `timeout_seconds: 18000` for long-running implementation commands such as `place_design` or `route_design`.

### Step 2: Confirm the golden design requirements

Explain and enforce these golden-design rules:
- The golden design is the **superset** of all PS-PL boundary connectivity needed by any reload variant.
- Enable every PS interface, NoC path, pin usage, and address aperture that any future variant may require.
- Keep the PS domain frozen across variants; only the PL domain may change.
- Compile the golden and all variants in the **same Vivado release**.
- For first-generation Versal devices where Segmented Configuration is optional, enable the project property before processing the design.

If needed, enable Segmented Configuration explicitly in project mode:

```tcl
set_property segmented_configuration true [current_project]
```

After the golden design reaches `route_design`, generate the NoC solution file:

```tcl
set ncr [file normalize "[current_design].ncr"]; write_noc_solution -force $ncr; puts "Generated NoC solution: $ncr"
```

### Step 3: Choose a safe variant spawning method

Generate Tcl for one of these supported methods:

```tcl
# Option A: Clone the entire project
save_project_as new_variant_project
```

```tcl
# Option B: Import the golden block design directory into a new project
import_files <path_to_golden>/<golden_project>.gen/sources_1/bd
```

```tcl
# Option C: Script the block design for recreation in the variant project
write_bd_tcl -force golden_bd.tcl; write_bd_tcl -hier_blks ps_hier -force golden_ps.tcl
```

**Warning:** Do NOT use `read_bd` — it creates a reference to the golden `.bd` source instead of a copy, so edits in the variant can corrupt the golden source.

### Step 4: Preserve NoC solution and address aperture compatibility

Import the golden `.ncr` file into the variant flow. Prefer setting the implementation run property:

```tcl
set_property NOC_SOLUTION_FILE <path_to_golden>/impl_1/<design>.ncr [get_runs impl_1]
```

Behind the scenes, this calls `read_noc_solution` before `place_design`.

If manually calling Tcl, use the syntax form supported by your Vivado release:

```tcl
read_noc_solution <path_to_golden>/impl_1/<design>.ncr
```

```tcl
read_noc_solution -file <path_to_golden>/impl_1/<design>.ncr
```

Then explain the aperture rules:
- The golden design defines the **largest** aperture needed for each PL slave interface.
- Variant designs may use a **subset** of that golden aperture.
- Variant designs may **not exceed** the golden aperture.
- Set apertures explicitly on INI ports so automated address assignment does not overwrite them.

### Step 5: Run `pr_verify -segcfg_only` after implementation

Use routed checkpoints only:

```tcl
pr_verify -segcfg_only -initial <golden_project>/impl_1/<golden>_routed.dcp -additional <variant_project>/impl_1/<variant>_routed.dcp
```

When `pr_verify` fails, direct the user to `/segcfg-design-check` for detailed DRC and `pr_verify` failure guidance, and use the aperture rules above to diagnose superset/subset mismatches.

### Step 6: Check UID compatibility and boot partition tile consistency

Explain and verify the runtime compatibility rules:
- `boot.pdi` keeps the PS domain fixed while `pld.pdi` changes.
- The boot image `unique_id` is derived from the PS domain construction.
- The PLD image `parent_unique_id` must match the boot image `unique_id`.
- Any PS-domain change (CIPS, NoC, DDR, boot-path tiles) can invalidate reload compatibility.

Use `bootgen` to inspect both PDIs:

```bash
bootgen -arch versal -read <boot.pdi>
bootgen -arch versal -read <pld.pdi>
```

Also compare `SegConfig_BootTiles.tcl` from the golden and variant implementation `hd_visual` directories. Differences indicate a boot-partition mismatch that can lead to UID incompatibility.

---

## Error Handling

| Error | Symptom | Action |
|---|---|---|
| No design open | `ERROR: No current design` | Use the Step 1 workspace auto-detect Tcl to `open_checkpoint` or `open_run impl_1` before running validation commands. |
| Missing `.ncr` file | `read_noc_solution` or `NOC_SOLUTION_FILE` points to a missing file | Re-run the golden design through `route_design`, then run `write_noc_solution` and use the generated absolute `.ncr` path. |
| `pr_verify` aperture mismatch | `pr_verify -segcfg_only` reports address or connectivity incompatibility | Confirm the golden design is the superset, ensure variants only shrink apertures, and review `references/address-aperture.md`. |
| PLM rejects `pld.pdi` | `parent_unique_id` does not match `boot.pdi unique_id` | Run `bootgen -arch versal -read` on both PDIs and compare IDs; then compare `SegConfig_BootTiles.tcl` to identify PS-domain drift. |
| `read_bd` was used in a variant flow | Variant edits unexpectedly affect the golden block design | Recreate the variant with `save_project_as`, `import_files`, or `write_bd_tcl`; never use `read_bd` for PL reload variants. |

---

## Validation

Success criteria for a correct PL reload flow:
- ✓ Golden design completed implementation and generated the `.ncr` NoC solution file
- ✓ Variant project was created with `save_project_as`, `import_files`, or `write_bd_tcl` — never `read_bd`
- ✓ `pr_verify -segcfg_only` passes between the routed golden and variant checkpoints
- ✓ `bootgen -arch versal -read` shows the variant `parent_unique_id` matches the boot image `unique_id`
- ✓ Golden and variant `SegConfig_BootTiles.tcl` files match for the boot partition

---

## Key Restrictions

- Mixed IO banks are supported but should be avoided because IO becomes active before PL loads and cannot change on reload.
- DFX within the PL is supported with Segmented Configuration starting in Vivado 2026.1; for DFX + Segmented Configuration scenarios, use `/segcfg-dfx`.
- PL Reload support is limited to designs compiled in the same Vivado release.
- For Gen 2 devices, avoid designs where both DDRMC5 ports connect to the PL domain.

---

## References

- **UG1387**: Versal Adaptive SoC Hardware, IP, and Platform Development Methodology
- **UG949**: UltraFast Design Methodology Guide
- **UG835**: Vivado Design Suite Tcl Command Reference Guide
- **UG909**: Vivado Design Suite User Guide: Dynamic Function eXchange
- **UG1283**: Bootgen User Guide
