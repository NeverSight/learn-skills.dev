---
name: open-insights
description: 基于本地多 Agent 工具（Cursor/ClaudeCode/OpenCode）会话记录生成使用洞察报告；仅在用户明确要求「生成会话分析报告」「做一份 Agent 使用洞察」或类似表述时调用
---

# Agent Insights

本技能支持分析 **Cursor**、**ClaudeCode** 和 **OpenCode** 三种主流 AI Agent 工具的本地会话记录。它按固定流程扫描、提取、汇总并调用 LLM 分析，最终生成一份可交互的 HTML 使用洞察报告。

## 支持的工具

| 工具 | 存储位置 | 文件格式 |
|------|---------|---------|
| Cursor | `~/.cursor/projects/` | JSONL |
| ClaudeCode | `~/.claude/projects/` | JSONL |
| OpenCode | `~/.local/share/opencode/storage/` | 分片 JSON |

## 处理流程

### 1. 内容读取

#### 1.1 扫描会话
- 执行 `bun run ./scripts/scan.ts` 扫描本地 Agent 会话数据
- 支持的命令行参数：
  - `--cursor`：仅扫描 Cursor
  - `--claude-code`：仅扫描 ClaudeCode
  - `--opencode`：仅扫描 OpenCode
  - `--all`：扫描所有已安装的工具
  - `--path=<路径>`：指定自定义数据路径

#### 1.2 选择要分析的工具
- 脚本会自动检测已安装的工具
- 用户可以选择扫描特定工具或所有已安装的工具
- 也可以指定自定义数据路径

#### 1.3 读取会话内容
- 扫描完成后，列出 `~/.agent-insights/conversations` 中的子目录
- 由用户**选择要分析的项目（对应一个子目录，支持多选全选，默认全部）**
- 根据所选目录，读取该目录下所有 `.md` 文件作为 Agent 对话内容

### 2. 摘要总结

```
请对 Agent 会话记录的这一部分进行摘要总结，重点关注：
1. 用户要求了什么
2. Agent 做了什么（使用了哪些工具、修改了哪些文件）
3. 遇到的摩擦或问题
4. 最终结果

保持简洁，3-5 句话。保留具体细节，如文件名、错误信息和用户反馈。

会话记录片段：
```

### 3. 特征提取

对会话内容进行结构化特征提取，**必须**遵守以下判定规则：

```
1. **goal_categories**：只统计**用户明确提出的请求**。
   - 不统计 Agent 主动进行的代码库探索或自行决定的工作
   - 仅在用户出现「你能…吗」「请…」「我需要…」「我们来…」等明确请求时计入

2. **user_satisfaction_counts**：只依据**用户明确表达的反馈**。
   - 「太棒了！「「很好！「「完美！」→ happy
   - 「谢谢」「看起来不错」「可以用了」→ satisfied
   - 「好的，现在让我们…」（无抱怨地继续）→ likely_satisfied
   - 「不对」「再试一次」→ dissatisfied
   - 「这坏了」「我放弃了」→ frustrated

3. **friction_counts**：按类型标注具体问题。
   - misunderstood_request：Agent 理解错误
   - wrong_approach：目标正确，但解法/思路错误
   - buggy_code：代码无法正常运行
   - user_rejected_action：用户拒绝或中止了某次工具调用
   - excessive_changes：过度设计或改动范围过大

4. 若会话极短或仅为热身，将目标类别标为 **warmup_minimal**。

会话内容：
<会话记录插入此处>

仅返回符合以下 schema 的有效 JSON 对象：
{
  "underlying_goal": "用户根本上想要实现的目标",
  "goal_categories": {"类别名": 数量, ...},
  "outcome": "fully_achieved | mostly_achieved | 
              partially_achieved | not_achieved | 
              unclear_from_transcript",
  "user_satisfaction_counts": {"级别": 数量, ...},
  "agent_helpfulness": "unhelpful | slightly_helpful | moderately_helpful | very_helpful | essential",
  "session_type": "single_task | multi_task | iterative_refinement | exploration | quick_question",
  "friction_counts": {"摩擦类型": 数量, ...},
  "friction_detail": "一句话描述摩擦点，或为空",
  "primary_success": "none | fast_accurate_search | correct_code_edits | good_explanations | proactive_help | multi_file_changes | good_debugging",
  "brief_summary": "一句话：用户想要什么以及是否达成"
}
```

#### 目标类别

| 类别 | 描述 |
| ------------------- | ---------- |
| debug_investigate | 调试/调查 |
| implement_feature | 实现功能 |
| fix_bug | 修复 Bug |
| write_script_tool | 编写脚本/工具 |
| refactor_code | 重构代码 |
| configure_system | 配置系统 |
| create_pr_commit | 创建 PR/提交 |
| analyze_data | 分析数据 |
| understand_codebase | 理解代码库 |
| write_tests | 编写测试 |
| write_docs | 编写文档 |
| deploy_infra | 部署/基础设施 |
| warmup_minimal | 缓存预热（最小会话） |

#### Agent 有用程度级别

unhelpful → slightly_helpful → moderately_helpful → very_helpful → essential

#### 会话类型

| 类型 | 描述 |
| -------------------- | ---------- |
| single_task | 单一聚焦任务 |
| multi_task | 一个会话中的多个任务 |
| iterative_refinement | 来回迭代优化 |
| exploration | 探索/理解代码库 |
| quick_question | 简短问答 |

#### 主要成功类别

| 类别 | 描述 |
| -------------------- | --------- |
| none | 没有显著成功 |
| fast_accurate_search | 快速准确的代码搜索 |
| correct_code_edits | 准确的代码修改 |
| good_explanations | 清晰的解释 |
| proactive_help | 超出要求的主动帮助 |
| multi_file_changes | 成功协调多文件编辑 |
| good_debugging | 有效的调试 |

