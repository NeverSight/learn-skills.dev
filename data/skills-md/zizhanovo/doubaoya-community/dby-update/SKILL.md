---
name: dby-update
description: >-
  都爆鸭（doubaoya / 本鸭）skill 对账更新器：把本机这套本鸭 skill 对账成官方仓库的当前全集——归档上游已下架的、
  装上新增的、刷新落后的，最后自检。按内容哈希认包，别人家的和用户自己改过的一个字不动；下架的移进归档目录而不是删除。
  Reconciles the installed doubaoya skills to the upstream set, then self-checks.
  触发方式：/dby-update、更新本鸭、更新都爆鸭、升级 doubaoya skill、检查本鸭更新、把本鸭更新到最新版。
version: 4.1.1
changelog: 新增触发层盲测用例 evals/triggers.jsonl（10 正 / 8 负）；包行为零变化
compatibility: >-
  需要 Node ≥ 18（`scripts/reconcile.mjs` 用全局 fetch），不装任何 npm 包。
  需要能对 GitHub / Gitee 的官方仓库发 HTTPS 请求以拉取上游全集。
---

# dby-update：把本鸭对账到最新

先 `--dry-run` 出清单，用户认可后再 `--yes`；不做清单之外的确认。Shell 权限由用户在宿主权限窗口里决定。

## 这个 skill 干的是「对账」，不是「更新」

让本机这套本鸭 skill **等于**上游当前全集：

- **归档**上游已经下架的
- **装上**新增的
- **刷新**内容哈希落后于上游当前版的，**以及内容虽是当前版、但少了一处落位的**；两者都不缺的一个都不动

> 🔴 **「内容是当前版」不等于「已经就位」。** 宿主按**自己那个目录**读 skill——Claude Code 只读
> `.claude/skills`，包只落进 `.agents/skills` 时对它**根本不存在**。
> 对账判据是「内容 **且** 落位」：本机任一受管安装目录缺落位，这个包就重装一遍补齐，计划里用 🩹 单列。

> 本机已和上游一致时结论是**无需任何操作**，一个包都不重下；想重装某个坏了的包用 `--force-refresh`。

> ⚠️ 别用 `npx skills update`：上游已改名 / 下架的包会被它**静默跳过、永远留在本机**，项目级安装它也看不见。

### 怎么判断「这包是不是本鸭发的」

**判据是 slug × 内容哈希，不看当初从哪个源装。** 上游 `index.json` 每个 slug 一条：`status`、历史哈希闭集、各版 semver + changelog：

| 状态 | 判据 | 处置 |
| --- | --- | --- |
| 当前版 | 哈希 = 索引当前版 | 保留，**不刷新**（除非 `--force-refresh`） |
| 我们的旧版 | 哈希命中闭集里某个历史版 | 刷新；索引 `status` 为 retired/renamed/merged 才归档 / 迁移 |
| **用户动过手** | 有 `.dby/origin.json` 时哈希 ≠ 装时记录；没 origin 时哈希谁都不命中 | 🔴 **跳过并列进报告，一个字都不动**，连刷新都不给 |
| 别人家的 | slug 根本不在索引里 | 不碰 |
| 已固定 | 用户 `--pin` 过 | 不刷新、不归档、不迁移，预检单列并带原因 |

→ origin / lock / pin、legacy 回退、Gitee 镜像：`references/index-and-lock.md`。

### 删除一律做成「归档」

要下架的包**移进 `<scope>/.doubaoya/archive/<时间戳>/`，不做 `rm`**，同目录留一份 `manifest.json`
写明每个包原来在哪、怎么移回去。

配套三条：归档后脚本打印一条可粘贴的**复原命令**（移回去立刻能用，skills CLI 记录要重装一次才认）；
归档目录在 `.doubaoya/.gitignore` 写 `*` 自忽略，**不改用户的 `.gitignore`**；
🔴 **受 git 跟踪的包一律不归档**（等于删受跟踪文件），脚本跳过并单列一栏，由用户自己决定。

## 改名迁移（renames.json）

