---
name: akcli-altium-interop
description: >-
  Work with Altium Designer through the `akcli` CLI — Altium is akcli's read-only
  import surface into the KiCad-first flow: parse Altium .SchDoc/.SchLib/.PcbDoc
  files, export normalized JSON and Protel/KiCad/CSV netlists, deliver schematic
  edits back into Altium (offline human draw instructions + importable netlist —
  there is no Altium write path at all), and migrate Altium designs to KiCad with
  netlist-diff verification. Use this
  skill whenever the task involves: reading, exporting, or converting an Altium file;
  getting a design out of Altium into another tool; getting changes into an Altium
  schematic; or an Altium-to-KiCad migration or equivalence check.
  Triggers on keywords: Altium, Altium Designer, SchDoc, SchLib,
  PcbDoc, Protel netlist, OLE2/CFBF, Altium export, Altium import, migrate to KiCad,
  AD to KiCad.
---

# akcli-altium-interop — Altium Designer in and out through `akcli`

This skill covers the Altium-specific interop surface of `akcli`: what Altium content
parses, how to get designs **out** (JSON / netlists), how to get changes **in** (offline
human instructions — akcli never writes Altium), and how to migrate AD → KiCad with
proof of equivalence. For general read/analyze/draw mechanics (op-list format, `plan`/
`draw`, checks, exit codes, config), **see the akcli-circuit-design skill** — do not
re-derive them here.

## What parses vs. what is refused (and the read-only guarantee)

`akcli` opens Altium OLE2/CFBF containers directly, on any OS, with **strictly
read-only** access — no code path modifies a `.SchDoc`/`.SchLib`/`.PcbDoc`, ever.

