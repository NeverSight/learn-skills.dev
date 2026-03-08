---
name: bilibili-toolkit
description: B 站综合工具箱。集成视频下载、文稿采集、向量知识库构建、语义检索问答及 UP 主人格画像分析等功能。
---

# B 站综合工具箱 (Bilibili Toolkit)

集成所有 B 站相关的自动化功能，支持视频处理、数据采集、知识库管理及深度分析。

## 主要功能与命令

### 1. 视频下载
下载指定 BVID 的视频并合并音视频。
```bash
uv run .claude/skills/bilibili-toolkit/scripts/bili_video.py <BVID_LIST>
```

### 2. 视频采集与导出
采集视频元数据、文稿并入库，或导出文稿。
- **采集 UP 主所有视频** (默认前 3 页，每页约 30 个): `uv run .claude/skills/bilibili-toolkit/scripts/bili_collect_and_export.py <UID> [页数]`
- **采集指定视频**: `uv run .claude/skills/bilibili-toolkit/scripts/bili_collect_and_export.py <BVID1> <BVID2> ...`
- **导出文稿**: `uv run .claude/skills/bilibili-toolkit/scripts/bili_collect_and_export.py export <QUERY>`

### 3. 知识库构建 (RAG)
将已采集的文稿转换为向量索引。
```bash
uv run .claude/skills/bilibili-toolkit/scripts/bili_kb_llama.py [--rebuild] [--stats]
```

### 4. 语义检索问答
基于知识库进行智能问答。
```bash
uv run .claude/skills/bilibili-toolkit/scripts/bili_search_llama.py "<QUERY>"
```

### 5. UP 主深度分析
基于已采集数据生成 UP 主人格画像和观点总结。
```bash
uv run .claude/skills/bilibili-toolkit/scripts/bili_up_summarizer.py "<UID>"
```

## 前置条件
- 配置好 `.env` 或 `secrets.json` 中的 API Keys (SiliconFlow, Zhipu, Bilibili Cookies)。
- 安装 FFmpeg（用于视频合并）。
- PostgreSQL (pgvector) 或 Neo4j 数据库运行中。
