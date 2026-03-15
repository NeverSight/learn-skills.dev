---
name: living-docs
description: "Generate and maintain living documentation for microservices by analyzing current code state and Git history when needed. Trigger when users ask to document a service, update docs after changes, compare branches, generate changelogs, audit doc freshness, sync docs to central repo, migrate legacy docs, create flow docs, ADRs, or system overviews. Trigger phrases: 'document [service]', 'document-branch', 'document-commits', 'sync', 'audit', 'migrate-legacy', 'document-flow', 'create-adr', 'system-overview', 'documenta', 'qué cambió', 'actualizar docs', 'generar changelog', 'release notes', 'living docs'."
---

# Living Docs

Generate documentation driven by current code reality and verified changes. Every document traces to specific files and, when relevant, commits.

## Philosophy

Documentation must be:
- **Accurate**: derived from code and commits, not imagination
- **Navigable**: a human or agent can find what they need in 1-2 hops
- **Maintainable**: updating docs is a natural part of the development flow
- **Dual-audience**: useful for both humans reading markdown and agents consuming context
- **Co-located**: per-service docs live with the service code they describe

**Language policy**: Generate all documentation in English. Include Spanish translations in the `aliases` frontmatter field.

## Technology-Agnostic Principle

The skill must infer architecture from evidence, not from framework assumptions.

- Prefer capability discovery (`http`, `queue`, `event`, `cron`, `rpc`, `storage`) over framework labels
- Use framework/tooling hints only as secondary evidence, never as a hard dependency
- Normalize findings into a shared capability model before generating docs
- Apply confidence scoring and mark uncertainty when evidence is weak
- Keep command behavior stable across mixed or uncommon stacks

---

## Commands

| Command | Description | Scope |
|---------|-------------|-------|
| `document [service]` | Full MS documentation (state-driven, current codebase) | Per-service |
| `document-branch` | Document current branch changes vs base branch | Per-service |
| `document-commits [N]` | Document last N commits | Per-service |
| `cmd-list` | Show available living-docs commands and when to use each one | Meta |
| `sync` | Sync per-MS docs to vault (CTO structure) | Central |
| `migrate-legacy` | Detect and migrate pre-existing docs to standard format | Per-service |
| `audit` | Freshness audit of all per-MS docs | All services |
| `document-flow [name]` | Create/update cross-service flow documentation | Central |
| `create-adr` | Create Architecture Decision Record | Central |
| `system-overview` | Generate/update system-level overview | Central |

### Prompt Invocation (explicit)

Users can invoke commands with the `living-docs:<command>` format.

- `living-docs:cmd-list`
- `living-docs:document [service]`
- `living-docs:document-branch`
- `living-docs:document-commits [N]`
- `living-docs:sync`
- `living-docs:migrate-legacy`
- `living-docs:audit`
- `living-docs:document-flow [name]`
- `living-docs:create-adr`
- `living-docs:system-overview`

If the user uses this explicit format, route directly to the matching command workflow without extra intent interpretation.

---

## Activation Signals

Use this skill when the user intent matches documentation-from-current-code-state, documentation-from-code-changes, or any command above.

High-confidence trigger phrases (English/Spanish):
- "document this feature", "document X functionality", "document current branch"
- "document the diff", "what changed", "generate release notes", "generate changelog"
- "living-docs:cmd-list", "cmd-list", "show commands", "listar comandos"
- "update docs for react/integrator/magento", "document all microservices"
- "documenta esta funcionalidad", "documenta la branch actual", "analiza el diff y genera documentacion"
- "sync docs", "audit docs", "migrate legacy", "document flow", "create adr"

Intent-to-scope defaults:
- "living-docs:cmd-list" / "cmd-list" / "show commands" → run `bash <skill-path>/scripts/list-commands.sh`
- "document this feature/funcionalidad" → `document-branch` (current branch vs default branch)
- "document current branch/branch actual" → `document-branch`
- "release notes/changelog" → `document-commits 20` (default 20 unless user specifies)
- "what changed" → `document-branch` first; fall back to `document-commits` if branch base is unclear
- "sync/sincronizar" → `sync`
- "audit/revisar docs" → `audit`

Do not trigger this skill for generic writing requests not tied to code analysis or git changes. `document [service]` is state-driven and does not require git history.

---

## Source of Truth Model

This is the most important concept. Understand it before doing anything.

