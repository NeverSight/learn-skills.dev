---
name: codometer-configure
description: Write or edit a codometer.config.ts, declaring inputs, limits, custom convention counters, comment budgets, exclusions, or output destinations. Use when a repository has no codometer configuration yet, when adding a size or count limit, when bounding how long a comment block or a JSDoc comment may run, when declaring an input for compiled or generated output, when counting a naming convention no built-in analyzer knows about, when a limit fails to bind or an input matches no files, or when deciding whether one configuration can describe every project in a workspace.
license: MIT
---

# Writing a codometer configuration

`codometer.config.{ts,mts,cts,js,mjs,cjs,json,jsonc}` is read from the directory
being measured, or from any directory above it — the search walks upward and
takes the **first** file found. The nearest configuration wins outright, and is
never merged with one further up: a merged limit that never applied to this
folder would look exactly like one that did. `format` is the one field every
configuration must set — there is no code-level fallback for it — and every
other field is optional.

```ts
import { type CodometerConfiguration } from "@codometer/configuration";

const codometerConfiguration: CodometerConfiguration = {
  format: "markdown",
  exclude: ["notepads/**"],
  excludeFrom: ["configuration/.codometerignore"],
  defaultInput: "codebase",
  limits: [{ metric: "typescript.interfaces", severity: "warn", value: 500 }],
  inputs: [
    {
      analyses: ["size"],
      include: ["dist/**/*.js", "!dist/**/*.map.js"],
      name: "compiled",
    },
  ],
  outputs: [{ path: "README.md", type: "markdown" }],
};

export default codometerConfiguration;
```

Output paths resolve relative to the process's own working directory, not to
the configuration file, so a configuration kept in a `configuration/` folder
still writes to wherever the run was invoked from. A configuration file is
always read as a plain object — there is no config-as-function escape hatch,
so one file cannot describe every project in a workspace on its own; a
repository with many projects gives each its own `codometer.config.ts` and
spreads a shared object across them, the way this repository's own
`configuration/codometer.config.ts` does.

## Exclusions

`.gitignore` is already in force through discovery, so `exclude` and
`excludeFrom` are for files that are **kept** but that nobody wrote by hand —
lockfiles, vendored bundles, generated documentation:

| Option | Syntax | Use it for |
| ------ | ------ | ---------- |
| `exclude` | Globs | A handful of paths named inline |
| `excludeFrom` | Paths to gitignore-syntax files | A list a repository would rather keep in a file |

Reusing an existing ignore file is a trap worth knowing about: most are written
for one other tool's concerns. A `.prettierignore` that excludes all markdown
because a formatter doesn't touch it will erase every markdown metric if
codometer is pointed at the same file. A dedicated `.codometerignore` is
usually the right answer instead of reaching for a file another tool owns.

## Inputs

An **input** is a named set of files matched by glob, with the analyses run
over it. The measured directory is always an input of its own, named
`codebase`; `inputs` declares the others — most often build output that every
`.gitignore` excludes, and that therefore needs an input rather than an
exclusion to reach at all.

| Field | Required | Default | Meaning |
| ----- | -------- | ------- | ------- |
| `name` | yes | — | Unique name for this input |
| `include` | yes | — | Globs that add files; at least one must add rather than only remove |
| `exclude` | no | none | Globs that remove files |
| `analyses` | yes | — | `"language"`, `"size"`, or both |
| `compression` | no | `gzip` | `gzip`, `brotli`, or `none`, for `size` analysis |
| `directory` | no | `.` | Where this input's globs start, relative to the process's working directory |

A `!` prefix in `include` removes files; every negation across the array forms
one set applied to the whole input, so reordering the array can never change
what it matches. `exclude` may not carry a `!` — it already removes, so there
is nothing left to negate there. Ignore files are **not** consulted for a
declared input, which is exactly what lets one match compiled output at all.

Naming an input `codebase` **replaces** the built-in whole-tree scan rather
than adding beside it, and only its `compression` and `analyses` are read —
its `include`/`exclude` are not consulted, because the whole-tree scan is
discovered by walking ignore files rather than by matching globs. To measure a
subset of the tree, declare an input under some other name instead.

## Limits

A limit bounds how high one measured metric may go. Any metric can carry one —
a compressed size, a line count, a declared counter's count — and a metric
with no limit is measured and reported exactly as before, gated by nothing.

```ts
defaultInput: "codebase",
limits: [
  { metric: "compiled.size", value: "8 KB" },
  { label: "Interfaces", metric: "typescript.interfaces", value: 500 },
  { metric: "linesOfCode", severity: "warn", value: 100_000 },
],
```

| Field | Required | Default | Meaning |
| ----- | -------- | ------- | ------- |
| `metric` | yes | — | Dotted path of the metric this bounds |
| `value` | yes | — | Ceiling, as a number or a string carrying a unit |
| `severity` | no | `fail` | `fail` stops the run on a breach; `warn` only reports it |
| `label` | no | the path | What the report calls this limit |

