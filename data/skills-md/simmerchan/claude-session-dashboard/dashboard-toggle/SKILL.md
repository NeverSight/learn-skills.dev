---
name: dashboard-toggle
description: 管理 Claude Session Dashboard 服务的启停。当用户请求打开/关闭/启动/停止/切换 Claude 会话面板、Session Dashboard 或 claude-session-dashboard 时触发此技能。如果服务未安装，会自动执行安装和构建操作。
---

# Claude Session Dashboard 服务管理

此技能用于管理 Claude Session Dashboard 服务的启停状态。

## 工作流程

1. 检查服务是否已安装
2. 如果服务正在运行，则停止服务
3. 如果服务未运行，则启动服务（如需要会先安装）
4. 向用户报告服务状态

## 使用脚本

执行 `scripts/manage_service.sh` 来管理服务：

```bash
# 切换服务状态（默认）
bash scripts/manage_service.sh toggle

# 启动服务
bash scripts/manage_service.sh start

# 停止服务
bash scripts/manage_service.sh stop

# 查看状态
bash scripts/manage_service.sh status

# 安装/重新安装
bash scripts/manage_service.sh install
```

## 项目路径

- 项目目录: `~/Documents/pythonprojects/claude_session_dashboard`
- PID 文件: `~/.claude-dashboard.pid`
- CLI 路径: `~/Documents/pythonprojects/claude_session_dashboard/packages/cli/dist/index.js`
- 访问地址: http://localhost:3000

## 用户请求示例

触发此技能的典型请求：
- "打开会话面板"
- "关闭 dashboard"
- "启动 claude-session-dashboard"
- "切换服务状态"
