---
name: wewrite-wechat-ai-publishing
description: Full-pipeline AI skill for WeChat Official Account articles — hotspot fetching, topic selection, writing, SEO, image generation, formatting, and draft box publishing.
triggers:
  - "写一篇公众号文章"
  - "帮我写微信公众号"
  - "抓取热点写文章"
  - "发布文章到微信草稿箱"
  - "生成公众号封面图"
  - "分析SEO关键词"
  - "排版微信文章"
  - "用wewrite写文章"
---

# WeWrite — WeChat AI Publishing Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

WeWrite is a full-pipeline AI skill for producing WeChat Official Account (公众号) articles end-to-end: hotspot fetching → topic selection → writing → SEO → AI image generation → formatting → draft box publishing. It runs as a Claude Code skill (via `SKILL.md`) but every component also works standalone.

---

## Installation

### As a Claude Code Skill

```bash
# Clone the repo
git clone https://github.com/oaker-io/wewrite.git ~/.claude/skills/wewrite

# Or copy into an existing project
cp -r wewrite ~/.claude/skills/wewrite
```

### Python Dependencies

```bash
cd wewrite
pip install -r requirements.txt
```

### Configuration

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml`:

```yaml
wechat:
  appid: "${WECHAT_APPID}"         # WeChat Official Account App ID
  secret: "${WECHAT_SECRET}"       # WeChat Official Account Secret

image_gen:
  provider: "doubao"               # "doubao" or "openai"
  doubao_api_key: "${DOUBAO_API_KEY}"
  openai_api_key: "${OPENAI_API_KEY}"

output_dir: "./output"
```

Set environment variables instead of hardcoding secrets:

```bash
export WECHAT_APPID="wx1234567890abcdef"
export WECHAT_SECRET="your_secret_here"
export DOUBAO_API_KEY="your_doubao_key"
export OPENAI_API_KEY="sk-..."
```

---

## Triggering the Full Pipeline

Once installed as a Claude Code skill, simply say:

```
用 demo 的配置写一篇公众号文章
```

Claude will execute all steps automatically using `clients/demo/style.yaml` as the client profile.

You can also specify a client:

```
用 clients/tech-blog 的风格，围绕今日热点写一篇公众号文章，发布到草稿箱
```

---

## Pipeline Steps & Scripts

### 1. Fetch Hotspots

Scrapes real-time trending topics from Weibo, Toutiao, and Baidu.

```bash
python3 scripts/fetch_hotspots.py --limit 20
python3 scripts/fetch_hotspots.py --limit 10 --json   # JSON output
```

Output example:
```json
[
  {"rank": 1, "title": "DeepSeek R2 发布", "source": "weibo", "heat": 98200},
  {"rank": 2, "title": "A股科技板块大涨", "source": "baidu", "heat": 75300}
]
```

### 2. SEO Keyword Analysis

Queries Baidu and 360 search suggestions to score keywords.

```bash
python3 scripts/seo_keywords.py "AI大模型" "科技股"
python3 scripts/seo_keywords.py --json "ChatGPT" "人工智能"
```

Python usage:

```python
from scripts.seo_keywords import analyze_keywords

results = analyze_keywords(["AI大模型", "大语言模型", "GPT-5"])
for kw in results:
    print(f"{kw['keyword']}: score={kw['score']}, volume={kw['estimated_volume']}")
```

### 3. Topic Selection

Claude reads `references/topic-selection.md` and generates 10 candidate topics scored on:
- **热度** (trending heat)
- **契合度** (client fit)
- **差异化** (differentiation)

### 4. Framework & Writing

Claude reads `references/frameworks.md` (5 frameworks) and `references/writing-guide.md` (de-AI style rules), then writes the article adapted to the client's tone.

### 5. AI Image Generation

```bash
# Cover image (recommended 900×383)
python3 toolkit/image_gen.py \
  --prompt "科技感封面，蓝色光线，未来感" \
  --output output/cover.png \
  --size cover

# Inline content image
python3 toolkit/image_gen.py \
  --prompt "程序员在办公室工作，现代风格插画" \
  --output output/img1.png \
  --provider openai
```

Python usage:

```python
from toolkit.image_gen import generate_image

