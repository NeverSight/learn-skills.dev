---
name: slidekit-create
description: Generate HTML slide presentations (1 slide = 1 HTML file, 1280x720px) using Tailwind CSS, Font Awesome, and Google Fonts. Use when the user asks to create a new presentation deck or slide HTML files. Covers design guidelines, 43 layout patterns, component library, and PPTX conversion compatibility rules. Supports style selection (creative, elegant, modern, professional, minimalist) and theme selection (marketing, portfolio, business, technology, education).
---

# SlideKit Create

**All communication with the user MUST be in Japanese.** Questions, confirmations, progress updates, and any other messages — always use Japanese.

Generate HTML files forming a complete presentation deck. Each file is a self-contained HTML document rendered at **1280 x 720 px**. All content is pure HTML + CSS. Chart.js is used automatically when data visualizations require it (line charts, radar charts, etc.) — no other JavaScript is permitted.

For DOM snippets and component patterns, see [references/patterns.md](references/patterns.md).
For user-provided custom templates, see [references/templates/](references/templates/).

---

## Workflow Overview

| Phase | Name | Description |
|-------|------|-------------|
| 0 | テンプレート検出・読み込み | templates/ を確認し、テンプレートモード or 通常モードを決定 |
| 1 | ヒアリング | モードに応じた質問でスライドの要件を確認 |
| 2 | デザイン決定 | カラーパレット・フォント・アイコンを確定 |
| 3 | スライド構成の設計 | 各スライドの役割・レイアウトパターンを計画 |
| 4 | HTML生成 | 全スライドを 001.html 〜 NNN.html として出力 |
| 5 | print.html 生成 | 全スライド一覧表示用ページを出力 |
| 6 | チェックリスト確認 | 制約・品質基準への適合を検証 |
| 7 | PPTX変換（任意） | /pptx スキルで PowerPoint に変換 |

---

## Phase 0: テンプレート検出・読み込み

Before starting the hearing, check `references/templates/` for user-provided HTML template files.

### 0-1. テンプレートの検出

Scan `references/templates/` for **both** subdirectories and loose `.html` files.

- **Subdirectories** — each subdirectory is treated as a separate template set (e.g., `templates/navy-gold/`, `templates/modern-tech/`)
- **Loose HTML files** — `.html` files directly under `references/templates/` are treated as a single template set named "default"

If nothing is found (no subdirectories and no HTML files) → proceed to Phase 1 in **通常モード**.

### 0-2. テンプレート選択

If templates are found, present them to the user and ask which to use.

**When multiple template sets (subdirectories) exist:**

> 「以下のカスタムテンプレートが見つかりました。どのテンプレートを使用しますか？番号で選択してください。」
>
> 1. {directory-name-1}/（{N}ファイル）
> 2. {directory-name-2}/（{N}ファイル）
> 3. 使用しない（通常モードで作成）

- **1 or 2 (directory number)** → that directory's HTML files become the template set. Proceed to 0-3
- **3 (使用しない)** → proceed to Phase 1 in **通常モード**

**When a single template set exists (one subdirectory, or loose HTML files only):**

> 「以下のカスタムテンプレートが見つかりました。使用しますか？番号で選択してください。」
>
> - {file1.html}, {file2.html}, ...
>
> 1. はい — このテンプレートを使用する
> 2. いいえ — 使用しない（通常モードで作成）

- **1** → proceed to 0-3
- **2** → proceed to Phase 1 in **通常モード**

### 0-3. テンプレート読み込み

Read the selected template files and extract:

- Color palette (CSS custom properties / Tailwind classes)
- Font pair (primary JP + accent Latin)
- Header/footer structure and style
- Decorative elements and visual motifs
- Layout patterns used

Proceed to Phase 1 in **テンプレートモード**.

### Cautions

