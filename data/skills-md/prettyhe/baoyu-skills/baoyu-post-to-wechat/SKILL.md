---
name: baoyu-post-to-wechat
description: Posts content to WeChat Official Account (微信公众号) via API or Chrome CDP. Supports article posting (文章) with HTML, markdown, or plain text input, and image-text posting (图文) with multiple images. Use when user mentions "发布公众号", "post to wechat", "微信公众号", or "图文/文章".
---

# Post to WeChat Official Account

## Language

**Match user's language**: Respond in the same language the user uses. If user writes in Chinese, respond in Chinese. If user writes in English, respond in English.

## Script Directory

**Agent Execution**: Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>.ts`.

| Script | Purpose |
|--------|---------|
| `scripts/wechat-browser.ts` | Image-text posts (图文) |
| `scripts/wechat-article.ts` | Article posting via browser (文章) |
| `scripts/wechat-api.ts` | Article posting via API (文章) |
| `scripts/generate-cover.ts` | Generate cover images (封面图生成) - No system dependencies |

## Preferences (EXTEND.md)

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-post-to-wechat/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md" && echo "user"
```

┌────────────────────────────────────────────────────────┬───────────────────┐
│                          Path                          │     Location      │
├────────────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-post-to-wechat/EXTEND.md           │ Project directory │
├────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md     │ User home         │
└────────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: Default theme | Default publishing method (api/browser) | Default author | Chrome profile path

## Image-Text Posting (图文)

For short posts with multiple images (up to 9):

```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./images/
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --title "标题" --content "内容" --image img.png --submit
```

See [references/image-text-posting.md](references/image-text-posting.md) for details.

## Article Posting Workflow (文章)

Copy this checklist and check off items as you complete them:

```
Publishing Progress:
- [ ] Step 0: Load preferences (EXTEND.md)
- [ ] Step 1: Determine input type
- [ ] Step 2: Check markdown-to-html skill
- [ ] Step 3: Convert to HTML
- [ ] Step 4: Validate metadata (title, summary)
- [ ] Step 5: Check and prepare cover image
- [ ] Step 6: Select method and configure credentials
- [ ] Step 7: Publish to WeChat
- [ ] Step 8: Report completion
```

### Step 0: Load Preferences

Check and load EXTEND.md settings (see Preferences section above).

### Step 1: Determine Input Type

| Input Type | Detection | Action |
|------------|-----------|--------|
| HTML file | Path ends with `.html`, file exists | Skip to Step 4 |
| Markdown file | Path ends with `.md`, file exists | Continue to Step 2 |
| Plain text | Not a file path, or file doesn't exist | Save to markdown, then Step 2 |

**Plain Text Handling**:

1. Generate slug from content (first 2-4 meaningful words, kebab-case)
2. Create directory and save file:

```bash
mkdir -p "$(pwd)/post-to-wechat/$(date +%Y-%m-%d)"
# Save content to: post-to-wechat/yyyy-MM-dd/[slug].md
```

3. Continue processing as markdown file

**Slug Examples**:
- "Understanding AI Models" → `understanding-ai-models`
- "人工智能的未来" → `ai-future` (translate to English for slug)

### Step 2: Check Markdown-to-HTML Skill

**Skip if**: Input is `.html` file

**Skill Discovery**:

```bash
# Check if baoyu-markdown-to-html exists
test -f skills/baoyu-markdown-to-html/SKILL.md && echo "found"
```

| Result | Action |
|--------|--------|
| Found | Read its SKILL.md, continue to Step 3 |
| Multiple skills | AskUserQuestion to choose |
| Not found | Show installation suggestion |

**When Not Found**:

```
No markdown-to-html skill found.

Suggested installation:
https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-markdown-to-html/SKILL.md

Options:
A) Cancel - install the skill first
B) Continue - provide HTML file manually
```

### Step 3: Convert Markdown to HTML

**Skip if**: Input is `.html` file

1. **Ask theme preference** (unless specified in EXTEND.md or CLI):

| Theme | Description |
|-------|-------------|
| `default` | 经典主题 - 传统排版，标题居中带底边，二级标题白字彩底 |
| `grace` | 优雅主题 - 文字阴影，圆角卡片，精致引用块 |
| `simple` | 简洁主题 - 现代极简风，不对称圆角，清爽留白 |

2. **Execute conversion** (using the discovered skill):

```bash
npx -y bun ${MD_TO_HTML_SKILL_DIR}/scripts/main.ts <markdown_file> --theme <theme>
```

3. **Parse JSON output** to get: `htmlPath`, `title`, `author`, `summary`, `contentImages`

### Step 4: Validate Metadata

Check extracted metadata from Step 3 (or HTML meta tags if direct HTML input).

| Field | If Missing |
|-------|------------|
| Title | Prompt: "Enter title, or press Enter to auto-generate from content" |
| Summary | Prompt: "Enter summary, or press Enter to auto-generate (recommended for SEO)" |

