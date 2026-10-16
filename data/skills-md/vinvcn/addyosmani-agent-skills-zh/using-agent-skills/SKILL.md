---
name: using-agent-skills
description: 发现并调用 agent skills。用于开始会话，或需要判断当前任务适用哪个 skill 时。这个 meta-skill 负责治理所有其他 skills 的发现与调用方式。
---

# 使用 Agent Skills

## 概览

Agent Skills 是一组按开发阶段组织的工程工作流 skills。每个 skill 都编码了资深工程师会遵循的特定流程。这个 meta-skill 帮助你为当前任务发现并应用正确的 skill。

## Skill 发现

当任务到来时，识别开发阶段并应用对应的 skill：

```
Task arrives
    │
    ├── Don't know what you want yet? ──────→ interview-me
    ├── Have a rough concept, need variants? → idea-refine
    ├── New project/feature/change? ──→ spec-driven-development
    ├── No quality bar written down? ──→ constraint-driven-development
    ├── Have a spec, need tasks? ──────→ planning-and-task-breakdown
    ├── Implementing code? ────────────→ incremental-implementation
    │   ├── UI work? ─────────────────→ frontend-ui-engineering
    │   ├── API work? ────────────────→ api-and-interface-design
    │   ├── Need better context? ─────→ context-engineering
    │   ├── Need doc-verified code? ───→ source-driven-development
    │   └── Stakes high / unfamiliar code? ──→ doubt-driven-development
    ├── Writing/running tests? ────────→ test-driven-development
    │   └── Browser-based? ───────────→ browser-testing-with-devtools
    ├── Something broke? ──────────────→ debugging-and-error-recovery
    ├── Reviewing code? ───────────────→ code-review-and-quality
    │   ├── Too complex? ─────────────→ code-simplification
    │   ├── Security concerns? ───────→ security-and-hardening
    │   └── Performance concerns? ────→ performance-optimization
    ├── Committing/branching? ─────────→ git-workflow-and-versioning
    ├── CI/CD pipeline work? ──────────→ ci-cd-and-automation
    ├── Deprecating/migrating? ────────→ deprecation-and-migration
    ├── Writing docs/ADRs? ───────────→ documentation-and-adrs
    ├── Adding logs/metrics/alerts? ───→ observability-and-instrumentation
    └── Deploying/launching? ─────────→ shipping-and-launch
```

## 核心运行行为

这些行为始终适用，横跨所有 skills。它们是不可协商的。

### 1. 显式提出假设

在实现任何非平凡内容之前，明确说明你的假设：

```
ASSUMPTIONS I'M MAKING:
1. [assumption about requirements]
2. [assumption about architecture]
3. [assumption about scope]
→ Correct me now or I'll proceed with these.
```

不要默默补全含糊的需求。最常见的失败模式是做出错误假设，然后在未经确认的情况下继续推进。尽早暴露不确定性，这比返工便宜得多。

### 2. 主动管理困惑

当你遇到不一致、互相冲突的需求，或不清楚的规格时：

1. **STOP.** 不要凭猜测继续。
2. 说清楚具体困惑在哪里。
3. 呈现权衡，或提出澄清问题。
4. 等待问题解决后再继续。

**坏例：** 默默选择一种解释，并希望它是对的。
**好例：** “我看到 spec 里是 X，但现有代码里是 Y。哪一个优先？”

### 3. 在必要时提出反对

你不是 yes-machine。当某种做法存在明确问题时：

- 直接指出问题
- 解释具体缺点（能量化时就量化，比如“这会增加约 200ms 延迟”，而不是“这可能会更慢”）
- 提出替代方案
- 如果人类在掌握完整信息后仍决定覆盖你的建议，接受该决定

逢迎是一种失败模式。“Of course!” 之后实现一个坏主意，对任何人都没有帮助。诚实的技术分歧比虚假的认同更有价值。

### 4. 强制保持简单

你的自然倾向是把事情复杂化。要主动抵抗。

在完成任何实现之前，问自己：
- 能用更少的代码完成吗？
- 这些抽象值得它们带来的复杂度吗？
- staff engineer 看了会不会说“为什么不直接……”？

如果你写了 1000 行，而 100 行就足够，那就是失败。优先选择无聊、明显的方案。聪明技巧很昂贵。

### 5. 保持范围纪律

只触碰被要求触碰的内容。

不要：
- 删除你不理解的注释
- “清理”与任务无关的代码
- 顺手重构相邻系统
- 未经明确批准删除看似未使用的代码
- 因为“看起来有用”而添加 spec 之外的功能

你的工作是外科手术式的精确，不是主动翻新。

### 6. 验证，不要假设

每个 skill 都包含验证步骤。验证通过之前，任务不算完成。“看起来没问题”永远不够，必须有证据（通过的测试、构建输出、运行时数据）。

