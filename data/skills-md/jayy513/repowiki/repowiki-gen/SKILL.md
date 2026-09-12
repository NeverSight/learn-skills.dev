---
name: repowiki-gen
description: >
  从代码库生成/更新项目 wiki。触发词：生成 repowiki、刷新 repowiki、
  整库生成 wiki、检查 repowiki 状态。
---

# repowiki-gen: Repo Wiki Generator

## 概述

自动从项目代码库分析模块结构，产出两族 OKF bundle（`docs/repowiki/`）：`knowledge/` 模块知识卡（五维默认卡 + 自定义维度卡）+ `content/` 文章树，供任意支持 `.agents` 标准的 agent 读取。写作体系对齐 Qoder 产物（五维知识卡基线与开放 category / 五类文章 / cite 引注 / 图表来源）。

## 流水线（Step 0 接线 + 7 步生成）

| 步 | 阶段 | 执行者 | 产出 |
|---|---|---|---|
| 0 | **wire** | `repowiki init`（幂等，每次运行先执行） | `AGENTS.md` 注入 `## repowiki` 分区 + 纪律句 + state 基线 |
| 1 | **scan** | `repowiki scan` | `.repowiki/snapshot.json` + 规模统计 |
| 2 | **budget** | agent（轻量评估） | 规模档位 + 文章 caps |
| 3 | **plan** | agent | 模块划分 + 知识卡 + 文章大纲 → `.repowiki/plan.json`（v2） |
| 4 | **generate** | agent（分批） | 4a 逐模块知识卡 → `knowledge/`；4b 自底向上文章 → `content/` |
| 5 | **link** | agent（轻量） | 卡片导航、父→子文章、index 清单、可达性 |
| 6 | **validate** | `repowiki validate` | OKF 校验报告（含可达性与 plan 一致性） |
| 7 | **finalize** | `repowiki state --update` | `state.json` + `log.md` + 完成报告 |

### 步骤详述

#### Step 0: wire（接线，自动）

运行 `repowiki init`（幂等，已接线时为 no-op）：

- 建 `.repowiki/state.json` 基线（若缺失）
- 向项目根 `AGENTS.md` 注入 `## repowiki` 分区声明 + 读取纪律（HTML 注释管理块）
- 检测到手写 `## repowiki` 分区 → 仅在缺失时补充 `- docs/repowiki/` 声明行（其余内容逐字保留）

每次运行本技能都先执行此步，确保读取端能发现声明——遗漏接线会使 `docs/repowiki/` 对 agent 不可见。

#### Step 1: scan

运行 `repowiki scan` 生成仓库快照。默认排除 vendor/node_modules/dist/build/target/__pycache__/.venv/.env 等目录、密钥类文件（.env\*/SSH 密钥/\*.key/\*.pem 等）、以及超大文件（>1MB）。尊重 `.gitignore` 与可选 `.repowikiignore`。

输出到 `.repowiki/snapshot.json`，包含所有源文件的路径、SHA256 hash、大小与语言分类。

#### Step 2: budget

agent 基于 scan 输出的规模统计（文件数、语言分布、目录结构深度），判定仓库规模档位，并取出该档位的文章 caps：

| 档位 | 条件 | MaxTotalModules | MaxDepth | max_total_articles | max_top_articles | max_sub_per_parent | max_article_words |
|---|---|---|---|---|---|---|---|
| 扁平单层 | <50 个源文件，单层结构 | 2 | 1 | 6 | 3 | 3 | 1500 |
| 模块树 | 50-500 个源文件，多层目录 | 8 | 2 | 30 | 8 | 5 | 2500 |
| 深度限制 | >500 个源文件或复杂多模块 | 20 | 3 | 60 | 10 | 7 | 3000 |

参考框架：`references/pipeline.md` 的 budget 评估与大纲规划规则。

#### Step 3: plan

agent 产出 `.repowiki/plan.json`（v2）：

```json
{
  "schema": 2,
  "budget": { "tier": "模块树", "max_total_articles": 30, "max_top_articles": 8, "max_sub_per_parent": 5, "max_article_words": 2500 },
  "modules": [
    { "slug": "payment", "title": "支付模块", "dir": "支付模块", "scope": ["src/payment/**"] }
  ],
  "articles": [
    { "slug": "overview", "title": "项目总览", "file": "content/项目总览.md", "type": "overview", "modules": ["payment", "auth"] },
    { "slug": "payment-domain", "title": "支付域", "file": "content/支付域/支付域.md", "type": "domain", "modules": ["payment"] },
    { "slug": "payment-flow", "title": "支付流程", "file": "content/支付域/支付流程.md", "type": "deep_dive", "modules": ["payment"], "parent": "payment-domain", "scope": ["README.md"] }
  ],
  "coverage_check": { "covered_files": 45, "total_files": 48, "uncovered": ["src/vendor/legacy.js"] }
}
```

