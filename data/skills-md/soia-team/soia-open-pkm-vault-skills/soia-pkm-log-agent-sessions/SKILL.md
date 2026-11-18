---
name: soia-pkm-log-agent-sessions
description: 为 Claude Code、Codex 等本地 AI 接入最小化 vault 会话改动快照，支持去重、dry-run、既有 notify 合并和安全卸载。触发：「接入 AI 会话日志」「记录 Codex 改动」「配置 SessionEnd 日志」
version: 1.1.2
created_at: 2026-08-01 12:00:00
updated_at: 2026-11-18 10:50:00
created_by: gpt-5
updated_by: gemini-4-hydrogen
---

# soia-pkm-log-agent-sessions

为 AI 会话结束接入**最小改动快照**（不存完整 prompt、对话/diff/事件 JSON，不做工作台分流或健康检查，不执行 git add/commit/push）。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 为 Claude Code `SessionEnd` / Codex `notify` 接改动快照 | 展示配置合并片段获同意后备份并无损合并（保留已有 notify），用 diff+未追踪哈希去重 | 轻量快照目录、`deduplicated` 去重结果与安全卸载方式 |

### 客户如何使用

给出 vault 路径、AI 名称与目标日志相对目录，确认待修改的配置片段后接入，再跑一次 dry-run 与真实小改动验证快照与内容去重。

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-log-agent-sessions`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。依赖 Python 3、Git 与 POSIX bash；配置 `$SOIA_PKM_AGENT_SESSION_CONFIG_FILE` 或 `~/.config/soia-skills/soia-pkm-log-agent-sessions/config.yml`。

### 私密信息与中间数据

日志仅写时间、agent、变更计数与分区统计（默认不列具体文件路径，仅显式 `--include-paths` 才记）；去重状态存 `$XDG_STATE_HOME/soia-pkm-log-agent-sessions/`（兼容 git worktree，不写 `.git`）。

### 日志与完成回执

汇报配置修改情况、快照写入/`deduplicated` 状态、日志相对目录与变更计数、状态目录类别、验收结果与卸载方式。

## 接入流程与硬边界

1. **手动校验与默认路径**：`python3 scripts/session_log.py --vault <vault> --agent <slug> [--dry-run]`。默认写入 `30_日志与思考/20_Agent工作日志/10_自动快照/<年>/<agent>/`（可用 `--log-dir`/`SOIA_SESSION_LOG_DIR` 覆盖，限 vault 内）；`--vault` 必须是独立 Git worktree 根（嵌套子目录拒绝运行）。
2. **接入与卸载（细则见 [references/session-log-setup.md](references/session-log-setup.md)）**：改 `.claude/settings.json` 或 Codex `config.toml` 前先备份并获明确同意；保留既有 hook/notify；写入真实安装脚本路径；旧日志清理只预览数量/体量，不自动删除。
3. **验收标准**：frontmatter 含 `tags: [Agent日志, 自动快照]`；连续编辑同文件生成新快照、无改动报 `deduplicated`；配置卸载后原 hook/notify 完好；日志零秘密值/diff/完整正文。
