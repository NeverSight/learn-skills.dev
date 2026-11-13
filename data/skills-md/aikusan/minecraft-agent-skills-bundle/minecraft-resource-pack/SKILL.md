---
name: minecraft-resource-pack
description: "Create and edit Minecraft resource packs for 1.21.x including custom block models, item models, blockstate definitions, textures (PNG format requirements), sounds.json, custom fonts, MCMETA animation files, OptiFine CIT (Custom Item Textures), and pack.mcmeta format. Covers the full block/item model JSON schema (parent, textures, elements, display, overrides), multi-layer items, GUI textures, GUI sprites, language files, shader integration (core shaders, Iris), and the pack format numbers for each 1.21.x version. Use to customize how Minecraft looks and sounds without mods."
---

# Minecraft Resource Pack Skill

## What Is a Resource Pack?

A resource pack is a folder (or `.zip`) that overrides or adds Minecraft's visual and
audio assets: textures, models, sounds, language files, fonts, and shaders. No Java
or mod loader required. Works on vanilla clients and servers.

### Routing Boundaries
- `Use when`: the deliverable is visual/audio assets (textures, models, sounds, fonts, shaders) in resource-pack format.
- `Do not use when`: the task requires gameplay logic or runtime behavior changes (use `minecraft-datapack`, `minecraft-plugin-dev`, or `minecraft-modding`).
- `Do not use when`: the task is server infrastructure/runtime administration (`minecraft-server-admin`).
- `Do not use when`: the task is a bitmap asset such as an icon or thumbnail (`minecraft-imagegen`).
- `Do not use when`: the task is converting a finished Java pack for Bedrock (`minecraft-resource-pack-conversion`).

---

## Pack Metadata (1.21.x)

| Minecraft Version | Preferred `pack` metadata |
|-------------------|---------------------------|
| 1.21 / 1.21.1     | `pack_format: 34` |
| 1.21.2 / 1.21.3   | `pack_format: 42` |
| 1.21.4            | `pack_format: 46` |
| 1.21.5            | `pack_format: 55` |
| 1.21.6            | `pack_format: 63` |
| 1.21.7 / 1.21.8   | `pack_format: 64` |
| 1.21.9 / 1.21.10  | `min_format: 69.0`, `max_format: 69.0` |
| 1.21.11           | `min_format: 75.0`, `max_format: 75.0` |
| 26.x              | Not verified here. Read the Minecraft Wiki resource pack format table for your exact release. |

Use `pack_format` through 1.21.8. Starting in 1.21.9, `pack.mcmeta` switches to
`min_format` / `max_format` instead of the older single-number field.

---

## Directory Layout

```
my-pack/
├── pack.mcmeta
├── pack.png                   ← 64×64 icon (optional)
└── assets/
    └── minecraft/             ← override vanilla (or <namespace>/ for new packs)
        ├── models/
        │   ├── block/
        │   │   └── stone.json
        │   └── item/
        │       └── diamond_sword.json
        ├── blockstates/
        │   └── stone.json
        ├── textures/
        │   ├── block/
        │   │   └── stone.png
        │   ├── item/
        │   │   └── diamond_sword.png
        │   ├── gui/
        │   │   └── sprites/
        │   │       └── my_sprite.png
        │   └── entity/
        │       └── zombie/
        │           └── zombie.png
        ├── sounds/
        │   └── custom/
        │       └── my_sound.ogg
        ├── sounds.json
        ├── font/
        │   └── default.json
        ├── lang/
        │   └── en_us.json
        ├── shaders/           ← core shader overrides (advanced)
        └── optifine/          ← OptiFine CIT / CTM (OptiFine only)
            └── cit/
                └── my_item.properties
```

---

## `pack.mcmeta`

### 1.21.8 and earlier

```json
{
  "pack": {
    "pack_format": 64,
    "description": "My Custom Resource Pack v1.0"
  }
}
```

### 1.21.9 and newer

```json
{
  "pack": {
    "min_format": 75.0,
    "max_format": 75.0,
    "description": "My Custom Resource Pack v1.0"
  }
}
```

---

## Block Models

### `assets/minecraft/models/block/my_cube.json`
Full cube — all six faces use the same texture:
```json
{
  "parent": "minecraft:block/cube_all",
  "textures": {
    "all": "minecraft:block/stone"
  }
}
```

Column block (like logs):
```json
{
  "parent": "minecraft:block/cube_column",
  "textures": {
    "end": "mypack:block/my_pillar_top",
    "side": "mypack:block/my_pillar_side"
  }
}
```

Different sides:
```json
{
  "parent": "minecraft:block/cube",
  "textures": {
    "up":    "mypack:block/my_block_top",
    "down":  "mypack:block/my_block_bottom",
    "north": "mypack:block/my_block_side",
    "south": "mypack:block/my_block_side",
    "east":  "mypack:block/my_block_side",
    "west":  "mypack:block/my_block_side",
    "particle": "mypack:block/my_block_side"
  }
}
```

