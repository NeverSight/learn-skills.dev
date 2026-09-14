---
name: setup-dell-monitors
description: Troubleshoot Arthur's Dell P2725DE/P2225D monitor setup, especially DisplayPort daisy chaining, "No DP signal from your device" on the P2225D, Windows Fast Startup or shutdown-related display breakage, and reset/reinstall steps for a Lenovo laptop or Dell desktop tower using original Dell cables.
---

# Setup Dell Monitors

This is a historical DisplayPort daisy-chain recovery workflow. Before applying it to the user's present desk, load `dell-monitor-kvm-setup` and its dated in-package inventory. Apply the topology below only if the current connection actually matches it; do not replace the newer saved hub/KVM or DisplayLink topology with these older assumptions.

## Overview

Use this skill to help recover or reason about Arthur's Dell monitor daisy-chain setup. The known hardware is:

- Lenovo laptop
- Dell desktop tower
- Dell P2725DE monitor, used as the hub / first monitor
- Dell P2225D monitor, used as the secondary daisy-chained monitor
- Original cables delivered with the monitors and desktop, assumed known-good unless new evidence contradicts that

The recurring symptom is the P2225D showing "No DP signal from your device" after the display setup has been broken.

## First Distinction

Start by asking which source computer is being used:

- Dell desktop tower: The known-good setup has previously supported P2725DE at QHD and P2225D at HD through DisplayPort daisy chaining.
- Lenovo laptop: The known-good workaround used lower resolution on the P2725DE so the P2225D could receive signal through the chain.

Do not assume the laptop and desktop have the same bandwidth behavior.

## Known-Good Physical Topology

For the Dell desktop tower, prefer this topology:

1. Connect the desktop to the P2725DE using DisplayPort.
2. Connect the P2725DE DisplayPort output to the P2225D using DisplayPort.
3. Set the P2725DE OSD:
   - Display > MST = On
   - Display > USB-C Prioritization = High Resolution / four-lane mode
4. Set the P2225D OSD:
   - Input Source = DisplayPort

For the Lenovo laptop, the source note used USB-C into the P2725DE and then DisplayPort from P2725DE to P2225D.

## Fast Startup Check

If the setup works after restart but breaks after shutdown and later power-on, suspect Windows Fast Startup or a similar fast boot behavior.

Guide the user to disable Fast Startup before repeating the cable reset workflow:

1. Open Control Panel.
2. Go to Power Options.
3. Open "Choose what the power buttons do".
4. Select "Change settings that are currently unavailable".
5. Clear "Turn on fast startup" if it is enabled.
6. Save changes.
7. Restart once, then shut down and power on normally to test whether the monitor chain stays stable.

Use exact Windows wording when possible, but adapt if the user's Windows version presents the setting differently.

## Full Daisy-Chain Recovery Workflow

Use this sequence when the chain has already broken and the secondary monitor reports no DisplayPort signal.

### Uninstall / Power Down Everything

1. Turn off both monitors using their physical power buttons.
2. Turn off the power strip.
3. Unplug all cables from both monitors and the computer:
   - DisplayPort
   - AC power
   - USB-C, if using the laptop path
4. Unplug each monitor power cable at both ends:
   - monitor side
   - AC / power-strip side
5. Turn off the laptop or desktop source computer.

### Reinstall / Power Up Everything

1. Plug power cables, DisplayPort cables, and USB-C cables back into the monitors first.
2. Do not connect the laptop USB-C cable yet if using the laptop path.
3. Turn the power strip on.
4. Turn on both monitors at the same time using their physical power buttons.
5. Confirm P2725DE OSD settings:
   - Display > MST = On
   - Display > USB-C Prioritization = High Resolution / four-lane mode
6. Confirm P2225D OSD setting:
   - Input Source = DisplayPort
7. Attach the laptop to USB-C if using the laptop path.
8. Boot the source computer.
9. Use Windows display switching:
   - Win+P > Second screen only
   - Then switch to extend display

## Resolution Guidance

For the Dell desktop tower:

- Preserve QHD on the P2725DE and HD on the P2225D if the chain works in that mode.
- The desktop has previously been powerful enough for this setup through DisplayPort daisy chaining.

For the Lenovo laptop:

- If the P2225D shows no DisplayPort signal while the P2725DE is at QHD, lower the P2725DE to HD.
- Set the P2725DE refresh rate to 60 Hz.
- Set the P2225D to HD.
- The source note says "1900x1080"; if Windows shows "1920x1080" instead, treat that as the likely HD option and mention the discrepancy.

## Response Style

When helping the user:

1. Preserve the user's current goal: productive work on the personal desktop is the priority.
2. Keep the workflow concrete and sequential.
3. Separate reversible software settings from physical cable and power reset steps.
4. Call out when a step applies only to the laptop path or only to the desktop path.
5. Avoid replacing the known-good original cables unless the user reports new cable damage or a failed cable-specific test.
6. If suggesting external research, target Dell manuals or official support pages for the exact P2725DE and P2225D models.
