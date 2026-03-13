---
name: video-script
description: Create video scripts and publishing materials for YouTubers/UP主. Use when user wants to prepare a video, write a script (口播稿), generate video title, description, tags, or chapter timestamps. Triggers on "写视频脚本", "视频口播稿", "video script", "prepare video", "视频发布素材", or mentions creating content for YouTube/Bilibili.
---

# Video Script & Publishing Materials

Help YouTubers/UP主 prepare video content: write structured scripts (口播稿), blog posts, and platform-specific publishing materials.

## Output Structure

Each video gets a date-based directory under user's chosen location:

```
./videos/{YYYY-MM-DD}-{short-slug}/
├── script.md       # 视频口播稿
├── blog.md         # 博客文章
├── youtube.md      # YouTube 发布素材
└── bilibili.md     # Bilibili 发布素材
```

## Interactive Workflow

### Step 1: Gather Information

**IMPORTANT**: Before writing anything, collect sufficient context from the user. Ask the user:

```
请提供以下信息，帮我为你准备视频内容：

1. **视频主题**：这期视频讲什么？（必填）
2. **目标平台**：YouTube / Bilibili / 两者都有？（默认：两者）
3. **目标时长**：大约几分钟？（默认：10分钟）
4. **目标观众**：面向什么人群？（如：开发者、AI爱好者、初学者）
5. **关键要点**：你希望视频覆盖哪些要点？（可以是大纲、笔记、或链接）
6. **相关资料**：有没有参考文章、文档、代码仓库？（可选，我可以帮你研究）
已有部分信息的话，直接告诉我就好，缺的我会追问。
```

If the user provides partial info upfront, only ask for the missing pieces.

### Step 2: Research (If Needed)

If the user provides reference URLs, docs, or repos:
- Use WebFetch to read reference articles/docs
- Use Read/Grep/Glob to explore code repos
- Use WebSearch to find supplementary information
- Summarize key points for script use

If the topic is about a specific technology/tool:
- Research its core features and selling points
- Find common pain points it solves
- Look for comparison angles with alternatives

### Step 3: Create Directory

Create the date-based directory:

```
./videos/{YYYY-MM-DD}-{short-slug}/
```

Example: `./videos/2026-03-07-react-server-components/`

The `short-slug` should be a brief, descriptive kebab-case label derived from the topic.

### Step 4: Write Script (script.md)

Write a structured 口播稿 in the user's preferred language. The script should be conversational and natural for speaking.

- See `templates/script.md` for the output format template
- See `references/script-guidelines.md` for detailed writing rules

### Step 5: Write Blog Post (blog.md)

Repurpose the video content into a blog post to maximize content utilization. The blog should NOT be a transcript - it should be a standalone article that reads naturally.

- See `templates/blog.md` for the output format template
- See `references/blog-guidelines.md` for detailed writing rules
- **IMPORTANT**: Follow the `personal-writing-style` skill conventions

### Step 6: Write Platform Descriptions (youtube.md & bilibili.md)

Generate separate publishing materials for each platform. The two platforms share the same core content but differ in structure and promo placement.

- See `templates/youtube.md` and `templates/bilibili.md` for output format templates
- See `references/platform-differences.md` for platform-specific rules and guidelines

### Step 7: Review & Iterate

完成后提示用户：

```
视频脚本和配套内容已准备好：

📂 {目录路径}/
├── script.md      — 口播稿（约 X 分钟）
├── blog.md        — 博客文章
├── youtube.md     — YouTube 发布素材
└── bilibili.md    — Bilibili 发布素材

请检查内容，如果需要调整，告诉我：
- 需要修改哪个部分？
- 风格/语气需要调整吗？
- 有要补充的要点吗？

提示：youtube.md 中的章节时间戳是估算值，请在剪辑完成后根据实际时长调整。
```

## Personal Promotion Info

Users should configure their promotion block. On first use, ask the user for their promotion links and save to **auto memory** for cross-session persistence.

When asking:

```
我注意到这是你第一次使用视频脚本 skill。请提供你的个人推广信息，我会记住以便后续使用：

- 社交媒体链接（Twitter、Bilibili、YouTube 等）
- 知识星球/社群链接
- 联系方式
- 其他固定推广信息（如课程链接、赞助信息等）
```

Save to auto memory directory as `video-promo.md` (e.g. `~/.claude/projects/.../memory/video-promo.md`). On subsequent uses, check if this file exists in the memory directory and read it directly — no need to ask again.

## Examples

See `references/examples.md` for detailed examples of different usage scenarios.

## Critical Rules

1. **先问后写** — 信息不足时必须追问，不要猜测用户意图
2. **口语化脚本** — 脚本是用来说的，不是用来读的
3. **时间戳是估算** — 明确提醒用户剪辑后需调整
4. **不要自动发布** — 只生成文件，不执行任何发布操作
5. **保留用户风格** — 如果用户提供了之前的视频风格参考，尽量保持一致
6. **推广信息复用** — 首次询问后保存到 auto memory，后续自动填充
7. **日期目录** — 每期视频按当天日期创建独立目录
