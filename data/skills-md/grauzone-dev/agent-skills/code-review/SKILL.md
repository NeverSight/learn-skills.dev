---
name: code-review
description: Two-axis review of a change set against repository standards and its originating spec. Use when reviewing a diff, branch, or pull request before merge.
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Code review

Two-axis review of the change set since a fixed point through the current working tree:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

## Process

### 1. Pin the change set

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it. Confirm it resolves with `git rev-parse <fixed-point>`.

Capture the merge base once: `git merge-base <fixed-point> HEAD`. The change set is:

- tracked changes, including committed and work-in-progress: `git diff <merge-base>`
- untracked files: `git ls-files --others --exclude-standard`, each reviewed as an added file

Record the commit list against that same merge base: `git log <merge-base>..HEAD --oneline`. Stop only when every part of the change set is empty.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the recorded commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.). When found, read `docs/agents/issue-tracker.md` and fetch them by its workflow; if the contract is absent, continue with the remaining sources.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Gather standards

Find every repository source that governs how code is written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`. Read [smells.md](references/smells.md) and apply its baseline unless a repository standard overrides it.

### 4. Spawn both sub-agents in parallel

**Standards sub-agent prompt** — include:

- The complete change-set commands and recorded commit list.
- The standards-source files and the full baseline from `references/smells.md`.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls — documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** — include:

- The complete change-set commands and recorded commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings.

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

**Complete when:** every changed and untracked file has been reviewed against every applicable standards source and the spec when available, and the separate Standards and Spec reports are returned.
