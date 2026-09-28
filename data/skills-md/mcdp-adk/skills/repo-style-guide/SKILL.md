---
name: repo-style-guide
description: Standardize names, wording, and links in Git and GitHub collaboration. Use when naming branches, creating or rewriting commits, pushing or merging changes, or creating, editing, or publishing issues, pull requests, and comments.
---

# Repository Style Guide

Follow the user's explicit instructions for the task, then explicit project conventions and templates, then these defaults. Use English by default and reuse project terminology.

## Default style

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for ordinary change commits and for PR titles. Choose a lowercase type for the overall change and describe it in the title in imperative mood, without a trailing period. Include a scope when it helps locate the change, reusing names and granularity established for similar work. For new scopes, use project terminology in lowercase kebab-case.

Use natural language for issue titles, naming the problem or requested outcome.

Name branches `type/short-topic`, using the same change types and a short kebab-case topic that describes the branch's overall purpose. Use a required project or tool prefix in place of the default type prefix.

Keep one coherent intention per commit, including its supporting tests and docs.

## Content and references

Write for the current record's purpose and intended readers. Include the key facts needed to understand it without the private task conversation. Distinguish proposals from established decisions.

Use the applicable project or task template for the body. Organize supporting explanations in short paragraphs or lists. A commit needs an explanatory body only when its title leaves important rationale, behavior, or consequences unclear. Reuse earlier descriptions where they remain accurate and useful for the final record.

Use comments to add information needed to decide or continue the work.

Link accessible sources for supporting evidence, detailed discussion, and history rather than repeating their contents. Make relationships clear and use the appropriate syntax for references and metadata, avoiding duplicate references that convey the same relationship.

## Applying the conventions

Where a record's format carries operation semantics or is interpreted by tooling, retain that structure and apply these defaults to its descriptive text where compatible. Before recording or publishing names or text, check their final form for accuracy, necessary context, and conformity to the applicable conventions.

Local commits can proceed under the current task's instructions, with each message checked. Before publishing names or text whose later correction would require rewriting shared history or disrupt others' work, show the complete proposed text as it will be recorded and wait for confirmation. Include any body and footer in the preview. Group related items into one preview, including the full messages for a series of commits.

Previously approved text needs no further confirmation while it and the applicable conventions remain unchanged. Check new or changed text produced by later operations. If the user explicitly requests direct execution, check the text and proceed within that request.
