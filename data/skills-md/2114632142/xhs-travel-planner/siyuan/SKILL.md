---
name: siyuan
description: "思源笔记 (SiYuan Note) 联动。支持管理笔记本、文档、块，支持 SQL 查询内容。当需要从思源笔记中读取、写入或搜索内容时使用。"
---

# 思源笔记 (SiYuan Note) 联动

本 Skill 允许 Antigravity 与用户的思源笔记进行交互。

## 核心功能

- **笔记本管理**：列出 (`list_notebooks`)、创建、重命名笔记本。
- **文档管理**：创建 (`create_doc`)、移动、删除文档。
- **块操作**：在文档中插入 (`insert_block`)、更新、删除内容块。
- **搜索与查询**：执行 SQL 查询 (`sql_query`) 或全文搜索。
- **导出**：导出 Markdown 或资源文件。

## 使用须知

1. **思源笔记必须启动**：确保本地思源笔记软件正在运行。
2. **API 令牌**：需要 `SIYUAN_TOKEN`（在思源笔记 -> 设置 -> 关于中获取）。
3. **环境变量**：默认地址为 `127.0.0.1:6806`。

## 如何调用

Antigravity 可以通过运行内置的 `scripts/siyuan_executor.py` 来调用具体的功能。

### 示例用法

#### 列出所有笔记本
```bash
python .agent/skills/siyuan/scripts/siyuan_executor.py list_notebooks
```

#### 创建文档
```bash
python .agent/skills/siyuan/scripts/siyuan_executor.py create_doc --notebook "id" --path "/path" --markdown "# Content"
```

#### SQL 查询
```bash
python .agent/skills/siyuan/scripts/siyuan_executor.py sql_query "SELECT * FROM blocks LIMIT 5"
```
