---
name: coinagerie-configure
description: Use when writing or changing a coinagerie.config.ts, choosing which files are scanned, excluding paths or words, reading another glossary into exclude.words, merging a word family with fold, declaring markdown or JSON glossary destinations, sharing one base configuration across folders, or when a configuration is rejected, a keyword list will not import, or a word is wrongly listed in the glossary.
license: MIT
---

# Writing a coinagerie configuration

A configuration is one default-exported **plain object** in
`coinagerie.config.ts` (or `.mts`, `.cts`, `.js`, `.mjs`, `.cjs`), loaded with
jiti, so TypeScript works and any field can be computed. Every field is
optional, and no file at all is valid: the run then scans the working
directory and prints.

The schema is strict at every level. A misspelled key fails the run, naming
the file, instead of being ignored. Exporting a function is refused.

```ts
import { typescriptKeywords } from "@coinagerie/languages";

import type { CoinagerieConfiguration } from "@coinagerie/configuration";

export default {
  include: ["src/**", "scripts/**"],
  exclude: {
    paths: ["**/*.test.ts", "**/generated/**", "coinagerie.config.ts"],
    words: [...typescriptKeywords, "src", "index"],
  },
  fold: (word) => (word === "configuration" ? "configure" : word),
  outputs: [
    {
      description: "Words this project uses. Regenerate with `coinagerie --write`.",
      path: "README.md",
      type: "markdown",
    },
  ],
} satisfies CoinagerieConfiguration;
```

The type import is optional and erased at load time. `@coinagerie/languages`
must be installed beside the configuration: an unresolvable import fails the
run as "Cannot find module".

## The folder is the root

Every path and glob is relative to the folder the configuration file sits in,
which is also the root the run scans. A path written in a shared base is read
against the folder of the configuration that was loaded, not the base's.

- `include` defaults to every file, dot-files included. Globs match with
  `path.matchesGlob`, where `*` and `**` never match a name starting with a
  dot: a custom `include` has to name `.github/**` and its kin outright.
- `exclude.paths` takes globs. A glob matching a folder prunes the whole
  folder. Globs match from the scanned folder, so `["dist"]` prunes only the
  top-level `dist`; write `**/dist` to prune it at any depth.
- `.gitignore` is honored on top of both, every one from the repository root
  (nearest ancestor holding `.git`) down, negations included.
- A glossary destination is never scanned, but the configuration file is: its
  own keys become words. Exclude it by path, or accept them.

## exclude.words

A list of entries, or a synchronous or asynchronous function returning one. An
entry is a word, a string, or a regular expression. The function is where a
configuration reads any other file, a parent glossary or a JSON file, because
coinagerie never reads another glossary itself:

```ts
import { readFile } from "node:fs/promises";
import path from "node:path";

const parentWords = async (): Promise<string[]> =>
  Object.keys(
    JSON.parse(await readFile(path.join(__dirname, "../glossary.json"), "utf8")),
  );

export default { exclude: { words: parentWords } };
```

- Nothing is excluded by default, not even language keywords. Spread the lists
  `@coinagerie/languages` exports as plain arrays: `typescriptKeywords`,
  `pythonKeywords`, `sqlKeywords`, `shellKeywords`, `cssKeywords`,
  `hclKeywords`, `tomlKeywords`, `jsonKeywords`, `yamlKeywords`.
- Exclusion runs **after folding**, and each entry is lowercased and folded the
  way the code's words are: excluding `service` also covers `services`, and
  excluding `implements` covers the `implement` it folds into.
- A string is one word, matched exactly. It is never split, so `"fooBar"` never
  excludes `foo` or `bar`; list each.
- A regular expression excludes every word it matches, so one pattern covers a
  family such as plan IDs: `/^(task|test|risk)\d{3}$/`, hash fragments
  `/^(?=.*\d)[0-9a-f]{2,}$/`, or lint rule IDs `/^md\d{3}$/`. It is tested
  against two forms of each word, and a match on either leaves the headword out
  as a string would: the lowercase word as the code wrote it (`MD001` is
  `md001`), and the headword after folding and `fold`. Words are lowercase, so
  write the pattern for lowercase text or add the `i` flag. The `g` and `y`
  flags are dropped, since they make a pattern stateful. Only a TypeScript or
  JavaScript configuration can hold one, since JSON cannot.
