---
name: code-documentation
description: This skill should be used when the user asks to "write documentation", "document this", "add a README", "create a changelog", "write a daily log", "document this service", "write an ADR", "create a technical report", "add JSDoc", "add docstrings", "document this API", "write a post-mortem", "create architecture docs", "update the docs", "write a migration guide", "document this decision", "create a service overview", "write a TESTS.md", or asks how to document any code, service, feature, or architectural decision. Covers both continuous documentation (daily logs, changelogs, API docs) and one-off documentation (reports, ADRs, post-mortems, migration guides) for any tech stack.
version: 1.0.0
---

# Code Documentation

Produce documentation that is discovered, read, and trusted over time. Every documentation task falls into one of two modes: **continuous** (routine, append-only, low friction) or **one-off** (deliberate, structured, time-bounded).

## Philosophy

Documentation exists to reduce future cognitive load — for the next engineer, the next agent, or the future self. Prioritize:

1. **Proximity** — docs live as close to the code as possible
2. **Brevity** — say what happened and why; skip what and how (the code shows that)
3. **Freshness** — outdated docs are worse than no docs
4. **Audience fit** — write for the next reader, not the current author
5. **Discoverability** — a doc no one finds is not a doc

## Documentation Taxonomy

Two axes govern every documentation decision:

**Axis 1: Longevity**
- **Continuous** — logs, changelogs, inline docs, API docs (ongoing maintenance)
- **One-off** — reports, ADRs, post-mortems, migration guides (created once)

**Axis 2: Placement**
- **Inline** — docstrings, comments, type annotations (lives in code)
- **Service-level** — README, ARCHITECTURE, TESTS.md (lives in the service directory)
- **Project-level** — `daily/`, `reports/`, `plans/`, `changelog/` (lives in `docs/`)
- **External** — wikis, Notion, Confluence (lives outside the repo)

## Quick Decision Guide

| Task | Type | Location |
|------|------|----------|
| What changed today | Continuous | `docs/daily/YYYY-MM-DD.md` |
| What this service does | Service-level | `services/name/README.md` |
| Why this architecture decision | One-off | `docs/reports/YYYY-MM-DD/adr-name.md` |
| Customer-facing release notes | Continuous | `docs/changelog/YYYY-MM-DD/` |
| API endpoint behavior | Inline + schema | docstrings + OpenAPI/schema file |
| Incident post-mortem | One-off | `docs/reports/YYYY-MM-DD/post-mortem.md` |
| Migration steps | One-off | `docs/plans/YYYY-MM-DD/migration-name.md` |
| Complex function explanation | Inline | comment above function |
| Component props/usage | Inline | JSDoc / TSDoc / Storybook |
| Component, hook, or route contract | Inline + local feature doc | TSDoc plus nearby README or feature doc when behavior spans files |
| Testing patterns | Service-level | `services/name/TESTS.md` |
| Investigation findings | One-off | `docs/reports/YYYY-MM-DD/report-name.md` |
| How-to guide | Project-level | `docs/cookbook/guide-name.md` |

---

## Continuous Documentation

### Daily Logs

Daily logs are the single most important continuous documentation habit. Write them after every meaningful change — new features, bug fixes, refactors, config changes.

**Rules (non-negotiable):**
- Append to the **latest existing date file** — never create new files
- **2 bullet points max** per change
- Format: **what happened + why** (not how — the code shows that)
- Past tense, active voice

**Finding the latest file:**
```bash
ls docs/daily/ | sort | tail -1
# Or use the helper script: .agents/skills/code-documentation/scripts/find-docs.sh
```

**Format:**
```
- Fixed OAuth token refresh by adding missing redirect URI — was causing silent login failures on mobile
- Refactored candidate serializer to use RetrievalLevelMixin — removed ad-hoc to_representation override
```

### Changelogs

Two distinct changelog types serve different audiences:

**Customer-facing** (`docs/changelog/YYYY-MM-DD/`): Features, fixes, improvements visible to users. Plain language. No implementation details. Written after release.

**Internal** (`docs/daily/`): Technical changes, refactors, infrastructure for the engineering team.

### Inline Documentation

Inline docs are the highest signal-to-noise documentation — they live next to the code they describe.

**Docstrings**: Required on all public functions, methods, classes, and modules. Include: purpose, params, return value, raised exceptions, and any non-obvious side effects.

**Comments**: Only where logic isn't self-evident. Explain *why*, never *what*.

**Type annotations**: Use throughout all code. They are documentation.

**Anti-patterns:**
- Comments that restate the code (`# increment counter`)
- Outdated comments that no longer match the code
- Missing docstrings on public APIs
- Over-documenting private implementation details

---

## One-Off Documentation

### Technical Reports

Use for: architecture audits, investigation findings, performance analyses, security reviews.

Structure: `summary → context → findings → evidence → recommendations`

Location: `docs/reports/YYYY-MM-DD/report-name.md`

### Architecture Decision Records (ADRs)

Use for: decisions with non-obvious trade-offs that future engineers will question.

Format: `context → decision → consequences → alternatives considered`

Write an ADR when: the decision is irreversible or expensive to reverse, the trade-offs are non-obvious, or the decision contradicts a common pattern for good reason.

