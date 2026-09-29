---
name: yueban-docs-freshness-audit
description: '检查 AGENTS.md/README.md/业务文档是否过时：悬空引用、状态/自相矛盾、链接失效、跨文档不一致、openspec change 状态不一致（若项目使用 openspec）、权威性冲突未标注、索引覆盖缺口、遗漏的新增基础设施、命令/路径不可执行、重复内容、历史叙事残留，发现问题直接改文件。范围按规则动态发现、不硬编码具体文件名单：根 AGENTS.md/README.md、docs/ 目录下全部 .md 文档、根目录下的 skills/ 文件夹（如果存在）下全部 .md 文档、每个当前维护 submodule（从 .gitmodules 动态取得、排除 deprecated/ 前缀）各自的 AGENTS.md/README.md 与 docs/ 子目录。默认排除：deprecated/ 整个目录树、项目明确标注的历史规划归档文档目录、整个 openspec/ 目录树（若项目使用 openspec）、.claude/.codex/.gemini/.agents 四个 agent 工具配置目录整体、.gitignore 里列出的路径。docs/、submodule docs/ 下的产品/业务资料判断需格外谨慎（若该目录下有项目自己的 AGENTS.md，先读一遍再处理），见「范围」一节说明。**仅手动触发**：只有用户明确输入 `/yueban-docs-freshness-audit`，或明确点名要用这个 skill 时才执行；用户说"检查一下文档""看看文档是不是过时了"这类泛化表述不要自作主张联想到这里，先按普通请求处理或直接追问，除非用户点名。'
allowed-tools: Bash, Read, Edit, Grep, Glob, Agent, WebFetch
---

# yueban-docs-freshness-audit：文档时效性/一致性审计

> ⚠️ **仅手动触发**：只有用户明确输入 `/yueban-docs-freshness-audit`，或明确点名要用这个 skill 时才执行下面的流程。

## 范围（按规则动态发现，不硬编码具体文件名单）

不要在这个文件里手写"仓库里现在有哪些 submodule/skill/历史归档目录"这种会随项目演进而过期的清单——过期的清单本身就是这个 skill 想要消灭的那类问题。每次执行都用下面的规则重新枚举（具体命令见第 1 步），必要的项目专属细节（比如"哪个目录是历史规划归档、不算当前产品文档"）当场问用户或从项目自己的 AGENTS.md/README.md 里找依据，不要凭经验/凭上次执行的记忆假设。

- 根目录：`AGENTS.md`、`README.md`
- `docs/` 目录下全部 `.md` 文件（含 `docs/README.md`、`docs/xxx.md` 这类顶层文件，以及子目录下的 PRD/背景知识类业务资料）
  - **处理 `docs/` 下 PRD/背景知识类业务文档时额外谨慎**：这类内容不是工程文档，"过去怎样、后来改成怎样"这类句子往往是需求变更的决策留痕，维度 11（历史叙事残留）不能直接套用工程文档的判断经验，拿不准一律不改、记入存疑；维度 6（权威性冲突）在这里尤其重要——如果项目自己的文档（比如 `docs/AGENTS.md` 或根 `AGENTS.md`）里已经写明了多份文档之间的权威性优先级，处理前先读一遍，不要在审计过程中意外改变这层权威性结论；如果项目里没有这类说明，就不要自己下权威性结论，拿不准记入存疑。
  - 如果 `docs/` 下存在明显不属于"当前产品文档"的历史规划/历史归档子目录（比如已废弃的功能规划、旧版本 plans/specs），执行前先跟用户确认具体路径并加入排除清单——不要自己猜哪个目录是历史归档，猜错了会漏审或误改不该动的目录。
- 根目录下的 `skills/` 文件夹（如果存在）下全部 `.md` 文件（如 `skills/<name>/SKILL.md`）——按普通工程/操作文档处理，不适用上面「处理 `docs/` 下 PRD/背景知识类业务文档时额外谨慎」那条特殊规则（skill 定义文档是操作说明，不是业务决策留痕）。
- **每个当前维护的 submodule**——动态来源是 `.gitmodules` 里路径不以 `deprecated/` 开头的条目（具体有哪些以 `.gitmodules` 当前内容为准，新增/移除 submodule 会自动跟着变，不需要改本文件）：
  - 各自的 `AGENTS.md`/`README.md`
  - 各自 `docs/` 子目录下全部 `.md` 文件（如果该 submodule 没有 `docs/` 目录，跳过即可，不算遗漏）——内容性质与上面「处理 `docs/` 下 PRD/背景知识类业务文档时额外谨慎」一致，同样要谨慎判断

