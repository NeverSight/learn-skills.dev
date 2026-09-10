---
name: product-prototype-figma
description: |
  用 Figma MCP 生成 B/C 端可编辑 UI 原型。用户说画原型、线框图、Figma 稿、后台页面、App 页面时使用。
  强制嵌入 frontend-design 全流程（design-plan → Anti-Slop → page.ui.yaml → Figma → 截图自审 → 增量 patch），
  配合 DESIGN.md 双轨视觉，避免 AI 默认审美与抽卡式重生成。无 spec 不生成；无 Anti-Slop PASS 不调用 use_figma。
inherits:
  - frontend-design
version: "1.0"
updated: "2026-07-08"
---

# 产品原型生成（Figma）

> 结构靠 `page.ui.yaml`，视觉靠 `DESIGN.md`（B/C 双轨），去 AI 味靠 **frontend-design 流程**。  
> IA 从 brief 推导，**禁止**套用任何「XX 后台标准八页」案例库。

## 启动必读（顺序固定）

1. 本文件 `SKILL.md`
2. `frontend-design` 源规则（来自宿主 Agent / Codex 环境）
3. [DESIGN.md](DESIGN.md)（路由 B/C 视觉轨）
4. [frontend-design-gates.md](references/frontend-design-gates.md)（闸门表）

按需再读：`references/ia-derivation.md`、`references/design-plan-template.md`、`references/anti-slop-checklist.md`、`references/spec-to-figma-map.md`、`references/incremental-edit.md`、`references/page-templates.yaml`。

## 触发条件

- 「画原型」「出线框」「Figma 稿」「UI 图」「页面原型」
- 「做个 XX 后台 / App / 小程序 原型」
- 明确 `@产品原型生成` 或指向本目录

## 前置环境

- Cursor 已装 Figma 插件，`plugin-figma-figma` MCP 已 OAuth
- 生成前调用 `whoami` 取 `planKey`（`create_new_file` 需要）
- 执行 Figma 写入前加载 `figma-use`；整页/多区块组装加载 `figma-generate-design`

## 流水线总览

| Phase | 名称          | 产出               | 闸门                            |
| ----- | ----------- | ---------------- | ----------------------------- |
| 0     | IA 推导       | `ia-draft.md`    | 禁止套模板 IA；须写推导依据               |
| 1     | Design Plan | `design-plan.md` | frontend-design 第一遍           |
| 2     | Anti-Slop   | checklist PASS   | **FAIL 禁止 yaml 与 Figma**      |
| 3     | 结构 Spec     | `*.page.ui.yaml` | `anti_slop: pass` + schema 校验 |
| 4     | Figma 执行    | 云文件 Frames       | 按 region 分批 `use_figma`       |
| 5     | 视觉再审        | screenshot 对照    | 每屏删 1 多余装饰                    |
| 6     | 交付          | 链接 + plan + yaml | —                             |
| 7     | 增量修改        | patch            | 禁止整页重 roll                    |

**全程**：Phase 0→6 可连跑；Phase 2 FAIL 只回 Phase 1 改 plan，不画 Figma。

---

## Phase 0：IA 推导

读 [ia-derivation.md](references/ia-derivation.md)。从 brief 推实体 → 角色 → 任务链 → 页面，输出 [ia-draft.template.md](templates/ia-draft.template.md) 格式。

禁止：

- 读取或引用任何「标准后台页面清单」固定案例
- 用「一般都有工作台/列表/详情」凑页数

用户未反对 IA 草案即可进入 Phase 1；有异议则修订后重进 Phase 1。

---

## Phase 1：Design Plan（frontend-design）

按 [design-plan-template.md](references/design-plan-template.md) 写 `design-plan.md`，必填：

1. Subject（产品、受众、单屏任务）
2. Tone + `surface: b_end | c_end`（路由规则见 [DESIGN.md](DESIGN.md)）
3. Token（色/字/间距/圆角，从 DESIGN 对应轨复制，可微调须说明）
4. Layout（每页 ASCII 线框）
5. Signature（全项目 1 个记忆点，服务当前 brief）
6. Differentiation（相对 AI 默认模板差在哪，一句话）

