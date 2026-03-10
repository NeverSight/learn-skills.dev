---
name: writing-agents-md
description: >
  Writes (generates or updates) AGENTS.md — a token-efficient context file for AI coding agents.
  Analyzes project stack, constraints, and commands. Produces AGENTS.md and agent-specific
  imports (CLAUDE.md, .cursorrules, GEMINI.md, etc.). Preserves curated sections on update.
  Use when: the user asks to create or update AGENTS.md, CLAUDE.md, or agent context files;
  or to onboard an AI agent to a project.
compatibility: "Codex CLI, Claude Code/Desktop, Cursor, Windsurf, Gemini, GitHub Copilot (no dependencies)"
---

# Write AGENTS.md

## Objective

Generate or update the single source of truth for AI coding agents. `CLAUDE.md` is generated alongside with `@AGENTS.md` import; other agent files on request. **Scope:** current working directory (CWD). All output paths are POSIX-style and relative to CWD.

## When to use / When not to use

Use when:
- The user asks to create or update AGENTS.md, CLAUDE.md, or agent context files (`.cursorrules`, `.windsurfrules`, `GEMINI.md`, `CODEX.md`, `.github/copilot-instructions.md`).
- The user wants to onboard an AI agent to a project.

Do not use when:
- Single-file scripts, throwaway PoCs with no build config, or repos with only a README. Minimum: a build config file with at least one runnable command.
- The user wants to review (not write) an existing AGENTS.md — use a reviewing skill instead.

## Quality Bar (default)

Target outcome:
- **No spec violations** (format/schema/validation checks), and
- **Rubric score ≥ 4.5/5.0** (A- or better), and
- **No P1 findings** in a critic review

The rubric: [references/agents-md-rubric.md](references/agents-md-rubric.md) (single source of truth).

## Safety / Constraints (non-negotiable)

- Never read, request, or paste secrets (examples: `.env`, API keys, tokens, private keys, credentials).
- Do not browse the web or call external systems unless the user explicitly requests it.
- Do not run destructive commands (database resets, deploys, publishes) as part of analysis/validation.
- Only write files after explicit user approval (see User Review section).

## Analysis Phase

Execute these steps to gather facts. Do NOT include analysis output in the final file.

**Priority & triage:** When context or time is limited, focus effort in this order:
- **P0 (must):** CRITICAL section accuracy, Commands correctness, Structure validity
- **P1 (should):** Domain & Context, Patterns, Testing Strategy, Security, Env. **If workspace config detected** (turbo.json, nx.json, pnpm-workspace.yaml, workspaces in package.json, `[workspace]` in Cargo.toml, go.work): promote Monorepo to P1.
- **P2 (nice-to-have):** Monorepo (unless promoted), CI, Tool Preferences, Search, Git, Debugging

When output exceeds line budget, drop sections in reverse priority: P2 first (Debugging -> CI -> Git -> Search -> Tool Preferences -> Monorepo), then P1 (Env -> Security -> Testing Strategy -> Patterns -> Domain & Context). P0 sections are never dropped. Within a priority level, prefer keeping sections with more concrete content.

**Targeted update:** If user requests update to specific section(s), run only the analysis steps relevant to those sections. Skip full re-analysis. Validate only the changed sections plus CRITICAL (always re-validated).

**File & env safety:** Safety / Constraints rules apply. Additionally during analysis:
- Only read env *templates*: `.env.example`, `.env.template`, `.env.sample`, `.env.local.example`
- Skip binary lock files (e.g., `bun.lockb`) — detect existence via glob but do not read contents
- Env section values: use description placeholders (e.g., `DB_PASSWORD=<from secrets manager>`); never copy actual defaults from `.env.example` or source code
- Exception: well-known local-dev defaults (`localhost`, `5432`, `postgres`) may be used

