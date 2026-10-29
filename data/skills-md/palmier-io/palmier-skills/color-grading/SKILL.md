---
name: color-grading
description: Color grade clips the way a professional colorist does — normalize, balance, match, then build a look — using inspect_color scopes and apply_color (exposure, white balance, wheels, curves, hue curves, LUTs). Use when the user asks to color, grade, match shots, fix white balance, fix exposure, neutralize a cast, or apply a look/film stock.
---

Grade in the colorist's order, scopes-first — never skip to a look, since a look on top of a cast just bakes it in. One `apply_color` call **merges** onto the current grade (only the params you pass change), so build up across calls and verify with `inspect_color` between stages. Ranges live in the reference tables below; prose names the knob, not the number.

## Workflow

```
- [ ] 1. inspect_color — read scopes BEFORE touching anything
- [ ] 2. Normalize — exposure + white balance to neutral
- [ ] 3. Primary — black/white points, contrast, saturation
- [ ] 4. Match — pull each shot toward the reference (if matching)
- [ ] 5. Secondary — hue curves for skin/sky/foliage
- [ ] 6. Look — wheels split-tone and/or LUT
- [ ] 7. inspect_color again — confirm scopes moved as intended
```

**1. Read first.** `inspect_color(clipId)`. Check `luma.black`/`luma.white` (near 0/1? `clipLowPct`/`clipHighPct` flag crush/clip), `balance.warmCool` + `balance.greenMagenta` (nonzero = a cast to neutralize), `zones` (where the cast lives), and `hueHistogram12` (orange bins 1–2 = skin, cyan/blue bins 6–8 = sky).

**2. Normalize.** `exposure` for global brightness (prefer it over gamma). `temperature` to correct `warmCool` — higher = warmer, so lower it if too warm. `tint` to correct `greenMagenta`, pushing opposite the cast. Re-inspect: both balances near 0 before moving on.

**3. Primary.** `blacks`/`whites` to set the points, `contrast` + `highlights`/`shadows` to shape roll-off, `saturation` for overall sat — reach for `vibrance` instead when you want to boost muted color without clobbering skin.

**4. Match shots.** Grade the hero fully, then for each other shot call `inspect_color(clipId, reference: <hero>)`, read the returned `gap` and its `hints` (e.g. "warmer than ref → cooler temperature"), apply the nudges, and repeat until the `gap` is small. Close it numerically — don't eyeball it.

**5. Secondary.** Adjust specific hues via `hueCurves.targets` (each `targetHue` affects ~±22°): `hueShift` rotates, `satScale` mutes/pops, `lumShift` darkens/brightens — e.g. deepen a sky without touching skin. Per-channel `redCurve`/`greenCurve`/`blueCurve` are tone-selective: tame a blown sky with `blueCurve: [[0,0],[0.7,0.7],[1,0.85]]`.

**6. Look.** Split-tone with the wheels (`*Hue`+`*Amount` per zone, e.g. teal/orange = `shadowsHue:210,shadowsAmount:0.2` + `highsHue:30,highsAmount:0.15`), add a film toe via `masterCurve` (`[[0,0.06],[1,0.95]]`), or fold in a `lut:{path,strength}` (`.cube`, absolute path; copied into project storage; pass `strength` alone to re-blend). For named stocks, build by hand — see **Film looks** below.

**7. Confirm.** Re-`inspect_color`: points near 0/1 without heavy clipping, neutral balance unless intentionally toned, skin in the orange bins.

## apply_color reference

Merges onto the current grade; `reset:true` starts neutral. `clipIds` required (video/image only).

| Group | Params | Range | Notes |
| :-- | :-- | :-- | :-- |
| Tone | `exposure` / `contrast` | −3…3 EV / 0.5–1.5 | 1 = neutral contrast |
| | `highlights` `shadows` `blacks` `whites` | −1…1 | points & roll-off |
| White balance | `temperature` / `tint` | 2000–11000 K / −100…100 | higher = warmer; +tint green, −magenta |
| Saturation | `saturation` / `vibrance` | 0–2 / −1…1 | 1 = neutral; vibrance protects skin |
| Wheels (per zone) | `shadowsHue`/`midsHue`/`highsHue` + matching `*Amount` | 0–360° / 0–1 | hue push + strength |
| | `shadowsLum` / `midsGamma` / `highsGain` | −0.5…0.5 / 0.5–2 / 0.5–1.5 | per-zone brightness |
| Curves | `masterCurve` `redCurve` `greenCurve` `blueCurve` | `[[x,y],…]` 0–1 | master preserves chroma |
| Hue curves | `hueCurves.targets[]` = `{targetHue, hueShift, satScale, lumShift}` | ±30° / 0–2 / ±0.5 | ~±22° selectivity |
| LUT | `lut` = `{path, strength}` | strength 0–1 | `.cube`, abs path |

Hues: 0 red · 30 orange/skin · 60 yellow · 120 green · 180 cyan · 210 sky-blue · 240 blue · 300 magenta.

`inspect_color(clipId | mediaRef, atFrame?, reference?)` — `clipId` reads a clip's **graded** look, `mediaRef` a **raw** asset. Returns scopes (`luma`, `meanRGB`, `zones`, `saturation`, `balance`, `hueHistogram12`, `colorfulPct`) + the frame; with `reference`, also a `gap` and actionable `hints` (the backbone of shot matching).

