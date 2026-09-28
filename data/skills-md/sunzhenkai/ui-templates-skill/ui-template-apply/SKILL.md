---
name: ui-template-apply
description: 消费 `design-system/v1` Active Instance 按 Phase 0–9 实现真实页面，维护 `.ui-template-apply` checkpoint/artifacts，完成 current-build 浏览器证据、review 与幂等 feedback。支持 `bootstrap | increment`。创建 package 交给 ui-template-author；完整重构 Active Instance 交给 ui-template-design。
---

# ui-template-apply

本 skill 只消费已有模板，不创建、迁移或索引模板；在统一契约下只消费有效 Active Instance 或从 published package 显式 adopt-only 建立 Active Instance。Authoring 由 `ui-template-author` 所有；完整 Design System 编辑由 `ui-template-design` 所有。官方 package 随 Author `catalog/` 安装；Apply 对项目库默认只读 pin，不写入项目 `templates/`；空项目缺 `templates/` 不是失败。

## Apply Mode 与移交

- 已有有效 Active Instance 且要求实现页面 → 进入 Phase 0–9，并声明 `mode: bootstrap | increment`。
- 无 Active Instance 且 greenfield bootstrap → 只能先从 **published** package adopt-only 建立 Active Instance，再写业务源码；该路径是普通消费降级，不得声称高保真。
- 用户明确要求对齐原版视觉 → 仍只读模板实现，并移交模板认证链路处理对照，见 [source-blind-boundary.md](references/source-blind-boundary.md)；Apply 不执行 source oracle 对照，差异回写 skill/模板后重生，不得改生成物。
- “做成模板/提取风格/导入模板/退役或删除模板” → 移交 `ui-template-author`。
- “建立或重构项目级 Design System / 统一 token 与 Pattern” → 移交 `ui-template-design`。没有 freeze 时本 skill 仍按现行 Phase 0–9 执行。

## 启动边界

- 已选 **published** 模板并要求实现页面 → 进入本流程（source-blind 干净实现）。
- 用户明确要求对齐原版视觉 → 仍只读模板实现，并移交模板认证链路处理对照；Apply 不执行 source oracle 对照，差异回写 skill/模板后重生，不得改生成物。
- “做成模板/提取风格/导入模板/退役或删除模板” → 移交 `ui-template-author`。
- “建立或重构项目级 Design System / 统一 token 与 Pattern / 修改 core 或 project binding 语义” → 移交 `ui-template-design`。
- 项目根必须有 digest 一致的 `design-system/v1` Active Instance；schema v2 template 与旧 freeze 都是 migration-only source。高保真需求必须先由 `ui-template-design` 领养、绑定并冻结 Active Instance；increment 缺 Active Instance 停止。bootstrap 可按 [active-implementation.md](references/active-implementation.md) adopt-only，但不能用于高保真认证。校验走 `runtime/check_active_instance.py`（discovery wrapper）→ `runtime/shared_validate_design_system.py`；禁止把 wrapper 写入 `UI_DESIGN_SYSTEM_VALIDATOR`。
- Intake 运行 `manage_template_index.py resolve <name>`（`require-published` 默认不播种）。项目 `published` 行优先；项目 `retired` 行不得被 catalog 覆盖；项目没有该行时只读 Author catalog 并 pin 到 `.ui-template-apply/`。只有项目库与 catalog 都没有该 published 模板时才报没有模板、停止并移交 Authoring，禁止猜测。空项目缺 `templates/` 不是失败。
- 判定对象是本次将写入前端应用源码的**输出根**，不是仓库根、`.ui-template-apply/` 或兄弟应用。先运行 `architecture-site <output-root>`。输出根不存在/为空/只有空子目录或 git 占位，或用户要求从零搭建时判定 `greenfield`：必须先向用户展示闭集层候选并等待确认，未确认不得写应用源码。仓库已初始化但输出根仍是新应用时仍是 `greenfield`。兄弟应用、workspace 约定或功能规格里的技术提及只可作为候选或 `observed_constraints`，不得当作已确认。仅当该输出根已有依赖清单或实质源码时才是 `existing`：已有工程只记录观察到的栈，禁止静默换栈。
- Phase 9 通过且无 proposed feedback 后会话 closed：必须提示可以删除 `.ui-template-apply/`；未领养则本仓不应有 `templates/`。不自动删除。
- MUST NOT 读取原版 checkout、`meta.sources[]` 路径或工作区已有生成物作为实现参考。生成目录是本次约定的空目录或当前输出目录，不得把历史输出当参考。

