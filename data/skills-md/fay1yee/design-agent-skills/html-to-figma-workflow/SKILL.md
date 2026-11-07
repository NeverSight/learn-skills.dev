---
name: html-to-figma-workflow
description: Orchestrate a controlled transfer of an approved HTML page, local web app, implemented UI, or deterministic UI state family into an authorized Figma file with reproducible state capture, page-first creation routing, final Section or Frame placement, editable structure, queue-stall recovery, privacy, and QA. Use when a user asks for HTML to Figma, code to Figma, webpage to Figma, 网页转 Figma, 代码回写 Figma, wants editable Figma reconstruction, needs default, selected, loading, empty, error, or reduced-motion states transferred, needs imported layers placed in a Section or Frame, or reports a conversion job stuck in the server queue. Require the installed official Figma integration for actual reads or writes; this skill supplies the project-safe workflow and does not redistribute Figma materials. / 在获得授权的前提下，将 HTML、本地网页、已实现界面或确定性状态族可控地转入 Figma，逐状态固化后先在 Page 级生成，再归位到 Section / Frame，并保留可编辑结构、队列恢复、隐私边界和 QA 记录。
---

# HTML to Figma Workflow / HTML 转 Figma 工作流

Use this skill as the orchestration and safety layer around an installed Figma integration. Keep proprietary project details out of reusable instructions and public artifacts.

本 Skill 作为已安装 Figma 集成之上的流程与安全层，不将专有项目细节带入可复用说明或公开产物。

## External dependency / 外部依赖

For Figma reads or writes, use the official Figma integration available in the current environment:

- `figma-use` for Figma Plugin API operations;
- `figma-generate-design` for building a page or composed view in Figma from code or a running web app;
- `figma-generate-library` when missing tokens or components must be created under an approved design-system scope;
- `figma-code-connect` when approved code-to-component mappings are part of the task.

Load and follow each external skill before calling its tools. Their materials remain governed by their upstream terms. Reference them by name; do not copy their instructions, assets, or implementation into this skill or relicense them.

Figma 读写需使用当前环境已安装的官方集成。调用工具前必须加载对应的外部 Skill；只引用名称，不复制其指令、资产或实现，也不重新许可。

## Preconditions / 前置条件

Confirm all of the following before any write:

- the user is authorized to access and modify the target Figma file;
- the exact source URL, local route, build, viewport, and state are identified;
- each required dynamic state has a stable state ID and a reproducible entry or setup sequence;
- the target file and destination page are explicit;
- the Page used as the creation parent and the Section or Frame used as the final placement target are recorded separately;
- the source assets may be transferred into that file;
- the design-system source of truth is known;
- a duplicate page, branch, version, or other recovery point exists;
- the user has approved any upload of non-public imagery or data.

写入前确认目标文件权限、源页面版本与视口、用于生成的目标 Page、最终归位的 Section 或 Frame、素材权利、设计系统事实源、恢复点和非公开数据上传授权。

If any item is missing, stop before Figma mutation and return a preflight gap list.

任一前置项缺失时，在 Figma 写入前停止，输出预检缺口清单。

## Workflow / 工作流程

### 1. Lock scope and privacy / 锁定范围与隐私

Record:

- included routes, sections, states, and viewports;
- excluded admin, test, account, or confidential surfaces;
- approved destination file and page;
- content or assets that require redaction or placeholders;
- operations requiring a separate confirmation, including shared-library publication and deletion.

记录纳入的路由、模块、状态与视口，排除管理、测试、账户和保密页面，明确目标文件与 Page、脱敏项和需要二次确认的操作。

Never place real file keys, node IDs, customer names, unpublished product names, proprietary font files, local user paths, credentials, or internal URLs in public examples or logs.

公开示例和日志中不得出现真实文件 Key、节点 ID、客户名、未发布产品名、专有字体文件、本地用户路径、凭证或内部 URL。

### 2. Freeze the source reference / 固化源页面证据

Capture or record the approved source at each scoped viewport and state. Preserve:

