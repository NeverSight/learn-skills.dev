---
name: soia-pkm-query-vault
description: 以只读方式搜索整个 Markdown/Obsidian 知识库或指定模块，检索文件名、正文、frontmatter、标签、反向链接、代码与附件，并按来源层级返回可核验结果。触发：「搜索知识库」「搜索知识库某个模块」「在知识库里找」「从知识库回答」「查需求/代码/PDF/Word/图片」「查反向链接」
version: 1.6.2
created_at: 2026-08-01 12:00:00
updated_at: 2026-11-18 10:25:00
created_by: gpt-5
updated_by: gemini-4-hydrogen
---

# soia-pkm-query-vault

面向 AI 与用户的 vault **只读查询层**：按层级找证据、排序并引用，不整理目录、不维护索引、不改任何文件，跳过所有隐藏目录（`.git`/`.obsidian`）、配置目录与 symlink 防越界。涉及入库状态时须区分 `captured`/`organized` 与五段完整回执（搜索命中不等于整理完成）。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 检索笔记、需求、frontmatter、标签、代码与反向链接 | 调用 `query_vault.py` 按文件名/正文/字段/标签/入链精确搜索 | 按可信层级排序的相对路径/wikilink 与短片段 |
| 查询 PDF / DOCX / 图片 / 音视频 | 优先走 Omnisearch/Text Extractor 或 MCP 查正文；无后端则退回文件名命中并明示限制 | 明确标注 `filename_hit`、`content_hit` 或 `ocr` 命中类型 |
| 避免敏感语料正文泄露 | 对历史导入、账号、安全或私人范围默认使用 `--no-snippets` | 只含路径、计数与元数据的脱敏回执 |

### 客户如何使用

给出 vault 路径与关键词/问题；只要求检索或回答时，先读根 `AGENTS.md` 与命中区规则，用最窄模式缩小候选后再打开必要正文。

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-query-vault`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。本地检索只需 Python 3；附件全文检索可选 Omnisearch + Text Extractor、`obsidian-mcp-server` 或 QMD（仅作候选召回，详情见 [multimedia-search-options.md](references/multimedia-search-options.md)）。

### 私密信息与中间数据

跳过隐藏目录、配置目录、symlink 与二进制正文，不写持久索引缓存；对历史导入/敏感语料使用 `--no-snippets`。

### 日志与完成回执

汇报 `checked_at`、查询模式、扫描/匹配/截断/不可读计数与 snippet 状态；回答按「当前状态 / 稳定知识 / 历史证据」组织并给出完整路径或 wikilink，标出 `needs_review`/`deprecated`/`superseded_by`/历史路径提示。

## 命令与分级检索规则

1. **命令入口**（`--path-prefix`/`--exclude-prefix` 可重复且限相对路径；`--limit` 防截断）：
   ```bash
   python3 scripts/query_vault.py --vault <vault> --mode all|filename|content|tag|frontmatter|backlinks|inventory --query '<kw>' [--field status] [--path-prefix '<p>'] [--exclude-prefix '20_资料库/90_历史导入'] [--include-ext .feature] [--no-snippets] --json
   ```
2. **层级排序（按层不按命中次数）**：`10 当前状态` → `20 精选（仅 10_主题知识 / 20_规范与手册 / 30_学习指南 标为 stable）` → `30 冻结证据` → `40/50/60 专项` → `20_资料库/90_历史导入（标 imported，先排除以免干扰）` → `90 历史归档（90_系统归档/60_整理与迁移记录 需标 evidence_class 并优先 canonical/superseded_by）`。搜索强时效事实时须说明需外部核验。
3. **代码与附件查询规范**：需求/代码先用精确专有名词、接口/符号名（未命中再拆 2–3 短词），先定义后调用与测试；查文档/组件先 `filename` 锁定导航与附件，再显式区分 `filename_hit` 与 `content_hit`（PDF/Word/图片无后端只可报 `filename_hit` / 正文尚未解析；DOC/PPT/XLS 禁当 UTF-8 读取）。
4. **严格只读**：绝不修改文件、frontmatter、Bases、地图或 git 状态；目录迁移转 `soia-pkm-manage-vault-lifecycle`，死链/标签审计转健康技能。

## 验证与前向测试

运行前后 vault 文件树哈希须一致；fixture 与前向测试须验证中文、标签/frontmatter/backlinks、UTF-8 代码与 `--include-ext`、`--no-snippets` 脱敏、附件命中区分及 90 区旧 `status` 不冒充现状。
