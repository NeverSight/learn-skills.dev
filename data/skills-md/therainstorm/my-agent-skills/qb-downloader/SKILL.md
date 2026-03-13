---
name: qb-downloader
description: 从 BT(BitTorrent) 和 PT(Private Tracker) 站点搜索资源，获取磁力链接，并添加到用户托管的 qBittorrent 站点进行下载。适用于用户想要从 BT/PT 下载资源并将种子添加到 qBittorrent 的特定分类（如 Anime1、Movie3） 时。
---

# qb-downloader

自动化从一些 BT/PT 站 搜索资源并添加到用户托管的 qBittorrent 下载。

## When to Use

适用于用户想要从 BT/PT 下载资源并将种子添加到 qBittorrent 的特定分类时。示例：

- PT 下载罗小黑大电影到 Movie1
- qb 下载芙莉莲2 到 Anime1
- PT 下载生化危机 9

## workflow

从*支持的站点列表*中按照*站点优先级*选择一个站点进行尝试，如果失败则继续下一个站点

1. **搜索资源**
  - 浏览器打开站点
  - 输入关键词搜索
    - **优先尝试完整名称**: 如"魔王的女儿过于温柔"
    - **如果无结果，尝试简化**: 如"魔王的女儿"
    - **可以尝试日文/英文原名**: 如果中文名无结果，通过 web_search 获取日文/英文名称后再搜索

2. **种子选择**
  - 查看所有匹配的种子
  - 按照*种子选择*说明优先选择符合条件的种子
  - 连载动漫可能没有全集，需要逐集下载

3. **获取磁力链接**
  - 根据站点的*获取磁链提示*，获取种子的磁力链接

4. **添加到 qBittorrent**
  - qb_url: http://docker.op1:9090
  - 如果用户没有指定分类，根据*qBittorrent分类*选择合适分类
  - 对每个磁力链接执行：
    ```bash
    curl -X POST "${qb_url}/api/v2/torrents/add" \
      -F "urls=磁力链接" \
      -F "category={category}" \
      -F "autoTMM=true"
    ```
  - 成功时 API 返回 "Ok" 或空字符串

5. **验证下载**
  - 查询 qBittorrent 确认种子已添加：
  ```bash
  curl "${qb_url}/api/v2/torrents/info?category={category}"
  ```
  - 检查新添加的种子状态

6. **返回结果**
  - 报告
    - 成功添加的种子数量
    - 失败的种子（如有）
    - 每个种子的名称和信息（如大小、编码、HDR、字幕组）

### 支持的站点列表

- **TJUPT**
  - url: https://www.tjupt.org/torrents.php
  - 介绍：天津大学 PT 站，资源丰富，更新及时，适合下载动漫、电影、电视剧、游戏、图书等。
  - 获取磁链提示：0）点开种子详情页 1）找到"种子名称"下面的"行为"一行 2）"下载种子"右边"复制种子直链" 3）点击获取磁力链接（格式：`https://tjupt.org/download.php?id=xxx&passkey=...`）
  - 注意：磁力链接包含 passkey，不要泄露
- **动漫花园**
  - url: https://share.dmhy.org
  - 介绍：以动漫资源为主的 BT 站
  - 获取磁链提示：无需点开种子详情页，在搜索页面，磁力链接位于表格的 "磁鏈" 列里的向下箭头上（格式`magnet:?xt=...`）。右键复制地址。


注意事项

- 获取磁力链接时，尽量不要点击，避免浏览器弹出窗口调用系统软件（如 xdg-open），应该右键复制链接地址。

### 站点优先级

- 优先尝试 TJUPT，若无结果再尝试动漫花园

### 种子选择

- 动漫、电视剧资源时优先集数完整的而非单集
- 编码格式：av1 > x265 > x264
- 4K 优先
- 有字幕优先，软字幕(not burned to the video)优先
- 杜比视界、HDR10 等增强画质的版本优先

### qBittorrent 分类

如果用户未指定分类，通过 `curl ${qb_url}/api/v2/torrents/categories` 获取现有分类列表，并根据资源类型选择合适分类。

- 类型
  - Anime: 动漫
  - Movie: 电影
  - TV: 电视剧
  - Movie_Anime: 动漫电影
  - GAME: 游戏
- 数字后缀表示不同磁盘
  - 1: zfs raid5(4x16TB)，适合最终珍藏
  - 2: 4TB 机械盘，适合临时下载和不常看的资源
  - 3: 3TB 机械盘，适合临时下载和不常看的资源
