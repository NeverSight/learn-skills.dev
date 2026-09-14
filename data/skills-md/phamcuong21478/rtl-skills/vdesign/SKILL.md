---
name: vdesign
description: Generate a design proposal, documentation, and RTL backbone from a requirement file
allowed-tools: Read, Write, Grep
---

# Verilog Designer

## Overview

This guide defines the workflow for generating a design proposal, documentation, and a skeleton RTL module from a Markdown requirement file.

The input is a `.md` requirement file that describes what the module should do, typically `./ddoc/<module>_req.md` produced by `varch`. The output is:

1. A proposal file with function description, architecture and algorithm if applicable
2. A design documentation file
3. A backbone Verilog file with `//@` direction comments, ready for implementation by `vfill`

`vdesign` runs once per **new submodule**. Reused `lib` modules have no `_req.md` (they are already designed and documented), so there is nothing here to drive — `vdesign` simply skips them; `varch` still instantiates them in the skeleton.

### Module Name Derivation

All output file names are derived from the **module name**, not the raw requirement file name. The module name is the requirement file base name with any trailing `_req` removed.

Example:

- requirement `./ddoc/foo_ctrl_req.md` → module name `foo_ctrl`

Use this module name consistently for the proposal, documentation, and RTL backbone file names below.

### Preconditions

Two stop conditions, checked before anything is written:

- **Requirement file missing.** `./ddoc/<module>_req.md` does not exist → stop and
  report: run `varch` first (or place a hand-written requirement file). Never
  design from a module name alone.
- **Target is the IP top.** The module name resolves to `<ip>_top` → refuse. The
  top-level integration skeleton is owned by `varch` (it has no `_req.md`, and its
  `//@` are integration notes, not fill directions); `vdesign` generates submodule
  backbones only.

### Before You Start — Re-run Safety

`vdesign` overwrites three artifacts. Two of them carry hand-owned downstream content once the flow has progressed past `vfill`:

- `rtl/<module>.v` — after `vfill`, this holds the real implementation and **every `//@` marker has been converted away**. A blind re-generate destroys the implementation.
- `ddoc/<module>_proposal.md` — `vfill` records design updates and debug notes in its `## Implementation Notes (vfill)` section (seeded empty in Step 2). A blind re-generate clobbers them.

So before writing anything, classify the current state of the backbone:

| State | How to detect | Action |
|-------|---------------|--------|
| **Fresh** | `rtl/<module>.v` does not exist | Generate all three outputs normally. |
| **Backbone only** | `rtl/<module>.v` exists and still contains `//@` markers, no real logic | Safe to regenerate — the requirement changed and nothing downstream depends on it yet. |
| **Filled** | `rtl/<module>.v` has no `//@` markers (the same marker `vflow` uses to detect completion, CodingStyle §18) / contains implemented logic, or the proposal's `## Implementation Notes (vfill)` section has content | **Stop and confirm with the user before overwriting.** Re-running discards `vfill`'s implementation and notes. The safe path is to re-run `vdesign` *before* `vfill`; after that, requirement changes must be reconciled into the filled RTL by hand. |

This mirrors how `varch` guards `<ip>_top.v` against clobbering integration edits.

## Step 1 - Read Requirements and Generate Proposal

Read the target requirement `.md` file and extract the design intent.

A `varch`-generated `_req.md` has **two parts** separated by the marker line
`<!-- functional-spec: hand-owned below this line -->`:

- **Structural section (above the marker)** — overview, parameters, and the port/interface table. This is the **authoritative interface contract**: `varch` already fixed these port and parameter names, widths, defaults, and directions and wired `<ip>_top.v` to them by name. Carry them through verbatim — **do not rename, re-width, re-default, or re-derive a port or parameter.** Renaming a port or parameter here breaks the skeleton wiring three phases later.
- **Hand-owned functional section (below the marker)** — `## Functional Description`. This is the real design intent the proposal and documentation must stay faithful to.

(If the requirement has no marker line — e.g. it was hand-written — treat the whole file as intent and take ports from whatever port table it provides.)

**If the design genuinely needs a port or parameter the requirement does not
list, that is an architecture change, not a local fix.** Do not invent it here —
adding a port that `<ip>_top.v` does not wire breaks integration. Stop and flag
the gap to the user so it can be resolved in `varch` (which updates the
architecture document, the `_req.md`, and the skeleton together), then re-run
`vdesign` against the corrected requirement.

Based on the requirements, generate a design proposal. The proposal must include:

- Functional description of the module, consistent with the requirement's functional section
- Port list with signal names, directions, and widths — **taken verbatim from the requirement's structural port table**
- Parameter list with names, defaults, and **legal ranges** — names and defaults **taken verbatim from the requirement's structural parameter table** (including `RS_LV` for a clocked module); the legal range is a design decision made here (it feeds the doc's Parameters table, `ModuleDocContract §2`, and ultimately the release datasheet)
- Algorithm description, if applicable
- **Micro-architecture design** — the heart of the proposal; which artifacts are mandatory depends on what the module contains (see "Micro-architecture design" below)
- **Intended timing — mandatory for every clocked module**: latency from input to output, pipeline depth, and throughput. If there is no fixed latency, state that explicitly (e.g. "handshake-bound, no fixed latency") rather than omitting the section — `vassert`'s Latency/Throughput properties and the doc's mandatory Timing Characteristics section (`ModuleDocContract §6`) are both derived from this. A purely combinational module states "combinational".

### Pattern scan (do this before finalizing the architecture)

Run an explicit two-part scan against `.claude/skills/shared/DesignPatterns.md` —
recognition is the weak link, so make it a deliberate pass, not incidental
noticing:

1. **Feature scan.** For each pattern, read its **Recognize when** line against the
   requirement's functional section. These are phrased in requirement/symptom
   language (back-pressure, arbitration, occupancy, configuration registers, …) so
   the match is keyword-level. A requirement may hit several.
2. **Reflex scan.** Walk the **Reflex triggers** table against the architecture you
   are *about to choose*. These patterns (P4, P8, P9, P10, P6, P7, P12) fire from a
   structural commitment you make — a RAM, a pipeline, a bus, an array port — not
   from anything the requirement says, so they are the ones silently missed. The
   moment you decide to put state in a RAM, the preclear (P4) and read-during-write
   (P8) checks become mandatory.

For every hit, shape the architecture after the matching pattern and **name the
pattern in the proposal's architecture section** (e.g. "the per-id count RAM needs
P4 preclear + P8 forwarding"; "buffer the output with `vb_stream_fifo`, P1"). This
keeps related modules consistent and tells `vfill` which idiom to implement. Be
precise — match a pattern only when its discriminator actually holds (don't add a
buffer where always-ready upstream is fine). Do not paste the pattern's code into the
proposal — reference it by name; the actual widths and reset scope are derived per
module.

### Using library modules inside the design

A pattern hit (or the architecture itself) often calls for a standard building
block — a stream FIFO, a synchronizer, a dual-port RAM. Before designing one from
scratch, check `./lib` for a module that already provides it (the same
reuse-first rule `varch` applies at the IP level):

- Take its ports and parameters **verbatim from its `<module>.md` documentation**
  (the doc follows `ModuleDocContract` and is usable without reading the RTL; fall
  back to the source only if the doc lacks them). Never invent, rename, or
  re-width a library port; bind only the parameters it actually declares.
- **Record the reuse in the proposal's architecture section** (library path +
  instance role), so `vfill` and the debuggers know the block is library code and
  do not re-derive or re-implement it.
- The instantiation goes **into the backbone as structural code** (Step 3), not
  into a `//@` marker — wiring a known, fixed interface is a design decision made
  here; leaving it to `vfill` forces a re-derivation of the same interface.

### Micro-architecture design (the heart of the proposal)

The proposal is a *design*, not a restatement of the requirement: every decision
`vfill` would otherwise have to make while implementing is made **here**, where it
can be reviewed. Which artifacts are mandatory depends on what the module
contains — detect, then design:

| The module has… | Then the proposal must carry |
|---|---|
| more than one internal block or stage | **Datapath & control diagram** (mermaid): the internal blocks, the signals between them named per `CodingStyle §3` (`s0_`/`s1_` stage prefixes, `_ff` registers), and which part is control vs datapath |
| control sequencing (modes, multi-step transactions, protocol handling) | **FSM design**: the state list with a one-line meaning each; the encoding choice (`localparam` binary / one-hot — and why); the reset state; a transition table or mermaid `stateDiagram-v2` covering every documented stimulus, including the error/abort paths; Moore vs Mealy per output; recovery from an illegal state (the mandatory `default:`) |
| latency > 1 cycle | **Pipeline table** — one row per stage: stage name (`s0`/`s1`/…), the registers it owns (named), the computation it performs, its valid qualifier, and its behavior on stall/bubble. The rows must sum to the `## Timing` latency. State the back-pressure strategy (full-pipe stall vs skid/elastic buffer) and the pattern it follows |
| internal state | **Storage inventory**: every register, counter, and RAM with its width, reset value (or "no reset, qualified by valid" per `CodingStyle §5`/`§14`), and the reflex-pattern rulings that apply (P4 preclear, P8 read-during-write, …) |
| a non-obvious choice (algorithm variant, encoding, RAM vs FF array, single- vs multi-cycle) | **Decision note**: one or two sentences — the choice, the alternative rejected, and why |