- **Mandatory Constraints still apply.** Even if a custom template uses `<table>` or non-CDN assets, the generated output must follow all rules in the Mandatory Constraints section below. Extract only the visual design (colors, fonts, spacing, decorative style) — not non-compliant implementation details.
- **Slide size must remain 1280x720px.** Ignore any different dimensions in custom templates.
- **Do not copy text content.** Custom templates are style references only. All text content comes from Phase 1 hearing.
- **Maximum 5 template files per set.** If a template set contains more than 5 HTML files, read only the first 5 (sorted alphabetically) to limit context usage. Warn the user that remaining files were skipped.
- **Supported format: HTML only.** Ignore non-HTML files (images, PDFs, etc.) in the templates directory.

---

## Phase 1: ヒアリング

Before generating any files, ask the user questions to capture intent. **All questions must be asked in Japanese.**

**Important rules:**

- **1ターン1質問**: Ask only one question per message. Wait for the user's answer before asking the next question.
- **番号選択**: All questions with predefined options must be presented as numbered lists. The user answers by entering the number only. Questions requiring free text input (directory path, title, company name, etc.) are the exception.

The hearing questions differ depending on the mode determined in Phase 0.

### テンプレートモード（テンプレートあり）

When custom templates were loaded in Phase 0, **skip all design-related questions** and ask only the following:

1. **出力ディレクトリ** — same as 1-1 below
2. **スライド内容のソース** — same as 1-4 below
3. **プレゼンタイトル** — same as 1-5 below
4. **スライド枚数** — same as 1-6 below
5. **会社名・ブランド名** — same as 1-7 below
6. **テンプレートデザインの確認** — present the extracted design (colors, fonts, decorative style) to the user and ask:

> 「テンプレートから以下のデザインを検出しました。」
>
> - カラー: {extracted colors}
> - フォント: {extracted fonts}
> - ヘッダー/フッター: {extracted structure}
>
> 「このデザインをどうしますか？番号で選択してください。」
>
> 1. そのまま使用する
> 2. 一部変更したい

- **1** → Phase 2 でテンプレートのデザインをそのまま確定
- **2** → 変更したい項目（カラー、フォント等）を聞き、テンプレートのデザインを部分的に上書き

### 通常モード（テンプレートなし）

Ask all of the following questions (1-1 through 1-9).

### 1-1. 出力ディレクトリ

> 「出力先ディレクトリを選択してください。番号で回答するか、パスを直接入力してください。」
>
> 1. デフォルト（`output/slide-page{NN}/`）
> 2. パスを指定する

- **1** → use `output/slide-page{NN}/` (NN = next sequential number based on existing directories)
- **2** → follow up by asking for the path (text input)
- **Direct path input** → if the user directly types a path instead of a number, use that path

### 1-2. スタイル選択

> 「スタイルを選択してください。番号で回答してください。」
>
> 1. **Creative** — 大胆な配色、装飾要素、グラデーション、遊び心のあるレイアウト
> 2. **Elegant** — 落ち着いたパレット（ゴールド系）、セリフ寄りのタイポグラフィ、広めの余白
> 3. **Modern** — フラットデザイン、鮮やかなアクセントカラー、シャープなエッジ、テック志向
> 4. **Professional** — ネイビー/グレー系、構造的なレイアウト、情報密度高め
> 5. **Minimalist** — 少ない色数、極端な余白、タイポグラフィ主導、最小限の装飾

### 1-3. テーマ選択

> 「テーマを選択してください。番号で回答してください。」
>
> 1. **Marketing** — 製品発表、キャンペーン提案、市場分析
> 2. **Portfolio** — ケーススタディ、実績紹介、作品集
> 3. **Business** — 事業計画、経営レポート、戦略提案、投資家ピッチ
> 4. **Technology** — SaaS紹介、技術提案、DX推進、AI/データ分析
> 5. **Education** — 研修資料、セミナー、ワークショップ、社内勉強会

### 1-4. スライド内容のソース

Ask the user how they want to provide the content for the slides. This determines what text, data, and structure will appear in the deck.

