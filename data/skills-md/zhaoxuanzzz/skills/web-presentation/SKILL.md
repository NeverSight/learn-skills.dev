---
name: web-presentation
description: Create modern, interactive web presentations powered by Reveal.js. Supports both single-file HTML presentations AND multi-presentation repository management with GitHub Pages deployment. Use for creating slides, presentations, slide decks, presentation repositories with auto-generated index pages. Features advanced animations, speaker notes, overview mode, and full Reveal.js API access.
license: Complete terms in LICENSE.txt
---

⚠️ **READ THIS ENTIRE FILE BEFORE CREATING A WEB PRESENTATION** ⚠️

# Web Presentation Skill

Create elegant, interactive presentations powered by **Reveal.js**. Supports **two modes**:
1. **Single-file mode**: Self-contained HTML presentations for quick sharing
2. **Repository mode**: Multi-presentation management system with GitHub Pages deployment and auto-generated index

Perfect for product launches, technical talks, educational content, and building a complete presentation portfolio.

## Overview

This skill supports two distinct modes:

### Mode 1: Single Presentation (Quick & Simple)
Creates self-contained HTML presentations with:
- **🎬 Advanced animations** - Fragment animations, auto-animate, parallax effects
- **🎤 Speaker notes** - Dedicated speaker view with notes and timer (press S)
- **🔍 Overview mode** - Bird's-eye view of all slides (press ESC)
- **🎨 Professional transitions** - Multiple transition effects (slide/fade/zoom/convex/concave)
- **📐 Multiple layouts** - Title, content, two-column, image+text, quotes, sections
- **🎯 Vertical navigation** - Nested slides for hierarchical content
- **⌨️ Keyboard shortcuts** - Full keyboard control including fullscreen mode
- **📊 Progress tracking** - Visual progress bar and slide counter
- **📱 Responsive design** - Automatic scaling to fit any screen size (desktop, tablet, mobile)
- **🔌 Plugin ecosystem** - Markdown, code highlighting, math equations, search
- **🚀 Single-file output** - Everything via CDN, no build process required
- **🛠️ Full API access** - Complete Reveal.js API for advanced customization

### Responsive Design Features

✨ **Smart Screen Adaptation**
- **Automatic scaling** - Presentations automatically scale to fill available screen space while maintaining proper aspect ratio
- **Viewport optimization** - Dynamic sizing based on window dimensions (16:9 aspect ratio)
- **Mobile-friendly** - Optimal font sizes and layouts for devices of all sizes
- **Margin management** - Configurable margins to ensure content stays readable on any screen
- **Window resize handling** - Presentations reflow automatically when browser is resized

🎯 **Configuration Options**
- `minScale` / `maxScale` - Control minimum (20%) and maximum (200%) scaling ranges
- `margin` - Set presentation margins (default 5%) to ensure breathing room
- `width` / `height` - Use 100% to fill available space with responsive sizing

### Mode 2: Presentation Repository (Professional & Scalable)
Manages multiple presentations with:
- **📁 Organized structure** - Each presentation in its own folder with metadata
- **🖼️ Auto-generated index** - Beautiful gallery page showing all presentations
- **🏷️ Metadata system** - JSON metadata files for each presentation (title, author, date, tags, etc.)
- **🌐 GitHub Pages ready** - One-command deployment to GitHub Pages
- **📸 Thumbnail support** - Visual previews for each presentation
- **🔍 Searchable & filterable** - Index page with tags and categories
- **🛠️ Build scripts** - Automated index generation via Node.js
- **📦 Template system** - Quick creation of new presentations from templates

## When to Use Each Mode

**Single Presentation Mode - Use for:**
✅ Quick one-off presentations
✅ Sharing a single deck via email or chat
✅ Embedding in documents or websites
✅ Claude.ai artifacts
✅ No-setup requirements

**Repository Mode - Use for:**
✅ Managing multiple presentations
✅ Building a presentation portfolio
✅ Team/organization presentation library
✅ GitHub Pages publication
✅ Categorized presentation collections
✅ Professional presentation website

## Common Use Cases

**Use this skill for:**
✅ Product presentations and pitches
✅ Conference talks and tech presentations
✅ Educational slideshows and lectures
✅ Company all-hands or team updates
✅ Portfolio showcases
✅ Workshop materials
✅ Documentation walkthroughs
✅ Presentation portfolio websites
✅ Team presentation libraries

**Don't use for:**
❌ Static documents (use docx skill instead)
❌ Printable handouts (use pdf skill instead)
❌ Spreadsheet data (use xlsx skill instead)
❌ Rich media editing (needs external tools)

---

## Repository Structure (Repository Mode)

When using repository mode, the following structure is created:

```
presentation-repo/
├── index.html                    # Auto-generated index page (DO NOT EDIT)
├── .nojekyll                     # GitHub Pages config
├── package.json                  # Project configuration
├── package-lock.json             # Dependencies lock file
├── presentations/                # All presentations directory
│   ├── my-first-presentation/    # Individual presentation folder
│   │   ├── index.html           # Presentation HTML file
│   │   ├── metadata.json        # Presentation metadata
│   │   └── thumbnail.png        # Presentation thumbnail (800x600)
│   └── another-presentation/
│       ├── index.html
│       ├── metadata.json
│       └── thumbnail.png
├── templates/                    # Template files
│   ├── presentation-template.html   # Presentation template
│   ├── metadata-template.json       # Metadata template
│   └── index-template.html          # Index page template
├── scripts/                      # Build scripts
│   └── generate-index.js        # Index generation script
├── assets/                       # Shared resources
│   └── css/
│       └── custom.css           # Custom global styles
└── README.md                     # Repository documentation
```

### Metadata JSON Schema

Each presentation has a `metadata.json` file:

```json
{
  "id": "my-presentation",              // Unique identifier
  "title": "My Awesome Presentation",   // Display title
  "description": "A brief description", // Short description
  "author": "Author Name",              // Author name
  "date": "2026-02-10",                // Date (YYYY-MM-DD)
  "tags": ["tech", "tutorial"],        // Tags array
  "thumbnail": "thumbnail.png",         // Thumbnail filename
  "slides": 15,                         // Number of slides
  "language": "zh-CN",                  // Language code
  "category": "Tutorial"                // Category
}
```

---

## Workflow

🎯 **CRITICAL:** First determine which mode the user needs, then follow the appropriate workflow.

### Decision: Which Mode?

**Ask the user:**
```
您需要创建什么类型的演示文稿项目？

1. **单个演示文稿** - 创建一个独立的HTML文件
   - 适合：快速分享、一次性演讲、嵌入文档
   
2. **演示文稿仓库** - 创建一个完整的演示文稿管理系统
   - 适合：多个演示文稿、团队库、GitHub Pages发布、演示文稿作品集

请选择：[1] 单个演示文稿  [2] 演示文稿仓库
```

---

## Workflow A: Single Presentation Mode

This workflow uses an **interactive, question-guided approach**. Always ask questions to understand the user's needs before generating any code.