All diagrams (architecture, FSM state, algorithm flow) are written in mermaid format.

A module with none of the above — pure combinational glue, a trivial register
slice — may compress the architecture section to a paragraph. **Omission is
allowed only when there is genuinely nothing to decide, never because the design
is merely unwritten.**

**The backbone mirrors the micro-architecture (Step 3).** Each diagram block /
pipeline stage becomes a section banner; the `//@` markers name the proposal's
states and stages (e.g. `//@ implement the IDLE→LOAD→RUN→DRAIN FSM from the
proposal, one-hot, default: recover to IDLE`), so `vfill` implements the
*designed* FSM and pipeline rather than inventing its own.

## Step 2 - Generate Proposal and Documentation Files

Generate the following files:

### Proposal File

Create a new Markdown file in the `./ddoc` folder, alongside the requirement file.

Output file rules:

- Use the module name as the base name
- Append `_proposal` before the extension
- Use the `.md` extension

Example:

- requirement `foo_req.md` → `./ddoc/foo_proposal.md`

#### Proposal sections

The proposal carries these sections in order (omitting only the ones Step 1 marks
optional): `## Function Description`, `## Ports`, `## Parameters` (with legal
ranges), `## Architecture` (the micro-architecture artifacts from Step 1 —
datapath/control diagram, FSM design, pipeline table, storage inventory, decision
notes — naming any matched patterns and reused lib modules), `## Algorithm`,
`## Timing`, and — always last — an empty seed:

```markdown
## Implementation Notes (vfill)

<!-- vfill records design updates and debug notes here, updating in place. -->
```

The seed is the contract that keeps re-runs safe: `vfill` writes its notes
**inside this section only**, updating in place rather than appending duplicates,
so "has vfill touched this proposal?" reduces to one check — whether the section
has content (the Re-run Safety table above relies on it).

### Design Documentation File

Create a new Markdown file in the `./doc` folder.

Output file rules:

- Use the module name as the base name
- Use the `.md` extension

Example:

- requirement `foo_req.md` → `./doc/foo.md`

#### Required Content for the Design Documentation

The design documentation must follow the module documentation contract defined in
`.claude/skills/shared/ModuleDocContract.md`. Populate every required section of
that contract from the proposal and the requirement file.

The functional description must be consistent with the proposal and with the
requirement's hand-owned functional section. Because the RTL is not yet
implemented at this stage, derive the port table, reset values, and timing
characteristics from the proposal's port list and architecture; if a value is
not yet decided, state the intended value from the proposal rather than leaving
it blank. The reset section must reflect the project convention: synchronous
reset, `rst_n` compared against `RS_LV` (default active-low).

For a register-bearing module, the Register Map (`ModuleDocContract §9`) is
**designed here**: addresses, access types (`RO`/`RW`/`W1C`/`RC`), and reset
values come from the requirement's register list plus the architecture's decode
design — they are design decisions, not implementation details, so they must not
be deferred to `vfill`. The Instantiation Template (`§11`) binds every parameter
to the default from the structural parameter table.

## Step 3 - Create Backbone RTL Module

Create a skeleton Verilog file in the `./rtl` folder.

Output file rules:

- Use the module name as the base name
- Use the `.v` extension

Example:

- requirement `foo_req.md` → `./rtl/foo.v`

This skill generates backbones for submodules only. The top-level integration skeleton `./rtl/<ip>_top.v` is owned by `varch`; do not create or overwrite it here.

### Backbone Structure

The backbone must be **style-compliant from the start** — `vfill` fills it in
place, so the scaffold must already match `.claude/skills/shared/CodingStyle.md`,
not just the empty-logic shape. When the proposal names a design pattern (Step 1),
lay the section dividers and `//@` markers out after that pattern's canonical
shape in `.claude/skills/shared/DesignPatterns.md`, keeping the markers
plain-English (no code, `CodingStyle §18`). It must include:

- Plain **Verilog-2005 only** (`CodingStyle §0`) — the backbone *is* the future
  synthesizable RTL; no SystemVerilog constructs.