A metric is addressed as its input's name followed by its path within that
input. Setting `defaultInput` lets an unprefixed path resolve to that input's
metric, but only where no input of a competing name exists — write the input
name in full wherever an input and a metric group could share one, because
**an ambiguous path is refused outright, never guessed at**. The same refusal
applies to a path naming no metric at all, or one from an analysis its input
never ran.

A string value's unit is decimal and its trailing `b` is required: `"8 KB"` is
8000 bytes, `"1 MB"` is 1000000, and `"8 K"` is refused rather than read as
anything. An input that matches no files only fails the run if a limit is
written against it — declaring the limit is what asserts the files should be
there.

**Never raise a limit's `value` to make a breach pass.** A configured limit is
a promise about the codebase's shape, and raising it on the change that broke
that promise erases the evidence the limit existed to keep. If a breach is a
real regression, reduce what is being measured instead — trim the metric down,
split the file, delete the dead code. If the limit itself was simply wrong for
what this metric should hold going forward, that is also a decision worth
making deliberately and explaining, not a number quietly bumped in the same
change that broke it. For everything else a breach could mean, reach for the
`codometer-triage` skill.

## Custom statistics

The top-level `custom` array is what **measures** a counter — declaring it
there is what computes it, regardless of whether, or where, any output
renders it:

```ts
custom: [
  { label: "Service Files", patterns: ["**/*.service.ts"] },
  { label: "Unit Tests", patterns: ["**/*.unit.test.ts"] },
  { color: "16a34a", label: "Migrations", patterns: ["**/migrations/*.sql"] },
],
```

Each entry renders as one badge everywhere it is selected, in configured
order. `color` is a shields.io hexadecimal triplet; an entry that omits it
takes the next color from a built-in palette per group, so a counter's color
stays stable between runs. A counter selects what it counts with exactly one
of three fields — `patterns`, `symbols`, or `comment` — and an entry naming
none of them is rejected rather than reported as a permanent zero.

An `outputs` entry's own `custom` array is a separate, later concern: it
**selects**, by label, which of the top-level counters that destination
renders — it never declares a counter of its own, so a JSON report and a
markdown report may still select entirely different labels:

```ts
outputs: [
  { custom: ["Service Files"], path: "codometer-report.json", type: "json" },
  { custom: ["Unit Tests"], path: "README.md", type: "markdown" },
],
```

A label an output selects that the top-level `custom` never declared is
refused when the configuration loads — selection cannot conjure a counter that
was never measured. A counter `custom` declares but no output selects is still
measured and still gates a limit; it simply renders nowhere.

### Counting declarations

`symbols` counts declarations in TypeScript and JavaScript sources instead of
files:

```ts
custom: [
  { group: "typescript", label: "Static Methods", symbols: { kinds: ["method"], modifiers: ["static"] } },
],
```

`kinds` is one or more of `class`, `enum`, `function`, `getter`, `interface`,
`method`, `property`, `setter`; `modifiers` narrows to declarations carrying
every named modifier from `abstract`, `async`, `export`, `override`, `private`,
`protected`, `public`, `readonly`, `static`. Both are read literally from the
syntax — a class member is a `method`, everything else callable is a
`function` including an arrow, and a class field holding an arrow function is
a `property` carrying none of the field's own modifiers.

`patterns` on a symbol counter narrows **which files are searched** rather than
being what is counted. `group` places the badge after a named group's
built-ins — `conventions` by default, or one of the built-in language groups —
and a name outside that set fails the configuration rather than rendering
nowhere.

### Selecting a comment budget

`comment` selects a comment budget for a counter to measure, rather than
counting files or declarations. There is no `comments`/`documentation`
mechanism of its own any more: a comment budget is an ordinary custom
statistic, and a `limits[]` entry against its `custom.<label>` metric is what
turns the count into a gate — the same consolidation every other counter goes
through.

```ts
custom: [
  { comment: { language: "yaml", maximumWords: 128 }, label: "YAML Comment Budget" },
  { comment: { kind: "class", maximumLines: 24 }, label: "Class Comment Budget" },
],
limits: [{ metric: "custom.YAML Comment Budget", value: 0 }],
```

| Field | Required | Default | Meaning |
| ----- | -------- | ------- | ------- |
| `language` | no | every language with comments | Narrows to one of `css`, `hcl`, `python`, `shell`, `sql`, `toml`, `typescript`, `yaml` |
| `kind` | no | a plain comment block | Narrows to a documented declaration's JSDoc-style comment for this declaration kind |
| `maximumCharacters` | no | — | Characters a block may hold, markers and newlines and all |
| `maximumLines` | no | — | Lines a block may span |
| `maximumWords` | no | — | Words of prose a block may hold, once markers are stripped |
| `severity` | no | `fail` | `fail` stops the run on a breach; `warn` only reports it |

Its count is how many blocks broke the selector's own maxima, and its
`instances` names each breaching block's `file` and 1-indexed `line`, plus how
much it measured. A block that stayed within budget contributes to neither.

