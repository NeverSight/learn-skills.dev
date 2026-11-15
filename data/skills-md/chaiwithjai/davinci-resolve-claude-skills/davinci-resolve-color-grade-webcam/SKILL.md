---
name: davinci-resolve-color-grade-webcam
description: Use when a user wants webcam, interview, or talking-head footage to look broadcast-quality — corrects exposure, white balance, skin tones, and overall color. Triggering symptoms include phrases like "my webcam footage looks dull", "skin tones look orange/green", "wash out background", "make the face pop", "match shots from two cameras", or any DaVinci Resolve color page question for talking-head content.
---

# DaVinci Resolve — color grade webcam and talking-head footage

## Overview

Three primary corrections + one secondary on a skin-tone qualifier = footage that looks like it cost money. The core principle: **read the waveform scope, do not trust your laptop screen.** Laptop displays are uncalibrated; the scope tells you objectively whether the shadows are crushed or the highlights are clipped.

## When to use

Symptoms:
- Webcam footage looks dull, flat, or washed out
- Skin looks orange / green / too red
- Two cameras (e.g. your face cam and a co-host's) do not match
- Want a consistent "look" across episodes
- The phrase "make it look more professional"

When NOT to use:
- You are shooting RAW (.braw, .ari, .r3d) — that needs the **HDR Wheels** workflow (Colorist Guide pp. 393-406).
- You need to fix a green-screen shot — that is Fusion territory (Fusion VFX Guide ch. 5).
- The footage is already graded and you want to *match* it to a reference — that is a shot-matching workflow (Colorist Guide pp. 46-71).

## Quick reference

The grade is a 4-node tree on the Color page:

| Node | Job | Primary tool |
|---|---|---|
| **Node 1: Normalize** | Set black and white points using the waveform | Lift + Gain master wheels |
| **Node 2: Balance** | Neutralize color cast | Lift + Gain *color* wheels |
| **Node 3: Contrast** | Add midtone punch | Contrast + Pivot at the top of the Primaries palette |
| **Node 4: Skin tones** | Refine just the face | HSL Qualifier + a power window |

## Steps

### Prep — switch to the Color page and bring up the scopes

1. Press **Shift-6** to go to the Color page.
2. Click the **Scopes** palette button (right side of the page).
3. Set the scope dropdown to **Waveform** (this shows luminance and color channels stacked).
4. Select your first webcam clip in the thumbnail strip at the top.

The waveform is your truth source. Everything you do below should be visually verified on it.

### Node 1 — Normalize (set black and white points)

1. Confirm the **Primaries — Color Wheels** palette is active in the left panel.
2. Find the **Lift** wheel (leftmost). The horizontal slider below it is the **Lift master wheel**.
3. Drag the Lift master wheel left until the darkest area of the waveform sits just above the 0 line (around 5-10 % luminance, which is approximately the 64 line on a 1023-line scope).
   - For webcam footage shot in a normal room, this typically means dragging Lift down to around `-0.02 to -0.05`.
4. Find the **Gain** wheel (rightmost). Drag its master wheel until skin-tone highlights sit between 50-75% of the scope height.
   - Watch the highest peaks — you want them at roughly the 768 line on the 1023 scale.
5. Find the **Gamma** wheel (middle). Drag its master wheel right to brighten midtones so the face is well-lit but not blown out.
6. At the top of the Primaries palette, adjust **Contrast** to `1.1 - 1.2` and **Pivot** to `0.3` for a punchier mid-range.

Colorist Guide pp. 11-15 walks through this in detail.

### Node 2 — Balance (neutralize the color cast)

1. Right-click the node in the **Nodes** panel > **Add Node > Add Serial** to add Node 2.
2. Look at the waveform — the RGB channels should overlap (white trace) for neutral areas of the image. If you see a band of one color riding above the others, that is the cast.
3. Use the **Lift** *color wheel* (drag the center dot, not the master wheel) to push the shadows toward the *complementary* color of any cast you see.
   - If the shadows are too red (a common webcam issue from indoor lighting), drag Lift toward cyan.
   - If the shadows are too blue (daylight through a window), drag Lift toward yellow.
4. Do the same with the **Gain** *color wheel* for the highlights.
5. Use Resolve's **Qualifier Focus** trick: from the Scopes palette options menu, enable **Display Qualifier Focus**. Hover the mouse over a neutral area in the viewer (a white wall, a piece of paper) — the scope shows the RGB values under your cursor. Aim to get those three values to overlap (= neutral).

Colorist Guide pp. 16-19 covers this exact workflow.

### Node 3 — Contrast (already partially done in Node 1)

If you set Contrast in Node 1, you can skip this node. Some colorists prefer a dedicated contrast node so they can disable it independently. Up to you.

### Node 4 — Skin tone refinement (HSL Qualifier + Power Window)

This is the secret sauce. Even a perfectly balanced face benefits from a tiny saturation boost and slight warmth on the skin only.

1. Add Node 4 (right-click Node 3 > Add Serial).
2. In the left palette, switch from Primaries to **Qualifier**.
3. Set the qualifier mode to **HSL** (default).
4. Click the **eyedropper** in the Qualifier palette, then click on a clean patch of skin in the viewer.
5. Refine the selection by adjusting the Hue / Saturation / Luminance range sliders. Toggle the **Highlight** button (top of the viewer) to see the matte — you want only the skin selected.
6. Switch back to **Primaries**. Any adjustment now only affects the qualified skin.
7. Push **Gain color wheel** slightly toward orange (warmer skin). Increase **Saturation** to ~60 (default is 50).
8. To prevent the qualifier from triggering on background objects with skin-tone colors (wooden furniture, beige walls), add a **Power Window** in the Window palette > Linear or Circle shape > draw it loosely around the face. The qualifier + window combine — only skin *inside the window* gets the boost.

Colorist Guide pp. 118-138 covers the full skin-tone refinement workflow (Enhancing Skin Tones with Face Refinement uses the Studio-only AI face detector; the manual qualifier + window approach works on free Resolve).

### Save the node tree as a PowerGrade so you can reuse it

1. Right-click in the Gallery panel (bottom-left of Color page) > **Add to PowerGrade**.
2. Name the still `WEBCAM_LOOK_v1`.
3. To apply to a future clip: select the new clip, right-click the saved still in the Gallery > **Apply Grade**.

Colorist Guide pp. 246-250 covers saving grades for reuse.

## Common mistakes

- **Adjusting by eye on an uncalibrated laptop screen** -> the colors you see on a MacBook are not the colors your audience sees on their phone, TV, or monitor. Always check the waveform. The waveform does not lie.
- **Cranking Saturation to 70+** -> faces start to look orange and fake. Stay under 60. The Saturation control is in the Primaries palette options at the bottom.
- **Skipping Node 1 normalization and going straight to creative grading** -> you are stacking creative choices on top of broken footage. Always normalize first.
- **Using the same grade on footage shot under different lighting** -> a "WebcamLook" grade tuned for tungsten room lights will look wrong under daylight. Either re-grade per scene, or use the **Color Match** feature (Colorist Guide pp. 52-69) to use a color chart as reference.
- **Forgetting to disable the qualifier highlight after refining** -> the matte preview stays on and you cannot see your real adjustments. Press the Highlight button at the top of the viewer to toggle it off.

## Verification

You succeeded if all of the following are true:

1. **Scope check**: the waveform trace fills most of the 0-1023 range. The darkest part sits near 50-100 (not 0). The brightest part sits near 700-900 (not 1023, unless you have intentional specular highlights).
2. **RGB overlap check**: in a neutral area (white wall, paper), the R, G, B traces overlap to form a white trace.
3. **Skin check**: faces are not pulled toward orange / green / red.
4. **Before/after check**: press **Cmd-D** (or Ctrl-D) to toggle the grade on and off. The "after" should look noticeably more dimensional than the "before."
5. The saved PowerGrade still is in your Gallery and applies cleanly to a different clip.

## Transfer

Now try this: apply the same grade to a clip shot under daylight (natural window light). The Lift wheel adjustment will likely be smaller because daylight already pushes shadows toward blue. The Temp slider at the top of the Primaries palette may need to come down (cooler). Skin-tone qualifier should still work — but the Power Window may need to be redrawn if the face is at a different position in the frame.

## Working reference

- `docs/wiki/colorist-guide.md#lesson-1--balancing-footage-pp-3-43` (primary grading with wheels, scope reading — primary)
- `docs/wiki/colorist-guide.md#lesson-3--correcting-and-enhancing-isolated-areas-pp-73-139` (qualifier + window for skin tones)
- `docs/wiki/colorist-guide.md#lesson-6--managing-grades-across-clips-and-timelines-pp-225-259` (PowerGrade save/reuse)
- `docs/wiki/beginners-guide.md#lesson-4--performing-primary-color-corrections-pp-189-245` (gentle starter workflow)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (skin-tone and shot-match symptom rows)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports that skin tones still look orange/green, the grade is washed out, or RGB doesn't overlap on neutral patches, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 11-19 (Primary Grading with Color Wheels, normalization workflow)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 16-19 (Balancing Colors with Master Wheels, RGB overlap trick)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 118-138 (Skin-tone refinement, qualifier + window workflow)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 246-250 (Saving Still Templates for Other Projects — PowerGrade)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 12-15 (Setting Tonal Range with Master Wheels, scope reading)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 189-245 (Primary Color Corrections — alternative starter workflow)