**Simple project shortcut:** Apply when ALL hold: (1) One primary build config (auxiliary wrappers like `Makefile` calling `uv run ...` don't count), (2) One primary source directory (tests/scripts/docs don't count), (3) No monorepo workspace config. When triggered: run Steps 0-3 fully; for Step 4, read only the main entry point.

**Context budget:** If analysis consumes excessive context (many large config files), stop expanding detection and proceed to generation with data gathered so far. Add `<!-- GAPS: [list of skipped categories] -->` to output. Prefer breadth (detect all categories shallowly) over depth (read every file in one category).

### 0. Review Existing AGENTS.md & Agent Context Files

**If `AGENTS.md` exists**, read it first. Treat as starting point, not authoritative. Verify curated sections:

| Section | Verify against |
|---------|---------------|
| Domain & Context | README, package description, source code |
| Patterns | Actual directory layout, import conventions, code style |
| Testing Strategy | Test config files, test directory structure |
| Security | `.gitignore`, secret manager imports, env var patterns |
| Git conventions | `git log --oneline -20`, branch names (skip if not a git repo) |

Also check for pre-existing agent context files (`.cursorrules`, `.windsurfrules`, `GEMINI.md`, `CODEX.md`, `.github/copilot-instructions.md`) — if found, inform the user these can be updated alongside AGENTS.md.

**Section update policy:**

| Update mode | Sections | Behavior on re-run |
|---|---|---|
| **Auto-detect** (always regenerate) | CRITICAL, Commands, Structure, Env, Execution Context, Data & State, Search, Monorepo, CI, Tool Preferences, Debugging | Overwrite from project files |
| **Curated** (preserve if valid) | Domain & Context, Security | Keep existing; only update if verifiably stale (see below) |
| **Hybrid** (detect + merge) | Patterns, Testing Strategy, Git | Regenerate base from detection, merge manual additions |

**Staleness criteria:** Domain & Context is stale when README purpose/name changed, project type changed, or key terms reference absent identifiers. Security is stale when secret-loading mechanism changed, `.gitignore` patterns diverged, or new env templates have unlisted sensitive vars.

**Staleness removal:** Auto-detect sections: remove references to nonexistent tools/paths/commands. Hybrid sections: flag removed items with `<!-- REMOVED: [item] -- verify -->`.

**Conflicts:** prefer project files; if uncertain, add `<!-- REVIEW: ... -->`.

**Domain term extraction:** Scan README (headings, bold/italic terms, glossary sections), doc comments in entry points, and config descriptions for domain-specific terms (acronyms, business concepts, project-specific jargon). Include terms that appear in code identifiers and would be ambiguous to an agent without context (e.g., `Workspace` meaning "tenant" not "IDE workspace"). Omit universally understood terms (API, URL, JSON). If no domain terms found, omit the Key Terms field.

**No existing AGENTS.md:** Infer all sections from project files. Populate only sections with concrete evidence. **Minimum viable output:** CRITICAL, Domain & Context, and Commands must all have concrete content. If Commands would be empty, do not generate — inform user the project lacks enough structure.

### 1. Detect Stack & Identify Constraints

Scan project root for config files. If build configs exist only in subdirectories (e.g., `backend/pyproject.toml` + `frontend/package.json`), also scan one level down. Use glob to detect; read to extract details. For large files (>500 lines), grep dependency sections instead.

**Detection goals:** Scan for files listed in `references/detection-reference.md` across these categories: Build & Runtime, Quality & Hooks, Infra & Deploy, Data & APIs, Security & Observability, Docs & Meta.

**Disambiguation rules:**
- `template.yaml` -> SAM only if first 20 lines contain `AWSTemplateFormatVersion`/`Transform: AWS::Serverless`
- `app.json` -> mobile only if `expo` field or `react-native` in deps
- `volta` in `package.json` -> pinned Node/npm/yarn
- `config.yaml`/`config.yml` -> Kubernetes if contains `apiVersion` + `kind`; else app config
- `package.yaml` -> Haskell (hpack) only if `*.cabal` or `stack.yaml` also present; else treat as generic config
- `Makefile` -> task runner wrapper if targets invoke `npm`/`uv`/`cargo`/`go`/`mix`; else build system
- `Dockerfile` in multi-service repos -> note each service in Structure with its Dockerfile path