### Step 1: Initial Discovery (Ask Questions)

**ALWAYS start by asking these questions to the user:**

```
让我为您创建一个精彩的演示文稿！首先，我需要了解一些信息：

📌 **内容方面：**
1. 演示文稿的主题是什么？
2. 目标受众是谁？（客户、团队、学生、投资人？）
3. 核心信息是什么？（3-5个主要观点）
4. 预计需要多少张幻灯片？（快速演讲5-10张 / 标准演示15-25张 / 长篇讲座30+张）

🎨 **视觉风格：**
5. 您偏好什么视觉风格？
   - □ 专业商务（深色、简约）
   - □ 创意活泼（彩色、动感）
   - □ 极简主义（留白、聚焦）
   - □ 技术感（代码、图表）
   
6. 是否有品牌颜色要求？（如果有，请提供色值）

✨ **动画效果：**
7. 您需要什么程度的动画效果？
   - □ 基础（简单淡入淡出）
   - □ 中等（逐步显示要点）
   - □ 高级（元素变换、数据可视化动画）

🎤 **特殊功能：**
8. 是否需要以下功能？
   - □ 演讲者备注（用于演讲提示）
   - □ 代码高亮显示
   - □ 数学公式支持
   - □ 垂直嵌套幻灯片（章节内子主题）
```

**Wait for user responses before proceeding to Step 2.**

### Step 2: Content Planning (Collaborative Structure)

Based on user's answers, **propose a slide structure** and ask for confirmation:

```
根据您的需求，我建议以下结构：

📋 **建议的幻灯片结构：**

1. 标题页 - [主题]
2. 议程 - 本次演示的内容概览
3. 【第一部分】章节分隔符 - [第一个主要话题]
   ├─ 4. [子主题1]
   ├─ 5. [子主题2]
   └─ 6. [子主题3]
4. 【第二部分】章节分隔符 - [第二个主要话题]
   ├─ 7. [子主题1]
   └─ 8. [子主题2]
5. 总结 - 核心要点回顾
6. 结束页 - 致谢与问答

这个结构符合您的需求吗？是否需要调整？
```

**Wait for user confirmation or adjustment before proceeding.**

### Step 3: Animation & Feature Selection

**Ask about specific animation and feature requirements:**

```
现在让我们确定动画和交互细节：

🎭 **动画配置：**
1. 幻灯片切换效果偏好？
   - slide（滑动，默认）
   - fade（淡入淡出）
   - zoom（缩放）
   - convex（凸出）
   - concave（凹陷）

2. 要点列表是否需要逐条显示？（推荐）
   ☐ 是，要点逐条淡入
   ☐ 否，一次全部显示

3. 是否需要特殊动画？
   ☐ 元素自动变换（数字变化、图形变形）
   ☐ 高亮强调（当前要点高亮）
   ☐ 代码逐行显示

📝 **演讲者功能：**
4. 每张幻灯片是否需要演讲者备注？
   ☐ 是，我会提供每页的讲解提示
   ☐ 否，仅幻灯片内容

选择您需要的选项，我将据此创建演示文稿。
```

**Wait for user's selections.**

### Step 4: Read the Template

**CRITICAL:** Before writing any code, read the Reveal.js template file:

```
templates/viewer-reveal.html
```

This template contains:
- ✅ **Reveal.js integration:** CDN links to Reveal.js 5.x core and plugins
- ✅ **Theme system:** CSS custom properties for brand colors
- ✅ **Layout classes:** Pre-built styles for all 6 layout types
- ✅ **Configuration object:** `PRESENTATION_CONFIG` with all Reveal.js options
- ✅ **Plugin setup:** Code highlighting, Markdown, Math, Notes, Zoom, Search
- ✅ **Full API access:** Complete Reveal.js API exposed via `window.PresentationAPI`

**The template is your foundation.** Copy it and customize the content sections.

### Step 5: Generate Slide Content

Create slides using standard HTML `<section>` tags within `.reveal .slides`:

**Basic structure:**
```html
<div class="reveal">
    <div class="slides">
        <!-- Each <section> is a slide -->
        <section class="slide-title">
            <h1>Title</h1>
        </section>
        
        <section class="slide-content">
            <h2>Content</h2>
            <ul>
                <li class="fragment">Point 1</li>
                <li class="fragment">Point 2</li>
            </ul>
            
            <!-- Speaker notes -->
            <aside class="notes">
                This is what you'll say...
            </aside>
        </section>
        
        <!-- Nested slides (vertical navigation) -->
        <section>
            <section><h2>Main Topic</h2></section>
            <section><h3>Subtopic 1</h3></section>
            <section><h3>Subtopic 2</h3></section>
        </section>
    </div>
</div>
```

**Fragment animations (progressive reveal):**
```html
<ul>
    <li class="fragment">Appears first</li>
    <li class="fragment">Appears second</li>
    <li class="fragment fade-in">Fades in</li>
    <li class="fragment fade-up">Slides up</li>
    <li class="fragment highlight-red">Highlights in red</li>
</ul>
```

**Available fragment animations:**
- `fragment` - Basic fade in
- `fragment fade-in` - Fade in
- `fragment fade-out` - Fade out
- `fragment fade-up` - Slide up
- `fragment fade-down` - Slide down
- `fragment grow` - Grow larger
- `fragment shrink` - Shrink smaller
- `fragment highlight-red` - Highlight in red
- `fragment highlight-blue` - Highlight in blue
- `fragment highlight-current-blue` - Highlight current item

### Step 6: Configure Presentation

Update the `PRESENTATION_CONFIG` object:

```javascript
const PRESENTATION_CONFIG = {
    // Basic info
    title: "Your Presentation Title",
    author: "Your Name",
    date: "2026年2月3日",
    
    // Theme colors
    theme: {
        primary: "#2E86AB",      // Main color
        secondary: "#A23B72",    // Secondary color
        accent: "#F18F01",       // Accent color
        background: "#0a0a0a",   // Background
        text: "#ffffff",         // Text color
        textMuted: "#cccccc"     // Muted text
    },
    
    // Reveal.js options
    revealOptions: {
        transition: 'slide',      // slide/fade/zoom/convex/concave
        controls: true,           // Show arrow controls
        progress: true,           // Show progress bar
        center: true,             // Vertical centering
        slideNumber: 'c/t',       // Show slide numbers
        hash: true,               // URL routing
        
        // Animation speed
        transitionSpeed: 'default', // default/fast/slow
        
        // Auto-advance (0 = disabled)
        autoSlide: 0,
        
        // Plugins (always included)
        plugins: [
            RevealMarkdown,
            RevealHighlight,
            RevealNotes,
            RevealZoom,
            RevealSearch,
            RevealMath.KaTeX
        ]
    }
};
```

**Full configuration options:** https://revealjs.com/config/

### Step 7: Add Advanced Features (Optional)

