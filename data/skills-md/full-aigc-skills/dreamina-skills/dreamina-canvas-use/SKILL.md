---
name: dreamina-canvas-use
description: 当用户要求即梦图像、视频、语音或音乐交付但未指定具体操作时使用：在九个 Canvas CLI 技能或专业视频制作流程之间按需求选择并交接阶段；只负责路由和生命周期报告，不复制命令规范。
license: Complete terms in LICENSE
---

# 即梦任务路由

## When to use
识别用户需要的产物和已有输入，选择最短操作链。使用 Canvas 作为新任务默认路径；明确要求旧版 dreamina CLI 时才交给冻结的 dreamina-cli 技能。

## Workflow
| 意图 | 唯一执行入口 |
|---|---|
| 安装、升级、PATH | dreamina-canvas-cli-setup |
| 登录、账户、刷新、退出 | dreamina-canvas-cli-auth |
| 文生图 | dreamina-canvas-cli-text2image |
| 图生图、放大 | dreamina-canvas-cli-image2image |
| 文生视频 | dreamina-canvas-cli-text2video |
| 单图、首尾帧、多模态视频 | dreamina-canvas-cli-ref2video |
| 语音旁白 | dreamina-canvas-cli-text2voice |
| 背景音乐 | dreamina-canvas-cli-text2audio |
| 画布、素材、时间轴、报价、查询、下载 | dreamina-canvas-cli |
| 参考视频到完整成片 | dreamina-video-production |

### Step 1：记录用户意图、输入、交付要求与已存在的身份。
### Step 2：只补齐缺失的安装/登录/素材条件，不重新执行已完成步骤。
### Step 3：将操作交给上表入口，按技能名称加载其规范。纯提示词需求交给对应 dreamina-prompt-*。
### Step 4：分别报告草稿、报价、已批准、已提交、终态和已验证文件；评估需要时交给 dreamina-video-evaluator。

## Rules
- 跨技能只按名称交接。安装缺失入口：`npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`。
- 不执行私有插件 Python API，不承担第二套参数和计费规则。
- 不将普通会员或本地登录状态等同于生成权限。

## Validation checklist
- [ ] 选择与输入和模式对应的唯一任务入口。
- [ ] 已有 submitId 走恢复，不重新生成。
- [ ] 最终结果包含产物验收和未完成阶段。

## Gotchas
- 单图参考属于 ref2video，不能臆造 i2v 模式。
- 视频制作依赖专门的项目工具，工具不可用时报告缺口。
- 编排不代替用户批准预算。

## Progressive disclosure（按需读取）

- 需要在九个入口之间选出最小技能链时，读取 [路由来源](references/routing-table.md)。
- 需要确定输入/输出、状态与授权点时，读取 [工作流契约](references/workflow-contract.md)。
- 遇到超时、部分成功或恢复场景时，读取 [错误与恢复](references/error-recovery.md)。
- 交付前自检时，读取 [验证清单](references/validation-checklist.md)。

## 不适用与边界

不适用于直接维护命令参数、安装脚本或替代质量判断。用户已指定原子技能时直接交接；缺少媒体或预算条件时只停在对应未满足阶段。
