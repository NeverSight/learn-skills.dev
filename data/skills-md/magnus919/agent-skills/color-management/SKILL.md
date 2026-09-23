---
name: color-management
description: >-
  Manage color workflows with ICC profiles, working spaces, gamut mapping, and color
  science. Use when inspecting ICC profiles, converting between color spaces, checking
  gamut clipping, validating well-behaved working spaces, or troubleshooting color
  workflow issues with ImageMagick, ArgyllCMS, Exiftool, or LittleCMS. Do not use this
  skill for unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: CLI tools used (ImageMagick, Exiftool, ArgyllCMS, LittleCMS) are platform-independent; Python scripts require Python 3.8+
metadata:
  spec-version: "1.0"
  source: Distilled from ninedegreesbelow.com (Elle Stone) and Bruce Lindbloom's color science resources
  version: "1.0.0"
---

# Color Management Skill

Expert-level guidance for ICC profile color management in open-source workflows. Covers color science fundamentals, working space selection, ICC profile operations, gamut analysis, and practical tool usage.

## Quick Reference

| If you need to... | Load this reference | Run this script |
|------------------|-------------------|-----------------|
| Understand CIELAB, xyY, or color science basics | `references/color-management-overview.md` | — |
| Inspect an ICC profile's metadata/primaries/TRC | — | `scripts/icc-profile-inspect.py` |
| Check if a profile is well-behaved (neutral gray axis) | `references/working-spaces-reference.md` | `scripts/well-behaved-check.py` |
| Convert images between color spaces | `references/icc-profile-operations.md` | `scripts/color-space-convert.py` |
| Check which image colors exceed a color space gamut | `references/soft-proofing-workflow.md` | `scripts/gamut-check.py` |
| Compare sRGB profile variants | `references/working-spaces-reference.md` | `scripts/srgb-compare.py` |
| Calculate color difference (dE) between two images | — | `scripts/color-difference.py` |
| Soft proof an image before conversion | `references/soft-proofing-workflow.md` | `scripts/gamut-check.py` |
| Calibrate and profile a monitor | `references/monitor-calibration-workflow.md` | — |
| Process raw files with dcraw | `references/dcraw-pipeline.md` | — |
| Understand hex quantization and create well-behaved profiles | `references/hex-quantization-and-profile-creation.md` | `scripts/well-behaved-check.py` |
| Generate a comprehensive color analysis report | — | `scripts/color-report.py` |
| Set up a GIMP LCH layer stack for separate tonality/color editing | `assets/templates/lch-layer-stack.md` | — |
| Extract embedded ICC profile from an image | `references/icc-profile-operations.md` | `scripts/icc-profile-inspect.py` |
| Understand conversion intents (relative/absolute/perceptual) | `references/color-management-overview.md` | — |
| Set up Firefox for color-managed browsing | `references/tool-reference.md` | — |

## Required Tools

The scripts in this skill check for these tools and report if missing. Install what you need:

- **ImageMagick** (`convert`, `identify`, `compare`, `composite`) — primary image processing
- **Exiftool** — metadata and ICC profile extraction
- **ArgyllCMS** (`xicclu`, `iccgamut`, `colprof`, `cctiff`) — professional color management
- **LittleCMS** (`tificc`, `transicc`) — ICC profile conversions

```bash
# macOS
brew install imagemagick exiftool argyllcms littlecms

# Debian/Ubuntu
sudo apt install imagemagick libimage-exiftool-perl argyll littlecms2

# Fedora
sudo dnf install ImageMagick perl-Image-Exiftool ArgyllCMS littlecms2
```

## Python Scripts

All scripts are in `scripts/`. They require Python 3.8+ with these optional dependencies:

```bash
pip install numpy colour-science Pillow  # optional but recommended
```

Each script has a `--help` flag:

```bash
python3 scripts/icc-profile-inspect.py --help
python3 scripts/well-behaved-check.py --help
```

## Gotchas

### sRGB profile variants
There is no single "sRGB" ICC profile. Different vendors produce profiles that differ in D50 adaptation, hexadecimal quantization, and TRC encoding. The ArgyllCMS `sRGB.icm` and the colord `Shared sRGB.icm` are both well-behaved; the Adobe/color.org/Windows 2000 variants are *not* well-behaved (they produce a false magenta cast at high bit depths). See `references/working-spaces-reference.md` and `scripts/srgb-compare.py`.

### Matrix profiles cannot use perceptual intent
sRGB, AdobeRGB, ProPhotoRGB, and all other matrix working space profiles do NOT support perceptual or saturation intents. When you select perceptual intent for a matrix destination profile, you actually get relative colorimetric (which clips out-of-gamut colors). The "perceptual keeps all colors" mantra only applies when converting *to* LUT profiles (printer profiles, some monitor profiles).

### Perceptual intent for sRGB is a lie
The oft-repeated statement "perceptual intent preserves colors when converting to sRGB" is false. sRGB is a matrix profile; it has no perceptual intent table. What actually happens is relative colorimetric intent, which clips. The only way to preserve out-of-gamut colors at floating point is to use LCMS2 unbounded mode.

