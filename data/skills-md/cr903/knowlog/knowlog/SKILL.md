---
name: knowlog
description: 知录（knowlog）—— 为一项目建立或维护「开发文档体系」——任务日志(daily)、结构化知识库(knowledge)、领域上下文(domain context)、两级索引(分端+根)、关键词召回(.keyword-map)与 AGENTS.md 约束注入；并让 agent 在任务收尾时自动记录日志、沉淀知识、跑索引门禁。当用户要给新项目/新仓库搭文档体系、规范开发日志、建知识库、整理 docs 目录、注入 AGENTS.md/CLAUDE.md 上下文约束，或说"这个任务做完了帮我记一下日志""沉淀一下这次的坑""把这次改动记进知识库""文档太乱了帮我整理""索引对不上"时使用。也用于体检/修复已有体系（索引缺失、死链、日志散落、路径不规范）。Use this skill whenever the user wants to set up or maintain a project documentation system (dev logs / knowledge base / domain context / doc indexes / keyword-based context recall), record a work log after finishing a task, or distill lessons into a knowledge base.
---

# knowlog — 项目的文档体系（记忆 + 约束 + 召回）

## 这套体系解决什么

agent 的上下文会被压缩、会丢；**文件不会**。所以约定：凡是"下个会话还需要知道"的东西，都必须落到文件里，
并且**能被找到**（索引 / 关键词）、**能被信任**（有判据、有来源）。

三个失败模式是这套体系的全部动机：

| 失败模式 | 后果 | 对应机制 |
|----------|------|----------|
| 上下文丢了，只能翻聊天记录 | 每次重开会话都要重新摸索 | **日志**：一任务一篇，索引可查 |
| 同一个坑踩第二次、第三次 | 重复浪费，且每次都像第一次 | **知识库**：可复用结论沉淀 + 关键词召回 |
| agent 不懂业务却写得很像真的 | 代码能跑、测试能过，业务是错的 | **领域上下文**：路由到领域文档，动手前全量读 |

再叠一层**约束**：把"必须做什么"写进 `AGENTS.md`（各大 agent 都会读根 AGENTS.md），
把"做得对不对"变成**脚本退出码**（`check-daily-index.sh --strict`）。约定靠自觉会烂，靠门禁不会。

设计细节与"每条规则为什么这样定"见 `references/memory-and-constraints.md`（遇到要改动体系本身、或用户质疑某条规则时读它）。

## 先决定两件事

**① 知识库布局（flat 还是 by-end）** —— 决定知识放几层目录：

| 布局 | 长什么样 | 什么时候用 |
|------|----------|-----------|
| `flat` | `docs/knowledge/{architecture,guides,troubleshooting,best-practices}/` | **单面项目**（一个后端服务、一个 CLI、一个数据管道）：没有技术栈明显不同的多个部分 |
| `by-end` | `docs/knowledge/<端>/{四个分类}/` | **多端项目**（Go 后端 + 前端 SPA + 移动端）：知识基本不通用，混在一起会互相淹没 |

`--knowledge-layout auto`（默认）会按探测到的端数量决定：≥2 个端 → by-end，否则 flat。
判断标准不是"仓库里有几个语言"，而是**知识会不会被复用**：真的是同一套约定就 flat，别硬造端层。
两种布局都能随时切换（bootstrap 幂等，不覆盖已有文件；`new-knowledge.sh` 用 `<端>` 或 `--flat` 区分）。

**② 项目里是不是已经有文档了**：

- 全新项目 → 直接 `bootstrap-docs.sh`
- **已有异构文档**（`docs/logs/2026-08-01-x.md`、根目录 `daily/`、中文按日流水…）→ **先 `adopt-docs.sh` 再 bootstrap**，
  否则会造出两套并行结构（两份真相）。见下方「采纳既有文档」。

## 两种使用方式

**A. 给新项目搭建**（用户说"建文档体系""搭 docs""规范日志"）：

> 装了 CLI 的话，最省事的是 `npx knowlog init --agent auto`
> （= 建结构 + 装脚本 + 写托管块 + 装召回 + 自检；没有 npx 就用 `node ~/.agents/skills/knowlog/bin/knowlog.mjs init --agent auto`）；
> 没装 CLI 就直接调脚本（下同）。



