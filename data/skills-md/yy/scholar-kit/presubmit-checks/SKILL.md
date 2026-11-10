---
name: presubmit-checks
user_invocable: true
description: Check a LaTeX paper before submission or circulation. Verify references, compilation, LaTeX hygiene, figure quality, affiliations, acknowledgements, and code or data availability, then return one severity-ranked report.
---

# Check a paper before submission

Inspect the paper without modifying it. Run independent checks concurrently when practical; the coordination method and number of agents may vary.

## Establish scope

Use a manuscript path supplied by the user. Otherwise, infer the main file from project configuration, build files, and the TeX document tree. Follow `\input` and `\include` dependencies and resolve figure and bibliography paths from the main document.

Use the project's documented build command. If none is documented and a Makefile exists, use its default target. Record the command and working directory so failures are reproducible.

## Run the checks

### References

Use the `check-refs` skill to verify cited works. Report retracted citations as blockers, distinguish unverified entries from nonexistent works, and note missing DOI or URL metadata separately.

### LaTeX and build

Use the `latex-cleanup` skill for source-level checks. Build the paper and inspect the log for:

- Compilation errors and missing files.
- Undefined references or citations.
- Draft artifacts and `draft` mode.
- Overfull boxes that visibly damage layout.

Continue the other checks if the build fails.

### Figures

Use the `critique-figures` skill on the manuscript's rendered figures. Incorporate its findings on format, effective resolution, legibility, accessibility, visual encoding, panel labels, and statistical presentation.

Carry every blocker identified by `critique-figures` into the unified report. In particular, raster-only plots, diagrams, and line art remain submission blockers; apply that skill's rules for pixel-native and mixed figures.

### Front matter

Extract enough information for the user to verify:

- Every author and affiliation. Flag missing affiliations and apparently incomplete department, institution, or country information.
- The acknowledgements, including every funding source, grant number, and named person thanked. Flag a missing acknowledgements section.
- Code and data availability statements. Flag a missing statement as a blocker only when the target venue requires one; otherwise report it as a warning.

## Report

Return one concise report organized by severity:

1. Blockers: compilation errors, missing figures, undefined references or citations, retracted citations, raster-only plots or line art, and missing venue-required availability statements.
2. Warnings: unverified references, draft artifacts, consequential overfull boxes, incomplete affiliations, material figure-quality findings, and other likely submission problems.
3. User verification: list the extracted affiliations, acknowledgements, funding details, and availability statements for completeness checks.
4. Suggestions: missing DOI or URL metadata and non-blocking typography or style improvements.

Give file and line references or log excerpts for each actionable finding. Group repeated warnings and state which checks could not be completed. Do not modify files unless the user approves a separate fix pass. Use `critique-manuscript` only when the user also requests a content-level review.
