---
name: diagramming-processes
description: Use when a business process, workflow, lifecycle, or interaction between systems needs a diagram - a flow that prose serializes badly, a state machine, a message sequence, an enterprise process map - or when drawing the process documentation of a legacy campaign. Encodes diagrams-as-source, the notation ladder from ArchiMate to PlantUML, the kind-per-question table, behavior-level participants, the diagram index, and the same-change maintenance rule. Use whenever a document needs a graph rather than more paragraphs, even if nobody says "PlantUML".
---

# Diagramming processes

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

A diagram is a set of claims drawn instead of written; every box and arrow is bound by the same truth rules as a sentence. Core principle: **diagram the behavior (processes, lifecycles, interactions), keep the source in version control, and treat every render as derived.** The prose owns the reasoning; the diagram carries what prose serializes badly: branching, concurrency, and state.

## When to invoke, and not

Invoke when a flow, lifecycle, or interaction needs showing: a business process spanning components or organizations, a state machine, a message exchange, the `processes.md` of a legacy campaign (`documenting-legacy-codebases`). Do NOT invoke to decorate: a linear flow of three or four steps is a numbered list, and a diagram restating one is furniture. Out of scope: charts generated from data (metrics, trends), and implementation structure, which the behavior rule below forbids.

## The notation ladder

Name the altitude before drawing, and match the notation to it:

- **Business layer: ArchiMate.** Processes spanning departments, organizations, or multiple systems, capability maps, and the TOGAF-style views enterprise stakeholders expect. The audience reads roles, services, and processes, never components.
- **System layer: PlantUML behavior diagrams.** Flows, state machines, and sequences within and between systems: code documentation, one level above the code.
- **Code layer: no diagrams.** Class and package structure is the code's own to show; an IDE generates a fresher picture on demand than any committed one.

The ladder sets the notation and the vocabulary, never the tool: one toolchain can serve both rungs, because PlantUML carries the ArchiMate notation in its standard library. The tool a repository uses is settled once, under "Source, not pictures".

## Source, not pictures

- The source is committed text, in the diagram tool the repository already uses. Where none is established, PlantUML is the default (rich standard library, ArchiMate included); where the choice is genuinely open, ask the owner, recommending PlantUML. The core skill's `references/truth.md` owns the ground rule: rendered output is derived, and stale renders are deleted rather than left to mislead.
- One diagram per source file, named for the process it shows, grouped in one diagrams directory beside the documents.
- Rendering requires tooling the repository owns (a script, a make target, or a build step), set up by the owner, not by the diagram's author. Tell the owner when it is missing; never route around the gap by picking whatever notation the hosting platform happens to render inline.
- One repo command renders everything; renders are committed unless the host already renders the repository's chosen source format. When a source changes, its outdated render is deleted in the same change, and the missing render is recorded in the index until regenerated.
- A screenshot, an exported picture, or a whiteboard photo with no source is a finding against the document that contains it: nobody can diff it, so nobody will maintain it.

## The kind answers the reader's question

Pick the kind from the question the reader brings, one question per diagram:

| The reader asks | Draw |
|---|---|
| How does this process run across the organization | ArchiMate business process view |
| What happens, in what order, with which decisions | Activity diagram |
| Which states can this thing be in, and what moves it | State machine |
| Who talks to whom, in what order, with what messages | Sequence diagram |
| What exists in this domain and how it relates | Concept diagram, at business-object level |

A diagram answering two questions answers neither; split it. A diagram that needs a legend of its own invented symbols is answering too many at once.

## Behavior, never implementation

The refactor test from `documenting-legacy-codebases` governs diagrams too, and a diagram hides its drift better than a paragraph does:

- **Participants are systems, roles, modules, and business objects.** Classes, methods, and functions stay in the code (see the ladder).
- **Edges carry the event or condition, in the domain's language**: "payment confirmed", never a callback name. A guard may name a config key, because config keys are contract surface; it never names a method.
- **Titles name the process**, never a spec, phase, or plan: the no-delivery-narrative hard rule applies inside diagram source too, including comments.
- **Error and exception paths are drawn where behavior differs**, and drawn distinguishably; a happy-path-only diagram of a process with real failure branches is an overstated claim.
- **Quirks are drawn, and are content.** The state nothing can leave, the flow that skips a step for one input: the surprising branch is why the diagram earns its place (`documenting-legacy-codebases`, quirks).

## The diagram index

More than five diagrams get one index document beside them, a derived artifact rebuilt from the files (core truth rules):

- A coverage table: what each diagram shows, its source file, its render if committed, and its status.
- Per diagram, the module it describes, as the drift anchor: the one place a diagram points at code.
- The render command, so the index is also the build instruction.
- Pending renders, named per source, so a missing render is a tracked state rather than a silent gap.

## Maintenance

A change that alters a flow updates the matching diagram source in the same change: a diagram is documentation, and documentation is part of done (core truth rules). Rendering is the diagram's compile step: source edits break syntax invisibly, and the break surfaces only when the render runs. The author renders before shipping the edit; where the repository's pipeline is still missing, a local one-off run of the tool satisfies this check. When a feature is removed, one change covers the prose, the diagram source, the index row, and the committed render. A diagram nobody can bring themselves to update is answering too big a question; split it along the seams that change independently.

## Verification

Everything legible in a diagram is a claim (core truth rules), so a diagram is grounded and reviewed like prose:

- The author verifies every box, arrow, and guard against the code before drawing it. A flow inferred rather than confirmed is labeled as inference beside the diagram in the embedding document, never silently drawn as fact.
- The reviewer reads the diagram against the behavior, and reviews the source text rather than the picture: the source is what the next editor changes.
- Diagram sources drift like prose and join every legacy campaign: the campaign (`documenting-legacy-codebases`) grounds the diagram sources with the documents that embed them.
- A diagram and its surrounding prose share one home per fact: the prose says why the process exists and what to look out for, the diagram shows the flow, and neither restates the other step by step.
