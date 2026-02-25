---
name: chat-profile-analysis
description: 通过AI分析聊天历史生成个性化用户画像报告。支持多种AI编程工具的聊天记录分析，包括Claude Code、OpenCode等。本技能强调AI驱动的灵活分析，而非死板模板。
---

# 聊天记录风格分析报告

## 概述

本技能通过分析用户与AI的对话历史，生成全面的个性化用户画像报告。重点关注沟通风格、性格特征、行为模式，并提供可操作的洞察和建议。

**核心理念**：使用AI理解和分析，而非僵化脚本。每个用户都是独特的，报告结构应根据实际数据特征动态调整。

## 支持的AI编程工具

| 编号 | 工具 | 数据格式 | 数据位置 | 状态 |
|------|------|----------|----------|------|
| 1 | Claude Code | JSONL | `~/.claude/history.jsonl` | ✅ 可用 |
| 2 | OpenCode | SQLite | `%USERPROFILE%\.local\share\opencode\opencode.db` | ✅ 可用 |
| 3 | [待添加] | - | - | 🚧 预留 |

---

## 步骤 0：选择数据源（必做）

当用户请求分析聊天记录时，**必须先询问用户要分析哪个工具**：

```
请选择要分析的AI编程工具：
1. Claude Code - 分析 ~/.claude/history.jsonl
2. OpenCode - 分析 SQLite 数据库
3. [其他工具 - 后续支持]

请输入编号或工具名称：
```

**重要**：只有当用户明确指定工具时，才跳过选择步骤。

---

## 步骤 1：加载聊天历史

根据用户选择的工具，加载对应的聊天历史数据。

### 工具 1：Claude Code（JSONL）

```
数据位置：
- ~/.claude/history.jsonl
- 用户提供的自定义路径

操作步骤：
1. 使用 read_file 工具加载历史文件
2. 解析 JSONL 格式（每行是一个JSON对象）
3. 提取关键信息：时间戳、消息内容、用户/AI角色
```

### 工具 1.5：Claude Code `/insights` 命令（增强分析）

**重要**：Claude Code 内置了 `/insights` 命令，可以直接生成使用洞察报告！

```
命令：在 Claude Code 中输入
/insights

输出：HTML报告文件
位置：~/.claude/usage-data/report.html
```

**为什么使用Insights**：

| 维度 | Insights分析 | 传统聊天分析 |
|------|------------|-------------|
| 数据来源 | 工具使用统计（Read/Edit/Bash等） | 对话文本 |
| 分析方式 | 量化统计 + AI推断 | 纯AI推断 |
| 独特价值 | 工作类型分布、摩擦点统计 | 语言风格、心理分析 |
| 可操作性 | 直接给出配置建议和Prompt模板 | 开放式建议 |

**Insights报告包含的独特维度**：

```
1. 工作类型分布
   - 错误修复占比（示例：71.5%）
   - 文档更新、调试、UI优化、功能实现占比

2. 编程语言使用统计
   - TypeScript、Python、JavaScript等使用频次

3. 工具使用频率
   - Read、Edit、TodoWrite、Write、Grep、Bash使用次数

4. 会话类型分布
   - 单任务、迭代优化、探索、多任务、快捷提问

5. 多会话并行分析
   - 并行会话数、涉及会话占比（示例：18%）

6. 时间段分布 + 工具错误统计
   - 按时间段的活跃度
   - 命令失败、编辑失败等错误类型统计

7. CLAUDE.md优化建议
   - 针对用户习惯的定制化文档建议

8. Hooks配置建议
   - 编辑后自动运行的类型检查等

9. TDD工作流模板
   - 测试驱动实现的Prompt模板
```

**推荐流程**：

1. 首先让用户运行 `/insights` 命令获取报告
2. 读取报告HTML或让用户导出为文本
3. 结合传统聊天分析进行综合评估
4. 基于Insights建议生成CLAUDE.md优化方案

### 工具 2：OpenCode（SQLite）

