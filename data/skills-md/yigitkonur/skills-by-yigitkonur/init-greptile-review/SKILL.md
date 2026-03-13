---
name: init-greptile-review
description: Use skill if you are generating `.greptile/` review config, scoped rules, or context-file mappings for Greptile pull request reviews in a specific repository.
---

# Init Greptile Review

Generate repo-specific Greptile configuration that makes Greptile catch meaningful bugs, security issues, architectural violations, and contract drift without wasting semantic review budget on lint-like trivia.

## What good Greptile setup looks like

Greptile is a semantic PR reviewer, not a linter.

- Use Greptile for architecture boundaries, security invariants, API contracts, performance pitfalls, dependency misuse, compliance, and cross-file reasoning.
- Leave semicolons, formatting, import sorting, and other linter/formatter work to ESLint, Prettier, Ruff, RuboCop, golangci-lint, and similar tools.
- Greptile reads repo-local config from the **source branch** of the PR.
- Changes apply on the **next PR or re-review**, not retroactively.
- Prefer `.greptile/` over legacy `greptile.json`.

## Decision tree

```
What are you doing?
│
├── First-time setup, permissions, or indexing ───────────────► references/setup.md
├── Authoring or tuning .greptile/config.json / files.json ──► references/config-spec.md
├── Designing repo-specific review rules ─────────────────────► references/rules-engineering.md
├── Matching a common stack or monorepo layout ───────────────► references/patterns.md
├── Needing full end-to-end examples ─────────────────────────► references/scenarios.md
├── Wiring status checks, API triggers, or CI/CD ─────────────► references/integration.md
└── Debugging ignored config, noisy reviews, or rollout checks ► references/troubleshooting.md + references/anti-patterns.md
```

## Quick start

By default, generate only the files the repo actually needs:

```
.greptile/
├── config.json      # always
├── rules.md         # only when rules need examples, migration notes, or nuanced narrative
└── files.json       # only when docs/specs/schemas materially improve review

packages/payments/.greptile/config.json  # only when a subtree needs different strictness or extra rules
```

Start lean:

- Default to `strictness: 2` and `commentTypes: ["logic", "syntax"]`
- Add `"style"` only when the repo lacks strong formatting/linting
- Start with **5-10 high-signal rules**, not 20 generic ones
- If migrating from `greptile.json`, move to `.greptile/` and delete the legacy file

## Workflow

Follow these six phases in order.

### Phase 1: Classify the request and current Greptile state

> **Read first:** `references/setup.md` for platform and placement questions; `references/config-spec.md` for parameter formats.

Before writing anything, determine what kind of job this is:

- **New setup** — no existing `.greptile/` or `greptile.json`
- **Tune existing config** — root config exists and should be extended, not replaced
- **Monorepo split** — different packages/services need different strictness or rules
- **Troubleshooting** — existing config is ignored, noisy, or missing real issues
- **Integration** — status checks, API triggers, CI/CD, or merge gating

Search the repository for these items (e.g. `find . -name '.greptile' -type d`, `find . -name 'greptile.json'`):

- Existing `.greptile/` folders at root and child directories
- Legacy `greptile.json`
- Docs, specs, and schemas that could feed `files.json` — look for: Prisma/Drizzle schemas, OpenAPI/Swagger specs, ADR documents, architecture docs (`docs/`, `architecture.md`), shared type definition files. Exclude READMEs and changelogs. Note these for Phase 2 refinement.
- Existing linters/formatters — check root config files (`.eslintrc*`, `prettier.config*`, `biome.*`, `.stylelintrc*`, `pyproject.toml`, `.rubocop.yml`) and `package.json` / `pyproject.toml` devDependencies for linter/formatter packages

> **⚠ Steering:** When searching for docs/specs/schemas, look for file extensions and paths, not file contents. Use commands like: `find . -name '*.prisma' -o -name 'openapi*' -o -name '*.graphql'` and `ls docs/ architecture.md ADR* 2>/dev/null`. Exclude READMEs and changelogs — they rarely contain information a reviewer needs.

If config already exists, preserve working pieces and tighten only what the repo evidence supports.

### Phase 2: Map the review surface

> **Read first:** `references/patterns.md` for stack-specific patterns and ignore lists.

