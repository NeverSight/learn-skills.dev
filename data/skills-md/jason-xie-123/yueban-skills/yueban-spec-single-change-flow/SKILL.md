---
name: yueban-spec-single-change-flow
description: 只有当用户用自己的话明确、直接要求把本仓库里某一个 pending 的 OpenSpec change 推进到完成时才调用（比如"推进下一个 spec"/"跑一下 spec 流程"/"用 yueban-spec-single-change-flow 跑一下"/直接点名某个 change 要求推进完成）。不要从一般性的 OpenSpec 相关讨论、提到 ROADMAP.md 或 openspec/changes/、或任何间接/启发式信号里推断要用这个 skill——它会触发多 agent workflow 和真实的 commit（不自动 push），必须由用户主动触发，不能靠 AI 推断。不确定用户是不是这个意思时，先问，不要直接调用。
license: MIT
compatibility: 'Requires the openspec CLI (on PATH), git, the openspec-apply-change skill at .claude/skills/openspec-apply-change/SKILL.md (installed by `openspec init`/`openspec update`; invoked via the Skill tool, e.g. `Skill({skill: "openspec-apply-change"})` — do not confuse with the built-in opsx:apply skill), the AskUserQuestion tool, and the Workflow tool (multi-agent orchestration).'
allowed-tools: Bash, Read, Edit, Grep, Glob, Skill, Workflow, AskUserQuestion
---

# OpenSpec 单 change 推进流程

本项目用 OpenSpec 管理产品/工程改动提案。这个 skill 把"选一个 pending change → 多轮校验 spec 文档本身 → openspec-apply-change 实施 → 一次性代码 review → archive → 提交（不自动推送）"这套完整生命周期固化下来，避免每次凭记忆重新拼装。这是一个通用 skill，随 `npx skills` 分发到任意装了 OpenSpec 的项目——下文不假设自己就装在"本仓库"里。

**spec 校验、实施、代码 review 是三个先后独立的阶段，不要混为一谈**：

- **第一步的多轮校验循环审查的是 spec 文档本身**（`proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md`）——这几份文档内部是否自洽、里面对代码库现状的假设是否还成立、任务拆分是否还对应当前代码结构。这一步发生在实施之前，此时 `tasks.md` 里的任务大概率还没做，**审查对象是文档描述本身，不是实施结果**，修复 agent 只改这几份 markdown 文档，不碰其他任何东西。
- **第二步的实施由标准的 `openspec-apply-change` skill 完成**（安装在目标项目的 `.claude/skills/openspec-apply-change/SKILL.md`，由 `openspec init`/`openspec update` 生成，不在本仓库里，通过 `Skill` 工具按名调用，不是相对路径引用），把 `tasks.md` 里的 `- [ ]` 逐条变成真实代码/文档产出。`tasks.md` 中（不限于末尾，验证类任务在实践中可能散落在功能任务附近，只有最终的"跑全量验证命令"收尾任务通常在末尾）按 `openspec/config.yaml` 规则本就要求包含真实的验证类任务，具体是什么验证命令由该 change 自己的 `tasks.md` 决定，这些验证命令本身就是 tasks.md 的一部分，会在这一步被 `openspec-apply-change` 自然执行到——**不需要在它之外再单独安排一轮"门禁验证"**。
- **第三步的一次性代码 review 审查的是第二步实际产出的代码**——正确性、spec 符合度、安全与健壮性、测试质量四个角度并行 review 一次，修复 agent 修一次 blocker/major（改代码和测试、不改 spec 文档、不 commit），修完跑一次构建+测试，不做第二轮 review。它和第一步是两回事：第一步回答"文档写得对不对"，这一步回答"代码写得对不对"。**代码 review 永远不会让流程停下来**：没解决的问题都记成已知缺口写进 commit message 和 `ROADMAP.md`，然后照常进入第四步 `openspec validate` + archive、第五步提交——这套 skill 的目的是让人不用守在执行过程里，review 的结果留给人事后看。

## 什么时候才能调用这个 skill

**只有用户显式、明确地要求推进/执行某个 pending change 的完整流程时，才能调用本 skill**——比如用户直接说"推进下一个 spec""帮我跑一下 xxx 这个 change""用 spec-driven-flow 跑一下"。

**不要**仅凭以下这类间接信号就自行判断要调用本 skill：

- 用户只是在讨论、查看、编辑 `ROADMAP.md`、`openspec/changes/` 目录，或某个 change 的文档内容；
- 用户要求"更新 ROADMAP""重写某个文档""看看这个 change 写了什么"之类与 spec 相关、但并不等于"执行完整生命周期"的任务；
- 通用的"只要有一点可能适用就该用 skill"的默认倾向（参见 `using-superpowers`）**不适用于本 skill**——这是一个会自动跑多轮多 agent workflow、修改代码、真实执行 `git commit` 的高开销、有副作用的操作，必须由用户主动、明确触发，AI 不能自己推断"现在该跑这个了"。

不确定用户是不是这个意思时，先用 `AskUserQuestion` 确认，不要直接开始跑。

