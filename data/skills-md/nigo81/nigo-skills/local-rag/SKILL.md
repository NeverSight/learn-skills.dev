---
name: local-rag
description: 本地向量知识库，支持按项目管理文档（docx/doc/pdf/md），语义检索。默认用硅基流动免费 API，零模型安装即可使用。支持多项目隔离、中文制度文档专用切片、Embedding+Rerank 两阶段检索。触发词：知识库、向量检索、RAG、制度检索、文档入库、语义搜索、local rag、搜制度、查条款、文档检索、从文档中搜、语义匹配。即使用户只是说"帮我从这些文件里找到关于XX的规定"或"对比两份制度的差异"，也应使用本 skill。
slug: nigo-local-rag
displayName: 本地向量知识库
version: 1.0.0
summary: 本地向量知识库，支持按项目管理文档（docx/doc/pdf/md），语义检索，默认用硅基流动免费 API，支持中文制度文档专用切片和 Embedding+Rerank 两阶段检索。
license: MIT
---

# 本地 RAG 知识库

轻量级本地向量知识库，支持按项目管理文档，语义检索制度条款。

> **作者**: nigo（公众号「逆行的狗」）
> 面向财务/审计从业者的 AI 效率工具，有任何问题可关注公众号反馈。

## 技术栈

- 切片：Chonkie RecursiveChunker + OverlapRefinery（15% overlap）
- 向量库：ChromaDB（persistent，多项目隔离）
- 默认 Embedding：硅基流动 BAAI/bge-m3（免费，1024维，8192 tokens）
- 默认 Reranker：硅基流动 BAAI/bge-reranker-v2-m3（免费）
- 文档解析：textutil（macOS .doc）+ python-docx（.docx）+ PyMuPDF（.pdf）+ MinerU（扫描件）
- 可选本地模式：Ollama embedding + Ollama reranker（完全离线）

## 使用方式

### CLI（推荐）

`bin/local-rag` 是独立的 CLI 入口脚本，自动定位 skill 目录，可在任意位置运行。

```bash
# 设置快捷方式（一次性，加到 PATH）
export PATH="$HOME/.claude/skills/local-rag/bin:$PATH"
# 或创建别名：alias local-rag="$HOME/.claude/skills/local-rag/bin/local-rag"

# 首次配置（交互式向导）
local-rag setup

# 项目管理
local-rag create my-project
local-rag delete my-project
local-rag list

# 入库
local-rag ingest my-project /path/to/docs
local-rag ingest my-project /path/to/file.docx --label "财务制度"

# 检索
local-rag search my-project "消防安全管理"
local-rag search my-project "消防安全管理" --rerank --top-k 20

# 工具
local-rag chunk-test /path/to/file.doc
local-rag info
```

也可以直接用完整路径：`~/.claude/skills/local-rag/bin/local-rag`

### Python API

```python
import sys, os
# 添加 skill 目录（根据实际安装位置调整）
sys.path.insert(0, os.path.expanduser("~/.claude/skills/local-rag"))
from src.pipeline import Pipeline

pipeline = Pipeline()

# 项目管理
pipeline.create_project("my-project")
pipeline.list_projects()
pipeline.delete_project("my-project")

# 入库（文件或文件夹）
result = pipeline.ingest("my-project", "/path/to/docs")

# 检索
results = pipeline.search("my-project", "消防安全管理", top_k=15)

# 检索 + Rerank
results = pipeline.search_with_rerank("my-project", "消防安全管理", final_k=10)

# 测试切片
result = pipeline.chunk_test("/path/to/file.doc")
```

### MCP Server

```bash
pip install fastmcp
python3 ~/.claude/skills/local-rag/mcp_server.py
```

6 个 tool：`create_project` / `delete_project` / `list_projects` / `ingest` / `search` / `rerank_search`

## Embedding Provider

| Provider | 适用场景 | 需要什么 |
|----------|---------|---------|
| **siliconflow**（默认） | 大多数场景，免费额度无限量 | API Key |
| **ollama** | 离线/内网环境 | Ollama + 模型（~2.5GB） |
| **openai** | 已有 OpenAI 账号 | API Key |

> ⚠️ **API Key 安全**: 不要把 API Key 直接写在 config.yaml 里！请设置环境变量 `SILICONFLOW_API_KEY`，config.yaml 中用 `${SILICONFLOW_API_KEY}` 引用。

