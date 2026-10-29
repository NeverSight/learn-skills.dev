---
name: dreamina-opencli-image2video
description: Use when the user is a standard (non-VIP) Jimeng member without the dreamina CLI and needs image-to-video on jimeng.jianying.com. opencli jimeng has no image2video, frames2video, or multimodal subcommands. Pair with dreamina-prompt-image2video for incremental motion prompts, manual mode selection on the Jimeng web UI, and opencli history for verification. Never invoke dreamina or jimeng-cli execution skills.
license: Complete terms in LICENSE.txt
---

# dreamina-opencli-image2video — 即梦图生视频（opencli / 普通会员）

面向**无 dreamina CLI** 的普通会员。仅允许 `opencli jimeng` 子命令，**禁止** `dreamina image2video`、`frames2video`、`multiframe2video`、`multimodal2video` 及 `dreamina-cli-image2video`。

增量运动 prompt 由 `dreamina-prompt-image2video` 提供；**图生视频 / 首尾帧 / 分镜 / 全能参考**在即梦网页由用户选择模式并上传素材后生成。

## opencli 命令

| 子命令 | 用途 |
|--------|----------------|
| `generate-image2video <prompt> --image <path>` | 单张参考图 + 运动 prompt（`type=video`） |
| `history` | 任务完成后核对 |
| `new` / `workspaces` | 会话管理 |

首尾帧、多分镜、多模态仍须在网页选手动模式；opencli **无** `--first`/`--last` 路由。

## 网页模式与 prompt 技能对齐

| 用户输入 | 网页侧（用户操作） | prompt 技能要点 |
|----------|-------------------|-----------------|
| 单张图 | 图生视频，上传 1 张 | 只写运动增量 |
| 首尾 2 张 | 首尾帧 / 过渡 | 描述过渡过程 |
| 多张分镜 | 多帧 / 故事板 | 叙事 + 转场 |
| 图 + 音视频 | 全能参考 / 多模态 | 合成关系说明 |

路由在**网页**完成；智能体用 prompt 技能协助文案，用 opencli 做会话与验收。

## 核心流程

```
1. PROMPT  → dreamina-prompt-image2video
2. SESSION → 可选 opencli jimeng new --type=video
3. GEN     → opencli jimeng generate-image2video "<motion prompt>" --image ./frame.png --wait 180
4. VERIFY  → opencli jimeng history --limit N --type=video（视频可长达十余分钟，分轮查询）
```

## 允许的 opencli 示例

```bash
opencli jimeng generate-image2video "镜头缓慢推进，发丝随风飘动" --image ./portrait.jpg --wait 180
opencli jimeng history --limit 10 --type=video
```

## 禁止事项

- 不得调用任何 dreamina 视频子命令或 `query_result` 轮询。
- 不得虚构 opencli 图生视频参数。
- 不得引导安装 dreamina。

## 与 dreamina-canvas-cli-ref2video 的分工

已安装 dreamina-canvas CLI 的用户用 `dreamina-canvas-cli-ref2video` 做模式选择与路由（旧 `dreamina image2video` 于 2026-11 停止维护，勿再路由过去）；本技能用户**不得**改用。

## 智能体规范

- prompt 只描述**动起来**的部分，不重复画面静态内容。
- 分轮 `history` 验收，禁止 shell 死循环。
- 单图图生视频用 `generate-image2video --image`；复杂模式仍引导用户在网页操作。

## Gotchas

1. 首尾帧 / 分镜 / 多模态须网页手动，不得虚构 opencli 参数。
2. 视频耗时长，默认 `--wait=120`，图生视频建议 180+。
3. 普通会员排队与积分以网页为准。

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user is a standard (non-VIP) Jimeng member without the dreamina CLI and needs image-to-video on jimeng.jianying.com. opencli jimeng has no image2video, frames2video, or multimodal subcommands. Pair with dreamina-prompt-image2video for incremental motion prompts, manual mode selection on the Jimeng web UI, and opencli history for verification. Never invoke dreamina or jimeng-cli execution skills.。

## Rules

- 先读后写：先确认当前状态与真实能力，再执行会改变外部状态的动作。
- 权限最小化：只使用完成当前步骤所需的文件、工具、账户与网络范围。
- 证据优先：运行结果、资源 ID、版本、哈希或测试输出缺失时，明确标记为 `NOT_VERIFIED`。
- 幂等优先：保留请求标识与阶段状态；结果不明确时先查询，不进行盲目重试。
- 隐私安全：日志、示例、回执和错误信息不得包含 token、cookie、密钥或个人敏感数据。

## Workflow

### Step 1：澄清意图

确认本技能是否匹配目标；若只是相邻需求，交给更精确的技能。
### Step 2：执行预检

校验输入、模型/工具能力、输出路径、预算上限和审批状态；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按一次批准执行并记录请求标识；模糊结果先查询而不是重提；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

验证产物存在性、格式、哈希/标识、成本状态和质量门禁，并把事实、推断和未验证项分开陈述。

## Validation checklist

- [ ] 技能触发条件与用户意图一致，没有把相邻任务误路由到本技能。
- [ ] 输入、目标对象、版本和输出位置均已明确，且没有使用猜测值替代必填值。
- [ ] 所有写入、付费、发布或不可逆动作都在用户授权范围内。
- [ ] 结果已用独立检查验证；仅有“命令成功”或“文件存在”不算完整验收。
- [ ] 输出包含实际证据、失败/跳过项、剩余风险和可执行的下一步。

## Gotchas

1. **把计划当结果**：文档或提示词不等于真实执行；必须标明实际运行层级。
2. **错误重试**：超时或响应丢失可能已经产生远端状态，先查询再决定是否重试。
3. **隐式扩大范围**：批量、全量、发布、覆盖和付费不是普通读写的自然延伸。
4. **版本漂移**：引用外部资源时记录版本、tag 或提交；不要把可变分支当发布证据。
5. **证据过期**：缓存、旧截图和历史测试不能证明当前环境；在交付前刷新关键证据。

## 不适用与边界

付费、发布、覆盖、上传或外部写入必须使用当前任务的显式授权；不自动扩大次数和预算。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
