---
name: wtk-setup
description: Set up, assess, or update a project's WTK guidance through source discovery and a focused policy/driver-skill interview. Use for project harness requests; not feature implementation or automatic installation.
license: CC-BY-4.0
metadata:
  author: Antonio Fulgêncio
  version: '1.0.0'
---

# Project harness setup

Produce a small project-owned contract whose adopted requirements reach feature planning and
independent verification. Installation only distributes this skill; setup changes guidance only
within the user's authorized request. An assessment is read-only and ends with findings and a
proposed delta. Do not install skills, provision runtimes, change applications, or infer or expand
delivery authority. Record explicitly authorized delivery decisions in their project owners.
Do not require native agent files, a new CLI or a machine-readable policy registry.

Before editing instructions, read [context budget](../wtk/references/context-budget.md). For the
inheritance contract and missing-source dispositions, read
[project requirements](../wtk/references/project-requirements.md#discover-applicability).

## Discover owners and evidence

Inspect root and scoped instructions, their conditional routing, product/architecture decisions,
existing guideline owners and directory convention. Follow the relevant sources and compare
representative implementation, tests and enforcement commands. In a blank project, record what is
absent rather than inventing conventions. In an existing project, identify stale pointers,
contradictions and unsettled policies even when driver bindings already exist.

Inspect the host's actual available skill metadata and project bindings across relevant areas.
For a proposed driver, read the instructions needed to establish its responsibility and limits.
One skill may cover several concerns; relevant skills need not have standard names. Distinguish
availability, adopted responsibility and ability to execute proofs. Do not claim runtime evidence
from a catalog entry or recommend an unavailable skill as though it were installed.

Classify findings as **adopted rule**, **observed pattern**, **proposal**, or **conflict**, citing
their sources. Name unavailable evidence separately. Use the project's precedence to resolve only
what existing authority settles; an observed convention or specialist recommendation is not adoption.
Discovery is complete when relevant owners, current decisions and material gaps are known well
enough to ask focused questions, not after an exhaustive repository audit.

## Interview unresolved responsibilities

Read [the area menu and baseline](references/interview.md). Select relevant areas from the project
and requested scope, including cross-cutting security. Propose a small baseline for adoption, then
ask only material unsettled policy and driver questions. Reuse explicit decisions from the current
session and existing adopted guidance; an existing driver choice does not answer an unsettled
policy question.

For each unsettled driver responsibility, present relevant actually available skills, what planning
must read from each, a recommendation and its limit. Ask the user to choose or confirm; keep frontend,
backend, security, architecture, database and other relevant responsibilities independently visible.
One answer may settle several areas. If no skill fits, identify whether existing guidance suffices
or policy, expertise or proof capability is missing; apply the shared gap dispositions before
dependent claims. Never silently substitute for a selected required driver.

Reuse existing guideline owners and locations first. Only when none exists, propose
`docs/guidelines/`; allow a user-selected alternative. Interview completion means each material
choice is adopted within existing authority, explicitly delegated, or classified as an unresolved
gap with dependent work and release condition. Do not treat silence or the starter baseline as adoption.

## Propose or apply the guidance delta

Show the concrete additions, edits, retired stale routes and unresolved decisions. For an assessment,
stop with the proposal and leave project files untouched. For authorized setup/update, apply settled
decisions within scope; ask only for missing decisions or new authority, not approval already given.

Keep root instructions limited to authority and conditional routing. Each adopted rule has one owning
source, a first-line trigger, an observable outcome and an evidence approach. Route by role, phase
and affected concern together; cross-cutting obligations must reach planners and Verifiers as well
as builders. Link procedures instead of copying them into guidelines. Create only applicable
documents at the selected project location, never an empty topic tree or a duplicate rule store.
Native role files remain optional; project routing works without them.

Connect the project routing to the shared
[requirement inheritance procedure](../wtk/references/project-requirements.md), which both WTK paths
use. Keep the project's adopted policies in its own documents, not inside distributed skills.

On rerun, compare policies, sources, skills and runtime assumptions with existing bindings. Preserve
equivalent decisions and owners without repeated settled questions. Repair or retire stale pointers
within authority, preserve unaffected policy, and ask about materially changed responsibilities.
A missing source/required driver exposes its dependent requirement before any successful-load claim;
an unresolved authority conflict never broadens delivery permission.

## Finish

Report **proposed**, **unresolved**, or **applied** with the scoped delta, source locations, adopted
decisions, driver responsibilities and remaining gaps; mixed results may use more than one
disposition. State what inspection or execution supports each claim. Check changed metadata,
links/routing and the project's relevant existing validation under
[validation](../wtk/references/validation.md). For authorized local edits/commits, follow
[evidence](../wtk/references/evidence.md); assessment-only requests make no project edits or commits.
Do not claim application compliance, measured reliability improvements, or a security certification
from this setup exercise.
