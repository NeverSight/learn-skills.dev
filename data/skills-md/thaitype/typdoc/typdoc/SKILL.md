---
name: typdoc
description: Work with a typdoc project — a folder of Markdown documents whose frontmatter is checked against schemas and whose references are tracked. Find documents, read them, create them, change their fields, move them without breaking links, and check the project before committing. Use whenever a repository has a `.typdoc/` folder, when a task mentions typdoc, or when asked to create, update, move, query or validate documents such as tickets, notes, learnings or decisions that live in one.
---

# typdoc

Written for **typdoc 0.6.0**. Source and issues: https://github.com/thaitype/typdoc —
use it only when something here does not match what the binary does.

typdoc treats a folder of Markdown files as typed, linked documents. Each document is YAML
frontmatter plus a free Markdown body. typdoc owns the frontmatter: which fields a document
has comes from a **schema**, which files a schema applies to comes from a **collection**, and a
**ref** is a frontmatter field or a body link that points at another document. Every command
has `--json` and meaningful exit codes, because its main users are agents.

This skill describes how typdoc works and what each way of doing a thing does to the files. It
does not decide for you.

## 1 · Check that typdoc is installed, and which version

```console
$ typdoc --version
typdoc 0.6.0
```

**Not found** (`command not found`, exit 127): typdoc is not installed, or its directory is not
on `PATH`. Try `~/.local/bin/typdoc --version` first, because the install script puts it there and
never edits `PATH`. If that works, call it by that path, or add the directory for this session:
`export PATH="$HOME/.local/bin:$PATH"`. On Windows the directory is `%USERPROFILE%\.local\bin`,
added for this PowerShell session with `$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"`.

**Not installed:** installing is the user's decision, since it downloads and runs a script from the
internet. Tell the user, and install only when they agree. This installs the version this skill
is written for:

```console
$ curl -fsSL https://typdoc.thaitype.dev/install | TYPDOC_VERSION=v0.6.0 sh
```

- macOS and Linux, amd64 and arm64, with no Rust toolchain. The script checks the SHA-256
  checksum and installs to `~/.local/bin`; `INSTALL_DIR` changes the directory.
- Put the variables after the pipe, right before `sh`. Written before `curl`, they never reach
  the script, and you get the latest release in the default directory.
- With a Rust toolchain instead: `cargo install typdoc --version 0.6.0`.
- On Windows, in PowerShell, with the variable set before the pipe:
  `$env:TYPDOC_VERSION = 'v0.6.0'; irm https://typdoc.thaitype.dev/install.ps1 | iex`.
  It installs `typdoc.exe` to `%USERPROFILE%\.local\bin`, and never edits `PATH` either.

**A different version:** say so to the user before relying on this skill, and prefer what
`typdoc <command> --help` says wherever the two disagree.

## 2 · Find the project

typdoc walks up from the current directory to the nearest folder holding `.typdoc/config.json`.
From anywhere else, point at it with `TYPDOC_DIR`:

```console
$ TYPDOC_DIR=path/to/project typdoc list --ids
```

No project found is exit 5: `no project found: there is no .typdoc/config.json in … or above it`.

A path argument that does not start with `/`, `./` or `../` is relative to the **project folder**,
not to the current directory. To learn what a project holds, read `.typdoc/config.json`,
`.typdoc/collections/*.json` and the schemas they name — see
[project-layout.md](references/project-layout.md).

## 3 · Read results by exit code and `--json`

Branch on the exit code, then read `--json`. Without `--json` every command prints labeled text
meant for a person.

| Exit | Means |
| --- | --- |
| 0 | Done. A query that matches nothing is 0 too |
| 1 | The call is wrong: bad syntax, or a key/namespace that is ambiguous |
| 2 | Validation failed (or the config cannot be read) |
| 3 | A `set --if` condition was false — nothing written |
| 4 | Could not get the namespace's lock in time |
| 5 | The document, key, path or project does not exist |
| 6 | A file cannot be read or written |
| 7 | The destination already exists — nothing written |

On exit 0 the result is on stdout. On any other exit the error is on stderr; with `--json` it is
one object `{"error", "code", "details": [...]}`, plus `candidates` when a name was ambiguous.
`validate` is the exception: its report is on stdout whatever the verdict. Details and what to
do next: [exit-codes.md](references/exit-codes.md).

## 4 · Name a document

