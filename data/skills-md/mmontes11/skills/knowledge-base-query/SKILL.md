---
name: knowledge-base-query
description: >
  Answer questions about what the mmontes11/knowledge-base knows — a tracked project (what it is, its API
  surface, its latest release, its features, its architecture), a book in `books/`, or a foundational topic in
  `foundation/` — by reading the root README's index tables to locate the right folder and then reading the
  relevant file. Use whenever the user asks something the knowledge base could hold and wants the answer
  grounded in it — "what does <project> do", "what's the latest release of <project>", "how does
  <project>'s API work", "which projects does the knowledge base track", "what does the knowledge base say
  about <topic>", "summarize chapter N of <book>" — rather than from general knowledge.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.0"
compatibility: Requires a checkout of the knowledge-base repository (canonical path ~/code/knowledge-base). Read-only — this skill never modifies the knowledge base.
allowed-tools: Read, Glob, Grep
---

# Query the knowledge base

Read information from the knowledge base — projects, books, and foundational topics — and answer grounded in
it. The root `README.md` is the **index**: it maps names to folders, so start there and go straight to the
target. Do not read the whole repository; use the indexes to open only the file(s) the question needs.

## Locate the knowledge base

Work inside the knowledge-base repository. The canonical local checkout is `~/code/knowledge-base`; if it
is absent, `git clone git@github.com:mmontes11/knowledge-base.git ~/code/knowledge-base`. All paths below are
relative to the repository root.

## Step 0 — Find it in the index

The root `README.md` holds the indexes:

- **Tracked projects** table — maps each project to its `projects/<category>/<project>/` folder and its
  upstream URL.
- **Tracked books** table — maps each book to its `books/<book>/` folder.
- **Tracked foundational knowledge** table — maps each foundational topic to its `foundation/<topic>/` folder.

If the thing you were asked about is not in the index, say so — the knowledge base does not cover it — and
stop. If a Tracked projects row exists and further research would help, surface its upstream URL.

## Step 1 — Read the right file

Go straight to the file that answers the question:

| Question | Read |
| -------- | ---- |
| What is the project / what problem does it solve | `projects/<c>/<p>/README.md` |
| What is its API / resource / CLI surface | `projects/<c>/<p>/api-reference.md` |
| What is the latest release / what changed | `projects/<c>/<p>/releases.md` |
| What features does it have | `projects/<c>/<p>/features.md` |
| How is it architected | `projects/<c>/<p>/architecture.md` (only if present) |
| What a book teaches / a chapter's content | `books/<book>/README.md`, then `NN-<chapter>.md` |
| How a concept actually works | `foundation/<topic>/README.md` |

## Step 2 — Answer

- Answer **from the knowledge base**, citing the file you read and, where useful, its `last_updated`
  frontmatter so the reader knows how current it is.
- For projects the KB *links* rather than *copies* upstream. If the entry is thin or stale, say so and
  surface the upstream link from the Tracked projects table so the reader can verify.
- If the question spans several files (e.g. "give me the picture of <project>"), read `README.md` first, then
  pull in only the specific files the question needs.

## Scope

This skill is **read-only** — it never edits, adds, or removes knowledge-base content. Adding a project or a
book, and refreshing a project, belong to the `knowledge-base-add-project` and `knowledge-base-add-book`
skills.