## 必读契约

先读 [active-implementation.md](references/active-implementation.md)：校验 Active Instance、声明 mode、checkpoint digest、Impact-based Resume、vendor conditional loading 和 feedback ownership。

再读旧迁移契约 [template-contract.md](references/template-contract.md)： [template-contract.md](references/template-contract.md)：只接受 `schema_version: 2` 与 `source | computed | estimated | default`；四种 origin 都按确定值消费；`spec.md` 是规则入口，`tokens.yaml` 是精确值唯一载体，coverage 在实现前形成 accepted/deferred/excluded 决定。存在 `fidelity.yaml` 时校验 supported profile；无 sidecar 为 legacy-baseline，未知 profile 停止。不得发布 stack adapter。消费项目根若有 design freeze，按 [apply-workflow.md](references/apply-workflow.md) 的规则投影为结构层约束或停止，不得静默混用；缺少 freeze 不是失败。

## Phase 0–9

严格按 [apply-workflow.md](references/apply-workflow.md) 执行，并在项目根维护标准 `.ui-template-apply/`：

0. Intake → `00-intake.md`、`00-architecture.yaml`
1. Design direction/token freeze → `01-design-direction.md`、`01-token-map.yaml`
2. IA/layout/routes → `02-routes.yaml`
3. Project structure → `03-structure.md`
4. Component inventory → `04-components.yaml`
5. Representative slice → `05-07-progress.yaml`
6. Complete included page modes → 同上
7. Global systems → 同上
8. Browser verification → `08-verification.json` + `evidence/`
9. Review/feedback → `09-review.md` + `feedback/`

每阶段状态和 digest 写入 `checkpoint.yaml`（新会话使用 `design-system-apply-checkpoint/v1`）。恢复先验证 scope、contract/binding/projection digest、stable IDs、change set、source/build identity 和 Phase 8/9 证据；用 Impact-based Resume 从最早失效 phase 重开。任何身份/digest 失配都停止，不得选择性继续。页面存在不能替代证据。

## 工具与质量

- 外部知识/审美/组件/浏览器/review 路由见 [toolchain.md](references/toolchain.md)。vendor rules 按 [active-implementation.md](references/active-implementation.md) 与 `resolve_vendor_refs.py` 条件加载，未匹配栈不预加载。
- 门禁见 [quality-gates.md](references/quality-gates.md)。每个结果绑定模板或 Phase 1 local rule ID、当前 template/source/build identity 和 evidence；风格一致性、信息语义和元素放置用 current-build 证据复验，不以固定 checklist 数量或 prose“已检查”宣称完成。
- 没有真实浏览器能力时停止并请求可运行方式；静态检查不能替代 Phase 8。

## Feedback 与汇报

Phase 9 先声明 `ownership: package | binding | apply-skill`。package/core 缺口按 [apply-workflow.md](references/apply-workflow.md) 创建 `design-system-feedback/v1` proposed feedback（UUID 文件名、相对 `.ui-template-apply/` 的 evidence refs、package identity、Stable Entity IDs、原子写入失败回滚）；binding 缺口只按显式确认的 binding change set 修复；workflow 缺陷回写本 skill。旧 schema v2 feedback 只用于迁移读取。`LOCAL-*` design rule IDs 只属于当前会话，不得作为 feedback targets。

最终汇报只引用 `.ui-template-apply/`：included/deferred/excluded、当前身份、完成 phases、current-build verification、P0/P1/recheck、反馈 UUID/receipt、实际工程命令及不可用工具回退。Phase 9 通过且 inbox 无 proposed 时必须输出 `session_closed: true`、`may_delete_apply_root: true` 与固定句子「可以删除整个 .ui-template-apply/；删除后生成页面不受影响；再次 Apply 视为新 Intake。」未领养则说明本仓不应存在 `templates/`。Phase 8/9 无效或任一 gate 失败时不得说“完成”，也不得说会话可删。
