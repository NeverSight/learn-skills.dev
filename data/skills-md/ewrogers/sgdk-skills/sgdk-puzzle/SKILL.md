---
name: sgdk-puzzle
description: Build SGDK grid and falling-block puzzles with atomic pushes, switches, gates, undo, piece rotation, lock timing, row clearing and deterministic board tests. Use when designing discrete puzzle rules, fixing partial moves or invalid rotations, or proving authored rooms are solvable; keep rendering separate from board state.
---

# SGDK puzzle

Make the board authoritative. A sprite crossing a cell boundary is presentation,
not proof that a push, rotation or clear is legal. SGDK supplies input, tiles and
audio; puzzle rules are application C code.

## Choose the rules before the renderer

Identify the puzzle family: push-and-switch, falling blocks, matching, routing,
or something else. Ask about uncertain rules that affect legality or outcomes.
Do not turn every puzzle into the included examples. Their art, music, board
layouts, scoring, rotation rules and timing are illustrative, not prescriptions.

Read [responsibility boundaries](references/boundaries.md) before crossing into
map importing, collision, input, saves or replay. Keep the game's established
clock and input snapshot; do not introduce another gameplay framework.

## Treat a move as a transaction

For a grid puzzle, separate immutable terrain, logical occupants and derived
state. Validate every destination and required capacity before changing live
state. Either commit the complete move, including triggered changes, or leave
the board and history untouched. Bound multi-object pushes or propagation.

Specify trigger ordering and gate closure around occupants. Decide whether a
failed push consumes a turn, how hazards resolve, and when completion occurs.
Derive doors and objectives from the resulting snapshot rather than leaving
stale cached flags. Read [grid rules and undo](references/grid.md).

Store bounded logical snapshots or reversible commands for undo. Include every
rule-affecting value, including RNG when used. Keep animation/audio handles out
of history. Explain what happens when history fills, and provide restart when
an authored puzzle can deadlock. Undo is not a persistent save format.

## Give falling blocks a separate resolution model

Represent an active piece separately from settled cells. Test the whole candidate
footprint for movement and rotation; apply a documented, bounded kick search if
the game needs one. Compute the landing preview through the same legality query.

Separate gravity, held-input repeat and lock timing. State which actions reset
lock delay, how soft/hard drops work, and what top-out means. Commit the piece,
identify complete rows from one snapshot, compact once, score once, then spawn
the next piece. Do not clear rows while still scanning a moving board.

Use deterministic randomization with a recorded seed/state and the distribution
the game requests. A shuffle bag is an option, not a guarantee of fair difficulty.
Read [falling blocks](references/blocks.md) for the executable Lab's policy and
bounded alternatives for match/cascade puzzles.

## Present committed results

Interpolate toward the committed board; choose whether input waits, buffers or
cancels during motion. Undo/restart must resynchronize presentation. Pause should
freeze the intended clocks and consume stale input edges deliberately.

Use tile planes for dense board cells where practical. Upload changed regions
or a small retained board during VBlank; keep queued DMA sources alive until
consumed. Reserve sprites for actors/effects that benefit from them. Keep HUD
text over a readable panel and make blocked moves, goals and completion clear.

Pull `ewrogers/sgdk:latest` before building and verify actual installed headers
for unfamiliar API calls. [SGDK adapters and budgets](references/sgdk.md) records
the checked APIs, memory/transfer costs and evidence limits.

## Prove the board, then play it

Test failed operations without side effects, edge cells, blocked and chained
pushes, trigger changes, undo/restart and history eviction. Independently search
small authored rooms for solutions; random play is not a solvability proof.
For falling blocks, test footprints, blocked rotations, bounded kicks, lock
deadlines, simultaneous clears, bag distribution, spawn failure and both video
schedules. Compare optimized host and base-68000 execution.

[Puzzle Labs](assets/puzzle-lab/README.md) builds two independent ROMs:
Clockwork Garden's three push/gate/bridge rooms and Falling Lanterns' falling
blocks. Both include original native art, FM music, finite PCM cues and pause.
Use emulator playtests to check readability and feel; host/CPU checks do not
certify VDP timing, audio quality or physical-console behavior.
