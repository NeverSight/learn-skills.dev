---
name: architecture-design-document
description: Scan an entire .NET repository (.NET 8–10, ASP.NET Core, workers, class libraries) and generate a professional Architecture Design Document as a Word (.docx) file, illustrated with rendered diagrams (system context, containers, components, sequences, ER model, deployment) whose editable sources (Mermaid .mmd and draw.io files) are exported to a diagrams/ subfolder. Use this skill whenever the user asks for an architecture document, design document, solution/system documentation, technical documentation, onboarding documentation, "document this codebase/solution", or any deliverable describing how a .NET system is designed — especially when they mention Word, docx, or diagrams.
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 solutions
  requires: Python 3.9+ with python-docx; internet access or local mermaid-cli for diagram rendering
---

# Architecture Design Document (.NET)

Produce a complete, professional Architecture Design Document (ADD) for a .NET
solution: a styled Word document with cover page, table of contents, and
evidence-based content, illustrated by diagrams that are also exported in
editable form. This is a **read-only analysis** of the repository — the only
writes are the new files in the output folder.

`<skill>` below means the folder containing this SKILL.md. `<output>` means
the output folder chosen in step 1.

## Deliverables

```
<output>/                                  (default: <repo>/docs/architecture/)
├── Architecture-Design-Document.docx      the document
├── architecture-design-document.md        markdown source (kept for regeneration)
└── diagrams/
    ├── 01-system-context.mmd / .png       every diagram: editable Mermaid
    ├── 02-container.mmd / .png            source + rendered image
    ├── 03-component-<name>.mmd / .png
    ├── 04-sequence-<flow>.mmd / .png
    ├── 05-data-model.mmd / .png
    ├── 06-deployment.mmd / .png
    ├── 01-system-context.drawio(.json)    editable draw.io copies of the two
    └── 02-container.drawio(.json)         structural diagrams
```

## Prerequisites — check before starting

1. `python --version` (3.9+) and `python -c "import docx"`. If the import
   fails, run `pip install python-docx` (this is the only required package).
2. Diagram rendering needs **one** of: `mmdc` on PATH (best, fully local),
   internet access to kroki.io, or `npx` (Node). The render script picks
   automatically. **Privacy note:** the kroki.io fallback sends diagram text
   (project/entity names, not code) to a public web service — if the
   codebase is confidential and no local renderer exists, tell the user and
   ask before rendering with kroki.

## Step 1 — Scan the repository

Read broadly before writing anything. Collect these facts (keep notes as you
go — every sentence in the document must trace back to them):

1. **Solution shape** — glob `**/*.sln` and `**/*.csproj`. Per project:
   `TargetFramework`, `OutputType`/SDK (web, worker, classlib, test), and all
   `PackageReference`s. Packages are architecture evidence: EF Core providers,
   `MediatR`, `FluentValidation`, `Serilog`, `MassTransit`, auth packages each
   imply a section of the document.
2. **Project references** — `ProjectReference` items give the dependency graph
   for the container diagram.
3. **Composition root** — read `Program.cs` / `Startup.cs` and any
   `ServiceCollectionExtensions` they call: DI registrations, middleware
   pipeline, auth setup, hosted services.
4. **HTTP surface** — controllers or minimal-API `Map*` calls: routes, verbs,
   auth attributes.
5. **Data layer** — `DbContext` classes, `DbSet<>` properties, entity classes
   and their navigation properties, `Migrations/` folder, connection strings
   in `appsettings*.json`.
6. **Integrations** — typed/named `HttpClient` registrations, message-bus
   producers/consumers, email/storage clients, background jobs
   (`IHostedService`, Hangfire, Quartz).
7. **Cross-cutting** — auth scheme, logging setup, error-handling middleware,
   validation, caching, resilience (Polly).
8. **Deployment evidence** — `Dockerfile`, `docker-compose*`, K8s manifests,
   `.github/workflows`/`azure-pipelines`, `launchSettings.json`.
