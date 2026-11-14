---
name: tool-call-repair
description: 工具调用输入修复管线。当构建或调试 LLM tool calling 层时使用此 skill——尤其是接入开源模型（DeepSeek、GLM、Qwen 等）发现工具调用频繁失败的情况。核心方法论：validate-then-repair（先校验后修复），通过四项通用修复、Markdown 链接解包、关系不变量默认值三个层次，在不改动模型的前提下显著提升工具调用成功率。触发场景：实现 tool call 中间件、调试函数调用解析失败、设计 Schema 校验层、接入新模型时工具调用不稳定。
agent_created: true
---

# Tool Call Repair — 工具调用输入修复管线

## 概述

当 LLM 输出工具调用参数时，频繁出现四种可穷举的结构性错误。不是模型能力问题，是合约设计问题。此 skill 提供一套 **validate-then-repair** 管线，在 Zod/JSON Schema 校验失败时自动修复可恢复的输入噪声，并记录修复率遥测数据。

## 核心理念

> 严格的 Schema 是一种有代价的选择——它过滤了噪声，也过滤了任何没有背下这个特定 JSON 合约的模型产生的可恢复噪声。

**validate-then-repair** > preprocess-then-validate：让校验器先报错，Schema 本身就是"哪里会坏"的先验，修复预算只花在校验器实际不同意的精确路径上。

---

## 工作流决策树

```
LLM 输出 tool call 参数
        │
        ▼
  按原样解析 (parse as-is)
        │
   ┌────┴────┐
   ▼         ▼
 成功       失败
   │         │
   ▼         ▼
直接执行   遍历 Zod issue list
           │
           ├─ 形状问题 ──→ 四项修复（按顺序尝试）
           ├─ 链接泄漏 ──→ Markdown 链接解包
           └─ 关系问题 ──→ 扩展语义 + 默认值
                │
                ▼
           再次解析
           ┌───┴───┐
           ▼       ▼
         成功     失败
           │       │
           ▼       ▼
    记录 repaired  记录 invalid
    执行工具       返回模型可读的重试消息
```

---

## 1. 四项通用形状修复

这是覆盖 ~90% 开源模型工具调用失败的模式集合。四项修复共享一个结构：输入 JSON、Zod 报出的 issue 路径、尝试修复 → 返回修复后 JSON 或 null。

### 修复 1: 剥离 null 值

模型常对可选字段发送 `null` 而非省略。

```python
# 修复前: {"limit": null, "query": "hello"}
# 修复后: {"query": "hello"}
```

### 修复 2: 解析字符串化的 JSON 数组

模型把数组序列化为 JSON 字符串。

```python
# 修复前: {"filePath": "[\"a\",\"b\"]"}
# 修复后: {"filePath": ["a", "b"]}
```

### 修复 3: 解包多余的外层对象包装

单参数被包在 `{}` 里。

```python
# 修复前: {"args": {"query": "hello"}}，但 schema 期望 args 是 string
# 修复后: {"args": "hello"}
```

### 修复 4: 裸值包装为单元素数组

```python
# 修复前: {"paths": "foo"}
# 修复后: {"paths": ["foo"]}
```

### ⚠️ 执行顺序（关键）

修复 2 必须在修复 4 之前运行。否则：

```
输入: {"paths": "[\"a\",\"b\"]"}
先执行修复4 → {"paths": ["[\"a\",\"b\"]"]}  ← 错误！
先执行修复2 → {"paths": ["a", "b"]}          ← 正确
```

### 使用方式

调用 `scripts/repair.py`：

```bash
python scripts/repair.py \
  --input '{"filePath":"[\"a\",\"b\"]"}' \
  --schema-path schema.json \
  --tool-name writeFile
```

输出 JSON：
```json
{
  "repaired": true,
  "output": {"filePath": ["a", "b"]},
  "repairs_applied": ["json_array_parse"],
  "telemetry": "tool_input_repaired:writeFile"
}
```

---

## 2. Markdown 链接泄漏修复

### 问题

训练于对话输出的模型，在工具调用中泄漏了自动链接行为：

```
filePath: "/Users/x/proj/[notes.md](http://notes.md)"
```

工具试图创建字面名为 `[notes.md](http://notes.md)` 的文件。

### 修复

两条正则，仅在**链接文本等于无协议前缀的 URL** 时解包。合法 Markdown（如 `[click](https://x.com)`）不受影响。

```python
import re

def unwrap_autolink(value: str) -> str:
    """只在退化情况下解包 Markdown 自动链接。"""
    match = re.match(r'^\[(.+?)\]\((\1)\)$', value)
    if match:
        unwrapped = match.group(1)
        # 确保解包后是合法路径（非完整 URL）
        if not re.match(r'^https?://', unwrapped):
            return unwrapped
    return value
```

### Schema 层面的预防

使用语义化类型别名替代裸 `z.string()`：

```typescript
// 不要用
const filePath = z.string()

// 用这个——给模型更强的上下文信号
const filePath = pathString()  // 语义暗示：这是给 fopen 的，不是进聊天气泡的
```

---

## 3. 关系不变量处理

### 问题

形状层面各自合法的字段，组合起来违反了关系不变量。例如 `read_file` 要求 `offset` 和 `limit` 必须同时出现。

模型发 `{ absolutePath, limit: 30 }` → Zod 报错。

### 解法：扩展语义 + 透明默认值