**Derive constraints:** Lock file determines mandated package manager. Forbid competing managers in same ecosystem (JS: npm/yarn/pnpm/bun; Python: pip/uv/poetry/pdm/pipenv). Cross-ecosystem lock files are not conflicts.

| Detected | Mandate | Forbid |
|---|---|---|
| Lock file in ecosystem | That package manager | Competing managers in same ecosystem |
| `biome.json` | `biome` | `eslint`, `prettier` |
| `ruff` in deps | `ruff` | `flake8`, `black`, `isort` |
| `Cargo.toml` | `cargo fmt`, `cargo clippy` | -- |
| `go.mod` + `.golangci.yml` | `golangci-lint` | -- |
| `deno.json` | `deno fmt`, `deno lint` | -- |
| `.editorconfig` | respect indent style/size | -- |
| Pre-commit hooks | -- | `--no-verify` |
| Mutually exclusive lib in deps | chosen library | replaced alternative |
| `pom.xml` (no `build.gradle*`) | `mvn` | `gradle` |
| `build.gradle` or `build.gradle.kts` (no `pom.xml`) | `./gradlew` (if `gradlew` exists) else `gradle` | `mvn` |
| `project.clj` | `lein` | `clj` |
| `deps.edn` (no `project.clj`) | `clj` | `lein` |
| `build.sbt` | `sbt` | `mill` |
| `build.mill` | `mill` | `sbt` |
| `stack.yaml` | `stack` | `cabal` |
| `*.cabal` + `cabal.project` (no `stack.yaml`) | `cabal` | `stack` |
| `.scalafmt.conf` | `scalafmt` | -- |
| `.clj-kondo/` | `clj-kondo` | -- |
| `checkstyle.xml` | `checkstyle` | -- |

**Additional rules:**
- **Lock file conflict** -> check CI to determine which manager; mandate that one. If unclear, `<!-- REVIEW: conflicting lock files -->`.
- **Private registries** -> note URL in Env (no credentials).
- **Containers** -> `docker compose run/exec` only when app runs in Docker (not infra-only like databases).
- **Monorepo** -> `turbo.json` -> `turbo run`; `nx.json` -> `nx run`/`nx affected`; note root vs package scope.
- **Polyglot (no workspace config)** -> label commands per-stack (e.g., `# install (backend)`). Don't use Monorepo section without orchestration tooling.
- **Git submodules** -> note paths in Structure.
- **Unrecognized stacks** -> read README and build config for commands. Do not guess — omit sections with no evidence.
- **Java coexistence**: When both `pom.xml` and `build.gradle*` present, check CI to determine primary; mandate that one.
- **Clojure coexistence**: `deps.edn` and `project.clj` can coexist. Prefer CI evidence. If CI is absent or ambiguous: `project.clj` present → `lein`; else `clj`. Add `<!-- REVIEW: verify Clojure build tool -->` if uncertain.
- **Gradle wrapper**: `gradlew` present -> use `./gradlew` instead of `gradle`.
- **Haskell coexistence**: `stack.yaml` + `*.cabal` is normal — Stack manages the toolchain; use `stack`.

### 2. Map Entry Points & Data

Locate main entry point(s), test runner entry & fixture locations, CI configuration.

**Execution Context:** **Host** (default / Docker infra-only) | **Docker** (app in compose) | **Devcontainer** | **Nix** | **Hybrid** | **Serverless** (Lambda/Cloud Functions/etc.)

**Project type** — classify as: **Library** (publish scripts, no deploy) | **Application** (deploy config, Dockerfile, entry point) | **CLI/Tool** (`bin`/`[project.scripts]` entries, no deploy) | **Both** (publish + deploy). Disambiguation: prefer Both if publish + deploy exist; default to Application when uncertain.