**核心原则：一次只做一个 change，做完停下来，不自动连续推进到下一个。** 每个 change 走完 archive+commit 之后，向用户报告结果并等待下一步指示，不要自己接着挑下一个开始。**如果用户要求的是连续做完多个甚至全部待办 change 这种批量场景，那不是本 skill 的职责，改用上层编排 skill [`yueban-spec-roadmap-flow`](../yueban-spec-roadmap-flow/SKILL.md)**——批量场景下由那个 skill 负责挑选顺序、逐个把具体 change 名传给本 skill，以及每个 change 完成后的清单维护；不要在本 skill 里自己实现"连续做完"的循环，也不要在本 skill 里读写任何待办清单（这里的"待办清单"specifically 指 `ROADMAP.md` 的「有依赖关系」「无强依赖」「阻塞中」三个待办小节——唯一的例外是「前置检查」里对「阻塞中」的只读检查；本 skill 收尾阶段仍会追加内容到 `ROADMAP.md` 的「已解决的问题」/「无法自主解决的问题」/「经验总结」三个日志小节，见下方「收尾」一节；两者不冲突，日志追加不算"待办清单读写"）。

## 什么时候不适合用这个 skill

- **change 还有未拍板的 Open Questions**（`proposal.md`/`design.md` 里明确写着需要用户决策的分歧点）：先用 `AskUserQuestion` 定案，不要指望校验循环替你做产品/技术方向判断——review agent 只负责核对"文档本身是否自洽、是否还符合代码现状"，不负责"设计本身对不对"这种需要人拍板的问题。
- **change 本身就是"评估一个外部分支/PR 要不要合并"**（不是从 `openspec/changes/` 里选一个 pending change 来实施）：那是不同的流程（对照检查基线分支当天新增的功能是否会被外部分支的旧结构覆盖、migration 编号冲突、语义合并冲突），这个 skill 的四角度只读评审模型不适用，需要人工设计验证方案。
- **change 涉及生产数据库 migration**（本条是本仓库 `backend/` 技术栈特有的检查，不是 OpenSpec 通用要求；这个 skill 移植到不用同一套 migration 机制的项目时，应替换成该项目自己的等价风险点，或直接删除本条）：正常走这个 skill 没问题，但额外确认新增的 `.up.sql`/`.down.sql` 编号没有和 `backend/db/migrations/` 目录下已有的最大编号冲突（多条开发线各自独立分配编号是常见冲突源），且 down 迁移经过验证能正确回滚。

## Change 被放弃/取消时怎么处理

这是和上面"正常走完流程"完全不同的另一条路径——**不要**套用第四步的 `openspec archive`/手动 mv 流程，那是给"做完了"的 change 用的。用户中途决定"这个 change 不做了/方案作废"时：

1. 先跟用户确认清楚这是真的放弃（不是"先搁置一下，以后可能还做"）——只有明确放弃才走下面的步骤，搁置的话什么都不用动，change 留在原地就行。如果搁置是因为外部前置条件还不具备（方案本身不变），提醒用户/调用方把它在 `ROADMAP.md` 里移到「阻塞中」小节，并写明解除条件和原位置（格式见 [`roadmap-template.md`](../yueban-spec-roadmap-flow/roadmap-template.md)）——同样不是本 skill 的职责。
2. 把 change 目录整个移到 `openspec/changes/archive/`，但用 `$(date +%Y-%m-%d)-abandoned-<change-name>` 命名（注意多了 `abandoned-` 前缀），跟正常完成的 `YYYY-MM-DD-<change-name>` 区分开，避免以后有人误以为它是"做完了"的记录。**不需要**跑 `openspec archive` CLI（那条命令会尝试同步 delta spec 到 `openspec/specs/`，而放弃的 change 从未真正实施，没有 spec 需要同步）。
3. 如果这个 change 在某份待办清单（如 `ROADMAP.md`）里有对应条目，提醒用户/调用方去处理（从待办小节删除、按需记录放弃原因）——**这不是本 skill 的职责**，本 skill 不读写任何待办清单，清单维护统一由调用方自己或 [`yueban-spec-roadmap-flow`](../yueban-spec-roadmap-flow/SKILL.md) 负责。
4. 如果已经产生了任何代码改动（哪怕只是校验循环里的中间修复），先跟用户确认要不要连同 revert，不要留下"半成品代码还在但待办清单里的记录已经不一致"这种断层状态。
5. 正常走 `git add`/`git commit` 提交这些文档改动即可（同样不自动 push），跟第五步的收尾方式一致。

## 输入

**change 名称，必须由调用方显式指定**——本 skill 不读任何待办清单（如 `ROADMAP.md`）来自己挑选要处理哪个 change，也不关心该清单的顺序/依赖结构。如果用户没有明确说要处理哪一个，先用 `AskUserQuestion` 或直接提问确认具体的 change 名称，不要自行读取其他文档代为决定。"按顺序挑一个 pending change 来做"或"连续做完剩下所有的"这类需要读待办清单来批量挑选的场景，由上层编排 skill [`yueban-spec-roadmap-flow`](../yueban-spec-roadmap-flow/SKILL.md) 负责选出具体 change 名后再调用本 skill。

## 前置检查

