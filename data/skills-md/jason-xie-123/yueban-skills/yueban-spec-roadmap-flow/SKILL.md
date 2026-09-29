---
name: yueban-spec-roadmap-flow
description: 只有当用户用自己的话明确要求把本仓库 openspec/changes/ROADMAP.md 里整条待办全部推进完成时才调用——不是只处理一个 change，比如"把 ROADMAP 剩下的都跑完"/"连续做完剩下所有的 spec"。不要从一般性 OpenSpec 讨论、提到 ROADMAP.md、或要求处理单个 change 的场景里推断适用（单个 change 请用 yueban-spec-single-change-flow）。这是一个持续数小时、高 token 消耗、多 agent、反复 commit（不自动 push）的操作，必须由用户主动触发，不能靠 AI 推断。不确定就先问。
license: MIT
compatibility: Requires the openspec CLI (on PATH) and the yueban-spec-single-change-flow skill. This skill itself never calls Workflow directly (see allowed-tools below); yueban-spec-single-change-flow uses Workflow internally when this skill delegates each change to it via the Skill tool.
allowed-tools: Bash, Read, Edit, Grep, Glob, Skill, AskUserQuestion
---

# OpenSpec 全量 ROADMAP 推进

本项目用 OpenSpec 管理产品/工程改动提案，`openspec/changes/ROADMAP.md` 记录当前所有 pending change。这个 skill 负责把整个 ROADMAP 待办清空，是 [`yueban-spec-single-change-flow`](../yueban-spec-single-change-flow/SKILL.md)（只处理**一个** change）的上层编排版本。这是一个通用 skill，随 `npx skills` 分发到任意装了 OpenSpec 的项目——下文不假设自己就装在"本仓库"里。

## 什么时候才能调用这个 skill

**只有用户显式、明确地要求把 ROADMAP 剩下的 change 连续跑完时，才能调用本 skill**——比如用户直接说"把剩下的 spec 都跑完""连续做完剩下所有的"。

**不要**仅凭以下这类间接信号就自行判断要调用本 skill：

- 用户只是在讨论、查看、编辑 `ROADMAP.md`、`openspec/changes/` 目录，或某个 change 的文档内容；
- 用户要求处理**某一个具体** change（那是 `yueban-spec-single-change-flow` 的场景，处理完一个就该停下来汇报，不能因为调用了本 skill 而擅自升级成"顺便都做完"）；
- 通用的"只要有一点可能适用就该用 skill"的默认倾向（参见 `using-superpowers`）**不适用于本 skill**——这是一个会持续数小时、反复跑多 agent workflow、反复修改代码、反复真实 `git commit` 的高开销、有副作用的操作，必须由用户主动、明确触发。

不确定用户是不是这个意思时，先用 `AskUserQuestion` 确认，不要直接开始跑。

## 核心原则

- **这是唯一允许"连续做完剩下所有 change"的场景**——`yueban-spec-single-change-flow` 自身默认一次只做一个就停，本 skill 调用它时可以显式豁免这条默认限制（因为用户在调用本 skill 时已经表达了"连续做完"的意图），但仍然遵守它的其它规则（一次只处理一个 change、不并行 apply 有文件重叠风险的 change）。
- **权限不预先固化**：本 skill 不预设"生产/测试数据库操作、CI/CD 操作均无需确认"这类标准权限。如果某个 change 涉及生产数据存量数据排查/迁移等敏感操作，仍按 `yueban-spec-single-change-flow` 及仓库一般准则的要求，在当次对话里向用户确认后再执行，不能因为在跑本 skill 就默认已经获得授权。
- **每完成一个 change 都要留痕**：进度体现在 `ROADMAP.md`（待办小节由本 skill 第 6 步自己更新；`yueban-spec-single-change-flow` 不维护待办小节，只在前置检查里只读「阻塞中」、在第五步追加日志小节）和每次 commit 里，本 skill 不额外维护一份平行的执行日志文档——不要在仓库里新建 `docs/YYYY-MM-DD-*.md` 之类的进度记录文件。
- **中途遇到需要用户拍板的事，暂停并问，不要猜**：某个 change 的 Open Questions 未定案、ROADMAP 依赖描述与代码现状不一致、发现真实 bug 但修复方案有分歧等，都要停下来用 `AskUserQuestion` 或直接提问，等回复后再继续。

