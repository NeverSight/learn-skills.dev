---
name: maintain-knowledge
description: Create and maintain a living markdown knowledge base in Documentation/ for a .NET solution (.NET 8–10) — project structure, architecture with Mermaid diagrams, feature inventory, data model, development guide, technical debt, improvement backlog, reusable components, plus an agent-optimised KnowledgeBase.md and machine-readable PROJECT_KNOWLEDGE.json. Use when asked to update docs, document the codebase in markdown, create or refresh a knowledge base, generate onboarding or agent-context docs, analyse the codebase, discover features, track technical debt, or keep Documentation/ in sync with the code. For one-off Word (.docx) deliverables use architecture-design-document or fs-mds-document instead.
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 solutions
---

# Project Knowledge Maintainer (.NET)

Scan the repository and maintain a complete, accurate knowledge base inside
`Documentation/`. The docset serves **two audiences at once**:

- **Humans** — a new developer can understand, build, run, and extend the
  system using only this folder.
- **Coding agents** — an LLM agent gets dense, factual context
  (`KnowledgeBase.md`, `PROJECT_KNOWLEDGE.json`) without reading the whole
  repo.

This skill only writes inside `Documentation/`. It never modifies source
code, and it is safe to re-run: repeated runs update sections in place
instead of appending duplicates.

## Deliverables

All files live in `Documentation/`. Create missing ones; update existing
ones following the merge rules below. Every file's exact skeleton is in
[references/doc-templates.md](references/doc-templates.md) — do not invent
your own structure.

**Human-facing docs**

| File | Purpose |
|---|---|
| `README.md` | Index of the docset with a reading order for humans and for agents |
| `ProjectStructure.md` | Solution map: projects, folders, responsibilities, dependency graph |
| `Architecture.md` | Style, layers, runtime data flow, integrations — with Mermaid diagrams |
| `Features.md` | Every implemented feature: purpose, entry points, key files, status |
| `DataModel.md` | DbContexts, entities, relationships, migrations, other stores |
| `DevelopmentGuide.md` | Prerequisites, build, run, test, debug, configuration, deployment |
| `TechnicalDebt.md` | Known debt with severity, effort, evidence — plus resolved items |
| `ImprovementBacklog.md` | Prioritised P1/P2/P3 backlog with effort and risk |
| `ReusableComponents.md` | Services, utilities, patterns worth lifting into future projects |

**Agent-facing docs**

| File | Purpose |
|---|---|
| `KnowledgeBase.md` | Dense fact sheet for AI agents — hard limit 150 lines, facts only |
| `PROJECT_KNOWLEDGE.json` | Machine-readable summary (schema in doc-templates.md) |
| `NextProjectSeed.md` | Bootstrap context for starting a similar project |

If the repo genuinely has no material for a file (e.g. no persistence layer
→ `DataModel.md`), still create it with the stamp line and a single sentence
stating what was searched and not found. Never silently skip a file.

## Step 0 — Full scan or incremental update?

1. Read `Documentation/PROJECT_KNOWLEDGE.json` if it exists and note its
   `last_commit` value.
2. If it exists and the commit is valid, list what changed:
   `git diff --name-status <last_commit>..HEAD`
   - **≤ ~200 changed files** → incremental mode: read the changed files
     plus their composition roots, and re-verify only the affected doc
     sections. Unchanged sections stay as they are.
   - More than that, the commit is unknown to git, or the JSON is missing
     → **full scan**.
3. Record today's date and current `git rev-parse --short HEAD` — every doc
   gets this in its stamp line, and the JSON gets it in `generated` /
   `last_commit`.

## Step 1 — Discover

Read [references/dotnet-discovery.md](references/dotnet-discovery.md) first.
It tells you exactly which files to enumerate, what each package reference
implies architecturally, and how to read the composition root. Follow its
order:

1. Solution shape — `*.sln`/`*.slnx`, every `*.csproj`, `Directory.Build.props`,
   `Directory.Packages.props`, `global.json`.
2. Packages → architecture evidence (the package table in the reference).
3. Composition root — `Program.cs`, DI registrations, middleware pipeline.
4. Entry points — HTTP endpoints, message consumers, hosted services,
   scheduled jobs, CLI verbs, UI pages.
5. Data layer — `DbContext`, entities, migrations, connection strings.
6. Configuration and environments.
7. Tests, CI/CD, deployment evidence.
8. Existing human docs — `README*`, `CLAUDE.md`, `AGENTS.md`, `docs/`, ADRs.
   Reuse their terminology; never contradict them without flagging it.

Skip: `bin/`, `obj/`, `node_modules/`, `dist/`, `build/`, `.git/`,
`packages/`, `TestResults/`, `*.g.cs`, `*.Designer.cs`, and anything in
`.gitignore`.

Large solutions (>15 projects): read every `.csproj` (cheap, gives complete
structure tables) but deep-read source only in the 3–5 projects where the
behaviour lives, and say so in `ProjectStructure.md`.

