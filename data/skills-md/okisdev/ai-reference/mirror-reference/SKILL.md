---
name: mirror-reference
description: Extract the load-bearing pattern from a reference URL, repository, or sibling path and re-express it in this codebase's own idiom with a deviation report, never cloning the reference.
argument-hint: "<url-or-path>... [target-area]"
---

## Context

Current branch and status: !`git branch --show-current; git status --short | head`

UI or primitives directories: !`find . -name node_modules -type d -prune -o -type d \( -iname ui -o -iname primitives \) -print 2>/dev/null | head -5 || echo "(none)"`

## Instructions

Study the reference until the pattern separates from its styling, implement the pattern in this repository's own primitives and conventions, and report where and why the result deviates from the reference.

### Process

1. Parse `$ARGUMENTS` (one or more references: a URL, an owner/repo, or a local sibling path; an optional target area names where in this codebase the pattern lands; with no arguments, infer both from the conversation instead).
2. Study each reference with the tool that matches its shape: a repository through `gh` (shallow clone or fetch files via the API) rather than scraping its rendered site, a docs or marketing page through a web fetch, a local sibling path by reading it directly. Identify the load-bearing pattern, the structure, API shape, interaction, or behavior that makes the reference work, and separate it from the reference's styling, naming, and tokens; the pattern transfers, the skin does not.
3. Read the target area's own idiom before writing: nearest siblings decide naming, placement, and import style, and the repository's own primitives and helpers are the building blocks. Compose `onboard-repo` first when the codebase is unfamiliar.
4. Implement the pattern expressed entirely in this repository's conventions and primitives. Search for an existing primitive before writing a new one; a new parallel implementation states what existing thing was rejected and why.
5. Write the deviation report as part of the result: where the implementation intentionally diverges from the reference and why (this repository's idiom, its constraints, its design system), where it matches, and which reference each adopted pattern came from when more than one reference was studied.
6. Verify with the repository's own checks; compose `verify-ui` for render evidence when the result is UI.

### Rules

- Never copy class strings, design tokens, colors, or naming verbatim from a reference; every borrowed pattern is re-expressed in this repository's own primitives.
- More than one reference means attribution per adopted pattern, not a blend nobody can trace.
- A reference the task says to study without implementing produces the pattern analysis and deviation notes only, with zero edits.
