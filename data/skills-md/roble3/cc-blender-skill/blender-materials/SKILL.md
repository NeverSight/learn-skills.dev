---
name: blender-materials
description: Create and assign PBR materials in Blender via Principled BSDF — metals, glass, plastic, fabric, skin, organics. Covers physically-based material recipes with real-world values, Coat layer (varnish/car paint), Sheen (cloth), Subsurface scattering (skin/wax), Transmission (glass), and procedural patterns (wood grain, marble, fabric weave). Use whenever the user asks to "make it look like X material", "give it a metallic finish", "apply a wood texture", "make this glass / plastic / brushed steel / leather / skin", or any look-development request. Make sure to use this skill even if the user does not say "material" — also covers "make it shiny", "matte finish", "looks like copper", "rough surface". Works with any geometry; pairs with blender-lighting (materials only look right under proper lighting).
when_to_use: Any material assignment, PBR setup, shader work, or look-dev request in Blender.
allowed-tools: Read Bash mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info
---

# Blender Materials

Apply physically-based materials to objects. Use **only Principled BSDF** — it's the only shader that exports cleanly to glTF and matches what other DCC tools expect.

## The metallic switch — never an in-between

The single most-important rule: **Metallic is a switch, not a slider.** Set it to `0.0` (dielectric: plastic, wood, glass, skin) or `1.0` (metal: steel, gold, copper). Values between 0.2 and 0.8 are almost always wrong; they produce energy-non-conservative renders that look "plasticky."

Exception: dark mirror lenses (sunglasses) use ~0.8 to combine strong reflection with slight tint — that's a stylistic choice, not strict PBR.

## Decision tree

```
What is it made of?
├── Raw metal (steel, gold, copper, etc.)
│   → Metallic=1.0, Base Color = F0 reflectance from physicallybased.info
│   → Roughness controls polish (0.05 mirror → 0.4 brushed → 0.7+ weathered)
│
├── Glass / clear / refractive
│   → Metallic=0, Transmission=1.0, IOR=1.5 (glass), Roughness=0.0
│   → Add Volume Absorption for thick tinted glass
│
├── Plastic / wood / stone (dielectric, opaque)
│   → Metallic=0, IOR=1.45 (plastic) or 1.5 (most others)
│   → Roughness per finish (0.15 glossy / 0.6 matte)
│   → Coat Weight 0.5+ for varnished/lacquered surfaces
│
├── Skin / wax / marble (subsurface scattering)
│   → Metallic=0, Subsurface Weight=1.0
│   → Subsurface Radius RGB tuned per material (skin: red scatters deepest)
│
├── Cloth / fabric (sheen)
│   → Metallic=0, Sheen Weight 0.2-0.5
│   → Roughness 0.6+, Sheen Roughness 0.5
│
└── Mirror / chrome (special metal)
    → Metallic=1.0, Roughness=0.02-0.05, near-white base
```

## Reference-look handoff

If the goal is to match an original/reference image rather than make a generally attractive render, chain-load `reference-look-calibration`. It owns measurement of hue/saturation/value, object extent, glow/aura color, and before/after look metrics. This skill should then apply the requested material/lighting/render changes within that calibrated target.


## Recipes (the 12 to know)

Each recipe creates the material and assigns it to a target object. Replace `'GEO-target'` with your actual object name.

### `set_input` helper — required for some Blender 5.x BSDF inputs

In Blender 5.x's Principled BSDF v2, **two inputs are flagged `enabled=False`** in the data API: `Weight` and `Subsurface IOR`. These are reachable by **iteration or index** but **not by string-key lookup** — `bsdf.inputs['Subsurface IOR']` raises `KeyError` even though the input exists and its value is respected at render time. This is a Blender 5.x quirk surfaced during v0.4.0 → v0.5.0 validation.

Use this helper whenever a recipe sets an input that might be in the disabled-but-functional state. It works on every input (enabled or not) and is forward-compatible if more inputs become disabled in future Blender versions:

