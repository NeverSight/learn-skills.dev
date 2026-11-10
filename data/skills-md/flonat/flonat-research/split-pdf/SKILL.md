---
name: split-pdf
description: "Download, split, and deeply read an academic PDF that is not available through Paperpile. Use when a long external PDF needs page-wise ingestion. For Paperpile items, use the Paperpile text-extraction route instead."
allowed-tools: Bash(uv:*), Bash(uv*), Bash(curl*), Bash(wget*), Bash(mkdir*), Bash(ls*), Bash(rm*), Read, Write, Edit, WebSearch, WebFetch, Agent, Bash(paperpile*)
argument-hint: "[pdf-path-or-search-query]"
---

# Split-PDF: Download, Split, and Deep-Read Academic Papers

**CRITICAL RULE: Never read a full PDF. Never.** Only read the 4-page split files, and only 3 splits at a time (~12 pages). Reading a full PDF will either crash the session with an unrecoverable "prompt too long" error — destroying all context — or produce shallow, hallucinated output. There are no exceptions.

## When This Skill Is Invoked

The user wants you to read, review, or summarize an academic paper. The input is either:
- A file path to a local PDF (e.g., `./articles/smith_2024.pdf`)
- A search query or paper title (e.g., `"Gentzkow Shapiro Sinkinson 2014 competition newspapers"`)

**Important:** You cannot search for a paper you don't know exists. The user MUST provide either a file path or a specific search query. If the user invokes this skill without specifying what paper to read, ask them. Do not guess.

**Prefer Paperpile when possible.** If the paper is in Paperpile, call `paperpile get-pdf-text(citekey=KEY)` directly — you get the full structured text without any splitting. Only fall through to this skill's page-split workflow when the PDF is NOT in Paperpile (preprints, referee materials, ad-hoc reading, third-party shared PDFs).

## Step 1: Acquire the PDF

**If a local file path is provided:**
- Verify the file exists
- **Use the PDF in place** — do not move or copy it. The folder containing the PDF becomes the working directory for splits and extracts.
- If downstream work will cite page numbers, run the read-integrity preflight first (`pdf-extract <file> --preflight`) — a non-PASS verdict means page indices from this file are untrustworthy (truncated or silently repaired document).
- Proceed to Step 2

**If a search query or paper title is provided:**

Determine the download directory:
- **Inside a research project** (has `CLAUDE.md`, `data/`, `paper/`, etc.): use `./articles/` in the project directory (create if needed).
- **Outside a project** (e.g., ad-hoc reading from Task Management root): use `to-sort/downloads/` in the Task Management folder.

Then:
1. Use web search to find the paper
2. If web search does not yield a direct PDF link, use a separately installed
   scholarly CLI when available (for example,
   `scholarly scholarly-search "paper title" --json`). Otherwise search the
   publisher, DOI landing page, arXiv, or an institutional repository directly.
3. Use web fetch or Bash (curl/wget) to download the PDF
4. Save it to the download directory
5. Proceed to Step 2

**CRITICAL: Always preserve the original PDF.** The source PDF must NEVER be deleted, moved, or overwritten at any point in this workflow. The split files are derivatives; the original is the permanent artifact. Do not clean up, do not remove, do not tidy.

## Step 2: Check for Cached Extract, then Split

**First, check for an existing extract.** Look for `<basename>_text.md` in the same folder as the PDF.

If found, ask:
> "An extract from a previous deep-read exists (`<basename>_text.md`). Use it for this request, or re-read the PDF from scratch?"
- **Use extract**: read `<basename>_text.md` and use it as the source notes — skip the rest of Steps 2 and 3 entirely.
- **Re-read**: proceed with splitting below.

This prevents redundant re-reading of papers you have already processed. The `_text.md` file is a structured plain-text extraction far cheaper to read than re-processing PDF page images.

**Second, check for existing splits.** Compute the build directory:

```python
import os
folder_path  = os.path.dirname(os.path.abspath(pdf_path))
foldername   = os.path.basename(folder_path)
pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]
build_dir    = os.path.join(folder_path, foldername + '_build')
split_dir    = os.path.join(build_dir, 'split_' + pdf_basename)
```

If `split_dir` already exists and contains `.pdf` files, ask:
> "Splits already exist for `<pdf-basename>` (N chunks in `<foldername>_build/split_<pdf-basename>/`). Reuse existing splits, or re-split from scratch?"
- **Reuse**: skip splitting, proceed to Step 3 using the existing files in `split_dir`.
- **Re-split**: delete the existing split folder, then split.

**Otherwise, split.** Create `<foldername>_build/split_<pdf-basename>/` and run:

```python
from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_path, output_dir, pages_per_chunk=4):
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(input_path)
    total = len(reader.pages)
    prefix = os.path.splitext(os.path.basename(input_path))[0]

    for start in range(0, total, pages_per_chunk):
        end = min(start + pages_per_chunk, total)
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])

        out_name = f"{prefix}_pp{start+1}-{end}.pdf"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "wb") as f:
            writer.write(f)

    print(f"Split {total} pages into {-(-total // pages_per_chunk)} chunks in {output_dir}")
```

If PyPDF2 is not installed: `uv pip install PyPDF2`.

**Directory convention:**
```
articles/                             # any folder containing a PDF
├── smith_2024.pdf                    # original — NEVER DELETE
├── smith_2024_text.md                # persistent extract — created after deep-read
└── articles_build/                   # <foldername>_build/ — shared build folder
    └── split_smith_2024/             # split_<pdf-basename>/
        ├── smith_2024_pp1-4.pdf
        ├── smith_2024_pp5-8.pdf
        ├── smith_2024_pp9-12.pdf
        ├── notes.md                  # working copy — source for _text.md
        └── ...
```