### 4. 内容分析

在完成所有会话的摘要与特征提取后，将汇总数据传入多组**专项分析提示**，分别得到项目领域、交互风格、有效之处、摩擦、建议、未来展望和趣味结尾等结构化结果。

#### 传入分析提示的数据

每组分析提示均接收同一份汇总统计数据：

```json
{
  "sessions": "<总会话数>",
  "analyzed": "<已分析的会话数>",
  "date_range": { "start": "...", "end": "..." },
  "messages": "<总消息数>",
  "hours": "<总时长（小时）>",
  "commits": "<git 提交数>",
  "top_tools": ["使用量前8的工具"],
  "top_goals": ["前8个目标类别"],
  "outcomes": { "结果分布" },
  "satisfaction": { "满意度分布" },
  "friction": { "摩擦类型统计" },
  "success": { "成功类别统计" },
  "languages": { "语言使用统计" },
  "by_agent": { "各工具会话数统计" }
}
```

以及以下文本材料：
- **会话摘要**：最多 50 条简短摘要
- **摩擦详情**：从特征中提取的最多 20 条
- **用户对 Agent 的指示**：用户重复给出的最多 15 条
- **工具分布**：各 Agent 工具的会话数量

#### 4.1 项目领域分析

```
分析上述 Agent 使用数据，归纳出 4–5 个项目领域。
仅返回有效 JSON，跳过内部 CC 操作。

{
  "areas": [
    {
      "name": "领域名称",
      "session_count": N,
      "description": "2-3 句话，描述工作内容以及如何使用 Agent。"
    }
  ]
}
```

#### 4.2 交互风格分析

```
分析上述 Agent 使用数据，归纳用户与 Agent 的交互风格。
仅返回有效 JSON：

{
  "style": "简要描述其风格（2-3 句话）",
  "strengths": ["2-3 件做得好的事"],
  "patterns": ["2-3 个值得注意的工作模式"]
}
```

#### 4.3 有效之处分析

```
分析上述 Agent 使用数据，识别运作良好的部分。
仅返回有效 JSON，包含 2–3 个「重大成果」，需具体并引用实际会话：

{
  "big_wins": [
    {
      "title": "简短标题（4-6 个字）",
      "description": "2-3 句话描述一项令人印象深刻的成就"
    }
  ]
}
```

#### 4.4 摩擦分析

```
分析上述 Agent 使用数据，归纳摩擦规律。
仅返回有效 JSON，包含 2–3 个摩擦点，诚实且有建设性：

{
  "friction_points": [
    {
      "category": "类别名称",
      "frequency": "rare | occasional | frequent",
      "description": "2-3 句话描述该规律"
    }
  ]
}
```

#### 4.5 建议分析

```
分析上述 Agent 使用数据并生成可执行建议。
仅返回有效 JSON，features_to_try 与 usage_patterns 各 2–3 条，需针对其实际使用模式：

{
  "features_to_try": [
    {
      "feature": "功能名称",
      "benefit": "有什么帮助",
      "example": "来自其使用记录的具体示例"
    }
  ],
  "usage_patterns": [
    {
      "pattern": "模式名称",
      "benefit": "为什么有帮助",
      "example": "如何应用"
    }
  ]
}
```

#### 4.6 未来展望分析

```
分析上述 Agent 使用数据，提炼未来 3–6 个月可尝试的机会。
仅返回有效 JSON，包含 3 个机会，可涉及自主工作流、并行代理、对照测试迭代等：

{
  "intro": "关于 AI 辅助开发演进的 1 句话",
  "opportunities": [
    {
      "title": "简短标题（4-8 个字）",
      "whats_possible": "2-3 句话，关于自主工作流的宏大愿景",
      "how_to_try": "1-2 句话，提及相关工具",
      "copyable_prompt": "可直接使用的详细提示词"
    }
  ]
}
```

#### 4.7 趣味结尾（难忘瞬间）

```
分析上述 Agent 使用数据，从会话摘要中找出一个难忘的瞬间（有人情味、有趣或出人意料，而非统计数字）。
仅返回有效 JSON：

{
  "headline": "来自记录的令人难忘的定性瞬间——不是统计数字。要有人情味、有趣或出人意料。",
  "detail": "该瞬间发生的时间/背景简述"
}
```

### 5. 生成概览

最后进行一次 LLM 调用，将前述所有洞察汇总为「一览概要」执行摘要。

### 6. 生成报告

将前述所有汇总数据与 LLM 洞察按模板渲染为可交互的 HTML 报告。

输出路径：`~/.agent-insights/reports/agent-insights-report-YYYY-MM-DD.html`

### 报告章节

1. **一览概要**：执行摘要
2. **项目领域**：用户在做什么
3. **交互风格**：用户如何与 Agent 协作
4. **有效之处**：重大成果
5. **摩擦点**：出了哪些问题
6. **建议**：可尝试的功能与可采纳的模式
7. **未来展望**：后续可探索的机会
8. **趣味结尾**：一个难忘的瞬间
9. **工具分布**：各 Agent 工具的使用统计（新增）

---

## 使用示例

```bash
# 扫描所有已安装的工具
bun run ./scripts/scan.ts --all

# 仅扫描 Cursor
bun run ./scripts/scan.ts --cursor

# 仅扫描 ClaudeCode
bun run ./scripts/scan.ts --claude-code

# 指定自定义数据路径
bun run ./scripts/scan.ts --path=~/.custom-agent/data/
```
