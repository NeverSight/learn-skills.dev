---
name: davinci-resolve-troubleshooting
description: Use when DaVinci Resolve is broken in some specific way — red playback indicator, missing media, clips offline, audio out of sync, GPU/render crashes, or render queue stuck. Triggering symptoms include phrases like "Resolve is dropping frames", "media offline", "clips show red diagonal", "audio drifts", "Resolve crashes when rendering", "GPU error", or any DaVinci Resolve "why is X broken" question.
---

# DaVinci Resolve — troubleshoot the 5 most common breakage modes

## Overview

A diagnostic protocol for the five problems that account for ~90% of DaVinci Resolve support questions: dropped-frame playback, missing media, audio sync drift, render crashes, and render queue stalls. The principle: **diagnose before you fix**. Treat the red indicator as data, not a verdict.

## When to use

Symptoms:
- Red GPU/playback indicator during playback
- Clips show a red diagonal slash (offline media)
- Audio drifts out of sync over time
- Resolve crashes mid-render or after a few minutes of rendering
- Render queue says "complete" but the output file is missing or 0 bytes
- "Why is X broken in Resolve" — any of these.

When NOT to use:
- Resolve will not launch at all — that is an install issue (see `davinci-resolve-setup`).
- You are getting a license error — contact Blackmagic support.
- The problem is creative ("I do not like how my edit looks") — not a troubleshooting problem.

## Quick reference — the five diagnostic flows

| Symptom | First check | Then |
|---|---|---|
| Red playback indicator | Run Blackmagic Disk Speed Test on your media drive | If drive is fast enough, generate proxies |
| Clips offline (red diagonal) | Right-click clip > Relink Media | Or change source folder for the bin |
| Audio out of sync | Confirm timeline frame rate matches source frame rate | Use Auto-Sync (waveform or timecode) |
| Crashes during render | Reduce render parallelism, disable hardware acceleration | Check Console for the exact error |
| Render queue stalled at 0% | Check disk space on output drive | Check Custom Export filename for invalid chars |

## Steps — diagnostic flow per problem

### Problem 1: Red playback indicator (dropped frames)

The indicator at the top of the source/timeline viewers turns red when Resolve cannot sustain real-time playback.

**Step 1.1** — Identify the bottleneck. Is it the **drive** or the **GPU**?

- Open **DaVinci Resolve > Preferences > System > Memory and GPU**. Check GPU usage during playback.
- If GPU is below 80% during playback, the bottleneck is the **drive** (read speed).
- If GPU is pinned at 100%, the bottleneck is the **GPU** (rare for talking-head content; common for 4K + heavy color grading).

**Step 1.2** — If the drive is the bottleneck, run Blackmagic Disk Speed Test:

- Free app, install from Mac App Store (macOS) or Desktop Video installer (Windows).
- Point it at your media drive. Look at the "Will It Work?" table. Confirm green checkmarks for your codec at your resolution and frame rate.
- If the drive cannot sustain the required read speed, you have two options:
  1. Move media to a faster drive (NVMe SSD, Thunderbolt).
  2. Generate proxies (see step 1.3).

Editor's Guide p. 326 details Blackmagic Disk Speed Test usage.

**Step 1.3** — Generate proxies if you cannot upgrade the drive.

- In the Media Pool, right-click your clips > **Generate Proxy Media**.
- Choose a proxy format: **H.264 Half-Res 1080p** is a good default for editing.
- Wait for proxies to generate.
- Switch the **Proxy Handling** menu at the top of the viewer to **Prefer Proxies**.
- Playback should now be green.

**Step 1.4** — Before delivery, switch back to camera originals:

- **Proxy Handling > Prefer Camera Originals**. Resolve renders from the high-quality sources, not the proxies.

Editor's Guide pp. 324-337 covers the full proxy workflow including the Blackmagic Proxy Generator separate app.

**The misconception this addresses**: "Red indicator means my computer is too slow." Often it means the drive is too slow, not the GPU. Diagnose first.

### Problem 2: Clips offline (red diagonal slash)

A red diagonal across a clip thumbnail in the Media Pool or timeline means Resolve cannot find the source file at the path it was indexed at.

**Step 2.1** — Determine if it is one clip or all clips.

- If **all clips** in a bin are offline, the source folder has moved or the drive is unmounted.
- If **one or two clips** are offline, those specific files have been moved/renamed.

**Step 2.2** — For all clips offline (typical case: project moved to a new machine):

- Right-click the affected bin > **Change Source Folder**.
- Browse to the actual current location of the media on this machine.
- Click Change. All clips in the bin re-link in one operation.

Editor's Guide p. 336 shows Clip Operations > Change Source Folder.

**Step 2.3** — For individual offline clips:

- Right-click the clip > **Relink Selected Clips**.
- Browse to the file. Resolve relinks just that clip.

**Step 2.4** — If the file genuinely no longer exists:

- Check your backup folder (`davinci-resolve-setup` covers the backup folder location).
- Or check `~/.Trash` / Recycle Bin if you may have deleted it.
- If the file is truly gone, you may need to re-shoot or re-export from the source.

### Problem 3: Audio drifts out of sync

The audio is in sync at the start but drifts over time (e.g. 1 second off after 10 minutes).

**Step 3.1** — Confirm the source clip frame rate matches the timeline frame rate.

- Right-click the source clip in the Media Pool > **Clip Attributes**.
- Note the clip's Frame Rate.
- File > Project Settings > Master Settings > **Timeline frame rate**. Confirm it matches.
- If they differ (e.g. clip is 29.97 fps but timeline is 24 fps), Resolve will interpret the audio differently. This is the most common cause of drift.

