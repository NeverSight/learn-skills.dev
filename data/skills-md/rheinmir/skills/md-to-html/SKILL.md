---
name: md-to-html
description: Render Markdown thành standalone HTML — Mermaid, Chart.js, styled tables, TOC
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: md-to-html

## WHAT

### Purpose và context
- **Purpose:** Markdown → self-contained HTML: Mermaid diagrams, Chart.js, styled tables, code highlight, floating TOC.
- **Trigger (when to use):**
  - Render/share `.md` as HTML
  - Doc has steps, comparisons, numbers to visualize
  - Need browser-ready professional output
  - Trigger phrases: `/md-to-html`, `md2html`, `biến md thành html`, `render md`, `xuất html từ md`, `visualize doc`
- **Non-goals:** không sửa nội dung file `.md` nguồn; không ghi HTML cạnh file `.md` nguồn; không phải site tài liệu nhiều trang có thiết kế riêng (đó là `docs-site-macos`).

### Mental model
`file .md → (template đầy đủ ngoài) → HTML standalone (Mermaid · Chart.js · bảng · code highlight · TOC) + output requirements bắt buộc → html/<tên>.html → output report draft`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | file `.md` nguồn | có | nội dung cần render |
| In | Full instructions `~/.gemini/antigravity/skills/md-to-html/SKILL.md` | không | template chi tiết bên ngoài; output requirements dưới đây áp dụng bất kể template |
| Out | HTML → `html/` dir (e.g. `html/tên-file.html`) | có | NOT same dir as source `.md`; self-contained |
| Out | output report `llmwiki/wiki/sources/draft/DDMMYY-<ten>.md` + index + log | có (trừ khi 0 artefact) | mục Delivery |

### Rules và capabilities
- RULE-01 (MUST): Output HTML → `html/` dir, NOT same dir as source `.md`.
- RULE-02 (MUST): Output requirements (don't ship a broken page) — the generated HTML must include every item in "Output requirements" below, regardless of the external template.
- Capabilities: đọc file Markdown; ghi file HTML tĩnh + draft wiki. Thư viện render (Mermaid, Chart.js) nhúng trong trang.

### Failure boundaries
- Không tìm thấy file `.md` nguồn → **blocked**, hỏi đường dẫn.
- Template ngoài (`~/.gemini/...`) không có → vẫn render theo Purpose + Output requirements ở đây (không coi là lỗi).
- Trang thiếu một mục trong Output requirements → **failed**, sửa trước khi giao ("don't ship a broken page").

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | đường dẫn `.md` | Đọc file nguồn (+ Full instructions ngoài nếu có) | nội dung | không có file → blocked |
| W02 | judgment | nội dung | Chọn cách visualize: steps/so sánh → Mermaid, số liệu → Chart.js, bảng styled, code highlight, floating TOC | bản dựng HTML | — |
| W03 | deterministic | HTML | Kiểm đủ Output requirements (danh sách dưới) | checklist đủ | thiếu → sửa, lặp W03 |
| W04 | effect | HTML | Ghi `html/<tên-file>.html` | file HTML | — |
| W05 | effect | kết quả | Output report draft (mục Delivery) | draft + index + log | 0 artefact → skip |

Chi tiết từng bước (nguồn chân lý cho W01–W05):

#### Output
HTML → `html/` dir (e.g. `html/tên-file.html`). NOT same dir as source `.md`.

#### Output requirements (don't ship a broken page)
The generated HTML must include, regardless of the external template:
- `<meta charset="utf-8">` + `<meta name="viewport" content="width=device-width, initial-scale=1">` and a real `<title>` — without viewport the TOC/tables overflow on mobile.
- `:focus-visible{outline:2px solid <accent>;outline-offset:2px}` so the floating-TOC links and any buttons show a keyboard focus ring.
- `font-variant-numeric:tabular-nums` on `table` (number columns must not jiggle).
- `@media(prefers-reduced-motion:reduce)` to skip Mermaid/Chart entry animation and set `scroll-behavior:auto`; add `html{scroll-behavior:smooth}` + `scroll-margin-top` so TOC anchor jumps glide and headings don't hide under any sticky header.
- A favicon (inline data-URI is fine) and `alt`/`<title>` on informative diagrams.

#### Full instructions
`~/.gemini/antigravity/skills/md-to-html/SKILL.md`

### Branches
Không có nhánh phụ trong version này.

### Validation và stopping
W03 là checklist tất định (grep được trong HTML: `charset`, `viewport`, `<title>`, `:focus-visible`, `tabular-nums`, `prefers-reduced-motion`, favicon). Chất lượng visualize (chọn Mermaid hay Chart) cần review mắt. Dừng khi file ở `html/` qua đủ checklist và report đã ghi.

### Examples
- **Positive:** `/md-to-html llmwiki/wiki/concepts/solid-what-how.md` → `html/solid-what-how.html` có TOC nổi, bảng WHAT/HOW styled `tabular-nums`, viewport + focus ring + reduced-motion; draft `DDMMYY-md-to-html-swh.md` + dòng index/log.
- **Boundary/failure:** bản dựng thiếu `<meta name="viewport">` → W03 fail (TOC/bảng tràn trên mobile) → thêm rồi mới ghi file; không ghi HTML cạnh file `.md` nguồn.

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