```
数据位置：
- Windows: %USERPROFILE%\.local\share\opencode\opencode.db
- macOS/Linux: ~/.local/share/opencode/opencode.db

数据库表结构：
┌─────────────┬────────────────────────────────────────────────────┐
│ 表名         │ 说明                                              │
├─────────────┼────────────────────────────────────────────────────┤
│ session     │ 会话信息                                          │
│   - id      │ 会话唯一标识                                      │
│   - title   │ 会话标题                                          │
│   - project_id │ 关联项目ID                                     │
│   - time_created │ 创建时间戳                                   │
│   - time_updated │ 更新时间戳                                   │
├─────────────┼────────────────────────────────────────────────────┤
│ message     │ 消息元数据                                       │
│   - id      │ 消息唯一标识                                      │
│   - session_id │ 所属会话ID                                     │
│   - data    │ JSON，包含：role, time{created}, agent, model   │
│             │   - role: "user" | "assistant" | "system"         │
│             │   - agent: Agent类型（如Sisyphus, multi-agent）   │
│             │   - model: 模型名称（如MiniMax, Claude等）         │
│             │   - tokenUsage: {input, output, total}            │
├─────────────┼────────────────────────────────────────────────────┤
│ part        │ 对话内容                                         │
│   - id      │ 内容唯一标识                                      │
│   - message_id │ 关联消息ID                                    │
│   - session_id │ 所属会话ID                                     │
│   - data    │ JSON，包含：type, text                          │
│             │   - type: "text" | "reasoning" | "tool_use"      │
│             │   - text: 实际对话文本                            │
├─────────────┼────────────────────────────────────────────────────┤
│ project     │ 项目信息                                         │
│   - id      │ 项目唯一标识                                      │
│   - name    │ 项目名称                                          │
│   - worktree│ 工作目录                                          │
└─────────────┴────────────────────────────────────────────────────┘

实际数据规模（参考示例）：
- 会话总数：190 个
- 消息总数：4,893 条
- 内容片段：19,929 个（part表）
- Token消耗：71,893,974（输入:69,998,758 / 输出:1,895,216）

关键数据发现示例（分析数据）：
┌─────────────────┬─────────────────┬────────────────────────┐
│ 维度             │ 数据             │ 说明                   │
├─────────────────┼─────────────────┼────────────────────────┤
│ 峰值时段         │ 18:00-19:00     │ 558条消息（最活跃）    │
│                  │ 13:00-14:00     │ 438条消息              │
│                  │ 01:00-02:00     │ 376条消息（夜猫子）    │
├─────────────────┼─────────────────┼────────────────────────┤
│ Agent使用分布    │ Sisyphus 64.8%  │ 主要Agent              │
│                  │ Multi-Agent 17.7%                       │
├─────────────────┼─────────────────┼────────────────────────┤
│ Model使用偏好   │ MiniMax 75%      │ 主要模型               │
└─────────────────┴─────────────────┴────────────────────────┘
```

操作步骤：
1. 使用 Python sqlite3 连接数据库
2. 查询 message 表获取角色、时间和 agent/model
3. 查询 part 表获取实际对话内容（type=text/reasoning）
4. 从 message.data 中解析 tokenUsage（可选）
5. 合并数据构建分析用消息列表

SQL查询示例：
```python
import sqlite3
import json
from collections import defaultdict

db_path = r"C:\Users\Administrator\.local\share\opencode\opencode.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ========== 基础查询 ==========

# 获取所有会话（按更新时间排序）
cursor.execute("SELECT id, title FROM session ORDER BY time_updated DESC LIMIT 10")
sessions = cursor.fetchall()

# 获取特定会话的所有消息
cursor.execute("""
    SELECT m.time_created, m.data, p.data as part_data
    FROM message m
    LEFT JOIN part p ON m.id = p.message_id
    WHERE m.session_id = ?
    ORDER BY m.time_created
""", (session_id,))

messages = []
for row in cursor.fetchall():
    msg_data = json.loads(row[1])
    part_data = json.loads(row[2]) if row[2] else {}
    
    role = msg_data.get('role')
    text = part_data.get('text', '')
    timestamp = msg_data.get('time', {}).get('created')
    
    if text and role in ['user', 'assistant']:
        messages.append({
            'role': role,
            'text': text,
            'timestamp': timestamp
        })

# ========== 增强查询：Token统计 ==========

# 获取所有消息的Token消耗
cursor.execute("""
    SELECT m.data
    FROM message m
    WHERE m.session_id = ?
""", (session_id,))

total_input = 0
total_output = 0

for row in cursor.fetchall():
    msg_data = json.loads(row[0])
    token_usage = msg_data.get('tokenUsage', {})
    total_input += token_usage.get('input', 0)
    total_output += token_usage.get('output', 0)

print(f"Input: {total_input}, Output: {total_output}, Total: {total_input + total_output}")

# ========== 增强查询：Agent分布 ==========

# 获取全局Agent使用统计
cursor.execute("""
    SELECT 
        json_extract(m.data, '$.agent') as agent,
        COUNT(*) as count
    FROM message m
    GROUP BY agent
    ORDER BY count DESC
""")
agent_stats = cursor.fetchall()
# 输出示例：[('sisyphus', 1245), ('multi-agent', 340), ...]

# ========== 增强查询：Model分布 ==========

# 获取全局Model使用统计
cursor.execute("""
    SELECT 
        json_extract(m.data, '$.model') as model,
        COUNT(*) as count
    FROM message m
    GROUP BY model
    ORDER BY count DESC
""")
model_stats = cursor.fetchall()
# 输出示例：[('MiniMax', 3670), ('Claude', 1223), ...]

# ========== 增强查询：时间模式 ==========

# 获取每小时的消息分布
cursor.execute("""
    SELECT 
        strftime('%H', datetime(m.time_created, 'unixepoch', 'localtime')) as hour,
        COUNT(*) as count
    FROM message m
    WHERE m.role = 'user'
    GROUP BY hour
    ORDER BY count DESC
""")
hourly_stats = cursor.fetchall()
# 输出示例：[('18', 558), ('13', 438), ('01', 376), ...]

# ========== 增强查询：项目分布 ==========

# 获取各项目的会话数
cursor.execute("""
    SELECT 
        p.name,
        COUNT(s.id) as session_count
    FROM session s
    LEFT JOIN project p ON s.project_id = p.id
    GROUP BY s.project_id
    ORDER BY session_count DESC
""")
project_stats = cursor.fetchall()
```
```

### 工具 N：添加新工具（预留）

如需添加新的AI编程工具支持，按以下格式添加：

```
### 工具 N：[工具名称]

