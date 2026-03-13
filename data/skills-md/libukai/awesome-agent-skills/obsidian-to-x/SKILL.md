---
name: obsidian-to-x
description: 发布内容和文章到 X (Twitter)。支持常规推文(文字/图片/视频)和 X Articles(长文 Markdown)。使用真实 Chrome 浏览器绕过反机器人检测。当用户说"发推"、"发到 X"、"发到 twitter"、"分享到 X"、"分享到 twitter"、"发 tweet"、"同步到 X"、"发布到 X"、提到"X Articles"、想从 Obsidian 笔记发布长文内容、或需要转换 Obsidian Markdown 到 X 格式时使用。适用于所有 X/Twitter 发布任务。
---

# Post to X (Twitter)

Posts text, images, videos, and long-form articles to X via real Chrome browser (bypasses anti-bot detection).

## Default Behavior (No Additional Instructions)

When user invokes this skill without specifying what to publish (e.g., just says "发到 X" or uses slash command):

1. **Clean Chrome CDP processes first** (REQUIRED - prevents port conflicts):
   ```bash
   pkill -f "Chrome.*remote-debugging-port" 2>/dev/null; pkill -f "Chromium.*remote-debugging-port" 2>/dev/null; sleep 2
   ```

2. **Get current active file** from Obsidian workspace:
   ```bash
   jq -r '.lastOpenFiles[0]' .obsidian/workspace.json
   ```

3. **Read the file content** using Read tool

4. **Auto-detect publishing type**:
   - Check if file has frontmatter with `title:`, `标题:`, or `Title:` field
   - **Has title in frontmatter** → Publish as **X Article** (long-form)
   - **No frontmatter or no title** → Publish as **Regular Post** (short-form)

5. **Inform user** of detected type and proceed with publishing

6. **Execute appropriate workflow**:
   - For X Article: Convert with `obsidian-to-article.ts` → Publish with `x-article.ts`
   - For Regular Post: Convert with `obsidian-to-post.ts` → Publish with `x-post.ts`

7. **Success Detection**: When running publishing scripts in background, check output for success markers:
   - **Best method**: Count `Image upload verified` occurrences matching expected image count
   - **Alternative**: Look for `Post composed (preview mode)` or `Browser remains open`
   - **For X Articles**: Look for `Article composed` or `Browser remains open`
   - Use short timeout (10-15s) with `block=false`, then check output content
   - Report success immediately when markers detected, don't wait for task completion
   - Example: 3 images → wait for 3x `Image upload verified` + text typing completion

**Example**:
```
User: "发到 X"
AI: ✓ Detected current file: Articles/news/my-article.md
    ✓ Found frontmatter with title → Publishing as X Article
    [proceeds with article publishing workflow]
```

## Content Types

**X Articles vs Regular Posts**:

| Feature | X Articles | Regular Posts |
|---------|-----------|---------------|
| Content | Rich text (Markdown) | Plain text only |
| Formatting | ✅ Bold, italic, headers, lists | ❌ All stripped |
| Code blocks | ✅ Syntax highlighting | ❌ Not supported |
| Images | ✅ Multiple images | ✅ Max 4 images |
| Length | Long-form (unlimited) | Short (280 chars) |
| Requirements | X Premium | Free |
| Script | `x-article.ts` | `x-post.ts` |
| Conversion | `obsidian-to-x.ts` | `extract-post-content.ts` |

**When to use**:
- **X Articles**: Blog posts, tutorials, technical articles with code
- **Regular Posts**: Quick updates, announcements, simple text + images

**AI Auto-Detection (for Obsidian files)**:

When user requests to publish the currently active Obsidian file without specifying the type:

1. **Read the file content** using Read tool
2. **Check for frontmatter** (YAML block between `---` markers at the start)
3. **Auto-select publishing type**:
   - **Has frontmatter with title field** (`title:`, `标题:`, or `Title:`) → Publish as **X Article**
   - **No frontmatter or no title field** → Publish as **Regular Post**
4. **Inform the user** of the detected type before publishing

**IMPORTANT**:
- **ONLY use frontmatter presence to determine publishing type**
- **DO NOT consider content length, word count, or any other factors**
- Even if content is very long (800+ words), if there's no frontmatter with title → publish as Regular Post
- Even if content is very short, if there's frontmatter with title → publish as X Article
- Strictly follow the frontmatter rule without exceptions

**Example decision logic**:
```
File with frontmatter:
---
title: My Technical Article
---
Content here...
→ Detected: X Article (has title in frontmatter)

File without frontmatter:
Just some quick thoughts to share...
→ Detected: Regular Post (no frontmatter)
```

## Quick Start

For Obsidian users who want to publish the currently active article:

```bash
bash ${SKILL_DIR}/scripts/publish-active.sh
```

