---
name: unpack-this
description: Unpack a handed-over codebase end to end and map its business processes, feature inventory, architecture, runtime flows, data model, and technical risks into a Markdown report plus an interactive HTML report. Use when the user wants to understand an inherited or unfamiliar project, onboard onto a codebase, prepare a handover document, or asks how the system works based on the existing code.
---

# Unpack-This: Codebase Handover & Flow Analyzer

Act as a **Principal Software Architect and Technical Product Analyst**. Help the user understand a repository they just inherited by unpacking the code and turning it into structured, readable, actionable documentation.

Do not narrate files one by one. **Connect the code to the business logic it implements.**

## Ground rules

- **Evidence first.** Every claim about a feature, flow, or rule cites the file path (and line or symbol when useful). Anything not directly confirmed by code is marked `inferred`. Never invent business flows to fill gaps; list them under open questions instead.
- **No secrets.** Name environment variables and config keys, never copy their values, tokens, passwords, or keys into the report.
- **Language.** Write the report in the language of the user's latest message. Keep common software engineering terms in English (controller, service, queue, webhook, etc.).
- **Read before concluding.** Finish Phase 1 before writing any section.

## Phase 1: Exploration (mandatory)

### Size up first

Before opening files, map the repo cheaply: list tracked files (`git ls-files | head -300` and a count per top-level folder), detect the stack from manifests, and skip what is not source: `node_modules/`, `vendor/`, `dist/`, `build/`, lock files, generated code, fixtures, and minified assets. Then pick a reading mode:

- **Small** (up to about 150 source files): read the paths below fully.
- **Medium** (about 150 to 1,000): read entry points, routes, and models fully; skim services and jobs by their public functions (grep for function and class names, open only the bodies that hold business rules); read large files by range, not whole.
- **Large or monorepo**: map modules first, then analyze one module at a time. If the harness has subagents, give each module to its own subagent with this skill's Phase 1 and ask for a compact summary with file references; merge the summaries yourself. Deliver sections 1 to 4 first (see Interaction rules).

### Always read (minimum set)

Read these whenever they exist, whatever the repo size. Sections 7 and 8 depend on them:

