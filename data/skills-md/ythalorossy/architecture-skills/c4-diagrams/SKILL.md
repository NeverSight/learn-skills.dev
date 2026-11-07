---
name: c4-diagrams
description: Use when the user asks for architecture documentation, C4 diagrams, the key request flows of a codebase as sequence diagrams, a deployment, API or configuration overview, a dependency graph or diagram, or an explanation of how a repository's projects, packages or modules fit together. Works on local repository paths (.NET, Java/Kotlin, Go, Node.js/TypeScript, Python). Not for a quick question about one file or import, for changing code, or for diagrams unrelated to a codebase.
license: MIT
compatibility: Requires python3 (3.11+, checked at startup). Node.js with @mermaid-js/mermaid-cli is optional, for SVG rendering.
metadata:
  author: ythalorossy
  version: "3.6.0"
---

# Architecture Diagram Generator

Turn a repository into C4 diagrams (system context, containers, components, code structure), key-flow sequence diagrams, deployment, API and configuration views, and evidence-based findings.

**If the user only asked a question** ("what talks to the database?", "is this a monolith?"), answer it from the facts and offer the diagrams. Ask before writing files into their repository.

## How the work is split

| Level | Shows | From |
|---|---|---|
| 1 · System context | the system, its people, the external systems it talks to | **you**, in `c4-model.json` |
| 2 · Containers | what runs on its own (API, web app, worker, CLI) and the data stores | the script finds them; you name and describe them |
| 3 · Components | each container's modules, then the packages/namespaces inside them and their imports | the script; you describe the important ones |
| 4 · Code | classes of 2–5 key components: inheritance, dependencies, methods | **you** pick them in `code`; the script extracts the types |
| Key flows | 1–3 important requests traced step by step (sequence diagrams) | **you**, in `flows` |
| Deployment, API, configuration, inventory, appendix | compose, Dockerfiles, Kubernetes, CI and hosting; HTTP routes; environment variables with defaults; frameworks and versions; every project and reference; the checks | the script |

The script does the objective parts, with `file:line` evidence on everything it finds. You add the judgement: who uses the system, what each external system is for, the descriptions. `render_c4.py` checks your model against the facts and draws every level in one style.

`<skill>/assets/detection-coverage.md` lists the patterns the script knows **and the blind spots they leave**. Read it before concluding something isn't there.

## Where things are

`<skill>` is the folder holding this `SKILL.md`; the harness prints its absolute path when the skill loads. Use that path wherever `<skill>` appears — the working directory is the user's repository, so a bare `scripts/…` path does not resolve.

