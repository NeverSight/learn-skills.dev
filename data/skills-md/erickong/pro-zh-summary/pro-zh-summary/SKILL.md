---
name: pro-zh-summary
description: 专业级中文长文本摘要工具。当用户要求“总结”、“摘要”、“提炼要点”、“缩写”或处理超长中文文本时，必须调用此工具进行自动分段与压缩。
version: 1.1.0
author: heack
metadata:
  openclaw:
    entry_point: "python main.py"
    requires:
      python: ">=3.8"
      packages: ["transformers", "torch", "sentencepiece"]
    emoji: "🔮"
---

# 专业中文摘要 (Pro Zh-Summary)

这是一个基于 MT5 架构深度优化的中文摘要技能。它擅长将长篇大论、新闻稿、会议记录转化为精炼的中文摘要。

## 如何使用
- "帮我总结一下这段话：[内容]"
- "摘要这篇文章，每段摘要约100字：[内容]"

## 配置说明
- `MAX_LENGTH`: 单段摘要的最大长度（默认 150）
- `CHUNK_SIZE`: 文本切割大小（默认 300）