- 确认 `openspec` 命令本身在 PATH 上（`command -v openspec`）——第四步的 `openspec validate`/`openspec archive`、以及委托给 `openspec-apply-change` 的实施步骤都依赖这个二进制，缺了它会在流程跑到一半才报错，不如提前发现，向用户说明并停下。
- 确认第二步要用到的 `openspec-apply-change` skill 已安装：`test -d .claude/skills/openspec-apply-change || echo "Missing .claude/skills/openspec-apply-change — re-run: openspec update --force"`。这一步必须在第一步的多轮校验循环（Workflow，高 token 消耗）之前做，否则会等整轮校验跑完、进入第二步才发现装不了，白白浪费掉第一步的开销。
- 读 `openspec/config.yaml`：里面的 `rules`（`proposal`/`design`/`specs`/`tasks`）是本仓库对 OpenSpec artifacts 的强制约定（如语言、验证方式、前端改动是否要求端到端测试等），第一步的四个评审角度和修复 agent、第二步的 `openspec-apply-change` 实施都要以它为准绳，而不是只凭经验判断。
- `git status --short` 确认工作区干净，`git fetch origin <base-branch>` 确认本地与远端同步，避免在过期代码上开工（`<base-branch>` 是当前分支所在项目的默认/基线分支，以该项目实际使用的名字为准，不要写死；不确定就先 `git symbolic-ref refs/remotes/origin/HEAD` 或直接问用户）。
- 如果发现远端有本次会话不知情的新提交（尤其是大规模重构、或删除了 `openspec/` 下的目录），先向用户说明情况，不要在不确定的地基上继续；用户明确说"不用管，直接拉最新代码"就照做，不要反复追问。
- 如果 `openspec/changes/ROADMAP.md` 存在、且要处理的 change 列在「阻塞中」小节里：先向用户说明它的阻塞原因与解除条件，确认条件已经满足再开始；用户确认前不进入第一步。这是本 skill 对待办小节唯一的读取，只读不改——把它移回待办小节由用户或 [`yueban-spec-roadmap-flow`](../yueban-spec-roadmap-flow/SKILL.md) 处理，本 skill 在收尾汇报里提醒即可。
- 确认要处理的 change 目录下 `proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md` 齐全（`openspec status --change "<name>" --json` 可以查 `isComplete`）。

## 第一步：多轮校验循环（Workflow 工具）——只审查 spec 文档本身

用 Workflow 工具跑一个「round = 只读评审（全量或增量）→ 单一顺序修复 agent（只处理 blocker/major）」的循环，直到 blocker/major 清零或撞轮次上限，收敛后再统一批量修一次累积的 minor。**这一步在实施之前进行**，审查对象是 `proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md` 这几份文档本身，不是代码实现（此时代码大概率还没写）。修复 agent 也**只修这几份文档**，不碰其他任何东西。

**轮次规则（已由用户拍板，不要再问）：MIN_ROUNDS=1（round 1 若已经是全量且 blocker/major 清零就立刻停，不强制凑够更多轮），MAX_ROUNDS=5（硬上限，撞到就不管是否收敛都强制结束进入下一步）。** **这里写的 1/5 只是复述给人/agent 快速理解用——真正被执行的唯一权威来源是 [`spec-cycle.template.js`](spec-cycle.template.js) 里的常量，这里和那边如果哪天不小心改得不一致了，以 `spec-cycle.template.js` 为准。**

**审查方式：round 1 全量，中间轮次增量，收敛前最后一轮再全量把关一次**——round 1 永远跑全量（下面 4 个并行只读评审角度都跑一遍）；中间轮次改成一个更便宜的**增量复核**：只核对上一轮发现的问题是否真的修好了、这次修复有没有在被改动的文档里引入新的不一致，不重新审查未涉及的部分，成本远低于全量。只要某一轮（不管全量还是增量）查出 blocker/major 数为 0，下一轮不会立刻停——如果这一轮本身就是全量，直接收敛结束；如果是增量，下一轮会被自动升级为全量，用一次完整审查确认"真的没问题"之后才收敛。命中 MAX_ROUNDS 时，无论前面走到哪一轮，最后一轮都会被强制升级为全量，保证最终报告始终来自一次完整审查，不会是增量复核的片面结论。

**停止条件：blocker/major 清零即可退出，不要求零问题；minor 级问题不在轮次里修，收敛后统一批量修一次。** 这是因为评审员总能挑出一些措辞类的 minor 问题，如果要求零问题才能停，几乎每次都会被迫跑满轮次——真正值得为它多跑一轮、反复来回改的只有 blocker/major。每轮发现的 minor 问题会被原样累积，等 blocker/major 真正清零、循环收敛之后，用**一次**修复 agent 统一处理掉，不再对这批 minor 修复单独起一轮复核（信任修复结果，这是收尾式的措辞/细节修正）。如果撞了 MAX_ROUNDS 仍有未解决的 blocker/major，minor 不处理——先解决 blocker/major 再说（同下面"已知坑"一节）。

**产品/技术取舍类分歧按固定顺序自动裁决，不停下来问用户，裁决后默认不再翻案**：像"某个功能点要不要做""某个字段要不要展示"这类没有唯一正确答案、需要判断优先级的问题（区别于"文档写错了"这类事实性错误），修复 agent 按 proposal.md 的 PRD 原文 > openspec/config.yaml 的 rules > 代码库现有实现的既定模式 > demo/原型这个固定优先级独立裁决，把结论和依据追加进 `design.md` 的『Decision Record』小节（没有就新建）。后续轮次的评审 agent 如果发现同一件事已经被裁决过，默认不能重复提出——除非能引用到 PRD 或 config.yaml 的新原文依据，而不是换一种措辞重新表达同一个偏好。这条规则直接针对一个真实发生过的问题：同一个产品取舍分歧在不同轮次被来回改判，白跑了好几轮才靠人工拍板定下来。

round 1 全量评审的 4 个角度：

