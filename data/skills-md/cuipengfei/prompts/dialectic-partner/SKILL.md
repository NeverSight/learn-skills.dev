---
name: dialectic-partner
description: 当用户要为重要决策、设计或假设寻找对立观点、暴露盲点或检验立场时使用。
---

# 辩证伙伴技能

启动**辩证式辩论**，让你（主代理）与子代理作为**批判性思考伙伴**进行对话：

- 质疑隐含假设
- 探索边界情况和替代方案
- 发现推理中的盲点
- 帮助用户做出更明智的决策

**目标**：共同发现更好的答案，而非赢得争论。

## 执行步骤

### 第一步：确认辩论主题

使用 AskUserQuestion 确认：

- 辩论主题和范围
- 用户的初始倾向（如有）
- 具体关注点或焦点领域

### 第二步：选择子代理

根据辩论主题从可用 `subagent_type` 中选择最合适的。如不确定或选择的代理不可用，回退到 `general-purpose`。

**记录选择**：在辩论记录中注明选了哪个代理及原因。

### 第三步：提供具体上下文

**关键**：子代理无法访问你的对话历史。必须提供：

- 相关**文件路径**（子代理可自行读取）
- 代码变更辩论需提供**变更文件列表**，并告知子代理**运行 git diff**
- 任何**约束或需求**

**告知子代理**：在 Task prompt 中说明：

- **单工具调用规则**：每次 invoke 一个 function，等待 function_results 返回后再 invoke 下一个
- 若上下文不足，请自主寻找并报告找到的额外文件或上下文
- 作为辩证伙伴应：质疑假设、提出替代方案、识别边界情况、保持建设性

Task prompt 示例：

```
## 🚨 铁律：单工具调用 🚨

每次 invoke 一个 function，等待 function_results 返回后再 invoke 下一个。
禁止中途停下来，自主完成所有步骤后再汇报。

---

作为辩证伙伴，请质疑这个设计决策。

需审查的文件：
- /path/to/design.md
- /path/to/implementation.ts

如需查看代码变更，请运行：
- `git diff` 查看未暂存变更
- `git diff --staged` 查看已暂存变更

背景：[决策及理由的简要说明]

请：质疑假设、提出替代方案、识别风险。
若上下文不足，请自主寻找相关文件并报告。
```

### 第四步：进行辩论轮次

使用 **Task + resume** 进行多轮辩论：

```
# 首轮
Task(prompt: "...", subagent_type: "...", description: "辩论第 1 轮")
→ 返回 agentId

# 后续轮次
# 注意：resume 时仍需提供 subagent_type，但可选择不同类型
# 例如：首轮用 backend-architect，后续可换 security-auditor 获取不同视角
Task(prompt: "...", resume: agentId, subagent_type: "...", description: "辩论第 2 轮")
```

**每轮操作**：

1. 陈述你的立场或回应
2. 调用子代理进行质疑
3. 更新 `.debates/YYYY-MM-DD-topic.md` 记录本轮内容
4. 每轮结束使用 AskUserQuestion 获取用户输入

### 第五步：用户参与

在关键时刻使用 AskUserQuestion，选项如：

- "继续辩论" / "让代理继续"
- "我想补充..."
- "深入讨论 X"
- "总结并结束"
- "让代理自行决定"

### 第六步：实时持久化

辩论开始时创建 `.debates/YYYY-MM-DD-topic-slug.md`，并**提示用户辩论将记录到该文件**。

**创建目录时**：同时创建 `.debates/.gitignore`（内容 `*` + `!.gitignore`），确保辩论记录不污染 git 仓库。

```markdown
# Debate: [主题]

**Date**: YYYY-MM-DD
**Status**: in-progress
**AgentIds**: [记录使用过的 agentId，用于 resume]
**Participants**: Main Agent ↔ Sub Agent ([代理类型])
**Selection Rationale**: [选择该代理的原因]

---

## Round 1

> 📝 **记录原则**：每轮只记录核心论点和关键质疑，不需逐字记录。

**Main**: [核心观点，1-2 句]

**Sub**: [关键质疑，1-2 句]

**User**: [如有]

---
```

每轮结束后追加内容。

**辩论结束时**：

1. 追加 Conclusion 部分
2. 使用 AskUserQuestion 询问是否保留记录
3. 如保留：更新 Status 为 `completed`，填写 Outcome（`consensus` | `partial` | `disagreement`）
4. 如删除：删除文件

### 第七步：总结

**Soft Limit**：10 轮后建议总结。

结束时呈现：

- 发现的关键洞察
- 共识点
- 仍存在的分歧
- 用户的最终决策

## ⚠️ 主代理隔离原则（硬性规则）

**主代理不得在用户同意前根据子代理建议修改代码或文件。**

这是防止主代理被子代理"污染"或"感染"的关键规则：

- 子代理提出修改建议时，主代理只能**展示**，不能**执行**
- 任何代码/文件修改必须先通过 AskUserQuestion 获得用户**明确同意**
- 用户未同意或未响应时，不得执行任何修改
- 违反此规则视为**严重错误**

**正确流程**：

1. 子代理提出建议
2. 主代理向用户展示建议内容
3. 使用 AskUserQuestion 询问"是否采纳此建议？"
4. 用户同意后才执行修改
5. 在辩论记录中注明"用户已同意"

## 注意事项

- **单工具调用规则**（传递给子代理）：为规避已知 bug，子代理每次回复只能包含一个 function call，否则 resume 会失败。务必在 Task prompt 中加入此约束。
- **resume 需要 subagent_type**：即使使用 `resume: agentId` 继续对话，仍必须提供 `subagent_type` 参数
- **agentId 持久化**：在 `.debates/*.md` 文件头部记录 `AgentIds`，每次使用新子代理时追加。若 resume 失败，可尝试列表中的其他 agentId
- 子代理角色是"辩证伙伴"，不是"反对者"
- 信任 SOTA 模型能力，不必过度指定辩论技巧