```python
def set_input(node, name, value):
    """Set a node input by name. Works on inputs with enabled=False
    that fail string-key lookup (e.g. 'Subsurface IOR' on Blender 5.x).
    """
    for inp in node.inputs:
        if inp.name == name:
            inp.default_value = value
            return True
    return False
```

For inputs that are reliably enabled (Base Color, Metallic, Roughness, IOR, Transmission Weight, Sheen Weight, etc.), direct string-key assignment still works fine — the helper is only required where an input is conditionally disabled. **Recipe 9 (Skin) uses it** because `Subsurface IOR` is one of the affected inputs.

### Recipe 1 — Brushed steel
```python
import bpy

mat = bpy.data.materials.new('MAT-steel_brushed')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.56, 0.57, 0.58, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.25

obj = bpy.data.objects['GEO-target']
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
print(f"material:MAT-steel_brushed→{obj.name}")
```

### Recipe 2 — Polished gold
```python
import bpy
mat = bpy.data.materials.new('MAT-gold_polished')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (1.022, 0.782, 0.344, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.05
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:gold_polished')
```

### Recipe 3 — Polished copper
```python
import bpy
mat = bpy.data.materials.new('MAT-copper_polished')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.926, 0.721, 0.504, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.05
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:copper_polished')
```

### Recipe 4 — Mirror chrome
```python
import bpy
mat = bpy.data.materials.new('MAT-chrome')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.55, 0.56, 0.55, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.02
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:chrome')
```

### Recipe 5 — Clear glass
```python
import bpy
mat = bpy.data.materials.new('MAT-glass_clear')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.0
bsdf.inputs['Transmission Weight'].default_value = 1.0
bsdf.inputs['IOR'].default_value = 1.5
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:glass_clear')
```

### Recipe 6 — Frosted glass
```python
import bpy
mat = bpy.data.materials.new('MAT-glass_frosted')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs['Transmission Weight'].default_value = 1.0
bsdf.inputs['IOR'].default_value = 1.5
bsdf.inputs['Roughness'].default_value = 0.3
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:glass_frosted')
```

### Recipe 6b — Coloured glass (wine bottle, tinted vials, decorative glass)

Using only `Base Color` to tint Principled BSDF makes coloured glass look **flat or metallic**. Real coloured glass has *volume absorption*: light passing through gets tinted by the distance it travels, so thick parts look darker and thin parts look lighter. This is the depth-based richness that makes glass read as glass.

Pattern: keep the surface near-white with slight roughness, attach a `Volume Absorption` shader to the Material Output's `Volume` input.

```python
import bpy

def set_input(node, name, value):
    for inp in node.inputs:
        if inp.name == name:
            inp.default_value = value
            return True
    return False

mat = bpy.data.materials.new('MAT-glass_wine')
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
bsdf = nodes['Principled BSDF']
output = nodes['Material Output']

# Surface: near-white with tiny roughness (breaks mirror-finish look)
set_input(bsdf, 'Base Color', (0.85, 0.95, 0.85, 1.0))   # near-white
set_input(bsdf, 'Metallic', 0.0)
set_input(bsdf, 'Roughness', 0.025)                       # critical: not 0.0; that looks metallic
set_input(bsdf, 'Transmission Weight', 1.0)
set_input(bsdf, 'IOR', 1.52)                              # bottle glass

# Volume Absorption — depth-based tint
volume = nodes.new('ShaderNodeVolumeAbsorption')
set_input(volume, 'Color', (0.10, 0.45, 0.18, 1.0))       # saturated wine-bottle green
set_input(volume, 'Density', 30.0)                         # higher = more colour over short distance

links.new(volume.outputs['Volume'], output.inputs['Volume'])

bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:glass_wine_volume_absorption')
```

**Tuning Density**: 0–10 = very subtle tint (clear bottle); 20–40 = clear bottle-green or amber; 60–100+ = nearly opaque (cobalt-blue medicine bottle).

