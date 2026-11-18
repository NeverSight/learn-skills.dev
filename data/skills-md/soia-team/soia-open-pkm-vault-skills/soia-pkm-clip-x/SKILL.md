---
name: soia-pkm-clip-x
description: 将单条 X/Twitter 推文、thread 或 Article 归档到 Obsidian vault。触发：「归档这条 X」「clip 这条推文」「整理这条 thread」
version: 1.1.8
created_at: 2026-07-02 03:51:43
updated_at: 2026-11-18 10:05:00
created_by: claude opus 4.6
updated_by: gemini-4-hydrogen
---

# soia-pkm-clip-x

将单条 X 推文、同作者 thread 或 X Article 长文沉淀为 Obsidian vault 笔记，按 `url:` 去重并支持随归档导出 PDF 与 Telegram 收藏同步。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 归档单条推文、thread 或 X Article | 调用 `archive_x.py` 走免密 FxTwitter API（兜底 syndication），回溯 thread、展开 `t.co`、提取 `content.blocks[]` 与首图 | `<articles>/<YYYY>/<MM>/` Markdown 笔记、摘要、双链与 MOC 更新 |
| 归档外文推文或导出 PDF | 自动补充自然中文意译段（`## 中文译文`）；请求导出 PDF 时走 Obsidian 原生导出参考 | 双语对照归档笔记或原生 PDF |
| 批量导入 Telegram「我的收藏」X 链接 | 解析 JSON 导出（或按授权走 MTProto），先 `--dry-run` 预览再去重归档 | 新增/跳过篇数与异常链接清单 |

### 客户如何使用

- 「归档这条 X：`https://x.com/<handle>/status/<id>`」
- 「整理这条 X thread 并导出 PDF」
- 「用 `--dry-run` 同步我的 Telegram 收藏导出 JSON 里的 X 链接」

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-clip-x`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。单条抓取纯 Python 3 stdlib；仅 MTProto 电报同步需 `telethon`。

### 私密信息与中间数据

单条 X 抓取无需登录；可选配置与电报 MTProto 凭据存 `$SOIA_PKM_CLIP_X_CONFIG_FILE`（兼容 `$SOIA_PKM_CLIP_X_ENV_FILE`）或 `~/.config/soia-skills/soia-pkm-clip-x/config.yml`（支持 `OBSIDIAN_VAULT`、`OBSIDIAN_ARTICLES`、`X_ARCHIVE_LANG`、`TELEGRAM_*`），不进仓库、vault 或日志。

### 日志与完成回执

先落盘再回执：汇报实际目录、新建/跳过状态及未展开短链/`未核实`字段；走 `Articles/` 兜底时必须警示并提示配置正式目录。单对象抓取只代表 `captured`，默认接生命周期完成 `organized → MOC/导航 → map → Base`（不适用写 `not_applicable`）。

## 工作流、定位与命名规范

1. **路径发现优先级**：vault 按 `--vault` → `OBSIDIAN_VAULT` → 私有 `config.yml` → cwd 向上找 `AGENTS.md`/`.obsidian`；文章目录按 `--articles-dir` → `OBSIDIAN_ARTICLES` → 私有 `config.yml` → `Articles/` 兜底（向 stderr 打警告且退出码 0）。
2. **抓取与正文处理**：`python3 scripts/archive_x.py <URL> [--force] [--vault <path>] [--articles-dir <dir>]` 按 frontmatter `url` 去重，优先以 FxTwitter facet `replacement` 展开短链；正文含论文/附件链接时只保留 canonical URL，下载与提取交给 `soia-pkm-clip-drive/scripts/archive_pdf.py --deep`。
3. **AI 补全与边界**：归档后补 1 句话 `## 摘要`、1–3 个 `topics`/`people` 双链；`language != zh` 默认补完整意译 `## 中文译文`（保留专有名词/命令/代码英文）；`## 我的看法` **永远留空**。
4. **文件名与 frontmatter**：写入 `<articles>/<YYYY>/<MM>/<YYYY-MM-DD>-X-<handle>-<title前50字>.md`（同日同作者重复加 `-<status_id 后6位>`），字段含 `tags:[文章摘抄]`、`source: X`、`url`、`author`、`handle`、`published_at`、`captured_at`、`language`、`type(tweet|thread|article)`、`topics`、`people`、`media`（视频仅记 mp4 直链）、`content_complete`、`metrics`。纯转推空内容告警；404 建议 archive.org；5xx 重试后兜底 syndication。
5. **扩展工作流**：PDF 原生导出见 [references/obsidian-pdf-export.md](references/obsidian-pdf-export.md)；Telegram 批量同步见 [references/telegram-sync.md](references/telegram-sync.md)。

## 验证与前向测试

```bash
python3 -m unittest tests.test_archive_x
```

离线 fixture 与前向测试覆盖 `t.co` facet 展开、同 status ID 原文/译文去重优先级与媒体保留。