1. **文档自洽性**：`proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md` 之间是否互相矛盾——`design.md` 里的每条 Decision（含『Decision Record』小节里的裁决记录）是否都体现在 `tasks.md` 的具体任务里；`tasks.md` 是否覆盖了 `proposal.md` 的 Capabilities/Impact 段落承诺的全部范围（有没有承诺了但没拆成任务的遗漏，或任务里做了但 proposal 没提及的范围蔓延）；`specs/**/*.md` 的验收标准是否和 `proposal.md`/`design.md` 一致。
2. **设计前提时效性**：`design.md`/`proposal.md` 里对当前代码库的假设（文件路径、页面/接口数量、依赖的其他 change 是否已落地、数据结构现状）是否还成立——**要去读实际代码库核实，不是拿文档和文档互相比对**。这个 change 立项可能是在依赖的上游 change 落地之前写的，现在代码现状可能已经变化（比如某个前置 change 已经归档、某个文件路径已经改变）。
3. **任务可执行性与规范合规**：`tasks.md` 里每条任务描述是否足够具体、可以被 `openspec-apply-change` 直接执行而不需要额外澄清（模糊的任务会导致下一步实施阶段卡住反复追问）；是否满足 `openspec/config.yaml` 里的 `rules`（尤其 `tasks` 下的强制项，如触及前端网页时验证段是否要求真实浏览器端到端测试，不能只写 `e2e/` 这类纯 API 套件、是否把 commit/PR 这类流程性收尾误写进了 tasks.md）。
4. **测试任务断言充分性**：`tasks.md` 里的验证类任务是否只写了"跑现有测试不报错""跑一遍验证套件"这类泛化描述，还是针对本次新增/变更的具体行为写了有针对性的新断言（比如新增字段在页面上的展示校验、新增交互路径的具体检查点、新增接口的边界条件断言）——泛化描述即使技术上"可执行"，也发现不了本次改动引入的回归，必须记为 issue 要求补充具体断言；已有断言若已经覆盖到位则不需要额外挑刺。**只检查"有没有针对新增/变更行为的断言"这一件事，不要求断言穷尽所有 edge case 或颗粒度足够细**——不能以"可以写得更细/更全"为理由反复提出新 issue。这条同样针对一个真实发生过的问题：断言颗粒度要求没有上限，导致 `tasks.md` 越写越长，实施阶段被迫写出大量非必要的用例。

**round 1 还会顺带并行跑一次一次性的基线探测**：找到项目当前标准的完整验证命令（构建+测试），在改动前的代码库上跑一遍，报告哪些失败是这次 change 实施之前就已经存在的（`baseline` 字段，只读，不修复也不影响本轮 issue 判断）。第二步实施完成后要用到这个结果，见下方"第二步"一节。

每条发现记一条 issue（`severity: blocker|major|minor`、`description`、`location`），并行角度的结果直接汇总（模板不做自动去重——几个角度偶尔会各自报出同一处问题，措辞不完全一样，机械去重容易漏判或误合并；这些重复项会原样进下一步修复 agent 的 prompt，修复 agent 按内容自行识别"这几条其实是同一处"，不需要单独处理，不影响修复结果，只是 prompt 会稍长）。

- 若本轮 blocker/major 数 > 0：跑**一个**顺序修复 agent（不并行，避免多个 agent 同时改同一批文件冲突），按顺序逐条修复这些 blocker/major（**minor 这一轮不碰**，累积到收尾统一处理）——**只编辑 `proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md` 这几份文档**，把过期的设计前提、不自洽的描述、不够具体的任务拆分改到位，遇到产品/技术取舍类分歧按上面的固定顺序裁决并记入决策记录；**不实施任何代码**，也不需要跑 `go build`/`npx tsc` 这类命令（这一步不产出代码，没有可编译的改动）。
- 修复 agent 之后紧跟着跑一次 `openspec validate <change-name>`（确定性的格式检查，不是 LLM 判断）——修复 agent 只保证语义/内容层面改对了，不保证没把 openspec CLI 要求的格式（必需 section、`specs/**/*.md` 里的 MUST/WHEN/THEN 关键字等）改坏。这一步比等到第四步（实施完之后）才第一次跑 validate 更早拦住格式问题，避免带着坏格式去实施。若不通过：再跑一次针对性修复+复检（只修一次，不无限重试）；若复检仍不通过，视为独立于语义 issue 之外的一类未解决问题，带进本轮汇总，不能被"blocker/major 数 = 0"掩盖。
- 若本轮 blocker/major 数 = 0：全量轮直接收敛结束（若已达 MIN_ROUNDS）；增量轮则把下一轮升级为全量，再确认一次才收敛。
- 达到 MAX_ROUNDS 仍未收敛：强制结束（最后一轮已经是全量），未解决的剩余 blocker/major 如实带进下一步的报告；这种情况下 minor 不处理。若还有 blocker 没解决，不要进入下一步，先向用户说明，让用户决定是否可以带着已知缺口进入实施阶段。
- 循环真正收敛（blocker/major 清零）后：如果这一路累积了 minor 级问题，跑一次批量修复 agent 统一处理，再跑一次 `openspec validate` 兜底确认格式没被改坏（不再对这次批量修复单独起一轮 review）。

具体怎么写这个 Workflow 脚本：本 skill 目录下的 [`spec-cycle.template.js`](spec-cycle.template.js) 就是这个模板，已经实现好上面描述的全部逻辑，是本 skill 唯一的权威来源——**不要依赖任何本地临时/缓存路径（scratchpad、`/tmp` 等）里可能残留的历次脚本副本**，那些是会话级临时产物，换一个 session、换一台机器就不存在，不能作为标准流程的一部分。

用法：`Read` 这个模板文件的内容，在你自己的上下文里把其中的 `CHANGE_NAME_PLACEHOLDER`（出现两处：`meta.name` 和 `const CHANGE = '...'`）替换成实际 change 名的字面量，然后把替换后的完整脚本文本通过 `Workflow` 工具的 `script` 参数直接传入（不要用 `scriptPath` 指向仓库里的模板原文——那份文件本身带着占位符，字面量不替换就跑不对；也不要自己先把替换后的内容写成一个新文件再用 `scriptPath` 指向它，没有必要多这一步文件落地）。`Workflow` 工具本身会把每次调用的脚本自动持久化到会话目录、并在结果里返回 `scriptPath`——那是工具自己的实现细节，用于本次调用之后的 resume，不是本 skill 需要维护的产物。