- page dimensions and scroll boundaries;
- typography, spacing, color, media, and layout evidence;
- hover, focus, pressed, selected, loading, error, empty, and reduced-motion states where relevant;
- source build or commit identifier;
- asset provenance and rights status.

为每个视口与状态保留已批准的源页面证据，包括尺寸、滚动边界、排版、间距、颜色、媒体、布局、交互状态、构建版本和素材来源。

For interactive surfaces, create a state manifest before conversion. Record one row per required state:

- stable `state_id`;
- route plus query or hash parameters;
- setup actions when a direct state URL is impossible;
- viewport, theme, locale, and motion preference;
- readiness signal or exact observable condition;
- expected visible result and final Figma target.

Prefer a deterministic URL, approved fixture, or authorized state injection over a transient hover, timed animation, or uncontrolled remote response. A capture mode may bypass entrance motion so content is immediately visible, but it must not change content, selected values, layout, or interaction meaning. Capture the default state and each required selected, loading, empty, error, completion, or reduced-motion state separately.

动态页面先建立状态清单：每个状态记录稳定 `state_id`、Route / Query / Hash、必要准备动作、视口与偏好、就绪信号、预期可见结果和最终目标。优先使用可重复入口，不把短暂 Hover、定时动画或不可控远端响应作为唯一状态来源；捕获模式可以跳过入场动效，但不得改写内容、选中值、布局或交互语义。

### 3. Inspect source and target systems / 检查源与目标系统

Inventory the source code and the target Figma file before creation:

- tokens, CSS variables, themes, and breakpoints;
- reusable code components and their default props;
- existing Figma variables, styles, components, variants, and libraries;
- fonts available in the target environment;
- image, SVG, icon, and video treatment;
- naming and page organization conventions.

创建前盘点源代码的 Token、CSS 变量、主题、断点与可复用组件，以及目标 Figma 中的变量、Style、组件、Variant、字体、素材和命名约定。

Use `design-system-contract-lock` first when ownership, precedence, component responsibilities, or acceptance rules remain ambiguous.

事实源、责任归属、组件边界或验收规则仍不清晰时，先使用 `design-system-contract-lock`。

### 4. Choose the representation / 选择 Figma 表达方式

Prefer, in order:

1. approved library component instances;
2. approved local components and variants;
3. editable Auto Layout structures bound to variables and styles;
4. documented primitives when no approved reusable asset exists.

Do not use one flattened screenshot as the final deliverable. A capture may be retained temporarily as visual evidence only.

优先使用已批准的库组件实例、本地组件与 Variant、绑定变量的 Auto Layout 结构。单张扁平截图只能作为临时视觉证据。

### 5. Create at Page level, then place / 先在 Page 级生成，再归位

Treat the destination Page as the default creation parent. Treat a Section or nested Frame as a final placement target unless the installed official integration explicitly supports direct nested creation and a small probe has already completed successfully.

目标 Page 默认承担图层生成；Section 或嵌套 Frame 默认承担最终归位。只有在官方集成明确支持、且小范围探针已经成功时，才允许直接向嵌套节点创建。

For each bounded import:

1. record the `state_id`, destination Page, final Section or Frame, insertion anchor, and a private run ID;
2. submit one conversion for one state and viewport at the Page level or the integration's default page canvas;
3. wait for a terminal job result before starting another import for the same source, state, and viewport;
4. verify that one editable top-level DOM result exists and that no partial duplicate was created;
5. move that exact result into the final Section or Frame without rebuilding its internal hierarchy;
6. verify parent, position, order, clipping, constraints, Auto Layout, prototype links, and visual parity after the move.

每个分区先记录生成 Page、最终 Section / Frame、插入锚点和私有 Run ID；只提交一次 Page 级转换；成功生成可编辑顶层图层后再整体移动，并复核父级、坐标、层级、裁切、约束、Auto Layout、Prototype 和视觉一致性。