Commands use `python3`; where it isn't on the PATH (common on Windows) use `python` or `py -3`. The scripts need Python 3.11+ and say so if it's older. When one fails, its message is in [Troubleshooting](https://github.com/ythalorossy/architecture-skills/blob/main/README.md#troubleshooting).

## Step 1 — Run the analysis

```bash
python3 "<skill>/scripts/analyze_repository.py" "<repository_path>"
```

- Quote paths: they may contain spaces.
- Run it from the user's working directory. Output goes to `./architecture-docs/<repository name>/` there, for them to keep, commit or delete. Pass `--output <directory>` only if they named another location; never write into the skill folder.
- It writes `c4-facts.json`, facts-only C4 diagrams (`c4-container.*`, `c4-component-*.*`, `c4-structure-*.*`, `c4-deployment.*`, each `.mmd` and `.svg`), `ArchitectureReport.md`, `dependency-graph.*`, `repository-scan.json` and `summary.json`.
- SVGs come from `mmdc` or `npx @mermaid-js/mermaid-cli@12.0.0` (pinned). Without Node.js the run prints a `NOTE:` and the report shows Mermaid source; tell the user. `--no-svg` or `C4_SVG=0` turns it off.

### Check `summary.json`

Read `status`. `"ok"` means the analysis understood the repository. `"degraded"` means a cause is waiting in `warnings`: `<skill>/assets/run-diagnostics.md` says what each `kind` means, what to do about it, and what `summary.json` stops telling you once you render your own model. Tell the user about any skipped or unparsed file.

## Step 2 — Read the facts and the code

Read `summary.json` and `c4-facts.json`. Then read enough code to answer what the facts can't:

- **Who uses it?** Controllers or routes, auth handlers, UI, CLI commands, README.
- **What is each external system for?** Open the evidence lines.
- **Is each fact real?** A `requests` call in a one-off script is not a dependency; a development-only compose service is not a container. Both belong in `excluded`, with a reason.
- **What does each container and key component do?** Open `containers[].code_components` in `c4-facts.json` and read a file or two per package, so you can describe them.
- **What are the main flows?** Follow 1–3 important requests from an entry point (an endpoint in `endpoints`, a UI action, a CLI command, a scheduled job) through the components to the stores and external systems.
- **Which components matter most?** Pick 2–5 holding the core behaviour (a workflow engine, a client wrapper) for Level 4, and read their main classes.
- **What did the script miss?** The detectors are pattern-based and `<skill>/assets/detection-coverage.md` lists where they are blind. When the code shows a container, store, external system or link the facts don't have (a queue consumer, a scheduled job, a gRPC or in-house SDK client, a call through a wrapper), add it with `evidence` pointing at that code. Recall matters as much as precision: a missing payment provider misleads more than a mislabelled one.

At **Level 3**, the component graph is the source of truth for which components and edges exist: draw those, and don't invent others. Levels 1 and 2 are not bounded by it — that is where the containers, stores and external systems the detectors missed belong.

## Step 3 — Write `c4-model.json` and draw

Write `c4-model.json` in the output folder, following `<skill>/assets/c4-model-reference.md`. In short:

- cover every fact id: as an element, in an element's `facts` list, or in `excluded` with a reason;
- data stores go in `containers` with `"type": "database"`;
- every element has `evidence`, or `"assumption": true`;
- describe each important component in one line, using the ids from `c4-facts.json` (module ids, and code ids such as `weather-api::controller`);
- add 1–3 `flows`: each a named, ordered list of steps between people, containers, external systems or components. Use component ids inside a container, so the flow shows the code path;
- add `code`: 2–5 key components (ids from `c4-facts.json`), each with a one-line `description` and, optionally, the `types` to center the class diagram on;
- add `summary`: an `overview` paragraph, your `findings` (each tied to a `file:line`) and `recommendations` (each backed by a finding). It becomes the report's "Architecture overview".

Then run:

```bash
python3 "<skill>/scripts/render_c4.py" "<output folder>"
```

Three tiers. `ok` draws the model as written. `drift` prints a `DRIFT:` line per uncovered fact and exits 0. `invalid` (a JSON syntax error with its line and column, a wrong-typed section with its JSON path, an unknown or duplicate id) draws facts-only and exits 1; `--strict` exits 2 on drift too. Messages suggest the likely fix (`did you mean 'bookshop-web'?`); evidence pointing at a missing file or line is a warning. It also warns once per diagram that fails to render, and rewrites the C4 section of `ArchitectureReport.md` and the `c4-*.mmd`/`.svg` files.

If `c4-model.json` already exists it was kept and may have been user-edited: update it rather than rewriting, and keep their wording.

### When Step 3 is finished

Stop when `render_c4.py` reports `ok` with no `DRIFT:` line, every warning fixed or justified, and a `Coverage:` line whose `facts`, `containers described` and `components described` are complete and whose `people`, `flows` and `code` counts are all non-zero. A short number there means the model is unfinished, not that the script is fussy; an undescribed component is how "bare package names" reaches the user.

## Step 4 — Report to the user

Your overview, findings and recommendations are already in `ArchitectureReport.md`. In the chat, give the short version:

1. **What the system is**: 2–3 sentences, from the Context level.
2. **Diagrams**: the Context and Container Mermaid blocks inline, then the component, code, flow and deployment diagrams by file.
3. **Findings**: the most important, each tied to a concrete element, component, file or edge. Say which came from the automated checks (appendix) and which are your judgement; for a cycle, name an import that causes it.
4. **Assumptions**: the elements, flows and flow steps you marked, for the user to confirm.
5. **Recommendations**: only ones backed by a finding.
6. **Artifacts**: the output folder and `ArchitectureReport.md` — the user's to keep, commit or delete; `c4-model.json` can be edited and re-rendered.

To check dependency structure, walk through `<skill>/assets/architecture-review-checklist.md`. For a system overview or per-service docs, fill `<skill>/assets/system-overview-template.md` / `<skill>/assets/service-template.md`.

**If nothing was detected** (no containers, empty graph — e.g. an unsupported stack): build the picture from the source yourself, write the model by hand, and tell the user the diagrams were derived manually.

## Common mistakes

| Mistake | Fix |
|---|---|
| Stopping after Step 1 | Facts-only diagrams have no people, purposes, flows or Context level. Write the model. |
| Findings only in the chat | The chat is gone when the session ends. Put them in `summary`. |
| Modelling only what the script found | Add what the code shows and the facts missed, with evidence. |
| Inventing people, external systems or flows | Only what code, config or docs support; mark the rest `"assumption": true`. |
| Drawing a development-only service, or a library, as a container | Neither runs in production. Put the service in `excluded` with a reason; leave the library as the component it is. |
| Reporting "0 projects, no concerns" as healthy | Empty graph = not analyzed. Analyze manually. |
| Calling the architecture healthy because the checks passed | They cover reference hygiene and cycles only. Say what you inspected. |
| Treating "outside solution/workspace" as dead code | Examples, fixtures and tooling are often standalone on purpose. Check first. |
| Inventing layers ("Controller → Service → Repository") | Name only components and edges in the facts, or that you saw in the code. |
| Writing output to a temp or scratchpad folder | The user can't find it later. Use `./architecture-docs/` or the location they named. |
| Level 4 on model or DTO folders | They only hold data. Pick components with behaviour: services, engines, agents, clients. |
