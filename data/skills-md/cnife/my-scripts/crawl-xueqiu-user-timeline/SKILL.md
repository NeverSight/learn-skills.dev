---
name: crawl-xueqiu-user-timeline
description: 抓取雪球用户的发言时间线，保存为 Markdown 文件
---

# crawl-xueqiu-user-timeline

抓取雪球用户的发言时间线，保存为 Markdown 文件。

## 前置准备

Base directory for this skill: `{base_dir}`

**调用时请将 `{base_dir}` 替换为实际路径**，例如：`/home/cnife/code/try-agent-browser-automation/.agents/skills/crawl-xueqiu-user-timeline`

确保 Chrome 处于 Debug 模式并安装 agent-browser：

```bash
sh {base_dir}/scripts/check-cdp.sh
sh {base_dir}/scripts/check-agent-browser.sh
```

## 使用方法

直接运行爬取脚本：

```bash
{base_dir}/scripts/crawl_xueqiu_user_timeline_api.py <雪球用户主页链接> [选项]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 雪球用户主页链接 | 必填 |
| `--days` | 爬取最近 N 天 | 3 |
| `--start-date` | 开始日期 (YYYY-MM-DD) | 3 天前 |
| `--end-date` | 结束日期 (YYYY-MM-DD) | 今天 |
| `-o, --output` | 输出文件名 | 自动生成 |

**注意**：`--days` 和 `--start-date` 参数互斥，不能同时使用。

### 示例

```bash
# 爬取最近 3 天（默认）
{base_dir}/scripts/crawl_xueqiu_user_timeline_api.py https://xueqiu.com/u/9493911686

# 爬取最近 7 天
{base_dir}/scripts/crawl_xueqiu_user_timeline_api.py https://xueqiu.com/u/9493911686 --days 7

# 爬取最近 30 天
{base_dir}/scripts/crawl_xueqiu_user_timeline_api.py https://xueqiu.com/u/9493911686 --days 30

# 指定日期范围
{base_dir}/scripts/crawl_xueqiu_user_timeline_api.py https://xueqiu.com/u/9493911686 --start-date 2026-01-01 --end-date 2026-03-05

# 指定输出文件名
{base_dir}/scripts/crawl_xueqiu_user_timeline_api.py https://xueqiu.com/u/9493911686 -o my_timeline.md
```

## 输出格式

生成 Markdown 文件，包含：
- 用户基本信息（UID、粉丝、关注、帖子数）
- 按时间排序的发言记录
- 每条发言包含：发布时间、内容、引用内容（如有）、互动数据、原文链接

## 注意事项

1. 需要先登录雪球账号
2. 如遇 Verification 验证页面，需手动完成验证后重新运行
3. 爬取过程中会自动处理分页和 md5__1038 令牌
4. 输出文件保存在当前工作目录

---

**是否需要进一步分析？**

爬取完成后，请询问用户：是否需要把雪球用户的发言总结分析一下？