```bash
# 1) 先跟用户确认三件事（别自己拍）：
#    ① 端（end）怎么分 —— 你探测出的是 backend/frontend，对不对？多仓 monorepo 要不要按子仓分？
#    ② 要不要装 Claude Code 召回钩子（--with-hook）
#    ③ 项目名（写进索引与 AGENTS.md 块）
bash .knowlog/bootstrap-docs.sh --project-name "我的项目" [--ends "backend frontend"] \
    [--knowledge-layout auto|flat|by-end] [--with-recall] [--dry-run]

# 2) 幂等：可重复跑；已存在的文件一律不覆盖；AGENTS.md 只在托管块标记之间写入
# 3) 跑完自检必须两个门禁都绿：
#    bash .knowlog/check-daily-index.sh --strict        # 日志 ↔ 索引
#    bash .knowlog/check-knowledge-index.sh --strict    # 知识 ↔ 索引（含 by-end 两级）
# 4) 召回要落到具体 agent 才生效：bash .knowlog/install-recall.sh --list 然后 --agent auto
```

搭建完成后，把结果讲给用户听**结构长什么样、以后每次收尾怎么用**（不要只说"建好了"），
并主动做一次演示：建一篇真实日志（哪怕内容还空着），让他看到索引行长什么样。

**B. 任务收尾记录**（用户说"做完了""记一下日志""沉淀一下"）：

```bash
bash .knowlog/new-daily-log.sh <slug> [YYYY-MM-DD]     # 落月份目录 + 插索引行骨架
# 然后由你（agent）把日志内容写实：概述 / 关键实现 / 问题与根因 / 判据 / 沉淀
bash .knowlog/new-knowledge.sh <端> <分类> <name> "<一句话说明>" --source "<日志路径>"   # 若这次有可复用结论
bash .knowlog/check-daily-index.sh --strict           # 门禁：红灯不许收摊
```

**沉淀会自动挂召回规则**（默认从「来源日志里的代码标识符」提取，最多 3 条）。
你（agent）比脚本更清楚哪个标识符是"写码当下会出现的"，所以**优先显式传**：

```bash
bash .knowlog/new-knowledge.sh --flat troubleshooting tenant-isolation "多租户查询必须带 tenantId" \
  --source docs/daily/2026-10/2026-10-20_xxx.md --keywords "tenantId,tenant_id"
```

- `--no-keyword`：明确这条知识不需要召回（纯流程/手册），会记入 `_exempt`，门禁不因此变红。
- 一条规则都没有、却已有知识文档时，结构门禁**会红**（防止召回永远空转）。
- 存量知识缺规则：`bash .knowlog/reindex-knowledge.sh --apply`（先不带 `--apply` 看候选）。

填日志时注意：**不要复述 diff**。要写"为什么这么做""踩了什么坑""怎么证明它是对的"。
判断是否沉淀知识的标准是**这条结论会不会被重复踩/被反复问**；一次性细节留在日志里就够。

## 采纳既有文档（项目已经有 docs，但结构不一样）

```bash
bash .knowlog/adopt-docs.sh              # 默认 dry-run：扫描 + 打印迁移计划（不动文件）
bash .knowlog/adopt-docs.sh --apply      # 执行：按文件名日期归入 docs/daily/<YYYY-MM>/，并登记索引
bash .knowlog/bootstrap-docs.sh          # 再补齐缺失的结构与脚本
bash .knowlog/check-daily-index.sh --strict
```

要点：

- **只采纳"像日志"的文件**：文件名以日期开头（`2026-08-01-x.md`、`2026-08-03_中文标题.md` 都行）；
  `README/AGENTS/CHANGELOG` 与非日期文件**不动**
- **已有 `docs/knowledge/`、`docs/domain context/` 原样保留**，只补它们缺的分类目录与索引；
  知识文档已有但索引只登记了一部分 → 用 `bash .knowlog/reindex-knowledge.sh --apply` 从磁盘反向补齐（只增不删）
- 迁移前自动备份 `docs/index.md.bak`；优先 `git mv`（保历史），非 git 项目退化为 `mv`
- 目标文件名规范化为 `<日期>_<kebab-slug>`（纯中文标题保留以保可读性，门禁允许）
- 采纳后**必跑门禁**；历史月份若故意不登记，先用 `LEGACY_MONTHS="2026-04 2026-05"` 降级为告警

