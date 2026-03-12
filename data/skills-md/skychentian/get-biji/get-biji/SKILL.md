---
name: get-biji
description: 从 Get 笔记 (biji.com) 同步语音笔记到本地 Markdown
---

# Get 笔记同步

24/7 录音卡 → Get Notes (biji.com) AI 转录 → 本地 Markdown。

## 同步命令

```bash
cd <skill-dir> && OUTPUT_DIR="<your-output-dir>" node scripts/sync.js
```

认证链：缓存 JWT（30min）→ refresh_token 静默刷新（~90天）→ Playwright 浏览器登录（最后手段）。
首次运行需弹出浏览器登录 biji.com，之后约 90 天内无需再开浏览器。

环境变量：
- `OUTPUT_DIR` — 输出目录（默认 `./notes`）
- `SINCE_DATE` — 起始日期过滤（默认 `2026-01-01`）
- `TEST_LIMIT` — 测试模式，限制同步条数（默认 `0` = 全部）

## 输出结构

```
Get笔记/
  YYYY-MM/
    YYYY-MM-DD_分类_标题.md          ← 摘要文件（短录音原文内嵌）
    YYYY-MM-DD_分类_标题_原文.md      ← 原文转录（长录音，>50行时分离）
```

分类由 `classifyNote()` 智能判断：客户、会议、灵感、待办、复盘、选题。

## 文件格式

### 摘要文件（主文件）

```yaml
---
title: "标题"
date: 2026-02-27
time: "10:34"
note_id: 1234567890
category: 客户
duration_min: 45           # 有录音时才有
transcript: "2026-02-27_客户_标题_原文.md"  # 长录音才有
---

（AI 生成的智能总结 + 章节概要 + 金句精选）

## 附件
- [audio (45 min)](https://...)

## 原文              ← 短录音时内嵌
[00:00] [Speaker 1] ...
```

### 原文文件（长录音）

```yaml
---
date: 2026-02-27
note_id: 1234567890
title: "标题"
summary: "2026-02-27_客户_标题.md"   # 互相引用
---

## [03:25] 章节标题          ← 章节标题自动注入
[03:25] [Speaker 1] 正文...
```

## 辅助脚本

- `rebuild-state.js` — 从 API 重建同步状态（丢失 `.sync-state.json` 时用）
- `dedupe.js` — 去重工具

## 状态文件

- `.sync-state.json` — 已同步的 note_id 列表（增量同步依赖）
- `.token-cache.json` — JWT + refresh_token 缓存
- `.auth-state.json` — Playwright 浏览器登录状态