path = generate_image(
    prompt="AI机器人与人类握手，科技感插画",
    output_path="output/cover.png",
    size="cover",          # "cover" (900x383) or "content" (800x600)
    provider="doubao"      # "doubao" or "openai"
)
print(f"Generated: {path}")
```

### 6. Formatting — Markdown → WeChat HTML

WeChat requires inline styles. The converter handles this automatically.

```bash
# Preview in browser
python3 toolkit/cli.py preview article.md --theme professional-clean

# Available themes
python3 toolkit/cli.py themes
```

Python usage:

```python
from toolkit.converter import MarkdownConverter
from toolkit.theme import load_theme

theme = load_theme("tech-modern")
converter = MarkdownConverter(theme=theme)

with open("article.md") as f:
    markdown_content = f.read()

html = converter.convert(markdown_content)
# html is WeChat-ready with all inline styles
```

### 7. Publish to WeChat Draft Box

```bash
python3 toolkit/cli.py publish article.md \
  --cover output/cover.png \
  --title "2026年AI大模型最新进展" \
  --author "科技观察"
```

Python usage:

```python
from toolkit.publisher import WeChatPublisher
from toolkit.wechat_api import WeChatAPI

api = WeChatAPI(appid=os.environ["WECHAT_APPID"], secret=os.environ["WECHAT_SECRET"])
publisher = WeChatPublisher(api=api)

# Upload cover image first
media_id = api.upload_image("output/cover.png")

# Push to draft box
draft_id = publisher.create_draft(
    title="2026年AI大模型最新进展",
    content=html_content,          # inline-styled HTML from converter
    cover_media_id=media_id,
    author="科技观察",
    digest="本文盘点2026年大模型最新进展..."   # summary/excerpt
)
print(f"Draft created: {draft_id}")
```

### 8. Fetch Article Stats (回填数据)

```bash
python3 scripts/fetch_stats.py --article-id "your_article_id"
```

### 9. Learn from Manual Edits

```bash
python3 scripts/learn_edits.py \
  --original output/draft.md \
  --edited output/final.md \
  --client demo
```

Extracts style rules from diffs and appends them to the client's playbook.

---

## Client Configuration

Each client lives in `clients/{name}/style.yaml`:

```yaml
# clients/my-tech-blog/style.yaml
name: "我的科技博客"
industry: "科技/AI"
topics:
  - "人工智能"
  - "大模型应用"
  - "编程技术"
tone: "专业严谨，偶尔幽默，面向中级开发者"
theme: "tech-modern"
avoid:
  - "过度营销语言"
  - "绝对化表述"
wechat:
  appid: "${WECHAT_APPID}"
  secret: "${WECHAT_SECRET}"
```

Create a new client:

```bash
mkdir clients/my-client
cp clients/demo/style.yaml clients/my-client/style.yaml
# Edit style.yaml for your client
```

---

## Themes

| Theme | Style |
|---|---|
| `professional-clean` | Clean professional (default) |
| `tech-modern` | Tech-forward blue/purple gradient |
| `warm-editorial` | Warm editorial tones |
| `minimal` | Minimal black/white |

```bash
python3 toolkit/cli.py themes          # list all themes with previews
python3 toolkit/cli.py preview article.md --theme warm-editorial
```

Custom theme (YAML):

```yaml
# toolkit/themes/my-theme.yaml
name: my-theme
body:
  font-family: "'PingFang SC', sans-serif"
  font-size: "16px"
  color: "#333"
  line-height: "1.8"
h2:
  color: "#1a73e8"
  font-weight: "bold"
  border-left: "4px solid #1a73e8"
  padding-left: "10px"
blockquote:
  background: "#f0f4ff"
  border-left: "3px solid #4285f4"
  padding: "12px 16px"
  color: "#555"
```

---

## Full Pipeline — Python Orchestration

```python
import subprocess
import json
import os
from toolkit.converter import MarkdownConverter
from toolkit.theme import load_theme
from toolkit.publisher import WeChatPublisher
from toolkit.wechat_api import WeChatAPI
from toolkit.image_gen import generate_image

