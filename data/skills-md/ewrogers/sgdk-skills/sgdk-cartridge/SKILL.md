---
name: sgdk-cartridge
description: Plan and implement large SGDK cartridges with Sega/SSF bank switching, FAR resources, pinned shared code and audio, and safe SRAM access. Use when a ROM exceeds the linear address window, stage assets live in separate banks, a FAR pointer becomes invalid, or saving interferes with banked content.
---

# SGDK Cartridge

Keep common code and assets reachable while loading different parts of a large
ROM. Use the mapper the target cartridge actually supports. Banking is a board
feature, not extra RAM or a way around VRAM and DMA limits.

## Establish the target

1. Identify ROM size, intended emulator/flash cart/physical board, SRAM wiring,
   and existing linker layout. Ordinary cartridges expose up to 4 MiB linearly;
   using SRAM can overlay part of that window. Do not add banking to a small
   game without a reason.
2. Pull `ewrogers/sgdk:latest`, run `doctor`, and inspect its `inc/mapper.h`,
   `inc/config.h`, `md.ld`, ResComp manual, and the chosen audio driver's source.
   The references below were checked with SGDK 2.11. Review differences when
   the image changes.
3. Separate physical ROM offsets from CPU addresses. Write down who owns each
   mapper window, which resources must stay pinned, and when a temporary view
   may change. See [mapping and resource lifetime](references/mapping.md).

## Implement a small proof

- Rebuild the SDK with `ENABLE_BANK_SWITCH=1`, including the library. Setting a
  flag only on game sources does not change an already compiled library.
- Keep entry points, interrupts, shared sprite metadata, hero/UI assets and
  initialized-data load bytes in stable storage. `NEAR` alone does not prove
  that something fits the fixed first bank. Add linker assertions.
- Read FAR resources through the selected SDK's helpers. Copy small values to
  owned RAM when they must survive another mapping. Never retain a transient
  mapped pointer in a scene, queue or callback without an explicit lifetime.
- Check actual ELF load sections and final ROM bytes. A symbol's address alone
  does not prove that its payload was emitted.
- Finish queued DMA readers before remapping their source, or queue a copy of
  owned RAM. Plan sprite uploads and interrupts as readers too.
- Reserve a stable audio window for a playing stream and its samples. A play
  call does not copy the entire song into Z80 RAM. Quiesce the driver before
  changing that window. See [audio and saves](references/audio-and-sram.md).
- Keep SRAM operations short, close its overlay on every path, and preserve
  mapper assignments. Use validated, versioned records. A checksum detects
  corruption; it does not make a single-slot write power-loss safe.

Adapt the [Bank Lab](assets/bank-lab/README.md) rather than inventing mapper
register calls. Its private SDK build leaves the installed container unchanged.
It demonstrates two stage banks, pinned common content, a cross-bank read,
queued palette copies, banked FM music and SRAM save/load. Its deliberately
sparse 6 MiB layout is a proof, not a recommended cartridge size.

## Validate and report

- Host tests: reject invalid ranges and saves, verify view invalidation,
  audio handoff order and unchanged bank assignments across SRAM access.
- Container builds: release and debug, base 68000 code, bank-enabled SDK,
  placement assertions, payload bytes, header, padding and SDK checksum.
- Emulator: switch stages repeatedly during music; save, move, switch and load;
  verify shared graphics, audio and checks remain intact.
- Hardware: validate the actual board/flash-cart mapper, SRAM and region.
  Emulator success is not evidence of physical cartridge compatibility.

Report the physical layout, window ownership, RAM staging cost, tool versions,
commands and tests performed. Keep ROM mapping, VRAM, DMA, sprite scanlines and
CPU budgets separate. Do not silently reset all banks or rewrite a project's
mapper/header to make a test pass.
