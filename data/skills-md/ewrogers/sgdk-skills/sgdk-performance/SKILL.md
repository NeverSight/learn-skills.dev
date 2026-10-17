---
name: sgdk-performance
description: Measure and optimize SGDK game performance with repeatable workloads, CPU/load counters, DMA and scanline budgets, and behavior-preserving comparisons. Use for frame-rate headroom and profiling, rather than general build failures or choosing a game's initial scope.
---

# SGDK Performance

Find the cost before changing the code. Establish the target display mode,
optimized build, representative workload and expected behavior. Keep the game's
architecture unless a measured bottleneck justifies a change.

## Choose the right reference

- [Measuring frame work](references/measurement.md): SGDK counters, recording
  windows, instrumentation overhead and fair comparisons.
- [CPU and data layout](references/cpu-and-data.md): collision broad phases,
  fixed-point arithmetic, pools, compiler output and assembly decisions.
- [Transfers and rendering](references/transfers-and-rendering.md): DMA queues,
  sprite scanlines, tile storage and audio contention.
- [Performance Lab](assets/performance-lab/README.md): deterministic moving
  bodies, equivalent collision queries, animation/DMA switches and an overlay
  comparison. It includes an emulator checklist and build command.

Use `ewrogers/sgdk:latest`, as shown in the lab. Check unfamiliar APIs against that image's `inc/sys.h`, `src/sys.c`,
`inc/timer.h`, `src/timer.c`, `inc/dma.h` and `inc/sprite_eng.h`.

## Run a controlled comparison

Record the seed or replay, active object counts, display region, viewport,
animation and sound state. Reproduce a normal scene and a busy case. Repeat
the same scene with diagnostics hidden: text formatting, VRAM writes and logging
can become the bottleneck themselves.

Use optimized release builds on both sides of a comparison. Warm up counters,
record a bounded interval and keep peaks and missed updates visible alongside
averages. Host CPU use and emulator presentation FPS do not measure 68000 work.
SGDK's load estimate is useful but is not an instruction counter.

Separate simulation CPU, transfers, scanline rendering and memory occupancy.
Low CPU load cannot prove a frame's DMA fits or prevent sprite dropout. Reducing
art, update frequency or collision checks is a behavior change unless the game
still produces its required results. Report that tradeoff explicitly.

## Optimize one cause at a time

Start with repeated work and algorithmic cost: candidate filtering, cached
lookups, dirty updates, bounded pools and sensible transfer granularity.
Keep an executable reference implementation when replacing a tricky algorithm.
Compare exact outputs where practical, not just a checksum or a faster counter.

Inspect generated 68000 code for a measured hot path before writing assembly.
Preserve signedness, overflow, fixed-point scaling and memory ownership. A small
RAM cost may buy useful CPU headroom, but account for it separately from VRAM.
Do not impose a universal CPU percentage target or claim that a synthetic lab
certifies a whole game.

Report the build/image, workload, observed result and correctness checks. Say
which tests ran on the host, which compiled for the target and which were tried
in an emulator or on a console. Do not turn compile success into a frame-rate
claim or invent profiler support that the selected emulator does not provide.
