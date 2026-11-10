---
name: camera-ready
description: "Convert an accepted anonymous-submission LaTeX paper (AAAI/AIES/ACM or Springer LNCS/LNAI) to camera-ready and implement the accepted reviews. Use when a paper is accepted with no rebuttal and you need to de-anonymize, add copyright, turn on section numbering, implement each reviewer's minor revisions, optionally move proofs to a non-counted appendix, and QA. Not for R&R/revise-and-resubmit (use strategic-revision --external) or for preprints (use preprint)."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(mkdir*)
  - Bash(cp*)
  - Bash(ls*)
  - Bash(grep*)
  - Bash(stat*)
  - Bash(latexmk*)
  - Bash(pdftotext*)
  - Bash(pdftoppm*)
  - Bash(mdls*)
  - Bash(uv run python*)
  - Bash(uv run --project*)
  - Bash(bash*)
  - Bash(shasum*)
  - Bash(cmp*)
  - Bash(unzip*)
  - Bash(git*)
  - AskUserQuestion
  - Task
skill-dependencies: [proofread]
---

# camera-ready: Accepted Paper → Camera-Ready + Review Implementation

For a paper that has been **accepted** (no rebuttal stage): produce the camera-ready version and implement the reviewers' (typically minor) revisions. Distinct from `strategic-revision --external`, which handles **R&R** (rebuttal, DAG, resubmission strategy).

## When to Use

- Acceptance notification arrived; reviews are final; you implement rather than argue.
- Triggers: "prepare the camera-ready", "implement the reviews for the accepted paper", "de-anonymize and finalize".

## Operating Rules (read first)

- **Overleaf-canonical**: edit the Overleaf/`paper/` symlink target, not any git mirror (`overleaf-canonical-source.md`). The `.tex` is a **live edit surface** — obey `reconcile-before-rewriting.md` (fresh-read, narrow edits, no `replace_all`/full-`Write`, mtime check).
- **Phased-work**: stop after each phase, summarize, await `continue` (`phased-work.md`) unless `--autonomous`.
- **mark-unverified**: never assert a reviewer-suggested citation/venue fact you haven't verified.
- **Status logging**: acceptance means the vault/atlas status *should* move to Accepted/camera-ready per `multi-system-completeness.md` — **but** if the formal decision letter hasn't landed yet (early prep), hold status changes until the user confirms. Once the camera-ready upload is confirmed (Phase 8), the Atlas output and the Vault submission move to `In Press`; the topic status stays `Accepted`.

## Phase 0 — Setup & verify
1. **File the venue correspondence** per `rules/submission-file-archive.md` (names are fixed; never dated or venue-ID names):
   - decision letter → `paper-{venue}/correspondence/editorial/{surface}-initial-decision.pdf` (+ optional parsed `.md`);
   - reviews → `paper-{venue}/correspondence/referee-reviews/{surface}-round1/{surface}-round1-reviews.pdf` (original) + `.md` (verbatim transcription with score table); a text extraction goes in that folder's `analysis/`.
   Never a project-root `correspondence/editorial/` or `correspondence/referee-reviews/`.
2. **Snapshot the pre-edit source** (`main.tex`, `.bib`, generated inputs, figures) → `paper-{venue}/submission/camera-ready/pre-edit-source-<YYYY-MM-DD>/` with a `SHA256SUMS`. Not `backup/`: that is hook-generated, git-ignored state. The frozen as-submitted PDF already lives in `submission/archive/<date>-initial/`.
3. **Verify reviewer-suggested citations** before adding any (DOI/title via `scholarly`/`paperpile`); reviewers often mis-spell/mis-date (e.g. "Edelmann 1996" → Suchman & Edelman 1996). Stash verified new entries.
4. **Build a reviewer-point → action table** so nothing is dropped; confirm scope with the user.
5. **Confirm the page-limit rule** (see Phase 3) — `[UNVERIFIED]` until checked against the CfP/acceptance email.

## Phase 1 — Camera-ready mechanics (low-risk)
- **De-anonymize**: replace `\author{Anonymous Submission}` with the real author/affiliation block.
- **Copyright**: AAAI auto-renders the slug from the style; set `\copyrightyear{<proceedings year>}`. ACM: set `\setcopyright`/`\acmConference`/DOI per the rights email. Never use `\nocopyright` for AAAI.
- **Section numbering**: AAAI submissions ship with `\setcounter{secnumdepth}{0}` → set to `2`. This also **fixes blank `Section~\ref{}`** references (a common reviewer complaint).
- Compile; confirm 0 undefined refs and the copyright slug renders on p1.