> 「スライドの内容をどのように提供しますか？番号で回答してください。」
>
> 1. **参考ファイル** — ファイル（Markdown、テキスト、Wordなど）を指定する
> 2. **直接入力** — チャットにテキストを入力する
> 3. **トピックのみ** — テーマだけ指定してClaude に内容を生成させる

**When a reference file is provided:**

1. Read the entire file
2. Extract the logical structure (headings, sections, bullet points, data)
3. Map the structure to the slide sequence — each major section becomes a section divider + content slides
4. Preserve key text, numbers, and data points faithfully
5. Adapt the content to fit the slide format (concise bullet points, not full paragraphs)

**When direct text is provided:**

1. Organize the text into a logical presentation flow
2. Ask clarifying questions if the structure is ambiguous

**When only a topic is given:**

1. Ask about the target audience (executives, engineers, clients, etc.)
2. Ask about key messages or points the user wants to convey
3. Generate content based on the answers

### 1-5. プレゼンタイトル

Ask for the presentation title. Skip if already clear from the content source in 1-4.

### 1-6. スライド枚数

> 「スライド枚数を選択してください。番号で回答してください。」
>
> 1. 10枚
> 2. 15枚
> 3. 20枚（推奨）
> 4. 25枚
> 5. 自動（内容に応じて最適な枚数を決定）

- **5（自動）** を選択した場合の判断基準:
  - Reference file: count the major sections/headings → each section ≈ 1 divider + 2-3 content slides, plus cover/agenda/summary/closing
  - Direct text: estimate from the volume and structure of the provided text
  - Topic only: default to 15-20 based on topic complexity
- When 5 is selected, inform the user of the determined count before proceeding (e.g., "内容から判断して18枚で作成します。よろしいですか？")

### 1-7. 会社名・ブランド名

Ask for the company or brand name to display in the header/footer.

### 1-8. カラーの希望

> 「カラーに希望はありますか？番号で回答してください。」
>
> 1. おまかせ（スタイル × テーマに基づいて自動提案）
> 2. 指定したい（次の質問でカラーコードや色名を入力）

- **1** → auto-suggest based on the selected style × theme combination
- **2** → follow up by asking for specific color codes or color names (text input)

### 1-9. 背景画像の使用

> 「背景画像を使用しますか？番号で回答してください。」
>
> 1. 使用しない（CSSグラデーションのみ）
> 2. 使用する（次の質問で画像を指定）

- **1** → no background images (CSS gradients only)
- **2** → follow up by asking the user to provide or approve specific images

---

## Phase 2: デザイン決定

Determine the following **before generating any HTML**:

### テンプレートモード

If custom templates were loaded in Phase 0:

1. **Color palette** — use the palette extracted from the template (or with user-requested modifications from Phase 1)
2. **Font pair** — use the fonts extracted from the template (or with user-requested modifications from Phase 1)
3. **Brand icon** (1 Font Awesome icon)

If the user confirmed the template design as-is in Phase 1, present a brief summary and proceed. If the user requested partial changes, apply those changes and present the updated design for confirmation.

### 通常モード

Based on Phase 1 hearing results, determine:

1. **Color palette** (3-4 custom colors)
2. **Font pair** (1 Japanese + 1 Latin)
3. **Brand icon** (1 Font Awesome icon)

Present the design decisions to the user for confirmation before proceeding.

### Proven Palette Examples

| Template | Style | Primary Dark | Accent | Secondary | Fonts |
|----------|-------|-------------|--------|-----------|-------|
| 01 Navy & Gold | Elegant | `#0F2027` | `#C5A065` | `#2C5364` | Noto Sans JP + Lato |
| 02 Casual Biz | Professional | `#1f2937` | Indigo | `#F97316` | Noto Sans JP |
| 03 Blue & Orange | Professional | `#333333` | `#007BFF` | `#F59E0B` | BIZ UDGothic |
| 04 Green Forest | Modern | `#1B4332` | `#40916C` | `#52B788` | Noto Sans JP + Inter |
| 05 Dark Tech | Creative | `#0F172A` | `#F97316` | `#3B82F6` | Noto Sans JP + Inter |