Map the repository by reading the workspace config (e.g. `pnpm-workspace.yaml`, `lerna.json`, `Cargo.toml`), listing top-level directories, reading root and app-level dependency manifests, and searching for risk-sensitive directories. Cover these seven areas:

1. **Structure** — monorepo vs single-service, top-level packages/apps/services, critical directories
2. **Stack** — languages, frameworks, ORM, transport layers, testing stack
3. **Risk zones** — auth, payments, PII, file system, shell execution, IPC, migrations, infra
4. **Generated/noisy files** — build output, generated code, lockfiles, snapshots, vendored code
5. **Useful context files** — refine the list from Phase 1; add any newly discovered architecture docs, ADRs, OpenAPI specs, schemas, shared types, or contribution guides
6. **Existing quality controls** — linters, formatters, CI, custom rules, security scanners
7. **Recurring failure patterns** — user-stated pain points, incident history, review gaps, repeated bugs. If no user input is available, infer from recent commit history (e.g. `git log --oneline --grep='fix' --grep='bug' --grep='revert' | head -20`) or skip this item.

> **⚠ Steering:** "Map the repository" means reading config files and directory structure, not reading every source file. For item 7 (recurring failure patterns), if the user hasn't stated pain points, run `git log --oneline --grep='fix' --grep='bug' --grep='revert' | head -20` to infer from history, or skip this item entirely.

**Depth guidance:** for a small repo (<50 files), a directory listing and dependency manifest may suffice. For a large monorepo, check each top-level package's purpose, key dependencies, and risk-sensitive directories. Stop when you can confidently answer all 7 items above.

**Exploration checklist** — confirm you can answer these before proceeding:
- [ ] What is the repo structure? (monorepo/single-service, key directories)
- [ ] What languages and frameworks are used?
- [ ] Where are the risk-sensitive paths? (auth, payments, PII, shell, IPC)
- [ ] What linters/formatters already exist?
- [ ] Are there context-worthy docs, schemas, or specs?
- [ ] What should be ignored? (generated code, build output, lockfiles)

Treat file targeting as part of the design: the same repo map should drive `rules`, `files.json`, `ignorePatterns`, child configs, and any `patternRepositories`.

### Phase 3: Choose file topology and strictness

> **Read first:** `references/config-spec.md` for parameter formats and cascading behavior.

**Always generate:** root `.greptile/config.json`

**Generate only when needed:**

- `.greptile/rules.md` — when a rule cannot be expressed as a single sentence under 200 characters, or when good/bad code examples are essential for the reviewer to apply it correctly
- `.greptile/files.json` — when a context file provides information a reviewer would need to validate correctness (e.g. a database schema to validate model field usage, an API spec to validate endpoint contracts, shared types to check interface conformance)
- Child `.greptile/config.json` — a subtree needs different strictness, extra rules, or `disabledRules`

> **⚠ Steering:** The decision thresholds are: (a) use `rules.md` when a rule needs >200 characters or good/bad code examples to be understood; (b) use `files.json` when a context file provides information the reviewer *needs* to validate correctness — not just "nice to have" background reading; (c) use child configs only when a subtree's rules, strictness, or comment types genuinely differ.

**Monorepo rule:** prefer root defaults plus child overrides only where review needs truly diverge.

Inheritance that matters:

- Child `rules` **extend** parent rules
- Child `disabledRules` turns off parent rules by `id`
- Child `strictness`, `commentTypes`, and `triggerOnUpdates` **override**
- Child `ignorePatterns` **extend**

Strictness guidance:

- `2` for most production code
- `1` for payments, auth, security-critical, or compliance-heavy paths
- `3` for internal tools, prototypes, or low-risk directories where noise must stay low

Only tune PR filters (`labels`, authors, branches, `fileChangeLimit`) or summary behavior when the user asks for it or the repo workflow clearly needs it.

### Phase 4: Engineer semantic rules from architecture signals

> **Read first:** `references/rules-engineering.md` for the rule quality bar and category catalog.

Every rule must be **repo-specific, specific, measurable, actionable, scoped, semantic, and identifiable**.

Use the repo signals to decide which rule categories matter:

| Repo signal you observe | Prefer rules about | Typical targeting move |
|---|---|---|
| Auth, payments, PII, file system, shell, IPC, secrets | Security + compliance | High severity, scoped to the sensitive subtree; consider child strictness `1` |
| Controllers/services/repositories, package boundaries, gateway clients, shared libraries | Architecture boundaries | Scope to the layers/packages where dependency direction matters |
| OpenAPI specs, shared SDKs, backend repos, design systems | API contracts + dependencies | Scope to routes, client hooks, components, or integration code; use `files.json` or `patternRepositories` if they materially help |
| ORM usage, query builders, background jobs, caching, async workflows | Performance + data integrity | Scope to DB, views, serializers, jobs, workers, or service paths |
| Monorepo packages with different stacks or risk profiles | Cascading configs | Root defaults, then child configs only for packages that need different behavior |

Rule-writing heuristics:

- Start with **5-10 rules max**
- Tie each rule to an actual repo path, library, contract, or failure mode
- Tell Greptile what the correct alternative is, not just what to avoid
- Give every parent-level rule an `id` if a child config might disable it
- If a rule applies to the majority of files in the repository rather than a specific subsystem, it is probably too broad — narrow the scope or reconsider whether it's linter work

> **⚠ Steering:** A rule that applies to the majority of files in the repository is almost certainly too broad. Ask: "Does this rule fire on a specific subsystem, or on everything?" If it fires on everything, it's probably linter work (e.g. "no console.log") or needs aggressive scoping. Also, to verify no rule duplicates a linter: for each rule, ask "Could ESLint/Pylint/RuboCop catch this with a regex or AST rule?" If yes, delete it.

### Phase 5: Scope rules, context, and file targeting precisely

> **Read first:** `references/patterns.md` for universal ignore patterns and stack-specific targeting.

Use Greptile's semantic budget where it matters:

- `scope` must be an **array** of globs, never a comma-separated string
- `ignorePatterns` must be a **newline-separated string**, not an array
- Scope context files to the code they inform; do not attach a Prisma schema to frontend components
- Use `patternRepositories` only for real cross-repo contracts or design systems, in `org/repo` format
- Start with the universal ignore patterns from `references/patterns.md` and add project-specific patterns for any generated or high-noise directories discovered in Phase 2
- If strong linting/formatting already exists, do **not** add style-focused Greptile rules
- If the repo uses status checks, merge gating, or CI/CD triggers, see `references/integration.md` for wiring Greptile into the delivery workflow

When deciding between JSON rules and prose rules:

- Use `config.json` for crisp pass/fail rules
- Use `rules.md` only when examples or narrative make the rule materially easier for Greptile to apply

### Phase 6: Validate, output, and recover if needed

> **Read first:** `references/troubleshooting.md` for diagnostic flow and canary verification; `references/anti-patterns.md` for preflight checks.

Before finalizing any output:

- [ ] JSON validates locally (for example: `python3 -m json.tool .greptile/config.json`)
- [ ] `scope` values are arrays of strings
- [ ] `ignorePatterns` is a newline-separated string
- [ ] `strictness` is 1, 2, or 3
- [ ] `commentTypes` only uses `"logic"`, `"syntax"`, `"style"`, `"info"`
- [ ] `patternRepositories` uses `org/repo`, not full URLs
- [ ] `files.json` only points to files that actually exist
- [ ] No rule duplicates lint/format tooling — review each rule against the litmus test: if ESLint, Pylint, RuboCop, or a regex grep could catch it, remove it
- [ ] No `.greptile/` + `greptile.json` coexistence remains after migration

> **⚠ Steering:** Output format matters. Agents commonly forget to include (a) the file tree, (b) reasoning annotations tied to repo evidence, or (c) the canary test. Use the output template: file tree → complete file contents → reasoning annotations (markdown list with **rule-id**: reason format) → canary rule → migration notes. See `references/scenarios.md` for complete examples of properly formatted output.

Output every generated configuration in your response to the user with:

1. A markdown code block showing the `.greptile/` directory structure (file tree)
2. Complete file contents for each generated file
3. Reasoning annotations as a markdown list tied to specific repo evidence, e.g.:
   - **auth-wrapper-required**: Added because all API routes use `withWorkspace`/`withSession` wrappers (see `lib/auth/workspace.ts:58`)
   - **stripe-webhook-sig**: Stripe webhook handlers process financial events at `app/api/stripe/webhook/`; unverified payloads allow forged billing
4. A canary test: a temporary rule to verify Greptile reads the config. Example: `{ "id": "canary", "rule": "Comment 'canary active' on any PR modifying a README.", "scope": ["**/README.md"], "severity": "low" }`. Open a test PR, confirm the canary fires, then remove the rule. See `references/troubleshooting.md` for the full canary protocol.
5. Migration notes if replacing `greptile.json`

