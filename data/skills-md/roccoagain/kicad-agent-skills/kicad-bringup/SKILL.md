---
name: kicad-bringup
description: "Writes or updates a board's bring-up and test plan (TEST_PLAN.md) from its KiCad schematic: visual checks, unpowered resistance readings computed from the netlist, current-limited first power, block-by-block function tests, and a per-board log. Use when a board is about to be ordered or assembled, when the user asks how to test or bring up a board, or after a schematic change that moves a reading."
---

# Write a bring-up plan

The plan should catch an assembly fault before it destroys anything, and point to the faulty part when a reading is
wrong. Compute every expected number from the schematic and datasheets, and show the working so the number can be
recomputed after a change. Read the circuit (`kicad-view`: the sheet plots and the pin list) and the design notes
first.

## TEST_PLAN.md layout

1. **Header:** the board, its revision, and the schematic the numbers come from. Run the stages in order and stop at
   the first failure.
2. **Circuit summary:** the blocks, their parts, and where to probe each.
3. **Stages 0–3:** one table per stage, with the columns `# | Measure / do | Expect | A wrong reading means`.
4. **Log:** one copy per board serial: date, tester, each reading, pass or fail.

## Stage 0: visual, unpowered

Name the fine-pitch parts and the pin pairs most likely to bridge, the polarised parts, and the parts easy to swap
(same package, different value).

## Stage 1: unpowered resistance, no modules fitted

Check each rail to GND, and each pair of nets whose short would cause damage. Include adjacent fine-pitch pins that
carry two different supplies, or a supply and ground. For each pair:
- **Resistor-only paths:** give the number from `view.py ohms board.kicad_sch <net> [GND]` (`kicad-view`), which
  solves the resistor network from the netlist and lists the other parts across the pair.
- **Capacitors:** the reading starts low and climbs. Write "rises to > X" and "never below Y". X is well below the DC
  value. Y is the short limit, a few tens of Ω.
- **IC supply pins:** datasheets rarely give the resistance, so write "not a short (> 100 Ω)" instead of a number you
  can't support.
- **Diodes or clamps across the pair:** give both polarities, and say where the red lead goes.

Run the assembly-fault pass from `kicad-schematic-review` section 3. Each bridge, missing part, rotated part or
wrong-value part that would cause damage at first power must change at least one Stage 1 reading. Add steps until it
does.

## Stage 2: first power, current-limited

- **What's left out:** fit nothing optional yet. List exactly what stays out: modules, jumpers and loads.
- **Current limit:** add up the expected draw (quiescent currents, LEDs, divider currents) and add about 50 %. Show the
  sum. Keep the limit within what the input protection can take.
- **Expected voltages:** include the regulator's accuracy and the resistor and supply tolerances. For example, a
  10k/10k divider of 1 % parts on 5.00 V gives 2.5 V ± 1 %, plus the supply's own tolerance.
- **Modules:** add them one at a time. Raise the limit by each module's draw, then repeat the rail checks.

## Stage 3: function, block by block

For each block: the input to apply, the probe point, and the expected result with its working. Misuse cases that
`kicad-schematic-review` says the board survives may be tested gently, at a low current limit; say what the test risks.

## Keeping it right

After a schematic change, recompute every reading it touches: a plan that disagrees with the schematic is worse than
none.