**A `comment` selector carries no inheritance.** There is no top-level default
a per-language entry merges over, so "every language at 128 words except shell
at 256" is written as one selector per language, not as a shared budget with
an override — this repository's own `configuration/codometer.config.ts`
derives that enumeration from `CODOMETER_COMMENT_LANGUAGES` and types it so a
language added to the schema is a compile error there until this repository's
list covers it. **A language codometer starts measuring comments in is not
gated until that enumeration is updated to name it** — nothing about adding a
language to the schema gates it automatically.

**The three maxima are separate fields rather than one `maximum` steered by a
`unit`, because they are not alternatives.** A block can sit inside a line
budget and outside a word one. A field left out is not measured, and
**nothing is defaulted to a number** — a budget nobody wrote is one nobody
chose.

**The budget is per block, never file-wide.** A block is the run of comment
lines a reader takes as one thought: a blank line ends one, a comment trailing
a value is never part of the block above it, and a `#!` shebang is never a
comment at all. There is no file-wide counterpart to a `comment` selector — a
file holding forty well-sized comments is not the same problem as one holding
a single essay, but codometer has no way to measure the second kind today.

Prefer a **word** budget over a character one where a linter already holds
lines to a column limit: the character count would only restate what
formatting already enforces, while words budget what the comment actually
says. JSDoc is ungated by default — a `comment` selector with a `kind` reaches
it, but declaring one is a deliberate choice, not something that happens by
naming a language.

### What a breach means, and what it does not

A breach names its file and line. Condense the block, or move the detail into
documentation that has room for it — **never raise the budget to make the run
pass**, for the same reason a limit's `value` is never raised.

Two accuracy caveats worth knowing before trusting a count:

- **Some languages read a real parser, and some a line scanner.** CSS
  (postcss), Python (`tokenize`), YAML (its CST), and TypeScript/JavaScript (the
  compiler's scanner) all know a comment marker inside a string literal from a
  real comment. Shell, TOML, SQL, and HCL use a line scanner and cannot — a `#`
  or `--` inside a string is read as a comment, exactly as those languages'
  existing comment counters already read it. HCL is the one language measured
  with three syntaxes: `#`, `//`, and `/* */`.
- **Python's comments need a reachable interpreter**, the same way every other
  Python metric does. An interpreter codometer cannot run leaves them
  unmeasured rather than miscounted.

For what to do about a breach, reach for the `codometer-triage` skill.

## Output destinations

`outputs` is an array of typed destinations — declare as many as you like, but
**at most one entry per type**; a configuration naming two `json` outputs, or
two `markdown` ones, is rejected at load time naming the duplicated type,
because nothing on the command line could address the second.

```ts
outputs: [
  { indentation: 2, path: "output/codometer.json", type: "json" },
  {
    description: "Measured on every push.",
    path: "README.md",
    type: "markdown",
  },
],
```

A JSON entry needs `path`; `indentation` defaults to `2`. A markdown entry
needs a `path`, a `write` function, or both — a destination naming neither is
rejected when the configuration loads.

### Writing markdown

`write` is the whole of the customizable behavior — it both decides what the
report says and where it lands, replacing what used to be two separate
`render` and `write` callbacks:

```ts
{
  path: "README.md",
  type: "markdown",
  write: ({ anchors, renderBadges, statistics }) =>
    anchors.syncAnchoredBlock({
      content: `Lines of code: ${statistics.linesOfCode}\n\n${renderBadges()}`,
    }),
}
```

| Argument | Meaning |
| -------- | ------- |
| `description` | The configured description, for a writer that wants to place it itself |
| `renderBadges()` | The built-in badge rendering of these same statistics — call it to build the default content, or to add to it |
| `statistics` | The measured statistics |
| `check` | True when nothing may be written and the file is only being inspected |
| `path` | The configured path, resolved against the process's working directory |
| `anchors` | The marker mechanics — `syncAnchoredBlock`, `wrapInAnchors`, `startMarker`/`endMarker` — so choosing a different file does not mean reimplementing the splice |

Leaving `write` unset keeps the built-in rendering and writing. A `write`
function returns `false` to report its destination as stale, which is what
fails a `--check reports` run; anything else counts as up to date.

## Authoring says inputs, the report says targets

`inputs` is what a configuration declares — this redesign renamed `targets` to
`inputs` and `defaultTarget` to `defaultInput` on the authoring side — but the
measured JSON report keeps its old vocabulary: `CodometerReport.targets`, and a
metric is still addressed as `codebase.typescript.interfaces` or
`Compiled JavaScript.size`, the input's name standing in for what the report
calls a target. That split is deliberate rather than drift, kept because
`CodometerReport.targets` predates this redesign and nothing downstream reading
a report needed to change; the `Measured Targets` badge group carries its own
code comment explaining why it keeps that name too. Write `inputs` in a
configuration; read `targets` in a report, a `configuration --limits` listing,
or a badge group heading.
