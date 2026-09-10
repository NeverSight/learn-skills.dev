---
name: jinko
description: >-
  Discover and route Jinkō QSP and mechanistic-modeling requests to the public
  Jinkō skill that owns the work. Use when the user is starting a Jinkō session,
  asks what capability or skill to use, describes a multi-area modeling request,
  or has not yet identified the relevant jinko-* or jinko-task-* skill. This
  skill does not make scientific decisions, plan workflows, execute SDK calls,
  or decide that a task step is complete.
metadata:
  author: Nova In Silico
license: MIT
---

# Jinkō Skill Router

Identify the user's immediate intent and load the narrowest published owner.
Do not reproduce its mechanics. Task skills own task-level decisions and
orchestration; resource skills own reusable Jinkō SDK/API mechanics.

## Routing Map

- Connection and credentials: `jinko-sdk-setup`.
- Terminology and navigation: `jinko-context`.
- Product capabilities and model-library discovery: `jinko-solution-and-product-guide`.
- Publication discovery: `jinko-task-literature-search`.
- ClinicalTrials.gov discovery: `jinko-task-trial-data-scoping`.
- Reference PDFs and source extracts: `jinko-reference`.
- Evidence-to-table extraction: `jinko-task-extract-data-table`.
- MATLAB/SimBiology export and solver parity: `jinko-task-export-to-matlab`.
- NONMEM model and trial conversion: `jinko-task-from-nonmem`.
- Data-table mechanics: `jinko-data-table`.
- Model mechanics: `jinko-model`.
- Calibration-input classification: `jinko-task-define-param-to-calibrate`.
- Confirmed CMA-ES execution: `jinko-task-cmaes`; SDK mechanics: `jinko-calibration-cmaes`.
- Protocol mechanics: `jinko-protocol`.
- Virtual-population mechanics: `jinko-vpop`.
- Trial mechanics: `jinko-trial`.
- Trial visualization mechanics: `jinko-trial-viz`.
- Document mechanics: `jinko-document`.

If a request spans several areas, state which owner applies to the immediate
request and let that skill determine its own prerequisites or handoffs. Do not
invent a project plan, artifact checklist, stage order, or completion gate here.

## Missing Capabilities

The public skills are an interdependent plugin bundle. If a named owner is not
available, direct the user to install or update the complete Jinkō plugin from
`novainsilico/jinko-skills`, then start a fresh session or reload plugins. Do not
recommend installing one skill in isolation.

## Resource Links

When an owner returns a resource, surface its SDK-provided `.url` or returned
resource URL. Never construct a link from a SID and a hard-coded hostname;
configured `JINKO_URL` and on-premises application URLs must be preserved.