By **key** (`WF-2`) when its schema has a code, or by **path** from the project folder
(`tickets/WF-2.md`). Anything ending in `.md` is a path. In a project with several namespaces a
bare key can be ambiguous (exit 1, with `candidates`); write `story-2:WF-1`, or use the path,
which is never ambiguous. The path form is the one to pass between programs.

## 5 · The usual loop

**Find**

```console
$ typdoc list --collection tickets --where status=open --where 'ref.all(blocked_by).status=done'
$ typdoc list --ids --where status=open          # one name per line, for pipes
$ typdoc refs WF-1 --reverse --json              # what points at WF-1
```

**Read**

```console
$ typdoc get WF-2 --json                         # frontmatter as data
$ typdoc toc notes/setup.md                      # headings with line ranges
```

The body is ordinary Markdown: read it with any file tool. `toc` gives line ranges to read one
section.

**Change** — what each way does to the files:

| Task | With typdoc | By hand |
| --- | --- | --- |
| Create a coded document | `typdoc new WF "Title"` takes the namespace lock, issues the next number, records it in `.typdoc/state/`, fills defaults; `--slug lock-order` names the file `WF-8-lock-order.md`, as the collection's `slug` allows | Writing `WF-3.md` yourself records nothing: `validate` warns `state.behind` until the next `typdoc new`, two people doing it at once can pick the same number, and if the file is deleted before any `new` its number can be issued again |
| Create a document without a code | `typdoc new notes/x.md --set title=…` refuses a path no collection's `match` fits (exit 1) and fills defaults | Same result if the path and frontmatter are right; `validate` tells you if they are not |
| Change fields | `typdoc set WF-2 status=done` checks the schema before writing; `--if` makes it compare-and-set | Keeps comments and formatting that `set` does not (see below); nothing is checked until `validate` |
| Move or rename a document without a code | `typdoc mv notes/dox.md notes/doc.md` renames it or moves it to another folder the collections allow, and rewrites every ref in this project that points at it, in frontmatter and body links, keeping each ref's written form | `git mv` or a file move leaves every ref pointing at the old name |
| Move a document with a code | Its file name carries its key, so inside its namespace only the slug after the key can change (`typdoc mv WF-1 tickets/WF-1-lock-order.md`); another key or folder is exit 1: `typdoc mv WF-1 tickets/WF-5.md` and `typdoc mv WF-1 --renumber <its own namespace>`. `typdoc mv WF-1 --renumber story-2` moves it to another namespace under the next key there, keeps its slug (`WF-1-lock-order.md` becomes `WF-4-lock-order.md`), and rewrites refs to the new key; a ref written with the slug gets the new key with the same slug | Renaming `WF-1.md` to `WF-7.md` by hand makes it a different document, `WF-7`: every ref to `WF-1` breaks (`refs.resolve`, `body.links`), and the state file falls behind (`state.behind`) |
| Edit the body | — (typdoc has no body command) | Any editor or file tool |

A `set` rewrites the whole frontmatter block: values are kept exactly, but comments, blank
lines between fields, flow lists (`[a, b]`), quote style, anchors/aliases and YAML tags are not.
The full list is in [commands.md](references/commands.md#set).

**Check**

```console
$ typdoc validate                                # the whole project; exit 2 if any error
$ typdoc validate notes/broken.md --json         # named documents only
```

Each finding has a `rule` id; [validation.md](references/validation.md) says what each one means
and how to fix it. Worth running after any hand edit: `set` and `new` check their own write, but
nothing checks what an editor or `git mv` did until `validate` runs.

## Quoting

Put every `--where`, `--if`, `--set` and `--namespace` value in single quotes. `<` and `>` are
shell redirections, `*` is expanded by the shell, and an expression is one argument with no
spaces around the operator (`status=open`, not `status = open`). Full syntax:
[query.md](references/query.md).

## References

| Need | Read |
| --- | --- |
| Every command, option and `--json` shape | [commands.md](references/commands.md) |
| `--where` / `--if` / `--set` syntax, `ref.*`/`refby.*`, escaping, quoting | [query.md](references/query.md) |
| Every rule id a finding can carry, and the fix | [validation.md](references/validation.md) |
| Each exit code and what to do next | [exit-codes.md](references/exit-codes.md) |
| How to read a project: config, collections, schemas, keys, namespaces, imports, state | [project-layout.md](references/project-layout.md) |