- Words never hold a separator. In `task-001` the `001` is a number, not a
  term, so only `task` remains and no pattern matches it; `TASK001` is the one
  word `task001`, which `/^(task|test|risk)\d{3}$/` matches.
- An excluded word leaves the glossary, and the next `--write` deletes its
  definition. Exclude a word because it carries no meaning of its own, not
  because its definition is missing.

## fold

`fold(word) => headword` merges words the lemmatizer left apart, or repairs a
headword it got wrong. It runs after plural and inflection folding, so it
receives lemmas, and its result is the final headword.

```ts
fold: (word) =>
  ({ configuration: "configure", set: "setting" })[word] ?? word,
```

It must be synchronous and return a non-empty string without whitespace or
`*`. A throw, an empty or non-string result, or a promise fails the run,
naming the configuration file.

## outputs

An array of destinations. With none, a run only prints, and `--check` and
`--write` refuse to run.

| Destination                                | Holds                                                               |
| ------------------------------------------ | ------------------------------------------------------------------- |
| `{ type: "markdown", path, description? }` | a block between the `coinagerie:start` and `coinagerie:end` anchors |
| `{ type: "json", path }`                   | the whole file, as a flat object sorted by word                     |

- A markdown file is created when absent, and gets the block appended at its
  end when it has no anchors yet, so point it at a README to add a section, or
  at a file of its own.
- A `description` is free prose under the heading. It may not contain a list
  item (`-`, `*`, `+`) or an HTML comment line, because that would parse back as
  glossary bullets. With none configured, prose already above the first bullet
  is kept.
- Two destinations on one file are refused.
- Destinations are judged independently. Definitions never copy between a JSON
  and a markdown glossary, so keep one authoritative destination per scope.

## One base for many folders

Put shared choices in one module and spread it; each folder's file adds only
what differs. The spread is shallow, so overriding `exclude` replaces all of
it:

```ts
import base from "../coinagerie.base";

export default {
  ...base,
  exclude: { ...base.exclude, paths: [...(base.exclude?.paths ?? []), "fixtures"] },
  outputs: [{ path: "README.md", type: "markdown" }],
};
```

When a folder's `exclude.words` reads its parent's glossary, the parent
decides what the child need not define. A word that leaves the parent returns
as missing in every child that excluded it, and moving its definition down is
a deliberate edit. Under Nx, declare the parent glossary as an input of each
child's target, or an edit to it will not re-run their checks.

## Try before editing

Every field except `exclude.words` and `fold` has a command-line flag that
replaces it for one run: `--include`, `--exclude-paths`, `--output-json`,
`--output-markdown`, `--description`. The `coinagerie-collect` skill has the
table. A bare `coinagerie` run prints the result of a change without writing
anything.

## When a run rejects the configuration

| Symptom                                     | Cause and fix                                                        |
| ------------------------------------------- | -------------------------------------------------------------------- |
| `expected object, received function`        | the file exports a function; export a plain object                   |
| `Unrecognized key: "<name>"`                | a misspelled or misplaced field; fix the key                         |
| `Invalid input` at `exclude.words`          | an entry is neither a word nor a pattern, or it is not a list        |
| `fold must return a non-empty string...`    | the function returned `""`, a space, `*`, a promise, or a non-string |
| `exclude.words boom`                        | the function threw; the error carries the configuration's path       |
| `Cannot find module`                        | install the package beside the configuration                         |
| `Two outputs name a.json`                   | give each destination its own file                                   |
| `A description may not hold a list item...` | the description has a `-`, `*`, `+`, or `<!--` line; reword it       |
| `fold threw on "<word>"`                    | the fold function raised; fix it for that word                       |
| `Configuration file not found`              | a named `--config` is relative to the working directory              |

For what to do about a failed check rather than a rejected configuration, use
the `coinagerie-triage` skill.
