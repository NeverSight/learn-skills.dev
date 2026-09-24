---
name: write-paper
description: Use when starting or writing a paper for a venue — venue selection, framing, contribution selection, and the full manuscript on the venue template.
license: MIT
---

# Write Paper

Build `papers/<slug>/`: a venue-specific paper assembled from the survey
and the contribution reports. The survey supplies related work; the reports
supply technical content; the root `references.bib` supplies every citation.

## Read First

- `papers/README.md` — the paper lifecycle contract
- `survey/survey.pdf` and the reports of candidate contributions
- `references/writing-rules.md`, `references/venue-fit.md`

## Procedure

1. **Venue.** If not fixed, compare candidates with the user using
   `references/venue-fit.md`. Fill `venue.md`: venue, track, deadlines,
   page/format rules, anonymization policy, template source, and the
   venue's specific badge/artifact requirements — from the real call for
   papers, never from memory.
2. **Framing.** Write `framing.md`: the story, the claims, which
   contributions support which claim and what each provides, and what is
   deliberately out of scope. Every claim must map to a contribution or to
   survey-grounded evidence.
3. **Template.** Import the venue's official LaTeX template into
   `manuscript/`; rename the entry point to `main.tex`. Use the bib system
   the venue class dictates (bibtex/natbib or biblatex), reading the root
   `references.bib` via relative path. The base manuscript defaults to
   **numeric** (biblatex); the venue class sets the final style. The same root
   `references.bib` is shared with the survey (author-year) — bibliography
   **style is per-document, not per-entry**; contribution reports stay numeric.
4. **Write.** Section by section: related work distilled from the survey
   (theme-first, never paper-by-paper); methods/results from the
   contribution reports and their figures; every `\cite{}` resolves in the
   root `.bib`. Follow `references/writing-rules.md`.
5. **Build and check.** `make paper P=<slug>`, verify page limits and
   format rules from `venue.md`, run `make check`.
6. Recommend an adversarial-review pass before any submission.

## External Mode (Overleaf)

When the user asks to work on an external LaTeX project (e.g. a
collaborator's Overleaf), use the overleaf MCP if configured: read or
contribute to that project directly. Nothing in this scaffold depends on
the external project; treat it as a foreign workspace, and apply
`references/writing-rules.md` there too.

## Rules

- A claim enters the manuscript only with its evidence: a contribution, a
  survey-grounded citation, or an explicitly labeled open question.
- Never invent or restyle bibliography entries; a missing entry means
  missing SOTA work — stop and report.
- Figures come from contribution folders; copy them in, never recreate
  data by hand.

## Done When

- `venue.md` and `framing.md` complete, the manuscript builds clean on the
  venue template within its limits, `make check` passes