The build directory (`<foldername>_build/`) keeps split artifacts separate from source material and finished outputs. Multiple PDFs in the same folder share one build directory, each with its own `split_<basename>/` subdirectory.

## Step 3: Read in Batches of 3 Splits

Read **exactly 3 split files at a time** (~12 pages). After each batch:

1. **Read** the 3 split PDFs using the active client's PDF-reading surface
2. **Update** the running notes file (`notes.md` in the split subdirectory)
3. **Pause** and tell the user:

> "I have finished reading splits [X-Y] and updated the notes. I have [N] more splits remaining. Would you like me to continue with the next 3?"

4. **Wait** for the user to confirm before reading the next batch.

Do NOT read ahead. Do NOT read all splits at once. The pause-and-confirm protocol is mandatory.

## Step 4: Structured Extraction (8 dimensions)

As you read, collect information along these dimensions and write them into `notes.md`:

1. **Research question** — What is the paper asking and why does it matter?
2. **Audience** — Which sub-community of researchers cares about this?
3. **Method** — How do they answer the question? What is the identification strategy?
4. **Data** — What data? Where from? Unit of observation? Sample size? Time period?
5. **Statistical methods** — What econometric/statistical techniques? Key specifications?
6. **Findings** — Main results? Key coefficient estimates and standard errors?
7. **Contributions** — What's learned that we didn't know before?
8. **Replication feasibility** — Public data? Replication archive? Data appendix? URLs?

These extract what a researcher needs to **build on or replicate** the work.

## Step 5: Persist the Extract

**After all batches are complete**, write the final notes to `<basename>_text.md` in the same folder as the source PDF:

```
articles/smith_2024_text.md
```

Then notify the user:
> "Extract saved to `smith_2024_text.md` alongside the source PDF. Future requests on this paper can reuse it without re-reading."

This file is the persistent, reusable artifact. The `notes.md` in the build directory is the working copy. Both are kept — never delete either.

## Structured Mode (Paperpile)

If the paper IS in Paperpile (user provides a citekey), skip the page-split workflow entirely:

1. `paperpile get-item KEY --json` — title, authors, abstract, affiliations
2. `paperpile get-pdf-text KEY --json` — full text from the attached PDF

Write the 8-dimension extraction directly to `<basename>_text.md` in the working directory. No splits needed.

**This skill's page-split workflow is for PDFs NOT in Paperpile.**

## Agent Isolation Protocol

**When split-pdf is invoked by another skill or workflow** (any process that continues working after the PDF has been read), the PDF reading MUST run inside a subagent to prevent context bloat in the parent conversation.

**Why:** Each PDF page rendered by a client's PDF-reading capability produces image data in the conversation context. A 35-page PDF (9 chunks) can add 10-20MB of image data that accumulates permanently. After reading one or two large PDFs on top of prior work, the conversation can hit its request-size limit and become unrecoverable.

**Pattern:** The parent skill handles splitting (Step 2's Python script) in its own context — this is lightweight. Then it launches an Agent to perform all the reading:

```
Read PDF split files and produce structured extraction notes.

Split directory: <split_dir>
Files (read in this order, 3 at a time): <file_list>
Notes output:    <notes_path>  (working copy in split_dir)
Text output:     <text_path>   (persistent <basename>_text.md)

Process:
1. Read 3 PDF files at a time using the active client's PDF-reading surface
2. After each batch, update notes.md with extracted content
3. Extract along the 8 dimensions (research question, audience, method,
   data, statistical methods, findings, contributions, replication feasibility)
4. Write the final structured extraction to <text_path>

Report when done: pages read, figures/tables found, one-sentence content summary.
```

After the agent returns, the parent reads the output files (plain markdown, not PDF images) and continues its workflow.

**Standalone invocations** (user calls `split-pdf` directly) use the interactive protocol above with reads in the main conversation and the pause-and-confirm protocol.

## When NOT to Split

- Papers shorter than ~15 pages: read directly with the PDF-reading surface, not a shell text dump
- Policy briefs or non-technical documents: a rough summary is fine
- Triage only: read just the first split (pages 1-4) for abstract and introduction
- Paperpile items: use `paperpile get-pdf-text` directly

## Quick Reference

| Step | Action |
|------|--------|
| **Acquire** | Use local PDF in place, or download to `./articles/` (in-project) / `to-sort/downloads/` (ad-hoc) |
| **Check cache** | `<basename>_text.md` or existing splits — offer to reuse |
| **Split** | 4-page chunks into `<foldername>_build/split_<pdf-basename>/` |
| **Read** | 3 splits at a time, pause after each batch |
| **Notes** | Update `notes.md` with 8-dimension extraction |
| **Persist** | Save final extract to `<basename>_text.md` alongside source PDF |
| **Confirm** | Ask user before continuing to next batch |

## Acknowledgments

The in-place PDF handling, persistent `_text.md` extraction, split reuse, build directory convention, and agent isolation protocol are adapted from Scott Cunningham's [MixtapeTools](https://github.com/scunning1975/mixtape-tools) split-pdf skill (April 2026), which itself incorporated improvements from [Ben Bentzin](https://www.mccombs.utexas.edu) (McCombs School of Business, UT Austin). Structured Paperpile mode is the user's addition.
