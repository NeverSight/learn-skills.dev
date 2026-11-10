---
name: evaluating-agents-with-deepeval
description: 用于项目配置、当前权威来源或用户明确指令已经选择 DeepEval，且需要建立、运行、审查或修正 Agent 评测时。
---

# 使用 DeepEval 评估 Agent

官方 Skill 负责实现，Test Privateer 负责质量门槛。先由 `agent-eval` 固定质量主张、自然场景、Oracle 和原始证据，再把实施交给 Confident AI 官方 Skill；本 Skill 不复制 DeepEval 的 API、模板、数据集或运行教程。

## 进入条件

先读取 `agent-eval`。只有项目配置、当前权威来源或用户明确指令选择 DeepEval 时继续；用户本轮明确调用只代表本轮选择，不自动改写项目配置。项目选择自有框架时回到通用 `agent-eval` 和项目入口，不安装、迁移或加载本专项。框架尚未决定且会改变资产时，交给 `setup-test-privateer`。

## 官方实现依赖

- **必需：** 使用官方 [`deepeval`](https://github.com/confident-ai/deepeval/tree/main/skills/deepeval) Skill 建立数据集、测试资产、指标、运行和迭代流程。
- **需要 DeepEval tracing 时：** 使用官方 [`deepeval-tracing`](https://github.com/confident-ai/deepeval/tree/main/skills/deepeval-tracing) Skill。
- **需要原始 OpenTelemetry／OTLP 接入时：** 使用官方 [`deepeval-otel`](https://github.com/confident-ai/deepeval/tree/main/skills/deepeval-otel) Skill。

优先读取宿主已安装的官方 Skill，并以其随版本提供的 references、templates 和命令为实施依据。Python 包存在不等于官方 Skill 已安装。

官方 Skill 不可用时，说明缺失名称、官方来源、准备安装的范围和安装后复检动作，再询问用户是否安装。用户尚未回答且尚未运行评测时，当前宿主所需官方 Skill 的就绪状态必须是 `awaiting_install_confirmation`，停在一个安装确认问题；可以说明当前缺少官方 Skill，但不得同时把这一待确认状态写成 `environment_error` 或最终 `missing_official_skill`。只有用户明确确认后，才调用宿主已有的 Skill 安装能力；只安装已经说明且当前任务需要的官方 Skill。安装后重新读取，实际可读才进入官方实施。

`agent-eval` 的 `pass`、`agent_failure`、`environment_error` 和 `invalid_case` 用于已运行评测案例或已经确定无法实施的结果。单纯等待安装选择不是一次评测结果，不进入这四类；没有答复不等于拒绝。当前宿主官方 Skill 状态不写入项目配置长期枚举，项目配置就绪也不代表宿主实施能力就绪。

安装位置和作用域由宿主安装能力与用户选择决定。宿主没有可用安装入口时，不得自行创建项目内 `skills/deepeval/`、克隆仓库、下载文件或复制官方 Skill 作为替代。

用户拒绝、宿主没有安装能力或安装后仍不可读时，将 DeepEval 实施标为 `environment_error: missing_official_skill`，给出恢复条件；不得凭记忆补写 API、复制本地教程、静默安装或切换框架。仍可完成框架无关的质量主张、场景和确定性 Oracle。

安装官方 Skill 的确认不授权安装 Python 依赖、修改锁文件、登录、上传、调用外部 Judge、产生费用或修改产品代码；这些动作仍按项目规则和官方 Skill 分别确认。

## 实施前交接

交给官方 Skill 前固定：

- 被测系统、目标任务、质量主张和当前授权；
- 目标失败与邻近正常场景；
- 业务状态、权限、安全、文件差异和工具结果等确定性 Oracle；
- 原始记录位置：完整输出、实际 Skill／文件加载、工具调用、文件变化、配置和环境状态；
- 本地运行、外部 Judge、登录、费用和上传的允许边界。

官方 Skill 决定具体项目结构、数据集、tracing、指标、命令和迭代方式。本 Skill 不替它做实现设计。

## 实施后质量门槛

1. **入口正确：** DeepEval 由项目或用户明确选择；自有框架没有被替换。
2. **资产可复跑：** 官方 Skill 生成或复用的测试、数据集、配置和运行入口位于项目约定位置，不只存在于临时脚本或回答中。
3. **原始证据保真：** 派生用例、trace 和报告保留原始记录指针。模型自述、摘要轨迹和人工补写计划不能冒充实际动作；没有事件支持的 Skill 加载记为未确认。
4. **Oracle 优先级正确：** 确定性业务、权限、安全、文件和工具结果优先。Judge 或指标通过不能覆盖真实失败；已知错误必须能够失败，邻近正常路径不能被误拒。
5. **授权没有扩大：** 默认本地、最小披露。登录、上传私有数据、调用外部 Judge、安装或升级依赖、修改产品代码和新增费用都需要已有项目约定或当前授权。
6. **结论有边界：** 分别保留 `pass`、`agent_failure`、`environment_error` 和 `invalid_case`；未运行项不计为通过，不生成平均总分，不用单项指标扩大为完整 Agent 通过。

任一门槛失败时，保留官方 Skill 的原始产物和输出，指出失败层与最小修正对象；只重跑受影响场景。不得为取得分数放宽确定性 Oracle、删除首次失败或补写不存在的轨迹。

## 交付

```markdown
官方 Skill 与版本 — 项目资产／运行入口 — 原始证据指针
确定性 Oracle — DeepEval 结果 — 冲突／未运行项
当前宿主官方 Skill 状态／实际评测状态 — 证据支持什么 — 不支持什么 — 下一验证
```

**完成条件：** 官方 Skill 实际可用并承担 DeepEval 实施；项目留下可复跑资产和真实运行证据；Test Privateer 的确定性 Oracle、证据、授权和失败分类没有被框架结果削弱。
