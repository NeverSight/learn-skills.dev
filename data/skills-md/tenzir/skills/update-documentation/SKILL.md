---
name: update-documentation
description: >-
  Coordinate docs.tenzir.com updates alongside code changes. Use when preparing
  the `.docs/` checkout, creating a matching docs branch, opening a
  `tenzir/docs` pull request, or cross-linking docs and code PRs. Also use when
  the user mentions "update the docs", "docs PR", ".docs/", or when a code
  change affects user-facing behavior that should be reflected on
  docs.tenzir.com.
metadata:
  requires:
    skills:
      - technical-writing
---

# Update Documentation

Handle the operational workflow around docs.tenzir.com changes.

## Workflow

1. Ensure `.docs/` exists and is up to date by cloning `tenzir/docs` or
   fetching from `origin`.
2. Create or check out a topic branch in `.docs/` that matches the parent repo
   branch name.
3. Author the content update in `.docs/` using the docs repository's own
   documentation guidance and conventions.
4. Run relevant documentation checks if the docs repository provides them.
5. File a `tenzir/docs` pull request from `.docs/`.
6. Cross-link the pull requests (see also the `create-pull-requests` skill for
   the code-side PR workflow):
   - In the docs PR, add a `Functional PRs` section linking the main PR.
   - In the main PR, add a `Documentation PR` section linking the docs PR.
7. Summarize what changed and note any follow-up work.

## Branching

Keep the `.docs/` branch name aligned with the code branch whenever possible.
If the code change spans multiple repositories, use the code branch as the
source of truth for naming and cross-links.

## Cross-Checks

Before opening the docs PR:

1. Confirm the changed pages still fit their Diataxis section.
2. Check nearby pages and "See also" links for follow-on edits.
3. Ensure code samples, paths, and UI labels match the current product
   behavior.