字段约定：

- `modules[]`：`slug`（ascii 全局唯一）+ `title`（显示名，跟随项目语言）+ `dir`（`knowledge/` 下的目录名，规范化自 title）+ `scope`（源文件 glob）。
- `articles[]`：`slug` + `title` + `file`（bundle 相对路径，规范化自 title）+ `type`（五类之一）+ `modules`（**非空**，覆盖的模块 slug；overview 类为全部模块）+ `parent`（可选，父文章 slug）+ `scope`（可选，额外源 glob，如 README）。
- `budget`：Step 2 的档位与 caps，落盘备查。

**大纲规划规则**：

- 类型决策：overview（项目级总览，1 篇）；getting_started（上手，1 篇）；domain（功能域聚合，可含子文章）；deep_dive（单域深入，叶子）；developer_guide（开发流程，叶子）。
- 按功能聚合模块，**禁止**一模块一文章、禁止按层命名（"Controllers"、"Repositories"）。
- 每个模块必须至少出现在一篇文章的 `modules` 中（跨递归层级）。
- caps 收敛：顶层超 `max_top_articles` → 按模块文件数排序，溢出合并到兄弟文章；总数超 `max_total_articles` → 同理合并。
- 拆父判据：子树 ≥4 个模块 且 ≥3 个子域 且 预估内容超 `max_article_words` → 可拆子文章；叶子类型（getting_started / developer_guide / deep_dive）不得作父。
- 稳定性：增量更新时保留既有大纲（slug 与 file 路径不变），只在模块变更处增删。

覆盖率自查：所有源文件至少被一个模块的 scope 覆盖；未覆盖文件在 `coverage_check.uncovered` 中列出。

### 来源目录纪律（语义过滤）

plan 阶段只对项目的**源码主干**做模块拆分。以下内容即使未被机械过滤（非二进制、不在排除目录），也**不应作为独立模块的 scope**：

- 构建产物目录：`bin/`、`obj/`、`dist/`、`build/`、`out/`
- 测试数据 / 夹具：`testdata/`、`fixtures/`、`mocks/`
- CI/CD 配置：`.github/`、`.gitlab/`、`.circleci/`
- 国际化 / 本地化数据：`locales/`、`i18n/`、`translations/`
- 生成代码（已知模式）：`*.pb.go`、`*.generated.*`、`openapi/`、`graphql/generated/`

判断：如果一个目录中大部分文件属于以上类别，跳过该目录，不纳入任何模块 scope。未覆盖文件留在 `uncovered` 列表中即可，不要求 100% 覆盖率。

#### Step 4: generate

**4a 知识卡（逐模块一批）**

1. 读取模块内关键文件（入口、类型定义、配置、README）
2. 五维知识字段 → 映射到五卡：

| 五维字段 | 目标卡（dimension） |
|---|---|
| name + 职责边界 | 概述（overview） |
| architecture_design + 依赖 | 架构设计（architecture） |
| tech_stack | 技术栈（tech_stack，仅非默认选型） |
| coding_conventions | 编码规范（coding_conventions，≤6 条、≥2 处验证） |
| unique_setup_and_commands | 特殊配置与命令（setup，仅非显而易见） |

3. **自定义维度评估**（开放分类扩展机制）：五维映射后，检查模块是否存在五维无法承载、且对任务意图有高命中率的知识主题——典型如数据模型、协议契约、错误语义、依赖治理、故障排查。命中则增建自定义分类卡：
   - 文件名 = **语义化标题**（跟随项目文档语言，如 `依赖治理.md`），不再是维度名；`dimension` 用自定义 ascii 值（如 `dependency_management`），语义稳定、同 bundle 内不冲突
   - frontmatter 规则与五维卡相同（dimension + 维度级 triggers + description）
   - 每模块 ≤2 张，宁缺毋滥；无真实信号则不建
4. 写入 `docs/repowiki/knowledge/<dir>/<卡名>.md`（完整 frontmatter：`dimension` + **维度级 triggers**——“怎么跑”→特殊配置与命令、“选型”→技术栈、“规范”→编码规范）
5. `概述.md` 必须含卡片导航（链接同目录其他卡，**含自定义卡**）