### Display-referred vs scene-referred
- **Display-referred**: RGB values bounded by 0.0-1.0. White (1,1,1) = maximum display brightness. ~9 stops dynamic range. Operations clamp.
- **Scene-referred**: No upper bound on RGB values. White has no special significance. 20+ stops possible (OpenEXR). Requires linear gamma. Operations do NOT clamp.
Always check which model your editing pipeline uses.

### Unbounded editing has limits
LCMS2 unbounded mode prevents clipping during conversions by allowing negative and >1.0 RGB values. This is useful for storage and transport, but many editing operations (Multiply, Divide, Screen, Levels gamma slider, Curves, color correction) produce *meaningless results* on out-of-gamut colors. Use integer precision if you don't want to manage out-of-gamut values.

### Luminance vs Luma is not pedantry
- **Luminance**: calculated on linearized RGB (radiometrically correct). Uses sRGB-specific multipliers (R*0.213 + G*0.715 + B*0.072).
- **Luma**: calculated on gamma-encoded RGB (perceptually uniform). Different multipliers (R*0.222 + G*0.717 + B*0.061 for GIMP 2.9+, Bradford-adapted to D50).
GIMP 2.8 used wrong multipliers. GIMP 2.9+ corrected them. Always use Luminance for physically meaningful black/white conversions.

### Camera profiles require negative tristimulus values
Every digital camera sensor needs negative XYZ tristimulus values in its input matrix profile (analysis of 233 dcraw cameras: 100% had negative green Z, 93% had negative blue Y). ICC V2 prohibited these; V4 allows them via 32-bit floating point. If your workflow clips negative values, you lose blue and green channel detail.

### 8-bit vs 16-bit vs floating point
- **8-bit**: Use only sRGB or AdobeRGB (small gamut, perceptually uniform TRC). Never use linear gamma (posterization in shadows).
- **16-bit integer**: ProPhotoRGB is usable. Linear gamma is OK for radiometrically correct editing.
- **32-bit floating point**: Any working space, any TRC. Unbounded conversions possible. Required for scene-referred HDR.

### LCH vs HSV is not an upgrade — it's a replacement
HSV is a 1960s "fast math" hack for slow CPUs. It cannot separate color from tonality. LCH (Lightness, Chroma, Hue) is derived from CIELAB and allows true separate editing of color and tonality. GIMP's LCH blend modes are the first correct implementation in open-source software. Never use HSV blend modes for serious editing.

### Concrete failure: Levels gamma slider + unbounded sRGB = disaster
If you take a ProPhotoRGB image with saturated reds, convert it to unbounded sRGB at 32-bit float, and apply a Levels gamma slider adjustment (e.g., gamma=3.0), the reds turn *magenta* and any chrome in the image turns *cyan*. This is because the gamma slider is chromaticity-dependent — it multiplies channels differently in different working spaces. The fix: do gamma adjustments in the same working space the image was edited in, or use a chromaticity-independent operation like Value channel Levels.

### Concrete failure: Color correction in the wrong working space
If an image was given a green color cast in the ProPhotoRGB color space, and you correct it in unbounded sRGB using the white balance eyedropper, the correction produces: cyan grass, orange skin tones, saturated sky, and a saturated red truck in the distance. Even though the white point dot itself turns neutral, all other colors are wrong. Color correction must be performed in the same color space in which the cast was created. Converting to a different space and correcting produces unpredictable results.

### Concrete failure: Channel-based mono mixing with out-of-gamut colors
Converting a yellow truck from its camera input profile to sRGB drives the blue channel negative over most of the yellow truck body. If you then try to use Channel Mixer (Mono Mixer) to create a black-and-white conversion by blending from the blue channel, the negative blue channel values produce completely meaningless results — you can't emulate orthochromatic film or any other channel-based effect on colors that are out of gamut.
Channel-based editing must be done before converting to a smaller gamut, or in a working space large enough to contain all image colors.

## References

| File | When to load |
|------|-------------|
| `references/color-management-overview.md` | You need to understand CIELAB, xyY, color science fundamentals |
| `references/icc-profile-operations.md` | You need to convert, assign, extract, or create ICC profiles |
| `references/tool-reference.md` | You need CLI commands for ImageMagick, ArgyllCMS, Exiftool, LCMS |
| `references/working-spaces-reference.md` | You need working space data (primaries, white points, gamma values) |
| `references/glossary.md` | You encounter an unfamiliar term |
| `references/soft-proofing-workflow.md` | You need to soft proof before conversion |
| `references/monitor-calibration-workflow.md` | You need to calibrate or profile a monitor |
| `references/dcraw-pipeline.md` | You're working with raw files and need a color-managed pipeline |
| `references/hex-quantization-and-profile-creation.md` | You need to create well-behaved ICC profiles |

## Assets

| File | Description |
|------|-------------|
| `assets/templates/icc-profile-report.md` | Template for a human-readable ICC profile analysis report |
| `assets/templates/lch-layer-stack.md` | GIMP LCH layer group template for separate tonality/color editing |
