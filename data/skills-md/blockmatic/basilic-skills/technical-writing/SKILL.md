---
name: technical-writing
description: Write, edit, and review technical docs in Basilic-based repos—Docu MDX, READMEs, and root product markdown—verifying every claim against source and keeping prose direct, accurate, and free of AI patterns.
---

# Technical writing

Write accurate, task-focused documentation for developers and coding agents. Each section should be easy to scan, retrieve, and act on without unstated context.

## Consuming repo

Read the repo's `AGENTS.md` before you write: doc layers, public one-liner, capability names, banned copy, and where `DESIGN.md` lives. Glob rules in `.cursor/rules/` override this skill. For which layer to update (MDX vs README vs rules), use `/w-docs`—do not duplicate its routing table here.

## Voice

- Address the reader as `you`; use imperative verbs for steps. Active voice, present tense, concrete nouns.
- American English, Oxford comma. Write `eve` lowercase when naming the runtime.
- Lead each page and section with the answer or outcome. One primary job per page.
- Preserve the author's supported meaning, nuance, and uncertainty. Make the minimum effective edit; leave strong prose alone.
- Use `we` only when describing a deliberate team action documented in the repo.

Ban filler and hype: `easy`, `simple`, `quick`, `just`, `obviously`, `utilize`, `facilitate`, `leverage`, `robust`, `seamless`, promotional adjectives, rhetorical questions, engagement bait.

Ban AI tells: summary transitions (`With this setup complete…`), stop-start fragments, datasheet verbs (`provides`, `is configurable`), cold opens with no antecedent, template closers and closing proverbs, manufactured specificity to sound human.

Cadence. Bad: "The API is flexible. It supports many use cases. That is the value. You will like it." Good: "Register the route in `apps/api`, expose it in OpenAPI, then run the client generator so the web app picks up typed calls."

## Sources of truth

Do not rely on training data for behavior. Verify in this order:

1. Owning source, public types, and tests in the repo
2. CLI help and package scripts named in the nearest README
3. Existing MDX or markdown in the doc layer `AGENTS.md` names
4. ADRs and architecture pages—proposed intent until merged behavior matches
5. Issues and user reports—to learn the reader's problem, not to establish product truth

If a claim cannot be verified, omit it or name the missing owner. Never leave `[VERIFY]` in finished copy. Do not document proposed behavior as shipped.

## Method

1. Name the piece's one job and the reader's task.
2. Find the page that already owns the topic; extend it before creating a new page.
3. Outline: outcome → prerequisites → happy path → alternatives → failures → related links.
4. Draft and verify claims together against source.
5. Self-edit for retrieval: repeat full nouns in key statements; put the critical fact locally, not only behind a link.
6. Review passes: purpose and structure, accuracy, completeness, style and retrieval, diff discipline (no drive-by rewrites).

## Modes

**Docu MDX** (when the repo has `apps/docu/content/docs/`): `title` and `description` frontmatter; folder `meta.json` when navigation changes; inbound body link from a related hub (no orphan pages); permanent redirects in doc app config when a route moves; MDX components only where nearby pages already use them. Finish with `pnpm --filter @repo/docu checktypes` when preparing to ship doc changes.

**README** (`**/README.md`): follow `.cursor/rules/base/readme.mdc`—root owns the product story; apps and packages stay lean with links to technical docs.

**Root product markdown** (e.g. `PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md` when `AGENTS.md` says so): same voice; capability names match that repo's architecture source; upstream hosted docs win only where `AGENTS.md` says they override local project docs.

## Constraints

- NEVER invent flags, endpoints, defaults, examples, metrics, or user reactions.
- NEVER turn one support thread into a new page without deciding docs vs product scope.
- NEVER duplicate a broad guide when a section or cross-link fixes the gap.
- NEVER contradict the consuming repo's public one-liner, banned copy, or capability names for narrative convenience.
- Support evidence identifies confusion; implementation and tests establish behavior.

## Not this skill

- `/w-docs` — which layer to patch
- `/w-api-docs` — OpenAPI and generated clients
- `/w-deslop` — code slop on branches
- `/w-architecture` — ADR and boundary planning
- Personal or marketing voice catalogs (e.g. gabo)
