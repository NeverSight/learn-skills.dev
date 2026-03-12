---
name: baoyu-compress-image
description: "Compresses images to JPEG/WebP/PNG using an automated multi-platform CLI (sips, cwebp, sharp). Washed for Obsidian Creator Vault: defaults to JPEG at 65 quality (for <1MB output), and auto-archives original files."
---

# baoyu-compress-image

Auto-compresses images using the best available CLI tool on the system (`sips`, `cwebp`, `convert`, or `sharp`).

This has been specifically adapted for the Obsidian Creator Vault:
- **Fast Web-focused**: Defaults to generating `.jpg` with `65` quality (perfect for most platform limits < 1MB).
- **Clean Vault**: When run in default mode (replace), it doesn't clutter your `Assets/` with `_original` files. Instead, it backs up the original unmodified file to `Archive/Original-Images/`. 
- **Dependency Sandboxing**: All runtime is wrapped through `bun` and isolated inside `.agents/skills`.

## Installation & System Requirements

This script automatically detects your OS and uses the fastest and highest quality image engine it can find in this order:

1. **macOS `sips` (Built-in, Highly Recommended)**  
   macOS ships with `sips` natively. No installation required.  
   *(Under the hood: `sips -s format jpeg -s formatOptions 65 <input> --out <output>`)*
   
2. **`cwebp` (Best for webp targets)**  
   - macOS: `brew install webp`
   - Ubuntu/Debian: `sudo apt install webp`

3. **ImageMagick (`convert`)**  
   - macOS: `brew install imagemagick`
   - Linux: `sudo apt install imagemagick`

4. **`sharp` (Node.js fallback for Windows / Non-Native Envs)**  
   Automatically installed when you run the local `bun install` command. The sharp engine handles compression via libvips without needing external binaries.

**First Time Setup (TS Environment):**
```bash
cd .agents/skills/baoyu-compress-image
bun install
```

## Usage

Run the script using `bun` from the root of the vault. 

```bash
bun .agents/skills/baoyu-compress-image/scripts/main.ts <input> [options]
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `<input>` | | Input target (File or directory) | Required |
| `--output` | `-o` | Strict output file path | Same dir as input |
| `--format` | `-f` | Output format (`jpeg`, `webp`, `png`) | `jpeg` |
| `--quality` | `-q` | Quality Level `0-100` | `65` |
| `--keep` | `-k` | Keep original file in-place (don't archive it) | `false` |
| `--recursive` | `-r` | Process directories recursively | `false` |

## Examples & Workflows

**1. Compress a generated AI image for publishing (Default)**
```bash
bun .agents/skills/baoyu-compress-image/scripts/main.ts Assets/cover-draft.png
```
*Effect*: It creates `Assets/cover-draft.jpg` and safely moves `cover-draft.png` out of the way into `Archive/Original-Images/`.

**2. Compress an image but keep it as WebP format**
```bash
bun .agents/skills/baoyu-compress-image/scripts/main.ts Assets/screenshot.png -f webp
```

**3. Test different quality manually and keep the original there**
```bash
bun .agents/skills/baoyu-compress-image/scripts/main.ts Assets/photo.png -q 80 --keep
```

**4. Batch-compress an entire directory**
```bash
bun .agents/skills/baoyu-compress-image/scripts/main.ts "00 Inbox/" -r
```
