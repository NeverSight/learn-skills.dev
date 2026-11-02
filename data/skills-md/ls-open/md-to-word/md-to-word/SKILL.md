---
name: md-to-word
description: "Compile a Markdown document into Word (.docx) that matches a declared format: typography, headings, native OMML equations, three-line tables, captions, cross-references, TOC field, per-section page numbers, CSL bibliographies, and pre/post-export quality gates. 把 Markdown 导出为符合规范的 Word：学位论文、期刊论文、技术报告、公文、说明书都适用；格式写在一份随稿件进 Git 的格式文件里。Use when the user wants a .docx — a submission, a report, an official document, or just a readable copy — including 导出Word、文档转Word、转成Word、论文排版、公文排版、报告排版、prepare submission docx. Not for PDF, HTML or LaTeX output."
license: MIT
---

# Markdown → compliant Word

Turns a Markdown manuscript into a `.docx` whose typography comes from a declared format file. The
engine is deterministic — the same manuscript and the same declarations produce a byte-identical
file on every run — so do not substitute a hand-written python-docx script; run this pipeline.

**Before the first export in a session, confirm the engine is available**: `md-to-word --version`
must print a version. This skill ships documentation; if the command is missing, install it with
`pip install md-to-word-docx`, then run the check again.

**Read this before the first run.** The flags are not enough to drive it: the manuscript has a
contract (§2) and the format file has a closed vocabulary (§3), and neither can be guessed from
`--help`. Work through §1 once, then the commands are enough for everything after. An identical
copy ships inside the package as `guide.md` (`md-to-word --guide`); reading one copy suffices.

**The facts live in the manual. This file is the order of work.** `md-to-word --contract` prints the
manual's absolute path (Chinese or English, following the manuscript), the built-in preset paths and
a one-screen contract summary. When a spelling is not certain, read the manual rather than guess:
every word outside the vocabulary is a hard error with a line number.

## 1. The work, in order

1. **Confirm requirements & decide format** (§3): built-in preset (`zh-academic`, `en-nature`),
   an edited copy of one, or a custom format file supplied by the user (or extracted from a reference `.docx`).
2. **Normalize the manuscript**: Standard Markdown natively represents headings and body text, but
   structures beyond standard Markdown (captions, TOC, page breaks, abstract, display math) must follow the contract
   in §2. Map what the source actually contains; do not invent missing elements.
   Write a new file; never edit the user's original in place.
3. **Export** (§4).
4. **Read the gates** (§4), fix the reported lines, export again. Repeat until the exit code is `0`.
5. **Report** (§5): what format was applied, what the run warned about, and that the layout still
   needs a look in Word.

Nothing here accepts arbitrary Markdown and returns a finished document: a preset supplies
formatting, not missing structure. Pre-flight stops with a line number instead of emitting a
document that looks acceptable while its formatting was never mapped.

## 2. The manuscript contract

**Headings** — `#`, `##`, `###`, consecutive and unskipped; a heading that carries its own number
(`1.`, `2.1`) needs as many `#` as its number has levels. Heading levels are set by `#` only.

**Style lines** — a line starting with `%% ` sets that paragraph's style. One line is one paragraph,
ended by a blank line, no closing fence. Names come from a closed list, valid in either language;
these are the ones that come up in almost every document:

| Style line | Sets |
|---|---|
| `%% Title …` / `%% 文档标题 …` | the document title |
| `%% Author …` / `%% 作者 …` | author line |
| `%% Abstract Title …` / `%% 摘要标题 …` | the "Abstract" heading |
| `%% Abstract …` / `%% 摘要 …` | abstract body |
| `%% Keywords …` / `%% 关键词 …` | keywords |
| `%% Table Caption …` / `%% 表题 …` | caption above a table |
| `%% Table Note …` / `%% 表注 …` | note below a table |
| `%% Image Caption …` / `%% 图片题注 …` | caption for a figure |
| `%% References Title …` / `%% 参考文献标题 …` | the bibliography heading |

Full list: manual §3.4.

**Paragraphs** — one line is one paragraph; consecutive lines are never joined. A break *inside* a
paragraph (an address, verse, a long title) is written as a backslash or two spaces at the end of the
line: it becomes a line break within the same paragraph, not a new paragraph. Suspected wrapping — a
plain line without closing punctuation followed by another plain line — is reported as a warning with
the line numbers; short paragraphs written one per line are correct as they are.

**Title, author, abstract and keywords go in the body as style lines, never in YAML** — their
position on the page is the author's decision and YAML has no position. Pre-flight blocks those keys
and prints the exact line to write instead.

**YAML holds only position-independent configuration**: `bibliography:`, `csl:`, `crossref:`
(`link-citations: false` drops the in-text hyperlink).

**Equations** — `$$...$$ {#eq-name}` on its own line, referenced as `@eq-name`. Chinese manuscripts
get 「式/图/表」 prefixes and （1）numbering, English ones Equation/Figure/Table and (1);
`crossref: chapters: true` switches to per-chapter numbering. `\tag{}` is blocked.

**Citations** — `[@key]` parenthetical, `@key` narrative, resolved from `bibliography:` + `csl:`. A
`.bib` is mandatory once the manuscript cites: handwritten reference lists are not supported, and
`[@key]` without `bibliography:` would be printed literally.

