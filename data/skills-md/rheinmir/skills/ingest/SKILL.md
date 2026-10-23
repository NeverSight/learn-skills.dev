---
name: ingest
description: Process new file in llmwiki/raw/ and distill into wiki pages
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: wiki-loop
---

# Skill: ingest

## WHAT

### Purpose và context
- **Purpose:** Process new file in `raw/`, distill knowledge into wiki. Each ingest touches 10-15 wiki files.
- **Trigger (when to invoke):** Automatically when new file appears in `raw/`.
- **Non-goals:** không sửa file trong `raw/`, không tạo trang cho thứ nguồn không thật sự giới thiệu, không viết code/triển khai theo nội dung nguồn (đó là `/propose` → `/plan`).

### Mental model
`raw/<file> (bất biến) → takeaways (facts · decisions · entities · concepts) → docs-impact-plan → trang concept/entity (canonical home) + trang source → wikilinks → index + log → draft output report`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | đường dẫn file trong `raw/` | có | nguồn đọc TRỌN, chỉ đọc |
| Out | trang `wiki/concepts/` · `wiki/entities/` | theo nguồn | tạo mới hoặc cập nhật surgical, có frontmatter OKF + `## Origin` |
| Out | trang `wiki/sources/<...>.md` | có | tóm tắt nguồn, link về `raw/` |
| Out | `wiki/index.md` + `wiki/log.md` | có | mỗi file tạo/sửa có dòng index; log `## YYYY-MM-DD — ingest — <filename>` |
| Out | `wiki/sources/draft/DDMMYY-<ten>.md` | có (trừ khi 0 artifact) | output report |

### Rules và capabilities
- RULE-01 (MUST): **OKF v0.1 (R9):** every wiki page starts with a YAML frontmatter block (`---`) carrying a non-empty `type` (e.g. `concept`, `entity`, `source`) plus optional `title`/`tags`/`timestamp`/`resource`. Copy the matching `_template.md`. Keep the `## Origin` body section (R2).
- RULE-02 (MUST): Never modify file in `raw/`. Read only.
- RULE-03 (MUST): No wiki page unless source actually introduces that entity or concept.
- RULE-04 (MUST): Prefer updating existing page over creating duplicate.
- RULE-05 (MUST): **Canonical home**: mỗi concept một trang chính chủ — chi tiết nằm ở đó, trang khác chỉ nhắc ngắn + `[[wikilink]]`; đừng nhân bản cùng giải thích ra nhiều trang.
- RULE-06 (MUST): **Surgical trên trang có sẵn**: cập nhật = thay đúng câu lỗi thời, không viết lại phần còn đúng; cấm edit formatting-only (reformat bảng/dòng trống/wording khi nội dung không sai).
- Capabilities: đọc `raw/`; ghi `wiki/` (concepts · entities · sources · draft) + index + log. Không ghi `raw/`, không mạng.

### Failure boundaries
- File nguồn không đọc được / rỗng → **blocked**, báo đường dẫn, không tạo trang.
- Nguồn không giới thiệu concept/entity mới nào → chỉ trang source + index + log (**succeeded** hẹp), không đẻ trang thừa.
- Nguồn mâu thuẫn trang wiki đang có → ghi mâu thuẫn vào trang source, **clarify** với user trước khi thay câu đang đúng.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | effect | file `raw/` | Đọc trọn nguồn, không tóm tắt sớm | nội dung đầy đủ | đọc lỗi → blocked |
| W02 | judgment | nội dung | Rút takeaways + lập docs-impact-plan | danh sách trang bị ảnh hưởng, mỗi trang truy về một điểm nguồn | trang không truy được → bỏ |
| W03 | effect | impact-plan | Cập nhật trang có sẵn / tạo concept·entity mới | trang wiki | — |
| W04 | effect | nguồn | Trang source trong `wiki/sources/` link về `raw/` | trang source | — |
| W05 | effect | trang đã chạm | Wikilinks + `wiki/index.md` + `wiki/log.md` | index/log khớp | thiếu dòng index → sửa rồi lặp |
| W06 | effect | kết quả | Output report draft (mục Delivery) | draft + index + log | 0 artifact → skip |

Chi tiết từng bước (nguồn chân lý cho W01–W06):

1. Read source file in `raw/` completely. No premature summarizing.
2. Extract key takeaways: facts, decisions, entities, concepts from source.
   Rồi lập **docs-impact-plan** trước khi ghi (distill openwiki 060726): `điểm mới trong nguồn → trang bị ảnh hưởng → sửa/tạo gì → vì sao`. Trang không truy được về một điểm cụ thể trong nguồn thì KHÔNG đụng.
3. For each entity or concept:
   - Has wiki page: open it, add/revise relevant info.
   - No page: create in `wiki/concepts/` or `wiki/entities/`.
4. Create or update summary page in `wiki/sources/` for source (link back to `raw/` file).
5. Add `[[wikilinks]]` between all new/updated pages.
6. Update `wiki/index.md` for every file created or modified.
7. Append to `wiki/log.md`: `## YYYY-MM-DD — ingest — <filename>` with bullet list of all pages touched.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | entity/concept đã có trang | mở trang, thêm/sửa đúng câu liên quan (surgical) | — | W04 |
| B02 | conditional_required | entity/concept chưa có trang | tạo trong `wiki/concepts/` hoặc `wiki/entities/` từ `_template.md` | nguồn không thật sự giới thiệu → không tạo | W04 |

### Validation và stopping
Mỗi trang mới có frontmatter `type` không rỗng + `## Origin` (R2/R9 do hook kiểm); mỗi file tạo/sửa có dòng trong `wiki/index.md` (R3). Dừng khi mọi mục của impact-plan đã xử lý hoặc bị loại có lý do.

### Examples
- **Positive:** thêm `raw/prd/X-PRD.md` giới thiệu chuẩn mới → tạo `wiki/concepts/<chuẩn>.md` + `wiki/sources/DDMMYY-x-prd.md`, sửa 1 câu ở concept liên quan, index + log + draft report.
- **Boundary/failure:** file raw chỉ là ảnh chụp màn hình không có chữ đọc được → blocked, báo user, không tạo trang rỗng.

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
