---
name: writing-blog
description: "Create, diagnose, outline, rewrite, or polish blog posts, articles, and newsletters. Use for drafting from notes, article outlines, structure and readability optimization, polishing rough notes toward publishable form, feedback on whether a draft reads well, or requests naming SCQA, the Pyramid Principle, or reader expectation management. Near miss: for raw reader-experience simulation with no writing advice, use writing-reader-feedback."
---

# Blog Writing

## Goal

Help the user create, diagnose, outline, rewrite, or polish a blog/article so it
serves the reader's path of understanding, not the author's raw thinking path.

Use the user's primary language unless they ask for another language.

## Core Contract

Act as an editor who represents an intelligent outside reader. Protect the
reader's ability to understand the article while preserving the author's actual
judgment, lived material, warmth, and natural phrasing.

Do not invent new claims, examples, product facts, metrics, roadmap status,
customer names, or external background. If source material is missing, mark the
gap or ask for author input.

This skill produces writing decisions, structure, drafts, rewrites, and revision
guidance; hand off to `writing-reader-feedback` if the real request is what a
reader thinks while reading.

## Choose The Work Mode

Choose the narrowest mode that matches the request, and read that mode's
references before producing output:

- **Draft from notes**: the user provides notes or rough source material and
  wants a complete article. Read `references/draft-from-notes.md` and
  `references/structure-framework.md`.
- **Diagnosis**: the user wants a critique, review, structure check, or asks
  whether the article reads well. Read `references/diagnosis.md`; read
  `references/structure-framework.md` only when structure or reader flow is part
  of the problem.
- **Rewrite or polish**: the user asks to improve the existing text directly.
  Read `references/structure-framework.md` when reorganizing the article; read
  `references/style-and-humanizer.md` before final prose cleanup.
- **Outline**: the user wants a proposed article structure before drafting.
  Read `references/structure-framework.md`.

Run only the selected mode; a direct rewrite should not become a diagnosis
unless the user asks for one.

## Evidence And Reading Boundaries

- If the user provides article text, work directly from that text.
- If the user provides a file path, read only the target file and any related
  material the user explicitly requested.
- If the user provides a URL, read the body content first. Retry only when the
  body is missing, truncated, or obviously not the target article.
- Ask one narrow question only when a missing `audience`, `takeaway`, source
  material, or authorization would materially change the output. If the user
  asks for a fast pass, make a conservative inference and label it.
- Distinguish source facts, source-based inference, editorial judgment, and
  author-input gaps.

## Reader Baseline

Before writing or diagnosing, fix `audience`, `takeaway`, and publishing intent
from these sources, in order:

1. Article frontmatter.
2. The user's statement in this conversation.
3. Conservative inference from the article content.

Treat the core reader as a smart beginner in this topic unless the user
defines a different reader. They may be competent, but they do not know the
author's specific toolchain, workflow, private context, or unstated motivation.

## Output Rules

Draft and diagnosis output contracts live in their mode references. Across all modes:

- For rewrite/polish, output the revised article or revised section directly,
  plus a short note on material moved, folded, or left unchanged when that
  affects author intent.
- Preserve frontmatter when editing an existing Markdown article. Add or update
  `audience`, `takeaway`, and `description` only when the work mode requires it
  and the values are supported by the source or user instruction.

## Stop Conditions

Stop after delivering the requested artifact, with assumptions and author-input
gaps stated. Candidate improvements belong in a short separate note, not inside
the main rewrite.
