---
name: genchi-genbutsu
description: "Inspect the real repository, environment, dependencies, and runtime evidence before designing or changing software. Use for greenfield construction, unfamiliar codebases, uncertain behavior, or any task where assumptions could create rework."
---

# Genchi Genbutsu

Genchi genbutsu means going to the source. In software, make decisions from
the actual repository, environment, runtime behavior, and authoritative
documentation instead of from memory or plausible-looking generated output.
This is a Japanese-inspired engineering metaphor, not a cultural universal.

## Use this skill when

- the codebase or toolchain is unfamiliar;
- a project is being built from scratch;
- the request references behavior that has not been observed;
- an API, dependency, framework, or command is uncertain;
- a bug or performance issue needs evidence; or
- a previous attempt relied on assumptions and created rework.

## Outcome

Produce a bounded reconnaissance report with:

- the relevant repository or environment surface;
- existing implementations, consumers, and conventions;
- commands, tests, builds, or runtime observations used as a baseline;
- constraints and failure boundaries;
- facts separated from inference;
- unknowns that still need resolution; and
- the narrowest safe seam for the next change.

For greenfield work, the report covers the domain, users, deployment target,
available services, language and toolchain constraints, operational ownership,
and the smallest behavior worth proving first.

## Workflow

### 1. Map the surface

Inspect the directory structure, entrypoints, package manifests, lockfiles,
configuration, schemas, routes, commands, tests, and deployment files relevant
to the request. Search before creating a new helper, module, route, or service.

### 2. Trace behavior

Follow the relevant input through callers, transformations, side effects,
storage, external calls, and failure paths. Identify who depends on observable
behavior, including behavior that is not documented.

### 3. Establish a baseline

Run the narrowest useful existing check: a reproduction, focused test, type
check, build, benchmark, health check, or representative command. Record the
exact command and result. If no check exists, state that explicitly and create
the smallest observation needed to reduce uncertainty.

### 4. Verify external facts

Read the project's actual usage and authoritative dependency documentation when
behavior is uncertain. Never invent an API from a familiar name or copy a
snippet without reconciling versions and local conventions.

### 5. Report and stop

Return only findings relevant to the request. Name the evidence, assumptions,
unknowns, risks, and recommended next seam. Do not begin unrelated cleanup
because reconnaissance exposed it.

## Evidence standard

Every important claim must be traceable to a file, command, test result,
runtime observation, or authoritative source. Say `not verified` when evidence
is missing. A clean report is more valuable than a confident guess.

## Boundaries

- Do not read the entire repository when a bounded slice answers the question.
- Do not treat comments, issue text, or AI output as stronger than behavior.
- Do not modify code during reconnaissance except for a clearly labeled,
  minimal probe that is required to observe the system.
- Do not convert an absence of evidence into evidence of absence.

## Handoff

Hand the next engineer a compact map of the system and a baseline they can
rerun. Recommend `nemawashi` if intent remains unclear, `kanso` if design
choices remain, or `kata` when the next slice is ready to implement.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
