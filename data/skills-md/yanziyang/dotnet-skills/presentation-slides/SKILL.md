---
name: presentation-slides
description: Scan an entire .NET repository (.NET 8–10, ASP.NET Core, workers, class libraries) and generate a professional 16:9 PowerPoint (.pptx) presentation about the solution — for new team members, management, or customers — illustrated with rendered diagrams (system context, containers, sequence, data model, deployment) whose editable sources (Mermaid .mmd and draw.io files) are exported to a diagrams/ subfolder. Use this skill whenever the user asks for a presentation, slides, slide deck, pitch deck, PowerPoint, pptx, onboarding deck, management briefing, project overview slides, or "present this codebase/solution" for a .NET project — even if they don't say "PowerPoint" explicitly.
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 solutions
  requires: Python 3.9+ with python-pptx; internet access or local mermaid-cli for diagram rendering
---

# Presentation Slides (.NET)

Produce a professional, evidence-based PowerPoint deck for a .NET solution:
a styled 16:9 `.pptx` with title/section/content slides, speaker notes, and
diagrams that are also exported in editable form. This is a **read-only
analysis** of the repository — the only writes are the new files in the
output folder.

`<skill>` below means the folder containing this SKILL.md. `<output>` means
the output folder chosen in step 2.

## Deliverables

```
<output>/                                  (default: <repo>/docs/presentation/)
├── <SolutionName>-Overview.pptx           the deck
├── deck.json                              content spec (kept for regeneration)
└── diagrams/
    ├── 01-system-context.mmd / .png       every diagram: editable Mermaid
    ├── 02-container.mmd / .png            source + rendered image
    ├── 03-sequence-<flow>.mmd / .png
    ├── 04-data-model.mmd / .png
    ├── 05-deployment.mmd / .png
    ├── 01-system-context.drawio(.json)    editable draw.io copies of the two
    └── 02-container.drawio(.json)         structural diagrams
```

## Prerequisites — check before starting

1. `python --version` (3.9+; on Windows try `py` if `python` is missing) and
   `python -c "import pptx"`. If the import fails, run
   `pip install python-pptx` (the only required package).
2. Diagram rendering needs **one** of: `mmdc` on PATH (best, fully local),
   internet access to kroki.io, or `npx` (Node). The render script picks
   automatically. **Privacy note:** the kroki.io fallback sends diagram text
   (project/entity names, not code) to a public web service — if the
   codebase is confidential and no local renderer exists, tell the user and
   ask before rendering with kroki.

## Step 1 — Pin down audience and scope

The same repo yields three different decks. If the user named an audience —
**new team members**, **management**, or **customers** — use it. If not,
default to new team members and say so when delivering; only ask when the
request makes the ambiguity costly (e.g. "slides for the board next week").
Audience changes which slides exist and how they are worded — the rules are
in [references/deck-outline.md](references/deck-outline.md).

## Step 2 — Choose the output folder

Default to `<repo>/docs/presentation/`; use whatever location the user asked
for instead. Create it plus the `diagrams/` subfolder. If a previous run's
files exist there, tell the user before overwriting.

## Step 3 — Scan the repository

Read broadly before writing anything. Every slide must trace back to these
facts — keep notes as you go:

1. **Solution shape** — glob `**/*.sln` and `**/*.csproj`. Per project:
   `TargetFramework`, `OutputType`/SDK (web, worker, classlib, test), and all
   `PackageReference`s. Packages are architecture evidence: EF Core providers,
   `MediatR`, `MassTransit`, auth and logging packages each earn a place on
   the tech-stack slide.
2. **Project references** — `ProjectReference` items give the dependency
   graph for the container diagram.
3. **Composition root** — `Program.cs` / `Startup.cs` and the
   `ServiceCollectionExtensions` they call: DI registrations, middleware,
   auth setup, hosted services.
4. **HTTP surface** — controllers or minimal-API `Map*` calls: routes, verbs,
   auth attributes. Count endpoints — real numbers feed the `stats` slide.
5. **Data layer** — `DbContext` classes, `DbSet<>` properties, key entities
   and relationships, `Migrations/` folder, connection strings in
   `appsettings*.json`.
