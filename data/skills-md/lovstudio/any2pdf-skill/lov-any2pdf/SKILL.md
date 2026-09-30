---
name: lov-any2pdf
description: >
  Convert Markdown to polished PDF with CJK typography, code, tables, images,
  covers, TOC, bookmarks, and reading themes. Trigger on md2pdf, Chinese report
  typesetting, or print-ready PDF requests.
license: MIT
compatibility: >
  Requires Python 3.8+ and reportlab (`pip install reportlab`).
  Optional: matplotlib (`pip install matplotlib`) for rendered display formulas.
  macOS: uses Palatino, Songti SC, Menlo (pre-installed).
  Linux: uses DejaVu/Liberation/FreeFont/Noto, Noto CJK, Droid Sans Fallback,
  DejaVu Sans Mono, and Noto Emoji when available.
depends_on:
  - lov-branding-consistency
metadata:
  author: contributors
  version: "1.5.2"
  tags:
    - markdown
    - pdf
    - cjk
    - reportlab
    - typesetting
---

# PDF大师 · PDF Master

This skill converts any Markdown file into a publication-quality PDF using Python's
reportlab library. It was developed through extensive iteration on real Chinese
technical reports and solves several hard problems that naive MD→PDF converters
get wrong.

## Triggers

### Activate when

- User wants to convert `.md` → `.pdf`
- User has a markdown report/document and wants professional typesetting
- Document contains CJK characters (Chinese/Japanese/Korean) mixed with Latin text
- Document has fenced code blocks, markdown tables, or nested lists
- Document has local/remote images, Obsidian callouts, emoji, or math formulas
- User wants a cover page, table of contents, or watermark in their PDF

### Do not activate when

- The user only wants to revise Markdown content and does not need a PDF output.
- The source is HTML, DOCX, or another format and the user has not authorized a Markdown conversion step.
- The user needs a slide deck, editable Word document, or image export rather than a PDF.

## Quick Start

```bash
python md2pdf/scripts/md2pdf.py \
  --input report.md \
  --output report.pdf \
  --title "My Report" \
  --author "Author Name"
```

All parameters except `--input` are optional. When no theme is supplied, the
renderer selects one from the document's content and structure.

## Configuration Resolution (MANDATORY)

Do not present a full configuration form before every conversion. Resolve each
setting independently in this order:

1. the user's explicit instruction in the current request, then CLI arguments or document frontmatter;
2. the user's last explicitly confirmed value from the `lov_any2pdf` preference namespace;
3. a content-aware decision for the theme, or the documented safe default for non-visual settings.

Proceed without asking when this resolves the conversion. Ask at most one concise
question only when an unresolved choice would materially change the result, such
as a missing local asset path or permission to generate a new image. Do not ask the
user to choose from every theme unless they explicitly request the theme catalog.

After the user explicitly confirms or changes a reusable parameter, record that
value as the latest preference. Reuse it next time when the user is silent. Never
persist an inferred value as though the user confirmed it, and honor requests to
reset or ignore saved preferences.

Reusable parameters include theme, cover/TOC, page size, frontispiece mode,
watermark text and geometry, image-cover mode, back-cover mode/banner, disclaimer,
copyright, header, and footer. Revalidate saved file paths before use; if an asset
no longer exists, ask for a replacement instead of silently substituting one.

### Content-Aware Theme Decision

When neither the current request nor the saved preferences specify a theme, read
the title, opening, headings, document length, code blocks, tables, imagery, and
publishing context, then select the theme that best serves the article. The
following are decision cues, not a fixed keyword router:

| Content character | Good starting theme |
|-------------------|---------------------|
| Long Chinese prose, knowledge notes, dense tables | `songti-reading` |
| Strategy, business, market, or research report | `consulting-navy` |
| Academic paper with abstract/method/results/references | `ieee-journal` or `classic-thesis` |
| Code-heavy technical guide or API documentation | `github-light` |
| Data narrative with charts and metrics | `tufte` |
| Literary, art, photography, or design essay | `ink-wash` |
| Formal Chinese policy or institutional document | `chinese-red` |
| Neutral English prose or print-first document | `paper-classic` |

