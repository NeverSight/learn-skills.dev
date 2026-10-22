---
name: office
description: MAIN method for Office and PDF — every read, create, edit, review, convert, version of .docx/.doc/.dotx/.xlsx/.xls/.xlsm/.pptx/.ppt/.pdf (and images) MUST go through officecli. Use whenever a task touches .docx/.doc/.xlsx/.xls/.pptx/.ppt/.pdf/image files or asks for document drafts, suggestions, track changes, history, batch generation, or format export. The native read/edit/write tools are blocked for these extensions.
---

# Office documents

> **MAIN for Office/PDF** — every **read** and **handle** (create/edit/accept/undo/history/revert/comment/track-change) of `.docx/.doc/.dotx/.dotm/.xlsx/.xls/.xlsm/.xlsb/.xltx/.pptx/.ppt/.potx/.pdf` (and images `.png/.jpg/.jpeg/.gif/.bmp/.tiff/.webp`) **MUST** go through `officecli`. The plugin's guard blocks the native `read`/`edit`/`write` tools for these extensions and errors with `use officecli tool for office/PDF files — office is the main method for read + handle`. Do not bypass.

The plugin overrides the builtin `edit` tool: every edit — text or binary — runs through a draft and needs `officecli accept` to reach the real file. Two edit surfaces:

- `officecli(action="edit", filePath, content)` — replaces the whole draft with your markdown (for office/PDF, this is the ONLY write surface)
- `edit` tool (`filePath`, `oldString`, `newString`) — patches the existing draft in place (text files only; blocked for office/PDF/images)

For office/PDF/images, `officecli` is the ONLY path: `read` returns markdown, `create`/`edit` consume markdown, both sides inside `officecli`. Never use `read`/`edit`/`write` on `*.docx,*.doc,*.dotx,*.xlsx,*.xls,*.xlsm,*.pptx,*.ppt,*.pdf,*.png,*.jpg,*.jpeg,*.gif` — guard fails them. For live Word content on the same machine use `officecli(action="read", live=true)` (prefers `Application.Word` document whose full name matches `filePath`, falls back to saved file; local-only).

## Draft lifecycle (every task)

Every write runs through a **draft**: nothing reaches the real file until `accept`. The lock is claimed lazily on the first mutating action and released on accept/undo.

**L1 path (markdown, 80% tasks):**
1. `create filePath + content` for a new file, or `edit filePath + content` to open an existing file's draft
2. Re-`edit`, `comment`, `approve`, `metadata`, `watermark` freely while iterating — all mutate the same draft
3. `accept` flushes the draft to disk, records a version snapshot, releases the lock