Cross model (flowers, plants):
```json
{
  "parent": "minecraft:block/cross",
  "textures": {
    "cross": "mypack:block/my_flower"
  }
}
```

### Custom geometry (elements)
```json
{
  "credit": "Custom model",
  "ambientocclusion": true,
  "textures": {
    "0": "mypack:block/panel",
    "particle": "mypack:block/panel"
  },
  "elements": [
    {
      "from": [0, 0, 7],
      "to": [16, 16, 9],
      "faces": {
        "north": { "texture": "#0", "uv": [0, 0, 16, 16] },
        "south": { "texture": "#0", "uv": [0, 0, 16, 16] }
      }
    }
  ],
  "display": {
    "thirdperson_righthand": {
      "rotation": [75, 45, 0],
      "translation": [0, 2.5, 0],
      "scale": [0.375, 0.375, 0.375]
    }
  }
}
```

> `from` and `to` are in 1/16th block units (0–16). `uv` is `[x1, y1, x2, y2]` in 0–16 units.

---

## Item Models

### Simple flat item
```json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "mypack:item/my_item"
  }
}
```

### Held item (in-hand model)
```json
{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "mypack:item/my_sword"
  }
}
```

### Two-layer item (colored like leather armor)
```json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "minecraft:item/leather_helmet",
    "layer1": "minecraft:item/leather_helmet_overlay"
  }
}
```

### Custom model data overrides (1.21.4 and prior)
Each `predicate` entry routes to a different model based on `custom_model_data`:
```json
{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "minecraft:item/stick"
  },
  "overrides": [
    { "predicate": { "custom_model_data": 1001 }, "model": "mypack:item/magic_wand" },
    { "predicate": { "custom_model_data": 1002 }, "model": "mypack:item/fire_staff" }
  ]
}
```

### 1.21.4+ Item Model (new format)
In 1.21.4, Mojang introduced a new item model system. Place model definitions at
`assets/<namespace>/items/<item_name>.json`:
```json
{
  "model": {
    "type": "minecraft:select",
    "property": "minecraft:custom_model_data",
    "fallback": {
      "type": "minecraft:model",
      "model": "minecraft:item/stick"
    },
    "cases": [
      {
        "when": 1001,
        "model": { "type": "minecraft:model", "model": "mypack:item/magic_wand" }
      }
    ]
  }
}
```

---

## Blockstate Definitions

### Simple block (no variants)
```json
{
  "variants": {
    "": { "model": "mypack:block/my_block" }
  }
}
```

### Facing block (4 rotations)
```json
{
  "variants": {
    "facing=north": { "model": "mypack:block/my_block" },
    "facing=south": { "model": "mypack:block/my_block",  "y": 180 },
    "facing=east":  { "model": "mypack:block/my_block",  "y": 90  },
    "facing=west":  { "model": "mypack:block/my_block",  "y": 270 }
  }
}
```

### Random texture (multipart)
```json
{
  "variants": {
    "": [
      { "model": "minecraft:block/grass_block",  "weight": 3 },
      { "model": "minecraft:block/grass_block_2" }
    ]
  }
}
```

### Multipart (slabs, fences, walls)
```json
{
  "multipart": [
    { "apply": { "model": "mypack:block/my_slab_bottom" }, "when": { "type": "bottom" } },
    { "apply": { "model": "mypack:block/my_slab_top"    }, "when": { "type": "top"    } },
    { "apply": { "model": "mypack:block/my_block"        }, "when": { "type": "double" } }
  ]
}
```

---

## Textures

- Format: **PNG**, RGBA (32-bit)
- Standard block/item size: **16×16 px**
- Textures can be larger (32×32, 64×64) — Minecraft scales them, but stick to powers of 2
- Animation requires height = N × width (e.g., 16×64 for 4 frames)
- Place block textures in `assets/<namespace>/textures/block/`
- Place item textures in `assets/<namespace>/textures/item/`
- All textures are referenced without the `.png` extension in JSON

### Animated texture MCMETA
`assets/minecraft/textures/block/fire_0.png.mcmeta`:
```json
{
  "animation": {
    "frametime": 2,
    "frames": [0, 1, 2, 3, 4, 5, 6, 7]
  }
}
```
If `frames` is omitted, all frames play sequentially. `frametime` is in game ticks (default 1).

### GUI sprites (1.20.2+)
Place sprites at `assets/minecraft/textures/gui/sprites/<category>/<name>.png`.
Reference them with `<category>/<name>` in code/JSON.

---

## Sounds

### `assets/minecraft/sounds.json`
```json
{
  "my_sound.play": {
    "sounds": [
      { "name": "mypack:custom/my_sound", "volume": 1.0, "pitch": 1.0, "weight": 1 },
      { "name": "mypack:custom/my_sound_alt", "weight": 2 }
    ],
    "category": "players"
  },
  "entity.player.levelup": {
    "replace": true,
    "sounds": [
      { "name": "mypack:custom/levelup_replaced", "volume": 0.75, "pitch": 1.0 }
    ]
  }
}
```

