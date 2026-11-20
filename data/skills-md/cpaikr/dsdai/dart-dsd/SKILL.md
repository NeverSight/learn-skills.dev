---
name: dart-dsd
description: "Read, review, and edit Korean DART Editor .dsd documents (감사보고서, 검토보고서, 사업·분기·반기보고서 drafts) without corrupting them, using the dsd CLI. Use when a task involves a .dsd file: converting it to Markdown or exporting it to Excel, finding or comparing figures, comparing two versions side by side, rolling a report forward to a new period, updating table cells or text, adding or removing rows, columns, tables, or paragraphs, or verifying an edited .dsd before it returns to DART Editor. Not for .drt submission packages, OpenDART API downloads, or operating the DART Editor GUI."
---

# DART DSD

A `.dsd` is a ZIP holding `contents.xml` (the document), `meta.xml` (editor
metadata and image list), and embedded images. DART Editor remains the
authority for layout and filing. Read the document faithfully and change only
what was asked, leaving every other byte as DART Editor wrote it. All mechanics
go through the `dsd` command-line tool.

## Treat documents as confidential

DSD files are usually unreleased client filings. Process them locally. Do not
upload them or their text to external services, commit them to repositories,
or copy them into shared locations. When only structure matters, use
`dsd inspect`, which reports no document text. Put converted Markdown and
edited copies where the user asked, or beside the source.

## Start with the available executable

Reuse a successful `dsd --version` from this execution context; otherwise run
it once. Recheck after the executable or environment changes, or after a
failure that suggests a broken installation.

- If `dsd` is missing or unusable, or the user asks to install or upgrade it,
  read [installation](references/installation.md), then resume the task. A
  document error or a refusal is not an installation problem.
- An `advisories[]` entry such as an update notice is not part of the result
  and does not authorize an upgrade.
- Use `dsd <command> --help` for exact options. Do not assume a feature from
  this skill's repository is in the installed release; check its help.

## Interpret the output

Each command prints one JSON object to stdout: `ok`, `command`, `result`,
`warnings`, `error`, `metadata`. Exit status 0 means `ok: true`; 1 is a failure
(`error.code`, `error.message`, `error.hint`), including `check` finding errors,
whose issues stay in `result`; 2 is an invalid invocation. Read `warnings`
before reporting success. `--format text` on `outline`, `read`, `table`,
`find`, `diff`, and `compare` gives a compact listing that costs fewer tokens;
failures stay JSON.

## Route the task

- Reading, converting, exporting to Excel, finding, or comparing (including a
  draft against a filed or colleague's version): read
  [reading](references/reading.md).
- Changing a document: read [editing](references/editing.md); it ends with the
  verification every edit needs.
- Content the views flag as unverified, a hand edit of `contents.xml`, or a
  `check` warning to interpret: also read the [format reference](references/format.md).

Locators: tables are `T1`, `T2`, … in document order; rows `R#` count THEAD,
TBODY, and TFOOT rows; columns `C#` are grid columns after span expansion.
Outputs print them together (`T3R4C2`); commands take bare numbers
(`dsd table FILE 3`, `--table 3 --row 4 --col 2`). Line numbers refer to
`contents.xml`.

## Universal rules

- Never write over the source unless the user explicitly authorizes it; edits
  refuse to replace an existing file without `--force`.
- Never re-serialize `contents.xml` with an XML library or re-zip the archive
  with a generic tool: that rewrites CP949 image names, quoting, empty
  elements, and line endings, which DART Editor may mis-handle.
- Quote figures and titles from the tool's output, never from memory or a
  generic unzip.
- Editor guidance (`◆click◆` comments, `LIBRARYLIST`, `WARNING`) and unfilled
  `INSERTION` slots are not document content.
- Do not claim DART Editor acceptance unless the file was opened there.

## Finish

Reading is complete when the requested content has been delivered from the
tool's output, with locators where the user needs to act on it. Editing is
complete when the new file exists, `dsd check --against` passes, and `dsd diff`
shows exactly the intended changes; report as [editing](references/editing.md)
describes.

## Report skill problems

This skill and the CLI are maintained at <https://github.com/cpaikr/dsdai>.
Propose an issue there when a task exposes a defect or avoidable friction in
them:

- the CLI crashes, hangs, or writes a file that `check` or DART Editor rejects;
- its output contradicts the XML or DART Editor: missing or altered text,
  coordinates that land on another cell, a wrong `diff`;
- a refusal or `unverified-*` report on content DART Editor routinely
  produces, forcing the text-editing route;
- guidance here that was wrong or missing, or that cost avoidable detours.

Errors in the document, DART Editor's own behavior, and tasks this skill
excludes are not skill issues. Work around the problem and finish the user's
task first; raise the issue in the final report.

The repository is public, so an issue carries no document content: no text,
figures, company or person names, file or image member names, or data values
such as `AUNITVALUE`. Describe structure instead: the command with placeholder
paths (`in.dsd`), `error.code` and the message with document text replaced by
`…`, element tags and attribute names, the `meta`/`document` versions from
`inspect`, `dsd --version`, and the OS. When a reproduction helps, write a
minimal `contents.xml` fragment with invented text. State expected and actual
behavior and the workaround used.

Search existing issues first (`gh issue list --repo cpaikr/dsdai --state all
--search "<keywords>"`) and prefer a comment on a match over a new issue.
Filing publishes, so show the user the drafted title and body, and file only
after they approve: `gh issue create --repo cpaikr/dsdai --title "<title>"
--body-file <draft> --label <bug|enhancement|documentation>`. Without `gh` or
GitHub access, give the user the draft and
<https://github.com/cpaikr/dsdai/issues/new>. Report the resulting URL.