**Data, infrastructure & generated code** — detect and route:
- DB/ORM/migrations/brokers/API schemas -> Data & State (paths and metadata only; runnable commands go in Commands to avoid duplication)
- IaC/K8s/Helm -> Execution Context + Structure; Secrets -> Security; Env loading + templates -> Env
- Build output dirs (`dist/`, `target/`, `.next/`) -> Structure (generated); Codegen dirs -> Structure `(generated -- do not edit)` + CRITICAL NEVER
- Codegen workflows (OpenAPI codegen, protobuf, GraphQL codegen) -> note generation command in Commands, source schema in Data & State, output in Structure
- Observability -> Patterns; ADR/RFC -> Domain & Context; Dep scanning -> Security; Debug tooling -> Debugging
- Virtual environments -> exclude from Structure, note in Env

### 3. Extract Commands

Find exact commands from build config scripts, task runners (`Makefile`, `Justfile`, `Taskfile.yml`), or tool conventions. Include publish/release, docs, deploy/IaC, debug/REPL, codegen commands if scripts exist. Reflect pinned tool versions from CI or build config. Verify commands exist in config files — do NOT execute any commands during analysis (not even read-only ones). **Working directory:** For commands that must run from a subdirectory (e.g., migrations in a specific package), prefix with `cd <path> &&` in the Commands code block so the command is copy-pasteable from repo root.

**Recovery steps:** For each command, determine the ON FAIL recovery action. Sources: companion `:fix` scripts (e.g., `lint` -> `lint:fix`), cache-clear commands (e.g., `rm -rf node_modules`), single-file re-run variants (e.g., `vitest run <file>`), or diagnostic steps (e.g., "check output for type errors"). If the tool has a well-known fix command, use it. If not, specify the diagnostic action.

### 4. Detect Architectural Patterns

**Scope:** Only examine ecosystems detected in Step 1.

**Approach:**
1. Identify the primary framework from entry point or dependencies using the checklists in `references/framework-patterns.md`.
2. Grep source files for that framework's known convention indicators (see framework-patterns reference).
3. Scan for cross-cutting patterns not tied to a specific framework (see framework-patterns reference, "Cross-cutting" table): error handling, logging, config loading, import conventions. **In monorepos:** explicitly detect cross-package import conventions (e.g., scoped package names like `@org/pkg` vs relative paths). Document the required import method in Patterns as a directive: "always import via `@scope/package-name`. Never use relative paths across package boundaries."
4. **Detect code conventions** — these are mandatory Patterns sub-items when detectable:
   - **Module system:** Grep for `import`/`export` (ESM) vs `require`/`module.exports` (CJS). Check `"type"` in `package.json`, `tsconfig.json` module setting, or language-equivalent indicators. If mixed, state which to use for new code.
   - **Async pattern:** Grep for `async`/`await`, `.then(`, callback signatures. State the dominant pattern. If mixed, state which to use for new code.
   - **Naming conventions:** Sample 10-20 source file names for casing pattern (kebab-case, camelCase, PascalCase, snake_case). Check component/class/function naming from the same sample. Only document conventions that are consistent across >80% of samples.
5. Read up to 3 representative files that exhibit detected patterns to confirm and document specifics.

**Record only patterns with concrete evidence.** Typically 4-8 items (cap at 12). If a category shows two coexisting patterns (e.g., callbacks in older modules, async/await in newer), **state which one to use for new code** and label the other as legacy. Use directive framing: "use X for new code. Y exists in older modules -- do not convert unless requested." Do not merely describe both — agents need to know what to write. Cap at 2 per category; if >2, note the dominant one and add `<!-- REVIEW: mixed conventions in [category] -->`.

**Tool Preferences** are agent-platform-specific. Populate based on target agent (Claude Code: prefer Read/Edit/Glob/Grep over shell) and project mandates from CRITICAL. Check README/CONTRIBUTING.md for project-specific preferences.

