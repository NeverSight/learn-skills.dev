---
name: grok-twitter-search
description: 使用 xAI Grok 模型的 x_search 工具智能搜索 Twitter 内容。首创 Fast/Reasoning 双引擎动态路由，支持 SOCKS5 代理（WARP）精准流量分流。相比官方 X API 成本呈断崖式下降（实测约 $2.8/千次），语义理解更强、结果更智能。当用户需要搜索推特、监控舆情、分析热点话题、获取实时推文数据时使用此技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🐦",
        "homepage": "https://github.com/your-repo/grok-twitter-search",
        "requires": { "bins": ["uv", "curl"], "env": ["GROK_API_KEY"] },
        "primaryEnv": "GROK_API_KEY",
      },
  }
---

# Grok Twitter Search Skill

基于 xAI `grok-4-1-fast` 与 `grok-4-1-fast-reasoning` 双擎驱动的推特原生数据检索引擎。

## 核心优势

| 特性 | Grok x_search (本技能) | X 官方 API (Basic) |
|------|------------------------|-------------------|
| **计费方式** | **按 Token 计费 (实测约 $2.8/千次)** | $100 / 月固定月租 |
| **检索逻辑** | ✅ 智能自然语言语义提取，自带 LLM 降噪 | ❌ 仅支持严格的布尔逻辑匹配 |
| **模型支持** | ✅ 使用 `grok-4-1-fast-reasoning`（唯一支持 x_search 工具的模型） | ❌ 单一数据返回 |
| **中文支持** | ✅ 深度优化，理解上下文隐喻 | ⚠️ 效果一般 |

## 快速开始

### 方式 1: 交互式配置（推荐首次使用）

```bash
uv run {baseDir}/scripts/setup_interactive.py
```

这个向导会引导你完成：
- ✅ 检查系统依赖 (uv, curl)
- ✅ 检测 WARP 代理状态
- ✅ 配置 Grok API Key
- ✅ 选择代理模式
- ✅ 测试连接
- ✅ 自动保存配置到 openclaw.json

### 方式 2: 手动配置

如果你更喜欢手动配置，可以继续阅读下面的详细说明。

## 使用方法

建议使用 `uv` 运行以保证依赖隔离与环境纯净：

### 极速检索模式（默认，超低成本）
```bash
uv run {baseDir}/scripts/search_twitter.py --query "{搜索内容}" --max-results 10
```

### 深度舆情分析模式（调用 Reasoning 模型）
```bash
uv run {baseDir}/scripts/search_twitter.py --query "{搜索内容}" --max-results 10 --analyze
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--query` | string | 是 | - | 搜索查询（支持自然语言） |
| `--max-results` | int | 否 | 10 | 最大返回结果数 |
| `--analyze` | flag | 否 | False | 启用 Reasoning 推理模型进行深度舆情总结 |
| `--api-key` | string | 否 | 读环境变量 | 优先读取 `GROK_API_KEY` |
| `--proxy` | string | 否 | auto-detect | SOCKS5 代理地址（自动检测 WARP） |

## 代理配置（WARP 智能检测）

本技能支持三种代理配置方式，优先级从高到低：

### 1. 显式配置（最高优先级）
在 `~/.openclaw/openclaw.json` 中设置：
```json5
{
  skills: {
    entries: {
      "grok-twitter-search": {
        enabled: true,
        env: {
          SOCKS5_PROXY: "socks5://127.0.0.1:40000",
          GROK_API_KEY: "your_api_key_here"
        }
      }
    }
  }
}
```

### 2. 环境变量
```bash
export SOCKS5_PROXY="socks5://127.0.0.1:40000"
export GROK_API_KEY="your_api_key_here"
```

### 3. 自动检测（默认行为）
脚本会自动检测 WARP 代理：
- 检查 `warp-svc` 进程是否在运行
- 检查端口 40000 是否在监听
- 如果检测到 WARP，自动使用 `socks5://127.0.0.1:40000`
- 如果未检测到代理但直连可用，则直连访问

### 检查 WARP 状态
```bash
bash {baseDir}/scripts/check_warp.sh
```

## 输出格式 (纯净提取)

引擎剥离了冗余的 LLM 文本，直接返回原生 Tool Call 拦截数据：

```json
{
  "status": "success",
  "query": "elon musk",
  "tweets": [
    {
      "author": "@elonmusk",
      "content": "推文内容...",
      "timestamp": "2026-02-26T10:00:00Z",
      "likes": 1234,
      "retweets": 567,
      "url": "https://x.com/elonmusk/status/123..."
    }
  ],
  "model_used": "grok-4-1-fast-reasoning",
  "x_search_calls": 1,
  "usage": {
    "input_tokens": 1250,
    "output_tokens": 45,
    "total_tokens": 1295
  }
}
```

## 真实成本估算 (实测数据)

*基于实测数据：200 次调用耗费 $0.56，即约 $2.8/千次*

| 运行模式 | 引擎模型 | 预估单次消耗 | 千次调用成本 | 适用场景 |
|----------|----------|--------------|--------------|----------|
| **标准检索** | `grok-4-1-fast-reasoning` | ~5,000 Tokens | **~$2.8** | 日常搜索、舆情监控、推文分析 |

## 与 opentwitter 的分工

本技能与 `opentwitter` (6551 API) 都是推特搜索方案，但定位不同：

| 场景 | 推荐技能 | 原因 |
|------|---------|------|
| **自然语言搜索**<br>例："币圈大佬最近动态"、"马斯克对 crypto 的看法" | ✅ grok-twitter-search | Grok 理解语义，能处理模糊查询 |
| **精确用户搜索**<br>例："from:cz_binance"、"获取 @elonmusk 最近 20 条推文" | ✅ opentwitter | 结构化参数，结果稳定 |
| **舆情分析/观点总结**<br>例："分析 CZ 对马斯克收购推特的态度" | ✅ grok-twitter-search | LLM 自带分析能力 |
| **批量数据获取**<br>例：获取用户 follower 列表、删除的推文 | ✅ opentwitter | 专用 API，数据结构完整 |
| **话题/标签搜索**<br>例："#bitcoin 热门推文"、"含 hashtag 的推文" | ✅ opentwitter | 支持 hashtag 参数过滤 |
| **日期范围搜索**<br>例："2025 年 1 月以来的推文" | ✅ opentwitter | 支持 sinceDate/untilDate |

**经验法则：**
- 用户用**自然语言**提问 → grok-twitter-search
- 用户用**推特搜索语法**（from:, to:, #hashtag）→ opentwitter

---

## 故障排查

### 检查环境配置
```bash
bash {baseDir}/scripts/check_warp.sh
```

### 常见问题

**Q: 提示 "缺少 API Key"**
- 确保已设置 `GROK_API_KEY` 环境变量或在 `openclaw.json` 中配置

**Q: 连接超时或无法访问 api.x.ai**
- 检查 WARP 是否运行：`sudo systemctl status warp-svc`
- 手动测试代理：`curl --socks5 127.0.0.1:40000 https://api.x.ai/v1`
- 如在中国大陆，必须使用 WARP 或其他出海代理

**Q: 返回空结果**
- 检查查询词是否过于具体或敏感
- 尝试简化查询或使用英文关键词
- 如果查询包含推特语法（如 `from:username`），改用 opentwitter
