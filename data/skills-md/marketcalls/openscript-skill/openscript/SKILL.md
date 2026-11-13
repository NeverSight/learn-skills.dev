---
name: openscript
description: Write an OpenScript study or strategy for OpenAlgo, and install it into strategies/openscript/ only after it compiles. Use when asked to create, port or debug an OpenScript indicator, study, strategy, backtest script or .oscript file, including converting a TradingView Pine Script, or an indicator or strategy from any other platform or language (another chart or terminal scripting language, a C-like or C# indicator, an array formula language, Python or pandas code, a spreadsheet, or a formula from a book) or a JavaScript chart indicator (an openalgo-charts descriptor) into a script that computes the same values, checked bar by bar against the original's own numbers. This is the OpenScript path, not the JavaScript chart-indicator path and not the Python openalgo.ta path.
argument-hint: "[what the study or strategy should do]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# OpenScript studies and strategies

Write an OpenScript study or strategy, from a description or converted from a
Pine Script or any other platform, compile it, and hand back the code. Inside
an OpenAlgo folder it can also be installed into `strategies/openscript/`,
where it becomes a study or a strategy a trader can open in the editor,
backtest on `/trading`, and deploy on an instrument.

## What to hand back

People use this skill for three things: writing an indicator, writing a
strategy, and converting one from Pine Script or another platform. What they
want is **the code**, so every answer ends with:

1. **The complete `.oscript` file**, in the reply and saved to a file: never a
   fragment, never a draft that has not compiled. Run it through
   `validate.mjs` first, and show it only once it reports PASSED.
2. **What the compile did not prove.** A compile runs no bars. For a
   conversion, say whether it was compared with the original's numbers
   (`compare.mjs`), and if not, that it was not.
3. **Every warning and every difference from the original**, in plain words.
4. **How to use it**: paste it into the OpenScript editor on `/trading`, or,
   when the skill sits inside an OpenAlgo folder and the person asked,
   install it with `validate.mjs --install`. Outside an OpenAlgo folder
   `--install` refuses, because there is nowhere to install it.

**Which path is this.** Three unrelated things in this repository are called
indicators, and they share nothing but the word:

- **OpenScript** (this skill) is a language, compiled to a program. Files are
  `.oscript`, and they can both draw and place orders.
- **`chart-indicator`** is a plain JavaScript descriptor on `openalgo-charts`,
  drawing only, loaded by the browser at runtime.
- **`openalgo.ta`** is a Python library used from the Python strategy host,
  scanners and backtests.

If the request names a `.oscript` file, the OpenScript editor, or a strategy to
deploy on `/trading`, it is this one. If it is "add an indicator to my chart"
with no more said, it is probably `chart-indicator`.

## The one rule

**Never write into `strategies/openscript/` by hand.** That folder holds two
files per script, `<name>.oscript` and `<name>.oscript.program.json`, and **the
runner reads only the program.** It never opens the source.

That makes two silent failures possible, and both matter more than a compile
error:

- **A source with no program is a strategy that cannot run.** It saves, it opens
  in the editor, it appears in the list, and starting it is refused a minute
  later in a log nobody is reading.
- **A program built from different text is worse.** A run executes one script
  while a trader reads another.

So the two files are written together, from one compile, or neither is:

```bash
# 1. draft to a scratch file (never the openscript folder)
#    e.g. <scratchpad>/my_strategy.oscript

# 2. compile it the way the browser will
node .claude/skills/openscript/validate.mjs <scratch>/my_strategy.oscript

# 3. only on PASSED, install both files
node .claude/skills/openscript/validate.mjs <scratch>/my_strategy.oscript --install

#    with a different installed name:
node .claude/skills/openscript/validate.mjs <scratch>/draft.oscript --install --as mean-reversion.oscript
```

`--install` writes both files **only** when there are zero errors, and exits 1
otherwise. Before writing either, it checks that the hash the compiled program
records matches the source it is about to write beside it, which is the same
check the platform's own save route makes. A mismatched pair is refused and
nothing is written, so the failure cannot be half-applied.

## What a pass means

The compiler accepted the text: the names resolve, the types agree, the calls
exist, the limits hold. **Nothing here runs a single bar.** It does not mean the
strategy is any good, that its numbers are right, or that it will make money.

Some refusals wait for a bar, and a pass rules out none of them: a cell written
outside its grid is `OS4008` on the bar that writes it. `OS6025`, a bar handed
over with no time, is the platform's data and not the script: report the
instrument and timeframe rather than changing the script.

`reference/strategies.md` ends with the four steps between a compile and money,
and they are not optional.

## Read these before writing

| Page | What it is for |
|---|---|
| `reference/library.md` | every one of the 350 names, with what it answers and its warmup. Generated from the installed compiler. |
| `reference/pitfalls.md` | what goes wrong, with the diagnostic code you will actually see. Every code on it is proved against the compiler. |
| `reference/strategies.md` | the shapes a strategy takes, and which example answers which ask. |
| `reference/porting-from-any-platform.md` | porting from any other platform or language: which way its history runs, the shapes that recur, the definitions that differ between platforms under the same name (measured), the future, higher timeframes, strategies, notes by source, and checking parity with `compare.mjs`. |
| `reference/porting-from-javascript.md` | porting a JavaScript chart indicator into a study that computes the same values: the chart helpers whose OpenScript twin differs, absent values, `fn` scope, markers, tables, inputs, and how to check parity. |
| `examples/*.oscript` | six worked files, all of which compile. The reasoning is in the comments. |

**Look a name up rather than recalling it.** 350 names is more than anyone holds,
and the dangerous failure is not reaching for a name that does not exist: it is
reaching for a neighbour that computes something else, which compiles and
reports a different strategy than the one that was meant.

## Porting from another platform

Any indicator or strategy can be ported, from any platform or language. Pick
the route by what the original looks like:

| The original | Route |
|---|---|
| a Pine Script that opens with `//@version=5` or `//@version=6` | `import.mjs` (below), then the definitions table in `reference/porting-from-any-platform.md` for each `OS9007` |
| a version 4 Pine Script | convert it to version 5 in its own editor and import; port by hand what does not convert |
| a version 3 or older Pine Script, or one with no version line | its editor converts version 3 to 4 only: convert where it can, port by hand where it cannot |
| a JavaScript `registerIndicator` descriptor | `reference/porting-from-javascript.md` |
| anything else: another chart or terminal language, C-like or C# indicator code, an array formula language, Python, a spreadsheet, a formula from a book | `reference/porting-from-any-platform.md` |

**Get the original's own numbers first.** A port is done when it computes what
the original computed, bar by bar, and the only proof is the original's values:
an export of its chart (bars plus indicator columns), the output of running a
Python original, a spreadsheet saved as CSV, or a book's worked table typed in.
Without them, say plainly that the port compiled and was not compared.

```bash
# the version-annotated chart language: a draft, with a finding per difference
node .claude/skills/openscript/import.mjs <scratch>/original.txt --out <scratch>/ported.oscript

# any source: compile, then compare with the original's printed values
node .claude/skills/openscript/validate.mjs <scratch>/ported.oscript
node .claude/skills/openscript/compare.mjs <scratch>/ported.oscript <scratch>/values.csv --zone Asia/Kolkata
```

The importer brings each statement across with its original meaning, or with a
warning stating the difference, or as a comment with an error, all in the range
`OS9001` to `OS9012`. Its output is a draft, not a port: read every finding.

`compare.mjs` pairs each plot with the column of the same title and reports the
first and largest difference, and when the difference has a recognisable shape
(a seed that converges, a one-bar shift, a population against a sample
deviation, a percentage against a fraction) it says so. Iterate until it
reports SAME on the settings that matter, and tell the trader about any
difference that remains and why.

**The same name rarely means the same numbers.** An "EMA", "RSI", "ATR" or
"standard deviation" on another platform can be seeded differently, smoothed
differently or divided by `n - 1`. Every one of those compiles. The definitions
table in `reference/porting-from-any-platform.md` says what each OpenScript
built-in computes, measured, and gives the helper for each common variant.

## Three things that cost the most time

**Ninety five of the 350 names are planned and not implemented in this version.**
The library describes a name whether or not a version implements it, so a name
resolving is not a promise that it compiles. Reaching for one is `OS2020`. They
are marked in `reference/library.md`. `order.qtyForRisk` is the one most likely
to be reached for by accident, because it reads exactly like the call you want;
whole families are planned, including all of `leg.*` and all of `book.*`.

**`buy` and `sell` move a position by an amount; they do not set it to a side.**
`sell(qty = lots)` while long one lot leaves the position flat, not short.
Nothing refuses it. It is the first entry in `reference/pitfalls.md` and the
reason `examples/stop-and-reverse.oscript` exists.

**A value that is absent is not zero.** Every stateful call has a warmup, and
arithmetic on an absent value is absent rather than zero, which is what keeps a
signal from firing before its average exists. A script that substitutes a number
during warmup, with `orElse` or otherwise, is quietly wrong for its first stretch
of bars and looks like it works.

## Keeping the skill honest

The generator and three checks, all four of which the CI job runs:

```bash
node .claude/skills/openscript/generate-reference.mjs   # rewrites reference/library.md
node .claude/skills/openscript/coverage.mjs             # must print COVERAGE COMPLETE
node .claude/skills/openscript/check-pitfalls.mjs       # must print PITFALLS VERIFIED
node .claude/skills/openscript/check-porting.mjs        # must print PORTING VERIFIED
```

`check-porting.mjs` compiles every code block on both porting pages as the page
says it behaves, and runs every row of the definitions table on test bars
against an implementation written from the stated definition, first bar
included. A porting page whose claim has drifted fails the build.

`coverage.mjs` holds the reference to the compiler in both directions (a name
the compiler has and the page lacks fails, and so does a name the page teaches
that the compiler does not have), checks that every planned name is marked, and
checks that each shape an author asks for is demonstrated in an example **that
compiles**, with the kind read from the compiled program rather than from the
text.

`check-pitfalls.mjs` compiles both halves of every entry in `reference/pitfalls.md`:
the wrong spelling must still produce the code named, and the fix offered must
still come out clean. It also checks that the page and the script name the same
set of codes, so neither can drift alone. Two claims on the first draft of that
page were wrong, and this is what found them.

This skill describes `openalgo-script` 0.8.1, the compiler `/trading` pins, with
the server engine `openscript` at the same version. OpenScript 0.9.0, with
fixes to the backtest engine, is coming; when the pin moves to it, read its
changelog for anything a backtest now reports differently and say so here.

**Bumping `openalgo-script` means updating this skill in the same change**, the
way a chart bump does. Run the generator, run both checks, then update the prose
by hand: the generator owns the name table and nothing generates the teaching.
