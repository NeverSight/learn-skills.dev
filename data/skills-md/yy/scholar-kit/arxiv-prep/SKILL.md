---
name: arxiv-prep
user_invocable: true
description: Prepare a LaTeX paper's source package and metadata for arXiv. Use when the user is ready to upload a paper or wants an arXiv-compatible staging copy, archive, and compilation check.
---

# Prepare an arXiv submission

Create a clean staging copy, verify that it compiles independently, and package it for upload. Never modify the original paper directory.

Treat this as packaging work. Run `presubmit-checks` only when the user also requests a readiness review.

## Establish the source tree

Use the manuscript path supplied by the user. Otherwise, infer the main file from project configuration, build files, and the TeX document tree. Determine the compiler, bibliography backend, included files, figures, custom packages, and generated files required for a successful build.

Identify supplements and ask only when their role is ambiguous. Keep material that belongs in the article's PDF within the TeX tree. Put supporting code, data, movies, or other non-article material in `anc/` only when the user wants it submitted as ancillary material.

Check current arXiv guidance before relying on version-specific processor behavior or limits:

- [TeX submissions](https://info.arxiv.org/help/submit_tex.html)
- [TeX Live at arXiv](https://info.arxiv.org/help/faq/texlive.html)
- [Archive creation](https://info.arxiv.org/help/tar.html)
- [Metadata fields](https://info.arxiv.org/help/prep.html)
- [Oversized submissions](https://info.arxiv.org/help/sizes.html)

## Create the staging copy

Create a sibling staging directory such as `<paper-dir>_arXiv`. If it already exists, stop and ask before replacing or modifying it.

Copy only what the submission needs:

- The top-level and included TeX sources, figures, and data read during compilation.
- Custom `.cls`, `.sty`, `.bst`, font, or macro files unavailable in arXiv's selected TeX Live environment.
- Either all required `.bib` files or a pre-generated `.bbl` whose basename matches the top-level TeX file. Preserve the backend and version compatibility expected by `biblatex` or Biber.
- Pre-generated `.ind`, `.gls`, or `.nls` files when the document uses an index, glossary, or nomenclature.
- User-approved ancillary files under `anc/`; do not place TeX article sources there.

Exclude version-control data, editor backups, referee correspondence, unused figures, unrelated source files, secrets, the compiled manuscript PDF, logs, and auxiliary files. Preserve required PDF figures and the generated bibliography and index-like files listed above.

Review the staged sources and embedded file metadata for private comments, credentials, absolute local paths, TODOs, and author-only notes. arXiv publishes submitted source files. Flag ambiguous material instead of deleting it automatically.

Flag journal-only wording, referee mode, and incompatible copyright notices for the user. Do not rewrite them or change the license without approval.

### Keep the package small

Measure the total uncompressed size and each individual file. arXiv currently flags either one above 50 MiB as oversized and may hold the submission for review. Keep avoidable excess below that guideline; if the scientific content requires more, report it rather than silently degrading the paper.

When the package is large, identify the largest files and remove unused material first. Optimize pixel-native images for their final display size without visible degradation. Preserve native vector plots, diagrams, text, and line art. Use `critique-figures` before making uncertain format or resolution changes. Do not rewrite bibliographies or blindly compress PDFs to save space.

## Verify the staged build

Build from the staging directory root with the processor intended for arXiv. Use the project's build command when it reproduces that processor; otherwise use an appropriate `latexmk` invocation. Let the build tool run enough passes rather than prescribing a fixed pass count.

Treat compilation errors, missing files, undefined citations, and undefined references as blockers. Check for case-sensitive path mismatches and dependencies that resolve only through the original directory. Compare the staged PDF with the original build, including page count, figures, bibliography, and supplements.

A successful local build does not replace inspection of arXiv's generated preview. Tell the user to verify the detected processor, top-level file, compilation log, and final PDF during upload.

## Prepare metadata and archive

Extract copy-ready title, authors, abstract, and comments from the manuscript. Remove layout commands and expand private macros, but preserve scientific notation and TeX accents accepted by arXiv. Report categories, report numbers, journal references, DOIs, and license as user decisions rather than guessing them.

Create a `.tar.gz` or `.zip` containing the staging directory's contents, not the directory itself. Inspect the archive listing and report its path, size, file count, top-level TeX file, processor, and build status.

Do not call the package ready when a blocker remains. In the handoff, list unresolved warnings and the remaining upload decisions, especially category and license.
