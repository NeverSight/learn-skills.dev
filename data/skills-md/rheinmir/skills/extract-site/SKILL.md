---
name: extract-site
description: >-
  Extract and convert a website or docs site into clean markdown
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

extract
Convert any website into a complete design system document, or convert between design token formats (DESIGN.md, tokens.json, variables.css, theme.css).

## WHAT

### Purpose và context
- **Purpose:** từ một website công khai, trích design system (màu, typography, spacing, radius, shadow, component + state) thành tài liệu/token (DESIGN.md, preview.html, tokens.json, variables.css, theme.css); hoặc chuyển đổi giữa các định dạng token đó.
- **Trigger (when to use):** hai mode kích hoạt — **Mode 1** lệnh tường minh tiền tố `rico` (`rico DESIGN.md [url]`, `rico tokens [url]`, `rico 全部输出 [brand]`, `rico 把 DESIGN.md 转为 tokens`…), **Mode 2** ngôn ngữ tự nhiên ("Create a DESIGN.md for linear.app", "Extract design tokens from stripe.com"…). Use cases: cần design system doc cho website có sẵn · trích token để implement · chuyển đổi định dạng token · trang tham chiếu trực quan cho design system một brand.
- **Non-goals:** KHÔNG dựng lại nguyên trang thành code chạy được (pixel-perfect) — đó là `/web-clone` Mode B (reconstruct), xem "Mode 3: Full-Clone"; không áp theme vào website của user (đó là rico-ui-ux-themes, xem FAQ); không trích trang cần đăng nhập.

### Mental model
`URL (hoặc file token có sẵn) → gather visual data (screenshot + DevTools) → tokens ngữ nghĩa (colors · typography · spacing · radius · shadows) → components + states → brand voice + Do's/Don'ts → file đầu ra trong themes/{brand-slug}/`. Chuyển đổi định dạng = parse file nguồn → sinh file đích, bỏ bước gather.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | URL công khai hợp lệ | có (trừ khi chuyển đổi định dạng) | `extract DESIGN.md <url>` |
| In | file token nguồn | có khi chuyển đổi | vd DESIGN.md có sẵn → tokens.json |
| In | cờ `--theme=light\|dark`, `--depth=basic\|full`, `--components-only`, `--tokens-only`, `--mobile-first`, `--desktop-first` | không | tinh chỉnh phạm vi trích |
| Out | `themes/{brand-slug}/DESIGN.md` + `preview.html` | mặc định | style reference + trang preview tự chứa |
| Out | `tokens.json` / `variables.css` / `theme.css` | theo lệnh | DTCG · CSS custom properties · Tailwind v4 `@theme` |
| Out | output report `llmwiki/wiki/sources/draft/DDMMYY-<ten>.md` | có (trừ khi 0 artifact) | mục Delivery |

### Rules và capabilities
- RULE-01 (MUST): Missing token categories → Skip sections and note the gap (never fabricate values).
- RULE-02 (MUST): Multi-theme (light/dark) → Ask user which theme to document; offer separate `dark/` subdirectory.
- RULE-03 (MUST): Auth-gated pages → Focus on public marketing pages.
- RULE-04 (MUST): Full-clone thành code chạy được → chuyển `/web-clone` Mode B, không làm trong skill này (canonical duy nhất, tránh drift).
- RULE-05 (SHOULD): Do's / Don'ts 7-8 mỗi loại, tham chiếu token cụ thể; brand voice 5-8 câu dạng design critique.
- Capabilities: đọc trang web công khai (chụp màn hình + đọc CSS/computed styles); ghi file vào `themes/{brand-slug}/` và draft wiki.

### Failure boundaries
- URL không hợp lệ / không công khai → **clarify** xin URL public; trang auth-gated → **partial** trên trang marketing công khai.
- Site có cả light/dark → **clarify** chọn theme trước khi trích.
- Không trích được một nhóm token → **partial**: bỏ mục đó và ghi rõ gap, không bịa giá trị.
- Yêu cầu rebuild thành code → ngoài phạm vi, chuyển `/web-clone`.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | lời user | Xác định mode (rico command / ngôn ngữ tự nhiên) + đầu ra (Workflow 1–4) + brand-slug | loại workflow | rebuild code → `/web-clone`; nhiều theme → clarify |
| W02 | effect | URL | Gather visual data: screenshot hero, nav, CTAs, cards, typography, footer; DevTools CSS variables, @font-face, computed styles | dữ liệu thô | SPA/CSS nén → Edge Cases |
| W03 | judgment | dữ liệu thô | Extract design tokens (colors, typography, spacing, radius, shadows) | bộ token | nhóm thiếu → ghi gap |
| W04 | judgment | trang + token | Document components với mọi state; brand voice; Do's/Don'ts | nội dung DESIGN.md | — |
| W05 | effect | token | Sinh file theo workflow vào `themes/{brand-slug}/` | file đầu ra | — |
| W06 | effect | kết quả | Output report draft + index + log (mục Delivery) | draft | 0 artifact → skip |

