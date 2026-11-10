---
name: venue-fork
description: "Fork an existing paper into a concurrent second-venue submission variant with policy checks, separate Overleaf ownership, format conversion, budget refit, QA, and Atlas/Vault writeback. Use when submitting the same work concurrently to another permitted venue. Not for preprints, ordinary retargeting, or camera-ready work."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - WebFetch
  - AskUserQuestion
---

# Venue Fork: Second-Venue Submission Variant

Fork a paper for a second venue while the original submission keeps living. A fork is a **copy**
(both venues track independently), unlike `retarget-journal` (a move) and `preprint` (a
non-archival variant that must NOT get a vault submission entry).

## When to Use

- A venue window explicitly permits concurrent submission (e.g. WINE 2026 ⟷ FOCS/SAGT/AFT 2026)
- A rejected paper needs a reformatted version for a differently-formatted venue
- the user says "submit this also to X", "concurrent submission to X", "make the X version"

## Phase 0 — CFP compliance sheet (blocks everything)

Fetch the **official CFP** (never WikiCFP alone; `mark-unverified` applies) and record:

| Item | Why it matters |
|---|---|
| Page limit + what's excluded (title page? references? appendix policy) | Drives the refit budget in Phase 3 |
| Font size / margins / class requirements | Submission format is often looser than camera-ready (e.g. WINE: ≥11pt, ≥1in, any class; LNCS only at camera-ready) |
| Blind policy | Anonymity QA in Phase 4; third-person self-citation per `double-blind-self-citation` rule |
| **Concurrent policy — on BOTH sides** | The target naming the source venue is not enough; verify the source venue's CFP reciprocates |
| Deadlines: submission, rebuttal, **notification** | Also the SOURCE venue's notification date |

**Timing analysis (report to the user):** if the source venue notifies before the target's
rebuttal/notification, acceptance there forces withdrawal from the target *before any reviews
arrive* — the fork is then insurance + comments-on-rejection, not guaranteed feedback. Say so
explicitly before doing the work.

## Phase 1 — Create the fork

1. New Overleaf project via Dropbox (the active client may create these — folder + main.tex = project):
   `Apps/Overleaf/Paper {Theme} {Short Name} ({VENUE} {YY})/` — Title Case, venue suffix, per
   the existing naming convention. Resolve the Dropbox root per `multi-machine.md`.
2. Copy from the source project: `main.tex`, the bib, figure dirs, any `.bst` the target format
   needs. **Never edit the source project's files** — it is a live submission surface.
   Copy **files by name only** — never `cp -r` a whole template/source dir into the new Overleaf
   folder, which would drag a `.git` in and make it a repo on the wrong remote. Confirm
   `find <new-overleaf-folder> -name .git` is empty. See `.claude/rules/template-scaffold-strip-git.md`.
3. Project dir: `mkdir <project>/paper-{venue}/` + **relative** symlink
   `paper-{venue}/paper → ../../../../../Apps/Overleaf/<name>` (absolute symlinks break
   cross-machine).

## Phase 2 — Document-class conversion

Target submission formats like WINE's are satisfied by plain `\documentclass[11pt,a4paper]{article}`
+ `\usepackage[margin=1in]{geometry}`. Conversion map:

| Source class | Strip | Replace with |
|---|---|---|
| `lipics-v2021` | `\Copyright`, `\ccsdesc`, `\category`, `\relatedversion`, `\supplement`, `\funding`, `\acknowledgements`, all `\Event*`/`\SeriesVolume`/`\ArticleNo`, `\titlerunning`/`\authorrunning`, 5-arg `\author{}{}{}{}{}` | article `\title` + `\author{Anonymous submission}` + `\date{}`; keywords as a `\noindent\textbf{Keywords:}` line inside the abstract |
| `llncs` | `\titlerunning`, `\institute`, `\spnewtheorem` defs, LNCS author-suppression hacks | amsthm with explicit `\newtheorem` for every env the body uses (`theorem`, `lemma`, `proposition`, `corollary`, `definition`, `example`, `remark`, `observation`, `claim`); `proof` comes from amsthm — do NOT redefine. `\keywords` shim: `\newcommand{\keywords}[1]{\par\medskip\noindent{\bfseries Keywords:} {\def\and{\unskip{} $\cdot$ }#1}}` |
| `acmart` | `\ccsdesc`, `\keywords`, `\copyright*`, `\settopmatter`, `\authornote` | as above |

- Grep the body first: `grep -o '\\begin{[a-z]*}' main.tex | sort | uniq -c` tells you exactly
  which theorem environments to define — the AFT paper needed none, the SAGT paper needed nine.
- `cleveref`: load `hyperref` then `\usepackage[capitalise,noabbrev]{cleveref}` when the body
  uses `\cref`/`\Cref` (LIPIcs loads it via class option).
- `.bst` files: `plainurl.bst` ships with TeX Live (urlbst); `splncs04.bst` must be copied into
  the fork. Check with `kpsewhich <name>.bst` before assuming.

**Shared math core.** A class conversion is a legitimate adoption window for
`user-math.sty` (`templates/venues/_shared/`): copy it in, load it AFTER the
new class, and delete the preamble's now-duplicate `\newcommand{\E}`-style
lines — it supplies the macro set, operators, delimiters, and theorem
environments clash-safely (`[notheorems]` when the kit owns them). Papers not
being converted are NOT retrofitted (`templates/venues/_shared/README.md`;
candidates: `docs/reference/user-math-adoption-candidates.md`).


## Phase 3 — Page-budget refit (relocate, never cut)