`warm-academic` remains available when its tone genuinely fits the article, but it
is never the default merely because the user omitted a style.

### Mapping User Choices to CLI Args

| Choice | CLI arg |
|--------|---------|
| Design style | `--theme` with value from table below (`latex-clean` uses pandoc engine) |
| Frontispiece local | `--frontispiece <path>` |
| Frontispiece AI | Generate image first, then `--frontispiece /tmp/frontispiece.png` |
| Watermark text | `--watermark "文字"` |
| Watermark style | `--wm-size 30 --wm-opacity 0.1 --wm-angle 45` (all optional) |
| Image as cover | `--image-cover true` (requires `--frontispiece`) |
| Back cover image | `--banner <path>` |
| Back cover text | `--disclaimer "声明"` and/or `--copyright "© 信息"` |

### Theme Name Mapping

| Style | `--theme` value | Inspiration |
|-------|----------------|-------------|
| 暖学术 | `warm-academic` | Warm editorial-academic palette |
| 经典论文 | `classic-thesis` | LaTeX classicthesis |
| Tufte | `tufte` | Edward Tufte's books |
| 期刊蓝 | `ieee-journal` | IEEE journal format |
| 精装书 | `elegant-book` | LaTeX ElegantBook |
| 中国红 | `chinese-red` | Chinese formal documents |
| 水墨 | `ink-wash` | 水墨画 / ink wash painting |
| GitHub | `github-light` | GitHub Markdown style |
| Nord | `nord-frost` | Nord color scheme |
| 海洋 | `ocean-breeze` | Clean teal editorial palette |
| LaTeX 清爽 | `latex-clean` | pandoc+XeLaTeX 原生排版，无封面 |
| 咨询深蓝 | `consulting-navy` | Consulting research reports |
| 宋黑阅读 | `songti-reading` | 中文出版物常见的宋体正文 + 黑体标题层级 |

### Handling AI-Generated Frontispiece

If user chose AI generation: read the document title + first paragraphs, use an
image generation tool to create a themed illustration matching the chosen design
style, show for approval, then pass via `--frontispiece /path/to/image.png`

## Architecture

```
Markdown → Preprocess (split merged headings) → Parse (code-fence-aware) → Story (reportlab flowables) → PDF build
```

Key components:
1. **Font system**: Palatino (Latin body), Songti SC Regular (CJK body), selectable serif/sans CJK emphasis, Menlo (code) on macOS; auto-fallback on Linux/Windows
2. **CJK wrapper**: `_font_wrap()` wraps CJK character runs in `<font>` tags for automatic font switching
3. **Mixed text renderer**: `_draw_mixed()` handles CJK/Latin mixed text on canvas (cover, headers, footers)
4. **Code block handler**: `esc_code()` preserves indentation, mid-line alignment, and line breaks in reportlab Paragraphs
5. **Smart table widths**: Proportional column widths based on content length, with 18mm minimum
6. **Bookmark system**: `ChapterMark` flowable creates PDF sidebar bookmarks + named anchors
7. **Heading preprocessor**: `_preprocess_md()` splits merged headings like `# Part## Chapter` into separate lines
8. **Image handler**: local, relative, `file://`, and remote markdown images are scaled into the body frame with fallback text on errors
9. **Callout renderer**: Obsidian-style `> [!NOTE]` blocks render as themed boxed callouts
10. **Formula renderer**: display formulas use optional matplotlib mathtext images, with styled text fallback
11. **Emoji fallback**: emoji are rendered as cached Twemoji PNGs when available, or with a local emoji font fallback

## Hard-Won Lessons

### CJK Characters Rendering as □

reportlab's `Paragraph` only uses the font in ParagraphStyle. If `fontName="Mono"` but
text contains Chinese, they render as □. **Fix**: Always apply `_font_wrap()` to ALL text
that might contain CJK, including code blocks.

### Code Blocks Losing Line Breaks

reportlab treats `\n` as whitespace. **Fix**: `esc_code()` converts `\n` → `<br/>` and
all spaces → `&nbsp;`, preserving indentation and mid-line alignment before `_font_wrap()`.

### CJK/Latin Word Wrapping

Default reportlab breaks lines only at spaces, causing ugly splits like "Claude\nCode".
**Fix**: Set `wordWrap='CJK'` on body/bullet styles to allow breaks at CJK character boundaries.

