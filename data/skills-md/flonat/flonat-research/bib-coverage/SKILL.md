---
name: bib-coverage
description: "Compare a project .bib against a Paperpile project/topic folder to find uncited papers or unfiled entries. Use when the user asks to compare a project .bib against a Paperpile project/topic folder to find uncited papers or unfiled entries."
allowed-tools: Read, Glob, Grep, Bash(paperpile*)
argument-hint: "[project-path or tex-file]"
---

# Bibliography Coverage

**LIBRARY-FIRST RULE: ALWAYS check Paperpile (`paperpile search-library`) when assessing coverage.**

Compare a project's `.bib` file against a Paperpile project/topic folder to identify gaps between the project bibliography and the reference library.

## When to Use

- After a literature search, to see what % of the topic collection is cited
- Before submitting a paper, to catch references you forgot to cite
- When reviewing a Paperpile project/topic folder, to find items not yet in any project's `.bib`
- After a bibliography-quality check, as a complementary completeness check

## When NOT to Use

- **Finding new references** — use an installed literature-discovery workflow or scholarly search
- **Validating .bib quality** (missing fields, DOI issues, preprint staleness) — use an installed bibliography validator
- **Building a .bib from scratch** — use `bib-parse` or an installed literature workflow

## Inputs

1. **Project `.bib` file** — detected automatically (same logic as `bib-validate`: look for `references.bib`, then any `.bib` in the project)
2. **Paperpile folder** — resolved from:
   - Explicit `--topic <slug>` argument
   - Project's `CLAUDE.md` or Atlas topic frontmatter
   - Directory name if inside a research project
   - If no collection can be resolved, report an error and suggest specifying `--topic`

## Workflow

### 1. Load Project Bibliography

Parse the `.bib` file to extract all entry keys and titles.

### 2. Load Paperpile Folder

1. Call `paperpile get-folders` to find the relevant full topic path
2. Call `paperpile get-items-by-folder "<full path>"` to get items in that folder
3. Extract item keys (citekey) and titles

Paperpile's `labelsNamed` and `foldersNamed` are distinct. Project/topic
collections use folders. If a leaf occurs under multiple parents, stop and
request or derive the full path; never silently choose one.

**Graceful degradation:** If the `paperpile` CLI is unavailable, skip with a warning — report .bib-only stats.

### 3. Compare

Produce three lists:

| Category | Description | Action |
|----------|-------------|--------|
| **Cited + In Folder** | Items in both `.bib` and the Paperpile folder | No action — healthy |
| **Cited but Not in Folder** | Items in `.bib` but not in the Paperpile folder | Needs filing in Paperpile |
| **In Folder but Not Cited** | Items in the Paperpile folder but not cited in any `.tex` | Potential references — review for inclusion |

### 4. Coverage Stats

```
## Coverage Report

**Paperpile folder:** [full path] ([N] items)
**Project .bib:** [M] entries

| Metric | Count | % |
|--------|-------|---|
| Cited + In Folder | X | X/N |
| Cited but Not Filed | Y | — |
| In Folder, Not Cited | Z | Z/N |
| Coverage (cited/folder) | — | X/N% |
```

### 5. Recommendations

Based on the results:

- **Low coverage (<50%):** "The project cites few papers from the topic collection. Consider reviewing uncited items for relevance."
- **Many unfiled citations (>5):** "Several cited papers aren't in the topic collection. Reconcile them with the configured reference manager."
- **High coverage (>80%):** "Good coverage of the topic collection."

## Report Format

```
## bib-coverage: [Project Name]

**Topic:** [slug] | **Collection:** [name] ([N] items) | **Bib:** [filename] ([M] entries)

### Coverage: X/N (XX%)

### Cited but Not in Collection (need filing)
| # | Key | Title | Year |
|---|-----|-------|------|

### In Collection but Not Cited (potential references)
| # | Key | Title | Year |
|---|-----|-------|------|
```

## Phase 6 (Optional): Gap Discovery via Recommendations

When coverage is low (<50%) or the user says "find what I'm missing", use the S2 Recommendations API to discover papers that should be in the collection but aren't.

1. **Select seed papers** — pick the 3-5 most-cited papers from the `.bib` file
2. **Get recommendations** — run `scholarly scholarly-similar-works <paper_id> --json` for each seed paper to get ML-based similar paper suggestions
3. **Filter against existing** — remove papers already in the `.bib` or Paperpile folder
4. **Rank by relevance** — sort by citation count and recency
5. **Present candidates** — show a table of recommended additions with titles, years, citation counts

**Dispatch rule.** If ≥5 seed papers are selected, dispatch a single Explore sub-agent that runs `scholarly scholarly-similar-works` for each seed and writes merged candidates to `/tmp/bib-coverage-similar.json`. Main context reads only the merged result. For 3–4 seeds, inline calls are fine. See [`_shared/cli-dispatch-policy.md`](../_shared/cli-dispatch-policy.md).

This turns a passive coverage check into an active discovery tool — finding papers the researcher should know about based on what they already cite.

## Cross-References

- **Installed bibliography validator** — Quality validation (missing fields, DOIs, preprints). Run alongside coverage for a complete check.
- **Installed literature workflow** — Discovery of new references. Coverage identifies gaps in existing collections.
- **`bib-parse`** — Extract citations from PDFs. Run coverage after parsing to see overlap with the topic collection.
- **`shared/reference-resolution.md`** — Topic collection resolution logic