## AGENTS.md Template

Generate this exact structure. Terse language, minimal prose. **Omit sections with no concrete data.** Strip template/placeholder HTML comments. **Preserve** these comment types in output: `<!-- agents-md-version: N -->`, `<!-- GAPS: ... -->`, `<!-- REVIEW: ... -->`, `<!-- REMOVED: ... -->`, `<!-- version: YYYY-MM-DD -->` (if user-added).

`agents-md-version` tracks the output schema — bump only when sections are added, removed, or restructured (not for content changes). Current schema: **1**. See `references/schema-changelog.md` for changelog.

**Handling older schema versions:** When an existing AGENTS.md has an older `agents-md-version`, apply Auto-detect/Curated/Hybrid update policy as normal. Add any new sections introduced in the current schema version. Remove sections deprecated between versions. Bump the version tag to current.

**Version tags:** Use `<!-- agents-md-version: 1 -->` as the mandatory schema version tag. A separate `<!-- version: YYYY-MM-DD -->` date tag may optionally be present (user-added, for tracking last regeneration) — preserve it if found but do not generate it.

**Line budget:** Under 150 lines for single-package repos, under 200 for monorepos, up to 250 for complex multi-stack monorepos. When over budget, apply triage order from Analysis Phase.

See `references/example-output.md` for a concrete Next.js + Prisma example.

````markdown
# AGENTS.md
<!-- agents-md-version: 1 -->

## CRITICAL

- MUST: [package manager command]
- MUST: [lint command] before commit
- MUST: [test command] before PR
- MUST: Use `[dependency command]` to change deps (DO NOT edit config manually)
- NEVER: [forbidden tool/pattern]
- NEVER: Force push (`git push --force`, `git push -f`) to shared branches
- NEVER: Skip pre-commit hooks (--no-verify)
- NEVER: Edit generated files in `[path]`
- PREFER: Built-in tools (file reader, editor, glob, grep) over shell equivalents (`cat`, `sed`, `find`, `grep`)
- ON FAIL: Read full error output before retry. Check Env for missing deps.
- ON FAIL (lint): If autofix available: run `[lint:fix command]`, then re-run `[lint command]`. Fix remaining errors manually.
- ON FAIL (test): Run single test file first: `[single test command]`
- ON FAIL (monorepo): Verify working directory with `pwd`

## Domain & Context

- Goal: [1 sentence project purpose]
- Type: [Library | Application | CLI/Tool | Both]
- License: [SPDX identifier]
- Key Terms:
  - `[Term]`: [Definition]
- Decisions: `[path to ADR/RFC dir]`

## Data & State

- Source of Truth: `[path to schema file]`
- Database: [engine]
- ORM/Driver: [name]
- Migrations: `[path]` (commands in Commands section)
- Seeding: `[path or reference to Commands]`
- API Schema: `[path]` ([OpenAPI | GraphQL | Protobuf])
- Codegen: `[command]` -> `[output path]` (generated -- do not edit)
- Broker: [type]

## Execution Context

- Run on: [Host | Docker | Devcontainer | Nix | Hybrid | Serverless]
- Prefix: [e.g., "docker compose exec app" or "N/A"]
- Deploys to: [target]
- Submodules: [paths]

## Monorepo

- Manager: [tool]
- Root: [commands that affect all packages]
- Scope: `[filter syntax]`
- Packages: [pattern]
- Deps: [root-level | package-level | both]

| Type | Path | Stack |
|------|------|-------|
| [category] | `[path]` | [runtime/tools] |

**Table compaction:** When multiple packages share the same type and stack, group them in a single row using brace expansion (e.g., `packages/{auth,billing,users}`). Use individual rows only where the stack differs meaningfully. Aim for under 12 rows. Every package must appear in the table — verify full coverage against the workspace listing.

## Commands

