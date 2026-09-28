---
name: ui-template-author
description: 从运行中的 Web 站点(URL)、代码仓库(本地路径或 Git 地址)、图片(截图/设计稿)或设计文档(Markdown/PDF)中提取 UI 设计风格，创建/导入/更新 `design-system/v1` portable package，并维护 templates/ 模板库；旧 schema v2 输入只走显式迁移。用于“做成模板/导入 UI 模板/提取设计规范/更新模板”；按模板实现页面应移交 ui-template-apply。
---

# ui-template-author — Template Authoring

本 skill 只创建、迁移、更新和索引 portable Design System Package；本 skill 只创建、迁移、更新和索引 UI 模板，不实现消费项目页面。浏览、退役与删除同样由本 skill 执行，手续见 [template-lifecycle.md](references/template-lifecycle.md)。新发布产物格式由 [references/package-format.md](references/package-format.md) 定义；旧 schema v2 只作为显式迁移 source，格式语义见 [references/spec-format.md](references/spec-format.md)。分层抽取见 [extraction-layers.md](references/extraction-layers.md)。Apply 通过该契约解耦消费。现行闭环目标见仓库 `governance/FUNCTIONAL-LOOP.md`（安装环境可只读本 skill 引用）。

模板产品成对安装，不要用 `--all`：

```bash
npx skills add sunzhenkai/ui-templates-skill -s ui-template-author -s ui-template-apply
```

项目级 Design System（可选、可单独安装，不要求本 skill）见 `ui-template-design`。

治理、checksum 与回滚仍用 `make bundle` / `make install`。官方 published 模板在本 skill 只读 `catalog/`；项目可写库是项目根 `templates/`。

## 路由

- URL → [source-web.md](references/source-web.md)
- 代码仓库 → [source-repo.md](references/source-repo.md)
- 图片/截图 → [source-image.md](references/source-image.md)
- Markdown/PDF 设计文档 → [source-doc.md](references/source-doc.md)
- 新建/更新 `design-system/v1` package → [package-format.md](references/package-format.md)
- schema v2 template / design-freeze v1 → 显式迁移为 candidate；不直接发布旧格式
- 浏览 / 退役 / 删除模板 → [template-lifecycle.md](references/template-lifecycle.md)
- “用模板实现页面/搭后台” → 停止 Authoring，移交 `ui-template-apply`。
- “建立或重构项目级 Design System / 选择技术栈 / 生成 project binding” → 停止 Authoring，移交 `ui-template-design`。仅当用户明确要求把已冻结视觉发布为可复用 package 时，才把 `.ui-template-design/` 当作可选 session source；日常库动词不读不改该目录。
- 官方 published 模板在本 skill 的只读 `catalog/`；消费项目可写库是项目根 `templates/`。项目库没有同名行时不得声称“没有模板”；只有用户要求写模板、落库 feedback、retire/delete 或明确「接到本仓」时，才从 catalog 领养到项目库。
- 用户要求“对齐原版视觉”的发布级对照 → Template Certification Gate（`scripts/run_template_certification.py` + `governance/release/CERTIFICATION-v1.md`）：固定 Visual Oracle revision、candidate package、同 identity 的 frozen Active Instance 与固定 prompts，source-blind 干净 Apply 后按 Pattern 产生 Pattern Equivalence Records。每个 passed Pattern 覆盖五个视觉维度组且逐条锚定 oracle measurement；package feedback 必须关闭。认证输入不进入 Apply，也通过 checkpoint 校验拒绝进入实现。candidate 停留在 `governance/candidates/`；publish/upgrade/catalog replacement 必须附带当前 accepted certification report，production promotion 仍需用户单独确认。

## 不变量

