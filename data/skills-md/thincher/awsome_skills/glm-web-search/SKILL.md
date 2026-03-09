---
name: glm-web-search
description: 使用 GLM 联网搜索 MCP 进行网络搜索。触发条件：(1) 用户要求进行网络搜索、在线搜索、查找信息 (2) 需要查询最新资讯、新闻、资料 (3) 使用 GLM 的 web_search 功能
---

# glm-web-search

使用 GLM 联网搜索 MCP 服务器进行网络搜索。

## 执行流程（首次需要安装，后续直接步骤6调用）

### 步骤 1: 检查并安装依赖

#### 1.1 检查 mcporter 是否可用

```bash
npx -y mcporter --version
```

如果命令返回成功，说明 mcporter 可用，跳到步骤 2。

mcporter 可以直接通过 npx 使用，无需安装。

### 步骤 2: 检查 API Key 配置

```bash
cat ~/.openclaw/config/glm.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('api_key', ''))"
```

如果返回非空的 API Key，跳到步骤 4。

### 步骤 3: 配置 API Key（如果未配置）

#### 3.2 如果没有找到 Key，向用户索要

如果用户没有智谱 API Key，可以访问 https://www.bigmodel.cn/glm-coding?ic=OOKF4KGGTW 购买。

询问用户提供智谱 API Key。

#### 3.3 保存 API Key

```bash
mkdir -p ~/.openclaw/config
cat > ~/.openclaw/config/glm.json << EOF
{
  "api_key": "API密钥"
}
EOF
```

### 步骤 4: 添加 MCP 服务器

使用 mcporter 添加 GLM 联网搜索 MCP 服务器：

```bash
mcporter config add glm-search \
  --type sse \
  --url "https://open.bigmodel.cn/api/mcp/web_search_prime/sse?Authorization=your-key"
```

注意：将 `your-key` 替换为实际的智谱 API Key。

### 步骤 5: 测试连接

```bash
mcporter list
```

确认 `glm-search` 服务器已成功添加。

### 步骤 6: 使用 mcporter 调用 MCP 进行网络搜索

#### 6.1 使用 mcporter 调用 MCP 工具

使用 mcporter 调用 MCP 服务：

```bash
mcporter call glm-search.webSearchPrime search_query="<搜索查询>"
```

**示例：**

```bash
# 搜索今日新闻
mcporter call glm-search.webSearchPrime search_query="今天的热点新闻"

# 搜索技术信息
mcporter call glm-search.webSearchPrime search_query="Python 异步编程最佳实践"
```

#### 6.2 API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| search_query | 搜索查询字符串 | string (必填) |


## 支持的工具

**重要提示：如果出现问题以官方说明为准**
官方版说明 ： https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server

GLM 联网搜索 MCP 服务器提供以下工具：
- `webSearchPrime` - 搜索网络信息，返回结果包括网页标题、网页URL、网页摘要、网站名称、网站图标等

## MCP 配置

MCP 服务器名称：`glm-search`

MCP 服务器类型：HTTP

MCP 服务器 URL：`https://open.bigmodel.cn/api/mcp/web_search_prime/mcp`

认证方式：Bearer Token（Authorization header）
