---
name: fiji-skill
description: Operate Fiji/ImageJ through Fiji MCP, Fiji Macro Bridge, or ImageJ macro scripts using native Fiji commands and documented workflows. Use when an agent needs to open, process, measure, segment, threshold, filter, register, visualize, export, batch-process, or analyze images in Fiji/ImageJ, especially when the task should rely on Fiji menus, plugins, Macro Recorder-style commands, Results Table, ROI Manager, Bio-Formats, stacks, hyperstacks, or standard ImageJ/Fiji analysis features instead of custom pixel-processing code.
---

# Fiji Skill

Use this skill to drive Fiji through the MCP/Macro Bridge while keeping the work grounded in Fiji/ImageJ's documented commands, menus, plugins, and macro conventions.

## Operating Rule

Prefer Fiji-native operations before writing custom image-processing code.

- For image processing or analysis requests, first propose the intended Fiji workflow and wait for user approval before running commands that alter images, create analysis outputs, change Results Table contents, add ROIs/overlays, open/close images, or save files.
- The proposal must name the active image or image-selection assumption, Fiji commands/plugins to use, key parameters, expected outputs, and whether the operation changes a working copy or the current image.
- Honor user-specified analysis choices such as threshold method, polarity, size range, channel, ROI, projection method, and whether to use object-splitting steps. If a required choice is not specified, propose a default explicitly and wait for approval.
- Read-only state checks are allowed before approval: connection checks, open-image listing, Log inspection, and other non-mutating inspection needed to draft the proposal.
- Use ImageJ/Fiji menu commands, Macro Recorder-style `run(...)` calls, `IJ.run(...)`, ImageJ APIs, and installed plugins first.
- Do not hand-roll thresholding, filtering, connected components, particle detection, ROI measurement, stack projection, channel splitting, registration, or file conversion when Fiji has a built-in command or plugin.
- Duplicate or create a working copy before irreversible processing unless the user explicitly wants to modify the current image.
- Preserve calibration and metadata when it affects measurements. Check spatial scale, channel, slice, frame, and redirect settings before measuring.
- Treat raw images and processed masks differently. Measure intensity on the intended source image; use masks/ROIs for object definition.

## Bridge Workflow

When Fiji MCP tools are available:

1. Check connection with `mcp__fiji.check_connection`.
2. If connected, inspect state with `mcp__fiji.list_open_images` and, when useful, `mcp__fiji.get_log`.
3. If not connected and Fiji must be launched, use the local Fiji executable configured in `references/bridge-workflow.md` or `mcp__fiji.launch_fiji` when available. After launch, start the MCP Bridge plugin and confirm with `mcp__fiji.check_connection`.
4. For image processing or analysis, propose the exact workflow and wait for user approval.
5. Run Fiji commands through `mcp__fiji.run_script`, preferably with JavaScript and `IJ.run(...)` or ImageJ macro-style command strings.
6. Verify output through open images, Results Table, Log, overlays, or screenshots.

Read `references/bridge-workflow.md` before executing nontrivial Fiji operations through MCP.

## Task Routing

Classify the request, then read only the relevant reference file:

- Connection, scripts, logs, macro execution: `references/bridge-workflow.md`
- Choosing native Fiji commands instead of custom algorithms: `references/native-command-policy.md`
- Common menu commands and macro patterns: `references/core-fiji-commands.md`
- Measurements, ROI Manager, Results Table, calibration: `references/measurements-roi-results.md`
- Thresholding, masks, segmentation, particles, skeletons: `references/thresholding-segmentation.md`
- Filters, background subtraction, contrast, projections for preprocessing: `references/filtering-background.md`
- Stacks, hyperstacks, channels, Z/T operations: `references/stacks-hyperstacks-channels.md`
- File I/O, Bio-Formats, export, batch processing: `references/file-io-batch.md`
- Registration, stitching, colocalization, plugin-heavy workflows: `references/registration-colocalization.md`

If the request spans categories, read the fewest references needed and compose the workflow from native Fiji commands.

## Macro Construction

Use Macro Recorder-compatible command names and options whenever possible. Prefer this shape:

```javascript
var imp = IJ.getImage();
IJ.run(imp, "Duplicate...", "title=working");
IJ.run("Set Measurements...", "area mean min max centroid perimeter shape decimal=3");
IJ.run("Measure");
```

For pure macro snippets, keep commands recorder-like:

```ijm
run("Duplicate...", "title=working");
run("Set Measurements...", "area mean min max centroid perimeter shape decimal=3");
run("Measure");
```

Use direct pixel loops only when:

- No Fiji/ImageJ command, plugin, or API reasonably covers the operation.
- The user explicitly requests a custom implementation.
- The operation is a small glue step around Fiji-native results, not a replacement for the analysis.

## Documentation Grounding

Base workflows on Fiji/ImageJ public documentation and recorder behavior. Useful starting points:

- ImageJ User Guide: `https://imagej.net/ij/docs/guide/user-guide.pdf`
- ImageJ macro language and `run(command, options)`: `https://imagej.net/ij/developer/macro/macros.html`
- ImageJ/Fiji documentation portal: `https://imagej.net/Documentation`
- Fiji scripting: `https://imagej.net/scripting/`
- Bio-Formats in Fiji: `https://imagej.net/formats/bio-formats`

If exact command options are uncertain, prefer checking Fiji's Macro Recorder or official command documentation before inventing options.

## Validation

After running commands:

- Confirm the expected image, overlay, ROI, Results Table, or Log entry exists.
- Summarize which Fiji command(s) were used.
- Report any assumptions: active image, selected ROI, threshold method, measurement settings, calibration, channel/slice/frame, or output path.
- If a command fails, inspect the Fiji Log and correct the native command/options before falling back to custom code.