**Tuning Color**: invert intuition — the volume Color is what gets *removed* from passing light, so for "wine green" use saturated green; for "amber" use saturated yellow-orange.

**Other coloured-glass examples** (density values updated v0.9.0 after subject-class lighting fix):

| Name | Volume Color | Density | Surface tint |
|------|-------------|---------|---------------|
| Wine bottle (deep green) | (0.05, 0.32, 0.10) | 80 | near-white |
| Pale tinted (clear vial) | (0.10, 0.45, 0.18) | 15 | near-white |
| Champagne / pale gold | (0.85, 0.65, 0.30) | 25 | near-white |
| Cobalt blue (medicine bottle) | (0.10, 0.20, 0.85) | 80 | near-white |
| Amber / brown beer bottle | (0.80, 0.40, 0.10) | 70 | near-white |
| Ruby red | (0.85, 0.10, 0.15) | 100 | near-white |

**Density tuning rule of thumb under neutral/glass-class lighting**:
- Density 5–15 = subtle hint of colour (clear + tinted)
- Density 30–50 = medium tint visible at thin sections
- **Density 60–100 = proper wine/beer/cobalt bottle look** (recommended for hero shots)
- Density 100+ = nearly opaque (artistic / decorative)

If under standard 4:1:2 metal-class lighting the volume tint washes out (v0.7.0 issue), don't crank density to compensate — switch to `subject_class='glass'` lighting in `blender-lighting` Recipe 0a, which uses softer rim that preserves the volume colour.

**Critical**: Cycles `transmission_bounces` must be ≥ 16 (default 12) for thick or layered colour glass; otherwise rays terminate and the glass renders black on the inside.

```python
scene.cycles.transmission_bounces = 24
```

**Pitfall**: don't set `Base Color` to the tint colour AND attach a Volume — you get double-tinting that looks wrong. Surface near-white, volume does the colour work.

### Recipe 7 — Matte plastic (red)
```python
import bpy
mat = bpy.data.materials.new('MAT-plastic_matte_red')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.8, 0.1, 0.05, 1.0)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.6
bsdf.inputs['IOR'].default_value = 1.45
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:plastic_matte_red')
```

### Recipe 8 — Lacquered plastic (car-paint look)
```python
import bpy
mat = bpy.data.materials.new('MAT-plastic_lacquered')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.8, 0.1, 0.05, 1.0)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.15
bsdf.inputs['IOR'].default_value = 1.45
bsdf.inputs['Coat Weight'].default_value = 0.8
bsdf.inputs['Coat Roughness'].default_value = 0.05
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:plastic_lacquered')
```

### Recipe 9 — Skin (light tone)

Uses the `set_input` helper because `Subsurface IOR` has `enabled=False` on Blender 5.x and isn't reachable by string-key lookup. The other inputs work fine either way; using the helper consistently keeps the recipe safe across versions.

```python
import bpy

def set_input(node, name, value):
    for inp in node.inputs:
        if inp.name == name:
            inp.default_value = value
            return True
    return False

mat = bpy.data.materials.new('MAT-skin_light')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']

set_input(bsdf, 'Base Color', (0.85, 0.65, 0.55, 1.0))
set_input(bsdf, 'Metallic', 0.0)
set_input(bsdf, 'Roughness', 0.4)
set_input(bsdf, 'Subsurface Weight', 1.0)
set_input(bsdf, 'Subsurface Radius', (1.0, 0.2, 0.1))
set_input(bsdf, 'Subsurface IOR', 1.4)   # ← string-key fails on Blender 5.x; helper bypasses it

bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:skin_light')
```

### Recipe 10 — Velvet / cloth with sheen
```python
import bpy
mat = bpy.data.materials.new('MAT-velvet_red')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.6, 0.0, 0.1, 1.0)
bsdf.inputs['Roughness'].default_value = 0.9
bsdf.inputs['Sheen Weight'].default_value = 0.5
bsdf.inputs['Sheen Roughness'].default_value = 0.5
bsdf.inputs['Sheen Tint'].default_value = (0.8, 0.6, 0.6, 1.0)
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:velvet_red')
```

