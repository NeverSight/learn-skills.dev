---
name: vikunja
description: Vikunja 任务管理工具，支持查看项目和任务，并将每周已完成的任务同步到 Joplin weekly 笔记。
---

# Vikunja Skill

从自托管 Vikunja 实例读取任务，同步到 Joplin。

## 前置依赖

- **joplin skill** 必须已安装（`https://github.com/zrong/skills`）
- Vikunja 实例需要可访问
- 在 `agent_config.toml` 中配置 `[vikunja]` section

## 环境配置

在 `agent_config.toml` 中添加：

```toml
[vikunja]
base_url = "https://nas.zengrong.net:8456/api/v1"
api_key = ""
api_key_env = "VIKUNJA_API_KEY"
```

`api_key` 保存 Vikunja 创建的 API token。直接值非空时优先使用，否则读取
`api_key_env` 指定的环境变量。旧配置 `api_token` / `api_token_env` 应改名为
`api_key` / `api_key_env`；请求使用 `Authorization: Bearer <API key>`。

配置查找顺序为：当前工作目录、skill 目录、当前 Git 项目根目录、
`~/.agents/agent_config.toml`。密钥为空时，联网操作在请求前停止。
可将 [agent_config.example.toml](agent_config.example.toml) 的 section 合并到现有配置。
Joplin 同步通过 joplin skill 读取 `[joplin]` 的 `api_key` / `api_key_env`。

## 命令指南

建议使用 `uv run --project vikunja/scripts vikunja/scripts/vikunja_tool.py --non-interactive <command>` 执行。

### 1. 项目

- **列出项目**: `list-projects`

### 2. 任务

- **列出任务**: `list-tasks [--project ID] [--done] [--week YYYY-Www] [--limit N]`
  - 使用 `--week` 时，任务归属周按有效日期判断：若任务设置了 `end_date`，优先使用 `end_date`；否则使用 `done_at`

### 3. 同步

- **同步到 Joplin**: `sync-weekly [--note "2026-03-14weeks"] [--week "2026-W14"]`
  - 无参数：同步当前周
  - `--note`：从笔记标题解析目标周
  - `--week`：直接指定 ISO 周
  - 写入 daily 小节时按任务有效日期分组：优先 `end_date`，未设置时使用 `done_at`

## 测试流程

1. `uv run --project vikunja/scripts vikunja/scripts/vikunja_tool.py list-projects`
2. `uv run --project vikunja/scripts vikunja/scripts/vikunja_tool.py list-tasks --done --limit 5`
3. `uv run --project vikunja/scripts vikunja/scripts/vikunja_tool.py sync-weekly`
