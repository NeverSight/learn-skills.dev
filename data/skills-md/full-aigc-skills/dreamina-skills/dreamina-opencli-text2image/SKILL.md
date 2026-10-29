---
name: dreamina-opencli-text2image
description: Use when the user cannot use the dreamina CLI (standard non-VIP member) and must automate 即梦 text-to-image through opencli Browser Bridge on jimeng.jianying.com. Covers generate, history, new, workspaces, user_credit, user_assets, user_subscription. Does not use the dreamina CLI. Pair with dreamina-prompt-text2image for prompts.
license: Complete terms in LICENSE.txt
---

# dreamina-opencli-text2image — 即梦文生图（opencli / 普通会员）

面向**未开通 dreamina CLI / 高级会员**、仅能用**即梦网页普通会员**能力的用户。本技能**只允许**调用 `opencli jimeng` 子命令，**禁止**调用 `dreamina` 或 `dreamina-cli-*` 执行类技能。

提示词由 `dreamina-prompt-text2image` 产出；本技能只负责 opencli 执行与会话管理。

## opencli jimeng 命令清单

| 子命令 | 作用 | 关键参数 / 输出 |
|--------|------|-----------------|
| `generate <prompt>` | 文生图 | `--model`、`--wait`、`--workspace`；列 `status`、`media_type`、`media_count`、`media_urls` |
| `generate-image2image <prompt>` | 图生图 | 必填 `--images`（逗号分隔路径，最多 10 张） |
| `history` | 最近作品 | `--limit`、`--workspace`、`--type`；列 `history_id`、`media_type`、`media_url` 等 |
| `new` | 新建 workspace | `--type`；列 `workspace_id`、`workspace_url`、`type` |
| `workspaces` | 工作区列表 | 列 `workspace_id`、`name`、`is_pinned`、`updated_at` |
| `user_credit` | 积分余额 | 列 `balance`、`vip_credit`、`gift_credit`、`purchase_credit` |
| `user_subscription` | 会员信息 | 列 `cur_vip_level`、`subscribe_type`、`end_time` 等 |
| `user_assets` | 资产库各 Tab | `--tab`、`--wait`；列 `tab`、`item_count`、`request_url` |

通用选项（各子命令）：`-f/--format`（table、plain、json 等）、`-v/--verbose`。策略：Cookie + Browser，域名 `jimeng.jianying.com`。

## 前置条件

1. 已安装 `opencli`，且 `opencli jimeng -h` 可列出上述四条子命令。
2. Chrome 已登录即梦，并安装 Browser Bridge（与 opencli 文档一致）。
3. 执行前用 `opencli jimeng history --limit 1` 或浏览器打开即梦，确认未掉线。

## 核心流程

```
1. PROMPT → dreamina-prompt-text2image 定稿并获用户确认
2. GEN    → opencli jimeng generate "<prompt>" [--model ...] [--wait ...]
3. CHECK  → 解析 status；timeout 时加大 --wait 或 history 对照
4. ORG    → 可选 new / workspaces 管理会话
```

## generate 用法

```bash
opencli jimeng generate "一只在星空下的猫"
opencli jimeng generate "赛博朋克城市夜景" --model high_aes_general_v50 --wait 60
opencli jimeng generate "水墨山水" --format json
```

| 参数 | 说明 |
|------|------|
| `prompt` | 位置参数，必填 |
| `--model` | 默认 `high_aes_general_v50`；可选 `high_aes_general_v42`（4.6）、`high_aes_general_v40`（4.0） |
| `--wait` | 等待出图秒数，默认 `40` |

`status` 为 `success` 时从 `media_urls` 取链接；`timeout` 时增加 `--wait` 或查 `history`；`failed` 时提示检查登录、积分（`user_credit`）或网页合规弹窗。

## 辅助命令

```bash
opencli jimeng history --limit 10
opencli jimeng new
opencli jimeng workspaces
```

## 与 dreamina-canvas-cli-text2image 的分工

| 用户条件 | 使用技能 |
|----------|----------|
| 仅有普通会员 / 无 dreamina CLI | **本技能**（仅 opencli） |
| 已安装 dreamina-canvas CLI | `dreamina-canvas-cli-text2image`（旧 `dreamina text2image` 于 2026-11 停止维护，勿再路由过去） |

## 智能体规范

- 不得建议安装 `dreamina` 或执行 `dreamina text2image`。
- 不得用 shell `while true` 死循环；等待由 `generate --wait` 在浏览器内完成。
- 不得在本技能内改写 prompt。

## Gotchas

1. `generate` 固定打开 `type=image` 文生图页；不含图生图、视频参数。
2. `--model` 以 `opencli jimeng generate -h` 为准；若网页未切换模型，以页面实际选项为准。
3. 中文 prompt 通常效果更好。
4. `history` 的 `status` 为 `completed` / `pending`，与 `generate` 的 `success` / `timeout` 字段不同，勿混用。

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user cannot use the dreamina CLI (standard non-VIP member) and must automate 即梦 text-to-image through opencli Browser Bridge on jimeng.jianying.com. Covers generate, history, new, workspaces, user_credit, user_assets, user_subscription. Does not use the dreamina CLI. Pair with dreamina-prompt-text2image for prompts.。

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