6. **Integrations** — typed/named `HttpClient`s, message-bus
   producers/consumers, email/storage clients, background jobs.
7. **Quality signals** — test projects and their scope, CI/CD workflows,
   logging/monitoring setup. Gaps are findings too ("no automated tests")
   and belong on the quality slide, honestly stated.
8. **Deployment evidence** — `Dockerfile`, `docker-compose*`, K8s manifests,
   pipelines, `launchSettings.json`.
9. **Existing docs** — `README`, `docs/`, ADRs. Reuse their terminology and
   any stated roadmap; do not contradict them without noting it.

Large solutions (>15 projects): read every csproj (cheap, gives the full
picture), but deep source reading only for the 3–5 projects where the
behavior lives.

## Step 4 — Author and render the diagrams

Read [references/diagram-recipes.md](references/diagram-recipes.md) first —
it has the syntax rules that keep renders from failing, the standard palette,
and the slide-specific size limits (≤10 nodes; slides are read from the back
of a room).

Write these `.mmd` files into `<output>/diagrams/` (skip a diagram only when
the repo has no material for it, or the audience rules exclude it):

| File | Shows |
|------|-------|
| `01-system-context.mmd` | actors, system boundary, external systems |
| `02-container.mmd` | projects/executables, data stores, dependency edges |
| `03-sequence-<flow>.mmd` | the key runtime flow end to end |
| `04-data-model.mmd` | core entities from the DbContext (≤6) |
| `05-deployment.mmd` | where containers run, from deployment evidence |

Then render, and keep fixing + re-running until every diagram passes:

```
python "<skill>/scripts/render_diagrams.py" "<output>/diagrams"
```

The script prints the renderer's syntax error for any failing file. Do not
continue with missing PNGs.

## Step 5 — Export editable draw.io copies

Read [references/drawio-spec.md](references/drawio-spec.md), write
`01-system-context.drawio.json` and `02-container.drawio.json` specs
(same nodes/edges/labels as their Mermaid twins), then:

```
python "<skill>/scripts/make_drawio.py" "<output>/diagrams/01-system-context.drawio.json" "<output>/diagrams/02-container.drawio.json"
```

## Step 6 — Write deck.json

Read [references/deck-outline.md](references/deck-outline.md) for the
storyline and audience adjustments, and
[references/pptx-spec.md](references/pptx-spec.md) for the exact JSON format
and per-slide-type quality rules. Write `<output>/deck.json`.

The quality bar: every number was counted, every name exists in the repo,
gaps are stated honestly, every content slide has speaker notes, and slide
types are varied — a deck of twelve bullet lists is a failure even if every
word is true.

## Step 7 — Build the .pptx

```
python "<skill>/scripts/build_pptx.py" "<output>/deck.json" "<output>/<SolutionName>-Overview.pptx"
```

The script exits non-zero and lists every problem (unknown slide type,
missing image, ragged table) — fix `deck.json` and re-run. A clean run
prints `Wrote <path> (<n> slides)`.

## Step 8 — Deliver

Confirm the `.pptx` exists and is non-trivial in size, then report to the
user:

- the path of the `.pptx` and the `diagrams/` folder;
- which audience the deck targets (and that it was the default, if assumed);
- how to change content later: edit `deck.json` and re-run `build_pptx.py`;
  edit a `.mmd` and re-run `render_diagrams.py`; open the `.drawio` files at
  app.diagrams.net or in the draw.io desktop/VS Code extension;
- one or two sentences on the most notable findings (architecture style,
  anything surfaced on the quality slide).

## Rules

- **Read-only scan.** Never modify source files; all writes go to `<output>`.
- **Evidence or silence.** Anything you cannot ground in a file you read is
  either omitted or explicitly labelled as an assumption/recommendation.
- **Diagrams must render.** A failed `.mmd` is fixed, not skipped — the deck
  build will flag the missing image anyway.
- **Scripts own the design.** Never hand-write python-pptx code or draw.io
  XML; the deck spec and diagram specs are the interface. That is what keeps
  output consistent and regenerable.
- **Keep the sources.** `deck.json`, `.mmd`, and `.drawio.json` files are
  part of the deliverable — they make the deck regenerable and the diagrams
  editable.