→ 上游偶尔会把某个包**改名**（而不是单纯下架），这时老目录里的本地数据（比如 `dby-publish`
的 `config.json`）需要跟着搬家。**需要处理改名迁移时读 `references/rename-migration.md`**，
不需要就别读。要点三条：改名 = 索引里 `status: renamed/merged` 的条目；顺序固定是**装新包 → 搬本地数据 →
老目录归档**且逐条独立；**新目录已有同名文件时不覆盖**，只提示「冲突未覆盖」并给出老文件
在归档目录里的路径——**这一句要原样转述给用户**。

## 执行步骤

### 1. 找到对账脚本

按顺序找第一个存在的：

```
~/.claude/skills/dby-update/scripts/reconcile.mjs
~/.agents/skills/dby-update/scripts/reconcile.mjs
./.claude/skills/dby-update/scripts/reconcile.mjs
./.agents/skills/dby-update/scripts/reconcile.mjs
```

**找不到** = 本机没装或是旧版。🔴 **别自动装**：报告「本机未装对账脚本」，把下面这条命令给用户，**确认后再跑**，跑完**重新找一遍**：

```bash
npx -y skills add zizhanovo/doubaoya-community -g -s '*' -a claude-code universal -y
```

🔴 **零输出且退出码 0** ≠ 没事可做，是旧版脚本经软链（`.claude/skills/…`）调用时一步不跑：先换 `.agents` 那条真路径重跑；
仍如此就按上面那条安装命令重装（确认后跑），再重新找路径。

### 2. 先看清单（🔴 显式给 scope，别靠 auto 猜）

```bash
node <上一步找到的路径> --dry-run --scope global              # 当初带 -g 装的（最常见）
node <上一步找到的路径> --dry-run --scope project --project-dir <项目目录>
```

scope 猜错时脚本会打 ⚠️ 警告，看到就先确认 scope；不确定装在哪就两个 scope 都看一眼。
两个 scope 都打「一个本鸭 skill 都没有」= 本机没装，回到第 1 步先问用户，别把「整仓装」当对账跑。

它会联网取上游索引，打印**要归档哪些、要装哪些、要刷新哪些（逐行 `slug 旧版 → 新版 changelog`；标 `auto` 的是占位文案）、以及哪些因用户动过手 / 固定而不碰**，一个字都不会改。把这份清单**原样转述给用户**——尤其是「要归档」「要刷新」「用户改过的」的名字与 changelog（刷新是覆盖安装，确认的得是具体清单）。

> 🔴 **结论不高于证据。** 上游目录 / 索引这一跑没核到时，脚本会降级但不中止（不归档、或退回旧三文件），
> **结论要如实说降级了**，别说「完全一致」。GitHub 限流会自动换 Gitee 镜像同一 tag；`mirrorMismatch` 才是真没推齐，
> 用 `dby-feedback` 报给维护者；镜像新但那版本在 GitHub 上已存在 = **只是缓存没刷新**——告诉用户「刚发布，几分钟后重跑就到新版」，别说联系维护者。
> 字段与判据细节 → `references/index-and-lock.md`。

> 🧩 旧版遗留副本（`agent/skills/`）的处置 → `references/edge-cases.md`。

### 3. 确认后执行

用户看过清单、认可了，再跑（**scope 参数和上一步给的保持一致**）：

```bash
node <路径> --yes --scope <上一步用的那个> [--project-dir <目录>]
```

脚本会自己完成：归档 → 拉齐全集 → 复核 → 自检，最后打印一份结果，并告诉用户归档放在哪。

> 🛡 项目 scope 刷新/新增走「旁路装→校验→原子切换」，失败自动回滚；全局 scope 无此保证 → `references/staged-install.md`。

**退出码**：`0` 全通过；`3` 对账做完了但自检有项没过；`1` 用户取消；`2` 需要确认但当前不是交互终端；`4` 出错。

> 📝 项目里的 `skills-lock.json` 会被一起改，属预期；用户问起 `git status` 多了什么再解释，不主动提。

> ⚠️ 跑挂在「拉取上游」怎么办、名单含 `dby-update` 自己要不要重跑 → 同上 `references/edge-cases.md`。

