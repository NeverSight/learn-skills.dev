---
name: spec-product-demo
description: Use when 需要在 sdlc-dev 的产品需求 Spec 流程执行 R4（基于 requirements/prototype.md 生成可交互 Demo 工程），并需要避免跳过 spec-context、在缺少 prototype.md 或缺少可运行 Demo 工程根目录时仍继续、或自创页面/目录导致不可追溯与无法回流闭环。
---

# spec-product-demo（R4：基于原型生成可交互 Demo）

## 概览

R4 的目标是把 `{FEATURE_DIR}/requirements/prototype.md` 的页面清单与交互说明落地为**可运行、可交互**的 Demo，用于走查/验证/对齐：

- **唯一页面来源**：只能来自 `prototype.md/页面/弹窗清单（P-xxx…）`（禁止自创页面）
- **共享工程模式**：默认落到 `{REPO_ROOT}/demo/prototypes/{CURRENT_BRANCH}/`
- **先骨架后细节**：先跑通路由/导航/跳转链路，再补字段/状态/校验/错误处理
- **数据可 Mock**：后端未就绪允许 Mock，但要把“真实数据接入”当作明确替换点

> R4 的核心价值是“把线框变成可点可跑”，不是替代设计稿，也不是在 Demo 里自由发挥新增需求。

## 何时使用 / 不使用

- **使用时机**
  - 已完成 R3，且存在 `{FEATURE_DIR}/requirements/prototype.md`
  - 需要更高保真走查（可用性验证/干系人对齐/研发与测试理解一致性校验）
- **不要用在**
  - `spec-context` 失败 → **立刻停止**
  - `{FEATURE_DIR}/requirements/prototype.md` 缺失 → **停止并回到 R3**
  - 仓库里没有可运行的 Demo 工程根目录，且用户未提供 `DEMO_PROJECT_ROOT` → **停止并要求提供路径**

## 输入 / 输出（落盘约定）

- **硬门禁输入**：`FEATURE_DIR`（必须由 `spec-context` 获取）
- **读取**
  - `{FEATURE_DIR}/requirements/prototype.md`（必读，页面清单/交互说明 SSOT）
- **可选输入**
  - `DEMO_PROJECT_ROOT`：可运行的 Demo 工程根目录（存在 `package.json` 且包含可启动脚本）
- **写入**
  - Demo 代码：默认 `{REPO_ROOT}/demo/prototypes/{CURRENT_BRANCH}/`（共享工程模式）

## 门禁（必须先过，否则停止）

### 1) REQUIRED SUB-SKILL：先执行 `spec-context` 并回显 `FEATURE_DIR=...`

```powershell
. ".\.aisdlc-cli\scirpts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
$CURRENT_BRANCH = $context.CURRENT_BRANCH
$REPO_ROOT = $context.REPO_ROOT
Write-Host "FEATURE_DIR=$FEATURE_DIR"
Write-Host "CURRENT_BRANCH=$CURRENT_BRANCH"
Write-Host "REPO_ROOT=$REPO_ROOT"
```

- `spec-context` 失败 → **停止**
- `{FEATURE_DIR}/requirements/prototype.md` 不存在 → **停止**（不得“先做个占位 Demo”）

> 违反门禁=违反精神：无论“老板 10 分钟后评审/先做出来再补/在 main 上先跑一版”，都禁止跳过上下文与输入文件。

### 2) Demo 工程根目录定位（必须遵守；找不到就停止）

判定“可运行 Demo 工程根目录”的最低标准：

- 目录存在
- 存在 `package.json`
- `package.json` 至少包含可启动脚本（例如 `dev` / `start` / `preview` 其一）

定位规则（从高到低）：

1. **优先使用输入**：用户提供 `DEMO_PROJECT_ROOT` → 以其为准（仍需满足可运行判定）
2. **未提供则自动查找**：
   - `{REPO_ROOT}/demo/`
   - `{REPO_ROOT}/prototype/` 或 `{REPO_ROOT}/prototypes/`
   - `{REPO_ROOT}/apps/demo/`、`{REPO_ROOT}/packages/demo/`
3. **查找失败就停止**：以上路径均不存在或不满足可运行判定 → **停止 R4，并要求用户提供 `DEMO_PROJECT_ROOT`**

**硬禁止**：在“未找到可运行 Demo 工程根目录”时，擅自初始化新的前端工程（Vite/Next.js/CRA 等）来“先跑起来”。这会污染仓库、破坏流程可追溯性。

## 核心流程（从 prototype 到可跑 Demo）

### 0) 输出目录固定：只写到 `prototypes/{CURRENT_BRANCH}/`

在 `DEMO_PROJECT_ROOT` 下为当前需求创建独立命名空间：

- `OUTPUT_DIR = {DEMO_PROJECT_ROOT}/prototypes/{CURRENT_BRANCH}/`

规则：

- **需求实现必须落在 `OUTPUT_DIR`**：页面/组件/样式/Mock/交互逻辑等都写在 `OUTPUT_DIR` 内，避免污染其他需求
- **允许最小粘合改动**：可在 Demo 根工程做最小改动用于“挂载当前需求”（例如路由注册、入口菜单、通用 layout），但禁止修改其他需求的 `prototypes/*` 目录
- 目录名必须精确等于 `CURRENT_BRANCH`（禁止手写或另起别名）

