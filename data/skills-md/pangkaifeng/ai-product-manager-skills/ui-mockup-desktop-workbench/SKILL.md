---
name: ui-mockup-desktop-workbench
description: >
  PRD 到高保真 UI 交付对齐 / 桌面工作台 UI mockup：当用户已有 PRD、UI 规范、真实前端项目路径、截图或页面状态清单，
  需要先从 PRD 提炼 UI 结构、状态模型和 ASCII 布局，再进入高保真 mockup、项目原生 preview 或开发交付 handoff 时使用。
  优先输出项目原生 preview route/component；只有早期概念确认或无法接入真实项目时才输出 standalone HTML。
  必须包含结构阶段产物、screen contract、component map、implementation notes、截图/验证结果和 HTML/preview 的迁移边界。
---

# ui-mockup-desktop-workbench

## 中文速查

- 中文名：高保真 UI 交付对齐器 / 桌面工作台 UI Mockup 生成器
- 英文稳定名：`ui-mockup-desktop-workbench`
- 分类：产品与 PRD
- 你可以这样叫我：`基于 PRD 和 UI 规范出高保真 mockup`、`先从 PRD 出 UI 结构和 ASCII 布局再做高保真`、`生成桌面工作台真实页面`、`把这个 Agent Client PRD 做成可交付开发的 UI`、`让前端按这个 UI 复刻`
- 适合：把 PRD、UI 规范、真实项目组件、参考截图和状态清单转成先结构、后视觉、再交付实现的 UI contract、mockup 或项目原生 preview。
- 不适合：问题还没定义清楚；只需要 PRD 文案；只做移动端或营销页；不需要视觉/状态确认而是直接写生产功能。

## Overview

Use this Skill when the goal is not just a pretty standalone page, but a staged UI handoff that product, design, and engineering can inspect and implement from.

The default output is a **UI implementation contract**, not disposable HTML. The contract starts with UI structure and states, then moves to visual fidelity only after the screen model is coherent. Standalone HTML is allowed only as one output mode. When the user provides a real frontend project path and wants development to reproduce the design, prefer a project-native preview route/component using the real app's components, tokens, icons, and layout conventions.

The workflow combines:

1. `structure-only` discipline: structure and state before polish.
2. Desktop Agent workbench patterns: navigation, task list, execution canvas, artifact/workspace panel, settings, and result surfaces.
3. User-provided UI specifications: tokens, layout rules, component style, copy tone, and interaction constraints override generic design instincts.
4. Project-native design discovery: real routes, components, styles, tokens, icons, screenshots, and nearby states must be inspected before claiming production alignment.
5. Frontend design quality: dense but readable desktop UI, realistic data, stable dimensions, no decorative one-note visual filler.

## Structure-only Mode

`structure-only` is the lightweight mode for users who only want UI structure, state model, ASCII layout, or a quick low-fidelity HTML wireframe. It is part of this Skill, so there is only one UI trigger surface.

This Skill owns the full chain:

`PRD -> screen inventory -> state model -> ASCII layout -> structure review gate -> high-fidelity visual handoff or project-native preview -> implementation handoff`

If the user asks for high fidelity, real project alignment, visual handoff, frontend replication, or component mapping, stay in this Skill and include the structure stage internally.

If the user explicitly wants only low-fidelity structure and does not need visual polish or implementation mapping, select `structure-only` and stop after the structure review gate.

## Output Modes

Choose one mode before implementing visuals. State the chosen mode and why.

For detailed selection rules, read `references/output-mode-selection.md`.

