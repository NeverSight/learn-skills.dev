---
name: minecraft-resource-pack-conversion
description: "Convert or assist conversion of Minecraft Java Edition resource packs to Bedrock Edition resource packs for 1.21.x. Use for Java pack inspection, choosing Thunder or Geyser PackConverter for simple packs, JE2BE for PBR or RTX-oriented packs, running the bundled conversion helper, producing .mcpack outputs, reporting unsupported Java-only assets, and planning manual Bedrock fixes."
---

# Minecraft Resource Pack Conversion Skill

## Scope

Use this skill when a Java Edition resource pack must become a Bedrock Edition
resource pack or `.mcpack`.

### Routing Boundaries
- `Use when`: the task is Java-to-Bedrock resource pack conversion, conversion feasibility analysis, `.mcpack` output, or unsupported asset reporting.
- `Do not use when`: the task is authoring a Java resource pack from scratch (`minecraft-resource-pack`), developing Bedrock add-ons (`minecraft-bedrock-addon-dev`), crossplay deployment (`minecraft-crossplay-ops`), or generating concept art (`minecraft-imagegen`).

## Conversion Strategy

Choose a path before editing files:

| Pack shape | Preferred path |
|---|---|
| Mostly vanilla texture overrides | Built-in helper or Thunder/Geyser PackConverter |
| Pack for Geyser crossplay clients | Thunder/Geyser PackConverter, then test through Geyser |
| PBR, RTX, or physically based texture sets | JE2BE Resource Pack Converter, then manual Bedrock review |
| OptiFine CIT, custom shaders, custom models, complex sounds | Manual conversion plan with unsupported-asset report |

The bundled helper is intentionally conservative. It copies simple Java texture
assets into Bedrock-style texture folders, writes `manifest.json`, packages a
`.mcpack`, and reports everything that needs manual review.

## Bundled Helper

Run from the skill folder or copy the script path from the installed skill:

```bash
python3 ./scripts/convert-java-pack-to-bedrock.py \
  --input ./MyJavaPack \
  --output ./MyBedrockPack.mcpack \
  --pack-name "My Bedrock Pack" \
  --description "Converted resource pack" \
  --report ./conversion-report.json \
  --converter auto
```

Converter modes:

- `auto`: use a configured external converter when available, otherwise use the built-in conversion path.
- `builtin`: use only the conservative built-in converter.
- `thunder`: require a Thunder or PackConverter jar path from `--thunder-jar` or `THUNDER_JAR`.
- `je2be`: require a JE2BE executable path from `--je2be-bin` or `JE2BE_BIN`.

Use `--strict` when unsupported Java-only assets should fail the run instead of
producing a best-effort pack.

## Built-In Conversion Behavior

The helper:

- Reads Java `pack.mcmeta`.
- Creates Bedrock `manifest.json` with unique UUIDs.
- Copies `assets/<namespace>/textures/block/*.png` to `textures/blocks/`.
- Copies `assets/<namespace>/textures/item/*.png` to `textures/items/`.
- Copies common entity, GUI, environment, map, misc, painting, and particle
  textures into matching Bedrock folders.
- Renames a small set of known Java texture paths that differ in Bedrock.
- Copies `pack.png` to `pack_icon.png` when present.
- Writes a JSON report with copied assets, warnings, unsupported assets, and
  the selected converter mode.

It reports unsupported files for manual work:

- Java model JSON and blockstate JSON.
- OptiFine `optifine/` assets.
- Java shader overrides.
- `sounds.json` and custom sound folders.
- Java animation `.png.mcmeta` metadata.
- Font and language files that need Bedrock-specific layout review.

## Manual Review Checklist

After conversion:

1. Import the `.mcpack` into a Bedrock client or attach it to a BDS test world.
2. Confirm manifest UUIDs are unique and versions match the world references.
3. Inspect blocks, items, entities, UI screens, particles, and pack icon.
4. Review the conversion report and resolve unsupported entries.
5. If deploying to Geyser, test with a Bedrock client through the crossplay path.

## Output Expectations

Return these items to the user:

- The converted pack path.
- The report path.
- A short summary of copied assets and unsupported assets.
- Any manual follow-up steps needed for Bedrock parity.
