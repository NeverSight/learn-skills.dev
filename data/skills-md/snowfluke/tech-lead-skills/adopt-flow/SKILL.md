---
name: adopt-flow
description: Bring a running project onto the tech-lead flow. Audits which flow documents the repository already has, in folder or older single-file form, then runs the skills that write the missing ones in order, each in its adopt mode, so they describe the system as built. Writes no retroactive user stories; new work enters through grill-me, to-prd, and to-issues. Use when a tech lead joins or takes over an existing codebase, or the user wants to adopt this flow on a project that already runs.
---

# Adopt Flow

The entry point for a project that already runs. It documents the system as it
is, going forward only. It does not write stories for features that already
shipped.

`scripts/audit.py` sits next to this `SKILL.md`. Call it by absolute path,
because the shell runs in the project. It needs only `python3`.

## 1. Audit

```bash
python3 <this skill's dir>/scripts/audit.py <repo root>
```

It prints one row per flow document: where it was found, the skill that owns
it, and its status. Then it prints the skills to run, in order. If it reports
"Running project: no", stop. This is a new project; point the user at
`product-discovery`.

Show the table to the user. Confirm the run order, and ask which documents they
want to skip. `api-spec` does not apply to a project with no API.

## 2. Run the missing skills in order

Run each skill from the audit's list, one at a time. Each one detects the
running project and uses its adopt mode. The document skills read the code and
describe what exists. `tech-lead-setups` adds only the missing tooling, such as
the test harness. It shows as `check` in every audit, so run it once.

- A document marked "present, older single file" or "older layout" stays as it is. The owning skill offers to migrate it only when you run that skill for another reason.
- Collect every finding the skills report: gaps, inconsistencies, missing controls.
- After each skill, run the audit again, so the next step starts from the real state.

Skip these, because they write the history of a project that already exists:
`product-discovery`, `grooming`, `us-ac-formatter`, `task-breakdown`.
On the first new feature, `to-prd` and `to-issues` extend the business docs
and the board where they exist, in their current layout. They create
`docs/business/` and `docs/task-breakdown/` only when the project has neither
in any form.

A document that exists in its own layout is the source of truth. Extend it in
that layout. Offer migration once. Never start a second document of the same
kind next to it.

## 3. Report

- The documents written, with their paths.
- The findings from every skill, grouped by document. Each one is a candidate first card.
- What comes next: new work enters through `grill-me`, then `to-prd`, then `to-issues`.
