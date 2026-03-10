---
name: stock-log-viewer
description: 翻阅郑大姐股票分析日记本的工具。支持查看最新n条日记、统计总数、按日期查询、按股票名称/代码查询、全文搜索关键词。

---

# 郑大姐日记本查阅工具

**触发关键词**: "郑大姐日记本"、"查看日记"、"查阅分析记录"

---

## 功能概述

这是一个用于查阅郑大姐股票分析历史记录的工具，方便用户随时调阅之前的分析观点。

### 支持功能

1. **查看最新n条日记** - 快速浏览最近的分析记录
2. **统计日记总数** - 了解已经记录了多少条分析
3. **按日期查询** - 查找特定日期的分析记录
4. **按股票查询** - 查找特定股票的所有历史分析
5. **全文搜索** - 按关键词搜索（如"低空经济"、"卖出"等）

---

## 使用方式

### 方式1：直接运行脚本

```bash
# 查看最新3条（默认）
./skills/stock-log-viewer/stock-log.sh latest

# 查看最新5条
./skills/stock-log-viewer/stock-log.sh latest 5

# 统计总数
./skills/stock-log-viewer/stock-log.sh count

# 按日期查询
./skills/stock-log-viewer/stock-log.sh date 2026-02-18

# 按股票名称查询
./skills/stock-log-viewer/stock-log.sh stock 恒锋信息

# 按股票代码查询
./skills/stock-log-viewer/stock-log.sh stock 300605

# 全文搜索
./skills/stock-log-viewer/stock-log.sh search 低空经济

# 显示全部
./skills/stock-log-viewer/stock-log.sh all

# 显示帮助
./skills/stock-log-viewer/stock-log.sh help
```

### 方式2：通过我（郑大姐）查询

你可以直接对我说：
- "郑大姐，查看日记本"
- "郑大姐，查看最新5条分析"
- "郑大姐，查一下恒锋信息的历史分析"
- "郑大姐，2月18日分析了哪些股票"

---

## 命令速查表

| 命令 | 用法 | 示例 |
|------|------|------|
| `latest` | 查看最新n条 | `stock-log.sh latest 5` |
| `count` | 统计总数 | `stock-log.sh count` |
| `date` | 按日期查询 | `stock-log.sh date 2026-02-18` |
| `stock` | 按股票查询 | `stock-log.sh stock 300605` |
| `search` | 全文搜索 | `stock-log.sh search 低空经济` |
| `all` | 显示全部 | `stock-log.sh all` |
| `help` | 显示帮助 | `stock-log.sh help` |

---

## 输出示例

### 查看最新记录
```
📔 郑大姐股票分析日记本 - 最新3条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 恒锋信息 (300605) | 2026-02-18 00:20

**股价**：16.66元（+1.52%）
**趋势判断**：高位震荡，顶背离风险
**核心观点**：蹭AI概念炒作，Q1亏损收窄但全年预计仍亏
**关键价位**：支撑16元 / 压力17元
**操作建议**：卖出 - 跌破16元无条件清仓
**风险提示**：概念退潮、业绩亏损、股东减持
**数据截至**：2025年一季报
---
```

### 统计总数
```
📊 郑大姐日记本统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 日记本路径: /root/.openclaw/workspace/memory/stock-analysis-log.md
📝 分析记录数: 15 条
📄 总行数: 245 行
📅 最早记录: 2026-02-15
📅 最新记录: 2026-02-18

💡 提示: 使用 'stock-log.sh latest 5' 查看最新5条记录
```

---

## 日记本文件位置

```
/root/.openclaw/workspace/memory/stock-analysis-log.md
```

---

## 注意事项

1. **日记本自动生成** - 每次郑大姐完成股票分析后会自动追加记录
2. **首次使用** - 如果没有记录过任何分析，会提示"日记本文件不存在"
3. **数据安全** - 日记本保存在本地，不会上传到云端
4. **记录格式** - 统一使用Markdown格式，方便阅读和导出

---

## 郑大姐唠叨

"记性不好？没关系！每次分析完我都给你记着呢。涨了跌了，对了错了，翻出来看看，复盘才有进步！"

"别光看现在的涨跌，翻翻之前的分析，看看郑大姐我说对了没有。这叫什么？这叫验证！"
