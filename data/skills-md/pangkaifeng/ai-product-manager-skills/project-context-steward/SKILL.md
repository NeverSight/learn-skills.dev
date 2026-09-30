---
name: project-context-steward
description: "Use when / 当用户进入一个新项目或跨仓库工作区，需要扫描产品、用户、业务工作流、技术架构、仓库边界、领域语言、阅读入口和历史踩坑，并生成或持续维护全局 PROJECT_CONTEXT.md。适合用户说“先完整看下项目并沉淀上下文”“给这个项目建上下文文档”“把这次踩坑更新到项目上下文”。不用于单个 PRD 起草、纯目录治理或一次性代码实现。"
---

# 项目上下文管家（project-context-steward）

## 中文速查

- 中文名：项目上下文管家 / 项目全局上下文维护
- 英文稳定名：`project-context-steward`
- 分类：项目治理
- 你可以这样叫我：`先完整看下项目并沉淀上下文`、`给这个项目建 PROJECT_CONTEXT.md`、`把这次踩坑更新到项目上下文`
- 适合：进入新项目、跨仓库项目、长期需求协作前，扫描全局并生成或维护可复用项目上下文
- 不适合：单个 PRD 起草、纯目录治理、一次性 bug 修复、只需要代码 review 的任务

## Overview

这个 Skill 用于把“新会话重新探索项目”的成本降下来。它帮助 Codex 先建立项目级事实、边界、入口路由和维护规则，再把长期有效的信息沉淀到 `PROJECT_CONTEXT.md` 或等价项目上下文文档。

核心原则：项目上下文文档不是某个需求的 PRD。它只记录跨需求复用的全局知识；阶段性判断、具体版本方案和待确认问题应进入 `prd/`、`research/`、`discussions/` 或 `decisions/`。

## Trigger Boundary

Use this Skill when the user asks to:

- onboard into a new repository or multi-repo workspace;
- generate a durable `PROJECT_CONTEXT.md`, `CONTEXT.md`, project map, or first-read document;
- update project context after a requirement, architecture change, or repeated pitfall;
- decide what belongs in global context versus PRD, ADR, research, handoff, runbook, or directory rules.

Do not use this Skill when:

- the user only wants a specific PRD: use `prd-architect`;
- the user only wants PRD critique: use `prd-review`;
- the user only asks where files should go: use `project-structure-governor`;
- the user asks to migrate a messy legacy directory: use `legacy-project-structure-migrator`;
- the user asks for a one-off implementation: inspect the relevant repo and implement normally.

## Workflow

### 0. Intake Required Context

Before scanning, capture the minimum inputs that change the result:

- target project root or workspace path;
- desired context document path, if the user already has one;
- whether the user wants create, refactor, or incremental maintenance;
- known sibling repositories that must not be confused;
- any user-stated product facts, decisions, or pitfalls from the current conversation.

If a required input is discoverable from the local workspace, discover it instead of asking. If a missing input changes where files will be written, ask a short clarification before editing.

### 1. Scope The Project

Identify the actual project boundary before writing anything.

- Is this a single repo, monorepo, parent folder with multiple checkouts, or product workspace spanning external repos?
- What is the user trying to preserve: product context, technical architecture, workflow knowledge, project-specific coding rules, or repeated pitfalls?
- Where should the context file live? Prefer the existing project docs root. If none exists, propose a stable location before writing.
- If the target contains multiple git repositories, treat each checkout independently and never assume the parent directory is the repo.

Ask at most three questions. Do not ask for information that can be discovered from local files.

### 2. Run A Fast Evidence Scan

Use `rg`, `find`, `git status`, README files, package manifests, app folders, docs roots, test directories, and existing project maps. If useful, run:

```bash
python3 <skill-dir>/scripts/scan_project_skeleton.py /path/to/project --max-depth 3 --format markdown
```

Read only enough to establish the global model. Do not deep-dive every file unless the project has no docs or the entry points are ambiguous.

### 3. Build The Project Model

Capture durable facts and route maps:

- product identity and current positioning;
- core users and recurring business workflows;
- top-level repo/module map;
- architecture and data flow;
- domain language and important entities;
- local dev, verification, and runtime entry points;
- ownership boundaries and things each layer must not do;
- first-read files for future AI sessions;
- pitfalls that caused wrong edits, wrong assumptions, or wasted exploration.

Separate `verified facts`, `current judgments`, and `open research points`. Do not present old memory or inference as current fact.

### 4. Choose The Right Documentation Destination

Use this routing:

- `PROJECT_CONTEXT.md` / `CONTEXT.md`: global project identity, module map, stable workflows, entry routes, terminology, permanent pitfalls.
- `prd/`: concrete product requirements, scope, states, acceptance criteria, version plans.
- `research/`: unresolved questions, competitor analysis, technical or product investigation.
- `decisions/`: ADR-style accepted decisions and their rationale.
- `runbook/` or repo docs: operational commands, deployment, local runtime, incident handling.
- `handoff/`: temporary work handoffs and current-task state.
- directory governance: invoke `project-structure-governor` if the main problem is where docs/code/assets should live.

### 5. Create Or Update The Context Document

When creating from scratch, start from `assets/PROJECT_CONTEXT.template.md`.

When updating an existing document:

- preserve stable project facts;
- remove or relocate requirement-specific content that belongs in PRD/research/discussions;
- add newly discovered durable facts;
- append reusable pitfalls;
- update first-read routes when paths, modules, or runtime entry points change;
- keep the document short enough to be read at the start of a new AI session.

### 6. Verify Before Completion

Before saying the context is ready:

- check referenced paths exist or mark them as unverified;
- search for stale requirement-specific wording masquerading as global context;
- verify the document answers the five entry questions: what product, who uses it, where to read next, how the main modules connect, what not to assume;
- if files were changed, show the changed paths and any verification commands run.

## Context Document Contract

Read `references/context-doc-model.md` before drafting or rewriting a major context document.

A good project context document should include:

1. purpose and maintenance rules;
2. current product positioning;
3. core users and recurring workflows;
4. architecture and repo map;
5. key data flows and domain language;
6. module ownership boundaries;
7. AI entry routes for future work;
8. topic index for PRDs, research, decisions, and handoffs;
9. repeated pitfalls;
10. verification and maintenance rules.

It should not include:

- full PRD text;
- one version's detailed solution;
- task-by-task implementation plans;
- temporary logs;
- unverified guesses;
- exact secrets, credentials, customer data, or private trace payloads.

## Maintenance Modes

### New Project Bootstrap

Use when there is no context doc yet. Output a first version plus a short list of unknowns.

### Context Refactor

Use when the existing context doc has the wrong granularity, mixes global facts with one requirement, or has stale paths. Preserve facts, relocate detail, and improve structure.

### Incremental Update

Use after a requirement or debugging session creates durable knowledge. Add only the stable part, usually to project map, entry route, terminology, or pitfalls.

### Pitfall Capture

Use when the agent or team made a wrong assumption. Write it as:

```text
Symptom -> cause -> durable prevention rule
```

## Output Format

For planning or no-write mode:

```markdown
**Project Context Plan**
- Target project/root:
- Existing context docs:
- Recommended context file:
- What belongs in global context:
- What should move to PRD/research/decisions:
- Evidence to read:
- Open questions:
- Proposed verification:
```

After editing:

```markdown
**Project Context Update**
- Updated files:
- Context scope:
- Durable facts added:
- Requirement-specific content relocated or removed:
- Pitfalls added:
- Verification:
- Remaining gaps:
```

## Resources

- `references/context-doc-model.md`: global context document model and best-practice synthesis.
- `references/discovery-checklist.md`: project scanning checklist.
- `references/maintenance-rules.md`: update rules and anti-bloat guidance.
- `assets/PROJECT_CONTEXT.template.md`: starting template for a new project context document.
- `scripts/scan_project_skeleton.py`: lightweight local scanner for repo/doc/runtime entry points.

## Definition of Done

The task is complete only when:

- the project scope and target context location are explicit;
- global context is separated from PRD, research, ADR, runbook, and handoff material;
- referenced paths are verified or clearly marked as unverified;
- durable facts, current judgments, and open questions are not mixed together;
- the document explains how future AI sessions should enter the project;
- repeated pitfalls and maintenance triggers are captured;
- changed files and verification results are reported.

## Evaluation

Smoke prompts:

- “先完整看下这个项目，生成一个 PROJECT_CONTEXT.md。”
- “这个上下文文档太像某个需求 PRD 了，帮我改成全局入口。”
- “我们刚踩了一个路径混淆的坑，把它更新到项目上下文。”

Non-trigger prompts:

- “帮我写这个功能的 PRD。”
- “这个 repo 的 docs 目录该怎么整理。”
- “直接修这个 bug。”

Regression checks:

- A desktop-specific or web-specific discussion must not become the global project positioning.
- Multi-checkout parent folders must not be described as one repository.
- A path listed in first-read routes must exist or be marked unverified.
