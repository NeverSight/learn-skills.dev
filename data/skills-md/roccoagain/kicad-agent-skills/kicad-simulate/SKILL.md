---
name: kicad-simulate
description: "Simulates part of a KiCad 10 schematic with ngspice from the command line: frequency response, -3 dB points, gain, clipping, transients, start-up and fault currents, using vendor models or ideal stand-ins. Use when a design decision depends on a frequency response, transient, headroom or power figure that is hard to work out by hand, or to back up a kicad-schematic-review finding."
---

# Simulate a circuit

Start from a specific question, such as "where is the -3 dB point?" or "does it clip at the largest input?". Simulate
only the stage that answers it. For a single RC or a divider, show the formula instead. Always say which models you
used.

## Setup

KiCad doesn't include the ngspice command-line program. Install it with `brew install ngspice` or
`apt install ngspice`; on Windows, use the zip from ngspice.sourceforge.io. This skill was tested with ngspice 47.

Run it in batch mode: `ngspice -b deck.cir`.

## 1. Get the circuit

`K` is `kicad-cli` (see `kicad-view`).

```bash
"$K" sch export netlist --format spice -o <scratch>/board.cir board.kicad_sch
```

- **Passives** export ready to use (`R2 +5V /VMID 10k`). KiCad converts the values (`4k7` becomes `4.7k`, `1M`
  becomes `1Meg`).
- **Nets** keep KiCad's names. `GND` is node 0.
- **Parts without a model** export as placeholders (`U1 __U1`). Replace or delete every one.
- **One stage:** copy that stage's lines into a new deck and drive its inputs with sources.

## 2. Write the deck

```
* <the question>
V1 in 0 DC 0 AC 1 SIN(0 0.1 1k)
VCC vcc 0 5
X1 in fb out vcc 0 OPAMP_MODEL        ; pins in the model's .subckt order
R1 out fb 10k
R2 fb 0 1k
RL out 0 10k                          ; the real load
.include /abs/path/vendor_model.lib
.control
ac dec 50 10 10Meg
meas ac gain_lf find vdb(out) at=100
let target = gain_lf - 3
meas ac f3db when vdb(out)=$&target fall=1
wrdata <scratch>/ac.txt vdb(out)
tran 10u 3m
meas tran vpk max v(out) from=1m to=3m
.endc
.end
```

- **`M` means milli.** SPICE ignores any letters after a scale factor. In decks you write yourself, use `1Meg` and
  `4.7k`. ngspice reads `4k7` as 4 kΩ and `1M` as 1 mΩ, and gives no warning. The scale factors are
  `f p n u m k Meg G T`.
- **Vendor models:** download them from the maker's product page. The `.subckt` line lists the pins in the model's own
  order, so map each one to the right node. Getting this order wrong is the most common simulation mistake.
- **PSpice-only models:** put `set ngbehavior=ps` in a `.spiceinit` file in the working folder.
- **No model, or none needed:** stand in an ideal part and report it as an idealisation:
  - op-amp: a one-pole controlled source set from the GBW;
  - diode: `IS`, `N` and `RS` fitted to the datasheet's forward curve.
- **Fault cases:** add the fault source, such as 12 V on a signal input. To measure a branch current, put a 0 V source
  in series with the branch and read `i(Vx)`.

## 3. Run and read

```bash
cd <scratch> && ngspice -b deck.cir 2>&1 | grep -v '^$'
```

- **`meas`** prints `name = value`. "out of interval" means the condition never occurred, so widen the sweep or check
  the circuit.
- **`i(V1)`** is the current into the source's + terminal, which is negative when the source delivers current.
- **`wrdata`** writes from the current plot. Put it right after its analysis, or run `setplot ac1` first.
- **Check against a hand estimate:** compare the low-frequency gain with the resistor ratio, and the -3 dB point with
  GBW/gain or 1/(2πRC). A result that disagrees with the estimate is wrong until you can explain it. A gain that never
  falls usually means a model or unit mistake.

## Report

Give:
- the question;
- what you simulated: the parts, the models, and anything idealised;
- each result with its conditions: supply, load, input level, and temperature (27 °C unless set);
- the hand estimate beside each result.

Keep the deck in `<scratch>`. If the project wants to keep it, put it in `sim/` and add a line to the design notes.
