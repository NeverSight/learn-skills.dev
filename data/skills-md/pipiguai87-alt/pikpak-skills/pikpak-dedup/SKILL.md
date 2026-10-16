---
name: pikpak-dedup
description: |
  分析 PikPak 云盘里的重复/多版本资源（同一影片的多个清晰度、不同压制版本），按所选策略给出「保留哪个、清理哪些」的建议清单，用户确认后将旧版本移入回收站。
  Must use this skill when:
  - 用户提到「查重」「去重」「重复文件」「多版本」「清理旧版本」「同一部电影下了好几次」
  - 用户发现同一资源存在多个清晰度/版本想清理
  - 用户说「保留最新」「保留最高清」「帮我看看哪些是重复的」
  - User says "find duplicates", "dedupe my cloud drive", "I downloaded the same movie twice", "clean up old versions", "keep the newest/highest quality copy"
  - User asks to "compare versions" or "save space by removing dupes"
  只在用户确认清单后执行删除；删除一律是移入回收站（可恢复），工具本身只读。
---

# PikPak 查重清理

在同一目录树内找出同一资源的多个版本，按策略建议保留哪份、清理哪些。**只读分析 + 用户确认 + 移入回收站。**

## 先决条件检查

1. `pikpak version` 确认 CLI 已安装；
2. `pikpak auth status -F json` 确认 `logged_in` 为 true，否则 `pikpak auth login`。

## 工作流程

### 1. 确定扫描范围与保留策略

询问用户扫描哪个文件夹。说明三种策略，让用户选择（默认 newest）：

| 策略 | 保留哪份 | 适用场景 |
|------|---------|---------|
| `newest`（默认） | 修改时间最新 | 想要最新导入/更新的版本 |
| `largest` | 体积最大 | 通常码率最高 |
| `highest-res` | 分辨率最高 | 优先画质梯队 |

### 2. 运行分析（只读）

```bash
python3 scripts/analyze_dupes.py --folder <folderID> --policy newest --json /tmp/pikpak-dup-report.json
```

脚本按「文件名归一化」分组：剔除清晰度/编码/来源等包装噪音词（1080p、x264、WEB-DL…），但**保留语义 token**（集数 S01E01、音轨语言、配音版等）——语义不同不会误合并。

### 3. 展示分组结果

每组展示：资源标识、版本数量、建议保留项（✓）、建议清理项（✗），附带体积/时间/分辨率佐证。先给一行**量化总结**（组数 + 可释放空间），例如：

> 发现 **12 组重复资源**，清理旧版可释放约 **86 GB**（保留每个资源的最新/最高清版本）。

（数字从 JSON 报告的 `groups[].trash_candidates[].size` 求和得出。）
说明分组逻辑，特别提醒用户检查：

- 被列为清理的版本是否真的是旧版（而非用户刻意保留的另一个拷贝）
- 「完全重复」（内容哈希相同）与「不同版本」的区别——前者可放心清理，后者需用户自己判断

### 4. 用户确认后执行

```bash
python3 scripts/analyze_dupes.py --folder <folderID> --policy newest --emit-trash-cmd
```

把生成的 `pikpak rm <id...>` 命令展示给用户并说明可恢复性，确认后执行。

### 5. 复核与产出

- `pikpak ls` 抽查确认；
- 报告清理了几组、几个文件、预计释放的空间（对比清理前后 `pikpak auth status -F json` 的 `storage.used`）。

## 归一化与匹配细节

规则集中在 `scripts/analyze_dupes.py`：`QUALITY_TOKENS`（剔除词表）、`KNOWN_EXTS`、最小体积阈值（默认 100 KB，避免把小海报图卷进分组）。调整后必须重跑 `dev/run_tests.py`。

匹配是**保守**的：宁可漏合并（用户手动处理）也不错误合并（可能误删珍藏版本）。同名文件在不同文件夹中也会被分组——清理前要留意是否为不同合集的一部分。

## 安全边界

- **只读分析**：脚本只调用 `pikpak ls`（源码级保证，有回归测试覆盖）
- **用户确认**：每个待清理项都必须经用户过目
- **可恢复**：`pikpak rm` 移入回收站，误删可恢复
- **不做内容判断**：只按文件名与元数据分组，不评判资源内容
