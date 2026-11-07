---
name: surface-coverage
description: "Kiểm 'phủ hết' bằng diff với BỀ MẶT THẬT đọc từ code (trang, route, module API, lệnh CLI, cron, tool MCP) thay vì đếm số artefact: liệt kê bề mặt tất định ra surface.json @commit, giữ sổ phủ coverage.json (mục → artefact giải thích hoặc loại trừ có lý do), gác bằng test đỏ khi có mục mới chưa phủ, báo 'N/M mục'. Gọi khi user hỏi 'đã phủ hết chưa', 'có đủ chưa', 'tương ứng hết chức năng chưa', 'vét cạn', 'không lọt chức năng', 'coverage', 'sổ chức năng', khi sinh bài học/flow/docs cho một codebase, hoặc khi sắp báo một con số (19 bài, 18 flow) như thể đã đủ."
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [fdk/tools/surface-coverage.py]
---

# Skill: surface-coverage

Đúc kết từ phiên Openship ↔ devops-agent ngày 01/10/2026 (GH#191). `/orca-onboard` chọn ra 18 flow, rồi sinh 19 bài học, và báo cáo như thể đã giải thích hết app. Bề mặt thật đọc từ code có 62 trang dashboard và 37 module API. Gần một nửa (servers, clusters, jobs, billing, members…) không có bài nào. Không có gì báo đỏ, vì không có gì đem danh sách đó so với sản phẩm. **Một con số không phải độ phủ. Độ phủ là một phép diff với bề mặt thật.**

## WHAT

### Purpose và context
- **Purpose:** trước khi nói tài liệu, bài học, sơ đồ, test, bề mặt CLI/MCP hay graph onboarding "phủ" một sản phẩm, phải chứng minh bằng diff. Liệt kê bề mặt thật từ code. Có một sổ phủ (coverage ledger), trong đó mỗi mục bề mặt trỏ tới thứ giải thích nó, hoặc được loại trừ kèm lý do. Có một cổng (gate) đỏ khi xuất hiện mục mới chưa phủ.
- **Trigger:**
  - User hỏi "đã phủ hết chưa", "có đủ chưa", "tương ứng hết các chức năng trên dashboard chưa", "vét cạn", "không lọt chức năng", "sổ chức năng".
  - Đang sinh bài học, flow hay docs cho một codebase (`/orca-onboard` Phase 2, `/teach-me` toàn hệ thống).
  - Sắp báo một con số artefact ("19 bài", "18 flow", "CLI có 40 lệnh") như thể nó đã đủ.
- **Non-goals:** không đo độ phủ dòng code của test (đó là coverage của test runner). Không tự sinh nội dung cho mục còn thiếu. Skill chỉ chỉ ra thiếu gì và cách lần code để lấp. Không thay schema `domain-graph.json` của `orca-onboard`.

### Mental model
```
code ──scan (script, tất định)──▶ surface.json {commit, items: page:/x · api:/x · module:x · cli:x …}
artefact (flow · bài · doc · op) ──người/agent ghi──▶ coverage.json {commit, items: mục → by[] | exclude:"lý do"}
surface.json ⊖ coverage.json ──check──▶ "N/M mục được phủ, K loại trừ" + danh sách CHƯA PHỦ + lỗi (rc 1)
```
Cùng một hình dạng lỗi xuất hiện ở nhiều chỗ khác: "CLI phủ mọi tính năng" cho tới khi có một lời gọi UI không có op tương ứng, "docs phủ mọi endpoint", "test phủ mọi route".

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | thư mục code của sản phẩm | có | nơi đọc bề mặt; nên là git repo để ghi commit |
| In | bộ artefact đang khẳng định là phủ | có | flow, bài học, trang docs, op CLI/MCP, test |
| In | glob thư mục module API / lệnh CLI | không | khi khung không phải file-based router |
| Out | `surface.json` | có | mọi mục bề mặt kèm file nguồn và commit lúc đọc |
| Out | `coverage.json` | có | mỗi mục → `by[]` (id artefact) hoặc `exclude` có lý do |
| Out | dòng báo cáo `N/M mục bề mặt được phủ, K loại trừ` + danh sách chưa phủ | có | thay mọi con số artefact trơn |
| Out | một test hoặc gate trong dự án chạy lại `check` | có | đỏ khi bề mặt mọc thêm mục |

### Rules và capabilities
- RULE-01 (MUST): bề mặt lấy từ CODE bằng script tất định. Không lấy từ trí nhớ, README hay bản tóm tắt của model. Ghi commit lúc đọc.
- RULE-02 (MUST): mọi mục bề mặt có đúng một dòng sổ: `by[]` không rỗng, hoặc `exclude` kèm lý do người đọc kiểm lại được (vd "chuyển hướng sang /servers", "callback đóng cửa sổ OAuth"). Loại trừ không lý do tính là lỗi.
- RULE-03 (MUST): báo độ phủ dạng **"N/M mục bề mặt được phủ, K loại trừ"** và nêu nguồn bề mặt (script nào, commit nào). Chưa chạy diff thì nói "chưa đối chiếu với code", không nói "đủ rồi".
- RULE-04 (MUST): bước flow có `file:line` phải được kiểm máy trước khi gộp: file tồn tại, dòng nằm trong file, ký hiệu được nhắc xuất hiện gần dòng đó. Sai thì từ chối gộp. Một `file:line` sai trong sơ đồ dạy học còn tệ hơn là thiếu.
- RULE-05 (MUST): cổng đỏ khi có: mục không có dòng sổ, dòng sổ trỏ mục đã mất, loại trừ không lý do, sổ dựng ở commit khác bề mặt.
- RULE-06 (SHOULD): lấp chỗ trống bằng cách lần code (trang → route API → controller → service → adapter, mỗi bước `file:line`), không đoán. Nhiều mục thì chia theo mảng cho nhiều agent song song, mỗi agent nhận đúng danh sách mục của mình và schema đầu ra.
- Capabilities: đọc cây thư mục và git của sản phẩm; chạy script cục bộ; ghi 2 file JSON; thêm 1 test vào dự án.

### Failure boundaries
- Khung không có router theo file (Express đăng ký route bằng code, Go, Rails…) → `scan` chỉ ra được `module:` từ `--modules`. Phần route phải viết script riêng cho khung đó (vd grep `router.get(` / `app.post(`) rồi gộp vào `surface.json`. Khai rõ "bề mặt route lấy bằng script riêng".
- Không phải git repo → `commit: null`, kiểm lệch commit bị bỏ qua. Báo "không ghim được commit".
- Bề mặt quá lớn (hàng trăm mục) → **partial** hợp lệ nếu báo đúng `N/M` và liệt kê phần chưa phủ. Không được làm tròn thành "đủ".
- Không đọc được code (chỉ có site đang chạy) → dừng skill này; dùng `ui-kit-from-code` W01b (khám phá theo link) để lấy bề mặt UI.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | thư mục code | `python3 ~/.claude/harness/fdk/tools/surface-coverage.py scan <root> [--modules 'apps/api/src/modules/*'] --out surface.json` (trong repo framework: `fdk/tools/surface-coverage.py`) | `surface.json` + dòng `bề mặt M mục @commit · page … · api … · module …` | M = 0 → kiểm lại `<root>`/`--modules`, khung không file-based → nhánh B01 |
| W02 | judgment | `surface.json` + artefact hiện có | ghi `coverage.json`: mỗi mục → id artefact giải thích nó, hoặc `exclude` kèm lý do | sổ phủ | — |
| W03 | deterministic | 2 file JSON (+ `domain-graph.json`) | `surface-coverage.py check surface.json coverage.json [--flows domain-graph.json --root <root>]` | rc 0 + `N/M mục …` | rc 1 → W04 |
| W04 | judgment | danh sách CHƯA PHỦ + LỖI | lần code từng mục chưa phủ thành flow/bài mới (RULE-06); sửa `file:line` sai | artefact mới + sổ cập nhật | quay W03, tối đa 3 vòng rồi báo partial |
| W05 | effect | sổ xanh | thêm test hoặc bước CI trong dự án chạy lại W01 + W03 trước mỗi lần sinh lại artefact | gate | dự án không có test runner → ghi lệnh vào README của artefact |
| W06 | judgment | kết quả | báo theo RULE-03: `N/M`, K loại trừ kèm lý do, nguồn bề mặt @commit, danh sách còn thiếu (nếu partial) | báo cáo | — |

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | khung không có router theo file | viết script nhỏ liệt kê route của khung đó, ghi cùng định dạng `items` vào `surface.json` | khung file-based → skip | W02 |
| B02 | conditional_required | artefact là sổ chức năng CLI/MCP của chính app | bề mặt = route + lời gọi `/api` từ UI + tham số route; mỗi mục phải là một op của registry (mẫu `src/surface/manifest.ts` + `tests/manifest.test.ts` ở devops-agent) | — | W03 |

### Validation và stopping
Máy kiểm: `surface-coverage.py check` rc 0. Test của chính tool: `python3 -m pytest -q harness/tests/test_surface_coverage.py`. Thêm một trang giả vào fixture thì test phải đỏ với `CHƯA PHỦ page:/…`. Người kiểm: lý do của từng `exclude`. Tối đa 3 vòng W03↔W04, sau đó báo partial kèm danh sách còn thiếu.

### Examples
- **Positive:** Openship @4fefe217. `scan` ra 62 trang + 37 module. Sổ ban đầu chỉ từ 18 flow → `check` báo khoảng nửa bề mặt CHƯA PHỦ. 6 agent lần code theo mảng ra 81 flow mới, mỗi bước có `file:line`. Kiểm máy từng bước rồi gộp → `99 flow / 21 domain`, `check` báo `62/62 trang, 37/37 module` và có test `lessons-coverage` gác.
- **Boundary/failure:** user hỏi "19 bài đủ chưa" nhưng chưa có `surface.json` → câu trả lời đúng là "chưa đối chiếu với code", rồi chạy W01. Không được trả lời "đủ rồi" dựa trên số bài.