# 1. Fetch hotspots
result = subprocess.run(
    ["python3", "scripts/fetch_hotspots.py", "--limit", "20", "--json"],
    capture_output=True, text=True
)
hotspots = json.loads(result.stdout)

# 2. SEO analysis on top topics
from scripts.seo_keywords import analyze_keywords
top_titles = [h["title"] for h in hotspots[:5]]
seo_scores = analyze_keywords(top_titles)

# 3. (Claude selects topic, writes article — handled by SKILL.md)
# After Claude produces article.md:

# 4. Generate cover
cover_path = generate_image(
    prompt="科技感封面图，蓝色渐变，数字化未来",
    output_path="output/cover.png",
    size="cover",
    provider=os.environ.get("IMAGE_PROVIDER", "doubao")
)

# 5. Convert Markdown → WeChat HTML
theme = load_theme("tech-modern")
converter = MarkdownConverter(theme=theme)
with open("output/article.md") as f:
    html = converter.convert(f.read())

# 6. Publish to draft box
api = WeChatAPI(
    appid=os.environ["WECHAT_APPID"],
    secret=os.environ["WECHAT_SECRET"]
)
publisher = WeChatPublisher(api=api)
media_id = api.upload_image(cover_path)
draft_id = publisher.create_draft(
    title="选定标题",
    content=html,
    cover_media_id=media_id,
    author="作者名"
)
print(f"✅ Published draft: {draft_id}")
```

---

## References Claude Uses During Pipeline

These files are read automatically by Claude when executing the skill:

| File | Purpose |
|---|---|
| `references/topic-selection.md` | 10-topic scoring rules (heat × fit × differentiation) |
| `references/frameworks.md` | 5 article structure templates |
| `references/writing-guide.md` | Style rules, de-AI-ification techniques |
| `references/seo-rules.md` | WeChat SEO: title length, keyword density, tags |
| `references/visual-prompts.md` | Image generation prompt templates |
| `references/wechat-constraints.md` | WeChat HTML/CSS technical limits |
| `references/style-template.md` | Client style.yaml schema documentation |

---

## Troubleshooting

**WeChat API 40001 / invalid credential**
```bash
# Access token expires every 2 hours — the API wrapper auto-refreshes,
# but verify your appid/secret are correct:
python3 -c "
from toolkit.wechat_api import WeChatAPI
import os
api = WeChatAPI(os.environ['WECHAT_APPID'], os.environ['WECHAT_SECRET'])
print(api.get_access_token())
"
```

**Image generation fails**
```bash
# Test provider connectivity
python3 toolkit/image_gen.py \
  --prompt "测试图片" \
  --output /tmp/test.png \
  --provider doubao
# If doubao fails, switch to openai in config.yaml
```

**Markdown conversion missing styles**
```bash
# Verify theme loads correctly
python3 -c "from toolkit.theme import load_theme; print(load_theme('tech-modern'))"

# Preview output before publishing
python3 toolkit/cli.py preview article.md --theme tech-modern
# Opens browser with rendered HTML
```

**Hotspot fetch returns empty**
```bash
# Platforms occasionally change their APIs — run with verbose:
python3 scripts/fetch_hotspots.py --limit 5 --verbose
# Check which sources are failing; the script supports weibo/baidu/toutiao independently
```

**Article not appearing in draft box**
- Ensure the WeChat account has **服务号** or **订阅号** API access enabled
- Check that your IP is whitelisted in the WeChat MP platform settings
- Draft box (`草稿箱`) requires `draft.add` API permission

---

## Quick Reference

```bash
# Full standalone workflow
python3 scripts/fetch_hotspots.py --limit 20 --json > hotspots.json
python3 scripts/seo_keywords.py --json "关键词1" "关键词2"
python3 toolkit/image_gen.py --prompt "封面描述" --output cover.png --size cover
python3 toolkit/cli.py preview article.md --theme tech-modern
python3 toolkit/cli.py publish article.md --cover cover.png --title "标题"

# Build playbook from historical articles
python3 scripts/build_playbook.py --client demo

# Learn from edits
python3 scripts/learn_edits.py --original draft.md --edited final.md --client demo

# Fetch article performance data
python3 scripts/fetch_stats.py --article-id "msgid_here"
```