## 清空 ROADMAP 待办

1. 先确认 `openspec` 命令本身在 PATH 上（`command -v openspec`）——本 skill 后续每处理完一个 change 都要靠它间接触发的 `openspec-apply-change`/`openspec validate`/`openspec archive`，缺了这个二进制会在流程跑到一半才报错，不如提前发现，向用户说明并停下。
2. 读 `openspec/changes/ROADMAP.md`（结构参照 [`roadmap-template.md`](roadmap-template.md)）。**文件不存在时**：说明这个项目还没有用这套 ROADMAP 机制管理待办（或者所有 change 都已处理完、之前从未创建过），不要凭空新建一份就当作"暂无待办"直接结束本 skill——向用户确认清楚现在到底有没有 pending change 需要处理、要不要参照 [`roadmap-template.md`](roadmap-template.md) 新建一份。
3. **轻量核实顺序/依赖描述是否还符合代码现状**（只核实排序/冲突相关的事实，不对每个 change 的完整设计前提做深度审计——那是 `yueban-spec-single-change-flow` 第一步评审角度1、3 在真正执行到该 change 时才做的事，提前几个小时做同样的事到轮值时也会过期，纯浪费）：
   - 「有依赖关系、需要按顺序执行」小节里标注的前置 change，核实是否真的还没完成（比如去看对应 capability 是否已在 `openspec/specs/` 下、或代码是否已体现该前置改动）。
   - 「无强依赖，可随时执行 / 穿插」小节里的条目，快速过一遍是否有未被文档记录、但实际会改到同一批文件/同一个数据结构的冲突（不需要逐行比对设计文档，重点看条目描述里提到的具体文件/结构，扫一眼现状是否仍如此）。
   - 发现描述与代码现状不一致（顺序判断错误、遗漏的文件冲突、某个"待实施"的 change 其实已经部分/全部实现）：**直接按代码现状更新 `ROADMAP.md`，不用停下来问用户**——以代码为准，把过期的顺序/冲突描述改对；如果是"已全部实现"，按第 6 步的方式直接从对应小节删掉该条目（`ROADMAP.md` 不再保留归档历史，见第 6 步），commit message 里写明"核实时发现已在代码中实现，跳过 `yueban-spec-single-change-flow` 流程"。更新完照常继续核实/处理下一项，不因为这类发现而暂停等待。
     - **例外**：如果某个"待实施"的 change 只是**部分**实现（不是全部），这通常意味着之前的实施半途而废或有缺陷，而不是单纯的文档滞后——这种情况不能靠猜测决定"当作已完成/当作未开始"，仍然要停下来向用户说明具体缺了什么，等用户拍板（补完剩余部分/重新走完整流程/其它处理方式）。
   - 「阻塞中，前置条件满足前不实施」小节（若存在且非空）里的条目，看一眼解除条件现在是否已经满足。能从代码或仓库核实的（比如依赖的外部库版本已发布、前提改动已在别的仓库落地）直接核实；业务条件（某个业务已上线、他方已交付等）从仓库里核实不了，问用户。条件满足时，**先问用户是否移回**，不要自己移：这一节的条目是人为判断暂缓的，和上面"描述过期直接改"不是一回事。用户同意后，按条目里记录的「原位置」移回「有依赖关系」或「无强依赖」（原位置前后的 change 已经变了的，按条目记录的前置/后续关系重新确定插入位置，拿不准就问用户），单独 commit（`docs(roadmap): unblock <change-name>`），再照常处理。