Parses:
- **`.SchDoc`** — components, pins (electrical-tip coordinates), designators,
  parameters, footprints, wires/junctions/net labels/power ports/ports/No-ERC markers
  → full inferred netlist. Two Altium-specific resolutions worth knowing when you read
  the output: a `Comment="=<ParamName>"` is an **indirection** to that component's own
  parameter, not a literal, and one it cannot resolve is reported
  (`warning: altium: N unresolved Comment parameter reference(s) (imported literally)`);
  and only a `ModelType=PCBLIB` (or absent) model becomes a `footprint`, `IsCurrent=T`
  winning — a SIM/SI/3D model name never lands there. Document-level parameters
  (Title/Revision/DocumentNumber/Date) surface as `title_block` in `read --json`.
  Hierarchical designs are followed: sheet symbols
  (RECORD 15/16) recurse into child `.SchDoc`s with per-instance namespaces and
  sheet-entry↔child-port pairing (Altium *Automatic* scope: ports merge globally
  only in designs without sheet symbols). `.PrjPcb` is accepted too — akcli reads
  the project's top sheet and honors `PowerPortNamesTakePriority`. Sheet-entry
  edge-position scale follows the documented convention; validating against a
  real AD hierarchical design is still pending — flag it when it matters.
  **Anything the reader does not model is counted, never dropped silently**: a read
  emits `warning: altium: skipped N unsupported record(s): 26 (Bus) ×3, ...` on stderr
  (and in `read --json`'s `warnings` array). Buses (RECORD 26) and bus entries (37) are
  NOT read — if that warning names them, the netlist is missing bus connectivity and you
  must say so instead of reporting a clean import. A `.PrjPcb` that lists more than one
  top-level sheet also warns, naming the sheets that were ignored (only one is read).
- **`.SchLib`** — text-record symbol libraries (symbol names + pin counts).
- **`.PcbDoc`** — ASCII sections `Nets6`, `Components6`, `Classes6`, `Rules6`
  → nets, footprints, classes, rules; **plus binary copper**: `Tracks6`, `Vias6`,
  `Arcs6`, `Pads6` decode into `tracks`/`vias`/`arcs`/`pads` (coordinates in mils,
  Altium's native +Y-up frame, net indices resolved to names). Layouts were
  cross-validated item-by-item against KiCad's own Altium importer on real boards.
  `Fills6`/`Regions6`/`Texts6`/`Polygons6` are still skipped.
- **`.PcbLib`** — decodes each footprint's pads (number, position, size, drill, shape,
  rotation, NPTH vs plated) into the `FootprintDef` model. Undecoded primitives (silk,
  text, 3D bodies) surface as `UNSUPPORTED_PRIMITIVE` warnings rather than failing the
  read. Read-only, same as every other Altium input.

Refused loudly with `ERROR: ALTIUM_UNSUPPORTED` and **exit 5** (unsupported, not
corrupt): binary `.SchLib` symbol records, and an unknown record type inside a
binary `.PcbDoc` copper section (truncated records exit 3, `ALTIUM_MALFORMED`).
Corrupt containers exit **3** (`ALTIUM_BAD_MAGIC`, `ALTIUM_FAT_CYCLE`, ...). Also note:
`net`/`component`/`check`/`diff`/`pinmap`/`export` accept schematics only — feeding
them a `.SchLib` or `.PcbDoc` exits 5 with a note to use `read` instead. An unknown
OLE2 container is now classified by its storage layout and fails loudly (exit 5)
instead of silently being read as an empty schematic. Separately, `akcli read --strict`
turns a non-empty source that normalizes to zero objects (`EMPTY_IMPORT`) into an
exit-1 failure rather than a quiet empty result.

## Getting designs OUT of Altium

```bash
akcli read main.SchDoc --json > model.json        # full normalized model (schema_version "2.0")
akcli net main.SchDoc --json > netlist.json       # structured netlist (stable_id per net)
akcli export main.SchDoc --format protel -o board.net   # Altium/Protel .NET for other EDA tools
akcli export main.SchDoc --format kicad -o board.net.kicad   # KiCad legacy eeschema netlist
akcli export main.SchDoc --format csv -o nets.csv            # flat net,ref,pin rows
```

`export` defaults to `--format protel` and writes stdout unless `-o` is given.
`akcli export --json` wraps the rendered netlist text in a `{schema_version, source,
format, content}` envelope (the netlist body itself is unchanged) — for a fully
structured netlist model use `akcli net --json` instead. All exports are
deterministically sorted; unnamed nets are named by membership-derived `stable_id`,
so re-exports are diffable.

Once you have read an Altium design, continue development in KiCad with `akcli
project new <dir>` (fresh project) or `akcli project init <dir>` (a
`.kicad_sch` from an earlier conversion is already there) — Altium stays
import-only, so this is where the design actually moves forward.

## Getting changes INTO Altium

`akcli` has **no Altium write path at all** — on any OS, offline or live. (The
Windows live-bridge scaffold that once existed was deleted in 0.17.) The offline
route below is the only route.

### Offline route: human draw instructions + importable netlist

1. Author the edit as a normal op-list (see the akcli-circuit-design skill for the format),
   then translate each op into unambiguous human instructions. Good instructions state,
   per op: the **exact library symbol** and designator (`Place Device:R as R10, value
   10k`), the **location in mils** on the 50-mil grid, **pin-level wiring** by
   `REF.PIN` (`wire R10.2 to U3.14`), and every power port / net label by **net name**.
   Never say "connect the resistor to the MCU" — name pins and nets.
2. Export the **current** (pre-edit) connectivity as a baseline Protel netlist the
   user can cross-probe against while editing — `export` has no `--ops` input, so it
   always emits the file as it is now, never the post-edit connectivity:
   ```bash
   akcli export main.SchDoc --format protel -o baseline.net
   ```
   If a netlist of the intended *new* connectivity is needed, first draw the op-list
   into a scratch KiCad schematic and export that file instead
   (`akcli draw scratch.kicad_sch --ops ops.json --apply`, then
   `akcli export scratch.kicad_sch --format protel -o intended.net`).
3. After the user edits in Altium, verify — never trust the human either:
   ```bash
   akcli diff main.SchDoc main_edited.SchDoc --fail-on never
   ```

## AD → KiCad migration workflow

`akcli` is **not** an Altium-to-KiCad converter — it carries connectivity truth, not
artwork. Migrate by re-drawing in KiCad and proving net equivalence:

1. **Read the source of truth.** `akcli read main.SchDoc --json` and
   `akcli net main.SchDoc --json` give the component list, values, footprints, and
   nets to reproduce.
2. **Map the library.** For each Altium component pick a KiCad `lib_id`: use symbols
   from a project `.kicad_sym` or the official KiCad libraries (passed to `plan`/`draw`
   via repeatable `--symbols`, or config `[paths]`), or convert real LCSC parts with
   `akcli jlc add <C-number>`. Carry the Altium `value` and
   resolved `footprint` fields from the `read --json` output into `place_component` ops.

   Going the OTHER way (a library the user needs **inside Altium**): `akcli jlc add`
   emits KiCad-6-dialect libraries that Altium Designer imports natively —
   **File » Import Wizard » KiCad Design Files** converts the `.kicad_sym`/`.kicad_mod`
   to a `.SchLib`/`.PcbLib`. That wizard is the supported route for any KiCad→AD
   library need; akcli itself never writes Altium files.

   If the project has its **own** Altium `.PcbLib` footprint (not an LCSC-sourced part,
   so `jlc add` doesn't apply), convert it directly:
   ```bash
   akcli library import-altium part.PcbLib --out vendor.pretty --courtyard 0.25 --apply
   ```
   Pads convert verbatim and are cross-validated against KiCad's own Altium importer;
   the run writes a `provenance.json` alongside the output (source file SHA-256,
   converter version, and every declared transformation — e.g. a synthesized courtyard).
   Dry-run by default; `--apply` is required to write the files.
3. **Draw into KiCad.** Author the op-list, then (see the akcli-circuit-design skill):
   ```bash
   akcli plan board.kicad_sch --ops ops.json
   akcli draw board.kicad_sch --ops ops.json --apply
   ```
4. **Prove equivalence** — the step that makes this a migration, not a guess:
   ```bash
   akcli diff main.SchDoc board.kicad_sch --fail-on never
   ```
   Nets match by pin **membership** (Jaccard), not display name, so `N$1234`-style
   auto-name churn does not break it. A cross-format diff has no shared UniqueIDs, so
   it is always reported `low_confidence` — read the per-net membership changes, not
   just the summary line.

What will **not** carry over (plan around it, state it in the report):
- Symbol artwork, sheet graphics, text/annotation placement — connectivity only.
- Hierarchy: a multi-sheet Altium design is rebuilt with ONE multi-sheet op-list —
  the envelope's `sheets` map + per-op `"sheet"` tags route ops onto the (pre-created)
  child files in one atomic transaction (`add_sheet` places the parent's reference;
  naming a sub-sheet *path* from the parent still fails `HIERARCHICAL_UNSUPPORTED`).
  The KiCad READER follows `(sheet ...)` children (per-instance namespaces,
  sheet-pin<->hierarchical-label connectivity), and the net gate evaluates the whole
  rebuilt tree from its root.
- Binary `.SchLib` symbol graphics; `.PcbDoc` fills/regions/texts/polygons (pads/tracks/
  vias/arcs DO read now, but nothing converts them to `.kicad_pcb` — read-side only).
- Altium pin electrical types map only ints 0–7 (no `POWER_OUT`/`NO_CONNECT`), so
  ERC fidelity differs slightly between the two sides.

## Verification: never trust a conversion

Any time a design crosses a tool boundary — Altium → KiCad, or human edits made from
your instructions — diff netlists between source and result before
declaring success:

```bash
akcli diff source.SchDoc result.kicad_sch --fail-on never    # membership-level diff
akcli export source.SchDoc --format csv -o a.csv         # or compare flat CSVs
akcli export result.kicad_sch --format csv -o b.csv
```

`diff` exits 1 when membership changed (`--fail-on never` for report mode). Corroborate
with `akcli check result.kicad_sch --fail-on never` and read its metadata caveats
(passive-pin ratio, No-ERC suppressed count, unnamed-net count) before calling the
migration clean — a findings-free run on a mostly-untyped board proves little.