- `` `default_nettype none `` at the top and `` `default_nettype wire `` at the end (`CodingStyle §14`).
- Module declaration with all ports from the proposal, ANSI style, with `//!` Doxygen doc-comments on every port and parameter (`CodingStyle §1`, `§10`).
- `RS_LV` as the **last parameter** of the (clocked) module, default `0` (`CodingStyle §1`, `§12`).
- `//@` direction comments that guide `vfill` on what to implement in each section.
- Section dividers using the standard banner format, indented to body level (4 spaces) (`CodingStyle §4`).
- Empty logic bodies — no implementation. The one exception is **structural code
  for a reused library module** (Step 1): instantiate it here with named port
  connections (`CodingStyle §9`), its interface taken verbatim from the lib doc;
  any glue logic *around* it stays a `//@` direction for `vfill`.

Port and signal naming follows `CodingStyle §3` (do not re-derive a partial copy
of those rules here): `s_`/`m_` interface prefixes, `_ff` for flip-flops,
`s0_`/`s1_` pipeline-stage prefixes, etc. Port names themselves come straight from
the requirement's structural port table (see Step 1).

Example backbone structure:

```verilog
`default_nettype none

module foo #(
    parameter DATA_W = 8,   //! data bus width
    parameter RS_LV  = 0    //! reset active level (0 = active-low)
) (
    input  wire              clk,      //! clock
    input  wire              rst_n,    //! reset (asserted when == RS_LV)
    input  wire [DATA_W-1:0] s_data,   //! input data
    input  wire              s_valid,  //! input data valid
    output reg  [DATA_W-1:0] m_data,   //! output data
    output reg               m_valid   //! output data valid
);

    //@ implement the input handshake logic here

    //==========================================================================
    // Stage 0 - Input Register
    //==========================================================================

    //@ register s_data and s_valid into s0_data_ff and s0_valid_ff

    //==========================================================================
    // Stage 1 - Output
    //==========================================================================

    //@ compute m_data from s0_data_ff and drive m_valid

endmodule

`default_nettype wire
```

The `//@` comments must be specific enough for `vfill` to implement the correct behavior without further design decisions. They must follow the marker grammar and lifecycle defined in `.claude/skills/shared/CodingStyle.md §18` — in particular, a marker must never contain Verilog code.

## Step 4 - Self-check the outputs

Before finishing, verify the three outputs agree with each other and with the
requirement. The interface is the contract `vfill` and `varch`'s skeleton build
against, so a mismatch here surfaces as a wiring or compile bug downstream. Walk
each port and parameter of the module and confirm:

| Check | Pass condition |
|-------|----------------|
| Ports & params match the requirement | Every port and parameter in the backbone header matches the requirement's structural tables by name, width/default, and direction. None added, dropped, renamed, re-widthed, or re-defaulted (a needed-but-missing one is an architecture change — see Step 1). |
| Proposal agrees | The proposal's port and parameter lists are identical to the backbone header. |
| Doc agrees | The doc's Ports table (`ModuleDocContract §3`) and Parameters table (`§2`) list the same ports and parameters with the same widths, directions, defaults, and legal ranges. |
| Conventions hold | `clk`, `rst_n` are the first two ports; `RS_LV` is the last parameter (default 0) for a clocked module; reset is described as synchronous against `RS_LV`. |
| Timing stated | For a clocked module, the proposal carries an explicit `## Timing` section (latency / pipeline depth / throughput, or an explicit no-fixed-latency statement) and the doc's Timing Characteristics (`§6`) matches it. |
| Micro-architecture complete | Every artifact the Step 1 content table mandates for this module is present: the FSM transition table covers every documented stimulus and has a reset + `default:` recovery state; the pipeline rows sum to the `## Timing` latency; the storage inventory covers every register the `//@` markers name. |
| Backbone mirrors the design | The backbone's section banners correspond to the proposal's blocks/stages, and FSM/pipeline `//@` markers name the proposal's states and stages — no marker asks `vfill` to make a design decision the proposal already made (or should have made). |
| Lib interfaces verbatim | Every library-module instantiation in the backbone matches the lib module's doc by port name, width, and declared parameters; the reuse is recorded in the proposal's architecture section. |
| Markers legal | Every `//@` in the backbone is plain-English intent with no Verilog code, one direction per line (`CodingStyle §18`). |
| vfill seed present | The proposal ends with the empty `## Implementation Notes (vfill)` section. |
| Functional fidelity | The doc and proposal functional descriptions are consistent with the requirement's hand-owned `## Functional Description`. |

If any check fails, fix the offending artifact and re-run the check — do not leave
the proposal, the documentation, and the backbone in disagreement.

## Known Issues and Fixes

This section records issues encountered when running this skill and how they were resolved. Use it to avoid repeating the same mistakes — missed pattern matches and interface drift belong here.

<!-- Add entries below as issues are discovered. Format:
### <short issue title>
**Symptom:** what was observed
**Cause:** root cause
**Fix:** what was done to resolve it
-->