**Speaker notes (press S to open):**
```html
<section>
    <h2>Slide Title</h2>
    <p>Public content...</p>
    
    <aside class="notes">
        Remember to emphasize this point.
        Mention the case study here.
        Time: 2 minutes on this slide.
    </aside>
</section>
```

**Code highlighting with line numbers:**
```html
<section>
    <h2>Code Example</h2>
    <pre><code class="language-javascript" data-trim data-line-numbers="1-2|4-6">
function hello(name) {
    console.log(`Hello, ${name}!`);
}

// Usage
hello('World');
    </code></pre>
</section>
```

**Math equations (KaTeX):**
```html
<section>
    <h2>Mathematical Formula</h2>
    <p>The quadratic formula:</p>
    <p>$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$</p>
</section>
```

**Auto-animate (element transitions):**
```html
<section data-auto-animate>
    <h2 style="margin-top: 100px;">Animate</h2>
</section>
<section data-auto-animate>
    <h2 style="margin-top: 400px; color: red;">Animate</h2>
</section>
```

**Custom backgrounds:**
```html
<section data-background-color="#ff0000">
    <h2>Red Background</h2>
</section>

<section data-background-image="url.jpg">
    <h2>Image Background</h2>
</section>

<section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">
    <h2>Gradient Background</h2>
</section>
```

### Step 8: Validate and Test

Generate the HTML file and verify:

1. **Open in browser** - File loads correctly
2. **Navigate all slides** - Arrow keys work (→ = next, ↓ = nested)
3. **Test fragments** - Progressive reveals work
4. **Speaker view** - Press S (opens in new window)
5. **Overview mode** - Press ESC (thumbnail view)
6. **Fullscreen** - Press F
7. **Search** - Press Ctrl+Shift+F
8. **Zoom** - Alt+Click to zoom in
9. **Help overlay** - Press ? for shortcuts

**Common issues:**
- **Slides not showing:** Check `<section>` tags are inside `.reveal .slides`
- **Fragments not working:** Ensure `class="fragment"` is set
- **Speaker notes not appearing:** Press S, check `<aside class="notes">`
- **Code not highlighted:** Verify `class="language-xxx"` on `<code>`

### Step 9: Deliver with Instructions

Provide the HTML file with clear instructions:

**File name:** `[topic]-presentation.html`

**Output location:** Save the HTML file to the `docs/` directory in your project

**Usage instructions:**
```
🎯 打开方式：在任何现代浏览器中打开此 HTML 文件

⌨️ 快捷键：
  → / Space    下一张幻灯片
  ←            上一张幻灯片
  ↓            向下进入子幻灯片（如果有）
  ↑            向上返回
  ESC          概览模式（查看所有幻灯片）
  S            演讲者视图（包含备注和计时器）
  F            全屏模式
  ?            显示所有快捷键
  Ctrl+Shift+F 搜索
  Alt+Click    放大区域

📱 移动端：左右滑动切换幻灯片

🎤 演讲提示：
  - 按 S 打开演讲者视图，可以看到备注、下一张预览和计时器
  - 建议使用双屏，一个屏幕给观众，一个屏幕给自己（演讲者视图）
```

**Editing note:**
```
如需修改内容，在 HTML 文件中找到 <div class="slides"> 部分，
编辑对应的 <section> 标签即可。
```

---

## Workflow B: Presentation Repository Mode

Use this workflow when the user wants to manage multiple presentations with GitHub Pages deployment.

### Step 1: Repository Initialization

**Ask initial questions:**
```
让我为您创建一个演示文稿管理仓库！首先：

📁 **仓库基本信息：**
1. 仓库名称是什么？（例如：my-presentations, tech-talks, company-slides）
2. 仓库放在哪个目录？（默认：当前工作目录）
3. 是否要立即创建示例演示文稿？（推荐：是）

📋 **初始内容：**
4. 如果创建示例，主题是什么？
5. 您的GitHub用户名是什么？（用于GitHub Pages配置）
```

**Wait for responses.**

### Step 2: Create Repository Structure

Create the complete repository structure:

1. **Create directories:**
```bash
mkdir -p {repo-name}/{presentations,templates,scripts,assets/css}
```

2. **Copy template files:**
   - `scripts/generate-index.js` - Index generation script
   - `templates/presentation-template.html` - Presentation template  
   - `templates/metadata-template.json` - Metadata template
   - `templates/index-template.html` - Index page template
   - `templates/README-template.md` - README template
   - `templates/.gitignore-template` - .gitignore template
   - `templates/custom-css-template.css` - Custom CSS template

3. **Generate package.json** with build scripts
4. **Create .nojekyll** for GitHub Pages
5. **Create assets/css/custom.css** for shared styles
6. **Create README.md** with usage instructions

### Step 3: Optional - Create Example Presentation

If user requested an example:

1. Create `presentations/example-presentation/` directory
2. Copy and customize presentation-template.html → index.html
3. Create metadata.json with provided information
4. Create or generate placeholder thumbnail.png (800x600)

### Step 4: Initialize and Build

```bash
cd {repo-name}
npm install
npm run build
```

This generates the initial `index.html` with the presentation gallery.

### Step 5: GitHub Pages Setup Instructions

Provide step-by-step deployment instructions:

```
📚 仓库已创建！现在设置GitHub Pages：

**1. 初始化Git并推送到GitHub：**
```bash
cd {repo-name}
git init
git add .
git commit -m "Initial commit: Presentation repository"
git remote add origin https://github.com/{username}/{repo-name}.git
git push -u origin main
```

**2. 配置GitHub Pages：**
1. 访问 https://github.com/{username}/{repo-name}/settings/pages
2. Source: Deploy from a branch
3. Branch: main / (root)
4. 点击 Save

**3. 等待部署（约1-3分钟）**
您的演示文稿集合将在以下地址可访问：
https://{username}.github.io/{repo-name}/

**4. 添加新的演示文稿：**
```bash
# 创建新演示文稿目录
mkdir presentations/my-new-talk

# 复制模板
cp templates/presentation-template.html presentations/my-new-talk/index.html
cp templates/metadata-template.json presentations/my-new-talk/metadata.json

# 编辑内容和元数据
# 然后重新生成索引并部署
npm run deploy
```

**本地预览：**
```bash
npm run dev
```
访问 http://localhost:8080 查看索引页
```

### Step 6: Optional - Create GitHub Action for Auto-Deploy

**Ask user:**
```
是否要创建GitHub Action自动部署？
这样每次push都会自动重新生成索引页。

[是] [否]
```

If yes, create `.github/workflows/deploy.yml`:

```yaml
name: Generate Index and Deploy

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Generate index
        run: npm run build
      
      - name: Commit and push if changed
        run: |
          git config --global user.name 'GitHub Action'
          git config --global user.email 'action@github.com'
          git add index.html
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto-generate index [skip ci]" && git push)
```

### Repository Mode Summary

After completion, the user has:
- ✅ Complete presentation repository structure
- ✅ Auto-generated index page with gallery view
- ✅ Templates for quick presentation creation
- ✅ Build scripts for automation
- ✅ GitHub Pages deployment ready
- ✅ npm scripts for common tasks
- ✅ (Optional) GitHub Action for auto-deployment

