---
name: ca-visual
description: >
  Generate the interactive, business-first Code Atlas HTML viewer from the current
  run's Canonical Markdown. Use for searchable business maps, Scenario Process Flow,
  Business Object/Lifecycle views, progressive technical drill-down, cross-project
  Execution Chain visualization, evidence access, and code-to-business reverse navigation.
  Never invent or modify business facts.
---

# ca-visual

## Mission

Transform Canonical Markdown into an interactive Code Atlas for software engineers.

> Markdown is truth.

> HTML is a derived, searchable, interactive view.

Primary UX principle:

> 默认展示业务，按需展开技术；默认展示局部，按需扩大范围；任何页面都能从“业务 → 流程 → 对象/数据 → 代码”继续下钻，也能反向返回。

Use the detailed viewer rules in:

```text
references/html-viewer-guidelines.md
```

## Six viewer principles

Always preserve:

```text
Business First
Context Preserved
Progressive Disclosure
Bidirectional Navigation
Search First
Interactive but Calm
```

If a visual choice conflicts with these principles, prefer understandability over visual novelty.

## Inputs

Read only the current run's confirmed Canonical Markdown from:

```text
<analysis-workspace-root>/docs/code-atlas/**/*.md
```

For multi-project analysis, read the one shared Atlas.

Also read current run metadata when available:

- generation time;
- Git branch;
- Git commit;
- worktree status;
- overall analysis result.

Do not use previous HTML as a fact source.

## Never do

Do not:

- infer missing business knowledge;
- add State Transitions not in Markdown;
- change Process ordering;
- invent reverse relationships;
- repair broken references silently;
- merge/split semantic entities;
- perform Semantic Canonicalization;
- use stale HTML data from prior runs;
- create a second source of truth in JSON/HTML;
- make a giant all-system graph the default view;
- expose raw technical detail before business context unless the user explicitly enters a technical view.

Broken canonical data must be returned to `ca-knowledge` / `ca-audit`.

## Global layout

Prefer a stable desktop workspace:

```text
Navigator | Main Canvas | Context Panel
```

Use a persistent global search and clickable Breadcrumb.

The three areas answer:

```text
Navigator
→ where can I go?

Main Canvas
→ what is happening here?

Context Panel
→ what is related to the selected thing?
```

## Primary navigation

Prefer five top-level user concepts:

```text
Business Map
Flows
Business Objects
Technical Map
Data
```

Do not make every internal knowledge type a top-level menu item.

## Business Map

Home should answer:

> What business does this system implement?

Default hierarchy:

```text
Domain
→ Subdomain [optional]
→ Capability
```

Projects/modules are secondary context, not the primary home structure.

## Capability view

Show first:

- business meaning;
- Scenarios;
- Business Objects;
- important Business Rules;
- result/unresolved state.

Do not lead with Controllers/Services/RPCs.

## Scenario view

Treat Scenario as the primary flow page.

Show Canonical Business Process Flow prominently.

Selecting a Process must:

- preserve the whole Scenario flow;
- highlight current/upstream/downstream nodes;
- show detail in the Context Panel or lower detail area;
- keep unrelated nodes subdued.

Do not expand full Java call graphs in the default Scenario view.

## Process view

Provide three primary modes:

```text
Business
Data
Code
```

Default to:

```text
Business
```

### Business

Show:

- business goal;
- start/end boundary;
- input/output;
- Business Objects;
- Business Rules;
- Sub-process/Steps when useful.

### Data

Show:

- Business Objects/tables;
- important fields;
- reads/writes;
- lifecycle/state impact.

### Code

Show key implementation first:

```text
Entry
→ important Service
→ RPC/MQ/Job boundary
→ Repository/DB
```

Provide progressive expansion to the full Execution Chain.

## Business Object view

Keep the selected Business Object in the center.

Show only nearby:

- Capabilities;
- Scenarios/Processes;
- Lifecycle;
- related Business Objects;
- tables.

Use direct business wording on relation edges.

## Lifecycle view

Use an interactive state diagram.

Selecting a transition may show:

- Process;
- Business Rule;
- state write;
- Execution Chain;
- Evidence.

Generate only canonical states/transitions.

## Execution Chain view

For cross-project execution, prefer Project swimlanes.

Visually distinguish:

```text
sync call
async / MQ
callback
Job / retry / compensation
```

Keep Common Chains collapsible/linkable.

Default to key technical nodes; allow full-chain expansion.

## Focus / Spotlight

Default to local context.

