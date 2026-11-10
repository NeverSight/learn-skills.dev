---
name: check-refs
user_invocable: true
description: Match references in a LaTeX paper against academic databases, flag entries that need review, and suggest missing DOIs or URLs. Use when checking citations or preparing a paper for submission.
---

# Check citation references

Match a LaTeX paper's references against academic databases with `bibsleuth`. Database matches support bibliographic verification but do not prove that a citation supports the manuscript's claim.

## Workflow

Use user-provided paths when available. Otherwise, identify the manuscript entrypoint from the project's build configuration and TeX structure, then resolve its bibliography declarations. Ask only if multiple plausible papers remain.

Run the database-only check by default:

```bash
uvx bibsleuth check <TEX_FILE> --bib <BIB_FILE> --no-llm
```

`uvx` supplies the tool without a separate installation step. Allow enough time for large bibliographies and use asynchronous execution when the harness supports it.

Read the generated `bibsleuth-report.md`. Prioritize unverified and error results, summarize suggested DOI or URL patches, and link the full report. Apply patches only when the user requested reference repair or approves the proposed edits, then check the diff for unintended bibliography changes.

For claim-level analysis, missing-citation suggestions, and contradiction searches, run the LLM mode only when the user requests it and accepts the additional model-provider exposure:

```bash
uvx bibsleuth check <TEX_FILE> --bib <BIB_FILE>
```

If the user explicitly requested full analysis at the outset, do not force a redundant `--no-llm` pass first. Present suspected miscitation and literature findings as items for review, not established errors.
