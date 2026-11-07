---
name: knowledge-base-add-book
description: >
  Add a new book to the mmontes11/knowledge-base `books/` section: create the book-shaped entry
  (entry README, one numbered file per chapter, the source PDF), summarize each chapter faithfully and
  attribute it, add mermaid diagrams where they clarify a mechanism, and register the book in the root
  README's Tracked books table. Use whenever the user wants to add, create, or import a book into the
  knowledge base — "add this book to the knowledge base", "summarize <book> for the KB", "create a books/
  entry for <title>", "work through chapter N of <book>" — even if they don't say "knowledge base"
  explicitly.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.0"
compatibility: Requires a checkout of the knowledge-base repository (canonical path ~/code/knowledge-base) and, for diagrams, the mermaid-render wrapper (pre-installed in the docker-opencode image).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(mermaid-render:*), Bash(mmdc:*)
---

# Add a book to the knowledge base

Add a published technical book to the `books/` section as a faithful, chapter-by-chapter study. The root
`README.md` of the knowledge base is the contract — it holds the layout, the section rules, and the index
tables. This skill is the *workflow* for adding a book. It does not restate the book's writing conventions:
those live in `books/README.md` (the section's own authority on the mandatory structure and style), which
you read first.

## Locate the knowledge base

Work inside the knowledge-base repository. The canonical local checkout is `~/code/knowledge-base`; if it
is absent, `git clone git@github.com:mmontes11/knowledge-base.git ~/code/knowledge-base`. All paths below are
relative to the repository root.

## Step 0 — Read the section rules

Read `books/README.md` before writing anything. It defines the mandatory book-shaped structure, the
Table-of-contents tracking rule, and the writing conventions (summarize and attribute — never copy the book
wholesale; diagrams encouraged). Follow it exactly.

## Step 1 — Establish the entry

1. Choose the **book slug**: the title in lowercase, kebab-case (e.g. *Build a Large Language Model (From
   Scratch)* → `build-a-large-language-model-from-scratch`).
2. Create `books/<book-slug>/`.
3. Place the source PDF in the entry as `book.pdf` — every chapter's claims must be verifiable against it.
4. Create the entry `README.md` with the fixed book facts and sections:
   - **Book facts** — title, author, publisher, year, ISBN, pages, language.
   - **Introduction** — what the book is and who it is for.
   - **Table of contents** — links to every chapter file and to any appendices. Appendices are sections of this
     `README.md`, not sibling files.
   - **Reference** — the source PDF and the publisher page.
5. Add the entry frontmatter — minimal, used only as a staleness signal; `upstream`, when present, is the
   publisher page (not a repository):
   ```yaml
   ---
   upstream: https://www.manning.com/books/<book>
   last_updated: <YYYY-MM-DD>
   ---
   ```

## Step 2 — Write the chapters

For each main chapter, in the book's reading order:

1. Create `NN-<chapter>.md` (zero-padded index, kebab-case title): frontmatter, the chapter title, a
   **Table of contents** of the book's own sections for that chapter, then the section content.
2. **Summarize and attribute** — restate the book's content in its own words, citing the book (author,
   chapter). Never reproduce the book's text, code listings, or figures beyond what the publisher's license
   permits for personal/study use.
3. Add a **mermaid diagram** wherever it makes a mechanism, flow, or data path obvious. Render each diagram
   before finishing to prove it is valid and legible:
   ```bash
   mermaid-render /tmp/d.mmd   # a clean, non-empty SVG/PNG means the block renders on GitHub
   ```
4. Keep the entry's **Table of contents** in lockstep: a chapter is linked the moment its file exists.

## Step 3 — Register the book

Add a row to the **Tracked books** table in the root `README.md` (columns: Book, Author, Source), linking to
`books/<book-slug>/README.md`. Books are project-agnostic and live at the repository root — never under
`projects/`, never in the Tracked projects table, and outside the monthly maintenance run.

## Step 4 — Deliver

- Commit with a conventional message: `docs(books/<book-slug>): <summary>` (e.g.
  `docs(books/build-a-large-language-model-from-scratch): summarize chapter 3 — attention`).
- Push directly to `main` — the knowledge base is maintained by direct push, not pull request.
- If a Multica issue drove this work, mark it done once the push lands.

## Constraints

- No credentials, tokens, or cluster-specific data — ever.
- One book is one canonical source; attribute every non-obvious claim to the book (collected in the entry's
  Reference).
- A chapter is done when it is readable top-to-bottom, attributed, diagrammed where it helps, and linked in
  the entry's Table of contents.
