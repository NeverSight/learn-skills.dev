---
name: jinko-context
description: >-
  Explain core Jinkō context, navigation, version management, and domain language for agents and users. Use this skill whenever the user needs a mental model of Jinkō projects, folders, project items, snapshots, references, extracts, highlights, protocols, trials, calibration, virtual populations, traceability links, or modeling context; when translating between generic terms and Jinkō terminology; or when an agent needs orientation before navigating or modifying Jinkō artifacts. It includes a safe SDK example to list folders, render their tree, and create a folder after explicit user confirmation. Use dedicated jinko-* workflow skills for creating or editing scientific artifacts.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Folder creation requires write access to the Jinkō project.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.16,<2.0"
license: MIT
---

# Jinkō Context

Use this skill to explain Jinkō's shared mental model and vocabulary. Keep answers practical: the goal is to help a user or agent navigate Jinkō artifacts without confusing project organization, scientific content, and immutable versions.

> **PREREQUISITE:** The folder-management example needs an initialized `jinko-sdk`
> connection and an SDK satisfying its `metadata.requires_sdk` range. Run the
> `jinko-sdk-setup` skill (`../jinko-sdk-setup/SKILL.md`) and proceed only once
> its check passes. A session code can be exchanged only once, so call
> `get_session_code` again before this skill's own SDK process. If that skill
> is not found, install it from `novainsilico/jinko-skills`.

## Navigation and Version Management

Jinkō project navigation behaves much like working in a Git repository, but for scientific modeling artifacts instead of source-code files.

- A **Project** is like the repository: it is the boundary for a concrete scientific modeling effort, including references, data, models, protocols, trials, reports, and collaboration history.
- **Folders** are like repository directories: they organize related project items by workflow, experiment, disease area, evidence package, or analysis thread. The folder API is an organizational surface; a folder is not a Project Item.
- **Project Items** are like tracked files or domain objects in the repository: each item has an SID and represents a Jinkō artifact such as a model, protocol, trial, data table, reference, output set, or document.
- **Snapshots** are immutable states exposed by versioned Jinkō core-item APIs. The latest state is head. Do not assume every Project Item type exposes snapshots; use the resource's SDK/API surface to determine whether snapshot identity exists.

This Git-like structure makes Jinkō easier for agents to navigate because agents can separate three questions:

- Where is the work organized? Look at the project and folders.
- Which artifact is being discussed? Identify the project item.
- Which exact state of a versioned artifact matters? Use its explicit version or snapshot surface, or use head when the user wants the latest state.

Use `Project`, `Project Item`, and `Snapshot` rather than generic words like workspace, file, upload, save, version, revision, or commit unless you are explicitly making the Git analogy.

## Domain Language

**Project**:
A concrete scientific modeling effort with its own References, data, modeling artifacts, and reports.
Avoid: workspace, case, study folder.

**Folder**:
An organizational container inside a project used to group related project items. Folders support navigation and workflow hygiene; they do not replace item identity or snapshot identity.
Avoid: Project Item or directory when speaking to end users unless making the Git analogy.

**Project Item**:
A named Jinkō object inside a project, such as a Reference, model, protocol, trial, data table, output set, or document. Its SID is the preferred user-facing identity. Versioned types can retain that identity across versions.
Avoid: file, asset, object when precision matters.

**Snapshot**:
An immutable state of a Jinkō model, protocol, trial, or other resource whose core-item API exposes snapshots. It enables exact version access; it is not a universal property of folders or every Project Item type.
Avoid: revision, save, version, commit except when explaining the analogy.

**Reference**:
A Project Item that holds a source PDF, usually a scientific paper, and its bibliography metadata, such as the DOI. It is the evidence for extraction and modeling. The Jinkō API type name of this item is `Source`.
Avoid: source, document, file, upload. Use `Source` only for the API type name.

**Extract**:
A Project Item that holds one selected textual, rectangular, formula, or data-table object from one Reference. It can carry a formulation that states the evidence, such as a parameter value, clinical endpoint, or mechanism statement, and a classification (Statement, Hypothesis, or Data).
Avoid: note, snippet, untracked fact.

**Highlight**:
A located piece of evidence inside an Extract. It links to its position in the Reference PDF. A Highlight is not a Project Item.
Avoid: annotation, quote.

**Model**:
A Jinkō-compatible executable representation of the biological or pharmacological mechanism being modeled.
Avoid: model file, script.

**Protocol**:
The Jinkō artifact that defines trial arms, interventions, dosing or treatment conditions, and simulation timing.
Avoid: study design, scenario file.

**Trial**:
The Jinkō artifact that combines a protocol, model, output sets, and data tables for simulation or comparison.
Avoid: run, simulation setup.

**Calibration**:
The stage that adjusts model parameters so simulations fit selected experimental evidence.
Avoid: fitting, tuning.

**Calibration Candidate**:
A model-intrinsic parameter proposed for calibration. It may be marked with a `toCalibrate` model tag.
Avoid: free parameter, tuned knob.

**Virtual Population**:
A generated population of parameterized virtual subjects used for in-silico trial execution.
Avoid: cohort, sample.

**Traceability Link**:
The link from a model, dataset, or report assertion back to the Extract, Reference, or explicit assumption that justifies it.
Avoid: reference (that term names the Project Item), citation, provenance.

**Modeling Context**:
The full scientific, protocol, trial, Reference, and artifact background needed to build or refine a Jinkō Model.
Avoid: extraction catalog, model input bundle.

## Relationships

- A **Project** contains one or more **Project Items**.
- A **Folder** organizes Project Items within a Project.
- Some versioned **Project Items** expose **Snapshots** through their core-item APIs.
- A **Snapshot** captures one immutable core-item state; consult the resource API rather than assuming one exists.
- A **Reference** supports one or more **Extracts**.
- An **Extract** comes from one **Reference** and holds its evidence as one or more **Highlights**.
- A **Highlight** links to its position in the Reference PDF.
- A **Model** represents executable biological or pharmacological mechanisms.
- A **Protocol** defines arms, interventions, and timing used by a Trial.
- A **Trial** uses a **Protocol**, a **Model**, output sets or measures, and optional transformed data overlays.
- A **Calibration** uses selected evidence and outputs to adjust Calibration Candidates.
- A **Virtual Population** provides parameterized virtual subjects for Trial execution.
- A **Traceability Link** connects Project Items, Model components, Trial outputs, data tables, and reports back to Extracts, References, or explicit assumptions.
- A **Modeling Context** gathers the relevant References, Extracts, Traceability Links, Models, Protocols, Trials, and reports needed to make a modeling decision.

## Response Guidance

- Translate user language into Jinkō language when it improves precision.
- Preserve the Git analogy for orientation, but do not imply Jinkō is literally Git.
- Distinguish stable SID identity from immutable snapshot identity where that resource exposes snapshots.
- Use head/latest only when the user wants the current state; name snapshots when exact reproducibility matters.
- When the user needs to inspect, create, or change folders, read `references/folder-management.md` and use its bundled script or the SDK calls it names rather than improvising API calls.
- Route implementation tasks to the relevant skill: `jinko-reference`, `jinko-model`, `jinko-protocol`, `jinko-trial`, `jinko-vpop`, `jinko-data-table`, or `jinko-sdk-setup`.