> **Enduser report rule:** endusers are office staff, not developers. Report after every office task in the **user's language**, plain words, fixed shape — never paste tool output, JSON, hashes, or tool names (`draft`, `lock`, `accept` stay internal):
>
> English template (render it in the user's language — never send it as-is to a non-English Enduser):
>
> ```
> Done: 3 changes in <Contract.docx>
> 1. <Clause 2 — payment term fixed> — waiting for you
> 2. <Pricing sheet — totals recomputed> — applied
> 3. <Cover page — date updated> — waiting for you
>
> Next: reply "approve 1 and 3" to apply, or "reject 1" to keep the old text.
> ```
>
> Shape: 1 line result → numbered changes (what + where + state: applied / waiting for you) → one clear next action phrased so a one-word reply works. Pending suggestions must be numbered the same way as comment ids so "approve 2" is unambiguous. The full standard — 8 rules, the four message shapes (report/question/failure/reminder), Vietnamese number & register conventions, and the pre-send self-check — is [references/enduser-output.md](references/enduser-output.md); apply it to every user-facing message.

> **Suggest-first rule:** when the target is a document you did **not** author this session (`create` reports *pre-existing document*), seed the draft with `edit` from the markdown you just `read`, then make every content change as `comment` + `suggestedText` on the exact range/cell/box (`approve` applies a suggestion into the draft). Direct content edits to such a draft are allowed only when the user chose that mode — if it is not clear whether the task wants suggested edits or direct edit, **ask the user before writing any content change, in the exact format of the mode question in [references/reviewing.md](references/reviewing.md)** — then wait for the answer. Bulk generation from a Reference (L3 `clone` + `substitute`) is direct by design and does not need to ask.

**L3 path (100% Format, clone + substitute — for Procurement Dossier or any task needing byte-identical Format):**
1. `clone filePath(source Reference) + targetPath(new file)` — copies ZIP verbatim, draft is real OOXML (PK), Format identical
2. `substitute filePath(target) + data(JSON map {{key}}→value)` — run-preserving replace in `w:t`/`a:t`/`t` (keeps `w:rPr`/`w:pPr`, theme, styles)
3. `accept` — copies draft ZIP verbatim to real file
4. `verify-l3 filePath(target) + referencePath(Reference)` — optional gate, asserts only text nodes differ

Done means: every write path ended in `accept` or `undo`. A dropped draft leaves the file locked and the change invisible. Use L3 when the Reference already carries the required Format; use L1 when authoring from scratch via markdown.

Universal actions (all via `officecli` — main for office/PDF):

- `read` — `officecli(action="read")` extract any office/PDF/image to markdown; inspect before editing anything you did not author this session (native `read` is blocked for `.docx/.doc/.xlsx/.xls/.pptx/.ppt/.pdf`)
- `diff` — unified markdown diff of draft vs real file; call before accept on edits to files you didn't create
- `preview` — renders the draft to an HTML file for human inspection
- `undo` — discard draft, real file unchanged
- `list` — active drafts across all files; run when resuming after an interruption
- Stale lock (`staleLockHours`, default 24h): `lock-status`, then `force-release` — the displaced session's next mutation fails with an error, expected

## Bundled format skills (anthropics/skills, source-available)

`skills/docx`, `skills/xlsx`, `skills/pptx`, `skills/pdf` are bundled verbatim from `anthropics/skills` (see `LICENSE.txt` in each). They hold the canonical gotchas and helper scripts per format. `skills/office` is the router + draft/history; delegate format-specific authoring to the bundled skill when fidelity matters. Quick markdown→officecli covers 80%; the bundled skill covers the 20% that silently corrupts.

| Need | Where |
|---|---|
| Simple headings + pipe tables (markdown enough) | `officecli create/edit` → v2 styled defaults (A4, D9E1F2, DXA) |
| Precise .docx: sections, images, TOC, page size, redlines, comments | `skills/docx` — `docx` npm + `scripts/merge_runs.py`/`comment.py`/`accept_changes.py`/`office/validate.py` + `soffice` |
| XLSX with formulas, styling, recalc | `skills/xlsx` — `openpyxl` + `scripts/recalc.py` (mandatory) + `pandas` for bulk |
| Styled .pptx / template fill | `skills/pptx` — `pptxgenjs` + `scripts/add_slide.py`/`thumbnail.py`/`clean.py` |
| PDF forms, table extraction, merge/split | `skills/pdf` — `forms.md`/`reference.md` + `pypdf`/`pdfplumber`/`reportlab` helpers |

Advanced edit on existing file: `officecli read` to inspect → `officecli edit` to open draft → run the format skill's script **against the draft file** (see `officecli list` / `.opencode/office/drafts/` in `src/core/draft/manager.ts:18`), iterate → `officecli accept`. Never touch the real file bypassing the lock. For quick markdown writes, `officecli edit` alone is enough.

## Task router

| Task type | Reference |
|---|---|
| New document (L1, markdown→office) | [authoring.md](references/authoring.md) + format skill (`docx`/`xlsx`/`pptx`/`pdf`) |
| New document (L3, 100% Format) — clone Reference + substitute | `officecli clone → substitute → verify-l3` + `references/template.docx` with `{{placeholder}}` |
| Template batch generation, validation gates, format conversion | [authoring.md](references/authoring.md) + format skill (`docx`/`xlsx`/`pptx`/`pdf`) |
| Editing/reviewing existing documents, suggestions, track changes, version recovery | [reviewing.md](references/reviewing.md) + `docx:editing` / `pptx:editing` sections |
| Writing any message to the Enduser (reports, questions, failures) | [enduser-output.md](references/enduser-output.md) |
| Enduser reports a problem for the developer ("report the problem…", complaint about a failed office task) | [reporting.md](references/reporting.md) |
| Fillable PDF forms | [pdf/forms.md](../pdf/forms.md) + `scripts/check_fillable_fields.py` |
| XLSX recalc / financial model | [xlsx SKILL](../xlsx/SKILL.md) `recalc.py` section |
