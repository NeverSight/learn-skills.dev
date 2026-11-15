---
name: ake
description: 在实现、架构、排障、部署、风险变更前检索工程知识；实质工程任务完成且用户确认验证通过后，评估是否按四类知识流程捕获、检查、审核，并等待用户授权后发布。
---

# AKE 使用帮助与入口路由

## A. Skill 日常命令（在对话中使用）

| 命令 | 功能 |
|---|---|
| `/ake` | 显示使用帮助（本页） |
| `/ake help` | 显示使用帮助（与 `/ake` 完全相同） |
| `/ake status` | 查看当前安装和版本状态（只读，不联网） |
| `/ake update` | 检查并更新 AKE（由用户明确发起，走确定性 CLI 流程） |

宿主只把 `/ake` token 交给本 Skill，后面的 `status`、`update`、`help` 是**自然语言**，不是宿主结构化参数路由。遇到歧义、或更新可能覆盖本地定制时，先询问用户，不要替用户决定。

## B. CLI 安装与项目初始化（在终端使用）

| 命令 | 功能 |
|---|---|
| `npx skills add Shakyae/agent-knowledge-engine@<完整commit> --skill ake -g` | 安装/更新到用户级 Skills 目录（Vercel Skills CLI） |
| `ake init` | 初始化当前工作目录 |
| `ake init --dir <project>` | 初始化指定目录 |
| `ake status` | 查看安装状态，同时保留原有知识统计 |
| `ake update` | 检查并更新已安装的 Skill（参数以 `ake --help` 为准） |

说明：`ake` 指 AKE 源码或项目内附带的 CLI（`node scripts/ake.mjs …` 或 `node .ake/tools/scripts/ake.mjs …`）。Skill 的安装与链接由上面的 Vercel Skills CLI 负责；`npx skills update` 不会推进已固定到某个 commit 的安装，因此更新请用 `ake update`。

## C. 知识管理能力

- **自动检索**：任务开始、涉及实现/排障/架构/风险变更时，先检索四类知识（Agent Notes、Defensive Patterns、Postmortems、Cookbooks）。
- **自动评估沉淀**：实质任务完成并经用户确认后，评估本次是否有可复用知识值得沉淀。
- **手动评估当前 Session**：直接要求 AKE 评估这段工作是否值得整理（不要求先跑完自动流程）。
- **手动整理指定经验**：明确指定「把某段经验整理成候选」，AKE 只按你的指定范围整理。
- **查看候选**：`node .ake/tools/scripts/ake.mjs candidate list`（查看全部候选及状态）。
- **检查审核状态**：`node .ake/tools/scripts/ake.mjs candidate show <id>` / `candidate check <id>`。
- **发布授权流程**：候选经独立 reviewer 审核后，需**用户明确授权**才 `approve <id> --by <human> --confirm` 并 `publish <id>`；未授权时保持未发布。

## 路由规则

- `/ake` 或 `/ake help`：**只输出本帮助**。无参数 `/ake` 不解释为知识沉淀任务、不扫描当前 Session、不自动检索、不创建候选。
- `/ake status`：执行 `ake status`（只读）。若当前目录没有 AKE 项目，如实报告错误，不改用其他项目。
- `/ake update`：执行确定性 CLI 更新流程，顺序如下：
  1. 若本 Skill 目录内存在 `resources/ake-source/scripts/ake.mjs` 且支持 `update` → 用它执行；
  2. 否则，若当前处于 AKE 官方源码 checkout（`origin` 为官方仓库、`skills/ake` 无未提交改动）→ 用 `node <checkout>/scripts/ake.mjs update`；
  3. 两者都不满足 → 停止并说明原因，**不得**由模型自行拼 shell、Git、复制或清理命令。
- 更新成功后提示：DSH 每次加载/注入 Skill 时读取磁盘，**本 Session 已注入的旧内容不会自动刷新**；请在新消息中重新调用 `/ake`，若仍使用旧内容则新开 Session。**无需**重启整个 DSH。
- 任何会覆盖用户定制、或无法确认安装目标的情况，先询问用户。

## 示例

1. `/ake` → 只显示本帮助（不检索、不沉淀）。
2. 在项目目录执行 `ake init` → 初始化**当前目录**；换到别处初始化才用 `ake init --dir <project>`。
3. `/ake status` 查看版本/安装/更新状态；需要更新时 `/ake update`（自动备份、校验、失败回滚）。

## 安装、初始化与日常使用的区别