This automatically:
1. Detects the active file (via workspace.json or Obsidian CLI)
2. Converts Obsidian syntax to X format
3. Opens X Articles editor with content filled in

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path
4. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun

**Script Reference**:
| Script | Purpose |
|--------|---------|
| **Publishing Scripts** | |
| `scripts/x-post.ts` | Publish regular posts (text + images, max 4) |
| `scripts/x-video.ts` | Publish video posts (text + video) |
| `scripts/x-quote.ts` | Publish quote tweet with comment |
| `scripts/x-article.ts` | Publish X Articles (rich text + images + code) |
| **Conversion Scripts** | |
| `scripts/obsidian-to-post.ts` | Convert Obsidian Markdown → plain text + images (for Posts) |
| `scripts/obsidian-to-article.ts` | Convert Obsidian Markdown → X Articles format (for Articles) |
| **Utilities** | |
| `scripts/publish-active.sh` | One-command publish for active Obsidian file |

## Prerequisites

- Google Chrome or Chromium
- `bun` runtime
- First run: log in to X manually (session saved)
- For Obsidian integration: `jq` tool (`brew install jq` on macOS)

## Pre-flight Check (Optional)

Before first use, suggest running the environment check:

```bash
${BUN_X} ${SKILL_DIR}/scripts/check-paste-permissions.ts
```

Checks: Chrome, Bun, Accessibility permissions, clipboard, paste keystroke.

**If any check fails**, provide fix guidance per item:

| Check | Fix |
|-------|-----|
| Chrome | Install Chrome or set `X_BROWSER_CHROME_PATH` env var |
| Bun runtime | `brew install oven-sh/bun/bun` (macOS) or `npm install -g bun` |
| Accessibility (macOS) | System Settings → Privacy & Security → Accessibility → enable terminal app |
| Paste keystroke (Linux) | Install `xdotool` (X11) or `ydotool` (Wayland) |

## Obsidian Integration

For Obsidian users, this skill can automatically detect the currently active file and convert Obsidian-specific syntax.

**Quick workflow**:
```bash
# One-command publish
bash ${SKILL_DIR}/scripts/publish-active.sh
```

**Manual workflow**:
```bash
# Step 1: Get active file (workspace.json method, 39x faster)
ACTIVE_FILE=$(jq -r '.lastOpenFiles[0]' .obsidian/workspace.json)

# Step 2: Convert Obsidian syntax
bun ${SKILL_DIR}/scripts/obsidian-to-article.ts "$ACTIVE_FILE" "Temp/converted.md"

# Step 3: Publish
bun ${SKILL_DIR}/scripts/x-article.ts "Temp/converted.md"
```

**For detailed Obsidian integration**, see `references/obsidian-integration.md`:
- How to detect active file (workspace.json vs CLI)
- Performance comparison (0.007s vs 0.274s)
- Error handling and fallback strategies

**For Obsidian syntax conversion**, see `references/obsidian-conversion.md`:
- Converting `![[]]` image syntax
- Handling Chinese frontmatter fields
- Manual conversion commands

---

## Regular Posts

Text + up to 4 images. **Plain text only** (all Markdown formatting stripped).

### From Obsidian Markdown

**Step 1: Clean Chrome CDP processes first** (REQUIRED - prevents port conflicts)

```bash
pkill -f "Chrome.*remote-debugging-port" 2>/dev/null; pkill -f "Chromium.*remote-debugging-port" 2>/dev/null; sleep 2
```

**Step 2: Convert Markdown to plain text + images**

```bash
# Extract content from Markdown file
# Supports both standard Markdown ![](path) and Obsidian ![[path]] image syntax
bun ${SKILL_DIR}/scripts/obsidian-to-post.ts "Articles/my-post.md" > /tmp/post-content.json
TEXT=$(jq -r '.text' /tmp/post-content.json)
IMAGES=$(jq -r '.images[]' /tmp/post-content.json)
```

**Image Syntax Support**:
- ✅ Standard Markdown: `![alt](path/to/image.png)`
- ✅ Obsidian syntax: `![[path/to/image.png]]`
- ✅ Network URLs: `![alt](https://example.com/image.jpg)` or `![[https://example.com/image.jpg]]`
- Local paths are converted to absolute paths
- Network images are automatically downloaded in parallel (3-4x faster than sequential)

**Step 3: Publish post**

```bash
${BUN_X} ${SKILL_DIR}/scripts/x-post.ts "$TEXT" --image "$IMAGES"
```

### Direct Usage

```bash
${BUN_X} ${SKILL_DIR}/scripts/x-post.ts "Hello!" --image ./photo.png
```

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `<text>` | Post content (plain text, positional) |
| `--image <path>` | Image file (repeatable, max 4) |
| `--profile <dir>` | Custom Chrome profile |

