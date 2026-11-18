---
name: soia-pkm-transform-article-notebooklm
description: 用 NotebookLM 将文章转换为学习材料。触发：「NotebookLM 生成试卷」「NotebookLM 做闪卡」「NotebookLM 生成播客」
version: 1.1.3
created_at: 2026-07-16 11:30:32
updated_at: 2026-11-18 10:45:00
created_by: claude opus 4.6
updated_by: gemini-4-hydrogen
---

# soia-pkm-transform-article-notebooklm

将 Markdown / vault 文章（URL 先 clip）转换为 `quiz`（试卷）、`flashcards`（Anki 闪卡）、`mindmap`（脑图）、`podcast`（播客脚本）或 `notes` 学习材料：支持 NotebookLM 或本地 Markdown 生成，Prompt 与产物规范落盘可重跑。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 生成试卷 / 闪卡 / 脑图 / 播客 / 学习笔记 | 按 `learning` 模式提炼全部核心知识点，选 `notebooklm` 或本地 Markdown 生成 | `outputs/transform/<YYYY>/<stem>/` 产物、`prompts/`、题数或节点数 |

### 客户如何使用

说明来源（vault 路径/URL 先 clip）及类型（`quiz` 默认 / `flashcards` / `mindmap` / `podcast` / `notes`），可选指定题数、难度与 `provider`（`local` / `notebooklm`；不用于做封面/PPT）。

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-transform-article-notebooklm`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。本地方案零额外依赖；`notebooklm` 为可选增强（缺时不阻断，参见 [provider-notebooklm.md](references/provider-notebooklm.md)）；配置 `~/.config/soia-skills/soia-pkm-transform-article-notebooklm/config.yml` 或 `$SOIA_PKM_TRANSFORM_ARTICLE_NOTEBOOKLM_CONFIG_FILE`。

### 私密信息与中间数据

NotebookLM 登录态仅留在本地专用浏览器 profile，绝不导出 Cookie 或 Google 凭据；上传源文前须由客户确认范围。

### 日志与完成回执

汇报 `source`、`artifact_type`、`provider`（含失败目标列表，严禁静默跳过）、Prompt 与产物路径/notebook id、题目=答案=解析或 Mermaid 可解析验证结果。

## 工作流与质量边界

1. `notebooklm` 路线先做健康检查（[provider-notebooklm.md](references/provider-notebooklm.md)），上传并记录 `notebook id`；`local` 路线读取 [prompt-notebooklm.md](references/prompt-notebooklm.md) 落盘 Prompt 到 `outputs/transform/<YYYY>/<stem>/prompts/` 后生成产物。
2. 质量验收对照 [quality-gates.md](references/quality-gates.md) 与 [notebooklm-test-matrix.md](references/notebooklm-test-matrix.md)：`quiz`/`flashcards` 必须验证 **题目数 == 答案数 == 解析数**，`mindmap` 校验 Mermaid 可解析。
