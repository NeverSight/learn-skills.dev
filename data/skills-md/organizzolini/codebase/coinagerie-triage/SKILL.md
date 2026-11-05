---
name: coinagerie-triage
description: Use when coinagerie --check exits non-zero, when a run names missing or stale words, refuses a glossary it cannot parse, or rejects a configuration or command line, when a --write deleted a definition, when a glossary headword looks wrong or surprising, when a check passes locally and fails in CI, or before adding a word to exclude.words, narrowing include, or deleting a glossary block to make a failing check pass.
license: MIT
---

# Acting on a failed coinagerie check

A failure is one of five kinds, and each calls for a different response. Read
which one occurred before reaching for the configuration file.

| Logged as                                    | Kind                                 |
| -------------------------------------------- | ------------------------------------ |
| `Found a glossary out of step with the code` | missing and stale words              |
| `Refused a glossary it cannot parse`         | a malformed destination              |
| `Rejected the configuration`                 | a configuration fault                |
| `Rejected the command line`                  | a flag the run cannot use            |
| `Found no glossary destination to check`     | no `outputs` and no destination flag |

The last three have one fix each: correct the configuration (the
`coinagerie-configure` skill), drop the conflicting flags (`--check` and
`--write` never combine, `--format` takes `json` or `markdown`), or add a
destination.

## Missing words

The code uses a word the glossary lacks. Decide each named word, one at a time:

| The word is...                                                   | Response                                                     |
| ---------------------------------------------------------------- | ------------------------------------------------------------ |
| a real term of the codebase                                      | `--write` adds it bare, then define it (`coinagerie-define`) |
| a language keyword or boilerplate that means the same everywhere | an `exclude.words` entry, with that reason                   |
| a headword nobody wrote (`set` from `settings`)                  | a `fold` entry mapping it to the word people mean            |
| an accident: a typo, a throwaway name                            | rename it in the code                                        |
| coming from files that are not the codebase's own words          | an `exclude.paths` glob for generated or vendored files      |

Find where a headword comes from by searching the code for the word **and its
forms**: its plural, its `-ing` and `-ed` forms, and the pieces of camelCase
names. Folding means the headword may not appear literally.

An empty bullet is a debt the check will never collect. Define each word that
carries meaning in the same change that adds it.

## Stale words

The glossary lists a word the code no longer uses, and `--write` deletes it
**together with its definition**. Ask why it went stale before writing:

- **Renamed.** The definition belongs to the new word, and a rename is the case
  that loses hand-written text. Before any write, edit the old bullet's bold
  headword to the new word by hand: the definition stays, and the check then
  passes without a write. After a write that already deleted it, recover the
  text from version control history of the glossary file.
- **Removed on purpose.** Write. Tracking the code is the design.
- **Newly excluded** by a words or paths entry. Write; the deletion is the
  intent.
- **The scan moved, not the code.** Dozens of stale words after a change to
  `include`, `exclude.paths`, a checkout, or a missing build step mean the
  scanned set shrank. Restore the scan, then check again: a write here deletes
  every definition the shrunken scan no longer sees.

Read the stale list before every write. After writing, run `--check` and
confirm it passes.

## A glossary it cannot parse

The error names the file, and the line for a markdown fault, and nothing was written. Causes: a line in
the block that is neither a bullet nor indented continuation, a word listed
twice, text placed directly after the colon with no space, a missing, doubled, or
reversed anchor, invalid JSON, or a value that is not a string. Fix the named
line by hand, and every definition around it survives.

Deleting the block or the file to get past the error makes the next write
start over with every definition empty.

## A check that disagrees between machines

- **Passes locally, fails in CI.** The scanned sets differ. Suspects: a
  generated or build folder present locally and ignored in CI, or the reverse;
  an uncommitted glossary or configuration; a different working directory. Run
  a bare `coinagerie --format json` in both and compare.
- **A cached pass survives an edit.** Under a task runner's cache, a file the
  configuration reads from elsewhere, such as a parent glossary, has to be
  declared as an input of the check.
- **A word reappears as missing after a parent glossary changed.** A child whose
  `exclude.words` reads the parent's words lists everything the parent drops.
  Move the definition down deliberately, or restore the parent's entry.

## Impulses to turn into decisions

| Impulse                                            | Instead                                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| exclude every missing word so the check goes green | decide each word with the table above; an excluded word loses its definition |
| widen `exclude.paths` until nothing is missing     | exclude only files that are not the codebase's own words                     |
| run `--write` and move on                          | read the stale list for renames, and edit each renamed headword first        |
| delete the block and regenerate                    | fix the line the error names                                                 |
| call a passing check finished                      | a green check allows empty definitions; define what you added                |