> 🏷 安装源固定到 `index.json` 顶层 `ref`；缺字段按 `main` 装并提示「未固定」。发布打 tag → `references/release-ref.md`。

### 4. 回复用户（普通人能看懂）

🔴 用户不是工程师。只说三件事：**结果一句话 → 这次变了什么 → 下一步**。路径、哈希、ref、scope、
`.agents/skills`、`skills-lock.json`、API 钥匙、健康检查——**一切正常时一个都不提**；只在出问题时说卡在哪、怎么办。
包名用脚本括号里的中文名，slug 放括号。

> 🔴 **例外：`--json` 顶层 `notes[]` 里的提示一律要转述**，翻成大白话——静音清单只管「一切正常」时的技术细节，
> 不管这类「跑完了但打了折扣」的降级提示。

```
更新好了。这次更新了 2 个：
- 公众号写作与复盘（dby-write）1.9.0 → 1.9.1：新增变更说明字段
- 都爆鸭 Skill 自更新（dby-update）3.3.1 → 3.4.3：隔多版更新时列出中间每一版的说明
    · 3.4.2 …（中间各版照抄脚本）
下架归档了 1 个：xxx。要恢复的话告诉我一声。
你自己改过的 1 个没动：yyy。
新开一个对话就能用上新版。
```
- 隔了很多版 → 中间版本最多列 8 版，超过折叠，照抄脚本转述即可（细节 → `references/index-and-lock.md`）。
- 没有更新 → 「都是最新的，不用更新。」+ 一行各包版本（脚本那行「版本：…」）。**别自己补「已刷新 N 个」。**
- 「已固定」「受 git 跟踪没动」「git 判不出跳过」各一句，别混：前者用户自己 `git rm`，后者先修 git 再重跑。
- 🩹「缺落位」→ 一句「内容是最新的，只是补了一处安装位置」。
- 归档 → 说放在哪、要恢复就说一声（复原命令用户要时再贴）。
- 自检 ❌ → 说卡在哪步（没装上 / 没配钥匙 / 连不上服务）+ 脚本给的办法。
- 问包版本 → 读其 `.dby/origin.json`，别读 `skills-lock.json`。

## 常用参数

| 参数 | 作用 |
| --- | --- |
| `--dry-run` | 只看清单，绝不执行 |
| `--yes` | 跳过确认直接执行（**只在用户已经看过清单之后用**） |
| `--force-refresh` | 连「已经是当前版且落位齐全」的包也重下一遍（留给「包坏了想重装」） |
| `--verbose` | 连「别人家的」和「用户改过的」一起列名字 |
| `--scope auto\|global\|project` | 🔴 **每次都显式给**。默认 `auto` 是按 cwd 猜的，猜错会静默变成「整仓重装」。当初带 `-g` 装的就是 `global` |
| `--project-dir <目录>` | 项目级安装在别的目录时指定 |
| `--json` | 机器可读输出 |
| `--self-check` | 离线自检脚本自身（不联网） |
| `--pin <slug> [--reason <文>]` / `--unpin <slug>` | 固定 / 解除固定某个包（不联网，只改 `<scope>/.dby/lock.json`）；固定后对账跳过它。用户说「这个包别更」就用它 |
| `--help` / `-h` | 看用法（不联网，不碰任何安装目录） |

## 边界

- **只碰本鸭发过的包**（判据是上面那张三态表）；别人家的、用户改过的一个字都不动。
- 🔴 git 探测跑不通、判不出来的包同样保守跳过；脚本把它和「受 git 跟踪」**分两栏**打出来，处置不同。
- **不动用户的本地数据 / 配置**（`dby-publish` 的 `config.json`、创作 DNA、封面 / 草稿等产出）——对账只覆盖 skill 目录里受版本管理的文件。
- 不创建后台任务、定时任务或 Agent Hook。
- 用户只问「有什么更新 / 现在什么版本 / 要不要更」→ **先回答，不执行**（`--dry-run` 正好用来回答这个）。
  明确要实际同步时才跑第 3 步。
- 只想更新某一个**全局**skill：`npx -y skills update <skill 名> -g`，只碰点名那个（不做对账；项目级安装它看不见，仍走本脚本）。