**Auto-Generation Logic**:
- **Title**: First H1/H2 heading, or first sentence
- **Summary**: First paragraph, truncated to 120 characters

### Step 5: Check and Prepare Cover Image

**CRITICAL**: WeChat Official Account requires a cover image for article (news) type posts.

**Check for existing cover image sources (in priority order)**:

1. CLI argument: `--cover <path>`
2. Frontmatter fields: `featureImage`, `coverImage`, `cover`, `image`
3. First image in HTML content (will be used if found)

**If NO cover image found**, use AskUserQuestion to prompt user with options:

```
Cover image required for WeChat article posting.

How would you like to provide a cover image?
```

Options to present:

| Option | Description |
|--------|-------------|
| Generate based on article content (Recommended) | Auto-generate a cover image using ImageMagick with article title and theme colors |
| Provide image path | Specify a local file path or URL to an existing image |
| Use first image from content | Extract and use the first image found in the article (if available) |
| Cancel | Stop publishing to add cover image manually |

**If user chooses "Generate based on article content"**:

1. **Check ImageMagick installation**:

```bash
which convert || which magick
```

2. **Choose generation method**:

**Method A: ImageMagick (Recommended if installed)**

If ImageMagick IS installed, use it directly:

```bash
# Extract article title and generate cover
convert -size 900x500 \
  -define gradient:angle=135 \
  gradient:'#667eea'-'#764ba2' \
  -gravity center \
  -font "DejaVu-Sans-Bold" \
  -pointsize 48 \
  -fill white \
  -annotate +0-30 '<Article Title Line 1>' \
  -pointsize 36 \
  -annotate +0+30 '<Article Title Line 2>' \
  <output_directory>/<article-basename>-cover.jpg
```

**Method B: Node.js Script (Fallback - No system dependencies required)**

If ImageMagick is NOT installed, use the npx fallback script:

```bash
# Generate cover using Node.js (works anywhere, no sudo needed)
npx -y bun ${SKILL_DIR}/scripts/generate-cover.ts \
  --title "<Article Title>" \
  --output <output_directory>/<article-basename>-cover.jpg \
  --gradient-start "#667eea" \
  --gradient-end "#764ba2"
```

**Fallback script features**:
- ✓ No system dependencies (ImageMagick) required
- ✓ Works on any platform with Node.js/Bun
- ✓ No sudo/admin privileges needed
- ✓ Supports multiple image libraries (tries @napi-rs/canvas → sharp → SVG fallback)
- ✓ Auto-wraps long titles
- ✓ Customizable colors and dimensions

**Library installation (optional, for better output)**:
```bash
# For PNG/JPEG output (choose one):
npm install @napi-rs/canvas  # Recommended - native performance
# OR
npm install sharp            # Alternative - pure Node.js
```

If neither library is installed, the script will generate an SVG file (which WeChat API also accepts).

3. Extract article title from HTML/markdown
4. Generate cover image using the chosen method:

```bash
# Example: Generate gradient background with title text
convert -size 900x500 \
  -define gradient:angle=135 \
  gradient:'#667eea'-'#764ba2' \
  -gravity center \
  -font "DejaVu-Sans-Bold" \
  -pointsize 48 \
  -fill white \
  -annotate +0-30 '<Article Title Line 1>' \
  -pointsize 36 \
  -annotate +0+30 '<Article Title Line 2>' \
  <output_directory>/cover-<slug>.jpg
```

4. Save to same directory as the article with naming pattern: `<article-basename>-cover.jpg`
5. Use this generated image as `--cover` parameter

**Image Requirements**:
- Format: JPEG, PNG, GIF, or WebP
- Recommended size: 900x500px or 2:1 aspect ratio
- File size: < 2MB

### Step 6: Select Publishing Method and Configure

**Ask publishing method** (unless specified in EXTEND.md or CLI):

| Method | Speed | Requirements |
|--------|-------|--------------|
| `api` (Recommended) | Fast | API credentials |
| `browser` | Slow | Chrome, login session |

**If API Selected - Check Credentials**:

```bash
# Check project-level
test -f .baoyu-skills/.env && grep -q "WECHAT_APP_ID" .baoyu-skills/.env && echo "project"

# Check user-level
test -f "$HOME/.baoyu-skills/.env" && grep -q "WECHAT_APP_ID" "$HOME/.baoyu-skills/.env" && echo "user"
```

**If Credentials Missing - Guide Setup**:

```
WeChat API credentials not found.

To obtain credentials:
1. Visit https://mp.weixin.qq.com
2. Go to: 开发 → 基本配置
3. Copy AppID and AppSecret

Where to save?
A) Project-level: .baoyu-skills/.env (this project only)
B) User-level: ~/.baoyu-skills/.env (all projects)
```

After location choice, prompt for values and write to `.env`:

```
WECHAT_APP_ID=<user_input>
WECHAT_APP_SECRET=<user_input>
```

### Step 6: Publish to WeChat

**API method**:

```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-api.ts <html_file> [--title <title>] [--summary <summary>] [--inline-css]
```