Chi tiết từng bước (nguồn chân lý cho W01–W06): xem "Workflow 1–4" dưới đây và các mục tham chiếu kèm theo, chép nguyên văn từ bản cũ.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | `rico tokens` / `rico variables` / `rico theme.css` / `rico preview` | Workflow 2: chỉ sinh một định dạng | — | W06 |
| B02 | user_optional | `rico 全部输出 [brand]` | Workflow 3: sinh đủ 5 file | — | W06 |
| B03 | conditional_required | đầu vào là file token có sẵn (`rico 把 DESIGN.md 转为 tokens`) | Workflow 4: parse file nguồn → sinh định dạng đích, bỏ W02 | file nguồn không có → clarify | W05 |
| B04 | conditional_required | site multi-theme light/dark | hỏi theme; dark khác biệt rõ → đề nghị `themes/{brand}-dark/` | user chọn một theme → chỉ theme đó | W03 |
| B05 | recovery | SPA / client-rendered hoặc CSS nén | view-source + network tab / DevTools computed styles | vẫn không có → ghi gap | W03 |

### Validation và stopping
Cần review bằng mắt: token có nguồn quan sát thật (không bịa), preview.html mở được qua `file://`, tokens.json đúng DTCG có `$description`. Dừng khi mọi file của workflow đã chọn được sinh hoặc gap đã được ghi rõ.

### Examples
- **Positive:** `rico DESIGN.md https://linear.app` → `themes/linear/DESIGN.md` + `themes/linear/preview.html`, trang Linear là dark khác biệt → hỏi theme trước, đề nghị `themes/linear-dark/`.
- **Boundary/failure:** "clone y hệt stripe.com thành Next.js chạy được" → không trích token; chuyển `/web-clone` Mode B. Site không lộ shadow nào → DESIGN.md bỏ mục Shadows và ghi gap, không bịa giá trị.

### Reference — Input Contract

#### Website Extraction
extract DESIGN.md <url>

Required:
- valid public URL

Optional flags:
- --theme=light|dark
- --depth=basic|full
- --components-only
- --tokens-only
- --mobile-first
- --desktop-first
### Reference — What Can This Skill Do?

#### Core Features

1. **Website to Design System** - Input any website URL, extract its design tokens, colors, typography, spacing, shadows, and component styles
2. **Multiple Output Formats** - Generate DESIGN.md, preview.html, tokens.json (DTCG), variables.css, and theme.css (Tailwind v4)
3. **Format Conversion** - Convert between any supported formats (e.g., DESIGN.md to tokens.json, variables.css to DESIGN.md)
4. **Visual Preview** - Generate a self-contained preview.html page that showcases the entire design system

#### Use Cases

- Need a design system document for an existing website
- Want to extract design tokens for implementation
- Need to convert between design token formats
- Want a visual reference page for a brand's design system

---

### Reference — Trigger Methods

This skill supports two trigger modes:

**Mode 1: Explicit Command (rico prefix)**

| Command | Output |
|---------|--------|
| `rico DESIGN.md [url]` | DESIGN.md + preview.html (default) |
| `rico preview [url]` | preview.html only |
| `rico tokens [url]` | tokens.json only |
| `rico variables [url]` | variables.css only |
| `rico theme.css [url]` | theme.css only |
| `rico 全部输出 [brand]` | All 5 files |
| `rico 把 DESIGN.md 转为 tokens` | Format conversion |

**Mode 2: Natural Language**

```
Create a DESIGN.md for linear.app
Extract design tokens from stripe.com
Generate a preview for github.com
Analyze GitHub's design system
```

---

### Reference — Mode 3: Full-Clone — rebuild to working code

