---
name: codometer-measure
description: Run a codometer measurement, decide where its report goes, or read a badge block or JSON report it produced. Use when running codometer or npx @codometer/cli, choosing --output-json/--output-markdown and --check flags, wiring codometer into a CI step, splicing a badge block into a README, or reading a codometer JSON report's metrics, limits, or failures. Covers the command-line host directly, without assuming any task runner.
license: MIT
---

# Running a codometer measurement

Codometer walks a directory, parses everything it recognizes, and reports what
it counted — as console output, a JSON report, a markdown document, or a badge
block spliced into an existing file. It counts languages the way any analyzer
would — files, lines, classes, functions — and also the declared conventions a
repository holds itself to, which is usually the more interesting number.

## One directory at a time

**Codometer measures one directory and knows nothing about workspaces, task
runners, or project graphs.** Pointed at a project, it measures that project's
own sources and whatever inputs its configuration declares — nothing else, and
nothing about sibling projects. There is no `--directory`: a run always
measures the process's working directory, with no per-invocation override.

```bash
cd packages/widgets && codometer --check limits
```

Do not assume it takes a project name, a package name, or anything a task
runner would resolve. If a workspace runs it per project, that iteration is the
runner's job, not codometer's. `--inputs [globs...]` narrows a single run to
exactly the globs given, running only `language` analysis over them, with no
configured input — not even the built-in `codebase` one — active.

## Finding the configuration

With no `--config`, codometer searches upward from the measured directory and
takes the **first** configuration file it finds. The nearest one wins outright:
nothing from a further ancestor is folded into it. A project with no
configuration of its own is measured by the nearest ancestor's, in full. A
configuration file is always read as a plain object — exporting a function is
not recognized and falls back to an empty configuration.

`.gitignore` is already in force through discovery — a build directory or
virtual environment pruned by an ignore file needs no exclusion naming it
again — and git itself is never invoked, so an unversioned directory measures
the same way a repository does.

## Every flag is independent

`--output-json`, `--output-markdown`, `--check`, and `--format` are asked for
separately, and none of them turns another on:

| Invocation | Writes | Fails on staleness | Fails on a breach |
| ---------- | ------ | ------------------ | ------------------ |
| `codometer` | no | no | no |
| `codometer --check limits` | no | no | yes |
| `codometer --check reports` | no | yes | no |
| `codometer --check limits,reports` | no | yes | yes |
| `codometer --output-json` | yes | no | no |
| `codometer --output-json --check limits` | yes | no | yes, after writing |

`--output-json`/`--output-markdown` passed **bare** write wherever the
resolved configuration's own output of that kind declares, and are refused
before anything is measured when the configuration names no such output —
there is then nowhere to write it. Passed **with a path**, that path is used
for this run alone, whether or not the configuration declares an output of
that kind: `codometer --output-json report.json` writes there regardless of
what `outputs` says.

Combining an `--output-*` flag with `--check reports` is refused rather than
obeyed: nothing can be stale in the run that just wrote it. A run that both
writes and gates still produces **every** resolved output before it fails, so
the report on disk reflects the current measurement even when the run's exit
code says no.

A **breach** and **staleness** are different findings, never reported as one. A
`warn`-severity breach prints and leaves the exit code alone; a `fail`-severity
breach exits `1`, and only where `--check limits` asked for a gate at all. For
what to do about either, reach for the `codometer-triage` skill.

```yaml
- run: npx @codometer/cli --check limits,reports
```

## Reading a report

The JSON report groups metrics by target. Every metric carries its value, its
path within its target, a unit (`"bytes"` or `null`), every limit declared
against it, and — for a `comment` selector's metric — the `instances` where
each breaching block was found:

```json
{
  "failures": [],
  "targets": [
    {
      "empty": false,
      "files": 42,
      "name": "codebase",
      "metrics": [
        {
          "instances": null,
          "limits": [{ "breached": false, "label": null, "severity": "fail", "value": 500 }],
          "name": "codebase.typescript.interfaces",
          "path": "typescript.interfaces",
          "unit": null,
          "value": 118
        },
        {
          "instances": [{ "file": "src/main.ts", "line": 4, "measured": 214 }],
          "limits": [{ "breached": true, "label": null, "severity": "fail", "value": 0 }],
          "name": "codebase.custom.TypeScript Comment Budget",
          "path": "custom.TypeScript Comment Budget",
          "unit": null,
          "value": 1
        }
      ]
    }
  ]
}
```

A limit that held is written out exactly like one that did not, so a consumer
can render headroom, not only failures. A `comment` selector's `value` counts
the blocks that broke its own budget, and `instances` names each one's file
and line — `null` on any metric that only counts. `failures` holds what the
run could not do at all — a target that matched no files despite carrying a
limit, a limit bound to a metric nothing measured — and is unrelated to a
breach or staleness.

## Where output goes

What a run prints and what it writes are asked for separately. `--format json`
prints the report and `--format markdown` prints the rendered badges; a path
always names a file, never the console. Left off, `--format` falls back to the
resolved configuration's own required `format` field — never inferred from
which other flags are present.

Two file sinks — `--output-json [path]` and `--output-markdown [path]` —
neither of which implies the other or implies printing.

`--output-markdown` writes into a file somebody else may have written the rest
of. The block sits between two markers, named `<!-- codometer:start -->` /
`<!-- codometer:end -->` unless the configuration renames them; it is spliced
between them when they are there, appended with them when they are not, and
the file is created when it does not exist.

Every file codometer would write is excluded from what it measures, on every
run regardless of flags — a written report left in the count would be stale
the instant it landed, and a splice would move the very markdown metrics it
just wrote into.

## A runtime detail that reads like a bug

Compressed sizes are Node-version dependent, because the bundled zlib differs
between releases. A report written on one Node runtime and checked on another
reads as stale even when nothing in the source changed. Run `--check reports`
on the same runtime the repository pins for everything else, and reach for the
`codometer-triage` skill before concluding a stale report is a real
regression.
