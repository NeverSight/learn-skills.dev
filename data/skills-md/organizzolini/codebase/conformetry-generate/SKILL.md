---
name: conformetry-generate
description: Scaffold code with a conformetry generator instead of writing it by hand. Use when adding a module, component, service, application, or package to a workspace that has a conformetry configuration; when deciding whether a generator exists for the shape you are about to create; when a generator run overwrote or misplaced files; or when a conformance run reports a file that a generator should have produced. Covers both the Nx plugin and the conformetry command-line host, whose input contracts differ.
license: MIT
---

# Generating with conformetry

Conformetry generators render a **template** — an ordinary folder of ordinary
files — into an **instance** on disk. The same template is then the standard the
instance is measured against, so generating is not a convenience. Code written
by hand in a shape a template already describes starts life failing conformance.

## Before you write a file by hand, check for a generator

A generator name you guess at is rejected, so read the registry rather than
inferring it:

```bash
conformetry templates
```

In an Nx workspace, the emitted plugin answers the same question:

```bash
nx list conformetry
```

Both read the live configuration, so they are correct for the workspace you are
in. Neither output is worth caching in a note — it changes as generators are
added.

## Generation overwrites, unconditionally

There is no existence check, no skip-if-exists, no merge, and no conflict
detection anywhere in the write path. Every file in the template is rendered and
written over whatever is there.

**Never point a generator at a path that already holds work you want.** To
change an existing instance, edit it. Regenerate only when you intend to discard
what is there, or when the instance is missing files a template requires and you
have read what will be replaced.

The Nx path writes through a `Tree`, so `--dry-run` is honest and shows exactly
what would land:

```bash
nx g conformetry:<generator> --name=<name> --project=<project> --dry-run
```

Do that first when you are unsure where output will go.

## The two entrypoints disagree about inputs

This is the single most confusing thing about generating, and it is not a bug:
the same generator behaves differently depending on how you invoke it.

| | Nx plugin | Command-line host |
| --- | --- | --- |
| Invocation | `nx g conformetry:<name>` | `conformetry generate --template <name>` |
| Inputs | **every declared input is required** | none is ever required |
| Missing input | refuses, or prompts | refuses when the template interpolates it |
| Default destination | resolved from the workspace; refused for a new project with no `type` | none: `--directory` is required |

The remaining asymmetry is about _when_ a missing value is caught. The Nx path
requires every declared input up front, so it refuses before rendering starts.
The command-line host requires none of them, and catches the omission at the
moment a template asks for it — `MissingSubstitutionError`, naming the
placeholder and the template file.

So an input a template never interpolates can be omitted on the command-line
host and not on the Nx path. Anything a template does interpolate is required on
both.

**Pass every input explicitly on either path.** A template that means "optional"
says so with a section — `{{#owner}}…{{/owner}}` renders nothing when `owner` is
absent — rather than relying on a bare `{{owner}}`.

A generator is addressed by its full name on both paths — there are no short
alternative names. Both hosts list the real names when you get one wrong.

**The flag is `--template`, not `--generator`.** It matches the word the
configuration (`templatePath`), the `templates` command, and the conformance
report already use. `--generator` was removed rather than kept as an alias, and
passing it is refused by name — this command accepts unknown flags so a
template's inputs can be passed as flags, so without that refusal a stale
script would have its `--generator` silently dropped and appear to work.

`--template` is also optional at the command line. Omitting it at a terminal
offers an autocomplete over every configured template, each with its
description; **an agent shell is not a terminal, so always pass it** — omitted
there, the run is refused with the available names listed rather than left
waiting on a prompt.

## Where the output lands

On the Nx path the destination is resolved in this order, first match winning:

1. An explicit `--directory`.
2. No `project` input — treated as a new project, placed by its `type` input
   alongside projects of the same type. With no `type` either, the run is
   refused rather than written at the workspace root.
3. A `module` input — placed in that existing module. Naming a module that does
   not exist is an error, not an invitation to create one.
4. The generator's own scoped directory, from the first tagged pattern in its
   instance groups.
5. The directory already holding the most instances of that generator.
6. The project root.

Steps 4 and 5 are why a generator usually needs no destination at all: it knows
where its own instances live. Reach for `--directory` when you are deliberately
placing something outside that convention.

On the command-line host only `--directory` applies, and it is required: a
run without it is refused rather than written to a default location.

## Running without a person present

The command-line host prompts whenever stdin is a terminal, and there is no
flag to turn that off — an attached terminal is the whole condition, so an
agent shell, a hook, or a CI job is never prompted.

**Every input a generator declares is required**, on both entrypoints: a
generator substitutes each of its placeholders, and mustache renders a missing
one as an empty string rather than failing, so an optional input would quietly
put a hole in the generated file. With no terminal, an input you did not pass
is therefore a hard error naming the flag to pass — never a silent default, and
never a menu drawn where nothing can answer it. Pass every input the template
declares, or run where you can be asked.

## After generating

Two steps, both cheap, both catching a whole class of mistake:

1. **Check conformance** of what you just made. A generated instance conforms by
   construction, so a difference means the destination was wrong, an input was
   empty, or you overwrote something. See the `conformetry-validate` skill.
2. **Implement inside the generated files.** Do not build a parallel structure
   beside them. The template's section comments and declarations are the
   contract; adding to them is always allowed, removing them is what breaks.

## When a generator does not exist yet

Adding one is a configuration change, not a code change — see the
`conformetry-configure` skill. Two things bite immediately after: the emitted Nx
plugin has to be regenerated with `nx sync`, and every conformetry command
refuses to run while it is out of date rather than working from stale
definitions.

## Seeing it rather than reading about it

[`conformetry-examples`](https://github.com/JimmyPaolini/codebase/tree/main/packages/ic-suite/conformetry/conformetry-examples) is eleven self-contained examples, each
with its own configuration, template, instances, and command. Two are worth
running before scaffolding something unfamiliar:

- **`hello-template`** — the smallest generator that exists, generated and then
  validated in two commands, so the loop is visible end to end.
- **`case-variants`** — every derived case variant in paths and in contents,
  and how an explicit input overrides one.

Each runs in about a second and its guide quotes the output it produces, which
the package's own test suite asserts. See
[its AGENTS.md](https://github.com/JimmyPaolini/codebase/blob/main/packages/ic-suite/conformetry/conformetry-examples/AGENTS.md) for which example answers which question.
