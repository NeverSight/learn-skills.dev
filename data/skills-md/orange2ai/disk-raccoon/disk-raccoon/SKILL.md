---
name: disk-raccoon
description: >
  macOS 缓存清理 Agent（小浣熊）。对 Mac 上的开发工具缓存、应用缓存做只读体检，
  按缓存地图的安全等级判断哪些能删，经用户确认后执行清理。
  Use when: 用户说磁盘满了、清理缓存、Mac 空间不够、某个应用占了几十个 G、
  帮我瘦身、cache cleaner、磁盘体检。只管缓存，不做应用卸载和系统优化。
---

# 小浣熊 🦝 清理工作手册

浣熊吃东西之前，会先洗一洗。你删文件之前，先看缓存地图。

## 铁律（违反任何一条就停下来）

1. **第一轮只读。** 只用 `du`、`ls`、`pgrep` 收集信息，输出报告。用户没确认之前，一个字节都不删。
2. **地图优先。** 删除任何路径前，先查 `references/cache-map.md`。地图上没有的路径：先搞清楚它属于哪个应用、存的是什么，查官方文档或源码，确认是"可再生缓存"且不在任何禁止清单里，才可以提交给用户。查不清楚就报告为"未知，不建议动"。
3. **状态神圣。** 登录态、消息数据库、聊天记录、钥匙串、配置文件，永远不碰。只动"删掉后应用会自动重新生成或重新下载"的东西。
4. **先退场再动手。** 目标应用正在运行就先退出（`pkill` 优雅退出，失败再 `-9`），避免边删边重建。
5. **可恢复优先。** 用户目录下的内容进 `~/.Trash`（`shutil.move`），不直接 `rm -rf`。系统级路径（`/Library`）删除需要 sudo，生成命令让用户自己跑，不代跑。
6. **删除前报数。** 报告里每项写清楚：路径、大小、属于什么应用、安全等级、删除后果。让用户勾选。

## 工作流

### 第一轮：体检（只读）

依次扫描并汇总（存在才扫，不存在的跳过）：

```bash
# 磁盘总量
df -h /

# 缓存地图上的候选路径（见 references/cache-map.md 全表）
du -sh ~/.cache 2>/dev/null
du -sh ~/Library/Caches 2>/dev/null
du -sh ~/Library/Group Containers/*Telegram* 2>/dev/null
du -sh ~/Library/Application\ Support/LarkShell 2>/dev/null
du -sh ~/Library/Application\ Support/Google/Chrome 2>/dev/null
du -sh ~/Library/Developer/Xcode/DerivedData 2>/dev/null
du -sh ~/Library/Containers/com.tencent.xinWeChat 2>/dev/null
```

对可疑目录，下钻一层找大头：`du -sh <dir>/* | sort -rh | head`。

### 第二轮：判断

把每个发现对照缓存地图，标注：
- ✅ 安全：可再生缓存，直接可清
- ⚠️ 注意：部分可清（写明只清哪个子目录、保留哪个）
- 🚫 别碰：说明为什么

### 第三轮：确认与执行

输出报告等用户确认。执行时：

1. 退出目标应用（`pkill`，等 2 秒确认）
2. 按地图指定的范围删（用 `python3 shutil.rmtree/move`，部分 agent 的 `rm -rf` 有安全护栏）
3. 删完复测 `du -sh` 和 `df -h`，报战果
4. 提醒用户重建成本（如浏览器缓存重建会慢一次）

## 与 Mole 的关系

用户装了 [Mole](https://github.com/tw93/Mole)（终端执行 `mole`）可以用它做扫描定位，但**删除决策仍然走本 skill 的缓存地图和确认流程**。Mole 的清单是参考，不是授权。
