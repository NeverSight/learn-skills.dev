---
name: slidev-builder
description: "Tạo Slidev presentation từ nội dung đầu vào. Sử dụng khi user yêu cầu tạo slides, build Slidev project, export PDF, hoặc gọi /slidev-builder. Nhận text hoặc file path."
disable-model-invocation: true
---

# Slidev Builder — Presentation Generator

Tạo Slidev project + PDF từ nội dung đầu vào. Activate `slidev` skill (built-in, cùng context) cho Slidev Markdown generation + PDF export.

Output: `output/{slug}-{YYMMDD-HHmm}/slides/{slug}-{theme-name}/` (package.json, slides.md, dist/{slug}.pdf)

## Step 1: Tiếp nhận nội dung & Cấu hình

1. Đọc input: text trực tiếp hoặc file path
2. Phân tích sơ bộ: topic, length, complexity
3. Hỏi user bằng AskUserQuestion (4 câu hỏi):

**Câu hỏi 1 - Loại nội dung** (header: "Content type"):
* "Hướng dẫn/Giáo dục" - Tutorial, hướng dẫn học (Gagné + scaffolding)
* "Business/Báo cáo" - Phân tích, đề xuất, báo cáo (Pyramid Principle)
* "Thuyết phục/Pitch" - Pitch sản phẩm, proposal (PAS + Sparkline)
* "Technical/Process" - Quy trình, kiến trúc, so sánh kỹ thuật (SCR)

**Câu hỏi 2 - Mức độ chi tiết** (header: "Detail level"):
* "L1 - Tổng quan" - Ý chính, bullet ngắn gọn (5+ slides)
* "L2 - Cân bằng" - Ý chính + giải thích + ví dụ (10+ slides)
* "L3 - Chi tiết" - Deep dive, code examples (18+ slides)

**Câu hỏi 3 - Ngôn ngữ** (header: "Language"):
* "Tiếng Việt" (Recommended)
* "English"
* "Song ngữ" - Title tiếng Anh, body tiếng Việt

**Câu hỏi 4 - Audience** (header: "Audience"):
* "Executive/Decision maker" - Bottom-line upfront, metrics, ngắn gọn
* "Technical team" - Jargon OK, chi tiết kỹ thuật
* "Mixed/General" - Cần giải thích thuật ngữ, ví dụ cụ thể
* "Workshop/Hands-on" - Interactive, knowledge checks

4. Phân tích nội dung → tạo slide plan nội bộ (title + key points cho mỗi slide)
5. Tạo output folder: `output/{slug}-{YYMMDD-HHmm}/`

## Slidev Theme List

**Official themes:**

| Theme | Package | Mô tả |
| --- | --- | --- |
| `default` | `@slidev/theme-default` | Minimalist, light/dark |
| `seriph` | `@slidev/theme-seriph` | Serif-based formal, light/dark |
| `apple-basic` | `@slidev/theme-apple-basic` | Keynote-inspired, light/dark |
| `bricks` | `@slidev/theme-bricks` | Playful blocks, light |
| `shibainu` | `@slidev/theme-shibainu` | Cute dark theme |

**Community themes (phổ biến):**

| Theme | Package | Mô tả |
| --- | --- | --- |
| `geist` | `slidev-theme-geist` | Vercel design system, light/dark |
| `academic` | `slidev-theme-academic` | Formal academic, light/dark |
| `dracula` | `slidev-theme-dracula` | Vibrant dark theme |

User cũng có thể nhập tên bất kỳ Slidev theme từ npm.

## Auto Theme Recommendation

| Content Type | Primary | Secondary |
| --- | --- | --- |
| Hướng dẫn/Giáo dục | seriph | default |
| Business/Báo cáo | default | apple-basic |
| Thuyết phục/Pitch | apple-basic | seriph |
| Technical/Process | default | seriph |

## Step 2: Chọn Slidev theme

1. Hiển thị bảng Slidev Theme List
2. Hỏi user bằng AskUserQuestion (header: "Theme"): đánh dấu recommended theme dựa trên Auto Theme Recommendation + cho phép nhập tên khác qua "Other"

## Step 3: Tạo slide (Slidev)

