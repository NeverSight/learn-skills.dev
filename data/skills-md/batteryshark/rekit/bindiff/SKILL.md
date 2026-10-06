---
name: bindiff
description: "Match functions across two builds of a binary with Google BinDiff: per-function similarity and confidence, renamed or moved functions, and functions added or removed. Use for patch diffing (what did this update actually change?), porting symbols from a named build onto a stripped one, malware variant comparison, and finding a known function again after a recompile moved every address. Complements intellidiff, which compares bytes and text rather than structure. Static — disassembles and matches, never executes either binary."
---

# BinDiff (binary structural diff)

Match **functions** across two builds of a binary. BinDiff compares call graphs and
control-flow graphs, so it survives recompiles that move every address, reorder
functions, and strip every symbol.

## When to use

- **Patch diffing** — a vendor shipped an update; which functions actually changed?
  The changed list, sorted by ascending similarity, is your bug-hunt worklist.
- **Symbol porting** — you have a named/debug build and a stripped one. Matched pairs
  where only one side has a real name (`portableNames`) tell you exactly which symbol
  goes where.
- **Variant comparison** — two samples from the same family: shared code shows up as
  high-similarity matches, the new payload as unmatched functions.
- **Finding a function again** — the routine you reversed last month has moved in the
  new build. Match old→new and read the pair off the table.

Reach for `intellidiff` instead when the question is byte or text identity (same file?
which lines changed?). BinDiff answers the structural question that byte diffing cannot.

## What it does

1. Turns each input into a `.BinExport` (BinDiff's disassembly interchange format) using
   IDA Pro or Ghidra, unless you pass `.BinExport` files directly.
2. Runs `bindiff` to match functions and basic blocks.
3. Parses the resulting `.BinDiff` SQLite database, and reads both `.BinExport` call
   graphs to recover the functions that matched *nothing* — BinDiff's database records
   matched pairs only, so added/removed code has to come from the exports.

Static throughout: disassemble, match, report. Neither binary is executed. Disassembler
databases go to a temp dir that is deleted afterward, so the sample's own directory is
left untouched.

## Prerequisites

- **`bindiff`** — BinDiff 8 (<https://github.com/google/bindiff/releases>) on PATH.
- **A disassembler backend**, unless both inputs are already `.BinExport`:
  - **IDA Pro** with the BinExport plugin — the runner drives `idat` headless with
    `-OBinExportAutoAction:BinExportBinary`.
  - **Ghidra** with the BinExport extension (`BinExport_Ghidra-Java.zip`) — the runner
    drives `analyzeHeadless` with the bundled Jython script `scripts/ghidra_binexport.py`.

  Plugins: <https://github.com/google/binexport/releases>. Set `IDA_HOME` or
  `GHIDRA_HOME` if the tools are not on PATH. Ghidra exports subtract the image base and
  remap mnemonics IDA-style, so exports from either backend diff against each other.

Until these are installed, `doctor` marks the skill not-ready and `run` reports the gap
with an install hint instead of failing obscurely.

## Usage

```bash
rekit run bindiff ./app-1.0.exe ./app-1.1.exe ./out
rekit run bindiff ./old.BinExport ./new.BinExport ./out --backend none --format json
rekit run bindiff ./stripped.bin ./with-symbols.bin ./out --backend ghidra --top 60
```

`primary` is the **old/reference** build, `secondary` the **new/candidate** one. Keep
that direction consistent: "added" means present only in `secondary`, "removed" means
present only in `primary`.

## Outputs

| File | Contents |
|---|---|
| `summary.json` | the same object printed to stdout under `--format json` |
| `matches.json` | every matched pair, plus `renamed` and `portableNames` subsets |
| `unmatched.json` | `added` (secondary-only) and `removed` (primary-only) functions |
| `*.BinDiff` | BinDiff's own result database — open it in the BinDiff UI or the IDA/Ghidra plugin |
| `binexport/*.BinExport` | exports the runner produced; reuse them to re-diff without re-disassembling |

## Interpret results

- **similarity** (0–1) is how alike two matched functions are; **confidence** (0–1) is how
  much to trust the *match itself*. A low-similarity, high-confidence pair is a genuinely
  changed function — that is the interesting case. Low confidence means the pairing may
  simply be wrong; verify it before drawing conclusions.
- **algorithm** names the matcher that produced the pair (name hash, MD index, call graph
  edges, …). Name-based matches are only as trustworthy as the symbols.
- Overall `similarity`/`confidence` in the summary describe the two files as a whole.
  Recompiles with a different compiler version routinely drop overall similarity while
  leaving the actual logic unchanged — read the per-function list, not the headline.
- `--identical-threshold` decides what counts as unchanged (default `1.0`, exact match).
  Raise the bar for noisy builds by lowering it, e.g. `0.98`.
- Added/removed lists cover functions with real bodies (normal, library, thunk); imports
  and invalid vertices are excluded as noise. If a `.BinExport` cannot be read, the
  summary sets those counts to `null` and says so rather than reporting zero.