### Songti Reading Needs a Sans Hierarchy

Using one sans family everywhere gives dense Chinese reports a uniform dark texture,
while using Songti everywhere weakens headings and table headers. **Fix**: use the
`songti-reading` theme for Songti SC Regular body text, Palatino Latin prose,
sans-serif Chinese headings/emphasis, Menlo code, wider leading, and serif table
bodies. Keep this as an explicit theme rather than silently changing every report.

On macOS, `Songti.ttc` index 0 is Songti SC Black, not Regular. The readable face is
index 6. Common report symbols such as `✓`, `✗`, and `→` need an explicit symbol-font
fallback or they may render as `□` even when the surrounding Chinese is correct.

### Canvas Text with CJK (Cover/Footer)

`drawString()` / `drawCentredString()` with a Latin font can't render 年/月/日 etc.
**Fix**: Use `_draw_mixed()` for ALL user-content canvas text (dates, stats, disclaimers).

### Images Silently Dropped (Relative Paths)

An image reference to `charts/chart_01.png` in a markdown file used to get skipped without warning
because the image path was resolved against the current working directory, not the
markdown's directory. **Fix**: `main()` now passes `input_dir` (the .md's directory)
into the builder, and the image handler resolves relative paths against it. Missing
images now also emit a `WARN: image not found: ...` to stderr instead of silently
dropping.

### Multi-Line Image References (pandoc `--wrap=auto`)

When feeding pandoc's output into md2pdf, pandoc's default `--wrap=auto` (72 cols)
wraps long image references to paths such as `path.png` across multiple lines, which defeated
the single-line image regex. **Fix**: `_preprocess_md()` now collapses multi-line
image references into one line (outside code fences) before parsing.

**Pipeline tip:** If you're piping HTML → markdown via pandoc, use
`pandoc --wrap=none input.html -o output.md` to avoid wrap-related parsing issues
for images and tables alike.

## Input Format

This skill takes **Markdown files only** as input. If you have HTML, DOCX, or
other formats, convert them to markdown first (e.g. `pandoc --wrap=none`).
Embedded HTML blocks in markdown are passed through as text — pre-process any
visual content (charts, complex tables) into plain markdown tables or image
references before invoking md2pdf.

## Configuration Reference

Most options can also be set in top-of-file YAML-style frontmatter. Explicit CLI
arguments take precedence over frontmatter values.

| Argument | Frontmatter Key | Default | Description |
|----------|----------------|---------|-------------|
| `--input` | — | (required) | Path to markdown file |
| `--output` | — | `output.pdf` | Output PDF path |
| `--title` | `title` | From first H1 | Document title for cover page |
| `--subtitle` | `subtitle` | `""` | Subtitle text |
| `--author` | `author` | `""` | Author name |
| `--date` | `date` | Today | Date string |
| `--version` | `version` | `""` | Version string for cover |
| `--watermark` | `watermark` | `""` | Watermark text (empty = none) |
| `--theme` | `theme` | content-aware `auto` | Color theme name; explicit and saved preferences take precedence |
| `--theme-file` | — | `""` | Custom theme JSON file path |
| `--cover` | `cover` | `true` | Generate cover page |
| `--toc` | `toc` | `true` | Generate table of contents |
| `--page-size` | `page-size` | `A4` | Page size (A4 or Letter) |
| `--frontispiece` | `frontispiece` | `""` | Full-page image after cover |
| `--banner` | `banner` | bundled `assets/backcover-banner.jpg` | Back cover banner image (pass `none` to disable) |
| `--header-title` | `header-title` | `""` | Report title in page header |
| `--footer-left` | `footer-left` | author | Brand/author in footer |
| `--stats-line` | `stats-line` | `""` | Stats on cover |
| `--stats-line2` | `stats-line2` | `""` | Second stats line |
| `--edition-line` | `edition-line` | `""` | Edition line at cover bottom |
| `--disclaimer` | `disclaimer` | `""` | Back cover disclaimer |
| `--copyright` | `copyright` | `""` | Back cover copyright |
| `--code-max-lines` | `code-max-lines` | `30` | Max lines per code block |
| `--image-cover` | `image-cover` | `false` | Use frontispiece as full-bleed cover (page 1), text cover becomes page 2 |
| `--heading-top-spacer` | `heading-top-spacer` | `5` | Top spacer before H1/H2 chapter titles in mm |
| `--wm-size` | `wm-size` | auto (half page width) | Watermark font size; auto-scales so text width ≈ 50% of page width |
| `--wm-opacity` | `wm-opacity` | `0.1` | Watermark opacity (0.0–1.0) |
| `--wm-angle` | `wm-angle` | `35` | Watermark rotation angle in degrees |
| `--wm-spacing-x` | `wm-spacing-x` | `9999` | Watermark horizontal spacing in pt (≥2000 = single centered per page) |
| `--wm-spacing-y` | `wm-spacing-y` | `9999` | Watermark vertical spacing in pt (≥2000 = single centered per page) |

