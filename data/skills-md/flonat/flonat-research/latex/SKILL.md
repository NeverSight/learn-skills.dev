---
name: latex
description: "Compile one specified LaTeX document, resolve build errors, audit citations, and report build quality. Use when a .tex source must be built or a concrete compilation failure repaired. Not for corpus-wide build checks, visual polish after a clean build, or creating a project; use $latex-health-check, $latex-polish, or $latex-scaffold."
allowed-tools: Bash(latexmk*), Bash(xelatex*), Bash(pdflatex*), Bash(biber*), Bash(bibtex*), Bash(mkdir*), Bash(ls*), Bash(wc*), Bash(cp*), Bash(cmp*), Bash(head*), Read, Write, Edit, Grep, Glob
argument-hint: "[tex-file-path]"
skill-dependencies: []
---

# LaTeX Document Compilation

> Default compilation skill for all LaTeX documents. Compiles with autonomous error detection and resolution (up to 5 iterations), runs a citation audit on clean builds, and produces a quality score.

## When to Use

- **Default method** for all LaTeX compilation
- Any `.tex` file that should compile to PDF
- When compilation fails and you want automatic diagnosis and repair
- When you want a post-compilation citation audit

## When NOT to Use

- Markdown documents — use plain markdown, not LaTeX
- Quick notes or drafts — LaTeX overhead not worth it
- Documents that don't need citations, equations, or precise formatting
- Documents with exotic custom classes that need manual debugging

---

## Quality Scoring

Apply numeric quality scoring using the shared framework and skill-specific rubric:

- **Framework:** [`../shared/quality-scoring.md`](../shared/quality-scoring.md) — severity tiers, thresholds, verdict rules
- **Rubric:** [`references/quality-rubric.md`](references/quality-rubric.md) — issue-to-deduction mappings for this skill

Start at 100, deduct per issue found, apply verdict. Include the Score Block in the final report.

## Critical Rules

1. **Build artifacts go to `out/`, PDF stays in the source directory.** Use this skill's fail-closed canonical bundle at `templates/build-config/.latexmkrc`; do not hand-write an `END { system(...) }` copy block because it can mask latexmk's failure status and copy stale PDFs. For VS Code builds, use the bundled canonical recipe that explicitly loads `%DIR%/.latexmkrc`—`-cd` alone is insufficient.
2. **NEVER write BibTeX entries from memory.** Verify against authoritative metadata sources such as Crossref or the DOI resolver before writing. Use an installed literature-search workflow when one is configured.
3. **Check document class before adding packages.** Some classes load packages internally (e.g., `elsarticle` loads `natbib` — adding `\usepackage{natbib}` causes errors).
4. **Maximum 5 fix iterations.** If the document still has errors after 5 auto-fix cycles, stop and report the unresolved errors to the user.
5. **Never silently swallow errors.** Every fix must be reported: what was wrong, what was changed, and which file was edited.
6. **Preserve user intent.** Auto-fixes should be minimal and conservative. Add packages or overrides — never remove user content.
7. **Citation audit requires clean compilation.** Only run the `\cite{}` vs `.bib` cross-check after zero errors.
8. **Validate new bibliography entries.** The built-in citation audit checks key cross-references. When `.bib` entries were added or modified, also check DOI resolution, required fields, author formatting, and whether a preprint has a published version. If a dedicated bibliography validator is installed, use it for this extended check; otherwise perform and report the direct checks.

---

## Protocol

### Phase 1: Pre-flight