- 新建/更新必须产出 `design-system/v1` portable package；package 禁止 `binding.yaml`。模板不得包含 `implementation/`、stack adapter、工程目录、依赖、API/mock/data、状态库或具体项目业务结构。
- 七层 core 为 tokens、primitives、patterns、page-types、layout、rules、evidence；`tokens-only | ui-kit | page-system` 决定必填层，缺层必须写成 capability 边界，不得即兴补语义。
- `core/tokens.yaml` 是精确值唯一权威；原生 theming 是消费项目 Token Projection，Author 不得生成。
- Primitive、Pattern、Page Type、Token 和 Rule 使用 Stable Entity ID；展示名不是身份。published ID 不复用，替代时保留 retired/superseded 说明。
- `fidelity.yaml` profile v1 只表达 `layout_scenes`、`component_geometry`、`state_presentations` 三类技术栈无关 observable；不发布 AST/call graph/source snapshot，不规定框架、DOM、CSS class 或 stack adapter。
- token leaf 统一含 `value`、适用 `unit`、`origin: source | computed | estimated | default`。缺口用有 basis 的 default，不留给 Apply 猜测。
- 每条提升进 package 的声明必须过三证准入：Observation（可观测证据 locator）、Basis（可复核 method/revision 或带 basis 的 default）、Consequence（`target` 解析到已声明 token/entity，且会改变实现选择）。缺一即 omit，禁止降级写入。
- 声明为 `product` scope 的规则必须由同一 role 上 ≥2 distinct sampled surface 的 recurrence 证据支撑；不足时收窄为 `surface` scope，不得用单 surface 证据冒充产品级规则。
- prose/rules 只保留会改变实现选择的陈述；Index 前执行 no-op pass，删除组件清单式罗列、重复 YAML 与泛泛建议。
- update 不得静默移除既有 active stable entity/rule ID：移除必须显式记为 `retired`/`superseded` 或在 change-set 声明，报告 `removal_set`；未声明丢失报 `SILENT_DECISION_REMOVAL`。
- Non-negotiables 与跨文档规则使用稳定 rule ID；coverage 对声明项作 observed/defaulted/unsupported 完整互斥分类。
- 来源、locator、revision、confidence、asset license/redistribution/privacy 与 default basis 都进入 evidence。
- `meta.sources[]` 是出处身份，不是文件系统绑定。Session source 只存在于本次用户明确给出的导入/从源更新；已发布模板缺 checkout 时走 portable 校验，禁止向用户索要历史本地路径、扫描 sibling/`/tmp`/`example/**` 或按 ref clone。
- 项目库与 catalog 都没有可用 published 模板时，才引导从源创建；catalog 已有官方模板时不得报“没有模板”。

## 强制工作流：Generate → Validate → Eval → Index → Report

顺序不可交换，任何 gate 失败即停止；失败后不得修改生产 `templates/INDEX.md`、不得把任务/模板标为完成、不得报告成功。对已发布模板的 portable 校验不走 capture/staging gate，缺 session source 不是失败。

### 0. Intake 与 feedback discovery

确认模板名、更新或新建、授权和范围，以及库动词（create / adopt / update-from-source / update-from-feedback / update-portable / validate / retire / delete）。先分清 **session source**（用户本会话给出的可读仓库/文档）与 **provenance**（已写入 `meta.sources[]` 的出处身份）。只有新建导入或从源更新才需要 session source；已发布模板的 provenance 不得当成「请提供本地绝对路径」的理由。

本次从源导入或从源更新时：固定 session source、将写入 meta 的 source ID、完整 revision、platform、**本次变更集合（路径/组件，可用 L0–L6 标签）**、scenes/components/contexts、limits 与 conformance；默认 structural，只有用户明确要求仅视觉语言时才是有理由的 style-only。未冻结变更集合不得 Generate-from-source；未声明文件保持原字节。对已发布模板做校验/改文档/消费反馈/退役/删除时跳过 session-source Intake。retired 模板不得被汇报为可被 Apply 新消费。

