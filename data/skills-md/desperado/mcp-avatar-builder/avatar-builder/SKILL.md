---
name: avatar-builder
description: Generate unique avatars instantly as SVG or PNG — no API keys, no cloud, no cost. Use when the user asks to "create an avatar", "make a profile picture", "generate a character", "pixel art portrait", "cyberpunk avatar", "horror character", "retro 80s avatar", "team avatars", "placeholder user icons", or needs procedurally generated faces. 4 styles (chibi, cyberpunk, horror, retro) with 100+ mix-and-match parts, SVG filter effects (neon glow, fog, VHS scanlines), and deterministic seed-based generation for consistent user identities.
---

# Avatar Builder

Procedural avatar generator powered by an MCP server. Instantly creates unique, composable avatars from mix-and-match SVG parts — no AI image generation, no API keys, no cloud dependency. Works fully offline.

## Why Use This

- **Instant** — generates in milliseconds, not seconds
- **Free** — no API keys or credits required
- **Offline** — runs entirely on your machine
- **Deterministic** — same seed always produces the same avatar, perfect for user identities
- **Scalable** — generate thousands of unique avatars from seeds (usernames, emails, IDs)
- **Vector-first** — SVG output scales to any resolution; PNG export up to 2048px

## When to Use

Activate this skill when the user:

- Asks to create an avatar, profile picture, or character image
- Needs placeholder user icons for a UI, app, or website
- Wants to generate unique avatars for a team, user list, or leaderboard
- Asks for pixel art, cyberpunk, or chibi character generation
- Wants consistent, reproducible avatars derived from usernames or IDs
- Needs SVG avatars they can embed directly in HTML or Markdown

## Setup

The avatar builder is an MCP server. Add to your MCP settings:

```json
{
  "mcpServers": {
    "avatar-builder": {
      "command": "npx",
      "args": ["-y", "mcp-avatar-builder"]
    }
  }
}
```

## Tools

### `generate_avatar`

Create an avatar with customizable style, parts, colors, and output format.

| Parameter | Type   | Default   | Description                           |
| --------- | ------ | --------- | ------------------------------------- |
| `style`   | string | `"chibi"` | Style: `chibi`, `cyberpunk`, `horror`, `retro` |
| `options`  | object | random    | Part selections per category          |
| `colors`  | object | palette   | Color overrides (hex or palette name) |
| `seed`    | string | —         | Seed for deterministic generation     |
| `format`  | string | `"svg"`   | Output: `svg` or `png`                |
| `size`    | number | `200`     | PNG size in pixels (16–2048)          |

### `list_styles`

List all available styles with their categories and palettes.

### `list_parts`

List available parts and variants for a style, optionally filtered by category.

## Styles

### Chibi (200x200)

Cute, minimal pixel-art style — great for friendly profile pictures and placeholder icons.

**8 categories:** head (3), eyes (3), eyebrows (3), mouth (3), hair_back (3), hair_front (3), clothing (3), accessories (3)

**Colors:** `skin` (6 tones), `hair` (8 colors), `eyes` (6 colors), `clothing`

### Cyberpunk (400x400)

High-detail style with SVG filter effects (neon glow, scanlines, noise grain), gradient fills, and cybernetic parts. Dark sci-fi aesthetic with 11 composable layers.

**11 categories, 34 variants:**

| Category    | Variants                                |
| ----------- | --------------------------------------- |
| background  | `circuit_grid` `rain_city` `dark_void`  |
| head        | `angular` `scarred` `implanted`         |
| eyes        | `led` `visor` `cyber`                   |
| eyebrows    | `sharp` `none`                          |
| mouth       | `neutral` `respirator` `smirk`          |
| hair        | `mohawk` `undercut` `wired` `shaved`    |
| face_mods   | `neural_port` `led_tattoo` `jaw_plate`  |
| clothing    | `techwear` `tactical_vest` `collar_rig` |
| accessories | `none` `headset` `holo_visor`           |
| effects     | `none` `scanlines` `glitch`             |

**Extra colors:** `neon` (6 neon colors for glow effects), `accent` (4 metal tones for cybernetic parts)

### Horror (400x400)

Dark survival-horror style with sickly skin, wounds, fog, and blood effects. Think Resident Evil, Silent Hill, The Last of Us.

**11 categories, 33 variants:**