数据格式：
[JSON/SQLite/其他]

数据位置：
[默认路径]

操作步骤：
1. [加载数据的方法]
2. [解析格式的方法]
3. [提取关键字段的方法]
```

---

## 步骤 2：查看框架参考（AI驱动）

在开始分析前，阅读框架参考以了解分析结构，但**不要死板遵循**：

```
read_file: references/analysis_framework.md
read_file: references/analysis_methods.md
```

**重要提示**：这些是参考资料，不是模板。根据以下因素调整分析：
- 实际数据特征
- 用户的独特特点
- 发现的显著模式
- 数据量和质量

---

## 步骤 3：执行AI驱动分析

使用AI灵活分析聊天历史。关注对这个特定用户重要的内容。

### 分析维度总览（20个）

| 编号 | 维度 | 来源 | 说明 |
|------|------|------|------|
| 3.0 | 深度数据挖掘 | 原创 | Token、Agent、Model偏好（SQLite增强） |
| 3.1 | 基础统计 | 原创 | 消息数、时间跨度、话题 |
| 3.2 | 时间模式 | 原创 | 活跃时段、频率趋势 |
| 3.3 | 互动模式 | 原创 | 发起方式、响应风格 |
| 3.4 | 语言风格 | 原创 | 词汇、情感、提问方式 |
| 3.5 | 人格评估 | 大五+BFI | 模拟BFI问卷回答增强准确性 |
| 3.6 | 潜在心理动机 | 知乎/心理侦探 | 深层需求、行为驱动力 |
| 3.7 | 矛盾与盲点 | 知乎/心理侦探 | 言行不一致、认知偏差 |
| 3.8 | 文化符号映射 | 知乎/心理侦探 | 语言习惯、价值观倾向 |
| **3.9** | **工作类型分布** | **Claude Insights** | **错误修复/文档/调试/UI优化/功能实现占比** |
| **3.10** | **编程语言统计** | **Claude Insights** | **TypeScript/Python/JS等使用频次** |
| **3.11** | **工具使用频率** | **Claude Insights** | **Read/Edit/TodoWrite/Grep/Bash使用次数** |
| **3.12** | **会话类型分布** | **Claude Insights** | **单任务/迭代优化/探索/多任务** |
| **3.13** | **多会话并行分析** | **Claude Insights** | **并行工作流、会话重叠率** |
| **3.14** | **摩擦点统计** | **Claude Insights** | **工具错误类型、错误频率** |
| 3.15 | 行为模式 | 原创 | 重复模式、触发条件 |
| 3.16 | 核心价值观 | 原创 | 原则、优先级、边界 |
| 3.17 | 问题发现 | 原创 | 返工、沟通、效率问题 |
| 3.18 | CLAUDE.md优化 | Claude Insights | 针对习惯的定制化配置建议 |
| 3.19 | 个性化建议 | 原创 | 可操作的改进建议 |

**关键原则**：每个结论必须标注置信度 [高/中/低]

**分析顺序建议**：
1. 如果用户使用Claude Code，优先运行 `/insights` 获取量化数据（3.9-3.14）
2. 结合传统聊天分析（3.1-3.8）
3. 生成综合建议（3.15-3.19）

### 3.0 深度数据挖掘（增强版）

对于OpenCode等SQLite数据源，建议提取以下增强指标：

```
AI任务：
"从聊天历史中提取以下深度指标：

1. **Token消耗统计**（如有）：
   - 总输入/输出Token
   - 平均每次对话Token
   - Token使用趋势

2. **Agent使用偏好**：
   - 各种Agent的使用次数和占比
   - 用户偏好的Agent类型

3. **模型使用偏好**：
   - 使用的模型及频率
   - 模型切换模式

4. **消息长度分布**：
   - 最短/最长/平均/中位数
   - 长文本比例

5. **项目分布**：
   - 各项目的会话数/消息数
   - 主要活跃项目"
