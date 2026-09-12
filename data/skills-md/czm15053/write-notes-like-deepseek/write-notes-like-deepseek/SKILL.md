---
name: write-notes-like-deepseek
description: Use when making non-trivial changes, choosing between technical alternatives (A vs B), performing architectural refactoring, investigating past design constraints, writing postmortems for non-obvious bugs, or simplifying/removing dead surfaces. Records, updates, and supersedes architectural decisions and trade-offs in .agents/notes/ while keeping code entry points tied to durable rationale.
---

# Write Notes Like DeepSeek

> 从 DeepSeek Harness 抄来。聊天里的 Agent 负责拆任务、排计划；本 Skill 只做一件事：为什么这样改、放弃了什么、怎么证明改对了，都留在一处，给下一个改这段代码的人用。

## 定位

这不是文档生成器，也不是模板合集。代码和普通文档扛不住的「为什么」和「放弃了什么」，写进仓库，跟这次改动同一批走。下一个改这段代码的人（包括 Agent）先读它。动手前的选型、被否掉的方案——没代码也写。

- **优先就地同步，非必要不新建**：DeepSeek 实践中 80% 的 Note 变更是原地修改现有 Note 的事实（路径、类名、默认参数），而不是开新文件。已有归属的改动直接更新那篇！
- **就近替代顺手归档（Supersession）**：写新 Note 时顺手检索同模块旧 Note。若新方案已彻底取代旧决策，在同次提交中将其 `git mv` 移至 `archived/`（或直接改写原 Note），杜绝新老事实冲突。
- **垃圾不进归档**：过时提案直接转 `Status: rejected — <原因>`（严禁归档）；无防坑价值的被否记录直接物理删除。
- **代码入口反向绑定**：每篇落地 Note 必须在核心代码入口留一行反向注释（`// Note: ... 见 .agents/notes/...`），为下一个接手的 Agent 建立物理索引。
- 只改格式 / 无歧义重命名 / 错别字 / 发布打标（RC/Release tag） → 标 `not applicable`，不写。
- 不确定要不要写 → 按要写处理。
- 别用「以后再补 / 代码即文档 / 改动小」给自己开绿灯。

要不要写，问一句：「以后还有人会问为什么这样改吗？」会，就写。

> 「决定」不重——个人项目里就是「为什么选 A 没选 B」。选型、取舍、踩过的坑，都值得写下。

## 0. 先探测，再落地

别一上来建全套目录。按这个仓库现在的样子选：

1. 有 `AGENTS.md` / `CLAUDE.md` / 贡献指南 → 读它；有 `docs/adr/`、`docs/decisions/`、Issue 模板等现成的决定记录 → 沿用，状态和种类按本 Skill 的文件夹来即可。
2. 没有现成的决定记录 → 建最小笔记树：轻量项目只建 `.agents/notes/implemented/<class>/`，用到 `proposed` / `rejected` / `archived` 再建；空目录可直接删。
3. 团队长期仓库 → 建全套 `proposed / implemented / rejected / archived × 6 class`。

## 1. 路径即分类

每条 Note 的路径就是身份：`{lifecycle}/{class}/yyyy-mm-dd-topic.md`

**Lifecycle（一层文件夹，这篇走到哪一步）：**

- `proposed` — 想法阶段，有了方案但还没落地
- `implemented` — 已落地，与代码同一次提交保持同步
- `rejected` — 审慎否掉的提案，仅当能防止重犯时保留，否则删整组
- `archived` — 已完成且未来参考价值低的 implemented 记录，冻结不可改

**Class（二层文件夹，种类，就这 6 个；再加要改检查脚本）：**

- `feature` 新能力 — 用户或模型看得见的选择（不显然的行为也算）
- `bug-fix` 修缺陷 — 修好了什么，或补上复盘里暴露的缺口
- `simplification` 只删不增 — 不增加能力，只删代码、行为或表面
- `architecture` 结构怎么搭 — 发出去的源码怎么组织、包怎么连
- `process` 工具和流程 — 检查、发布、怎么协作（围着代码转，不是运行时行为）
- `testing` 测试怎么写 — 测试策略和基建

