---
name: isometric-asset-sheets
description: Generate sprite sheet images for the isometric city game using the GenerateImage tool. Use when creating new game assets, sprite sheets, vehicle sprites, building sprites, or any visual assets for the isometric city builder. Ensures consistent format, sizing, and isometric projections.
---

# Isometric Asset Sheet Generation

Generate consistent sprite sheets for the isometric city game using the GenerateImage tool.

## Standard Format

All asset sheets follow this format:
- **Size**: Square, max width and height
- **Background**: Solid red (#FF0000), no variation in red tone
- **Grid**: 6 rows x 5 columns (30 cells total)
- **Style**: Hyper-realistic
- **Lighting**: No shadows

## Grid Layout

Each row represents ONE complete asset (vehicle, building, etc.):

| Column | View |
|--------|------|
| 1 | Isometric facing **North West** |
| 2 | Isometric facing **North East** |
| 3 | Isometric facing **South East** |
| 4 | Isometric facing **South West** |
| 5 | Special view (varies by asset type) |

### Special Views by Asset Type

| Asset Type | Column 5 View |
|------------|---------------|
| Airplanes | Gears down, head-first isometric (landing approach) |
| Helicopters | Top-down rotor view |
| Vehicles/Cars | 3/4 front isometric |
| Boats | Docked/stationary view |
| Trains | Front cab view |

## Prompt Template

```
Using the same format as [reference if available] - red background, 6 rows, 5 columns - I need you to make a new asset sheet with [ASSET TYPE] for my isometric city game. 

Each row should be ONE [ASSET]. The first 4 items should be the [ASSET] isometrically projected 4 times for flying/facing north west, north east, south east, and then south west. The last one should be [SPECIAL VIEW DESCRIPTION].

ALL [ASSETS] SHOULD BE HYPER REALISTIC. [CATEGORY DESCRIPTIONS BY ROW].

NO SHADOWS. [ADDITIONAL CONSTRAINTS]. Full size, 2048x2048 square.
```

## Example Prompts

### Airplanes

```
Using the same format as this image - red background, 6 rows, 5 columns - I need you to make a new asset sheet with AIRPLANES for my isometric city game. 

Each row should be ONE PLANE. The first 4 items should be the airplane isometrically projected 4 times for flying north west, north east, south east, and then south west. The last one should be a gears down head-first isometric view.

ALL PLANES SHOULD BE HYPER REALISTIC. Commercial or private jets. First 3 rows commercial airliners.

NO SHADOWS. For the first 4, NO LANDING GEAR. Full size, 2048x2048 square.
```

### Ground Vehicles

```
Red background, 6 rows, 5 columns - asset sheet with VEHICLES for my isometric city game.

Each row should be ONE VEHICLE. The first 4 items should be the vehicle isometrically projected facing north west, north east, south east, and then south west. The last one should be a 3/4 front isometric view.

ALL VEHICLES SHOULD BE HYPER REALISTIC. Row 1-2: sedans. Row 3-4: SUVs. Row 5-6: trucks.

NO SHADOWS. Full size, 2048x2048 square.
```

### Boats/Ships

```
Red background, 6 rows, 5 columns - asset sheet with BOATS for my isometric city game.

Each row should be ONE BOAT. The first 4 items should be the boat isometrically projected facing north west, north east, south east, and then south west. The last one should be a docked/stationary overhead isometric view.

ALL BOATS SHOULD BE HYPER REALISTIC. Row 1-3: small boats (fishing, sailboat, speedboat). Row 4-6: larger vessels.

NO SHADOWS. NO WATER/WAKE. Full size, 2048x2048 square.
```

## Asset Constraints

| Asset Type | Constraints |
|------------|-------------|
| Airplanes | No landing gear (flying views), no contrails |
| Helicopters | Rotors visible, no motion blur |
| Vehicles | Wheels visible, no reflections |
| Boats | No water, no wake effects |
| Buildings | Consistent lighting angle |

## Row Organization

Organize rows by category/size:

- **Vehicles**: Small to large, or by type (sedans, SUVs, trucks)
- **Airplanes**: Commercial (rows 1-3), private (rows 4-6)
- **Buildings**: Similar style/era per row
- **Nature**: Trees grouped by season or type

## After Generation

Once the asset sheet is generated:
1. Save to `/public/assets/` with descriptive name
2. Follow the [adding-asset-sheets guide](../../../skills/adding-asset-sheets.md) to integrate
3. Configure in `renderConfig.ts` with correct row/column mappings

## Common Issues

| Problem | Solution |
|---------|----------|
| Inconsistent sizing | Specify "same size for all assets" |
| Shadows appearing | Explicitly state "NO SHADOWS" |
| Wrong projections | Reference compass directions (NW, NE, SE, SW) |
| Cut-off assets | Add "centered in each cell" to prompt |