```

### 3.1 提取基础统计

```
AI任务：
"从聊天历史中提取：
1. 消息总数
2. 时间跨度（第一条到最后一条消息）
3. 讨论的主要话题/项目
4. 消息频率模式"
```

### 3.2 分析时间模式

```
AI任务：
"分析这些消息的时间分布：
1. 最活跃的时间段
2. 使用频率随时间的变化趋势
3. 任何规律性模式（每日、每周）"
```

### 3.3 分析互动模式

```
AI任务：
"分析用户的互动风格：
1. 用户如何发起对话？
2. 是命令式、提问式还是讨论式？
3. 用户如何回应AI？
4. 在对话中的控制程度"
```

### 3.4 分析语言风格

```
AI任务：
"分析用户的语言特征：
1. 消息长度模式（简洁 vs 详细）
2. 情感表达（批评、赞扬、中性）
3. 提问模式
4. 技术术语的使用
5. 任何独特的短语或表达"
```

### 3.5 人格评估（大五人格 + BFI问卷模拟）

```
AI任务：
"基于大五人格模型进行评估（可模拟BFI问卷回答以增强准确性）：

1. **外向性** (⭐⭐⭐⭐⭐ 到 ⭐)
   - 社交活跃度
   - 表达频率
   - 聊天记录中的证据

2. **宜人性** (⭐⭐⭐⭐⭐ 到 ⭐)
   - 合作意愿
   - 同理心指标
   - 聊天记录中的证据

3. **尽责性** (⭐⭐⭐⭐⭐ 到 ⭐)
   - 计划行为
   - 细节关注度
   - 聊天记录中的证据

4. **神经质** (⭐⭐⭐⭐⭐ 到 ⭐)
   - 情绪稳定性
   - 压力反应
   - 聊天记录中的证据

5. **开放性** (⭐⭐⭐⭐⭐ 到 ⭐)
   - 接受新事物的程度
   - 创造力指标
   - 聊天记录中的证据

**重要**：为每个评分提供具体证据，并标注置信度 [高/中/低]"
```

### 3.6 潜在心理动机（新增）

```
AI任务：
"基于对话分析用户的深层心理动机：

1. **核心需求**：
   - 用户最频繁寻求的是什么？（知识？效率？陪伴？认可？）
   - 潜在的情感需求是什么？

2. **行为驱动力**：
   - 什么触发用户发起对话？
   - 期待从AI获得什么价值？

3. **动机强度**：
   - 持续使用AI的动力来源
   - 深层心理诉求

**强调**：尖锐深刻，挖掘真实动机，不要表面化解读"
```

### 3.7 矛盾与盲点（新增）

```
AI任务：
"识别用户的言行矛盾和认知盲点：

1. **言行不一致**：
   - 说了但没做到的事
   - 观点与行为矛盾

2. **认知盲点**：
   - 用户没意识到自己的特点
   - 可能的自我认知偏差

3. **潜在问题**：
   - 自己没发现但可能影响效率的问题
   - 思维定式或偏见

**格式**：每个发现标注 [高/中/低] 置信度"
```

### 3.8 文化符号映射（新增）

```
AI任务：
"分析用户的语言习惯和文化特征：

1. **语言风格**：
   - 常用词汇/短语
   - 方言或网络用语
   - 中英文混用习惯

2. **价值观倾向**：
   - 东方 vs 西方思维
   - 集体主义 vs 个人主义倾向
   - 传统 vs 现代

3. **身份认同**：
   - 技术/职业身份表达
   - 圈层文化特征
   - 自我定位"
```

### 3.9 工作类型分布（Claude Code Insights）

```
AI任务：
"基于 /insights 报告或聊天内容，分析用户的工作类型分布：

1. **需求类型分布**：
   - 错误修复占比（示例：71.5%）
   - 文档更新占比
   - 调试占比
   - UI优化占比
   - 产品设计建议占比
   - 功能实现占比

2. **工作重心**：
   - 主要时间花在什么类型的工作上？
   - 有什么值得注意的偏向？

**数据来源**：Claude Code /insights 报告中的「你的需求」统计"
```

### 3.10 编程语言统计（Claude Code Insights）

```
AI任务：
"分析用户使用的编程语言分布：

1. **主要语言**：
   - 最常用的语言（TypeScript/Python/JavaScript等）
   - 使用频次

2. **语言多样性**：
   - 使用多少种语言
   - 主语言vs辅助语言

**数据来源**：Claude Code /insights 报告中的「编程语言」统计"
```

### 3.11 工具使用频率（Claude Code Insights）

```
AI任务：
"分析用户最常用的工具/命令：

1. **工具使用排行**：
   - Read（代码阅读）使用次数
   - Edit（代码编辑）使用次数
   - TodoWrite（任务规划）使用次数
   - Write（文件写入）使用次数
   - Grep（代码搜索）使用次数
   - Bash（终端命令）使用次数

2. **读改比率**：
   - Read/Edit 比率分析
   - 反映用户的工作模式（探索型 vs 实现型）

**数据来源**：Claude Code /insights 报告中的「最常用工具」统计"
```

### 3.12 会话类型分布（Claude Code Insights）

```
AI任务：
"分析用户的会话类型分布：