- Manifests and `README.md`: `package.json`, `composer.json`, `requirements.txt` / `pyproject.toml`, `go.mod`, `pom.xml` / `build.gradle`, `Gemfile`, `Cargo.toml`.
- Runtime config: `Dockerfile`, `docker-compose.yml` / `compose.yaml`, `Procfile`, `Makefile`.
- Environment template: `.env.example`, `.env.sample`, or `.env.dist` (variable names only; never open a real `.env`).
- CI config: `.github/workflows/*`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`, `Jenkinsfile`.
- Tests: the test command from the manifest or CI, plus one or two test files for the most critical module, to confirm intended behavior.

### Then walk the code in this order

1. **Entry points and routing**: `routes/`, `app/`, `pages/`, `controllers/`, `cmd/`, `main.*`, API definitions (OpenAPI, GraphQL schema). List every user-facing and API entry point.
2. **Data and domain model**: `models/`, `entities/`, `prisma/schema.prisma`, `migrations/`, ORM definitions, SQL schema. Identify the core business entities, their relations, and their status fields.
3. **Business logic and services**: `services/`, `usecases/`, `handlers/`, `jobs/`, `domain/`. Find the rules that actually run.
4. **Background and hidden logic**: schedulers, cron definitions, queue workers, event listeners, webhooks, DB triggers.
5. **External integrations**: config files, HTTP clients, SDK imports. Detect payment gateways, email/SMS, storage, auth providers, third-party APIs, and message brokers.

Offer, rather than do, extra digging the report does not need, such as `git log` hot spots or a full test-coverage read.

## Phase 2: Report structure

Use these nine sections in this order. Open every section with a one or two sentence summary that answers the section's question before any detail, so a reader skimming only the summaries still gets the whole picture.

Never drop a section. When one does not apply (a CLI or library has no user roles, a stateless service has no data model), keep it and write `N/A` with a one-sentence reason, e.g. "N/A: this is a stateless CLI; it stores no data." The same goes for a sub-part: no status field means no state diagram, so write `N/A` with the reason in its place. When a minimum-set file from Phase 1 does not exist (no CI, no Dockerfile, no env template), say so in Risks or Getting Started instead of skipping it silently.

### Overview
*What is this, and what is it built with?*
- **Purpose**: 2 to 3 sentences on the business problem the application solves. (The HTML page header also carries a one-sentence version of it.)
- **At a glance**: language, framework, database, cache/queue, frontend, hosting/infra (only what the code shows).

### System Context
*Who and what interacts with the system?*
- **Actors / roles**: every user type (e.g. Admin, Customer, Vendor, Cron/System) and what each does.
- **External systems**: payment, email/SMS, storage, auth, third-party APIs, brokers, each with where it is integrated.
- **Context diagram**: one Mermaid `flowchart` at C4 context level: the system as a single box, actors on one side, external systems on the other.

### Business Processes
*How does the business run through this code?*
- **End-to-end flow**: the main journey from start to finish (e.g. *Registration → Order → Payment → Verification → Fulfillment*), then one short paragraph per major process.
- **Business rules**: a table of `Rule | Condition / value | Enforced in`, covering validations, calculations, expiry windows, limits, and status transitions. One row per rule, for example:

| Rule | Condition / value | Enforced in |
| :--- | :--- | :--- |
| Unpaid order expiry | Cancelled 15 minutes after creation if still `pending` | `app/Jobs/ExpireUnpaidOrders.php:18` |

### Feature Inventory
*What can the system do, and where does each feature live?*

| Module | Key Features | Code Location | Notes |
| :--- | :--- | :--- | :--- |
| *Auth* | *Login, SSO, password reset* | `src/modules/auth/...` | *JWT + refresh token* |

### Architecture & Runtime Flows
*How is the code organized, and what happens at runtime?*
- **Building blocks**: the deployable parts (web app, API, worker, scheduler, database, cache) and the code layering (routes → controllers → services → repositories), as a C4 container-level `flowchart`.
- **Critical flows**: the 2 to 3 most critical flows as Mermaid `sequenceDiagram`s, tracing `Request → Controller / Route → Service → Database / External API → Response`.

### Data Model
*What data matters, and how does it change state?*
- **Core entities**: the main tables/models, their key fields, and relations, with file references. Add an `erDiagram` when there are more than three related entities.
- **Status lifecycle**: a `stateDiagram-v2` for the most important status field (e.g. order status) with what triggers each transition.

### Risks & Technical Debt
*What can hurt the new owner?*
Each finding has a severity (High / Medium / Low), what it is, its impact, the file, and a suggested action. In Markdown, write one bullet per finding, for example:

- **High · Payment webhook accepts unsigned requests.** `WebhookController@handle` marks orders as paid without checking `signature_key`, so anyone can fake a payment. Verify the signature before updating the order. `app/Http/Controllers/WebhookController.php:24`

Cover:
- **Hidden logic**: cron jobs, webhooks, event listeners, background workers, DB triggers.
- **Technical debt and sensitive areas**: complex code, hardcoded values, weak validation, missing tests, security concerns, parts likely to break when changed.

### Getting Started
*How do I run it locally?*
Prerequisites, required env variable names, services to start, setup and run commands, and how to run tests, all derived from the actual config.

### Open Questions & Glossary
- **Open questions**: what the code could not answer and needs confirmation from the previous team.
- **Glossary**: domain terms used in the code and what they mean in this system.

Keep every diagram under about 12 nodes or participants with short labels.

## Phase 3: Deliverables

Write into `docs/handover/` at the analyzed repo's root (create the folder if missing; ask before overwriting existing files). `HANDOVER.md` is the source of truth; `handover.html` is a rendering of it.

1. **Write `HANDOVER.md` first**: a `# <Project name>: Handover Report` title, then exactly these nine `##` headings, in English and unnumbered so they match the HTML: `Overview`, `System Context`, `Business Processes`, `Feature Inventory`, `Architecture & Runtime Flows`, `Data Model`, `Risks & Technical Debt`, `Getting Started`, `Open Questions & Glossary`. Everything under them, including `###` sub-headings, is in the report language. Mermaid goes in fenced ```` ```mermaid ```` blocks.
2. **Render it into `handover.html`**: copy `assets/report-template.html` from this skill's own directory (not the analyzed repo) and fill it with the same content, adding nothing and leaving nothing out. Keep the template's styling, scripts, and the Pele `<script>` tag (with its `integrity` hash) unchanged.
   - Read the template's documentation comment, then delete it. Fill every `{{PLACEHOLDER}}`: `{{PROJECT_NAME}}` is the product's human name (README title over package name), `{{PURPOSE}}` is one sentence, `{{STACK_SUMMARY}}` is three to five key technologies joined with ` · `, `{{REPO_PATH}}` is the repo name or its remote URL (never a local absolute path), `{{LANG}}` is a BCP 47 code (`id`, `en`), `{{GENERATED_DATE}}` is `YYYY-MM-DD`.
   - Put content inside the nine existing `<section>`s, replacing each guide comment; do not rename their `id`s, the sidebar links to them.
   - Start each section with `<p class="lead">` for its summary. Map Markdown to the template's components and use nothing else (no inline styles, new classes, emoji, or icons):

     | Markdown | HTML component |
     | :--- | :--- |
     | First paragraph of a section | `<p class="lead">` |
     | `###` sub-heading | `<h3>` |
     | Paragraph, bullet list, numbered list | `<p>`, `<ul>`, `<ol>` |
     | Tech stack key-value list | `dl.facts` |
     | End-to-end journey (`A → B → C`) | `ol.flow` |
     | Table | `<table>`; the feature inventory gets `class="filterable"` |
     | `- **Name** (meta): text` `file`: actor, external system, entity, finding, open question, glossary term | `.item` inside `.items`: name in `.item-name`, meta in `.item-meta`, file in `code.file` |
     | Numbered list of setup steps with fenced commands under each | `ol.steps`, each command block as `pre.code` |
     | `> **Title.** text` caveat | `.callout` (`.warn`, `.risk`) |
     | Backticked file path | `code.file`; other inline code stays `<code>` |
     | `*(inferred)*` after a claim | `<span class="badge warn">inferred</span>` |
     | Mermaid block followed by an `*italic caption*` line | `<figure><pre class="mermaid">` with that `<figcaption>` |

   - Severity badges on findings: High is `badge risk`, Medium is `badge warn`, Low is a plain `badge`. Use `badge ok` only for positive status (tested, healthy).
   - Copy every Mermaid block into a `<pre class="mermaid">` in the same order. Pele (Mermaid syntax) renders them, themed by the template's CSS. In the 12-node diagram limit, sequence diagram participants count as nodes.
   - Escape `<`, `>`, `&` in code, text, and diagram source.