4. 先处理「有依赖关系、需要按顺序执行」小节（若非空），严格按记录顺序，不能跳过未完成的前置项——**列表顺序就是执行顺序**，其中可能有用户为没有硬依赖的 change 指定的先后，同样照做，不要按编号或自己的判断重新排序。
   - **遇到外部前置条件不满足的 change**（本步和第 5 步都适用。核实时或实施时发现它依赖的业务条件、他方交付、需要人工完成的前提还不具备——区别于 Open Questions 未定案。实施时才发现的，子流程第二步会以 `openspec-apply-change` 阻塞中止的形式停下，这种情况按这里处理，不按第 6 步的"子流程失败"处理）：停下来向用户说明具体缺什么。用户确认暂缓后：
     - 如果已经进入实施、工作区里留有这个 change 的未提交改动（`git status --short` 非空），先问用户怎么处理——丢弃、`git stash`，还是提交到一条单独的 WIP 分支——不要自己决定，也不要把这些改动混进下面的 roadmap commit。处理完工作区必须是干净的，否则下一个 change 的前置检查会被挡住。
     - 把它移到「阻塞中」小节（没有就按 [`roadmap-template.md`](roadmap-template.md) 新建），写明阻塞原因、解除条件和原位置（在哪个小节、排第几、前置和后续 change 各是谁——移回时要靠它恢复顺序），单独 commit（`docs(roadmap): block <change-name>`），然后继续后面的项。
     - 排在它后面、又依赖它的 change 同样不能做：一并向用户说明，由用户决定一起移入「阻塞中」（每条同样记下原位置）还是在这里停下（停下时照常走「收尾」汇报）。
5. 该小节清空后，处理「无强依赖，可随时执行 / 穿插」小节。默认**串行**逐个处理（**REQUIRED SUB-SKILL:** 从 `ROADMAP.md` 里取出具体的 change 名，通过 `Skill` 工具调用 [`yueban-spec-single-change-flow`](../yueban-spec-single-change-flow/SKILL.md) 并**显式传入该 change 名**，完整走完 校验 spec 文档→openspec-apply-change 实施→代码 review→archive→commit 生命周期——`yueban-spec-single-change-flow` 本身不读、也不维护 `ROADMAP.md` 的「有依赖关系」「无强依赖」两个待办小节——它只认调用方显式传入的 change 名，挑选顺序和「有依赖关系」「无强依赖」「阻塞中」三个待办小节的增删都是本 skill 自己的职责；但它第五步的提交**会**写 `ROADMAP.md`（追加底部「已解决的问题」「无法自主解决的问题」「经验总结」三个常驻日志小节，见第 6 步说明），这部分不算"不读写"的例外）；只有用户额外明确要求"并行加速"时才考虑分批并行，且分批前必须先核实候选 change 之间是否有文件级重叠（同一文件的不同区块也算重叠），有重叠的必须错开，不能真并行改代码。遇到外部前置条件不满足的 change，按第 4 步「遇到外部前置条件不满足的 change」那条处理。
6. 每个 change 走完 `yueban-spec-single-change-flow` 的第五步（提交，不自动 push）后，**由本 skill 自己更新 `ROADMAP.md`**：从「有依赖关系」或「无强依赖」对应小节删掉该 change 的条目——这两个待办小节不再保留已归档 change 的历史记录（见文件顶部「实施方式」一节的说明），完成的 change 直接删除条目，不额外新增"已归档"子小节去记录它曾经存在过。真正需要长期沉淀的发现（校验中修了什么、卡在哪个决策点问过用户什么、有没有推翻/修正立项时的技术假设）已经由 `yueban-spec-single-change-flow` 在它自己第五步的提交里，追加进 `ROADMAP.md` 底部「已解决的问题」「无法自主解决的问题」「经验总结」三个常驻日志小节（结构参照 [`roadmap-template.md`](roadmap-template.md)）——本 skill 这一步不重复处理这三个日志小节，只负责从「有依赖关系」「无强依赖」两个待办小节里删掉已完成的条目（「阻塞中」的移入移出见第 3、4 步）。**这次 ROADMAP.md 更新本身必须单独 commit**（`git add openspec/changes/ROADMAP.md && git commit -m "docs(roadmap): remove <change-name>, archived"`，同样不自动 push）——这一步发生在 `yueban-spec-single-change-flow` 第五步的 commit 之后，不在那次 commit 范围内，如果不单独提交，这处改动会以未提交状态留在工作区，下一个 change 走 `yueban-spec-single-change-flow` 前置检查的 `git status --short`（要求工作区干净）就会被它挡住。更新+提交完 `ROADMAP.md` 后直接继续处理下一个 pending change，不用等用户确认——这是本 skill 存在的意义（用户已经在触发本 skill 时表达了"连续做完"的意图）。**但每完成一个 change 后，都暂停一下向用户汇报一次进度**（刚处理完的 change 名、commit hash、接下来还剩几个）再继续——这不是要用户批准继续（那会违背本 skill"连续做完"的存在意义），只是不能让好几个小时、好几次未经人看过 diff 的本地提交全程零可见性（子流程第三步的代码 review 是同一个模型做的，不能代替人看 diff），给用户一个能随时叫停的检查点。汇报时如果该 change 的代码 review 留下了已知缺口（commit 标题带 ` [known gaps]`），把遗留项一并列出来——代码 review 按设计从不让流程停下，这里的汇报就是这些缺口被人看到的地方。如果某个 change 因为 Open Questions 未定案而卡住，向用户提问，拿到答复前不要跳过它去做后面的（除非用户明确说"先跳过这个，做完其它的再回来"）。**子流程本身没能走完全程**（第一步校验反复撞到轮次上限仍有未解决的 blocker、或第二步 `openspec-apply-change` 遇到阻塞而中止；第三步代码 review 不在此列，它按设计从不阻塞；因外部前置条件不满足而中止的也不在此列，按第 4 步移入「阻塞中」）同样要暂停、向用户说明失败详情——不能把这个 change 标记为已完成写入 `ROADMAP.md`，也不能跳到下一个 change 去，处理方式和"Open Questions 未定案"一致：等用户拍板（跳过/调整方案/终止本 skill）后再继续。
7. `ROADMAP.md` 的「有依赖关系」和「无强依赖」两个小节都清空后，本 skill 结束。「阻塞中」小节里还有条目不影响结束——它们本来就不在批量推进的范围内。