1. **会话类型**：
   - 单任务：一次性完成一个任务
   - 迭代优化：在同一个会话中多次修改
   - 探索：让AI探索代码库
   - 多任务：一个会话处理多个任务
   - 快速提问：简单的问答

2. **主导类型**：
   - 用户最常用的会话模式是什么？
   - 这反映了什么工作风格？

**数据来源**：Claude Code /insights 报告中的「会话类型」统计"
```

### 3.13 多会话并行分析（Claude Code Insights）

```
AI任务：
"分析用户的多会话并行工作模式：

1. **并行程度**：
   - 同时运行的会话数
   - 会话重叠事件数
   - 涉及并行会话的消息占比（示例：18%）

2. **并行工作流**：
   - 用户习惯同时处理多个任务
   - 这反映了什么工作习惯？

**数据来源**：Claude Code /insights 报告中的「多会话并行」统计"
```

### 3.14 摩擦点统计（Claude Code Insights）

```
AI任务：
"分析用户遇到的摩擦点和工具错误：

1. **时间段分布**：
   - 上午(6-12)、下午(12-18)、傍晚(18-24)、夜间(0-6)
   - 哪个时间段最活跃？

2. **工具错误类型**：
   - 命令失败次数
   - 编辑失败次数
   - 文件未找到次数
   - 用户拒绝次数

3. **常见问题**：
   - 最频繁的错误是什么？
   - 这些错误有什么规律？

**数据来源**：Claude Code /insights 报告中的「遇到的工具错误」统计"
```

### 3.15 识别行为模式

```
AI任务：
"识别重复出现的行为模式：
1. 什么触发了某些行为？
2. 典型的响应是什么？
3. 潜在的动机是什么？

格式： 
- 模式名称
- 触发条件
- 典型表现（附引用）
- 行为解读
- 出现频率
- [置信度：高/中/低]"
```

### 3.16 提取核心价值观

```
AI任务：
"识别用户的核心原则和价值观：
1. 反复强调的理念
2. 决策时的优先级顺序
3. 行为边界（必须做/不能做的事）

提供具体引用作为证据，标注置信度。"
```

### 3.17 发现问题

```
AI任务：
"识别潜在问题或改进机会：
1. 返工或重复尝试
2. 沟通差距或误解
3. 可能影响协作的情绪表达
4. 流程低效

为每个问题评定严重程度：高/中/低"
```

### 3.18 CLAUDE.md优化建议

```
AI任务：
"基于分析结果，生成CLAUDE.md优化建议：

1. **文档简洁原则**：
   - 建议添加什么约束？
   - 避免冗长的描述

2. **技术栈约束**：
   - 框架版本限制
   - 认证模式规范
   - 导入/导出模式

3. **自定义规则**：
   - 针对用户常见错误的预防规则
   - 特定文件的处理方式

**数据来源**：Claude Code /insights 报告中的「建议的CLAUDE.md添加项」

**输出格式**：
```markdown
## 建议添加到 CLAUDE.md 的内容

1. [建议1的具体内容]
2. [建议2的具体内容]
3. [建议3的具体内容]
```
"
```

### 3.19 生成个性化建议

```
AI任务：
"基于识别的问题，生成可操作的建议：
1. 针对每个问题的具体解决方案
2. 适合用户风格的沟通模板
3. 流程改进建议
4. 工具和工作流优化

为每条建议提供：
- 预期收益
- 实施难度
- 具体步骤"
```

---

## 步骤 4：生成报告

将所有分析结果综合成一份全面的Markdown报告。

**报告结构**（动态调整，增强版）：

```markdown
# 用户聊天记录个人分析报告（增强版）

**分析日期**: [当前日期]
**数据源**: [工具名称 + 文件路径/数据库位置]
**分析范围**: [消息数量、时间跨度]

---

## 📊 数据概览

### 核心指标（增强版）
| 指标 | 数值 | 说明 |
|------|------|------|
| 会话总数 | [X] | [X]个项目 |
| 消息总数 | [X] | 含user/assistant |
| [Token消耗] | [X] | 输入:X / 输出:X |
| 日均消息 | [X] | [计算] |
| 平均消息长度 | [X]字符 | 最短X，最长X |

### 时间分布
| 时段 | 消息数 | 活跃度 |
|------|--------|--------|
| [时间1] | [X] | 🔥 |
| [时间2] | [X] | |

[时间模式分析]

### 项目分布
| 项目 | 会话数 | 消息数 | 占比 |
|------|--------|--------|------|
| [项目1] | [X] | [X] | [X]% |
| [项目2] | [X] | [X] | [X]% |

---

## 🧠 Agent/模型使用偏好（增强版）

### 主要Agent分布
| Agent | 使用次数 | 占比 |
|-------|----------|------|
| [Agent1] | [X] | [X]% |
| [Agent2] | [X] | [X]% |

### 模型使用偏好
| 模型 | 使用次数 | 占比 |
|------|----------|------|
| [模型1] | [X] | [X]% |
| [模型2] | [X] | [X]% |