When an entity is selected:

- highlight it;
- highlight direct relations;
- fade unrelated content;
- preserve parent business context.

Allow explicit expansion such as:

```text
current
→ 1-hop
→ 2-hop
→ all related
```

Do not render the complete graph by default.

## Global search

Search is mandatory.

Support business and technical terms:

- business name;
- canonical ID;
- alias/source name;
- Class;
- Method;
- Table;
- Field when available;
- RPC;
- MQ;
- Job.

Keep search visible in the global header.

Recommended shortcuts:

```text
Ctrl/Cmd + K
/
```

Group results by meaning rather than returning one flat list.

Example groups:

```text
Business
Flows
Objects
Code
Data
Integration
```

Search result navigation should preserve semantic context.

Example:

```text
WithdrawService.freeze()
```

should navigate to the related Process/Scenario and focus the Code view when the canonical relationships allow it.

## Reverse navigation

Derive reverse navigation such as:

```text
Method → Execution Chain → Process → Scenario → Capability
Table  → Business Object → Process → Scenario
Transition → Process → Execution Chain
RPC/MQ/Job → Execution Chain → Process
```

Provide a visible semantic action such as:

```text
Back to Business
```

Do not persist reverse links as new canonical facts.

## Evidence

Evidence must always be reachable but should not dominate the main canvas.

Prefer a side drawer/panel:

```text
View Evidence
```

Show:

- Project;
- file/symbol;
- SQL/table/config anchor;
- relevant source context;
- analysis result.

Do not clutter the business flow with source paths.

## Visual language

Aim for a modern developer intelligence console.

Prefer:

- dark workspace;
- restrained blue/cyan for business;
- green/teal for Business Object/Data;
- neutral/slate for technical nodes;
- amber for PARTIAL/UNRESOLVED;
- monospace for technical identifiers;
- standard UI font for business names;
- subtle glow/grid/transition effects.

Avoid:

- cyberpunk overload;
- large always-moving effects;
- 3D graph as default;
- one unique color per entity type;
- animations that reduce reading efficiency.

## Interaction

Useful interactions include:

- hover relationship highlight;
- upstream/downstream highlight;
- selected-node glow;
- unrelated-node fade;
- expand/collapse;
- search-result pulse;
- Focus/Spotlight mode;
- evidence drawer;
- keyboard escape to close focus/detail.

Interactions must explain information structure, not decorate it.

## Header metadata

Display:

```text
生成时间：...
代码分支：...
代码版本：...
代码状态：与当前 Git 提交一致
```

or:

```text
代码状态：包含本地未提交修改
```

Also show:

```text
分析结果：VERIFIED | PARTIAL | UNRESOLVED
```

Do not expose raw CLEAN/DIRTY wording or numeric confidence.

## Derived output

Prefer a static viewer that requires no backend.

Recommended:

```text
docs/code-atlas/html/
├── index.html
├── assets/
│   ├── app.js
│   └── app.css
└── data/
    ├── atlas.json
    └── search-index.json
```

A maintainable single-file HTML output is also allowed.

`atlas.json` and `search-index.json` are derived artifacts.

They must not become Canonical Knowledge.

## Desktop-first

Optimize primarily for developer desktop use.

Mobile may remain readable, but do not sacrifice desktop flow/graph usability for mobile-first layout.

## First-version priorities

Prioritize:

1. Business Map;
2. Scenario Process Flow;
3. Process Business/Data/Code modes;
4. Business Object + Lifecycle navigation;
5. Execution Chain Project swimlanes;
6. Global search + reverse navigation.

Do not prioritize decorative dashboards, 3D graphs, or advanced analytics.

## Full generation

Every run generates one coherent HTML snapshot from the current Canonical Markdown.

Avoid exposing mixed old/new pages while generation is incomplete.

When possible:

```text
generate to staging
→ validate
→ replace visible HTML atomically
```

## Quality gate

Before completion verify:

- every canonical Markdown file required by the view was parsed;
- references resolve;
- no visualization invented facts;
- Scenario flow matches canonical Process relations;
- Lifecycle diagram matches canonical transitions;
- Search finds both business and technical identifiers;
- Method/Table reverse navigation reaches business context when relations exist;
- Process drill-down preserves Scenario context;
- technical detail is collapsed by default;
- cross-project Execution Chain boundaries are visually clear;
- Evidence remains reachable without dominating the main flow;
- navigation has no broken canonical IDs;
- current run metadata is shown;
- generated viewer works without a required backend service.