```bash
# install
[exact command]                # ON FAIL: [recovery step]
# test:unit
[exact command]                # ON FAIL: [recovery step]
# lint
[exact command]                # ON FAIL: [recovery step]
# [additional detected categories...]
[exact command]                # ON FAIL: [recovery step]
```

**ON FAIL comments:** Every command must include an inline `# ON FAIL: ...` comment with a concrete recovery step. Use the command's actual fix/retry mechanism (e.g., `# ON FAIL: rm -rf node_modules && pnpm install`). If no programmatic recovery exists, state the diagnostic step (e.g., `# ON FAIL: check output for type errors`). Omit ON FAIL only for commands where failure is self-explanatory (e.g., `dev` server start).

## Structure

```
[dir]/          # [2-4 word purpose]
[dir]/          # [2-4 word purpose] (generated -- do not edit)
```

## Patterns

- **Module:** [ESM | CJS | dual]
- **Async:** [async/await | callbacks | Promises | mixed (use X for new code)]
- **Naming:** [file-naming-convention] files, [ComponentCase] components, [functionCase] functions
- [Framework/architectural pattern]: [where it applies]

## Search

- Semantic: `[tool] [index] "[query]"` -- conceptual queries . Exact: `[grep tool] "[pattern]" [path]` -- regex . Files: `[glob pattern]`

## Testing Strategy

- Runner: [tool]
- Fixtures: `[path]` [and/or factory library]
- Separation: [method]
- Coverage: [threshold or "No threshold"]
- E2E: [tool]
- Conventions: [key conventions]

## Security

- NEVER read/write: [paths]
- NEVER log/commit: [patterns]
- Secrets via: [mechanism]
- CI secrets: [mechanism, e.g., "GitHub Actions secrets", "Vault"]
- Dep scanning: `[command]`

## Env

- [Runtime]: [version or version file]

```bash
# Required vars
[VAR]=[description]
# Env-specific config
[path or mechanism for dev/staging/prod differentiation]
# Local setup
[commands]
```

## Debugging

- Logs: [how to access application logs locally]
- REPL: `[command]`
- Debugger: [launch config or attach instructions]

## Git

- Branch: `[pattern]`
- Commit: `[format]`
- Hooks: [description]
- PR: [requirements]
- Reviews: [conventions, e.g., "DB migrations require DBA review"]
- PR template: `[path]`
- Code owners: `[path]`

## CI

- Runs: [jobs]
- Required checks: [list]
- Artifacts: [location]

## Tool Preferences

| Task | Prefer | Avoid |
|------|--------|-------|
| [task] | [preferred tool] | [avoided alternative] |
````

## When to Re-run

Re-generate when: package manager switched, test/lint framework changed, monorepo package added, major dependency added (ORM, framework, broker), CI restructured, or directory layout reorganized. Not for routine code changes or minor dependency updates.

## User Review

| Scenario | Show to user | Action |
|----------|-------------|--------|
| **New** | Summary: section name + 1-line synopsis each | Ask confirmation before writing. Show full draft on request. |
| **Update (full)** | Changed/added/removed sections as diff; list unchanged by name only | Ask confirmation. |
| **Update (targeted)** | Only the requested section(s) as diff | Ask confirmation. |
| **Rejection** | N/A | Ask which sections need changes, re-analyze only those, re-present. Skip full re-analysis unless requested. |
| **Unattended** | Nothing | Skip review; write directly. Only when user explicitly requests. |

Only write files after approval.

## Execution

After approval, write `AGENTS.md` and create or update `CLAUDE.md` in the same directory.

**CLAUDE.md merge strategy:**
- **No existing** -> create with `@AGENTS.md` import.
- **Already imports `@AGENTS.md`** -> preserve all content, update header comment.
- **Has content but no import** -> read existing content; scan for section headings that overlap with AGENTS.md (`## CRITICAL`, `## Commands`, etc.). If overlaps found, warn user with specific section names and ask whether to keep (as overrides), merge, or remove duplicates. Then prepend `@AGENTS.md` import. Always preserve additional `@` imports.