1. **Locate the `.tex` file.** Resolve the path (absolute or relative to CWD).
2. **Identify the project directory** — the folder containing the `.tex` file.
3. **Ensure the canonical `.latexmkrc` exists** in the project directory. Resolve `templates/build-config/.latexmkrc` relative to this installed skill and stop if the bundle is missing. Never recreate a partial version from memory. Compare an existing file byte-for-byte with the bundled canonical; do not overwrite divergence blindly. Move project-specific bibliography paths or custom dependencies into `.latexmkrc.local`; move engine selection into a `% !TEX program = ...` driver comment. Replacing a divergent file remains an explicit migration.
4. **Create `out/` directory** if it doesn't exist: `mkdir -p <project-dir>/out`.
5. **Identify the `.bib` file(s)** referenced in the document (scan for `\bibliography{}`, `\addbibresource{}`, or `\bibinput{}`). Note their paths for Phase 5.

### Phase 2: Compile-Fix Loop

Run up to **5 iterations**. Each iteration:

#### Step 2a — Compile

```bash
cd <project-dir> && latexmk -interaction=nonstopmode <filename>.tex 2>&1
```

Capture the full output. The log file will be at `out/<filename>.log`.

#### Step 2b — Read the log

Read `out/<filename>.log` in full. Parse for errors and warnings.

#### Step 2c — Classify errors

Check the log against the known error patterns below. If an error matches, apply the fix and go to Step 2a. If no known pattern matches, record the error as **unresolved** and stop the loop.

**Same-error circuit breaker.** Independent of the 5-iteration cap: if the same error (same line family, same pattern signature) survives **3 consecutive fix attempts**, stop the loop early. Continued attempts on a stuck error compound damage rather than resolve it. Report what was tried, quote the log line, and ask the user how to proceed. A common signature: `Illegal parameter number` jumping between line numbers as you edit — that is the diagnostic for a parameterized TikZ style defined inside a Beamer frame; see `skills/shared/tikz-rules.md` Rule 11.

---

### Known Error Patterns & Auto-Fixes

Check the log against these patterns. Full fix instructions: [`references/known-errors.md`](references/known-errors.md)

| # | Pattern | Key log signature |
|---|---------|-------------------|
| 1 | Missing package | `File '<pkg>.sty' not found` or undefined command from known package |
| 2 | Font/symbol conflicts | `Command \<name> already defined` |
| 3 | Undefined citation | `Citation '<key>' ... undefined` or biblatex entry not found |
| 4 | Missing image/file | `File '<path>' not found` (pdftex.def or LaTeX) |
| 5 | Stale auxiliary files | Corrupted `.aux`/`.bbl`/`.bcf`, or `no \bibstyle command` |
| 6 | Beamer/enumitem clash | `Option clash for package enumitem` or `\item already defined` |
| 7 | xcolor option conflicts | `Option clash for package xcolor` or undefined `\rowcolor` |
| 8 | TikZ reserved keys | `I do not know the key '/tikz/<name>'` or pgfkeys error |

If an error matches, read the full fix from the reference and apply it. If no pattern matches, record as **unresolved** and stop the loop.

#### 2.4 PDF backup (paper directories only)

**Only run if the compile-fix loop above ended with a successful compilation (PDF exists).**

If the `.tex` file is inside a `paper-{venue}/paper/` structure (where `paper/` is a symlink to Overleaf):

1. **Identify the paper wrapper** — the parent of the `paper/` symlink (e.g., `paper-jbdm/`).
2. **Create the backup directory:** `mkdir -p <paper-wrapper>/backup`
3. **Copy the PDF:**
   ```bash
   cp <paper-wrapper>/paper/<filename>.pdf <paper-wrapper>/backup/<wrapper-name>_vcurrent.pdf
   ```

**Detection logic:**

- The project directory containing the `.tex` file is a symlink named `paper`.
- Its parent directory name starts with `paper-`.
- If either condition is false, skip this sub-step silently.

---

### Phase 3: Final Report

After the loop ends (either clean compilation or max iterations reached), report:

#### Compilation Status