## Themes

Available: `songti-reading`, `warm-academic`, `nord-frost`, `github-light`,
`solarized-light`, `paper-classic`, `ocean-breeze`, `monokai-warm`,
`dracula-soft`, `tufte`, `classic-thesis`, `ieee-journal`, `elegant-book`,
`chinese-red`, `ink-wash`, and `consulting-navy`.

Each theme defines: page background, ink color, accent color, faded text, border, code background, watermark tint.

## Fallback: pandoc + XeLaTeX

When reportlab fails (e.g. wide/complex tables cause infinite loops in table width
calculation), fall back to pandoc with XeLaTeX. This produces high-quality CJK PDFs
with proper table handling.

### When to use pandoc engine

- User chose `latex-clean` theme (k) — pandoc is the primary engine, not a fallback
- Document has many wide multi-column tables (reportlab's table layout may hang)
- Document needs LaTeX-quality typesetting (justified text, hyphenation)
- reportlab md2pdf.py hangs or crashes on the input

### Basic command

    pandoc input.md -o output.pdf \
      --pdf-engine=xelatex \
      -V CJKmainfont="Songti SC" -V mainfont="Palatino" -V monofont="Menlo" \
      -V geometry:margin=2.5cm -V fontsize=11pt \
      --toc -V toc-title="目录" -V documentclass=article

### Adding watermark + headers/footers

    pandoc input.md -o output.pdf \
      --pdf-engine=xelatex \
      -V CJKmainfont="Songti SC" -V mainfont="Palatino" -V monofont="Menlo" \
      -V geometry:margin=2.5cm -V fontsize=11pt \
      -V colorlinks=true -V linkcolor=red -V toccolor=red -V urlcolor=red \
      --toc -V toc-title="目录" -V documentclass=article \
      -V header-includes='
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhf{}
    \fancyhead[L]{\small 页眉左侧文字}
    \fancyhead[R]{\small 页眉右侧文字}
    \fancyfoot[C]{\thepage}
    \usepackage{draftwatermark}
    \SetWatermarkText{水印文字}
    \SetWatermarkScale{0.5}
    \SetWatermarkColor[gray]{0.9}
    '

### Pandoc theme presets

Each preset defines a complete set of pandoc `-V` flags. Use the full command from
"Adding watermark + headers/footers" above, replacing the color/link flags per preset.

| Theme | linkcolor | toccolor | urlcolor | Watermark color | Notes |
|-------|-----------|----------|----------|-----------------|-------|
| chinese-red | `red` | `red` | `red` | `[gray]{0.9}` | 朱红正式，适合政企报告、白皮书 |
| warm-academic | `brown` | `brown` | `brown` | `[gray]{0.9}` | 陶土色调，温润学术风 |
| classic-thesis | `brown` | `brown` | `brown` | `[gray]{0.85}` | LaTeX classicthesis 灵感 |
| ieee-journal | `blue` | `blue` | `blue` | `[gray]{0.9}` | 藏蓝严谨，期刊风格 |
| github-light | `blue` | `blue` | `blue` | `[gray]{0.92}` | 极简蓝白，程序员友好 |
| ink-wash | `black` | `black` | `black` | `[gray]{0.92}` | 水墨素雅，文学/设计类 |
| nord-frost | `teal` | `teal` | `teal` | `[gray]{0.9}` | 北欧冰霜蓝灰 |
| consulting-navy | `blue` | `blue` | `blue` | `[gray]{0.88}` | 咨询深蓝，研究报告风 |

#### chinese-red 完整示例（本次一滕项目实际使用）

    pandoc input.md -o output.pdf \
      --pdf-engine=xelatex \
      -V CJKmainfont="Songti SC" -V mainfont="Palatino" -V monofont="Menlo" \
      -V geometry:margin=2.5cm -V fontsize=11pt \
      -V colorlinks=true -V linkcolor=red -V toccolor=red -V urlcolor=red \
      --toc -V toc-title="目录" -V documentclass=article \
      -V header-includes='
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhf{}
    \fancyhead[L]{\small 报告标题 | 品牌名}
    \fancyhead[R]{\small 商业机密}
    \fancyfoot[C]{\thepage}
    \usepackage{draftwatermark}
    \SetWatermarkText{商业机密}
    \SetWatermarkScale{0.5}
    \SetWatermarkColor[gray]{0.9}
    '

#### latex-clean 完整示例（最简洁的 LaTeX 学术风格）

选择 `latex-clean` 时，**跳过 reportlab**，直接使用 pandoc 生成。特点：无封面、无扉页、
无装饰色块，纯 LaTeX 排版 + 点线 TOC 引导符，适合内容为王的学术/技术文档。

    pandoc input.md -o output.pdf \
      --pdf-engine=xelatex \
      -V CJKmainfont="Songti SC" -V mainfont="Palatino" -V monofont="Menlo" \
      -V geometry:margin=2.5cm -V fontsize=11pt \
      -V colorlinks=true -V linkcolor=brown -V toccolor=brown -V urlcolor=brown \
      --toc -V toc-title="目录" -V documentclass=article

如需添加页眉页脚或水印，参考上方 "Adding watermark + headers/footers" 追加 `-V header-includes`。

### Known limitations (pandoc fallback)

- No cover page (pandoc article class has no built-in cover — use `--include-before-body` with a LaTeX snippet if needed)
- Frontispiece/back cover not supported (use md2pdf.py for these)
- `→` `★` `☆` symbols may warn in Palatino — they render via CJK font fallback, safe to ignore
- ASCII art diagrams render as code blocks (same as md2pdf.py)

### Dependencies (pandoc fallback)

Requires `pandoc` and a TeX distribution with XeLaTeX:

    brew install pandoc
    brew install --cask mactex-no-gui   # or basictex

## Dependencies

```bash
pip install reportlab --break-system-packages
# Optional formula rendering:
pip install matplotlib --break-system-packages
```

Recommended Ubuntu/Debian fonts:

```bash
sudo apt install fonts-dejavu-core fonts-liberation fonts-freefont-ttf fonts-noto fonts-noto-cjk fonts-noto-color-emoji
```

## Runtime context (shared)

运行前读取本 Skill 包的 `skill.yaml`，由宿主提供 `skill-runtime/v1` 上下文。字段解析顺序为：当前请求、项目上下文、个人 Preferences、品牌 Profile、通用默认值。

- 只使用 Manifest 声明的字段；Profile 保存公开品牌事实，Preferences 保存个人工作偏好。
- `required: true` 字段缺失时，按 Manifest 的问题配置向用户提出一个聚焦问题；用户明确同意后再保存回答。
- 报错提供可复制的 `context_id`、字段路径与来源，诊断内容避开秘密、完整私人路径和原始配置。

## 通用反馈闭环

用户在 Skill 驱动任务中提出修改意见时，继续当前产物前必须执行：

1. 先判断意见是 `task-specific`（仅本次）还是 `reusable`（可跨任务复用）。
2. `task-specific` 只修改当前任务，不改 Skill。
3. `reusable` 先确定作用域：领域规则先更新对应 canonical Skill；适用于所有 Skill 的规则先更新共享规范。
4. 完成规则更新、版本、lint 与分发核验后，再把修改应用到当前任务。
5. `reusable` 修改会使此前的“确认”“继续”“发吧”失效；完成当前产物修改和回读后必须停下，等待用户下一步指示，不自动进入发布、提交或其他外部写入。
