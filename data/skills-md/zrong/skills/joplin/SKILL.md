---
name: joplin
description: 完整的 Joplin REST API 客户端，支持笔记(Notes)、笔记本(Folders)、标签(Tags)、资源/附件(Resources)的 CRUD 操作，以及搜索、修订版本和事件流。
---

# Joplin Skill (Complete API)

此 Skill 提供了对 Joplin REST API 的全面访问，允许 Agent 深度管理 Joplin 笔记库。

## 环境配置

在 `agent_config.toml` 中配置：

```toml
[joplin]
base_url = "http://localhost:41184"
api_key = ""
api_key_env = "JOPLIN_API_KEY"
```

`api_key` 是 Web Clipper 设置中的授权密钥。直接值非空时优先使用，否则读取
`api_key_env` 指定的环境变量；脚本不会自动加载 `.env`。旧配置 `token` / `token_env`
应改名为 `api_key` / `api_key_env`。请求仍按 Joplin 协议使用 `token` query 参数。

配置查找顺序为：当前工作目录、skill 目录、当前 Git 项目根目录、
`~/.agents/agent_config.toml`。密钥为空时，联网操作在请求前停止。
可将 [agent_config.example.toml](agent_config.example.toml) 的 section 合并到现有配置。

## 功能列表与命令指南

建议使用 `uv run --project joplin/scripts joplin/scripts/joplin_tool.py --non-interactive <command>` 执行。

### 1. 全局与系统
- **检查连接**: `ping`
- **获取事件流**: `events [--cursor <cursor>] [--limit <limit>]`
- **获取修订版本**: 
    - `revision list`
    - `revision get <id>`

### 2. 笔记 (Note)
- **列出笔记**: `note list [--limit 10] [--page 1] [--fields "id,title"] [--order-by "updated_time"] [--order-dir "DESC"]`
- **获取详情**: `note get <id>`
- **创建笔记**: `note create --title "标题" [--body "内容"] [--body-from <文件路径>] [--parent <folder_id>]`
  - `--body` 适用于短文本；长文本或含有多行内容的，推荐用 `--body-from <文件路径>` 从本地文件读取
- **更新笔记**: `note update <id> [--title "新标题"] [--body "新内容"] [--body-from <文件路径>] [--parent <new_folder_id>]`
- **删除笔记**: `note delete <id>`
- **查看笔记标签**: `note tags <id>`
- **查看笔记资源**: `note resources <id>`

### 3. 笔记本 (Folder)
- **列出笔记本**: `folder list [--fields "id,title,parent_id"]`
- **获取详情**: `folder get <id>`
- **创建笔记本**: `folder create "标题" [--parent <parent_id>]`
- **更新笔记本**: `folder update <id> "新标题"`
- **删除笔记本**: `folder delete <id>`

### 4. 标签 (Tag)
- **列出标签**: `tag list`
- **获取详情**: `tag get <id>`
- **创建标签**: `tag create "标题"`
- **更新标签**: `tag update <id> "新标题"`
- **删除标签**: `tag delete <id>`
- **给笔记打标签**: `tag add <tag_id> <note_id>`
- **移除笔记标签**: `tag remove <tag_id> <note_id>`

### 5. 资源/附件 (Resource)
- **列出资源**: `resource list [--limit 100]`
- **获取详情**: `resource get <id>`
- **上传附件**: `resource upload <file_path> [--title "标题"]`
- **下载附件**: `resource download <id> <dest_path>`
- **删除资源**: `resource delete <id>`

### 6. 搜索 (Search)
- **执行搜索**: `search --query "关键词" [--type note|folder|tag] [--limit 10] [--page 1]`

## 测试流程
执行以下命令进行完整验证：
1. `uv run --project joplin/scripts joplin/scripts/joplin_tool.py ping`
2. `uv run --project joplin/scripts joplin/scripts/joplin_tool.py folder list`
3. `uv run --project joplin/scripts joplin/scripts/joplin_tool.py note list --limit 1`

## 注意事项
- 必须确保 Joplin 桌面端的 **Web Clipper** 已启用。
- 附件上传和下载涉及本地文件路径，请确保路径正确且有读写权限。