See `references/scenarios.md` for complete end-to-end output examples to model your output on.

If Greptile still behaves incorrectly, recover in this order:

1. Repo indexed?
2. JSON valid?
3. `.greptile/` conflicting with `greptile.json`?
4. Config on the PR's **source branch**?
5. `scope` actually matches changed files?
6. `strictness` suppressing the severity you used?
7. Author/branch/file-limit filters excluding the PR?
8. Force a re-review, then remove any canary rule after verification

## Do this, not that

| Do this | Not that |
|---|---|
| Write rules that require semantic reasoning, architecture awareness, or cross-file understanding | Spend Greptile on semicolons, formatting, or other linter work |
| Tie each rule to actual repo evidence: paths, libraries, contracts, incident patterns | Paste generic "best practices" or framework boilerplate |
| Start lean with 5-10 high-signal rules | Dump 20-30 mediocre rules and hope strictness fixes the noise |
| Scope rules and context files aggressively | Apply database, auth, or design-system rules to the whole repo |
| Use child configs only where behavior truly differs | Create a child config for every package by default |
| Use `rules.md` for nuanced examples and migrations | Put explanatory comments inside JSON |
| Use `patternRepositories: ["org/repo"]` only when external code truly informs review | Use full GitHub URLs or add repos that do not affect review decisions |
| Raise strictness only in critical paths | Set `strictness: 1` across the whole repo without evidence |

## Minimal reading sets

### "I need to set up Greptile from scratch"

- `references/setup.md`
- `references/config-spec.md`
- `references/troubleshooting.md`

### "I need repo-specific rules that catch real issues"

- `references/rules-engineering.md`
- `references/patterns.md`
- `references/anti-patterns.md`

### "I need a monorepo design"

- `references/config-spec.md`
- `references/patterns.md`
- `references/scenarios.md`

### "I need CI/CD or status-check integration"

- `references/integration.md`
- `references/setup.md`
- `references/config-spec.md`

### "The config is noisy, ignored, or not firing"

- `references/troubleshooting.md`
- `references/anti-patterns.md`
- `references/rules-engineering.md`

## Reference files

| Reference | What it covers | When to read |
|---|---|---|
| `references/setup.md` | GitHub/GitLab install, indexing, permissions, placement, first config | First-time setup or platform questions |
| `references/config-spec.md` | Parameter formats, `.greptile/` file roles, cascading behavior, child overrides | Writing or editing `config.json`, `files.json`, or monorepo overrides |
| `references/rules-engineering.md` | Rule quality bar, categories, severity, scoping, rule lifecycle | Designing repo-specific rules |
| `references/patterns.md` | Stack patterns, ignore patterns, monorepo strategy, context-file patterns | Matching a detected architecture to a starting shape |
| `references/scenarios.md` | Complete end-to-end examples for common stacks | You need a full output example to adapt |
| `references/integration.md` | Status checks, API triggers, manual review triggers, CI/CD, notifications | Integrating Greptile into delivery workflows |
| `references/troubleshooting.md` | Diagnostic flow, common failures, validation protocol, migration steps | Config is ignored, too noisy, or not triggering |
| `references/anti-patterns.md` | Anti-pattern catalog, troubleshooting chain, canary verification | Final preflight before shipping |
| `evals/evals.json` | Evaluation scenarios covering diverse stacks | Validating generated configs against expected outputs |

## Key gotchas

- Greptile reads config from the **source branch**, not the target branch
- Config changes affect the **next PR or re-review**, not past reviews
- `ignorePatterns` skips **review**, not **indexing**
- `includeAuthors: []` means **all authors**
- `fileChangeLimit: 0` skips **all** PRs
- `statusCheck: true` suppresses "X files reviewed" comment spam better than `statusCommentsEnabled: false`
- `.greptile/` silently overrides `greptile.json`
- `scope` is an array; `ignorePatterns` is a newline-separated string
- Dashboard or org rules may still influence behavior outside repo-local files

## Final reminder

Start with the smallest relevant reading set, then expand only when the task requires it. The goal is not to write the most rules — it is to generate the smallest `.greptile/` configuration that helps Greptile catch the issues this specific repository actually misses.