### Recipe 11 — Soft silicone
```python
import bpy
mat = bpy.data.materials.new('MAT-silicone')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.65, 0.63, 0.60, 1.0)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.7
bsdf.inputs['IOR'].default_value = 1.4
bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:silicone')
```

### Recipe 11b — Emission (light-emitting mesh, e.g. lamp bulb, neon sign, screen glow)

Emission is a **separate shader from Principled BSDF** — replace the BSDF entirely with a `ShaderNodeEmission` and connect to Material Output's Surface input. The mesh becomes a light source itself (contributes to scene illumination in Cycles).

```python
import bpy

mat = bpy.data.materials.new('MAT-bulb_emission')
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Remove the default Principled BSDF
for n in list(nodes):
    if n.type == 'BSDF_PRINCIPLED':
        nodes.remove(n)

emission = nodes.new('ShaderNodeEmission')
emission.inputs['Color'].default_value = (1.0, 0.92, 0.78, 1.0)   # warm tungsten
emission.inputs['Strength'].default_value = 1500.0                 # see strength guide below

output = nodes['Material Output']
links.new(emission.outputs['Emission'], output.inputs['Surface'])

bpy.data.objects['GEO-bulb'].data.materials.append(mat)
print('material:bulb_emission')
```

#### Strength tuning — critical for mesh emitters

Mesh emission's effective brightness scales with **mesh surface area**, not just the Strength value. A small sphere at Strength=50 is barely visible; the same sphere at Strength=1500 lights a desk like a real bulb. Use this table for ballpark values:

| Mesh size | Bulb-equivalent | Strength |
|-----------|-----------------|----------|
| 1-2 cm sphere (Edison bulb) | 40W warm bulb | 800-1500 |
| 3-5 cm sphere (LED globe) | 60-100W bulb | 1500-3000 |
| 10×10 cm flat panel (LED panel) | Indoor light panel | 100-300 |
| 100×30 cm strip (neon tube) | Neon sign | 50-150 |
| Large window plane (sky simulation) | Daylight | 5-20 |

**Rule of thumb**: smaller surface area → higher Strength. Doubling sphere radius reduces required Strength by ~4× (inverse surface-area scaling).

Use `(R, G, B)` to set colour temperature:
- Tungsten (3200K) — `(1.0, 0.85, 0.6)`
- LED warm (3000K) — `(1.0, 0.8, 0.6)`
- Daylight (5500K) — `(1.0, 1.0, 1.0)`
- Cool fluorescent (4500K) — `(0.95, 0.95, 1.0)`

#### Lamp shade — separate flipped-normal interior

If the bulb sits inside a shade, the shade's INSIDE surface needs to be bright matte (white) so it reflects bulb light realistically. Single-mesh shades only show the OUTSIDE material. Solution: duplicate the shade mesh, flip normals, scale 97% smaller, apply bright-white material. This gives proper interior-glow when the bulb illuminates the shade.

```python
import bpy

# Assuming `shade` is the outer cone with the dark exterior material already applied
shade = bpy.data.objects['GEO-lamp_shade']
bpy.ops.object.select_all(action='DESELECT')
shade.select_set(True); bpy.context.view_layer.objects.active = shade
bpy.ops.object.duplicate()
shade_in = bpy.context.active_object
shade_in.name = shade.name + '_interior'

# Flip normals so the inside surface faces inward
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.flip_normals()
bpy.ops.object.mode_set(mode='OBJECT')

# Bright white interior
mat_in = bpy.data.materials.new('MAT-shade_interior')
mat_in.use_nodes = True
b = mat_in.node_tree.nodes['Principled BSDF']
b.inputs['Base Color'].default_value = (0.95, 0.93, 0.88, 1.0)
b.inputs['Roughness'].default_value = 0.5

shade_in.data.materials.clear()
shade_in.data.materials.append(mat_in)
shade_in.scale = (0.97, 0.97, 0.97)
print('material:shade_interior_white')
```

