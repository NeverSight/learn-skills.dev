---
name: share-reading
description: Draft social media posts to share valuable readings, articles, or resources. Use when user wants to share a link, article, or reading on social media (X/Twitter, Substack, 知识星球), or mentions "分享这篇文章", "share this article", "write a post about this", "推荐一下这个", or provides a URL and asks to write sharing content.
---

# Share Reading

Help draft social media posts for sharing valuable readings, articles, tools, or resources. Generates multiple candidate posts with appropriate tone and style, ready for publishing on X, Substack, or 知识星球.

## Workflow

### Step 1: Process Input

Determine the input type and extract content accordingly:

**If input is a URL:**
- Use WebFetch to retrieve the page content
- Extract: title, author, key points, publication date
- Preserve the original URL for inclusion in the post

**If input is a file path:**
- Use Read to load the file
- Extract the same metadata from frontmatter or content

**If input is direct text/notes:**
- Use the provided content as-is
- Ask for the source URL if not included

### Step 2: Understand Context

Before writing, consider:
- What makes this worth sharing? (insight, practical value, novelty, controversy)
- Who would care about this? (developers, AI enthusiasts, general tech audience)
- What's the user's likely angle? (recommendation, commentary, discussion)

If the intent is unclear, ask briefly:

```
这篇内容你想从什么角度分享？比如：
- 推荐给大家（觉得很有价值）
- 分享某个观点/发现
- 提出讨论/问题
- 其他想法？
```

### Step 3: Generate Candidates

Produce 2-3 candidate posts with varying approaches. Each candidate should:

1. **Include the source link** — always present, naturally placed
2. **Be self-contained** — readers should understand the value without clicking
3. **Match the platform tone** — see Platform Guidelines below

#### Candidate Approaches (pick 2-3 that fit)

- **Summary + takeaway**: Concise summary with a personal takeaway or opinion
- **Key highlight**: Pull out the most striking point or quote, add brief context
- **Question/discussion**: Frame a question around the content to spark engagement
- **Practical angle**: Focus on actionable value — "if you're doing X, read this because Y"
- **Contrarian/fresh take**: Offer a perspective the article didn't cover

### Step 4: Present to User

Present candidates clearly labeled, e.g.:

```
## 候选 1：总结推荐型

{content}

## 候选 2：观点提炼型

{content}

## 候选 3：讨论引导型

{content}
```

Ask user to pick one, or mix elements from multiple candidates.

## Platform Guidelines

### X (Twitter)

- Keep main post concise (under 280 chars for single tweet, or use thread format)
- Front-load the hook — first line matters most
- Use line breaks for readability
- Hashtags: 1-3 relevant ones, placed at the end or naturally inline
- Link can be in the main tweet or a reply

### Substack Notes / 知识星球

- Can be longer and more conversational
- Add more personal commentary and context
- Structure with short paragraphs
- OK to include bullet points for key takeaways

### General Style

- Write in the same language as the source content (Chinese article → Chinese post, English → English)
- If the user has a personal-writing-style skill, follow those preferences
- Avoid hype words ("revolutionary", "game-changing") — be genuine
- Be specific rather than vague ("reduces build time by 40%" > "makes things faster")

## Examples

### Example 1: User shares a link

**User**: 分享一下这个 https://example.com/article-about-rust-in-linux

**Claude**: Fetches the page, reads the content, generates candidates:

**候选 1：总结推荐型**

Rust 正式进入 Linux 6.12 内核的网络子系统。这意味着内核中最关键、也最容易出内存安全问题的模块，开始用 Rust 重写了。

文章详细讲了迁移策略：不是一刀切，而是新模块用 Rust 写，老代码逐步替换。最实际的一点 - 已经在生产环境跑了 3 个月，零内存安全 bug。

https://example.com/article-about-rust-in-linux

**候选 2：观点提炼型**

"我们不是要用 Rust 重写 Linux，而是让新代码不再产生旧问题。"

Linux 网络子系统开始引入 Rust，最值得关注的不是语言之争，而是他们的渐进式迁移策略 - 这对所有大型 C 项目都有参考价值。

https://example.com/article-about-rust-in-linux

**候选 3：讨论引导型**

Linux 内核的网络子系统开始用 Rust 了。跑了 3 个月，零内存安全 bug。

但评论区有个好问题：Rust 的编译时间和学习曲线，对内核贡献者社区的影响会有多大？快速迭代和安全保障之间，怎么平衡？

https://example.com/article-about-rust-in-linux

### Example 2: User shares with a specific angle

**User**: share this, really interesting approach to prompt engineering https://example.com/prompt-patterns

**Claude**: Fetches the page, generates candidates focused on the user's angle (interesting approach):

**Candidate 1: Highlight**

This is the clearest framework I've seen for systematic prompt engineering. Instead of trial-and-error, the author breaks it down into 5 composable patterns you can mix and match.

The "constraint layering" pattern alone is worth the read — it's how they got GPT-4 to consistently output valid JSON without schema enforcement.

https://example.com/prompt-patterns

**Candidate 2: Practical**

If you're writing prompts for production (not just ChatGPT conversations), this is worth 10 minutes of your time.

Key insight: treat prompts like function signatures — define inputs, expected output shape, and edge case handling upfront. The author shares 5 patterns with before/after examples.

https://example.com/prompt-patterns

### Example 3: User provides notes directly

**User**: 帮我写个分享帖，关于我今天试用了 Cursor 的新 Background Agent 功能，感觉很惊艳，可以后台自动完成任务

**Claude**: No URL to fetch, works with the provided notes, asks:

```
要附上 Cursor 官方的介绍链接吗？或者你有截图/录屏想一起分享？
```

Then generates candidates based on the user's first-hand experience.

## Critical Rules

1. **Always include the source link** — never omit it
2. **Don't fabricate content** — only reference what's actually in the article
3. **Match source language** — Chinese content gets Chinese posts, English gets English
4. **Multiple candidates** — always offer 2-3 options, not just one
5. **No auto-publishing** — only generate text, don't execute any publishing
6. **Genuine tone** — avoid marketing speak and excessive superlatives