**默认排除**（根仓库和每个 submodule 统一适用，和 `yueban-proj-prune-historical` 用同一份清单；这几类理由各不相同、分别判断，不要因为都叫"排除"就混为一谈）：
- `deprecated/` 整个目录树（含已停止维护、冻结在某个分支上的历史子仓库及其文档）。
- 项目里明确标注为"历史功能规划归档"的文档目录（如果存在）——具体路径按项目约定，执行前先确认，没有明确依据不要自己认定某个目录属于这一类。
- 整个 `openspec/` 目录树（若项目使用 openspec）——`changes/`（含 `archive/`）、`specs/` 等都是 OpenSpec 工具自己的管理范畴，不纳入审计/编辑范围；维度 5 需要核对文档里提到的 change 状态时，只读 `openspec/changes/` 的**目录结构**（哪些 change 在顶层、哪些在 `archive/`）做参考，不读取/编辑其中文件内容。
- `.claude/`、`.codex/`、`.gemini/`、`.agents/` 四个 agent 工具配置目录整体（不论符号链接还是真实安装的 skill 副本）。
- `.gitignore` 里列出的路径——枚举只用 `git ls-files`，天然不会枚举到。

## 十一个检查维度

对上面清单里的每个文件，逐条过以下检查点。除非特别说明，发现问题直接用 Edit 修改文件；拿不准的问题不强行改，记入最终摘要的"存疑"项。

1. **悬空引用**：文档中提到的文件/目录/路径在仓库里已不存在。
2. **状态矛盾/自相矛盾/失效指引**：文档声称的状态（"待实现""已支持""尚未……"）与实际情况相反；同一文档内前后表述冲突；描述的操作步骤/前提条件已不成立。
3. **链接有效性**：Markdown 相对链接指向的文件/锚点是否存在（`[text](path#anchor)` 里的 `path` 要能在仓库里找到，`#anchor` 要能在目标文件的标题里找到对应 slug）；外部 `http(s)://` URL 用 WebFetch 确认可达（超时/持续 4xx/5xx 视为失效）。
4. **跨文档一致性**：同一话题在根文档与 submodule 自己的文档之间，描述是否一致。
5. **openspec 状态一致性**（若项目使用 openspec）：文档中提到的 change 状态（已归档/待实施/进行中）是否与 `openspec/changes/` 顶层（未归档）和 `openspec/changes/archive/`（已归档）的实际目录情况一致。
6. **权威性冲突**：多份文档对同一件事说法不一致时，是否已标注了谁更权威。缺失标注且项目自己的文档里能找到明确依据（如某份 AGENTS.md 已有权威性优先级的定论）的，直接补充；找不到明确依据的不擅自下结论，记入"存疑"。
7. **索引覆盖缺口**：`docs/README.md` 这类索引类文档是否列全了对应目录下的实际子目录/文件（用 `ls`/`find` 对照文档里列出的条目做差集）。
8. **遗漏的新增基础设施**：代码库中已有、但对应文档没提及的新增能力/服务（方向与"过时内容"相反，是"该写而未写"，比如新增了一个部署配置/服务但根 `AGENTS.md` 没提）。
9. **命令/路径可执行性**：
   - 路径用 `ls`/`test -e` 确认存在。
   - Shell 命令按以下规则处理：
     - 本地可安全跑的命令（不依赖真实生产/预发布凭据、不依赖连接真实外部数据库或云服务、幂等或只读）**实际执行**一遍确认能跑通；执行前必须先查对应 submodule `AGENTS.md`「测试」一类章节里的前提条件（本地依赖服务、VPN 等），不满足前提条件的不盲跑。
     - 涉及连接真实生产/预发布数据库、需要真实云凭证、或有其它不可逆副作用的命令，**不实际执行**，只做静态合理性检查（命令在对应脚本/构建配置文件里确实存在，语法上说得通）。
     - 跑不动的命令记入摘要"跳过"项并说明原因，不当作失败处理。