3. **Validate, then fix until it passes**:

   ```bash
   node <this-skill-dir>/scripts/check-report.mjs docs/handover
   ```

   It fails on unfilled `{{PLACEHOLDERS}}` or leftover guide comments, missing or empty sections, a section count other than nine in the Markdown, a different number of diagrams in the two files, any Mermaid diagram that does not parse, and a modified Pele script tag. It needs Node 18+ and no network. If Node is unavailable, say so and at least confirm `grep -n '{{' docs/handover/handover.html` prints nothing.

Only when the user asks for an offline report: copy `assets/pele.global.js` from this skill next to `handover.html` and replace the Pele tag with `<script src="pele.global.js"></script>` (a local file cannot use the `integrity` check from a `file://` page). The checker accepts both forms.

In the chat, reply with a short summary (purpose, stack, top 3 risks), the paths of both files, and the checker's result. Do not paste the whole report into chat.

## Interaction rules

- **Always cite files.** Every feature and flow references its specific path so the user can open it directly.
- **Large repos go in stages.** If the repo is very large (monorepo, many services), first deliver sections 1 to 4 and fill sections 5 to 9 with "Pending: continues per module", then offer to continue with architecture, data model, and risks per module.
- **Offer, don't overreach.** Suggest extra analysis (security review, test coverage, dependency audit) when it looks valuable, but only do it if the user asks.
