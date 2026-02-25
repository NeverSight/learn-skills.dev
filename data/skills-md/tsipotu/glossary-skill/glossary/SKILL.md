---
name: glossary
description: Create and manage a project-wide ubiquitous language glossary — a shared vocabulary that developers, product managers, UX designers, QA engineers, and business analysts all use consistently. Use this skill whenever the user mentions "glossary", "terminology", "ubiquitous language", "what does X mean", "define a term", "add a term", "look up term", "glossary health", "stale terms", or wants to establish, query, or maintain shared project vocabulary. Also use when writing code, tests, or specs and consistent terminology matters — the glossary is the single source of truth for what terms mean in this project.
---

# Glossary — Ubiquitous Language Manager

Manage a project's shared vocabulary as version-controlled YAML files. The glossary bridges the gap between what developers call things in code (`cart_item`), what users see in the UI ("Shopping Bag"), and what the team says in meetings ("basket"). It's the single source of truth for terminology — consumable by humans, AI tools, CI pipelines, and future web frontends alike.

Inspired by Domain-Driven Design's [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html) and compatible with [Contextive](https://docs.contextive.tech/community/guides/setting-up-glossaries/).

## Glossary location and discovery

The glossary can live anywhere in the project. Users may choose a custom path (e.g. `docs/terminology/`, `content/glossary/`). **Always resolve the glossary root before reading or writing.**

**Discovery order:**

1. **Explicit pointer** — Check project config for a stated glossary path:
   - **CLAUDE.md** — section like "Glossary: `path/to/glossary`" or "Glossary lives in `…`"
   - **.cursorrules** or **AGENTS.md** — terminology or glossary path
   - **README.md** — project structure or "Glossary" section
2. **Conventional locations** (if no pointer found):
   - `glossary/glossary.config.yml` (project root)
   - `docs/glossary/glossary.config.yml`
   - `.claude/glossary/glossary.config.yml`
3. **Search** — Look for any `glossary.config.yml` in the project. If exactly one is found, use its directory as the glossary root. If multiple, list them and ask the user which to use.

**If no glossary exists:** Proceed to **Scaffolding** and create the glossary at the **project root** (`glossary/`) unless the user asks for a different location. If they specify a path, create it there and add a pointer in CLAUDE.md or .cursorrules so future discovery finds it.

All paths in this skill (e.g. "read the context file", "append to the correct glossary file") are relative to the **resolved glossary root** (the directory containing `glossary.config.yml`).

## Modes

The skill operates in three modes based on what the user asks.

### Explore (default)

When the user wants to look something up. Resolve the glossary root (see **Glossary location and discovery**), then read the relevant glossary files under that root and answer the question.

- **"What does Order mean?"** — look up the term, show its definition, context, code_name, ui_label, and relationships. If it appears in multiple contexts, show both definitions and explain how they differ.
- **"What terms are in checkout?"** — read the checkout context file, list all terms with brief definitions.
- **"How does Cart relate to Checkout Session?"** — trace the relationship chain through `related` fields and explain the path. Include any `when` conditions.
- **"Show me stale terms"** — scan all glossary files for terms with `status: deprecated` or `status: proposed`.
- **"What do we call X in the frontend?"** — look up the term's `ui_label`. Or reverse: given a UI label, find the `code_name`.

For the full term schema and field reference, read `references/term-schema.md`.

### Add

When the user wants to add or update terms. Walk through it conversationally — the user shouldn't need to write YAML.

**Step 1: Find the glossary.** Resolve the glossary root using **Glossary location and discovery** above. If no glossary exists, switch to **Scaffolding** (see below).

**Step 2: Understand the term.** Ask the user:

- What's the term?
- What does it mean? (in plain language)
- What do developers call it in code? (`code_name`)
- What do users see in the UI? (`ui_label`)
- Which context does it belong to?

Don't ask all questions at once — infer what you can from context. If the user says "add Cart to the checkout glossary," you already know the name and context. Just ask for the definition and the fields you can't infer.

**Step 3: Check for conflicts.** Before adding:

- Does this term already exist in this context? → Offer to update instead
- Does it exist in a different context? → Flag as cross-context term, ask if intentional
- Is it an alias of an existing term? → Suggest adding to that term's `aliases` instead
- Does the `code_name` or `ui_label` conflict with another term? → Flag the collision

**Step 4: Suggest relationships.** Based on existing terms in the glossary:

- "I see Cart already exists. Does Cart contain this new term?"
- "Checkout Session is in the same context. How does this term relate to it?"

Only suggest relationships that make sense. Don't force the user to define relationships for every term — orphan terms are fine, especially early on.

**Step 5: Write the YAML.** Generate the term entry with the separator comment, append it to the correct context file under the resolved glossary root, and regenerate `relationships.md` in that root if any relationships were defined.

Show the user the generated YAML before writing it. Let them adjust.

### Maintain

