---
name: dreamina-cli-text2image
description: 仅在用户明确要求旧版 dreamina CLI、恢复旧版 submit_id 或排查历史命令时使用；冻结兼容技能，新任务转交对应 dreamina-canvas-cli 技能。
license: Complete terms in LICENSE.txt
---

# 即梦 CLI 文生图

> ⚠️ **停维护公告**：旧版 Dreamina CLI（`dreamina`，v1.4.18）将于 **2026 年 11 月** 起停止维护。新任务请改用 Canvas 替代技能 **`dreamina-canvas-cli-text2image`**（安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-canvas-cli-text2image`）。本技能内容保留作历史契约参考。

执行前先运行 `dreamina text2image -h`。本技能记录 v1.4.18 稳定工作流；实际 help 始终是参数事实源。

## When to use and boundary

用于已经进入 CLI 执行、轮询或故障诊断阶段的文生图任务。不该用于图生图、视频生成或单纯的提示词创作；这些场景分别加载对应的 `dreamina-cli-*` 或 `dreamina-prompt-*` 技能。

协作路由：`dreamina-prompt-text2image` 负责提示词创作；本 Skill 负责本地
`dreamina` CLI 执行；用户明确选择 OpenCLI 传输时改用
`dreamina-opencli-text2image`，不要同时提交两条执行链。

## 必须遵守

- 每次提交显式传 `--resolution_type=1k|2k|4k`。
- `--width` 与 `--height` 必须成对出现、为正整数，并与 `--ratio` 互斥。
- 模型 token 使用 `5.0Pro`，不要写成人类可读名称 `5.0 Pro`。
- `generate_num` 范围为 1–10。
- 提交前说明会消耗积分；优先 `--poll=0` 获取 `submit_id`。

模型与分辨率矩阵、宽高像素限制见
[`dreamina-cli` skill 的 `references/dreamina-cli-v1.4.18-contract.md`](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)。
如未安装,请先 `npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`。

## 标准执行

```bash
dreamina user_credit
dreamina text2image \
  --prompt="一只橘猫坐在窗边，柔和晨光，浅景深" \
  --ratio=1:1 \
  --model_version=5.0 \
  --resolution_type=2k \
  --poll=0
```

自定义尺寸时省略 ratio：

```bash
dreamina text2image \
  --prompt="竖版产品海报，留出标题区域" \
  --model_version=5.0 \
  --resolution_type=2k \
  --width=1536 \
  --height=2048 \
  --poll=0
```

## 异步闭环

### Step 1：验证

运行 `dreamina text2image -h`，校验模型、分辨率、ratio 或自定义尺寸组合。

### Step 2：提交

检查积分、说明消费影响、提交并保存 `submit_id`。

### Step 3：终态闭环

`querying` 仅表示已受理；继续 `query_result`，直到 `success` 或 `fail`。失败时报告
`fail_reason`；需要文件时增加 `--download_dir=<absolute-path>`。

## Gotchas

1. **分辨率遗漏**：v1.4.18 会拒绝未传 `resolution_type` 的请求。
2. **宽高冲突**：自定义 width/height 不能与 ratio 同时出现。
3. **展示名误作 token**：`5.0 Pro` 必须转换为 `5.0Pro`。
4. **受理误作成功**：`querying` 不是成功终态。
5. **积分消耗**：真实提交前必须让用户知道会消费积分。

## References

- [`dreamina-cli` skill 的 v1.4.18 参数契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）
- [参数参考](references/parameter-reference.md)
- [模型选择](references/model-guide.md)
- [工作流模式](references/workflow-patterns.md)
- [示例](examples/basic-generation.md)

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants to submit, poll, or troubleshoot Dreamina 即梦 text-to-image tasks through `dreamina text2image`. Covers CLI v1.4.18 required resolution, custom width/height, Seedream model tokens, batch count, sessions, and async terminal status handling.。

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