每个 skill 内部的验证是局部检查。而适用于*每一个*变更的项目级标准，无论当前激活的是哪个 skill，都是 Definition of Done（完成定义）：测试通过、无回归、行为已在运行时验证、文档已更新。参见 `../../references/definition-of-done.md`。它是对每个任务验收标准的补充，而不是替代。

## 需要避免的失败模式

这些细微错误看起来像是在提高效率，但会制造问题：

1. 未经检查就做出错误假设
2. 没有管理自己的困惑，在迷失时硬往前冲
3. 没有暴露你注意到的不一致
4. 对非显而易见的决策没有呈现权衡
5. 对明显有问题的方案逢迎（“Of course!”）
6. 把代码和 API 过度复杂化
7. 修改与任务无关的代码或注释
8. 删除你没有完全理解的东西
9. 因为“很明显”而在没有 spec 的情况下构建
10. 因为“看起来对”而跳过验证

## Skill 规则

1. **开始工作前检查是否有适用的 skill。** Skills 编码了能避免常见错误的流程。

2. **Skills 是工作流，不是建议。** 按顺序遵循步骤。不要跳过验证步骤。

3. **多个 skills 可以同时适用。** 一个功能实现可能会按顺序涉及 `idea-refine` → `spec-driven-development` → `planning-and-task-breakdown` → `incremental-implementation` → `test-driven-development` → `code-review-and-quality` → `code-simplification` → `shipping-and-launch`。

4. **拿不准时，从 spec 开始。** 如果任务不平凡且没有 spec，就从 `spec-driven-development` 开始。

## 生命周期顺序

对于完整功能，典型 skill 顺序是：

```
1.  interview-me                → Extract what the user actually wants
2.  idea-refine                 → Refine vague ideas
3.  spec-driven-development     → Define what we're building
4.  planning-and-task-breakdown → Break into verifiable chunks
5.  context-engineering         → Load the right context
6.  source-driven-development   → Verify against official docs
7.  incremental-implementation  → Build slice by slice
8.  observability-and-instrumentation → Instrument as you build (runs parallel with 7-9, not after)
9.  doubt-driven-development    → Cross-examine non-trivial decisions in-flight
10. test-driven-development     → Prove each slice works
11. code-review-and-quality     → Review before merge
12. code-simplification         → Reduce unnecessary complexity while preserving behavior
13. git-workflow-and-versioning → Clean commit history
14. documentation-and-adrs      → Document decisions
15. deprecation-and-migration   → Retire old systems and move users safely when needed
16. shipping-and-launch         → Deploy safely
```

并不是每个任务都需要每个 skill。一个 bug 修复可能只需要：`debugging-and-error-recovery` → `test-driven-development` → `code-review-and-quality`。

## 快速参考

| 阶段 | Skill | 一句话摘要 |
|-------|-------|-----------------|
| 定义 | interview-me | 在任何计划、spec 或代码存在之前，先弄清楚用户真正想要什么 |
| 定义 | idea-refine | 通过结构化的发散和收敛思考打磨想法 |
| 定义 | spec-driven-development | 在写代码前明确需求和验收标准 |
| 计划 | planning-and-task-breakdown | 拆解为小而可验证的任务 |
| 构建 | incremental-implementation | 薄的垂直切片，每次扩展前先测试 |
| 构建 | source-driven-development | 实现前先对照官方文档验证 |
| 构建 | doubt-driven-development | 用对抗式 fresh-context 审查每个非平凡决策 |
| 构建 | context-engineering | 在正确时间加载正确上下文 |
| 构建 | frontend-ui-engineering | 具备可访问性的生产级 UI |
| 构建 | api-and-interface-design | 有清晰契约的稳定接口 |
| 验证 | test-driven-development | 先写失败测试，再让它通过 |
| 验证 | browser-testing-with-devtools | 使用 Chrome DevTools MCP 做运行时验证 |
| 验证 | debugging-and-error-recovery | 复现 → 定位 → 修复 → 加保护 |
| 评审 | code-review-and-quality | 基于五个维度和质量门禁进行评审 |
| 评审 | code-simplification | 在保持行为不变的前提下减少不必要的复杂度 |
| 评审 | security-and-hardening | OWASP 防护、输入验证、最小权限 |
| 评审 | performance-optimization | 先测量，只优化重要内容 |
| 发布 | git-workflow-and-versioning | 原子提交、干净历史 |
| 发布 | ci-cd-and-automation | 每次变更都运行自动化质量门禁 |
| 发布 | deprecation-and-migration | 移除旧系统并安全地迁移用户 |
| 发布 | documentation-and-adrs | 记录为什么，而不只是记录做了什么 |
| 发布 | observability-and-instrumentation | 结构化日志、RED 指标、traces、基于症状的告警 |
| 发布 | shipping-and-launch | 发布前检查清单、监控、回滚计划 |