**Content Processing**:
- ✅ Plain text (all formatting stripped)
- ✅ Images (max 4)
- ❌ No rich text formatting
- ❌ No code blocks
- ❌ No HTML

**Browser Behavior**:
- Script opens browser with content filled in
- Browser **remains open** for manual review
- User can review, edit, and publish at their own pace
- User manually closes browser when done
- Add `--submit` flag to auto-publish (closes after 2 seconds)

**AI Success Detection** (for background execution):
- Don't wait for task completion (browser stays open indefinitely)
- **Best method**: Count `Image upload verified` in output matching expected image count
- **Alternative**: Check for `Post composed (preview mode)` or `Browser remains open`
- Use short timeout (10-15s) then check output content
- Report success immediately when markers detected
- Example workflow:
  ```
  1. Know you're uploading 3 images
  2. Wait 10-15s for uploads
  3. Check output: grep "Image upload verified" | wc -l
  4. If count == 3 → Report success immediately
  ```

---

## Video Posts

Text + video file.

**Step 1: Clean Chrome CDP processes** (REQUIRED)

```bash
pkill -f "Chrome.*remote-debugging-port" 2>/dev/null; pkill -f "Chromium.*remote-debugging-port" 2>/dev/null; sleep 2
```

**Step 2: Publish video post**

```bash
${BUN_X} ${SKILL_DIR}/scripts/x-video.ts "Check this out!" --video ./clip.mp4
```

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `<text>` | Post content (positional) |
| `--video <path>` | Video file (MP4, MOV, WebM) |
| `--profile <dir>` | Custom Chrome profile |

**Limits**: Regular 140s max, Premium 60min. Processing: 30-60s.

---

## Quote Tweets

Quote an existing tweet with comment.

**Step 1: Clean Chrome CDP processes** (REQUIRED)

```bash
pkill -f "Chrome.*remote-debugging-port" 2>/dev/null; pkill -f "Chromium.*remote-debugging-port" 2>/dev/null; sleep 2
```

**Step 2: Publish quote tweet**

```bash
${BUN_X} ${SKILL_DIR}/scripts/x-quote.ts https://x.com/user/status/123 "Great insight!"
```

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `<tweet-url>` | URL to quote (positional) |
| `<comment>` | Comment text (positional, optional) |
| `--profile <dir>` | Custom Chrome profile |

---

## X Articles

Long-form Markdown articles (requires X Premium).

**Step 1: Clean Chrome CDP processes** (REQUIRED)

```bash
pkill -f "Chrome.*remote-debugging-port" 2>/dev/null; pkill -f "Chromium.*remote-debugging-port" 2>/dev/null; sleep 2
```

This prevents "Chrome debug port not ready" errors. **Always run this first, automatically, without asking the user.**

**Step 2: Publish article**

```bash
${BUN_X} ${SKILL_DIR}/scripts/x-article.ts article.md
${BUN_X} ${SKILL_DIR}/scripts/x-article.ts article.md --cover ./cover.jpg
```

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `<markdown>` | Markdown file (positional) |
| `--cover <path>` | Cover image |
| `--title <text>` | Override title |

**Frontmatter**: `title`, `cover_image` supported in YAML front matter.

**Note**: Script opens browser with article filled in. User reviews and publishes manually.

### Code Blocks Support

Code blocks are automatically extracted from Markdown and inserted into X Articles editor. Supports all languages (JavaScript, Python, TypeScript, Rust, Go, Shell, etc.). No manual action required.

---

## Troubleshooting

**Common issues**:
- Chrome debug port not ready → Always clean CDP processes first (see above)
- macOS Accessibility Permission Error → Enable in System Settings
- Code blocks not inserting → Automatic, check console for errors

**For detailed troubleshooting**, see `references/troubleshooting.md`.

---

## References

- `references/obsidian-integration.md` - Obsidian file detection and integration
- `references/obsidian-conversion.md` - Converting Obsidian syntax to standard Markdown
- `references/regular-posts.md` - Regular posts workflow and troubleshooting
- `references/articles.md` - X Articles detailed guide
- `references/troubleshooting.md` - Common issues and solutions

## Extension Support

Custom configurations via EXTEND.md. Check these paths (priority order):
- `.libukai-skills/obsidian-to-x/EXTEND.md` (project directory)
- `$HOME/.libukai-skills/obsidian-to-x/EXTEND.md` (user home)

**EXTEND.md Supports**: Default Chrome profile

## Notes

- First run: manual login required (session persists)
- All scripts fill content into the browser and keep it open for manual review
- Browser remains open until user manually closes it (except when using `--submit` flag)
- Cross-platform: macOS, Linux, Windows