1. Compile; find where the body ends: `pdftotext -f N -l N main.pdf -` per page around the
   expected boundary — locate the References header page.
2. Compute overrun against the CFP budget (mind what's excluded: title page/references usually
   don't count; an 18pp LNCS body ≈ 12–13pp at 11pt/1in — LNCS text block is ~40% smaller).
3. Relocate in this order until the body fits, adding `\appendix` sections with pointer lines
   (`\noindent\emph{The proof appears in Appendix~\ref{...}.}`):
   1. Detail subsections readers can defer (experimental-design grids, implementation details)
   2. Large floats (tables/figures) — `\cref` keeps resolving when labels move with the float
   3. Longest proofs → "Omitted Proofs" appendix, re-titled `\begin{proof}[Proof of Theorem~\ref{...}]`
   4. Whole peripheral sections (motivating applications, extended demarcation)
4. **Never cut prose to fit** — relocation only (`manuscript-edit-budget` rule). Update any
   in-text `Section~\ref` pointing at moved content to `Appendix~\ref`.

## Phase 4 — QA gates (all must pass)

- `latexmk -pdf` exit 0; `grep -c 'LaTeX Warning: Reference\|Warning: Citation' main.log` → 0.
- Body-end page ≤ budget (re-run the Phase 3 boundary check — floats move on recompile).
- Anonymity grep on the tex: author surname, first name, all affiliated institutions,
  `acknowledg`, `our prior`, `we showed`, `in earlier work`. Then eyeball p1 of the PDF.
- **Render-level check** (compile logs cannot catch wrong-symbol output): `pdftotext` the PDF and
  grep for symbols that should/shouldn't appear — especially after any macro rename (see Gotchas).

## Phase 5 — Submission + writeback (after the user submits)

Multi-system completeness — all of these, then verify:

1. **Vault submission file** `submissions/<topic>-<venue>-<year>.md`: `status: Submitted`,
   `submitted_date`, and exactly one attention date: **`notification_date`** for a real CFP
   decision date or **`follow_up_date`** for an operational journal check-in. Set conference
   dates, `double_blind`,
   `paper_id`, and a body **concurrency clause**: which venue notifies first and the withdrawal
   obligation. Link the primary submission entry.
2. **Atlas topic** `outputs[]`: new venue entry, `status: Submitted` (output-ladder canon only),
   same dates, notes carrying the concurrency clause, **and the full submission-join set** per
   `rules/atlas-status-vocabulary.md` § submission-join completeness: `paper_id` (same as the
   vault entry), `paper_title` (must equal the registry `canonical_title`), and — if the venue is
   a Conference/Workshop — `cycle: <Venue> <edition-year>` (journals exempt). (Do NOT bump
   `last_reviewed` — a venue swap is not topic-file curation; only `update-topic-file` writes
   that field.) Validate with `atlas-vault/schema.py`; `validate-portfolio-registry.py` catches
   any missed join as `cycle-gap`/`title-gap` at the next `session-close`.
   If the fork target has **no venue file** yet, create `~/vault/venues/<slug>.md` with
   canon-only ranking fields (`cabs`/`core`/`scimago`/`venue_type` from the fixed sets — lookup
   caveats go in `#` comments after a canon value, never in the value).
3. **Submitted-PDF archive**: verify the HotCRP/CMT-downloaded PDF page-matches the local build,
   file at `<project>/paper-{venue}/submitted-YYYY-MM-DD.pdf` (outside the Overleaf symlink),
   add a pointer line in the vault entry.
4. **Inbox**: `curl -X POST localhost:8765/api/sync` (Mac Mini) and confirm the notification item
   appears; mark the met submission-deadline item done.

## Gotchas (each cost real time on 2026-07-02)

- **Macro renames: `\b` does not fire before `_`.** `re.sub(r'\\cap\b', ...)` misses `\cap_j`
  (underscore is a word char) — and the un-renamed token still compiles, rendering the WRONG
  symbol silently. Use `(?![a-zA-Z])` as the boundary and pdftotext-verify the output.
- **Macro names:** `\newcommand{\cap_}` is invalid (redefines `\cap`); never end a macro name
  with `_`; check clashes with amssymb (`\Cap`) before choosing.
- **Missing bib looks fine in Overleaf** because a copied `.bbl` renders references anyway —
  check the file list, not the PDF, when confirming the fork is complete.
- **Paperpile CLI snapshot lag:** freshly imported refs miss in `get-item`/`lookup-by-doi` for a
  while; the app-side BibTeX export is the authoritative canonical-key source meanwhile.
- Merge adjacent `\cite{a}\cite{b}` → `\cite{a,b}` after batch key swaps.

## Anti-Patterns

- **Don't** edit or compile inside the source venue's Overleaf project — fork first, then touch.
- **Don't** cut prose to make the page budget — relocate to appendices.
- **Don't** create the vault submission entry for a preprint-server post — that's `preprint`'s
  domain and the `preprint-vs-submission` rule forbids it.
- **Don't** skip verifying the concurrent policy on the SOURCE venue's side.
- **Don't** report "ready" from compile success alone — run the render-level check.
- **Don't** hand-author bib entries — Paperpile-canonical keys only (`paperpile-citations` rule).

## Verification

The fork is done when: fork compiles clean at/under budget with 0 warnings; anonymity + render
checks pass; source project untouched (`ls -lt` mtimes); after submission, vault + atlas agree
(`Submitted`, same dates), schema validates, the inbox shows the notification or follow-up item, and the
submitted-PDF archive is filed with a pointer.