不要依赖 Workflow 的 `args` 运行时传参来传 change 名——直接把 change 名字面量写进脚本文本里传给 `script` 参数，让脚本本身自包含，换一个 session/机器重放同一段脚本文本时行为完全确定，不依赖 `args` 在运行时怎么被传入。（早期版本这里的理由是"观察到 args 间歇性收到字面量 `undefined`，疑似模板替换异常"——但 Workflow 的 `args` 语义是把值原样作为 JS 值暴露给脚本，并不经过脚本文本的模板替换，这个具体机制站不住，也未经独立复现确认；保留字面量替换的做法本身没问题，理由改成"自包含更可靠"，如果之后真的复现出 `args` 的问题，再把这里换成经过验证的实际原因。）

`MIN_ROUNDS`/`MAX_ROUNDS` 模板里已经是 1/5，一般不需要改；如果用户当次明确要求不同的轮次策略，替换文本时一并改这两个值。

## 第二步：实施（openspec-apply-change）

第一步收敛（blocker/major 清零、累积的 minor 也已批量修完）后，spec 文档本身已经核实过是准确的，现在用 `Skill` 工具调用 `openspec-apply-change`（`Skill({skill: "openspec-apply-change"})`，传入 change 名），让它按自己的"逐任务实施循环"把 `tasks.md` 里的任务全部做完。

- 先用 `openspec instructions apply --change "<name>" --json` 看任务级 Progress 的 `remaining`/`complete` 计数与 `state`；如果已经是 `state: "all_done"`，说明上次会话已经实施过，跳过调用，直接进入第三步代码 review（注意这和"前置检查"一节用的 `openspec status --change "<name>" --json` 是两个不同命令：`status` 只报告 `isComplete` 这类 artifact 齐全性，不含任务级进度字段，任务级 `remaining`/`complete`/`state: "all_done"` 只出现在 `instructions apply` 的输出里）。
- `openspec-apply-change` 会自己反复循环直到 `all_done` 或遇到需要人拍板的阻塞（任务描述不清楚、实施中发现设计问题、报错）——**遇到阻塞就按它自己的 Guardrails 停下来问用户，不要替它猜答案硬推进**，这和本 skill"什么时候不适合用"一节里"Open Questions 未定案先问用户"的原则是一致的。
- `tasks.md` 里按 `openspec/config.yaml` 规则要求的验证类任务（不限于末尾）本身就是这一步要执行的任务之一，**不需要额外安排一轮独立的门禁验证**——如果 `openspec-apply-change` 报告某条验证任务失败，那就是这一步的阻塞，按上面的方式停下来问用户，不要跳过验证任务直接标完成。
- 实施完成后，`grep -c "^\- \[ \]" tasks.md` 确认真的是 0（不要只信 `openspec-apply-change` 自己报告的 `all_done`，用文件内容做一次交叉核实）。
- **既有失败一律修复，单独提交**：第一步 Workflow 返回结果里的 `baseline` 字段记录了这次 change 实施之前代码库本就存在的失败（`baseline.failingTests`/`baseline.output`）。`openspec-apply-change` 完成后，如果这次实施过程中遇到的测试/构建失败能在 `baseline` 里对上号，说明它是既有问题、不是本次改动引入的——**不要因为"改动前就有"就放着不管，也不要和本次 change 的实现混在同一个 commit 里**：单独修一次、单独 `git commit`（message 里写明是与 `<change-name>` 无关的既有失败修复），修完再继续走后面的步骤。如果某个失败在 `baseline` 里查不到、看起来是本次改动新引入的，那按正常的实施阻塞处理（回到 `openspec-apply-change` 自己的循环里解决），不要混淆这两类失败。**`baseline` 字段本身可能是 `null`**——round 1 的基线探测和这个 change 自己一样，也是一次 agent 调用，同样可能因为 API 重试耗尽而失败（见下方"已知坑"一节）；`baseline` 为 `null` 时，不能假设"没有既有失败"，也不能拿 `baseline.failingTests` 直接取值（会报错）——按"这次没能拿到基线快照"处理，第二步遇到的失败无法直接对照判断新旧，需要更谨慎地人工核实（参照下面"不要在没有对照组的情况下断言"这条已知坑里的手动核对方式）。

## 第三步：一次性代码 review（Workflow 工具）——审查第二步产出的代码，不阻塞流程

第二步完成、`tasks.md` 全部勾选后，先对实现代码做**一次** review 再进入 validate/archive/提交。**已由用户拍板：代码 review 只跑一次、修一次，不管结果如何都不让流程停下来**——这套 skill 的目的是让人不用守在执行过程里，review 没解决的问题记成已知缺口，留给人事后看。

流程（全部在 [`code-review.template.js`](code-review.template.js) 里，是唯一的权威来源）：