| Field | Value |
|-------|-------|
| **Status** | Clean / Errors remaining |
| **Iterations** | N of 5 |
| **Pages** | (from log: `Output written on ... (N pages)`) |
| **LaTeX/package warnings** | Count of `Warning`-tagged log lines (undefined refs, font subs, package warnings) |
| **Typographic boxes** | Overfull/underfull h/vboxes by severity — see box report below (NOT counted by a `Warning` grep) |
| **Fixes applied** | List each fix: what error, what was changed, which file |
| **Unresolved errors** | List any errors that couldn't be auto-fixed |

#### How to extract page count

```bash
grep -o "Output written on .* ([0-9]* page" out/<filename>.log | grep -o "[0-9]* page"
```

#### How to count warnings and boxes

Warnings and typographic boxes are **separate** — box messages are not
`Warning`-tagged, so a single `Warning` grep misses every overfull/underfull box.
Report both, using the recipes in [`../shared/overfull-boxes.md`](../shared/overfull-boxes.md):

```bash
# LaTeX/package warnings (refs, fonts, packages)
grep -c "Warning" out/<filename>.log
# Overfull/underfull boxes (the thing the Warning grep cannot see)
grep -cE 'Overfull \\[hv]box \([0-9.]+pt too (wide|high)\)' out/<filename>.log
grep -cE 'Underfull \\[hv]box \(badness [0-9]+\)' out/<filename>.log
```

#### Box report (typographic quality)

Extract the top offenders by overflow magnitude and report each box `≥ 1 pt` with
its location, width, and a remediation tier per the severity gradient + ladder in
[`../shared/overfull-boxes.md`](../shared/overfull-boxes.md):

```bash
awk -F'[()]' '/Overfull \\[hv]box/ {
    split($2, a, "pt"); w = a[1] + 0;
    loc = $0; sub(/.*too (wide|high)\) */, "", loc);
    printf "%7.1f pt  %s\n", w, loc
}' out/<filename>.log | sort -rn | head -20
```

Report only — do not silently reword prose to close a box (`rules/manuscript-edit-budget.md`).
The only safe auto-fix is inserting `\usepackage{microtype}` when genuinely absent.

**Breadcrumb:** Append to `.planning/state.md` (if exists) or `.context/current-focus.md`:
```
### [latex] Compilation complete [YYYY-MM-DD HH:MM]
- **Done:** [Clean/Errors remaining, N iterations, N pages, N fixes applied]
- **Outputs:** [PDF at <path>]
- **Next:** [Citation audit (if clean) or manual error resolution]
```

---

### Phase 4: Visual-Fragility Source Lint (clean builds only)

**Only run if Phase 2 ended with zero errors.** Sits between the final report (Phase 3) and the citation audit (Phase 5). Catches LaTeX source patterns that compile clean but produce visually fragile output — the failure class the title-page incident (2026-06-19) exposed.

Full detector catalogue with regex signatures, severity tiers, remediation, and false-positive caveats: [`references/source-pathologies.md`](references/source-pathologies.md).

#### What to run

1. **Nine grep-based source-pathology detectors** against `main.tex` plus any `\input`/`\include`'d files:

   | # | Pattern | Tier |
   |---|---|---|
   | 1 | Spacing hacks fighting global spacing (`\onehalfspacing` + local `\\[-Xcm]` / `\vspace{-…}`) | Major |
   | 2 | Manual vertical-rhythm surgery (repeated `\vspace`/`\vskip`/`\pagebreak` in body) | Moderate–Major |
   | 3 | Line breaks as layout engine (`\\` / `\newline` / `\linebreak` inside `\section`/`\caption`) | Moderate–Major |
   | 4 | Forced-float carpet bombing (`[H]`/`[!h]` pinning, `\FloatBarrier` overuse) | Moderate |
   | 5 | Shrink-to-fit tables/figures (`\resizebox{\textwidth}{!}{…}`, `\adjustbox{width=\textwidth}`) | Major |
   | 6 | Tiny-table typography hacks (`\scriptsize`/`\tiny` in tables; negative `\tabcolsep`; `\arraystretch<0.9`) | Moderate–Major |
   | 7 | Absolute / overlap positioning (`\raisebox`, `\makebox[0pt]`, `\llap`, `\rlap`, `\smash`, `\hspace*`) outside math | Major |
   | 8 | Fixed-width layout assumptions (`p{Xcm}`, `\begin{minipage}{Xcm}`, `\parbox{Xcm}`) | Moderate |
   | 9 | Label-before-caption inside floats (`\label{…}` precedes `\caption{…}` in a `figure`/`table` block) | Major |