### Recipe 12 — Procedural wood (10 nodes)
```python
import bpy

mat = bpy.data.materials.new('MAT-wood_procedural')
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

bsdf = nodes['Principled BSDF']

# Texture coordinate
tex_coord = nodes.new('ShaderNodeTexCoord')
tex_coord.location = (-800, 0)

# Mapping
mapping = nodes.new('ShaderNodeMapping')
mapping.location = (-600, 0)
mapping.inputs['Scale'].default_value = (3, 3, 3)

# Wave (the grain)
wave = nodes.new('ShaderNodeTexWave')
wave.location = (-400, 100)
wave.wave_type = 'BANDS'
wave.bands_direction = 'X'
wave.inputs['Scale'].default_value = 5.0
wave.inputs['Distortion'].default_value = 4.0

# Noise (variation)
noise = nodes.new('ShaderNodeTexNoise')
noise.location = (-400, -100)
noise.inputs['Scale'].default_value = 8.0

# Mix wave + noise
mix = nodes.new('ShaderNodeMixRGB')
mix.location = (-200, 0)
mix.blend_type = 'MULTIPLY'
mix.inputs[0].default_value = 0.5

# ColorRamp (tonal range)
ramp = nodes.new('ShaderNodeValToRGB')
ramp.location = (0, 0)
ramp.color_ramp.elements[0].color = (0.15, 0.07, 0.03, 1.0)  # dark wood
ramp.color_ramp.elements[1].color = (0.6, 0.35, 0.18, 1.0)   # light wood

# Wire
links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
links.new(wave.outputs['Color'], mix.inputs[1])
links.new(noise.outputs['Color'], mix.inputs[2])
links.new(mix.outputs['Color'], ramp.inputs['Fac'])
links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])

bsdf.inputs['Roughness'].default_value = 0.7

bpy.data.objects['GEO-target'].data.materials.append(mat)
print('material:wood_procedural')
```

**Note**: procedural materials don't export to glTF. For web/game export, bake to image textures first.

## PBR values reference

For exact F0 reflectance values for any metal: [physicallybased.info](https://physicallybased.info/) — covers 50+ materials. The recipes above use values from this database.

## Material naming convention

`MAT-{purpose}_{subtype}_{finish}`. Examples:
- `MAT-frame_metal_brushed`
- `MAT-lens_glass_dark_mirror`
- `MAT-pad_silicone_warm_gray`
- `MAT-wood_oak_glossy`

Avoid `Material.001`, `Material.027`. Always rename.

## Common pitfalls

| Symptom | Fix |
|---------|-----|
| "Plasticky" metals | Metallic must be exactly 0 or 1 |
| Black metal | Base color too dark; metals reflect 30–100%; keep ≥0.5 sRGB |
| Roughness 0 = artifacts | Use 0.01–0.05 minimum |
| Glass renders black | Increase Cycles transmission bounces (Recipe section 11-rendering) |
| Material not visible in glTF | Procedural shader; bake to image first |
| Normal map looks wrong | Set image texture to "Non-Color" color space |
| sRGB on roughness map | Set image texture to "Non-Color" |
| `KeyError: 'Subsurface IOR'` (or any other input) | Blender 5.x quirk: input has `enabled=False`; use the `set_input` helper at the top of this file instead of `bsdf.inputs['Name']` |

## When to load `references/overview.md`

Load when:
- The recipe you need isn't in the 12 above
- You need anisotropy (brushed metal direction), volume absorption (tinted thick glass), or advanced shader-node combos
- The user asks for material variation across one mesh (Mix Shader patterns)
- You're baking procedural to image textures for export

The reference covers: full Principled BSDF parameter map, 50+ materials database link, procedural texture combinations (Voronoi, Wave, Noise), Sheen + Subsurface deep-dives, and bake-for-export workflow.
