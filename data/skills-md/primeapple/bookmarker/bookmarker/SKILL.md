---
name: bookmarker
description: >
  Use when the user refers to a non-exact directory, repository, or bookmark
  that is not the current relevant location, including an unfamiliar named
  location or a request to go there. Do not use for an exact path: use it
  directly, and ask the user if it is missing without trying `bm`.
---

# Bookmarker

Use this skill for a non-exact location only. First decide whether the current
working directory already fits the user's request. Stay there when it does.

When another location is needed:

1. Set `LOCATION` to the user's named location. Run `bm get LOCATION`.
2. Use the result when `bm get LOCATION` returns exactly one path.
3. Otherwise run `bm list --porcelain`. Each record is
   `bookmark<TAB>path`; the separator is a literal tab. Parse bookmark and
   path as separate fields so paths containing spaces remain intact.
4. Rank fallback matches in this order:
   - exact bookmark name;
   - exact path basename;
   - `LOCATION` as a path component;
   - a contextually related bookmark name.

   Prefer basename matches over path-component matches. For example, `foo`
   selects `/Users/toni/foo` over `/Users/toni/src/foo/design-system`.
   For related names, use the task's meaning: `backend-repo` is more relevant
   to backend work than `frontend-for-backend`. Do not choose by substring
   matching alone.
5. If one path is clearly the best match, select it. If multiple paths remain
   plausible, inspect each for task relevance. Check its directory, repository
   status and remote when applicable, and read `README.md` or `AGENTS.md` when
   present. Continue when one candidate is clearly relevant; otherwise show the
   candidates and ask the user to choose.
6. If no match exists, tell the user what was tried and ask for a bookmark name
   or path. Do not search the entire drive.
7. Run every following operation from the selected path. Set tool `cwd` when
   supported; otherwise use `cd -- "$path" && ...`.
8. Continue the user's task there. Do not merely report the path or ask the user
   to change directory.

Completion: the user's task runs from the selected relevant path. If selection
remains unclear, stop after showing candidates and asking the user.