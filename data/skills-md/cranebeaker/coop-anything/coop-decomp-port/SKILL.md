---
name: coop-decomp-port
description: Get a console game running natively on PC as source code (decompilation, static recompilation or engine reimplementation) so co-op can be added in code, the way Ocarina of Time co-op works on Ship of Harkinian and Super Mario 64 on sm64coopdx.
---

# Decomp or recomp a console game for co-op

1. Look for an existing PC port, decompilation or static recompilation of the exact game and region. Contributing to one beats starting over.
2. A PC port exists: add networking in its code (host authority, synced flags and items, save state on join, remote players as puppets). Read how Anchor (Ship of Harkinian) and sm64coopdx did it.
3. Only a recompilation exists (N64Recomp, XenonRecomp, PS2 and PS3 recompilers): co-op goes in through its mod or patch hooks; the code is still machine-translated, so expect more reverse engineering.
4. Partial decompilation: help finish the parts you need (player, actors, saves, scene loading) rather than the whole game.
5. Starting a decompilation: split the binary (splat, decomp-toolkit), then match function by function with objdiff as the oracle. Worker agents can match functions in parallel; the lead verifies every match and watches for score gaming. For an agent-run pipeline with a behaviour oracle as the judge, start from DecompPipeline (github.com/GeneralAtrox/DecompPipeline; Dreamcast target, add a target for other CPUs).
6. Legal: never ship ROMs, ISOs or extracted assets. Ports extract assets from the player's own dump at runtime.

Details: `playbook/decomp-and-recomp.md`.