10. **重复内容**：同一信息在多个文件间重复维护的段落，判断是否应该收敛为"单一来源 + 其它文件改为引用链接"。只在信息完全等价、且改成引用不会丢失上下文时才合并；改动时保留原文件的相对位置和读者预期（不要把一个自然段变成一句"见 xxx"就完事，除非原文确实只是纯复制粘贴）。
11. **历史叙事残留**：识别"过去怎样、后来因为……改成怎样""随某次迁移/change 删除/变更"这类记录变更过程、不再具有操作指导意义的叙事段落并精简，只删叙事句子、保留后面仍然生效的操作指南（不整节删除）。**本维度独立处理，不调用 `yueban-proj-prune-historical`**；各当前维护 submodule 的 `AGENTS.md`/`README.md` 同时在两个 skill 检查范围内，接受这层重叠。

## 执行流程

### 第 1 步：枚举文件

```bash
# 根目录
git ls-files AGENTS.md README.md

# docs/ 全部 .md（如果项目里有需要排除的历史归档子目录，在这里加 grep -v 排除掉）
git ls-files 'docs/*.md' 'docs/**/*.md'

# 根目录 skills/ 文件夹（如果存在）下全部 .md
git ls-files 'skills/*.md' 'skills/**/*.md' 2>/dev/null

# 当前维护的 submodule：从 .gitmodules 动态取得（排除 deprecated/ 前缀），不要硬编码模块名
# 不用 mapfile/readarray（bash 4+ 才有；macOS 自带 /bin/bash 是 3.2，没有这个内置命令，会直接报
# command not found）——改用 while read 循环拼数组，bash 3.2 和更新的 bash 都能跑
ACTIVE_SUBMODULES=()
while IFS= read -r sm; do
  ACTIVE_SUBMODULES+=("$sm")
done < <(git config -f .gitmodules --get-regexp '\.path$' 2>/dev/null | awk '{print $2}' | grep -v '^deprecated/')
for sm in "${ACTIVE_SUBMODULES[@]}"; do
  git -C "$sm" ls-files AGENTS.md README.md | sed "s#^#$sm/#"
  git -C "$sm" ls-files 'docs/*.md' 'docs/**/*.md' 2>/dev/null | sed "s#^#$sm/#"
done
```

`'docs/*.md' 'docs/**/*.md'` 两个 pattern 必须一起用（对每个 submodule 的 `docs/` 也一样）——`**/*.md` 这个 pathspec 在 git 里要求至少一层子目录，单独用会漏掉目录顶层的 `.md` 文件。

用 `git ls-files`/`git config -f .gitmodules` 而不是手写清单或 `ls`，确保每次执行都反映仓库当前的真实状态（新增 submodule、新增 docs 子目录都会自动被下一次执行捕捉到，不需要回来改这个 SKILL.md）。`ACTIVE_SUBMODULES` 为空数组时上面的 `for` 循环直接跳过，不报错；没有 `.gitmodules` 也一样。

枚举完 `docs/` 之后，先扫一眼有没有明显不属于当前产品文档的历史规划/归档子目录——如果拿不准，问用户一句再决定要不要排除，不要自己猜。

### 第 2 步：分组派发

按第 1 步的实际枚举结果动态分组派发（每组一个 `general-purpose` 子 agent，**在同一条消息里一次性并行发出**）——组数不固定，随当前 submodule/docs 子目录数量变化，按下面原则划分：

- 组 A：根目录 `AGENTS.md`、`README.md`
- 组 B：`docs/` 目录下的顶层 `.md` 文件（如 `docs/README.md` 及其它直接放在 `docs/` 下的文件）
- 组 B2：`docs/` 下的业务/PRD 类子目录（按实际存在的子目录划分，不含已确认排除的历史归档目录；每组子任务 prompt 里必须附上「范围」一节里"处理 `docs/` 下 PRD/背景知识类业务文档时额外谨慎"那段原文，并强调拿不准一律不改、记入存疑）
- 组 B3：每个当前维护 submodule 各自 `docs/` 子目录下全部 `.md` 文件（有几个 submodule 存在 `docs/` 就分几组，或体量小时合并成一个 agent；同样附上「处理 `docs/` 下 PRD/背景知识类业务文档时额外谨慎」那段原文）
- 组 D：根目录 `skills/` 文件夹（如果存在）下全部 `.md` 文件（如有多个 skill 子目录，体量大时可拆多组，体量小时合并成一组）
- 组 C：**全部**当前维护 submodule 各自的 `AGENTS.md`/`README.md`，一起给同一个 agent（不管当前有几个 submodule，都放一组，因为「跨文档一致性」维度需要它们互相对照，拆开反而看不到全貌）