**4b 文章（自底向上）**

1. 按 `articles[].parent` 拓扑排序（先子后父）
2. 每篇输出 `summary` + `key_topics`，写入 `.repowiki/run.json`（供父文章合成与续跑）
3. 父文章写作时读取直接子文章的 `summary` / `key_topics` 做综述合成与交叉引用
4. 按 `references/output-spec.md` §4 写作契约写 `content/` 文件；字数 ≤ `max_article_words`（+10% 硬顶）
5. 引注用 `file://` + 行号锚；Mermaid 图后附图表来源

**增量模式**（已有产物时）

1. 运行 `repowiki status --json` → 取 `affected_pages`
2. 重生成范围 = 受影响模块的全部卡 + `modules` 命中这些模块的文章 + 这些文章的祖先文章（summary 传播）
3. 祖先文章仅重写综述段落与 `## 更新摘要`；无受影响页时跳过 4a/4b

每完成一批写入 `.repowiki/run.json`（已写页面清单 + 文章 summary），支持断点续跑。

生成前按 D4 规则比对既有页面 `content_hash`（对两族全部受管页面适用）：
- hash 一致 → 正常重生成
- hash 不一致且不在 `run.json` 已写清单中 → 判定人工修改，默认跳过
- `protected: true` 显式锁定的页面永久跳过

#### Step 5: link

agent 补全并自查链接（bundle 相对路径）：

- 概述卡 → 同目录其他卡的卡片导航
- 父文章 → 直接子文章
- `index.md` → 每个模块的概述卡 + 每篇顶层文章
- 全文可达性：除 index.md 与 log.md 外，所有页面可从 index.md 到达

#### Step 6: validate

运行 `repowiki validate` 校验 OKF bundle：

- frontmatter 必填字段（status/type/triggers/description；知识卡另需 `dimension`）
- type 值域按族（`knowledge/` → module；`content/` → 五类）
- status 值域（stable|draft|deprecated）
- 根 index.md 仅允许 okf_version/description
- 知识模块目录锚（存在 `dimension: overview` 的卡）
- bundle 内相对链接可达（锚点与百分号编码已归一；代码块与行内示例链接跳过）
- 链接可达性：所有页面可从 index.md 到达
- plan.json（v2）一致性：计划文章文件与模块目录存在
- log.md 豁免 frontmatter 检查

不合格项回炉修正（P0 只报不修，agent 根据报告手动修正）。

#### Step 7: finalize

运行 `repowiki state --update` 写入 / 刷新 `state.json`（CLI 已实现）：

- 当前 git commit/branch（供 `status` 做新鲜度基线）
- 扫描 `docs/repowiki/` 全部页面，写入 `pages`：每页 `content_hash`；若存在 `.repowiki/plan.json`（v2），按模块 `scope` 与 `articles[].modules` 填 `sources`
- `snapshot_digest`（来自 `snapshot.json`）
- `last_run`（phase=`finalize`，status=`success`）；若有 `.repowiki/run.json` 则读取其 `started_at`，成功后删除 `run.json`

写出 `log.md`（生成日志：日期、模式、提交、范围、validate 结果）。

输出完成报告：页面数、覆盖率（若 plan 含 coverage_check）、提交信息。

## 质量门

### 人工修改保护

- 所有受管页面记录 `content_hash`（知识卡与文章同规则）
- 生成前逐页比对；hash 不一致的页面默认跳过
- 报告跳过的页面供用户确认
- `protected: true` 显式锁定（`--force` 可覆盖）

### 上下文防爆

- 一次只处理一个模块批次
- 批次间清理上下文
- 单模块源文件过多 → 优先读入口文件、类型定义、配置，抽样读实现

### 并发互斥

- 启动时写入 `run.json`（含 pid、phase）
- 检测到存活 pid 的运行即拒绝启动
- finalize 成功后删除 `run.json`

### 断点续跑

- 每批完成后写入 `run.json`（已写页面清单 + 文章 summary）
- 崩溃重跑时跳过已完成模块
- 崩溃遗留页面不触发人工保护

### 语言

- 正文与文件名/目录名默认跟随项目文档语言
- 可由 `.repowiki/config.json` 的 `language` 字段覆盖
- `slug` 保持 ascii 机器身份（不进入文件名与链接）

## 参考

- [输出规格](references/output-spec.md) — 目录组织、frontmatter、知识卡与文章原型、命名与链接纪律
- [流水线参考](references/pipeline.md) — 各阶段详细指引与提示词思路