**Next steps for the user:**
1. Run `npm run dev` to preview locally
2. Edit presentations and metadata
3. Run `npm run build` after changes
4. Run `npm run deploy` to push to GitHub
5. Visit their GitHub Pages URL to see the live site

---

## Available Layouts (with Reveal.js)

All layouts are implemented as CSS classes applied to `<section>` elements. Combine with Reveal.js features for enhanced interactivity.

### 1. Title Slide (`class="slide-title"`)

**Use for:** Opening, closing, major section breaks

```html
<section class="slide-title" data-transition="zoom">
    <h1>Main Title</h1>
    <p class="subtitle">Subtitle or description</p>
    <p class="author">Author Name | Date</p>
</section>
```

**Features:**
- Full-screen, centered
- Gradient background (primary → secondary colors)
- White text with shadow
- Large, impactful typography
- Recommended transition: `zoom` or `fade`

**With animation:**
```html
<section class="slide-title" data-transition="zoom">
    <h1 class="fragment">Main Title</h1>
    <p class="subtitle fragment">Subtitle appears second</p>
    <p class="author fragment">Author appears last</p>
</section>
```

---

### 2. Content Slide (`class="slide-content"`)

**Use for:** Main content, bullet points, text, code

```html
<section class="slide-content">
    <h2>Slide Title</h2>
    <p>Introduction paragraph...</p>
    <ul>
        <li class="fragment">Point one appears first</li>
        <li class="fragment">Point two appears second</li>
        <li class="fragment">Point three appears last</li>
    </ul>
    
    <aside class="notes">
        Speaker notes: Emphasize point two.
    </aside>
</section>
```

**With code highlighting:**
```html
<section class="slide-content">
    <h2>Code Example</h2>
    <pre><code class="language-python" data-trim data-line-numbers="1-3|5-7">
def calculate_total(items):
    total = sum(item.price for item in items)
    return total

# Usage example
items = [Item(10), Item(20)]
result = calculate_total(items)
    </code></pre>
</section>
```

**Supported elements:**
- `<h2>`, `<h3>` - Headings (styled with theme colors)
- `<p>` - Paragraphs
- `<ul>`, `<ol>`, `<li>` - Lists with custom bullets
- `<code>` - Inline code (monospace font)
- `<pre><code>` - Code blocks with syntax highlighting
- `<strong>` - Bold (colored with accent)
- `<em>` - Italic (colored with primary)

---

### 3. Two-Column Layout (`class="two-column"`)

**Use for:** Comparisons, before/after, pros/cons

```html
<section>
    <h2>Comparison</h2>
    <div class="two-column">
        <div class="fragment">
            <h3>Before</h3>
            <ul>
                <li>Slow performance</li>
                <li>Complex setup</li>
                <li>Limited features</li>
            </ul>
        </div>
        <div class="fragment">
            <h3>After</h3>
            <ul>
                <li>2x faster ✨</li>
                <li>One-click setup</li>
                <li>Full-featured</li>
            </ul>
        </div>
    </div>
</section>
```

**Best practices:**
- Balance content between columns
- Use parallel structure
- Animate columns separately with fragments
- Works great with auto-animate

---

### 4. Image + Text (`class="image-text"`)

**Use for:** Product showcases, visual explanations, diagrams

```html
<section>
    <div class="image-text">
        <div>
            <h2>Feature Name</h2>
            <p>Description of the feature...</p>
            <ul>
                <li class="fragment">Benefit one</li>
                <li class="fragment">Benefit two</li>
                <li class="fragment">Benefit three</li>
            </ul>
        </div>
        <div class="fragment">
            <img src="https://via.placeholder.com/600x400" alt="Feature screenshot">
        </div>
    </div>
</section>
```

**Image options:**
- **External URLs:** Quick and easy (requires internet)
- **Data URIs:** Embed for offline use
- **SVG inline:** Best for diagrams and icons

**With auto-animate:**
```html
<section data-auto-animate>
    <div class="image-text">
        <div><h2>Initial State</h2></div>
        <img src="before.png" data-id="product">
    </div>
</section>
<section data-auto-animate>
    <div class="image-text">
        <div><h2>After Transformation</h2></div>
        <img src="after.png" data-id="product">
    </div>
</section>
```

---

### 5. Quote Slide (`class="slide-quote"`)

**Use for:** Testimonials, impactful statements, emphasis

```html
<section class="slide-quote" data-background-gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
    <blockquote class="fragment">
        An impactful quote that emphasizes a key message
        and inspires the audience.
    </blockquote>
    <cite class="fragment">— Author Name, Title</cite>
</section>
```

**Features:**
- Large italic font
- Centered layout
- Border-left accent
- Works great with background gradients
- Perfect for breaks between sections

---

### 6. Section Divider (`class="slide-section"`)

**Use for:** Major topic transitions, chapter breaks

```html
<section class="slide-section" data-background-gradient="linear-gradient(135deg, #A23B72 0%, #F18F01 100%)">
    <h2 class="fragment">Part Two</h2>
</section>
```

**Features:**
- Full-screen colored background
- Large white text with shadow
- Creates visual rhythm
- Use sparingly (2-4 per presentation)
- Recommended transition: `convex` or `zoom`

---

### 7. Nested Slides (Vertical Navigation)

**Use for:** Hierarchical content, deep dives, optional details

```html
<!-- Main topic (horizontal) -->
<section>
    <section>
        <h2>Main Topic</h2>
        <p>Press ↓ to dive deeper</p>
    </section>
    
    <!-- Subtopic 1 (vertical) -->
    <section>
        <h3>Subtopic 1</h3>
        <p>Detailed explanation...</p>
    </section>
    
    <!-- Subtopic 2 (vertical) -->
    <section>
        <h3>Subtopic 2</h3>
        <p>More details...</p>
    </section>
</section>

<!-- Next main topic (horizontal) -->
<section>
    <h2>Next Topic</h2>
</section>
```

**Best practices:**
- Use for optional deep dives
- Main topics go horizontal (→)
- Subtopics go vertical (↓)
- Visual indicator in controls
- Great for Q&A sections

---

## Reveal.js Advanced Features

### Fragment Animations

Progressive reveal of content within a slide:

**Basic fragments:**
```html
<ul>
    <li class="fragment">Fade in (default)</li>
    <li class="fragment fade-in">Also fades in</li>
    <li class="fragment fade-out">Fades out</li>
    <li class="fragment fade-up">Slides in from bottom</li>
    <li class="fragment fade-down">Slides in from top</li>
    <li class="fragment fade-left">Slides in from right</li>
    <li class="fragment fade-right">Slides in from left</li>
</ul>
```

