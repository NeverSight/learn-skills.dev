---
name: outline-writer
description: "Phân tích nội dung và tạo outline chuyên nghiệp. Sử dụng khi user yêu cầu tạo outline, phân tích content, lập dàn ý cho presentation/blog/document, hoặc gọi /outline-writer. Output: outline.md với YAML frontmatter."
disable-model-invocation: true
---

# Outline Writer — Content Analysis & Outline Generator

Tạo professional outline từ content input. Hỗ trợ nhiều output types: presentation slides, blog post, documentation. Vietnamese default.

## Output Folder Structure

```
output/
└── {slug}-{YYMMDD-HHmm}/
    ├── outline.md
    ├── content-map.md
    ├── coverage-report.md
    └── research-notes.md (nếu có research)
```

**Naming rules:**

- `{slug}`: kebab-case từ topic chính (max 30 chars)
- `{YYMMDD-HHmm}`: timestamp lúc tạo folder

## Step 0: Detect Mode

1. Kiểm tra input từ user:
  - Nếu user chỉ vào **folder output đã có** (chứa `outline.md`) → Hướng dẫn: "Outline đã có. Dùng `/slidev-builder {folder}/` để tạo slides, hoặc cung cấp nội dung mới để tạo outline mới."
  - Nếu user cung cấp **nội dung mới** (text, file path) → Tiếp tục Step 1

## Step 1: Tiếp nhận nội dung & Cấu hình

1. Đọc input từ user: text trực tiếp hoặc file path (.md, .txt, .pdf)
2. Nếu input là file path, đọc nội dung file
3. Phân tích sơ bộ: topic, length, complexity
4. Hỏi user bằng AskUserQuestion (4 câu hỏi trong 1 lần):

**Câu hỏi 1 - Output type** (header: "Output type"):

- "Presentation slides" - Outline cho slide deck (tiếp tục hỏi audience & framework ở Step 1.1)
- "Blog post" - Outline cho bài viết blog
- "Documentation/Report" - Outline cho tài liệu/báo cáo

**Câu hỏi 2 - Mức độ chi tiết** (header: "Detail level"):

- "L1 - Tổng quan" - Chỉ ý chính, bullet ngắn gọn (5+ items)
- "L2 - Cân bằng" - Ý chính + giải thích + ví dụ minh họa (10+ items)
- "L3 - Chi tiết" - Đầy đủ nội dung, deep dive, code examples (18+ items)

**Câu hỏi 3 - Ngôn ngữ** (header: "Language"):

- "Tiếng Việt" - Toàn bộ nội dung tiếng Việt (Recommended)
- "English" - Toàn bộ nội dung tiếng Anh
- "Song ngữ" - Title tiếng Anh, body tiếng Việt

**Câu hỏi 4 - Research bổ sung** (header: "Research"):

- "Chỉ dùng source" - 100% từ nội dung đầu vào, không tìm thêm
- "Research thêm" - Tìm thêm data, statistics, examples từ web
- "Auto" - Tự động: research nếu source ít thông tin, skip nếu đủ

**Logic Recommended cho câu hỏi 4:** Source < 500 words HOẶC thiếu data/metrics → recommend "Research thêm". Source >= 500 words VÀ đủ data → recommend "Chỉ dùng source".

5. Nếu output_type = "Presentation slides" → hỏi thêm content type (AskUserQuestion, header: "Content type"):
  - "Hướng dẫn/Giáo dục" - Giải thích khái niệm, tutorial (Gagné + scaffolding)
  - "Business/Báo cáo" - Phân tích, đề xuất, báo cáo (Pyramid Principle)
  - "Thuyết phục/Pitch" - Bán ý tưởng, pitch sản phẩm (PAS + Sparkline)
  - "Technical/Process" - Quy trình, kiến trúc, so sánh kỹ thuật (SCR + step-by-step)

## Step 1.1: Audience & Framework Selection (Chỉ khi output_type = "Presentation slides")

Hỏi user bằng AskUserQuestion (1-2 câu hỏi tùy content type):

**Câu hỏi 1 — Audience** (header: "Audience", luôn hỏi):

- "Executive/Decision maker" - C-level, cần bottom-line upfront, metrics, ngắn gọn
- "Technical team" - Engineers, developers — jargon OK, chi tiết kỹ thuật
- "Mixed/General" - Đa dạng trình độ — cần giải thích thuật ngữ, ví dụ cụ thể
- "Workshop/Hands-on" - Đào tạo thực hành — interactive, knowledge checks

**Câu hỏi 2 — Framework** (header: "Framework", chỉ hỏi khi content type = "Business/Báo cáo"):

- "Pyramid Principle" - Kết luận trước, supporting arguments sau (Recommended khi audience = Mixed)
- "SCQA" - Situation → Complication → Question → Answer (Recommended khi audience = Executive)

**Audience ảnh hưởng outline:**