```
ms-root/                              # Non-git parent directory (e.g., /home/user/tripulse/microservices)
├── react/                            # Git repo
│   ├── src/
│   └── docs/
│       ├── index.md                  ← NAVIGATION INDEX (auto-generated links)
│       ├── components/               ← Component docs
│       ├── changelogs/               ← Changelogs
│       ├── adrs/                     ← Per-service ADRs
│       ├── guides/                   ← User guides
│       ├── technical/                ← Technical deep-dives
│       ├── bugs/                     ← Bug reports
│       ├── runbooks/                 ← Runbooks
│       ├── plans/                    ← Plans
│       └── tasks/                    ← Task docs
├── integrator/                       # Git repo
│   └── docs/
│       └── ...                       (same structure)
├── sap/                              # Git repo
│   └── docs/
│       └── ...
└── vault/               # Git repo — Obsidian Vault structure
    ├── CLAUDE.MD.md                  ← Agent rules and vault config
    ├── Global_Architecture_Map.md    ← ENTRY POINT for navigation
    ├── engineering/
    │   ├── adrs/                     ← Architecture Decision Records (transversal)
    │   ├── microservices/            ← Per-service architecture docs
    │   │   ├── react/
    │   │   ├── integrator/
    │   │   └── ...
    │   ├── guides/                   ← SOPs, runbooks, guides
    │   ├── diagnostics/              ← Troubleshooting runbooks
    │   ├── database/                 ← Schema docs
    │   ├── infrastructure/           ← Infra specs per service
    │   ├── frontend/                 ← Frontend docs
    │   └── onboarding/               ← Dev setup guides
    ├── reference/
    │   ├── react/                    ← Per-repo component/technical docs
    │   ├── integrator/
    │   └── ...                       ← Tech reference cards (Ref_*.md)
    ├── reports/
    │   ├── changelogs/               ← Changelogs
    │   └── ...                       ← Bug reports, incident reports
    └── strategy/
        ├── data-flows/               ← Cross-service flow docs
        └── ...                       ← Plans, registries
```

### Source of Truth Rules