**Emphasis fragments:**
```html
<ul>
    <li class="fragment grow">Grow larger</li>
    <li class="fragment shrink">Shrink smaller</li>
    <li class="fragment strike">Strike through</li>
    <li class="fragment highlight-red">Highlight in red</li>
    <li class="fragment highlight-blue">Highlight in blue</li>
    <li class="fragment highlight-green">Highlight in green</li>
    <li class="fragment highlight-current-red">Highlight current</li>
</ul>
```

**Fragment index (control order):**
```html
<p class="fragment" data-fragment-index="3">Appears third</p>
<p class="fragment" data-fragment-index="1">Appears first</p>
<p class="fragment" data-fragment-index="2">Appears second</p>
```

**Combining fragments:**
```html
<span class="fragment fade-in">
    <span class="fragment highlight-red">
        <span class="fragment fade-out">
            Text fades in, highlights red, then fades out
        </span>
    </span>
</span>
```

---

### Auto-Animate

Smooth transitions between slide states:

**Basic example:**
```html
<section data-auto-animate>
    <h2>Auto-Animate</h2>
</section>
<section data-auto-animate>
    <h2 style="margin-top: 100px; color: red;">Auto-Animate</h2>
</section>
```

**Element matching (using data-id):**
```html
<section data-auto-animate>
    <div data-id="box" style="height: 50px; background: red;"></div>
</section>
<section data-auto-animate>
    <div data-id="box" style="height: 200px; background: blue;"></div>
</section>
```

**Code morphing:**
```html
<section data-auto-animate>
    <pre><code data-trim data-line-numbers>
let x = 10;
    </code></pre>
</section>
<section data-auto-animate>
    <pre><code data-trim data-line-numbers>
let x = 10;
let y = 20;
let sum = x + y;
    </code></pre>
</section>
```

**Auto-animate settings:**
```html
<section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)">
<section data-auto-animate data-auto-animate-duration="2.0">
```

---

### Speaker Notes

Visible only in speaker view (press S):

**Basic notes:**
```html
<section>
    <h2>Slide Title</h2>
    <p>Public content...</p>
    
    <aside class="notes">
        These notes are only visible in speaker view.
        - Remember to mention the case study
        - Emphasize the 2x performance improvement
        - Allow 2 minutes for this slide
    </aside>
</section>
```

**Formatted notes:**
```html
<aside class="notes">
    <h4>Key Points:</h4>
    <ul>
        <li>Point one</li>
        <li>Point two</li>
    </ul>
    
    <p><strong>Time:</strong> 3 minutes</p>
</aside>
```

**Speaker view features:**
- Current slide on left
- Next slide preview on right
- Speaker notes in center
- Timer and slide counter
- Can be full-screen on second monitor

---

### Transitions

Control slide transitions:

**Per-slide transition:**
```html
<section data-transition="zoom">
    <h2>This slide zooms in</h2>
</section>

<section data-transition="fade">
    <h2>This slide fades</h2>
</section>
```

**Available transitions:**
- `none` - Instant cut
- `fade` - Cross-fade
- `slide` - Slide horizontally (default)
- `convex` - Slide at a convex angle
- `concave` - Slide at a concave angle
- `zoom` - Scale in/out

**Separate in/out transitions:**
```html
<section data-transition="slide-in fade-out">
    <h2>Slides in, fades out</h2>
</section>
```

**Transition speed:**
```html
<section data-transition-speed="fast">
    <h2>Quick transition</h2>
</section>
<!-- Options: default, fast, slow -->
```

---

### Backgrounds

Customize slide backgrounds:

**Color backgrounds:**
```html
<section data-background-color="#ff0000">
    <h2>Red background</h2>
</section>
```

**Gradient backgrounds:**
```html
<section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">
    <h2>Gradient background</h2>
</section>
```

**Image backgrounds:**
```html
<section data-background-image="url.jpg">
    <h2>Image background</h2>
</section>

<section data-background-image="url.jpg" data-background-size="cover">
<section data-background-image="url.jpg" data-background-opacity="0.3">
```

**Video backgrounds:**
```html
<section data-background-video="video.mp4" data-background-video-loop data-background-video-muted>
    <h2>Video background</h2>
</section>
```

**iframe backgrounds:**
```html
<section data-background-iframe="https://example.com" data-background-interactive>
    <h2>Interactive webpage background</h2>
</section>
```

---

### Code Highlighting

Syntax highlighting with Highlight.js:

**Basic code block:**
```html
<pre><code class="language-javascript">
function hello(name) {
    console.log(`Hello, ${name}!`);
}
</code></pre>
```

**Line numbers:**
```html
<pre><code class="language-python" data-line-numbers>
def calculate(x, y):
    result = x + y
    return result
</code></pre>
```

**Highlight specific lines:**
```html
<pre><code class="language-java" data-line-numbers="1-2|4-6|8">
public class Hello {
    private String name;
    
    public Hello(String name) {
        this.name = name;
    }
    
    public void greet() {
        System.out.println("Hello, " + name);
    }
}
</code></pre>
```

**Line number offset:**
```html
<pre><code data-line-numbers="10-15">
// Code starting at line 10
</code></pre>
```

**Supported languages:**
JavaScript, Python, Java, C++, C#, Ruby, PHP, Go, Rust, TypeScript, SQL, HTML, CSS, Markdown, Bash, and 150+ more

---

### Math Equations

KaTeX integration for beautiful math:

**Inline math:**
```html
<p>The formula $E = mc^2$ shows energy-mass equivalence.</p>
```

**Display math:**
```html
<p>$$\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$</p>
```

**Complex equations:**
```html
<section>
    <h2>Quadratic Formula</h2>
    <p>
    $$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$
    </p>
    
    <aside class="notes">
        Explain each component of the formula.
    </aside>
</section>
```

**Multi-line equations:**
```html
<p>
$$
\begin{aligned}
a &= b + c \\
&= d + e + f
\end{aligned}
$$
</p>
```

---

### Markdown Support

Write slides in Markdown:

**External Markdown file:**
```html
<section data-markdown="slides.md" data-separator="^\n---\n$" data-separator-vertical="^\n--\n$"></section>
```

**Inline Markdown:**
```html
<section data-markdown>
    <textarea data-template>
        ## Slide Title
        
        - Bullet point one
        - Bullet point two
        
        **Bold text** and *italic text*
        
        ```javascript
        const code = "highlighted";
        ```
    </textarea>
</section>
```

**Markdown with fragments:**
```html
<section data-markdown>
    <textarea data-template>
        ## Progressive Reveal
        
        - Item 1 <!-- .element: class="fragment" -->
        - Item 2 <!-- .element: class="fragment" -->
        - Item 3 <!-- .element: class="fragment" -->
    </textarea>
</section>
```

---

### Interactive Features

**Search (Ctrl+Shift+F):**
- Automatically enabled with RevealSearch plugin
- Searches all slide content
- Highlights matches
- Navigate between results

**Zoom (Alt+Click):**
- Click any element while holding Alt
- Zooms in to that element
- Click again to zoom out
- Great for highlighting details