更新前按 [feedback-lifecycle.md](references/feedback-lifecycle.md) 扫描显式路径及已授权消费项目 `.ui-template-apply/feedback/`，按 UUID/fingerprint 幂等处置。将要修改项目库而项目无同名行且无目录时，先按 pin 身份从 catalog 领养并在 Report 声明；已有同名行或目录不覆盖。未知 schema 或非法状态记录先修复，不跳过。

repo capture 仅在已有 session source 时运行，且只接受 [repo-capture-format.md](references/repo-capture-format.md) 的 closed JSON/YAML literal source graph。不得执行来源代码、用 regex 冒充 TSX/JS parser、以“3–5 个代表组件”静默抽样，也不得为补 source 而按 provenance 自行联网 clone。用户把 Git 地址作为**本会话导入输入**时，读取该地址是 session source，不是补取。歧义、动态表达式、同 context/slot 冲突和 limit 超限均 unresolved；先请求收窄 scope 或显式 decision。structural 导入需要 chrome-complete graph（`shell_variant` + 有序 slots；已声明的锚点必须闭合）。缺 graph、chrome incomplete 或用页面模式分类学覆盖来源壳 IA 时不得 Index。`confidence.layout: high` 需要 chrome-complete sidecar。

### 1. Generate

本次从源导入时，在 staging 生成/更新候选模板四个必备文件、repo 适用的 `fidelity.yaml`、capture receipt、可选设计文档/assets/`apply/` 与**候选 INDEX**。为规则分配稳定 ID，补齐 coverage、证据、默认依据和资产决定。`fidelity.yaml` 的 token usage/关系/negative facts 必须来自完整 closure；structural records 有 unresolved 时停止。没有 session source 时不得为已发布模板伪造 source-direct sidecar，也不得停下来要历史路径。此阶段不得改 production template/INDEX。

### 2. Validate

`design-system/v1` candidate 先运行统一 package validator；旧 schema v2 candidate 才使用模板 checker。任何 gate 失败即停止，package candidate 失败不改 production INDEX。

```bash
python3 scripts/validate_design_system.py validate <candidate-package> --kind package --json
```

旧模板 portable 校验继续使用：

```bash
python3 scripts/validate_templates.py <template-or-templates-root> --index <index> --json
```

已发布模板、无 session source：portable 即可；replay 为 `not-run` 是成功，不是要路径的理由。

仅当**本会话**用 session source 做 structural Generate-from-source 时，才绑定该 source 并要求 replay 的 `declared = resolved = executed = passed > 0`。这时 portable `not-run` 不能替代这次 replay。

```bash
python3 scripts/validate_templates.py <candidate-template-or-templates-root> \
  --index <candidate-index> --json \
  --source-root <source-id>=<session-source-root> --require-source-replay
```

`--source-root` 只能是本会话用户给出的路径。安装环境不得假设本仓 `AGENTS.md` 或固定当前目录。只运行 prose checklist 不算通过。

### 3. Eval

本次从源导入时，无论候选是否已有 `design-system/v1` manifest，都先对相同 request/revision/scope/decisions 重复 capture；closure digest、record identities/status 与 unresolved 必须完全一致。package candidate 不得把 source gate 降级为 portable-only shortcut。已发布模板无 session source 时跳过 capture 重复，只跑 portable eval。page-system 的 Generate-from-source 必须具备结构化 placement closure、stable Pattern/Page Type identity、可解析 evidence 和通过的 source replay；无法闭合时只能显式降级 capability，不得继续发布为 page-system。再运行 Authoring/schema/反馈/repo-profile portable contract eval；要求 runner 报告 `declared = parsed = executed > 0` 且所有阻断 script judge 通过。LLM judge 仅在发布策略要求且已授权时运行。Eval 不存在、不可执行、输出不可解析、reproducibility 漂移或 case 数不一致都视为失败。

bundle 在本 skill 根分发 `runtime/capture_repo_fidelity.py`、`runtime/run_authoring_gate.py` 和 `runtime/run_contract_evals.py`；普通离线执行确定性 judges，不调用模型或网络。runner 缺失、能力不足或输出不满足计数/身份契约时停在 Eval，保持 production INDEX 不变。

