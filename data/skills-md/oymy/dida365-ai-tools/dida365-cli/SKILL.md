---
name: dida365-cli
description: 使用 Node.js CLI 管理滴答清单（Dida365）的任务、项目、标签等，支持已完成任务按日期查询、全量同步、标签管理、批量操作等，适用于日常任务管理与自动化场景。
---

说明：以下调用方式均以 `dida365` 为 CLI 入口。

安装后直接使用：
```bash
# npx（推荐）
npx dida365 <command> [options]

# 或全局安装后
npm install -g dida365-ai-tools
dida365 <command> [options]
```

## 1. 认证

使用前必须先设置 Cookie 认证。

```bash
dida365 auth cookie <token>     # 设置 Cookie token 完成认证
dida365 auth status             # 检查当前认证状态
```

## 2. 项目管理

```bash
dida365 project list                    # 列出所有项目
dida365 project list --json             # JSON 格式输出
dida365 project show <projectId>        # 查看项目详情和任务列表
dida365 project show <projectId> --json
```

## 3. 任务管理

```bash
# 创建任务
dida365 task create <title> -p <projectId>
dida365 task create <title> -p <projectId> -c <content> --priority <0|1|3|5> -d <dueDate>

# 查看任务
dida365 task show <taskId>
dida365 task show <taskId> --json

# 更新任务
dida365 task update <taskId> -p <projectId> -t <newTitle>
dida365 task update <taskId> -p <projectId> -c <content> --priority <0|1|3|5> -d <dueDate>

# 完成任务
dida365 task complete <projectId> <taskId>

# 删除任务（危险操作，删除前需确认）
dida365 task delete <projectId> <taskId>
```

参数说明：
- `-p, --project <projectId>` — 项目 ID（必填）
- `-t, --title <title>` — 任务标题（update 时可选）
- `-c, --content <content>` — 任务内容
- `-d, --due <date>` — 截止日期（ISO 8601）
- `--priority <n>` — 优先级：0=无, 1=低, 3=中, 5=高
- `-j, --json` — JSON 格式输出

## 4. 已完成任务查询

```bash
dida365 completed today                              # 今天完成的
dida365 completed yesterday                          # 昨天完成的
dida365 completed week                               # 本周完成的
dida365 completed date <YYYY-MM-DD>                  # 指定日期
dida365 completed range <startDate> <endDate>        # 日期范围
dida365 completed today --timezone "Asia/Shanghai"   # 指定时区
dida365 completed today --json                       # JSON 输出
```

## 5. 全量同步与用户设置

```bash
dida365 sync all                # 一次拉取所有项目、任务、标签、文件夹
dida365 sync all --json
dida365 sync settings           # 查看用户设置（时区、日期格式等）
dida365 sync settings --json
dida365 sync timezone           # 快速获取用户时区
```

`sync all` 返回的数据结构：
- `projects` — 项目列表
- `tasks` — 所有未完成任务
- `tags` — 标签列表
- `projectGroups` — 项目文件夹
- `inboxId` — 收件箱项目 ID

## 6. 标签管理

```bash
dida365 tag list                            # 列出所有标签
dida365 tag list --json
dida365 tag create <name>                   # 创建标签
dida365 tag create <name> --color "#ff0000" --parent <parentTag>
dida365 tag rename <oldName> <newName>      # 重命名
dida365 tag color <name> <color>            # 修改颜色
dida365 tag nest <name> <parentTag>         # 设置父标签（层级关系）
dida365 tag merge <fromTag> <toTag>         # 合并标签（fromTag 任务归入 toTag）
dida365 tag delete <name1> [name2...]       # 删除（支持多个）
```

## 7. 批量操作

### 任务批量操作

```bash
# 移动任务到其他项目
dida365 batch move-task <taskId> <fromProjectId> <toProjectId>

# 设置子任务关系
dida365 batch set-subtask <taskId> <parentId> <projectId>

# 批量删除任务（格式：taskId:projectId）
dida365 batch delete-tasks <taskId1:projectId1> [taskId2:projectId2 ...]
```

### 项目批量操作

```bash
dida365 batch create-project <name>                 # 创建项目
dida365 batch create-project <name> --color "#ff0000" --group <groupId> --view kanban
dida365 batch delete-projects <projectId1> [projectId2 ...]  # 危险，需确认
```

### 项目文件夹操作

```bash
dida365 batch create-folder <name>                  # 创建文件夹
dida365 batch delete-folders <groupId1> [groupId2 ...]
```

## Dida365 概念模型

- **Project**：项目，任务的容器。
  - 常用字段：`id`, `name`, `color`, `viewMode`(list/kanban/timeline), `kind`(TASK/NOTE), `groupId`, `closed`, `permission`, `sortOrder`
- **Task**：任务，隶属于某个 Project。
  - 常用字段：`id`, `projectId`, `title`, `content`, `desc`, `tags`, `priority`(0/1/3/5), `status`(0=未完成,2=已完成), `startDate`, `dueDate`, `timeZone`, `reminders`, `repeatFlag`, `items`(子任务), `completedTime`, `parentId`
- **SubTask / ChecklistItem**：子任务。
  - 常用字段：`id`, `title`, `status`(0/1), `completedTime`, `sortOrder`
- **Tag**：标签，可嵌套。
  - 常用字段：`name`, `color`, `parent`, `sortOrder`, `sortType`
- **ProjectGroup**：项目文件夹，用于组织项目。
  - 常用字段：`id`, `name`, `sortOrder`
- **Column**：看板列，用于 kanban 视图。
  - 常用字段：`id`, `projectId`, `name`, `sortOrder`

## 私有 API 端点参考

以下端点基于 `https://api.dida365.com/api/v2`，非官方，可能随时变更：

| HTTP | Endpoint | 功能 |
|------|----------|------|
| GET | `/user/preferences/settings` | 用户设置 |
| GET | `/batch/check/0` | 全量同步 |
| GET | `/project/all/completed?from=&to=&limit=` | 按日期查询已完成任务 |
| POST | `/batch/task` | 批量任务操作 |
| POST | `/batch/taskParent` | 设置子任务关系 |
| POST | `/batch/taskProject` | 移动任务 |
| POST | `/batch/project` | 批量项目操作 |
| POST | `/batch/projectGroup` | 项目文件夹操作 |
| POST | `/batch/tag` | 批量标签操作 |
| PUT | `/tag/rename` | 重命名标签 |
| PUT | `/tag/merge` | 合并标签 |
| DELETE | `/tag?name=` | 删除标签 |

## 为什么不用 Open API

Dida365 提供了 [Open API](https://developer.dida365.com/)，但其功能是私有 API 的子集，且需要注册开发者应用。本项目选择使用私有 API + Cookie 认证，覆盖更全面、配置更简单。

## 资源

- 项目源码：[GitHub](https://github.com/oymy/dida365-ai-tools)
- 私有 API 实现参考：[ticktick-py](https://github.com/lazeroffmichael/ticktick-py)
