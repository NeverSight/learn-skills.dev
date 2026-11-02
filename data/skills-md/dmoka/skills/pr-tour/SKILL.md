---
name: pr-tour
description: "Review one PR as a guided tour, in a sane reading order. Turn one pull request into a guided reading tour — the author's intent, which files that intent explains and which it does not, and checkable claims first, then where to look and why (script-computed facts plus line-checked pointers), then the files in the order a reviewer should read them with each test next to its code, and noise (lockfiles, generated files, renames, formatting) collapsed last — rendered as one self-contained HTML page plus JSON that agents can read. Not GitHub stacked PRs. Use when the user asks to review, walk through, explain, or understand a PR or diff, asks what to read first or what to worry about in a PR, or mentions PR tour or reading order."
---

# PR tour

A reviewer who reads a diff top to bottom reads it in alphabetical order —
the order Git prints it, not the order that explains it. Labelling code as
AI-written does not make people read it more carefully; changing what they
read first is the lever. This skill changes it: WHY first, the files that
matter next, noise last.

The tour points attention. It never judges. It gives no merge verdict and no
security verdict, and "collapsed" means low reading value, never "checked".
It serves humans (the HTML) and agents (the JSON) with the same content — an
adversarial reviewer can start from its high-severity items.

Scripts sit in `scripts/` beside this file (Node ≥ 18, zero dependencies,
`gh` logged in). If you fetched this over HTTP, fetch `scripts/*.mjs` and
[references/config.md](references/config.md) as raw text with `curl -sSL`.

## The loop

0. **Start clean.** Run the tour in a fresh session, never in the one that
   wrote the diff. An author cannot point at its own blind spots.