| Mode | Use When | Primary Outputs | Do Not Use When |
| --- | --- | --- | --- |
| `project-native-preview` | The user provides a real frontend project path or asks development to "replicate" the UI. | `ascii-layout.md`, preview route/component in the project, `screen-contract.md`, `component-map.md`, `implementation-notes.md`, screenshots. | The user only wants early concept exploration or forbids repo edits. |
| `visual-handoff` | The PRD is stable and development needs exact visual guidance, but direct project integration is risky or not requested. | `ascii-layout.md`, high-fidelity HTML/React artifact, screenshots, component map, implementation notes, migration boundary. | The user expects production-ready code. |
| `concept-html` | Early product/design discussion needs a quick visual reference after structure is checked. | `ascii-layout.md`, standalone `mockup.html`, screen contract, assumptions. | The user wants frontend to implement it accurately; then use `visual-handoff` or `project-native-preview`. |

Default to `project-native-preview` when all are true:

- A real frontend project path is provided or discoverable.
- The user says the UI should match the production app, online version, existing components, or screenshots.
- The mockup is intended to guide implementation.

Default to `visual-handoff` when the real project exists but editing it would exceed the requested scope.

Use `concept-html` only when the goal is fast concept confirmation, not production implementation alignment.

## PRD Boundary

This Skill is downstream of PRD maturity:

- If the user still needs to define the product goal, scope, workflow, states, or acceptance criteria, hand off to `prd-architect`.
- If a PRD exists but has conflicts, missing acceptance criteria, unclear states, or untestable flows, hand off to `prd-review` before producing the formal mockup.
- If the PRD and UI spec are clear enough, use this Skill to create the desktop mockup artifact.
- If the mockup process exposes PRD gaps, stop and record a PRD feedback note instead of silently inventing requirements.

`prd-architect` may include lightweight UI references, screenshots, or mockup notes inside a PRD. Formal multi-state desktop HTML mockups belong here.

If the UI is meant to drive implementation, update the PRD or prepare a PRD UI appendix after the final visual decision. The PRD should link the final mockup/preview, screenshots, and screen contract.

## Context Intake

Before generating UI, collect or discover:

- PRD path or pasted PRD content.
- UI specification path or pasted style rules.
- Real frontend project path, app name, route, or package when available.
- Target page set: workbench, task list, execution session, artifact page, settings page, empty state, error state, or all of them.
- Runtime/product context: desktop app, browser shell, Electron/Tauri/native wrapper, logged-in assumptions, target viewport.
- Existing app conventions, component library, screenshots, or competitor references if provided.
- Output destination and expected format: standalone HTML, React route, static artifact folder, screenshot, or design handoff markdown.

Minimum input maturity:

- product goal and target user are known
- page or screen set is known
- primary workflow and key states are known
- non-goals or out-of-scope states are known
- acceptance or review criteria are known enough to judge the mockup

If these are missing, route back to `prd-architect` or `prd-review` depending on whether the PRD must be created or reviewed.

Ask at most three questions only when missing information changes the page set, design constraints, or output format. If the user supplied PRD and UI spec paths, read them and proceed with explicit assumptions.

## Design Discovery Gate

Before any visual implementation, inspect project-local design evidence when available. Do not ask the user for information that can be read from the repo.

Read or inspect:

- Real page entrypoints, route files, shell/layout components, and adjacent page states.
- Global styles, theme tokens, CSS variables, design token files, icon system, and UI library usage.
- Existing navigation, sidebar, modal, menu, avatar/settings, button, input, tab, toast/error, artifact/result, and empty-state components.
- Local screenshots, Storybook, design docs, or current running app screenshots when available.
- Existing copy tone, density, spacing, radius, shadows, status colors, and light/dark mode defaults.

Before generating UI, output 5-8 bullets under `Discovered UI Constraints`:

- concrete component/style evidence found
- what must be reused
- what can be newly created
- where assumptions start

If the project cannot be started or inspected fully, say so and mark the mockup as static inference. Never claim "matches production" without project evidence.

## Wireframe Stage And Review Gate

Always model structure before visual fidelity. This is the reusable core of `structure-only` mode.

Create or include:

