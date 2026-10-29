---
name: dreamina-cli-image2video
description: 仅在用户明确要求旧版 dreamina CLI、恢复旧版 submit_id 或排查历史命令时使用；冻结兼容技能，新任务转交对应 dreamina-canvas-cli 技能。
license: Complete terms in LICENSE.txt
---

# 即梦 CLI 图生视频

> ⚠️ **停维护公告**：旧版 Dreamina CLI（`dreamina`，v1.4.18）将于 **2026 年 11 月** 起停止维护。新任务请改用 Canvas 替代技能 **`dreamina-canvas-cli-ref2video`**（安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-canvas-cli-ref2video`）。本技能内容保留作历史契约参考。

先按输入意图选命令，再运行对应的 `dreamina <command> -h`：

## When to use and boundary

用于至少有一张参考图或一个参考视频的 CLI 视频任务。不该用于纯文本视频、图片生成或纯提示词润色；这些场景改用对应的 `dreamina-cli-*` 或 `dreamina-prompt-*` 技能。

协作路由：`dreamina-prompt-image2video` 负责单图、首尾帧、多帧和多模态提示词；
本 Skill 负责本地 `dreamina` CLI 执行；用户明确选择 OpenCLI 传输时改用
`dreamina-opencli-image2video`，不要同时提交两条执行链。

| 场景 | 命令 | 关键输入 |
|---|---|---|
| 单图动画 | `image2video` | `--image`、必填 `--prompt` |
| 首尾帧过渡 | `frames2video` | `--first`、`--last` |
| 2–20 张故事板 | `multiframe2video` | `--images` |
| 图/视频/音频全能参考 | `multimodal2video` | 至少一张图、一个视频或一个音频 |

## v1.4.18 硬约束

- 所有四种模式都必须显式传 `--video_resolution`。
- 分辨率 token 使用小写 `480p`/`720p`/`1080p`/`4k`；`480p` 仅 `seedance2.5` 支持。
- `multiframe2video` 固定模型，不接受 `seedance2.5`，只接受 720p/1080p。
- `seedance2.5` 支持 480p/720p/1080p，不支持 4k；其他模型组合以运行时 help 为准。
- `image2video` 支持 `seedance1.0fast`、`seedance1.5pro`、Seedance 2.0 家族与 `seedance2.5`。
- `frames2video` 支持 `seedance1.5pro`、Seedance 2.0 家族与 `seedance2.5`。
- `multimodal2video` 支持 Seedance 2.0 家族与 `seedance2.5`；`seedance2.5` 允许**纯音频**输入。
- `seedance2.5` 时长 4–30 秒，参考音视频总时长 2–30 秒。
- 比例必须在运行时通过 `dreamina <command> --help` 发现：`image2video`、`frames2video`、
  `multimodal2video` 暴露 `--ratio`，`multiframe2video` 不暴露并跟随首图。
- `image2video` 与 `frames2video` 使用 `seedance2.5` 时禁止显式传 `--ratio`，比例跟随首帧；
  `multimodal2video` 可显式传比例，省略时默认 16:9。

完整矩阵见 [`dreamina-cli` skill 的 v1.4.18 契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）。

## 最小正确示例

```bash
dreamina image2video --image=./photo.png --prompt="镜头缓慢推近" --video_resolution=720p --poll=0
dreamina frames2video --first=./start.png --last=./end.png --prompt="季节自然变化" --video_resolution=720p --poll=0
dreamina multiframe2video --images=./a.png,./b.png --prompt="人物转身走向远处" --video_resolution=720p --poll=0
dreamina multimodal2video --image=./subject.png --audio=./music.mp3 --prompt="按音乐节奏运镜" --video_resolution=720p --poll=0
```

3 张以上多帧故事，每 N 张图提供 N−1 个 transition；单段时长 1–8 秒：

```bash
dreamina multiframe2video \
  --images=./a.png,./b.png,./c.png \
  --transition-prompt="从 A 走向 B" \
  --transition-prompt="从 B 走向 C" \
  --transition-duration=3 \
  --transition-duration=3 \
  --video_resolution=1080p \
  --poll=0
```

## 异步闭环

### Step 1：路由与验证

根据输入意图选择四个命令之一，验证文件可读，再用对应 `--help` 在运行时校验模型、时长、比例和分辨率。

### Step 2：提交

检查积分、说明消费影响、异步提交并保存 `submit_id`。

### Step 3：终态闭环

对 `querying` 持续调用 `query_result`，直到 `success` 或 `fail`。失败时报告
`fail_reason`。遇到 `AigcComplianceConfirmationRequired` 时提示用户先在 Web 端完成授权。

## Gotchas

1. **模式误路由**：单图、首尾帧、故事板、全能参考的参数名不同。
2. **分辨率遗漏**：四个命令都必须传 `video_resolution`；`seedance2.5` 支持 480p/720p/1080p。
3. **多帧越权**：multiframe 不接受 model_version，也不能用 4k，也不可用 `seedance2.5`。
4. **transition 数量**：N 张图需要 N−1 条 transition。
5. **比例误传**：`seedance2.5` 的 image/frames 模式禁止显式比例；multiframe 根本没有 `--ratio`。
6. **音频单独提交**：`multimodal2video` 的 `seedance2.5` 允许纯音频输入（参考音视频总时长 2–30 秒）。
7. **时长越界**：`seedance2.5` 4–30 秒；Seedance 2.0 家族 4–15 秒；超出会被拒。

## References

- [`dreamina-cli` skill 的 v1.4.18 参数契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）
- [模式选择](references/mode-guide.md)
- [参数参考](references/parameter-reference.md)
- [VIP 指南](references/official-doc-vip-guide.md)
- [工作流模式](references/workflow-patterns.md)
- [示例](examples/single-image.md)

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user provides image, video, or audio references and wants Dreamina 即梦 video generation through `image2video`, `frames2video`, `multiframe2video`, or `multimodal2video`. Covers CLI v1.4.18 runtime ratio discovery, required video resolution, Seedance model constraints, input limits, and async terminal statuses.。

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
