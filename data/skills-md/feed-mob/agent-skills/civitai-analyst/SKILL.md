name: civitai-analyst
description: "Generate and execute SQL queries against the civitai_records PostgreSQL database to analyze video performance on Civitai. Use when users ask about: video engagement metrics (likes, hearts, comments), content performance analysis, tag/theme analysis, quality scores, weekly reports, comparing videos, content recommendations, trend analysis, or any Civitai data queries. Triggers: Civitai, video stats, engagement, likes, hearts, comments, weekly report, tag analysis, quality score, content strategy, top performers, SQL query, video comparison, WoW analysis, 数据分析, 视频表现, 周报, 内容分析."
metadata: {"openclaw":{"requires":{"bins":["npx"],"env":["CIVITAI_RECORD_MCP_SERVER_TOKEN"]}}}
---

# Civitai Analyst

Analyze video performance data on Civitai through natural language queries. Generate SQL, execute against the database, and provide actionable insights.

## Capabilities

1. **SQL Generation** - Convert natural language to optimized PostgreSQL queries
2. **Query Execution** - Run queries via `query_civitai_db`
3. **Data Analysis** - Interpret engagement metrics and find patterns
4. **Content Insights** - Analyze tags, themes, quality scores from video_analysis
5. **Recommendations** - Suggest content strategies based on performance data
6. **Weekly Reports** - Generate JSON/HTML performance summaries

## mcporter Setup

1. Export the required token and point mcporter at this skill's config:

```bash
export CIVITAI_RECORD_MCP_SERVER_TOKEN="<token>"
export MCPORTER_CONFIG="${SKILL_DIR}/mcporter.json"
```

2. Optional validation commands:

```bash
test -f "${MCPORTER_CONFIG}"
npx mcporter list --config "${MCPORTER_CONFIG}"
npx mcporter list civitai_records --config "${MCPORTER_CONFIG}"
```

## Tool Usage

Execute SQL with mcporter so every query is auditable and consistently configured:

```
npx mcporter call civitai_records.query_civitai_db \
  --config "${MCPORTER_CONFIG}" --output json \
  sql="SELECT ..."
```

Rules:
1. Always include `--output json`
2. Pass SQL as a single string. For multi-line queries use `sql=$(cat <<'SQL' ... SQL)`
3. Surface mcporter errors directly—most rejections return JSON with details

**Error Handling:** If query is rejected, response contains:
```json
{
  "allowed": false,
  "reason": "...",
  "violation_type": "...",
  "suggestions": "..."
}
```

Fix the SQL based on the error and retry.

## Workflow

1. **Understand** - Parse user's question, identify metrics/filters needed
2. **Generate SQL** - Use schema.md for tables, query-index.md for templates
3. **Execute** - Run `npx mcporter call civitai_records.query_civitai_db` with validated SQL
4. **Analyze** - Interpret results, find patterns, compare data points
5. **Present** - Format with links, provide insights and recommendations

## Key Parameters

### civitai_account
- User-provided account identifier
- **Default fallback: `'c29'`** if not specified

### on_behalf_of
- User's first name, inferred from session context
- Used to filter assets/stats by uploader

### Date Ranges
- Use **calendar weeks** (Monday 00:00 to Sunday 23:59 UTC)
- Format: PostgreSQL timestamptz `'2025-01-06T00:00:00Z'`

**Date Calculations:**
- "This week" = Current Monday to next Monday
- "Last week" = Previous Monday to current Monday
- "Past 2 weeks" = Monday 2 weeks ago to next Monday

## Link Formatting

**Assets (videos/images):**
```
https://civitai.com/images/{assets.civitai_id}
```

**Posts:**
```
https://civitai.com/posts/{civitai_posts.civitai_id}
```

Always include clickable links in results for easy navigation.

## Analysis Guidelines

### Engagement Metrics
- **Positive engagement**: likes + hearts + laughs
- **Total engagement**: all reactions + comments
- **Engagement rate**: total_engagement / asset_count

### Pattern Recognition
- Compare top performers vs average
- Identify common tags in high-engagement videos
- Correlate quality_score with engagement
- Analyze motion_intensity impact

### Comparative Analysis
When comparing videos (e.g., "rank 2 vs rank 9"):
- Extract shared tags
- Compare quality scores
- Analyze description/prompt similarities
- Identify differentiating factors

## Recommendation Framework

Based on analysis, provide actionable suggestions:

1. **Content themes** - Which topics/tags drive engagement
2. **Quality factors** - Optimal quality_score ranges
3. **Timing patterns** - Best posting times if data shows trends
4. **Improvement areas** - Underperforming high-quality content

Example insights:
- "Anime + high-motion videos get 2x engagement"
- "Videos with quality_score > 0.85 need better tags for visibility"
- "Comments spike on 'cinematic' tagged content"

## Report Generation

For weekly reports, use templates from `references/report-templates.md`:

- **JSON format** - Structured data for programmatic use
- **HTML format** - Visual report with Tailwind CSS styling

Generate reports by:
1. Run weekly-feedback-stats.sql for summary
2. Run top-performing-assets.sql for highlights
3. Run tag-performance.sql for content insights
4. Combine into report template

## Language

**Respond in the same language as the user's query.**
- English query → English response
- Chinese query → Chinese response (中文提问 → 中文回答)

## Reference Files

| File | When to Read |
|------|--------------|
| `references/schema.md` | Understanding table structures, columns, relationships |
| `references/query-index.md` | Finding the right query template for user's request |
| `references/queries/*.sql` | Loading specific query when needed |
| `references/report-templates.md` | Generating weekly reports |
