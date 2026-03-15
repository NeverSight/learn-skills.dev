---
name: deepthink
description: Use when user asks with /deepthink prefix, or wants deep analysis - triggers adaptive structured reasoning with automatic complexity detection. Uses effort-based depth control (low/medium/high) similar to Claude's adaptive thinking mechanism.
---

# /deepthink - Smart Deep Thinking Skill

## When to Use
- User writes `/deepthink xxx`
- Complex problem solving, research, step-by-step thinking
- User wants high-confidence, well-reasoned answers

---

## Core Protocol

> **Note**: Use **sequentialthinking MCP** to structure the reasoning process.
> Inspired by Claude's adaptive thinking: automatically detect complexity and adjust reasoning depth.

### 1. 问题拆解

> **假设检查**: 第一轮思考后，必须列出关键假设，并问"这些假设都对吗？"适用任何问题，对抗"初始假设锁定"。

- 拆解为最小逻辑子问题，按依赖顺序排列
- 明确最终目标和成功标准
- 设定目标置信度 (High/Medium/Low)

**复杂度评估（Effort级别）**：
根据问题类型动态评估所需的思考深度

| Effort级别 | 问题特征 | 思考轮次 |
|-----------|---------|---------|
| **low** | 简单事实查询、数学推导、单一维度分析 | 2-3轮 |
| **medium** | 需要多角度分析、有模糊性、可能需要搜索 | 5-6轮 |
| **high** | 复杂推理、多系统交互、需要深度论证 | 7-9轮 |

**复杂度判断规则**：
- 是否需要外部信息搜索？→ +1级，且**必须进行搜索验证**
- 是否涉及多个子问题？→ +1级
- 是否有道德/伦理/价值判断？→ +1级
- 是否是纯逻辑/数学问题？→ -1级（可简化）
- 是否是简单事实查询？→ 直接回答，不启动deepthink

**搜索和提问规则**：
- **确认时间**：搜索前先确认当前时间（日期/年份），避免使用过时的信息
- **联动规则**：复杂度评估中判断"需要外部信息搜索"的维度，必须进行搜索验证——不能因为"觉得我已知道"而不搜索
- **评估当下是否需要搜索**：遇到不确定的信息就搜索，遵循自然的"我不确定，所以要查"
- **如对问题有疑问**: 立即使用 AskUserQuestion 工具提问

### 2. 苏格拉底提问
选择适用的追问：

1. **Clarify** - 我真正理解问题了吗？→ **如有疑问必须使用 AskUserQuestion 工具提问**
2. **Assumptions** - 我做了什么假设？
3. **Evidence** - 需要什么证据？不确定的信息有哪些？
4. **Counterexamples** - 有反例吗？
5. **Alternatives** - 有其他方案吗？
6. **Consequences** - 错了会怎样？

**5 Whys** - 仅在寻找根因时使用

### 3. 多层次分析
对每个子问题循环执行：

- **Tree of Thoughts (ToT)**: 复杂问题先探索2-3条推理路径，比较后再深入
- **理解**: 用自己的话重述，列出假设和边界
- **规划**: 头脑风暴N个策略，评估优缺点
- **执行**: 步步为营，需要外部信息→立即搜索验证
- **验证**: 检查逻辑一致性，寻找矛盾，测试边界
- **假设验证**: 列出关键假设，通过迭代自行验证假设是否成立
- **证据支撑**: 每轮论证需有信息源或推理依据支撑，避免空泛推演

### 4. 验证
根据问题类型选择验证方式：

- **反思机制**: 前提反转结论还成立吗？最弱链是哪个假设？
- **第一性原理**: 剥离表象，最核心的物理/逻辑约束是什么？
- **逆向验证**: 从目标倒推，必经路径是什么？
- **自洽性检验**: 如果用完全不同的推理路径重新分析，结论是否仍然一致？

**动态评估**：在验证阶段，必须评估当前思考轮次是否足够：
- 是否还有重要维度未充分展开？
- 是否有新发现需要追加思考？
- 如需要，继续追加思考轮次

### 5. 迭代
如满足任一条件则迭代：
- 问题涉及多个子系统
- 结论依赖多个假设
- 置信度为 Low/Medium

迭代流程：重新定义问题 → 补充证据 → 重新分析 → 验证

### 6. 流程完整性确认
输出结论前，确认以下步骤都已执行：
- ToT多路径探索是否完成？
- 验证（反思/第一性原理/逆向/自洽性检验）是否完成？
- 论证是否有证据支撑（信息源或推理依据）？
- 迭代是否完成（如果需要）？
- 如有遗漏，补充完成后再输出结论

---

## 工具使用

遇到不确定的信息时，自然的"我不确定，所以要查"

**显式使用 ReAct 循环：**
- **Reason**: 我需要查什么？明确要搜索的问题
- **Act**: 调用搜索/读取等工具
- **Observe**: 看工具返回的结果
- **Reason**: 基于结果继续推理

- **Never guess**: 不确定的信息先搜索验证
- **工具返回后**: 基于新信息重新验证

---

## 输出格式

```
---
## 🤔 DeepThink 分析

### 核心问题
[1句话概括真正问题]

### 关键假设
[列出分析中的关键假设，自行迭代验证]

### 结论
[最终答案]

### 一句话总结
[用一句话概括核心建议]

### 置信度: [High/Medium/Low]
---
```

## 流程图

```
问题 → 问题拆解 → ToT多路径探索 → 苏格拉底提问 → 多层次分析
    ↓
验证（反思/第一性/逆向/自洽性）←— 迭代（如需要）
    ↓
流程完整性确认 → 总结输出 + 置信度
```
