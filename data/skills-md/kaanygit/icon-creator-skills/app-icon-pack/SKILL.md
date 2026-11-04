---
name: app-icon-pack
description: Convert one master app icon into platform asset packs for iOS, Android, Web, macOS, watchOS, and Windows.
---

# app-icon-pack

Use this skill when the user has a `master.png` and wants ready-to-drop app icon assets.

## How to invoke

```bash
icon-skills create-app-icon-pack \
  --master output/example/master.png \
  --app-name "Example" \
  --platforms ios,android,web,macos,watchos,windows
```

Optional arguments:

- `--output-dir <path>`: output root, default `output`
- `--platforms <list>`: comma-separated list; defaults to `ios,android,web`
- `--bg-color <hex>`: background color for opaque platform assets, default `#FFFFFF`
- `--no-zip`: skip zip creation
- `--no-validate`: skip generated-file validation

The script prints the generated asset-pack directory on the last stdout line.

## Current limits

PNG masters are fully supported. SVG masters require optional `cairosvg`. Background removal and Android vector drawable conversion are intentionally deferred.