**Figures and tables** — `![](path/img.png){width=13cm}`, caption in its own `%% Image Caption`
paragraph; table caption above, note below. Do not put `{#fig-...}` labels on images. Column widths
follow the separator row's dash lengths.

**Block markers** — three, each on its own line with blank lines around it: `{{< pagebreak >}}`,
`{{< toc >}}`, `{{< section page_number=lowerRoman start=1 >}}` (Chinese parameters `页码=` `起始=`
also work). A section marker closes *the section above it*; never add a page break next to one.

**Unsupported Markdown is blocked with a replacement, never printed literally** — the list is manual §2.8.

## 3. The format file

0. **Starting from nothing** — `md-to-word init` writes a complete preset copy plus a one-page
   manuscript that exports as-is. Useful when the user has no format file and no template.
1. **Built-in preset** — `zh-academic` or `en-nature`. Use as-is when the user has no custom
   template or spec; it provides a complete, compliant baseline out of the box.
2. **Copy and edit a preset** — change only the lines the user mentioned. Field order is fixed: font,
   size, bold, italic, alignment, line spacing, space before, space after, indent. Every style line
   must be complete; missing fields are errors.
3. **Reverse-engineer a target `.docx`** — `md-to-word-template target.docx -o format.txt`, then work
   through the "to confirm" list at the end of the draft.

Each property has exactly one accepted spelling, plus its Chinese or English counterpart; anything
else is a hard error with a line number (manual §3.1). `format.txt` in these instructions means *the
format file* — any filename works, `-f` takes it.

Citation style comes from `csl:` with a bundled name (manual §7) or a path to the user's own CSL.
Without `csl:`, Chinese manuscripts get GB/T 7714 numeric and everything else APA 7th.

Without `-f` the only file picked up is one named exactly `format.txt` beside the manuscript;
anything else there is ignored and named in a reminder. With no `format.txt`, the preset follows the
**manuscript's language**.

## 4. Export, then the gates

```bash
md-to-word manuscript.md -o manuscript.docx                    # preset by language
md-to-word manuscript.md -f format.txt -o manuscript.docx      # explicit format
md-to-word --guide                                             # this file, printed (pip-only entry)
md-to-word manuscript.md --contract                            # contract + guide, manual and preset paths
```

Run every command from the manuscript's directory: relative image and `.bib` paths resolve against
it. Add `--pdf` (macOS with Word) to expand fields and spot-check the result.

Add `--json` whenever the result has to be read back programmatically: stdout then carries one JSON
object — `ok`, `returncode`, `input`, `output`, `pdf`, `lang`, `messages`, `errors` — while progress
logs stay on stderr. The keys are fixed; the sentences inside them follow the manuscript's language.

Two gate levels, split by "would the mistake be visible afterwards" (criteria: manual §5):

- **Blocking** — invisible afterwards (dropped content, literal syntax, unmapped formatting); fix the line, never `--no-check`.
- **Warning** — visible but non-compliant (over-wide image, distant caption, skipped level); report it.

Exit codes: `0` every gate passed; `1` manuscript, gate or dependency problem; `2` a usage error
(bad flags or a missing argument); `3` the `.docx` was written but the optional `--pdf` proof was
skipped. Messages follow the manuscript's language.

## 5. Verify before delivery

- Confirm the `.docx` exists and the command exited `0`.
- Report the preset or format file, the citation style, and anything the run warned about.
- Say plainly that the layout still needs a manual check in Word. The engine verifies text and
  structure; row heights, column widths and where equations and captions settle are only visible in
  a real renderer.
- With a TOC, `{style-title}` headers or per-section page numbers, run once with `--pdf` and check the
  first page, the widest table, an equation-heavy page and the references.

## 6. Boundaries

- No custom cover pages, merged cells, multi-column text, inline text colour or text-wrapped figures.
  Export the body, then complete those in Word.
- Only equation cross-references are supported (`{#eq-x}` + `@eq-x`); figure and table numbers are
  typed into the caption.
- Sum and integral limits stay to the right of the symbol in numbered equations (Word stacks limits
  only in display math). Content and symbols are correct; only the arrangement differs.
- TOC page numbers and chapter headers are Word fields; Word asks once whether to update them.

Full statements: manual §6 (limits) and §8 (symptom → fix).

## 7. Scope

This skill compiles a finished manuscript into a `.docx` and nothing else. Drafting, rewriting,
polishing, searching for sources and verifying reference metadata belong to whatever writing tools
the user already works with: take the Markdown they hand you, produce the `.docx`, return it. The
interface in both directions is a Markdown file plus a `format.txt`.

## 8. What this file may rely on

- the commands `md-to-word`, `md-to-word-template` and `init`; every flag named in this file
  (`-o`, `-f`, `--preset`, `--contract`, `--guide`, `--version`, `--json`, `--pdf`, `--lang`) keeps
  its name and meaning
- exit codes `0` / `1` / `2` / `3`, and the JSON keys under `--json`
- the manuscript contract in §2, the vocabulary in §3, the preset names `zh-academic` and
  `en-nature`, and the fixed file name `format.txt`

Everything else — message wording, the layout inside the installed package, the version number — may
change. Never parse the prose of a message: pass `--json` and read the keys.