When the user wants to check the health of the glossary. Resolve the glossary root (see **Glossary location and discovery**), then load all glossary files under that root and run checks:

- **Orphan detection** — terms with no relationships (no `related` and not referenced by any other term). List them. Not necessarily a problem, but worth reviewing.
- **Stale term review** — terms with `status: deprecated`. Ask if they should be removed or if the replacement term needs updating.
- **Consistency check** — scan the codebase for identifiers that match or resemble `code_name` values. Report:
  - Code identifiers not in the glossary (potential missing terms)
  - Glossary `code_name` values that don't appear in the code (potentially stale)
- **Cross-context conflict report** — terms with the same `name` in multiple context files. Show how their definitions differ. Ask if the divergence is intentional.
- **Relationship integrity** — check that every term referenced in a `related` field actually exists in the glossary. Flag broken references.
- **Relationship diagram** — regenerate `relationships.md` with Mermaid diagrams.

Present findings as a report with suggested actions. Don't auto-fix anything — let the user decide.

## Scaffolding

When the skill is invoked in a project with no glossary, bootstrap the structure.

**Step 1: Ask about the project.**
"What's this project about? What are the main domain areas?"

**Step 2: Propose bounded contexts.**
Based on the answer, suggest 2-4 initial contexts. Always include `core` for terms shared across the whole project. Present as a checklist:

> I'd suggest starting with these contexts:
>
> - [x] **core** — terms shared across the whole project (User, Permission, Notification)
> - [x] **auth** — authentication and authorization
> - [x] **billing** — payments, subscriptions, invoicing
>
> Want to adjust these?

**Step 3: Scaffold the directory.**
Create the glossary directory at the **project root** as `glossary/` (unless the user asked for a different path). That directory must contain:

- `glossary.config.yml` with project name, description, and context entries
- One `.glossary.yml` file per context, each with the context header and empty `terms: []`
- An empty `relationships.md`

**Step 4: Seed from the codebase.**
Scan for likely domain terms:

- Model/entity names from source code (class names, type definitions)
- Component names from frontend code
- Terms from existing `.feature` files
- Domain language from README and docs

Present findings as suggestions — never add terms automatically:

> I found these terms in your codebase that aren't in the glossary yet:
>
> - `User` (appears in 34 files)
> - `Session` (appears in 12 files)
> - `CartItem` (appears in 8 files — likely "Cart Item")
>
> Want to add definitions for any of these?

**Step 5: Update project configuration.**
If the project has any of these files, add a glossary pointer so discovery finds the glossary next time:

- **CLAUDE.md** — add a Glossary section with the path (e.g. `Glossary: glossary/` or the custom path used)
- **.cursorrules** — add a terminology note with the glossary path
- **README.md** — add a mention in the project structure section

If you scaffolded at a **custom path** (user requested), always add or update a pointer. Only touch files that already exist. Don't create new config files for tools the project doesn't use.

## How Other Skills Use the Glossary

The glossary is plain YAML; its root is resolved the same way as in this skill. Any skill or tool can read it — no special API needed. The file format is the API.

When another skill (e.g. gherkin) needs terminology:

1. Resolve the glossary root using the same **Glossary location and discovery** (pointer → conventional locations → search).
2. Read `glossary.config.yml` in that root to find context files.
3. Read the relevant context file(s) based on scope (paths relative to the glossary root).
4. Use terms in its output (ui_label for user-facing text, code_name for technical text).

The glossary skill doesn't need to be invoked for this — other skills read the files directly once the root is known.

### Integration examples

| Tool | How it uses the glossary |
| --- | --- |
| **Gherkin skill** | Reads `ui_label` for Then/When steps, `code_name` for Given setup. `when` conditions map to scenario Given steps. |
| **Code review** | Flags variable names that don't match `code_name` entries |
| **Testing** | Validates test names use consistent terminology |
| **CI linting** | Script validates code identifiers against `code_name` entries |
| **Web frontend** | Serves YAML files as JSON via API |

## Loading Strategy

Don't load the entire glossary into context. Use tiered loading:

| Tier | What | When |
| --- | --- | --- |
| **Pointer** | Glossary path from CLAUDE.md / .cursorrules / discovery | Every session (negligible) — yields the glossary root |
| **Scoped** | Relevant context file(s) + core (under that root) | When this skill or another skill needs terminology |
| **Full** | All glossary files under the resolved root | Maintain mode only |

Use the `scope` field in `glossary.config.yml` to determine which context files are relevant. If working in `src/checkout/`, load `checkout.glossary.yml` + `core.glossary.yml` from the glossary root. If scope is ambiguous, ask: "Which context are you working in?"

## Compatibility

The YAML format is compatible with [Contextive](https://docs.contextive.tech/community/guides/setting-up-glossaries/). Contextive's VS Code extension can read these files and show hover definitions in the editor — it picks up `name` and `definition`, ignoring extra fields like `code_name` and `related`.
