---
name: ui-template-design
description: 在消费项目创建、领养、重构、迭代并冻结 `design-system/v1` Active Instance（portable core、project binding、Token Projection、Primitive/Pattern/Page Type、Gallery 与浏览器证据）。用于“做设计系统/统一 UI 框架/抽取 token 与页面模板/重构漂移的前端视觉/给 Agent 可组装的组件层”。无 package、未安装 ui-template-author 或 ui-template-apply 时也必须使用本 skill。发布 package 交给 ui-template-author；实现业务页交给 ui-template-apply。
---

# ui-template-design

把前端从「Agent 直接生成页面」变成「在 Active Design System 约束下组装页面」。本 skill 创建并冻结 `design-system/v1` Active Instance：portable core + `binding.yaml` + Token Projection + Stable Entity IDs；不发布 package，不实现全站业务页。缺少 Author、Apply、catalog 或项目 `templates/` 不是失败。

## 路由

先按可观察信号判定任务类，写入 `00-intake.md`，再只加载 [task-classes.md](references/task-classes.md) 中该类必读文件。禁止凭「优化一下 UI」猜测。判定顺序、必读/禁止预加载表只以 `task-classes.md` 为准。

所有影响 freeze 本体的选择都执行 [decision-gates.md](references/decision-gates.md)：先给出至少 2 个合法候选与影响，等待用户选择或明确授权；框架默认和 Agent 偏好都不是确认。

移交红线：「做成模板 / 做成可复用模板 / 提取风格入库」→ 停止，移交 `ui-template-author`；「用模板实现页面 / 用 Active Instance 实现页面」→ 停止，移交 `ui-template-apply`。未安装 Apply 时说明 Active Instance 冻结后可再装，不得假装已实现业务页。

## 不变量

- 可在未安装 Author/Apply、没有模板的环境执行到完成态。
- 后一层不得重新决定前一层的精确值或结构。仅有 Primitive 或只安装第三方组件库不算完成；复用组件体系组件不豁免 Primitive 注册。
- `core/tokens.yaml` 是 token 精确值唯一权威；原生 theming 是合法载体形态，但在统一契约中只是 `binding.yaml` 声明的 Token Projection，不得双向同步或手改绕过。禁止未映射调色板、hex、任意 spacing。
- 页面只组装已登记 Page Type 与 Pattern，禁止为单页私造页头、间距或空状态。
- 约束靠 Agent 会加载的规则文件和扫描，不靠自觉。禁止默默覆盖项目根 `AGENTS.md`。
- 生成物不是修复面：缺陷回写 token / Primitive / Pattern / 本 skill 后重生。
- 无模板时禁止写 `templates/INDEX.md`。不把项目 token 伪装成 published 模板。
- greenfield 未确认闭集层前不得写应用源码或依赖清单。existing 不静默换栈，默认冻结业务行为。

## 阶段 0–9

阶段不可跳过。完成看产物与证据，不看「已经写了页面」。状态在项目根 `.ui-template-design/`。

0. Intake → `00-intake.md`：任务类 `bootstrap | refactor | iterate`、source origin `blank | template-package | legacy-freeze-migration`、站点 `greenfield | existing`、输出根、变更集合、decision gates 账本。Active digest 不匹配则停止。`iterate` 不重开完整 0–9。
1. Stack / binding → `00-architecture.yaml` 与 `binding.yaml`：greenfield 按选型引导逐层列出候选（分层建议语义 + 官方 CLI 优先，见 greenfield.md）并由用户选择；existing 确认保持或另行拆分迁移。未确认不得写应用源码。
2. UX Model & Inventory → `01-ux-model.md`、`01-inventory.yaml`。`refactor` 必做；`iterate` 禁止全量 inventory。
3. Token Freeze / Projection → `core/tokens.yaml` 与 binding projections；existing 含 `02-legacy-mapping.yaml`。精确值只在 `core/tokens.yaml`。
4. Primitives → `core/primitives.yaml` + binding `primitive_paths`。Stable Entity ID 状态表闭合，只消费 token。
5. Patterns & Page Types → `core/patterns.yaml`、`core/page-types.yaml`、`core/layout.yaml`。含 Data-State、断点、运动白名单、禁止组合。
6. Constitution & rules → `05-rules-receipt.md`。写入 `AGENTS.design.md` 与 `.cursor/rules/ui-design-system.mdc`（或等价可加载片段）。
7. Gallery → `07-gallery.yaml`。应用内 `/dev/design-system` 或等价；Storybook 可选。
8. Visual loop → `08-verification.json` + `evidence/`。真实浏览器；自愈最多 3 轮。无浏览器则停止。
9. Freeze & Report → `design-system.yaml` 的 `status: frozen`。contract、binding、projection、Gallery 和 browser evidence digest 绑定当前本体。未迁完业务页仍可完成。

Validate/Freeze 前运行 runtime。本 skill 可单独安装：`check_active_instance.py` 是 discovery wrapper，会启动同目录 `shared_validate_design_system.py`。`UI_DESIGN_SYSTEM_VALIDATOR` 只能指向该共享实现；指向本 wrapper 或 Author wrapper 会以 `VALIDATOR_SELF_INVOCATION` 失败，不得 freeze。

```bash
python3 skills/ui-template-design/runtime/check_active_instance.py validate .ui-template-design --kind active --json
python3 skills/ui-template-design/runtime/check_design_freeze.py gate --design-root .ui-template-design --project-root . --json  # legacy-freeze migration only
python3 skills/ui-template-design/runtime/scan_design_constraints.py <output-root> --json
```

安装态（无仓库 `scripts/`、无 Author）同样调用：

```bash
python3 runtime/check_active_instance.py validate .ui-template-design --kind active --json
```

仅有 Constitution、规则未落地、扫描失败或 digest 不一致不得 freeze。digest 算法为 `sha256-canonical-json-v1`；写 freeze.yaml 前用 `compute-digest` 子命令计算：

```bash
python3 scripts/validate_design_system.py compute-digest .ui-template-design/design-system.yaml --json
```

## 完成定义

可以声明完成，当且仅当：decision gates 均已选择或获得明确授权；UX Model 无 unresolved；`core/tokens.yaml` 已冻结且 projection 一致；Primitive/binding 路径闭合；声明的 Pattern/Page Type/layout 引用闭合；可执行规则已写入且本次扫描通过；Gallery 覆盖 stable IDs 且有 current-build 截图；视觉 loop 通过或 3 轮后升级人类；`design-system.yaml` 为 `frozen` 且 contract digest 一致，binding/projection digest 一致。高保真 Apply/Certification 只能消费这个 frozen Active Instance，并在认证 gate 记录三个 digest。`iterate` 另须：变更集合已声明、只动点名层、未声明路径保持原字节、扫描通过、freeze digest 已刷新。不得称为完成：只有 Markdown、只有 shadcn 初始化、只改了一个业务页、截图身份过期。全站未迁完不是失败。未装 Author/Apply、未用模板不是失败。

## 汇报

报告 Active Instance 路径、contract/binding/projection digest、task class/source origin、capability、kit 覆盖、Gallery 身份、实际命令。不要求 Apply Phase 8。提示：可以删除 `.ui-template-design/` 状态目录；设计系统本体仍留在输出根。不自动删除。