- **安装**：把 Skill 放进用户级 Skills 目录，每台机器/每个用户一次。
- **初始化**：为某个 Git 项目建立 `.ake/`（知识目录、配置、项目内 CLI），每个项目一次。
- **日常使用**：以具体请求调用（例如 `/ake 评估这段经验是否值得沉淀`），或由 AKE 按任务阶段自动检索/沉淀；单独输入 `/ake` 只显示帮助，不触发检索或沉淀。日常使用不重复安装或初始化。

# AKE knowledge operations

先确定目标项目的绝对路径，并使用 Skill 加载器提供的 **本 Skill base directory** 绝对路径；不得从当前工作目录、目标项目或 AKE 源码 checkout 推导 Skill 路径。若加载环境未提供该绝对路径，先请用户提供/确认已安装 Skill 的位置，不要猜路径。

## 项目初始化（按需）

首次检查用下面的 `bootstrap.mjs --dry-run` 对目标做只读预检；不要把继承 `GIT_*` 环境的普通 shell `git` 结果当作授权依据。Bootstrap 清理全部 `GIT_*` 环境变量后再检查：目标可以是独立 Git 工作树根目录，也可以是已有父级工作树中的项目子目录；它只在用户给定的确切目录初始化，不向上迁移、不创建嵌套 Git 仓库，也不运行 `git init`。若结果明确为非 Git 工作树，询问用户是否先选择/初始化 Git 项目；只有用户确认且目录已由用户建立为有效工作树后才重试。缺少 Git、bare 仓库或其他 Git 检查错误时，不得推测可新建，停止并报告原因。检查失败时零写。

如果目标中 `.ake/config.json` 与 `.ake/tools/scripts/ake.mjs` 都是现有文件，视为已初始化：不要重复运行 bootstrap、不要复制或升级配置/CLI。bootstrap 仅安全读取 config 版本与随附 bundle 的 package 元数据并报告是否不同；它不会执行项目 CLI，且不能由 config 版本证明 CLI 本身的版本。无法判断时明确报告未知。旧版或版本未知的项目 CLI 在任何写操作前，要求用户自行运行只读 `node <绝对目标路径>/.ake/tools/scripts/ake.mjs status --json`，确认返回的 `project` 精确等于目标绝对路径；Agent 不自动执行现有项目 CLI，也不在未确认前执行写命令。若项目根错误，先备份并让用户人工审阅当前官方 AKE 版本的迁移/合并方案；不要自动复制、升级或覆盖项目 CLI、配置、知识文件。确认后才可使用该项目自己的 CLI。

若缺任一文件，使用本 Skill 随附的离线资源执行器，不依赖 AKE 源码 checkout 或调用时的工作目录。先展示计划：

```bash
node <本 Skill base directory 的绝对路径>/bootstrap.mjs --dir <绝对目标路径> --dry-run
```

dry-run 若报告任何 `conflict`，停止并报告冲突路径；不要应用部分计划。无冲突后再应用：

```bash
node <本 Skill base directory 的绝对路径>/bootstrap.mjs --dir <绝对目标路径>
```

bootstrap 从本 Skill 的 `resources/ake-source/` 离线资源调用原有 AKE 初始化器。若资源不完整，它会列出确切缺失文件且不写项目文件；按 README 中的官方 Skill 安装说明从 AKE 源码 checkout 恢复/更新 Skill，再重试。初始化不安装任何全局 Skill，也不升级已有项目 CLI。

程序可测试的行为包括 Git 根校验、dry-run、冲突拒绝、离线初始化和既有 CLI/config 保留；“非 Git 时询问用户”是本 Skill 对 Agent 的软指令，不能由脚本或自动化测试证明真实 Agent 会遵循。不要把提示规则描述成安全边界。

## 任务前：用户可见通知与按需检索
- 当任务首次进入 AKE 触发阶段（相关工程知识检索或任务后沉淀）时，在首个 AKE CLI 操作前给用户一条简短通知；同一阶段连续进行的多次搜索/候选命令合并在这条通知中，不逐条重复通知。
- Agent Teams 由 Lead/任务 owner 统一发用户通知；成员只将检索/候选结果汇报给 Lead，不各自重复通知用户。
- 在触发的检索阶段，先说明「我会检索 AKE 项目知识并按相关性使用」，再按模块/技术、症状、操作构造具体关键词执行 `node .ake/tools/scripts/ake.mjs search <terms>`。只在触发相关任务时检索，不要求无关任务做空搜索。
- 搜索默认覆盖四类知识根：Agent Notes、Defensive Patterns、Postmortems、Cookbooks；结果须展示/说明类别标签。需要时使用 `--include-candidates`，并可用 `--type`/`--limit` 缩小结果。
- 命中后只读查看相关文档；判断其 scope、status、verified、证据和当前代码是否仍适用，不把命中视为自动指令。最终报告指出检索词、命中文档/类别及适用性；没有命中只表示“未找到”，不表示知识不存在。

