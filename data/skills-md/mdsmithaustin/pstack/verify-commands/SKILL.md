---
name: verify-commands
description: "Apply whenever you write or review a command that decides whether work is done: a test invocation, an acceptance check, a CI gate, a shell assertion, a grep-based verify step. Names the failure signal, grounds paths, and catches the shapes that pass green while measuring nothing."
---

# Verify commands

A verify command is an acceptance test. Before shipping one, answer: **if this command were silently doing nothing, what in its output would tell me?** If you cannot answer, you have a command, not a check. Fix the command; do not invent a statement for it.

## Name the failing direction

Next to every runnable check, write one line naming the observable signal that means failure: `non-zero exit`, `"0 passed" in the summary line`, `the coverage line is absent`, `stderr contains "ECONNREFUSED"`. "The command fails" and "an error occurs" are restatements, not signals. `TBD`, `N/A`, and `none` are refusals. Short is fine; `non-zero exit` is complete. Prefer the signal the tool actually emits over one you imagine: for a command that already ran, state what you saw; for a new one, take the signal from the tool's documented output. N commands need N statements.

## Ground every path

Inherit the command that already worked in this repo, verbatim, before deriving a new one. A `cd` target or `--prefix` target must exist, or be created by an earlier step, and must hold the matching manifest (`package.json`, `Makefile`, `pyproject.toml`). Prefer `npm --prefix <dir> run <script>` over `cd <dir> && npm run <script>`; it does not depend on the caller's working directory. Do not hand-reason the filesystem: list it. If you cannot ground a path, say so instead of guessing.

## Shapes that pass while measuring nothing

| Trap | Why it passes | Instead |
|---|---|---|
| `pnpm ls vite \| grep -E '^vite@7'` | tree output starts each line with `└──`, so `^` never matches | drop the anchor, or match `(└\|├)── vite@7` |
| `npm test \| grep '714 passed'` | a count recalled from memory, stale from training | `grep -E '[0-9]+ passed'`, or run the count first |
| `X=$(cmd 2>/dev/null \|\| echo 0)` feeding `[ "$X" = "$Y" ]` | both sides default to `0` when inputs are missing, so parity passes on nothing | let the failure propagate, or guard with `test -f` and exit |
| `grep -c 'LITERAL' file == 0` while an instruction or comment quotes `LITERAL` | the gate trips on comment text, not on code | describe the forbidden thing by concept, not by literal |
| `! grep -q PATTERN file` when a sibling change legitimately adds `PATTERN` elsewhere in the file | a file-wide negative is unsatisfiable across regions | scope it: `awk '/^def f/,/^def /' file \| grep`, or an AST check, or a unit test |
| a test-name filter that matches zero tests | exit 0 with nothing asserted | list tests first (`--collect-only`, `--list`), then run the one named test |
| `npm test \| tail -20` whose exit status is read as the verdict | a pipeline exits with its last command's status, so `tail` reports 0 while `npm test` failed | start the same command line with `set -o pipefail; npm test \| tail -20` (bash, zsh). A `set` from an earlier tool call is gone |

The anchor trap has a family: `npm ls`, `yarn list`, `docker ps`, and `kubectl get` all print column or tree prefixes. `|| echo default` is acceptable only when absence is the default and the value is not used in a comparison meant to detect absence.

## Reviewing someone else's command

Report; never prescribe a replacement path you did not verify. A prescribed path is copied verbatim and carries zero information. A missing directory or manifest is a blocker: quote the raw target. A dynamic path, glob, `~`, or variable is a warning, not a licence to guess the literal.