**Springer LNCS/LNAI** (`llncs` ≥ 2.2x): author line `Name\textsuperscript{(\Letter)}\orcidID{…}` for the corresponding author (load `marvosym`), `\authorrunning`, `\institute{…\\ \email{…}}`. End matter goes in a `credits` environment before the references: code/data availability, `\subsubsection{\ackname}` (funding with grant number), `\subsubsection{\discintname}` (Disclosure of Interests — mandatory, even if none), and any AI-use declaration the venue requires. Confirm against the venue's camera-ready instructions whether these count toward the page limit. The signed Licence to Publish is a separate upload.

## Phase 2 — Bibliography
- If adopting canonical (e.g. Paperpile) keys, invoke **`bib-rekey`** (DOI-safe remap + diff-verified `\cite` rewrite).
- Add the verified reviewer-suggested citations and any self-citations (camera-ready is de-anonymized, so self-cites are normal — use the **published** entry, not the arXiv preprint, when one exists).
- Compile; **0 undefined citations**.

## Phase 3 — Structure (appendix offload) — GATED on the page rule
- **First verify** whether the venue's page limit **excludes the technical appendix** (AAAI/AIES typically count body + figures; references and a post-references appendix are often exempt — confirm). This determines how aggressively to offload.
- If excluded: move full proofs / long derivations / worked-example arithmetic to `\appendix` after references; leave each result's **statement + a 3–5 sentence proof sketch + appendix pointer** in the body.
- **Equation-label coupling**: if a proof you are moving *defines* equations the body references, **lift those equations into the body** first (else body text points at appendix equation numbers). Verify 0 undefined after.

## Phase 4 — Reviewer revisions + intuition aids
- Implement each row of the Phase-0 action table.
- Common high-value additions for broad-audience venues: a **plain-language mechanics paragraph**, a **notation table**, a **results-at-a-glance table**, one-line **Reading** glosses, and a **mechanism figure/boxed causal chain** (covers "more visualization" and "more plain-language" asks at once).
- Apply any consistency fixes surfaced in Phase 0 (e.g. clamped first-best, index-vs-probability clarifications) — flag any that touch a theorem's math for author sign-off before editing.

## Phase 5 — QA
- `latexmk` clean (exit 0); **0 undefined** refs/citations; no large overfull boxes; no placeholders/TODOs.
- **Page-budget check**: locate where references/appendix begin (`pdftotext` + form-feed page count, or per-label pages from `.aux`); confirm **body ≤ limit** (appendix/refs exempt per Phase 3).
- **Visual render** key pages (`pdftoppm`) — de-anon header + copyright slug, new tables/figures, appendix.
- Run `proofread` scoped to the **new prose** only.
- **Token conservation vs the submitted version** — `uv run python .scripts/check_token_conservation.py --source backup/<submitted>.tex --revision <current>.tex` per edited file: every advisory row (changed number, dropped/added citation) must map to a Phase-0 action-table row or a Phase-3 appendix move. Spot-check reworded claims against the claim-strength ladder (`docs/reference/claim-strength-ladder.md`) — no silent strength moves between the reviewed version and camera-ready.
- **Arithmetic forensics** (empirical papers) — `uv run python .scripts/check_stat_forensics.py <main>.tex`: recomputed p-values, df-vs-N, t-vs-descriptives, GRIM. Any HARD finding gets resolved or explained before upload — reviewers approved the numbers as submitted; the camera-ready must not introduce (or ship) an arithmetic impossibility.

## Phase 6 — Package for upload

Work in `paper-{venue}/submission/camera-ready/`:

```
camera-ready/
├── build-package.sh                 # stages + verifies the upload package
├── pre-edit-source-<date>/          # Phase 0 snapshot
├── package/
│   ├── <venue><year>-paper<ID>-source/      # staged source tree
│   ├── <venue><year>-paper<ID>-source.zip
│   ├── <venue><year>-paper<ID>-camera-ready.pdf
│   └── SHA256SUMS
├── licence/<venue><year>-paper<ID>-licence-to-publish-filled.{docx,pdf}
└── zenodo/                          # only when Phase 7 runs
```

`build-package.sh` must: stage exactly the files the publisher needs (`main.tex`, `.bib`, the built `.bbl`, generated inputs, figures, class and style files); **fail if any placeholder remains** (`PENDING`, `TODO`, `\CiteTodo`, anonymous author block); compile the staged copy **in isolation**; check it against the canonical build (`cmp` the `.bbl`, diff `pdftotext` output); then write the zip, PDF and `SHA256SUMS`. Fill the licence form from the venue template; the human signs it.

## Phase 7 — Public artifact (when the submission had an anonymous artifact)

If the vault submission or atlas output carries `anonymous_repo`/`anonymous_url`:
1. De-anonymise the artifact repository (LICENSE holder, README title/author line, BibTeX `note = {To appear}`, docstrings, any anonymity scanner → public-release check). **Do not change its visibility.** Verify the paper's generated inputs are byte-identical to the artifact's copies.
2. If the repo's git identity is anonymous, rewrite author/committer with a backup branch first; confirm the tree hash is unchanged; push with `--force-with-lease=<branch>:<old-sha>` after `git remote -v`.
3. Build `git archive` of the release commit → `zenodo/<repo-name>-v1.0.0.zip`; write `zenodo/form-values.md` (resource type, licence matching `LICENSE`, version, funder/grant, conference fields, description). Reserve the DOI, cite it in the paper's availability statement, and after the human publishes, verify the DOI resolves and the file's MD5 matches.