**Overview Mode (ESC):**
- Shows all slides as thumbnails
- Click to jump to any slide
- Great for navigation during Q&A
- Shows slide hierarchy (horizontal/vertical)

**Help Overlay (?):**
- Shows all keyboard shortcuts
- Customizable
- Automatically includes plugin shortcuts

---

## Reveal.js API Usage

The template exposes the full Reveal.js API via `window.PresentationAPI`:

**Basic navigation:**
```javascript
// Access Reveal instance
const reveal = window.PresentationAPI.reveal;

// Navigate programmatically
reveal.slide(3);          // Go to slide 3
reveal.slide(2, 1);       // Go to slide 2, vertical slide 1
reveal.next();            // Next slide
reveal.prev();            // Previous slide
reveal.left();            // Navigate left
reveal.right();           // Navigate right
reveal.down();            // Navigate down (nested)
reveal.up();              // Navigate up (nested)
```

**State management:**
```javascript
// Get current state
const state = reveal.getState();
console.log(state);  // {indexh: 2, indexv: 0, indexf: 1}

// Get total slides
const total = reveal.getTotalSlides();

// Get current slide element
const currentSlide = reveal.getCurrentSlide();

// Check if at first/last
reveal.isFirstSlide();
reveal.isLastSlide();
```

**Toggle features:**
```javascript
// Toggle overview mode
reveal.toggleOverview();

// Toggle pause
reveal.togglePause();

// Toggle help overlay
reveal.toggleHelp();

// Toggle auto-slide
reveal.toggleAutoSlide();
```

**Event listeners:**
```javascript
// Slide changed event
reveal.on('slidechanged', event => {
    console.log('Now on slide:', event.indexh);
    // Send analytics
    // Update external UI
    // Trigger custom logic
});

// Fragment shown/hidden
reveal.on('fragmentshown', event => {
    console.log('Fragment shown:', event.fragment);
});

reveal.on('fragmenthidden', event => {
    console.log('Fragment hidden:', event.fragment);
});

// Ready event
reveal.on('ready', event => {
    console.log('Presentation ready');
});

// Overview toggled
reveal.on('overviewshown', () => {
    console.log('Overview mode activated');
});

reveal.on('overviewhidden', () => {
    console.log('Overview mode deactivated');
});
```

**Sync with external systems:**
```javascript
// Send slide changes to server
reveal.on('slidechanged', async event => {
    await fetch('/api/analytics', {
        method: 'POST',
        body: JSON.stringify({
            slide: event.indexh,
            timestamp: Date.now()
        })
    });
});

// Multi-screen synchronization
reveal.on('slidechanged', event => {
    // Broadcast to other windows
    localStorage.setItem('currentSlide', JSON.stringify(event));
});

window.addEventListener('storage', e => {
    if (e.key === 'currentSlide') {
        const {indexh, indexv} = JSON.parse(e.newValue);
        reveal.slide(indexh, indexv);
    }
});
```

**Dynamic content:**
```javascript
// Load slide content dynamically
reveal.on('slidechanged', async event => {
    const slideId = event.currentSlide.getAttribute('data-slide-id');
    if (slideId) {
        const data = await fetch(`/api/slides/${slideId}`).then(r => r.json());
        event.currentSlide.innerHTML = data.content;
    }
});
```

**Custom theme switching:**
```javascript
// Change theme colors dynamically
function changeTheme(themeName) {
    const themes = {
        blue: { primary: '#2E86AB', secondary: '#A23B72', accent: '#F18F01' },
        green: { primary: '#2d6a4f', secondary: '#52b788', accent: '#d8f3dc' },
        red: { primary: '#9d0208', secondary: '#dc2f02', accent: '#f48c06' }
    };
    
    const theme = themes[themeName];
    Object.entries(theme).forEach(([key, value]) => {
        const cssVar = `--color-${key}`;
        document.documentElement.style.setProperty(cssVar, value);
    });
}

// Usage: changeTheme('green')
```

**Complete API reference:** https://revealjs.com/api/

---

## Advanced Customization

### Custom CSS

Add custom styles in the `<style>` section:

```css
/* Custom slide variant */
.slide-highlight {
    background: linear-gradient(135deg, #fff5f5, #ffffff);
    border-left: 8px solid var(--color-accent);
    padding-left: 3em !important;
}

/* Custom animation */
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.pulse-on-show.fragment.visible {
    animation: pulse 0.5s ease-in-out;
}

/* Responsive grid layout */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2em;
}
```

### Adding External Libraries

**Charts (Chart.js):**
```html
<!-- In <head> -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>

<!-- In slide -->
<section>
    <h2>Sales Data</h2>
    <canvas id="salesChart" width="800" height="400"></canvas>
    <script>
        Reveal.on('slidechanged', event => {
            if (event.currentSlide.querySelector('#salesChart')) {
                new Chart(document.getElementById('salesChart'), {
                    type: 'line',
                    data: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr'],
                        datasets: [{
                            label: 'Sales',
                            data: [12, 19, 3, 5],
                            borderColor: '#2E86AB',
                            tension: 0.1
                        }]
                    }
                });
            }
        });
    </script>
</section>
```

**Diagrams (Mermaid):**
```html
<!-- In <head> -->
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
</script>

<!-- In slide -->
<section>
    <h2>Architecture</h2>
    <div class="mermaid">
    graph TD
        A[Client] --> B[Load Balancer]
        B --> C[Server 1]
        B --> D[Server 2]
    </div>
</section>
```

**3D Visualizations (Three.js):**
```html
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>

<section>
    <h2>3D Model</h2>
    <div id="three-container" style="width: 800px; height: 600px;"></div>
    <script>
        // Initialize Three.js scene when slide is shown
        Reveal.on('slidechanged', event => {
            if (event.currentSlide.querySelector('#three-container')) {
                // Three.js setup code...
            }
        });
    </script>
</section>
```

---

## Keyboard Shortcuts Reference

Provide these shortcuts to users:

| Action | Shortcut | Description |
|--------|----------|-------------|
| Next slide | `→` or `Space` or `N` | Move to next slide |
| Previous slide | `←` or `P` | Move to previous slide |
| Navigate down | `↓` | Go to nested slide below |
| Navigate up | `↑` | Go to nested slide above |
| First slide | `Home` | Jump to first slide |
| Last slide | `End` | Jump to last slide |
| **Speaker view** | `S` | Open speaker notes window |
| **Overview mode** | `ESC` or `O` | Toggle thumbnail overview |
| **Fullscreen** | `F` | Toggle fullscreen mode |
| **Search** | `Ctrl+Shift+F` | Search presentation content |
| **Zoom** | `Alt+Click` | Zoom into element |
| Help overlay | `?` | Show all shortcuts |
| **Pause** | `.` (period) or `B` | Pause presentation (black screen) |
| **Auto-slide** | `A` | Toggle auto-advance |
| **Print/PDF** | `E` | Switch to print view (add `?print-pdf` to URL) |

**Mobile gestures:**
- Swipe left → Next slide
- Swipe right → Previous slide
- Swipe up → Navigate down
- Swipe down → Navigate up
- Pinch → Toggle overview

