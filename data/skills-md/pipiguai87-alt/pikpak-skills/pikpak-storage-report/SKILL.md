---
name: pikpak-storage-report
description: |
  生成 PikPak 云盘空间体检报告：总容量/已用/回收站占用、文件夹体积排行、最大文件清单、可清理空间估算。只读分析，不执行删除。
  Must use this skill when:
  - 用户问「我的云盘用了多少空间」「空间不够了」「哪些文件占地方」
  - 用户想清理空间但不知道从哪下手
  - 用户说「空间体检」「容量报告」「大文件排行」
  - User asks "how much space", "storage full", "what's taking up space", "largest files"
  关键词：空间 / 容量 / 存储 / 大文件 / 清理空间 / storage
---

# PikPak 空间体检报告

扫描云盘给出空间使用全景：哪里占了多少、哪些能清。**只读分析，不执行任何删除。**

## 先决检查

```bash
pikpak auth status -F json    # 读取 storage.total / storage.used / storage.in_trash
```

## 1. 总览

```bash
pikpak auth status -F json | jq '{total: .storage.total, used: .storage.used, trash: .storage.in_trash, vip: .vip.type, expire: .vip.expire_time}'
```

向用户展示：已用/总量（百分比）、回收站占用（回收站也算空间！提示可去 PikPak 网页版清空回收站释放）、会员类型与到期时间。

## 2. 目录体积排行

逐层扫描计算各文件夹体积。用脚本（本 skill 的 `scripts/storage_report.py`）：

```bash
python3 scripts/storage_report.py --folder "" --depth 2 --json /tmp/pikpak-storage.json
```

输出：每个一级/二级目录的体积合计与文件数排行。深度可调（`--depth`），底层目录多时建议从 1-2 层开始逐层下钻。

## 3. 大文件清单

```bash
python3 scripts/storage_report.py --folder "" --top 30
```

按体积列出全盘最大的 N 个文件（路径、大小、修改时间），这是清理的第一抓手。

## 4. 报告与建议

组合输出给用户：

1. **总览卡片**：已用/总量/回收站/会员
2. **体积 TOP 目录**：可能存了整套剧集/合集的大户
3. **大文件 TOP N**：单文件大的（4K 原盘等）
4. **清理建议**：
   - 回收站占空间 → 提示清理回收站（需用户自己在网页版操作，CLI 暂无此功能）
   - 重复多版本 → 引导到 `pikpak-dedup`
   - 垃圾广告文件 → 引导到 `pikpak-ad-cleaner`
   - 老文件/看过的大文件 → 用户自行判断

## 诚实说明（重要）

- 报告是**某一时刻的快照**，存储空间会随上传/下载变化
- 「可释放空间」只能给出上界估计，实际由用户决定删什么
- CLI 无法直接清空回收站/永久删除；需要用户在 PikPak 网页版或 App 操作
- 扫描慢时告知用户进度，不假装秒回