1. **Per-MS docs** (`{ms-root}/{service}/docs/`) are the authoritative source. This is where living-docs generates and updates documentation.
2. **vault/** follows the Obsidian Vault structure. Never invent new top-level folders. The `sync` command copies per-MS docs to the correct Vault paths.
3. **Transversal docs** (system overview, flows, ADRs, architecture map) live ONLY in vault. They don't belong to any single service.
4. **Never edit vault directly** for per-service content — generate in the service repo first, then sync.
5. **Sacred Documents**: Docs authored by [[Erick Blangino]] or [[Jorge Cruz]] are preserved verbatim. Append new sections — never edit their original content.

---

## The 4-Layer Documentation System

Read `references/documentation-layers.md` for full details. Summary:

| Layer | What | Source of Truth | Updated by |
|---|---|---|---|
| 1. System Overview | Architecture, service map, glossary | `vault/engineering/` | `system-overview` command (rare) |
| 2. Flows | End-to-end business flows across services | `vault/strategy/data-flows/` | `document-flow` command |
| 3. Per-MS Docs | Endpoints, modules, internal decisions | `{service}/docs/` | `document` / `document-branch` commands |
| 4. ADRs | Architecture decisions with context | `vault/engineering/adrs/` | `create-adr` command |

---

## Folder Structure per Microservice

```
{service}/docs/
├── index.md              # Navigation index linking all docs (auto-generated)
├── components/           # Component Docs + service overview
│   ├── {repo}_comp_overview.md
│   └── {repo}_comp_{name}.md
├── changelogs/           # Changelogs by date
│   └── {repo}_cl_{YYYY-MM-DD}.md
├── adrs/                 # Per-service Architecture Decision Records
│   └── {repo}_adr_{NNN}_{slug}.md
├── guides/               # User Guides
│   └── {repo}_guide_{topic}.md
├── technical/            # Technical deep-dives
│   └── {repo}_tech_{topic}.md
├── bugs/                 # Bug Reports
│   └── {repo}_bug_{issue}.md
├── runbooks/             # Operational Runbooks
│   └── {repo}_rb_{operation}.md
├── plans/                # Plans and roadmaps
│   └── {repo}_plan_{initiative}.md
└── tasks/                # Task documentation
    └── {repo}_task_{name}.md
```

### File Naming Convention

**Pattern**: `${REPO}_${TYPE_CODE}_${SLUG}.md`

Always use the prefix, even inside the service repo. This ensures files are identifiable when synced to vault.

| Doc Type | Folder | Type Code | Example |
|----------|--------|-----------|---------|
| Service Overview | `components/` | comp | `react_comp_overview.md` |
| Component Doc | `components/` | comp | `react_comp_auth.md` |
| Changelog | `changelogs/` | cl | `react_cl_2026-03-01.md` |
| ADR | `adrs/` | adr | `react_adr_001_oauth.md` |
| Runbook | `runbooks/` | rb | `react_rb_deploy.md` |
| Guide | `guides/` | guide | `react_guide_oauth_setup.md` |
| Technical | `technical/` | tech | `react_tech_state_mgmt.md` |
| Bug Report | `bugs/` | bug | `react_bug_auth_timeout.md` |
| Plan | `plans/` | plan | `react_plan_q2_migration.md` |
| Task Doc | `tasks/` | task | `react_task_deps_update.md` |

### Navigation Index (index.md)

After generating or updating docs, update `docs/index.md` with links to all docs. Use the `templates/navigation-index.md` template. Example:

```markdown
# Documentation Index — react

> Auto-generated. Last updated: 2026-03-01

## Components & Features
- [[react_comp_overview]] — Service overview
- [[react_comp_auth]] — Authentication service

## Recent Changelogs
- [[react_cl_2026-03-01]] — Feature release

## Architecture Decisions
- [[react_adr_001_oauth]] — OAuth provider selection

## Guides
- [[react_guide_oauth_setup]] — OAuth setup guide

## Legacy Docs (not yet migrated)
- [React.md](./React.md) — Original service documentation
```

---

## Workspace Detection (mandatory)

Run `git status` before selecting a repo path.

- If `git status` succeeds: continue in current git repository
- If `git status` returns `fatal: not a git repository`:
  - Treat current location as microservices root
  - Ask: "Which microservice(s) should I document: react, integrator, sap, magento, or all?"
  - Accept answers like `react`, `integrator`, `magento`, `todos`/`all`, or comma-separated combinations
  - Resolve `all` to all available microservice repos with a `.git` directory

For each selected microservice, set `REPO_PATH=<workspace-root>/<microservice>` and process independently.

### Ambiguity Protocol

If scope, branch, or repository is ambiguous, ask a focused question before generating docs.

- Prefer an interactive question tool when available (single-select or multi-select options)
- Ask one targeted question at a time, with a recommended default
- Continue with safe defaults only when ambiguity does not change the output materially

---

## Command Instructions

### CMD 1: `document [service]` (State-Scan Mode)

**Trigger**: User asks to document a microservice, or wants to regenerate docs.
**Philosophy**: This command documents the **current state** of the codebase, not the commit history. Git is used only for optional metadata, not as the primary analysis source.

**Steps**:

1. **Identify the repo**:
   ```bash
   REPO_NAME=$(bash <skill-path>/scripts/get-repo-name.sh <repo-path>)
   ```
   If no existing docs → full generation. If docs exist → incremental state comparison.

2. **State Scan (Primary Analysis, Technology-Agnostic)**:
   Instead of git diffs, analyze the codebase at HEAD using capability discovery and evidence scoring.

   Build a language-agnostic inventory:
   ```bash
   # Source tree candidate roots (do not assume a framework)
   find <repo-path> -maxdepth 3 -type d \( -name src -o -name app -o -name internal -o -name api -o -name services -o -name handlers -o -name routes \)

   # Project manifests (detect ecosystem, not framework)
   ls <repo-path>/{package.json,requirements.txt,pyproject.toml,go.mod,pom.xml,build.gradle,Cargo.toml,composer.json,Gemfile} 2>/dev/null
   ```

   Discover integration surfaces by semantic signals (no framework branching):
   ```bash
   # HTTP/API candidates: method + path-like signal in same file
   grep -RniE "(get|post|put|patch|delete|request|route|endpoint|handler|controller)" <repo-path> --include="*.{js,jsx,ts,tsx,py,go,java,kt,rb,php,rs,cs}" | head -200
   grep -RniE "(/[a-zA-Z0-9_./:-]+|\{[a-zA-Z_][a-zA-Z0-9_]*\}|:[a-zA-Z_][a-zA-Z0-9_]*)" <repo-path> --include="*.{js,jsx,ts,tsx,py,go,java,kt,rb,php,rs,cs}" | head -200

   # Async/event surfaces
   grep -RniE "(queue|topic|publish|subscribe|consumer|producer|listener|webhook|event|kafka|rabbit|sqs|pubsub|nats)" <repo-path> --include="*.{js,jsx,ts,tsx,py,go,java,kt,rb,php,rs,cs}" | head -200

   # Scheduled/background work
   grep -RniE "(cron|schedule|scheduler|timer|job|worker|celery|bull|agenda)" <repo-path> --include="*.{js,jsx,ts,tsx,py,go,java,kt,rb,php,rs,cs}" | head -120

   # Config and runtime parameters
   grep -RniE "(env|config|settings|secret|token|key|url|timeout|retry)" <repo-path> --include="*.{js,jsx,ts,tsx,py,go,java,kt,rb,php,rs,cs,yml,yaml,json,toml,ini,env}" | head -200
   ```

   Normalize findings into a capability model:
   - `kind`: `http` | `queue` | `event` | `cron` | `rpc` | `storage`
   - `operation`: verb/action (e.g., `GET`, `consume`, `publish`, `run`)
   - `path_or_topic`: route, queue/topic, job identifier, or API contract id
   - `handler_symbol`: function/class/module entry point if available
   - `source_file`: file path + line reference
   - `confidence`: `high` | `medium` | `low`
   - `evidence`: matched tokens/patterns used to infer behavior

   Apply confidence scoring before asserting facts:
   - `+3` explicit external interface signal (route/topic/job id)
   - `+2` executable handler symbol resolved in code
   - `+1` corroborated by tests/config/wiring
   - Score `>=6` = high, `4-5` = medium, `<4` = low

   Focus on: entry points, external interfaces, internal modules, config, schemas/contracts, and runtime wiring.

3. **Optional Git Metadata** (not required for generation):
   ```bash
   # Only for frontmatter tracking - not for analysis
   CURRENT_SHA=$(git -C <repo-path> rev-parse HEAD)
   LAST_UPDATED=$(date +%Y-%m-%d)
   ```
   - Read `last_verified_sha` from existing docs (if any) to detect if state changed
   - Do NOT use commit range to determine what to document

4. **Compare vs Existing Docs** (Incremental Mode):
   If docs exist, compare current state against documented state:
   - List current capabilities (`http`, `queue`, `cron`, `event`, etc.) → check if documented
   - List current handlers/modules → check if documented
   - List current helpers/utilities (`*helper*`, `*util*`, shared functions) → check if documented
   - List current schemas/interfaces/contracts/types → check if documented
   - List explicit business rules/validations/branching logic → check if documented
   - List current config/runtime parameters → check if documented
   - Flag anything in docs that no longer exists in code (stale)

5. **Classify State Elements**:
   | Capability / Element | Doc Type |
   |----------------------|----------|
   | External interface (HTTP/RPC/GraphQL) | Component Doc |
   | Async interface (queue/topic/event/webhook) | Component Doc |
   | Internal module/service boundary | Component Doc |
   | Helper/utility function with business impact | Technical Doc or Component subsection |
   | Schema/interface/type/DTO/contract | Component Doc (Contract section) |
   | Business rule (pricing, eligibility, state transitions, validations) | Component Doc (Business Rules section) |
   | Config/runtime parameters | Technical Doc |
   | Data schema/contract | Component Doc (+ ADR if architectural impact) |
   | New major dependency/integration | Guide or Technical Doc |
   | Existing capability changed | Update matching doc |

6. **Select and fill templates**: Read templates from `templates/` directory. See `references/frontmatter-schema.md` for frontmatter rules.

   Frontmatter rules:
   - Include required fields: `aliases`, `type`, `layer`, `status`, `owner`, `tech_stack`, `last_updated`
   - Use `last_verified_sha` (optional, from git) instead of `source_branch` and `commit_range`
   - Include `audience` tag per CTO's distribution model
   - Use `[[wiki-links]]` for owner, tech_stack, and cross-references
   - Set `last_updated` to today's date
   - Set `status` honestly: `active`, `debt`, `zombie`, or `gap`
   - Populate `aliases` with English keywords + Spanish equivalents
   - **Omit template sections that don't apply**
   - When analysis detects issues/bugs/inconsistencies, include the optional `Risks & Inconsistencies` section using `templates/section-risk-observations.md`

7. **Generate docs**: Write docs to the folder structure. For incremental updates, use the merge strategy:

   | Section | Strategy |
   |---------|----------|
   | Frontmatter | **Merge**: Update `last_updated`, `last_verified_sha`, `status`. Preserve `owner`, `aliases` (append new ones) |
   | What It Does | **Replace** with current description from code analysis |
   | API/Interface Surface | **Replace** with current capability map (scan from code) |
   | Dependencies | **Replace** with current dependency manifests |
   | Configuration | **Replace** with current runtime parameters (scan from code) |
   | Key Files | **Replace** with current file structure |
   | Recent Changes | **Omit** - this belongs to `document-branch` |

   Minimum depth requirements for generated docs (`document [service]`):
   - Include low-level sections when evidence exists: `Helpers & Utilities`, `Schemas & Interfaces`, `Business Rules`.
   - Include `Risks & Inconsistencies` when evidence shows a possible bug, mismatch, fragile assumption, unclear behavior, or security/operational risk.
   - Document helpers with: purpose, inputs/outputs, side effects, call sites.
   - Document schemas/interfaces with: fields, constraints, optional/required semantics, compatibility notes.
   - Document business rules with: trigger conditions, decision branches, validation rules, failure behavior.
   - Document each risk with: severity, finding, code evidence, impact, recommended action, and owner (if known).

   Mini templates:
   - `templates/section-business-rules.md`
   - `templates/section-helpers-utilities.md`
   - `templates/section-risk-observations.md`
   Use these templates when generating low-level sections for component/technical docs.

   Visual + code evidence requirements:
   - Include at least one Mermaid diagram per component doc when there are 3+ meaningful steps (flowchart or sequence).
   - Include at least one code snippet per major section (`API/Interface`, `Business Rules`, `Helpers`) when available.
   - Snippets must be short (10-40 lines), copied from real code, and include file references.
   - Never fabricate snippets; if code cannot be safely excerpted, provide precise file:line references instead.

8. **Verify output**: Before presenting to the user:
   - [ ] Every interface/capability mentioned in docs has code evidence in the current codebase
   - [ ] Helper functions, schemas/interfaces, and business rules are documented when present
   - [ ] Mermaid diagram(s) included where flow complexity >= 3 steps
   - [ ] Snippets are real excerpts and linked to file references
   - [ ] All frontmatter required fields are populated
   - [ ] File paths referenced in "Key Files" actually exist
   - [ ] Detected risks/inconsistencies are documented with severity + evidence, or explicitly marked as not reproducible
   - [ ] No stale content from previous docs remains
   - [ ] No duplicate docs (check existing files before creating new ones)

9. **Update index.md**: Regenerate `docs/index.md` with links to all docs.

10. **Present summary**:
    ```
    ## Documentation Generated

    | File | Type | Scope |
    |------|------|-------|
    | docs/components/react_comp_auth.md | Component Doc | Current state - 5 endpoints |
    | docs/technical/react_tech_config.md | Technical Doc | Current state - 12 env vars |

    ### State Captured
    - Services: auth, users, payments
    - Endpoints: 15 total
    - Dependencies: 23 packages

    ### Incremental Changes
    - Added: 2 new endpoints (POST /auth/refresh, GET /users/profile)
    - Updated: 3 env vars (OAUTH_CALLBACK_URL, etc.)
    - Removed: 1 deprecated endpoint (GET /auth/logout)
    ```

**Rules**:
- NEVER invent interfaces, configuration parameters, or behaviors not found in current code
- If something is unclear, document it as "⚠️ Unclear: [what you found] — needs human verification"
- If risk severity is `high` or `critical`, also create/update a bug report in `docs/bugs/{repo}_bug_{slug}.md` and cross-link it from the parent doc
- Every claim must be grounded in current code analysis
- Never create docs outside a git repo or in the workspace root
- **Recent Changes section is NOT generated here** - use `document-branch` for change tracking
- If confidence is medium/low, include explicit evidence and mark uncertainty

---

### CMD 2: `document-branch`

**Trigger**: User wants to document current branch changes, or says "document this feature".

**Steps**:

1. **Identify branches**:
   ```bash
   cd <repo-path>
   CURRENT=$(git branch --show-current)
   BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
   # Fallback: try Develop, main, master
   ```

2. **Extract diff**:
   ```bash
   bash <skill-path>/scripts/extract-diff.sh <repo-path> --branch $BASE
   ```

3. **Classify changes**: Run `detect-changes.sh` and apply classification from `references/analysis-patterns.md`, then map results into the same technology-agnostic capability model used by CMD 1.

4. **Generate docs**: Reuse CMD 1 steps 5-9 with one addition: include a "Recent Changes" section sourced from the branch diff/commits.
   - If the diff reveals potential regressions/inconsistencies, add `Risks & Inconsistencies` entries with severity/evidence and cross-link bug reports for high/critical items.

5. **Check for flow impact** (critical step):
   If vault exists, read frontmatter of all docs in `strategy/data-flows/`. If any flow lists this service in its `services:` array, flag it:
   ```
   ⚠️ FLOW IMPACT DETECTED:
   - strategy/data-flows/order-b2b-flow.md references this service
   - Changes in: [endpoints, business-logic]
   - Recommendation: review flow doc for accuracy
   ```
   Do NOT auto-update flow docs. Only flag.

6. **Present summary**: Same format as CMD 1.

---

### CMD 3: `document-commits [N]`

**Trigger**: User wants to document the last N commits, or says "release notes", "changelog".

**Steps**: Same as CMD 2 (including capability-model mapping), but use `--commits N` instead of `--branch`:
```bash
bash <skill-path>/scripts/extract-diff.sh <repo-path> --commits <N>
```

Default N = 20 unless user specifies otherwise.

---

### CMD 4: `sync`

**Trigger**: User says "sync", "sync docs", "sincronizar docs".

**Steps**:

1. **Run sync**:
   ```bash
   bash <skill-path>/scripts/sync-to-central.sh \
     --repos-dir <ms-root> \
     --docs-repo <ms-root>/vault
   ```

2. **Review the output**: The script shows what was copied, updated, or skipped.

3. **Mapping rules** (see `references/central-mapping.md` for full table):
   ```
   Per-MS docs/              → vault/
   docs/components/*.md      → reference/{repo}/
   docs/changelogs/*.md      → reports/changelogs/
   docs/adrs/*.md            → engineering/adrs/
   docs/runbooks/*.md        → engineering/guides/
   docs/guides/*.md          → engineering/guides/
   docs/technical/*.md       → reference/{repo}/
   docs/bugs/*.md            → reports/
   docs/plans/*.md           → strategy/
   docs/tasks/*.md           → engineering/microservices/{repo}/
   ```

4. **Remind the user**: The script does NOT auto-commit. The user must review and commit.

**Rules**:
- Never overwrite docs authored by [[Erick Blangino]] or [[Jorge Cruz]] — flag conflicts instead
- Check `audience` frontmatter tag before syncing (only sync docs with `audience: [microservices]` or multi-audience)
- Never auto-commit or auto-push

---

### CMD 5: `migrate-legacy`

**Trigger**: User says "migrate legacy", "migrate docs", "migrar docs legacy".

**Steps**:

1. **Scan for legacy docs**: Look for `.md` files in `docs/` that:
   - Have no YAML frontmatter (no `---` block at top)
   - Don't follow the naming convention `${REPO}_${TYPE}_${SLUG}.md`
   - Are not in a subdirectory (e.g., `docs/React.md`, `docs/SAP.md`)

2. **For each legacy doc**:
   - Read its content to determine type (component, guide, technical, etc.)
   - Propose: new filename, target subdirectory, frontmatter to add
   - Show preview of the migration (diff)

3. **Ask for confirmation** before applying each migration.

4. **After migration**: Update `index.md` to replace legacy links with standard links.

**Rules**:
- Never auto-migrate without showing the user what will change
- Preserve all original content — only add frontmatter and rename
- If the content doesn't map cleanly to a doc type, ask the user

---

### CMD 6: `audit`

**Trigger**: User says "audit", "audit docs", "check freshness", "revisar docs".

**Steps**:

1. **Run freshness check**:
   ```bash
   bash <skill-path>/scripts/check-freshness.sh --repos-dir <ms-root>
   ```

2. **Generate freshness report**:
   ```markdown
   ## Doc Freshness Report — 2026-03-01

   | Service | Doc SHA | Current HEAD | Commits Behind | Status |
   |---|---|---|---|---|
   | integrator | abc123 | def456 | 12 | ⚠️ STALE |
   | sap | xyz789 | xyz789 | 0 | ✅ Current |
   | magento | — | fed321 | ∞ | ❌ No docs |
   ```

3. **For stale docs**, offer to run `document [service]` (incremental update).

4. **For undocumented services**, offer to run `document [service]` (full generation).

5. **Check flow docs**: For each flow doc in `vault/strategy/data-flows/`, verify all referenced services have current docs. Flag any flows that reference stale services.

---

### CMD 7: `document-flow [name]`

**Trigger**: User wants to document a business flow that spans multiple services.

**Steps**:

1. **Identify the flow**: Ask the user to describe the flow if not clear.

2. **Identify involved services**: From user input or by tracing code:
   - Check queue consumers/producers across services
   - Check HTTP calls between services
   - Check shared Redis keys or database references

3. **Read existing docs** for each involved service from their source of truth (`{service}/docs/`).

4. **Trace the flow in code**: Actually read the code paths. Don't rely solely on docs.
   - Start from the entry point (webhook, cron, queue message)
   - Follow the chain: which service calls which
   - Document data transformations at each boundary
   - Document error handling at each step

5. **Generate flow doc** using `templates/flow.md`:
   - Include mermaid sequence diagram (mandatory for 3+ steps)
   - Reference specific files/functions in each service
   - Document retry behavior and dead letter queues

6. **Save to vault**:
   ```
   vault/strategy/data-flows/{flow-name}.md
   ```
   With frontmatter including `services: [list]` array for impact detection.

**Rules**:
- Every step must reference actual code (file:line or function name)
- If you can't trace a step in code, mark it: "⚠️ Could not verify in code"
- Flows are the highest-value docs. Take extra care.

---

### CMD 8: `create-adr`

**Trigger**: User wants to record a technical decision, or a significant architectural change is detected.

**Steps**:

1. **Gather context**: Ask or extract:
   - What was decided?
   - Why? (what problem does it solve?)
   - What alternatives were considered?
   - What are the consequences/trade-offs?

2. **Number it**: Read existing ADRs in `vault/engineering/adrs/`, take the next number.

3. **Generate ADR** using `templates/adr.md`.

4. **Save** to `vault/engineering/adrs/{NNN}-{slug}.md`.

**Rules**:
- ADRs are immutable once merged. If a decision is reversed, create a new ADR that supersedes the old one.
- Keep the "Consequences" section honest — include downsides.
- Use CTO frontmatter schema with `audience: [microservices]`.

---

### CMD 9: `system-overview`

**Trigger**: User wants to create or update the top-level system documentation.

**Steps**:

1. **Scan all service repos**:
   ```bash
   for dir in <ms-root>/*/; do
     if [ -d "$dir/.git" ]; then echo "$(basename $dir)"; fi
   done
   ```

2. **Read existing per-MS docs** from each service repo (`{service}/docs/`).

3. **If no per-MS docs exist** for a service, do a lightweight scan:
   - Read any project manifest found (npm/pip/go/maven/gradle/cargo/composer/ruby)
   - Read service entry points and interface wiring files
   - Read Docker/K8s/runtime config for infrastructure context

4. **Generate** using `templates/system-overview.md`:
   - Service inventory (name, purpose, tech stack, integrations)
   - Architecture diagram (mermaid)
   - Communication patterns
   - Domain glossary

5. **Save** to `vault/engineering/` (coordinate with existing `Global_Architecture_Map.md`).

---

## Global Rules

### Accuracy Rules
1. **Every factual claim must be grounded in code or commits.** No hallucination. Read the actual code.
2. **If uncertain, flag with ⚠️.** Always better to say "unclear" than to guess.
3. **Include provenance.** Every doc section should be traceable to specific files or commits.

### Quality Rules
- **No fluff**: Every sentence carries information. Cut filler.
- **Trace to code**: Every claim references a file, commit, or config.
- **Tables over prose**: For endpoints, env vars, dependencies — always tables.
- **Document depth**: Capture not only interfaces but also helpers, contracts, and business rules when they influence behavior.
- **Risk visibility**: When code analysis finds possible bugs/issues/inconsistencies, record them in `Risks & Inconsistencies` with severity + evidence; escalate high/critical findings to a bug report doc.
- **Be honest**: If current state or diff reveals tech debt, set `status: debt`. Living docs tell the truth.
- **Aliases matter**: Include concept name, Spanish translation, common abbreviations.
- **Omit empty sections**: Don't include template sections that have no content for this component.

### Safety Rules
1. **NEVER delete existing documentation** without explicit user confirmation
2. **NEVER auto-commit or auto-push** — always generate locally and let the user review
3. **NEVER include secrets, tokens, or credentials** even if found in code — flag them as security issues instead
4. **Preserve manual edits**: If a doc section has been manually edited, flag it and ask before overwriting
5. **Sacred Documents**: Never overwrite content authored by [[Erick Blangino]] or [[Jorge Cruz]]. Append, don't replace.

### Formatting Rules
1. **All docs use frontmatter** (see `references/frontmatter-schema.md`)
2. **Status values**: `active` | `debt` | `zombie` | `gap` (per-MS docs). `draft` | `verified` | `needs-review` | `stale` (for doc lifecycle).
3. **Language**: Generate docs in English. Include Spanish translations in `aliases` field.
4. **Mermaid diagrams**: Required for any flow with 3+ steps or any architecture with 3+ components. For `document [service]`, include at least one Mermaid diagram per major component doc when flow/logic complexity meets this threshold.
5. **Code references**: Use format `service-name/path/to/file.ext:functionName` or `service-name/path/to/file.ext:L42`.
6. **Code snippets**: Include fenced snippets for key interfaces/rules/helpers (10-40 lines each), grounded in real code and accompanied by file references.
7. **Audience tag**: Always include `audience` field per CTO's distribution model.

### Per-Microservice Execution Rules (mandatory)

For every selected microservice repository:

1. Validate repo: `git -C <repo-path> rev-parse --is-inside-work-tree`
2. Write docs only inside that repo: `<repo-path>/docs/`
3. Never create docs outside a git repo
4. Never create shared docs in workspace root
5. Update `<repo-path>/docs/index.md` for that repo

If multiple microservices are selected, repeat the full workflow per repo and present a grouped summary.

---

## Large Diff Strategy

When the diff is large (100+ files changed or output exceeds ~50KB):

1. **Start with `--stat` only** — Use the file list and change counts to plan
2. **Read full diff only for high-impact files** — APIs, schemas, configs, contracts, new files
3. **Read only changed hunks for medium-impact files** — Business logic, services
4. **Skip full diff for low-impact files** — Tests, formatting, comments
5. **Split by directory** — If still too large, analyze one component/service at a time

```bash
# Start with stat only
bash <skill-path>/scripts/extract-diff-repo.sh <repo-path> --branch feature/X --stat
```

---

## Few-Shot Example

### Input: Diff Summary

```
=== REPO: react ===
=== BRANCH: feature/oauth vs Develop ===
=== COMMIT RANGE: a1b2c3d..d4e5f6g ===

