---
name: mcp-deploy
description: MCP 服务器自动部署工具。当用户说"部署 MCP"、"安装 MCP"、"配置 MCP"时使用。支持智谱 MCP、Minimax MCP、Gitea MCP 等平台的自动配置。
---

# MCP Deploy

自动部署和配置各种 MCP 服务器。

## 支持的 MCP 平台

| 平台 | 类型 | 需要的配置 |
|------|------|------------|
| 智谱 (zhipu) | HTTP | API Key |
| 智谱搜索 (web-search-prime) | HTTP | API Key |
| 智谱网页读取 (web-reader) | HTTP | API Key |
| 智谱 GitHub (zread) | HTTP | API Key |
| Minimax | STDIO | API Key |
| Gitea | STDIO | API URL + Token + 二进制 |
| 其他 MCP | STDIO/HTTP | 根据具体情况 |

## 工作流程

1. **确认 MCP 平台**：询问用户要部署哪个平台的 MCP
2. **收集配置信息**：根据平台询问必要的配置（如 API Key、URL 等）
3. **执行配置**：使用 mcporter 命令添加 MCP 服务器
4. **验证部署**：测试 MCP 服务器是否正常工作
5. **报告结果**：展示部署结果和可用工具

## 常用配置参考

### 智谱 MCP (HTTP)

```bash
# 视觉理解
mcporter config add zhipu --url "https://open.bigmodel.cn/api/mcp/vision/mcp" --header "Authorization=Bearer YOUR_API_KEY"

# 联网搜索
mcporter config add web-search-prime --url "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp" --header "Authorization=Bearer YOUR_API_KEY"

# 网页读取
mcporter config add web-reader --url "https://open.bigmodel.cn/api/mcp/web_reader/mcp" --header "Authorization=Bearer YOUR_API_KEY"

# GitHub 仓库
mcporter config add zread --url "https://open.bigmodel.cn/api/mcp/zread/mcp" --header "Authorization=Bearer YOUR_API_KEY"
```

### Minimax MCP (STDIO)

```bash
# 需要先安装 uvx
which uvx || curl -LsSf https://astral.sh/uv/install.sh | sh

mcporter config add minimax --command "uvx" --args "minimax-coding-plan-mcp" --env "MINIMAX_API_KEY=YOUR_KEY,MINIMAX_API_HOST=https://api.minimaxi.com"
```

### Gitea MCP (STDIO)

#### 第一步：下载 Gitea MCP 二进制

访问 https://gitea.com/gitea/gitea-mcp/releases 下载对应平台的二进制文件。

根据 CPU 架构选择：

- **Apple Silicon (M1/M2/M3/M4)**: 选择 `darwin-arm64`
- **Intel Mac**: 选择 `darwin-amd64`
- **Linux x86_64**: 选择 `linux-amd64`
- **Linux ARM64**: 选择 `linux-arm64`

#### 第二步：安装二进制

```bash
# 下载后复制到系统路径
cp gitea-mcp /usr/local/bin/

# 赋予执行权限
chmod +x /usr/local/bin/gitea-mcp
```

#### 第三步：配置 MCP

```bash
# 创建配置文件目录
mkdir -p ~/.config/mcp-deploy

# 创建 .env 文件（根据你的 Gitea 实例配置）
cat > ~/.config/mcp-deploy/gitea.env << 'EOF'
GITEA_TOKEN=your_token_here
GITEA_API_URL=http://your-gitea-instance:3000/api/v1
EOF

# 使用 mcporter 添加（根据你的 Agent 调整路径）
mcporter config add gitea --command "gitea-mcp" --env "GITEA_TOKEN=your_token,GITEA_API_URL=http://your-gitea-instance:3000/api/v1"
```

**注意**：更多配置选项请参阅 https://gitea.com/gitea/gitea-mcp

## 配置文件位置

- MCP 配置：`~/.config/mcporter.json` 或项目级 `config/mcporter.json`
- Gitea Token：可在 .env 文件中配置

## 注意事项

- 如果用户没有提供必要的配置信息，先询问
- 部署前检查目标 MCP 是否需要特殊的依赖（如 uvx、gitea-mcp 二进制）
- 某些 MCP 需要内网访问（如自建 Gitea），确认网络可达
- 部署后务必验证 MCP 是否正常工作
- 如果 MCP 离线，尝试诊断问题（网络、内网、依赖等）
- Gitea MCP 建议使用二进制方式安装，避免 npm 包的兼容性问题