---

## 💬 互动模式分析

[用户如何与AI互动]

---

## 🗣️ 语言风格分析

[用户的沟通特征]

---

## 🧠 人格特质分析

[大五人格评估及证据]

---

## 💻 行为画像

[技能、工具、工作模式]

---

## 🎯 核心价值观与原则

[反复强调的理念]

---

## ⚠️ 发现的问题

[问题及其影响]

---

## ✅ 改进建议

[具体、可操作的建议]

---

## 📋 综合画像总结

[一句话总结 + 维度画像]

---

## 📎 附录

[引用的对话，分析依据、局限性]
```

**关键原则**：
1. **基于证据**：每个结论都必须有实际聊天引用支撑
2. **具体**：使用具体例子，而非模糊描述
3. **个性化**：突出该用户的独特特征
4. **可操作**：建议应该具体且可实施
5. **客观**：避免主观偏见，保持中立语气
6. **灵活**：根据数据特征调整报告结构

### 工具特定字段（可选）

根据数据来源，可在报告中添加特定信息：

**OpenCode 专有**：
```markdown
## 🔧 OpenCode 额外分析

### 项目分布
[各项目的会话数、消息数]

### 常用Agent
[用户偏好的Agent类型]

### Token消耗
[输入/输出/推理Token统计]
```

---

## 步骤 5：保存与交付

保存生成的报告：

```markdown
文件名: 用户聊天记录个人分析报告.md
位置: 当前工作区目录
```

告知用户：
- 报告已生成
- 报告文件位置
- 关键发现摘要
- 后续步骤（可选）

---

## 步骤 6：生成可视化提示词（AI 绘图专用）

**重要功能**：在完成分析报告后，自动生成 3-5 个 AI 绘图提示词，用于在 Midjourney、DALL-E、Stable Diffusion 等工具中生成高密度信息图。

### 6.1 提示词生成原则

```
AI任务：
"基于生成的分析报告，从以下维度提取关键信息并生成高密度信息图提示词：

📐 固定规格要求：
- 尺寸：9:16 竖版（vertical format）
- 质量：4K ultra HD
- 风格：**高密度信息图**（dense infographic）
- 布局：**文字密集 + 适当配图**，多面板分区
- 字体：Microsoft YaHei 或 Heiti（必须明确指定）
- 标题：固定显示 'Chat Profile Analysis 个人分析报告'
- 质量控制：字体清晰、无错别字、无笔画错误
- 适合平台：小红书、LinkedIn、朋友圈分享

🎨 推荐生成角度（5个，建议全部生成）：
1. 人格特质雷达图 - 大五人格评分 + 行为标签
2. 工作模式时间轴 - 双峰分布 + Token统计
3. Agent/模型使用分布 - 工具偏好 + 模型切换
4. 核心价值观海报 - 价值观体系 + 行为红线
5. 综合技能画像 - 技能雷达 + 项目分布 + 工具生态

⚡ 增强要求：
- 每个提示词至少包含10个以上数据点
- 使用【】标注中文分组标题
- 使用📊📁🔧等emoji作为视觉元素
- 描述统计图表类型（radar chart, bar chart, timeline等）
"
```

### 6.2 提示词生成模板（高密度版）

每个提示词应遵循以下结构：

```
### 提示词 [编号]：[主题名称]（高密度版）

**可视化角度**：[完整描述图表展示内容]

**关键数据提取**：
- [数据点1及说明]
- [数据点2及说明]
- [数据点3及说明]
- [数据点4及说明]
- [数据点5及说明]
- [...更多数据点]

**AI绘图提示词**：
```
[完整的英文提示词，包含：
- 9:16 vertical format 声明
- 标题 "Chat Profile Analysis 个人分析报告"
- 详细的各区块中文数据标签，使用【】分组
- Microsoft YaHei 或 Heiti 字体声明
- 4K ultra HD 质量声明
- dense multi-panel layout 或 high information density 声明
- radar chart / timeline / donut chart / bar chart 等图表类型
- 配色方案
- 清晰度要求（highly legible, crystal clear, no typos）
- 适当配图（icons, symbols等）
]
```

### 6.3 示例提示词参考（高密度版）

**示例 1：人格特质雷达图（高密度版）**