---

## Design Guidelines

### Content Density

**Per slide guidelines:**
- **Title slides:** 1 title + 1-2 supporting lines
- **Content slides:** 1 heading + 3-7 bullet points OR 2-3 paragraphs
- **Two-column:** 3-5 items per column
- **Image slides:** 1 image + short description

**The 6×6 rule:** Maximum 6 bullets with 6 words each

**Avoid:**
- ❌ Paragraphs longer than 4 lines
- ❌ More than 7 bullet points per slide
- ❌ Tiny font sizes (< 24px)
- ❌ Wall of text
- ❌ Cramped spacing

### Animation Best Practices

**Use fragments for:**
- ✅ Building lists progressively
- ✅ Revealing data points step-by-step
- ✅ Highlighting key information
- ✅ Controlling information flow

**Use auto-animate for:**
- ✅ Showing transformations
- ✅ Morphing code examples
- ✅ Animating diagrams
- ✅ Data visualizations

**Avoid:**
- ❌ Excessive animations (don't animate every element)
- ❌ Distracting transitions
- ❌ Animations longer than 1 second
- ❌ Too many concurrent animations

### Visual Hierarchy

**Create clear structure:**
- **Large to small:** Titles (3em) → Headings (2em) → Body (1em)
- **Bold to regular:** Important points → Supporting details
- **Color emphasis:** Accent color → Primary → Body text
- **Spacing:** More space = more importance

### Color and Accessibility

**Accessibility requirements:**
- Maintain **4.5:1 contrast** for normal text
- Maintain **3:1 contrast** for large text (18pt+)
- Don't rely solely on color to convey information
- Test with colorblind simulators

**Color usage:**
- **Primary:** Headings, links, emphasis
- **Secondary:** Gradients, backgrounds
- **Accent:** Call-to-actions, highlights

---

## Troubleshooting

### Slides Not Displaying

**Issue:** Blank screen or no slides appear  
**Solution:**
- Check browser console for JavaScript errors
- Ensure `<section>` tags are inside `.reveal .slides`
- Verify CDN links are accessible (internet required)
- Check for unclosed HTML tags

### Fragments Not Working

**Issue:** All content appears at once  
**Solution:**
- Verify `class="fragment"` is set correctly
- Check that `fragments: true` in configuration
- Ensure no CSS overrides are hiding fragments
- Test in different browser

### Speaker Notes Not Showing

**Issue:** Press S but no speaker window opens  
**Solution:**
- Check popup blocker settings
- Ensure `<aside class="notes">` is inside `<section>`
- Verify RevealNotes plugin is loaded
- Try opening in a new browser tab manually

### Code Not Highlighted

**Issue:** Code appears as plain text  
**Solution:**
- Add `class="language-xxx"` to `<code>` element
- Ensure RevealHighlight plugin is loaded
- Check that CDN for highlight styles is accessible
- Verify language identifier is supported

### Navigation Issues

**Issue:** Arrow keys don't work  
**Solution:**
- Check if presentation has focus (click on it)
- Ensure `keyboard: true` in configuration
- Check for JavaScript errors in console
- Test in incognito mode (disable extensions)

### Vertical Slides Not Showing

**Issue:** Can't navigate down to nested slides  
**Solution:**
- Ensure slides are properly nested (outer `<section>` contains inner ones)
- Check for proper HTML structure
- Look for down arrow indicator in controls
- Try pressing ↓ or clicking down arrow

---

## Example Presentation Structures

### Product Launch (12-15 slides)

```
1. 🎬 Title - Product name + tagline [TITLE, zoom transition]
2. 📋 Agenda - What we'll cover [CONTENT, fragments]
3. 🔴 Section - "The Problem" [SECTION, red background]
4. 😰 Pain Points - Current challenges [CONTENT, fragment list]
5. 💡 Solution Overview - How product solves it [CONTENT]
6. 🟢 Section - "Key Features" [SECTION, green background]
7-10. 📱 Feature Deep Dives [IMAGE-TEXT, one per slide, auto-animate]
    ├─ 7. Performance (fragment metrics)
    ├─ 8. Security (diagram)
    ├─ 9. UX (before/after comparison)
    └─ 10. Integration (code example)
11. 💰 Pricing - Tiers and packages [TWO-COLUMN]
12. 💬 Testimonial [QUOTE, gradient background]
13. 📞 Call to Action [TITLE, zoom transition]
14. 🙏 Thank You + Q&A [TITLE]
```

### Technical Talk (20-25 slides)

```
1. Title + Speaker Bio [TITLE]
2. Agenda [CONTENT, fragment]
3. Section - "Background" [SECTION]
4-6. Context (nested slides)
    <section>
        4. Main concept [CONTENT]
        5. Why it matters [CONTENT]
        6. Current approaches [TWO-COLUMN]
    </section>
7. Section - "Deep Dive" [SECTION]
8-15. Technical Details
    8. Architecture diagram [IMAGE-TEXT]
    9-11. Code examples (auto-animate)
    12. Performance metrics [CONTENT, fragments]
    13-14. Comparison (before/after)
    15. Demo transition [TITLE, fade]
16. Section - "Results" [SECTION]
17-19. Outcomes
    17. Benchmark data [CONTENT, chart.js]
    18. Real-world impact [QUOTE]
    19. Lessons learned [CONTENT]
20. Future Work [CONTENT, fragments]
21. Resources + Links [CONTENT]
22. Q&A [TITLE]
```

### Educational Lesson (25-30 slides)

```
1. Lesson Title [TITLE]
2. Learning Objectives [CONTENT, fragment]
3. Section - "Introduction" [SECTION]
4-7. Background (vertical nested)
8. Section - "Core Concepts" [SECTION]
9-20. Main Content
    - One concept per slide
    - Use fragments for progressive reveal
    - Mix layouts: content, two-column, image-text
    - Add speaker notes for teaching points
21. Section - "Practice" [SECTION]
22-25. Examples and Exercises
    - Code examples with line highlighting
    - Interactive elements
    - Step-by-step walkthroughs
26. Summary [CONTENT, fragments]
27. Additional Resources [CONTENT]
28. Questions [TITLE]
```

---

## Best Practices Checklist

### Before Creating:
- [ ] Ask all discovery questions to user
- [ ] Confirm slide structure and count
- [ ] Clarify animation requirements
- [ ] Verify color/brand guidelines
- [ ] Understand special feature needs

### During Creation:
- [ ] Read template file first
- [ ] Use appropriate layouts for content types
- [ ] Add fragments for progressive reveal
- [ ] Include speaker notes for key slides
- [ ] Apply consistent color scheme
- [ ] Add transitions strategically
- [ ] Nest slides for hierarchical content
- [ ] Test code highlighting
- [ ] Verify math formulas render

### After Creation:
- [ ] Test in browser (open HTML file)
- [ ] Navigate through all slides
- [ ] Test speaker view (press S)
- [ ] Check overview mode (press ESC)
- [ ] Verify fragments animate correctly
- [ ] Test keyboard shortcuts
- [ ] Check mobile responsiveness
- [ ] Validate accessibility (contrast)
- [ ] Proofread content
- [ ] Test fullscreen mode

### DO:
✅ Ask questions before starting  
✅ Use fragments for progressive reveals  
✅ Include speaker notes for presentations  
✅ Keep slides focused (one idea each)  
✅ Test navigation thoroughly  
✅ Ensure good color contrast  
✅ Use nested slides for deep dives  
✅ Provide clear instructions  
✅ Test on different screen sizes  
✅ Leverage Reveal.js API when needed  

### DON'T:
❌ Skip the discovery questions  
❌ Overcrowd slides with text  
❌ Use too many different animations  
❌ Forget to test speaker view  
❌ Ignore accessibility standards  
❌ Create slides without clear purpose  
❌ Use more than 3 font families  
❌ Add distracting effects  
❌ Skip validation testing  
❌ Forget to provide usage instructions  

---

## Additional Resources

**Official Documentation:**
- [Reveal.js Official Docs](https://revealjs.com/) - Complete API reference
- [Reveal.js GitHub](https://github.com/hakimel/reveal.js) - Source code and examples
- [Reveal.js Plugins](https://github.com/hakimel/reveal.js/wiki/Plugins,-Tools-and-Hardware) - Community plugins

**Reference Files (in this skill):**
- `reference/layouts.md` - Detailed layout guide with Reveal.js examples
- `reference/themes.md` - Theme customization and color theory with Reveal.js
- `templates/viewer-reveal.html` - Reveal.js base template with full documentation
- `examples/reveal-advanced-demo.html` - Advanced features showcase

**Design Tools:**
- [Coolors.co](https://coolors.co/) - Color palette generator
- [Google Fonts](https://fonts.google.com/) - Web font library
- [SVG OMG](https://jakearchibald.github.io/svgomg/) - SVG optimizer
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Accessibility testing

**Related Libraries:**
- [Chart.js](https://www.chartjs.org/) - Data visualization charts
- [Mermaid](https://mermaid.js.org/) - Diagram and flowchart generation
- [KaTeX](https://katex.org/) - Math equation rendering
- [Highlight.js](https://highlightjs.org/) - Syntax highlighting for 190+ languages

**Reveal.js Themes:**
- [Reveal.js Themes Gallery](https://revealjs.com/themes/) - Official themes
- [Custom Theme Builder](https://slides.com/news/custom-themes) - Visual theme creator

**Export and Sharing:**
- **PDF Export:** Add `?print-pdf` to URL and use browser print (Ctrl+P)
- **Hosting:** Upload to GitHub Pages, Netlify, Vercel for free hosting
- **Embedding:** Use `<iframe>` to embed in websites

---

## Migration Guide (from Classic Template)

If you have existing presentations using `viewer.html`, here's how to migrate:

### Key Differences

| Feature | Classic (`viewer.html`) | Reveal.js (`viewer-reveal.html`) |
|---------|------------------------|----------------------------------|
| **Framework** | Custom JavaScript | Reveal.js 5.x |
| **Slides** | JavaScript array | HTML `<section>` tags |
| **Animations** | CSS transitions only | Fragments, auto-animate, transitions |
| **Speaker Notes** | ❌ Not available | ✅ Full speaker view (press S) |
| **Overview Mode** | ❌ Not available | ✅ Thumbnail overview (press ESC) |
| **Vertical Slides** | ❌ Not available | ✅ Nested navigation |
| **Code Highlighting** | Basic | Highlight.js with line numbers |
| **Math Equations** | ❌ Not available | ✅ KaTeX support |
| **Search** | ❌ Not available | ✅ Full-text search (Ctrl+Shift+F) |
| **Plugins** | ❌ None | ✅ Extensive ecosystem |
| **API Access** | Limited | Full Reveal.js API |

### Migration Steps

1. **Convert slide structure:**
```javascript
// OLD (viewer.html)
const SLIDES = [
    {
        layout: "title",
        content: `<h1>Title</h1>`
    }
];

// NEW (viewer-reveal.html)
<section class="slide-title">
    <h1>Title</h1>
</section>
```

2. **Update theme configuration:**
```javascript
// OLD
const PRESENTATION = {
    title: "...",
    theme: { primary: "#...", ... }
};

// NEW
const PRESENTATION_CONFIG = {
    title: "...",
    theme: { primary: "#...", ... },
    revealOptions: { ... }
};
```

3. **Add new features:**
- Add `class="fragment"` for progressive reveals
- Wrap nested content in `<section>` for vertical navigation
- Add `<aside class="notes">` for speaker notes
- Use Reveal.js transitions and animations

---

## Summary

This skill creates modern, interactive presentations powered by **Reveal.js** as single HTML files. The upgraded workflow features:

### Interactive Workflow
1. **Ask discovery questions** - Gather content, style, and animation requirements
2. **Propose structure** - Collaborative slide planning with user confirmation
3. **Configure features** - Select animations, transitions, and special functions
4. **Read template** - Study `templates/viewer-reveal.html`
5. **Generate slides** - Create HTML content with appropriate layouts
6. **Configure presentation** - Set theme colors and Reveal.js options
7. **Add advanced features** - Fragments, speaker notes, nested slides, plugins
8. **Validate thoroughly** - Test all features and navigation
9. **Deliver with instructions** - Provide complete usage guide

### Key Advantages over Classic Template
- ✅ **Advanced animations:** Fragments, auto-animate, parallax
- ✅ **Speaker tools:** Notes, timer, next slide preview
- ✅ **Navigation:** Vertical slides, overview mode, search
- ✅ **Rich content:** Code highlighting, math equations, Markdown
- ✅ **Plugin ecosystem:** Extensible with hundreds of plugins
- ✅ **Full API:** Complete programmatic control
- ✅ **Active development:** Reveal.js is actively maintained
- ✅ **Community:** Large user base and resources

### Success Factors
- **Always ask questions first** - Don't assume requirements
- **Use appropriate layouts** - Match content type to layout
- **Leverage fragments** - Progressive reveals keep audience engaged
- **Add speaker notes** - Essential for presentations
- **Test thoroughly** - Verify all features work
- **Ensure accessibility** - Good contrast, keyboard nav, semantic HTML
- **Provide clear instructions** - Users need to know all features

### The Result
A professional, feature-rich presentation that:
- Runs in any modern browser
- Works offline (CDN resources cached)
- Supports advanced features (speaker view, overview, search)
- Offers smooth animations and transitions
- Provides full keyboard and touch control
- Scales from simple pitches to complex technical talks
- Can be easily shared, embedded, or hosted

**Ready to create amazing presentations! 🎉**

---

*For detailed layout examples and animation techniques, see `reference/layouts.md`*  
*For theme customization and color theory, see `reference/themes.md`*  
*For a complete working example, see `examples/reveal-advanced-demo.html`*