1. Xác định theme package name:
   * Official themes: `@slidev/theme-{name}`
   * Community themes: `slidev-theme-{name}`
   * Custom name → dùng nguyên tên

2. Đọc `references/slide-templates.md` (relative to this skill folder) để nắm Slidev Markdown patterns

3. **Activate `slidev` skill** trong cùng agent context. Cung cấp:

   **Headmatter config:**
   ```yaml
   theme: { theme-name }
   fonts:
     sans: Tahoma
     serif: Arial
     mono: Fira Code
     provider: none
   ```

   **Layout mapping table:**

   | Slide Type | Slidev Layout |
   | --- | --- |
   | title | cover |
   | agenda | default |
   | content | default |
   | comparison | two-cols-header |
   | comparison-simple | two-cols |
   | summary | default |
   | cta | end |
   | transition | section |
   | statement | statement |
   | metric | fact |
   | quote | quote |
   | table | default |
   | diagram | default |
   | code | default |

   * Nội dung từng slide (title, body content, slide type → layout)
   * Slidev Markdown templates từ `references/slide-templates.md`
   * Vietnamese fonts: `Tahoma, Arial, sans-serif` qua fonts config
   * Output path: `{output_folder}/slides/{slug}-{theme-name}/`

4. Slidev skill tạo project: `package.json` (deps: `@slidev/cli`, `{theme-package}`, `playwright-chromium`) + `slides.md` (headmatter + all slides)
5. **Install**: `pnpm install` trong Slidev project folder
6. **Export PDF**: `npx slidev export --output dist/{slug}.pdf --timeout 60000`
7. Thông báo output:
   * Slidev project path + PDF path (nếu export thành công)
   * Hướng dẫn: `cd {project-path} && pnpm dev` để xem slides
   * "Chạy lại `/slidev-builder {output_folder}/` với theme khác để tạo variant mới."

## Slidev Constraints (CRITICAL)

Khi activate slidev skill, PHẢI tuân thủ:

* **Vietnamese fonts**: `Tahoma, Arial, sans-serif` qua fonts config, `provider: none`. KHÔNG dùng Impact, Courier New
* **Text-only**: Không image layouts, không embed images. Chỉ text, bullets, code blocks
* **Speaker notes**: HTML comments `<!-- notes -->` sau content mỗi slide
* **Code blocks**: Native Markdown fenced blocks với language tag. Max 10-15 dòng/slide. Line highlighting `{2,3}` hoặc click-based `{1|3-4|all}`
* **Nested lists**: Indent 2 spaces. Dùng thoải mái cho L2/L3 sub-bullets
* **Max content per slide**: L1: 2-3 bullets, <8 words/bullet. L2: 3-5 bullets + 1-2 sub-bullets. L3: 3-5 bullets + 2-3 sub-bullets, max 100 words/slide
* **Slide separator**: `---` giữa các slides
* **Layout front matter**: Mỗi slide PHẢI có layout specification
* **Projector contrast**: contrast ratio >= 4.5:1 (WCAG AA)
* **v-click**: `<v-clicks>` wrapper cho L2/L3 bullet lists. L1 KHÔNG dùng v-click
* **Mermaid diagrams**: Built-in, `` ```mermaid `` code block. Max 8-10 nodes
* **Slide transitions**: `transition: fade` hoặc `slide-left`. Global trong headmatter
* **v-mark**: `<span v-mark.highlight>` cho key terms. Max 1-2 per slide
* **Shiki Magic Move**: ```` ````magic-move ```` cho L2/L3 technical. Max 3-4 steps
* **Inline code trên dark slides**: `layout: cover`, `end`, `section` chứa inline code → thêm scoped style:
  ```html
  <style>
  code {
    color: #e2e8f0 !important;
    background: rgba(255,255,255,0.15) !important;
  }
  </style>
  ```

## Important Notes

* Chỉ tạo text-only slides, không hình ảnh
* Slidev Markdown templates: xem `references/slide-templates.md`
* Theme do user chọn từ Slidev ecosystem, không cần custom CSS
* `pnpm dev` để preview slides trong browser
* PDF export dùng Playwright (cần `playwright-chromium` dependency)