### 4. Index

只有本次从源导入的 capture/reproducibility、对该 session source 的 required replay 与 Eval 全部成功后，才可由 staging gate 原子应用候选 INDEX 到 production `templates/INDEX.md`。已发布模板的 portable 校验成功不写入 INDEX，也不调用需要 `--source-root` 的 staging gate。应用前 gate 必须证明 production INDEX digest 未变化；应用后核对 INDEX 的 name/description/source.type/captured_at 与 meta 一致。任何失败或并发变化都不 promotion；写入失败回滚并不得进入成功 Report。

### 5. Report

按 [authoring-report.md](references/authoring-report.md) 报告 package 路径、`design-system/v1` identity/version/capability、contract digest、来源与 coverage、模板路径、对比度、default/estimated 摘要、validation receipt、canonical digest、unresolved、资产决定、规则/feedback receipts、catalog adoption、实际命令及 checker identity。legacy v2 报告 migration source identity；无 sidecar 明确为 `legacy-baseline`；style-only 明确未提供 layout/geometry/state structural fidelity。已发布模板 portable 成功且 replay `not-run` 时不得使用 `STRUCTURAL_REPLAY_REQUIRED`，也不得把「请提供本地绝对路径」当作失败原因。无 sidecar 时 layout 不得为 high。仅在本次从源导入的全部 gate 与 Index 成功后，或已发布模板 portable 校验成功后，使用相应“完成”。失败报告必须给出阻断 gate/稳定 issue code；若动过 INDEX 路径，证明 production INDEX before/after digest 相同。

## Portable checker/eval 发现协议

对 validator 和 eval runner 分别执行以下**有序且不模糊**的发现；第一个存在的候选必须通过调用/输出契约，否则失败，不继续尝试同名未知程序：

1. 用户或受控环境显式设置的绝对路径：`UI_TEMPLATE_VALIDATOR` / `UI_TEMPLATE_EVAL_RUNNER`；
1. package validator：`UI_DESIGN_SYSTEM_VALIDATOR` **只能**指向共享实现 `runtime/shared_validate_design_system.py`（或仓库根 `scripts/validate_design_system.py`）。`runtime/validate_design_system.py` 是 discovery wrapper，**不是**实现，禁止写入该环境变量。缺共享实现或 schema 时 `DESIGN_SYSTEM_VALIDATOR_MISSING`；指向 wrapper 时 `VALIDATOR_SELF_INVOCATION`。安装态调用：`python3 runtime/validate_design_system.py validate <candidate-package> --kind package --json`。
2. 本 skill 根目录 `runtime/validate_templates.py` / `runtime/run_contract_evals.py`；
3. 仅当检测到仓库根同时含 `schemas/template/v2/` 时，使用该根的 `scripts/validate_templates.py` / `scripts/run_contract_evals.py`。

禁止从任意 `PATH`、网络下载或另一 checkout 猜测 runner。旧模板 validator 必须接受候选路径、`--index`、`--json`，输出 schema version、findings、contrast counters 与失败退出码；package validator 必须接受 `validate <path> --kind package|active --json`，输出 stable sorted errors/digests 与失败退出码；eval runner 必须接受 skill/case scope 和 JSON 输出，提供 runner version、revision、fixture hash、declared/parsed/executed。候选缺失或能力不满足即 fail closed。bundle 与生产镜像必须把 runtime、共享 design-system validator、schema 和固定 eval resources 一起分发。

## Feedback 状态

Apply 创建 proposed；Authoring 负责 accepted/known-gap/rejected，落盘后 applied，Validate+Eval 后 verified。重复 UUID 或 active fingerprint 合并证据，不重复生成规则；rejected/verified 返回终态 receipt。完整状态机见 [feedback-lifecycle.md](references/feedback-lifecycle.md)。