环境变量 `SILICONFLOW_API_KEY` 设置硅基流动 Key 即可使用默认配置。如果没有 Key，请先到 [硅基流动](https://cloud.siliconflow.cn) 免费注册并创建 API Key。

### API Key 查找顺序

当用户没有设置 API Key 时，按以下顺序查找，**不要 grep 搜索**：

1. 环境变量 `SILICONFLOW_API_KEY`（`echo $SILICONFLOW_API_KEY` / Windows: `echo %SILICONFLOW_API_KEY%`）
2. 配置文件（按平台自动定位）：
   - macOS: `~/Library/Application Support/local-rag/config.yaml`
   - Windows: `%LOCALAPPDATA%\local-rag\config.yaml`
   - Linux: `~/.local/share/local-rag/config.yaml`
3. 如果都没有 → **直接引导用户设置**，不要到处搜索：
   ```
   请先设置硅基流动 API Key（免费，注册地址：https://cloud.siliconflow.cn）：
   
   macOS/Linux:
   echo 'export SILICONFLOW_API_KEY="sk-xxx"' >> ~/.zshrc && source ~/.zshrc
   
   Windows (PowerShell):
   [Environment]::SetEnvironmentVariable("SILICONFLOW_API_KEY", "sk-xxx", "User")
   
   或运行：local-rag setup
   ```

## 项目管理

- 每个项目 = 一个 ChromaDB collection
- 项目名只能用英文、数字、点、横线（ChromaDB 限制）
- 不同项目的文档完全隔离
- 删除项目会删除所有文档和向量

## 切片策略

### 中文制度文档（默认）
Chonkie RecursiveChunker 三级递归：
1. Level 1: 按"第X章"分章节
2. Level 2: 按双换行分大段落
3. Level 3: 按单换行分条款/段落
4. 目标 ~800 字符/chunk，最小 50 字符，15% overlap

### 通用 Markdown（可选）
- 按标题层级（#、##、###）分割
- config.yaml 中设 `chunking.strategy: generic`

## 配置

配置文件路径（跨平台自动选择）：
- macOS: `~/Library/Application Support/local-rag/config.yaml`
- Windows: `%LOCALAPPDATA%\local-rag\config.yaml`
- Linux: `~/.local/share/local-rag/config.yaml`

环境变量优先：`SILICONFLOW_API_KEY` / `OPENAI_API_KEY` / `RAG_DATA_DIR` / `RAG_EMBEDDING_MODEL`

## 数据存储

默认路径（跨平台自动选择）：
- macOS: `~/Library/Application Support/local-rag/`
- Windows: `%LOCALAPPDATA%\local-rag\`
- Linux: `~/.local/share/local-rag/`

可通过环境变量 `RAG_DATA_DIR` 或 config.yaml 的 `storage.data_dir` 修改。

## 前置条件

### 默认模式（零模型安装）
- Python 3.10+
- pip install -r requirements.txt
- 硅基流动 API Key（注册：https://cloud.siliconflow.cn）

### 本地模式（可选）
- Ollama 运行中，已拉取 `qwen3-embedding:4b`
- 无需额外 Python 包

### 高级离线（极少数需求）
- pip install torch transformers
- bge-reranker-v2-m3 cross-encoder（~2.3GB）

## Key Rules

- **首次使用必须先运行 `local-rag setup`** 或手动设置 `SILICONFLOW_API_KEY` 环境变量
- **执行任何 CLI 命令前，先用 `local-rag info` 检查配置是否就绪**
- **API Key 只能由用户提供，禁止 grep/搜索文件系统找 key**。如果 `local-rag info` 报错"API Key 未设置"，直接引导用户（见上方"API Key 查找顺序"），不要到处 grep
- **不要在没有 API key 的情况下继续执行** ingest/search 等命令，必定失败
- **首次使用还需安装依赖**：`pip install -r ~/.claude/skills/local-rag/requirements.txt`，如果命令报 ImportError，引导用户安装
- v3 默认用硅基流动 API，不需要 GPU 或 Ollama
- 推荐用 search_with_rerank（top-20 检索 + rerank top-10），给 LLM 足够候选
- LLM 必须阅读候选 chunk 的**完整内容**，不能只看前几行
- 由 LLM 从候选文本中做深度语义匹配，精确定位条款
- LLM 判断的关键：不是选"文字最相似的"，而是选"管理同一件事的"
- 向量检索无法判断"无对标"，需要 LLM 二次判断
- .doc 文件优先用 macOS textutil 转换，非 macOS 用 python-docx 回退
- 扫描版 PDF（每页文字 < 50 字符）自动调 MinerU 处理
- 环境变量 `RAG_EMBEDDING_MODEL` 可切换模型

## 踩坑记录

1. ChromaDB 1.3.5 `list_collections()` 返回 Collection 对象，需要 `.name`
2. Chonkie RecursiveLevel 不能同时设 delimiters 和 whitespace
3. Ollama reranker（chat API）输出乱码，v3 改用 embedding-based cosine similarity
4. Embedding 余弦相似度做 rerank 效果有限，但比没有好；cross-encoder 更精准
5. Ollama `/api/embed` 返回 `{"embeddings": [[...]]}` 不是 `{"embedding": [...]}`
6. 硅基流动 reranker 是 Cohere 风格 API，不是 OpenAI 格式