## Film looks (no LUT)

A LUT just freezes a set of curve/wheel/saturation moves — build any of them by hand, in this order:

1. **Tone curve (toe + shoulder).** The biggest tell: film never hits pure black or clips white. Lift the `masterCurve` toe and roll off its shoulder with gentle mid-S, e.g. `[[0,0.04],[0.25,0.22],[0.75,0.82],[1,0.97]]`.
2. **Per-channel crosstalk.** Hue shifts with brightness — what separates real emulation from "S-curve + a tint." Lift the **blue** toe and pull its shoulder → teal shadows + warm highlights (`blueCurve: [[0,0.05],[0.5,0.5],[1,0.92]]`); nudge green mids for Fuji.
3. **Split-tone** the wheels (shadows→teal, highlights→amber).
4. **Saturation sculpting** — `vibrance` over flat `saturation`, plus `hueCurves` `satScale` to mute/boost individual hues.
5. **Hue rotation** — small hue-vs-hue shifts (≤8°): Kodak warms oranges, Fuji greens.

The recipes below are this method with the dials pre-set — apply onto an already-normalized clip, then re-`inspect_color` and tune toward the shot (scale `*Amount` and curve deviations toward neutral for less intensity). If the user has the real `.cube`, prefer `lut:{path,strength:0.85}`; these approximate a stock's character, not its science.

**Kodak 2383 — Hollywood print** (warm, contrasty; dense blacks, teal shadows, amber highlights):
```json
{ "contrast": 1.25, "saturation": 1.15, "vibrance": 0.1, "temperature": 6800, "blacks": -0.1, "whites": 0.05,
  "shadowsHue": 195, "shadowsAmount": 0.12, "highsHue": 40, "highsAmount": 0.12, "masterCurve": [[0,0.02],[0.25,0.21],[0.75,0.83],[1,0.98]] }
```
**Kodak 2389 — low-con print** (clean, neutral; filmic roll-off, little tone):
```json
{ "contrast": 1.08, "saturation": 1.03, "temperature": 6550, "blacks": -0.04, "highsHue": 45, "highsAmount": 0.06, "masterCurve": [[0,0.015],[0.3,0.29],[0.7,0.72],[1,0.99]] }
```
**Fuji Eterna / 3513-like** (soft, green-pastel; milky lifted blacks). The lifted toe is the signature — don't flatten it:
```json
{ "contrast": 1.05, "saturation": 0.95, "vibrance": 0.12, "temperature": 6300, "blacks": 0.08, "shadows": 0.1, "highlights": -0.15, "whites": -0.04,
  "midsHue": 120, "midsAmount": 0.08, "shadowsHue": 185, "shadowsAmount": 0.1, "masterCurve": [[0,0.06],[0.25,0.27],[0.8,0.82],[1,0.95]] }
```
**Kodak Portra — warm negative** (soft, skin-flattering). The −tint + orange curve flatters skin — confirm the orange bins grew, not the reds:
```json
{ "contrast": 1.05, "saturation": 1.0, "vibrance": 0.15, "temperature": 6900, "tint": -3, "blacks": 0.06, "highlights": -0.1, "highsHue": 38, "highsAmount": 0.08,
  "hueCurves": { "targets": [ { "targetHue": 30, "satScale": 1.08, "hueShift": -4 } ] } }
```
**Bleach bypass** (desaturated, high-contrast, metallic). Scale `saturation` 0.4–0.7 for intensity:
```json
{ "contrast": 1.35, "saturation": 0.55, "temperature": 6300, "tint": 5, "blacks": -0.15, "whites": 0.1, "masterCurve": [[0,0.0],[0.2,0.13],[0.8,0.9],[1,1.0]] }
```
**Teal & orange — blockbuster** (cool shadows, warm skin). Keep the orange curve modest so faces don't go radioactive:
```json
{ "contrast": 1.2, "saturation": 1.1, "vibrance": 0.15, "shadowsHue": 210, "shadowsAmount": 0.2, "highsHue": 30, "highsAmount": 0.15,
  "hueCurves": { "targets": [ { "targetHue": 30, "satScale": 1.15 } ] } }
```
**Vintage / faded** (milky blacks, low sat, warm-yellow age). The high toe is the whole look — blacks never reach 0:
```json
{ "contrast": 0.95, "saturation": 0.8, "temperature": 6700, "tint": 4, "blacks": 0.12, "highlights": -0.1, "masterCurve": [[0,0.1],[0.5,0.52],[1,0.92]] }
```

## Notes
- `apply_color` is the colorist path and folds in LUT + curves + hue curves as live, editable effects. `apply_effect` is for generic, non-color FX — don't grade with it.
- `get_timeline` exposes each graded clip's `color` object in the same vocabulary — pass that object as `apply_color({ clipIds, color })` to **copy** a whole grade (replaces; mutually exclusive with knobs/`reset`).
- Mutations return timeline deltas (including updated `color`) — patch from those; don't re-read the whole timeline after every nudge.
- Trust scopes over the preview for balance — monitors and JPEGs lie about subtle casts; use the frame for composition/look judgment.
- `lumShift` is an additive HSV value shift in display space, not a linear luma divide, so per-hue darkening won't amplify shadow macroblocks.
- Curve points are piecewise-linear, clamped flat outside their range — include endpoints near `[0,0]`/`[1,1]` unless you mean to clip.