1. **Compute.** `node scripts/tour.mjs <pr-number>` (add `--repo owner/name`
   outside the repo; `--git main...feat/x` before a PR exists; `--spec
   <path>` when the spec or review contract lives elsewhere; `--out <dir>` to
   change the output folder). It writes `.pr-review/tour-<n>.json` — `<n>` is
   the PR number, or the branch name in `--git` mode — with FACT items,
   per-file classification, a reading order, and the author's words from
   every source it finds, strongest first: a spec (a markdown file in
   `docs/`, `specs/`, `.scratch/` or `contracts/` whose name contains the
   branch name), the PR description, linked issues and `#123` refs in
   commits, the commit messages, the title. Intent status is `spec`,
   `described`, `title only`, or `UNKNOWN`. It collapses noise last:
   lockfiles, renames, formatting, and generated files (ORM snapshots,
   minified bundles, large machine-written JSON, files with a generated
   header; the full list is in [references/config.md](references/config.md#built-in-defaults)).
   Noise is never an ASK WHY file. It prints the noise line count.
   An empty diff stops here with an error.
2. **Read** the diff in the reading order (`gh pr diff <n>` or `git diff`),
   noise included — skim it, it is collapsed for humans, not for you. Read
   surrounding source **at the PR head**, without checking it out (others
   may share the checkout): `git fetch origin <head>` then `git show
   "origin/<head>:<path>"` (quoted: zsh reads `:a` and `:s` as modifiers). Other open PRs that touch the same code are fair
   game: a change that breaks another open PR is a medium item.
3. **Write the WHY** to `.pr-review/tour-<n>.notes.json`. The full format,
   a worked example, and the severity rubric are in
   [references/notes.md](references/notes.md). In short:
   - `attention` — optional here, required when `pr-triage` runs you: how
     much attention the PR needs (`critical` / `high` / `medium` / `low`),
     what happened, why, and the line that drives it. Shown as a badge at
     the top of the tour.
   - `whatItDoes` — one or two sentences on what the diff actually does,
     shown as the model's reading, never as the author's intent.
   - `why`, `points`, `shape`, `diagrams`, `chapters` — the author's reason
     (quoted), a 3–5 line overview with keyword links, 1–3 structure views,
     0–2 Mermaid diagrams where flow or structure changes, and the
     walkthrough grouped into chapters. All optional; see the reference.
   - `explains` — **the intent map**: each thing the author says the PR
     does, quoted verbatim, with the code files that implement it. Leave out
     a file nothing explains — the gate lists it as ASK WHY, and that list is
     the most useful thing the tour shows.
   - `claims` — checkable promises the author makes ("no change to
     guest checkout"), quoted verbatim, each pointed at the line to check.
   - `items` — at most eight LOOK HERE pointers, each with `severity`,
     `file`, `line`, a verbatim `code` fragment of that line, `title`, `why`.
     Phrase each as what to check, never as a conclusion. Skip what CI
     already catches.
   - `fileNotes` — per non-noise file: a **bold takeaway**, then 2–5 bullets.
4. **Gate.** `node scripts/annotate.mjs <tour.json> <notes.json>`. It
   rejects a quote that is not verbatim in the author's text, a pointer whose
   line does not contain its `code`, a noise file in the intent map, more
   than eight items, and verdict words. It then derives the unexplained files
   and the unmatched quotes, and recomputes the reading order. Fix the notes,
   never the check; rerunning is safe.
5. **Render.** `node scripts/render.mjs <tour.json>` writes the `.html` next
   to it: one file with the viewer and the data inside, no server, safe to
   publish as a CI artifact. Look at it
   before you report — in a browser if you have one (serve the folder with
   `python3 -m http.server -d .pr-review` when `file://` is blocked), or at least confirm
   the WHY panel text in the JSON reads right.
6. **Report** in chat: the HTML path, the intent status, the unexplained
   files, the high items with `file:line`, and the noise line count.

## Hard rules

- **Point, never judge.** No "LGTM", "looks safe", "approve", "exploitable",
  "no issues", "nothing to review". The gate rejects the common phrasings;
  do not reword around it.
- **Never invent intent.** Only the author's words are intent. Your summary
  goes in `whatItDoes`, where it is labelled as yours. Do not stretch a quote
  to cover a file so the ASK WHY list looks clean — an unexplained file is a
  finding, not a failure.
- **Facts come from the script.** Do not restate a FACT item as your own, and
  do not dismiss one — if a FACT is harmless in context, say why in an item
  or file note and let the reviewer decide.
- **Read-only.** Never comment on, approve, or change the PR, and never edit
  code. The output is two files in `.pr-review/`.

## What the tour cannot see

- **Whether the code works.** Run it; the tour does not.
- **Vulnerabilities.** It asks about missing security decisions. It is not a
  scanner — run a real one (Trivy, opengrep) in CI.
- **Noise that is not harmless.** A lockfile can carry a malicious package; a
  "formatting only" file is detected by a heuristic. Collapsed files stay one
  click away and are listed with their reason.
- **Tests outside the diff.** "No changed test shares its name" does not mean
  no test covers the file.

## For agents reading the JSON

`intent.status` and `unexplained[]` give the big picture: what the author
said, and which changed files nothing they said accounts for. `explains[]`
maps quotes to files; `unmatched[]` lists quotes with no matching change.
`items[]` holds every pointer: `source` (`fact` = script, `model` =
line-checked, `map` = unexplained file), `severity`, `file`, `line`, `side`, `text`, `why`. `order[]` is
the reading order with a `why` per position; `files[]` holds the hunks. Start
from `severity: "high"`. `intent.status: "UNKNOWN"` means there is no spec to
review against — say so instead of guessing one. Schema:
[references/config.md](references/config.md#report-json).

## Done means

- `tour-<n>.json` passed `annotate.mjs` and `tour-<n>.html` exists.
- Every LOOK HERE item points at a real line of the diff, and every claim is
  a verbatim quote.
- The chat report names the intent status, the unexplained files, and the
  high items.

The intent search order and the fresh-session rule are adapted from Matt
Pocock's [`code-review`](https://github.com/mattpocock/skills) skill (MIT).

Last verified: 2026-09-25 with Claude Code (shipped in dmoka/skills #1)
