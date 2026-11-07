---
name: vivado-timing-methodology-checks
description: >
  Runs 55+ timing methodology checks (UG906) on synthesized FPGA designs to identify timing violations and generate actionable RTL/XDC fixes. Make sure to use this skill whenever user mentions: "timing methodology", "methodology checks", "methodology report", "report_methodology", "UG906", "fix timing issues", "resolve methodology", "timing violations", "methodology violations", "clock violations", or any specific check IDs (TIMING-1 through TIMING-57). Use when user asks "how do I fix", "resolve", "waive", or "understand" any methodology check, warning, or violation. Also use when debugging timing problems after synthesis/implementation, interpreting methodology violation reports, or when user provides violation IDs like "TIMING-1#1". Use even if user just says "I have methodology violations" or "my design has timing warnings".
license: MIT
compatibility: Requires Vivado 2026.1+
metadata:
  version: "2.0.0"
---

<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->
# Table of Contents
- [Prerequisites](#prerequisites)
- [Step-by-Step Instructions](#step-by-step-instructions)
  - [Step 1: Open the Run](#step-1-open-the-run)
  - [Step 2: Running report_methodology](#step-2-running-report_methodology)
  - [Step 3: Extract information from the constraints file](#step-3-extract-information-from-the-constraints-file)
  - [Step 4: Consider Check Rules](#step-4-consider-check-rules)
  - [Step 5: Group IDs and prioritize](#step-5-group-ids-and-prioritize)
  - [Step 6: Generate data](#step-6-generate-data)
  - [Step 7: Follow Resolution Flow](#step-7-follow-resolution-flow)
  - [Step 8: Progress update](#step-8-progress-update)
  - [Step 9: Repeat until all groups are resolved](#step-9-repeat-until-all-groups-are-resolved)
  - [Step 10: Final report](#step-10-final-report)
- [Design Edits and Actions](#design-edits-and-actions)
  - [Automatic Fixes](#automatic-fixes)
  - [User Directed Fixes](#user-directed-fixes)
  - [Creating Waivers](#creating-waivers)
- [Critical Rules](#critical-rules)
- [File Locations](#file-locations)
- [Integration with Other Skills](#integration-with-other-skills)


# Prerequisites

1. Ensure your working directory is set up correctly:

```bash
# From your design directory (where the .dcp file is located)
# Step 1: Create working directory and symlink to skills
mkdir -p <cwd>/results
```
2. Understand whether the user input. 
  * Is it project or non-project flow
  * Is there a checkpoint or design run already open or do you need to open it

**Non project directory structure:**
```
<cwd>/
├── <design>.dcp                              # Your design checkpoint (optional, might be referenced from elsewhere)
|   ├── run.tcl                               # Vivado TCL script lists all the commands the agent executes
|   └── results/                              # Output directory (MUST BE CREATED FIRST)
|       ├── methodology.json                  # Generated violation data
|       ├── methodology_after_fix.json        # Generated violation data after fixes
|       ├── constraints.xdc                   # Backup before fixes
|       ├── constraints_after_fix.xdc         # Constraints after fixes
|       ├── constraints_diff.html             # HTML diff report
|       ├── run.log                           # full transcript of the skill run
|       ├── prompt.log                        # Capture of the user prompts entered
|       └── agent.log                         # output of agent verification used to confirm agent understanding of the issue and resolution
└── METHODOLOGY_RESOLUTION_REPORT.md  # Design report capturing what changes were made, resolutions, and remaining violations
```

**Project directory structure:**
```
<proj-dir>
└── <run-dir>
    ├── results/
    ├── run.tcl
    └── METHODOLOGY_RESOLUTION_REPORT.md
```

**Important:** When running scripts from the skill, understand the skill location and reference them `./scripts/`.

# Step-by-Step Instructions

## Step 1: Open the Design/Run

### Non Project
```tcl
open_checkpoint <design>.dcp
```

### Project
```tcl
open_project <proj_name>.xpr
open_run <run_name>
```

## Step 2: Running report_methodology
* Run report methodology and process json file

**Example script:**
```tcl
report_methodology -json methodology.json
```

**Required properties to extract from methodology report:**
* `RULE` - The violation rule (e.g., TIMING-1). This is the check ID.
* `NAME` - The violation rule (e.g., TIMING-1#1) This is presented in the order they are reported for each ID
* `SEVERITY` - Impact level
* `DETAILS` - Detailed description of the violation
* `NETLIST_ELEMENT` - Object causing violation extracted from DETAILS <cell: hier_name/leaf_cell_name> or <pin: hier_name/leaf_cell_name/Q>


## Step 3: Extract information from the constraints file
Write out constraints and process

**Example script:**
```tcl
write_xdc -force -exclude_physical ./results/constraints.xdc
```

**Required information to extract from xdc file:**
- Constraints are merged and written in a single file. The report must tell the user the original file.

**Example:** Capturing file name `pbf_pblocks.xdc` from unified XDC file.
```xdc
####################################################################################
# Constraints from file : 'pbf_pblocks.xdc'
####################################################################################

create_clock -period 8.000 -name REF_CLK [get_ports REF_CLK_p]
```

Capture:
* ✅ Original Filename = pbf_pblocks.xdc
* ✅ Line number = 2
* ✅ constraint type = create_clock
* ✅ clock object name = REF_CLK
* ✅ target_object = REF_CLK_p 
* ✅ target_object type = port
* ✅ period = 8.000


##  Step 4: Consider Check Rules
For each of the rule ids found in the methodology report:
1. Understand if a check is supported
2. If it is, capture group, priority and if there is a reference doc
3. General guildelines are always to be used. 
4. Additional guidelines are contained in a reference doc for a given ID. These can overwrite, or supplement general guidelines.

List of supported IDs are [./references/SUPPORTED_IDS.md](./references/SUPPORTED_IDS.md)
General guildelines [./references/GENERAL_GUIDELINES.md](./references/GENERAL_GUIDELINES.md)
Reference docs are in [./references/<ID>.md](./references/<ID>.md)

# Example: Find support level for TIMING-16 (supported) and TIMING-99 (not supported)
```sh
./scripts/get_id_info.sh TIMING-16
# Returns
# ID=TIMING-16
# GROUP=1
# PRIORITY=-
# HAS_REFERENCE_FILE=1

../scripts/get_id_info.sh TIMING-99
# Error: ID TIMING-99 not found in SUPPORTED_IDS.md
```

##  Step 5:  Group IDs and prioritize
In SUPPPORTED_IDS.md file there is a "GROUP" and "PRIORITY" value. 
GROUP defines which order the groups should be resolved. Group 1 is highest priority and should be solved first.
PRIORITY defines the order within the group. Priority 1 should be solved first before moving to priority 2 within the same group.

✅ **Do:**
* Order them at this stage.

❌ **Do not:**
* Solve them at this stage. We will solve them in the order of their groups and priorities in Step 5.

## Step 6: Generate data
Inside each reference is a `Generate Data` section. Generate the data specified for each check ID.

✅ **Do:**
* Collect all the data within the group being worked on

❌ **Do not:**
* Collect data for other groups at this stage
* Collect the same data more than once.

## Step 7: Follow Resolution Flow
* Each check has a defined flow to follow based on the reference documentation. 
* In the order defined by GROUP and PRIORITY, follow the flow to resolution
* Resolutions are either:
- **AUTO**: You can fix it automatically
- **USER**: You must get user input; never guess their design intent

**Critical**: Prioritize reference files over general guidelines when they exist.

* Confirm the message understanding by outputting in the agent.log file:
[x] Find the problematic constraint or issue
[x] Understand why it is problematic
[x] Understand the correct resolution and why it is correct
[x] Understand why the selected resolution is better than the other options if they exist
* Increases confidence that any constraint fixes do not have unintended consequences

## Step 8: Progress update
At the end of each group stage, checks are regenerated and fix criteria is tested. 
```tcl
reset_timing
read_xdc <new_constraints.xdc>   
report_methodology
write_json_report -report methodology -file ./tmp/methodology_after_fix_group_n.json
```

## Step 9: Repeat until all groups are resolved
Repeat steps 2-8 until all groups are resolved.

## Step 10: Final report
At the end of all groups, generate `METHODOLOGY_RESOLUTIONS_REPORT.md`

**FILE LOCATION: Write to `./METHODOLOGY_RESOLUTION_REPORT.md` in the current working directory (the design directory where the .dcp file is located). Do NOT use parent directory paths like `../` or absolute paths.**

1. Summary
   - Methodology violations before and after
   - Include IDs that are not resolved because they are not supported
   - Include IDs that are not resolved because user decision is required and user has not made a decision yet.
2. Resolved Violations
  - Foreach violation resolved, capture the action in a concise way
  - Include user decisions for each violation
  - Group IDs whose actions are the same when the same action solves multiple violations together to make the report more concise
  - Include a snippet of changes made to constraint file with diffs, 
3. Waivers section
4. Remaining Actions

**CRITICAL MARKDOWN FORMATTING:**
- Use proper markdown code fences with THREE backticks (```) for TCL code blocks
- Use single backticks (`) for inline code in tables and text
- Do NOT escape backticks with backslashes or forward slashes
- Write markdown directly to the file without escaping special characters
- **IMPORTANT**: Write actual newlines (`\n`), not the literal string `/n`

**HOW TO WRITE THE MARKDOWN FILE PROPERLY:**

When generating `METHODOLOGY_RESOLUTION_REPORT.md`, you MUST write it as a properly formatted markdown file with actual newlines. Use one of these approaches:

**Build content string with proper newlines:**
```tcl
set content "# Methodology Resolution Report\n\n"
append content "**Design:** $design_name\n"
append content "**Date:** $timestamp\n\n"
append content "## 1. Summary\n\n"
# ... continue building content
set report_file [open "./METHODOLOGY_RESOLUTION_REPORT.md" w]
puts -nonewline $report_file $content
close $report_file
```
**CRITICAL MARKDOWN FORMATTING:**
- Use proper markdown code fences with THREE backticks (```) for TCL code blocks
- Use single backticks (`) for inline code in tables and text
- Do NOT escape backticks with backslashes or forward slashes
- Write markdown directly to the file without escaping special characters
- **IMPORTANT**: Write actual newlines (`\n`), not the literal string `/n`
- **TABLES**: Use exactly ONE pipe `|` between columns and at start/end of rows
- **TABLES**: Separator rows must have SINGLE pipes only: `|----------|----------|`
- **NEVER use double pipes `||`** - this breaks markdown table rendering

**CORRECT table format:**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value A  | Value B  | Value C  |
```
**INCORRECT table format (DO NOT USE):**
```markdown
| Check ID | Severity | Count |
|----------|----------|-------||  ← WRONG! Double pipe breaks rendering
```

**PER-VIOLATION TABLE FORMAT:**
For each resolved violation, include a comparison table with this exact format (following TIMING-1.md Final Report example):

| Aspect | Period | Waveform | Clock Definition Object | Constraint |
|--------|--------|----------|------------------------|-----------|
| **Before** | <value> ns | {<rise> <fall>} | <clock_name> | `<full constraint command>` |
| **After** | <value> ns | {<rise> <fall>} | <clock_name> | `<full constraint command>` |

Requirements:
- Column headers must be: Aspect, Constraint, Period, Waveform, Clock Definition Object
- Constraint column must show FULL TCL command with all options, source, and target objects
- Do NOT truncate constraint commands - include complete `-source`, `-name`, `-multiply_by`, `-divide_by`, and target pin/port specifications
- Period column format: numeric value followed by "ns" (e.g., "8.000 ns")
- Waveform column format: {rise fall} (e.g., "{0 4.000}")

Create a diff report in HTML file. 
- review with before on the left and after on the right.

  ### Example: Before and After Comparison

  | Check ID | Severity | Count Before | Count After | Status & Resolution |
  |----------|----------|--------------|-------------|---------------------|
  | TIMING-1 | Critical Warning | 5 | 0 | **Resolved**: Modified `create_clock` period in pbf_timing.xdc |
  | TIMING-2 | Critical Warning | 3 | 0 | **Resolved**: Added `set_clock_groups -asynchronous` for clock domain crossing |
  | TIMING-3 | Critical Warning | 2 | 0 | **Resolved**: Converted to `create_generated_clock` |
  | TIMING-17 | Info | 2 | 2 | **Waived**: Design intent verified with user |
  | TIMING-5 | Warning | 1 | 0 | **Resolved**: Commented out redundant constraint |
  | SYNTH-5 | Warning | 864 | 864 | **Not Supported**: Connection to uninitialized flip-flop (requires RTL changes) |
  | SYNTH-6 | Warning | 1012 | 1012 | **Not Supported**: Timing of unconnected port (requires RTL changes) |
  | TIMING-18 | Warning | 160 | 160 | **Not Supported**: Missing input or output delay constraints (requires user decision) |
  | LUTAR-1 | Warning | 27 | 27 | **Not Supported**: LUT equation term check (requires RTL review) |
  | **Total** | | **2076** | **2065** | **11 violations resolved, 2065 require RTL changes or user decisions** |

  ### Example: TIMING3#2 Resolution
  - **Violation**: TIMING-1#1 - Invalid clock waveform on Clock Modifying Block
  - **Action**: Modified `create_clock` period from 5.000 to 12.800 in `pbf_timing.xdc` on line 45
  - **Reasoning**: User confirmed resolution
  #### Before
  ```tcl
  create_clock -period 8.000 -name REF_CLK [get_ports REF_CLK]
  ```

  #### After
  ```tcl
  # Fixed TIMING-3#2: Changed from create_clock to create_generated_clock
  # Preserves clock name SYS_CLK while respecting MMCM output
  create_generated_clock -name SYS_CLK -source [get_pins ios_0/mmcm_0/CLKIN1] -multiply_by 30 -divide_by 30 [get_pins ios_0/mmcm_0/CLKOUT1]
   ```

# Design Edits and Actions

## Automatic Fixes
When the reference documentation marks a resolution as **AUTO** with high confidence, apply the fix directly without prompting:

1. Create backup file: `cp constraints.xdc constraints_after_fix.xdc`
2. Apply the change using the **modify** approach (replace/add/remove constraint as specified)
3. Report exactly what was changed with before/after code blocks
4. Re-run `report_methodology` to verify the fix
5. Generate HTML diff file showing differences between `constraints.xdc` and `constraints_after_fix.xdc`

**Note**: For AUTO fixes, always use the "modify" approach (direct replacement). Only use "comment out" for USER-directed fixes where the user explicitly requests it.



## User Directed Fixes
1. Generate Vivado command based on user's choice
2. Show command for review
3. Ask: "Execute this command? [Y/n]"
4. If yes, 
a. Create a new file: `cp constraints.xdc constraints_after_fix.xdc`
b. Apply the change (remove/modify/add constraint)
c. Report exactly what was changed
d. Say: "Re-run report_methodology to verify"
e. Generate a HTML file detailing the differences between `constraints.xdc` and  `constraints_after_fix.xdc`
5. If no, save command to script for manual execution

## Creating Waivers
1. Ask: "Provide justification (will be recorded):"
2. Collect: reason for waiving
3. Format: `<username> <date> "<reason>"`
4. Generate: `create_waiver -of_objects [get_methodology_violations TIMING-3#1] -user poldark -description <description> -tags <related_waiver_tag>"`
5. Warn: "This violation will be ignored in future runs"

---

# Critical Rules

## DO:
✅ Always read `references/<CHECK_ID>.md` when it exists before responding
✅ Verify AUTO conditions before claiming you can fix it
✅ Present ALL options for USER resolutions
✅ For AUTO fixes: Apply immediately without prompting (high/medium confidence cases)
✅ For USER fixes: Ask confirmation before modifying any files
✅ Document every change made
✅ Solve violations by group (Group-1 before Group-2)
✅ Solve violations by priority (Group-1-P1 before Group-1-P2)
✅ Re-run report_methodology after completing each group
✅ Generate HTML diff after constraint modifications
✅ Recommend verification after fixes
✅ Use single pipes `|` in markdown tables
✅ Verify table formatting before writing files

## DON'T:
❌ Never guess design intent for USER resolutions
❌ Never apply AUTO fixes without verifying the conditions in the reference docs
❌ Never apply USER fixes without explicit user confirmation
❌ Never skip reading the reference documentation
❌ Never approve waivers without proper justification
❌ Never proceed if violation properties are missing
❌ Never skip to next group without re-running report_methodology
❌ **Never use double pipes `||` in markdown tables**
❌ Never end table separator rows with `||`
❌ Never add extra pipes at end of table rows


# File Locations

**Scripts:**
- `./scripts/trace_clock_tree.tcl` - Clock tracing utility
- `./scripts/get_id_info.sh`       - Utility to understand supported checks

**Reference Docs:**
- `./references/<CHECK_ID>.md` - Resolution guidance per violation
- Example: `./references/TIMING-1.md`

---

# Integration with Other Skills

Use alongside:
- **creating-vivado-tcl**: Generate constraint scripts after determining fix
- **design-analysis**: Understand design context before choosing resolution
- **creating-custom-qor-suggestion-checks**: Cross-reference with QoR recommendations
