---
name: novita-social-monitor
description: Social media intelligence monitoring for Novita. Use when systematically browsing X/Twitter accounts from personal following list (@Jax_Zhang_4R) to gather AI industry intelligence. Performs sequential account review with per-account record keeping (including original tweet links), followed by comprehensive summary. Always use @skills/twitterapi-cli for data retrieval.
---

# Novita Social Monitor

AI industry intelligence gathering through sequential X/Twitter account review.

## Output Language

**Default**: Chinese (中文) - All reports, summaries, and records should be in Chinese unless the user explicitly requests English.

## Commands

### Get Following List

```bash
twitterapi user following Jax_Zhang_4R --limit 200
```

**Response includes:** `id`, `screen_name`, `name`, `description`, `followers_count`, `verified` for each account. No additional API calls needed for account info.

### Fetch Tweets (Time-Filtered)

```bash
# Read last check time from state file
STATE_FILE="$HOME/.novita-monitor/state.json"
LAST_CHECK=$(cat "$STATE_FILE" | grep -o '"last_check": "[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "2026-01-01_00:00:00_UTC")

# Get current time
UNTIL=$(date -u +"%Y-%m-%d_%H:%M:%S_UTC")

# Fetch tweets from last check to now
twitterapi tweet search "from:<account> since:${LAST_CHECK} until:${UNTIL}" --limit 3 --compact

# Update state file with current time
echo "{\"last_check\": \"$UNTIL\"}" > "$STATE_FILE"
```

### Fallback (No Time Filter)

```bash
twitterapi user tweets <account> --limit 3 --compact
```

### Search Brand Mentions

```bash
twitterapi tweet search "@novita_labs" --limit 50 --compact
```

## Processing Workflow

For each account in the following list:

1. **按描述分类** - 使用 following 列表返回的 `description` 字段确定分类:
   - **LLM 竞争对手**: LLM 提供商、模型托管、推理 API
   - **GPU 竞争对手**: GPU 云、计算基础设施
   - **合作伙伴**: 集成合作伙伴、生态协作者
   - **生态领袖**: 主要平台 (OpenAI、Anthropic 等)
   - **中国开源**: 中国 AI 模型提供商
   - **AI KOL**: 行业思想领袖、研究人员
   - **未分类**: 一般 AI 行业相关性

   **注意**: `following` 命令已返回 `description`、`name`、`followers_count` 和 `verified` 状态 - 无需单独获取账户信息。

2. **获取推文** - 使用上述时间过滤命令

3. **按分类分析**:
   - 竞争对手: 产品发布、定价、合作
   - 合作伙伴: 集成更新
   - 生态: 平台变化
   - 检查互动: 100-500 (有趣)、500-2000 (值得关注)、2000+ (重要)

4. **立即记录** - **重要**: 在完成每个账户审查后立即保存结果到文件，然后再处理下一个账户。这确保:
   - 如果进程中断不会丢失数据
   - 可以进行增量汇总
   - 为将来提供审计追踪

## Record Format & File Storage

### Directory Structure

```
~/.novita-monitor/
├── <datetime>/                # Per-run directory (e.g., 2026-02-26_14-30)
│   ├── @<account>.md          # Individual account reviews
│   ├── brand-mentions.md      # @novita_labs brand mentions
│   └── summary.md             # End-of-run summary
└── state.json                 # Last check timestamp
```

**DateTime format:** `YYYY-MM-DD_HH-MM` (UTC)

Each execution creates a new directory based on the start time:
```bash
# Get current datetime for directory name
RUN_DATETIME=$(date -u +"%Y-%m-%d_%H-%M")
mkdir -p "$HOME/.novita-monitor/$RUN_DATETIME"
```

### Individual Account Record

**File:** `~/.novita-monitor/<datetime>/@<account>.md`

**Create immediately after reviewing each account.**

```markdown
# @<account> - <日期>

## 账户信息
- **分类**: [分类]
- **粉丝数**: [数量]
- **认证**: [是/否]

## 推文分析

### [摘要]
- **互动**: [点赞] 点赞, [转发] 转发
- **时间**: [时间戳]
- **链接**: https://x.com/<account>/status/<tweet_id>
- **相关性**: [为什么重要]
```

**每条推文必须包含原始链接。**

### Brand Mentions Record

**File:** `~/.novita-monitor/<datetime>/brand-mentions.md`

```markdown
# 品牌提及 - <日期时间>

## 概述
总提及数: [数量]

## 重要提及
### @<提及账户>
- **推文**: [摘要]
- **链接**: https://x.com/<account>/status/<tweet_id>
- **情感**: [正面/负面/中性]
- **需要行动**: [是/否]
```

### End-of-Run Summary

**File:** `~/.novita-monitor/<datetime>/summary.md`

```markdown
# 运行总结 - <日期时间>

## 已审查账户
总计: [数量]

## 按分类统计
- **LLM 竞争对手**: [数量] - [关键洞察]
- **GPU 竞争对手**: [数量] - [关键洞察]
- **合作伙伴**: [数量] - [关键洞察]
- **生态领袖**: [数量] - [关键洞察]
- **中国开源**: [数量] - [关键洞察]
- **AI KOL**: [数量] - [关键洞察]
- **未分类**: [数量]

## 重大动态
[需要关注的关键事件]

## 行动项
- [ ] [行动 1]
- [ ] [行动 2]
```

### Data Aggregation (Optional)

To aggregate data across multiple runs:

```bash
# Get all summaries from today
cat ~/.novita-monitor/2026-02-26_*/summary.md

# Get all records for a specific account across all runs
find ~/.novita-monitor -name "@github.md" -exec cat {} \;
```

## State File

Location: `~/.novita-monitor/state.json`

```json
{
  "last_check": "2026-02-26_14:50:00_UTC"
}
```

**Purpose**: Records last execution time. Each run reads this time as `since:` value, then updates to current time after fetching tweets.

**First run**: Create file manually or script will use default `2026-01-01_00:00:00_UTC`.

## Language Preference

**Default**: All reports are generated in Chinese (中文).

**English output**: If you explicitly request English reports, specify at the start of your request:
```
"请生成英文报告" or "Generate reports in English"
```

This applies to:
- Individual account records
- Brand mentions summaries
- End-of-run summaries
- All analysis and insights