## Step 2 — Infer features from code, not filenames

A feature exists only if you can point to its entry point **and** its
implementation. For each entry point found in step 1.4, trace one level into
the handler/service to confirm what it actually does.

Classify each feature with this table (first matching row wins):

| The entry point… | Category |
|---|---|
| requires an admin/elevated role, or manages users/tenants/settings | Administrative |
| is authentication, authorization, auditing, or secrets handling itself | Security |
| talks to an external system (third-party API, message broker, email, storage) | Integration |
| is health checks, logging, migrations, background housekeeping | Infrastructure |
| anything else an end user or API consumer invokes | User |

## Step 3 — Detect drift

Compare what you discovered against the existing `Documentation/` content.
Build an explicit change list before writing anything:

- **New** — implemented in code, absent from docs.
- **Changed** — docs describe it, code now differs (renamed routes, moved
  projects, swapped packages, new auth scheme).
- **Removed** — documented, no longer in code. Delete from `Features.md` /
  JSON; move any related debt items to the Resolved section.
- **New debt** — TODO/HACK comments, failing patterns from the discovery
  reference, missing tests for new features.

In incremental mode, limit this to sections touched by the git diff.

## Step 4 — Write / update the docs

Read [references/doc-templates.md](references/doc-templates.md) and follow
each skeleton exactly. Merge rules for existing files:

1. **Template headings are the contract.** Find the section by its heading
   and rewrite that section's content in place. Never append a second copy
   of a section that already exists.
2. **Unrecognised headings are user content.** A section whose heading is
   not in the template was written by a human — preserve it verbatim, in
   place.
3. **Delete stale entries** (removed features, fixed debt). Fixed debt moves
   to the `## Resolved` table with the date, it is not silently dropped.
4. **Update the stamp line** (`> Last updated: YYYY-MM-DD · commit <short-sha>
   · generated by maintain-knowledge`) directly under the H1 of every file
   you touch. Leave files you did not touch alone.
5. **Stable IDs.** Debt items (`TD-001`), backlog items (`IB-001`), and
   feature names keep their identifiers across runs. New items take the next
   free number; never renumber existing ones.

Mermaid rules (diagrams that don't render are worse than no diagrams):

- Quote any label containing spaces, parentheses, or slashes: `A["ASP.NET Core API"]`.
- Node IDs: letters, digits, underscore only — never start with a digit.
- One statement per line; no `<br>` HTML, use `\n` in quoted labels sparingly.
- Keep each diagram under ~20 nodes; split rather than cram.
- Use `flowchart LR`/`TB`, `sequenceDiagram`, and `erDiagram` only — these
  render everywhere GitHub-flavoured markdown does.

## Step 5 — Update PROJECT_KNOWLEDGE.json

Follow the schema and the fully-populated example in
[references/doc-templates.md](references/doc-templates.md). Rules:

- Keep the schema stable — same keys, same shapes as the example.
- `schema_version` stays `"2"`; set `generated` and `last_commit`.
- Remove stale entries; preserve existing `id` values on debt/backlog items.
- Arrays of objects, not arrays of prose strings, for `features`, `apis`,
  `entities`, `technical_debt` — agents consume this file programmatically.

## Step 6 — Verify before reporting

Run this gate; fix failures and re-check rather than shipping them:

1. `PROJECT_KNOWLEDGE.json` parses (`pwsh`: `Get-Content Documentation/PROJECT_KNOWLEDGE.json -Raw | ConvertFrom-Json | Out-Null`; or `python -c "import json;json.load(open('Documentation/PROJECT_KNOWLEDGE.json'))"`).
2. Spot-check 5 file paths cited in `Features.md` — each must exist on disk.
3. Every relative link inside `Documentation/` resolves to a real file.
4. Every Mermaid block follows the rules in step 4.
5. No template placeholder text (`<...>`, `TODO-fill`) remains in any file.
6. `KnowledgeBase.md` is ≤ 150 lines; stamp lines updated in every touched file.

## Step 7 — Report

End with a short summary for the user:

1. Mode (full / incremental) and commit range covered
2. New features discovered · changed · removed
3. Architecture changes
4. New reusable components
5. New technical debt items (and any resolved)
6. Top 3 improvement recommendations (P1s from the backlog)
7. Files created vs updated vs untouched

## Rules

- **Evidence or silence.** Every claim cites a file path (and member name
  where useful). If evidence is insufficient, write "not verified" rather
  than guessing — never invent components, packages, or flows.
- **Infer from implementation, not filenames.** `PaymentService.cs` being
  empty means there is no payment feature.
- **Docs only.** Never modify anything outside `Documentation/`.
- **Concise beats complete.** A wrong-but-plausible sentence is the worst
  output this skill can produce; a short accurate one is the best.
- **Respect existing terminology** from README/ADRs/CLAUDE.md — the docset
  must not introduce a second name for the same thing.
