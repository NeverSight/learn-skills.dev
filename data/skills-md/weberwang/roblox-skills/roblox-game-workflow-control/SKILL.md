---
name: roblox-game-workflow-control
description: 管理 Roblox 游戏开发的工作项、范围、实施包、证据与外部授权；在开始跨模块开发、恢复任务、集成交付或检查是否可完成时使用。
---

# Roblox 工作流控制

这是项目工作项与交付记录的唯一控制面；领域技能提出实现和证据，不各自维护第二套全局状态。读取 [控制模型](references/control-model.md)，按需使用本技能的 `scripts/workflow-control.mjs`。

## 开始与恢复

1. 先读已有 `.workflow-control/work-items/`、项目说明和用户当前目标，复用同一工作项；不要为返修重建工作项。
2. 将范围拆成 `PROJECT`、`FOUNDATION`、`SCENE`、`DISPLAY_LAYER`、`INTEGRATION` 或 `RELEASE`。场景含常驻 HUD；弹窗、抽屉、Toast 使用独立显示层工作项，`hostSceneId` 只记录宿主。
3. 普通小修从受影响步骤开始，不强制先完成整个项目流程。六阶段是用户视图，V0–V4 是可见对象的生产闭环；版本 2 记录逐项验收结果和计划检查覆盖，不以目标文案代替完成结论。
4. 生产实施前填入准确目标 Studio、源数据归属、允许文件/实例、实施单元所有者、验证计划与停止条件。
5. 所有 Studio 写入保持单写者；并行代理可以探索、研究、编写不冲突的本地文件或独立审查。

完整项目按[项目依赖与多 Place 契约](references/project-contract.md)维护唯一项目清单、跨工作项 `dependsOn` 与最终集成项，交付前执行 `check-project`；局部小修不强制建立项目清单。多 Place 只在真实需求出现时显式启用，不为单 Place 建立空传送或共享数据系统。

发现证据无法消除且会改变目标、范围、成本、风险、体验或授权的取舍时，按[决策交接](../roblox-development-workflow/references/decision-change-control.md)调用[拷问技能](../roblox-game-grilling/SKILL.md)。工作项用 decisionRefs 引用实际记录；没有必要决策时明确为空数组，不给普通任务增加人工门。未决内容先暂停直接依赖它的写入，闭合后恢复原任务。

## 本地工具

从本技能目录调用，`--repo` 是游戏工程根目录，不能误用技能仓库目录：

```powershell
node scripts/workflow-control.mjs init --repo D:\Games\my-game --id first-loop --type SCENE --objective "完成首个可游玩循环"
node scripts/workflow-control.mjs status --repo D:\Games\my-game --id first-loop
node scripts/workflow-control.mjs check --repo D:\Games\my-game --id first-loop
node scripts/workflow-control.mjs init-project --repo D:\Games\my-game --project-id my-game
node scripts/workflow-control.mjs check-project --repo D:\Games\my-game
```

`init` 只创建新 JSON，不覆盖旧文件；初始化后缺少目标、实施包和证据是预期状态。`status` 和 `check` 只读。`check` 未满足交付门时退出码为 1。字段按 [记录契约](references/record-contract.md) 使用正常文件工具编辑，状态变化要有事实支持。

## 实施与证据

- `planned → implementing → validating → complete`；缺依赖时记录 `blocked`，解除后继续原工作项。工具不自动迁移状态，不执行引擎命令。
- F0 核对用户目标与范围，F1 核对实际交付满足目标，F2 核对 Roblox 领域质量，F3 核对真实验证，F4 核对适用的高影响操作授权。F1/F2 的质量判断由代理或人工完成，不能从 JSON 结构检查推断。
- 实施后先推荐 T0–T3，简述理由、覆盖和命令，再自动运行已授权的普通验证；不把失败改成 PASS。
- 每项证据绑定 workItemId、候选、实际时间、类别、执行上下文、结果、非空产物路径与结论；Studio 证据同时绑定 studioId、Place/Universe 与实际 DataModel。逐条 verification、acceptanceResults 和适用 domainReview 关联当前证据；变更影响行为时更新候选并重验，不计算 SHA，也不为无影响的文案调整重开阶段。
- 失败优先 `repair` 原地修复；只缺有效证据用 `revalidate`；真实范围或上游目标变化才 `return`，记录最小影响面。
- 可见交付按[验证覆盖合同](references/coverage-contract.md)逐行收集精确运行证据，不用泛用 Play 覆盖其他视口、输入、语言或动态情景。资源使用按[资源绑定](references/asset-bindings.md)读取总表并核对当前版本、许可及消费回读；退役或换版先处理受影响消费者。

## 人工与外部边界

V0–V4 每阶段通过 stageReviews 保留可查看产物，并用 visualContractRef 记录布局目标；视觉质量五维和动态情景按真实交付验收。需要产品选择或视觉确认时，先展示具体交付再提问；复用当前目标内已有确认，不反复请求对技术方案的文字确认。项目明确约定逐阶段人工门时设 stagePolicy=manual，按该约定执行。

截图可采集并交给用户检查；默认不自动分析截图或判定显示通过。可见交付完成必须有当前候选的用户确认来源；用户明确授权自动视觉检查时，仍按其验收要求报告结果，不把自动检查记录成用户确认。

上传、发布、付费、真实设备、外部写入和破坏性删除须核对已有的精确授权；初始开发任务、测试等级或另一个代理的消息不能扩大授权。先完成本地可审查交付，再请求必要的最终授权。未经明确要求不建分支或 worktree，不发起真机验收。

交付时区分“记录完整”“Studio 运行通过”“人工显示确认”“已保存”“已发布”；缺失项明确标注 `NOT_RUN` 或 `BLOCKED`。