1. **并行 review 一次**：4 个只读评审角度，同时并行跑一次项目标准的构建+测试拿到当前状态。
   - **正确性**：逻辑错误、边界条件、错误处理、并发与资源泄漏、对既有调用方的破坏。
   - **spec 符合度**：`tasks.md` 勾选了的任务是否真的做了、`specs/**/*.md` 的每条 Requirement/Scenario 是否被满足、是否违背 `design.md` 的决策（含『Decision Record』）、有没有超出 `proposal.md` 的范围蔓延。
   - **安全与健壮性**：输入校验、注入、鉴权越权、敏感信息、migration/数据变更的安全性、外部调用的超时重试。
   - **测试质量**：新增测试是否真的断言了新增/变更的行为，有没有跳过/删除既有测试或放宽既有断言。和第一步角度 4 一样，只看"有没有有效断言覆盖"，不以"可以写得更细"为理由提 issue。

   严重程度：**blocker** = 一定会出错且影响主路径/数据/安全（含构建或测试失败、MUST 级需求没实现、任务勾选了没做）；**major** = 现实可触发的缺陷、新增行为没有测试断言覆盖、明显违背 `design.md`；**minor** = 不影响行为的问题。每条 blocker/major 都必须写出具体触发场景，给不出触发场景的猜测不报。
2. **修一次**：一个修复 agent 处理全部 blocker/major（构建/测试没通过也算一条 blocker），逐条报告处理结果——`fixed`（已修）/ `disputed`（误报，附具体理由）/ `not_fixed`（真实存在但这次修不了，附原因）。护栏：不能靠删除/跳过测试、放宽断言来"修"，不改 `proposal.md`/`design.md`/`specs/**/*.md`，不把已勾选任务改回未勾选，不 commit/stash/reset。**minor 只记录、不修**——没有第二轮 review，顺手的"小清理"是没人审过的新 bug 来源，不值得。
3. **修完由一个独立 agent 再跑一次构建+测试**——不信修复 agent 自己说的"已经跑过、通过了"，改代码的 agent 不给自己打分。修坏了（出现 `baseline` 之外的新失败）给一次针对性修复，再独立跑一次；还是不行也不停，记进已知缺口。评审 agent 只做静态审查、不跑构建/测试，避免和并行的构建探测抢端口或构建目录、制造假失败。
4. **不再做第二轮 review**：修复本身没有被重新审查，构建+测试是对修复的唯一检查，所以留痕里"已修"的条目都标成"未经复核"。

**审查范围 = 从 `REVIEW_BASE` 到当前工作区的全部改动**（`git diff <REVIEW_BASE>` 加上未跟踪的新文件）。**`REVIEW_BASE` 就是跑这个 Workflow 之前的 `git rev-parse HEAD`**：本 flow 的实现代码到第五步才提交，所以此刻它全部是未提交的改动，都在范围里；第二步单独提交的既有失败修复在 `REVIEW_BASE` 之前，刻意不在范围里——它们必须和本 change 的提交分开，修复 agent 不能去改它们（模板里已经这么要求），否则改动会在第五步被 `git add -A` 混进本 change 的提交。换了会话续跑时也一样取当时的 HEAD，不需要回溯历史提交。

`git status --short` 里没有 `openspec/changes/<name>/` 之外的改动（纯文档/纯 spec 类 change）时，跳过这一步，直接进入第四步。

**用法**：`Read` 模板，把 `CHANGE_NAME_PLACEHOLDER` 替换成 change 名、`REVIEW_BASE_PLACEHOLDER` 替换成 `REVIEW_BASE`（此刻 `git rev-parse HEAD`）的完整 SHA，按模板里的注释用第一步返回的 `baseline` 填 `BASELINE_NOTE`（让评审和修复 agent 不把既有失败当成本次问题），然后通过 `Workflow` 的 `script` 参数直接传入。其余规则同第一步（不用 `scriptPath` 指向模板，不先落地成新文件，不用 `args`）。

**跑完 Workflow 再 `git rev-parse HEAD` 和 `REVIEW_BASE` 比一次**：不一样说明有 agent 违规 commit 了（模板禁止 commit/stash/reset）。不用停：review 范围按 `REVIEW_BASE` 算，这些改动都在范围内；在最后的汇报里列出这些提交（`git log --oneline <REVIEW_BASE>..HEAD`），让用户事后看一眼。

**拿到返回结果后，不管是什么都继续进入第四、五步**，只负责把留痕写对。`records` 里的每一行都由模板确定性生成，**原样使用，不要改写措辞**：

| 字段 | 写到哪里 |
|---|---|
| `records.knownGaps`（没处理/修不了的 blocker/major、构建/测试仍未通过或结果未知、没拿到结果的评审角度） | commit message 的 "Known gaps" 段、`ROADMAP.md`「无法自主解决的问题」，汇报时放在最前面；非空时 commit 标题行末尾加 ` [known gaps]` |
| `records.fixed`（已修，未经复核） | commit message、`ROADMAP.md`「已解决的问题」 |
| `records.disputed`（被驳回的误报及理由） | commit message，留给人复查驳回是否站得住 |
| `records.minors`（未修的 minor） | 只写进 commit message |

构建/测试失败的提交只在本地、不会推送；如果是 `yueban-spec-roadmap-flow` 批量推进，下一个 change 第一步的基线探测会把它列为既有失败，按第二步"既有失败一律修复，单独提交"的规则被修掉。

## 第四步：openspec validate + archive

```bash
openspec validate <change-name>
```

如果校验失败：不要跳过或强行 archive，先读报错定位是哪个文件（`proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md`）格式不对，修正后重新跑 `openspec validate` 直到通过，再继续下一步；如果报错内容本身看不懂或疑似 openspec CLI 的问题而非本 change 的格式问题，向用户说明情况再决定怎么处理。

确认 tasks.md 全部任务已勾选（`grep -c "^\- \[ \]"` 应为 0）。

**用 CLI 自带的 `archive` 命令，不要手写 `mkdir`/`mv`/复制合并 spec 文件**——CLI 已经原生实现了这件事，手写等于自己重新拼一遍逻辑，容易漏步骤：

```bash
openspec archive <change-name> -y
```