- Sound files go in `assets/<namespace>/sounds/` as `.ogg` files (Vorbis encoded)
- Use `"replace": true` to replace vanilla sounds instead of adding to them
- Categories: `master`, `music`, `record`, `weather`, `block`, `hostile`, `neutral`, `player`, `ambient`, `voice`

---

## Language Files

`assets/minecraft/lang/en_us.json`:
```json
{
  "block.mypack.my_block": "My Custom Block",
  "item.mypack.my_item": "Magic Wand",
  "entity.mypack.my_mob": "Forest Guardian",
  "death.attack.mypack.laser": "%1$s was zapped by %2$s"
}
```

- Use the exact translation key format for your mod/datapack namespace
- File name is the locale code (e.g., `fr_fr.json`, `de_de.json`)
- Always provide `en_us.json` as the primary fallback

---

## Fonts

### `assets/minecraft/font/default.json` — add glyph
```json
{
  "providers": [
    {
      "type": "bitmap",
      "file": "mypack:font/icons.png",
      "ascent": 8,
      "height": 9,
      "chars": ["\uE000", "\uE001", "\uE002"]
    }
  ]
}
```

Custom icons via private use area (U+E000–U+F8FF). Reference in text with `\uE000`.
The `icons.png` must have each character cell `height` pixels tall.

---

## OptiFine CIT (Custom Item Textures)

> OptiFine-only feature. Does not work in vanilla or Iris.

### `assets/minecraft/optifine/cit/my_sword.properties`
```properties
type=item
items=minecraft:diamond_sword
texture=my_sword_texture.png
model=my_sword_model
nbt.display.Name=ipattern:*Excalibur*
```

Common CIT properties:
- `type=item` — item texture override
- `type=enchantment` — custom enchantment glint
- `type=armor` — armor overlay
- `items=` — comma-separated item IDs
- `damage=` — damage range (e.g., `0-50%`)
- `nbt.display.Name=ipattern:*text*` — NBT name filter
- `texture=` — PNG file (relative to `.properties` file)
- `model=` — JSON model file (relative)

---

## Iris Shaders (Resource Pack Method)

Iris shaders live inside a resource pack at:
```
assets/iris/
    shaders/
        core/
            rendertype_terrain.vsh    ← vertex shader override
            rendertype_terrain.fsh    ← fragment shader override
```

Full shader pack distribution uses the `.zip` format with a `shaders/` root folder
(not inside `assets/`). Resource pack shader overrides target specific render types.

---

## Installation

```bash
# Singleplayer: place in
~/.minecraft/resourcepacks/my-pack/
# or
~/.minecraft/resourcepacks/my-pack.zip

# Server-side (forces on clients):
# Set in server.properties:
resource-pack=https://example.com/my-pack.zip
resource-pack-sha1=<sha1 hash>
resource-pack-prompt={"text":"Required pack","color":"gold"}
```

---

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Model not showing | Wrong JSON path or syntax error | Check `assets/<namespace>/models/` path; validate JSON |
| Black/pink checkerboard | Texture path wrong or missing | Check `textures/` path, file extension not in JSON |
| Blockstate not applying | Wrong state property name | Match exact property names from `/blockdata` |
| Animation not working | Wrong MCMETA location | Must be same folder as texture, named `texture.png.mcmeta` |
| Custom sound not playing | Not in `sounds.json` | Register sound event in `sounds.json`, match namespace |
| Pack not loading | Wrong `pack_format` or `min_format` / `max_format` values | Update `pack.mcmeta` for the exact 1.21.x patch |

## Validator Script

Use the bundled validator script before shipping a resource-pack update:

```bash
# Run from the installed skill directory (for example `.claude/skills/minecraft-resource-pack`):
./scripts/validate-resource-pack.sh --root /path/to/resource-pack

# Strict mode treats warnings as failures:
./scripts/validate-resource-pack.sh --root /path/to/resource-pack --strict
```

What it checks:
- JSON validity for `pack.mcmeta` and `assets/**/*.json`
- Model/blockstate/font/sounds references resolve to real files
- Every `*.png.mcmeta` has a matching `*.png`

---

## References

- Minecraft Wiki — Resource pack: https://minecraft.wiki/w/Resource_pack
- Minecraft Wiki — Model: https://minecraft.wiki/w/Tutorials/Models
- Minecraft Wiki — Blockstates: https://minecraft.wiki/w/Blockstate_(Java_Edition)
- Pack format history: https://minecraft.wiki/w/Pack_format
- Misode's model viewer: https://misode.github.io/
- OptiFine CIT guide: https://optifine.readthedocs.io/cit.html