Read [references/destination-routing-and-queue-recovery.md](references/destination-routing-and-queue-recovery.md) whenever the requested destination is a Section or Frame, or a conversion job remains queued without progress.

### 6. Recover from a stalled queue / 从队列卡住中恢复

Treat a job as stalled when it exceeds the integration's documented wait or shows no state change across two normal status checks. Do not submit repeated copies to the same nested destination.

当任务超过集成规定等待时间，或连续两次正常状态检查都没有推进时，将其标记为 `stalled`，不要继续向同一嵌套目标重复提交。

Before one controlled retry:

- record the private job ID, state ID, source/build, viewport, creation-parent node type, final-target node type, and last status;
- inspect the destination Page and final region for a partial or delayed result;
- cancel the stalled job when the integration supports cancellation; otherwise record an orphan-job risk;
- remove nothing without authorization; quarantine or label partial output when possible;
- retry once with the same frozen source at Page level and a new run ID;
- scan for duplicate top-level results before moving the successful result.

If the Page-level retry also stalls or returns an ambiguous result, stop and report the blocker. Do not keep queueing jobs, move an unverified partial result, or claim completion.

重试前记录任务状态并检查半成品；支持取消时先取消，不支持时标记孤儿任务风险。使用相同源页面和新 Run ID 进行一次 Page 级重试，移动前扫描重复顶层图层。重试仍卡住或结果不明确时停止并报告。

### 7. Transfer in bounded sections / 按有界分区转换

Create or update one meaningful section, state, and viewport at a time. Name the top-level result so the page, viewport, and `state_id` remain distinguishable. After each result:

- return the affected node IDs privately to the task context;
- compare a rendered screenshot against the frozen source;
- verify fonts, layout constraints, Auto Layout, variables, component linkage, images, and clipping;
- record exceptions before continuing.

每次只创建或更新一个有明确边界的分区，然后检查字体、约束、Auto Layout、变量、组件关联、图片和裁切，记录例外后再继续。

Keep node IDs inside the authorized working context. Redact them from reusable examples, public issues, screenshots, and repository documentation.

节点 ID 仅限已授权的当前任务上下文，不进入可复用示例、公开 Issue、截图或仓库文档。

### 8. Validate before handoff / 交付前验证

Check every scoped viewport and required state for:

- structural hierarchy and reading order;
- typography family, style, size, line height, and wrapping;
- spacing, alignment, dimensions, and overflow;
- token and component-instance linkage;
- image crop, icon source, and asset rights;
- responsive constraints and resize behavior;
- interaction targets, prototype links, and focus order where included;
- state identity, readiness condition, and adjacency with related default or alternate-state results;
- temporary captures, placeholders, detached instances, and unexplained hard-coded values.

逐个视口与状态检查结构、排版、间距、对齐、溢出、Token 绑定、组件实例、图片裁切、多端约束、交互连线、占位内容、Detach 和未解释硬编码值。

Do not delete temporary captures, source pages, components, or versions without explicit approval. Do not publish or update a shared library unless that exact external action was authorized.

未获得明确批准时，不删除临时截取、源 Page、组件或版本，不发布或更新共享组件库。

## Required output / 必须输出

Return:

1. authorized source and target scope;
2. privacy and asset-rights decisions;
3. external Figma skills used;
4. deterministic state manifest, state IDs, and readiness signals;
5. Page-level creation parent and final Section or Frame target;
6. conversion job terminal status, retries, orphan risk, and duplicate scan result;
7. created or updated sections and state-family results;
8. component, variable, font, and asset mapping summary;
9. viewport and state QA matrix;
10. exceptions, blockers, and temporary artifacts;
11. explicit confirmation that no shared library was published unless authorized.

输出授权范围、隐私与素材权利决定、外部 Figma Skill 使用记录、确定性状态清单与就绪信号、Page 级生成父级、最终归位目标、任务状态与重试记录、重复扫描、分区与状态族变更、组件与 Token 映射、多视口 / 多状态 QA、异常与临时产物，并明确说明是否发布过共享库。
