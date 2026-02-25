---
name: dd
description: "Document-Driven Development (文档驱动开发). Use when: (1) /dd help — explain workflow and suggest next step based on project state, (2) /dd init — initialize doc-driven structure in a project, (3) /dd spec [requirement] — create temporary spec to align intent before development, (4) /dd dev [spec-path|doc-path] — implement code following spec or doc (auto enters plan mode for spec-based dev), (5) /dd sync [--check|--scope] — update living docs, archive spec, and audit consistency. Triggers on mentions of: document-driven, design document, doc-driven, spec-driven, 文档驱动, 设计文档, 规格, /dd."
---

# Document-Driven Development (DD)

A workflow that maintains **two kinds of documents** with distinct roles:

- **Spec（规格）**: Temporary, task-bound. Guides AI implementation with precise acceptance criteria. Created before development, archived after.
- **Doc（文档）**: Permanent, module-bound. Describes system as-is — architecture, rationale, business logic. The living knowledge base for both AI and human architects.

The lifecycle forms a closed loop:

```
Doc(理解现状) → Spec(定义变更) → Dev(plan + 实现) → Sync(更新文档 + 一致性检查) → Doc'(新的现状)
                                       ↑ small changes skip here
```

## Command Routing

Parse the first argument after `/dd`:

| Argument | Phase | Action |
|----------|-------|--------|
| `help` | [Help](#help) | Explain workflow, detect project state, suggest next step |
| `init` | [Init](#init) | Set up doc-driven structure |
| `spec <requirement>` | [Spec](#spec) | Create temporary spec for intent alignment |
| `dev [spec-path\|doc-path]` | [Dev](#dev) | Implement code from spec (with plan mode) or doc |
| `sync [options]` | [Sync](#sync) | Update living docs, archive spec, audit consistency |
| _(none)_ | Same as `help` | — |

### Task Sizing — Choosing the Right Ceremony

Not every change needs the full workflow. Choose based on the nature of the change:

| Change Type | Workflow | Example |
|-------------|----------|---------|
| New feature / behavioral change | `spec → dev → sync` | Add refund functionality |
| Multi-module design change | `spec → dev → sync` | Redesign auth flow |
| Small feature addition | `dev → sync` | Add a filter parameter to existing API |
| Bug fix | `dev → sync` | Fix off-by-one error |
| Refactor (no behavior change) | `dev → sync` | Extract function, rename module |
| Config / dependency / typo | Just code | Change env var, fix typo |

**Rule of thumb**: If the change introduces **new data models, new interfaces, new states, or new business rules** → write a spec. If not → go directly to dev, but still read related module docs first and sync afterwards.

---

<a id="help"></a>
## help

Explain document-driven development and guide the user to the right next step.

### Workflow

1. **Detect project state** by checking:
   - Does `docs/` exist? → If not, recommend `init`
   - Does `docs/.vitepress/config.mts` exist? → If not, recommend `init`
   - Are there module docs in `docs/modules/`? → If empty, recommend creating docs for existing code
   - Are there active specs in `docs/specs/`? → If yes, recommend `dev`
   - Are there uncommitted code changes? → Recommend `sync`
   - Are module docs stale (last-updated far behind recent commits)? → Recommend `sync`

2. **Output a status summary**:

```
## DD Status

Project: [project name]
Docs structure: [initialized / not initialized]
Module docs: [N modules documented, M modules undocumented]
Active specs: [N active, N completed]

## Suggested Next Step

→ /dd [recommended command] — [reason]
```

3. **If user seems unfamiliar**, explain the core concepts:

```
Document-Driven Development 维护两种文档：

  Spec（规格）— 临时的，开发前写，指导 AI 按意图实现
  Doc（文档） — 持久的，按模块组织，描述系统现状和设计理由

完整工作流（显著变更）：

  /dd spec    写规格，对齐开发意图（开发前）
       ↓
  /dd dev     基于规格进入 plan mode，规划后逐步实现
       ↓
  /dd sync    更新模块文档，归档规格，检查一致性（开发后）

轻量工作流（小改动）：

  /dd dev     直接开发（先读模块文档）
       ↓
  /dd sync    更新模块文档

定期健康检查：

  /dd sync --check    只检查不修改，输出一致性报告
```

---

<a id="init"></a>
## init

Set up documentation structure and configure project for document-driven development.

### Directory Structure

1. Check if `docs/` exists at project root
2. **If not (greenfield)**, create core structure:
   ```
   docs/
   ├── .vitepress/config.mts
   ├── index.md
   ├── modules/           # Living docs — permanent, per-module, code-aligned
   │   └── index.md
   ├── specs/             # Specs — temporary, per-task
   │   └── index.md
   └── adr/               # Architecture Decision Records
       ├── index.md
       └── 000-template.md
   ```
   Optionally ask user if they need additional directories (e.g., `product/`, `business/`, `guide/`) for non-code-aligned documentation.

3. **If exists (brownfield)**, analyze current structure and migrate non-destructively:
   - **Scan all existing directories** under `docs/` — never delete or ignore them
   - If `docs/design/` exists (legacy DD structure):
     - Explain: design docs should be reviewed and content migrated to `modules/` (as living docs) or `specs/` (as active specs)
     - Do NOT auto-delete `design/` — keep it until user confirms migration is complete
   - If `product/`, `business/`, `guide/` or other directories exist — **preserve them**. These are non-code-aligned docs that serve different audiences and are complementary to `modules/`.
   - Add only missing DD-required directories: `modules/`, `specs/`, `adr/`

4. Generate or **update** VitePress `config.mts`:
   - **Include ALL existing directories** in nav and sidebar — not just DD directories
   - DD directories get standard labels: Modules, Specs, ADR
   - Existing directories keep their current labels (or derive from directory name)
   - Mermaid plugin for diagrams
   - If `config.mts` already exists, **merge** new entries into existing config rather than overwriting

5. Write ADR template — see [references/templates.md](references/templates.md) § ADR Template

### CLAUDE.md Integration

Append (or create) a `## Document-Driven Development` section in the project's `CLAUDE.md`:

```markdown
## Document-Driven Development

本项目使用文档驱动开发，维护两种文档：

### Spec（规格）
- 临时性文档，位于 `docs/specs/`，在开发前创建，开发后归档
- 定义做什么、不做什么、验收标准，指导 AI 按意图实现
- 命令: `/dd spec <需求>` 创建

### Doc（模块文档）
- 持久性文档，位于 `docs/modules/`，描述系统现状和设计理由
- 修改任何代码前，先查找并阅读关联的模块文档
- 代码与文档冲突时，确认后更新文档或修正代码

### 工作流
- `/dd help` — 查看项目文档状态和下一步建议
- `/dd spec <需求>` — 创建规格（显著变更时）
- `/dd dev` — 按规格或文档实现代码（基于 spec 时自动进入 plan mode）
- `/dd sync` — 开发后更新模块文档、归档规格、检查一致性
- `/dd sync --check` — 只检查不修改，输出健康报告
```

If `CLAUDE.md` already has a DD section, update it to match the above.

### Confirm

Show user a summary of all changes made, then confirm.

---

<a id="spec"></a>
## spec

Create a temporary spec to align intent before development. This is the **contract between human intent and AI implementation**.

A spec answers: **What should the AI build, and what should it NOT build?**

A spec does NOT explain why (that's the doc's job after development).

### Self-Spec Mode

The agent autonomously drafts the spec, then presents it to the user for review. The agent does the heavy lifting, the human validates intent.

**Agent responsibilities**: Analyze requirements, read existing module docs for context, draft complete spec.
**Human responsibilities**: Verify the spec captures their actual intent, correct misunderstandings, provide context the agent lacks.

### Workflow

1. **Understand requirement** — If unclear, ask. Never assume.
2. **Read project context**:
   - `CLAUDE.md` / `AGENTS.md` for project conventions
   - Existing module docs in `docs/modules/` (understand current system state)
   - Related specs in `docs/specs/` (avoid conflicts)
   - Relevant existing code
3. **Plan scope** — Which spec(s) to create. Confirm with user if scope is ambiguous.
4. **Generate spec** using template from [references/templates.md](references/templates.md) § Spec Template
   - Save to `docs/specs/<name>.md` with `status: active`
5. **Self-check** against [references/quality.md](references/quality.md) § Spec Quality
6. **Update VitePress index** — Add to sidebar in `config.mts` + update `docs/specs/index.md`
7. **Present to user** — Highlight key design decisions that need confirmation

### Spec Writing Rules

| Rule | Bad | Good |
|------|-----|------|
| No vague words | "should", "might", "usually" | "must", "when X then Y" |
| No rationale in spec | "We chose PostgreSQL because..." | Constraint: `must use PostgreSQL` |
| Explicit exclusions | (silence) | OUT: OAuth login, phone registration |
| Verifiable acceptance criteria | "works correctly" | `AC-001: POST /api/x returns 201 with {id, status}` |
| Typed interfaces | "accepts user info" | `function create(input: CreateUserInput): User` |
| Numbered business rules | prose paragraph | `BR-001: WHEN [condition] THEN [action]` |
| Error handling table | "handle errors" | Error code table with trigger + response |
| State machines over prose | "status changes over time" | Mermaid stateDiagram + transition table |

### Document Meta Block

Every spec MUST begin with a meta comment after frontmatter:

```markdown
<!-- DD-SPEC
Temporary implementation spec for [feature].
- Agent: implement strictly from this spec. Do not add unspecified features.
- This spec will be archived after development. Decision rationale will be captured in module docs during sync.
-->
```

---

<a id="dev"></a>
## dev

Implement code following a spec or module doc.

### Spec-Based Dev: Auto Plan Mode

When dev is based on a spec, **always enter plan mode first** before writing any code. This leverages the AI agent's native planning capability — no separate plan document needed.

The plan mode should:
1. Read the spec thoroughly
2. Read target module docs for current system context
3. Decompose the spec into implementation steps, mapping spec sections to code tasks
4. Present the plan for user confirmation
5. Then implement step by step, verifying each step against spec acceptance criteria

This is more effective than a static plan document because the agent can adapt the plan as implementation progresses.

### Mandatory Doc Binding

Before modifying ANY code, locate its related documentation:

1. Check `// ref: docs/modules/xxx.md` or `// ref: docs/specs/xxx.md` comments in the code
2. Match code module/directory name against module docs in `docs/modules/`
3. Check `docs/specs/` for active specs whose `target-modules` reference the module

**If a related doc is found → read it in full before writing any code.**
This rule applies whether invoked via `/dd dev` or any other coding task.

### Workflow

1. **Load context**:
   - If spec path given → read the spec, then **enter plan mode** (see above)
   - If doc path given → read the module doc, implement within its documented architecture
   - If neither → use Doc Binding above to find related docs
   - **If working on a significant change with no spec → STOP. Suggest `/dd spec` first.**
2. **Read related module docs** — Understand current system state
3. **Implement** following the Iron Rules below
4. **Post-implementation divergence check** — see below

### Iron Rules During Implementation

| Situation | Required Action |
|-----------|----------------|
| Spec doesn't cover a scenario | **STOP.** Report gap to user. Do not decide independently. |
| Spec is ambiguous | **STOP.** Ask user to clarify. Do not assume. |
| Found a better approach than spec | **Propose spec update first.** Only change code after spec is updated. |
| Feature not in spec | **Never add it.** |
| Contradicts module doc | **Flag it.** The spec takes precedence during dev, but divergence must be resolved at sync. |

At key business logic points, add doc references in code:
```
// ref: docs/specs/xxx.md BR-001
// ref: docs/modules/yyy.md#业务逻辑
```

### Post-Implementation Divergence Check

After implementation, compare what was actually written against the spec:

1. For each interface/function implemented, compare signature with spec definition
2. For each data model touched, compare fields with spec table
3. For each business rule (BR-NNN), confirm code logic matches the WHEN/THEN

**If divergence is found**:
- List each divergence with code location and spec reference
- Ask user: **update the spec** to match reality, or **fix the code** to match spec?
- Do not silently proceed — every divergence must be explicitly resolved

---

<a id="sync"></a>
## sync

The single command for keeping docs healthy. Combines **doc updates** (after development) with **consistency auditing** (detecting drift and rot).

### Modes

| Invocation | Mode | What it does |
|------------|------|-------------|
| `/dd sync` | **Update** | Update module docs for recent changes, archive specs, run consistency checks |
| `/dd sync --check` | **Audit only** | Full project health check — report issues without modifying any files |
| `/dd sync --scope=commit` | **Scoped update** | Only process modules affected by current git diff |
| `/dd sync <module-doc-path>` | **Targeted update** | Sync a specific module doc |

### When to Sync

- **After `/dd dev`** — always. This is the natural next step after any code change.
- **Periodically** — run `/dd sync --check` to catch drift before it accumulates.

### Update Workflow (default mode)

1. **Identify what changed**:
   - If spec exists → read spec + code diff to understand changes
   - If no spec → read code diff + git log to understand changes
2. **Read existing module doc** in `docs/modules/`
   - If no module doc exists for the changed code → create one using [references/templates.md](references/templates.md) § Module Doc Template
3. **Generate doc update** — This is the core transformation:

   **From spec, extract and inject into doc**:
   - Decision rationale (WHY this approach was chosen, what alternatives were considered)
   - Constraints that are now permanent system properties
   - New business rules (convert from BR-NNN format to narrative with context)

   **From code, update in doc**:
   - Current data model state (what fields actually exist now)
   - Current interface signatures (what the API actually looks like now)
   - Current state machine (what states and transitions actually exist)
   - Architecture changes (new modules, changed relationships)

   **Preserve in doc**:
   - Historical rationale that still applies
   - Architecture context that hasn't changed
   - Known limitations and future plans (update if relevant)

4. **Run consistency checks** (see below) on affected modules
5. **Present results to user**:
   - Doc update diff (proposed changes)
   - Consistency report (any issues found)
   - User reviews and confirms before writing
6. **Archive spec** (if one was used):
   - Change spec frontmatter `status: active` → `status: completed`
   - Add `completed: YYYY-MM-DD` to frontmatter
   - Move to `docs/specs/archive/` (or delete, per user preference)
7. **Update VitePress index** — Sidebar, parent index.md
8. **Update `last-updated` in module doc frontmatter**

### Consistency Checks

These checks run automatically during update mode, or standalone in `--check` mode:

**1. Code-Doc Consistency** (Critical)
- Data model fields in code match module doc tables
- Function/API signatures match module doc interfaces
- Business logic matches documented business rules
- Error handling covers all documented error scenarios
- State transitions match documented state machines

**2. Unimplemented Content Detection** (Critical)
- Doc contains data model / interface / business rule definitions that have **no corresponding code**
- This means the doc has "future state" content that should be a spec, not a doc
- Action: offer to **extract** unimplemented sections into `docs/specs/` as a new active spec, and remove them from the module doc
- Exception: the `已知限制` section may briefly mention planned features (e.g., "手机号注册暂未实现"), but must NOT contain implementation details (no data models, no interface definitions, no BR-NNN rules for unbuilt features)

**3. Doc-Doc Consistency** (Critical)
- Scan all module docs for shared entities (same table, interface, enum, field)
- When the same entity appears in multiple docs, compare definitions
- Flag conflicting definitions
- Recommend: consolidate into one doc and use cross-references elsewhere

**4. Spec Hygiene** (Warning)
- Active specs with no recent development activity (stale specs)
- Completed code with specs still marked `active` (forgot to sync)
- Specs whose target modules have no corresponding module doc

**5. Doc Rot Detection** (Warning)
- Code modules with no corresponding module doc
- Module doc descriptions for deleted/changed code
- Broken cross-reference links between docs
- `last-updated` significantly older than recent code commits

**6. Information Duplication** (Warning)
- Same data model defined in full in multiple module docs
- Same business rule described in multiple docs
- Recommend: define once, cross-reference elsewhere

**7. Doc Quality** (Info)
- Missing rationale for design decisions
- Missing architecture context or module relationships
- Module docs without TL;DR block
- Vague words in specs (should/might/usually)

Full quality criteria: [references/quality.md](references/quality.md)

### Report Format

Both update mode and `--check` mode output a consistency report:

```markdown
## DD Sync Report

### Doc Updates
- [x] `docs/modules/payment.md` — updated data model, added refund business rules
- [x] `docs/specs/refund.md` — archived (status: completed)

### Critical — Code-Doc Inconsistency
- [ ] `src/xxx.ts:42` vs `docs/modules/xxx.md#接口定义`
      Code: `function foo(a: string): void`
      Doc:  `function foo(a: string, b: number): Result`

### Critical — Unimplemented Content in Doc
- [ ] `docs/modules/auth.md#数据模型` defines table `phone_verifications` — no corresponding code found
      → Extract to `docs/specs/phone-auth.md` or remove from doc
- [ ] `docs/modules/payment.md#接口定义` defines `refundBatch()` — not implemented
      → Extract to spec or remove

### Critical — Doc-Doc Conflict
- [ ] Entity `UserStatus` defined differently:
      `docs/modules/auth.md#数据模型`: enum('active','inactive')
      `docs/modules/membership.md#数据模型`: enum('active','suspended','closed')

### Warning — Spec Hygiene
- [ ] `docs/specs/refund.md` status is `active` but all code appears implemented

### Warning — Doc Rot
- [ ] `docs/modules/payment.md` last-updated 2025-10-01, but `src/payment/` has 12 commits since
- [ ] `docs/modules/auth.md#数据模型` field `legacy_token` not found in code

### Warning — Duplication
- [ ] Table `users` fully defined in both `docs/modules/auth.md` and `docs/modules/profile.md`
      → Keep in `auth.md`, replace in `profile.md` with cross-reference

### Info — Quality
- [ ] `docs/modules/payment.md` missing rationale for choosing Stripe over PayPal

### Stats
- Module docs checked: N | Specs checked: N | Code files checked: N
- Updated: N | Critical: N | Warning: N | Info: N
```

In `--check` mode, the "Doc Updates" section is replaced with "Proposed Updates" showing what **would** be changed.

### Doc Writing Rules (Different from Spec!)

Docs are for **understanding what IS**, not for **planning what WILL BE**. Write accordingly:

| Rule | How |
|------|-----|
| **Current state only** | Every data model, interface, and business rule in a doc must exist in code. No "future" implementation details — those are specs. |
| Explain the WHY | Every design choice should have rationale: "使用 PostgreSQL 而非 MongoDB，因为需要强一致性的事务支持" |
| Describe current state | "注册模块目前支持邮箱注册，手机号注册因国际化短信成本暂缓（参见 ADR-003）" |
| Show module relationships | Mermaid diagrams showing how this module connects to others |
| Include known limitations | Brief notes only: "当前不支持批量导入" — no implementation details for unbuilt features |
| Keep it scannable | TL;DR first, diagrams over prose, tables for data models |
| Size limit | Single module doc ≤ **200 lines**. Split into sub-docs if longer. |

---

## VitePress Index Maintenance

After ANY doc change under `docs/`, always:

1. Read `docs/.vitepress/config.mts`
2. Add new docs to sidebar items
3. Add new directories to sidebar groups + top nav
4. Update parent `index.md` with links to new docs
5. Verify all sidebar references point to existing files

---

## References

- **[references/templates.md](references/templates.md)** — Spec template, module doc template, ADR template, frontmatter schemas.
- **[references/quality.md](references/quality.md)** — Quality checklists for specs and docs. Read during self-check and review.
