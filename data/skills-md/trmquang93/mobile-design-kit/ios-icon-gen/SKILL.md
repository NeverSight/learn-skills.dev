---
name: ios-icon-gen
description: Generate iOS app icons as PNG imagesets for Xcode asset catalogs. Two sources available -- SF Symbols (macOS built-in, 5000+ icons) and Iconify API (275k+ open source icons from 200+ collections like Material Design, Lucide, Tabler, Phosphor). Use when the user asks to "generate icons", "create icon assets", "add icons to asset catalog", "search for icons", or needs PNG icons for an iOS project.
argument-hint: '[search <query> | <icon-source> <asset-name> [options]]'
allowed-tools: Read, Bash, Glob, Grep, Write
---

# iOS Icon Generator

Generate PNG icon imagesets for Xcode asset catalogs from two sources:

| Source | Icons | Requires | Best for |
|--------|-------|----------|----------|
| **Iconify API** | 275,000+ from 200+ collections | Internet | Wide selection, specific icon styles, open source icons |
| **SF Symbols** | 5,000+ Apple symbols | macOS only | Apple-native style, offline use |

## Scripts

```
$SKILL_DIR/scripts/iconify_gen.sh      # Iconify API (recommended)
$SKILL_DIR/scripts/generate_icons.swift # SF Symbols
```

---

## Method 1: Iconify API (Recommended)

### Search for icons

```bash
$SKILL_DIR/scripts/iconify_gen.sh search <query> [--prefix <collection>] [--limit <n>]
```

Examples:
```bash
# Search all collections
$SKILL_DIR/scripts/iconify_gen.sh search "receipt"

# Search within a specific collection
$SKILL_DIR/scripts/iconify_gen.sh search "business card" --prefix mdi

# List available collections
$SKILL_DIR/scripts/iconify_gen.sh collections
```

### Generate icon

```bash
$SKILL_DIR/scripts/iconify_gen.sh <collection:icon-name> <asset-name> [options]
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--size <pt>` | 68 | Base size in points. Generates 1x, 2x, 3x |
| `--color <hex>` | 8E8E93 | Hex color code without # |
| `--output <dir>` | /tmp/icons | Output directory |

Examples:
```bash
# Basic
$SKILL_DIR/scripts/iconify_gen.sh mdi:receipt-text-outline editTool_expenseReport

# Custom color, direct to asset catalog
$SKILL_DIR/scripts/iconify_gen.sh mdi:business-card-outline myCardIcon --color 007AFF --output ./Assets.xcassets/icons

# Preview before generating
$SKILL_DIR/scripts/iconify_gen.sh preview mdi:receipt-text-outline
```

### Popular collections

| Prefix | Name | Count | Style |
|--------|------|-------|-------|
| `mdi` | Material Design Icons | 7400+ | Filled + outline variants |
| `ph` | Phosphor | 9000+ | 6 weights per icon |
| `solar` | Solar | 7400+ | Bold, linear, outline |
| `tabler` | Tabler Icons | 6000+ | Consistent stroke width |
| `lucide` | Lucide | 1700+ | Clean, minimal |
| `ri` | Remix Icon | 3100+ | Filled + line variants |
| `carbon` | Carbon | 2400+ | IBM design language |
| `heroicons` | HeroIcons | 1200+ | Tailwind CSS companion |

Browse all: https://icon-sets.iconify.design/

### Workflow: find and generate

```bash
# 1. Search
$SKILL_DIR/scripts/iconify_gen.sh search "document scan" --prefix mdi

# 2. Preview (optional)
$SKILL_DIR/scripts/iconify_gen.sh preview mdi:document-scanner

# 3. Generate
$SKILL_DIR/scripts/iconify_gen.sh mdi:document-scanner scanIcon --output ./Assets.xcassets/icons
```

---

## Method 2: SF Symbols

### Generate icon

```bash
swift $SKILL_DIR/scripts/generate_icons.swift <sf-symbol-name> <asset-name> [options]
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--size <pt>` | 68 | Base size in points. Generates 1x, 2x, 3x |
| `--color <hex>` | 8E8E93 | Hex color code without # |
| `--weight <name>` | thin | ultralight, thin, light, regular, medium, semibold, bold, heavy, black |
| `--output <dir>` | /tmp/icons | Output directory |

Examples:
```bash
swift $SKILL_DIR/scripts/generate_icons.swift doc.text.below.ecg editTool_expenseReport
swift $SKILL_DIR/scripts/generate_icons.swift person.crop.rectangle myIcon --color 007AFF --weight regular
swift $SKILL_DIR/scripts/generate_icons.swift star.fill starIcon --size 48 --output ./Assets.xcassets/icons
```

### Common SF Symbol names

| Use Case | Symbol Name |
|----------|-------------|
| Document | `doc.text`, `doc.fill` |
| Receipt | `doc.text.below.ecg`, `receipt` |
| Business Card | `person.crop.rectangle`, `person.text.rectangle` |
| Camera | `camera`, `camera.fill` |
| Scan | `doc.viewfinder`, `qrcode.viewfinder` |
| Signature | `signature` |
| OCR/Text | `doc.text.magnifyingglass`, `text.viewfinder` |
| Settings | `gearshape`, `slider.horizontal.3` |
| Share | `square.and.arrow.up` |

Browse: Open the **SF Symbols** app (free from Apple).

---

## Output Format

Both methods produce a complete Xcode imageset:

```
<output-dir>/<asset-name>.imageset/
  Contents.json
  <asset-name>.png        # 1x (68px default)
  <asset-name>@2x.png     # 2x (136px default)
  <asset-name>@3x.png     # 3x (204px default)
```

## After Generation

1. **Verify visually** -- Read the @2x PNG to preview
2. **Copy to asset catalog** (if not output there directly):
   ```bash
   cp -r /tmp/icons/<name>.imageset path/to/Assets.xcassets/<group>/
   ```
3. **Build** to verify Xcode picks up the new assets

## Matching Existing Project Icons

Before generating, check the existing icon style:

1. Read an existing @2x PNG to see visual style
2. Check dimensions: `sips -g pixelWidth -g pixelHeight <existing>@2x.png`
3. Match color, weight/style, and size accordingly
