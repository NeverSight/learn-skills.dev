---
name: wxmp-article-harvester
description: 抓取、筛选并导出微信公众号公开文章的独立 Skill。用户提到微信公众号、公众号文章、mp.weixin、wcx、搜索公众号、导出最近 N 天或某年度文章、批量抓取、断点续抓、正文补全、教程文章筛选、微信文章链接保存时使用。支持 Markdown/JSON/CSV，默认用 wcx 获取索引、Playwright 提取正文；付费 Metaso 兜底必须显式授权。
---

# wxmp-article-harvester

目标：把公开公众号文章稳定加工成可检索、可审计、可恢复的本地资料包。

## 运行架构

1. `preflight.py` 只检查依赖，不自动安装或升级任何软件。
2. `wcx_run.py` 搜索公众号、刷新登录态、抓元数据并导出索引。
3. `harvest_wxmp.py` 过滤日期和标题，复用一个 Playwright 上下文提取正文并保留图片顺序。
4. 首次命中微信验证码或风控页后打开浏览器熔断，停止本轮后续页面请求；刷新失败时保留已通过质量门的旧正文。
5. 没有可信正文时标记 `partial`。只有用户明确授权付费和第三方 URL 传输后，才加 `--allow-metaso`。

## 开始前

运行预检：

```bash
python3 <skill-root>/scripts/preflight.py --json
```

缺少依赖时明确报告并停止。安装命令见 `README.md`。登录过期由 `wcx_run.py` 打开浏览器刷新一次；token 不打印，cookie 不进入进程参数。

## 意图路由

| 用户意图 | 执行 |
| --- | --- |
| 搜索公众号 | `python3 scripts/wcx_run.py -- search "账号名"` |
| 最近文章索引 | `python3 scripts/harvest_wxmp.py --account "账号名" --limit 50 --no-fulltext` |
| 日期范围全文 | `python3 scripts/harvest_wxmp.py --account "账号名" --from-date YYYY-MM-DD --to-date YYYY-MM-DD --fulltext` |
| 教程类文章 | 在日期范围命令后加 `--title-regex '(教程|手把手|教你|技巧|实操|实践|工作流)'` |
| 年度/深历史 | 首轮加 `--batch`，冷却后只用 `--resume`；状态会恢复账号、范围和全文策略 |
| 保存单篇链接 | `python3 scripts/browser_reader.py --url "https://mp.weixin.qq.com/s/..." --output-dir "目录"` |

没有指定数量时默认最近 50 篇。最近 N 天默认最多取 `min(N × 8, 80)` 篇元数据。

## 硬规则

- 只接受 `https://mp.weixin.qq.com/s...` 公开文章链接；拒绝其他域名、协议和带用户信息的 URL。
- 所有 `wcx search/fetch/list/export/status` 都走 `wcx_run.py`。运行时禁止自动 `pip install` 或强制升级。
- `--limit`、`--batch-size` 的代码硬上限都是 80。深历史任务使用 offset 游标分批，每轮最多 80 篇，并校验远端总数、头部文章 ID 和上一批边界 ID。
- 只补正文或重新筛选时加 `--skip-fetch`，避免重复触发微信频控。
- 默认不调用 Metaso。用户明确接受付费和把文章 URL 发给第三方后，才使用 `--allow-metaso`。
- `wcx` 摘要占位、`正文尚未抓取`、微信页面壳、通用 `Video` 页面和低信息量结果都不能标记成功。
- 正文成功后同步更新标题、页面发布时间、作者、来源 URL 和提取通道。索引保存相对路径，迁移目录后仍可用。
- 默认输出到系统用户数据目录下的 `wxmp-article-harvester/exports/<公众号>/`；可用 `WXMP_HARVEST_HOME` 覆盖。
- 文章仅用于用户授权的研究、学习和归档。保留原文 URL、作者和发布时间；不把抓取结果包装成可再分发版权。

## 分批与恢复

```bash
# 第一轮：按真实 offset 抓一批
python3 scripts/harvest_wxmp.py --account "账号名" --year 2025 --fulltext --batch --batch-size 60

# 到达 .harvest-state.json 的 resume_after 后继续
python3 scripts/harvest_wxmp.py --resume
```

存在多个待恢复账号时，`--resume` 会停止并要求补 `--account` 或 `--output-dir`。监控 JSON 中的 `status`、`task_id` 和 `batch.completion_reason`；`complete` 才代表本次契约完成，`cursor_drift` 必须停止并重新建任务。

## 常用命令

```bash
# 最近 30 天全文，默认不使用付费兜底
python3 scripts/harvest_wxmp.py --account "账号名" --since 30d --fulltext

# 精确日期范围 + 教程标题筛选
python3 scripts/harvest_wxmp.py --account "账号名" \
  --from-date 2026-06-25 --to-date 2026-07-25 --fulltext \
  --title-regex '(教程|手把手|教你|技巧|实操|实践|工作流)'

# 已有索引，只补正文；用户已明确授权 Metaso
python3 scripts/harvest_wxmp.py --account "账号名" --skip-fetch --fulltext --allow-metaso
```

## 输出契约

- `index.json`、`index.csv`、`index.md`：文章元数据、相对路径、状态和失败原因。
- `articles/*.md`：保留原文 URL、发布时间、作者、提取通道以及正文中的图片顺序。
- `harvest-report.md`：`success`、`partial`、`failed` 分开统计；任何页面壳或摘要占位进入 unresolved。
- `.harvest-state.json`：稳定任务 ID、配置指纹、批次 offset、远端头/边界 ID、范围、完成原因、全文策略、Metaso 授权和冷却状态。

回执必须说明保存目录、成功/部分/失败数量、报告路径和未解决文章。排障时读取 `references/troubleshooting.md`。