## 任务后：判断是否值得沉淀
- **Agent Note**：有可复用的设计/实现决策、重要取舍或变更依据。按生命周期写入 `.agents/notes/{proposed,implemented,rejected}/{class}/`。
- **Defensive Pattern**：可重复的规则/防错检查，写入 `docs/defensive-patterns/`。
- **Postmortem**：已发生的故障、影响、时间线、根因与护栏，写入 `docs/postmortem/`。
- **Cookbook**：可复用的操作步骤及验证方式，写入 `docs/cookbook/`。

只把有据、可复用的新知识写成候选。普通问答、琐碎改动、没有稳定经验或已被现有文档覆盖时，报告「AKE · 本次无新增知识」。若已发现可能有价值的新知识但核心证据不足，不要误报“无新增知识”：不创建候选，明确标注“潜在知识待补证据”，说明缺少什么以及如何验证。不得编造 scope、evidence、验证日期、会话/事件标识或解决状态。先搜索正式知识及候选，优先修订真正对应的现有目标。候选应对应实际有价值的结果，并用与核心主张相关的 A/B 级证据支持；可追溯证据可以是当前会话中可核对的直接观察，无需额外持久化产物或 ID。按主张选择合适验证；不得声称未执行的测试/检查已运行，也不要求每个候选都必须有实际测试。写明适用范围和验证条件。创建或更新前通知用户「AKE · 准备沉淀为 <类别>：<简要主题>」。使用 `candidate new` 或 `candidate revise`、`candidate submit` 和 `candidate check`；逐项核对格式、目标、链接、重复项、范围、证据、内容哈希和目标哈希。

## 独立审核与发布授权
- **Agent Teams**：优先由未参与候选生成、且适合该领域的独立 reviewer 检查。以真实 reviewer 名称运行 `review <id> --reviewer ... --verdict <approve|request-changes|reject> --notes ...`；不得伪装身份。发出一次请求后，等待该 reviewer 的实际审核结果；派单成功、工具接受或沉默都不是审核完成。若当前轮次无法等待实际结果，暂停并如实告知用户/Lead，不自行假称已审核。
- **Single Session**：有可用独立子代理时，交由未参与生成的 reviewer 审核并等待其实际结果；没有可用 reviewer 时，说明独立审核不可用并暂停，等待安排 reviewer。作者自检可作为补充记录，但不得声称独立，也不得替代所需的独立审核。
- Reviewer 报告使用 `PASS`、`PASS WITH LIMITATIONS`、`BLOCK` 标签；现有 CLI verdict 保持 `approve|request-changes|reject`：`PASS` 映射 `approve`；`PASS WITH LIMITATIONS` 若核心主张有据且限制已明确写入候选，也映射 `approve`；若需先补充/明确限制，则映射 `request-changes`。`BLOCK` 按问题是否可修复映射 `request-changes` 或 `reject`。不要将新标签作为 CLI verdict。
- 证据等级针对候选的核心主张，而非元数据完整度。**A（强直接证据）** = 与主张相关的源代码/差异、实际测试日志、可复现结果，或有意义的前后对比；不相关的代码或测试不能支撑该主张。**B（当前上下文中的可用证据）** = 与主张相关的当前运行/系统状态、实际浏览器检查、此 Session Agent 的直接验证、用户对其意图/验收的确认，或可读取的配置、安装脚本、系统状态。B 不要求持久化材料、独立证据文件、session/event ID，也不要求把会话内直接观察再包装成独立佐证；按主张判断关联性和局限。**C（核心证据缺失）** = 核心主张没有基本相关证据、证据与主张不匹配，或被现有证据反驳。A/B 可支持相关核心主张；C 对核心主张须标 `BLOCK`，并按可修复性映射 `request-changes`/`reject`。缺少 session ID、事件号、独立证据文件或不相关主题本身不降级证据等级，也不构成 BLOCK；不得为了满足字段制造证据。
- 若潜在知识有价值但因 C 级证据不足不能形成候选，报告“潜在知识待补证据”及具体缺口/验证路径，不能说“无新增知识”。`AKE · 本次无新增知识` 仅用于确实没有新的、可复用结果。