Mặc định extract-site cho ra *design system* (token → DESIGN.md/css/json). Khi user muốn
**dựng lại nguyên trang thành code chạy được** (pixel-perfect, ví dụ Next.js + shadcn), đây
không còn là job của extract-site — chuyển sang **`/web-clone` Mode B (reconstruct)**, skill
đó là canonical duy nhất cho pipeline recon → component spec → parallel builder → visual-diff
QA (distilled từ `ai-website-cloner-template`, MIT). Trước 2026-07-23, pipeline này từng viết
trùng ở cả hai skill; hợp nhất về `web-clone` để tránh drift khi một bên sửa mà bên kia quên.

---

### Reference — Output Structure

All generated files are saved in the `themes/{brand-slug}/` directory:

```
themes/{brand-slug}/
├── DESIGN.md         # Full style reference (default output)
├── preview.html      # Visual design system preview (default output)
├── tokens.json       # DTCG format design tokens
├── variables.css     # CSS custom properties
└── theme.css         # Tailwind v4 @theme
```

---

### Reference — Workflow

#### Workflow 1: Generate DESIGN.md + Preview (Default)

```
User: rico DESIGN.md https://linear.app
    ↓
Step 1: Gather visual data
  • Screenshot hero, nav, CTAs, cards, typography, footer
  • Inspect DevTools for CSS variables, @font-face, computed styles
    ↓
Step 2: Extract design tokens
  • Colors → semantic tokens (canvas, surface-1, ink, accent-blue, etc.)
  • Typography → font families, sizes, weights, line-height, letter-spacing
  • Spacing → base unit detection (4px or 5px grid)
  • Radius → xs to full scale
  • Shadows → full CSS syntax
    ↓
Step 3: Document components with all states
  • Navigation, Buttons, Inputs, Cards, Footer
  • Include hover, focus, active, selected states
    ↓
Step 4: Write brand voice (5-8 sentences as design critique)
    ↓
Step 5: Write Do's / Don'ts (7-8 each, referencing specific tokens)
    ↓
Step 6: Generate DESIGN.md + preview.html
```

#### Workflow 2: Single Format Output

```
User: rico tokens https://stripe.com
    ↓
Generate tokens.json only (DTCG format)
```

#### Workflow 3: Full Output (All 5 Files)

```
User: rico 全部输出 github
    ↓
Generate all 5 files:
  • DESIGN.md, preview.html, tokens.json, variables.css, theme.css
```

#### Workflow 4: Format Conversion

```
User: rico 把 DESIGN.md 转为 tokens
    ↓
Parse existing DESIGN.md → generate tokens.json
```

---

### Reference — Output Format Details

#### DESIGN.md

A comprehensive markdown document containing:

- Brand voice and design philosophy
- Color system with semantic token names
- Typography scale with font-feature-settings
- Spacing system
- Border radius scale
- Shadow specifications
- Component documentation (with all states)
- Do's and Don'ts (referencing specific tokens)

#### preview.html

A self-contained, single-file visual design system reference page:

- Linear top-to-bottom layout (no bento grid)
- Sections: Hero → Colors → Gradients → Typography → Spacing & Shapes → Shadows → Depth & Surfaces → Components → Do's & Don'ts
- Download links for all spec files
- Sticky nav with section anchors
- Scroll-triggered entrance animations
- Responsive (mobile-first)
- Works with `file://` protocol (no external dependencies except Google Fonts)

#### tokens.json

DTCG (Design Tokens Community Group) standard format:

- Each token includes `$description` explaining its intended use
- Grouped by category: colors, typography, spacing, radius, shadows
- Compatible with style dictionary and token transformers

#### variables.css

CSS custom properties grouped by:

- Colors, Font Families, Type Scale, Weights
- Spacing, Layout, Border Radius, Shadows, Surfaces

#### theme.css

Tailwind v4 `@theme` format for direct integration with Tailwind CSS v4.

---

### Reference — Usage Examples

#### Example 1: Generate Design System from Website

```
User: rico DESIGN.md https://linear.app

AI: [Extracts design tokens from Linear's website]
    [Generates themes/linear/DESIGN.md + themes/linear/preview.html]

    Generated 2 files:
    • themes/linear/DESIGN.md - Full style reference
    • themes/linear/preview.html - Visual preview
```