- `screen-inventory`: pages, modals, popovers, panels, and major regions.
- `state-model`: empty, draft, loading, queued, running, stopped, success, partial failure, error, permission, and settings states relevant to the PRD.
- `ascii-layout.md` or an equivalent section: desktop layout zones, fixed/flexible widths, scroll containers, primary actions, and state-specific changes.
- `wireframe-handoff.md` or an equivalent review note: confirmed structure, assumptions, open questions, and the gate before high fidelity.
- `interaction-notes`: user actions, agent actions, state transitions, and recovery paths.
- `prd-traceability`: the PRD section, UI spec rule, screenshot, or assumption that justifies each screen/state.

Run a structure review gate before high fidelity:

- If the user asked for exploration, stop after the wireframe stage and ask for confirmation before visual implementation.
- If the user already asked for high-fidelity implementation handoff, continue after documenting unresolved structure assumptions.
- If the wireframe reveals missing PRD states, conflicting IA, or untestable flows, record a PRD feedback note and route to `prd-review` or `prd-architect` before polishing.
- Do not use visual polish to hide unresolved navigation, state, or artifact ownership questions.

## Workflow

1. **Read authoritative inputs**
   - Read the PRD before designing screens.
   - Read the UI specification before choosing colors, typography, spacing, density, or component styling.
   - Read the real frontend project when provided; project-local design language outranks generic mockup style.
   - If both conflict, preserve product requirements from the PRD and visual constraints from the UI spec; call out unresolved conflicts.
   - If conflicts block screen/state decisions, create a PRD feedback note and recommend `prd-review`.

2. **Choose output mode**
   - Select `project-native-preview`, `visual-handoff`, or `concept-html`.
   - Explain the selection in one paragraph.
   - If the user wants implementation alignment and a project path exists, do not default to standalone HTML.

3. **Run the Design Discovery Gate**
   - Inspect the real app's route, components, styles, tokens, and screenshots when available.
   - Write `Discovered UI Constraints` before implementing.
   - If the project cannot be inspected, document the limitation and lower confidence.

4. **Run the Wireframe Stage**
   - Extract the screen inventory from the PRD and target workflow.
   - Draft the state model before drawing final visuals.
   - Produce `ascii-layout.md` or an equivalent layout section before styling.
   - Identify scroll containers, fixed rails, flexible work areas, primary actions, and state-specific region changes.

5. **Pass the structure review gate**
   - If structure is exploratory, stop and ask for confirmation.
   - If the user already requested final handoff, proceed while clearly marking unresolved assumptions.
   - If structure gaps block implementation, produce PRD feedback instead of high-fidelity output.

6. **Extract a screen contract**
   - Identify primary user roles, core jobs, navigation model, data objects, and page hierarchy.
   - List required screens and states, including empty, loading, streaming/running, success, partial failure, error, permission/login, and recovery.
   - Map each screen to PRD sections and UI spec constraints.

7. **Create a component map**
   - Map every visible UI region to a production component, style source, or explicit "new component needed" entry.
   - Include related file paths, reuse/new/modify status, states, and implementation notes.
   - Do not treat standalone HTML class names as production component names.

8. **Refine structure before visual styling**
   - Use the confirmed ASCII layout as the visual skeleton.
   - For Agent workbenches, default to a four-zone shell when suitable:
     - left navigation and account/workspace switcher
     - task/session list or recent work rail
     - central execution/conversation/work canvas
     - right artifact, resource, preview, inspector, or settings panel
   - Do not invent large marketing heroes, decorative cards, or mobile-first stacks for dense desktop tools.

9. **Design realistic page states**
   - Use real product nouns from the PRD.
   - Fill tables, task cards, logs, artifact panels, and settings with plausible domain data.
   - Include the state transitions a PM or engineer needs to judge: first-run empty, active execution, completed output, error/retry, and settings or artifact management.

