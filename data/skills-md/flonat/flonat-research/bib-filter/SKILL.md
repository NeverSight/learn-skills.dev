---
name: bib-filter
description: "Filter a LaTeX project's bibliography to the entries actually cited, with Overleaf-source resolution, temporary staging, validation, approval-gated canonical replacement, and compilation. Use when a manuscript's bibliography carries uncited entries, typically before submission or after a large revision. Not for checking citation keys or DOIs; use $bib-validate."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(ls*), Bash(wc*), Bash(realpath*), Bash(readlink*), Bash(shasum*), Bash(uv*), Bash(latexmk*), Bash(mv*), Bash(rm*), Bash(mktemp*), Skill, AskUserQuestion
argument-hint: "[path-to-tex-or-project-dir]"
---

# Bibliography Filter

Produce and validate a cited-only bibliography, then replace the manuscript's canonical `.bib` only after explicit approval. In an Overleaf-linked project, the resolved Overleaf bibliography is canonical; a wrapper-local copy is not a second authority.

## When to Use

- Before submission — strip unused references from the bibliography
- When a shared `.bib` (e.g., Paperpile/Paperpile export) contains hundreds of entries but the paper cites a subset
- To reduce `.bib` file size for Overleaf or arXiv upload
- As a cleanup step after major revision (removed sections may leave orphan citations)

## Process

### Step 1: Locate files

If given a directory, resolve the actual manuscript source first:
- For `paper-<arm>/paper`, run `realpath`/`readlink` and inspect the resolved Overleaf target before declaring a bibliography missing.
- Read `\bibliography{...}` or `\addbibresource{...}` from the canonical driver and resolve the referenced `.bib` relative to that source tree.
- Do not select a project-root export, backup, or stale wrapper copy merely because it has the same filename.

Then find the main `.tex` and `.bib` files:
- `.tex`: Glob for `*.tex` in the directory (and `paper/` subdirectory if it exists). The main file is the one containing `\begin{document}`.
- `.bib`: Look for `\bibliography{...}` or `\addbibresource{...}` in the main `.tex` to find the bib filename. Fall back to globbing `*.bib`.

If given a specific `.tex` file, derive the `.bib` from it.

### Step 2: Extract all citation keys from `.tex`

Scan **all** `.tex` files in the project (main + any `\input{}`/`\include{}` files) for citation commands:

```
\cite{key1,key2}
\citep{key1,key2}
\citet{key1}
\citealt{key1}
\citealp{key1}
\citeauthor{key1}
\citeyear{key1}
\citetext{key1}
\parencite{key1,key2}
\textcite{key1}
\autocite{key1}
\footcite{key1}
\fullcite{key1}
\nocite{key1}
```

Handle:
- Multiple keys in one command: `\cite{key1,key2,key3}` → extract all three
- Whitespace around commas: `\cite{key1, key2}` → trim
- Optional arguments: `\cite[p.~5]{key1}` or `\citep[see][]{key1}` → extract `key1`
- `\nocite{*}` → special case: means "include everything", so `filtered.bib` = full `.bib` (warn and stop)

Collect into a deduplicated set of cited keys.

### Step 3: Parse `.bib` and filter

Read the `.bib` file. For each entry (`@article{key,`, `@book{key,`, `@inproceedings{key,`, etc.):
- If the entry's key is in the cited set → include in output
- If not → exclude
- Preserve `@string{}`, `@preamble{}`, and `@comment{}` blocks (they may be needed by included entries)

### Step 4: Stage a cited-only candidate

Write a temporary candidate beside the canonical bibliography, using a collision-safe name such as `.references.filtered.<timestamp>.bib`. Do not create a durable second bibliography authority.

Report:
```
Original: N entries
Cited: M keys found in .tex
Filtered: M entries written to <temporary candidate>
Removed: N-M unused entries
```

If any cited keys are **not found** in the `.bib`, list them as warnings and recommend the configured bibliography validator or manual reconciliation.

### Step 5: Validate before replacement

Before asking to replace anything:

1. verify every cited key is present, including `crossref` parents;
2. run the configured bibliography validator against the candidate;
3. compile the manuscript in a temporary build/output directory using the candidate;
4. compare bibliography entry count and rendered reference count with the expected cited set;
5. report the exact canonical target, its current hash, the candidate hash, kept keys, dropped keys, and validation result.

If any cited key is missing or validation/compilation fails, leave the canonical bibliography unchanged and stop.

### Step 6: Approval-gated canonical replacement

Ask: “Replace `<canonical-bib-path>` with the validated cited-only candidate?” Only an explicit approval authorizes replacement.

After approval:

1. recheck the canonical file hash to detect concurrent Overleaf changes;
2. atomically replace the canonical `.bib` at the resolved Overleaf path;
3. compile again from the canonical source and confirm no missing citations or bibliography errors;
4. remove the temporary candidate after successful verification;
5. report the final canonical path and hash.

Do not retain both `references.bib` and `filtered.bib` in the Overleaf tree.

Dropped but strategically important comparator records belong in the literature authority, Paperpile, or a registered literature review packet—not in the live manuscript bibliography merely for safekeeping.

## Edge Cases

- **Multiple `.bib` files:** preserve the driver's declared multi-file structure unless the user separately approves consolidation; stage one filtered candidate per canonical source
- **`\nocite{*}`:** Warn that all entries are cited and stop — filtering would be a no-op
- **Cross-references:** Some `.bib` entries use `crossref = {parent-key}`. If a cited entry cross-references another, include the parent even if it's not directly cited
- **Empty result:** If no citations found in `.tex`, warn and do not write an empty file
- **Concurrent Overleaf change:** if the canonical hash changes between staging and replacement, discard the replacement attempt, re-resolve, and repeat validation

---

## Output Verification (Guard)

This skill writes files. Before any auto-commit, emit an outputs manifest and run the shared verifier. See [`skills/_shared/verify-outputs.md`](../_shared/verify-outputs.md) for the full protocol.

**Required tail steps** (before `git commit`):

1. Write manifest to `<project>/.claude/state/outputs-manifest-<UTC-timestamp>.json` listing every file this skill claims to have written in this invocation (paths relative to the project root).
2. Run:

   ```bash
   uv run python "<skills-root>/_shared/verify_outputs.py" \
       --manifest "$MANIFEST" \
       --project-root "$PROJECT_ROOT"
   ```

3. If the verifier exits non-zero, **do not commit** — surface the missing-files list to the user and stop. The verifier has already logged an `error` entry to `~/.local/state/ai-workflows/skill-outcomes.jsonl`, which feeds the shared skill-health dashboard.

**Why:** closes the "hallucinated outputs" failure class (commit `b2cff75`, 2026-04-18).