2. **`chktex`** if installed: `chktex -q -n8 -n44 main.tex 2>&1 | grep -v "^$"`. Advisory only — collect warnings; deduct -1 each, capped at -10. Skip if `chktex` not on PATH.

3. **`latexindent -k`** if installed: `latexindent -k main.tex 2>&1; echo "Exit: $?"`. Source-cleanliness smoke test. Non-zero exit → -3 once. Skip if `latexindent` not on PATH.

#### Output

Append a **Source pathologies** subsection to the Phase 3 report:

```markdown
### Source pathologies

| Pattern | Location | Detail | Tier |
|---------|----------|--------|------|
| 1 Spacing-hacks | titlepage, line 56 | `\\[-0.3cm]` under global `\onehalfspacing` (line 43) | Major |
| 9 Label-before-caption | tab:results, line 412 | `\label` at L410 precedes `\caption` at L413 | Major |
```

If no findings: "No source pathologies detected." If `chktex` or `latexindent` ran, note their PASS/N-warnings status.

#### Auto-fix scope

Phase 4 is **report-only**, with one exception: Pattern 1 ("Spacing hacks fighting global spacing") has a deterministic remediation (wrap the affected block in `\begin{singlespace}…\end{singlespace}`, delete the negative kerns). The skill **offers** this as an opt-in fix in the final report; the user accepts or declines per case. Do not auto-apply.

For Patterns 2–9 and tool findings: report only.

#### When to skip

- Compile failed in Phase 2 (pathology lint is meaningless without a build).
- User explicitly invoked `latex --no-lint`.

---

### Phase 5: Citation Audit (clean builds only)

**Only run this phase if Phase 2 ended with zero errors.**

1. **Extract all `\cite` keys** from the `.tex` file (and any `\input`/`\include` files):
   - Match `\cite{...}`, `\citep{...}`, `\citet{...}`, `\textcite{...}`, `\parencite{...}`, `\autocite{...}`, and multi-key variants like `\cite{key1,key2}`.
2. **Extract all bib entry keys** from the `.bib` file(s): match `@<type>{<key>,`.
3. **Cross-reference:**

| Check | What it finds |
|-------|--------------|
| **Missing in .bib** | Keys cited in `.tex` but absent from `.bib` |
| **Unused in .tex** | Keys defined in `.bib` but never cited |
| **Possible typos** | Near-matches between missing cite keys and existing bib keys |

4. **Report** the results as a table. Do not modify any files during the audit — report only.

---

### Phase 6: Quality Score

After all phases complete, compute the quality score:

1. Read [`references/quality-rubric.md`](references/quality-rubric.md) for deduction mappings.
2. Log every issue from Phases 2-5 (unresolved errors, remaining warnings, overfull/underfull boxes from the Phase 3 box report, citation mismatches). The rubric deducts per box by severity (`>10pt: -5`, `1-10pt: -2`, underfull: `-1`) — feed it the box report, not a `Warning` count.
3. Compute score (100 - total deductions), apply verdict per [`../shared/quality-scoring.md`](../shared/quality-scoring.md).
4. Append the Score Block to the compilation report:

```markdown
## Quality Score

| Metric | Value |
|--------|-------|
| **Score** | XX / 100 |
| **Verdict** | Ship / Ship with notes / Revise / Revise (major) / Blocked |

### Deductions

| # | Issue | Tier | Deduction | Category |
|---|-------|------|-----------|----------|
| 1 | [description] | [tier] | -X | [category] |
| | **Total deductions** | | **-XX** | |
```