> `refactor` 不单列：能看见的行为变了，归到对应类；没变就是 `simplification`。不建 `INDEX.md`。细判据见 `references/classification.md`。

## 2. 文件格式（检查脚本会核对）

前三行固定：

```markdown
# Agent Note: <标题>

Status: <状态>
```

- `proposed` → `Status: proposed`
- `implemented` → `Status: implemented`
- `rejected` → `Status: rejected — <一句话原因>`

状态必须与所在 lifecycle 文件夹一致；文件名日期是**首次提出日**，状态不带日期。

**Body 骨架：**

- `proposed`：`## Problem` → `## Proposal` → …自由节… → `## Alternatives considered` → `## Acceptance criteria` → `## Risks`
- `implemented`：`## Problem` → `## Decision`（现在时） → …自由节… → `## Alternatives considered` → `## Consequences`
- `rejected`：冻结的 proposal 形态，结论在 `Status:` 行

> 禁止在 `implemented` 中出现 `## Proposal` / `## Plan` / `## Acceptance criteria` 等提案口吻；详见 `references/note-format.md`。
> 每篇 Note 必含 `## Alternatives considered`——没写就重审。
> `implemented` 用现在时描述已落地事实；一条 Note 永远不被改写成另一个决定。

模板见 `templates/`。

## 3. 动手前检索历史决策（去中心化 4 法）

动手重构或选型前，先查历史约束，防止重复踩坑或破坏前人妥协：

1. **入口反向追溯**：阅读模块入口、核心接口或状态机时，优先看顶部的 `// Note: ... 见 .agents/notes/...` 注释。
2. **分类树物理切片**：不扫全库，按意图直切目录（架构看 `implemented/architecture/`，避坑看 `rejected/`）。
3. **精准全局检索**：使用 ripgrep 搜关键词或机制名，**必带 `--hidden` 并排除 `archived/`**：
   ```bash
   rg --hidden --glob '!.agents/notes/archived/**' "<机制名或关键词>" .agents/notes/
   ```
4. **模块文档下钻**：子模块 README 涉及设计依据时，顺着相对 Markdown 链接直达对应 Note。

## 4. 什么时候写、什么时候改

优先查现有归属（Update the owning note）——**绝大多数日常维护是原地更新老 Note 事实，严禁盲目建新篇**：

- 拍板新路线："就选 X"、"决定用 X"、"我们先用 X 顶着" → 触发 Note
- 比较中："X 和 Y 怎么选"、"为什么倾向 X" → 触发备选记录
- 同一段理由被人解释了第二遍 → 该写下来了

**判定与操作流：**

- **既有架构重构 / 路径迁移 / 参数改动** → **【首选原地同步】**：直接在持有该决定的老 Note 里修正事实（代码路径、方法签名、默认值），不另起新篇，也不要在正文追加流水账历史。
- **有新想法、还没动手** → 先写 `proposed`（为什么想这么做、考虑过哪几条路），评审完再动手。交互纪律：一次最多问 3 个问题；落笔前先复述一遍"这是否准确反映了决定"，人点头再写。
- **动手施工完** → 改为 `implemented`，随代码同一次提交（同 PR / commit），并在关键源码入口留反向注释。
- **方案被新决策部分取代** → 新旧两篇都保留，在双方正文添加相对链接互相引用。
- **方案被新决策完全取代（Supersession）** → 新 Note 接管并承接所有仍有价值的旧理由；旧 Note 移入 `archived/` 冻结，并全局检查修复入站相对链接。
- **免写场景**：版本发布打标（RC/Release Tag）、依赖补丁（不改行为）、纯排版格式化 → 直接提交代码，无需 Note。

> 判定与流转见 `references/when-to-write.md`，归档与删除见 `references/archiving.md`。

## 5. 怎么写好