10. **Implement the chosen artifact**
   - For `project-native-preview`, create a non-production preview route, story, fixture state, or preview component following local conventions. Keep it isolated and reversible.
   - For `visual-handoff`, create a high-fidelity HTML/React artifact and mark it as visual reference, not production code.
   - For `concept-html`, create a standalone HTML/CSS mockup that opens locally without a build step.
   - Keep dimensions stable with explicit desktop layout constraints, fixed rails, responsive min/max widths, and scrollable panels.
   - Use icons from the existing project icon library when available. For standalone HTML, use inline SVG or simple CSS shapes only when no icon library is available.

11. **Verify visually**
   - Open or render the mockup when tools are available.
   - Check at least one desktop viewport around 1440x900 and one narrower desktop viewport around 1280x800.
   - Verify text does not overflow buttons, cards, rails, tabs, or panels.
   - Verify the UI is not blank, overlapped, or dominated by a single decorative color family.
   - For project-native previews, start the local app if feasible and capture screenshots from the real route.

12. **Package the result**
   - Provide file paths, local open/run instructions, screenshots if generated, and a short handoff note.
   - Include the wireframe-stage output or link to `ascii-layout.md`.
   - Include a traceability table from PRD requirement to screen/state.
   - Include `component-map.md` and `implementation-notes.md` when the UI is meant to guide frontend implementation.
   - Include known assumptions and any PRD/UI-spec conflicts.
   - Include any PRD feedback discovered while building the mockup, with recommended next route: `prd-review` for conflict/readiness issues, `prd-architect` for missing PRD sections.
   - Update the PRD UI appendix or provide exact PRD changes to sync the final UI contract.

## Desktop Workbench Rules

Read `references/desktop-workbench-ui-principles.md` before designing a desktop Agent workbench shell, multi-panel workspace, settings page, artifact page, or task execution UI.

Key defaults:

- Dense operational UI beats landing-page composition.
- User attention should flow from navigation/context to task list to execution canvas to artifact panel.
- Running, queued, failed, and completed task states must be visually distinct.
- Settings pages should feel like system controls, not content cards.
- Artifact pages should prioritize inspection, versioning, actions, and provenance.

## Output Contract

Read `references/mockup-output-contract.md` before finalizing deliverables.

Default deliverables:

- `README.md` or handoff note with purpose, assumptions, and open/run instructions.
- `screen-inventory.md` and `state-model.md` covering the structure-stage contract.
- `ascii-layout.md` or equivalent wireframe-stage section covering UI structure, layout zones, and state model.
- `wireframe-handoff.md` or equivalent structure review note before visual polish.
- `screen-contract.md` or equivalent section describing screens, states, and PRD traceability.
- `component-map.md` when the result is used for implementation alignment.
- `implementation-notes.md` when a frontend team will build or convert the UI.
- `mockup.html`, high-fidelity React artifact, or project-native page/component depending on the chosen mode.
- Screenshot or browser verification notes when feasible.

### Product Delivery Package Evidence

When a `product-delivery-manifest.yaml` is present, read the canonical contract from `prd-architect/references/product-delivery-manifest.md` before packaging the result.

- Update only the UI Producer partition: `artifacts.action_contract`, `artifacts.html`, `artifacts.screenshots`, `ui_baselines`, and `anchors`.
- Every HTML/preview record binds to a current baseline. Every screenshot records the current source HTML ref/hash, state, viewport, and stable artifact ID; changing HTML makes its old screenshots stale regardless of mtime.
- The Action Contract must identify screens, states, actions, next states, and recovery paths. An HTML file without this contract is incomplete Package evidence.
- Each required screenshot must bind to a stable PRD anchor ID, heading path, normalized anchor content fingerprint, screen/state/action semantics, and the screenshot artifact ID.
- Use the screenshot coverage defined by the PRD acceptance criteria and Action Contract: every materially changed page default state plus success, failure, permission, or confirmation states that change acceptance. Do not invent a cross-project screenshot checklist.
- Run the canonical Manifest validator after updating evidence. Do not write the Package verdict, approval, release record, or a ready state.

## Resource Guide