#### 6.1 Output verification (before commit)

When the compile produced a PDF (and any backup copy), emit an outputs manifest and run the shared verifier per [`_shared/verify-outputs.md`](../_shared/verify-outputs.md):

1. Write manifest to `<project>/.claude/state/outputs-manifest-<UTC-timestamp>.json` listing every file written this invocation (PDF, backup PDF if 2.4 ran, log files).
2. Run:

   ```bash
   uv run python "<skills-root>/_shared/verify_outputs.py" \
       --manifest "$MANIFEST" \
       --project-root "$PROJECT_ROOT"
   ```

3. If the verifier exits non-zero, **do not commit**. Surface the missing-files list and stop.

Closes the "hallucinated outputs" failure class (commit `b2cff75`, 2026-04-18).

---

## Configuration Reference

### Output Directory

All LaTeX build artifacts (`.aux`, `.log`, `.bbl`, `.fls`, etc.) go to an `out/` subfolder relative to the source file. The **PDF is copied back** to the source directory after each successful build, so it lives alongside the `.tex` file for easy access.

The PDF-copy convention is enforced in **two places** — keep them in sync when making changes:

1. **`.latexmkrc`** (per-project) — the canonical success-gated copy-back logic handles terminal builds
2. **VS Code `.vscode/settings.json`** (per-workspace) — explicitly loads the document-directory canonical before `-cd`

VS Code integration, engine auto-detection (pdfLaTeX/XeLaTeX/LuaLaTeX), manual override configs, reference checking scripts, and manual compilation commands:

**[references/latex-configs.md](references/latex-configs.md)**

### Overleaf-Synced Projects

When a project is synced to Overleaf (via Dropbox or Git):
- The `out/` directory will sync to Overleaf but Overleaf ignores it — this is fine
- Always use `.latexmkrc` to enforce `out/` — Overleaf ignores this file too
- Overleaf compiles independently on its server; local compilation is for verification only
- The `.bst` file (e.g., `elsarticle-harv.bst`) lives in the source directory, not `out/`

### Local-Only Projects (No Overleaf)

Not all projects sync to Overleaf. For local-only projects:
- The same `out/` and `.latexmkrc` conventions apply — this keeps the working directory clean regardless of sync method
- There is no `paper/` symlink — `.tex` files live directly in the project root or a subdirectory

---

## Templates

See [`references/templates.md`](references/templates.md) for working paper template location, files, citation style toggle, bibliography file naming conventions, and bibliography command reference.

---

## Related Skills

| Situation | Delegate to |
|-----------|-------------|
| Need to find or verify a bibliography entry | Installed scholarly-search workflow, or direct authoritative metadata lookup |
| Full academic proofreading after clean compilation | `proofread` |
| Detailed `.bib` validation beyond cite-key matching | Installed bibliography validator, when available |
| Beamer presentations specifically | `beamer-deck` (which uses this skill internally for compilation) |
| Fleet-wide compilation health check | `latex-health-check` (project discovery, 3 iterations per project, cross-project checks) |

---

## Examples

### Basic usage

> "Compile my paper at `~/papers/mcdm-survey/main.tex`"

Runs the full protocol: pre-flight → compile-fix loop → report → citation audit → quality score.

### After fixing a known issue

> "Recompile — I added the missing package manually"

Runs from Phase 2 directly (pre-flight can be skipped if `.latexmkrc` and `out/` already exist).

### Targeted fix

> "My paper won't compile — something about Bbbk"

Identifies as Pattern 2 (font conflict), applies the `\let\Bbbk\relax` fix, recompiles.

**Source format.** Paper prose stays one line per paragraph; normalize edited files with `.scripts/latex_paragraph_format.py --apply` and recompile. Canonical: `rules/latex-source-format.md`.
