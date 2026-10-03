---
name: ai-work
description: Use when a user wants help choosing an AI work approach, designing a reusable AI workflow, or coordinating an unfamiliar multi-step task. Simple self-contained requests need no routing.
---

# AI 工作方法入口

帮助用户从目标推进到可使用的结果。先用最简单可行的方式；明确的单步任务直接完成，不做方法问卷。

## 按瓶颈加载

从现有上下文确认结果、接收方和主要缺口；只问会改变下一步的未知取舍。每阶段先选一主模块，确有独立瓶颈才补充。阶段结束后按新瓶颈加载，避免把上下文预算当整个任务的硬上限。按环境提供的技能机制使用下表模块，或读取其相对文件；不默认全加载。

| 当前瓶颈 | 主模块 |
| --- | --- |
| 实现、交付或验收真假 | [ai-work-delivery](../ai-work-delivery/SKILL.md) |
| AI、程序与人的边界 | [ai-work-intelligence](../ai-work-intelligence/SKILL.md) |
| 分工、模型、依赖和并行 | [ai-work-orchestration](../ai-work-orchestration/SKILL.md) |
| 重复流程、恢复和跨应用操作 | [ai-work-workflow](../ai-work-workflow/SKILL.md) |
| 来源、检索复用和知识纠正 | [ai-work-knowledge](../ai-work-knowledge/SKILL.md) |
| 经验是否值得固化成 Skill | [ai-work-distill](../ai-work-distill/SKILL.md) |

职责重叠时读 [routing.md](references/routing.md)；缺工具、跨专业执行或读取失败时读 [tools-context.md](references/tools-context.md)。每个模块也只读取符合条件的 reference。

## 推进与收口

用户要求现成产物且输入足够时，实际完成并提供产物，不能只给下一步计划或方法建议。仅当用户要计划或缺必需输入时输出计划/未决项；不强迫固定长报告。已有用户授权继续有效；常规可逆步骤直接推进，不能从方法推导额外外部权限。下层模块不反向召回本入口。

完成时说明可用结果与真实未决项。脚本通过、模型认同、文件保存各证明对应层；最终可用性从接收方检查。无更多瓶颈就停止加载。