```
A 9:16 vertical ultra-detailed infographic poster with title "Chat Profile Analysis 个人分析报告" at top center in bold Microsoft YaHei or Heiti font, 4K ultra HD resolution, featuring a comprehensive personality radar chart with Big Five traits in Chinese with detailed descriptions:

【大五人格评估】
尽责性(Conscientiousness) 100/100 ⭐⭐⭐⭐⭐ - 任务明确，要求明确
开放性(Openness) 100/100 ⭐⭐⭐⭐⭐ - 尝试多种工具/模型
宜人性(Agreeableness) 80/100 ⭐⭐⭐⭐ - 尊重AI，合作顺畅
外向性(Extraversion) 60/100 ⭐⭐⭐ - 线上活跃但非社交型
神经质(Neuroticism) 40/100 ⭐⭐ - 情绪稳定，理性决策

【行为特征标签】
🔧 技术极客 | 📈 效率至上 | 🛡️ 风险意识 | 🔄 迭代改进 | 🎯 结果导向

Dense multi-panel layout, Microsoft YaHei or Heiti font for all Chinese text, highly legible and crystal clear typography with no typos or character errors, modern dark blue gradient background with white and light blue accents, minimalist radar chart visualization, professional data visualization style, each dimension with icon representation, balanced composition with clear sections, corporate infographic aesthetic, high information density, suitable for LinkedIn sharing.
```

**示例 2：沟通风格词云**

```
A 9:16 vertical infographic poster titled "Chat Profile Analysis 个人分析报告",
4K resolution, dense word cloud visualization with Chinese keywords sized by frequency:
"是"(largest, 50+), "确认"(large, 15+), "推送"(medium, 8+),
"效率至上", "实用主义", "极简风格", "命令式表达", "快速迭代".
Microsoft YaHei or Heiti font, crystal clear typography, no spelling mistakes,
modern gradient color scheme (blue to purple), larger words more prominent,
minimal decorative elements, professional infographic style,
white background with colorful text, centered layout.
```

**示例 3：行为模式时间轴**

```
A 9:16 vertical infographic poster with "Chat Profile Analysis 个人分析报告" header,
4K quality, showing a vertical timeline of activity patterns with Chinese labels:
"活跃时间：凌晨2点", "高频开发期：2026年1月3-12日", 
"项目类型：React/Vue全栈", "工作模式：双轨并行".
Dense information layout, Microsoft YaHei or Heiti font, highly readable,
no character errors, timeline dots connected by lines,
navy blue and white color scheme, clock icons for time markers,
professional corporate style, clean modern design, balanced spacing.
```

**示例 4：核心价值观海报**

```
A 9:16 vertical poster design titled "Chat Profile Analysis 个人分析报告",
4K ultra HD, featuring core values in bold Chinese characters:
"效率至上" (top, largest), "实用主义优先", "质量第一", 
"持续迭代", "结果导向", arranged in hierarchical layout.
Microsoft YaHei or Heiti bold font, crystal clear and legible,
no typos, minimalist design with geometric shapes,
gradient background (dark blue to light blue),
white text with subtle shadows, modern corporate aesthetic,
balanced negative space, professional infographic style.
```

**示例 5：技能能力图谱**

```
A 9:16 vertical infographic poster with "Chat Profile Analysis 个人分析报告" title,
4K resolution, displaying a skill tree diagram with Chinese tech labels:
"前端开发：React/Vue", "后端：Node.js", "部署：Vercel/Netlify",
"工具：Claude Code", "AI集成", connected by lines showing relationships.
Dense layout, Microsoft YaHei or Heiti font, highly legible typography,
no spelling errors, tree structure with nodes and connections,
blue and green color coding by skill category,
tech icons alongside text, modern flat design,
professional data visualization style, clean composition.
```

### 6.4 生成与追加到报告

将生成的提示词作为新章节追加到 Markdown 报告末尾：

```markdown
---

## 🎨 AI 绘图提示词生成

> 以下提示词可用于 Midjourney、DALL-E 3、Stable Diffusion 等 AI 绘图工具，生成个性化信息图海报

### 📋 使用说明

1. **选择提示词**：从下方 3-5 个提示词中选择你想要的可视化角度
2. **复制提示词**：复制完整的提示词文本（在代码块内）
3. **粘贴到 AI 绘图工具**：
   - Midjourney: `/imagine` 命令后粘贴
   - DALL-E 3: 直接粘贴到对话框
   - Stable Diffusion: 粘贴到 prompt 输入框
4. **生成图片**：等待 AI 生成，可能需要 30-60 秒
5. **调整优化**：根据生成效果可微调提示词重新生成

### 🎯 推荐用途

- 📱 小红书/朋友圈分享配图
- 📊 个人品牌展示素材
- 📈 工作汇报视觉化呈现
- 🎁 打印装裱作为纪念

---

[在此处插入 3-5 个生成的具体提示词]

---

💡 **提示**：生成的图片可能与预期有差异，建议多次生成选择最佳效果。如需修改字体或布局，可在提示词中调整相应描述。
```

### 6.5 质量检查清单

在生成提示词后，确保：

- [ ] 每个提示词都明确指定了 9:16 竖版格式
- [ ] 标题 "Chat Profile Analysis 个人分析报告" 已包含
- [ ] 中文内容来自真实报告数据（非虚构）
- [ ] 字体明确指定为 Microsoft YaHei 或 Heiti
- [ ] 包含 4K ultra HD 质量声明
- [ ] 包含清晰度要求（legible, crystal clear, no typos）
- [ ] 提供了 3-5 个不同维度的提示词
- [ ] 每个提示词都有简短的使用说明
- [ ] 提示词格式易于复制（代码块包裹）