`-y` 跳过交互式确认提示——agent 环境无法响应交互式输入，不加这个参数命令会卡住等待。默认行为已经包含：validate 一遍（和上面单独跑的那次重复无害，是双重保险）、把该 change 的 delta spec 同步合并进 `openspec/specs/<capability>/spec.md`（新增能力用 `## ADDED Requirements` 提升成正式 baseline，修改/移除的能力做增量合并，不会整份覆盖丢掉其他未改动的 Requirement）、把变更目录移到 `openspec/changes/archive/YYYY-MM-DD-<change-name>`。

跑完之后**必须**用 `git status`/`git diff openspec/specs/` 确认 spec 确实被同步了（比如新增能力对应的 `openspec/specs/<capability>/spec.md` 真的被创建/修改了）——不能只看命令退出码 0 就假设同步生效，这条核实习惯即使改用 CLI 之后仍然值得保留。

只有该 change 确实是纯基础设施/工具/文档类改动、`openspec/changes/<name>/specs/` 目录本就不存在或为空时，才加 `--skip-specs` 跳过 spec 同步——先确认这个判断站得住，不要图省事乱加。

## 第五步：提交（不自动推送）

**只 commit，不 push**——不管当前检出的是基线分支、feature 分支还是某个隔离 worktree，直接在当前分支上提交即可；什么时候把这些提交推到远端、推到哪个分支、要不要先合并回基线分支，都交给用户自己决定，本 skill 不替用户做这个判断。

```bash
git add -A
git status --short   # 过一遍确认没有意外文件被带进来
git commit -m "$(cat <<'EOF'
<type>(<scope>): <一句话概括这次改动做了什么>[ [known gaps]——records.knownGaps 非空时加]

<正文：说清楚为什么改、第一步校验中发现并修正了什么真实问题（不是简单复述 tasks.md）、
第二步实施跑了什么验证、结果如何。>

<第三步返回的 records 各字段非空时，各起一段原样贴入，不要改写：
Known gaps (code review):
- <records.knownGaps 的每一行>
Fixed by code review (unreviewed):
- <records.fixed 的每一行>
Disputed review findings:
- <records.disputed 的每一行>
Minor findings (not fixed):
- <records.minors 的每一行>>

Archives <change-name> -> openspec/specs/<capability>.
EOF
)"
```

提交信息要老实反映校验和代码 review 中的真实发现（哪怕是"立项时的技术前提已过期，实测后改了设计"这种），不要只写"implement change per tasks.md"——这是本仓库这套流程的价值所在：让校验轮次挖出来的东西留下痕迹。

## 收尾

**第五步提交之前**，先把这一轮真实发生的发现追加进 `openspec/changes/ROADMAP.md`（结构参照 [`roadmap-template.md`](../yueban-spec-roadmap-flow/roadmap-template.md)）的日志小节，随第五步 `git add -A` 一起提交，不需要额外单独提交：

- **「已解决的问题」**：追加一行 `- YYYY-MM-DD [change-name] <描述>`，内容是第一步 4 个评审角度实际发现并修复了什么（尤其是纠正了立项假设、补齐了测试断言这类真实发现），以及第三步返回的 `records.fixed`（每行前面加上 `- YYYY-MM-DD ` 原样追加，不要改写）。
- **「无法自主解决的问题」**：如果这一轮曾经用 `AskUserQuestion` 停下来问用户（Open Questions 未定案、修复方案有分歧等），追加一行 `- YYYY-MM-DD [change-name] <问了什么、用户答复是什么>`——即使当场就解决了，也要记录这个决策点，不因为"已解决"就略过。第三步返回的 `records.knownGaps` 非空时，把每一行前面加上 `- YYYY-MM-DD ` 原样追加到这里，不要改写措辞。
- **「经验总结」**：只在这一轮产生了跨 change、跨轮次都适用的通用流程经验时才追加一条，不强制每次都写。

**这是对上面"本 skill 不读写任何待办清单"这条原则的限定例外**：只追加这三个日志小节，不触碰「有依赖关系」「无强依赖」「阻塞中」这三个由 `yueban-spec-roadmap-flow` 独占维护的待办小节本身——这三个小节的增删仍然完全不是本 skill 的职责。

日志追加完成后，向用户报告：第一步的轮次数与是否收敛、真实发现的问题、第二步实施/验证结果、第三步代码 review 的结果（`records.knownGaps` 放在汇报最前面单独列出；已修、被驳回的问题也列出来供人复查；review 期间如果多出了 agent 违规的提交，也列出来）、archive 后的 commit hash，并提醒改动**只提交到了当前分支，尚未推送**，是否推送、推到哪里由用户自己决定。如果这个 change 在 `ROADMAP.md` 的「有依赖关系」「无强依赖」「阻塞中」待办小节里有对应条目，提醒用户/调用方去处理（在「阻塞中」的，说明它是在前置检查确认解除条件后才推进的）——这三个小节的维护仍然不是本 skill 的职责。

然后**停下来**，问是否继续下一个 change——不要自己接着往下做。**例外**：如果本次是被 [`yueban-spec-roadmap-flow`](../yueban-spec-roadmap-flow/SKILL.md) 通过 `Skill` 工具调用的（批量推进场景），不要在这里停下来问用户——按上一段完成汇报后，直接把控制权交还给调用方，由它按自己第 6 步的规则决定是否继续下一个 change；这条"停下来问"的默认限制只在**被用户直接触发**时生效。

## 已知坑