**Step 3.2** — Check audio sample rate.

- Clip Attributes > Sample Rate (typically 48000 Hz).
- Project Settings > Master Settings > Sample Rate. Match them.

**Step 3.3** — If video and audio were recorded separately (dual-system audio), re-sync them.

- In the Media Pool, select the video and audio clips together.
- Right-click > **Auto Sync Audio**.
- Choose **Based on Waveform** (works without timecode) or **Based on Timecode** (faster if both have matching timecode).
- Resolve aligns the two clips into a single synced clip.

Editor's Guide pp. 267-277 covers the audio sync workflow.

**Step 3.4** — For drift caused by drifting hardware clocks (e.g. external audio recorder vs camera):

- Use the **Stretch** parameter on the audio clip in the Inspector to slow/speed by tiny amounts (0.5% or less).
- Or split the audio into multiple sections and re-sync each section.

### Problem 4: Resolve crashes during render

**Step 4.1** — Check the Console for the actual error.

- **Workspace > Console** opens the Console panel.
- Look at the last messages before the crash. Common causes:
  - "Out of memory" — reduce render frame rate or close other apps
  - "GPU error" — disable hardware decoding (see 4.2)
  - "File system error" — disk full or drive disconnected

**Step 4.2** — Disable hardware acceleration if you see GPU errors.

- **Preferences > Decode Options** > uncheck **Decode H.264/H.265 using hardware acceleration**.
- This is slower but more stable, especially on older or mixed-GPU systems.

**Step 4.3** — Reduce render concurrency.

- Some Resolve crashes during render are caused by trying to use both GPUs (in a dual-GPU machine).
- **Preferences > System > Memory and GPU** > set GPU processing mode to **CUDA** or **Metal** explicitly (not Auto).
- Restart Resolve.

**Step 4.4** — Free disk space.

- Renders need 2-3x the source file size as scratch during processing.
- Check that both your media drive and your output drive have at least 50 GB free.

### Problem 5: Render queue stalls at 0%

A render shows "Render in Progress" but the file size on disk does not grow.

**Step 5.1** — Check the output filename for invalid characters.

- macOS file systems do not allow `:` in filenames. Windows does not allow `< > : " / \ | ? *`.
- If your render preset has `%timeline_name` and your timeline name contains a colon or slash, the render will silently fail.
- Rename the timeline first, or change the Custom Export filename to use plain characters.

**Step 5.2** — Confirm the output folder exists and is writable.

- Check the **Location** field in Render Settings. Browse to it manually in Finder/Explorer.
- If it does not exist, create it.
- If it exists but is owned by another user, change permissions or pick a different location.

**Step 5.3** — Reduce the render frame range.

- If a specific clip is corrupted, the render hangs on that frame.
- In Render Settings, change **Render** from "Entire Timeline" to "In/Out Range" and set an Out point before the suspected bad frame.
- If that completes, walk forward by a few seconds at a time to find the problem frame.

**Step 5.4** — Restart Resolve.

- If all the above fail, kill Resolve (Force Quit on macOS, Task Manager on Windows) and reopen the project. Render queue often stalls after a long session and a restart clears it.

## Common mistakes

- **Assuming red indicator = old computer** -> often it is the drive, not the GPU. Diagnose with Blackmagic Disk Speed Test first. **(This is the misconception this skill addresses head-on.)**
- **Re-importing offline clips instead of relinking** -> you lose all your edits if you re-import. Always relink.
- **Letting Resolve auto-select GPU in dual-GPU systems** -> manually set it to CUDA or Metal explicitly. Auto can cause crashes.
- **Naming timelines with colons or slashes** -> renders silently fail. Stick to alphanumerics, underscores, dashes.

## Verification

You succeeded if all of the following are true:

1. Playback indicator is green during a 30-second play-through of your timeline.
2. Every clip in your Media Pool has a thumbnail (not a red diagonal).
3. Audio waveform aligns with video action throughout the timeline (clap on the slate matches the slate visual; mouth movements match speech).
4. Render completes and the output file is the expected size and duration.
5. You can identify which of the 5 problems applied (or no problem applied) by name.

## Transfer

Now try this when you encounter a *new* breakage mode — say, a Fusion comp that will not render correctly. Apply the same diagnostic protocol: (1) identify the symptom precisely, (2) check the Console for an actual error message, (3) reduce scope (render just that one Fusion comp segment) to isolate the cause, (4) test a fix on a copy before applying to the project. This problem-solving discipline scales beyond the five cases above.

## Working reference

- `docs/wiki/editors-guide.md#lesson-6--ai-workflows-pp-323-387` (Disk Speed Test, proxies, relink workflows — primary)
- `docs/wiki/editors-guide.md#lesson-5--project-organization-pp-245-321` (audio sync, frame-rate matching)
- `docs/wiki/colorist-guide.md#lesson-8--adjusting-image-properties-pp-343-379` (Render Cache for Color-page playback)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (every troubleshooting symptom row maps here)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports the diagnostic flow didn't fix the symptom (red playback returns, clips still offline, render still fails), read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 326 (Is Your Drive Fast Enough? — Blackmagic Disk Speed Test)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 324-340 (Generating Proxy Files — complete workflow including Blackmagic Proxy Generator)
- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 336 (Change Source Folder for bulk relink)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 267-277 (Syncing Audio to Video and Channel Configuration)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 597-617 (Customizing Deliver Presets, render failure causes)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 6-8 (Relinking the Media Files)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 350-364 (Syncing Audio to Video)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 369-377 (Optimizing Performance with Render Cache — for color page playback)