## 收尾

两个待办小节清空后，或者用户中途决定停下时，向用户汇报：共处理了多少个 change（列名字+各自的 commit hash，并提醒这些 commit 都还只在本地、尚未推送，是否推送由用户自己决定）；中途停下的，再列出两个待办小节里还剩哪些 change 没处理。全程如果被某个 change 的 Open Question 卡住过，也一并说明当时是怎么决定的。「阻塞中」小节还有条目时，逐条列出 change 名、阻塞原因与解除条件，提醒用户条件满足后再把它们移回待办小节——这是这些条目被人看到的地方，不列出来很容易被遗忘。

## 已知坑

参见 [`yueban-spec-single-change-flow`](../yueban-spec-single-change-flow/SKILL.md) 的"已知坑"一节。额外补充三条本 skill 自己层面的坑：

- **"阻塞"、"Open Questions 未定案"与"放弃"是三回事**：阻塞是外部前置条件还不具备，方案本身没问题，移到「阻塞中」，条件满足后照原方案实施；Open Questions 未定案是方案还要人拍板，停下来问，拿到答复前不跳过（第 6 步）；放弃是方案不做了，按 `yueban-spec-single-change-flow`「Change 被放弃/取消时怎么处理」归档为 `abandoned-`。不要把一个 change 移到「阻塞中」来绕开没定的 Open Questions，也不要把长期阻塞的 change 当作放弃处理。

- **"无强依赖"不等于"能安全并行"**：ROADMAP 判定无执行顺序依赖的两个 change，仍可能改同一个共享文件的不同区块（比如同一个前端菜单数组）。默认串行能完全规避这个问题；如果为了速度改成并行，必须先做文件级重叠核实，不能只看 ROADMAP 的依赖标注。
- **批次并行计划会被执行中新增的文件打破**：即使事前用静态重叠分析规划好了"互不冲突的批次"，某个 change 实际执行中新建的文件也可能被同批次另一个 change 引用到，产生计划外的依赖。这类情况要靠每个 change 自己的门禁验证（真实 build/test/e2e）兜底探测，不能完全信任事前的批次划分。
