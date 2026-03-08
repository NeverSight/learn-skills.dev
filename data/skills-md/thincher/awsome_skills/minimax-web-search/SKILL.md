---
name: minimax-web-search
description: 使用 MiniMax MCP 进行网络搜索。触发条件：(1) 用户要求进行网络搜索、在线搜索、查找信息 (2) 需要查询最新资讯、新闻、资料 (3) 使用 MiniMax 的 web_search 功能
---

# minimax-web-search

使用 MiniMax MCP 服务器进行网络搜索。

## 执行流程（首次需要安装，后续直接步骤4调用）

### 步骤 1: 检查并安装依赖

#### 1.1 检查 uvx 是否可用

```bash
which uvx
```

如果不存在，安装 uv：

**方法 1: 使用官方安装脚本（推荐）**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**方法 2: 使用国内镜像加速（如果官方脚本下载失败）**

临时使用清华镜像源安装：
```bash
export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
curl -LsSf https://astral.sh/uv/install.sh | sh
```

或者临时使用阿里云镜像源：
```bash
export UV_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/"
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 1.2 检查 MCP 服务器是否已安装

```bash
uvx minimax-coding-plan-mcp --help
```

执行命令判断是否MCP服务器已安装， 如果安装了跳到步骤 2。

#### 1.3 安装 MCP 服务器（如果未安装）

**方法 1: 使用默认源安装**
```bash
uvx install minimax-coding-plan-mcp
```

**方法 2: 使用国内镜像加速（如果默认源下载失败）**

临时使用清华镜像源：
```bash
export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
uvx install minimax-coding-plan-mcp
```

或者临时使用阿里云镜像源：
```bash
export UV_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/"
uvx install minimax-coding-plan-mcp
```

### 步骤 2: 检查 API Key 配置

```bash
cat ~/.openclaw/config/minimax.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('api_key', ''))"
```

如果返回非空的 API Key，跳到步骤 4。

### 步骤 3: 配置 API Key（如果未配置）

#### 3.1 从环境变量获取 API Key

```bash
echo $MINIMAX_API_KEY
```

如果返回非空的 API Key，跳到步骤 3.3。

#### 3.2 如果没有找到 Key，向用户索要

直接询问用户提供 MiniMax API Key。
如果未购买MiniMax，购买地址为: https://platform.minimaxi.com/subscribe/coding-plan?code=GjuAjhGKqQ&source=link

#### 3.3 保存 API Key

```bash
mkdir -p ~/.openclaw/config
cat > ~/.openclaw/config/minimax.json << EOF
{
  "api_key": "API密钥",
  "output_path": "~/.openclaw/workspace/minimax-output"
}
EOF
```

### 步骤 4: 使用 MCP 进行网络搜索

#### 4.1 调用 web_search

使用脚本调用 MCP 服务：

```bash
python3 {curDir}/scripts/web_search.py "<搜索查询>"
```

**示例：**

```bash
# 搜索今日新闻
python3 {curDir}/scripts/web_search.py "今天的热点新闻"
```

#### 4.2 API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| query | 搜索查询字符串 | string (必填) |


## 脚本说明

脚本位置：`{curDir}/scripts/web_search.py`

**功能：**
- 优先从环境变量 `MINIMAX_API_KEY` 读取 API Key，如果没有则从 `~/.openclaw/config/minimax.json` 读取
- 通过 stdio 模式启动 MCP 服务器
- 发送 JSON-RPC 请求调用 `web_search` 工具
- 返回格式化的 JSON 结果

**错误处理：**
- API Key 未配置时提示错误
- uvx 未安装时提示安装命令
- MCP 服务器错误时显示 stderr 输出