- **archive 时容易漏删旧目录 / 漏同步新 spec**：`git status` 确认 `mv` 后的新旧路径都被正确 add/remove，不能只信 `openspec archive` 命令的输出。
- **第一步 Workflow 返回的 `unresolvedBlockers` 字段**：撞到 MAX_ROUNDS 仍未收敛时，检查这个字段（最后一轮——一定是全量轮——里 severity=blocker 的 issue）——非空就不要直接进入第二步实施，先向用户说明还有哪些 blocker 级的文档问题没解决，blocker 通常意味着任务拆分本身不可执行，带着它去实施大概率会卡住或做错方向；只有 major/minor 级别的剩余问题可以酌情带着已知缺口继续。
- **第一步 Workflow 返回的 `unresolvedValidateFailure` 字段**：最后一轮 `blockerMajorCount > 0`（validate 因此实际跑过）却没能拿到明确的通过结果时，这个字段为 `true`——既包括"`openspec validate` 修复重试一次后仍未通过"，也包括"validate 这个 agent 调用本身失败，没能拿到结果"这两种情况，两者都不能默认"应该是没问题"。为 `true` 时同样不要直接进入第二步实施，先向用户说明具体情况（validate 报错在 `roundLog` 最后一项的 `validateOutput` 里；agent 调用失败则没有 `validateOutput`，需要向用户说明是哪一步的调用没拿到结果），不能假设"`blockerMajorCount` = 0"就等于文档没问题——这个字段本来就只在有 blocker/major 时才可能非 null。
- **产品/技术取舍类分歧如果被反复提出，先查 `design.md` 的『Decision Record』小节**：按规则，评审 agent 发现同一件事已经裁决过时，默认不该重复提出，除非引用到 PRD/config.yaml 的新原文依据。如果观察到同一个分歧在不同轮次来回改判，多半是评审 agent 没遵守"无新证据不翻案"的约束，需要人工核实分歧本身，不能默认最新一轮的判断就是对的。
- **第一步 Workflow 返回的 `pendingMinorsFixed` 为 `null` 不代表"没有 minor 问题"**：只有循环真正收敛（`fullyConverged: true`）且确实累积过 minor 才会有值；如果撞了 MAX_ROUNDS 仍未收敛，minor 不会被处理，`pendingMinorsFixed` 保持 `null`，这是预期行为，不是遗漏。
- **第一步的修复 agent 越权碰其他文件**：模板的修复 agent prompt 已经明确限定只改 `proposal.md`/`design.md`/`tasks.md`/`specs/**/*.md`，如果发现某次修复实际改动了这 4 类文档之外的任何文件（`git status` 能看出来），说明 agent 没有遵守边界，需要人工核实这些改动是否合理，不能默认它是对的。
- **第三步的修复 agent 越界**：模板要求它不改 `proposal.md`/`design.md`/`specs/**/*.md`、不 commit/stash/reset、不靠删测试或放宽断言来"修"问题。多出来的提交靠 Workflow 跑完后的 `git rev-parse HEAD` 和 `REVIEW_BASE` 比对发现（不要用 `git log -1`，它区分不出第二步单独提交的既有失败修复）；测试文件的删改用 `git diff <REVIEW_BASE> --stat` 扫一眼。越界了就人工核实这些改动是否合理，不能默认它是对的。
- **第三步大量驳回（`disputed`）要人工看一眼**：驳回让修复 agent 不必硬改误报，但也可能被它用来回避真问题。驳回理由写得空泛（没有引用具体代码位置）或者被驳回的是 blocker 时，在汇报里点出来让用户判断。
- **第三步的评审和实施是同一个底层模型**：新上下文能可靠抓到漏做的任务、明显的 bug 和测试问题，但抓不到实施 agent 和评审 agent 恰好共有的误解。而且只 review 一次、修复本身没有被再审查（只跑了构建+测试）。它能降低风险，不能代替人看 diff——所以第五步只 commit 不 push，推送前的最终把关仍然在用户手里，`records` 就是留给这次把关看的。
- **`openspec-apply-change` 报告 `all_done` 不等于真的全部完成**：第二步末尾用 `grep -c "^\- \[ \]" tasks.md` 交叉核实，不要只信它自己的进度汇报。
- **workflow 里某个 agent 因 API 错误重试耗尽失败（`StructuredOutput retry cap exceeded`）不等于整轮作废**：全量轮里其余并行 agent 的结果仍然有效，通常不影响该轮结论；增量轮只有唯一一个 agent，如果它失败，本轮会按 0 issue 处理，但下一轮会被自动升级为全量兜底，不算漏检，只是浪费一轮。如果同一个 change 反复在同一个 agent 上失败，要向用户报告而不是无限重试。
- **不要在没有对照组的情况下断言"这是本次改动引入的问题"**：第一步 round 1 已经并行跑过一次 `baseline` 探测（见"第一步"一节），第二步实施中遇到 lint/build/测试报错时先对照这个 baseline，能对上号的就是既有问题（按"第二步"一节单独修复、单独提交），避免把既有技术债误判成本次改动的缺陷、或反过来把本次改动的真实问题当成"无关的历史遗留"放过；`baseline` 只是实施开始前的一次性快照，如果实施过程本身改了测试/构建配置，仍要以实际跑到的结果为准去核对，不能机械地假设 `baseline` 列出的失败原样不变。`baseline` 探测本身也是一次 agent 调用，同样可能因 API 重试耗尽而 resolve 成 `null`（和其它并行评审 agent 一样）——为 `null` 时不代表"没有既有失败"，只是"没能拿到基线快照"，此时判断新旧失败只能靠人工核对（比如 `git stash`/对比 merge-base 的干净检出），不能跳过这一步直接假设都是本次改动引入的。