---

## 重要提醒

### ✅ 应该做的

- **使用AI理解上下文和语义**
- **引用原始消息作为证据**
- **根据数据特征调整分析结构**
- **提供具体、可操作的建议**
- **突出用户的独特特征**
- **保持客观、中立的语气**
- **标注结论的置信度**

### ❌ 不应该做的

- **不要死板遵循模板**
- **不要套用机械公式**
- **不要在没有证据的情况下下结论**
- **不要过度推测**
- **不要使用一刀切的方法**
- **不要生成通用性报告**

---

## 资源文档

本技能包含参考文档：

### references/analysis_framework.md
提供报告结构参考（非死板模板）。包含：
- 报告核心结构
- 分析维度
- 重要原则
- 分析工作流

### references/analysis_methods.md
提供AI驱动的分析方法。包含：
- 核心原则（AI优先、个性化、证据驱动）
- 分析维度（时间，内容、情感、互动、人格）
- 行为模式识别方法
- 问题发现方法
- 建议生成方法
- 报告撰写原则
- 质量检查清单

### references/EXAMPLE_PROMPTS.md
提供AI绘图提示词示例（用于步骤6）。包含：
- 5个完整的提示词模板
- 使用说明和技巧
- 自定义修改指南
- 常见问题解答
- 适用场景建议

**使用说明**：分析前阅读这些参考文档，但将其作为指导而非严格规则。每个用户的报告都应该是独特的。

---

## 使用示例

### 示例 1：分析 Claude Code

**用户请求**：
```
分析我的聊天记录,生成用户画像报告
```

**AI操作**：
1. 询问用户选择数据源（用户选择 Claude Code）
2. 加载 `~/.claude/history.jsonl`
3. 阅读框架参考文档
4. 执行AI驱动分析
5. 生成个性化报告
6. 生成 AI 绘图提示词
7. 保存并通知用户

### 示例 2：分析 OpenCode

**用户请求**：
```
分析我在 OpenCode 的聊天记录
```

**AI操作**：
1. 询问用户选择数据源（用户选择 OpenCode）
2. 连接 SQLite 数据库并查询数据
3. 阅读框架参考文档
4. 执行AI驱动分析
5. 生成个性化报告
6. 生成 AI 绘图提示词
7. 保存并通知用户

---

## 成功关键因素

1. **AI驱动分析** - 让AI理解语义，不要使用僵化公式
2. **动态结构** - 根据每个用户的独特数据调整报告
3. **基于证据** - 所有结论都有实际聊天引用支持
4. **可操作洞察** - 提供具体、可实施的建议
5. **个性化** - 没有两份报告应该完全相同
6. **可视化支持** - 生成高质量 AI 绘图提示词，让报告更具传播力

---

## 附录：添加新工具指南

如需添加新的AI编程工具支持，请按以下格式在 "支持的AI编程工具" 章节添加：

```markdown
### 工具 N：[工具名称]

| 属性 | 值 |
|------|-----|
| 数据格式 | [JSON/SQLite/其他] |
| 数据位置 | [默认路径] |
| 关键字段 | [role, text, timestamp等] |

#### 数据加载步骤
1. [加载数据的方法]
2. [解析格式的方法]
3. [提取关键字段的方法]

#### 注意事项
[该工具特有的注意事项]
```

---

**技能版本**: 2.5  
**最后更新**: 2026-02-20  
**更新内容**: 
- 重构为多工具支持架构
- 新增工具选择菜单（步骤0）
- 新增 OpenCode SQLite 数据源支持
- 预留添加新工具的位置
- 新增深度数据挖掘维度（Token、Agent、模型偏好）
- 增强版报告模板（核心指标、时间分布、项目分布）
- **高密度信息图提示词生成**（文字密集、适当配图）
- **补充数据库详细表结构**（session/message/part/project）
- **补充SQL查询示例**（Token统计、Agent/Model分布、时间模式）
- **补充实际数据发现参考**（190会话、4893消息、7189万Token）
- **新增分析维度**：潜在心理动机、矛盾与盲点、文化符号映射
- **新增BFI问卷模拟**：增强大五人格评估准确性
- **新增置信度标注**：每个结论标注 High/Medium/Low
- **【重大更新】新增 Claude Code /insights 命令支持**
  - 步骤1.5：新增 /insights 命令使用说明
  - 3.9-3.14：新增6个Claude Code Insights专属分析维度
    - 工作类型分布（错误修复/文档/调试/UI优化/功能实现）
    - 编程语言统计（TypeScript/Python/JS等）
    - 工具使用频率（Read/Edit/TodoWrite等）
    - 会话类型分布（单任务/迭代优化/探索等）
    - 多会话并行分析（并行工作流、18%消息占比）
    - 摩擦点统计（工具错误类型、错误频率）
  - 3.18：新增CLAUDE.md优化建议生成