---

## Phase 3: スライド構成の設計

Plan the full deck structure before writing any HTML. This phase produces a slide map.

### 3-1. Required Slides (All Decks)

| Position | Type | Pattern | Category |
|----------|------|---------|----------|
| First | Cover | Center | `cover` |
| Second | Agenda | HBF | `agenda` |
| Second to last | Summary | HBF | `conclusion` |
| Last | Closing | Full-bleed / Center | `conclusion` |

### 3-2. Section Dividers by Slide Count

| Slides | Section Dividers | Content Slides |
|--------|-----------------|----------------|
| **10** | 2 | 4 |
| **15** | 3 | 8 |
| **20** | 4 | 12 |
| **25** | 5 | 16 |

### 3-3. Build the Slide Map

For each slide, determine:

1. **File number** (`001.html`, `002.html`, ...)
2. **Type** (Cover / Agenda / Section Divider / Content / Summary / Closing)
3. **Layout pattern** (from the 43 patterns — see Phase 4 reference)
4. **Content summary** (what text/data goes on this slide)

Rules:
- Never use the same layout pattern for 3 or more consecutive slides
- Match content from Phase 1-3 (reference file / text / topic) to appropriate slide types
- Use good variety across the 43 layout patterns
- **Chart.js auto-detection:** For slides with data visualizations, decide whether to use Chart.js or CSS-only based on the "When to Use Chart.js vs CSS-Only" table in [references/patterns.md](references/patterns.md). Mark Chart.js slides in the slide map. CSS-only and Chart.js charts can coexist in the same deck

### 3-4. Standard Composition for 20 Slides (Reference)

| File | Type | Pattern | Purpose |
|------|------|---------|---------|
| `001.html` | Cover | Center | Title, subtitle, presenter, date |
| `002.html` | Agenda | HBF | Numbered section list |
| `003.html` | Section Divider 1 | Left-Right Split | Section 1 introduction |
| `004.html` | Content | HBF + Top-Bottom Split | Challenges vs. solutions + KPI |
| `005.html` | Content | HBF + 2-Column | Comparison / contrast |
| `006.html` | Section Divider 2 | Left-Right Split | Section 2 introduction |
| `007.html` | Content | HBF + 3-Column | 3-item cards |
| `008.html` | Content | HBF + Grid Table | Competitive comparison table |
| `009.html` | Content | HBF + 2x2 Grid | Risk analysis / SWOT |
| `010.html` | Section Divider 3 | Left-Right Split | Section 3 introduction |
| `011.html` | Content | HBF + N-Column | Process flow |
| `012.html` | Content | HBF + Timeline/Roadmap | Quarterly roadmap |
| `013.html` | Content | HBF + KPI Dashboard | KPI cards + CSS bar chart |
| `014.html` | Section Divider 4 | Left-Right Split | Section 4 introduction |
| `015.html` | Content | HBF + Funnel | Conversion funnel |
| `016.html` | Content | HBF + Vertical Stack | Architecture / org chart |
| `017.html` | Content | HBF + 3-Column | Strategy / policy (3 pillars) |
| `018.html` | Content | HBF + 2-Column | Detailed analysis / data |
| `019.html` | Summary | HBF | Key takeaways + next actions |
| `020.html` | Closing | Full-bleed / Center | Thank-you slide + contact info |

---

## Phase 4: HTML生成

Generate all slide HTML files based on the slide map from Phase 3.

### 4-1. For Each Slide

1. Use the HTML Boilerplate (below)
2. Apply the design decisions from Phase 2 (colors, fonts, icon)
3. Use the layout pattern assigned in Phase 3
4. Fill in the content from Phase 1-3 (reference file / text / generated)
5. **If the slide is marked "Chart.js" in the slide map:** use Chart.js `<canvas>` patterns from [references/patterns.md](references/patterns.md) (Chart.js Patterns section). Include the Chart.js CDN `<script>` in `<head>` and initialization `<script>` before `</body>`
6. Save as `{output_dir}/{NNN}.html` (zero-padded: 001.html, 002.html, ...)