每个子任务 prompt 必须完整包含本文件"十一个检查维度"整节原文内容（把文字直接粘贴过去，不要只给文件路径——子 agent 是全新上下文，看不到这个 SKILL.md），并附上该组的具体文件路径列表、以及下面这段执行方式说明：

```
你的任务：对以下文件做文档时效性/一致性审计：
<该组文件路径列表>

【十一个检查维度】
（粘贴上面"十一个检查维度"整节内容）

【交叉引用资料源】
- 涉及"跨文档一致性"/"openspec 状态一致性"时，对照的资料源包括：其它 submodule 的 AGENTS.md/README.md（用 Read 打开）、openspec/changes/ 与 openspec/changes/archive/ 目录实际内容（用 Glob/Bash ls 枚举，若项目使用 openspec）、实际代码库结构（用 Grep/Glob 确认某个类/文件/服务是否存在）。
- 涉及"命令/路径可执行性"时，先 Read 对应 submodule 的 AGENTS.md「测试」一类章节确认前提条件，不满足前提条件的命令不要跑。

【执行方式】
直接用 Edit 工具修改文件，不要先列候选清单等待确认——用户会自己用 git diff 复核你的改动。拿不准的问题不要强改，记下来。
改完输出一份结构化摘要（不要写成文件，直接在你的回复里返回）：
- 改了哪些文件、每处改动内容和理由
- 存疑但没改的问题，及理由
- 命令验证：哪些跑了、结果如何；哪些跳过、为什么
```

### 第 3 步：汇总输出

收到全部分组的摘要后，合并成一份终端摘要回复用户，按文件分组列出：

```
## yueban-docs-freshness-audit 执行摘要

### 已修改
- <文件路径>：<改了什么，为什么>
- ...

### 存疑（未修改，建议人工确认）
- <文件路径>：<问题描述，为什么没直接改>

### 命令验证
- 通过：<命令列表>
- 跳过：<命令> — <原因>

复核方式：`git diff`（各 submodule 需要 `git -C <submodule> diff`）。本次未自动创建 commit，是否提交由你决定。
```

不生成额外的报告文件。

## 与 yueban-proj-prune-historical 的关系

检查范围有交集——各当前维护 submodule 各自的 `AGENTS.md`/`README.md`（以及各自的 `docs/` 子目录），根仓库自身 `AGENTS.md`/`README.md`/`docs/`/`skills/`，维度 11（历史叙事残留）与该 skill 职责重叠。本 skill 独立处理这一维度，不调用/依赖 `yueban-proj-prune-historical`，接受两边逻辑并存的重复。两边现在用的是同一份「默认排除」清单（见「范围」一节），不需要再分别记忆两套规则。

唯一的差异点：`yueban-proj-prune-historical` 对 `deprecated/` 模块多了一条例外——如果该模块被其它文档明确依赖用来做同步比对，则不适用它的清理逻辑（因为它要删的"历史叙事"正是那类同步流程依赖的信息）；本 skill 对 `deprecated/` 的排除没有这条例外（本 skill 本来就不检查 `deprecated/` 下任何文档的时效性，不存在"是否依赖它做比对"这层考量）。

项目里如果还有其它专门生成/维护某份具体文档内容的 skill（比如某个自动生成 schema 文档字段说明的工具），本 skill 只检查文档级维度（链接、索引覆盖、跨文档一致性等），不涉及该文档的领域字段语义本身，两者不冲突——遇到这种情况按此原则判断即可，不需要为每个项目专属 skill 单独列关系说明。

## 不做的事

- 不是不加区分地扫描仓库里所有 `.md` 文件——范围规则本身是动态发现（见「范围」一节），但仍然按「默认排除」清单限定：不扫 `deprecated/`、已确认的历史规划归档目录、整个 `openspec/` 目录树、`.claude/`、`.codex/`、`.gemini/`、`.agents/` 四个 agent 工具配置目录。
- 不生成候选清单等待二次确认——直接改，靠 git diff 复核。
- 不自动创建 git commit。是否提交、何时提交由用户决定，遵循仓库自己 `AGENTS.md`「提交约定」（仅在用户明确要求时才创建 git commit）。
- 不实际执行需要真实生产/预发布凭据、或连接真实外部数据库/云服务的命令。
- 不额外写报告文件——摘要直接打印在回复里。