**CLAUDE.md content** — always includes the generated header `<!-- Generated by writing-agents-md. Custom edits (extra @imports, overrides) are preserved on re-run. -->` plus imports:

| Scenario | CLAUDE.md imports |
|----------|------------------|
| Standalone repo | `@AGENTS.md` |
| Monorepo subproject (ancestor has CLAUDE.md/AGENTS.md) | `@AGENTS.md` + `@<relative-path>/CLAUDE.md` (walk up to `.git` root to find ancestor; compute relative path) |
| Per-package split (root >250 lines, different stacks) | `@AGENTS.md` + `@<relative-path>/AGENTS.md` (both local and root) |

**Per-package split rules:** Root `AGENTS.md` holds shared sections (CRITICAL, Monorepo, Git, CI, Tool Preferences). Package `AGENTS.md` holds package-specific sections (Commands, Structure, Patterns, Testing, Env, Data & State). Package sections override root; CRITICAL is **additive** (contradictions: package wins, add `<!-- REVIEW: overrides root CRITICAL -->`). Only split when single-file fails line budget.

**Re-run scope:** From repo root -> root only (warn about stale per-package files; list packages that may need re-run). From package dir -> that package only. Never silently update files outside CWD.

**Partial failure:** If AGENTS.md is written but CLAUDE.md write fails, inform the user that AGENTS.md was written successfully and CLAUDE.md needs manual creation. Do not roll back AGENTS.md. If AGENTS.md write itself fails, do not proceed to CLAUDE.md.

### Other agent context files

On user request only, generate equivalent files: `.cursorrules`/`.windsurfrules` (inline content), `GEMINI.md`/`CODEX.md`/`.github/copilot-instructions.md` (copy content). All include sync header `<!-- source: AGENTS.md @ [git-short-sha] -->` (if not a git repo, use `<!-- source: AGENTS.md -->`). AGENTS.md is source of truth — regenerate derived files on update. No symlinks.

**Agent-specific adjustments:** When generating for non-Claude agents, adapt Tool Preferences to that agent's capabilities (e.g., Cursor uses terminal commands; Copilot uses inline suggestions). Replace Claude-specific tool names (Read/Edit/Glob/Grep) with generic equivalents or that agent's tool names.

## Validation

After writing, verify:

**Structural checks (1-10):**
1. **Commands exist** — grep each command's binary/script name in build config to confirm traceability
2. **Structure matches** — glob each listed directory to confirm it exists on disk
3. **No placeholders** — no `[value]` brackets remain
4. **No stale comments** — no HTML comments remain except: `<!-- agents-md-version: N -->`, `<!-- GAPS: ... -->`, `<!-- REVIEW: ... -->`, `<!-- REMOVED: ... -->`, and `<!-- version: YYYY-MM-DD -->`
5. **Line count** — within budget (150 / 200 / 250)
6. **CLAUDE.md valid** — `@` import paths resolve (glob target files)
7. **Generated dirs marked** — all codegen/build output dirs annotated in Structure
8. **CRITICAL completeness** — at least one MUST rule each for: package manager, linting, testing. Warn user if any missing
9. **Commands minimum set** — `install`, `lint`, and at least one `test` command exist. Warn if missing
10. **Constraint consistency** — every NEVER in CRITICAL traces to a detection in Step 1 (e.g., NEVER `pip` because `uv.lock` detected). Flag orphaned NEVERs with `<!-- REVIEW: no detection basis for NEVER [item] -->`