Location: inline in service README *or* `docs/reports/YYYY-MM-DD/adr-name.md`

### Post-Mortems

Use for: any production incident or significant bug causing user impact.

Structure: `impact → timeline → root cause → contributing factors → action items`

Tone: blameless, factual, forward-looking. Never assign individual blame.

Location: `docs/reports/YYYY-MM-DD/post-mortem-incident-name.md`

### Migration Guides

Use for: schema changes, API breaking changes, service restructuring.

Structure: `motivation → before/after state → step-by-step → rollback plan → verification`

Location: `docs/plans/YYYY-MM-DD/migration-name.md`

---

## Service Documentation

Every service or module directory should have, at minimum:

```
services/service-name/
├── README.md         # What it does, when to use it, key concepts
├── ARCHITECTURE.md   # How it works internally, data flows, design decisions
└── TESTS.md          # Testing patterns, how to run, what's covered
```

Additional files as needed:
- `SETUP.md` — non-obvious configuration or initialization
- `OVERVIEW.md` — high-level conceptual overview for newcomers
- `CHANGELOG.md` — version history (if the service has versioned releases)
- `FAQ.md` — common questions, troubleshooting, gotchas

**README minimum requirements:**
1. One-sentence description of the service's purpose
2. When to use it vs. alternatives (what it's NOT)
3. Key concepts (2–5 bullets)
4. Quick start or usage example
5. Links to ARCHITECTURE.md and TESTS.md

---

## API Documentation

**Backend (REST/Django/FastAPI/Express):**
- Docstrings on all view classes, endpoint functions, and serializers
- Document request body shape, auth requirements, query params, and error codes
- OpenAPI/Swagger annotations where the framework supports them

**Frontend (JS/TS):**
- JSDoc/TSDoc on all exported functions, hooks, and components
- Document props (type, required, default, description) for all components
- Mark deprecated items with `@deprecated` and provide migration path

## Frontend Documentation

Frontend docs should capture contracts that types and screenshots alone do not make obvious.

- Document reusable components, hooks, stores, and route helpers at the public boundary, not by narrating internal implementation.
- When a feature spans multiple files, add a nearby feature or service doc that explains ownership: data, URL state, form state, client state, side effects, and analytics.
- For user-facing flows, document important states and constraints: loading, empty, error, success, disabled, optimistic, permission-restricted, and responsive behavior.
- Record accessibility expectations when they are part of the contract: labeling, keyboard flow, focus behavior, dialogs, and destructive-action safeguards.
- If automated coverage does not yet protect a risky frontend flow, include concise manual verification notes in the most natural nearby doc until tests exist.

---

## Project Documentation Placement Rules

**Never create new top-level directories in `docs/`**. Use the existing structure:

```
docs/
├── daily/          ← development logs (append only, YYYY-MM-DD.md)
├── reports/        ← audits, analyses, investigations (YYYY-MM-DD/ folders)
├── plans/          ← specs, plans, migrations (YYYY-MM-DD/ folders or flat)
├── changelog/      ← customer-facing releases (YYYY-MM-DD/ folders)
├── cookbook/       ← how-to guides (flat, no timestamps)
├── references/     ← code references, schemas (flat)
└── snapshots/      ← deep-dive analyses (YYYY-MM-DD/ folders, explicit request only)
```

**Repo-local instructions override this structure** — always check for `AGENTS.md`, `CLAUDE.md`, or similar files that define project-specific doc placement rules before writing anything.

---

## Quality Standards

Good documentation passes this test: **can a new engineer understand what they need to know from this doc alone, in under 2 minutes?**

**Before writing, ask:**
- Who reads this? What do they need to know?
- Where does it live? Is that the most natural location?
- How long should it be? (Default: shorter than you think)
- When does it become outdated? Who updates it?

**After writing, verify:**
- Does every sentence earn its place?
- Are there code examples where prose would be slower to parse?
- Does the structure match how readers scan (headers, bullets, tables)?
- Is the tone right for the audience (technical vs. customer-facing)?
- Is there an existing doc to update rather than a new one to create?

---

## Additional Resources

### Reference Files

For in-depth guidance, consult:
- **`references/documentation-types.md`** — Full taxonomy of all doc types, audience, examples, when to use each
- **`references/continuous-docs.md`** — Deep guide on daily logs, changelogs, API docs, inline docs, and maintenance cadence
- **`references/frontend-documentation.md`** — Component, hook, route, design-system, and browser-behavior documentation guidance
- **`references/one-off-docs.md`** — Full guide for reports, ADRs, post-mortems, migration guides, investigation reports
- **`references/writing-standards.md`** — Tone, voice, tense, structure, anti-patterns, quality checklist, audience patterns

### Templates

Ready-to-use templates in `templates/`:
- **`templates/daily-log.md`** — Daily log format, examples, edge cases
- **`templates/technical-report.md`** — Technical report structure
- **`templates/adr.md`** — Architecture Decision Record
- **`templates/service-readme.md`** — Service README skeleton
- **`templates/changelog-entry.md`** — Changelog entry for both audiences
- **`templates/post-mortem.md`** — Post-mortem structure

### Scripts

Utility scripts in `scripts/`:
- **`scripts/find-docs.sh`** — Locate the latest daily log file and relevant doc locations in any repo
