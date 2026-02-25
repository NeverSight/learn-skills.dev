---
name: epub-chinese-cleaner
description: Convert Chinese-language epub files from vertical layout (直排) to horizontal layout (橫排) with punctuation normalization and left-to-right page flow. Use when a user has a Chinese epub with vertical text direction or right-to-left page progression and wants to convert it to standard horizontal reading.
license: MIT
compatibility: Requires Python 3.8+. Optionally uses Calibre with TradSimpChinese plugin for best results.
metadata:
  author: William Yeh <william.pjyeh@gmail.com>
  version: "1.1"
---

# epub-chinese-cleaner

Converts Chinese epub files from vertical (直排) + RTL page flow to horizontal (橫排) + LTR page flow.

## What it does

1. **Detects** whether the epub needs conversion (checks CSS `writing-mode` and OPF `page-progression-direction`)
2. **Converts writing mode** from `vertical-rl` to `horizontal-tb` (including vendor prefixes)
3. **Normalizes punctuation** from vertical Unicode forms to horizontal equivalents
4. **Fixes page direction** by removing `page-progression-direction="rtl"` from OPF spine
5. **Preserves original** — outputs a new file with `_horizontal` suffix

## Usage

Run the conversion script:

    python3 scripts/convert_horizontal.py <input.epub> [-o output.epub]

If no `-o` is specified, output is `<input>_horizontal.epub`.

The script automatically:
- Tries Calibre CLI (TradSimpChinese plugin) if available at standard paths
- Falls back to direct epub manipulation if Calibre is not installed
- Skips conversion if the epub is already horizontal

## Example

    python3 scripts/convert_horizontal.py 三體.epub

Output: `三體_horizontal.epub`

## Self-test

    python3 scripts/convert_horizontal.py --self-test

Creates a test epub with vertical layout, converts it, and verifies the output.

## Punctuation mapping

See [references/punctuation-map.md](references/punctuation-map.md) for the full vertical → horizontal punctuation mapping.