在函数内部教它理解模型的意图，而非拒绝：

```python
def read_file(absolutePath: str, offset: int | None = None, limit: int | None = None):
    # 修复关系不变量
    if limit is not None and offset is None:
        offset = 0
        repaired = True
    elif offset is not None and limit is None:
        limit = 2000  # 匹配常见 read tool 的默认值
        repaired = True
    
    result = _do_read(absolutePath, offset, limit)
    
    if repaired:
        # 透明化决策——不用 Error: 前缀，终端不标红
        result["_note"] = (
            f"Note: {'offset' if offset == 0 else 'limit'} was not provided; "
            f"defaulted to {offset if offset == 0 else limit}. "
            "To adjust, retry with both offset and limit."
        )
    
    return result
```

### 原则

- **能修就修** → 形状问题
- **修不了就扩展语义** → 关系不变量
- **无论哪种都把选择透明化** → 结果中告知模型

---

## 4. 遥测集成

修复管线天然产出按 `(model, tool)` 维度的修复率数据。在工具执行层记录：

```python
# 成功修复
metrics.increment(f"tool_input_repaired:{tool_name}", tags={"model": model_id})

# 修复失败
metrics.increment(f"tool_input_invalid:{tool_name}", tags={"model": model_id})
```

这些数据可以：
- 在用户察觉之前发现某个模型在特定合约上退化
- 指导 Schema 设计优化
- 帮助决策是否需要针对特定模型增加更多修复规则

---

## 修复优先级总结

| 优先级 | 修复类型 | 适用条件 | 策略 |
|--------|---------|---------|------|
| P0 | 四项形状修复 | Zod 报出 type/key/container 错误 | 按固定顺序尝试 |
| P1 | Markdown 链接解包 | 路径字段匹配 `[text](text)` 模式 | 正则解包 |
| P2 | 关系不变量默认值 | 字段各自合法但组合违反约束 | 扩展语义 + 透明标注 |

---

---

## 5. 集成方式（推特作者的实际架构）

修复层是工具执行器内部的**薄中间件**，不是独立预处理步骤。核心代码只有 `safeParseWithRepair` 一个函数，嵌在 `execute()` 方法里。

### TypeScript 实现（推荐）

直接使用 `scripts/repair.ts` 中的 `ToolExecutor` 类：

```typescript
import { ToolExecutor, pathString } from "./repair";
import { z } from "zod";

const executor = new ToolExecutor({ debug: true });

// 注册工具——Schema + 关系不变量默认值
executor.register({
  name: "writeFile",
  schema: z.object({
    filePath: pathString(),     // 语义类型，防 autolink 泄漏
    content: z.string(),
  }),
  handler: async (input) => {
    // 实际写文件逻辑
    return { ok: true };
  },
});

executor.register({
  name: "readFile",
  schema: z.object({
    absolutePath: pathString(),
    offset: z.number().optional(),
    limit: z.number().optional(),
  }),
  relationalDefaults: {
    offset: 0,     // model 忘了 offset → 自动补
    limit: 2000,   // model 忘了 limit → 自动补
  },
  handler: async (input) => {
    return { content: "...", _note: "..." };
  },
});

// 调用——修复管线在 execute() 内部自动运行
const result = await executor.execute("readFile", {
  absolutePath: "/x/file.txt",
  limit: 30,  // model 漏了 offset，executor 自动补 offset:0
});
```

### 集成要点

| 关注点 | 做法 |
|--------|------|
| 集成位置 | `execute()` 方法内，`safeParse` 失败之后 |
| 快速通道 | 合法输入直接执行，修复预算为零 |
| 修复层 | `applyRepairs()` 递归遍历 + 按顺序尝试四项修复 |
| 关系不变量 | `relationalDefaults` 配置，在 schema 校验通过后补字段 |
| 遥测 | `metrics.increment()` 按 tool name 计数 |
| 错误返回 | 不用 `Error:` 前缀，终端不标红；附加 `_note` 告知模型 |

### 与直接使用 `safeParseWithRepair` 的区别

如果不想用 `ToolExecutor` 类，也可以直接调用核心函数：

```typescript
import { safeParseWithRepair, extractHints } from "./repair";

const schema = z.object({ filePath: pathString(), content: z.string() });
const result = safeParseWithRepair(rawArgs, {
  toolName: "writeFile",
  schema,
  hints: extractHints(schema),
  metrics: myMetrics,
});

if (result.error) {
  return { error: result.error };  // model-readable retry message
}
// result.data is the validated & repaired input
```

---

## 参考资源

- `scripts/repair.ts` — TypeScript 实现（推荐），含 `ToolExecutor` 类 + `safeParseWithRepair` + `pathString()` 语义类型
- `scripts/repair.py` — Python CLI 实现，适合脚本/管道场景
- `references/failure_catalog.md` — 各模型的典型失败案例及对应修复

## 已集成项目

- **CodeBuddy/WorkBuddy** — 通过 `PreToolUse` hook 注入修复管线，所有工具调用自动经过修复层
  - Hook 脚本：`~/.workbuddy/hooks/tool-call-repair-hook.py`
  - 配置：`~/.workbuddy/settings.json`（`hooks.PreToolUse`，matcher: `*`）
  - 修复范围：strip_nulls / json_parse / unwrap_object / autolink（不含 wrap_array，hook 无 Schema 信息）