- `## Consequences` 同时写**代价和收益**，不是只写"放弃了什么"。
- 自由节（package 拓扑、wire 契约、schema 等）放在 `Decision` 与 `Alternatives` 之间，保持可检索的机制名与 `must / may / never` 时序强调。
- 跨 Note 引用用相对 Markdown 链接 `[topic](../../implemented/architecture/2026-…-….md)`，不要裸数字，以便机械可校验。
- 实现点在核心入口（优先选公开接口/类型定义、模块顶层导出或核心状态机入口）留一行注释指回这篇：`// Note: 用 SQLite 存会话，为何不用 JSONL — 见 .agents/notes/implemented/feature/2026-08-23-xxx.md`，不逐行标。决定被取代时，这些注释就是要同步的代码清单。
- 文风与去推导痕迹见 `references/prose-checklist.md`；简化机会见 `references/simplification-checklist.md`。
- 写完后过一遍 `references/quality-gate.md` 的语义自检，只向用户报**缺口和写得好的地方**（≤5 行），缺口给具体修法。结构靠脚本，意思靠人点头。

## 6. 校验与运维命令

在仓库根目录直接运行（已配置 npm script 时）：

```sh
npm run verify-agent-note-tree     # 校验目录合法性、分类、文件名及相对 Markdown 链接有效性
npm run verify-agent-note-format   # 校验头块、状态、必选节（Alternatives）与现在时禁令
npm run archive-agent-note <path>  # 方案被取代时一键归档并提示修复入站相对死链
npm run init-board                 # [日常开发] 生成 ~69KB 轻量直连看板 board.html（推荐）
npm run bundle-board               # [脱机打包] 生成内嵌全量数据的自包含演示看板 demo.html
```

若直接通过 tsx 执行脚本（脚本位于当前仓库 `scripts/` 或 `<skill安装目录>/scripts/`）：

```sh
npx tsx scripts/verify-agent-note-tree.ts
npx tsx scripts/verify-agent-note-format.ts
npx tsx scripts/archive-agent-note.ts <note-path>

# 日常开发（轻量直连，推荐）：在工作目录快速生成轻量看板 board.html (仅 ~69KB)
npx tsx scripts/build-board.ts --init [targetPath] [projectName]

# 静态打包（脱机大单体）：生成包含全量内嵌笔记数据的单文件 demo.html (供脱机分发或 GitHub Pages)
npx tsx scripts/build-board.ts --bundle [notesDir] [outputPath] [projectName]
```

### 💡 工程决策看板运行机制 (Agent Notes Board)

**1. 日常开发模式（推荐）：**
- 运行 `npx tsx <skill路径>/scripts/build-board.ts --init board.html "项目决策看板"` 生成约 69KB 的纯模板文件；
- 用浏览器打开后，点击右上角 **「连接本地目录」** 授权选择 `.agents/notes`，浏览器通过 File System Access API 直读本地；
- **零构建、零大单体冗余**：开发或 Agent 增删改 Note 后，只要切回浏览器窗口立刻自动静默热更新！

**2. 离线演示与静态分发模式：**
- 运行 `npx tsx <skill路径>/scripts/build-board.ts --bundle .agents/notes demo.html "项目决策看板"`；
- 脚本会将全部笔记数据编译内嵌为单文件，可直接作为离线 Demo 分发或部署至 GitHub Pages。

**3. 看板四大核心能力：**
- **🏛️ 架构基线**：自动基于入度计算系统承重墙（Core Pillars）、按分类聚合活跃领域事实；
- **⏱️ 演进时间线**：精确日期标牌 + 月份与分类双维正交切片；
- **🛡️ 避坑智库**：检索技术选型中「为什么放弃方案 B」与被否决提案（`rejected`）；
- **📋 决策清单**：全量检索、分类状态快速筛选与即时搜索下拉直达。

每个校验都是独立 tsx 脚本，可串进 `doc-sync` 与 CI 流水线。团队项目可在 `CONTRIBUTING.md` / PR 模板加一句「重要改动必带一篇笔记」，并把上面校验脚本接进 CI。详见 `references/verification.md`。

## References

按需加载：

- `references/note-format.md` — 头块与 body 骨架展开
- `references/classification.md` — 6 class 判定与边界
- `references/when-to-write.md` — 何时新建 / 更新 / 流转
- `references/archiving.md` — 归档与合并删除（含"未来参考价值"判定与新增即审计）
- `references/prose-checklist.md` — 行文与去泄露自检
- `references/simplification-checklist.md` — 简化机会自检
- `references/quality-gate.md` — 写后语义自检：Problem / Alternatives / Consequences / Verification 判定 + 汇报形态
- `references/verification.md` — 校验脚本说明