| Category    | Variants                                |
| ----------- | --------------------------------------- |
| background  | `lab_corridor` `hive` `dark_forest`     |
| head        | `gaunt` `scarred` `infected`            |
| eyes        | `bloodshot` `mutant` `hollow`           |
| eyebrows    | `thin` `furrowed` `none`                |
| mouth       | `grimace` `gas_mask` `stitched`         |
| hair        | `military` `messy` `slicked`            |
| face_mods   | `bite_wound` `stitches` `infection`     |
| clothing    | `tactical_vest` `lab_coat` `jumpsuit`   |
| accessories | `none` `dog_tags` `herb_vial`           |
| effects     | `none` `fog` `blood_splatter`           |

**Extra colors:** `blood` (6 wound/blood tones), `atmosphere` (4 environmental tones)

### Retro (400x400)

Warm 1980s nostalgia style — Stranger Things, The Goonies, Stand By Me. Sunset backgrounds, feathered hair, VHS effects.

**11 categories, 35 variants:**

| Category    | Variants                                     |
| ----------- | -------------------------------------------- |
| background  | `sunset` `arcade` `suburban`                 |
| head        | `round` `square_jaw` `soft`                  |
| eyes        | `wide` `determined` `cool`                   |
| eyebrows    | `thick` `thin` `arched`                      |
| mouth       | `grin` `bubblegum` `neutral`                 |
| hair        | `feathered` `mullet` `shaved` `ponytail`     |
| face_mods   | `nosebleed` `freckles` `band_aid`            |
| clothing    | `denim_jacket` `hawkins_tee` `leather_jacket`|
| accessories | `none` `headband` `shades`                   |
| effects     | `none` `vhs_lines` `warm_glow`               |

**Extra colors:** `retro` (6 warm/neon tones), `accent` (4 material tones)

## Instructions

1. If the user doesn't specify a style, pick based on context — `chibi` for friendly/casual, `cyberpunk` for dark/techy, `horror` for dark/survival themes, `retro` for 80s/nostalgic vibes
2. For a quick unique avatar, just pass a `seed` — the RNG picks all parts and colors
3. For full control, specify `options` and `colors` explicitly
4. Default to `format: "png"` and `size: 800` when the user wants to see the result visually
5. Use `list_parts` with a category filter to show the user what's available before customizing
6. When generating avatars for multiple users, use their username or email as the `seed` for consistent identity

### Quick: Random Avatar from Seed

```json
{
  "style": "cyberpunk",
  "seed": "username123",
  "format": "png",
  "size": 800
}
```

### Full Control: Customized Cyberpunk Character

```json
{
  "style": "cyberpunk",
  "options": {
    "background": "rain_city",
    "head": "angular",
    "eyes": "led",
    "eyebrows": "sharp",
    "mouth": "smirk",
    "hair_back": "mohawk",
    "hair_front": "mohawk",
    "face_mods": "led_tattoo",
    "clothing": "techwear",
    "effects": "glitch"
  },
  "colors": {
    "neon": "hot-pink",
    "hair": "electric-blue",
    "eyes": "cyan",
    "skin": "pale-tech"
  },
  "format": "png",
  "size": 800
}
```

### Batch: Team Avatars from Names

Generate consistent avatars for a list of users by seeding with their names:

```json
{"style": "cyberpunk", "seed": "alice", "format": "png", "size": 256}
{"style": "cyberpunk", "seed": "bob", "format": "png", "size": 256}
{"style": "cyberpunk", "seed": "carol", "format": "png", "size": 256}
```

Each person always gets the same avatar. Change the seed, get a different face.

## Tips

- Use palette **names** (`"hot-pink"`, `"chrome"`, `"electric-blue"`) or **hex values** (`"#FF2D95"`) for colors
- The `seed` parameter is the key to deterministic generation — same seed = same avatar, every time
- For cyberpunk, `neon` controls glow color on eyes/tattoos/effects, `accent` controls metal surfaces on implants/armor
- `effects: "scanlines"` adds a CRT overlay; `"glitch"` adds color displacement bars and vignette
- Combine `face_mods` with `accessories` for maximum cyberpunk detail (e.g. `led_tattoo` + `holo_visor`)
- For horror, `blood` controls wound/stain colors, `atmosphere` controls environmental tones (steel, rust, concrete, moss)
- For retro, `retro` controls highlight colors (sunset-orange, neon-pink), `accent` controls material tones (denim, leather)
- SVG output can be embedded directly in HTML — no file hosting needed
