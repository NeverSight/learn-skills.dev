---
name: dreamina-video-evaluator
description: Use when judging generated Dreamina shot clips against measured gates, producing shot_evaluation.schema.json content only.
license: Complete terms in LICENSE
---

# Dreamina Video Evaluator

Evaluate only, and only after measurement. This Skill produces
`shot_evaluation.schema.json` content and nothing else.

## Example request

```text
Use dreamina-video-evaluator for shot S03 attempt 1 after reading its measured
gates and approved design. If retry is necessary, select only the next request
fingerprint already present in the activated batch allowance.
```

## 能力边界说明

### ✅ 能做

- Read the measured clip gates for one shot attempt.
- Judge whether the clip satisfies the design intent.
- Return `accepted`, a prequoted `retry`, `rejected`, or `manual_review`.

### ⚠ 需要素材

- A measured artifact with its SHA-256 and deterministic gate results.
- The design version the attempt was generated from.

### ❌ 超出范围

- Do not produce `shot_annotation.schema.json`. Shot semantics belong to `dreamina-shot-annotator`.
- Do not re-measure media or override the measured gates.
- Do not request more attempts than the batch quote already covers.
- Do not resubmit. `retry` must reference an attempt the quote already enumerated.

## Workflow

1. Receive the measured gates for exactly one shot attempt.
2. Compare against the design intent for that shot.
3. Return the evaluation with one of the four decisions, and for `retry` the prequoted attempt.

## Never do

- Never accept a clip whose measured gates failed.
- Never invent an attempt beyond the quote.
- Never blur the line between design intent and acceptance verdict.

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when judging generated Dreamina shot clips against measured gates, producing shot_evaluation.schema.json content only.。

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
