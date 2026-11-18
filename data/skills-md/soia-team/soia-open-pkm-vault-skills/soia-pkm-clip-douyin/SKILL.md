---
name: soia-pkm-clip-douyin
description: 归档单条抖音视频到 Obsidian vault，并保留本地媒体索引。触发：「归档这条抖音」「clip 这个抖音视频」「只要抖音文案」
version: 1.0.5
created_at: 2026-07-24 15:52:29
updated_at: 2026-11-18 10:10:00
created_by: claude fable 5
updated_by: gemini-4-hydrogen
---

# soia-pkm-clip-douyin

把单条抖音视频的元数据与文案沉淀进 Obsidian vault，MP4 本体下载至本地 `~/Downloads/soia-pkm-clip-douyin/<video_id>/video.mp4`（`media_local_path` 索引），避免大体积二进制进 git 仓库。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 归档一条抖音视频 | 用 Playwright 拦截签名响应、校验 `video_id` 去重、下载 MP4 至本机目录并写入 Markdown | vault 笔记路径、MP4 本地路径、作者/时长/互动数 |
| 只要文案与元数据（暂不下载视频） | `--metadata-only` 跳过下载并写笔记 | `media_local_path` 置空、`media_fetched: false` |
| 强制更新已归档视频 | `--force` 重抓并在覆盖时保留人工 `topics`/`people`/`## 摘要` | 更新后的笔记与核验回执 |

### 客户如何使用

- 「归档这条抖音：`https://www.douyin.com/video/<id>`」（支持 `modal_id=`/`resource_id=` 与 `v.douyin.com` 短链）
- 「先只抓这条抖音文案和元数据，不要下视频（`--metadata-only`）」

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-clip-douyin`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。强制依赖 `playwright` + Chromium（`pip install playwright && python -m playwright install chromium`）；缺依赖直接报错提示安装命令，不猜测降级。

### 私密信息与中间数据

仅使用匿名一次性 headless context，不登录、不持久化 cookie；拦截到的签名直链（含 `msToken`/`a_bogus`）严禁写入 vault、stdout 或错误日志（仅印去 query 的 host+path）。可选配置放 `$SOIA_PKM_CLIP_DOUYIN_CONFIG_FILE`（兼容 `$SOIA_PKM_CLIP_DOUYIN_ENV_FILE`）或 `~/.config/soia-skills/soia-pkm-clip-douyin/config.yml`（模板见 [assets/config.example.yml](assets/config.example.yml)）。

### 日志与完成回执

先落盘再回执：汇报实际目录（若走 `Articles/` 兜底须提示配置正式目录）、vault 笔记与 MP4 路径、MP4 `ftyp` 校验结果及`未核实`字段；视频落盘仅代表 `captured`，默认接生命周期完成 `organized → MOC/导航 → map → Base`（转写/OCR 等可检索性单独说明）。

## 运行机制与规范

1. **配置与目录优先级**：CLI `--vault`/`--articles-dir` > `OBSIDIAN_VAULT`/`OBSIDIAN_ARTICLES` > 私有 `config.yml` > cwd 向上探测（`AGENTS.md`/`.obsidian`）> `Articles/` 兜底（stderr 打警告，退出码 0）。
2. **去重、拦截与下载**：
   - 运行 `python3 scripts/archive_douyin.py <URL> [--force] [--vault <p>] [--articles-dir <d>] [--metadata-only] [--timeout 90]`。
   - 用数字边界 `(?<!\d){video_id}(?!\d)` 对 frontmatter `url:` 去重，已存在 `SKIP`（建议用完整链接以防短链漏判）。
   - Playwright 监听 `douyin.com` JSON 响应，按 `aweme_id` + `"video"` 匹配；取 `play_addr` → `play_addr_h264` → `download_addr` 用 stdlib `urllib`（带 `Referer` + `Range: bytes=0-`）流式下载并校验 `ftyp` box；下载全败时非 0 退出且不写笔记。
   - `--metadata-only` 后若想补下视频必须完整重跑（签名直链短时效，不存中间链接）。
3. **落盘结构**：文件 `<YYYY-MM-DD>-抖音-<作者前20字>-<文案前50字>.md`（同日同作者多条加 `-<video_id 后6位>`），frontmatter `tags:[视频摘抄]`、`source: 抖音`、`url`、`author`、`published_at`、`captured_at`、`language: zh`、`type: video`、`topics`、`people`、`media_local_path`、`content_complete`、`metrics`。正文含 `> [!source]-`、`## 摘要`（AI 补 1 句）、`## 原文`（不加工）、`## 我的看法`（**永远留空**）、`## 关联`。

## 验证与前向测试

改后须跑 `python3 -m py_compile scripts/archive_douyin.py`、`python3 scripts/audit_skills.py --strict` 及真实公开链接烟测（核对 `MP4 ftyp box`、互动数与原文一致、重跑 `SKIP`）。