**Quality checks (11-15):**
11. **Specificity lint** — scan CRITICAL and Patterns for vague directives without adjacent concrete examples. Flag phrases like `follow conventions`, `use standard`, `as appropriate`, `see docs`, `when necessary`. Each directive must include either a command, path, or literal example. Add `<!-- REVIEW: add concrete example -->` to vague entries
12. **Failure recovery coverage** — every command in the Commands code block (except `dev`/server-start commands) has an `# ON FAIL:` comment. Missing recovery comments: add `<!-- REVIEW: add ON FAIL for [command] -->`
13. **Domain terms coverage** — if Domain & Context has a Key Terms list, verify each term appears in at least one other section (Structure, Patterns, Commands, or Data & State). Orphaned terms that appear nowhere else in the file: remove or add `<!-- REVIEW: term "[X]" unused in other sections -->`
14. **Conventions minimum** — if Patterns section exists and the project has source code, verify it includes Module, Async, and Naming sub-items (or a subset appropriate to the detected stack). Missing conventions for detected stacks: add `<!-- REVIEW: detect [convention type] for [stack] -->`
15. **No orphaned REVIEW comments** — verify every `<!-- REVIEW: ... -->` added during validation has a clear, actionable description. Remove any that were resolved during validation.

**On failure:** Fix and re-validate. If fix requires re-analysis, remove the invalid entry. Never write a file that fails validation — report unresolvable failures to the user.

## Quality Gate

Two-phase review after validation. Target: Quality Bar (score >= 4.5, no P1 findings).

### Phase 1: Self-critic review

Grade the generated AGENTS.md using [references/agents-md-rubric.md](references/agents-md-rubric.md). Read the file as if encountering the project for the first time.

**Check for:**
1. **Ambiguous CRITICAL rules** — any MUST/NEVER that an agent could reasonably misinterpret. Test: could two competent developers disagree on what this rule requires? If yes, make it more specific.
2. **Cross-section contradictions** — commands referenced in CRITICAL but absent from Commands; tools in Commands not mentioned in Env; paths in Structure not matching paths in other sections.
3. **Missing danger guards** — for each risky tool detected in Step 1 (database, IaC, deployment, package publishing), verify CRITICAL or Security contains a corresponding safeguard. Examples: DB detected but no migration safety rule; deploy tool detected but no "never deploy from local" rule; publish config detected but no "never publish without CI" rule.
4. **Unresolvable references** — terms used without definition, paths referencing external documentation without summarizing the relevant content, tool names without version or install context.

**Actions:**
- Fixable without re-analysis (wording clarification, adding a missing cross-reference, tightening a vague rule) -> fix inline.
- Requires re-analysis or user input -> add `<!-- REVIEW: [description] -->` and continue.
- If score < 4.5 or P1 findings remain, fix P1/P2 gaps and re-run Validation checks before proceeding.

### Phase 2: Fresh-context subagent review

Run a **fresh-context critic** pass using [references/review-prompt.md](references/review-prompt.md):
- If your environment supports subagents, **spawn a fresh-context subagent** with the review prompt. Otherwise, perform the review directly following the prompt instructions.
- Apply **P1 + P2** fixes (P3 last).
- Re-run Validation checks.
- Repeat up to **3 loops**, stop early when the Quality Bar is met.
- If 3 loops pass without meeting the bar: report remaining P1/P2 findings to the user with patch text and ask whether to apply fixes or accept as-is.

## Output Rules

1. **Minimal prose** — bullets/tables preferred; no placeholders (resolve or omit section); no examples (actual values only)
2. **Line budget** — omit lowest-priority sections first (see triage order); ASCII only (no emoji)
3. **Safety** — Safety / Constraints rules apply (no secrets, no web, no destructive commands)
5. **Idempotency** — identical output on unchanged project (no timestamps, random values); deterministic alphabetical ordering
6. **Tool priority** — use built-in file reader, glob, and grep tools as the PRIMARY method; Bash commands are FALLBACKS — use only when the agent lacks built-in equivalents
7. **Resilience** — skip unreadable configs (including permission-denied errors), empty globs, binary files, and sections with no concrete data — never fabricate values. If analysis is incomplete, add `<!-- GAPS: [list of skipped categories] -->` as the first line of AGENTS.md