## Phase 8 — Author-side handoff
Report what remains for the human: **acknowledgments** (now un-anonymized — offer a funding stub), signed copyright/rights form, reproducibility checklist, registration, and the presentation.

When the user confirms the upload, archive the files they say they uploaded per `rules/submission-file-archive.md` (human-supplied only) into `submission/archive/<date>-camera-ready/` as `{surface}-camera-ready-{manuscript.pdf,source.zip,licence.pdf}` with a README (provenance, sizes, SHA-256). Then run ONE atomic writeback (`multi-system-completeness.md`: show every diff, confirm once, apply all-or-none):

| System | Update |
|---|---|
| Vault submission | `status: In Press`; `history:` — the `decision` row (`round: initial`, `files:` = decision PDF + reviews PDF) if absent, and a `camera-ready` row (`round: camera-ready`, `files:` = the archived manuscript, note `CMT <ID>: camera-ready, source, signed licence`); `submitted_files:` += manuscript; `artifact_doi:` (bare DOI) when Phase 7 ran; the body **Status paragraph** and checklist (upload done; registration/presentation open) |
| Atlas topic | output `status: In Press` (topic `status:` stays `Accepted`); output `artifact_doi:`; `## Next steps` (tick camera-ready, add registration/presentation); `## History` entry, **newest first**; `last_worked` |
| `papers.yml` | append the upload + DOI to the paper's `notes` |
| Project docs | `CLAUDE.md`, `AGENTS.md`, `README.md`, `MEMORY.md`, `.context/project-recap.md`, `.context/current-focus.md` (header lines + a new dated block) |

`In Press` is an output and submission status, never a topic status (`atlas-status-vocabulary.md`): leave the topic `status:` and the `CLAUDE.md` status line that mirrors it at `Accepted`, and move the `.context/projects/_index.md` row to `In Press` with the other project docs. The upload is the trigger; do not wait to be asked (both 2026-10-10 PRIMA camera-readies sat at `Accepted` until the author asked the next day).

If another output of the same venue cycle exists (e.g. two accepted papers at one conference), compare its camera-ready archive and records and keep the two consistent.

**Verify before reporting done.**
Then check that no project document still says the camera-ready is pending:
```bash
grep -rnE 'camera-ready (paper )?.*(due|pending)|not yet (been )?uploaded' CLAUDE.md AGENTS.md README.md MEMORY.md .context/
```

## Anti-Patterns

- **Don't move proofs to an appendix before confirming the appendix is page-exempt.** If it counts, you've just relocated, not saved, space.
- **Don't `replace_all` or full-`Write` the live `.tex`.** Narrow edits; for bulk citekey work defer to `bib-rekey`'s diff-verified flow.
- **Don't add a reviewer-suggested citation from memory.** Verify it — reviewers mis-cite.
- **Don't chain all phases in one response.** Checkpoint per `phased-work.md`.
- **Don't log acceptance to vault/atlas if the formal decision letter hasn't arrived** — confirm with the user.
- **Don't name correspondence by date or venue paper ID**, and never file it in a project-root `correspondence/editorial/` or `correspondence/referee-reviews/`.
- **Don't treat the vault writeback as frontmatter-only.** The body Status paragraph, project docs and `papers.yml` notes go stale too; the 2026-10-10 PRIMA camera-readies missed all three until a manual sweep.

## Verification

- All reviewer points map to a concrete edit (action table fully checked off).
- Build clean, 0 undefined, body within page limit, copyright slug present, author block de-anonymized.
- Pre-edit source preserved in `submission/camera-ready/pre-edit-source-<date>/`; the as-submitted PDF stays frozen in `submission/archive/<date>-initial/`.
- Upload package built by `build-package.sh` (isolated compile matches the canonical build); archive README hashes match the uploaded files.
- Writeback verified: both schema modes, the portfolio validator, `generate-paper-history --check`, and the stale-wording grep are clean; the Atlas output and the Vault submission read `In Press`, the topic `Accepted`.

## Cross-References

| Skill | Relationship |
|---|---|
| `bib-rekey` | Phase 2 bibliography rekey + `\cite` remap |
| `strategic-revision --external` | The R&R counterpart (rebuttal + DAG) — use that, not this, for revise-and-resubmit |
| `proofread`, `latex`, `bib-validate` | QA components composed in Phases 2 & 5 |
| `preprint` | For an arXiv/working-paper variant instead of a venue camera-ready |
