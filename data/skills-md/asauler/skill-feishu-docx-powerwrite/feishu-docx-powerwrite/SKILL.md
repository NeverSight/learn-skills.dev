---
name: feishu-docx-powerwrite
description: High-quality Feishu/Lark Docx writing via OpenClaw. Covers tool selection, chunked writing, native tables, $ symbol escaping, and all known pitfalls. Trigger on Feishu doc/docx links, "write to Feishu doc", "generate a Feishu doc", "append/replace docx", or when users want consistently good doc formatting.
tags: [feishu, document, writing, formatting]
---

# Feishu Docx PowerWrite

Reliably write great-looking Feishu Docx using OpenClaw's tools.

## Tool Selection

| Tool | Use When | Notes |
|------|----------|-------|
| `feishu_doc(action="create")` | 新建文档 | 返回 doc_token |
| `feishu_doc(action="write")` | 写首段内容 | 覆盖整个文档 |
| `feishu_doc(action="append")` | 追加后续内容 | 每次 ≤1500 字 |
| `feishu_table.py` | 插入原生表格 | Markdown 表格不支持 |

⚠️ **不要用** `create_feishu_doc` 工具 — 有 JSON parse bug，会失败。

## 核心工作流

### 1. 创建 + 写入文档

```
feishu_doc(action="create", title="标题")
→ 拿到 doc_token
feishu_doc(action="append", doc_token=xxx, content="第一段...")
feishu_doc(action="append", doc_token=xxx, content="第二段...")
```

### 2. 分块写入规则

- 每次 append **≤1500 字**（超过会 400 错误）
- 长报告分 4-5 次 append
- 按章节自然分块，不要在段落中间断开

### 3. 表格写入

Markdown 表格通过 `feishu_doc append` 写入会**散落成碎片文本**（Table block type 被跳过）。

正确方式：用 `feishu_table.py` 脚本创建原生表格：

```bash
python3 workspace/tools/feishu_table.py
```

代码调用：
```python
from feishu_table import create_table
create_table(doc_token, [
    ["列1", "列2", "列3"],   # 表头
    ["数据1", "数据2", "数据3"],
], header_bold=True)
```

### 4. $ 符号处理

飞书把 `$...$` 当 LaTeX 公式渲染。写入包含美元符号的内容时：
- ❌ `$82.78` → 被解析为公式
- ✅ `82.78美元` 或 `USD 82.78`

## Markdown 格式最佳实践

### 渲染良好的格式
- `# ## ###` 标题层级
- `- ` 无序列表 + 2 空格缩进嵌套
- `1. 2. 3.` 有序列表
- ` ```code``` ` 代码块
- `**加粗**` `*斜体*`
- `---` 分割线
- 短段落（每段 3-5 行）

### 避免的格式
- Markdown 表格（`| col |`）→ 用原生表格
- 超长段落 → 拆短
- `$` 符号 → 用文字替代
- 深层嵌套列表（>3 层）→ 拍平

## 长文档写作模式

### Sub-agent 搜索 + 主 session 写作
- Sub-agent 负责搜索和数据收集
- 主 session 综合数据写报告
- 原因：sub-agent maxTokens 限制（16k）导致无法写长文，content 参数会被截断

### 如果必须用 sub-agent 写
- 任务描述中明确"分块写入，每块不超过 3000 字"
- 用 `exec heredoc` 分块写本地文件，再上传飞书

## Context 管理

长文档写作会导致 session context 膨胀：
- 大量文本操作用 sub-agent 隔离
- exec 命令输出用 `tail/head` 限制行数
- 写完长文档后提醒可能需要重启 gateway

## 权限设置

新建文档默认设为「互联网获得链接即可访问」：
```python
feishu_perm(action="add", token=doc_token, type="docx",
            member_type="openchat", member_id="oc_xxx", perm="view")
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| append 返回 400 | 单次内容过长 | 每次 ≤1500 字 |
| 表格变碎片文本 | Markdown 表格不支持 | 用 feishu_table.py |
| `$` 变公式 | LaTeX 解析 | 用"美元"或"USD" |
| create_feishu_doc 失败 | 工具有 bug | 用 feishu_doc create + append |
| sub-agent 写入空白 | maxTokens 截断 | 主 session 写或分块 |
| 上游 400 bad request | context 过大 | 重启 gateway |