若用户明确"不要动我的文件"：只跑 bootstrap（它会跳过已存在的一切），并如实告知
"这些日志不在索引覆盖范围内，门禁管不到它们" —— 不要假装已经纳入。

## 让召回落到具体 agent（这一步常常被忘）

**匹配逻辑只有一份**（`.knowlog/recall-core.py`），各 agent 的适配器只是"怎么把它送进上下文"：

```bash
bash .knowlog/install-recall.sh --list          # 看本机检测到哪些 agent、各自会写什么（不落盘）
bash .knowlog/install-recall.sh --agent auto --dry-run   # 先看计划
bash .knowlog/install-recall.sh --agent auto    # 确认后再装（幂等）
```

**装之前先问用户**（同 bootstrap 的三问）：往 `.claude/settings.json`、`.codex/hooks.json`、
`opencode.json` 这些**属于用户的配置**里写条目，属于"改别人的环境"。默认策略：
`--list`/`--dry-run` 可以直接跑；真正落盘前给出清单并等一句确认。Codex 那条还要额外说明
"需你之后在交互式会话里批准一次信任，否则钩子不执行"。

| agent | 机制 | 验证状态（本仓实测） |
|-------|------|----------------------|
| Claude Code | `.claude/settings.json` 的 `UserPromptSubmit` 钩子 | ✅ **端到端**：`claude -p` 让模型复述注入块，逐字命中 |
| Codex | `.codex/hooks.json` 的 `UserPromptSubmit`（同 JSON 契约） | ⚠️ 钩子本体 ✅；**真机需人在交互会话里一次性信任**（`~/.codex/config.toml` 的 `hooks.state.*.trusted_hash`），未信任则静默不跑 |
| OpenCode v2 | 项目 `opencode.json` 的 `instructions`（每会话必读） | ✅ **端到端**：`opencode run` 复述探针字符串命中 |
| OpenCode v1 | `.opencode/plugins/*.ts` 的 `chat.message`（每轮关键词召回） | 契约来自 v1 API；v2 装了不报错也不触发，故默认不装（`DOCS_RECALL_OPENCODE_V1_PLUGIN=1` 可强制） |
| Cursor / Gemini / Copilot | `.cursor/rules/*.mdc` / `GEMINI.md` / `.github/copilot-instructions.md` | 文件级（指针，不复制规则） |
| DSH | `agent/pre-step` waterfall：插件把召回结果当一条带来源的 `UserMessage` 追进本轮进入批次 | ✅ **机制已定位并落地**（读官方 d.ts 契约 + 4 处真实实现，含用户已装的 `dsh-mnemon`）；`bash adapters/dsh/verify.sh` 6 项全绿 + `bridge/selftest.mjs` 16 条断言；⚠️ 真实会话端到端需你把自己 profile 的那一行 patch 加上（脚本不改宿主配置） |
| 其它（Aider/Cline/Roo/Qwen/iFlow/Antigravity/Kilo/Windsurf/Devin/Amp…） | 无可靠每轮机制 → 靠 `AGENTS.md` 托管块 + `knowledge-retrieve.sh` | ✅ 命令行路径与有钩子的 agent 同源 |

**关键取舍**：宁可"静态规则 + 命令行召回"也不装"看起来能自动但实际不触发"的适配器 ——
后者会让人以为有保护，实则没有（OpenCode v2 的 v1 插件就是这种陷阱）。
任何 agent 都能用的底线是 `AGENTS.md` 托管块 + `bash .knowlog/knowledge-retrieve.sh "<prompt>"`。

## 关键不变量（改动体系时不能破）

1. **路径是日期的纯函数**：`docs/daily/<YYYY-MM>/YYYY-MM-DD_<slug>.md`，月份取日志日期所在月。
   因此没有"事后归档"这一步，也永远不需要回改索引链接。
2. **三处月份一致**：目录月 == 文件名月 == `docs/index.md` 所在表格月。脚本会校验。
3. **索引双向一致**：每篇日志在 `docs/index.md` 有且仅有一行；每条链接都指向真实文件。
4. **知识登记到索引**：by-end 布局是"分端 `index.md` + 根 `index.md`"两级；flat 布局只有根 `docs/knowledge/index.md`。
   两种都由 `bash .knowlog/check-knowledge-index.sh --strict` 校验。