#### Example 2: Extract Tokens Only

```
User: rico tokens https://github.com

AI: [Extracts tokens from GitHub]
    [Generates themes/github/tokens.json]

    Generated DTCG tokens with 87 tokens across 6 categories.
```

#### Example 3: Convert Between Formats

```
User: rico 把 DESIGN.md 转为 tokens

AI: [Parses existing DESIGN.md]
    [Converts markdown tables to DTCG format]

    Generated themes/github/tokens.json
```

#### Example 4: Full Output

```
User: rico 全部输出 github

AI: [Generates all 5 files in themes/github/]
    • DESIGN.md
    • preview.html
    • tokens.json
    • variables.css
    • theme.css
```

---

### Reference — Edge Cases

| Scenario | Handling |
|----------|----------|
| SPA / client-rendered | Use view-source + network tab for CSS files |
| Compressed CSS | Use DevTools computed styles panel |
| Multi-theme (light/dark) | Ask user which theme to document; offer separate `dark/` subdirectory |
| Auth-gated pages | Focus on public marketing pages |
| Missing token categories | Skip sections and note the gap (never fabricate values) |

---

### Reference — File Structure

```
skills/
└── rico-design-md/
    ├── SKILL.md                          # Core skill definition
    └── references/
        ├── DESIGN-TEMPLATE.md            # Template for new DESIGN.md files
        └── themes-github/                # Reference example (GitHub)
            ├── DESIGN.md                 # Complete DESIGN.md example
            ├── github-preview.html       # Visual preview example
            ├── tokens.json               # DTCG format reference
            ├── variables.css             # CSS custom properties reference
            └── theme.css                 # Tailwind v4 @theme reference
```

---

### Reference — FAQ

#### How is this different from rico-ui-ux-themes?

- **rico-ui-ux-themes**: Applies existing design themes to optimize your website's visual design
- **rico-design-md**: Extracts design systems FROM websites and generates documentation/tokens

#### Can I use the generated tokens in my project?

Yes. All output formats are production-ready:
- `tokens.json` works with style dictionary and token transformers
- `variables.css` can be imported directly
- `theme.css` integrates with Tailwind v4

#### What if the website has both light and dark modes?

The skill will ask which mode to document. If the dark mode is visually distinct (e.g., Linear, Supabase), it offers to generate a separate `themes/{brand}-dark/` subdirectory.

---

**Last Updated**: 2026-05-13

**Maintainer**: [@ricouii](https://x.com/ricouii)

**Blog**: [rico'blog](https://ricoui.com)

**Status**: Active Development

---

### Delivery — Output Report

After all main skill tasks complete, write a propose draft to the wiki.

#### Steps

**1. Build the filename:**
- Format: `DDMMYY-<ten>.md`
- `DDMMYY` = today (e.g., `020626` for 2 June 2026)
- `<ten>` = 2–4 kebab-case words summarising what was done (e.g., `landing-page-coteccons`, `brand-kit-fintech`, `ingest-auth-spec`)

**2. Write** `llmwiki/wiki/sources/draft/DDMMYY-<ten>.md`:

```
---
type: draft
title: "DDMMYY-<ten>"
status: proposed
tags: [<skill-name>, output-report]
timestamp: YYYY-MM-DD
---

# DDMMYY-<ten>
**Type:** draft
**Status:** proposed
**Tags:** <skill-name>, output-report
**Proposed:** YYYY-MM-DD

## What
<One sentence — what this skill invocation produced or decided>

## Output
<Key artefacts, files created/modified, or decisions made>

## Files
| File | Action |
|------|--------|
| `path/to/file` | created / modified |

## Notes
- Invoked via: `/<skill-name>` skill

## Origin
- **Draft:** `wiki/sources/draft/DDMMYY-<ten>.md`
- **Commit:** _(filled by verify-before-commit)_
- **Date promoted:** _(filled by verify-before-commit)_
```

**3. Update wiki index & log:**
- `llmwiki/wiki/index.md` — append one row: `| [DDMMYY-<ten>](sources/draft/DDMMYY-<ten>.md) | draft | YYYY-MM-DD |`
- `llmwiki/wiki/log.md` — append: `## YYYY-MM-DD — <skill-name> — <ten>`

> Skip only when the skill produces zero artefacts and zero decisions (e.g., a pure display mode like `/caveman-stats`).
