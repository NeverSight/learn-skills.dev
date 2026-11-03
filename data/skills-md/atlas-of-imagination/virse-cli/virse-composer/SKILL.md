---
name: virse-composer
description: >-
  交办 Virse 画布内创作家 Composer 子任务，传入素材引用、管理节点与会话、读取历史、继续对话、观察回合或请求停止。精确管理与指定模型、工具产物的执行优先由 CLI 直做。
---
# Composer 创作家委派

<!-- virse:background:start -->
Virse 是 AI native 的创作系统，用画布连接想法、素材、审美、工具与模型，支持图片、视频、3D 和文本。资源目录管理素材与归属，画布组织创作输入、过程与结果。

只读当前任务所需参考，已读且适用的内容沿用，链接不自动加载内容。
<!-- virse:background:end -->

用户指定后端时，在首条远端命令前设置 `VIRSE_BACKEND_URL`。

## 交办目标与执行分工

Composer 是平台内 Agent 的独立画布节点与会话。用户明确委派时使用；未点名时，外部 Agent 也可根据任务主动选择：需要围绕画布材料连续创作、组合多步操作并根据结果反馈时适合委派。精确的对象管理、已指定模型或工具产物的执行，优先由 CLI 直做；复杂程度本身不是委派理由。

混合任务由外部 Agent 统筹宿主与其他应用上下文、安排适合的 Virse 创作环节，可把范围明确的画布子任务交给 Composer，再整合并验收全部交付。委派不保证解决排版问题，也不补足未公开的功能。

完整品牌中心任务由 `virse-brand-center-creator` 统筹建设计划、规范与品牌文件夹；Composer 按本次交办承担画布子任务，不把单回合完成当成整个品牌系统已交付。

宿主准备图片创作 brief 或检查图片时，按问题读取 `virse-image-craft`；视频模式、动作镜头、连续性与声音使用 `virse-video-craft`。把本次选定的目标、参考分工、保留项和验收要求写进 brief，Composer 不会因为消息中出现 Skill 名称就自动加载宿主的技巧或上下文。

沿用用户指定或已有承担同一目标的节点，不为追问另建节点；宿主不重复执行已交办目标，节点引用仅覆盖指定元素，不等于整个画布上下文。

涉及生成时，把用户已确认的模型、关键配置或明确授权的自主选择范围一并交给 Composer；尚未确认时先在宿主准备建议，不提前发送可能开始生成的任务。已有相应授权的任务可以发送并等待：

```bash
virse --org "$ORG" --canvas "$CANVAS" --json composer send "$COMPOSER" --input "$BRIEF" --reference "$ELEMENT" --wait
```

`COMPOSER` 为实际 agent 元素 UUID，`ELEMENT` 为明确引用节点；没有引用时省略 `--reference`。先创建节点不会提交任务。上一回合结束后，向同一节点再次 `send` 才是继续会话。

`send` 每次都是新消息，没有可用于重放的幂等回执。受理结果不明先查 `get/history/watch`，不重发；本机记录保存摘要和受理身份，不保证保留完整原文。节点 UUID、run ID 与 Agent turn ID 不混用。

## 当前任务直达

| 用户正在做什么 | 需要的参考 |
| --- | --- |
| 开启 Ultra Design／全能创作，统筹完整创作项目 | `virse-ultra-design` |
| 查找、创建、读取、改名或删除创作家节点 | [独立节点与会话](references/sessions.md) |
| 交办、引用材料、传入长任务或在原会话继续 | [消息、上下文与继续会话](references/messages-and-continuation.md) |
| 读历史、观察指定回合、断线续看或请求停止 | [观察、历史与停止](references/observe-and-stop.md) |
| 检查或取回已交付文件 | [文件交付](references/shared/contracts/delivery.md) |

仅在缺相关信息时直读[连接](references/shared/contracts/connection.md)、[对象](references/shared/context/objects.md)、[执行](references/shared/contracts/execution.md)合同。引用审美等特殊对象时，按[审美消费条件](references/shared/context/aesthetics.md)及 Composer 实际允许的请求字段处理，不能把作者草稿正文自动暴露给普通委派。

## 完成判断

记录节点、已受理 run/turn、真实终态与具体产物。节点查询成功不是执行成功，回合完成也不是作品质量已核验；按目标检查实际图片、文本或其他交付，不能只转述 Agent 自己宣称完成。

`stop` 针对节点当前运行请求协作中断；返回受理不等于供应商已停机，也不回滚已完成的画布修改。删除节点不等于停止；超时或 Ctrl+C 只停止本机等待。当前没有 REPL、历史分叉、运行中追加队列、精确续跑或撤销整个回合的合同。
