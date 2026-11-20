---
name: code-review
description: >
  Review a code change on three independent lenses — correctness, standards,
  spec — plus security when the diff touches a trust boundary, run as parallel
  sub-agents, reporting findings with severity, confidence, and file:line
  evidence. Use before shipping a branch or PR, or
  when glen-mode asks for a review. Not for documents, bug hunts, or applying
  fixes.
argument-hint: "[fixed-point] [spec path]"
---

# Code review

Review the change, not the author's taste. A finding earns its place by naming
a consequence: broken behaviour, a violated rule, or a missed requirement.

The lenses are **independent**: a change can meet the spec and be wrong, be
correct and break the repo's conventions, or follow every convention and build
the wrong thing. Each lens reports under its own heading, in its own order,
with its own severities, so the same line can appear under two lenses.

## Process

### 1. Pin the fixed point

The commit, branch, tag, or ref the user names; if they name none, ask.

```bash
git rev-parse <fixed-point>
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

Stop if the ref does not resolve or the diff is empty.

### 2. Find the spec

First hit wins: issue references in the commits (`#123`, `Closes #45`,
`!67`); a path the user passed; a spec under `docs/`, `specs/`, or the
project's own spec path. Otherwise ask. No spec means the Spec lens is skipped.

### 3. Find the standards

Collect the files that say how code is written here: `CODING_STANDARDS.md`,
`CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, style guides, ADRs binding the
changed area.

### 4. Write the intent

Three lines from the commits and spec: what the change makes true, and what it
deliberately leaves alone. It keeps reviewers from inventing requirements.

### 5. Check for a trust boundary

The Security lens runs only when the diff touches a trust boundary: parsing or
validating outside input, authentication or authorisation, secrets or
credentials, network or file-system access driven by input, deserialisation,
SQL, shell, HTML, or paths built from input, permissions, or crypto. Decide from
the diff. Name the boundary with its file:line, or state that none was touched.

### 6. Dispatch

Issue the sub-agent calls together, foreground, each with fresh context:
Correctness and Standards always, Spec only when step 2 found one, Security
only when step 5 named a boundary. Each call gets its brief from
[`references/lenses.md`](references/lenses.md) plus the inputs listed there.

### 7. Validate and report

Follow [`references/report.md`](references/report.md): validate each lens's
findings, then fill the template. Done when every returned finding is either in
the report with its cite opened, or named as dropped in Coverage, and every
skipped lens is named with its reason.

Report only. Fixes, commits, pushes, branch switches, and issues wait for a
separate request.
