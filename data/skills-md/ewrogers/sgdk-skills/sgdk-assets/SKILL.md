---
name: sgdk-assets
description: Prepare, import and troubleshoot Mega Drive graphics, palettes, spritesheets, tiles, maps, fonts and audio resources with SGDK ResComp in Docker. Use for .res files, palette or tile budgets, broken imports, sprite cutting and asset pipeline changes.
---

# SGDK assets

Turn source art into SGDK resources without surprising the artist or exceeding the console's budgets.

## Start with the project

1. Find its `.res` files, source art, build instructions and toolchain configuration. Preserve the original art and any palette ordering. Work on derived exports when conversion is needed.
2. Use the project's image. Otherwise use `ewrogers/sgdk:latest`. It supports Linux ARM64 and AMD64; Docker supplies Linux containers on macOS and Windows too. Do not force `--platform` unless testing another architecture.
3. Read the installed manual before adding or changing a resource declaration. Use `/opt/sgdk/bin/rescomp.txt`, the matching headers in `/opt/sgdk/inc`, and examples in `/opt/sgdk/sample`. Verify symbol names and signatures there before writing C. An API from another SGDK version is not evidence.

Run `docker run --rm IMAGE cat /opt/sgdk/bin/rescomp.txt`, replacing `IMAGE` with the chosen image. Commands run as argument arrays from automation. Avoid building shell command strings from asset filenames.

## Import workflow

1. Decide how the asset is used: a moving character, background, scrolling map, font, music or sample. Choose the matching ResComp resource rather than treating everything as a sprite.
2. Agree on frame dimensions, palette ownership, transparency and animation layout. Show a preview when possible. Do not silently quantize colors, resize, crop, reorder palette indices or rewrite source files.
3. Make a small `.res` change. Keep resource names valid C identifiers and paths relative to that `.res` file. Check exact options in the manual.
4. Build in the container. Use `docker run --rm --pull=always --mount "type=bind,source=PROJECT,target=/workspace" IMAGE`, replacing `PROJECT` with the absolute project directory. PowerShell and POSIX shells both support this quoted mount argument. Use `sgdk-project` if installed for project creation or broader build setup.
5. Fix the first resource error, then rebuild. Inspect the generated header and ResComp's resource totals. Consult [importing.md](references/importing.md) for common causes and costs.
6. Test the ROM in an emulator. Check colors, transparency, frame order, sprite dropout and scrolling. A successful build proves conversion and linking, not visual correctness or 60 Hz performance.

## Guardrails

- Separate **hardware limits**, **SGDK implementation choices** and **game policy** when explaining a restriction. Refer to the budget table in the reference.
- Count used pixel indices and per-tile palette needs. A PNG's palette table can contain unused entries; its table length alone does not prove an invalid image.
- Budget shared palettes, resident tile patterns, decompression/upload work and scanline sprite pressure. Standard 8 by 8 patterns have 2048 theoretical addresses; tables and SGDK reservations leave less room for art. Check the actual allocated range before uploads. SGDK logical sprites may contain several hardware sprites. Compression saves ROM; it does not make the decoded tiles free in VRAM.
- Prefer preparing and loading shared data once. Do not decompress images, reload whole palettes or recreate sprites each update without a measured reason. Use SGDK's supported DMA/VBlank flow and check allocation failures.
- Keep generated assembly, headers, objects and ROMs out of source control unless the project explicitly needs them. Retain the authored `.res`, source exports and asset license/provenance.
- For audio, inspect the selected driver's documentation and the `WAV`, `XGM` or `XGM2` declarations in the installed manual. Do not mix driver-specific resources or assume every WAV rate and channel layout is accepted. Audio conversion succeeding does not prove playback quality.

## Small verified example

[assets/import-example](assets/import-example) is a standalone resource project with an indexed background, two-frame sprite and generated resource types used by C. Copy it to a writable project directory before building. Its [README](assets/import-example/README.md) explains the layout and proof limits. For unfamiliar options, build this small case before changing a large asset pipeline.

Report what changed, which image and resource declarations were used, build results, relevant budget changes and anything still needing visual or audio review. Do not claim that estimated totals are measured runtime usage.
