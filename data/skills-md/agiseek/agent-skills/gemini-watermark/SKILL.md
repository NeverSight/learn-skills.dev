---
name: gemini-watermark
description: Remove visible Gemini AI watermarks from images via reverse alpha blending. Use for cleaning Gemini-generated images, removing the star/sparkle logo watermark, batch watermark removal.
metadata:
  author: agiseek
  version: "2.0.1"
---

# Gemini Watermark Remover

Remove the visible Gemini AI watermark (star/sparkle logo) from generated images using mathematically accurate reverse alpha blending. Fast, offline, single binary with zero runtime dependencies.

## When to Use

- Remove the Gemini watermark from AI-generated images
- Batch process a directory of Gemini-generated images
- Clean images before publishing or sharing
- Automate watermark removal in pipelines

## Quick Start

### Install

**Option 1 — Recommended: Build from source (Rust toolchain required)**

```bash
cargo install gemini-watermark-removal
gemini-watermark --version
```

Building from source lets you audit the code before running it and avoids
dependency on a third-party pre-built binary.

**Option 2 — Pre-built binary (third-party download)**

> **Security notice:** The installer downloads a binary from the
> `easynote-cc` GitHub organization, which is an independent third party.
> Review the source at `https://github.com/easynote-cc/gemini-watermark-removal`
> before proceeding. SHA256 verification is mandatory; the install will abort
> if the checksum file is missing.

```bash
# Interactive (asks for confirmation before downloading)
./scripts/install.sh

# Non-interactive (auto-confirm, e.g. in a script)
./scripts/install.sh --yes

# Install a specific pinned version
VERSION=v0.1.1 ./scripts/install.sh
```

Supported platforms: macOS (Apple Silicon / Intel), Linux (x86_64 / ARM64),
Windows (x86_64, via Git Bash / MSYS2).

### Basic Usage

```bash
# Single image (auto-detect watermark, save as photo_cleaned.jpg)
./scripts/gemini-watermark photo.jpg

# Specify output path
./scripts/gemini-watermark photo.jpg -o clean_photo.jpg

# Batch process directory
./scripts/gemini-watermark ./input_dir -o ./output_dir

# Force removal without detection
./scripts/gemini-watermark photo.jpg -o clean.jpg --force
```

## How It Works

Gemini adds a semi-transparent white star/sparkle logo to generated images using alpha blending:

```
watermarked = alpha * 255 + (1 - alpha) * original
```

This tool reverses the equation to recover the original pixels:

```
original = (watermarked - alpha * 255) / (1 - alpha)
```

The alpha maps (watermark transparency patterns) are embedded in the binary at two sizes:
- **48x48** with 32px margin: for images where either dimension <= 1024px
- **96x96** with 64px margin: for images where both dimensions > 1024px

### Detection

Before removal, a three-stage detection algorithm checks if a watermark is present:
1. **Spatial NCC** (50% weight): normalized cross-correlation with the alpha map
2. **Gradient NCC** (30% weight): edge signature matching via Sobel operators
3. **Variance Analysis** (20% weight): texture dampening detection

Images without detected watermarks are automatically skipped to protect originals.

## CLI Parameters

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `input` | | (required) | Input image file or directory |
| `--output` | `-o` | `{name}_cleaned.{ext}` | Output file or directory |
| `--force` | `-f` | `false` | Skip detection, process unconditionally |
| `--threshold` | `-t` | `0.25` | Detection confidence threshold (0.0-1.0) |
| `--force-small` | | `false` | Force 48x48 watermark size |
| `--force-large` | | `false` | Force 96x96 watermark size |
| `--verbose` | `-v` | `false` | Enable detailed output |
| `--quiet` | `-q` | `false` | Suppress all non-error output |

## Supported Formats

| Format | Read | Write |
|--------|------|-------|
| JPEG (.jpg, .jpeg) | Yes | Yes (quality 100) |
| PNG (.png) | Yes | Yes |
| WebP (.webp) | Yes | Yes |
| BMP (.bmp) | Yes | Yes |

## Usage Examples

```bash
# Remove watermark with verbose output
./scripts/gemini-watermark photo.png -o clean.png -v

# Lower detection threshold (more sensitive)
./scripts/gemini-watermark photo.jpg -t 0.15

# Force large watermark size regardless of image dimensions
./scripts/gemini-watermark photo.jpg --force-large -o clean.jpg

# Batch process, quiet mode
./scripts/gemini-watermark ./gemini_images/ -o ./cleaned/ -q

# Force removal on all images in batch (no detection)
./scripts/gemini-watermark ./images/ -o ./output/ --force
```

## Output

- **Single file**: Saves to specified `-o` path, or `{name}_cleaned.{ext}` by default
- **Directory**: Saves all processed images to the output directory with original filenames
- **Skipped images**: Images without detected watermarks are not processed (unless `--force`)
- **Exit code**: 0 on success, 1 if any image fails

## Troubleshooting

### Download failed or checksum missing during install

If the SHA256 checksum file is absent for a release, the installer will abort to
protect you from an unverified binary. Build from source instead:
```bash
cargo install gemini-watermark-removal
```

### Unsupported platform

`cargo install` works on any platform with a Rust toolchain. The pre-built binary
installer covers macOS, Linux, and Windows (Git Bash / MSYS2) only.

### "No watermark detected" on a watermarked image
- Try lowering the threshold: `-t 0.1`
- Or use `--force` to skip detection

### Image looks distorted after removal
- The image may not have a Gemini watermark. Use detection (don't use `--force`)
- Try `--force-small` or `--force-large` to match the correct watermark size

### "Image too small" warning
The image dimensions are smaller than the watermark region. This typically means the image does not have a Gemini watermark.

## Limitations

- **Visible watermark only**: This tool removes the visible star/sparkle logo watermark
- **Cannot remove SynthID**: Google's invisible watermark (SynthID) is embedded at the pixel level during generation and cannot be reversed
- **Fixed positions only**: Only handles watermarks in the standard bottom-right position
