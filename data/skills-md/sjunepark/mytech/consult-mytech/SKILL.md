---
name: consult-mytech
description: "Consult mytech technical preferences to guide a coding task or assess a project's alignment. Explicit invocation only."
---

# Consult Mytech

Use the current mytech guidance to inform the consuming project's task. Keep
mytech as the source of preferences and the consuming project as the source of
requirements and implementation evidence.

Requires read access to the consuming project and the mytech repository at
`https://github.com/sjunepark/mytech`. The repository is an external input;
preferences are not bundled with this skill.

## Locate the guidance

Use a mytech checkout identified by the user, project instructions, or
`MYTECH_ROOT`. Otherwise check known workspace locations and an existing
repository cache for a checkout with the matching Git remote. Do not assume
the skill's installation directory is inside mytech.

If no checkout is available, read the repository through an available Git or
repository API using the environment's external-repository conventions. Use
one consistent revision. If access fails or the source is ambiguous, report
the missing source and ask only for what resolves it; continue independent
project work without claiming a preference check.

Inspect a local checkout as it stands, including relevant uncommitted guidance.
Record the source location, revision when available, and whether consulted
files have local changes. Do not update, reset, or switch its checkout merely
to read preferences. A local read does not establish freshness against remote.

## Read for the actual decision

1. Establish the task's scope from the request and the consuming project's
   instructions, requirements, and relevant implementation. A focused task
   calls for a focused check; an explicit project assessment calls for coverage
   of its material decisions.
2. Start with mytech's `README.md` and follow its guidance index to the documents
   relevant to those decisions. Inspect further project evidence as needed to
   determine applicability. Search narrowly when the index does not resolve a
   topic; do not load the whole repository.
3. Use accepted guidance as defaults. Check status and applicability in the
   owning document. Drafts are proposals, references supply evidence, and
   history explains changes; consult those only when the task needs them and
   label their role. A provenance project name does not prove current adoption.
4. Read the selected preferences, rationale, constraints, and revisit
   conditions before applying them. Preserve links to the owning documents
   instead of copying a catalog of preferences into this skill or the project.

## Check and apply

Compare each relevant preference with concrete project evidence. Distinguish
alignment, an actionable gap, a justified deviation, and insufficient evidence.
If no accepted guidance covers a decision, say so rather than inventing a
mytech preference.

Project requirements and local instructions take precedence. A preference can
break a tie; it does not justify a rewrite or stack migration by itself. Explain
material conflicts using the project's constraints and the guidance's rationale.
Document an intentional deviation in the consuming project's owning decision
document when edits are authorized; for an assessment-only task, report the
rationale and proposed documentation instead.

Consultation does not expand the underlying task's authority. For advice or
review, report the assessment. When implementation is already requested, use
applicable preferences in that work, preserve unrelated changes, and perform
the project's checks for changed behavior. Do not turn a focused task into
repository-wide remediation or edit mytech as a side effect of consultation.

## Complete the consultation

Give a concise result that identifies:

- the inspected mytech source and the scope checked;
- the relevant owning documents, linked alongside decisions or findings;
- material gaps, justified deviations, and unknowns, with project evidence;
- changes and validation performed when implementation was authorized.

Finish when the scoped decisions have dispositions supported by inspected
guidance and project evidence. State coverage limits; do not imply that a
focused check certifies the whole project.