- 收到 `request-changes` 后最多自动修订一次，再交由独立 reviewer 实际复核一次；第二次仍未通过就暂停并报告，不循环。CLI 记录 verdict 时保留原有候选状态和绑定门禁。
- Reviewer 通过后，向用户报告候选及限制并等待用户明确授权发布。不得默认自动授权，不得预先运行 `approve --confirm` 或 `publish`。收到明确授权后，使用现有 CLI `approve <id> --by <human> --confirm` 记录授权，再运行 `publish <id>`；`--by` 是声明，不是身份认证。用户未授权时保持未发布，并说明候选 ID、状态和等待原因。
- 内容修改或观察到漂移后，必须按现有门禁重新提交并重新审核；发布仍须保留绑定校验、漂移检测、账本和 unknown-result reconcile。Skill/AGENTS 是软约束，普通文件工具可绕过，不是安全边界。
- 合成回归例（不是已观察事实）：假设本 Session Agent 实际检查 Tampermonkey 目标页面的按钮文字与背景/边框、`::before`/`::after` 伪元素层叠、真实计算样式和下拉交互，且用户确认这些观察；其他页面/菜单主题未检查并已作为限制写明。此即时上下文证据属 B，不要求持久化截图、独立证据文件或 session/event ID；预期 `PASS WITH LIMITATIONS`，映射 CLI `approve`。不能仅因缺少标识/持久化文件或其他主题未验证而 BLOCK。若同一候选对这些核心主张实际没有基本证据（C），则应 `BLOCK`，按可修复性映射 `request-changes`/`reject`。此例为合成测试向量，不是实际浏览器检查或 Tampermonkey 行为验收。


## 触发路由与连续执行能力边界
- 按阶段应用触发并只执行当前阶段适用的步骤：任务前触发只做检索与适用性判断，不启动候选捕获；任务后触发先评估沉淀价值和证据。用户显式调用 `/ake` 时按其请求的阶段执行，不受自动完成语句条件限制。仅在任务后评估确认有据、可复用且未被覆盖的结果时，才继续查重、创建/修订候选和请求独立 reviewer；无价值则报告「AKE · 本次无新增知识」，证据不足则报告“潜在知识待补证据”，不得强制建候选。
- 当前阶段的所有适用步骤一次连续执行，不要在检索、适用性判断、价值/证据评估、查重或合格候选的准备/提交/reviewer 请求之间额外询问“是否继续”。只在必须取得实际 reviewer 回复或用户发布授权时等待；无法等待 reviewer 的真实结果时如实报告，不伪造结果。现有 candidate/submit/review/approve/publish 权限、安全、验证和状态门槛不因连续执行而放宽。
- 自动完成语句路由的条件仅适用于这一个额外的自动信号：此前确有实质工程任务（实现、调试、测试、架构或风险变更），本 Skill 已加载，且用户随后明确说「验证 ok」「测试通过」「没问题了」「验收通过」等。该条件不限制显式 `/ake` 调用或既有适用知识触发。普通问答、解释、无工程产出的对话不因完成语句路由自动进入候选流程；完成确认也不等于发布授权。
- 以上消息判断是模型软约束，不是宿主硬触发。普通语言消息不能保证自动加载本 Skill；显式 `/ake` 可通过宿主机制注入，但不得声称 AKE 能观察所有消息或保证检测任意完成语句。无法确认 Skill 已加载时如实说明。


## 常用命令
- `node .ake/tools/scripts/ake.mjs candidate new --kind <note|defensive-pattern|postmortem|cookbook> --title <title> --author <actual-name> --target <path> --body <file>`
- `node .ake/tools/scripts/ake.mjs candidate submit <id>`
- `node .ake/tools/scripts/ake.mjs candidate check <id>`
- `node .ake/tools/scripts/ake.mjs review <id> --reviewer <actual-reviewer> --verdict <approve|request-changes|reject> --notes <evidence>`；CLI verdict 不接受 PASS 标签
- 仅在用户明确授权发布后：`node .ake/tools/scripts/ake.mjs approve <id> --by <human> --confirm`，随后 `publish <id>`

## 用户可见最终报告
任务结束时简要填写，不隐去未验证项：

```text
AKE 知识流程
- 检索：<关键词>；命中 <类别/文档及适用性>，或未找到
- 沉淀：<Agent Note | Defensive Pattern | Postmortem | Cookbook + 标题/目标>；若潜在知识待补证据，写明证据缺口/验证路径；仅确无可复用结果时写「AKE · 本次无新增知识」
- 检查/审核：<candidate check 结果；独立 reviewer 实际结果，或独立审核不可用并暂停>
- 授权/发布：<用户明确授权后发布，或未授权/未完成审核而保持未发布及原因；候选状态>
- 验证：<实际运行的命令与结果>
- 风险/未验证：<剩余事项>
```

## 边界
AKE 是流程和工具层，不是安全边界。普通文件/shell 工具可绕过流程；身份无法验证，自动授权标记不证明人类授权或审核者真实独立。发布仅对经 CLI 处理的候选执行绑定、格式、目标与漂移检查。
