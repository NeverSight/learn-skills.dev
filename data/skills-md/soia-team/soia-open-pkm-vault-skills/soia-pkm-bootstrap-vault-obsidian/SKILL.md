---
name: soia-pkm-bootstrap-vault-obsidian
description: 以 dry-run 和保留未知配置的结构化合并方式，把已有 Markdown vault 配置为 Obsidian 消费端，启用 Bases 与可选宽页 CSS。触发：「配置 Obsidian vault」「启用 Obsidian Bases」「接入 Obsidian 消费端」
dependencies:
  hard: [soia-pkm-bootstrap-vault-base]
version: 2.1.3
created_at: 2026-07-16 16:00:31
updated_at: 2026-11-18 10:35:00
created_by: gpt-5.6-luna
updated_by: gemini-4-hydrogen
---

# soia-pkm-bootstrap-vault-obsidian

在 `soia-pkm-bootstrap-vault-base` 创建的通用 Markdown vault 上安全启用 Obsidian 消费端（Bases、可选 `wide-page` CSS 与 `.base` 视图）；Markdown、frontmatter 与 Git 仍是唯一内容真源，不代写云端笔记。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 为已有 Markdown vault 启用 Obsidian Bases 与宽页样式 | dry-run 预览并结构化合并 `core-plugins.json`/`appearance.json`/`app.json`，保留已有主题/插件/未知键，建缺失 `.base` | JSON 合并、CSS create/drift 清单、备份路径与 `--check` 结果 |

### 客户如何使用

先确认已完成 `soia-pkm-bootstrap-vault-base` 初始化（base 不写 `.obsidian`），提供 vault 路径跑默认 dry-run，核对清单后再 `--apply` 与 `--check`，最后在 Obsidian（建议 1.9+，可按需装社区插件如 Tars/Terminal/Obsidian Git）中验证打开视图。

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-bootstrap-vault-obsidian`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。依赖 `soia-pkm-bootstrap-vault-base`；客户端见 <https://obsidian.md/download>。

### 私密信息与中间数据

无需账号与私有 config；待改文件修改前备份在 `.obsidian/.soia-backups/<timestamp>/`，回执只汇报键类别、数量与状态，不泄露完整私有 JSON。

### 日志与完成回执

汇报已检查 Obsidian 版本、Bases/CSS/link format 的 create/update/skip/drift 状态、`.obsidian` 文件变更、`--check` 与客户端实测结果及需客户手动补做项。

## 配置执行与回滚流程

```bash
python3 scripts/configure_obsidian.py <vault-path>                              # 1. dry-run
python3 scripts/configure_obsidian.py <vault-path> --apply [--link-format relative]  # 2. 备份后安全合并
python3 scripts/configure_obsidian.py <vault-path> --check                      # 3. 验收
```

- 默认启用 Bases、工作台/资料库/历史三个 create-only `.base`（不用 Dataview）及 `wide-page.css`（已有 CSS 与 bundled 不同时仅报 `drift` 跳过；仅看过 plan 并明确授权覆写才加 `--force-managed --apply`）。
- 兼容新版对象与旧版列表两种核心插件格式；保留未知核心插件、主题、snippet 与 JSON 键。
- 回滚须先关闭 Obsidian，再从 `.obsidian/.soia-backups/<timestamp>/` 按批精确恢复（勿删整个 `.obsidian`）；验后打开真实 `.md` 与 `.base` 复核样式与配置保留。