5. **索引写入只有一份实现**：`.knowlog/index-util.py`（`new-daily-log.sh` 与 `adopt-docs.sh` 都调它）——
   索引格式一漂移，门禁就会误报，人就开始绕过门禁。
6. **召回是非全量的**：关键词命中只给"提示 + 文档路径"，确认相关再全量读那份文档。
   全量注入会让真正相关的规则被淹没，且上下文预算很贵。
7. **`AGENTS.md` 托管块**：`<!-- KNOWLOG:START -->` 与 `END` 之间由脚本生成；
   用户/AI 的手工内容放在块外，脚本不碰。不要在别处复制出第二份真相。

## 脚本速查

| 脚本 | 何时用 | 关键行为 |
|------|--------|----------|
| `bootstrap-docs.sh` | 搭新体系 / 补建缺失部分 | 幂等（可 `shasum` 对拍）、不覆盖、注入托管块+新建手工区、把 assets/脚本复制进项目（自包含） |
| `adopt-docs.sh [--apply]` | 项目已有异构文档 | 默认 dry-run 出计划；`--apply` 按文件名日期归月 + 登记索引 + 备份索引 |
| `reindex-knowledge.sh [--apply]` | 老项目知识库"文档多、索引少" | 从磁盘**反向补齐**索引行（只增不删、幂等）；本仓实测一次补 60 行 |
| `install-recall.sh --agent auto` | 让召回落到具体 agent | 按检测到的 agent 写适配器（钩子/插件/规则文件），幂等；`--verify` 自测 |
| `check-knowledge-index.sh --strict` | 知识库体检 | 知识文档 ↔ 索引（两级/flat 自适应）；抓"文档没登记/死链/根索引漏登记" |
| `check-docs-structure.sh --strict` | **结构规范自检** | 目录/脚本齐备、布局不变量（flat/by-end 混用）、托管块、召回表可用性、未采纳残留 |
| `docs-doctor.sh [--strict] [--quiet]` | **体检总入口**（推荐） | 串起上面三个 checker + 汇总；失败时给"常见修法速查"；`--quiet` 适合 pre-commit |
| `install-skill.sh --agent auto` | 把 skill **本体**装到各 agent | `--mode auto|link|copy`（auto：有 `~/.agents/skills` 就"权威副本+软链"）；`--check` 对比版本 |
| `package-skill.sh [--out DIR]` | 打包分发单元 .skill | 纯 zip，不依赖任何第三方打包工具；默认 `~/.agents/skills/.packages/` |
| `bin/knowlog.mjs`（零依赖 CLI） | 给人用的统一入口 | `npx knowlog init\|log(add)\|doctor\|knowledge\|adopt\|reindex\|install-skill\|package`；内部转发同一批脚本 |
| `new-daily-log.sh <slug> [日期]` | 每次任务收尾 | 自动算月份目录、复制模板、**在 index.md 插入索引行骨架** |
| `new-knowledge.sh <端> <分类> <name> "<说明>" --source <日志> [--keywords "a,b"]` | 有可复用结论时 | 复制知识模板 + **更新两级索引 + 自动挂召回规则**（`--no-keyword` 记豁免） |
| `new-keyword.sh "<正则>" "<提示>" "<文档>"` | 手工补规则（沉淀时已自动挂） | 往 `.keyword-map.json` 追加召回规则（正则要命中标识符；文档路径可写相对 docs/ 或项目根，会自动归一化） |
| `knowledge-retrieve.sh "<prompt 或 diff>"` | 写码前 / 排查前 | 关键词召回：给提示 + 文档路径（非全量） |
| `check-daily-index.sh [--strict] [--fix-hint]` | 提交前 / 收尾前 / 体检 | 双向一致 + 路径格式 + 三处月份；`--fix-hint` 给可执行的修复命令 |
| `recall-core.py` / `index-util.py` | 被上面的脚本调用 | 召回匹配与索引写入的**唯一实现**（适配器/脚本都调它们，别另写一份） |

其它 agent 没有钩子机制时，`knowledge-retrieve.sh` 就是等价入口（Claude Code 可用 `inject-knowledge.py` 挂 `UserPromptSubmit`）。

## 体检与修复现有体系