### 1) 从 `prototype.md` 生成页面任务清单（不落盘）

以 `prototype.md/页面/弹窗清单` 为唯一页面来源（SSOT）：

- 每个 `P-xxx` 至少 1 个任务条目（可再细分）
- 每个条目必须包含：
  - 页面路由/入口、页面目标
  - 主要控件/字段与默认值
  - 关键状态（正常/加载/空/错误/无权限）与提示文案要点
  - 与任务流节点（T-xxx）及 AC 的映射（引用 `prototype.md` 位置）

**禁止**：为“看起来更完整”而新增登录页/设置页/通用布局页等未在 `prototype.md` 声明的页面。需要新增页面 → 回流 R3 更新 `prototype.md` 后再做 R4。

### 2) 先搭骨架（必须先跑通）

先完成：

- 所有页面/弹窗的路由或入口占位
- 导航入口与关键跳转链路（至少覆盖核心任务流主链路）

此阶段允许：

- 仅用静态/Mock 数据渲染
- 仅实现关键按钮与跳转（字段/校验可后补）

### 3) 再补细节（按优先级）

按“核心主链路优先”补齐：

- 字段与校验（含错误提示要点）
- 状态与异常分支（加载/空/失败/无权限）
- 交互细节（取消/返回/二次确认/恢复路径）

数据依赖未就绪时：

- 用 Mock 数据/Mock API 让交互可跑
- 把“真实数据接入”作为明确替换点（避免把 Mock 当最终实现）

### 4) 运行与冒烟（完成检查）

最小完成标准（缺一不可）：

- Demo 工程可启动
- 可导航到 `OUTPUT_DIR` 的页面集合
- 关键链路可走通（至少覆盖 `prototype.md` 的核心任务流主链路）

## Quick reference（高频规则速查）

- **必须**
  - 先跑 `spec-context`，只用其输出的 `FEATURE_DIR/CURRENT_BRANCH/REPO_ROOT`
  - 必须存在 `{FEATURE_DIR}/requirements/prototype.md`
  - 页面清单只来自 `prototype.md`（不加页）
  - Demo 根目录找不到/不可运行 → 立即停止并要求 `DEMO_PROJECT_ROOT`
  - 需求实现写在 `{DEMO_PROJECT_ROOT}/prototypes/{CURRENT_BRANCH}/`；Demo 根工程只做最小粘合改动（路由/入口）
- **禁止**
  - 在 main（或非 `{num}-{short-name}` 分支）上硬做 R4
  - 用“先做占位 Demo”替代缺失的 `prototype.md`
  - 未找到 Demo 工程根目录时擅自 `npm create vite@latest` / `npx create-next-app` 初始化新工程
  - 自创页面/路由并声称“demo 常见”

## 红旗清单（出现任一条：停止并纠正）

- 没跑 `spec-context` 就开始找/写 `requirements/*.md` 或 demo 目录
- `{FEATURE_DIR}/requirements/prototype.md` 不存在，却仍要继续
- Demo 根目录不存在/不可运行，却仍要“先初始化一个 Vite 工程”
- 在 Demo 里新增 `prototype.md` 未定义的页面（登录/设置/随便加页）
- 输出目录不是 `prototypes/{CURRENT_BRANCH}`（写到根目录、写错分支名、或写到别的需求目录）

## 常见借口与反制（基线测试中的高频点）

| 借口（压力来源） | 常见违规行为 | 必须的反制动作 |
|---|---|---|
| “老板 10 分钟后要看，先在 main 上做一版” | 跳过 `spec-context`；在 main 上写 demo | **门禁不过就停止**：先切到合法 spec 分支并跑 `spec-context`；否则只能交付“阻断原因 + 需要的输入/下一步” |
| “prototype 还没写/找不到，就先做个占位 Demo” | 自创页面与流程，导致不可追溯 | `prototype.md` 缺失 → **回到 R3**；R4 禁止替代 R3 的交互决策 |
| “仓库里没有 demo/，我先初始化一个 Vite/Next.js 工程” | 在未知位置创建新工程污染仓库 | **停止并要求 `DEMO_PROJECT_ROOT`**；只有在已存在可运行 demo 工程时才允许继续 |
| “顺便加登录页/设置页，demo 常见” | 自创页面，偏离 SSOT | **拒绝加页并回流 R3**：先把页面写进 `prototype.md` 的页面清单（含编号、说明、AC 映射） |

## 一个好例子（找不到 Demo 根目录时如何正确停止）

当未提供 `DEMO_PROJECT_ROOT` 且自动查找失败时，应当输出类似结论：

- 阻断原因：当前仓库未发现可运行的 Demo 工程根目录（缺 `demo/` 或缺 `package.json`/启动脚本）
- 需要用户提供：`DEMO_PROJECT_ROOT`（例如 `E:\\path\\to\\demo`），并说明其必须可启动
- 下一步：拿到 `DEMO_PROJECT_ROOT` 后，在 `{DEMO_PROJECT_ROOT}/prototypes/{CURRENT_BRANCH}/` 生成 Demo