`b_end` 禁止选 frontend-design 的 extreme 美学；`c_end` 用 `refined-consumer`，仍禁 landing 炫技。

---

## Phase 2：Anti-Slop（frontend-design 第二遍）

逐项勾选 [anti-slop-checklist.md](references/anti-slop-checklist.md)。在 `design-plan.md` 末尾写：

```markdown
## Anti-Slop Review
- surface: b_end | c_end
- 命中项: ...
- 修订: ...
- 结论: PASS | FAIL
```

仅 `PASS` 可进入 Phase 3。把 `anti_slop: pass` 写入各 `page.ui.yaml` 的 `meta`。

---

## Phase 3：page.ui.yaml

- 模板：[page.ui.template.yaml](templates/page.ui.template.yaml)
- 校验：[page.ui.schema.json](schema/page.ui.schema.json)
- 页型约束：[page-templates.yaml](references/page-templates.yaml)

每页一文件，命名 `{page-id}.page.ui.yaml`。`meta.surface` 与 design-plan 一致；`regions` 与 plan ASCII 一一对应。

落盘：

- 项目明确 → 项目 `assets/` 或用户指定目录
- 不明确 → `99-收件箱/待整理/产品原型/{项目名}/`

---

## Phase 4：Figma 执行

读 [spec-to-figma-map.md](references/spec-to-figma-map.md)。

1. 无 `file_key` → `create_new_file`（需 `planKey`）
2. 共享 shell（侧栏/顶栏/TabBar）先画一版，各页引用同一结构模式
3. **按 region 分批** `use_figma`，每批对照 yaml + plan
4. 颜色/字号/间距只来自 `design-plan.md` + DESIGN 对应轨
5. 字体：中文 `PingFang SC` 或 `思源黑体`，数据列 `SF Mono`；**禁止 Inter**
6. 有设计系统 → `search_design_system` 填 `catalog_map`；无则 primitive

---

## Phase 5：视觉再审

每屏 `get_screenshot`：

1. 对照 `design-plan.md` 该页 ASCII
2. **香奈儿法则**：删 1 个多余装饰
3. 仍像 AI 默认 dashboard/App → patch，不整页重 roll

---

## Phase 6：交付

交给用户：

1. **Figma 链接**（主交付）
2. `design-plan.md`
3. `ia-draft.md` + `*.page.ui.yaml`
4. 页面清单表：帧名、职责、根 nodeId（便于 Phase 7）
5. Anti-Slop 结论摘要

---

## Phase 7：增量修改

读 [incremental-edit.md](references/incremental-edit.md)。

- 结构变更 → 改 yaml + patch 对应 node
- 视觉变更 → 先改 design-plan 相关 token → 视情况重跑 Anti-Slop → patch
- **禁止**收到修改意见后无 plan/yaml 更新直接整文件重生成

---

## 红线

- 无 `design-plan.md` → 禁止 Figma
- Anti-Slop 非 PASS → 禁止 Figma
- `meta.anti_slop` 非 `pass` → 禁止 Figma
- 产品复盘 Skill 所需 UI 截图须用户提供，本 Skill 不冒充真机截图
- 不 `git push`、不公开发布

## 与其他 Skill

| Skill | 关系 |
|-------|------|
| `frontend-design` | 继承流程与 Nevers |
| `figma-use` / `figma-generate-design` | Figma 执行层 |
| 产品复盘文档生成 | 复盘截图不由本 Skill 伪造 |

## 文件索引

| 文件 | 用途 |
|------|------|
| [DESIGN.md](DESIGN.md) | B/C 路由 + 摘要 |
| [design-shared.md](references/design-shared.md) | 共用 nevers、a11y |
| [design-b-end.md](references/design-b-end.md) | B 端 token |
| [design-c-end.md](references/design-c-end.md) | C 端 token |