- `references/output-mode-selection.md`：选择 `project-native-preview`、`visual-handoff` 或 `concept-html`。
- `references/templates/screen-inventory.md`、`state-model.md`、`ascii-layout.md`、`wireframe-handoff.md`：结构阶段模板；用户只要 `structure-only` 时优先读取。
- `references/verification-checklist.md`：最终视觉和交付包验证清单。
- `references/desktop-workbench-ui-principles.md`：桌面 Agent 工作台布局和状态规则。
- `references/mockup-output-contract.md`：交付物结构、迁移边界和 implementation handoff。
- `../prd-architect/references/product-delivery-manifest.md`：Package 中 HTML、Action Contract、截图、anchor、baseline 与写权限合同。
- `scripts/check_mockup_package.py`：检查 mockup package 的最小文件结构。

## Side Effects And Safety

- Do not overwrite existing product routes or design files unless the user explicitly asks for repo integration.
- For project-native preview, prefer isolated preview routes, fixtures, or story files. Do not wire preview-only data into production flows.
- Do not push, publish, or commit unless explicitly requested.
- Do not fetch paid/private competitor assets unless credentials and permission are clear.
- Do not treat standalone HTML as production implementation; mark migration boundaries clearly.
- Do not invent missing product requirements to make a page look complete; surface them as PRD feedback.
- Keep generated data fictional unless the user supplied safe real examples.

## Definition Of Done

The Skill run is complete when:

- PRD, UI spec, and real project constraints have been read or explicitly marked unavailable.
- Output mode has been selected and justified.
- `Discovered UI Constraints` are documented when a project path or existing UI is provided.
- UI structure, screen inventory, state model, and ASCII layout are mapped before visual implementation.
- The structure-stage screen inventory, state model, ASCII layout, and wireframe handoff can be reviewed independently.
- The structure review gate has either been passed, explicitly skipped because the user requested final handoff, or converted into PRD feedback.
- Key UI elements are mapped to production components/styles or marked as new.
- The mockup is runnable or openable from a local path.
- Desktop layout, state coverage, and visual quality have been checked.
- The final response includes created, modified, or proposed files, verification result, assumptions, migration boundary, and remaining decisions for production implementation.

## Evaluation

Smoke prompts:

- `基于 /path/to/prd.md、/path/to/ui-spec.md 和 /path/to/frontend 输出桌面端 Agent Client 高保真 preview，开发要按这个实现。`
- `从这份 PRD 开始，先输出 UI 结构、状态模型和 ASCII 布局，确认后再继续做高保真。`
- `把这个桌面工作台 PRD 做成视觉 handoff，包含 component map、screen contract 和 HTML mockup。`
- `只想早期讨论布局，按这份 UI 规范做一个可打开的 concept HTML。`
- `我已经确认 PRD 了，现在要让前端完全复刻这个 UI。`

Non-trigger prompts:

- `帮我写一份 PRD。`
- `只审一下这个 PRD 有没有问题。`
- `做一个手机端 landing page。`
- `直接实现生产功能并补测试。`

Capability checks:

- The output names the PRD and UI spec used.
- The output chooses and explains one of the three output modes.
- Project-local UI constraints are discovered before visual implementation when a project path is provided.
- The result includes structure-stage output such as `ascii-layout.md`, screen inventory, and state model before high fidelity.
- The result includes `screen-contract.md`; implementation-oriented runs include `component-map.md` and `implementation-notes.md`.
- Standalone HTML is clearly labeled as visual reference when it is not production code.
- The mockup/preview includes at least one active execution state and one non-happy-path state when relevant.
- The desktop layout remains coherent at 1440x900 and 1280x800.
- Catalog or project files outside the requested mockup scope are untouched.

## Catalog Notes

- Category: `product-prd`
- Chinese name: 高保真 UI 交付对齐器 / 桌面工作台 UI Mockup 生成器
- Status: `active`
- Provenance: new team Skill created locally for the AI Product Manager Skills Library; no upstream import source.