9. **Existing docs** — `README`, `docs/`, `ARCHITECTURE.md`, ADRs. Reuse their
   terminology; do not contradict them without noting it.

Large solutions (>15 projects): read every csproj (cheap, gives the full
structure tables), but do deep source reading only for the 3–5 projects where
the behavior lives; say in the document's Scope section which projects were
analyzed in depth.

## Step 2 — Choose the output folder

Default to `<repo>/docs/architecture/`; use whatever location the user asked
for instead. Create it plus the `diagrams/` subfolder. If a previous run's
files exist there, tell the user before overwriting.

## Step 3 — Author and render the diagrams

Read [references/diagram-recipes.md](references/diagram-recipes.md) first —
it has the syntax rules that keep renders from failing, the standard init
directive and palette, and a recipe per diagram type.

Write these `.mmd` files into `<output>/diagrams/` (skip a diagram only when
the repo has no material for it — e.g. no DbContext means no 05):

| File | Shows |
|------|-------|
| `01-system-context.mmd` | actors, system boundary, external systems |
| `02-container.mmd` | projects/executables, data stores, dependency edges |
| `03-component-<project>.mmd` | inside the core project: real classes, grouped |
| `04-sequence-<flow>.mmd` | 1–2 key runtime flows end to end |
| `05-data-model.mmd` | entities and relationships from the DbContext |
| `06-deployment.mmd` | where containers run, from deployment evidence |

Then render, and keep fixing + re-running until every diagram passes:

```
python "<skill>/scripts/render_diagrams.py" "<output>/diagrams"
```

The script prints the renderer's syntax error for any failing file. Do not
continue with missing PNGs.

## Step 4 — Export editable draw.io copies

Read [references/drawio-spec.md](references/drawio-spec.md), write
`01-system-context.drawio.json` and `02-container.drawio.json` specs
(same nodes/edges/labels as their Mermaid twins), then:

```
python "<skill>/scripts/make_drawio.py" "<output>/diagrams/01-system-context.drawio.json" "<output>/diagrams/02-container.drawio.json"
```

## Step 5 — Write the document

Read [references/document-template.md](references/document-template.md) and
write `<output>/architecture-design-document.md` following its skeleton
exactly — frontmatter (drives the cover page), all sections, figures
referenced as `![caption](diagrams/xx.png)`.

The quality bar: every claim cites evidence (file, class, package); missing
things are stated honestly ("no automated tests were found") rather than
papered over; no invented components or generic architecture prose.

## Step 6 — Build the .docx

```
python "<skill>/scripts/build_docx.py" "<output>/architecture-design-document.md" "<output>/Architecture-Design-Document.docx"
```

The script exits non-zero and lists any image it could not find — fix the
paths and re-run. A clean run prints only `Wrote <path>`.

## Step 7 — Deliver

Confirm the `.docx` exists and is non-trivial in size, then report to the
user:

- the path of the `.docx` and the `diagrams/` folder;
- that Word will offer to update the table of contents on open (or Ctrl+A,
  F9 populates it manually);
- how to edit diagrams later: change a `.mmd` and re-run
  `render_diagrams.py`, or open the `.drawio` files at app.diagrams.net /
  in the draw.io desktop or VS Code extension;
- one or two sentences on the most notable findings (architecture style,
  any risks you documented).

## Rules

- **Read-only scan.** Never modify source files; all writes go to `<output>`.
- **Evidence or silence.** Anything you cannot ground in a file you read gets
  either omitted or explicitly marked as an assumption in the document.
- **Diagrams must render.** A failed `.mmd` is fixed, not skipped — the docx
  build will flag the missing image anyway.
- **Keep the sources.** The `.md`, `.mmd`, and `.drawio.json` files are part
  of the deliverable; they are what make the document regenerable and the
  diagrams editable.
