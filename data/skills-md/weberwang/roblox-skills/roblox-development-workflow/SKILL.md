---
name: roblox-development-workflow
description: 使用 Roblox Studio 插件编排完整游戏开发或跨模块功能，从需求、工程基线到场景、界面、玩法、数据、QA 和发布候选；局部领域任务只加载对应技能。
---

# Roblox 游戏开发编排

以 [工作流控制](../roblox-game-workflow-control/SKILL.md) 管理唯一工作项，按 [插件路由](references/studio-plugin-routing.md) 执行真实 Studio 操作。延续 Unity 工程的阶段、实施包与证据纪律，采用 Roblox 原生数据与执行边界。

## 最短路径

1. 先读项目与已有工作项，区分“技能工程”“本地源码游戏”“Studio Place”。技能工程任务不自动创建游戏或修改当前打开的 Place。
2. 发现已连接 Studio 并读取模式；按 [项目发现](references/project-discovery.md) 与[有界只读探针](references/studio-probes.md) 确定目标、现有代码、同步来源和玩家主循环。证据仍无法消除的关键取舍，或用户明确要求拷问时，按[决策与变更交接](references/decision-change-control.md)调用[拷问技能](../roblox-game-grilling/SKILL.md)，闭合后回到原工作项。
3. 展示六阶段进度：需求范围、全局基线、基础工程、场景/显示层生产、全局集成验证、发布。局部任务直接进入最早受影响步骤。
4. 按[项目文档与清单](references/project-artifacts.md)初始化或复用 GDD/TDD、模块及资源登记；完整项目另按[项目依赖契约](../roblox-game-workflow-control/references/project-contract.md)登记工作项候选、前置依赖和最终集成项，多 Place 仅按需启用。[制作](../roblox-game-production/SKILL.md) 给出范围与验收，[架构](../roblox-game-architecture/SKILL.md) 确定服务端/客户端职责和模块接口。按[基础工程与集成](references/foundation-integration.md)冻结实施包与单写者，先完成代表性垂直切片。
5. 按职责调用玩法、UI、资产、音频、反馈、数值、在线服务；只加载本次相关技能。写入遵守 [Studio 执行契约](references/studio-execution.md)。
6. 推荐测试等级并自动执行已授权普通验证；由 [QA](../roblox-game-qa-performance/SKILL.md) 汇总技术证据，截图交用户检查。真实设备、上传、发布和付费单独核对授权。
7. 以 [交付要求](references/delivery.md) 结束本次工作项；项目级交付执行 `check-project` 汇总全部登记工作项与集成结果。发布候选交 [发布技能](../roblox-game-release/SKILL.md)，不从 Play 成功推断已保存或已上线。

## 领域分工

| 任务 | 技能 |
| --- | --- |
| 核心循环、范围、场景增量 | [制作](../roblox-game-production/SKILL.md) |
| 无法由证据消除的必要人工取舍 | [拷问与决策](../roblox-game-grilling/SKILL.md) |
| 服务端权威、模块、Remote、生命周期 | [架构](../roblox-game-architecture/SKILL.md) |
| 移动、战斗、交互、回合、关卡状态 | [玩法](../roblox-gameplay-development/SKILL.md) |
| HUD、弹窗、触控、手柄、适配、本地化 | [UI](../roblox-game-ui/SKILL.md) |
| 模型、材质、贴图、图片、资源来源 | [视觉资产](../roblox-game-visual-assets/SKILL.md) |
| 声音路由、环境声、音量与生命周期 | [音频](../roblox-game-audio/SKILL.md) |
| 经济、成长、难度和奖励 | [数值](../roblox-game-balance/SKILL.md) |
| 镜头、动画、粒子、声音与事件反馈 | [体验反馈](../roblox-game-juice/SKILL.md) |
| 存档、收据、商店、云配置、在线状态 | [在线服务](../roblox-game-live-ops/SKILL.md) |
| 测试、断点、场景分析、性能取证 | [QA 与性能](../roblox-game-qa-performance/SKILL.md) |
| 保存、发布候选、授权、回滚 | [发布](../roblox-game-release/SKILL.md) |

## 可见对象与协作

场景与显示层分别按 V0 分流、V1 定义、V2 拆解、V3 资源组合、V4 运行接入交付。按[视觉工作流](references/visual-workflow.md)、[响应式 UI](references/responsive-ui-contract.md)、[共享资源](references/shared-asset-usage.md)、[动画意图](references/animation-intent-contract.md)按需展开。先复用节点、组件与资源，复杂 UI 保持语义分组，不用单张概念图替代按钮和文本。

可独立的研究、探索、实现和审查按项目代理规则委派；明确文件/实例所有权与验收，禁止多个代理并发写同一 Studio。图片生成或编辑由 image_generator 子代理使用 imagegen 执行，本技能不自行生成位图。

项目记录保存在游戏工程，不写入技能包；不得把某次会话的 Studio ID、功能开关、Asset ID 或用户授权固化成全局默认值。未明确要求不建分支/worktree，不自动发起真机验收。