**CRITICAL: Style Preservation** (API method):

- **ALWAYS use `--inline-css` for HTML files with styling** (especially those with `<style>` tags)
- WeChat Official Account does NOT support `<style>` tags or external CSS
- Without `--inline-css`, all styles will be removed and the article will appear unstyled
- The `--inline-css` flag converts CSS rules to inline `style="..."` attributes
- **Recommended command for styled HTML**:
  ```bash
  npx -y bun ${SKILL_DIR}/scripts/wechat-api.ts <html_file> --cover <cover_image> --inline-css
  ```

**Image Handling** (API method):

- Automatically downloads remote images (HTTP/HTTPS URLs)
- **Auto-cleans metadata** for images containing AIGC/Coze markers (e.g., `AIGC{...}`)
- Retries with forced cleaning if upload fails due to "unsupported file type" errors
- Supports formats: JPEG, PNG, GIF, WebP

**Browser method**:

```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --html <html_file>
```

### Step 7: Completion Report

**For API method**, include draft management link:

```
WeChat Publishing Complete!

Input: [type] - [path]
Method: API
Theme: [theme name]

Article:
• Title: [title]
• Summary: [summary]
• Images: [N] inline images

Result:
✓ Draft saved to WeChat Official Account
• media_id: [media_id]

Next Steps:
→ Manage drafts: https://mp.weixin.qq.com (登录后进入「内容管理」→「草稿箱」)

Files created:
[• post-to-wechat/yyyy-MM-dd/slug.md (if plain text)]
[• slug.html (converted)]
```

**For Browser method**:

```
WeChat Publishing Complete!

Input: [type] - [path]
Method: Browser
Theme: [theme name]

Article:
• Title: [title]
• Summary: [summary]
• Images: [N] inline images

Result:
✓ Draft saved to WeChat Official Account

Files created:
[• post-to-wechat/yyyy-MM-dd/slug.md (if plain text)]
[• slug.html (converted)]
```

## Detailed References

| Topic | Reference |
|-------|-----------|
| Image-text parameters, auto-compression | [references/image-text-posting.md](references/image-text-posting.md) |
| Article themes, image handling | [references/article-posting.md](references/article-posting.md) |

## Feature Comparison

| Feature | Image-Text | Article (API) | Article (Browser) |
|---------|------------|---------------|-------------------|
| Plain text input | ✗ | ✓ | ✓ |
| HTML input | ✗ | ✓ | ✓ |
| Markdown input | Title/content | ✓ (via skill) | ✓ (via skill) |
| Multiple images | ✓ (up to 9) | ✓ (inline) | ✓ (inline) |
| Auto-clean image metadata | ✗ | ✓ (AIGC/Coze) | N/A |
| CSS inline conversion | ✗ | ✓ (--inline-css) | Auto |
| Auto-generate cover | ✗ | ✓ (2 methods) | ✓ |
| Cover generation methods | N/A | ImageMagick + Node.js | Manual |
| Themes | ✗ | ✓ | ✓ |
| Auto-generate metadata | ✗ | ✓ | ✓ |
| Requires Chrome | ✓ | ✗ | ✓ |
| Requires API credentials | ✗ | ✓ | ✗ |
| Requires system dependencies | ✗ | ✗ (npx fallback) | ✓ |
| Speed | Medium | Fast | Slow |

## Prerequisites

**For API method**:
- WeChat Official Account API credentials
- Guided setup in Step 5, or manually set in `.baoyu-skills/.env`

**For Browser method**:
- Google Chrome
- First run: log in to WeChat Official Account (session preserved)

**For Markdown conversion**:
- A markdown-to-html skill (e.g., `baoyu-markdown-to-html`)
- If not installed, the workflow will suggest installation

**Config File Locations** (priority order):
1. Environment variables
2. `<cwd>/.baoyu-skills/.env`
3. `~/.baoyu-skills/.env`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No markdown-to-html skill | Install `baoyu-markdown-to-html` from suggested URL |
| Missing API credentials | Follow guided setup in Step 6 |
| Missing cover image | Use auto-generation (ImageMagick or npx fallback) or provide image path |
| Cover generation failed | Try npx fallback: `npx -y bun ${SKILL_DIR}/scripts/generate-cover.ts --title "Title" --output cover.jpg` |
| Styles lost in WeChat | Add `--inline-css` flag to preserve HTML styles |
| Access token error | Check if API credentials are valid and not expired |
| Access token error 40164 (invalid ip) | Add current server IP to WeChat Official Account whitelist: mp.weixin.qq.com → 开发 → 基本配置 → IP白名单 |
| Not logged in (browser) | First run opens browser - scan QR to log in |
| Chrome not found | Set `WECHAT_BROWSER_CHROME_PATH` env var |
| Title/summary missing | Use auto-generation or provide manually |
| Paste fails | Check system clipboard permissions |
| Image upload 40113 (unsupported file type) | **Auto-resolved**: Script automatically cleans AIGC/Coze metadata. If persists, manually download and re-save image without metadata. |

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