| Audience  | Ảnh hưởng                                              |
| --------- | ------------------------------------------------------ |
| Executive | Ưu tiên metrics, bottom-line upfront, max 12-15 slides |
| Technical | Sequential IA, jargon OK, code examples, L2-L3 phù hợp |
| Mixed     | Thêm definition cho thuật ngữ, ví dụ concrete bắt buộc |
| Workshop  | Force Gagné framework, thêm knowledge check items      |


## Step 1.5: Research bổ sung (Optional)

Chạy sau Step 1, trước Step 2. Quyết định dựa trên câu hỏi Research ở Step 1.

**Khi nào chạy:**

- User chọn "Research thêm" → luôn chạy
- User chọn "Auto" → chạy NẾU source < 500 words HOẶC thiếu data/metrics
- User chọn "Chỉ dùng source" → SKIP hoàn toàn

**Process:**

1. Extract 3-5 topic keywords từ source
2. Tạo 2-3 search queries: `"{topic}" statistics data {năm}`, `"{topic}" trends insights`, `"{topic}" examples best practices`
3. Chạy WebSearch cho mỗi query
4. Extract findings relevant: statistics, data points, examples, quotes
5. Lưu kết quả vào `{output_folder}/research-notes.md`
6. Append selected items vào Content Map với prefix `[R]`
7. Thông báo user: "Research xong: X data points, Y insights. Đã lưu tại research-notes.md"

**Quy tắc:** Chỉ thông tin factual có nguồn. Ưu tiên: số liệu > xu hướng > ví dụ. KHÔNG thay thế source, chỉ BỔ SUNG. Max 10 items.

## Visual Patterns per Content Type (Chỉ khi output_type = "Presentation slides")

| Content Type       | Visual Patterns                         | Recommended Slide Types                     |
| ------------------ | --------------------------------------- | ------------------------------------------- |
| Hướng dẫn/Giáo dục | Numbered steps, before/after comparison | content, comparison, statement, quote       |
| Business/Báo cáo   | Accent bars, data callout               | content, metric, comparison, table, summary |
| Thuyết phục/Pitch  | Bold statements, high contrast, CTA     | statement (30%+), metric, quote, cta        |
| Technical/Process  | Code blocks, process flow, Mermaid      | content, comparison, code, diagram, table   |


## Step 2: Phân tích nội dung & Tạo outline

1. Tạo output folder: `output/{slug}-{YYMMDD-HHmm}/`
2. Đọc `references/outline-rules.md` (relative to this skill folder) để nắm quy tắc outline
3. **Framework selection:**
  - Presentation: áp dụng framework tương ứng content type (xem Content Type → Framework Mapping trong outline-rules.md). Nếu audience = "Workshop", override sang Gagné
  - Blog/Doc: sắp xếp logic — Introduction → Body sections (clustered) → Conclusion
4. **Content Map**: Parse source → silent clustering → extract topics → assign priority (`must`/`should`/`nice`) theo detail level. Nếu Step 1.5 đã chạy → append items `[R]`. Lưu `{output_folder}/content-map.md`
5. Phân tích nội dung theo detail level + audience-aware adjustments (nếu presentation). Xem Detail Level Mapping + Audience-Aware Adjustments trong outline-rules.md
6. Tạo outline: Opening > Body > Closing (presentation) hoặc Introduction > Body > Conclusion (blog/doc). Áp dụng Cognitive Sequencing + Narrative Arc (xem outline-rules.md). Cross-check Content Map: mọi `must` topics phải xuất hiện
7. **Lưu outline** ra `{output_folder}/outline.md` với YAML frontmatter:
  ```yaml
   ---
   title: "Tên outline"
   slug: "ten-outline"
   output_type: "presentation" | "blog" | "doc"
   content_type: "..." # chỉ khi presentation
   framework: "..." # chỉ khi presentation
   audience: "..." # chỉ khi presentation
   detail_level: "L1" | "L2" | "L3"
   language: "vi" | "en" | "bilingual"
   source: "mô tả source input"
   created: "YYYY-MM-DD HH:mm"
   total_slides: N # hoặc total_sections cho blog/doc
   ---
  ```
8. Hiển thị outline cho user review
9. **Coverage Report**: Generate `{output_folder}/coverage-report.md` (xem Coverage Report Rules trong outline-rules.md)
10. **Feedback loop**: Hỏi "Outline OK?" (AskUserQuestion, header: "Outline review"):
  - "OK, tiếp tục" - Chấp nhận outline
    - "Chỉnh sửa" - User mô tả thay đổi → cập nhật → hỏi lại
11. Khi approved, thông báo tùy output_type:
  - Presentation: "Outline xong. Chạy `/slidev-builder {output_folder}/` để tạo slides."
    - Blog/Doc: "Outline xong tại `{output_folder}/outline.md`."

## Important Notes

- Chi tiết quy tắc outline: xem `references/outline-rules.md`
- Outline rules áp dụng chủ yếu cho presentation. Blog/doc dùng subset rules phù hợp (Content Map, Coverage Report, Cognitive Sequencing)
- Content Map và Coverage Report bắt buộc cho mọi output type
