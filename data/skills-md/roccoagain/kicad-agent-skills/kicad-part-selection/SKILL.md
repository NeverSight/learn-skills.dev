---
name: kicad-part-selection
description: "Chooses real, orderable parts for a KiCad design: ratings with margin, a package suited to hand or JLC assembly, stock, lifecycle, JLC Basic vs Extended, and a footprint that matches the exact part number. Records MPN, LCSC and distributor numbers in the schematic. Use when adding or replacing a part (out of stock, obsolete), building a BOM, or when the user asks which part to use."
---

# Choose parts

A part counts as chosen when it has all four of these:
- an exact orderable part number;
- a datasheet that proves its ratings;
- stock where the board will be built;
- a footprint checked against that exact package.

Stock, prices and lifecycle change monthly. Look them up, never answer from memory, and give the date you checked.

## 1. Requirements

Take the worst cases from `kicad-schematic-review` and choose ratings with margin. Easy to miss:
- **Ceramic capacitors** lose capacitance under DC bias. Where the value matters (regulator input and output, timing,
  filters), read the maker's bias curve at the working voltage; high-value parts in small cases lose most of theirs.
  Rating at twice the working voltage is enough only for small decoupling caps.
- **ICs:** every absolute maximum the circuit can reach, not only the supply.
- **Ordering variants:** a value field may hold only part of the number ("TLV9061"). Read the ordering table, list
  the variants that fit (package, temperature, options), and let the user pick when it isn't obvious.

**Package and build:** follow the project's existing package sizes and suppliers (its notes or BOM fields). If they
don't settle hand or machine assembly, ask. JLC Economic assembly takes 0402 and up, and IC pitch 0.4 mm and up.

## 2. Search

**JLC:**
- Search jlcpcb.com/parts or lcsc.com.
- Prefer **Basic** parts, which have no loading fee.
- **Extended** parts carry a fee for each unique part on Economic assembly (about $3 when checked on 2026-11-05; look up
  the current fee). **Preferred Extended** parts skip that fee.
- Record the LCSC number (`C` + digits). Check stock against the build quantity plus attrition.

**DigiKey and Mouser:**
- Filter the parametric search to in stock, active, and cut tape.
- Record the MPN and the distributor's part number.

**Lifecycle:**
- Reject NRND, last-time-buy and obsolete parts.
- Record single-source parts in the design notes, with a fallback if one exists.

**MCP parts search:** if one is connected, use it, then confirm on the distributor's page and in the datasheet.

**Suffixes:** read the datasheet for the exact suffix. It selects package, temperature range and voltage option, and two
suffixes of one part can have different pinouts.

## 3. Footprint

- **Match by dimensions.** Find the package code in the ordering table (TI's `DBV` is SOT-23-5, `DCK` is SC-70-5).
  Match it to a KiCad footprint by pitch, body size and pads, not by name.
- **Check the pinout.** Compare that package's pinout with the symbol's pin numbers (`kicad-library`'s `pinpad.py`).
  Generic symbols often assume a different pinout.
- **No stock footprint fits:** make one with `kicad-library`.

## 4. Record it

Set the project's existing field set on the symbol (`kicad-schematic`). Without one: `Value`, `Footprint`,
`Datasheet` (a stable PDF URL), `MPN`, `Manufacturer`, and the supplier's number (`LCSC`, `DigiKey`, `Mouser`).

The schematic is the BOM's source, so regenerate order files from it (`kicad-assembly-export`). Then carry the fields
to the board with `board.py sync` (`kicad-board-edit`).

## Report

For each part, give:
- the requirement;
- the part number, its key ratings, and the margin on each;
- the package and footprint;
- stock and price, with the date checked;
- Basic or Extended at JLC;
- one alternative.

If stock or lifecycle rules out the obvious part, say so.
