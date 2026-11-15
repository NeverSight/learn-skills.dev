---
name: kicad-schematic-review
description: "Reviews a KiCad schematic's electrical design (the circuit, not the board) against datasheets: what each connector can see (power states, misuse, ESD), absolute maximum ratings, clamp current, resistor and capacitor ratings and derating, floating inputs, interfaces between boards. Use before ordering, after a schematic change, when adding a part, or when the user asks whether an input can take a voltage or whether the design survives a fault. For the board layout, use kicad-layout-review; for ERC, DRC and manufacturing limits, kicad-check."
---

# Review a schematic

This covers the schematic: what each part sees electrically. Where parts sit and how they're connected on the board
is `kicad-layout-review`.

Read the schematic and netlist (`kicad-view`) and each part's datasheet. Two netlist checks to run first:
`view.py decoupling` (every IC supply pin has a capacitor on its rail) and, if the design notes list key connections
as `` `U2.4 = +3V3` `` lines, `view.py expect board.kicad_sch DESIGN.md`. Back anything that depends on a frequency
response or transient with `kicad-simulate`. Give every number with its source. The output is a table the user can
check, not a verdict.

## 1. State the environment

Write these down, and confirm any guesses with the user:
- **Rails:** the range of each rail while on (e.g. 5 V ± 5 %).
- **Power states:**
  - on;
  - off with signals still connected;
  - partly powered from another source (e.g. a module on USB with the main supply off);
  - bench bring-up with parts missing;
  - supply reversed.
- **Each connector pin:** what normally drives or loads it (level, source impedance, frequency), and what can happen by
  mistake:
  - a wire on the wrong terminal;
  - a short to a supply;
  - a hot-plug;
  - ESD from a touch;
  - a louder source than intended.

  Misuse may stop the board working, but it must not damage anything.

## 2. Check each case

Take one power state or one misuse at a time, with everything else normal. Find the worst-case voltage at every IC
pin, with tolerances at their worst corner. A coupling cap passes a sine unchanged, but a step can double the swing
behind it.

| Check | Pass when |
|---|---|
| Absolute max, every IC pin | Inside the rating, including relative to its own rails when they're at 0 V |
| Clamp diodes | Current through the series resistance stays under the injection rating. If the datasheet gives no rating, report that as a risk |
| Operating range | Inputs stay inside the common-mode range, and outputs don't clip at the levels the design assumes |
| Resistor power | V²/R at worst case, under the rating (0402 ≈ 0.063 W, 0603 ≈ 0.1 W, 0805 ≈ 0.125 W, 1206 ≈ 0.25 W unless stated), derated above about 70 °C |
| Resistor voltage | Under the maximum working voltage (typically 50 V for 0402 and 0603, 150 V for 0805, 200 V for 1206): it limits high-voltage dividers before power does. Surge or pulse loads need a pulse-rated part |
| Capacitor voltage | Under the rating. Electrolytics are never reverse-biased by more than ≈ 0.5 V |
| Ceramic DC bias | Where the capacitance matters (regulator input and output, timing, filters), the maker's bias curve at the working voltage, less tolerance and temperature drift, still meets the requirement. A 10 µF 0402/0603 X5R can lose 50–80 % at half its rating. The "≤ 50 % of rated voltage" rule is enough only for small decoupling caps |
| Regulator stability | Output capacitance after DC bias, and its ESR, inside the range the regulator's datasheet requires |
| Dissipation | Every LDO ((Vin − Vout) · I at worst-case Vin), regulator and MOSFET: Tj = Ta + P · θJA stays under Tj max, with θJA for the actual copper area |
| MOSFETs, switches | Vgs and Vds inside ratings, current under the limit, and the gate never floats |
| Output loads | At least the minimum load impedance, and current under the limit, including a shorted connector |
| ESD | Every exposed pin has a TVS or ESD diode at the connector, rated for the signal's swing |
| Floating inputs | Every input has a DC path to a defined level in every power state |
| Start-up | Boot and strap pins are at the intended level at power-up, and programming/debug pins are reachable |
| Polarity and pinout | Each diode's, LED's and SOT-23 transistor's symbol pin numbers match the footprint for the exact part (BCE vs EBC differs by maker) |
| Board interfaces | Each signal stays within what the other board's notes accept |

If an assumed value decides a pass or fail, report the assumption itself as a finding.

## 3. Test plan and assembly faults

If the project has a bring-up plan (`kicad-bringup`):
- Recompute each expected reading from the schematic, and propose a correction for any that changed.
- Go through the likely assembly faults:
  - bridges between adjacent pins of fine-pitch parts and connectors;
  - a part missing, rotated, or the wrong value;
  - a rail shorted to its neighbour.

  For each fault, does it cause damage at first power, and would an unpowered reading in the plan catch it first?
  Propose readings for the damaging faults the plan misses.

## 4. Report

- **Findings, worst first.** For each: what happens physically, in which case, the numbers and their sources, and a fix
  (or "accept, because ...") for the user to decide.
- **Passed checks**, closest to their limits first, so the user can see the margins.
- **Design notes.** Record only decisions the user accepted, with the reason. If a number in the notes is wrong, say so,
  and edit the notes only with the user's agreement.
