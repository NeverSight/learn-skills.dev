---
name: kicad-check
description: "Runs ERC and DRC (with schematic parity) on a KiCad 10 design, then checks the board against JLCPCB's manufacturing limits, including what DRC can't check (size, thickness, slots, mask, silk). Use after any schematic or board change, before committing, when there are ERC or DRC errors, or when the user asks whether a board can be manufactured. Whether the circuit and layout are right is kicad-schematic-review and kicad-layout-review."
---

# Check a KiCad design

```bash
python3 <skill dir>/check.py board.kicad_pro          # this SKILL.md's folder
```

It runs everything below with KiCad's own checkers, changes nothing in the project, and prints a few lines per
check, ending in PASS or FAIL:
1. **ERC** on the schematic, then **lint** (`kicad-schematic`): overlapping text and wires through parts, as
   warnings.
2. **DRC** with the project's rules, unrouted nets and schematic parity: the same ground as KiCad's DRC dialog.
3. **DRC against JLCPCB's rules**, on a copy, with the rule files in this folder (2-layer or multilayer, picked from
   the board). It reports only findings the project's DRC didn't:
   - **Limits pass:** an error. JLC can't make the board as drawn.
   - **Recommended pass:** a warning. JLC builds it, but it may print poorly or yield worse.

Findings excluded in KiCad (stored in the `.kicad_pro`) aren't reported. The JLC passes end by printing the date
their values were read.

Options:
- `--no-jlc`: run just ERC and DRC.
- `--rules-dir DIR`: take the rule files from DIR instead. They must keep this folder's names
  (`jlcpcb-2layer-limits.kicad_dru`, `jlcpcb-2layer-recommended.kicad_dru` and the `multilayer` pair), even for
  another fab; the output still labels them "JLC".
- `--json out.json`: keep the full reports.

Library warnings (`lib_footprint_issues`, `lib_footprint_mismatch`) are dropped from the JLC passes: the copy can't
reach the project's libraries. The rule files assume JLC's standard FR-4 process with 1 oz outer copper. For 2 oz,
edit the values marked `[2oz]` in copies of both files (same names) in another folder, and pass
`--rules-dir <that folder>`.

## Rule files
- **Comments on their own line.** KiCad 10.0.5 silently skips every rule after a `#` comment that shares a line with
  code.
- **Prove the whole file loads.** Append this rule to a copy:

  ```
  (rule "canary" (condition "A.Type == 'Track'") (constraint track_width (min 1000mm)))
  ```

  Run DRC on a board that has tracks, and confirm that violations of `canary` appear.
- **Test one rule:** raise its minimum to an absurd value in a copy. For a given constraint, the last matching rule
  wins.

JLC's numbers come from jlcpcb.com/capabilities/pcb-capabilities, read on 2026-11-05. Re-check them before an order.

## What DRC can't check

Read these from the `.kicad_pcb` and report them. The values are for JLC's standard FR-4 process.

- **Size:**
  - minimum 3 × 3 mm, or 10 × 10 mm if castellated;
  - maximum 670 × 600 mm (2-layer) or 663 × 593 mm (4-layer);
  - any price-tier limit the user mentions, often 100 × 100 mm.
- **Thickness** (`(general (thickness ...))`): one of 0.4, 0.6, 0.8, 1.0, 1.2, 1.6 or 2.0 mm.
- **Copper:** 1 or 2 oz outer. Inner layers default to 0.5 oz.
- **Slots** (`(drill oval W H)`):
  - plated slots at least 0.5 mm wide;
  - non-plated slots at least 1.0 mm wide;
  - length at least twice the width;
  - rectangular cut-outs have rounded corners.
- **Edges:**
  - copper at least 0.4 mm from a V-cut;
  - castellated holes at least 0.5 mm, ENIG only.
- **Solder mask:**
  - mask bridges at least 0.10 mm (0.13 mm on black or white mask);
  - Board Setup's "Minimum web width" should match.
- **Silkscreen:**
  - line width at least 0.15 mm. Stock footprints use 0.12 mm, which JLC prints, but mention it;
  - text stroke at least 1/6 of the text height. KiCad's default 1.0 mm / 0.15 mm text is just under that; mention
    it, but it isn't an error.
- **Assembly:** see `kicad-assembly-export`.

## Report

- **Order:** errors first, then warnings. For each, give the location (board mm) and its physical meaning.
- **Repeats:** group them, e.g. "21 × silk clipped by edge, all at the jack footprints".
- **Accepted findings:** check the design notes (DESIGN.md, CLAUDE.md, AGENTS.md) and mark findings already accepted
  there as "expected".
- **Fixes:** propose a fix for each new finding, and re-run the checks until no errors remain. Look at each spot with
  `kicad-view`.
