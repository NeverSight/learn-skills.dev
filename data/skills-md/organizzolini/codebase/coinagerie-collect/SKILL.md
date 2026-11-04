---
name: coinagerie-collect
description: Use when running coinagerie or npx @coinagerie/cli, printing the vocabulary of a codebase, checking or writing a glossary, choosing between --check, --write, and a bare run, reading the glossary block or JSON it printed, reading the missing and stale words a failed check named, finding which words are still undefined, or wiring a glossary check into CI, a commit hook, or an Nx target.
license: MIT
---

# Running coinagerie

Coinagerie lists the words a codebase uses, one headword each, and keeps a
glossary of them in step with the code. It reads names, never prose:
identifiers (object keys, enum members, quoted keys, and JSON or YAML keys
included) plus folder and file names without their extension. Comments, string
literals, template text, and regular expressions contribute nothing.

## One folder at a time

A run scans the folder its configuration file sits in. `--config <path>`
names the file, relative to the working directory. Without the flag, the
working directory (never a parent) is searched for `coinagerie.config.ts`,
then `.mts`, `.cts`, `.js`, `.mjs`, `.cjs`, first match wins. With no file,
defaults apply: scan the working directory, write nothing.

```bash
cd packages/widgets && coinagerie --check
coinagerie --config packages/widgets/coinagerie.config.ts --check
```

## Three modes

| Invocation           | Writes                                 | Exits 1 when                                                                                                             |
| -------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `coinagerie`         | nothing; prints a glossary to stdout   | the configuration or command line is rejected                                                                            |
| `coinagerie --check` | nothing                                | a destination has a missing or stale word, a glossary cannot be parsed, or the configuration or command line is rejected |
| `coinagerie --write` | each destination whose content changes | a glossary cannot be parsed, or the configuration is rejected                                                            |

- `--check` and `--write` together are refused.
- Each needs a destination, which is an `outputs` entry in the configuration or
  an `--output-json` or `--output-markdown` flag. Without one the run fails
  naming "no glossary destination".
- A bare run prints the **code's** words with every definition empty. It never
  reads a destination, so it cannot show a definition anyone wrote. Markdown is
  the default print; `--format json` prints a flat object. `--format` is
  ignored beside `--check` or `--write`, though an invalid value is still
  rejected.

## What counts as a word

- Identifiers split on case changes, `_`, `-`, and `.`. Acronym runs split
  sensibly (`HTTPServer` gives `http` and `server`). A word carrying digits stays
  whole (`utf8`). Words are lowercased; pure numbers and one-letter words are
  dropped.
- Plurals fold into their singular and inflections into their lemma, so
  `aspects` joins `aspect` and `configured` joins `configure`. Derivational
  families stay apart: `configuration` and `configure` are two words.
- The lemmatizer sometimes lands on a stranger headword than anyone wrote
  (`settings` becomes `set`). A glossary headword can
  therefore be absent from the code as spelled.
- TypeScript and JavaScript are read from the syntax tree, tolerating syntax
  errors. Python, SQL, shell, CSS, HCL, TOML, JSON, and YAML are read by
  lexical scanners. A file in any other language still contributes the words
  of its path.
- `.gitignore` is honored always. The files a run writes to are never scanned.
- The configuration file is scanned like any other: its own keys (`exclude`,
  `fold`, `outputs`) appear as words unless the configuration excludes them.

## Reading what it printed

Markdown destination: a block between `<!-- coinagerie:start -->` and
`<!-- coinagerie:end -->`, under a `## 🪙 Coinagerie` heading, with an optional
description, then one bullet per word, sorted.

```markdown
- **orbit**: The path a body follows around another.
- **phase**:
- **tolerance**:
  Continues on an indented line.
```

A bare `- **phase**:` is undefined. A bullet whose definition starts on an
indented line is defined. JSON destination: a flat object sorted by word, `""`
for an undefined one.

To list the gaps in a file:

```bash
grep -A1 -E '^- \*\*[^*]+\*\*:$' glossary.md   # a bare bullet whose next line is indented is defined
jq -r 'to_entries[] | select(.value == "") | .key' glossary.json
```

## Check and write

- **missing**: the code uses a word the destination lacks. **stale**: the
  destination lists a word the code no longer uses. Each destination is
  judged on its own, and no definition is ever copied between destinations.
- `--check` fails on any missing or stale word, and **passes when definitions
  are empty**. A green check means the words are listed, not that they are
  defined.
- `--write` adds each missing word as an empty bullet, keeps every existing
  definition exactly, and **deletes each stale word together with its
  definition**. A second `--write` with no code change changes nothing. A file
  with no anchors yet gets the block appended at its end, so the first write
  needs no hand-placed markers.
- A glossary that cannot be fully parsed stops the run before any destination
  is written: an unrecognized line, a duplicated word, invalid JSON, a
  non-string value. Nothing on disk changes.
- Diagnostics go to stderr, and a print run's stdout carries only the glossary.
  A failed check logs one line per out-of-step destination (abridged here):

```text
ERROR: 🪙 Found a glossary out of step with the code {"missing":["gate"],"path":"/repo/README.md","stale":["ephemeris"]}
```

Act on the failure with the `coinagerie-triage` skill.

## Flags

Each flag replaces the field it names; a field with no flag keeps the
configuration file's value.

| Flag                       | Replaces                                                                    |
| -------------------------- | --------------------------------------------------------------------------- |
| `--config <path>`          | which configuration file is read                                            |
| `--include <glob>`         | `include`; repeat for several                                               |
| `--exclude-paths <glob>`   | `exclude.paths`; repeat for several                                         |
| `--output-json <path>`     | the whole `outputs` list, with a JSON destination                           |
| `--output-markdown <path>` | the whole `outputs` list, with a markdown destination (both flags give two) |
| `--description <text>`     | the description of every markdown destination                               |
| `--format json\|markdown`  | what a bare run prints                                                      |

Destination paths are relative to the working directory, globs to the scanned
folder. No flag exists for `exclude.words` or `fold`: both are code, so they
live in the configuration. The `coinagerie-configure` skill covers every field.

## Wiring it in

- **CI or a commit hook**: run `coinagerie --check` from the folder holding the
  configuration, and let the exit code gate. Write locally with `--write`,
  commit the glossary, and check in CI.
- **Nx** (optional): the `@coinagerie/nx` plugin infers a cached
  `coinagerie-check` target, running `coinagerie --check` in the project's
  folder, for every project with a configuration file beside its
  `project.json` or a named `package.json`. The configuration and the project's
  own files are its inputs. A file the configuration reads from elsewhere, such
  as a parent glossary, belongs in the plugin's `inputs` option: otherwise a
  cached pass outlives an edit to it. The `command` option names how to run the
  binary when `coinagerie` is not on the path.