=== FILE STATS ===
 src/routes/auth.ts   | 45 +++++++++--
 src/services/oauth.ts | 120 ++++++++++++++++++++++++++++
 src/types/auth.dto.ts |  15 ++++
 package.json          |   2 +  (added passport-google-oauth20)
 tests/oauth.test.ts   |  85 ++++++++++++++++++++

=== COMMIT LOG ===
a1b2c3d feat: add Google OAuth2 login flow
d4e5f6g feat: add OAuth callback handler
h7i8j9k fix: handle missing email in OAuth profile
l0m1n2o chore: add passport-google-oauth20 dependency
```

### Output: Classification

1. **New OAuth service** (oauth.ts, 120 lines) → High impact → Component Doc
2. **Route changes** (auth.ts, 45 lines) → Public API change → Component Doc + Changelog
3. **New major dependency** (passport-google-oauth20) → Technical Guide
4. **New tests with different expectations** → Confirms business logic change

### Output: Generated Docs

- `docs/components/react_comp_auth.md` — Updated: added OAuth endpoints
- `docs/changelogs/react_cl_2026-03-01.md` — New: 2 features, 1 fix
- `docs/guides/react_guide_oauth_google.md` — New: Google OAuth integration guide
- `docs/technical/react_tech_oauth_architecture.md` — New: OAuth flow deep-dive

---

## Resources

- `scripts/extract-diff.sh` — Extract structured diff data (file stats, commit log, full diff)
- `scripts/extract-diff-repo.sh` — Extract diff with automatic repository name detection
- `scripts/list-commands.sh` — Show all `living-docs:<command>` prompts with when-to-use guidance
- `scripts/get-repo-name.sh` — Get the current git repository name
- `scripts/detect-changes.sh` — Categorize changes by type with priority levels
- `scripts/check-freshness.sh` — Compare doc timestamps vs last code change
- `scripts/sync-to-central.sh` — Sync per-MS docs to vault (CTO structure)
- `references/analysis-patterns.md` — How to classify changes from diffs
- `references/documentation-layers.md` — The 4-layer documentation system
- `references/frontmatter-schema.md` — Frontmatter schema and validation rules
- `references/central-mapping.md` — Mapping from per-MS paths to vault paths
- `references/ci-integration.md` — GitHub Actions workflow examples
- `templates/section-business-rules.md` — Reusable section template for business rule documentation
- `templates/section-helpers-utilities.md` — Reusable section template for helper/utility documentation
- `templates/section-risk-observations.md` — Reusable section template for documenting issues, bugs, and inconsistencies
- `templates/` — All document templates
