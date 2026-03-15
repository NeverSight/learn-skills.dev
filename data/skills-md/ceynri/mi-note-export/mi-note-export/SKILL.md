---
name: mi-note-export
description: 从小米云服务笔记批量导出 Markdown 文件，支持删除云端笔记。当用户提到"导出小米笔记"、"同步小米云笔记"、"备份小米笔记"、"删除小米笔记"、"mi-note-export"时触发此 skill。
---

# mi-note-export

从小米云服务（i.mi.com）批量导出笔记为 Markdown，支持增量同步和删除云端笔记。

## 输出目录

执行前需确定笔记的输出目录。按优先级查找：

1. 读取项目根目录下的 `.mi-note-export.json` 配置文件中的 `output` 字段（CLI 原生支持）
2. 如果配置文件不存在（首次使用），向用户确认输出目录（建议默认 `./mi-notes`），确认后将配置写入 `.mi-note-export.json`：
   ```json
   { "output": "./mi-notes" }
   ```

后续执行时 CLI 会自动读取该配置，无需再次询问或手动传 `-o`。

## 使用

通过 `npx` 直接执行，无需提前安装。如已配置 `.mi-note-export.json`，可省略 `-o`：

```bash
npx mi-note-export                          # 增量同步（使用配置文件中的输出目录）
npx mi-note-export -o <output>              # 增量同步（手动指定输出目录）
npx mi-note-export --force                  # 全量重新同步
npx mi-note-export --delete-id <noteId> -y  # 删除指定云端笔记
npx mi-note-export --help                   # 查看所有可用选项
```

遇到其他不适用以上指令的场景时，优先通过 `--help` 查阅是否有合适的选项。

> ⚠️ 首次执行时会自动下载工具及其依赖 Playwright Chromium（约 200+ MB），需提醒用户确认。

首次运行会自动打开 Chromium 浏览器，用户需手动登录小米账号，登录成功后自动提取 Cookie 并缓存。

## 删除笔记流程

删除操作会将笔记移到小米云服务的回收站（30 天内可恢复），**不是永久删除**。

### Agent 执行删除的约束

执行 `--delete-id` 前，**必须**向用户展示待删除笔记的标题、修改时间等详情，并获得用户明确确认后才可执行。笔记详情可从本地同步状态（`<output>/.sync-state.json`）、已导出的文件、或上下文中获取。

## 运行时数据

- **系统缓存目录**（macOS `~/Library/Caches/mi-note-export/`、Linux `~/.cache/mi-note-export/`、Windows `%LOCALAPPDATA%/mi-note-export/cache/`）：存放 Cookie 缓存和浏览器身份数据
- **输出目录内** `<output>/.sync-state.json`：增量同步状态文件

## 输出格式

导出的文件按以下结构组织：

```
<output>/
├── assets/              # 所有笔记的附件（图片、音频等），文件名格式: type_date_hash.ext
├── 文件夹名/            # 笔记所属文件夹
│   └── 笔记标题.md
├── 笔记标题.md          # 无文件夹的笔记
└── 2025-01-01_12-00-00.md  # 无标题笔记以创建时间命名
```

## 常见问题

| 问题 | 操作 |
|---|---|
| Cookie 过期 | 加 `--login` 重新登录 |
| Playwright 未安装 | `npx playwright install chromium` |
| 笔记内容不完整 | 加 `--force` 全量重新同步 |

## 限制

- 不支持私密笔记、待办事项和思维导图
- Cookie 有效期有限（通常数天），过期后需手动重新登录
- 空笔记（无标题且无内容）会被跳过