**先跑总入口**（一次跑完全部三项，并给出可复制的修复命令）：

```bash
bash .knowlog/docs-doctor.sh --fix-hint          # 结构 + 日志索引 + 知识索引
bash .knowlog/docs-doctor.sh --strict            # 告警也算失败，接 CI / pre-commit 用这个
bash .knowlog/docs-doctor.sh --quiet             # 只输出汇总（pre-commit 场景）
```

三项的分工：**结构规范**（目录/脚本齐备、布局没混用、托管块在、召回表可用、有没有该采纳却没采纳的旧日志）、
**日志↔索引**、**知识↔索引**。单跑一个绿灯不代表健康 —— 结构跑偏时索引照样"一致"。

最常见的四类偏差与修法（`references/maintenance.md` 有更细的配方）：

| 报告 | 处理 |
|------|------|
| 日志散落在 `daily/` 根 | 按文件名月份 `git mv` 进 `daily/<YYYY-MM>/`，再改索引链接 |
| 目录月 ≠ 文件名月 | 以**文件名日期**为准移动（跨月补写按日期归月） |
| 索引缺行 | 补一行（或删掉冗余文件）；`--fix-hint` 会给插入位置 |
| 死链 | 删该行或修链接 |
| 表格月 ≠ 文件月 | 把该行移到正确月份表格下 |
| 历史遗留月大量缺行（迁移旧仓常见） | 用 `LEGACY_MONTHS="2026-04 2026-05"` 先降级为告警，再逐月回填 |

迁移历史日志前**先备份 index**（`cp docs/index.md /tmp/index.bak`），插入/移动后用脚本验证集合相等（文件数 == 索引行数且无差集）。

## 什么时候不要用这个 skill

- 用户只想写一篇文档、一个 README —— 直接写，别搭体系
- 项目明确不需要跨会话记忆（一次性脚本、实验草稿）
- 用户已有自己的文档规范且不想改 —— 尊重现状；可以只提供 `check-daily-index.sh` 这类校验工具

## 安装（本体）与项目落地

**两层，别混**：

```bash
# ① 本体安装：--mode auto 默认"共享权威副本（~/.agents/skills/<name>）+ 各 agent 软链"，
#    没有共享仓库时自动退回"每 agent 真复制"；项目范围默认真复制（可提交）
bash .knowlog/install-skill.sh --agent auto        # 或 --mode link|copy、--scope project
bash .knowlog/bootstrap-docs.sh --with-recall      # ② 在某个项目里落地（结构 + 脚本 + 约束 + 召回）
bash .knowlog/docs-doctor.sh --fix-hint            # ③ 体检
```

- 各 agent 的**真实**安装位置、Codex/Cursor/DSH 为什么只能"项目级"、要不要自造 skill 管理器、
  以及**与 Trellis 安装流程的对应关系** → `references/installation.md`
- 一句话结论：**不需要自造管理器**；版本用 `VERSION` + `.knowlog-install.json` 记录，
  升级就是重跑 `bootstrap-docs.sh`（幂等 + 托管块，不会覆盖你手改的内容）。
- **分发**（给别的人/别的机器）：首选**一个 git 仓库 + 一行 `npx skills add https://github.com/CR903/knowlog`**
  （复用本机已有的 `skills` 管理器：自动装到 40+ agent + 软链 + `skills update` 可升级）；
  离线场景给 `.skill` 包 + `install-skill.sh`。CLI 也发布到了 npm（0.3.1 起）：`npx knowlog …`；不想用 npx 就用已安装路径 `node ~/.agents/skills/knowlog/bin/knowlog.mjs …`。
  详见 `references/installation.md`。

## 参考文件

- `references/structure.md` —— 完整目录/文件清单与每个文件干什么（改造体系、或用户问"XX 放哪"时读）
- `references/memory-and-constraints.md` —— 记忆分层与约束设计原理（为什么这么定；每条规则的失败模式）
- `references/maintenance.md` —— 日常维护配方：加端/加分类、布局切换、历史迁移、接 CI 与 pre-commit、装钩子、monorepo/多仓、非 git 项目
- `references/installation.md` —— 本体安装矩阵、升级机制、与 Trellis 的对比
- `adapters/README.md` —— 各 agent 适配器清单与"为什么有些只能静态注入"