### HTML Boilerplate

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>{Slide Title}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family={PrimaryFont}:wght@300;400;500;700;900&family={AccentFont}:wght@400;600;700&display=swap" rel="stylesheet" />
    <!-- Chart.js (only on slides marked "Chart.js" in Phase 3) -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> -->
    <style>
        body { margin: 0; padding: 0; font-family: '{PrimaryFont}', sans-serif; overflow: hidden; }
        .font-accent { font-family: '{AccentFont}', sans-serif; }
        .slide { width: 1280px; height: 720px; position: relative; overflow: hidden; background: #FFFFFF; }
        /* Custom color classes: .bg-brand-dark, .bg-brand-accent, .bg-brand-warm, etc. */
    </style>
</head>
<body>
    <div class="slide {layout-classes}">
        <!-- Content -->
    </div>
    <!-- Chart.js initialization (only on slides that contain charts) -->
    <!-- <script> new Chart(...) </script> -->
</body>
</html>
```

**Chart.js CDN inclusion rules:**
- Only uncomment the `<script src="...chart.js...">` line on slides marked "Chart.js" in the Phase 3 slide map
- Only add the Chart.js CDN to slides that actually contain a `<canvas>` chart — do not include it on every slide
- The `<script>` for Chart initialization must be placed just before `</body>`, **after** the slide `<div>`
- Each chart `<canvas>` must have a unique `id` attribute

### 43 Layout Patterns

Use one pattern per slide. For full DOM trees and component snippets, see [references/patterns.md](references/patterns.md).

| # | Pattern | Root classes | When to use |
|---|---------|-------------|-------------|
| 1 | **Center** | `flex flex-col items-center justify-center` | Cover, thank-you slides |
| 2 | **Left-Right Split** | `flex` with `w-1/3` + `w-2/3` | Chapter dividers, concept + detail |
| 3 | **Header-Body-Footer** | `flex flex-col` with header + `flex-1` + footer | Most content slides (default) |
| 4 | **HBF + 2-Column** | Pattern 3 body with two `w-1/2` | Comparison, data + explanation |
| 5 | **HBF + 3-Column** | Pattern 3 body with `grid grid-cols-3` | Card listings, 3-way comparison |
| 6 | **HBF + N-Column** | Pattern 3 body with `grid grid-cols-{N}` | Process flows (max 5 cols) |
| 7 | **Full-bleed** | `relative` with `absolute inset-0` layers | Impact covers (CSS gradient default) |
| 8 | **HBF + Top-Bottom Split** | Pattern 3 body with `flex flex-col` two sections | Content top + KPI/summary bar bottom |
| 9 | **HBF + Timeline/Roadmap** | Pattern 3 body with timeline bar + `grid grid-cols-4` | Quarterly roadmaps, phased plans |
| 10 | **HBF + KPI Dashboard** | Pattern 3 body with KPI `grid` + `flex-1` chart area | KPI cards + chart/progress visualization |
| 11 | **HBF + Grid Table** | Pattern 3 body with flex-based rows (`w-1/N`) | Feature comparison, competitive analysis |
| 12 | **HBF + Funnel** | Pattern 3 body with decreasing-width centered bars | Conversion funnel, sales pipeline |
| 13 | **HBF + Vertical Stack** | Pattern 3 body with stacked full-width cards + separators | Architecture diagrams, layered systems |
| 14 | **HBF + 2x2 Grid** | Pattern 3 body with `grid grid-cols-2` (2 rows) | Risk analysis, SWOT, feature overview |
| 15 | **HBF + Stacked Cards** | Pattern 3 body with vertically stacked full-width cards + numbered badges | FAQ, Q&A, numbered key points, interview summary |
| 16 | **HBF + TAM/SAM/SOM** | Pattern 3 body with description list + nested circles or horizontal bars | Market size visualization (2 variants) |
| 17 | **Chapter Divider** | `flex` with `w-1/4` dark + `w-3/4` light (no HBF) | Chapter/section dividers with large number |
| 18 | **HBF + Contact** | Pattern 3 body with `w-1/2` message + `w-1/2` contact card | Contact info, CTA slides |
| 19 | **HBF + 5-Column Process** | Pattern 3 body with `grid grid-cols-5` + optional RACI box | 5-step process flows, methodology |
| 20 | **HBF + VS Comparison** | Pattern 3 body with two cards + central VS badge | Head-to-head competitor comparison |
| 21 | **Section End / Summary** | `flex flex-col` with numbered key points + accent border | Section closing, key takeaways |
| 22 | **Table of Contents** | `flex flex-col` with numbered agenda items + active highlight | Agenda, table of contents |
| 23 | **HBF + 2×3 Grid** | Pattern 3 body with `grid grid-cols-3 grid-rows-2` | 6-element overview, feature grid |
| 24 | **HBF + Icon List** | Pattern 3 body with icon circles + text rows | Feature lists, benefit highlights |
| 25 | **HBF + Image Header Panel** | Pattern 3 body with image-topped cards | Visual category cards |
| 26 | **HBF + Emphasis Panel** | Pattern 3 body with left-border accent panels | Key message emphasis, callouts |
| 27 | **Glass Panel (Dark)** | `relative` dark bg + `backdrop-blur` glass panels | Premium dark-theme content |
| 28 | **HBF + Gradient Panel** | Pattern 3 body with gradient-bg panels | Highlighted content sections |
| 29 | **HBF + Card Layout with Image** | Pattern 3 body with icon + description cards | Service/product feature cards |
| 30 | **Right-Side Background Image** | `flex` with text left + image right (`w-2/5`) | Text + supporting image |
| 31 | **Quote Slide** | `flex flex-col items-center justify-center` with large quotation marks | Inspirational quotes, testimonials |
| 32 | **Multiple Images Split** | `flex` with multiple image panels side by side | Photo gallery, visual comparison |
| 33 | **Statistics Emphasis** | Pattern 3 body with large stat numbers + labels | KPI highlights, data callouts |
| 34 | **Center Message** | `flex flex-col items-center justify-center` with single message | Key statement, transition message |
| 35 | **Q&A Slide** | Centered large "Q&A" text with subtitle | Question & answer session |
| 36 | **Question Slide** | Centered question mark with audience prompt | Audience engagement, reflection |
| 37 | **Movie / Book Quote** | `flex` with dark accent bar + quote + attribution | Famous quotes, literary references |
| 38 | **HBF + Inline Image** | Pattern 3 body with image + numbered text items | Image-supported explanations |
| 39 | **HBF + Statistics Ratio** | Pattern 3 body with vertical bar chart comparison | Ratio visualization, benchmarks |
| 40 | **HBF + Text + Stats Panel** | Pattern 3 body with text block + stat cards | Mixed narrative + data |
| 41 | **Summary Glass Vertical** | Dark bg + vertical glass panels with key points | Premium summary, dark-theme recap |
| 42 | **HBF + Simple List + Supplement** | Pattern 3 with bullet list (60%) + supplement panel (40%) | Lists with additional context |
| 43 | **HBF + Case Study** | Pattern 3 with challenge → solution → result flow | Company case studies, success stories |

### Heading Convention

Bilingual: small English label above, larger Japanese title below.

```html
<p class="text-xs uppercase tracking-widest text-gray-400 mb-1 font-accent">Market Analysis</p>
<h1 class="text-3xl font-bold text-brand-dark">市場分析</h1>
```

### Number Emphasis Convention

Large digits + small unit span:

```html
<p class="text-4xl font-black font-accent">415<span class="text-sm font-normal ml-1">M</span></p>
```

---

## Phase 5: print.html 生成

After all slide HTML files are generated, create `{output_dir}/print.html` for viewing and printing all slides:

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>View for Print</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #FFFFFF; }
        .slide-frame {
            width: 1280px; height: 720px;
            margin: 20px auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            border: 1px solid #e2e8f0;
            overflow: hidden;
        }
        .slide-frame iframe { width: 1280px; height: 720px; border: none; }
        @media print {
            body { background: #FFFFFF; }
            .slide-frame {
                page-break-after: always; box-shadow: none; border: none;
                margin: 0 auto;
                transform: scale(0.85); transform-origin: top center;
            }
        }
    </style>
</head>
<body>
    <!-- One iframe per slide -->
    <div class="slide-frame"><iframe src="001.html"></iframe></div>
    <!-- ... repeat for all slides ... -->
</body>
</html>
```

Add one `<div class="slide-frame"><iframe src="{NNN}.html"></iframe></div>` per slide.

---

## Phase 6: チェックリスト確認

After Phase 4 and Phase 5 are complete, verify the following. Fix any issues before delivering to the user.

- [ ] All files use identical CDN links
- [ ] Custom colors defined identically in every `<style>`
- [ ] Root is single `<div>` under `<body>` with `overflow: hidden` (only sibling allowed: Chart.js `<script>` on chart slides)
- [ ] Slide size exactly 1280 x 720
- [ ] No external images (unless user approved)
- [ ] No JavaScript except Chart.js on chart slides (no other `<script>` tags allowed)
- [ ] All files for the chosen slide count are present
- [ ] Font sizes follow hierarchy
- [ ] Consistent header/footer on content slides
- [ ] Page numbers increment correctly
- [ ] `Confidential` in footer
- [ ] Decorative elements use low z-index and low opacity
- [ ] File naming: zero-padded 3 digits (`001.html`, `002.html`, ...)
- [ ] Text uses `<p>` / `<h*>` (not `<div>`)
- [ ] No visible text in `::before` / `::after`
- [ ] No one-off colors outside palette
- [ ] Content density guidelines followed
- [ ] `print.html` generated with iframes for all slides

---

## Phase 7: PPTX変換（任意）

After all checks pass, ask the user in Japanese:

> 「HTMLスライドの生成が完了しました。PowerPoint（PPTX）に変換しますか？」

If the user declines, the workflow ends here.

### Prerequisite Check

Before invoking the pptx skill, verify it is available by checking the list of available skills in the current session. The pptx skill will appear in the system's skill list if installed.

**If the pptx skill is NOT available**, inform the user and provide installation instructions:

> `/pptx` スキルが必要ですが、現在インストールされていません。
>
> 以下のコマンドでインストールできます:
>
> ```
> claude install-skill https://github.com/anthropics/claude-code-agent-skills/tree/main/skills/pptx
> ```
>
> インストール後、新しいセッションで `/pptx` を実行し、出力ディレクトリ `{output_dir}` を指定してください。

Then end the workflow. Do not attempt conversion without the pptx skill.

### Chart.js Slides and PPTX Conversion

When the deck contains Chart.js `<canvas>` charts (determined in Phase 3):

1. **Chart slides require screenshot-based conversion.** The pptx converter cannot parse `<canvas>` elements rendered by JavaScript. Chart.js charts will be captured as raster images (PNG) and embedded in the PPTX slide
2. **Non-chart elements remain editable.** Text, icons, and CSS-only elements on the same slide are still extracted as native PPTX objects
3. **Inform the pptx skill** which slides contain Chart.js so it can apply the screenshot fallback selectively

### Invocation (pptx skill available)

If the pptx skill is available, invoke `/pptx` using the Skill tool. Pass the following context:

1. **Source directory** — the output path containing all `NNN.html` files
2. **Slide count** — total number of HTML files
3. **Presentation title** — from Phase 1 hearing
4. **Color palette** — the 3-4 brand colors chosen in Phase 2
5. **Font pair** — primary (JP) and accent (Latin) fonts

Example invocation prompt for the Skill tool:

```
Convert the HTML slide deck in {output_dir} to a single PPTX file.
- {N} slides (001.html through {NNN}.html)
- Title: {title}
- Colors: {primary_dark}, {accent}, {secondary}
- Fonts: {primary_font} + {accent_font}
- Chart.js slides: {list of slide numbers, e.g., "004, 013" or "none"}
- Output: {output_dir}/presentation.pptx
```

**Important:** Do not attempt HTML-to-PPTX conversion yourself. Always delegate to the `/pptx` skill, which has its own specialized workflow, QA process, and conversion tools.

---

## Reference: Mandatory Constraints

| Rule | Value |
|------|-------|
| Slide size | `width: 1280px; height: 720px` |
| CSS framework | Tailwind CSS 2.2.19 via CDN |
| Icons | Font Awesome 6.4.0 via CDN |
| Fonts | Google Fonts (1 JP primary + 1 Latin accent) |
| Language | `lang="ja"` |
| Root DOM | `<body>` -> single wrapper `<div>` (only sibling allowed: Chart.js `<script>` on chart slides) |
| Overflow | `overflow: hidden` on root wrapper |
| External images | None by default. Explicit user approval required |
| JavaScript | **Forbidden by default.** Exception: Chart.js is used automatically when data visualizations require it (see Phase 3 auto-detection). No other JS libraries permitted |
| Custom CSS | Inline `<style>` in `<head>` only; no external CSS files |

### PPTX Conversion Rules (Critical)

These directly affect PPTX conversion accuracy. **Always follow.**

- Prefer `<p>` over `<div>` for text (tree-walkers may miss `<div>` text)
- Never put visible text in `::before` / `::after`
- Separate decorative elements with `-z-10` / `z-0`
- Max DOM nesting: 5-6 levels
- Font Awesome icons in `<i>` tags (converter detects `fa-` on `<i>`)
- Use flex-based tables over `<table>`
- `linear-gradient(...)` supported; complex multi-stop may fall back to screenshot
- `box-shadow`, `border-radius`, `opacity` all extractable
- **Chart.js `<canvas>` elements** are not parseable by DOM tree-walkers → require screenshot fallback for PPTX. Prefer CSS-only charts when PPTX editability is a priority

### Anti-Patterns (Avoid)

- Purposeless wrapper `<div>`s (increases nesting)
- One-off colors outside the palette
- `<table>` for layout
- Inline styles that Tailwind can replace
- Text in `::before` / `::after`
- `<div>` for text (use `<p>`, `<h1>`-`<h6>`)

---

## Reference: Design Guidelines

### Color Palette

Define 3-4 custom colors as Tailwind-style utility classes in `<style>`:

| Role | Class Example | Purpose |
|------|---------------|---------|
| Primary Dark | `.bg-brand-dark` | Dark backgrounds, titles |
| Primary Accent | `.bg-brand-accent` | Borders, highlights, icons |
| Warm/Secondary | `.bg-brand-warm` | CTAs, emphasis, badges |
| Body text | Tailwind grays | Body, captions |

Keep palette consistent across all slides. No one-off colors.

### Font Pair

| Role | Examples | Usage |
|------|----------|-------|
| Primary (JP) | Noto Sans JP, BIZ UDGothic | Body, headings |
| Accent (Latin) | Lato, Inter, Roboto | Numbers, English labels, page numbers |

Set primary on `body`; define `.font-accent` for the accent font.

### Font Size Hierarchy

| Purpose | Tailwind class |
|---------|---------------|
| Main title | `text-3xl` - `text-6xl` + `font-bold`/`font-black` |
| Section heading | `text-xl` - `text-2xl` + `font-bold` |
| Card heading | `text-lg` + `font-bold` |
| Body text | `text-sm` - `text-base` |
| Caption/label | `text-xs` |

### Content Density Guidelines

| Element | Recommended Max |
|---------|----------------|
| Bullet points | 5-6 |
| Cards per row | 3-4 |
| Body text lines | 6-8 |
| KPI boxes | 4-6 |
| Process steps | 4-5 |
